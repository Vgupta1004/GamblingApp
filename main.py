from services.table_creator import TableCreator
from model.gambler import Gambler
from services.profile_service import ProfileService

if __name__ == "__main__":

    TableCreator.create_table(Gambler)

    res = ProfileService.create_gambler(
        name="Angelina",
        initial_stake=1000,
        win_threshold=2000,
        loss_threshold=500,
        min_bet=50,
        max_bet=500
    )

    gid = res["id"]
    print(res)

    print(ProfileService.update_gambler(gid, name="UpdatedName", max_bet=800))

    print(ProfileService.get_gambler(gid))

    print(ProfileService.validate_gambler(gid))

    print(ProfileService.reset_gambler(gid))