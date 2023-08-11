from prettytable import PrettyTable

CROSS = '✗'
CIRCLE = '○'
PLAYERS = {"A": CIRCLE, "B": CROSS}
count = 0

#TODO: create a scoreboard
#TODO: create a widget to play


def init_board() -> list:
    return [[' '] * 3 for _ in range(3)]


def print_board(rows: list) -> None:
    board = PrettyTable(header=False)
    board.add_row(rows[0], divider=True)
    board.add_row(rows[1], divider=True)
    board.add_row(rows[2], divider=True)
    print(board)
    return None


def check_win(rows: list, turn: str) -> bool:
    """Return True if player of the turn wins."""

    # check horizontal direction
    for r in range(3):
        if rows[r][0] == turn and rows[r][1] == turn and rows[r][2] == turn:
            return True
    
    # check vertical direction
    for c in range(3):
        if rows[0][c] == turn and rows[1][c] == turn and rows[2][c] == turn:
            return True

    # check forward diagonal direction
    if rows[0][2] == turn and rows[1][1] == turn and rows[2][0] == turn:
        return True

    # check backward diagonal direction
    if rows[0][0] == turn and rows[1][1] == turn and rows[2][2] == turn:
        return True

    return False

def check_end(rows: list):
    """Return True if all positions have been placed."""
    for i in range(3):
        for j in range(3):
            if rows[i][j] == ' ':
                return False
    return True


def get_position(is_row=True) -> int:
    pos = input("Row: ") if is_row is True else input("Column: ")
    if pos not in {'1', '2', '3'}:
        print('You must enter correct numer (1~3).')
        return get_position(is_row)
    else:
        return int(pos) - 1


def play_game() -> None:
    global count
    if count == 0:
        user_input = input("Welcome to Tic Tac Toe. Let's play! (Y/N): ")
        if user_input.lower() != 'y':
            return None
    else:
        print("Welcome to Tic Tac Toe.")

    rows = init_board()
    player = "A"
    is_game_on = True
    while is_game_on:
        turn = PLAYERS[player]
        print_board(rows)
        print(f"It's player {player}'s turn ({turn}). Pick a position.")
        r = get_position(is_row=True)
        c = get_position(is_row=False)
        if rows[r][c] != ' ':
            print("It's not allowed to place here. It's already taken.")
        else:
            rows[r][c] = turn
            if check_win(rows=rows, turn=turn):
                print(f"Player {player} ({turn}) wins!")
                is_game_on = False
            elif check_end(rows=rows):
                print("It's a draw.")
                is_game_on = False
            else:
                player = "B" if player == "A" else "A"


    if input("Continue? (Y/N): ").lower() == 'y':
        count += 1
        play_game()


if __name__ == "__main__":
    play_game()
