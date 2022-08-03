from cmath import rect
import turtle
from point import Point,GuiPoint
from rectangle import Rectangle,GuiRectangle
from random import randint
from turtle import Turtle

def generate_random_int(where: str = 'upper') -> int:
    """_summary_

    Args:
        where (str, optional): _description_. Defaults to 'upper'.

    Returns:
        int: _description_
    """
    if where == 'lower':
        return (randint(0,99))
    else:
        return (randint(200,299))

def generate_upper_right_point() -> Point:
    """_summary_

    Returns:
        Point: _description_
    """
    return (Point(x=generate_random_int(),y=generate_random_int()))

def generate_lower_left_point() -> Point:
    """_summary_

    Returns:
        Point: _description_
    """
    return (Point(x=generate_random_int('lower'),y=generate_random_int('lower')))

# rectangle = Rectangle(lower_left=generate_lower_left_point(),upper_right=generate_upper_right_point())

# print(f"Rectangle co-ordinates:\nLower Left x: {rectangle.lower_left.x}\nLower Left y: {rectangle.lower_left.y}\nUpper Right x: {rectangle.upper_right.x}\nUpper Right y: {rectangle.upper_right.y}")

# user_point=Point(x=float(input("Guess x: ")),y=float(input("Guess y: ")))

# print(f"Was your point inside rectangle? {user_point.is_inside_rectangle(rectangle=rectangle)}")

# print(f"Area of the rectangle is : {rectangle.area}")

gui_rectangle=GuiRectangle(lower_left=generate_lower_left_point(),upper_right=generate_upper_right_point())
gui_point=GuiPoint(x=float(input("Guess x: ")),y=float(input("Guess y: ")))
print(f"Was your point inside rectangle? {gui_point.is_inside_rectangle(rectangle=gui_rectangle)}")
turtle.done()