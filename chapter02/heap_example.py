import heapq
from heapq import heappop
from typing import Iterable

# 比如列表，可使用函数headpq.heapify将其转换为堆
# collection = [10, 3, 3, 4, 5, 6, 2, 1]
collection = [10, 9, 8, 7, 6, 5, 4, 3]
heapq.heapify(collection)
print(f"heap: {collection}")
# 要对堆执行插入和提取操作，可使用heapq.heappush和heapq.heappop。
# 函数heapq.heappop提取集合中的最小值，时间复杂度为O(log(N))。用法如下：
print(f"heappop: {heapq.heappop(collection)}")
print(f"heappop: {heapq.heappop(collection)}")
print(f"heappop: {heapq.heappop(collection)}")
print(f"heap: {collection}")
# 同理，要压入整数1，可使用函数heapq.heappush，如下所示：
heapq.heappush(collection, 1)
print(f"heap: {collection}")

# 堆排序可以通过将所有值推入堆中然后每次弹出一个最小值项来实现
test_heap_list = [1, 3, 5, 7, 9, 2, 4, 6, 8, 0]


def heapsort(iterable):
    h = []
    for value in iterable:
        heapq.heappush(h, value)
    return [heapq.heappop(h) for i in range(len(h))]


print(f"heapsort: {heapsort(test_heap_list)}")
