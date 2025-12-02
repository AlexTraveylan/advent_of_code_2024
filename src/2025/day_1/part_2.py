from src.utils import main

DAY = 1


def code(s: str):
    position = 50
    count = 0

    for line in s.strip().split("\n"):
        if not line:
            continue

        direction = line[0]
        distance = int(line[1:])

        if direction == "L":
            for i in range(1, distance):
                current_pos = (position - i) % 100
                if current_pos == 0:
                    count += 1
            position = (position - distance) % 100
            if position == 0:
                count += 1
        else:
            for i in range(1, distance):
                current_pos = (position + i) % 100
                if current_pos == 0:
                    count += 1
            position = (position + distance) % 100
            if position == 0:
                count += 1

    return count


if __name__ == "__main__":
    main(day=DAY, part=2, code=code)
