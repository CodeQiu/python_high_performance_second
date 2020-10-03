from queue import PriorityQueue

# 要在PriorityQueue类中填充元素，可使用方法PriorityQueue.put
# 要提取最小值，可使用方法PriorityQueue.get
collection = [10, 3, 3, 4, 5, 6, 2, 1]
queue_demo1 = PriorityQueue()
for element in collection:
    queue_demo1.put(element)

print(f"queue_demo1 get: {queue_demo1.get()}")
print(f"queue_demo1 get: {queue_demo1.get()}")

# 要提取最大的元素，可采用一种简单的诀窍--将每个元素都乘以-1，这将反转元素的排列顺序。
# 另外，如果要件每个数字(可能表示优先级)关联到一个对象(如要执行的任务)，可插入形如(number, object)的元组，这是因为元素的比较运算符将根据其第一个元素进行排序
# 如下所示：
queue_demo2 = PriorityQueue()
queue_demo2.put((3, "priority 3"))
queue_demo2.put((2, "priority 2"))
queue_demo2.put((1, "priority 1"))

print(f"queue_demo2 get: {queue_demo2.get()}")
print(f"queue_demo2 get: {queue_demo2.get()}")
