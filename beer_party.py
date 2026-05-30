def solve_beer_party(n, b, preferences_string):
    preferences_string = preferences_string.replace(" ", "").replace("\n", "").replace("\r", "")

    beer_masks = [0] * b
    for i in range(n):
        for j in range(b):
            if preferences_string[i * b + j] == 'Y':
                beer_masks[j] |= (1 << i)

    valid_beers = [(mask, j + 1) for j, mask in enumerate(beer_masks) if mask > 0]

    beers_covering_emp = [[] for _ in range(n)]
    for mask, beer_idx in valid_beers:
        for i in range(n):
            if mask & (1 << i):
                beers_covering_emp[i].append((mask, beer_idx))

    target = (1 << n) - 1
    min_beers_count = b + 1
    best_combinations = []

    def dfs(current_mask, current_path):
        nonlocal min_beers_count, best_combinations

        if current_mask == target:
            if len(current_path) < min_beers_count:
                min_beers_count = len(current_path)
                best_combinations = [current_path[:]]
            elif len(current_path) == min_beers_count:
                best_combinations.append(current_path[:])
            return

        if len(current_path) >= min_beers_count:
            return

        uncovered_bits = ~current_mask & target
        lowest_bit = uncovered_bits & -uncovered_bits
        uncovered_emp = lowest_bit.bit_length() - 1

        candidates = beers_covering_emp[uncovered_emp]

        def get_new_coverage(item):
            return bin(current_mask | item[0]).count('1')

        sorted_candidates = sorted(candidates, key=get_new_coverage, reverse=True)

        for b_mask, b_idx in sorted_candidates:
            if b_idx not in current_path:
                current_path.append(b_idx)
                dfs(current_mask | b_mask, current_path)
                current_path.pop()

    dfs(0, [])

    unique_combinations = list(set([tuple(sorted(combo)) for combo in best_combinations]))

    return min_beers_count, unique_combinations


def main():
    try:
        first_line = input("Введіть кількість працівників і видів пива (через пробіл): ").strip().split()
        if not first_line:
            return

        n = int(first_line[0])
        b = int(first_line[1])

        preferences = input("Введіть рядок вподобань (Y та N): ").strip()

        min_count, combinations = solve_beer_party(n, b, preferences)

        print(f"\nМінімальна кількість видів пива: {min_count}")
        print("Оптимальні варіанти закупки (номери видів пива):")

        for idx, combo in enumerate(combinations, 1):
            beers_str = ", ".join([f"Пиво №{beer_num}" for beer_num in combo])
            print(f"  Варіант {idx}: [{beers_str}]")

    except EOFError:
        pass
    except Exception as e:
        print(f"Помилка: {e}")


if __name__ == "__main__":
    main()