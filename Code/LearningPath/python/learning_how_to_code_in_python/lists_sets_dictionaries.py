"""
Exercise: an improved lottery! (Python 3.10)
Welcome to this coding exercise!

For this exercise we've provided you with a list of lottery players, and also with 6 random lottery numbers.

Find out the player with the most correct numbers, and print out their winnings and their name.

The random numbers are generated like this (I know we've not looked at the import keyword yet, bear with me on that one!):

import random
lottery_numbers = set(random.sample(range(22), 6))
And the list of players we've given you are:

players = [
    {'name': 'Rolf', 'numbers': {1, 3, 5, 7, 9, 11}},
    {'name': 'Charlie', 'numbers': {2, 7, 9, 22, 10, 5}},
    {'name': 'Anna', 'numbers': {13, 14, 15, 16, 17, 18}},
    {'name': 'Jen', 'numbers': {19, 20, 12, 7, 3, 5}}
]
Your task is to find who matched the most numbers, and print out a string with their name and the amount they won. For this exercise, assume there will only be 1 winner. Don't worry about two players matching the same amount of numbers.

For example:

Jen won 1000. 

The winnings are calculated with this formula:

winnings = 100 ** len(numbers_matched) 
"""

import random

lottery_numbers = set(random.sample(range(22), 6))

players = [
    {"name": "Rolf", "numbers": {1, 3, 5, 7, 9, 11}},
    {"name": "Charlie", "numbers": {2, 7, 9, 22, 10, 5}},
    {"name": "Anna", "numbers": {13, 14, 15, 16, 17, 18}},
    {"name": "Jen", "numbers": {19, 20, 12, 7, 3, 5}},
]

result = {}

for player in players:
    name, numbers = player.items()
    amount_won = 100 * len(lottery_numbers.intersection(set(numbers[1])))
    result[name[1]] = amount_won

name_list = list(result.keys())
amount_won_list = list(result.values())
max_amount_won = max(amount_won_list)
who_won_max = name_list[amount_won_list.index(max_amount_won)]

print(f"{who_won_max} won {max_amount_won}")
