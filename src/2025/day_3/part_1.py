from src.utils import main

DAY = 3


def code(s: str):
    lines = s.strip().split("\n")
    total_joltage = 0

    for bank in lines:
        max_joltage = 0
        digits = list(bank)

        for i in range(len(digits)):
            for j in range(i + 1, len(digits)):
                joltage = int(digits[i] + digits[j])
                max_joltage = max(max_joltage, joltage)

        total_joltage += max_joltage

    return total_joltage


if __name__ == "__main__":
    main(day=DAY, part=1, code=code)
