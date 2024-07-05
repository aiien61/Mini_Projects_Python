from turtle import Turtle
from enum import Enum

class Paddle(Turtle):
    class Position(Enum):
        LEFT = 0
        RIGHT = 1

    def __init__(self, position: Position):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=5, stretch_len=1)
        self.penup()

        if position == self.Position.LEFT:
            self.goto(-350, 0)
        elif position == self.Position.RIGHT:
            self.goto(350, 0)

    def go_up(self):
        new_y = self.ycor() + 20
        self.goto(self.xcor(), new_y)

    def go_down(self):
        new_y = self.ycor() - 20
        self.goto(self.xcor(), new_y)