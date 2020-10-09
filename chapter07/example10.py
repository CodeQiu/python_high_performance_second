import multiprocessing


class Process(multiprocessing.Process):
    def __init__(self, counter):
        super(Process, self).__init__()
        self.counter = counter

    def run(self):
        for i in range(1000):
            self.counter.value += 1


def main():
    counter = multiprocessing.Value("i", lock=True)
    counter.value = 0

    processes = [Process(counter) for i in range(4)]
    [p.start() for p in processes]
    [p.join() for p in processes]
    print(f"counter.value is {counter.value}")


if __name__ == "__main__":
    main() # 结果不符合预期，没有加锁
