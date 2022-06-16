import colorgram, random, os
from turtle import Screen, Turtle

turtle=Turtle()
screen=Screen()

def fetch_colors_from_painting():
    return([tuple(x.rgb) for x in colorgram.extract(f'{os.path.dirname(os.path.realpath(__file__))}/random.jpg',10) if not sum(x.rgb) > 255*3-50])

colors=fetch_colors_from_painting()
turtle.shape("circle")
turtle.pensize(5)
turtle.hideturtle()
turtle.penup()
turtle.setposition(-250,-250)
starting_pos=turtle.position()
screen.colormode(255)
def paint():
    for i in range(1,6):
        for j in range(0,6):
            turtle.color(random.choice(colors))
            turtle.dot()
            turtle.forward(100)
        turtle.setposition(-250,-250+(i*100))

paint()

screen.exitonclick()