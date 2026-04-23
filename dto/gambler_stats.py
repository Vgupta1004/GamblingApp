class GamblerStatistics:

    def __init__(self, data):
        self.name = data["name"]
        self.current_stake = data["current_stake"]
        self.total_bets = data["total_bets"]
        self.total_wins = data["total_wins"]
        self.total_losses = data["total_losses"]

        self.net_profit = data["current_stake"] - data["initial_stake"]

        self.win_rate = (
            self.total_wins / self.total_bets
            if self.total_bets > 0 else 0
        )

        self.avg_bet = (
            data["initial_stake"] / self.total_bets
            if self.total_bets > 0 else 0
        )

    def to_dict(self):
        return self.__dict__