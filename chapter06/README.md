&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;如何测量程序的性能，以及如何通过巧妙的算法和高效的机器码来减少CPU执行的操作数，进而改善程序的性能。在有些程序上，大部分时间都花在等待速度比CPU慢得多的资源(如永久性存储和网络资源)上。异步编程是一种编程范式，可帮助处理速度缓慢且不可预测的资源(如用户)，被广泛用于打造响应迅速的服务和用户界面。

### 6.1 异步编程

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;异步编程是一种处理缓慢且不可预测资源的一种方式。异步程序能够高效地同时处理多种资源，而不是在那里等待资源可用。

#### 6.1.1 等待I/O

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;现代计算机利用各种不同的存储器来存储数据和执行操作。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;在存储器层次结构的顶端是*CPU寄存器*，它们集成在CPU中，用于存储和执行机器指令。访问寄存器中的数据所需要的时间通常为一个时钟周期，这意味着如果CPU的频率为3GHz，访问CPU寄存器中一个元素所需的时间大约为0.3纳秒。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;寄存器下面是*CPU缓存*。缓存有多级，也被集成到处理器中。缓存的速度比寄存器慢些，但在一个数量级。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;存储器层次结构中的接下来一层是*主存(内存)*，它能够存储的数据比缓存多得多，但速度更慢。从内存中获取一个元素所需的时间可能是几百个时钟周期。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;最底层是*永久性存储*，如旋转磁盘(HDD)和固态硬盘(SDD)。这些设备能够存储的苏联最多，但速度比主存差几个数量级。

#### 6.1.2 并发

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;并发是一种实现系统同时处理多个请求的方式，其基本理念是在等待值呀un期间可着手处理其他的资源。并发的工作原理是：将任务划分成可不按顺序执行的子任务，这样就能够同时处理多个子任务，而无须等到前面的值任务完成。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;在example01.py中，将介绍如何实现对缓慢的网络资源的并发访问。假设有一个Web服务，它获取数字的平方；另外，假设从请求该Web服务到获取响应的时间大约为1秒。可以实现函数network_request，它接受一个数字，并返回一个字典，其中包含有关计算是否成功的信息以及计算结果。为模拟该Web服务，可使用函数time.sleep，如下所示：

```py
import time

def network_request(number: int):
    time.sleep(1)
    return {"success": True, "result": number ** 2}
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;另外，还编写其他一些代码，它们发送请求，核实请求成功并打印结果。在下面的代码中，定义了函数fetch_square，并使用它来计算数字2的平方(而它通过调用network_request计算这个数的平方)。

```py
def fetch_square(number: int):
    response = network_request(number)
    if response["success"]:
        print(f'Result is: {response["result"]}')

fetch_square(2)
# 输出：
# 结果：4
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;由于网络速度缓慢，从网络上获取一个数字需要1秒。如果要计算多个数字的贫乏，可多次调用fetch_square，其中每个调用都将在前一个调用结束后发起网络请求。

```py
fetch_square(2)
fetch_square(3)
fetch_square(4)
# 输出:
# 结果：4
# 结果：9
# 结果：16
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;上述代码需要3秒才能执行完成，但这样的结果不是最佳的。没必要等待前一个请求结束，因为从技术上来说，可以同时提交多个请求，再等待它们的结果。而上述代码执行的大部分时间都花在了等待资源上，而在等待期间，机器什么都没做。理想情况下，应在等待已提交的任务结束时开始另一个新任务，这样可减少CPU等待时间，并在有了结果后立即处理。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;之所以能够采取这种策略，是因为这三个请求是完全独立的，无须等待前一个任务完成后再着手处理下一个任务。另外，单个CPU就能够处理这种情形。虽然将工作分配给多个CPU去完成可进一步提高执行速度，但如果相对于处理时间而言等待时间很长，这样做带来的速度提升将很有限。

#### 6.1.3 回调函数

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;为了让代码立即着手处理其他任务，需要想办法避免阻塞程序流程，让程序的其他部分能够继续完成其他任务。最简单的办法是使用回调函数。在example02.py中演示这种机制。将对阻塞代码time.sleep与threading.Timer进行比较。在这个示例中，编写一个函数wait_and_print，它将程序执行流程阻塞一秒，再打印一条消息。

```py
def wait_and_print(msg: str):
    time.sleep(1)
    print(msg)
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;要以非阻塞方式编写这个函数，可使用threading.Timer类。可初始化一个threading.Timer实例：传递要等待的时长以及一个回调函数。*回调函数*不过是一个将在定时器到期后被调用的函数。请注意，还必须调用方法Timer.start来激活定时器。

