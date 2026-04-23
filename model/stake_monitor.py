class StakeMonitor:

    def __init__(self):
        self.history = []
        self.peak = 0
        self.low = float("inf")

    def update(self, balance):

        self.history.append(balance)

        if balance > self.peak:
            self.peak = balance

        if balance < self.low:
            self.low = balance

    def get_summary(self):

        if len(self.history) < 2:
            volatility = 0
        else:
            changes = [
                abs(self.history[i] - self.history[i - 1])
                for i in range(1, len(self.history))
            ]
            volatility = sum(changes) / len(changes)

        return {
            "peak": self.peak,
            "lowest": self.low,
            "volatility": volatility
        }