import random
from replit import clear
from typing import List

from game_data import data
from art import logo_higher_lower, logo_vs

class Player:
    def __init__(self):
        self.score: int = 0


class Game:
    _data: List[dict] = data

    def __init__(self, player: Player) -> None:
        self.player: Player = player

    def generate_new_comparison(self, old: dict=None) -> dict:
        if old is None:
            return random.choice(self._data)

        while True:
            new: dict = random.choice(self._data)
            if new['follower_count'] != old['follower_count']:
                return new
    
    def format_data(self, account: dict) -> str:
        """Format the accoutn data into printable format."""
        return f"{account['name']}, a {account['description']}, from {account['country']}"
    
    def make_a_guess(self, account_a: dict, account_b: dict) -> dict:
        print(f'Compare A: {self.format_data(account_a)}.')
        print(logo_vs)
        print(f'Against B: {self.format_data(account_b)}.')
        user_guess: str = input("Who has more followers? Type 'A' or 'B': ").upper()
        return account_a['follower_count'] if user_guess == 'A' else account_b['follower_count']
    
    def check_answer(self, guess: int, *comparisons: List[dict]) -> bool:
        """
        Take the follower count of the user guess and all accounts, and returns True if the user 
        got it right.
        """
        a, b = comparisons
        a_follower, b_follower = a['follower_count'], b['follower_count']
        
        if a_follower > b_follower:
            return True if guess == a_follower else False
        else:
            return True if guess == b_follower else False

    def play(self) -> None:
        print(logo_higher_lower)
        b: dict = self.generate_new_comparison()
        game_should_continue: bool = True

        while game_should_continue:
            a: dict = b
            b: dict = self.generate_new_comparison(old=b)
            guess: int = self.make_a_guess(a, b)
            is_correct: bool = self.check_answer(guess, a, b)

            clear()
            print(logo_higher_lower)

            if is_correct:
                self.player.score += 1
                print(f"You're right! Current score: {self.player.score}")
            else:
                game_should_continue = False
                clear()
                print(logo_higher_lower)
                print("Sorry, that's wrong.", end=' ')

        return None
                

if __name__ == '__main__':
    while True:
        player: Player = Player()
        game: Game = Game(player)
        game.play()
        print(f"Final score: {player.score}")
        if input('Play again? (y/n): ') == 'n':
            break
        clear()
