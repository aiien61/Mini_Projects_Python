from turtle import Turtle
from typing import List

STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10
FINISH_LINE_Y = 280

class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.penup()
        self.go_to_start()
        self.setheading(90)

    def go_up(self) -> None:
        self.forward(MOVE_DISTANCE)
        return None
    
    def collides_with_car(self, cars: List[Turtle]) -> bool:
        for car in cars:
            if self.distance(car) < 20:
                return True
        return False
    
    def is_at_finish_line(self) -> bool:
        return True if self.ycor() > FINISH_LINE_Y else False
    

    def go_to_start(self):
        self.goto(STARTING_POSITION)
