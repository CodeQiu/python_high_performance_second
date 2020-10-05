import time
import threading


# 阻塞版
def wait_and_print(msg: str):
    time.sleep(1)
    print(msg)


# 非阻塞版
def wait_and_print_async(msg: str):
    def callback():
        print(msg)

    timer = threading.Timer(1, callback)
    timer.start()


# 同步的
wait_and_print("First call")
wait_and_print("Second call")
print("After call")

# 输出：
# First call
# Second call
# After call

# 异步的
wait_and_print_async("First call async")
wait_and_print_async("Second call async")
print("After submission")

# 输出：
# After submission
# First call async
# Second call async
