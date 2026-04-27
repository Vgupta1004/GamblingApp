from services.profile_service import ProfileService
from services.stake_service import StakeService
from model.session_enums import SessionStatus
from services.session_manager import GameSessionManager
from services.betting_service import BettingService
from utils.safe_input_handler import SafeInputHandler
from strategies.fixed_strategy import FixedAmountStrategy
from strategies.percentage_strategy import PercentageStrategy
from strategies.martingale_strategy import MartingaleStrategy


class InteractiveMenu:

    def __init__(self):
        self.gambler_id = None
        self.session = None
        self.strategy = None
        self.probability = None


    def display_main_menu(self):
        print("\n====== MAIN MENU ======")
        print("1. View Profile")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Start Session")
        print("5. Place Single Bet")
        if self.session and self.session.status == SessionStatus.PAUSED:
            print("6. Resume Session")
        else:
            print("6. Play Full Session")
        print("7. Show Session Summary")
        print("8. Exit")
        print("=======================\n")


    def create_gambler(self):

        name = input("Enter name: ")

        initial_stake = SafeInputHandler.get_valid_stake()
        win_threshold = SafeInputHandler.get_valid_number("Enter win threshold: ", "win_threshold")
        loss_threshold = SafeInputHandler.get_valid_number("Enter loss threshold: ", "loss_threshold")
        min_bet = SafeInputHandler.get_valid_number("Enter min bet: ", "min_bet")
        max_bet = SafeInputHandler.get_valid_number("Enter max bet: ", "max_bet")

        res = ProfileService.create_gambler(
            name=name,
            initial_stake=initial_stake,
            win_threshold=win_threshold,
            loss_threshold=loss_threshold,
            min_bet=min_bet,
            max_bet=max_bet
        )

        self.gambler_id = res["id"]
        print("Gambler created with ID:", self.gambler_id)


    def view_profile(self):

        if not self.gambler_id:
            print("Create gambler first!")
            return

        data = ProfileService.get_gambler(self.gambler_id)

        print("\n--- PROFILE ---")
        for k, v in data.items():
            print(f"{k}: {v}")
        print("---------------\n")


    def start_session(self):

        if not self.gambler_id:
            print("Create gambler first!")
            return
        
        if self.session and self.session.is_active():
            print("A session is already active. End it before starting a new one.")
            return

        upper = SafeInputHandler.get_valid_number("Enter upper limit: ", "upper")
        lower = SafeInputHandler.get_valid_number("Enter lower limit: ", "lower")

        self.session = GameSessionManager.start_new_session(
            self.gambler_id,
            upper,
            lower
        )
        self.strategy = None
        self.probability = None

        print(" Session started!")

    def choose_strategy(self):
        print("\n--- SELECT STRATEGY ---")
        print("1. Fixed Amount - Bet a fixed amount each time")
        print("2. Percentage   - Bet a % of your current stake")
        print("3. Martingale   - Double bet after each loss")
        print("----------------------\n")
        
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == "1":
            amount = SafeInputHandler.get_valid_number("Enter fixed bet amount: ", "bet")
            return FixedAmountStrategy(amount)
        
        elif choice == "2":
            print("Enter percentage (e.g., 10 for 10%, 0.1 for 10%)")
            pct = SafeInputHandler.get_valid_number("Enter percentage: ", "percentage")
            if pct > 1:
                pct = pct / 100
            return PercentageStrategy(pct)
        
        elif choice == "3":
            base = SafeInputHandler.get_valid_number("Enter base bet amount: ", "bet")
            return MartingaleStrategy(base)
        
        else:
            print("Invalid choice, using Fixed Amount (100)")
            return FixedAmountStrategy(100)

    
    def place_single_bet(self):

        if not self.gambler_id:
            print(" Create gambler first!")
            return

        prob = SafeInputHandler.get_valid_probability()
        strategy = self.choose_strategy()

        result = BettingService.place_bet_with_strategy(
            self.gambler_id,
            strategy,
            prob
        )

        print("\n RESULT")
        print(result)


    def play_session(self):

        if not self.session:
            print(" Start session first!")
            return
        
        if self.session.status == SessionStatus.PAUSED:
            self.session.resume()
            print("\n--- Session Resumed ---")

        if not self.strategy or not self.probability:
            self.probability = SafeInputHandler.get_valid_probability()
            self.strategy = self.choose_strategy()

        print(f"\n Playing with: {self.strategy.__class__.__name__}")

        while self.session.is_active():

            result = BettingService.place_bet_with_strategy(
                self.gambler_id,
                self.strategy,
                self.probability
            )

            self.session.record_game(result)
            GameSessionManager.update_session(self.session, self.strategy, self.probability)

            print(result)

            action = input("Press Enter for next bet, or type 'pause' to return to menu: ").strip().lower()
            if action == 'pause':
                self.session.pause("USER_PAUSE")
                GameSessionManager.update_session(self.session, self.strategy, self.probability)
                print("\nSession paused.")
                return

        print(" Session ended!")


    def show_summary(self):

        if not self.session:
            print(" No session found!")
            return

        # If session is not ended, get a live summary
        if self.session.status in [SessionStatus.ACTIVE, SessionStatus.PAUSED, SessionStatus.INITIALIZED]:
             summary = self.session.get_summary()
        else: # otherwise, it's ended, get final summary
            summary = GameSessionManager.end_session(self.session)


        print("\n SESSION SUMMARY")
        for k, v in summary.items():
            print(f"{k}: {v}")


    def run(self):
        self.entry_menu()
        while True:
            self.display_main_menu()
            choice = input("Enter choice: ")

            if choice == "1":
                self.view_profile()

            elif choice == "2":
                self.deposit()

            elif choice == "3":
                self.withdraw()

            elif choice == "4":
                self.start_session()

            elif choice == "5":
                self.place_single_bet()

            elif choice == "6":
                self.play_session()

            elif choice == "7":
                self.show_summary()

            elif choice == "8":
                print(" Exiting...")
                break

            else:
                print("Invalid choice")

    def deposit(self):
        if not self.gambler_id:
            print("Create or login to a gambler profile first!")
            return
        amount = SafeInputHandler.get_valid_number("Enter deposit amount: ", "deposit_amount")
        if amount <= 0:
            print("Deposit amount must be positive.")
            return
        try:
            result = StakeService.deposit(self.gambler_id, amount)
            print(f"Deposit successful. New balance: {result['balance']}")
        except Exception as e:
            print(f"Error during deposit: {e}")

    def withdraw(self):
        if not self.gambler_id:
            print("Create or login to a gambler profile first!")
            return
        amount = SafeInputHandler.get_valid_number("Enter withdrawal amount: ", "withdrawal_amount")
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return
        try:
            result = StakeService.withdraw(self.gambler_id, amount)
            print(f"Withdrawal successful. New balance: {result['balance']}")
        except Exception as e:
            print(f"Error during withdrawal: {e}")

    def entry_menu(self):
        while True:
            print("\n====== WELCOME ======")
            print("1. Login")
            print("2. Create New Gambler")
            print("3. Exit")
            print("=====================\n")
            choice = input("Enter choice: ")

            if choice == "1":
                self.login()
                if self.gambler_id:
                    break

            elif choice == "2":
                self.create_gambler()
                break

            elif choice == "3":
                exit()

            else:
                print("Invalid choice")

    def login(self):
        try:
            gid = int(input("Enter Gambler ID: "))

            data = ProfileService.get_gambler(gid)

            if not data:
                print("Gambler not found")
                return

            self.gambler_id = gid
            print(f"Logged in as {data['name']}")
            
            # Load any existing session
            self.session, self.strategy, self.probability = GameSessionManager.get_current_session(self.gambler_id)
            if self.session:
                print(f"Loaded an existing session (Status: {self.session.status.value})")

        except Exception:
            print("Invalid ID")