from model.gaming_session import GamingSession
from model.session_parameters import SessionParameters
from services.profile_service import ProfileService


class GameSessionManager:

    active_sessions = {}

    @staticmethod
    def start_new_session(gambler_id, upper, lower):

        gambler = ProfileService.get_gambler(gambler_id)

        params = SessionParameters(
            upper_limit=upper,
            lower_limit=lower
        )

        session = GamingSession(
            gambler_id,
            gambler["current_stake"],
            params
        )

        session.start()

        GameSessionManager.active_sessions[gambler_id] = session

        return session

    @staticmethod
    def get_session(gambler_id):
        return GameSessionManager.active_sessions.get(gambler_id)

    @staticmethod
    def end_session(gambler_id):

        session = GameSessionManager.get_session(gambler_id)

        if session:
            session.end_time = session.end_time or session.start_time
            del GameSessionManager.active_sessions[gambler_id]

            return session.get_summary()