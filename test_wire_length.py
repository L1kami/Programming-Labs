import unittest
from wire_length import get_max_wire_length


class TestWireLength(unittest.TestCase):
    """
    Набір юніт-тестів для перевірки правильності обчислення максимальної довжини дроту.
    """

    def test_example_1(self):
        """
        Перевіряє базовий випадок з трьома однаковими максимальними висотами.
        Очікуваний результат: ~5.66.
        """
        result = get_max_wire_length(2, [3, 3, 3])
        self.assertAlmostEqual(result, 5.66, places=2)

    def test_example_2_all_equal(self):
        """
        Перевіряє випадок, коли всі опори мають максимальну висоту 1.
        Очікуваний результат: рівно відстань між опорами помножена на кількість проміжків.
        """
        result = get_max_wire_length(100, [1, 1, 1, 1])
        self.assertEqual(result, 300.00)

    def test_example_3_alternating(self):
        """
        Перевіряє випадок з опорами, де вигідно чергувати мінімальну та максимальну висоти.
        Очікуваний результат: 396.32.
        """
        result = get_max_wire_length(4, [100, 2, 100, 2, 100])
        self.assertEqual(result, 396.32)

    def test_example_4_large_dataset(self):
        """
        Перевіряє великий набір даних (50 опор) з різноманітними максимальними висотами.
        Очікуваний результат: 2738.18.
        """
        heights = [
            56, 18, 17, 94, 23, 7, 21, 94, 29, 54, 44, 26, 86, 79, 4, 15, 5, 91, 25, 17,
            88, 66, 28, 2, 95, 97, 60, 93, 40, 70, 75, 48, 38, 51, 34, 52, 87, 8, 62, 77,
            35, 52, 3, 93, 34, 57, 51, 11, 39, 72
        ]
        result = get_max_wire_length(4, heights)
        self.assertEqual(result, 2738.18)


if __name__ == '__main__':
    unittest.main()