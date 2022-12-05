from turtle import Turtle

SCORE_BOARD_COLOR="white"
FONT=("Courier",80,"normal")
ALIGNMENT="center"

class ScoreBoard(Turtle):
    def __init__(self) -> None:
        super().__init__()
        self.color(SCORE_BOARD_COLOR)
        self.penup()
        self.hideturtle()
        self.l_score=0
        self.r_score=0
        self.update_scoreboard()
        
    def update_scoreboard(self):
        self.clear()
        self.goto(-100,200)
        self.write(self.l_score,align=ALIGNMENT,font=FONT)
        self.goto(100,200)
        self.write(self.r_score,align=ALIGNMENT,font=FONT)

    def l_point(self):
        self.l_score += 1
        self.update_scoreboard()
    
    def r_point(self):
        self.r_score += 1
        self.update_scoreboard()

    def reset_position(self):
        self.goto(0,0)