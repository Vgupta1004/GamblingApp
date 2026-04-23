from services.table_creator import TableCreator
from model.gambler import Gambler
from services.profile_service import ProfileService
from model.stake_transaction import StakeTransaction
from services.stake_service import StakeService
from model.bet import Bet
from services.betting_service import BettingService
from services.betting_service import BettingService
from strategies.fixed_strategy import FixedAmountStrategy
from strategies.percentage_strategy import PercentageStrategy
from strategies.martingale_strategy import MartingaleStrategy
from strategies.martingale_strategy import MartingaleStrategy
from services.betting_service import BettingService
from services.session_manager import GameSessionManager
from strategies.fixed_strategy import FixedAmountStrategy
from services.betting_service import BettingService
from strategies.outcome.random_strategy import RandomOutcomeStrategy
from model.odds_config import OddsConfig
from services.winloss_service import WinLossCalculator
from strategies.outcome.random_strategy import RandomOutcomeStrategy
from model.odds_config import OddsConfig
from services.winloss_service import WinLossCalculator


if __name__ == "__main__":

    TableCreator.create_table(Gambler)
    TableCreator.create_table(StakeTransaction)
    TableCreator.create_table(Bet)

    gid = 1
    ProfileService.reset_gambler(gid)

    strategy = RandomOutcomeStrategy()
    odds = OddsConfig("FIXED", 2)

    result = WinLossCalculator.run_session(
        initial_stake=1000,
        bet_amount=100,
        rounds=10,
        strategy=strategy,
        odds=odds,
        probability=0.5
    )

    print(result)
    