from math import factorial


def nPr(n, r):
    result = 1
    for i in range(r):
        result *= (n - i)
    return result

print(nPr(3, 3))

print(factorial(3))