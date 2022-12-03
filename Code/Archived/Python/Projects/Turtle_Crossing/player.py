from turtle import Turtle
START_POS=(0,-380)
MOVE_DISTANCE=10
FINISH_LINE_Y=380
PLAYER_SHAPE="turtle"

class Player(Turtle):
    def __init__(self) -> None:
        super().__init__()
        self.shape(PLAYER_SHAPE)
        self.penup()
        self.go_to_start()
        self.setheading(90)

    def move_player(self):
        self.forward(MOVE_DISTANCE)

    def is_at_finish_line(self):
        if self.ycor() >= 370:
            return True
        else:
            return False

    def go_to_start(self):
        self.goto(START_POS)