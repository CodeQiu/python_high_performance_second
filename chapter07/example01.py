import multiprocessing
import time
import random


class Process(multiprocessing.Process):
    def __init__(self, id: int):
        super(Process, self).__init__()
        self.id = id

    def run(self):
        sleep_time = random.randint(1, 4)
        time.sleep(sleep_time)
        print(f"I'm the process with id {self.id}, sleep {sleep_time}s. need {time.time() - start_time:.3f}s.")


if __name__ == "__main__":
    processes = [Process(i) for i in range(1, 6)]
    start_time = time.time()
    [p.start() for p in processes]
