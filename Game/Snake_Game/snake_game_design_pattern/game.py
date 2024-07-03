import time
from turtle import Screen
from snake import Snake

class SnakeGame:
    screen = Screen()

    def __init__(self, window_width: int, window_height: int, background_color: str, title: str):
        self.width: int = window_width
        self.height: int = window_height
        self.bg_color: str = background_color
        self.title: str = title
    
    def config(self):
        self.screen.setup(width=self.width, height=self.height)
        self.screen.bgcolor(self.bg_color)
        self.screen.title(self.title)
        self.screen.tracer(0)


    # TODO
    def play(self):
        self.config()
        snake: Snake = Snake()
        game_is_on: bool = True
        while game_is_on:
            self.screen.update()
            time.sleep(0.1)
            snake.move()

            


        self.screen.exitonclick()
