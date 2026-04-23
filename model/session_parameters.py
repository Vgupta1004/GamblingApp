class SessionParameters:

    def __init__(
        self,
        upper_limit,
        lower_limit,
        max_games=100,
        default_probability=0.5
    ):
        self.upper_limit = upper_limit
        self.lower_limit = lower_limit
        self.max_games = max_games
        self.default_probability = default_probability