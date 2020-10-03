import time


def loop():
    res = []
    for i in range(100000):
        res.append(i * i)
    return sum(res)


def comprehension():
    return sum([i * i for i in range(100000)])


def generator():
    return sum(i * i for i in range(100000))


loop_start_time = time.time()
loop()
loop_end_time = time.time()
comprehension_start_time = time.time()
comprehension()
comprehension_end_time = time.time()
generator_start_time = time.time()
generator()
generator_end_time = time.time()

print(f"loop took {loop_end_time - loop_start_time:.5f}s")
print(f"comprehension took {comprehension_end_time - comprehension_start_time:.5f}s")
print(f"generator took {generator_end_time - generator_start_time:.5f}s")
