def range_generator(n: float):
    i = 0
    while i <= n:
        print(f"Generating value {i}")
        yield i
        i += 1


generator = range_generator(4)
next(generator)
next(generator)

for j in generator:
    pass
