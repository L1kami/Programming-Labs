from enum import Enum
from datetime import datetime


class AssetType(Enum):
    FUTURE = "Ф'ючерс"
    ASSET = "Акція"


class Asset:
    """Представляє один актив у портфелі."""

    def __init__(self, name: str, asset_type: AssetType, quantity: float, buy_price: float, leverage: float = 1.0):
        if not name or not name.strip():
            raise ValueError("Назва активу не може бути порожньою.")
        if quantity <= 0:
            raise ValueError(f"Кількість повинна бути > 0, отримано: {quantity}")
        if buy_price <= 0:
            raise ValueError(f"Ціна купівлі повинна бути > 0, отримано: {buy_price}")
        if leverage < 1.0:
            raise ValueError(f"Кредитне плече повинно бути >= 1.0, отримано: {leverage}")

        self.name = name
        self.asset_type = asset_type
        self.quantity = quantity
        self.buy_price = buy_price
        # Кредитне плече (актуально для ф'ючерсів)
        self.leverage = leverage if asset_type == AssetType.FUTURE else 1.0

        self.price_history: list[tuple[datetime, float]] = [
            (datetime.now(), buy_price)
        ]

    def update_price(self, new_price: float) -> None:
        if new_price <= 0:
            raise ValueError(f"Ціна повинна бути > 0, отримано: {new_price}")
        self.price_history.append((datetime.now(), new_price))

    def current_price(self) -> float:
        return self.price_history[-1][1]

    def profit_loss(self) -> float:
        """Прибуток/збиток з урахуванням кредитного плеча."""
        return (self.current_price() - self.buy_price) * self.quantity * self.leverage

    def profit_loss_percent(self) -> float:
        """Відсоток прибутку/збитку з урахуванням плеча."""
        return ((self.current_price() - self.buy_price) / self.buy_price) * 100 * self.leverage

    def is_monotonic_price(self) -> bool:
        prices = [price for _, price in self.price_history]
        if len(prices) <= 1: return True

        is_increasing = True
        is_decreasing = True

        for i in range(len(prices) - 1):
            if prices[i] > prices[i + 1]: is_increasing = False
            if prices[i] < prices[i + 1]: is_decreasing = False

        return is_increasing or is_decreasing

    def price_trend(self) -> str:
        prices = [price for _, price in self.price_history]
        if len(prices) <= 1: return "Без змін"
        if all(prices[i] <= prices[i + 1] for i in range(len(prices) - 1)):
            return "↑ Зростання"
        elif all(prices[i] >= prices[i + 1] for i in range(len(prices) - 1)):
            return "↓ Спадання"
        else:
            return "↕ Змішаний"

    def get_sparkline(self) -> str:
        """Генерує текстовий міні-графік історії цін."""
        prices = [price for _, price in self.price_history]
        if len(prices) <= 1: return "➖"

        bars = ' ▂▃▄▅▆▇█'
        min_p, max_p = min(prices), max(prices)
        if min_p == max_p: return bars[0] * len(prices)

        return ''.join(bars[int((p - min_p) / (max_p - min_p) * 7)] for p in prices)


