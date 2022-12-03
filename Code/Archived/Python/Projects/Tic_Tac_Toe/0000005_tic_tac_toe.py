"""
Classic Tic,tac,toe
    -- user_symbol_choice : [X] | [Y]
    -- user_cell_choice : [X] | [Y]
    -- user_input_name : <User name>
    -- Max retry of wrong input = 3.

--@soumyajyotibiswas
"""

import custom_config as cc

def set_game_prechecks():
    print(f"\n{cc.rules}")
    cc.press_enter_to_continue()
    cc.validate_user_input_name()
    print(f"\n{cc.user_input_name} will play against {cc.cpu_player_name}. {cc.cpu_player_name} says Hello :)")
    print(f"{cc.cpu_player_ascii}")
    cc.press_enter_to_continue()
    cc.validate_user_input_symbol()
    cc.set_score_board()

def cpu_plays():
    cpu_input_cell_value = cc.set_cpu_input_cell_value()
    cc.set_cell_value_to_input(cpu_input_cell_value,cc.cpu_input_symbol)

def user_plays():
    user_input_cell_value = cc.validate_user_input_cell_value()
    cc.set_cell_value_to_input(user_input_cell_value,cc.user_input_symbol)

def play_game():
    cc.play_count = 1
    while cc.play_count < 5:
        cc.display_score_board()
        if cc.user_input_symbol == 'X':
            user_plays()
            cpu_plays()
            print(f"\n{cc.cpu_player_name} is making its choice. Please wait")
            cc.sleep_in_seconds(2)
        else:
            cpu_plays()
            print(f"\n{cc.cpu_player_name} is making its choice. Please wait.")
            cc.sleep_in_seconds(2)
            cc.display_score_board()
            user_plays()
        game_status = cc.is_game_over()
        if game_status[0] == True:
            cc.game_over(game_status[2])
            break
        else:
            cc.display_score_board()
            print(f"\nEnd of round {cc.play_count}")
            cc.press_enter_to_continue()
        cc.play_count += 1    
    if cc.play_count == 5:
        empty_slots = cc.get_empty_slots()
        cc.set_cell_value_to_input(empty_slots[0],'X')    
    game_status = cc.is_game_over()
    if cc.play_count == 5 and game_status[0] == True:
        cc.game_over(game_status[2])
    elif cc.play_count == 5 and game_status[0] == False:
        cc.game_draw()
    cc.press_enter_to_continue()

def main():
    try:
        set_game_prechecks()
        cc.press_enter_to_continue()
        play_game()
    except ValueError as e:
        print("\n" + str(e))
        cc.press_enter_to_continue()
    except Exception as e:
        print("\n" + str(e))
        print("Unknown error encountered. Exiting.")

main()
