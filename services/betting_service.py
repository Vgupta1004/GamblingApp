import random
from config.db import get_connection, get_cursor, close_all
from services.stake_service import StakeService
from model.bet import Bet
from exceptions.gambler import GamblerNotFound
from model.betting_session import BettingSession


class BettingService:

    @staticmethod
    def place_bet(gambler_id, amount, win_probability):

        conn = get_connection()
        cursor = get_cursor(conn)

        # get gambler
        cursor.execute("SELECT * FROM gamblers WHERE id=%s", (gambler_id,))
        g = cursor.fetchone()

        if not g:
            close_all(cursor, conn)
            raise GamblerNotFound()

        if amount > g["current_stake"]:
            raise Exception("Insufficient balance")

        stake_before = g["current_stake"]

        StakeService.place_bet(gambler_id, amount)

        is_win = BettingService.determine_outcome(win_probability)

        odds = 1 / win_probability if win_probability > 0 else 0

        win_amount = amount * odds if is_win else 0

        result = StakeService.settle_bet(gambler_id, win_amount, is_win)

        stake_after = result["balance"]

        bet_id = Bet.generate_id()

        cursor.execute("""
        INSERT INTO bets
        (id, gambler_id, amount, win_probability, odds, is_win,
         stake_before, stake_after)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            bet_id,
            gambler_id,
            amount,
            win_probability,
            odds,
            is_win,
            stake_before,
            stake_after
        ))

        conn.commit()
        close_all(cursor, conn)

        return {
            "bet_id": bet_id,
            "is_win": is_win,
            "win_amount": win_amount,
            "bet_amount": amount,
            "balance": stake_after
        }

    @staticmethod
    def determine_outcome(probability):
        return random.random() < probability
    

    @staticmethod
    def place_bet_with_strategy(gambler_id, strategy, win_probability):

        conn = get_connection()
        cursor = get_cursor(conn)

        cursor.execute("SELECT * FROM gamblers WHERE id=%s", (gambler_id,))
        g = cursor.fetchone()

        if not g:
            close_all(cursor, conn)
            raise GamblerNotFound()

        current_stake = g["current_stake"]

        amount = strategy.get_bet_amount(current_stake)

        close_all(cursor, conn)

        if amount > current_stake:
            raise Exception("Insufficient balance")

        result = BettingService.place_bet(
            gambler_id,
            amount,
            win_probability
        )

        if hasattr(strategy, "update_after_result"):
            strategy.update_after_result(result["is_win"])

        return result
    
    @staticmethod
    def place_consecutive_bets(gambler_id, strategy, num_bets, win_probability):

        session = BettingSession(gambler_id)

        for _ in range(num_bets):
            try:
                result = BettingService.place_bet_with_strategy(
                    gambler_id,
                    strategy,
                    win_probability
                )
                session.add_bet(result)

            except Exception as e:
                print("Session stopped:", str(e))
                break

        session.end_session()

        return session.get_summary()