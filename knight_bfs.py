from collections import deque
from typing import Tuple


def min_knight_moves(n: int, src: Tuple[int, int], dest: Tuple[int, int]) -> int:
    """
    Знаходить мінімальну кількість ходів коня від src до dest на дошці N x N.
    Повертає -1, якщо шлях неможливий.
    """
    if src == dest:
        return 0

    moves = [(2, -1), (2, 1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

    queue = deque([(src[0], src[1], 0)])
    visited = {src}

    while queue:
        x, y, dist = queue.popleft()

        if (x, y) == dest:
            return dist

        for dx, dy in moves:
            nx, ny = x + dx, y + dy

            if 0 <= nx < n and 0 <= ny < n and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny, dist + 1))

    return -1


def solve_from_file(input_file: str = 'input.txt', output_file: str = 'output.txt') -> None:
    """
    Зчитує дані з файлу, викликає алгоритм BFS та записує результат у файл.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

            n = int(lines[0].split('#')[0].strip())
            src_str = lines[1].split('#')[0].strip().split(',')
            dest_str = lines[2].split('#')[0].strip().split(',')

            src = (int(src_str[0]), int(src_str[1]))
            dest = (int(dest_str[0]), int(dest_str[1]))

        result = min_knight_moves(n, src, dest)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(str(result) + '\n')

    except Exception as e:
        print(f"Помилка обробки файлів: {e}")

    result = min_knight_moves(n, src, dest)

    print(f"Успіх! Знайдено найкоротший шлях: {result}. Відповідь записана у файл output.txt")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(str(result) + '\n')


if __name__ == "__main__":
    solve_from_file()