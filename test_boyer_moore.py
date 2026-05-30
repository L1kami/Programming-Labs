import unittest
from boyer_moore import boyer_moore_search


class TestBoyerMooreSearch(unittest.TestCase):
    """
    Набір тестів для перевірки алгоритму пошуку підрядка Боєра-Мура.
    """

    def test_single_occurrence(self):
        """
        Перевіряє пошук підрядка, який зустрічається у тексті лише один раз.
        """
        self.assertEqual(boyer_moore_search("hello world", "world"), [6])

    def test_multiple_occurrences(self):
        """
        Перевіряє пошук підрядка, який зустрічається у тексті кілька разів.
        """
        self.assertEqual(boyer_moore_search("abracadabra", "abra"), [0, 7])

    def test_no_occurrence(self):
        """
        Перевіряє випадок, коли шуканий підрядок відсутній у тексті.
        """
        self.assertEqual(boyer_moore_search("hello world", "python"), [])

    def test_empty_needle(self):
        """
        Перевіряє поведінку алгоритму при порожньому шуканому рядку.
        """
        self.assertEqual(boyer_moore_search("hello", ""), [])

    def test_empty_haystack(self):
        """
        Перевіряє поведінку алгоритму при порожньому тексті для пошуку.
        """
        self.assertEqual(boyer_moore_search("", "hello"), [])

    def test_overlapping_occurrences(self):
        """
        Перевіряє пошук підрядків, які перекриваються один з одним у тексті.
        """
        self.assertEqual(boyer_moore_search("aaaaa", "aa"), [0, 1, 2, 3])

    def test_ukrainian_text(self):
        """
        Перевіряє коректність роботи алгоритму з кириличними символами.
        """
        self.assertEqual(boyer_moore_search("політехніка", "тех"), [4])


if __name__ == "__main__":
    unittest.main()