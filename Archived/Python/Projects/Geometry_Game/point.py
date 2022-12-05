from __future__ import annotations
import imp
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from rectangle import Rectangle
from turtle import Turtle

class Point:
    """_summary_
    """
    def __init__(self, x:float, y:float) -> None:
        """_summary_

        Args:
            x (float): _description_
            y (float): _description_
        """
        self.x = x
        self.y = y
        self.coordinates = (x,y)
    
    def is_inside_rectangle(self, rectangle: Rectangle) -> bool:
        """_summary_

        Args:
            rectangle (Rectangle): _description_

        Returns:
            bool: _description_
        """
        if rectangle.lower_left.x < self.x < rectangle.upper_right.x and rectangle.lower_left.y < self.y < rectangle.upper_right.y:
            return True
        else:
            return False

    def calculate_distance(self, from_object: Point) -> float:
        """_summary_

        Args:
            from_object (Point): _description_

        Returns:
            float: _description_
        """
        return(round(((self.x - from_object.x)**2 + (self.y - from_object.y)**2)** 0.5,2))

class GuiPoint(Point):
    """_summary_

    Args:
        Point (_type_): _description_
    """
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y)
        self.draw_point()
        pass
    def draw_point(self, size=5, color='red'):
        point_turtle=Turtle()
        point_turtle.penup()
        point_turtle.goto(self.coordinates)
        point_turtle.hideturtle()
        point_turtle.dot(size,color)

