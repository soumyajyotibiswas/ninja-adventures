# Learning Algorithms

## Linear search

Start at the front and work up to the end.

* Define the problem.
* Define the input.
* Define the output.
* Start at the beginning.
* Move sequentially.
* Compare current value to target.
* Reach end of list.
* Does not matter if the range is sorted or not.
* It has to produce a result which is consistent for the same set of input.

```python
def linear_search(any_list, any_target):
    """Returns the index position of the target if found, else returns None

    Args:
        list (List[any]): List of items
        target (any): Target item

    Returns:
        _type_: any | None
    """
    for count, value in enumerate(any_list):
        if value == any_target:
            return count
    return None
```

## Binary search

* Input - sorted list.
* Output - Either the searched value or does not exist.
* Go to middle position, if match return or if smaller, eliminate everything above middle, and if low, eliminate everything lower than middle value. Repeat.

```python
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
```
