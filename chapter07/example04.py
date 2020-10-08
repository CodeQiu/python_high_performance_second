import multiprocessing


def square(x: float):
    return x ** 2


pool = multiprocessing.Pool()
result_async = [pool.apply_async(square, (i,)) for i in range(100)]
results = [r.get() for r in result_async]
print(results)
