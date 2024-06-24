import random
from turtle import Turtle, Screen


class HirstPaint:
    colors = [(246, 242, 235), (248, 242, 245), (240, 246, 242), (239, 242, 247), (198, 165, 116),
              (144, 79, 55), (221, 201, 138), (58, 93, 121), (167, 153, 48), (132, 34, 23),
              (137, 162, 181), (69, 40, 34), (51, 117, 87), (195, 93, 75), (146, 178, 150),
              (18, 93, 72), (231, 176, 165), (162, 143, 158), (35, 60, 75), (105, 73, 77),
              (180, 204, 177), (148, 19, 23), (83, 147, 127), (70, 37, 40), (18, 70, 60),
              (27, 82, 88), (40, 66, 89), (190, 86, 89), (68, 64, 58), (223, 176, 180),
              (174, 194, 209), (110, 130, 147), (108, 134, 142), (185, 195, 196)]

    def __init__(self) -> None:
        self._pen = Turtle()
        self._pen.speed('fast')
        self._pen.penup()
        self._pen.hideturtle()
        self.move_to_corner()

    
    def move_to_corner(self) -> None:
        self._pen.setheading(225)
        self._pen.forward(300)
        self._pen.setheading(0)

    def draw_hirst_painting(self, width: int, height: int):
        """Draw a dots image in Hirst Painting style.

        Args:
          width:
            The number of dots in every row.
          height:
            The number of dots in every column.
        """
        Screen().colormode(255)
        x, y = self._pen.position()
        for dot_count in range(1, width * height + 1):
            self._pen.dot(20, random.choice(self.colors))
            self._pen.forward(50)

            level, leftover = divmod(dot_count, width)
            if leftover == 0:
                next_position = (x, y + 50 * level)
                self._pen.goto(*next_position)
                self._pen.setheading(0)  # not necessary

        screen = Screen()
        screen.exitonclick()


if __name__ == '__main__':
    hirst = HirstPaint()
    hirst.draw_hirst_painting(10, 10)
