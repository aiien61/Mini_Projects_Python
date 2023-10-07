def nCr(n, r):
    result = 1
    for i in range(1, r + 1):
        result = result * (n - i + 1) // i
    return result

print(nCr(3, 2))