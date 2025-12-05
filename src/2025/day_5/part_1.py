from src.utils import main

DAY = 5


def code(s: str):
    parts = s.strip().split("\n\n")
    ranges_str = parts[0]
    available_ids_str = parts[1]

    ranges = []
    for line in ranges_str.strip().split("\n"):
        start, end = map(int, line.split("-"))
        ranges.append((start, end))

    available_ids = [
        int(line.strip()) for line in available_ids_str.strip().split("\n")
    ]

    fresh_count = 0
    for ingredient_id in available_ids:
        is_fresh = False
        for start, end in ranges:
            if start <= ingredient_id <= end:
                is_fresh = True
                break
        if is_fresh:
            fresh_count += 1

    return fresh_count


if __name__ == "__main__":
    main(day=DAY, part=1, code=code)
