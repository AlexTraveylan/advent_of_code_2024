import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))


from src.utils import extract_statement

if __name__ == "__main__":
    day, part = int(sys.argv[1]), int(sys.argv[2])

    print(extract_statement(day, part))
