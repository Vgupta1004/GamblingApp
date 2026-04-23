from services.table_creator import TableCreator
from model.gambler import Gambler
from services.profile_service import ProfileService
from model.stake_transaction import StakeTransaction
from services.stake_service import StakeService
from model.bet import Bet
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
    print(BettingService.place_bet(gid, 100, 0.5))
    print(BettingService.place_bet(gid, 200, 0.3))
    print(BettingService.place_bet(gid, 50, 0.7))