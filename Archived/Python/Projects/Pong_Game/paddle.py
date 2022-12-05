from turtle import Turtle
PADDLE_SHAPE="square"
PADDLE_COLOR="white"

class Paddle(Turtle):
    def __init__(self, position:tuple) -> None:
        super().__init__()
        self.shape(PADDLE_SHAPE)
        self.color(PADDLE_COLOR)
        self.shapesize(stretch_wid=5,stretch_len=1)
        self.penup()
        self.goto(position)

    def go_up(self):
        if self.ycor() != 340:
            new_y=self.ycor() + 20
            self.goto(self.xcor(),new_y)

    def go_down(self):
        if self.ycor() != -340:
            new_y=self.ycor() - 20
            self.goto(self.xcor(),new_y)