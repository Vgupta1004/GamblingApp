import json
from datetime import datetime
from model.gaming_session import GamingSession
from model.session_parameters import SessionParameters
from services.profile_service import ProfileService
from config.db import get_connection, get_cursor, close_all
from model.session import Session
from model.session_enums import SessionStatus, SessionEndReason
from strategies.fixed_strategy import FixedAmountStrategy
from strategies.percentage_strategy import PercentageStrategy
from strategies.martingale_strategy import MartingaleStrategy


class GameSessionManager:

    @staticmethod
    def start_new_session(gambler_id, upper, lower):

        # End any existing session for the gambler
        existing_session, _, _ = GameSessionManager.get_current_session(gambler_id)
        if existing_session:
            GameSessionManager.end_session(existing_session)

        gambler = ProfileService.get_gambler(gambler_id)

        params = SessionParameters(
            upper_limit=upper,
            lower_limit=lower
        )

        session_id = Session.generate_id()
        session = GamingSession(
            gambler_id,
            gambler["current_stake"],
            params,
            session_id=session_id
        )

        session.start()

        conn = get_connection()
        cursor = get_cursor(conn)
        query = """
        INSERT INTO sessions (id, gambler_id, status, initial_stake, current_stake, start_time, games_played, total_pause_time)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            session.session_id, session.gambler_id, session.status.value,
            session.initial_stake, session.current_stake, session.start_time,
            session.games_played, session.total_pause_time
        ))
        conn.commit()
        close_all(cursor, conn)

        return session

    @staticmethod
    def update_session(session, strategy=None, win_probability=None):
        conn = get_connection()
        cursor = get_cursor(conn)

        strategy_name = None
        strategy_details = None
        if strategy:
            strategy_name = strategy.__class__.__name__
            if isinstance(strategy, MartingaleStrategy):
                strategy_details = json.dumps({'base_amount': strategy.base_amount, 'current_amount': strategy.current_amount})
            elif isinstance(strategy, PercentageStrategy):
                strategy_details = json.dumps({'percentage': strategy.percentage})
            elif isinstance(strategy, FixedAmountStrategy):
                strategy_details = json.dumps({'fixed_amount': strategy.fixed_amount})

        query = """
        UPDATE sessions SET
            status = %s, end_reason = %s, current_stake = %s, end_time = %s,
            games_played = %s, total_pause_time = %s, strategy_name = %s,
            strategy_details = %s, win_probability = %s
        WHERE id = %s
        """
        cursor.execute(query, (
            session.status.value,
            session.end_reason.value if session.end_reason else None,
            session.current_stake,
            session.end_time,
            session.games_played,
            session.total_pause_time,
            strategy_name,
            strategy_details,
            win_probability,
            session.session_id
        ))
        conn.commit()
        close_all(cursor, conn)

    @staticmethod
    def get_current_session(gambler_id):
        conn = get_connection()
        cursor = get_cursor(conn)

        query = "SELECT * FROM sessions WHERE gambler_id = %s AND (status = 'ACTIVE' OR status = 'PAUSED')"
        cursor.execute(query, (gambler_id,))
        data = cursor.fetchone()
        close_all(cursor, conn)

        if not data:
            return None, None, None

        # Reconstruct session
        # Note: Session limits are not persisted in this version. They are reset upon loading.
        params = SessionParameters(upper_limit=float('inf'), lower_limit=float('-inf'))
        session = GamingSession(data['gambler_id'], data['initial_stake'], params, session_id=data['id'])
        
        # Repopulate state from DB
        session.status = SessionStatus(data['status'])
        session.end_reason = SessionEndReason(data['end_reason']) if data['end_reason'] else None
        session.current_stake = data['current_stake']
        session.start_time = data['start_time']
        session.end_time = data['end_time']
        session.games_played = data['games_played']
        session.total_pause_time = data['total_pause_time']

        # Reconstruct strategy
        strategy = None
        win_probability = data.get('win_probability')
        strategy_name = data.get('strategy_name')
        strategy_details = data.get('strategy_details')

        if strategy_name and strategy_details:
            details = json.loads(strategy_details)
            if strategy_name == 'MartingaleStrategy':
                strategy = MartingaleStrategy(details['base_amount'])
                strategy.current_amount = details['current_amount']
            elif strategy_name == 'PercentageStrategy':
                strategy = PercentageStrategy(details['percentage'])
            elif strategy_name == 'FixedAmountStrategy':
                strategy = FixedAmountStrategy(details['fixed_amount'])

        return session, strategy, win_probability

    @staticmethod
    def end_session(session):
        if not session:
            return None

        session.end_time = session.end_time or datetime.now()
        
        if session.status not in [SessionStatus.ENDED_WIN, SessionStatus.ENDED_LOSS, SessionStatus.ENDED_MANUAL]:
             session.status = SessionStatus.ENDED_MANUAL
             session.end_reason = SessionEndReason.MANUAL
        
        GameSessionManager.update_session(session)
        return session.get_summary()

    @staticmethod
    def get_all_sessions(gambler_id):
        conn = get_connection()
        cursor = get_cursor(conn)
        query = "SELECT * FROM sessions WHERE gambler_id = %s ORDER BY start_time DESC"
        cursor.execute(query, (gambler_id,))
        sessions_data = cursor.fetchall()
        close_all(cursor, conn)
        return sessions_data