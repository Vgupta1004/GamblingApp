from datetime import datetime
from model.session_enums import SessionStatus, SessionEndReason
from model.pause_record import PauseRecord
from model.game_record import GameRecord

class GamingSession:

    def __init__(self, gambler_id, initial_stake, params):

        self.gambler_id = gambler_id
        self.initial_stake = initial_stake
        self.current_stake = initial_stake

        self.params = params

        self.status = SessionStatus.INITIALIZED
        self.end_reason = None

        self.start_time = None
        self.end_time = None

        self.games_played = 0

        self.pause_records = []
        self.current_pause = None
        self.total_pause_time = 0

        self.game_records = []

    def start(self):
        self.status = SessionStatus.ACTIVE
        self.start_time = datetime.now()

    def update_after_game(self, new_stake):

        self.current_stake = new_stake
        self.games_played += 1

        if self.current_stake >= self.params.upper_limit:
            self.status = SessionStatus.ENDED_WIN
            self.end_reason = SessionEndReason.UPPER_LIMIT
            self.end_time = datetime.now()

        elif self.current_stake <= self.params.lower_limit:
            self.status = SessionStatus.ENDED_LOSS
            self.end_reason = SessionEndReason.LOWER_LIMIT
            self.end_time = datetime.now()

        elif self.games_played >= self.params.max_games:
            self.status = SessionStatus.ENDED_MANUAL
            self.end_reason = SessionEndReason.MANUAL
            self.end_time = datetime.now()

    def is_active(self):
        return self.status == SessionStatus.ACTIVE

    def get_summary(self):
        summary =  {
            "status": self.status.value,
            "end_reason": self.end_reason.value if self.end_reason else None,

            "games_played": self.games_played,
            "final_stake": self.current_stake,

            "total_profit": self.get_total_profit(),
            "win_rate": self.get_win_rate(),
            "avg_bet": self.get_avg_bet(),
            "roi": self.get_roi(),

            "total_duration": self.get_total_duration(),
            "pause_time": self.total_pause_time,
            "active_play_time": self.get_active_play_time(),

            "total_pauses": len(self.pause_records)
        }
        summary.update(self.get_advanced_stats())
        return summary
        
    def pause(self, reason="USER"):
        if self.status != SessionStatus.ACTIVE:
            raise Exception("Session not active")

        self.status = SessionStatus.PAUSED

        self.current_pause = PauseRecord(reason)
        self.pause_records.append(self.current_pause)

    def resume(self):
        if self.status != SessionStatus.PAUSED:
            raise Exception("Session not paused")

        self.current_pause.resume()

        self.total_pause_time += self.current_pause.get_duration()

        self.current_pause = None
        self.status = SessionStatus.ACTIVE

    def get_total_duration(self):
        if not self.end_time:
            return 0

        return (self.end_time - self.start_time).total_seconds()
    
    def get_active_play_time(self):
        return self.get_total_duration() - self.total_pause_time
    
    def record_game(self, bet_result):
        record = GameRecord(bet_result)
        self.game_records.append(record)

        self.current_stake = bet_result["balance"]
        self.games_played += 1

        # boundary checks
        if self.current_stake >= self.params.upper_limit:
            self.status = SessionStatus.ENDED_WIN
            self.end_reason = SessionEndReason.UPPER_LIMIT
            self.end_time = datetime.now()

        elif self.current_stake <= self.params.lower_limit:
            self.status = SessionStatus.ENDED_LOSS
            self.end_reason = SessionEndReason.LOWER_LIMIT
            self.end_time = datetime.now()

        elif self.games_played >= self.params.max_games:
            self.status = SessionStatus.ENDED_MANUAL
            self.end_reason = SessionEndReason.MANUAL
            self.end_time = datetime.now()

    def get_total_profit(self):
        return sum(r.get_profit() for r in self.game_records)


    def get_win_rate(self):
        if not self.game_records:
            return 0

        wins = sum(1 for r in self.game_records if r.is_win)
        return wins / len(self.game_records)


    def get_avg_bet(self):
        if not self.game_records:
            return 0

        return sum(r.bet_amount for r in self.game_records) / len(self.game_records)


    def get_roi(self):
        total_bet = sum(r.bet_amount for r in self.game_records)
        if total_bet == 0:
            return 0

        return self.get_total_profit() / total_bet
    
    def get_advanced_stats(self):
        profits = [r.profit for r in self.game_records]

        total_profit = sum(profits)

        max_drawdown = 0
        peak = self.game_records[0].balance if self.game_records else 0

        for r in self.game_records:

            if r.balance > peak:
                peak = r.balance

            drawdown = peak - r.balance
            max_drawdown = max(max_drawdown, drawdown)

        return {
            "total_profit": total_profit,
            "max_drawdown": max_drawdown
        }