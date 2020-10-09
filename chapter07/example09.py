import random
import multiprocessing


def sample():
    x = random.uniform(-1.0, 1.0)
    y = random.uniform(-1.0, 1.0)

    if x ** 2 + y ** 2 <= 1:
        return 1
    else:
        return 0


def sample_multiple(samples_partial):
    return sum(sample() for i in range(samples_partial))


samples = 1000000
n_tasks = 10
chunk_size = int(samples / n_tasks)

pool = multiprocessing.Pool()
results_async = [pool.apply_async(sample_multiple, [chunk_size]) for i in range(n_tasks)]

hits = sum(r.get() for r in results_async)
pi = 4.0 * hits / samples
print(f"pi is {pi}")
