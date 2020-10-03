import timeit


def fibonacci(n):
    if n < 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


setup_code = """
from functools import lru_cache
from __main__ import fibonacci
fibonacci_memoized = lru_cache(maxsize=None)(fibonacci)
"""

# 为设计合适的基准测试程序，需确保每次运行时都实例化新缓存，为此使用函数timeit.repeat
results = timeit.repeat("fibonacci_memoized(20)", setup=setup_code, repeat=1000, number=1)
print(f"Fibonacci took {min(results):.2f}us.")
