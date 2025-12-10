import os
import re
import sys

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, linprog, milp

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))))

from src.utils import ExampleOrReal, main

DAY = 10


def parse_line(line: str):
    joltage_match = re.search(r"\{([^}]+)\}", line)
    if not joltage_match:
        return None, None

    joltage_str = joltage_match.group(1)
    target = [int(x.strip()) for x in joltage_str.split(",")]

    buttons = []
    button_matches = re.findall(r"\(([^)]+)\)", line)
    for btn_str in button_matches:
        indices = [int(x) for x in btn_str.split(",")]
        buttons.append(indices)

    return target, buttons


def solve_machine_joltage(target, buttons):
    n_counters = len(target)
    n_buttons = len(buttons)

    if n_buttons == 0:
        return 0 if all(x == 0 for x in target) else None

    A = np.zeros((n_counters, n_buttons), dtype=int)
    for j, button in enumerate(buttons):
        for counter_idx in button:
            if counter_idx < n_counters:
                A[counter_idx, j] = 1

    c = np.ones(n_buttons)

    constraints = LinearConstraint(A, target, target)

    max_val = max(target) * 2 if target else 100
    bounds = Bounds(lb=0, ub=max_val)

    integrality = np.ones(n_buttons, dtype=int)

    try:
        result = milp(
            c=c,
            constraints=constraints,
            bounds=bounds,
            integrality=integrality,
        )

        if result.success:
            solution_int = np.round(result.x).astype(int)
            if np.allclose(A @ solution_int, target, atol=1e-6):
                return int(np.sum(solution_int))
    except Exception:
        pass

    try:
        b_eq = np.array(target, dtype=int)
        bounds_list = [(0, max_val) for _ in range(n_buttons)]

        result = linprog(
            c,
            A_eq=A,
            b_eq=b_eq,
            bounds=bounds_list,
            method="highs",
            integrality=1,
        )

        if result.success:
            solution_int = np.round(result.x).astype(int)
            if np.allclose(A @ solution_int, b_eq, atol=1e-6):
                return int(np.sum(solution_int))
    except Exception:
        pass

    return solve_optimized_search(A, target, n_buttons)


def solve_integer_linear_programming(A, target, n_buttons):
    n_counters = len(target)

    aug_matrix = np.zeros((n_counters, n_buttons + 1), dtype=int)
    aug_matrix[:, :n_buttons] = A
    aug_matrix[:, n_buttons] = target

    row = 0
    pivot_cols = []

    for col in range(n_buttons):
        pivot_row = None
        for r in range(row, n_counters):
            if aug_matrix[r, col] != 0:
                pivot_row = r
                break

        if pivot_row is None:
            continue

        aug_matrix[[row, pivot_row]] = aug_matrix[[pivot_row, row]]
        pivot_cols.append(col)

        pivot_val = aug_matrix[row, col]
        if pivot_val != 1:
            pass

        for r in range(n_counters):
            if r != row and aug_matrix[r, col] != 0:
                factor = aug_matrix[r, col] // aug_matrix[row, col]
                aug_matrix[r] -= factor * aug_matrix[row]

        row += 1
        if row >= n_counters:
            break

    for r in range(row, n_counters):
        if aug_matrix[r, n_counters] != 0:
            return None

    return solve_with_search(A, target, n_buttons)


def solve_with_search(A, target, n_buttons):
    n_counters = len(target)

    solution = np.zeros(n_buttons, dtype=int)

    remaining = np.array(target, dtype=int)

    max_iterations = sum(target) * 2
    iteration = 0

    while np.any(remaining > 0) and iteration < max_iterations:
        iteration += 1

        best_button = None
        best_reduction = float("inf")

        for btn_idx in range(n_buttons):
            reduction = 0
            for counter_idx in range(n_counters):
                if A[counter_idx, btn_idx] > 0:
                    if remaining[counter_idx] > 0:
                        reduction -= 1
                    else:
                        reduction += 1

            if reduction < best_reduction:
                best_reduction = reduction
                best_button = btn_idx

        if best_button is None:
            break

        solution[best_button] += 1
        for counter_idx in range(n_counters):
            if A[counter_idx, best_button] > 0:
                remaining[counter_idx] -= 1

    if np.any(remaining != 0):
        return solve_with_backtracking(A, target, n_buttons, solution)

    return int(np.sum(solution))


