from src.utils import main

# ================================
# PART 1
# ================================


def find_two_entries_product(entries, target=2020):
    seen = set()
    for num in entries:
        complement = target - num
        if complement in seen:
            return num * complement
        seen.add(num)
    return None


def code(s: str):
    # Your code here

    entries = s.splitlines()
    entries = [int(entry) for entry in entries]

    return find_two_entries_product(entries)


if __name__ == "__main__":
    main(day=1, part=1, code=code)
