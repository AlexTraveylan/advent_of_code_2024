import re

from utils import main

# ================================
# PART 1
# ================================


def extract_mul(text: str) -> list[str]:
    pattern = r"mul\((\d+),(\d+)\)"
    return re.findall(pattern, text)


def code(s: str):
    # Your code here

    muls = extract_mul(s)
    return sum([int(a) * int(b) for a, b in muls])


# ================================
# PART 2
# ================================


def custom_split(text: str) -> list[str]:
    separators = [r"don't\(\)", r"do\(\)"]
    pattern = f"({('|'.join(separators))})"
    parts = re.split(pattern, text)
    return [part for part in parts if part]


def code(s: str):
    # Your code here

    s_splited = custom_split(s)

    is_ok = True
    result = 0
    for part in s_splited:
        if part == "don't()":
            is_ok = False
            continue

        if part == "do()":
            is_ok = True
            continue

        if is_ok is False:
            continue

        muls = extract_mul(part)
        result += sum([int(a) * int(b) for a, b in muls])

    return result


if __name__ == "__main__":
    main(day=3, part=2, code=code)
