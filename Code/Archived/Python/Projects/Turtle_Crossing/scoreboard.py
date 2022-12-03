from turtle import Turtle
FONT=("Courier",10,"normal")
ALIGNMENT="center"
START_POS=(-370,370)
class Scoreboard(Turtle):
    def __init__(self) -> None:
        super().__init__()
        self.level=0
        self.hideturtle()
        self.penup()
        self.goto(START_POS)
        self.update_score()

    def update_score(self):
        self.clear()
        self.write(f"Current Level: {self.level}",align=ALIGNMENT,font=FONT)

    def increase_level(self):
        self.level += 1
        self.update_score()

    def game_over(self):
        self.goto(0,0)
        self.write(f"GAME OVER",align=ALIGNMENT,font=FONT)