import os
import sys
import numpy as np
from typing import List, Tuple, Optional

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))))

from src.utils import ExampleOrReal, main

DAY = 12


def parse_shapes(s: str) -> List[np.ndarray]:
    """Parse les formes de présents et génère toutes leurs rotations/flips uniques"""
    shapes = []
    current_shape = []
    current_id = None
    
    for line in s.split('\n'):
        line = line.strip()
        
        if ':' in line and not 'x' in line.split(':')[0]:
            # Nouvelle forme (format "N:")
            if current_shape and current_id is not None:
                shape_array = np.array(current_shape, dtype=bool)
                # Générer toutes les rotations et flips uniques
                unique_variants = generate_unique_variants(shape_array)
                shapes.append(unique_variants)
            try:
                current_id = int(line.split(':')[0])
                current_shape = []
            except ValueError:
                pass
        elif line and current_id is not None and not 'x' in line:
            # Ligne de la forme (contient # ou .)
            if '#' in line or '.' in line:
                row = [c == '#' for c in line]
                current_shape.append(row)
    
    # Ajouter la dernière forme
    if current_shape and current_id is not None:
        shape_array = np.array(current_shape, dtype=bool)
        unique_variants = generate_unique_variants(shape_array)
        shapes.append(unique_variants)
    
    return shapes


def generate_unique_variants(shape: np.ndarray) -> List[np.ndarray]:
    """Génère toutes les rotations et flips uniques d'une forme"""
    variants = set()
    
    # 4 rotations
    for rotation in range(4):
        rotated = np.rot90(shape, rotation)
        # Pour chaque rotation, essayer avec et sans flips
        variants.add(tuple(map(tuple, rotated)))
        variants.add(tuple(map(tuple, np.fliplr(rotated))))
        variants.add(tuple(map(tuple, np.flipud(rotated))))
        # Flip les deux axes (équivalent à rot90(rotated, 2) pour certaines formes)
        flipped_both = np.fliplr(np.flipud(rotated))
        variants.add(tuple(map(tuple, flipped_both)))
    
    # Convertir en listes de numpy arrays (garder la taille originale)
    # Trier par taille pour tester les plus grandes variantes en premier
    result = [np.array(v, dtype=bool) for v in variants]
    result.sort(key=lambda x: -x.sum())  # Plus grandes d'abord
    return result


def parse_regions(s: str) -> List[Tuple[int, int, List[int]]]:
    """Parse les régions : dimensions et quantités de chaque forme"""
    regions = []
    
    for line in s.split('\n'):
        line = line.strip()
        if not line or ':' not in line:
            continue
        
        parts = line.split(':')
        if len(parts) != 2:
            continue
        
        # Parser dimensions
        dims = parts[0].split('x')
        if len(dims) != 2:
            continue
        
        width = int(dims[0])
        height = int(dims[1])
        
        # Parser quantités
        quantities = [int(x) for x in parts[1].strip().split()]
        
        regions.append((width, height, quantities))
    
    return regions


def can_place_shape(grid: np.ndarray, shape: np.ndarray, row: int, col: int) -> bool:
    """Vérifie si on peut placer une forme à la position donnée"""
    h, w = shape.shape
    if row + h > grid.shape[0] or col + w > grid.shape[1]:
        return False
    
    # Vérifier qu'il n'y a pas de chevauchement : là où la forme a un #, la grille doit être vide
    grid_slice = grid[row:row+h, col:col+w]
    return np.all((grid_slice & shape) == 0)


def place_shape(grid: np.ndarray, shape: np.ndarray, row: int, col: int) -> None:
    """Place une forme sur la grille"""
    h, w = shape.shape
    grid[row:row+h, col:col+w] |= shape


def remove_shape(grid: np.ndarray, shape: np.ndarray, row: int, col: int) -> None:
    """Retire une forme de la grille"""
    h, w = shape.shape
    grid[row:row+h, col:col+w] &= ~shape


