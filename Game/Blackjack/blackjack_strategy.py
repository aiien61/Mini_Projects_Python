import random
from abc import ABC
from replit import clear
from typing import List
from art import logo_blackjack


class Game:
    def __init__(self, *players) -> None:
        self.players = players

    def is_game_over(self) -> bool:
        user, computer = self.players
        if user.score == 0 or computer.score == 0 or user.score > 21:
            return True
        else:
            return False

    @classmethod
    def deal_card(self) -> int:
        """Returns a random card from the deck."""
        cards: List[int] = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
        card: int = random.choice(cards)
        return card

    def compare(self):
        user, computer = self.players
        user_score: int = user.calculate_score()
        computer_score: int = computer.calculate_score()

        if user_score == computer_score:
            return "Draw 🙃"
        elif computer_score == 0:
            return "Lose, opponent has Blackjack 😱"
        elif user_score == 0:
            return "Win with a Blackjack 😎"
        elif user_score > 21:
            return "You went over. You lose 😭"
        elif computer_score > 21:
            return "Opponent went over. You win 😁"
        elif user_score > computer_score:
            return "You win 😃"
        else:
            return "You lose 😤"


class Player(ABC):
    def __init__(self) -> None:
        self.cards = []
        for _ in range(2):
            self.cards.append(Game.deal_card())

    @property
    def score(self) -> int:
        return self.calculate_score()
    
    def calculate_score(self) -> int:
        """Calculates and returns the sum of cards."""

        """A blackjack (a hand with only 2 cards: Ace + 10) and return 0 instead of
        the actual score. 0 will represent a blackjack in our game.
        """
        if sum(self.cards) == 21 and len(self.cards) == 2:
            return 0

        """If the score is already over 21, remove the 11 and replace it with a 1
        if there is.
        """
        if 11 in self.cards and sum(self.cards) > 21:
            self.cards.remove(11)
            self.cards.append(1)

        return sum(self.cards)


class Dealer(Player):
    def __init__(self) -> None:
        super().__init__()

    def can_get_more(self) -> bool:
        if self.score != 0 and self.score < 17:
            return True
        else:
            return False
    

def play_game():
    print(logo_blackjack)
    user: Player = Player()
    computer: Dealer = Dealer()
    game: Game = Game(user, computer)
    while True:
        print(f"\tYour cards: {user.cards}, current score; {user.score}")
        print(f"\tComputer's cards: {computer.cards[0]}")
        if game.is_game_over():
            break

        user_should_deal: str = input("Type 'y' to get another card, type 'n' to pass: ")
        if user_should_deal == 'y':
            user.cards.append(game.deal_card())
        else:
            break

    while computer.can_get_more():
        computer.cards.append(game.deal_card())

    print(f"\tYour final hand: {user.cards}, final score: {user.score}")
    print(f"\tComputer's final hand: {computer.cards}, final score: {computer.score}")
    print(game.compare())


if __name__ == '__main__':
    while input("Do you want to play a game of Blackjack? Type 'y' or 'n': ") == 'y':
        clear()
        play_game()