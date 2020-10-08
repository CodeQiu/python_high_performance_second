&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;通过使用多核进行并行处理，无须速度更快的处理器，就可让程序在给定时间内执行更多的计算。将问题划分成独立的子单元，并使用多个内核并行地处理这些子单元。

### 7.1 并行编程简介

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;要让程序并行地运行，必须将问题划分为可彼此独立(或几乎独立)运行的子单元。如果一个问题的各个子单元是完全彼此独立的，这个问题就是高度并行的。对数组的各个元素分别执行的操作就是一个典型的例子--这种操作只需直到当前处理的元素。另一个例子是前面的粒子模拟器：由于彼此不影响，每个粒子都是独立地运动的。对于高度并行的问题，其解决方案很容易实现，在并行架构上的性能也非常高。有些问题可划分为不同的子单元，但不同的子单元涉及的计算需要共享数据。在这种情况下，解决方案实现起来不那么容易，还可能因为通信开销带来的性能问题。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;假设有个粒子模拟器，其中的粒子在距离位于特定范围内时会彼此吸引。为并行地处理这个问题，将模拟箱划分成区域，其中每个区域都由一个不同的处理器来负责处理。如果每计算异步，有些粒子将与邻接区域内的粒子交互。未完成下一次迭代，相邻区域之间必须通告粒子的新位置。进程间通信的开销非常高，可能严重影响并行程序的性能。在并行程序中，处理数据通信的方式主要有两种：*共享内存*和*分布式内存*。在共享内存中，各个子单元可访问相同的内存空间。这种方法的优点在于，无须显式地处理通信，因为只需读写共享内存就够了。然而，多个进程试图同时访问并修改相同的内存单元时，将出现问题。因此，必须使用同步技术避免这样的冲突。在分布式内存模型中，每个进程都与其他进程完全分开，并有自己的内存空间。在这种情况下，必须显式地处理进程之间的通信。与共享内存相比，通信开销通常更高，因为数据可能穿过网络接口。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;以共享内存方式实现并行的一种常见方式是使用*线程*。线程是源自进程地独立子任务，并共享内存等资源。线程生成多个执行上下文并共享内存空间，而进程提供多个执行上下文，有自己的内存空间，因此必须显式地处理通信。python能够生成并处理线程，但使用线程不能改善性能。由于python解释器的设计，每次只能执行一个python指令，这种机制称为*全局解释器锁*(GIL).每当线程执行python语句时，都获取一个锁，执行完毕后，再释放这个锁。由于每次只有一个线程能够获得这个锁，因此一个线程获得这个锁后，其他线程就不能执行python语句。虽然GIL导致python指令无法并行执行，但在可释放这个锁的情况下(如在耗时地I/O操作或C语言扩展中)，依然可使用线程来实现并发。

```text
为何不将GIL删除呢？过去几年，有过很多这样的尝试，其中包括最近的GIL切除术实验。受希腊，要删除GIL并不那么容易，必须修改大部分python数据结构。另外，细粒度的锁定可能代价高昂，还可能导致单线程程序的性能急剧下降。虽然如此，有些python实现没有使用GIL，其中最著名的是Jython和IronPython。
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;通过使用进程而不是线程，可完全避开GIL。进程不共享内存区域，而且是彼此独立的--每个进程都有自己的解释器。进程有一些缺点：启动新进程通常比启动新线程慢；它们消耗的内存更多；进程间通信的速度可能很慢。另一方面，进程也非常灵活，分布在多台计算机中时可伸缩性更佳。

#### 图形处理单元

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;图形处理单元是特殊的处理器，是为运行计算机图形学应用程序而设计的。这些应用程序通常需要处理3D场景的几何结构，并将像素数组输出到屏幕。GPU执行的操作包括浮点数数组和矩阵运算。GPU就是为高效地运行与图形相关的操作而设计的，这是通过采用高度并行的体系结构来实现的。相比于CPU，GPU包含的小型处理单元要多得多。CPU以每秒60帧的速度生成数据，这比时钟速度更高的CPU的典型响应速度要慢得多。GPU专门用于执行浮点数运算，其体系结构与标准CPU有天壤之别。因此，要编译供GPU运行的程序，必须使用特殊的编程平台，如CUDA和OpenCL。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*统一计算设备体系结构*(CUDA)是一种NVIDIA专用的技术，提供了可在其他语言中访问的API。CUDA提供了工具NVCC，可用来编译使用CUDA C语言(类似于C)编写的GPU程序；它还提供了大量的库，这些库实现了高度优化的数学例程。*OpenCL*是一种开放技术，使用它编写的并行程序可针对各种目标平台(不同厂商生产的CPU和GPU)进行编译，因此对非NVIDIA设备来说，使用OpenCL是个不错的选择。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;GPU编程编程好像很神奇，但不要因此而抛弃CPU。GPU编程很棘手，而且仅在特定情况下才能受益于GPU体系结构。程序员必须明白将数据写入内存以及从内存读取数据的成本，还必须知道如何实现算法以充分发挥GPU体系结构的作用。一般而言。GPU可极大地提高单位时间内可执行的操作数(即吞吐量)，但它们需要更多的时间来准备要处理的数据。相反，CPU从头开始生成单个结果的速度要快得多(这被称为延时)。对于合适的问题，使用GPU可极大地提高速度(高达10-100倍)，因此，在改善数据密集型应用的性能方面，GPU提供了极其廉价的解决方案(要实现相同的速度提升，需要数百个CPU)。

### 7.2 使用多个进程

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;标准模块multiprocessing可用来生成多个进程，以快速并行化简单任务，同时避免GIL问题。这个模块的接口使用起来很容易，其中包含多个处理任务提交和同步的实用工具。

#### 7.2.1 Process和Pool类

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;要创建独立运行的进程，可从multiprocessing.Process派生出子类。可通过扩展方法__init__来初始化资源，还可通过实现方法Process.run来编写将在子进程中执行的代码。在下面的代码中，定义了一个Process类，它等待一秒钟再打印分配给自己的id。见文件example01.py。

```py
import multiprocessing
import time

