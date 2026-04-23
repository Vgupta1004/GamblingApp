import random
from config.db import get_connection, get_cursor, close_all
from services.stake_service import StakeService
from model.bet import Bet
from exceptions.gambler import GamblerNotFound


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
            "balance": stake_after
        }

    @staticmethod
    def determine_outcome(probability):
        return random.random() < probability