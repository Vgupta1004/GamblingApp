class GameStatusDisplay:

    @staticmethod
    def display_current_status(gambler):

        print("\n====== CURRENT STATUS ======")
        print(f"Name: {gambler['name']}")
        print(f"Current Stake: {gambler['current_stake']}")
        print(f"Total Bets: {gambler['total_bets']}")
        print("============================\n")

    @staticmethod
    def display_game_outcome(result):

        print("\n------ GAME RESULT ------")
        print(f"Bet Amount: {result['bet_amount']}")
        print(f"Win: {result['is_win']}")
        print(f"Win Amount: {result['win_amount']}")
        print(f"New Balance: {result['balance']}")
        print("-------------------------\n")