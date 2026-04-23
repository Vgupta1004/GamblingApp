class StakeTransaction:

    TABLE_NAME = "stake_transactions"

    SCHEMA = {
        "id": "INT AUTO_INCREMENT PRIMARY KEY",
        "gambler_id": "INT",
        "transaction_type": "VARCHAR(50)",
        "amount": "FLOAT",
        "balance_after": "FLOAT",
        "reference_id": "INT",  # bet id (future use)
        "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    }