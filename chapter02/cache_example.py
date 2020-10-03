from functools import lru_cache

# 创建一个名为sum2的函数，它打印一条豫剧并返回两个数字的和
# 运行这个函数两次。
# @lru_cache(maxsize=0) # max_size限制缓存区大小
@lru_cache()
def sum2(a, b):
    print(f"Calculating {a} + {b}")
    return a + b


print("-" * 10)
print(sum2(1, 2))
# 输出：
# Calculating 1 + 2
# 3
print("-" * 10)
print(f"sum2 info: {sum2.cache_info()}") # 查看缓存性能
# sum2.cache_clear() # 清除缓存
print(sum2(1, 2))
# 输出：
# 3
print("-" * 10)
# 从输出结果可知，第一次执行函数sum2时生成了字符串"Calculating ..."，而第二次直接返回结果，没有运行该函数。