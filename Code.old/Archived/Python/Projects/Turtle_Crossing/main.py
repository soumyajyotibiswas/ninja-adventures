from turtle import Turtle,Screen
from car_manager import CarManager
import time
from player import Player
from scoreboard import Scoreboard

SCREEN_SETUP_SIZE=900
SCREEN_SIZE=800
SCREEN_BG_COLOR='white'
GAME_IS_ON=True

screen=Screen()
screen.setup(width=SCREEN_SETUP_SIZE,height=SCREEN_SETUP_SIZE)
screen.screensize(canvheight=SCREEN_SIZE,canvwidth=SCREEN_SIZE)
screen.bgcolor(SCREEN_BG_COLOR)
screen.tracer(0)
screen.title("Turtle car crossing")
screen.listen()

scoreboard=Scoreboard()

#Create the initial cars
car_manager=CarManager()

#Create player
player=Player()
screen.onkeypress(player.move_player,"Up")

while(GAME_IS_ON):
    time.sleep(0.1)
    screen.update()

    car_manager.create_car()
    car_manager.car_move()
    
    #Detect car collision
    for car in car_manager.all_cars:
        if car.distance(player) < 20:
            GAME_IS_ON=False
            scoreboard.game_over()
            break
    
    #Detect turtle finish
    if player.is_at_finish_line():
        player.go_to_start()
        car_manager.level_up()
        scoreboard.increase_level()



screen.exitonclick()