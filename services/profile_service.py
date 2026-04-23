from config.db import get_connection, get_cursor, close_all
from exceptions.gambler import *
from dto.gambler_stats import GamblerStatistics


class ProfileService:

    # ✅ CREATE
    @staticmethod
    def create_gambler(name, initial_stake, win_threshold, loss_threshold,
                       min_bet=10, max_bet=1000, auto_play=False):

        if initial_stake <= 0:
            raise InvalidStake("Initial stake must be > 0")

        if win_threshold <= initial_stake:
            raise ThresholdError("Win threshold must be greater than initial stake")

        if loss_threshold >= initial_stake:
            raise ThresholdError("Loss threshold must be less than initial stake")

        conn = get_connection()
        cursor = get_cursor(conn)

        query = """
        INSERT INTO gamblers 
        (name, initial_stake, current_stake, win_threshold, loss_threshold,
         min_bet, max_bet, auto_play)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(query, (
            name,
            initial_stake,
            initial_stake,
            win_threshold,
            loss_threshold,
            min_bet,
            max_bet,
            auto_play
        ))

        conn.commit()
        gid = cursor.lastrowid

        close_all(cursor, conn)

        return {"message": "Gambler created", "id": gid}

    # ✅ UPDATE (FULL)
    @staticmethod
    def update_gambler(gambler_id, **kwargs):

        if not kwargs:
            return {"message": "Nothing to update"}

        conn = get_connection()
        cursor = get_cursor(conn)

        fields = []
        values = []

        for key, value in kwargs.items():
            fields.append(f"{key}=%s")
            values.append(value)

        values.append(gambler_id)

        query = f"UPDATE gamblers SET {', '.join(fields)} WHERE id=%s"

        cursor.execute(query, tuple(values))
        conn.commit()

        close_all(cursor, conn)

        return {"message": "Updated successfully"}

    # ✅ RETRIEVE (DTO)
    @staticmethod
    def get_gambler(gambler_id):

        conn = get_connection()
        cursor = get_cursor(conn)

        cursor.execute("SELECT * FROM gamblers WHERE id=%s", (gambler_id,))
        data = cursor.fetchone()

        close_all(cursor, conn)

        if not data:
            raise GamblerNotFound("Gambler not found")

        stats = GamblerStatistics(data)
        return stats.to_dict()

    # ✅ VALIDATE
    @staticmethod
    def validate_gambler(gambler_id):

        conn = get_connection()
        cursor = get_cursor(conn)

        cursor.execute("SELECT * FROM gamblers WHERE id=%s", (gambler_id,))
        g = cursor.fetchone()

        close_all(cursor, conn)

        if not g:
            raise GamblerNotFound()

        if g["current_stake"] <= g["loss_threshold"]:
            return {"status": "STOP_LOSS_REACHED"}

        if g["current_stake"] >= g["win_threshold"]:
            return {"status": "TARGET_REACHED"}

        return {"status": "ACTIVE"}

    # ✅ RESET (PROPER — proportional thresholds)
    @staticmethod
    def reset_gambler(gambler_id):

        conn = get_connection()
        cursor = get_cursor(conn)

        cursor.execute("SELECT * FROM gamblers WHERE id=%s", (gambler_id,))
        g = cursor.fetchone()

        if not g:
            close_all(cursor, conn)
            raise GamblerNotFound()

        initial = g["initial_stake"]

        # proportional thresholds (example logic)
        win_ratio = g["win_threshold"] / g["initial_stake"]
        loss_ratio = g["loss_threshold"] / g["initial_stake"]

        new_win = initial * win_ratio
        new_loss = initial * loss_ratio

        query = """
        UPDATE gamblers
        SET current_stake=%s,
            win_threshold=%s,
            loss_threshold=%s,
            total_bets=0,
            total_wins=0,
            total_losses=0
        WHERE id=%s
        """

        cursor.execute(query, (initial, new_win, new_loss, gambler_id))
        conn.commit()

        close_all(cursor, conn)

        return {"message": "Reset complete"}