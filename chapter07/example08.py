import random
import multiprocessing


def sample():
    x = random.uniform(-1.0, 1.0)
    y = random.uniform(-1.0, 1.0)

    if x ** 2 + y ** 2 <= 1:
        return 1
    else:
        return 0


samples = 1000000
pool = multiprocessing.Pool()
results_async = [pool.apply_async(sample) for i in range(samples)]
hits = sum(r.get() for r in results_async)
pi = 4.0 * hits / samples
print(f"pi is {pi}")
