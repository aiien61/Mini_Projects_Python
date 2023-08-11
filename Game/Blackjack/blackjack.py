import random
from art import logo_blackjack

play_prompt = "Do you want to play a game of Blackjack? Type 'y' or 'n': "
add_card_prompt = "\nType 'y' to get another card, type 'n' to pass: "
score_prompt = "  {whose} final hand: {cards}, final score: {score}"

def deal_card() -> int:
    """Returns a random card from the deck."""
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    card = random.choice(cards)
    return card


def calculate_score(cards: list) -> int:
    """Calculates and returns the sum of cards."""

    """A blackjack (a hand with only 2 cards: Ace + 10) and return 0 instead of
    the actual score. 0 will represent a blackjack in our game.
    """
    if sum(cards) == 21 and len(cards) == 2:
        return 0

    """If the score is already over 21, remove the 11 and replace it with a 1
    if there is.
    """
    if 11 in cards and sum(cards) > 21:
        ace_index = cards.index(11)
        cards[ace_index] = 1
    return sum(cards)


def compare(user_score: int, computer_score: int) -> None:
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


def play_game():
    print(logo_blackjack)

    user_cards, computer_cards = [], []
    for _ in range(2):
        user_cards.append(deal_card())
        computer_cards.append(deal_card())
    
    is_game_over = False
    while not is_game_over:
        user_score = calculate_score(user_cards)
        computer_score = calculate_score(computer_cards)
        print(f"  Your cards: {user_cards}, current score: {user_score}")
        print(f"  Computer's first cards: {computer_cards[0]}")

        if computer_score == 0 or user_score == 0 or user_score > 21:
            is_game_over = True
        else:
            if input(add_card_prompt) == "y":
                user_cards.append(deal_card())
            else:
                is_game_over = True

    if user_score < 21 and computer_score < user_score:
        while computer_score != 0 and computer_score < 17:
            computer_cards.append(deal_card())
            computer_score = calculate_score(computer_cards)

    print()
    print(score_prompt.format(
        whose="Your", cards=user_cards, score=user_score))
    print(score_prompt.format(
        whose="Computer's", cards=computer_cards, score=computer_score))
    print(compare(user_score, computer_score))


if __name__ == '__main__':
    while input(play_prompt) == 'y':
        play_game()
