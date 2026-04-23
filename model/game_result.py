from datetime import datetime
class GameResult:
    def __init__(self, bet_amount, is_win, win_amount, stake_before, stake_after):

        self.bet_amount = bet_amount
        self.is_win = is_win
        self.win_amount = win_amount

        self.stake_before = stake_before
        self.stake_after = stake_after

        self.timestamp = datetime.now()

    def get_profit(self):
        return self.win_amount - self.bet_amount