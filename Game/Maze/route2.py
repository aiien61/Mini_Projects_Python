def search(x, y):
    if x >= w:
        return search(0, y + 1)
    
    if y >= h:
        return route[w-1][h-1]
    
    if y > 0:
        route[x][y] += route[x][y-1]
    
    if x > 0:
        route[x][y] += route[x - 1][y]

    return search(x + 1, y)


w, h = 2, 3
route = [[0] * h for _ in range(w)]
route[0][0] = 1
n = search(1, 0)

w, h = 4, 2
route = [[0] * h for _ in range(w)]
route[0][0] = n

print(search(1, 0))
