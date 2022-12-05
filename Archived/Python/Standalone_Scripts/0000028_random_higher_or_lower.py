import random

# Global var
user_score=0
game_choices=['high','low']
intro_message='''

  _   _ _       _                    _                  
 | | | (_) __ _| |__     ___  _ __  | |    _____      __
 | |_| | |/ _` | '_ \   / _ \| '__| | |   / _ \ \ /\ / /
 |  _  | | (_| | | | | | (_) | |    | |__| (_) \ V  V / 
 |_| |_|_|\__, |_| |_|  \___/|_|    |_____\___/ \_/\_/  
          |___/                                         

This is an addictive game, where you have to out-guess the computer.
The computer is thinking about an integer between 1 and 1000. You will
be displayed a an integer between 1 and 1000. You have to guess if the
integer the computer is thinking about is higher or lower than your
integer. If you guess correctly, the game continues, and if you do not
guess correctly, the game ends.
Note: You and the computer will not have two same integers at the same
time.

Example:
Guess if the computer has a number in mind higer or lower than '15'. Enter high or low. [eg: high] --> high
Your guess was correct. Your score is '1'.
Guess if the computer has a number in mind higer or lower than '303'. Enter high or low. [eg: high] --> low
Your guess was not correct. Game over! Your score is '1'.
'''
# Play game
print(intro_message)
while(True):
    computer_choice=random.randint(1,1000)
    for_user_choice=random.randint(1,1000)
    while(for_user_choice == computer_choice):
        for_user_choice=random.randint(1,1000)
    user_choice=input(f"Guess if the computer has a number in mind higer or lower than '{for_user_choice}'. Enter high or low. [eg: high] --> ").lower()
    if user_choice not in game_choices:
        raise Exception(f"Your choice of '{user_choice}' is not valid. Choose from '{game_choices}'. Try running the game again!")
    if (computer_choice > for_user_choice and user_choice == 'high') or (computer_choice < for_user_choice and user_choice == 'low'):
        user_score += 1
        print(f"Your guess was correct. Your score is '{user_score}'.")
    else:
        print(f"Your guess was not correct. Game over! Your score is '{user_score}'.")
        break
    