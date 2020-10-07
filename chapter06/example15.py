collection = list([1, 2, 3, 4, 5, 6])
iterator = iter(collection)

print("Next")
print(next(iterator))
print(next(iterator))
print("For loop")
for i in iterator:
    print(i)
