from datetime import datetime

class GameRecord:

    def __init__(self, bet_result):

        self.bet_id = bet_result["bet_id"]
        self.bet_amount = bet_result["bet_amount"]
        self.win_amount = bet_result["win_amount"]
        self.is_win = bet_result["is_win"]
        self.balance = bet_result["balance"]
        self.profit = self.win_amount - self.bet_amount

        self.timestamp = datetime.now()

    def get_profit(self):
        return self.win_amount - self.bet_amount