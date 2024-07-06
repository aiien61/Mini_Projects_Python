import random
from turtle import Turtle
from typing import List

COLORS = ["red", "orange", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10

class CarManager:
    def __init__(self, road_length: int, road_width: int) -> None:
        self.all_cars: List[Turtle] = []
        self.car_speed: int = STARTING_MOVE_DISTANCE
        self.road_length: int = road_length
        self.road_width: int = road_width


    def create_car(self) -> None:
        random_chance: int = random.randint(1, 6)
        if random_chance != 1:
            return None
        new_car: Turtle = Turtle("square")
        new_car.shapesize(stretch_wid=1, stretch_len=2)
        new_car.penup()
        new_car.color(random.choice(COLORS))
        random_y: int = random.randint(-self.road_width / 2, self.road_width / 2)
        new_car.goto(self.road_length / 2, random_y)
        self.all_cars.append(new_car)
        return None
    
    def move_cars(self) -> None:
        for car in self.all_cars:
            car.backward(self.car_speed)
        return None
    
    def level_up(self) -> None:
        self.car_speed += MOVE_INCREMENT
        return None
