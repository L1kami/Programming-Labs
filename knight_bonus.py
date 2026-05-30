from collections import deque
from typing import Tuple, List, Optional


def find_knight_path(n: int, src: Tuple[int, int], dest: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    """
    Модифікований BFS: шукає не просто кількість кроків, а сам маршрут.
    Повертає список координат від старту до фінішу.
    """
    if src == dest:
        return [src]

    moves = [(2, -1), (2, 1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

    queue = deque([src])
    # Словник parent зберігає історію: {куди_стрибнули: звідки_стрибнули}
    parent = {src: None}

    while queue:
        curr_x, curr_y = queue.popleft()

        # Якщо дійшли до фінішу, зупиняємо пошук
        if (curr_x, curr_y) == dest:
            break

        for dx, dy in moves:
            nx, ny = curr_x + dx, curr_y + dy

            # Якщо клітинка в межах дошки і ми там ще не були
            if 0 <= nx < n and 0 <= ny < n and (nx, ny) not in parent:
                parent[(nx, ny)] = (curr_x, curr_y)  # Запам'ятовуємо, звідки прийшли
                queue.append((nx, ny))

    # Відновлення маршруту (йдемо від фінішу до старту по словнику parent)
    if dest not in parent:
        return None  # Шляху не існує

    path = []
    curr = dest
    while curr is not None:
        path.append(curr)
        curr = parent[curr]

    return path[::-1]  # Перевертаємо список, щоб вийшло від старту до фінішу


def visualize_board(n: int, path: List[Tuple[int, int]]):
    """
    Створює красиве текстове представлення шахівниці з маршрутом коня.
    """
    # Створюємо порожню дошку (заповнену крапками)
    board = [[' . ' for _ in range(n)] for _ in range(n)]

    # Позначаємо кроки на дошці
    for step_num, (x, y) in enumerate(path):
        if step_num == 0:
            board[x][y] = '[S]'  # Start
        elif step_num == len(path) - 1:
            board[x][y] = '[F]'  # Finish
        else:
            board[x][y] = f' {step_num} '  # Номер кроку

    # Друкуємо дошку
    print("\n" + "=" * 30)
    print("ВІЗУАЛІЗАЦІЯ МАРШРУТУ КОНЯ:")
    print("=" * 30)

    # Виводимо координати стовпців для зручності
    header = "   " + "".join([f" {i} " for i in range(n)])
    print(header)

    for i in range(n):
        row_str = f"{i} |" + "".join(board[i]) + "|"
        print(row_str)

    print("=" * 30)
    print(f"Легенда: [S] - Старт, [F] - Фініш, 1..N - кроки.")
    print(f"Загальна кількість кроків: {len(path) - 1}\n")


def main():
    # Тестові дані з методички
    n = 10
    src = (7, 0)
    dest = (0, 7)

    print("Запуск розширеного алгоритму BFS...")
    path = find_knight_path(n, src, dest)

    if path:
        visualize_board(n, path)
        print("Точна послідовність координат:")
        print(" -> ".join([f"({x},{y})" for x, y in path]))
    else:
        print("Шляху не існує!")


if __name__ == "__main__":
    main()