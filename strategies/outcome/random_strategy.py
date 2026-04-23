import random
class RandomOutcomeStrategy:
    def determine_outcome(self, probability):
        return random.random() < probability