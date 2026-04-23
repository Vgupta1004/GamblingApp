from datetime import datetime
from model.session_enums import SessionStatus, SessionEndReason
from model.pause_record import PauseRecord

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
        return {
            "status": self.status.value,
            "end_reason": self.end_reason.value if self.end_reason else None,
            "games_played": self.games_played,
            "final_stake": self.current_stake,

            "total_duration": self.get_total_duration(),
            "pause_time": self.total_pause_time,
            "active_play_time": self.get_active_play_time(),

            "total_pauses": len(self.pause_records)
        }
    
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