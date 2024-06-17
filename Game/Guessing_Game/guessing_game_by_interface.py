from random import randint
from termcolor import colored
from art import logo_make_a_guess
from enum import Enum, auto
from typing import List
from replit import clear

class Level(Enum):
    HARD = auto()
    EASY = auto()


class Game:
    def __init__(self, min_max: List[int]) -> None:
        self.min_max: List[int] = min_max
        self.turns: int = None
        self.answer: int = randint(*min_max)

    def set_difficulty(self, level: str) -> None:
        self.turns = Level[level].value * 5
        return None
    
    def show_attempts(self) -> None:
        print(f'You have {self.turns} attempts to guess the number.')
        return None
    
    def make_a_guess(self) -> int:
        try:
            guess = int(input('Make a guess: '))
        except TypeError as e:
            print(colored(e, on_color='on_red'))
            return self.make_a_guess()
        else:
            self.turns -= 1
            return guess
        
    def check_answer(self, guess: int) -> bool:
        if guess < self.answer:
            print(colored(f'Too Low', color='blue'))
            return False
        elif guess > self.answer:
            print(colored(f'Too High', color='red'))
            return False
        else:
            print(colored(f"You got it! The answer was {self.answer}.", color='green'))
            return True
        
    def setting(self) -> None:
        print(logo_make_a_guess)
        print('Welcome to the Number Guessing Game!')
        print(f"I'm thinking of a number between {self.min_max[0]} and {self.min_max[1]}.")
        level = input("Choose a difficulty. Type 'easy' or 'hard': ").upper()
        self.set_difficulty(level)
        return None

    def play(self) -> None:
        self.show_attempts()
        guess: int = self.make_a_guess()
        while not self.check_answer(guess):
            if self.turns == 0:
                print(colored(f'Psst, the correct answer is {self.answer}', color='yellow'))
                break
            print('Guess again.')
            self.show_attempts()
            guess = self.make_a_guess()
        return None          


if __name__ == '__main__':
    while True:
        clear()
        game: Game = Game(min_max=[1, 100])
        game.setting()
        game.play()
        
        play_again: str = input("Play again? (y/n): ")
        if play_again != 'y':
            break
