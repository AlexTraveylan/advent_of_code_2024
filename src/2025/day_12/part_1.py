import os
import sys
from typing import List, Tuple

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))))

from src.utils import ExampleOrReal, main

DAY = 12


def parse_shapes(s: str) -> List[List[List[Tuple[int, int]]]]:
    """Parse les formes et génère toutes leurs variantes comme listes de coordonnées relatives"""
    shapes = []
    current_shape = []
    current_id = None

    for line in s.split("\n"):
        line = line.strip()

        if ":" in line and "x" not in line.split(":")[0]:
            if current_shape and current_id is not None:
                variants = generate_variants(current_shape)
                shapes.append(variants)
            try:
                current_id = int(line.split(":")[0])
                current_shape = []
            except ValueError:
                pass
        elif line and current_id is not None and "x" not in line:
            if "#" in line or "." in line:
                row = [c == "#" for c in line]
                current_shape.append(row)

    if current_shape and current_id is not None:
        variants = generate_variants(current_shape)
        shapes.append(variants)

    return shapes


def generate_variants(shape: List[List[bool]]) -> List[List[Tuple[int, int]]]:
    """Génère toutes les variantes uniques d'une forme"""
    coords = [(r, c) for r, row in enumerate(shape) for c, val in enumerate(row) if val]

    def normalize(coords):
        if not coords:
            return tuple()
        min_r = min(r for r, c in coords)
        min_c = min(c for r, c in coords)
        return tuple(sorted((r - min_r, c - min_c) for r, c in coords))

    def rotate90(coords):
        return [(c, -r) for r, c in coords]

    def flip_h(coords):
        return [(r, -c) for r, c in coords]

    variants = set()
    current = coords
    for _ in range(4):
        variants.add(normalize(current))
        variants.add(normalize(flip_h(current)))
        current = rotate90(current)

    return [list(v) for v in variants]


def parse_regions(s: str) -> List[Tuple[int, int, List[int]]]:
    """Parse les régions"""
    regions = []

    for line in s.split("\n"):
        line = line.strip()
        if not line or ":" not in line:
            continue

        parts = line.split(":")
        if len(parts) != 2:
            continue

        dims = parts[0].split("x")
        if len(dims) != 2:
            continue

        width = int(dims[0])
        height = int(dims[1])
        quantities = [int(x) for x in parts[1].strip().split()]

        regions.append((width, height, quantities))

    return regions


def solve_region_bitboard(
    width: int, height: int, shapes: List[List[List[Tuple[int, int]]]], quantities: List[int]
) -> bool:
    """
    Résout le problème de placement en utilisant des bitboards.
    Chaque case (r, c) est représentée par le bit (r * width + c).
    """
    total_area = sum(qty * len(shapes[i][0]) for i, qty in enumerate(quantities))
    grid_area = width * height
    if total_area > grid_area:
        return False

    # Pré-calculer tous les placements possibles comme masques de bits
    all_placements_by_shape = []
    for shape_variants in shapes:
        shape_placements = []
        for variant in shape_variants:
            max_r = max(r for r, c in variant)
            max_c = max(c for r, c in variant)
            if max_r < height and max_c < width:
                for start_r in range(height - max_r):
                    for start_c in range(width - max_c):
                        # Calculer le masque de bits
                        mask = 0
                        min_pos = float("inf")
                        for r, c in variant:
                            pos = (r + start_r) * width + (c + start_c)
                            mask |= 1 << pos
                            min_pos = min(min_pos, pos)
                        shape_placements.append((min_pos, mask))
        # Trier par position minimale
        shape_placements.sort()
        all_placements_by_shape.append(shape_placements)

    # Vérifier que chaque forme a au moins un placement
    for shape_idx, qty in enumerate(quantities):
        if qty > 0 and not all_placements_by_shape[shape_idx]:
            return False

    occupied = 0  # Bitboard des cases occupées
    remaining_qtys = quantities.copy()
    last_placement_idx = [-1] * len(shapes)

    def backtrack(shape_idx: int) -> bool:
        nonlocal occupied

        # Pruning rapide
        remaining_cells = sum(remaining_qtys[i] * len(shapes[i][0]) for i in range(len(shapes)))
        if remaining_cells > grid_area - bin(occupied).count("1"):
            return False

        if remaining_qtys[shape_idx] == 0:
            if shape_idx + 1 >= len(shapes):
                return True
            last_placement_idx[shape_idx + 1] = -1
            return backtrack(shape_idx + 1)

        placements = all_placements_by_shape[shape_idx]
        start_idx = last_placement_idx[shape_idx] + 1

        for i in range(start_idx, len(placements)):
            min_pos, mask = placements[i]
            if not (occupied & mask):  # Pas de chevauchement
                occupied |= mask
                old_idx = last_placement_idx[shape_idx]
                last_placement_idx[shape_idx] = i
                remaining_qtys[shape_idx] -= 1

                if backtrack(shape_idx):
                    return True

                remaining_qtys[shape_idx] += 1
                last_placement_idx[shape_idx] = old_idx
                occupied &= ~mask

        return False

    if not quantities or all(q == 0 for q in quantities):
        return True

    return backtrack(0)


def code(s: str) -> int:
    lines = s.strip().split("\n")

    shape_lines = []
    region_lines = []
    in_shapes = True

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if "x" in line and ":" in line:
            parts = line.split(":")
            if len(parts) == 2:
                dim_part = parts[0].strip()
                if "x" in dim_part and all(c.isdigit() or c == "x" for c in dim_part.replace("x", "")):
                    in_shapes = False

        if in_shapes:
            shape_lines.append(line)
        else:
            region_lines.append(line)

    shapes_str = "\n".join(shape_lines)
    regions_str = "\n".join(region_lines)

    shapes = parse_shapes(shapes_str)
    regions = parse_regions(regions_str)

    count = 0
    for width, height, quantities in regions:
        needed_shapes = [shapes[i] for i in range(len(quantities)) if i < len(shapes) and quantities[i] > 0]
        needed_quantities = [quantities[i] for i in range(len(quantities)) if i < len(shapes) and quantities[i] > 0]

        if not needed_shapes or solve_region_bitboard(width, height, needed_shapes, needed_quantities):
            count += 1

    return count


if __name__ == "__main__":
    main(day=DAY, part=1, code=code, example_or_real=ExampleOrReal.REAL)
