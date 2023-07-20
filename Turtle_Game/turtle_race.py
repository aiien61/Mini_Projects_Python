from turtle import Turtle, Screen
import random

is_race_on = False
screen = Screen()
screen.setup(width=500, height=400)
user_bet = screen.textinput(title="Make Your Bet",
                            prompt="Which turtle will win the race? Enter the color: ")

colors = ["red", "orange", "green", "blue", "purple", "yellow"]
y_position = [-70, -40, -10, 20, 50, 80]
all_turtles = []
for i in range(6):
    new_turtle = Turtle(shape="turtle")
    new_turtle.color(colors[i])
    new_turtle.penup()
    new_turtle.goto(x=-250, y=y_position[i])
    new_turtle.pendown()
    all_turtles.append(new_turtle)

if user_bet:
    is_race_on = True

while is_race_on:
    for turtle_runner in all_turtles:
        if turtle_runner.xcor() > 230:
            is_race_on = False
            winning_color = turtle_runner.pencolor()
        turtle_runner.forward(random.randint(0, 10))

if winning_color == user_bet:
    print(f"You've won! The {winning_color} turtle is the winner!")
else:
    print(f"You've lost! The {winning_color} turtle is the winner!")

screen.exitonclick()
