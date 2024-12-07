import itertools

from utils import main

# ================================
# PART 1
# ================================


def code(s: str):
    operarators_possibles = ["+", "*", "||"]

    lines = s.split("\n")
    counter = 0
    for line in lines:
        result, numbers = line.split(":")
        result = int(result)
        numbers = numbers.split()

        combinations = itertools.product(operarators_possibles, repeat=len(numbers) - 1)

        for combination in combinations:
            evaluated_result = int(numbers[0])
            for number, operator in zip(numbers[1:], combination):
                if operator == "||":
                    evaluated_result = int(f"{evaluated_result}{number}")
                else:
                    if operator == "+":
                        evaluated_result += int(number)
                    elif operator == "*":
                        evaluated_result *= int(number)

            if evaluated_result == result:
                counter += result
                break

    return counter


if __name__ == "__main__":
    main(day=7, part=2, code=code)
