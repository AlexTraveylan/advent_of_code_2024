from utils import main

# ================================
# PART 1
# ================================


def distance_vector(
    coord1: tuple[int, int], coord2: tuple[int, int]
) -> tuple[int, int]:
    return (coord1[0] - coord2[0], coord1[1] - coord2[1])


def has_double(vectors: list[tuple[int, int]]) -> bool:
    seen = set(vectors)
    return any(x1 * 2 == x2 and y1 * 2 == y2 for x1, y1 in vectors for x2, y2 in seen)


def is_aligned(coord: tuple[int, int], antenne_coords: list[tuple[int, int]]) -> bool:
    for i in range(len(antenne_coords)):
        for j in range(i + 1, len(antenne_coords)):
            antenne1 = antenne_coords[i]
            antenne2 = antenne_coords[j]

            vector1 = distance_vector(coord, antenne1)
            vector2 = distance_vector(coord, antenne2)

            if (vector1[0] * vector2[1]) - (vector2[0] * vector1[1]) == 0:
                return True

    return False


def is_anti_node(
    coord: tuple[int, int], cell: str, antennes: dict[str, list[tuple[int, int]]]
) -> bool:
    for antenne_type, coords in antennes.items():
        distance_vectors = [distance_vector(coord, c) for c in coords]
        if antenne_type != cell and has_double(distance_vectors):
            return True
    return False


def is_anti_node(
    coord: tuple[int, int], cell: str, antennes: dict[str, list[tuple[int, int]]]
) -> bool:
    for antenne_type, coords in antennes.items():
        if is_aligned(coord, coords):
            return True
    return False


def code(s: str):
    # Your code here

    grid = [list(c) for c in s.split("\n")]

    antennes: dict[str, list[tuple[int, int]]] = {}
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell != ".":
                antennes.setdefault(cell, []).append((i, j))

    count_anti_node = 0
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if is_anti_node((i, j), cell, antennes):
                count_anti_node += 1

    return count_anti_node


# ================================
# PART 2
# ================================


# def code(s: str):
#     # Your code here
#     return 0

if __name__ == "__main__":
    main(day=8, part=2, code=code)
