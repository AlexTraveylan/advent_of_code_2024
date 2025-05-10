from typing import Literal

from tqdm import tqdm

from utils import main

# ================================
# PART 1
# ================================

DIRECTIONS = [
    (-1, 0),  # up
    (0, 1),  # right
    (1, 0),  # down
    (0, -1),  # left
]


def find_guard(grid: list[str]) -> tuple[int, int]:
    for i, line in enumerate(grid):
        if "^" in line:
            return i, line.index("^")


def next_dir(dir: tuple[int, int]) -> tuple[int, int]:
    return DIRECTIONS[(DIRECTIONS.index(dir) + 1) % 4]


def run_a_step(
    grid: list[str], pos: tuple[int, int], dir: tuple[int, int]
) -> tuple[int, int] | Literal["end", "turn"]:
    new_pos = (pos[0] + dir[0], pos[1] + dir[1])

    if (
        new_pos[0] < 0
        or new_pos[0] >= len(grid)
        or new_pos[1] < 0
        or new_pos[1] >= len(grid[0])
    ):
        return "end"

    if grid[new_pos[0]][new_pos[1]] in (".", "^"):
        return new_pos

    return "turn"


def code(s: str):
    # Your code here

    grid = [case for case in s.split("\n")]

    init_i, init_j = find_guard(grid)
    init_dir = DIRECTIONS[0]

    step = {
        (init_i, init_j),
    }
    while True:
        result = run_a_step(grid, (init_i, init_j), init_dir)
        if result == "end":
            break
        elif result == "turn":
            init_dir = next_dir(init_dir)
        else:
            init_i, init_j = result
            step.add((init_i, init_j))
    return len(step)


# ================================
# PART 2
# ================================


def code(s: str):
    # Your code here

    init_grid = [case for case in s.split("\n")]

    init_i, init_j = find_guard(init_grid)
    init_dir = DIRECTIONS[0]

    nb_cycle = 0
    for x, line in tqdm(enumerate(init_grid)):
        for y, case in enumerate(line):
            if case in ("#", "^"):
                continue

            grid = [list(line) for line in init_grid]
            grid[x][y] = "#"

            step = {(init_i, init_j): {init_dir}}
            i = init_i
            j = init_j
            dir = init_dir
            while True:
                result = run_a_step(grid, (i, j), dir)
                if result == "end":
                    break
                elif result == "turn":
                    dir = next_dir(dir)
                else:
                    i, j = result
                    if dir in step.get((i, j), set()):
                        nb_cycle += 1
                        break
                    step[(i, j)] = step.get((i, j), set()) | {dir}

    return nb_cycle


if __name__ == "__main__":
    main(day=6, part=2, code=code)
