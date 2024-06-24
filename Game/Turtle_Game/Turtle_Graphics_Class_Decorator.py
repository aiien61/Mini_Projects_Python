import random
from turtle import Turtle, Screen
from typing import List, Tuple


class Graphics:
    _colors = ["CornflowerBlue", "DarkOrchid", "IndianRed",
               "DeepSkyBlue", "LightSeaGreen", "wheat", "SlateGray", "SeaGreen"]

    def __init__(self, shape: str=None, color: str=None):
        self._pencil = Turtle()

        if shape:
            self._pencil.shape(shape)
        if color:
            self._pencil.color(color)

    @staticmethod
    def on_screen(func):
        def wrapped(*args, **kwargs):
            result = func(*args, **kwargs)
            screen = Screen()
            screen.exitonclick()
        return wrapped
    
    @staticmethod
    def draw_shape(pen: Turtle, number_of_sides: int, length: int):
        angle, rest = divmod(360, number_of_sides)
        if rest != 0:
            raise ValueError("number_of_sides must be able to divide 360.")

        for _ in range(number_of_sides):
            pen.forward(length)
            pen.left(angle)

    @staticmethod
    def random_color() -> Tuple[int]:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return r, g, b


    @on_screen
    def draw_a_square(self, side: int) -> bool:
        for _ in range(4):
            self._pencil.forward(side)
            self._pencil.left(90)
        return True
    
    @on_screen
    def draw_a_dashed_line(self, length: int) -> bool:
        steps_number, rest_steps = divmod(length, 10)
        for _ in range(steps_number):
            filled_length = steps_number // 2
            self._pencil.forward(filled_length)
            self._pencil.penup()
            self._pencil.forward(steps_number - filled_length)
            self._pencil.pendown()
        self._pencil.forward(rest_steps)
        return True
    
    @on_screen
    def draw_different_shapes_at_once(self, colored: bool=False) -> bool:
        length: int = random.randint(50, 200)
        for shape_side_n in range(3, 11):
            try:
                if colored:
                    self._pencil.color(random.choice(self._colors))
                self.draw_shape(self._pencil, shape_side_n, length)
            except ValueError:
                continue

    
    @on_screen
    def draw_a_random_walk(self, colored: bool = False, speed: int = 6) -> bool:
        if colored:
            Screen().colormode(255)

        grid_length: int = random.randint(30, 50)
        directions: List[int] = [0, 90, 180, 270]
        self._pencil.pensize(5)
        self._pencil.speed(speed)
        while True:
            if colored:
                self._pencil.color(self.random_color())
            self._pencil.setheading(random.choice(directions))
            self._pencil.forward(grid_length)

    @on_screen
    def draw_a_spirograph(self, size_of_gap: int, colored: bool = False):
        if colored:
            Screen().colormode(255)

        self._pencil.speed('fastest')

        round: int = 360 // size_of_gap
        for _ in range(round):
            if colored:
                self._pencil.color(self.random_color())
            self._pencil.circle(radius=100)
            self._pencil.setheading(self._pencil.heading() + size_of_gap)


def main():
    myplot = Graphics()
    # myplot.draw_a_square(100)
    # myplot.draw_a_dashed_line(200)
    # myplot.draw_different_shapes_at_once(colored=True)
    # myplot.draw_a_random_walk(colored=True, speed=6)
    myplot.draw_a_spirograph(size_of_gap=5, colored=True)


if __name__ == '__main__':
    main()