from turtle import Turtle, Screen
import random


def square(t: Turtle, length: int):
    for _ in range(4):
        t.forward(length)
        t.left(90)


def draw_dash(t: Turtle, length: int):
    for _ in range(int(length/10)):
        t.forward(10)
        t.penup()
        t.forward(10)
        t.pendown()


def draw_shape(t: Turtle, number_of_sides: int):
    for _ in range(number_of_sides):
        angle = 360 / number_of_sides
        t.forward(100)
        t.right(angle)


def random_color() -> tuple:
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return r, g, b


def random_walk(t: Turtle, length: int):
    Screen().colormode(255)

    directions = [0, 90, 180, 270]
    step_length = 30
    steps = length // step_length
    t.speed("fastest")
    for _ in range(steps):
        t.pensize(15)
        t.pencolor(random_color())
        t.forward(step_length)
        t.setheading(random.choice(directions))


def draw_spirograph(t, radius, size_of_gap):
    Screen().colormode(255)

    t.speed("fastest")
    for _ in range(360 // size_of_gap):
        t.color(random_color())
        t.circle(radius)
        t.setheading(t.heading() + size_of_gap)



def main():
    tim = Turtle()
    # colors = ["CornflowerBlue", "DarkOrchid", "IndianRed",
    #           "DeepSkyBlue", "LightSeaGreen", "wheat", "SlateGray", "SeaGreen"]
    # for shape_side_n in range(3, 11):
    #     tim.color(random.choice(colors))
    #     draw_shape(tim, shape_side_n)

    # random_walk(tim, 6000)

    draw_spirograph(tim, 100, 10)
    


if __name__ == '__main__':
    main()
    screen = Screen()
    screen.exitonclick()
