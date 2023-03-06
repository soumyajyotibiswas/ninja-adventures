from turtle import Turtle
import random

BALL_COLOR="white"
BALL_SHAPE="circle"
START_POS=(0,0)

class Ball(Turtle):
    def __init__(self) -> None:
        super().__init__()
        self.color(BALL_COLOR)
        self.shape(BALL_SHAPE)
        self.penup()
        self.goto(START_POS)
        self.x_move = random.choice(random.choice([[5,6],[-5,-6]]))
        self.y_move = random.choice(random.choice([[7,8],[-7,-8]]))
        self.move_speed=0.1

    def move(self):
        new_x=self.xcor() + self.x_move
        new_y=self.ycor() + self.y_move
        self.goto(new_x,new_y)

    def bounce(self,direction):
        if direction == 'y':
            self.y_move *= -1
        else:
            self.x_move *= -1
            self.move_speed *= 0.9
    

    
    def reset_pos(self,position):
        self.goto(START_POS)
        self.move_speed=0.1
        self.bounce(position)