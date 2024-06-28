import random
from abc import ABC, abstractmethod
from turtle import Turtle, Screen
from typing import List


class TurtleRunner(Turtle):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def run(self):
        self.forward(random.randint(1, 10))


class TrurtleRace:
    colors = ['red', 'orange', 'green', 'blue', 'purple', 'yellow']
    
    def __init__(self):
        self.runners: List[TurtleRunner] = []

    def register_runner(self, color: str=None):
        if color is None:
            color = random.choice(self.colors)
        self.colors.remove(color)
        
        new_runner = TurtleRunner(shape='turtle')
        new_runner.color(color)
        self.runners.append(new_runner)

    def deregister_runner(self, color: str):
        for runner in self.runners:
            if runner.color == color:
                self.runners.remove(runner)

    def start_race(self):
        screen = Screen()
        screen.setup(width=500, height=400)
        user_bet = screen.textinput(
            title="Make Your Bet", prompt="Which turtle will win the race? Enter the color: ")
        self.register_runner(user_bet)
        self.get_runners_ready()
        is_race_on = True
        while is_race_on:
            for runner in self.runners:
                if runner.xcor() > 230:
                    is_race_on = False
                    winner_color = runner.pencolor()
                    break
                runner.run()
        
        if winner_color == user_bet:
            print(f"You've won! The {winner_color} turtle is the winner!")
        else:
            print(f"You've lost! The {winner_color} turtle is the winner!")

        screen.exitonclick()

    def get_runners_ready(self):
        for _ in range(len(self.colors)):
            self.register_runner(self.colors[0])

        for i, runner in enumerate(self.runners):
            runner.penup()
            runner.goto(-230, -60 + i * 30)


if __name__ == '__main__':
    race = TrurtleRace()
    race.start_race()