class Process(multiprocessing.Process):
    def __init__(self, id):
        super(Process, id).__init__()
        self.id = id

    def run(self):
        time.sleep(1)
        print(f"I'm the process with id: {self.id}")
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;要生成进程，必须实例化Process类并调用方法Process.start。请注意，不直接调用Process.run，而是调用Process.start，它将创建一个新进程，进而调用方法Process.run。要创建并启动新进程，可在上述代码片段末尾加如下代码行。

```py
if __name__ == "__main__":
    p = Process(0)
    p.start()
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Process.start后面的指令将立即执行，而不是等到进程p结束后再执行。要等待任务结束，可使用方法Process.join,如下所示：

```py
if __name__ == "__main__":
    p = Process(0)
    p.start()
    p.join()
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;可启动4个并行执行的进程。在串行程序中，需要的总时间为4秒，但并行执行时，只需要1秒。在下面的代码中，创建了4个并行执行的进程。

```py
if __name__ == "__main__":
    processes = Process(1), Process(2), Process(3), Process(4)
    [p.start() for p in processes]
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;请注意，并行进程的执行顺序是无法预测的，它们以什么样的顺序执行取决于操作系统是如何调用的。为验证这一点，可执行上述代码多次。将会发现每次运行时进程的执行顺序都不同。multiprocessing暴露了一个便利的接口，能够轻松地给驻留在multiprocessing.Pool类中的进程分配任务。multiprocessing.Pool类生成一组进程(称为*工作进程*)。要提交任务，可使用这个类的方法apply/apply_async和map/map_async。方法Pool.map对列表中的每个元素执行指定的函数，并返回一个包含结果的列表，其用法与内置(串行)函数map相同。要使用并行映射(map)，必须先初始化一个multiprocessing.Pool对象。它将工作进程数作为第一个参数；如果没有指定，这个参数将为系统包含的内核数量。见文件example02.py。要初始化multiprocessing.Pool对象，可像下面这样做：

```py
pool = multiprocessing.Pool()
pool = multiprocessing.Pool(processes=4)
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;下面使用pool.map。如果有一个计算平方的函数，可将其应用于列表，方法是调用Pool.map，并将函数和输入列表作为参数传递给它，如下所示：

```py
def square(x:float):
    return x ** 2
input_list = [0,1,2,3,4]
output = pool.map(square, input_list)
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;函数Pool.map_async与Pool.map相同，但返回一个AsyncResult对象，而不是实际结果。调用Pool.map时，主程序将停止运行，直到所有工作进程处理完毕。使用map_async时，将立即返回一个AsyncResult对象，而不阻塞主程序，因此计算是在后台进行的。接下来，可随时使用方法AsyncResult.get来获取结果，代码见example03.py。如下所示：

```py
outputs_async = pool.map_async(square, input_list)
outputs = outputs_async.get()
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Pool.apply_async将单个函数组成的任务分配给一个工作进程，它将这个函数及其参数作为参数，并返回一个AsyncResult对象。可使用apply_async来获取类似于使用map的效果，见文件example04.py，如下所示：

```py
results_async = [pool.apply_async(square, (i,)) for i in range(100)]
results = [r.get() for i in results_async]
```

#### 7.2.2 接口Executor

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;从python3.2开始，就可使用模块concurrent.futures中的接口Executor来并行地执行python代码。ProcessPoolExecutor暴露的接口非常简单，至少相比于功能强大的multiprocessing.Pool来说如此。实例化ProcessPoolExecutor的方式与ThreadPoolExecutor类似，只需通过参数max_workers传入工作线程数量即可(这个参数默认为可用的CPU内核数量)。方法submit将一个函数作为参数，并返回一个Future,用于跟踪提交的函数执行的情况。方法map类似于函数Pool.map，但返回一个迭代器，而不是一个列表。文件example05.py。

```py
from concurrent.futures import ProcessPoolExecutor

executor = ProcessPoolExecutor(max_workers=4)
fut = executor.submit(square, 2)

# 结果：
# <Future at 0x********** state=running>
result = executor.map(square, [0,1,2,3,4])
list(result)
# 结果：
# [0,1,4,9,16]
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;要从一个或多个Future实例中提取结果，可使用函数concurrent.futures.wait和concurrent.futures.as_completed。函数wait将爱嗯一个future列表作为参数，并阻塞程序执行，直到所有future都执行完毕。然后，就可使用方法Future.result来提取结果了。函数as_completed也将一个函数作为参数，但返回一个包含结果的迭代器。文件example06.py。

```py
from concurrent.futures import wait, as_completed

fut1 = executor.submit(square, 2)
fut2 = executor.submit(square, 3)
wait([fut1, fut2])

# 然后就可使用fut1.result()和fut2.result()来提取结果了

results = as_completed([fut1, fut2])
list(results)
# 结果：
# [4, 9]
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;另外，可使用函数asyncio.run_in_executor来生成future，并使用asyncio库提供的工具和语法来操作结果，这样可同时实现并发和并行。

#### 7.2.3 使用蒙特卡洛方法计算pi的近似值

#### 7.2.4 同步和锁

### 7.3 使用OpenMP编写并行的Cython代码

### 7.4 并行自动化计算

#### 7.4.1 Theano初步

#### 7.4.2 Tensorflow

#### 7.4.3 在GPU中运行代码

### 7.5 小结
