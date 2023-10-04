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

#BFS
log = [[1, 1]]

queue = [[1, 1, 0]]
def bfs_search(queue, log):
    while len(queue) > 0:
        x, y, depth = queue.pop(0)
        for move in directions:
            xd, yd = x + move[0], y + move[1]
            if maze[xd][yd] == 1:
                print(depth + 1)
                return 

            elif maze[xd][yd] != 9:
                if [xd, yd] not in log:
                    log.append([xd, yd])
                    queue.append([xd, yd, depth + 1])

bfs_search(queue, log)