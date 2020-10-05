&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;就提高代码速度而言，最重要的是找出程序中速度缓慢的部分。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;通过剖析(profiling)，可确定应用程序的哪些部分消耗的资源最多。剖析器(profiler)是这样一种程序：运行应用程序并监控各个函数的执行时间，以确定应用程序中哪些函数占用的时间最多。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;python提供了多个工具，可帮助找出瓶颈并度量重要的性能指标。本章将介绍如何使用标准模块cProfile和第三方包line_profiler，还将介绍如何使用工具memory_profiler剖析应用程序的内存占用情况。本章还将介绍另一个很有用的工具--KCachegrind，使用它能以图形化方式显示各种剖析器生成的数据。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;基准测试程序(benchmark)是用于评估应用程序总体执行时间的小型脚本。本章将介绍如何编写基准测试程序以及如何准确地测量程序的执行时间。

### 1.1 设计应用程序

- 让它能够运行
- 确保设计正确
- 提高运行速度

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;在本节中，编写一个粒子模拟器测试应用程序并对其进行剖析。这个模拟器程序接受一些粒子，并根据指定的规则模拟这些粒子随时间流逝的运动情况。

### 1.2 编写测试和基准测试程序

#### 测量基准测试程序的运行时间

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;要计算基准测试程序的运行时间，一种方式是使用Unix命令time。

```text
$ time python 脚本名.py
real    ****s
user    ****s
sys     ****s
    默认情况下，time显示3个指标：
        real:从头到尾运行进程实际花费的时间。
        user:在计算期间，所有CPU花费的总时间。
        sys:在执行与系统相关的任务(如内存分配)期间，所有CPU花费的总时间。
    在某些情况下，user与sys的和可能大于real，这是因为可能有多个处理器在并行地工作。
```

### 1.3 使用pytest-benchmark编写更加的测试和基准测试程序

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;测试框架是一组测试工具，可简化编写/执行和调试测试的工作，还提供了丰富的测试结果报告和摘要。使用pytest框架时，建议将测试和应用程序代码放在不同的文件中。创建test_particle_simulator.py文件为测试文件。要执行特定的测试，可使用语法：

```text
$ pytest path/to/module.py::function_name
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;为执行test_evolve，可在控制台输入以下命令，将获得简单但信息丰富的输出：

```text
$ pytest test_particle_simulator::test_evolve
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;编写好测试后，就可使用插件pytest-benchmark将测试作为基准测试程序来执行。如果修改函数test_evolve，使其接受一个名为benchmark的参数，框架pytest将自动将资源benchmark作为参数传递给这个函数。在pytest中，这些资源被称为测试夹具(fixture)。为调用基准测试资源，可将要作为测试基准程序的函数作为第一个参数，并在它后面制定其他参数。将test_veolve改成test_evolve_benchmark之后，再次执行上述命令即可。

### 1.4 使用cProfile找出瓶颈

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;核实程序的正确性并测量其执行时间后，便可着手找出需要进行优化的代码片段了。与整个程序相比，这些代码的规模通常很小。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;在python中标准库中，有两个剖析模块。

- 模块profile：这个模块完全是由python编写的，给程序执行带来了很大的开销。这个模块之所以出现在标准库中，原因在于其强大的平台支持和易于扩展。
- 模块cProfile：这是主要的剖析模块，其接口与profile相同。这个模块是使用C语言编写的，因此开销很小，适合用作通用的剖析器。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;无须对其源代码做任何修改，就可对现有python脚本或函数执行cProfile。要在命令行使用cProfile，可像下面这样做：

```text
$ python -m cProfile python_filename.py
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;这将打印长长的输出，其中包括针对应用程序中调用的所有函数的多个指标。要按特定的指标对输出进行排序，可使用选项-s。在下面的示例中，输出是按后面的指标tottime排序的。

```text
$ python -m cProfile -s tottime python_filename.py
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;要将cProfile生成的数据保存到输出文件中，可使用选项-o。cProfile使用模块stats和其他工具能够识别的格式。下面演示了选项-o的用法。

