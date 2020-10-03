from joblib import Memory

# 使用方法Memory.cache还可指定仅在参数发生变化时才重新计算，这让被装饰的函数具备清除和分析缓存的基本功能
memory = Memory("./.cache")  # 指定缓存目录


@memory.cache
def sum3(a, b):
    print("computing...")
    return a + b


print(f"sum3(10, 74)={sum3(10, 74)}")
print(f"sum3(10, 74)={sum3(10, 74)}")
print(f"sum3(20, 53)={sum3(20, 53)}")
print(f"sum3(20, 53)={sum3(20, 53)}")
print(f"sum3(10, 74)={sum3(10, 74)}")

# 输出：
# ________________________________________________________________________________
# [Memory] Calling __main__--path-cache_joblib.sum3...
# sum3(10, 74)
# computing...
# _____________________________________________________________sum3 - 0.0s, 0.0min
# sum3(10, 74)=84
# sum3(10, 74)=84
# ________________________________________________________________________________
# [Memory] Calling __main__--path-cache_joblib.sum3...
# sum3(20, 53)
# computing...
# _____________________________________________________________sum3 - 0.0s, 0.0min
# sum3(20, 53)=73
# sum3(20, 53)=73
# sum3(10, 74)=84
