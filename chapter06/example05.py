import time


class Timer:
    def __init__(self, timeout: float):
        self.timeout = timeout
        self.start = time.time()

    def done(self):
        return time.time() - self.start > self.timeout

    def on_timer_done(self, callback):
        self.callback = callback


timers = []

timer1 = Timer(1)
timer1.on_timer_done(lambda: print("First timer is done!"))

timer2 = Timer(2)
timer2.on_timer_done(lambda: print("Second timer is done!"))

timer3 = Timer(3)
timer3.on_timer_done(lambda: print("Third timer is done!"))

timer4 = Timer(2.5)
timer4.on_timer_done(lambda: print("fourth timer is done!"))

timers.append(timer1)
timers.append(timer2)
timers.append(timer3)
timers.append(timer4)

while True:
    for timer in timers:
        if timer.done():
            timer.callback()
            timers.remove(timer)
    if len(timers) == 0:
        break
