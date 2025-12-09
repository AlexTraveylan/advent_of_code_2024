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

    def get_sizes(self):
        roots = set()
        for i in range(len(self.parent)):
            root = self.find(i)
            roots.add(root)
        return [self.size[root] for root in roots]


def code(s: str) -> int:
    boxes = []
    for line in s.strip().split("\n"):
        if line.strip():
            x, y, z = map(int, line.split(","))
            boxes.append((x, y, z))

    n = len(boxes)

    target_connections = 10 if n <= 20 else 1000

    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1, z1 = boxes[i]
            x2, y2, z2 = boxes[j]
            dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) ** 0.5
            distances.append((dist, i, j))

    distances.sort()

    uf = UnionFind(n)
    connections_attempted = 0

    for dist, i, j in distances:
        uf.union(i, j)
        connections_attempted += 1
        if connections_attempted >= target_connections:
            break

    circuit_sizes = uf.get_sizes()
    circuit_sizes.sort(reverse=True)

    if len(circuit_sizes) >= 3:
        result = circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]
    else:
        result = 1
        for size in circuit_sizes[:3]:
            result *= size

    return result


if __name__ == "__main__":
    main(day=DAY, part=1, code=code, example_or_real=ExampleOrReal.REAL)
