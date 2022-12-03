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
machine_choices_values = list(machine_choices.values())
machine_choices_keys = list(machine_choices.keys())
machine_wins = [-2,1]
cpu_player_name = "THE_MACHINEEE"
user_input_name = ''
user_input = ''
null_input = ''
rules = f"""
                                    [[[[[[[[[[[[// RULES //]]]]]]]]]]]]
                            Welcome to the classic game of Rock, Paper and Scissors.

        > You will play a game for best of 5 with "THE MACHINE".
        > Rock beats scissors, paper beats rock and scissors beats paper.
        > If you want to choose
            >> ROCK : Enter '1' without the quotes
            >> PAPER : Enter '2' without the quotes
            >> SCISSORS : Enter '3' without the quotes
            >> Example: // If your choice is Rock, just enter 1 //
            >> You will get a prompt each round to help you with the choices.
            >> The prompt will be {machine_choices}
            >> The player with maximum number of wins, will win the game.
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
    print(f"\n{what_to_print}")

def map_choice_to_key(choice_of_play):
    index_of_choice = machine_choices_values.index(choice_of_play)
    return (machine_choices_keys[index_of_choice])

def get_machine_choice():
    return(random.choice(machine_choices_values))

def validate_user_input():
    global user_input
    user_input = input(f"\nEnter either {machine_choices}  : ")
    if len((str(user_input)).strip()) == 0:
        return False
    elif int(user_input) not in machine_choices_values:
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
    machine_c_key = map_choice_to_key(machine_c)
    user_c_key = map_choice_to_key(user_input)
    custom_print(f"{user_input_name} chose {user_c_key}:{user_input} and {cpu_player_name} chose {machine_c_key}:{machine_c}.")
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
    custom_print(score_board)

def screen_clear():
    clear_screen = os.system('clear')

def play_game():
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
            null_input = input("\nPress ENTER to continue")
            screen_clear()
        if play_count > max_plays:
            break
        retry_count += 1
    final_scoring()

def final_scoring():
    if play_count > max_plays:
        custom_print(f"Final score after max no plays {max_plays} is: '{user_input_name}':{score_board.sum()[f'{user_input_name}_score_card']}, {cpu_player_name}:{score_board.sum()[f'{cpu_player_name}_score_card']} and draws:{score_board.sum()['Draws']}.")
        custom_print(score_board)
        if player_score > machine_score:
            custom_print(f"{user_input_name} wins the game.")
        elif player_score < machine_score:
            custom_print(f"{cpu_player_name} wins the game.")
        else:
            custom_print(f"Its a DRAW between {user_input_name} and {cpu_player_name}.")
        custom_print(f"Max no plays {max_plays} reached. Thank you for playing. Press ENTER to EXIT !!")
    else:
        custom_print(f"Max invalid inputs of {max_retries} reached. Press ENTER to EXIT !!")
    null_input = input()

def set_scoreboard():
    global score_board
    score_board = pandas.DataFrame(columns=[f"{user_input_name}_score_card",f"{cpu_player_name}_score_card",'Draws'])

def main():
    custom_print(rules)
    null_input = input("If you understand the rules, press ENTER to continue: ")
    screen_clear()
    validate_user_input_name()
    screen_clear()
    custom_print(f"The game will be played between {user_input_name} and {cpu_player_name}.")
    custom_print(f"{cpu_player_name} says Hello!!")
    custom_print(cpu_player_ascii)
    null_input = input("\nPress ENTER to continue: ")
    set_scoreboard()
    screen_clear()
    play_game()

main()