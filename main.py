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


if __name__ == "__main__":

    TableCreator.create_table(Gambler)
    TableCreator.create_table(StakeTransaction)
    TableCreator.create_table(Bet)


    # res = ProfileService.create_gambler(
    #     name="Angelina",
    #     initial_stake=1000,
    #     win_threshold=2000,
    #     loss_threshold=500,
    #     min_bet=50,
    #     max_bet=500
    # )

    # gid = res["id"]
    # print(res)

    # print(ProfileService.update_gambler(gid, name="UpdatedName", max_bet=800))

    # print(ProfileService.get_gambler(gid))

    # print(ProfileService.validate_gambler(gid))

    # print(ProfileService.reset_gambler(gid))

    # StakeService.initialize_stake(gid)

    # print(StakeService.place_bet(gid, 100))

    # print(StakeService.settle_bet(gid, 200, True))

    # print(StakeService.place_bet(gid, 1000))

    # print(StakeService.settle_bet(gid, 0, False))

    # print(StakeService.get_stake_analysis())

    # # deposit
    # print(StakeService.deposit(gid, 500))

    # # withdraw
    # print(StakeService.withdraw(gid, 200))

    # # full report
    # report = StakeService.generate_report(gid)
    # print(report)

    # # filtered report

    # print(StakeService.generate_filtered_report(gid, "BET_WIN"))

    gid = 1
    ProfileService.reset_gambler(gid)
    # print(BettingService.place_bet(gid, 100, 0.5))
    # print(BettingService.place_bet(gid, 200, 0.3))
    # print(BettingService.place_bet(gid, 50, 0.7))

    # print("--- Individual Bets ---")
    # # Fixed strategy
    # fixed = FixedAmountStrategy(100)
    # print("1. Fixed:", BettingService.place_bet_with_strategy(gid, fixed, 0.5))

    # # Percentage strategy
    # percent = PercentageStrategy(0.1)
    # print("2. Percentage:", BettingService.place_bet_with_strategy(gid, percent, 0.5))

    # # Martingale strategy
    # martingale = MartingaleStrategy(50)
    # for i in range(3):
    #     print(f"{3+i}. Martingale:", BettingService.place_bet_with_strategy(gid, martingale, 0.5))

    # print("\n--- Starting 5 Consecutive Bets (Silently) ---")
    martingale = MartingaleStrategy(50)

    summary = BettingService.place_consecutive_bets(
        gid,
        martingale,
        num_bets=5,
        win_probability=0.5
    )

    print(summary)