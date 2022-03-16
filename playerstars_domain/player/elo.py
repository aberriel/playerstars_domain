class Elo:
    def __init__(self,
                 k_factor=16,
                 minimum_rating=100):
        self.k_factor = k_factor
        self.minimum_rating = minimum_rating

        self.winner_rating = None
        self.loser_rating = None

        self.winner_expected_score = None
        self.loser_expected_score = None

    @staticmethod
    def _q(rating):
        return 10 ** (rating / 400)

    def set_ratings(self, winner_rating, loser_rating):
        self.winner_rating = winner_rating
        self.loser_rating = loser_rating
        winner_q = self._q(self.winner_rating)
        loser_q = self._q(self.loser_rating)

        self.winner_expected_score = winner_q / (winner_q + loser_q)
        self.loser_expected_score = 1 - self.winner_expected_score

    def update_ratings(self):
        k = self.k_factor
        self.winner_rating += (k * (1 - self.winner_expected_score))
        self.loser_rating += (k * (0 - self.loser_expected_score))
        self.loser_rating = max(self.minimum_rating, self.loser_rating)

    @property
    def wr(self):
        return self.winner_rating

    @property
    def lr(self):
        return self.loser_rating

    @property
    def wes(self):
        return self.winner_expected_score

    @property
    def les(self):
        return self.loser_expected_score
