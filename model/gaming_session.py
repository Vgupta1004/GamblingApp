from datetime import datetime
from model.session_enums import SessionStatus, SessionEndReason


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
            "start_time": self.start_time,
            "end_time": self.end_time,
            "final_stake": self.current_stake
        }