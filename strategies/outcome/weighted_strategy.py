import random
class WeightedOutcomeStrategy:
    def __init__(self, house_edge=0.05):
        self.house_edge = house_edge

    def determine_outcome(self, probability):
        adjusted_prob = probability * (1 - self.house_edge)
        return random.random() < adjusted_prob