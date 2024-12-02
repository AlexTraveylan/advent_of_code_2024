from collections import Counter

import numpy as np

from utils import main

# ================================
# PART 1
# ================================


def code(s: str):
    # Your code here

    lines = s.split("\n")
    lines = np.array([[int(x) for x in line.split()] for line in lines])
    transposed_sorted = np.sort(lines.T, axis=1)
    sum_abs_dif = np.sum(np.abs(transposed_sorted[1] - transposed_sorted[0]))

    return sum_abs_dif


# ================================
# PART 2
# ================================


def code(s: str):
    # Your code here

    lines = s.split("\n")
    lines = np.array([[int(x) for x in line.split()] for line in lines])
    transposed_sorted = np.sort(lines.T, axis=1).tolist()
    scores_dict = {k: v * k for k, v in Counter(transposed_sorted[1]).items()}

    return sum(scores_dict.get(number, 0) for number in transposed_sorted[0])


if __name__ == "__main__":
    main(day=1, part=2, code=code)
