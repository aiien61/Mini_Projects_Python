import random
from turtle import Turtle
from paddle import Paddle

class Ball(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.x_move = 10
        self.y_move = 10
        self.move_speed = 0.1

    def move(self):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self):
        self.y_move *= -1
        return None
    
    def bounce_x(self):
        self.x_move *= -1
        self.move_speed *= 0.9
        return None
    
    def collide_with_walls(self) -> bool:
        return abs(self.ycor()) > 280
    
    def collide_with_paddle(self, paddle: Paddle) -> bool:
        if self.distance(paddle) < 50 and abs(self.xcor()) > 320:
            return True
        
    def pass_right_paddle(self, paddle: Paddle) -> bool:
        return self.xcor() > paddle.xcor()
    
    def pass_left_paddle(self, paddle: Paddle) -> bool:
        return self.xcor() < paddle.xcor()

    def reset_position(self):
        self.goto(0, 0)
        self.move_speed = 0.1
        self.bounce_x()
        


