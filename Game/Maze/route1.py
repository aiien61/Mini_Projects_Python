def search(w, h):
    if (w == 1) and (h == 1):
        return 1
    
    cnt = 0

    
    if w > 1:
        cnt += search(w - 1, h)

    if h > 1:
        cnt += search(w, h - 1)

    return cnt

m = search(2, 3)
n = search(4, 2)

print(m * n)