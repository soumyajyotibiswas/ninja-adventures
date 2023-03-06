"""
Binary search algorithm
"""


def binary_search(any_list, any_target):
    """Binary search algorithm

    Args:
        any_list (_type_): _description_
        any_target (_type_): _description_

    Returns:
        _type_: _description_
    """
    first_position = 0
    last_position = len(any_list) - 1

    while first_position <= last_position:
        mid_point = (first_position + last_position) // 2

        if any_list[mid_point] == any_target:
            return mid_point
        elif any_list[mid_point] < any_target:
            first_position = mid_point + 1
        else:
            last_position = mid_point - 1

    return None


def verify(result):
    """_summary_

    Args:
        index (any): An item

    Returns:
        _type_: string
    """
    if result is not None:
        return f"Target found at index: {result}"
    return "Target not found."
