import uuid

class Bet:

    TABLE_NAME = "bets"

    SCHEMA = {
        "id": "VARCHAR(50) PRIMARY KEY",
        "gambler_id": "INT",
        "amount": "FLOAT",
        "win_probability": "FLOAT",
        "odds": "FLOAT",
        "is_win": "BOOLEAN",
        "stake_before": "FLOAT",
        "stake_after": "FLOAT",
        "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    }

    @staticmethod
    def generate_id():
        return str(uuid.uuid4())