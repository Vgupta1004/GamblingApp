class RunningTotals:

    def __init__(self, initial_stake):
        self.initial_stake = initial_stake
        self.current_stake = initial_stake

        self.balance_history = [initial_stake]

        self.total_profit = 0

    def update(self, game_result):

        profit = game_result.get_profit()

        self.total_profit += profit
        self.current_stake = game_result.stake_after

        self.balance_history.append(self.current_stake)

    def get_net_profit(self):
        return self.current_stake - self.initial_stake
    
    def get_max_drawdown(self):
        peak = self.balance_history[0]
        max_drawdown = 0

        for value in self.balance_history:

            if value > peak:
                peak = value

            drawdown = (peak - value)

            if drawdown > max_drawdown:
                max_drawdown = drawdown

        return max_drawdown