```py
import threading

def wait_and_print_async(msg: str):
    def callback():
        print(msg)    
    timer = threading.Timer(1, callback)
    timer.start()
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;函数wait_and_print_async的一个重要特征是，其中的所有语句都不会阻塞程序的执行流程。

```text
threading.Timer是如何做到在等待的同时不阻塞的呢？threading.Timer使用的策略是启动一个新线程，该线程能够并行地执行代码。
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;这种注册回调函数，以便在特定事件发生时执行它的方式称为*好莱坞原则*，阻塞版wait_and_print和非阻塞的差别，见example02.py。同步版本的行为：代码等待1秒钟，打印First call，再等待1秒钟，然后打印消息Second call和After call。在异步版本中，wait_and_print_async提交(而不是执行)这些调用并立即接着往前走。从输出可知，立即打印了消息After submission，这说明这种机制发挥了作用。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;使用回调函数重写network_request。定义函数network_request_async。相比于阻塞版，函数network_request_async最大的不同在于它什么都没有返回，这是因为在network_request_async被调用时，只提交请求，而结果要等到请求完成后才能得到。既然什么都不返回，如何传递请求的结果？将结果作为参数传递给回调函数on_done，而不是返回它。在文件example03.py中，向timer.Timer类提交了一个回调函数(timer_done)，它将在准备就绪后调用on_done。

```py
def network_request_async(number, on_done):
    def timer_done():
        on_done({"success": True, "result": number ** 2})  
    timer = threading.Timer(1, timer_done)
    timer.start()
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;要在fetch_square中使用network_request_async，需要对其进行修改，以使用异步结构。在下面的代码中，修改了fetch_square，定义了回调函数on_done并将其传递给network_request_async。

```py
def fetch_square(number):
    def on_done(response):
        if response["success"]:
            print(f'{number} ** 2 is {response["result"]}')
    network_request_async(number, on_done)
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;相比于同步代码，异步代码要复杂的多。这是因为每次需要获取结果时，都必须编写并传递一个回调函数。这导致代码一层套一层，变得难以理解。

#### 6.1.4 future

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;future是一种更简便的模式，可用来跟踪异步调用的结果。在前面的代码中，没有返回结果，而是接受一个回调函数，并在结果就绪后将其传递给这个回调函数。有趣的是，到目前为止，没有跟踪资源状态的简单途径。future是一种抽象，可帮助跟踪请求的资源并等到它可用。在python中，concurrent.futures.Future类提供了一种future实现。要创建这个类的实例，可调用其构造函数并不提供任何参数。

