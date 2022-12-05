import random

# Game variables
pirate_ascii = """
                 _____
              .-" .-. "-.
            _/ '=(0.0)=' \_
          /`   .='|m|'=.   `\\
          \________________ /
      .--.__///`'-,__~\\\\~`
     / /6|__\// a (__)-\\\\
     \ \/--`((   ._\   ,)))
     /  \\  ))\  -==-  (O)(
    /    )\((((\   .  /)))))
   /  _.' /  __(`~~~~`)__
  //"\\,-'-"`   `~~~~\\~~`"-.
 //  /`"              `      `\\
//
"""
treasure_ascii='''
*******************************************************************************
          |                   |                  |                     |
 _________|________________.=""_;=.______________|_____________________|_______
|                   |  ,-"_,=""     `"=.|                  |
|___________________|__"=._o`"-._        `"=.______________|___________________
          |                `"=._o`"=._      _`"=._                     |
 _________|_____________________:=._o "=._."_.-="'"=.__________________|_______
|                   |    __.--" , ; `"=._o." ,-"""-._ ".   |
|___________________|_._"  ,. .` ` `` ,  `"-._"-._   ". '__|___________________
          |           |o`"=._` , "` `; .". ,  "-._"-._; ;              |
 _________|___________| ;`-.o`"=._; ." ` '`."\` . "-._ /_______________|_______
|                   | |o;    `"-.o`"=._``  '` " ,__.--o;   |
|___________________|_| ;     (#) `-.o `"=.`_.--"_o.-; ;___|___________________
____/______/______/___|o;._    "      `".o|o_.--"    ;o;____/______/______/____
/______/______/______/_"=._o--._        ; | ;        ; ;/______/______/______/_
____/______/______/______/__"=._o--._   ;o|o;     _._;o;____/______/______/____
/______/______/______/______/____"=._o._; | ;_.--"o.--"_/______/______/______/_
____/______/______/______/______/_____"=.o|o_.--""___/______/______/______/____
/______/______/______/______/______/______/______/______/______/______/______/
*******************************************************************************
'''
story_line="""
Rudger the terrible stored all his treasure on this remote island.
To find his treasure, you have to rise to all his challenges, hidden
across the island. Any wrong move will end your game. The islead has
a mind of its own and will keep changing your right choices, so best
of luck.
"""
path_choices = ['left','right']
move_choices = ['run','walk']
door_choices = ['wooden','stone']
win_path = random.choice(path_choices)
win_move = random.choice(move_choices)
win_door = random.choice(door_choices)

# Start of game
print(pirate_ascii)
print(story_line)
print(f"You are at the entry of the maze, you can either go {path_choices}")
user_input_path=input("Enter which direction you want to go: ").lower()
if user_input_path not in path_choices:
    print(f"Your choice of direction '{user_input_path}' is not valid. Try again!")
else:
    if user_input_path == win_path:
        print(f"You see nothing for miles ahead, do you want to {move_choices} for rest of the way?")
        user_input_move=input("Enter your move: ").lower()
        if user_input_move not in move_choices:
            print(f"Your choice of move '{user_input_move}' is not valid. Try again!")
        else:
            if user_input_move == win_move:
                print(f"Your choices have brought you to final hurdle. You see two doors, one has the treasure, and another who knows what. Choose well from {door_choices}")
                user_input_door=input("Enter your choice of door: ").lower()
                if user_input_door == win_door:
                    print(treasure_ascii,"\n","The treasure of Rudger the terrible is all yours. Congratulations!. Thank you for playing.")
                else:
                    print(f"As soon as you opened the '{user_input_door}' door you are consume by a dark entity. Game Over!")
            else:
                print(f"As soon as you started to '{user_input_move}' you are hit by an arrow. Game Over!")
    else:
        print(f"As soon as you stepped '{user_input_path}' you fall into a deep dark hole. Game Over!")
