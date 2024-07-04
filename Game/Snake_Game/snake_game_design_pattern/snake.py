from turtle import Turtle

class Snake:
    STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]
    MOVE_DISTANCE = 20
    UP = 90
    DOWN = 270
    LEFT = 180
    RIGHT = 0

    def __init__(self):
        self.body_parts = []
        self.create_snake()
        self.head = self.body_parts[0]
    
    def create_snake(self) -> None:
        for position in self.STARTING_POSITIONS:
            self.add_part(position)
        return None

    def add_part(self, position: int) -> None:
        new_part: Turtle = Turtle(shape="square")
        new_part.color("white")
        new_part.penup()
        new_part.goto(position)
        self.body_parts.append(new_part)
        return None
    
    def grow(self) -> None:
        self.add_part(self.body_parts[-1].position())
        return None

    def move(self) -> None:
        for part_index in range(len(self.body_parts) - 1, 0, -1):
            new_x = self.body_parts[part_index - 1].xcor()
            new_y = self.body_parts[part_index - 1].ycor()
            self.body_parts[part_index].goto(new_x, new_y)
        
        self.head.forward(self.MOVE_DISTANCE)
        return None
    
    def up(self) -> None:
        if self.head.heading() != self.DOWN:
            self.head.setheading(self.UP)
        return None
    
    def down(self) -> None:
        if self.head.heading() != self.UP:
            self.head.setheading(self.DOWN)
        return None
    
    def left(self) -> None:
        if self.head.heading() != self.RIGHT:
            self.head.setheading(self.LEFT)
        return None
    
    def right(self) -> None:
        if self.head.heading() != self.LEFT:
            self.head.setheading(self.RIGHT)
        return None
    
    
