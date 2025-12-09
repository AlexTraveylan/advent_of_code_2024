import os
import sys
from collections import deque

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))))

from src.utils import ExampleOrReal, main

DAY = 9


def get_line_tiles(start: tuple[int, int], end: tuple[int, int]) -> set[tuple[int, int]]:
    """Retourne toutes les tuiles sur la ligne entre start et end (inclus)"""
    x1, y1 = start
    x2, y2 = end
    tiles = set()

    if x1 == x2:  # Ligne verticale
        for y in range(min(y1, y2), max(y1, y2) + 1):
            tiles.add((x1, y))
    elif y1 == y2:  # Ligne horizontale
        for x in range(min(x1, x2), max(x1, x2) + 1):
            tiles.add((x, y1))

    return tiles


def flood_fill_exterior(
    valid_tiles: set[tuple[int, int]], min_x: int, max_x: int, min_y: int, max_y: int
) -> set[tuple[int, int]]:
    """Marque l'extérieur du polygone en utilisant flood fill depuis les bords"""
    # Utiliser un set pour les tuiles visitées (extérieur)
    exterior = set()
    visited = set()
    queue: deque[tuple[int, int]] = deque()

    # Points de départ sur les bords
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

    # Flood fill depuis les bords
    while queue:
        x, y = queue.popleft()

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            pos = (nx, ny)
            if min_x <= nx <= max_x and min_y <= ny <= max_y and pos not in valid_tiles and pos not in visited:
                visited.add(pos)
                exterior.add(pos)
                queue.append(pos)

    # Tout ce qui n'est pas extérieur et pas dans valid_tiles est intérieur
    # On ajoute les tuiles intérieures à valid_tiles
    interior = set()
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            pos = (x, y)
            if pos not in valid_tiles and pos not in exterior:
                interior.add(pos)

    return valid_tiles | interior


def code(s: str) -> int:
    # Parse les coordonnées des tuiles rouges
    red_tiles = []
    for line in s.strip().split("\n"):
        if line.strip():
            x, y = map(int, line.split(","))
            red_tiles.append((x, y))

    if not red_tiles:
        return 0

    # Déterminer les bornes
    min_x = min(x for x, y in red_tiles)
    max_x = max(x for x, y in red_tiles)
    min_y = min(y for x, y in red_tiles)
    max_y = max(y for x, y in red_tiles)

    # Utiliser un set pour stocker les tuiles valides (beaucoup plus efficace en mémoire)
    valid_tiles = set()

    # 1. Marquer les tuiles rouges
    for x, y in red_tiles:
        valid_tiles.add((x, y))

    # 2. Marquer les tuiles vertes sur les lignes entre les tuiles rouges consécutives
    for i in range(len(red_tiles)):
        start = red_tiles[i]
        end = red_tiles[(i + 1) % len(red_tiles)]
        line_tiles = get_line_tiles(start, end)
        valid_tiles.update(line_tiles)

    # 3. Trouver les tuiles à l'intérieur de la boucle fermée avec flood fill
    valid_tiles = flood_fill_exterior(valid_tiles, min_x, max_x, min_y, max_y)

    # Trouve le plus grand rectangle valide
    # Fonction helper pour vérifier si un rectangle est valide avec early exit
    def is_rect_valid(min_x_rect, max_x_rect, min_y_rect, max_y_rect):
        """Vérifie si un rectangle est entièrement valide - early exit si une tuile manque"""
        # Vérifier toutes les tuiles du rectangle - sortir immédiatement si une manque
        for y in range(min_y_rect, max_y_rect + 1):
            for x in range(min_x_rect, max_x_rect + 1):
                if (x, y) not in valid_tiles:
                    return False
        return True

    max_area = 0
    n_red = len(red_tiles)

    # Générer et trier les paires par aire décroissante pour trouver le maximum plus tôt
    # Utiliser un générateur pour éviter de stocker toutes les paires en mémoire
    pairs_with_area = [
        ((abs(red_tiles[j][0] - red_tiles[i][0]) + 1) * (abs(red_tiles[j][1] - red_tiles[i][1]) + 1), i, j)
        for i in range(n_red)
        for j in range(i + 1, n_red)
    ]

    # Trier par aire décroissante
    pairs_with_area.sort(reverse=True)

    for area, i, j in pairs_with_area:
        # Si l'aire actuelle est plus petite que le max trouvé, on peut arrêter
        if area <= max_area:
            break

        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[j]

        # Déterminer les coins du rectangle
        min_x_rect = min(x1, x2)
        max_x_rect = max(x1, x2)
        min_y_rect = min(y1, y2)
        max_y_rect = max(y1, y2)

        # Vérifier si le rectangle est valide (avec early exit)
        if is_rect_valid(min_x_rect, max_x_rect, min_y_rect, max_y_rect):
            max_area = area

    return max_area


if __name__ == "__main__":
    main(day=DAY, part=2, code=code, example_or_real=ExampleOrReal.REAL)
