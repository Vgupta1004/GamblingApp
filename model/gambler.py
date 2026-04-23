class Gambler:

    TABLE_NAME = "gamblers"

    SCHEMA = {
        "id": "INT AUTO_INCREMENT PRIMARY KEY",
        "name": "VARCHAR(100)",
        "initial_stake": "FLOAT",
        "current_stake": "FLOAT",
        "win_threshold": "FLOAT",
        "loss_threshold": "FLOAT",

        "min_bet": "FLOAT",
        "max_bet": "FLOAT",
        "auto_play": "BOOLEAN",

        "total_bets": "INT DEFAULT 0",
        "total_wins": "INT DEFAULT 0",
        "total_losses": "INT DEFAULT 0",

        "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "updated_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"
    }

    def __init__(self, name, initial_stake, win_threshold, loss_threshold):
        self.name = name
        self.initial_stake = initial_stake
        self.current_stake = initial_stake
        self.win_threshold = win_threshold
        self.loss_threshold = loss_threshold