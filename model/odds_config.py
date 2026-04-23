class OddsConfig:

    def __init__(self, odds_type="FIXED", value=2):
        self.odds_type = odds_type
        self.value = value

    def calculate_win(self, bet_amount, probability):

        if self.odds_type == "FIXED":
            return bet_amount * self.value

        elif self.odds_type == "PROBABILITY":
            return bet_amount * (1 / probability)

        elif self.odds_type == "DECIMAL":
            return bet_amount * self.value

        elif self.odds_type == "AMERICAN":

            if self.value > 0:
                return bet_amount * (self.value / 100)
            else:
                return bet_amount * (100 / abs(self.value))

        return bet_amount * 2