import time
from turtle import Screen
from paddle import Paddle
from ball import Ball
from scorebaord import Scoreboard

class PongGame:
    screen: Screen = Screen()

    def __init__(self):
        self.screen.bgcolor("black")
        self.screen.setup(width=800, height=600)
        self.screen.title("Pong")
        self.screen.tracer(0)

    
    def create_paddles(self, position: Paddle.Position, up_key: str, down_key: str) -> Paddle:
        paddle: Paddle = Paddle(position)
        self.screen.listen()
        self.screen.onkey(paddle.go_up, up_key)
        self.screen.onkey(paddle.go_down, down_key)
        return paddle
    

    def play(self):
        ball: Ball = Ball()
        scoreboard: Scoreboard = Scoreboard()
        right_paddle: Paddle = self.create_paddles(Paddle.Position.RIGHT, 'Up', 'Down')
        left_paddle: Paddle = self.create_paddles(Paddle.Position.LEFT, 'w', 's')
        
        game_is_on = True
        while game_is_on:
            time.sleep(ball.move_speed)
            self.screen.update()

            ball.move()

            if ball.collide_with_walls():
                ball.bounce_y()

            if ball.collide_with_paddle(right_paddle) or ball.collide_with_paddle(left_paddle):
                ball.bounce_x()

            if ball.pass_right_paddle(right_paddle):
                scoreboard.left_scored()
                ball.reset_position()
            
            if ball.pass_left_paddle(left_paddle):
                scoreboard.right_scored()
                ball.reset_position()
        
        self.screen.exitonclick()
