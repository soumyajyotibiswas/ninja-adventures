import pandas,tabulate,os,random,time

symbol_choices = ['X','O']
cpu_player_name = "THE_MACHINE"
play_count = 0
rules = f"""
                                    [[[[[[[[[[[[// RULES //]]]]]]]]]]]]
                                Welcome to the classic game of Tic, tac, toe.

        > You will play with {cpu_player_name}.
        > The game is played on a grid that's 3 squares by 3 squares.
        > You choose either one of {symbol_choices}. Your opponent, in this case {cpu_player_name}, will choose the other one.
        > If you choose 'X' you will start the game, else {cpu_player_name} will be assigned 'X' and will start the game.
        > The first player to get 3 of their marks in a row (up, down, across, or diagonally) is the winner.
        > When all 9 squares are full, the game is over. If no player has 3 marks in a row, the game ends in a tie.
        > Choices
            >> You have to choose a cell which does NOT have a 'X' or 'O' already assigned to it. If you choose one which is already occupied, it will be considered an invalid input. The game ends after 3 invalid inputs, consecutive or not.
            >> Choose the cell value displayed as your choice. For example, if row 1 column 1 is your choice, enter the corresponding cell value of 11. Valid cell values are 11,12,13,21,22,23,31,32,33. If you choose anything else, it will be considered an invalid input. The game ends after 3 invalid inputs, consecutive or not.
        > If you leave your name as blank, will call you Bob :)
"""
cpu_player_ascii = '''
 ______________
||            ||
||    THE     ||
||  MACHINE   ||
||            ||
||____________||
|______________|
 \\############\\
  \\############\\
   \      ____    \ 
    \_____\___\____\

'''

def set_score_board():
    global score_board
    global player_choices
    score_board = pandas.DataFrame([['11','12','13'],['21','22','23'],['31','32','33']],columns=['C1','C2','C3'],index=['R1','R2','R3'])
    player_choices = {f"{user_input_symbol}":f"{user_input_name}",f"{cpu_input_symbol}":f"{cpu_player_name}"}

def display_score_board():
    print("\n--------------------------------------------------------------")
    print(f"\nPlayer choices - {player_choices}")
    print("\n--------------------------------------------------------------")
    print(f"MATCH SCORE BOARD | ROUND {play_count}")
    print(tabulate.tabulate(score_board, tablefmt = 'fancy_grid', showindex=False))
    print("\n--------------------------------------------------------------")

def validate_user_input_name():
    global user_input_name
    user_input_name = input("\nEnter your name: ")
    if len(user_input_name.strip()) == 0:
        user_input_name = 'BOB'
    else:
        user_input_name = user_input_name.upper()

def validate_user_input_symbol():
    global user_input_symbol
    invalid_input_count = 0
    while invalid_input_count < 3:
        user_input_symbol = (input(f"\nPlayer {user_input_name} enter either {symbol_choices} without the quotes : ")).upper()
        if user_input_symbol in symbol_choices:
            set_cpu_symbol_choice()
            break
        else:
            invalid_input_count += 1
            continue        
    if invalid_input_count == 3:
        raise ValueError(f"Maximum '{invalid_input_count}' invalid symbol choice attempts reached. Thank you for playing.")

def set_cpu_symbol_choice():
    global cpu_input_symbol
    if user_input_symbol == 'X':
        cpu_input_symbol = 'O'
    else:
        cpu_input_symbol = 'X'

def validate_user_input_cell_value():
    empty_slots = get_empty_slots()
    invalid_input_count = 0
    while invalid_input_count < 3:
        user_input_cell_choice = input(f"\nEnter either {empty_slots} without the quotes : ")
        if user_input_cell_choice not in empty_slots:
            invalid_input_count += 1
        else:
            return user_input_cell_choice
    if invalid_input_count == 3:
        raise ValueError(f"Maximum '{invalid_input_count}' invalid input choice attempts reached. Thank you for playing.")

def set_cpu_input_cell_value():
    empty_slots = get_empty_slots()
    return(random.choice(empty_slots))

def set_cell_value_to_input(cell_value,cell_symbol):
    global score_board
    a,b = [int(i) for i in str(cell_value)]
    a -= 1
    b -= 1
    score_board.iloc[a][b] = cell_symbol

def get_empty_slots():
    return([score_board.iloc[a][b] for a in range(3) for b in range(3) if score_board.iloc[a][b] not in symbol_choices])

def press_enter_to_continue():
    null_void = input("\nPress ENTER to continue.")
    null_void = os.system('clear')

def is_game_over():
    for symbol_choice in symbol_choices:
        for i in range(3):
            if (symbol_choice == score_board.iloc[i][0] == score_board.iloc[i][1] == score_board.iloc[i][2]) or (symbol_choice == score_board.iloc[0][i] == score_board.iloc[1][i] == score_board.iloc[2][i]):
                return(True,symbol_choice,player_choices[symbol_choice])
        if (symbol_choice == score_board.iloc[0][0] == score_board.iloc[1][1] == score_board.iloc[2][2]) or (symbol_choice == score_board.iloc[0][2] == score_board.iloc[1][1] == score_board.iloc[2][0]):
            return(True,symbol_choice,player_choices[symbol_choice])    
    return (False,symbol_choice,player_choices[symbol_choice])

def game_over(player_name):
    null_void = os.system('clear')
    print(f"\n{player_name} has won the game. Congratulations.")
    display_score_board()

def game_draw():
    null_void = os.system('clear')
    print("\nThe match is a Draw. We are at the end of the game. Thank you for playing")
    display_score_board()

def sleep_in_seconds(seconds):
    time.sleep(seconds)