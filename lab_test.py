import unittest
from lab2 import Asset, AssetType, Portfolio


class TestAsset(unittest.TestCase):

    def setUp(self):
        """Ініціалізація тестових активів перед кожним тестом."""
        # Звичайна акція (плече за замовчуванням 1.0)
        self.stock = Asset("AAPL", AssetType.ASSET, quantity=10, buy_price=150.0)
        # Ф'ючерс із кредитним плечем x10
        self.future = Asset("OIL-FUT", AssetType.FUTURE, quantity=5, buy_price=80.0, leverage=10.0)

    # --- Базові тести активу ---

    def test_initial_price(self):
        """Початкова ціна повинна дорівнювати ціні купівлі."""
        self.assertEqual(self.stock.current_price(), 150.0)

    def test_update_price(self):
        """Після оновлення ціни поточна ціна повинна змінитися."""
        self.stock.update_price(170.0)
        self.assertEqual(self.stock.current_price(), 170.0)

    def test_price_history_grows(self):
        """Кожне оновлення ціни додає запис в історію."""
        self.stock.update_price(160.0)
        self.stock.update_price(170.0)
        self.assertEqual(len(self.stock.price_history), 3)

    # --- Тести прибутку/збитку (Акції без плеча) ---

    def test_profit_when_price_rises(self):
        """При зростанні ціни маємо прибуток."""
        self.stock.update_price(200.0)
        self.assertAlmostEqual(self.stock.profit_loss(), 500.0)  # (200-150)*10

    def test_loss_when_price_falls(self):
        """При падінні ціни маємо збиток."""
        self.stock.update_price(100.0)
        self.assertAlmostEqual(self.stock.profit_loss(), -500.0)  # (100-150)*10

    def test_zero_profit_same_price(self):
        """При незмінній ціні прибуток/збиток = 0."""
        self.stock.update_price(150.0)
        self.assertAlmostEqual(self.stock.profit_loss(), 0.0)

    def test_profit_loss_percent_positive(self):
        """Перевірка відсоткового прибутку."""
        self.stock.update_price(165.0)
        self.assertAlmostEqual(self.stock.profit_loss_percent(), 10.0)

    def test_profit_loss_percent_negative(self):
        """Перевірка відсоткового збитку."""
        self.stock.update_price(135.0)
        self.assertAlmostEqual(self.stock.profit_loss_percent(), -10.0)

    # --- Тести монотонності та тренду ---

    def test_monotonic_increasing(self):
        self.stock.update_price(160.0)
        self.stock.update_price(170.0)
        self.stock.update_price(180.0)
        self.assertTrue(self.stock.is_monotonic_price())

    def test_not_monotonic_mixed(self):
        self.stock.update_price(160.0)
        self.stock.update_price(140.0)
        self.stock.update_price(170.0)
        self.assertFalse(self.stock.is_monotonic_price())

    def test_trend_rising(self):
        self.stock.update_price(160.0)
        self.stock.update_price(170.0)
        self.assertIn("Зростання", self.stock.price_trend())

    # --- Тести ф'ючерсу (з урахуванням КРЕДИТНОГО ПЛЕЧА) ---

    def test_future_profit_with_leverage(self):
        """Ф'ючерс: прибуток множиться на кредитне плече (x10)."""
        self.future.update_price(100.0)
        # Формула: (100 поточна - 80 покупка) * 5 кількість * 10 плече = 1000
        self.assertAlmostEqual(self.future.profit_loss(), 1000.0)

    def test_future_loss_with_leverage(self):
        """Ф'ючерс: збиток множиться на кредитне плече (x10)."""
        self.future.update_price(60.0)
        # Формула: (60 поточна - 80 покупка) * 5 кількість * 10 плече = -1000
        self.assertAlmostEqual(self.future.profit_loss(), -1000.0)


