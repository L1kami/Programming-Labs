import unittest
import tempfile
import os
from telecom_network import calculate_minimum_cable_length


class TestTelecomNetwork(unittest.TestCase):
    """
    Клас для юніт-тестування функції calculate_minimum_cable_length.
    Використовує тимчасові файли для імітації вхідних CSV-даних без
    необхідності створювати реальні файли на диску вручну.
    """

    def create_temp_csv(self, data: str) -> str:
        """
        Допоміжний метод. Створює тимчасовий CSV-файл із заданими текстовими
        даними та повертає шлях до нього.
        """
        fd, path = tempfile.mkstemp(suffix='.csv')
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(data)
        return path

    def test_connected_graph(self):
        """
        Тестує сценарій, коли всі колодязі можуть бути успішно з'єднані.
        У цьому прикладі оптимальний шлях: K2-K3 (1500), K3-K4 (1000) та K1-K2 (2000).
        Очікувана сума: 4500.
        """
        csv_data = "K1, K2, 2000\nK2, K3, 1500\nK1, K3, 3000\nK3, K4, 1000\n"
        temp_path = self.create_temp_csv(csv_data)

        try:
            result = calculate_minimum_cable_length(temp_path)
            self.assertEqual(result, 4500)
        finally:
            os.remove(temp_path)

    def test_disconnected_graph(self):
        """
        Тестує сценарій, коли існують ізольовані групи колодязів.
        Оскільки групи (K1, K2) та (K3, K4) не мають зв'язку між собою,
        очікуваний результат -1.
        """
        csv_data = "K1, K2, 2000\nK3, K4, 1500\n"
        temp_path = self.create_temp_csv(csv_data)

        try:
            result = calculate_minimum_cable_length(temp_path)
            self.assertEqual(result, -1)
        finally:
            os.remove(temp_path)

    def test_single_connection(self):
        """
        Тестує мінімальний граф, що складається лише з двох колодязів
        і одного зв'язку між ними.
        """
        csv_data = "A, B, 500\n"
        temp_path = self.create_temp_csv(csv_data)

        try:
            result = calculate_minimum_cable_length(temp_path)
            self.assertEqual(result, 500)
        finally:
            os.remove(temp_path)


if __name__ == '__main__':
    unittest.main()