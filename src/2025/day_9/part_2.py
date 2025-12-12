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

    if len(red_tiles) < 2:
        return 0

    n = len(red_tiles)

    xs = sorted(set(x for x, y in red_tiles))
    ys = sorted(set(y for x, y in red_tiles))

    segments = []
    for i in range(n):
        segments.append((red_tiles[i], red_tiles[(i + 1) % n]))

    def is_inside_or_on_border(px, py):
        for (x1, y1), (x2, y2) in segments:
            if x1 == x2:
                if px == x1 and min(y1, y2) <= py <= max(y1, y2):
                    return True
            else:
                if py == y1 and min(x1, x2) <= px <= max(x1, x2):
                    return True

        crossings = 0
        for (x1, y1), (x2, y2) in segments:
            if x1 == x2:
                if px < x1 and min(y1, y2) < py <= max(y1, y2):
                    crossings += 1
        return crossings % 2 == 1

    def make_zones(coords):
        zones = []
        sizes = []

        zones.append((coords[0], coords[0]))
        sizes.append(1)

        for i in range(1, len(coords)):
            if coords[i] > coords[i - 1] + 1:
                zones.append((coords[i - 1] + 1, coords[i] - 1))
                sizes.append(coords[i] - 1 - (coords[i - 1] + 1) + 1)

            zones.append((coords[i], coords[i]))
            sizes.append(1)

        return zones, sizes

    x_zones, _x_sizes = make_zones(xs)
    y_zones, _y_sizes = make_zones(ys)

    num_x_zones = len(x_zones)
    num_y_zones = len(y_zones)

    valid = [[False] * num_y_zones for _ in range(num_x_zones)]

    for i, (x_start, x_end) in enumerate(x_zones):
        px = (x_start + x_end) // 2
        for j, (y_start, y_end) in enumerate(y_zones):
            py = (y_start + y_end) // 2
            valid[i][j] = is_inside_or_on_border(px, py)

    prefix_count = [[0] * (num_y_zones + 1) for _ in range(num_x_zones + 1)]
    for i in range(num_x_zones):
        for j in range(num_y_zones):
            prefix_count[i + 1][j + 1] = (
                (1 if valid[i][j] else 0) + prefix_count[i][j + 1] + prefix_count[i + 1][j] - prefix_count[i][j]
            )

    def count_valid_zones(xi1, xi2, yj1, yj2):
        return (
            prefix_count[xi2 + 1][yj2 + 1]
            - prefix_count[xi1][yj2 + 1]
            - prefix_count[xi2 + 1][yj1]
            + prefix_count[xi1][yj1]
        )

    coord_to_zone_x = {}
    coord_to_zone_y = {}
    for i, (x_start, x_end) in enumerate(x_zones):
        if x_start == x_end:
            coord_to_zone_x[x_start] = i

    for j, (y_start, y_end) in enumerate(y_zones):
        if y_start == y_end:
            coord_to_zone_y[y_start] = j

    max_area = 0

    red_zone_indices = [(coord_to_zone_x[x], coord_to_zone_y[y]) for x, y in red_tiles]

    pairs = []
    for a in range(n):
        x1, y1 = red_tiles[a]
        for b in range(a + 1, n):
            x2, y2 = red_tiles[b]
            area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            pairs.append((area, a, b))

    pairs.sort(reverse=True)

    for area, a, b in pairs:
        if area <= max_area:
            break

        xi1, yj1 = red_zone_indices[a]
        xi2, yj2 = red_zone_indices[b]

        min_xi, max_xi = min(xi1, xi2), max(xi1, xi2)
        min_yj, max_yj = min(yj1, yj2), max(yj1, yj2)

        total_zones = (max_xi - min_xi + 1) * (max_yj - min_yj + 1)

        valid_count = count_valid_zones(min_xi, max_xi, min_yj, max_yj)

        if valid_count == total_zones:
            max_area = area

    return max_area


if __name__ == "__main__":
    main(day=DAY, part=2, code=code, example_or_real=ExampleOrReal.REAL)
