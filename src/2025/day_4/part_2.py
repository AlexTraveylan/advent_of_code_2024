from src.utils import main

DAY = 4


def code(s: str):
    grid = [list(line) for line in s.strip().split("\n")]
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    total_removed = 0

    while True:
        accessible_positions = []

        for i in range(rows):
            for j in range(cols):
                if grid[i][j] != "@":
                    continue

                adjacent_rolls = 0
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if di == 0 and dj == 0:
                            continue
                        ni, nj = i + di, j + dj
                        if 0 <= ni < rows and 0 <= nj < cols:
                            if grid[ni][nj] == "@":
                                adjacent_rolls += 1

                if adjacent_rolls < 4:
                    accessible_positions.append((i, j))

        if not accessible_positions:
            break

        for i, j in accessible_positions:
            grid[i][j] = "."
            total_removed += 1

    return total_removed


if __name__ == "__main__":
    main(day=DAY, part=2, code=code)
