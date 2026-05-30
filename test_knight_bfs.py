import unittest
from knight_bfs import min_knight_moves


class TestKnightBFS(unittest.TestCase):

    def test_provided_example(self):
        """Тест на основі прикладу з методички (N=8, (7,0) -> (0,7) = 6)"""
        self.assertEqual(min_knight_moves(8, (7, 0), (0, 7)), 6)

    def test_same_position(self):
        """Тест, коли початкова і кінцева точки збігаються"""
        self.assertEqual(min_knight_moves(8, (3, 3), (3, 3)), 0)

    def test_one_move(self):
        """Тест досяжності за 1 хід"""
        self.assertEqual(min_knight_moves(8, (0, 0), (2, 1)), 1)
        self.assertEqual(min_knight_moves(8, (4, 4), (5, 6)), 1)

    def test_impossible_move(self):
        """
        Тест для неможливого шляху.
        На дошці 3х3 кінь з кута (0,0) ніколи не потрапить у центр (1,1).
        """
        self.assertEqual(min_knight_moves(3, (0, 0), (1, 1)), -1)


if __name__ == '__main__':
    unittest.main()