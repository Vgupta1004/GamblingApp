from strategies.fixed_strategy import FixedAmountStrategy
from services.betting_service import BettingService


class SimpleGameEngine:

    def __init__(self, gambler_id):
        self.gambler_id = gambler_id
        self.strategy = FixedAmountStrategy(100)

    def play_one_round(self):

        result = BettingService.place_bet_with_strategy(
            self.gambler_id,
            self.strategy,
            0.5
        )

        return result