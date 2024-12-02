from itertools import pairwise

from utils import ints, main

# ================================
# PART 1
# ================================


def is_line_ok(line: list[int]) -> bool:
    is_sign_ok = all(n1 < n2 for n1, n2 in pairwise(line)) or all(
        n1 > n2 for n1, n2 in pairwise(line)
    )
    max_diff = max(abs(n1 - n2) for n1, n2 in pairwise(line))

    return is_sign_ok and max_diff <= 3


def code(s: str):
    # Your code here

    lines = [ints(line) for line in s.split("\n")]

    return sum(is_line_ok(line) for line in lines)


# ================================
# PART 2
# ================================


def find_first_error_in_line(line: list[int]) -> int | None:
    sign = 0
    for index, (n1, n2) in enumerate(pairwise(line)):
        if abs(n1 - n2) > 3:
            return index

        if n1 == n2:
            return index

        if n1 > n2 and sign == -1:
            return index

        if n1 < n2 and sign == 1:
            return index

        sign = 1 if n1 > n2 else -1

    return None


def code(s: str):
    # Your code here

    lines = [ints(line) for line in s.split("\n")]

    valid_lines = 0
    for line in lines:
        error_index = find_first_error_in_line(line)

        if error_index == 1:
            is_valid = is_line_ok(line[1:])

            if is_valid:
                valid_lines += 1
                continue

        if error_index is not None:
            line.pop(error_index)

        is_valid = is_line_ok(line)

        if is_valid:
            valid_lines += 1

    return valid_lines


if __name__ == "__main__":
    main(day=2, part=2, code=code)
