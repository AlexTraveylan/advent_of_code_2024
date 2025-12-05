from src.utils import main

DAY = 5


def code(s: str):
    parts = s.strip().split("\n\n")
    ranges_str = parts[0]

    ranges = []
    for line in ranges_str.strip().split("\n"):
        start, end = map(int, line.split("-"))
        ranges.append((start, end))

    if not ranges:
        return 0

    ranges.sort()

    merged = []
    for start, end in ranges:
        if not merged:
            merged.append([start, end])
        else:
            _, last_end = merged[-1]
            if start <= last_end + 1:
                merged[-1][1] = max(last_end, end)
            else:
                merged.append([start, end])

    total = 0
    for start, end in merged:
        total += end - start + 1

    return total


if __name__ == "__main__":
    main(day=DAY, part=2, code=code)
