"""
1. Add new movies to my collection
1.1. Keep track of all my movies.
2. List all movies in my collection.
2.1. So I can see what all movies I have.
3. Find a movie using the movie title.
3.3. So I can locate a specific movie easily when the collection grows.
"""

import json
from typing import Dict

movie_list = [
    {"title": "Movie1", "director": "Director1", "year": "1992", "genre": "Horror"},
    {"title": "Movie2", "director": "Director2", "year": "1993", "genre": "Comedy"},
    {"title": "Movie3", "director": "Director1", "year": "1992", "genre": "Horror"},
    {"title": "Movie4", "director": "Director2", "year": "1992", "genre": "Comedy"},
]
valid_operations = ["add", "list", "find", "q"]
valid_fields_to_find = ["title", "director", "year", "genre"]
USER_DISPLAY = """
Enter operation of choice:
add - to add movie
list - to list all movies
find - to find a movie
q - to quit
"""


def check_empty_string(string_to_check: str):
    """_summary_

    Args:
        string_to_check (str): String to check for null or empty.

    Raises:
        ValueError: "String is empty or null."

    Returns:
        str: string_to_check
    """
    if len(string_to_check) != 0 and not string_to_check.isspace():
        return string_to_check
    else:
        raise ValueError("String is empty or null.")


def check_if_movie_exists(movie_to_add: Dict):
    """Checks if movie already exists

    Args:
        movie (Dict): Movie to add

    Raises:
        ValueError: "{movie} already present in database."
    """
    for movie in movie_list:
        if list(movie_to_add.values()) == list(movie.values()):
            raise ValueError(f"{movie_to_add} already present in database.")


def check_if_input_values_are_empty(movie_to_add):
    """_summary_

    Args:
        movie_to_add (_type_): _description_
    """
    for _value in movie_to_add.values():
        check_empty_string(_value)


def add_movie_to_list(title: str, director: str, year: str, genre: str):
    """_summary_

    Args:
        title (str): _description_
        director (str): _description_
        year (str): _description_
        genre (str): _description_

    Raises:
        e: _description_
    """
    try:
        movie_to_add = {
            "title": title,
            "director": director,
            "year": year,
            "genre": genre,
        }
        check_if_input_values_are_empty(movie_to_add)
        check_if_movie_exists(movie_to_add)
        movie_list.append(movie_to_add)
    except Exception as exception:
        raise exception


def is_operation_valid(choice: str):
    """_summary_

    Args:
        user_choice (_type_): _description_

    Raises:
        ValueError: _description_
    """
    if choice not in valid_operations:
        raise ValueError(
            f"{choice} is not a valid operation. Chose from {','.join(valid_operations)}."
        )


def is_input_field_valid(field):
    """_summary_

    Args:
        field (_type_): _description_

    Raises:
        KeyError: _description_
    """
    if field not in valid_fields_to_find:
        raise KeyError(
            f"{field} is not a valid field to find by. Try from {valid_fields_to_find}."
        )


def find_movie_by_input(field, value):
    """_summary_

    Args:
        field (_type_): _description_
        value (_type_): _description_

    Returns:
        _type_: _description_
    """
    check_empty_string(field)
    check_empty_string(value)
    is_input_field_valid(field)
    return_value = []
    for movie in movie_list:
        if movie[field] == value:
            return_value.append(movie)
    return return_value


def add_movie():
    """_summary_"""
    title = input("Enter title of the movie: ")
    director = input("Enter director of the movie: ")
    year = input("Enter year of the movie: ")
    genre = input("Enter genre of the movie: ")
    add_movie_to_list(title, director, year, genre)


def list_movies():
    """_summary_"""
    print(json.dumps(movie_list, indent=4))


def find_movie():
    """_summary_

    Raises:
        NotImplementedError: _description_
    """
    user_choice_field = input(
        f"Enter field of the movie to find it by, valid choices are {valid_fields_to_find}: "
    )
    user_choice_field_value = input("Enter value of the choice: ")
    movie_found = find_movie_by_input(user_choice_field, user_choice_field_value)
    print(json.dumps(movie_found, indent=4))


def operation(choice: str):
    """_summary_

    Args:
        choice (str): _description_
    """
    if choice == "add":
        add_movie()
    elif choice == "list":
        list_movies()
    elif choice == "find":
        find_movie()


def main():
    """_summary_"""
    while True:
        user_choice = check_empty_string((input(USER_DISPLAY)).lower())
        is_operation_valid(user_choice)
        operation(user_choice)
        if user_choice == "q":
            break


if __name__ == "__main__":
    main()
