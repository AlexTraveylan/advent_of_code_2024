from src.utils import main


def find_three_entries_product(expense_report, target=2020):
    """
    Find three entries in the expense report that sum to the target value and return their product.

    :param expense_report: List of integers representing the expense report.
    :param target: The target sum to find in the list (default is 2020).
    :return: The product of the three entries that sum to the target.
    """
    n = len(expense_report)
    expense_report.sort()
    for i in range(n - 2):
        left = i + 1
        right = n - 1
        while left < right:
            current_sum = (
                expense_report[i] + expense_report[left] + expense_report[right]
            )
            if current_sum == target:
                return expense_report[i] * expense_report[left] * expense_report[right]
            elif current_sum < target:
                left += 1
            else:
                right -= 1
    return None


def code(s: str):
    # Your code here

    entries = s.splitlines()
    entries = [int(entry) for entry in entries]

    return find_three_entries_product(entries)


if __name__ == "__main__":
    main(day=1, part=2, code=code)
