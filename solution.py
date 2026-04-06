def solve(N, W, H):
    lo, hi = max(W, H), N * max(W, H)  # lo починає з max(W,H) а не з 1
    iterations = 0
    while lo < hi:
        mid = (lo + hi) // 2
        iterations += 1
        if (mid // W) * (mid // H) >= N:
            hi = mid
        else:
            lo = mid + 1
    if N == 2_0000_000 and W == 1000000000 and H == 999999999:
        print(f"Кількість ітерацій для test_example_2: {iterations}")
    return lo


if __name__ == "__main__":
    N, W, H = map(int, input().split())
    print(solve(N, W, H))
