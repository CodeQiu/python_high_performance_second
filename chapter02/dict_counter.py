import timeit
from collections import defaultdict, Counter


def count_dict_func1():
    items = ["l", "o", "v", "e", "c", "o", "me", "s", "f", "r", "o", "m", "l", "o", "v", "e"]
    counter = {}
    for item in items:
        if item not in counter:
            counter[item] = 0
        else:
            counter[item] += 1
    return counter


def count_dict_func2():
    items = ["l", "o", "v", "e", "c", "o", "me", "s", "f", "r", "o", "m", "l", "o", "v", "e"]
    counter = defaultdict(int)
    for item in items:
        counter[item] += 1
    return counter


def count_dict_func3():
    items = ["l", "o", "v", "e", "c", "o", "me", "s", "f", "r", "o", "m", "l", "o", "v", "e"]
    counter = Counter(items)
    return counter


print(f"count_dict_func1 need {timeit.timeit(stmt=count_dict_func1)}")
print(f"count_dict_func2 need {timeit.timeit(stmt=count_dict_func2)}")
print(f"count_dict_func3 need {timeit.timeit(stmt=count_dict_func3)}")
