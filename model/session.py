import uuid

class Session:

    TABLE_NAME = "sessions"

    SCHEMA = {
        "id": "VARCHAR(50) PRIMARY KEY",
        "gambler_id": "INT",
        "status": "VARCHAR(50)",
        "end_reason": "VARCHAR(50)",
        "initial_stake": "FLOAT",
        "current_stake": "FLOAT",
        "start_time": "TIMESTAMP",
        "end_time": "TIMESTAMP NULL",
        "games_played": "INT",
        "total_pause_time": "FLOAT",
        "strategy_name": "VARCHAR(50)",
        "strategy_details": "TEXT",
        "win_probability": "FLOAT"
    }

    @staticmethod
    def generate_id():
        return str(uuid.uuid4())