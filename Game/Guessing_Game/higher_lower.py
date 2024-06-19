from art import logo_higher_lower, logo_vs
from game_data import data
import random

FORMAT_TEXT = "{name}, {article} {description}, from {country}"

# Format the account data into printable format.
def format_data(account: dict) -> str:
    """Format the accoutn data into printable format."""

    account_name = account['name']
    account_descr = account['description']
    account_country = account['country']
    if account_descr[0].lower() in {'a', 'e', 'i', 'o', 'u'}:
        article = 'an'
    else:
        article = 'a'

    formatted_text = FORMAT_TEXT.format(
        name=account_name, article=article, description=account_descr,
        country=account_country
    )
    return formatted_text


def check_answer(guess, a_followers, b_followers):
    """Take the user guess and follower counts and returns if they got it right
    """
    if a_followers > b_followers:
        return guess == "a"
    else:
        return guess == "b"

score = 0
game_should_continue = True

# Generate a random account from the game data.
account_b = random.choice(data)

# Make the game repeatable.
while game_should_continue:
    # Making account at position B become the next account at position A
    account_a = account_b
    account_b = random.choice(data)

    while account_a == account_b:
        account_b = random.choice(data)

    print(f"Compare A: {format_data(account_a)}.")
    print(logo_vs)
    print(f"Against B: {format_data(account_b)}.")
    # Ask user for a guess
    guess = input("Who has more followers? Type 'A' or 'B': ").lower()

    # Check if user is correct.
    ## Get follower count of each account.
    a_follower_count = account_a["follower_count"]
    b_follower_count = account_b["follower_count"]
    ## Use if statement to check if user is correct.
    is_correct = check_answer(guess, a_follower_count, b_follower_count)

    # Clear the screen between rounds.
    # clear()
    # Display art
    print(logo_higher_lower)
    
    # Give user feedback on their guess.
    if is_correct:
        # Score keeping
        score += 1
        print(f"You're right! Current score: {score}.")
    else:
        game_should_continue = False
        print(f"Sorry, that's wrong. Final score: {score}")