```py
fut = Future()
# 结果：
# <Future at 0x************ state=pending>
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;future表示一个还不可用的值，其字符串表示指出了结果的当前状态(这里为pending，即还未确定)。要让结果可用，可使用方法Future.set_result()。

```py
fut.set_result("Hello)
# 结果：
# <Future at 0x************ state=finished returned str>
fut.result()
# 结果：
# "Hello"
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;设置结果后，Future将指出任务结束了，此时可使用方法Future.result来访问结果。还可给future指定一个回调函数，这样一旦结果可用，就将执行这个回调函数。要指定回调函数，只需向方法Future.add_done_callback传递一个函数即可。这样任务结束后，指定的函数将被调用，并将Future实例作为第一个参数。在指定的回调函数中，可使用方法Future.result来访问结果。

```py
fut = Future()
fut.add_done_callback(lambda future: print(future.result(), flush=True))
fut.set_result("Hello")
# 输出：
# Hello
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;在文件example04.py中修改前面的函数network_request_async，在其中转而使用future。这里的理念时，不再什么都不返回，而是返回返回一个Future，用于跟踪结果。这里需要注意两点：

- 不再接受回调函数on_done，因为可在以后使用方法Future.add_done_callback来关联到回调函数。另外，将通用方法Future.set_result作为回调函数传递给threading.Timer。

- 这次可以返回一个值，因此代码与前一节介绍的阻塞版本更像。

```py
from concurrent.futures import Future
import threading

def network_request_async(number: float):
    future = Future()
    result = {"success": True, "result": number ** 2}
    timer = threading.Timer(1, lambda : future.set_result(result))
    timer.start()
    return future

fut = network_request_async(2)
```

```text
在这些示例中，直接实例化并管理future，但在世纪应用中，future是由框架处理的。
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;如果执行上述代码，什么都不会发生，因为这些代码只是创建并返回一个Future实例。要进一步操作future的结果，需要使用方法Future.add_done_callback。在下面的代码中，修改函数fetch_squaer以使用future。

```py
def fetch_square(number: float):
    fut = network_request_async(number)

    def on_done_future(future):
        response = future.result()
        if response["success"]:
            print(f'{number} ** 2 is {response["result"]}')
    fut.add_done_callback(on_done_future)
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;这些代码依然与回调版本很像。future提供了另一种使用回调函数的方式，而且更方便些。使用future也更好，因为它们能够跟踪资源状态，撤销已调度的任务以及以更自然的方式处理异常。

#### 6.1.5 事件循环

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;在很多异步框架中，并发任务之间的协调工作是由*事件循环*管理的。时间循环背后的理念是，不断地监视各种资源(如网络链接和数据库查询)的状态，并在事件发生(如资源准备就绪或定时器到期)时执行相应的回调函数。

```text
为什么不坚持使用线程？在有些情况下，事件循环是更加的选择，因为每个执行单元都不会与其他执行单元同时进行，这简化了共享变量，数据结构和资源的处理工作。
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;在本节的第一个示例中，将实现threading.Timer的非线性版本。自定义一个Timer类，它接受超时时间，并实现方法Timer.done(这个方法在定时器到期时返回True)。

```py
class Timer:

    def __init__(self, timeout: float):
        self.timeout = timeout
        self.start = time.time()
    def done(self):
        return time.time() - self.start > self.timeout
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;为判断定时器是否已到期，可编写一个循环，它不断调用方法Timer.done来检查定时器的状态。定时器到期后，可打印一条消息，并退出循环。

```py
timer = Timer(1)
while True:
    if timer.done():
        print("Timer is done!")
        break
```

```
通过使用循环不断轮询来等待事件发生，这通常会被称为忙等待(busy-waiting)。
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;通过以这样的方式实现定时器，可确保执行流程绝不会被阻塞，因此从原则上说，可在这个while循环中执行其他动作。理想情况下，应指定一个在定时器到期时执行的指定函数，就像threading.Timer中那样。为此，可实现方法Timer.on_timer_done，它接受一个要在定时器到期时执行的回调函数。

```py
class Timer:
    def __init__(self, timeout: float)
        self.tomeout = timeout
        self.start = time.time()
    def done(self):
        return time.time() - self.start > self.timeout  
    def on_timer_done(self, callback):
        self.callback = callback
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;请注意，on_timer_done只存储了一个指向回调函数的引用，负责监视事件并执行回调函数的是循环。下面来演示这一点。在这里，不再在循环中使用函数print，而是在合适的情况下调用timer.callback。

```py
timer = Timer(1)
timer.on_timer_done(lambda :print("Timer is done!"))

while True:
    if timer.done():
        timer.callback()
        break
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;一个异步框架的雏形已经形成。再循环外面，只定义了定时器和回调函数，监视定时器和执行回调函数的工作由循环负责。可进一步扩展这些代码，以支持多个定时器。为实现多个定时器，一种方法是将多个Timer实例添加到一个列表中，并修改循环，使其定时地检查所有的定时器，并在必要时调用回调函数。在下面的代码中，定义了两个定时器，并将每个定时器都关联到一个回调函数。这些定时器被添加到一个列表中。时间循环不断地监视这个列表，一旦有定时器到期，就执行相应的回调函数，并将该定时器从该列表中删除。见文件example05.py。

```py
timers = []
timer1 = Timer(1)
timer1.on_timer_done(lambda: print("First timer is done!"))

timer2 = Timer(2)
timer2.on_timer_done(lambda: print("Second timer is done!"))

timers.append(timer1)
timers.append(timer2)

while True:
    for timer in timers:
        if timer.done():
            timer.callback()
            timers.remove(timer)
    # 如果列表中没有任何定时器，就退出循环：
    if len(timers) == 0:
        break
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;事件循环的主要局限在于*绝不能使用阻塞调用*，因为执行流程是由不断运行的循环管理的。可以想见，如果在循环中使用了阻塞语句(如time.sleep)，事件监视和回调函数分派将停止，直到阻塞调用完成。为避免这种情况，不使用阻塞调用(如time.sleep)，而是让事件循环负责检测资源是否已就绪，并在资源就绪后调用回调函数。通过避免阻塞执行线程，事件循环可同时监视多项资源。

```text
事件通知通常是通过操作系统调用(如Unix工具select)实现的，操作系统调用会在事件就绪后恢复程序执行，而不是忙等待。
```

### 6.2 asyncio框架

#### 6.2.1 协程

#### 6.2.2 将阻塞代码转换为非阻塞代码

### 6.3 响应式编程

#### 6.3.1 被观察者

#### 6.3.2 很有用的运算符

#### 6.3.3 hot被观察者和cold被观察者

#### 6.3.4 打造CPU监视器

### 6.4 小结
