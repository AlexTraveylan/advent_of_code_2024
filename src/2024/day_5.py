import itertools

from utils import ints, main

# ================================
# PART 1
# ================================


def check_rule(rule: tuple[int, int], order: list[int]) -> bool:
    try:
        return order.index(rule[0]) < order.index(rule[1])
    except ValueError:
        return True


def is_valid_order(order: list[int], rules: list[tuple[int, int]]) -> bool:
    for rule in rules:
        if not check_rule(rule, order):
            return False
    return True


def middle_number(order: list[int]) -> int:
    return order[len(order) // 2]


def code(s: str):
    # Your code here

    rules, orders = s.split("\n\n")
    rules = [ints(r, sep="|") for r in rules.split("\n")]
    orders = [ints(o, sep=",") for o in orders.split("\n")]

    valid_orders = []
    for order in orders:
        if is_valid_order(order, rules):
            valid_orders.append(order)

    return sum(middle_number(o) for o in valid_orders)


# ================================
# PART 2
# ================================


def invalid_to_valid(order: list[int], rules: list[tuple[int, int]]) -> list[int]:
    for possible_order in itertools.permutations(order):
        if is_valid_order(possible_order, rules):
            return possible_order


def invalid_to_valid(order: list[int], rules: list[tuple[int, int]]) -> list[int]:
    # Créer un graphe orienté à partir des règles
    graph = {}
    in_degree = {}

    # Initialiser le graphe
    for num in order:
        graph[num] = set()
        in_degree[num] = 0

    # Construire le graphe à partir des règles
    for before, after in rules:
        if before in order and after in order:
            graph[before].add(after)
            in_degree[after] = in_degree.get(after, 0) + 1

    # Tri topologique avec file d'attente
    result = []
    queue = [num for num in order if in_degree[num] == 0]

    while queue:
        current = queue.pop(0)
        result.append(current)

        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return result if len(result) == len(order) else order


def code(s: str):
    rules, orders = s.split("\n\n")
    rules = [ints(r, sep="|") for r in rules.split("\n")]
    orders = [ints(o, sep=",") for o in orders.split("\n")]

    invalid_orders = []
    for order in orders:
        if not is_valid_order(order, rules):
            invalid_orders.append(order)

    return sum(middle_number(invalid_to_valid(o, rules)) for o in invalid_orders)


if __name__ == "__main__":
    main(day=5, part=2, code=code)