class TestPortfolio(unittest.TestCase):

    def setUp(self):
        """Ініціалізація тестового портфеля."""
        self.portfolio = Portfolio("Тестовий Брокер")

    def test_add_asset(self):
        """Додавання активу до портфеля."""
        self.portfolio.add_asset("AAPL", AssetType.ASSET, 10, 150.0)
        self.assertIn("AAPL", self.portfolio.assets)

    def test_add_duplicate_raises(self):
        """Додавання дублікату повинно кидати помилку."""
        self.portfolio.add_asset("AAPL", AssetType.ASSET, 10, 150.0)
        with self.assertRaises(ValueError):
            self.portfolio.add_asset("AAPL", AssetType.ASSET, 5, 160.0)

    def test_remove_asset(self):
        """Видалення активу з портфеля."""
        self.portfolio.add_asset("AAPL", AssetType.ASSET, 10, 150.0)
        self.portfolio.remove_asset("AAPL")
        self.assertNotIn("AAPL", self.portfolio.assets)

    def test_update_price(self):
        """Оновлення ціни активу в портфелі."""
        self.portfolio.add_asset("AAPL", AssetType.ASSET, 10, 150.0)
        self.portfolio.update_price("AAPL", 200.0)
        self.assertEqual(self.portfolio.assets["AAPL"].current_price(), 200.0)

    def test_total_invested(self):
        """Загальна сума вкладень (плече не впливає на суму вкладень)."""
        self.portfolio.add_asset("AAPL", AssetType.ASSET, 10, 150.0)  # 1500
        self.portfolio.add_asset("OIL", AssetType.FUTURE, 5, 80.0, leverage=10)  # 400
        self.assertAlmostEqual(self.portfolio.total_invested(), 1900.0)

    def test_total_profit_with_mixed_assets(self):
        """Загальний прибуток з урахуванням акцій та ф'ючерсів з плечем."""
        self.portfolio.add_asset("AAPL", AssetType.ASSET, 10, 150.0)  # Акція
        self.portfolio.add_asset("OIL", AssetType.FUTURE, 5, 80.0, leverage=10)  # Ф'ючерс х10

        self.portfolio.update_price("AAPL", 200.0)  # Прибуток: (200-150)*10 = 500
        self.portfolio.update_price("OIL", 100.0)  # Прибуток: (100-80)*5 * 10 = 1000

        # Разом має бути 1500
        self.assertAlmostEqual(self.portfolio.total_profit_loss(), 1500.0)

    def test_empty_portfolio_value(self):
        """Порожній портфель має нульову вартість."""
        self.assertAlmostEqual(self.portfolio.total_value(), 0.0)
        self.assertAlmostEqual(self.portfolio.total_profit_loss(), 0.0)

    def test_price_history_nonexistent_raises(self):
        """Запит історії для неіснуючого активу кидає помилку."""
        with self.assertRaises(KeyError):
            self.portfolio.print_price_history("NONEXISTENT")

    # --- Тести валідації ---

    def test_invalid_empty_name_raises(self):
        """Порожня назва активу повинна кидати помилку."""
        with self.assertRaises(ValueError):
            self.portfolio.add_asset("", AssetType.ASSET, 10, 150.0)

    def test_invalid_negative_quantity_raises(self):
        """Від'ємна кількість повинна кидати помилку."""
        with self.assertRaises(ValueError):
            self.portfolio.add_asset("AAPL", AssetType.ASSET, -5, 150.0)

    def test_invalid_zero_price_raises(self):
        """Нульова ціна купівлі повинна кидати помилку."""
        with self.assertRaises(ValueError):
            self.portfolio.add_asset("AAPL", AssetType.ASSET, 10, 0)

    def test_invalid_leverage_raises(self):
        """Плече менше 1.0 повинно кидати помилку."""
        with self.assertRaises(ValueError):
            self.portfolio.add_asset("OIL", AssetType.FUTURE, 5, 80.0, leverage=0.5)

    def test_update_price_negative_raises(self):
        """Оновлення ціни від'ємним значенням повинно кидати помилку."""
        self.portfolio.add_asset("AAPL", AssetType.ASSET, 10, 150.0)
        with self.assertRaises(ValueError):
            self.portfolio.update_price("AAPL", -10.0)

    # --- Тести часткового продажу ---

    def test_sell_partial_reduces_quantity(self):
        """Частковий продаж зменшує кількість активу."""
        self.portfolio.add_asset("AAPL", AssetType.ASSET, 10, 150.0)
        self.portfolio.sell_partial("AAPL", 3)
        self.assertAlmostEqual(self.portfolio.assets["AAPL"].quantity, 7.0)

    def test_sell_all_removes_asset(self):
        """Продаж всієї кількості видаляє актив з портфеля."""
        self.portfolio.add_asset("AAPL", AssetType.ASSET, 10, 150.0)
        self.portfolio.sell_partial("AAPL", 10)
        self.assertNotIn("AAPL", self.portfolio.assets)

    def test_sell_more_than_owned_raises(self):
        """Продаж більше ніж є в портфелі повинен кидати помилку."""
        self.portfolio.add_asset("AAPL", AssetType.ASSET, 10, 150.0)
        with self.assertRaises(ValueError):
            self.portfolio.sell_partial("AAPL", 99)

    def test_sell_nonexistent_raises(self):
        """Продаж неіснуючого активу повинен кидати помилку."""
        with self.assertRaises(KeyError):
            self.portfolio.sell_partial("NONEXISTENT", 5)

    # --- Тести best/worst ---

    def test_best_asset(self):
        """Повертає актив з найбільшим % прибутку."""
        self.portfolio.add_asset("AAPL", AssetType.ASSET, 10, 100.0)
        self.portfolio.add_asset("GOOGL", AssetType.ASSET, 5, 100.0)
        self.portfolio.update_price("AAPL", 150.0)   # +50%
        self.portfolio.update_price("GOOGL", 110.0)  # +10%
        self.assertEqual(self.portfolio.best_asset().name, "AAPL")

    def test_worst_asset(self):
        """Повертає актив з найбільшим % збитком."""
        self.portfolio.add_asset("AAPL", AssetType.ASSET, 10, 100.0)
        self.portfolio.add_asset("GOOGL", AssetType.ASSET, 5, 100.0)
        self.portfolio.update_price("AAPL", 90.0)   # -10%
        self.portfolio.update_price("GOOGL", 60.0)  # -40%
        self.assertEqual(self.portfolio.worst_asset().name, "GOOGL")

    def test_best_worst_empty_portfolio(self):
        """Порожній портфель повертає None для best/worst."""
        self.assertIsNone(self.portfolio.best_asset())
        self.assertIsNone(self.portfolio.worst_asset())


if __name__ == '__main__':
    unittest.main()