from turtle import Turtle, Screen
import random
screen = Screen()
screen.setup(width=500,height=800)
user_bet=screen.textinput(title="User bet",prompt="Which color do you think will win?")
turtle_colors=['red','green','blue','orange','purple']
x_co=-250
y_co=-200
game_on=True

def build_turtles(x_co,y_co,colors):
    all_turtles=[]
    for turtle_color in colors: 
        new_turtle=Turtle()
        new_turtle.penup()
        new_turtle.shape(name="turtle")
        new_turtle.color(turtle_color)
        new_turtle.goto(x=x_co,y=y_co)
        y_co += 100
        all_turtles.append(new_turtle)

build_turtles(x_co,y_co,turtle_colors)

while(game_on):
    all_turtles=screen.turtles()
    for turtle in all_turtles:
        turtle.forward(random.randint(8,15))
        if turtle.xcor() >= 230:
            if turtle.pencolor() == user_bet:
                print(f"You won. The color that won was {turtle.pencolor()}.")
            else:
                print(f"You lost. The color that won was {turtle.pencolor()}.")
            game_on=False
            break

screen.exitonclick()