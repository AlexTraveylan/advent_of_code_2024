import os
import sys
from functools import lru_cache

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))))


from src.utils import ExampleOrReal, main

DAY = 11


def code(s: str) -> int:
    graph: dict[str, list[str]] = {}

    for line in s.strip().split("\n"):
        parts = line.split(": ")
        node = parts[0]
        neighbors = parts[1].split() if len(parts) > 1 else []
        graph[node] = neighbors

    @lru_cache(maxsize=None)
    def count_paths(node: str) -> int:
        if node == "out":
            return 1

        if node not in graph:
            return 0

        total = 0
        for neighbor in graph[node]:
            total += count_paths(neighbor)

        return total

    return count_paths("you")


if __name__ == "__main__":
    main(day=DAY, part=1, code=code, example_or_real=ExampleOrReal.REAL)
