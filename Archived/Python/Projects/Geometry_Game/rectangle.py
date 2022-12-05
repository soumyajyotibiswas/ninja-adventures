from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from point import Point    
from turtle import Turtle

class Rectangle():
    """_summary_
    """
    def __init__(self, lower_left: Point, upper_right: Point) -> None:
        """_summary_

        Args:
            lower_left (Point): _description_
            upper_right (Point): _description_
        """
        self.lower_left = lower_left
        self.upper_right = upper_right
        self.area = self.area_of_rectangle()

    def area_of_rectangle(self) -> float:
        """_summary_

        Returns:
            float: _description_
        """
        return (round(abs((self.lower_left.x - self.upper_right.x)*(self.lower_left.y - self.upper_right.y)),2))

class GuiRectangle(Rectangle):
    """_summary_

    Args:
        Rectangle (_type_): _description_
    """
    def __init__(self, lower_left: Point, upper_right: Point) -> None:
        super().__init__(lower_left, upper_right)
        self.draw_rectangle()
        pass

    def draw_rectangle(self):
        rect_turtle=Turtle()
        rect_turtle.penup()
        rect_turtle.goto(self.lower_left.coordinates)
        rect_turtle.pendown()
        rect_turtle.goto(self.upper_right.x,self.lower_left.y)
        rect_turtle.left(90)
        rect_turtle.goto(self.upper_right.x,self.upper_right.y)
        rect_turtle.left(90)
        rect_turtle.goto(self.lower_left.x,self.upper_right.y)
        rect_turtle.left(90)
        rect_turtle.goto(self.lower_left.x,self.lower_left.y)
        rect_turtle.hideturtle()