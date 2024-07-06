from turtle import Turtle

ALIGNMENT: str = 'center'
FONT: tuple = ('Arial', 24, 'normal')

class Scoreboard(Turtle):    
    def __init__(self):
        super().__init__()
        self.score: int = 0
        self.high_score: int = self.retrieve_score_record()
        self.color('white')
        self.penup()
        self.goto(0, 270)
        self.hideturtle()
        self.update_scoreboard()

    def increase_score(self) -> None:
        self.score += 1
        self.update_scoreboard()
        return None
    
    def update_scoreboard(self) -> None:
        self.clear()
        self.write(f"Score: {self.score} High Score: {self.high_score}", align=ALIGNMENT, font=FONT)
        return None
    
    def game_over(self) -> None:
        self.goto(0, 0)
        self.write("GAME OVER", align=ALIGNMENT, font=FONT)
        return None
    
    def reset(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.overwrite_high_score(self.high_score)
        self.score = 0
        self.update_scoreboard()

    @staticmethod
    def overwrite_high_score(high_score: int) -> bool:
        with open("score_data.txt", 'w') as data:
            data.write(str(high_score))
        return True
    
    def retrieve_score_record(self) -> int:
        with open("score_data.txt") as data:
            high_score: str = data.read()

        return int(high_score) if high_score else 0
