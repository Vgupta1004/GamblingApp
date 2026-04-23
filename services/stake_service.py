from config.db import get_connection, get_cursor, close_all
from enums.transaction_type import TransactionType
from exceptions.gambler import GamblerNotFound
from model.stake_monitor import StakeMonitor
from model.stake_boundary import StakeBoundary

monitor = StakeMonitor()
boundary = StakeBoundary(min_stake=200, max_stake=5000)


class StakeService:

    @staticmethod
    def initialize_stake(gambler_id):

        conn = get_connection()
        cursor = get_cursor(conn)

        cursor.execute("SELECT * FROM gamblers WHERE id=%s", (gambler_id,))
        g = cursor.fetchone()

        if not g:
            close_all(cursor, conn)
            raise GamblerNotFound()

        StakeService._create_transaction(
            cursor,
            gambler_id,
            TransactionType.INITIAL_STAKE,
            g["initial_stake"],
            g["current_stake"]
        )

        conn.commit()
        close_all(cursor, conn)

        return {"message": "Stake initialized"}

    @staticmethod
    def place_bet(gambler_id, amount):

        conn = get_connection()
        cursor = get_cursor(conn)

        cursor.execute("SELECT * FROM gamblers WHERE id=%s", (gambler_id,))
        g = cursor.fetchone()

        if not g:
            close_all(cursor, conn)
            raise GamblerNotFound()

        if amount > g["current_stake"]:
            raise Exception("Insufficient balance")

        new_balance = g["current_stake"] - amount

        cursor.execute(
            "UPDATE gamblers SET current_stake=%s, total_bets=total_bets+1 WHERE id=%s",
            (new_balance, gambler_id)
        )

        StakeService._create_transaction(
            cursor,
            gambler_id,
            TransactionType.BET_PLACED,
            -amount,
            new_balance
        )

        conn.commit()
        close_all(cursor, conn)

        monitor.update(new_balance)

        status = boundary.validate(new_balance)

        return {
            "balance": new_balance,
            "boundary_status": status
        }

    @staticmethod
    def settle_bet(gambler_id, amount, is_win):

        conn = get_connection()
        cursor = get_cursor(conn)

        cursor.execute("SELECT * FROM gamblers WHERE id=%s", (gambler_id,))
        g = cursor.fetchone()

        if not g:
            close_all(cursor, conn)
            raise GamblerNotFound()

        if is_win:
            new_balance = g["current_stake"] + amount

            cursor.execute(
                "UPDATE gamblers SET current_stake=%s, total_wins=total_wins+1 WHERE id=%s",
                (new_balance, gambler_id)
            )

            t_type = TransactionType.BET_WIN

        else:
            new_balance = g["current_stake"]

            cursor.execute(
                "UPDATE gamblers SET total_losses=total_losses+1 WHERE id=%s",
                (gambler_id,)
            )

            t_type = TransactionType.BET_LOSS

        StakeService._create_transaction(
            cursor,
            gambler_id,
            t_type,
            amount if is_win else 0,
            new_balance
        )

        conn.commit()
        close_all(cursor, conn)

        monitor.update(new_balance)

        status = boundary.validate(new_balance)

        return {
            "balance": new_balance,
            "boundary_status": status
        }


    @staticmethod
    def _create_transaction(cursor, gambler_id, t_type, amount, balance):

        query = """
        INSERT INTO stake_transactions
        (gambler_id, transaction_type, amount, balance_after)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(query, (
            gambler_id,
            t_type.value,
            amount,
            balance
        ))

    @staticmethod
    def get_stake_analysis():
        return monitor.get_summary()