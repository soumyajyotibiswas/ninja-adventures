"""
Classic Rock, Paper, Scissors
    -- user_input : [Rock || Paper || Scissors].
    -- user_input_name : <User name>
    -- Game best of FIVE.
    -- Max retry of wrong input = 3.

--@soumyajyotibiswas
"""

import random,pandas,os

score_board = ''
draw_score = machine_score = player_score = 0
play_count = retry_count = 1
max_plays = 5
max_retries = 3
machine_choices = {'Rock':1, 'Paper':2, 'Scissors':3}
machine_wins = [-2,1]
cpu_player_name = "THE_MACHINEEE"
user_input_name = ''
user_input = ''
null_input = ''
rules = """
            [[[[[[[[[[[[// RULES //]]]]]]]]]]]]
Welcome to the classic game of Rock, Paper and Scissors.
    > You will play a game for best of 5 with "THE MACHINE".
    > Rock beats scissors, paper beats rock and scissors beats paper.
    > If you want to choose
        >> ROCK : Enter '1' without the quotes
        >> PAPER : Enter '2' without the quotes
        >> SCISSORS : Enter '3' without the quotes
        >> Example: // If your choice is Rock, just enter 1 //
    > Input other than 1,2,3 will be considered invalid and the game will end after 3 invalid inputs, consecutive or not.
    > If you leave your name as blank, will call you Bob :)
"""
cpu_player_ascii = '''
 ______________
||            ||
||    THE     ||
|| MACHINEEE  ||
||            ||
||____________||
|______________|
 \\############\\
  \\############\\
   \      ____    \ 
    \_____\___\____\

'''

def custom_print(what_to_print):
    print(f"\n{what_to_print}\n")

def get_machine_choice():
    return(random.choice(list(machine_choices.values())))

def validate_user_input():
    global user_input
    user_input = input("\nEnter either 'Rock':1, 'Paper':2 or 'Scissors':3: ")
    if len((str(user_input)).strip()) == 0:
        return False
    elif int(user_input) not in list(machine_choices.values()):
        return False
    else:
        user_input = int(user_input)
        return True

def validate_user_input_name():
    global user_input_name
    user_input_name = input("\nEnter your name: ")
    if len(user_input_name.strip()) == 0:
        user_input_name = 'Bob'

def get_match_winner():
    machine_c = get_machine_choice()
    custom_print(f"{user_input_name} chose {user_input} and {cpu_player_name} chose {machine_c}.")
    custom_print("REMINDER !! // // Rock(1) beats scissors, paper(2) beats rock and scissors beats paper(3) // //")
    if machine_c == user_input:
        global draw_score
        draw_score += 1
        score_board['Draws'][(play_count-1)] = 1
        custom_print(f"Round '{play_count}' is a DRAW !!")
    elif (machine_c - user_input) in machine_wins:
        global machine_score
        machine_score += 1
        score_board[f'{cpu_player_name}_score_card'][(play_count-1)] = 1
        custom_print(f"Round '{play_count}' goes to '{cpu_player_name}'")
    else:
        global player_score
        player_score += 1
        score_board[f'{user_input_name}_score_card'][(play_count-1)] = 1
        custom_print(f"Round '{play_count}' goes to '{user_input_name}'")
    custom_print(f"Score after round '{play_count}' is, '{user_input_name}':{player_score}, {cpu_player_name}:{machine_score} and draws:{score_board.sum()['Draws']}.")   
    print(score_board)

def play_game():
    clear_screen = os.system('clear')
    global retry_count
    global play_count
    global score_board
    while retry_count <= max_retries:
        while play_count <= max_plays:            
            return_user_input = validate_user_input()
            if return_user_input == False:
                break
            score_board.loc[f'Round {play_count}'] = [0,0,0]
            get_match_winner()
            play_count += 1
            null_input = input("\nPress ANY key to continue")
            clear_screen = os.system('clear')
        if play_count > max_plays:
            break
        retry_count += 1
    final_scoring()

def final_scoring():
    if play_count > max_plays:
        custom_print(f"Final score after max no plays {max_plays} is: '{user_input_name}':{score_board.sum()[f'{user_input_name}_score_card']}, {cpu_player_name}:{score_board.sum()[f'{cpu_player_name}_score_card']} and draws:{score_board.sum()['Draws']}.")
        print(score_board)
        if player_score > machine_score:
            custom_print(f"{user_input_name} wins the game.")
        elif player_score < machine_score:
            custom_print(f"{cpu_player_name} wins the game.")
        else:
            custom_print(f"Its a DRAW between {user_input_name} and {cpu_player_name}.")
        custom_print(f"Max no plays {max_plays} reached. Thank you for playing. Press ANY key to EXIT !!")
    else:
        custom_print(f"Max invalid inputs of {max_retries} reached. Press ANY key to EXIT !!")
    null_input = input()

def set_scoreboard():
    global score_board
    score_board = pandas.DataFrame(columns=[f"{user_input_name}_score_card",f"{cpu_player_name}_score_card",'Draws'])

def main():
    custom_print(rules)
    null_input = input("If you understand the rules, press ANY key to continue: ")
    validate_user_input_name()
    custom_print(f"The game will be played between {user_input_name} and {cpu_player_name}.")
    custom_print(f"{cpu_player_name} says Hello!!")
    custom_print(cpu_player_ascii)
    null_input = input("\nPress ANY key to continue: ")
    set_scoreboard()
    play_game()

main()