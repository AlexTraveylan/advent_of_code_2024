import os
import sys
from collections import deque

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))))

from src.utils import ExampleOrReal, main

DAY = 9


def get_line_tiles(start: tuple[int, int], end: tuple[int, int]) -> set[tuple[int, int]]:
    x1, y1 = start
    x2, y2 = end
    tiles = set()

    if x1 == x2:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            tiles.add((x1, y))
    elif y1 == y2:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            tiles.add((x, y1))

    return tiles


def flood_fill_exterior(
    valid_tiles: set[tuple[int, int]], min_x: int, max_x: int, min_y: int, max_y: int
) -> set[tuple[int, int]]:
    exterior = set()
    visited = set()
    queue: deque[tuple[int, int]] = deque()

    for y in [min_y, max_y]:
        for x in range(min_x, max_x + 1):
            pos = (x, y)
            if pos not in valid_tiles and pos not in visited:
                queue.append(pos)
                visited.add(pos)
                exterior.add(pos)

    for x in [min_x, max_x]:
        for y in range(min_y, max_y + 1):
            pos = (x, y)
            if pos not in valid_tiles and pos not in visited:
                queue.append(pos)
                visited.add(pos)
                exterior.add(pos)

    while queue:
        x, y = queue.popleft()

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            pos = (nx, ny)
            if min_x <= nx <= max_x and min_y <= ny <= max_y and pos not in valid_tiles and pos not in visited:
                visited.add(pos)
                exterior.add(pos)
                queue.append(pos)

    interior = set()
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            pos = (x, y)
            if pos not in valid_tiles and pos not in exterior:
                interior.add(pos)

    return valid_tiles | interior


def code(s: str) -> int:
    red_tiles = []
    for line in s.strip().split("\n"):
        if line.strip():
            x, y = map(int, line.split(","))
            red_tiles.append((x, y))

    if not red_tiles:
        return 0

    min_x = min(x for x, y in red_tiles)
    max_x = max(x for x, y in red_tiles)
    min_y = min(y for x, y in red_tiles)
    max_y = max(y for x, y in red_tiles)

    valid_tiles = set()

    for x, y in red_tiles:
        valid_tiles.add((x, y))

    for i in range(len(red_tiles)):
        start = red_tiles[i]
        end = red_tiles[(i + 1) % len(red_tiles)]
        line_tiles = get_line_tiles(start, end)
        valid_tiles.update(line_tiles)

    valid_tiles = flood_fill_exterior(valid_tiles, min_x, max_x, min_y, max_y)

    def is_rect_valid(min_x_rect, max_x_rect, min_y_rect, max_y_rect):
        for y in range(min_y_rect, max_y_rect + 1):
            for x in range(min_x_rect, max_x_rect + 1):
                if (x, y) not in valid_tiles:
                    return False
        return True

    max_area = 0
    n_red = len(red_tiles)

    pairs_with_area = [
        ((abs(red_tiles[j][0] - red_tiles[i][0]) + 1) * (abs(red_tiles[j][1] - red_tiles[i][1]) + 1), i, j)
        for i in range(n_red)
        for j in range(i + 1, n_red)
    ]

    pairs_with_area.sort(reverse=True)

    for area, i, j in pairs_with_area:
        if area <= max_area:
            break

        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[j]

        min_x_rect = min(x1, x2)
        max_x_rect = max(x1, x2)
        min_y_rect = min(y1, y2)
        max_y_rect = max(y1, y2)

        if is_rect_valid(min_x_rect, max_x_rect, min_y_rect, max_y_rect):
            max_area = area

    return max_area


if __name__ == "__main__":
    main(day=DAY, part=2, code=code, example_or_real=ExampleOrReal.REAL)