class Portfolio:
    """Портфель активів брокера."""

    def __init__(self, owner: str):
        self.owner = owner
        self.assets: dict[str, Asset] = {}

    def add_asset(self, name: str, asset_type: AssetType, quantity: float, buy_price: float,
                  leverage: float = 1.0) -> None:
        if name in self.assets:
            raise ValueError(f"Актив '{name}' вже існує в портфелі.")
        self.assets[name] = Asset(name, asset_type, quantity, buy_price, leverage)

        lev_info = f" | Плече: x{leverage}" if asset_type == AssetType.FUTURE else ""
        print(f"[+] Додано: {name} ({asset_type.value}) | Кількість: {quantity} | Ціна: ${buy_price:.2f}{lev_info}")

    def remove_asset(self, name: str) -> None:
        if name not in self.assets:
            raise KeyError(f"Актив '{name}' не знайдено.")
        del self.assets[name]
        print(f"[-] Видалено: {name}")

    def update_price(self, name: str, new_price: float) -> None:
        if name not in self.assets:
            raise KeyError(f"Актив '{name}' не знайдено.")
        asset = self.assets[name]
        old_price = asset.current_price()
        asset.update_price(new_price)
        change = new_price - old_price
        sign = "+" if change >= 0 else ""
        print(f"[~] Оновлено {name}: ${old_price:.2f} → ${new_price:.2f} ({sign}{change:.2f})")

    def total_value(self) -> float:
        return sum(a.current_price() * a.quantity for a in self.assets.values())

    def total_invested(self) -> float:
        return sum(a.buy_price * a.quantity for a in self.assets.values())

    def total_profit_loss(self) -> float:
        return sum(a.profit_loss() for a in self.assets.values())

    def sell_partial(self, name: str, quantity: float) -> None:
        """Частково продає актив. Якщо залишок = 0 — видаляє з портфеля."""
        if name not in self.assets:
            raise KeyError(f"Актив '{name}' не знайдено.")
        if quantity <= 0:
            raise ValueError("Кількість для продажу повинна бути > 0.")
        asset = self.assets[name]
        if quantity > asset.quantity:
            raise ValueError(
                f"Неможливо продати {quantity} — в портфелі лише {asset.quantity}."
            )
        realized_pl = (asset.current_price() - asset.buy_price) * quantity * asset.leverage
        asset.quantity -= quantity
        sign = "+" if realized_pl >= 0 else ""
        print(
            f"[💰] Продано {quantity} x {name} @ ${asset.current_price():.2f} | "
            f"Реалізований П/З: {sign}${realized_pl:.2f}"
        )
        if asset.quantity == 0:
            del self.assets[name]
            print(f"[-] {name} повністю виведено з портфеля.")

    def best_asset(self) -> Asset | None:
        """Повертає найприбутковіший актив за %."""
        if not self.assets:
            return None
        return max(self.assets.values(), key=lambda a: a.profit_loss_percent())

    def worst_asset(self) -> Asset | None:
        """Повертає найзбитковіший актив за %."""
        if not self.assets:
            return None
        return min(self.assets.values(), key=lambda a: a.profit_loss_percent())

    def print_summary(self) -> None:
        """Виводить короткий підсумок: кращий та гірший актив."""
        best = self.best_asset()
        worst = self.worst_asset()
        print("\n   Топ активи:")
        if best:
            print(f"     Найкращий:  {best.name:<12} {best.profit_loss_percent():+.1f}%")
        if worst and worst.name != (best.name if best else None):
            print(f"     Найгірший:  {worst.name:<12} {worst.profit_loss_percent():+.1f}%")

    def print_report(self) -> None:
        separator = "=" * 90
        print(f"\n{separator}")
        print(f"  ПОРТФЕЛЬ БРОКЕРА: {self.owner}")
        print(separator)

        if not self.assets:
            print("  Портфель порожній.")
            print(separator)
            return

        print(
            f"  {'Актив':<10} {'Тип':<10} {'К-сть':<6} {'Куп.':<8} {'Пот.':<8} {'П/З $':<10} {'П/З %':<8} {'Графік':<12} {'Тренд'}")
        print(f"  {'-' * 10} {'-' * 10} {'-' * 6} {'-' * 8} {'-' * 8} {'-' * 10} {'-' * 8} {'-' * 12} {'-' * 12}")

        for asset in self.assets.values():
            pl = asset.profit_loss()
            pl_pct = asset.profit_loss_percent()
            pl_str = f"+${pl:.2f}" if pl >= 0 else f"-${abs(pl):.2f}"
            pl_pct_str = f"+{pl_pct:.1f}%" if pl_pct >= 0 else f"{pl_pct:.1f}%"
            type_str = f"{asset.asset_type.value} x{asset.leverage}" if asset.asset_type == AssetType.FUTURE else asset.asset_type.value

            print(
                f"  {asset.name:<10} "
                f"{type_str:<10} "
                f"{asset.quantity:<6.1f} "
                f"${asset.buy_price:<7.0f} "
                f"${asset.current_price():<7.0f} "
                f"{pl_str:<10} "
                f"{pl_pct_str:<8} "
                f"{asset.get_sparkline():<12} "
                f"{asset.price_trend()}"
            )

        print(separator)
        total_pl = self.total_profit_loss()
        total_invested = self.total_invested()
        total_pct = (total_pl / total_invested * 100) if total_invested != 0 else 0

        print(f"  Вкладено:       ${total_invested:.2f}")
        if total_pl >= 0:
            print(f"  РЕЗУЛЬТАТ:       ПРИБУТОК: +${total_pl:.2f} (+{total_pct:.1f}%)")
        else:
            print(f"  РЕЗУЛЬТАТ:       ЗБИТОК:   -${abs(total_pl):.2f} ({total_pct:.1f}%)")
        print(separator)

    def print_price_history(self, name: str) -> None:
        if name not in self.assets:
            raise KeyError(f"Актив '{name}' не знайдено.")
        asset = self.assets[name]
        print(f"\n  Історія цін: {name} ({asset.asset_type.value})")
        for timestamp, price in asset.price_history:
            print(f"  {timestamp.strftime('%H:%M:%S')} -> ${price:.2f}")