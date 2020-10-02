import timeit


def func1():
    lis = []
    lis = list(range(1000))


def func2():
    lis = []
    lis = [i for i in range(1000)]


def func3():
    lis = []
    for i in range(1000):
        lis.append(i)


def func4():
    lis = []
    for i in range(1000):
        lis += [i]


# func1 >> func2 >> func3 >> func4
print(f"func1 need {timeit.timeit(stmt=func1, number=1000)}")
print(f"func2 need {timeit.timeit(stmt=func2, number=1000)}")
print(f"func3 need {timeit.timeit(stmt=func3, number=1000)}")
print(f"func4 need {timeit.timeit(stmt=func4, number=1000)}")
