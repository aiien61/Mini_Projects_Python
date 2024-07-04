import time
from turtle import Screen
from snake import Snake
from food import Food
from scoreboard import Scoreboard

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

    def create_snake(self):
        snake: Snake = Snake()
        self.screen.listen()
        self.screen.onkey(snake.up, "Up")
        self.screen.onkey(snake.down, "Down")
        self.screen.onkey(snake.left, "Left")
        self.screen.onkey(snake.right, "Right")
        return snake
    
    def snake_eats_food(self, snake: Snake, food: Food):
        return True if snake.head.distance(food) < 15 else False
    
    def collides_with_walls(self, snake: Snake):
        if abs(snake.head.xcor()) > 280:
            return True
        if abs(snake.head.ycor()) > 280:
            return True
        return False
    
    def collides_with_itself(self, snake: Snake):
        for part in snake.body_parts[1:]:
            if snake.head.distance(part) < 10:
                return True
        return False

    def play(self):
        self.config()
        scoreboard: Scoreboard = Scoreboard()
        snake: Snake = self.create_snake()
        food: Food = Food()
        game_is_on: bool = True
        while game_is_on:
            self.screen.update()
            time.sleep(0.1)
            snake.move()

            # detect if snake collides with the food object
            if self.snake_eats_food(snake, food):
                food.refresh()
                scoreboard.increase_score()
                snake.grow()

            # detect if snake collides with the wall
            if self.collides_with_walls(snake):
                game_is_on = False
                scoreboard.game_over()

            # detect if snake collides with itself
            if self.collides_with_itself(snake):
                game_is_on = False
                scoreboard.game_over()

        self.screen.exitonclick()
        return None
