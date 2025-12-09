import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))))


from src.utils import ExampleOrReal, main

DAY = 9


def code(s: str) -> int:
    red_tiles = []
    for line in s.strip().split("\n"):
        if line.strip():
            x, y = map(int, line.split(","))
            red_tiles.append((x, y))

    max_area = 0

    for i in range(len(red_tiles)):
        x1, y1 = red_tiles[i]
        for j in range(i + 1, len(red_tiles)):
            x2, y2 = red_tiles[j]

            area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            max_area = max(max_area, area)

    return max_area


if __name__ == "__main__":
    main(day=DAY, part=1, code=code, example_or_real=ExampleOrReal.REAL)
