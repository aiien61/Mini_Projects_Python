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


# bidirectional search

log_fw = [[1, 1]]
log_bw = [[4, 7]]

fw = [[1, 1]]
bw = [[4, 7]]

depth = 0

def get_next(queue, log):
    result = []
    for x, y in queue:
        for move in directions:
            xd, yd = x + move[0], y + move[1]
            if maze[xd][yd] != 9:
                if [xd, yd] not in log:
                    log.append([xd, yd])
                    result.append([xd, yd])
    return result

def check_duplicate(fw, bw):
    for i in fw:
        if i in bw:
            return True
    return False

while True:
    fw = get_next(fw, log_fw)
    depth += 1
    if check_duplicate(fw, bw):
        break

    bw = get_next(bw, log_bw)
    depth += 1
    if check_duplicate(fw, bw):
        break

print(depth)