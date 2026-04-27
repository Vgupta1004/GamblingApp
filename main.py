from ui.interactive_menu import InteractiveMenu
from services.table_creator import TableCreator
from model.gambler import Gambler
from model.stake_transaction import StakeTransaction
from model.bet import Bet
from model.session import Session


if __name__ == "__main__":

    TableCreator.create_table(Gambler)
    TableCreator.create_table(StakeTransaction)
    TableCreator.create_table(Bet)
    TableCreator.create_table(Session)

    app = InteractiveMenu()
    app.run()