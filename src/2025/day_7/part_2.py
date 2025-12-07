import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))))


from src.utils import ExampleOrReal, main

DAY = 7


def code(s: str) -> int:
    lines = s.strip().split("\n")
    grid = [list(line) for line in lines]
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Trouver la position de S
    start_row = -1
    start_col = -1
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == "S":
                start_row = i
                start_col = j
                break
        if start_row != -1:
            break

    if start_row == -1:
        return 0

    timelines = {}
    timelines[(start_row, start_col)] = 1

    for current_row in range(start_row + 1, rows):
        new_timelines = {}

        for (prev_row, prev_col), count in timelines.items():
            if grid[current_row][prev_col] == "^":
                if prev_col > 0:
                    pos_left = (current_row, prev_col - 1)
                    new_timelines[pos_left] = new_timelines.get(pos_left, 0) + count
                if prev_col < cols - 1:
                    pos_right = (current_row, prev_col + 1)
                    new_timelines[pos_right] = new_timelines.get(pos_right, 0) + count
            else:
                pos_continue = (current_row, prev_col)
                new_timelines[pos_continue] = new_timelines.get(pos_continue, 0) + count

        timelines = new_timelines

    return sum(timelines.values())


if __name__ == "__main__":
    main(day=DAY, part=2, code=code, example_or_real=ExampleOrReal.REAL)
