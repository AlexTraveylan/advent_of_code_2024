import os
import re
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))))

from src.utils import ExampleOrReal, main

DAY = 10


def parse_line(line: str):
    pattern_match = re.search(r"\[([.#]+)\]", line)
    if not pattern_match:
        return None, None

    pattern_str = pattern_match.group(1)
    target = [1 if c == "#" else 0 for c in pattern_str]

    buttons = []
    button_matches = re.findall(r"\(([^)]+)\)", line)
    for btn_str in button_matches:
        indices = [int(x) for x in btn_str.split(",")]
        buttons.append(indices)

    return target, buttons


def gaussian_elimination_gf2(matrix, target):
    n_lights = len(target)
    n_buttons = len(matrix)

    aug_matrix = [[0] * (n_buttons + 1) for _ in range(n_lights)]

    for j, button in enumerate(matrix):
        for light_idx in button:
            if light_idx < n_lights:
                aug_matrix[light_idx][j] = 1

    for i in range(n_lights):
        aug_matrix[i][n_buttons] = target[i]

    row = 0
    pivot_cols = []

    for col in range(n_buttons):
        pivot_row = None
        for r in range(row, n_lights):
            if aug_matrix[r][col] == 1:
                pivot_row = r
                break

        if pivot_row is None:
            continue

        aug_matrix[row], aug_matrix[pivot_row] = aug_matrix[pivot_row], aug_matrix[row]
        pivot_cols.append(col)

        for r in range(n_lights):
            if r != row and aug_matrix[r][col] == 1:
                for c in range(n_buttons + 1):
                    aug_matrix[r][c] ^= aug_matrix[row][c]

        row += 1
        if row >= n_lights:
            break

    for r in range(row, n_lights):
        if aug_matrix[r][n_buttons] != 0:
            return None

    solution = [0] * n_buttons

    for r in range(row - 1, -1, -1):
        col = pivot_cols[r]
        val = aug_matrix[r][n_buttons]
        for c in range(col + 1, n_buttons):
            val ^= aug_matrix[r][c] & solution[c]
        solution[col] = val

    return sum(solution)


def solve_machine(target, buttons):
    n_lights = len(target)
    n_buttons = len(buttons)

    if n_buttons == 0:
        return 0 if all(x == 0 for x in target) else None

    aug_matrix = [[0] * (n_buttons + 1) for _ in range(n_lights)]

    for j, button in enumerate(buttons):
        for light_idx in button:
            if light_idx < n_lights:
                aug_matrix[light_idx][j] = 1

    for i in range(n_lights):
        aug_matrix[i][n_buttons] = target[i]

    row = 0
    pivot_cols = []

    for col in range(n_buttons):
        pivot_row = None
        for r in range(row, n_lights):
            if aug_matrix[r][col] == 1:
                pivot_row = r
                break

        if pivot_row is None:
            continue

        aug_matrix[row], aug_matrix[pivot_row] = aug_matrix[pivot_row], aug_matrix[row]
        pivot_cols.append(col)

        for r in range(n_lights):
            if r != row and aug_matrix[r][col] == 1:
                for c in range(n_buttons + 1):
                    aug_matrix[r][c] ^= aug_matrix[row][c]

        row += 1
        if row >= n_lights:
            break

    for r in range(row, n_lights):
        if aug_matrix[r][n_buttons] != 0:
            return None

    solution = [0] * n_buttons

    for r in range(row - 1, -1, -1):
        col = pivot_cols[r]
        val = aug_matrix[r][n_buttons]
        for c in range(col + 1, n_buttons):
            val ^= aug_matrix[r][c] & solution[c]
        solution[col] = val

    free_vars = [i for i in range(n_buttons) if i not in pivot_cols]

    best_solution = solution[:]
    best_weight = sum(best_solution)
    if len(free_vars) <= 10:
        for mask in range(1 << len(free_vars)):
            test_solution = solution[:]
            for i, fv_idx in enumerate(free_vars):
                if (mask >> i) & 1:
                    test_solution[fv_idx] = 1

            test_solution2 = [0] * n_buttons
            for i, fv_idx in enumerate(free_vars):
                test_solution2[fv_idx] = (mask >> i) & 1

            for r in range(row - 1, -1, -1):
                col = pivot_cols[r]
                val = aug_matrix[r][n_buttons]
                for c in range(col + 1, n_buttons):
                    val ^= aug_matrix[r][c] & test_solution2[c]
                test_solution2[col] = val

            weight = sum(test_solution2)
            if weight < best_weight:
                best_weight = weight
                best_solution = test_solution2
    else:
        pass

    return best_weight


def code(s: str) -> int:
    lines = s.strip().split("\n")
    total_presses = 0

    for line in lines:
        if not line.strip():
            continue

        target, buttons = parse_line(line)
        if target is None or buttons is None:
            continue

        min_presses = solve_machine(target, buttons)
        if min_presses is not None:
            total_presses += min_presses

    return total_presses


if __name__ == "__main__":
    main(day=DAY, part=1, code=code, example_or_real=ExampleOrReal.REAL)
