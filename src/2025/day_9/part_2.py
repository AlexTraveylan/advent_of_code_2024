import os
import sys
from collections import deque

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))))

import numpy as np

from src.utils import ExampleOrReal, main

DAY = 9


def get_line_tiles_numpy(start: tuple[int, int], end: tuple[int, int]) -> np.ndarray:
    """Retourne toutes les tuiles sur la ligne entre start et end (inclus)"""
    x1, y1 = start
    x2, y2 = end

    if x1 == x2:  # Ligne verticale
        y_coords = np.arange(min(y1, y2), max(y1, y2) + 1)
        x_coords = np.full_like(y_coords, x1)
    elif y1 == y2:  # Ligne horizontale
        x_coords = np.arange(min(x1, x2), max(x1, x2) + 1)
        y_coords = np.full_like(x_coords, y1)
    else:
        return np.array([], dtype=int).reshape(0, 2)

    return np.column_stack((x_coords, y_coords))


def flood_fill_exterior(grid: np.ndarray) -> None:
    """Marque l'extérieur du polygone en utilisant flood fill depuis les bords"""
    height, width = grid.shape
    visited = np.zeros_like(grid)

    # Points de départ sur les bords (utiliser deque pour O(1) pop)
    queue = deque()
    for y in [0, height - 1]:
        for x in range(width):
            if not grid[y, x] and not visited[y, x]:
                queue.append((y, x))
                visited[y, x] = True
    for x in [0, width - 1]:
        for y in range(height):
            if not grid[y, x] and not visited[y, x]:
                queue.append((y, x))
                visited[y, x] = True

    # Flood fill depuis les bords
    while queue:
        y, x = queue.popleft()

        # Marquer comme extérieur (on ne le marque pas dans grid, on utilise visited)
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < height and 0 <= nx < width and not visited[ny, nx] and not grid[ny, nx]:
                visited[ny, nx] = True
                queue.append((ny, nx))

    # Tout ce qui n'est pas visité et pas dans grid est intérieur
    interior_mask = ~visited & ~grid
    grid[interior_mask] = True


def code(s: str) -> int:
    # Parse les coordonnées des tuiles rouges
    red_tiles_list = []
    for line in s.strip().split("\n"):
        if line.strip():
            x, y = map(int, line.split(","))
            red_tiles_list.append((x, y))

    if not red_tiles_list:
        return 0

    red_tiles = np.array(red_tiles_list)

    # Déterminer les bornes et créer un offset pour la grille
    min_x = red_tiles[:, 0].min()
    max_x = red_tiles[:, 0].max()
    min_y = red_tiles[:, 1].min()
    max_y = red_tiles[:, 1].max()

    width = max_x - min_x + 1
    height = max_y - min_y + 1

    # Créer une grille pour marquer les tuiles valides (0 = invalide, 1 = valide)
    grid = np.zeros((height, width), dtype=bool)

    # 1. Marquer les tuiles rouges
    red_x_norm = red_tiles[:, 0] - min_x
    red_y_norm = red_tiles[:, 1] - min_y
    grid[red_y_norm, red_x_norm] = True

    # 2. Marquer les tuiles vertes sur les lignes entre les tuiles rouges consécutives
    for i in range(len(red_tiles)):
        start = red_tiles[i]
        end = red_tiles[(i + 1) % len(red_tiles)]
        line_tiles = get_line_tiles_numpy(start, end)
        if len(line_tiles) > 0:
            line_x_norm = line_tiles[:, 0] - min_x
            line_y_norm = line_tiles[:, 1] - min_y
            grid[line_y_norm, line_x_norm] = True

    # 3. Trouver les tuiles à l'intérieur de la boucle fermée avec flood fill
    flood_fill_exterior(grid)

    # Trouve le plus grand rectangle valide
    # Utiliser des sommes cumulatives 2D pour vérifier rapidement si un rectangle est valide
    # grid_cumsum[y, x] = somme de grid[0:y+1, 0:x+1]
    grid_int = grid.astype(np.int32)
    grid_cumsum = np.cumsum(np.cumsum(grid_int, axis=0), axis=1)
    
    # Fonction helper pour vérifier si un rectangle est valide en O(1)
    def is_rect_valid(min_y_rect, max_y_rect, min_x_rect, max_x_rect):
        """Vérifie si un rectangle est entièrement valide en utilisant les sommes cumulatives"""
        rect_area = (max_y_rect - min_y_rect + 1) * (max_x_rect - min_x_rect + 1)
        
        # Calculer la somme dans le rectangle
        top_sum = grid_cumsum[min_y_rect - 1, max_x_rect] if min_y_rect > 0 else 0
        left_sum = grid_cumsum[max_y_rect, min_x_rect - 1] if min_x_rect > 0 else 0
        diag_sum = grid_cumsum[min_y_rect - 1, min_x_rect - 1] if min_y_rect > 0 and min_x_rect > 0 else 0
        total_sum = grid_cumsum[max_y_rect, max_x_rect] - top_sum - left_sum + diag_sum
        
        return total_sum == rect_area
    
    # Précalculer les coordonnées normalisées
    red_tiles_norm = np.column_stack((red_tiles[:, 0] - min_x, red_tiles[:, 1] - min_y))

    max_area = 0
    n_red = len(red_tiles)

    # Trier par aire potentielle décroissante pour trouver le maximum plus tôt
    # Calculer les aires potentielles et trier
    areas = []
    pairs = []
    for i in range(n_red):
        x1, y1 = red_tiles[i]
        x1_norm, y1_norm = red_tiles_norm[i]
        for j in range(i + 1, n_red):
            x2, y2 = red_tiles[j]
            x2_norm, y2_norm = red_tiles_norm[j]
            area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            areas.append(area)
            pairs.append((i, j, x1_norm, y1_norm, x2_norm, y2_norm, x1, y1, x2, y2))
    
    # Trier par aire décroissante
    sorted_indices = np.argsort(areas)[::-1]
    
    for idx in sorted_indices:
        i, j, x1_norm, y1_norm, x2_norm, y2_norm, x1, y1, x2, y2 = pairs[idx]
        area = areas[idx]
        
        # Si l'aire actuelle est plus petite que le max trouvé, on peut arrêter
        if area <= max_area:
            break
        
        # Déterminer les coins du rectangle
        min_x_rect = min(x1_norm, x2_norm)
        max_x_rect = max(x1_norm, x2_norm)
        min_y_rect = min(y1_norm, y2_norm)
        max_y_rect = max(y1_norm, y2_norm)

        # Vérifier rapidement avec les sommes cumulatives
        if is_rect_valid(min_y_rect, max_y_rect, min_x_rect, max_x_rect):
            max_area = area
            # On peut continuer car on cherche le maximum, mais on a déjà trié par ordre décroissant

    return max_area


if __name__ == "__main__":
    main(day=DAY, part=2, code=code, example_or_real=ExampleOrReal.REAL)
