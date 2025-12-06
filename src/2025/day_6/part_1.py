import numpy as np

from src.utils import ExampleOrReal, main

DAY = 6


def code(s: str):
    lines = [l.strip() for l in s.strip().split("\n")]

    lines_numbers, operations = lines[:-1], lines[-1].split()

    cols_numbers = np.array(
        [[int(number) for number in line.split()] for line in lines_numbers]
    )

    result = 0
    for index, col_numbers in enumerate(cols_numbers.T):
        if operations[index] == "+":
            result += np.sum(col_numbers)
        else:
            result += np.prod(col_numbers)

    return result


if __name__ == "__main__":
    main(day=DAY, part=1, code=code, offset=1, example_or_real=ExampleOrReal.REAL)
