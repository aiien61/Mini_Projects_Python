from random import randint
from art import logo_make_a_guess

EASY_LEVEL_TURNS = 10
HARD_LEVEL_TURNS = 5


# Function to check user's guess against actual answer.
def check_answer(guess: int, answer: int, turns: int) -> int:
    """Checks answer against guess. Returns the number of turns remaining."""
    if guess < answer:
        print("Too low.")
        return turns - 1
    elif guess > answer:
        print("Too high.")
        return turns - 1
    else:
        print(f"You got it! The answer was {answer}.")


# Function to set difficulty.
def set_difficulty():
    level = input("Choose a difficulty. Type 'easy' or 'hard': ")
    return EASY_LEVEL_TURNS if level == 'easy' else HARD_LEVEL_TURNS


def game():
    # Choosing a random number betweeb 1 and 100.
    print(logo_make_a_guess)
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    answer = randint(1, 100)

    turns = set_difficulty()

    # Repeat the guessing functionality if they get it wrong.
    guess = 0
    while guess != answer:
        print(f"You have {turns} attempts remaining to guess the number.")

        # Let the user guess a number
        guess = int(input("Make a guess: "))
        
        # Track the number of turns and reduce by 1 if they get it wrong.
        turns = check_answer(guess, answer, turns)
        if turns == 0:
            print(f"Psst, the correct answer is {answer}.")
            return None
        elif guess != answer:
            print("Guess again.")


if __name__ == "__main__":
    game()
