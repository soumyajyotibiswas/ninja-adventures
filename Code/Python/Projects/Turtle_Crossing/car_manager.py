from turtle import Turtle
import random

CAR_SHAPE='square'
CAR_COLORS=['red','green','violet','indigo','grey','orange','purple','black']
STARTING_POSITIONS=[item for sublist in [[(380,i*10),(380,i*-10)] for i in range(1,36)] for item in sublist]
START_MOVE_DIST=5
SPEED_INC=1

class CarManager:
    def __init__(self) -> None:
        self.all_cars=[]
        self.car_speed = START_MOVE_DIST

    def create_car(self):
        if random.randint(1,6) == 6:
            new_car=Turtle()
            new_car.shape(CAR_SHAPE)
            new_car.color(random.choice(CAR_COLORS))
            new_car.shapesize(stretch_len=2,stretch_wid=1)
            new_car.penup()
            new_car.goto(random.choice(STARTING_POSITIONS))
            self.all_cars.append(new_car)
    
    def car_move(self):
        for car in self.all_cars:
            car.backward(self.car_speed)

    def level_up(self):
        self.car_speed += SPEED_INC