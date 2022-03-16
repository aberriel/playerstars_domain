from playerstars_domain.player.elo import Elo
from unittest import TestCase


class TestElo(TestCase):
    def test_elo_instance(self):
        elo = Elo()
        elo.set_ratings(1500, 1500)
        self.assertEqual(elo.k_factor, 16)
        self.assertEqual(elo.minimum_rating, 100)
        self.assertEqual(elo.winner_rating, 1500)
        self.assertEqual(elo.loser_rating, 1500)
        self.assertEqual(elo.winner_expected_score, 0.5)
        self.assertEqual(elo.loser_expected_score, 0.5)

    def test_elo_instance2(self):
        elo = Elo()
        elo.set_ratings(1500, 1510)
        self.assertAlmostEqual(elo.winner_expected_score, 0.4856, 3)
        self.assertAlmostEqual(elo.loser_expected_score, 0.5143, 3)

    def test_elo_q(self):
        self.assertAlmostEqual(Elo._q(1500), 5623.413, 3)

    def test_update_ratings(self):
        elo = Elo()
        elo.set_ratings(1500, 1510)
        elo.update_ratings()

        self.assertAlmostEqual(elo.winner_rating, 1508.2301, 3)
        self.assertAlmostEqual(elo.loser_rating, 1501.7698, 3)

    def test_properties(self):
        elo = Elo()
        elo.set_ratings(1500, 1510)
        elo.update_ratings()

        self.assertEqual(elo.wr, elo.winner_rating)
        self.assertEqual(elo.lr, elo.loser_rating)
        self.assertEqual(elo.les, elo.loser_expected_score)
        self.assertEqual(elo.wes, elo.winner_expected_score)
