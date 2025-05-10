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


def code(s: str):
    # Your code here

    lines = [ints(line) for line in s.split("\n")]

    valid_lines = 0
    for line in lines:
        if is_line_ok(line):
            valid_lines += 1
            continue

        for i in range(len(line)):
            line_without_i = line[:i] + line[i + 1 :]

            if is_line_ok(line_without_i):
                valid_lines += 1
                break

    return valid_lines


if __name__ == "__main__":
    main(day=2, part=2, code=code)
