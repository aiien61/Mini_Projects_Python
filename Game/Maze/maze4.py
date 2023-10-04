import random

maze = [
    [9, 9, 9, 9, 9, 9, 9, 9, 9],
    [9, 0, 0, 0, 9, 9, 0, 9, 9],
    [9, 0, 9, 9, 0, 0, 0, 0, 9],
    [9, 0, 0, 0, 0, 9, 9, 9, 9],
    [9, 9, 0, 9, 0, 9, 0, 1, 9],
    [9, 0, 0, 9, 0, 0, 0, 9, 9],
    [9, 0, 9, 0, 0, 9, 0, 0, 9],
    [9, 9, 9, 9, 9, 9, 9, 9, 9]
]

directions = [[0, -1], [-1, 0], [0, 1], [1, 0]]

x, y = 1, 1

toward = 0

while maze[x][y] != 1:
    move = directions[(toward + 1) % 4]
    if maze[x + move[0]][y + move[1]] != 9:
        toward = (toward + 1) % 4
        x += move[0]
        y += move[1]
        print([x, y])
    else:
        toward = (toward + 3) % 4