```text
$ python -m cProfile -o prof.out python_filename.py
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;要cProfile作为python模块使用，必须像下面这样调用函数cProfile.run。

```py
from modulename import testfunc
import cProfile

cProfile.run("testfunc()")
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;还可调用对象cProfile.Profile的方法的代码之间包含一段代码，如下所示：

```py
from modulename import testfunc
import cProfile

pr = cProfile.Profile()
pr.enable()
testfunc()
pr.disable()
pr.print_stas()
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;也可在IPython中以交互的方式使用cProfile。魔法命令%prun能够剖析特定的函数调用。

```text
cProfile的输出分成了5列：
    - ncalls：函数被调同的次数。
    - tottime：执行函数花费的总时间，不考虑其他函数调用。
    - cumtime：执行函数花费的总时间，考虑其他函数调用。
    - percall：单次函数调用花费的时间--可通过将中时间除以调用次数得到。
    - filename:lineno：文件名和相应的行号。
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;最重要的指标是tottime，它表示执行函数花费的时间(不包含子调用)，能够知道瓶颈在那里。在文件夹cProfile_taylor中编写递归函数计算exp(x)和sin(x)的泰勒章开始的多项式。

### 1.5 使用line_profiler逐行进行剖析

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;要使用line_profiler，需要对要监视的函数应用装饰器@profile。请注意，无须从其他模块中导入函数profile，因为运行剖析脚本kernporf.py时，它将被注入全局命名空间。要对程序进行剖析，需要给函数evolve添加装饰器@profile。

```py
@profile
def evolve(self, dt):
    # 代码
    pass
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;脚本kernprof.py生成一个输出文件，并将剖析结果打印到标准输出。运行这个脚本时，应指定两个选项：

- l:以使用函数line_profiler
- v:以立即将结果打印到屏幕

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;下面演示了kernprof.py的用法：

```text
$ kernprof -l -v python_script.py
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;也可在Ipython中运行这个剖析器，这样可以进行交互式编辑。应该首先加载line_profiler扩展，它提供了魔法命令lprun。使用这个命令，就无须添加装饰器@profile。输出非常直观。分成了6列：

```text
- line # : 运行的代码行号。
- Hits   : 代码行运行的次数。
- Time   : 代码行的执行时间，单位为微秒。
- Per Hit: Time/Hits。
- % Time : 代码行总执行时间所占的百分比。
- Line Contents: 代码行的内容。
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;只需要查看% Time列，就可以清楚的知道时间都花在了什么地方。

### 1.6 优化代码

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;要优化纯粹的python代码，其中效果最显著的方式是对使用的算法进行改进。另一种方式是最大限度地减少指令数，交换循环顺序，较少中间变量。

### 1.7 模块dis

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;在CPython解释器中，Python代码首先被转换为中间表示--字节码，再由python解释器执行。要了解代码是如何转换为字节码的，可使用python模块dis(dis表示disassemble，即反汇编)。这个模块的用法非常简单，只需对目标代码调用函数dis.dis即可。

```py
import dis
from modulename import funcname
dis.dis(funcname)
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;这将打印美方代码对应的字节码指令列表。

### 1.8 使用memory_profiler剖析内存使用情况

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;memory_profiler要求对源代码进行处理：要给监视的函数加上装饰器@profile。在particle_simulator.py中对函数benchmark改造为函数benchmark_memory，以实例化大量Particle实例，并缩短模拟时间。

```shell
$ python -m memory_profiler python_script.py
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;为减少内存消耗，可在Particle类中使用__slots__。这将避免将实例的变量存储在内部字典中，从而节省一些内存。然而，这种策略也有缺点：不能添加__slots__中没有指定的属性。

```py
class Particle():
    __slots__ = ("x", "y", "ang_vel")

    def __init__(self, x, y, ang_vel):
        self.x = y
        self.y = y
        self.ang_vel = ang_vel
```

### 1.9 小结

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;优化时，首先是测试，并找出应用程序的瓶颈。
