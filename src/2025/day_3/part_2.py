from src.utils import main

DAY = 3


def code(s: str):
    lines = s.strip().split("\n")
    total_joltage = 0

    for bank in lines:
        digits = list(bank)
        n = len(digits)
        k = 12

        if n < k:
            continue

        result = []
        to_remove = n - k

        for digit in digits:
            while result and result[-1] < digit and to_remove > 0:
                result.pop()
                to_remove -= 1
            result.append(digit)

        joltage = int("".join(result[0:k]))
        total_joltage += joltage

    return total_joltage


if __name__ == "__main__":
    main(day=DAY, part=2, code=code)
