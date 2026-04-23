class BettingPreferences:
    def __init__(self, min_bet=10, max_bet=1000, auto_play=False):
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.auto_play = auto_play