from src.utils import main

DAY = 2


def is_invalid_id(product_id: int) -> bool:
    id_str = str(product_id)
    length = len(id_str)
    
    if length % 2 != 0:
        return False
    
    half_length = length // 2
    first_half = id_str[:half_length]
    second_half = id_str[half_length:]
    
    return first_half == second_half


def code(s: str):
    ranges_str = s.replace("\n", "").strip()
    ranges = ranges_str.split(",")
    
    total_invalid = 0
    
    for range_str in ranges:
        if not range_str.strip():
            continue
        
        start_str, end_str = range_str.split("-")
        start = int(start_str)
        end = int(end_str)
        
        for product_id in range(start, end + 1):
            if is_invalid_id(product_id):
                total_invalid += product_id
    
    return total_invalid


if __name__ == "__main__":
    main(day=DAY, part=1, code=code)

