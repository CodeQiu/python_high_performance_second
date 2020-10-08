import multiprocessing


def square(x: float):
    return x ** 2


pool = multiprocessing.Pool()
input_list = range(6)
outputs_async = pool.map_async(square, input_list)
print(outputs_async.get())
