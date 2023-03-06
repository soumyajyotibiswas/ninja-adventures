from turtle import Turtle,Screen
import time
from snake import Snake
from food import Food
from scoreboard import Scoreboard
game_is_on=True

screen = Screen()
screen.setup(width=800,height=800)
screen.bgcolor("black")
screen.title("My Snake Game")
screen.tracer(0)
snake = Snake()
food = Food()
scoreboard=Scoreboard()

screen.listen()
screen.onkey(snake.up,"Up")
screen.onkey(snake.down,"Down")
screen.onkey(snake.left,"Left")
screen.onkey(snake.right,"Right")

while(game_is_on):
    screen.update()
    time.sleep(0.1)
    snake.move()

    #Detect collision
    if snake.head.distance(food) < 15:
        food.refresh()
        snake.extend()
        scoreboard.increase_score()

    #Detect collision to the wall
    if snake.head.xcor() > 380 or snake.head.xcor() < -380 or snake.head.ycor() > 370 or snake.head.ycor() < -380:
        scoreboard.game_over()
        game_is_on=False

    #Detect collision with tail
    for segment in snake.segments[1:]:
        if snake.head.distance(segment) < 10:
            scoreboard.game_over()
            game_is_on=False
            break

screen.exitonclick()