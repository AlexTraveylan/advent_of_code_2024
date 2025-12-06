from src.utils import ExampleOrReal, main

DAY = 6


def code(s: str):
    lines = s.strip().split("\n")
    if not lines:
        return 0

    width = max(len(line) for line in lines)

    problems = []
    col = width - 1

    while col >= 0:
        col_chars = [line[col] if col < len(line) else " " for line in lines]

        if all(c == " " for c in col_chars):
            col -= 1
            continue

        problem_cols = []
        while col >= 0:
            col_chars = [line[col] if col < len(line) else " " for line in lines]
            if all(c == " " for c in col_chars):
                break
            problem_cols.append(col_chars)
            col -= 1

        if not problem_cols:
            continue

        numbers = []
        operation = None

        for col_chars in problem_cols:
            if col_chars[-1] in ["+", "*"]:
                operation = col_chars[-1]

            num_str = "".join(c for c in col_chars[:-1] if c.isdigit())
            if num_str:
                numbers.append(int(num_str))

        if operation and numbers:
            if operation == "+":
                result = sum(numbers)
            else:
                result = 1
                for num in numbers:
                    result *= num
            print(f"Problem: numbers={numbers}, operation={operation}, result={result}")
            problems.append(result)

    return sum(problems)


if __name__ == "__main__":
    from src.utils import ExampleOrReal

    main(day=DAY, part=2, code=code, example_or_real=ExampleOrReal.REAL)
