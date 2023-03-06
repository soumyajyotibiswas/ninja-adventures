from turtle import Turtle, Screen
from paddle import Paddle
from ball import Ball
import time
from scoreboard import ScoreBoard

SCREEN_BG_COLOR="black"
SCREEN_SIZE=800
SCREEN_TITLE="Pong"
GAME_IS_ON=True
L_PADDLE_POS=(-350,0)
R_PADDLE_POS=(350,0)
GAME_OVER_SCORE=5

screen=Screen()
screen.bgcolor(SCREEN_BG_COLOR)
screen.screensize(canvheight=SCREEN_SIZE,canvwidth=SCREEN_SIZE)
screen.setup(width=SCREEN_SIZE,height=SCREEN_SIZE)
screen.title(SCREEN_TITLE)
screen.tracer(0)

scoreboard=ScoreBoard()

ball=Ball()

l_paddle=Paddle(L_PADDLE_POS)
r_paddle=Paddle(R_PADDLE_POS)

screen.listen()
screen.onkey(r_paddle.go_up,"Up")
screen.onkey(r_paddle.go_down,"Down")
screen.onkey(l_paddle.go_up,"w")
screen.onkey(l_paddle.go_down,"s")


while(GAME_IS_ON):
    time.sleep(ball.move_speed)
    screen.update()
    ball.move()

    # Detect collision with wall
    if ball.ycor() > 380 or ball.ycor() < -380:
        ball.bounce('y')

    # Detect collision with paddle
    if ball.distance(r_paddle) < 50 and ball.xcor() > 340 or ball.distance(l_paddle) < 50 and ball.xcor() < -340:
        ball.bounce('x')

    # Detect miss by paddle
    if ball.xcor() > 360:
        ball.reset_pos('x')
        scoreboard.l_point()

    if ball.xcor() < -350:
        ball.reset_pos('y')
        scoreboard.r_point()

    # Game over    
    if scoreboard.l_score == GAME_OVER_SCORE or scoreboard.r_score == GAME_OVER_SCORE:
        scoreboard.reset_position()
        scoreboard.write("GAME_OVER")
        break

screen.exitonclick()