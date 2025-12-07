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

    beams = set()
    beams.add((start_row, start_col))

    splits = 0

    for current_row in range(start_row + 1, rows):
        new_beams = set()

        for beam_row, beam_col in beams:
            if grid[current_row][beam_col] == "^":
                splits += 1
                if beam_col > 0:
                    new_beams.add((current_row, beam_col - 1))
                if beam_col < cols - 1:
                    new_beams.add((current_row, beam_col + 1))
            else:
                new_beams.add((current_row, beam_col))

        beams = new_beams

    return splits


if __name__ == "__main__":
    main(day=DAY, part=1, code=code, example_or_real=ExampleOrReal.REAL)
