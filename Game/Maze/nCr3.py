from functools import lru_cache

@lru_cache(maxsize=1000)
def nCr(n, r):
    if (r == 0) or (r == n):
        return 1
    return nCr(n - 1, r - 1) + nCr(n - 1, r)

print(nCr(30, 10))