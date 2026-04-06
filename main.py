from lab2 import Portfolio, AssetType


def main():
    # Створюємо портфель
    portfolio = Portfolio("Іван Петренко")

    print("\n СИСТЕМА УПРАВЛІННЯ ПОРТФЕЛЕМ БРОКЕРА")
    print("=" * 70)

    # Додаємо активи
    print("\n[1] Додаємо активи до портфеля...")
    portfolio.add_asset("AAPL", AssetType.ASSET, quantity=10, buy_price=150.00)
    portfolio.add_asset("GOOGL", AssetType.ASSET, quantity=5, buy_price=2800.00)

    # ОСЬ ТУТ МИ ДОДАЛИ КРЕДИТНЕ ПЛЕЧЕ ДЛЯ Ф'ЮЧЕРСІВ:
    portfolio.add_asset("OIL-FUT", AssetType.FUTURE, quantity=20, buy_price=75.00, leverage=5.0)  # Плече x5
    portfolio.add_asset("GOLD-FUT", AssetType.FUTURE, quantity=3, buy_price=1900.00, leverage=10.0)  # Плече x10

    # Початковий звіт
    portfolio.print_report()

    # Симулюємо зміни цін
    print("\n[2] Симулюємо зміни ринку...")
    portfolio.update_price("AAPL", 180.00)  # +30
    portfolio.update_price("AAPL", 195.00)  # +15
    portfolio.update_price("GOOGL", 2600.00)  # -200
    portfolio.update_price("OIL-FUT", 90.00)  # +15
    portfolio.update_price("OIL-FUT", 70.00)  # -20 (змішаний тренд)
    portfolio.update_price("GOLD-FUT", 2100.00)  # +200

    # Звіт після змін
    portfolio.print_report()

    # Показуємо історію цін для одного активу
    print()
    portfolio.print_price_history("OIL-FUT")
    portfolio.print_price_history("AAPL")

    # Видаляємо актив
    print("\n[3] Частково продаємо OIL-FUT (10 з 20)...")
    portfolio.sell_partial("OIL-FUT", 10)

    print("\n[4] Повністю продаємо GOOGL...")
    portfolio.remove_asset("GOOGL")

    # Фінальний звіт з підсумком
    portfolio.print_report()
    portfolio.print_summary()


if __name__ == '__main__':
    main()