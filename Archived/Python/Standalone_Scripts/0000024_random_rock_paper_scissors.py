import random

# Game variables
intro_message='''
Welcome to the game of rock, paper and scissors.
This classic game has been played for ages.
The game has three elements, rock, paper and scissors.
Rock beats scissors, paper beats rock and scissors beats paper.
This game will allow you to choose between rock, paper or scissors.
The computer will choose a random element.
'''
ascii_robot = '''
                  ,--.    ,--.
                 ((O ))--((O ))
               ,'_`--'____`--'_`.
              _:  ____________  :_
             | | ||::::::::::|| | |
             | | ||::::::::::|| | |
             | | ||::::::::::|| | |
             |_| |/__________\| |_|
               |________________|
            __..-'            `-..__
         .-| : .----------------. : |-.
       ,\ || | |\______________/| | || /.
      /`.\:| | ||  __  __  __  || | |;/,'\\
     :`-._\;.| || '--''--''--' || |,:/_.-':
     |    :  | || .----------. || |  :    |
     |    |  | || '-ROBOTIE--' || |  |    |
     |    |  | ||   _   _   _  || |  |    |
     :,--.;  | ||  (_) (_) (_) || |  :,--.;
     (`-'|)  | ||______________|| |  (|`-')
      `--'   | |/______________\| |   `--'
             |____________________|
              `.________________,'
               (_______)(_______)
               (_______)(_______)
               (_______)(_______)
               (_______)(_______)
              |        ||        |
              '--------''--------'
'''
element_associations={'rock':1,'paper':2,'scissors':3}
player_win_combinations=[-2,1]

# Game start
print(intro_message)
print("You will play against the computer. Say hello to robotie!")
print(ascii_robot)
computer_choice=random.choice(list(element_associations.keys()))
player_choice=input("Enter your choice between rock, paper or scissors: ").lower()
if player_choice not in list(element_associations.keys()):
    print(f"Your choice of '{player_choice}' is not a valid input, it has to be between rock, paper and scissors. Try again!")
else:
    if computer_choice == player_choice:
        print(f"Computer choose {computer_choice} and the player choose {player_choice}. It is a draw.")
    elif element_associations[player_choice] - element_associations[computer_choice] in player_win_combinations:
        print(f"Computer choose {computer_choice} and the player choose {player_choice}. The player wins.")
    else:
        print(f"Computer choose {computer_choice} and the player choose {player_choice}. The compuer wins.")