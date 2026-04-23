from datetime import datetime

class BettingSession:

    def __init__(self, gambler_id):
        self.gambler_id = gambler_id
        self.start_time = datetime.now()
        self.end_time = None

        self.bets = []

    def add_bet(self, bet_result):
        self.bets.append(bet_result)

    def end_session(self):
        self.end_time = datetime.now()

    def get_summary(self):
        total_bets = len(self.bets)
        wins = sum(1 for b in self.bets if b["is_win"] == True)
        losses = total_bets - wins

        # Calculate profit as change in balance if bets exist
        if total_bets > 0:
            initial_balance = self.bets[0]["balance"] - (self.bets[0]["win_amount"] - self.bets[0]["bet_amount"])
            final_balance = self.bets[-1]["balance"]
            total_profit = final_balance - initial_balance
        else:
            total_profit = 0

        win_rate = wins / total_bets if total_bets > 0 else 0

        return {
            "total_bets": total_bets,
            "wins": wins,
            "losses": losses,
            "win_rate": win_rate,
            "total_profit": total_profit,
            "start_time": self.start_time,
            "end_time": self.end_time
        }