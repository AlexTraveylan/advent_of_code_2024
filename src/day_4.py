from utils import main

# ================================
# PART 1
# ================================

DIRECTIONS = [
    (0, 1),
    (1, 0),
    (1, 1),
    (-1, 1),
    (0, -1),
    (-1, 0),
    (-1, -1),
    (1, -1),
]


def find_xmas(grid: list[str]) -> int:
    rows = len(grid)
    cols = len(grid[0])
    count = 0

    def check_xmas(x: int, y: int, dx: int, dy: int) -> bool:
        if not (0 <= x + 3 * dx < rows and 0 <= y + 3 * dy < cols):
            return False
        word = ""
        for i in range(4):
            word += grid[x + i * dx][y + i * dy]
        return word == "XMAS"

    for i in range(rows):
        for j in range(cols):
            for dx, dy in DIRECTIONS:
                if check_xmas(i, j, dx, dy):
                    count += 1

    return count


def code(s: str):
    grid = s.strip().split("\n")
    return find_xmas(grid)


# ================================
# PART 2
# ================================


def find_xmas(grid: list[str]) -> int:
    rows = len(grid)
    cols = len(grid[0])
    count = 0

    def check_xmas(x: int, y: int) -> bool:
        is_A = grid[x][y] == "A"

        # 1ere diagonale
        is_MAS = grid[x - 1][y - 1] == "M" and grid[x + 1][y + 1] == "S"
        is_SAM = grid[x - 1][y - 1] == "S" and grid[x + 1][y + 1] == "M"

        is_diag1_ok = is_MAS or is_SAM

        # 2eme diagonale
        is_MAS = grid[x - 1][y + 1] == "M" and grid[x + 1][y - 1] == "S"
        is_SAM = grid[x - 1][y + 1] == "S" and grid[x + 1][y - 1] == "M"

        is_diag2_ok = is_MAS or is_SAM

        return is_A and is_diag1_ok and is_diag2_ok

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if check_xmas(i, j):
                count += 1

    return count


def code(s: str):
    grid = s.strip().split("\n")
    return find_xmas(grid)


if __name__ == "__main__":
    main(day=4, part=2, code=code)
