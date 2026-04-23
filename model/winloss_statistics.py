class WinLossStatistics:

    def __init__(self):

        self.total_games = 0

        self.wins = 0
        self.losses = 0
        self._results = []
        self.total_winnings = 0
        self.total_losses = 0

        self.current_win_streak = 0
        self.current_loss_streak = 0

        self.longest_win_streak = 0
        self.longest_loss_streak = 0

    def update(self, game_result):

        self.total_games += 1

        if game_result.is_win:
            self.wins += 1
            self.total_winnings += game_result.win_amount

            self.current_win_streak += 1
            self.current_loss_streak = 0

            self.longest_win_streak = max(
                self.longest_win_streak,
                self.current_win_streak
            )

        else:
            self.losses += 1
            self.total_losses += game_result.bet_amount

            self.current_loss_streak += 1
            self.current_win_streak = 0

            self.longest_loss_streak = max(
                self.longest_loss_streak,
                self.current_loss_streak
            )
        self._results.append(game_result)

    def get_win_rate(self):
        if self.total_games == 0:
            return 0
        return self.wins / self.total_games

    def get_profit_factor(self):
        if self.total_losses == 0:
            return float('inf')
        return self.total_winnings / self.total_losses

    def get_summary(self):
        return {
            "total_games": self.total_games,
            "wins": self.wins,
            "losses": self.losses,
            "win_rate": self.get_win_rate(),
            "profit_factor": self.get_profit_factor(),
            "longest_win_streak": self.longest_win_streak,
            "longest_loss_streak": self.longest_loss_streak,
            "net_profit": self.get_net_profit()
        }
    
    def get_net_profit(self):
        return sum(
            (r.win_amount - r.bet_amount)
            for r in self._results
        )