def backtrack(
    grid: np.ndarray,
    shapes: List[List[np.ndarray]],
    quantities: List[int],
    shape_idx: int = 0,
    must_cover_first: bool = True
) -> bool:
    """Backtracking optimisé pour placer toutes les pièces"""
    # Si toutes les pièces sont placées
    if shape_idx >= len(shapes):
        return True
    
    # Si on n'a plus besoin de cette forme, passer à la suivante
    if quantities[shape_idx] == 0:
        return backtrack(grid, shapes, quantities, shape_idx + 1, True)
    
    # Trouver la première position libre (pour éviter les symétries)
    first_free_row, first_free_col = -1, -1
    if must_cover_first:
        for row in range(grid.shape[0]):
            for col in range(grid.shape[1]):
                if not grid[row, col]:
                    first_free_row, first_free_col = row, col
                    break
            if first_free_row != -1:
                break
    
    if must_cover_first and first_free_row == -1:
        return all(q == 0 for q in quantities)
    
    # Essayer de placer une instance de cette forme
    for variant in shapes[shape_idx]:
        h, w = variant.shape
        
        if must_cover_first and first_free_row != -1:
            # Essayer seulement les positions qui couvrent la première case libre
            row_start = max(0, first_free_row - h + 1)
            row_end = min(grid.shape[0] - h + 1, first_free_row + 1)
            col_start = max(0, first_free_col - w + 1)
            col_end = min(grid.shape[1] - w + 1, first_free_col + 1)
        else:
            # Essayer toutes les positions (pour les instances suivantes)
            row_start, row_end = 0, grid.shape[0] - h + 1
            col_start, col_end = 0, grid.shape[1] - w + 1
        
        for row in range(row_start, row_end):
            for col in range(col_start, col_end):
                # Si must_cover_first, vérifier que cette position couvre la première case libre
                if must_cover_first and first_free_row != -1:
                    if (first_free_row < row or first_free_row >= row + h or
                        first_free_col < col or first_free_col >= col + w):
                        continue
                    if not variant[first_free_row - row, first_free_col - col]:
                        continue
                
                if can_place_shape(grid, variant, row, col):
                    # Placer la forme
                    place_shape(grid, variant, row, col)
                    quantities[shape_idx] -= 1
                    
                    # Pour la prochaine instance de la même forme, ne pas forcer must_cover_first
                    # mais après avoir placé toutes les instances, forcer à nouveau
                    next_must_cover = quantities[shape_idx] == 0
                    if backtrack(grid, shapes, quantities, shape_idx, next_must_cover):
                        return True
                    
                    # Backtrack
                    quantities[shape_idx] += 1
                    remove_shape(grid, variant, row, col)
    
    return False


def can_fit_presents(width: int, height: int, shapes: List[List[np.ndarray]], quantities: List[int]) -> bool:
    """Vérifie si on peut placer toutes les pièces dans la région"""
    # Vérification rapide : la somme des surfaces doit être <= surface de la grille
    total_area = sum(qty * shapes[i][0].sum() for i, qty in enumerate(quantities))
    if total_area > width * height:
        return False
    
    # Créer une grille vide
    grid = np.zeros((height, width), dtype=bool)
    
    # Créer une copie des quantités pour ne pas modifier l'original
    qty_copy = quantities.copy()
    
    # Trier les formes par taille décroissante (surface * quantité) pour optimiser le backtracking
    shape_indices = sorted(range(len(shapes)), 
                          key=lambda i: -(qty_copy[i] * shapes[i][0].sum() if qty_copy[i] > 0 else 0))
    
    # Réorganiser shapes et quantities selon l'ordre trié
    sorted_shapes = [shapes[i] for i in shape_indices]
    sorted_quantities = [qty_copy[i] for i in shape_indices]
    
    return backtrack(grid, sorted_shapes, sorted_quantities)


def code(s: str) -> int:
    lines = s.strip().split('\n')
    
    # Séparer les formes et les régions
    shape_lines = []
    region_lines = []
    in_shapes = True
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Détecter le début des régions (format "WxH: ...")
        if 'x' in line and ':' in line:
            parts = line.split(':')
            if len(parts) == 2:
                dim_part = parts[0].strip()
                if 'x' in dim_part and all(c.isdigit() or c == 'x' for c in dim_part.replace('x', '')):
                    in_shapes = False
        
        if in_shapes:
            shape_lines.append(line)
        else:
            region_lines.append(line)
    
    shapes_str = '\n'.join(shape_lines)
    regions_str = '\n'.join(region_lines)
    
    # Parser les formes
    shapes = parse_shapes(shapes_str)
    
    # Parser les régions
    regions = parse_regions(regions_str)
    
    # Compter combien de régions peuvent contenir toutes leurs pièces
    count = 0
    for width, height, quantities in regions:
        # Filtrer les formes nécessaires (quantité > 0)
        needed_shapes = [shapes[i] for i in range(len(quantities)) if i < len(shapes) and quantities[i] > 0]
        needed_quantities = [quantities[i] for i in range(len(quantities)) if i < len(shapes) and quantities[i] > 0]
        
        if needed_shapes and can_fit_presents(width, height, needed_shapes, needed_quantities):
            count += 1
    
    return count


if __name__ == "__main__":
    main(day=DAY, part=2, code=code, example_or_real=ExampleOrReal.REAL)

