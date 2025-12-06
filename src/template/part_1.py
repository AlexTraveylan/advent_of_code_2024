import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))))


from src.utils import ExampleOrReal, main

DAY = 1


def code(s: str) -> int:
    # Your code here

    return 0


if __name__ == "__main__":
    main(day=DAY, part=1, code=code, example_or_real=ExampleOrReal.REAL)