def solve_with_backtracking(A, target, n_buttons, initial_solution=None):
    if initial_solution is None:
        initial_solution = np.zeros(n_buttons, dtype=int)

    current_solution = initial_solution.copy()
    current_sum = np.sum(current_solution)

    current_state = A @ current_solution
    remaining = np.array(target, dtype=int) - current_state

    if np.all(remaining == 0):
        return int(current_sum)

    if np.any(remaining < 0):
        return None

    from scipy.optimize import linprog

    c = np.ones(n_buttons)
    A_eq = A
    b_eq = np.array(target)
    bounds = [(0, None) for _ in range(n_buttons)]

    result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs", integrality=1)

    if result.success:
        solution = result.x.astype(int)
        if np.allclose(A_eq @ solution, b_eq, atol=1e-6):
            return int(np.sum(solution))


def solve_optimized_search(A, target, n_buttons):
    n_counters = len(target)
    target = np.array(target, dtype=int)

    upper_bound = estimate_upper_bound(A, target, n_buttons)
    if upper_bound is None:
        return None

    memo = {}

    def search(remaining, button_idx, current_sum):
        nonlocal upper_bound
        if current_sum >= upper_bound:
            return float("inf")

        if button_idx == n_buttons:
            if np.all(remaining == 0):
                return current_sum
            return float("inf")

        key = (tuple(remaining), button_idx)
        if key in memo:
            cached = memo[key]
            if cached is not None:
                return cached + current_sum

        best = float("inf")

        max_needed = 0
        for counter_idx in range(n_counters):
            if A[counter_idx, button_idx] > 0 and remaining[counter_idx] > 0:
                max_needed = max(max_needed, remaining[counter_idx])

        max_presses = min(max_needed, upper_bound - current_sum)

        for presses in range(0, max_presses + 1):
            new_remaining = remaining.copy()
            for counter_idx in range(n_counters):
                if A[counter_idx, button_idx] > 0:
                    new_remaining[counter_idx] -= presses

            if np.any(new_remaining < 0):
                continue

            result = search(new_remaining, button_idx + 1, current_sum + presses)
            if result < best:
                best = result
                if result < float("inf"):
                    upper_bound = min(upper_bound, int(result))

        memo[key] = best - current_sum if best != float("inf") else None
        return best

    result = search(target, 0, 0)
    return int(result) if result != float("inf") else None


def estimate_upper_bound(A, target, n_buttons):
    n_counters = len(target)
    remaining = target.copy()
    total_presses = 0

    button_effects = [np.sum(A[:, j]) for j in range(n_buttons)]
    button_order = sorted(range(n_buttons), key=lambda i: button_effects[i], reverse=True)

    for btn_idx in button_order:
        min_remaining = float("inf")
        for counter_idx in range(n_counters):
            if A[counter_idx, btn_idx] > 0:
                min_remaining = min(min_remaining, remaining[counter_idx])

        if min_remaining > 0 and min_remaining != float("inf"):
            presses = min_remaining
            total_presses += presses
            for counter_idx in range(n_counters):
                if A[counter_idx, btn_idx] > 0:
                    remaining[counter_idx] -= presses

    if np.all(remaining == 0):
        return total_presses

    return sum(target) * 2


def code(s: str) -> int:
    lines = s.strip().split("\n")
    total_presses = 0

    for line in lines:
        if not line.strip():
            continue

        target, buttons = parse_line(line)
        if target is None or buttons is None:
            continue

        min_presses = solve_machine_joltage(target, buttons)
        if min_presses is not None:
            total_presses += min_presses

    return total_presses


if __name__ == "__main__":
    main(day=DAY, part=2, code=code, example_or_real=ExampleOrReal.REAL)
