import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

class Game:
    
    def __init__(self, window_width: int, window_height: int):
        self.car_manager: CarManager = CarManager(road_length=window_width, road_width=window_height-100)
        self.screen = Screen()
        self.screen.setup(width=window_width, height=window_height)
        self.screen.tracer(0)

    def create_player(self):
        player: Player = Player()
        self.screen.listen()
        self.screen.onkey(player.go_up, "Up")
        return player

    def start(self):
        scoreboard: Scoreboard = Scoreboard()
        player: Player = self.create_player()

        game_is_on: bool = True
        while game_is_on:
            time.sleep(0.1)
            self.screen.update()
            self.car_manager.create_car()
            self.car_manager.move_cars()

            # Detect collision with cars
            if player.collides_with_car(self.car_manager.all_cars):
                game_is_on = False
                scoreboard.game_over()

            # Detect successful crossing
            if player.is_at_finish_line():
                player.go_to_start()
                scoreboard.increase_level()
                self.car_manager.level_up()

        self.screen.exitonclick()
        
