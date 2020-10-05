&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Cython是一种扩展Python的语言，这是通过支持给函数，变量和类声明类型来实现的。这些类型声明让Cython能够将python脚本编译成高效的C语言代码。Cython还可充当python和C语言之间的桥梁，因为它提供了易于使用的结构，能够编写到外部C和C++例程的接口。

### 4.1 编译Cython扩展

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Cython语法被设计成python语法的超集。在不做任何修改的情况下，Cython就能够编译大部分python模块(例外的情况不多)。Cython源代码文件艾伦的扩展名为.pyx，可使用命令cython编译成C语言文件。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;例如在文件hello.pyx中的一个打印Hello, World！的简单函数，使用下面的cython命令读取文件艾伦hello.pyx，并生成文件hello.c。
```shell
$ cython hello.pyx
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;为将hello.c编译成python扩展模块，使用编译器GCC。需要添加一些python专用的编译选项，这些选项因操作系统而异。必须指定包含头文件艾伦的目录，如下命令：
```shell
$ gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing -lm -I/./ -o hello.so hello.c
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;报错fatal error: Python.h: 没有那个文件或目录，安装python3-dev和python-dev-tools尚未解决。

### 4.2 添加静态类型

#### 4.2.1 变量

#### 4.2.2 函数

#### 4.2.3 类

### 4.3 共享声明

### 4.4 使用数组

#### 4.4.1 C语言数组和指针

#### 4.4.2 NumPy数组

#### 4.4.3 类型化内存视图

### 4.5 使用Cython编写粒子模拟器

### 4.6 剖析Cython代码

### 4.7 在Jupyter中使用Cython

### 4.8 小结
