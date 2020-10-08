from concurrent.futures import ProcessPoolExecutor, wait, as_completed


def square(x: float):
    return x ** 2


executor = ProcessPoolExecutor(max_workers=4)

fut1 = executor.submit(square, 2)
fut2 = executor.submit(square, 3)
wait([fut1, fut2])

resultsFut = as_completed([fut1, fut2])
res = [i.result() for i in resultsFut]
print(f"res: {res}")
