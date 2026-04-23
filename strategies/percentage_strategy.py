from strategies.base_strategy import BettingStrategy

class PercentageStrategy(BettingStrategy):

    def __init__(self, percentage):
        self.percentage = percentage

    def get_bet_amount(self, current_stake):
        return current_stake * self.percentage