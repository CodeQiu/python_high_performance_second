from concurrent.futures import ProcessPoolExecutor


def square(x: float):
    return x ** 2


executor = ProcessPoolExecutor(max_workers=4)
fut = executor.submit(square, 2)
print(f"fut: {fut}")
result = executor.map(square, range(5))
res = list(result)
print(f"res: {res}")
