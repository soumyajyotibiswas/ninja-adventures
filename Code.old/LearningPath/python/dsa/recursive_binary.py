"""_summary_
"""


def recursive_binary_search(any_list, any_target):
    """_summary_

    Args:
        any_list (_type_): _description_
        any_target (_type_): _description_

    Returns:
        _type_: _description_
    """
    if len(any_list) == 0:
        return False
    mid_point = len(any_list) // 2
    if list[mid_point] == any_target:
        return True
    if list[mid_point] < any_target:
        return recursive_binary_search(any_list[mid_point + 1 :], any_target)
    return recursive_binary_search(any_list[:mid_point], any_target)


def verify(result):
    """_summary_

    Args:
        index (any): An item

    Returns:
        _type_: string
    """
    print(f"Target found: {result}")
