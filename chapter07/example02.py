import multiprocessing


def square(x: float):
    return x ** 2


pool = multiprocessing.Pool()
# input_list = [0, 1, 2, 3, 4]
input_list = range(5)
# output = pool.map(square, range(5))
output = pool.map(square, input_list)
print(output)
