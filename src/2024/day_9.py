from typing import Literal

from utils import main

# ================================
# PART 1
# ================================


def compress(disk: list[int | Literal["."]]) -> str:
    result = [str(x) if x != "." else "." for x in disk]
    empty_indexes = [i for i, x in enumerate(result) if x == "."]

    def reverse_index(index: int) -> int:
        return len(result) - index - 1

    while True:
        modified = False

        for index, bit in enumerate(result[::-1]):
            if bit.isdigit() is False:
                continue

            reversed_index = reverse_index(index)
            for empty_index in empty_indexes:
                if empty_index < reversed_index:
                    result[empty_index] = bit
                    result[reversed_index] = "."
                    modified = True
                    empty_indexes.remove(empty_index)
                    break

        if not modified:
            break

    return result


def compute_score(disk: list[str]) -> int:
    return sum(i * int(x) for i, x in enumerate(disk) if x != ".")


def code(s: str):
    # Your code here

    disk = []
    pair_bit = [int(b) for i, b in enumerate(s) if i % 2 == 0] + [0]
    imp_bit = [int(b) for i, b in enumerate(s) if i % 2 == 1] + [0]

    for id, (file_slot, empty_slot) in enumerate(zip(pair_bit, imp_bit)):
        disk.extend([id] * file_slot + ["."] * empty_slot)

    compressed = compress(disk)
    return compute_score(compressed)


# ================================
# PART 2
# ================================


# def code(s: str):
#     # Your code here
#     return 0

if __name__ == "__main__":
    main(day=9, part=1, code=code)
