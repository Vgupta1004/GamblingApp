class StakeBoundary:

    def __init__(self, min_stake, max_stake):
        self.min_stake = min_stake
        self.max_stake = max_stake

        self.warning_low = min_stake * 1.2
        self.warning_high = max_stake * 0.8

    def validate(self, current_stake):

        if current_stake < self.min_stake:
            return "BREACH_LOW"

        if current_stake > self.max_stake:
            return "BREACH_HIGH"

        if current_stake <= self.warning_low:
            return "WARNING_LOW"

        if current_stake >= self.warning_high:
            return "WARNING_HIGH"

        return "SAFE"