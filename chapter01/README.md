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
```
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
```
$ pytest path/to/module.py::function_name
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;为执行test_evolve，可在控制台输入以下命令，将获得简单但信息丰富的输出：
```
$ pytest test_particle_simulator::test_evolve
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;编写好测试后，就可使用插件pytest-benchmark将测试作为基准测试程序来执行。如果修改函数test_evolve，使其接受一个名为benchmark的参数，框架pytest将自动将资源benchmark作为参数传递给这个函数。在pytest中，这些资源被称为测试夹具(fixture)。为调用基准测试资源，可将要作为测试基准程序的函数作为第一个参数，并在它后面制定其他参数。将test_veolve改成test_evolve_benchmark之后，再次执行上述命令即可。

### 使用cProfile找出瓶颈

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;核实程序的正确性并测量其执行时间后，便可着手找出需要进行优化的代码片段了。与整个程序相比，这些代码的规模通常很小。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;在python中标准库中，有两个剖析模块。
- 模块profile：这个模块完全是由python编写的，给程序执行带来了很大的开销。这个模块之所以出现在标准库中，原因在于其强大的平台支持和易于扩展。
- 模块cProfile：这是主要的剖析模块，其接口与profile相同。这个模块是使用C语言编写的，因此开销很小，适合用作通用的剖析器。

