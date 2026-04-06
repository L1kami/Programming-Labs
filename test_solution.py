import unittest
from solution import solve


class TestSolve(unittest.TestCase):

    def test_example_1(self):
        self.assertEqual(solve(10, 2, 3), 9)

    def test_example_2(self):
        self.assertEqual(solve(2000000, 1000000000, 999999999), 1999999998)

    def test_example_3(self):
        self.assertEqual(solve(4, 1, 1), 2)

    def test_one_sheet_1x1(self):
        self.assertEqual(solve(1, 1, 1), 1)

    def test_one_large_sheet(self):
        self.assertEqual(solve(1, 109, 109), 109)

    def test_many_small_sheets(self):
        self.assertEqual(solve(1012, 1, 1), 32)

    def test_narrow_sheet(self):
        self.assertEqual(solve(1, 1, 109), 109)

    def test_four_sheets(self):
        self.assertEqual(solve(4, 3, 2), 6)


if __name__ == "__main__":
    unittest.main()
