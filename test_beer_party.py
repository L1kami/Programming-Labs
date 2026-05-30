import unittest
from beer_party import solve_beer_party

class TestBeerParty(unittest.TestCase):

    def test_example_1(self):
        n, b = 2, 2
        prefs = "YNNY"
        min_count, _ = solve_beer_party(n, b, prefs)
        self.assertEqual(min_count, 2)

    def test_example_2(self):
        n, b = 6, 3
        prefs = "YNNYNYYNYNYYNYYNYN"
        min_count, _ = solve_beer_party(n, b, prefs)
        self.assertEqual(min_count, 2)

    def test_everyone_likes_same_beer(self):
        n, b = 3, 3
        prefs = "YNNYNNYNN"
        min_count, _ = solve_beer_party(n, b, prefs)
        self.assertEqual(min_count, 1)

    def test_disjoint_preferences(self):
        n, b = 4, 4
        prefs = "YNNNNYNNNNYNNNNY"
        min_count, _ = solve_beer_party(n, b, prefs)
        self.assertEqual(min_count, 4)

    def test_all_like_all(self):
        n, b = 5, 4
        prefs = "Y" * 20
        min_count, _ = solve_beer_party(n, b, prefs)
        self.assertEqual(min_count, 1)

if __name__ == "__main__":
    unittest.main()