import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))))

from src.utils import ExampleOrReal, main

DAY = 8


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        if self.size[root_x] < self.size[root_y]:
            root_x, root_y = root_y, root_x

        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]
        return True

    def count_components(self):
        roots = set()
        for i in range(len(self.parent)):
            root = self.find(i)
            roots.add(root)
        return len(roots)


def code(s: str) -> int:
    boxes = []
    for line in s.strip().split("\n"):
        if line.strip():
            x, y, z = map(int, line.split(","))
            boxes.append((x, y, z))

    n = len(boxes)

    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1, z1 = boxes[i]
            x2, y2, z2 = boxes[j]
            dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) ** 0.5
            distances.append((dist, i, j))

    distances.sort()

    uf = UnionFind(n)
    last_connection = None

    for dist, i, j in distances:
        if uf.union(i, j):
            last_connection = (i, j)
            if uf.count_components() == 1:
                break

    if last_connection:
        i, j = last_connection
        x1, _, _ = boxes[i]
        x2, _, _ = boxes[j]
        result = x1 * x2
    else:
        result = 0

    return result


if __name__ == "__main__":
    main(day=DAY, part=2, code=code, example_or_real=ExampleOrReal.REAL)
