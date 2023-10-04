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

# DFS
def dfs_search(log):
    x, y = log[-1]
    if maze[x][y] == 1:
        return len(log) - 1
    
    depth = [999999]

    for move in directions:
        if maze[x + move[0]][y + move[1]] != 9:
            if [x + move[0], y + move[1]] not in log:
                log.append([x + move[0], y + move[1]])
                depth.append(dfs_search(log))
                log.pop(-1)
    return min(depth)

print(dfs_search(log=[[1, 1]]))