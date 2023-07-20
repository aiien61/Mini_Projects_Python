from turtle import Turtle, Screen

tim = Turtle()
screen = Screen()

def move_froward():
    tim.forward(10)


def move_backward():
    tim.backward(10)


def turn_left():
    tim.left(10)


def turn_right():
    tim.right(10)


def clear():
    tim.clear()
    tim.penup()
    tim.home()
    tim.pendown()


def main():
    screen.listen()
    screen.onkey(key="w", fun=move_froward)
    screen.onkey(key="s", fun=move_backward)
    screen.onkey(key="d", fun=turn_left)
    screen.onkey(key="a", fun=turn_right)
    screen.onkey(key="c", fun=clear)
    screen.exitonclick()


if __name__ == '__main__':
    main()
