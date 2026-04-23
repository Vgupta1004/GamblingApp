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


if __name__ == "__main__":

    TableCreator.create_table(Gambler)
    TableCreator.create_table(StakeTransaction)
    TableCreator.create_table(Bet)

    gid = 1
    ProfileService.reset_gambler(gid)

    session = GameSessionManager.start_new_session(gid, 1500, 500)

    strategy = FixedAmountStrategy(100)

    while session.is_active():

        result = BettingService.place_bet_with_strategy(gid, strategy, 0.5)

        session.record_game(result)

    summary = session.get_summary()

    print(summary)
    