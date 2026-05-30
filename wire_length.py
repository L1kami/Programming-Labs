import math


def get_max_wire_length(w: int, heights: list[int]) -> float:
    """
    Обчислює максимально можливу необхідну довжину дроту для з'єднання електроопор.

    Алгоритм використовує динамічне програмування для знаходження найгіршого випадку
    (максимальної довжини дроту). Оскільки функція відстані є опуклою, максимальна
    відстань завжди досягається, коли висота опори є або мінімальною (1),
    або максимальною (heights[i]).

    Аргументи:
        w (int): Відстань між сусідніми електроопорами.
        heights (list[int]): Список максимальних можливих висот для кожної опори.

    Повертає:
        float: Максимально можлива необхідна довжина дроту з точністю до 2 знаків після коми.
    """
    n = len(heights)
    if n <= 1:
        return 0.0

    dp = [[0.0, 0.0] for _ in range(n)]

    for i in range(1, n):
        h_prev = heights[i - 1]
        h_curr = heights[i]

        d_1_1 = math.sqrt(w ** 2 + (1 - 1) ** 2)
        d_prevH_1 = math.sqrt(w ** 2 + (h_prev - 1) ** 2)
        d_1_currH = math.sqrt(w ** 2 + (1 - h_curr) ** 2)
        d_prevH_currH = math.sqrt(w ** 2 + (h_prev - h_curr) ** 2)

        dp[i][0] = max(dp[i - 1][0] + d_1_1, dp[i - 1][1] + d_prevH_1)
        dp[i][1] = max(dp[i - 1][0] + d_1_currH, dp[i - 1][1] + d_prevH_currH)

    max_length = max(dp[n - 1][0], dp[n - 1][1])

    return float(f"{max_length:.2f}")