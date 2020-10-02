&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;改善应用程序的性能，最有效的方式之一是使用更合适的算法和数据结构。

### 2.1 有用的算法和数据结构

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;计算复杂度是一个描述执行任务所需资源的指标，可根据它对算法进行分类。这样的分类是使用大O表示法来表示的。所谓大O表示法，指的是为完成任务需要执行的操作数的上限，这通常取决于输入的规模。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;例如，要将列表的每个元素都加1，可像下面这样使用一个for循环来实现：
```py
input_nums = list(range(10))
for i,_ in enumerate(input_nums):
    input[i] += 1
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;如果操作不依赖于输入的规模(如访问列表的第一个元素)，相应算法所需要的时间就被认为是固定的，用O(1)表示。这意味着不管有多少数据，运运行算法所需要的时间都相同。在上述简单的算法中，操作input[i] += 1将重复10次，这与输入的规模相同。如果将输入的规模翻倍，操作数将成比例地增加。由于操作数与输入规模成正比，这种算法所需要的时间为O(N),其中N为输入的规模。有些情况下，运算时间可能取决于输入的结构，如集合是否是有序的，以及是否包含很多重复的元素。

#### 2.1.1 列表和双端队列
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;python列表是有序的元素集合，在python中是使用大小可调整的数组实现的。数组是一种基本数据结构，由一系列连续的内存单元组成，其中每个内存单元都包含指向一个python对象的引用。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;要访问或修改元素，需要从底层数组的相应位置获取对象引用，因此其复杂度为O(1)。当茶ungjian一个空列表时，将分配一个长度固定的数组；而当插入元素时，数组中的位置将逐渐被填满。当所有位置都被占据后，列表需要增大其底层数组的长度，进而触发内存的重新分配，这需要的时间为O(N)。在列表开头(或中间)添加或删除元素的操作可能在效率方面存在问题。在列表开头插入或删除元素时，后续所有元素都需要移动一个位置，因此需要的时间为O(N)。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;在某些情况下，必须高效地执行在集合开头和末尾插入或删除元素的操作，python通过collections.deque类提供了一种具有这种特征的数据结构。dequ指的是双端队列，在python中，双端队列是以双向链表的方式实现的。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;模块bisect能够在有序数组中进行快速查找。对于有序列表，可使用函数bisect.bisect来确定将元素插入到什么位置，同时可确保插入后列表依然是有序的。从下面的示例可知，要在列表中插入元素3，并确保插入后列表依然是有序的，应将元素3放在第三个位置(对应的索引为2)。
```py
import bisect
collection = [1, 2, 4, 5, 6]
bisect.bisect(collection, 3)
# 结果:2
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;这个函数使用二分查找算法，运行时间为O(log(N))。如果要插入的值已包含在列表中，函数bisect.bisect将返回这个既有值后面的位置。因此，可以使用变种bisect.bisect_left，它以下面的方式返回正确的索引。
```py
def index_bisect(a, x):
    “找到第一个与x相同的值”
    i = bisect.bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    raise ValueError
```

#### 2.1.2 字典
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;字典是以散列映射的方式实现的。在插入/删除和访问元素方面操作的时间复杂度都是O(1)。
```text
在python3.5及以前的版本中，字典是无序集合，但从python3.6起，字典能够保留元素的插入顺序。
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;散列映射是一种将键关联到值的数据结构，其背后的原理是给每个键都指定索引，以便将关联的值存储在数组中。索引可使用散列函数计算得到；python为多种数据类型实现了散列函数，例如，获取散列码的通用函数是hash。下面的粒子演示了如何在给定字符串"hello"的情况下获取散列码。
```py
# 每次启动解释器，hash结果不一定相同。
# 在默认情况下，str和bytes对象的__hash__()值会使用一个不可预知的随机值“加盐”。
# 虽然它们在一个单独python进程中会保持不变，但它们的值在重复运行的python间是不可预测的。
# 这种做法是为了防止拒绝服务攻击：通过仔细选择输入来利用字典插入操作在最坏的情况下执行效率即O(n^2)复杂度。
hash("hello")
# 结果是: -6682460587834533392

# 要得到的数字限定在特定范围内，可使用求模运算符
hash("hello") % 10
# 结果是: 8
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;散列映射实现起来可能比较棘手，因为它们需要处理冲突，即两个不同对象的散列码相同。然而，所有的复杂性都被隐藏在实现后面，且在大多数情况下，默认的冲突解决方案就挺管用。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;使用字典可高效地计算列表中独特元素的个数。在dict_counter.py中使用了三种方式实现。时间复杂度都相同。

##### 使用散列映射在内存中创建查找索引
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;使用字典可在文档列表中快速查找特定的单词。假设有一个包含4个文档的集合，要获取与查找匹配的所有文档，一种简单的方式是扫描每个文档，并检查其中是否包含指定的单词，这种方法简单，对一次性查询来说挺管用的，但如果需要频繁地查询这个集合，对查询时间进行优化将大有裨益。由于线性扫描的总查询开销为O(N)，因此，提高可伸缩型后，将能够处理大得多的文档集合。
```py
docs = ["the cat is under the table",
        "the dog is under the table",
        "cats and dogs smell roses",
        "Carla eats an apple"]

matches = [doc for doc in docs if "table" in doc]
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;一种更佳的策略是花些时间对文档进行预处理，以便查询时更容易找到它们。可以创建一个名为*反向索引*的结构，它将集合中的每个单词都关联到包含该词的文档列表。在前面的示例中,单词table将关联到文档the cat is under the table和the dog is under the table，而这两个文档的索引分别为0和1。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;为实现这种映射，可遍历文档集合，并将包含指定单词的文档的索引存储在一个字典中。这种实现与函数count_dict_func1类似，但不累积计数器，而是不断增大列表，其中包含与指定单词匹配的文档。如文件docs_search_index.py中。有了索引后，查询集合时只需要执行一次字典访问操作，有了反向索引，无论查询多少文档(只要它们都能够加入到内存中)，所需要的时间都一样。创建反向索引是一种代价高昂的操作，必须考虑每个可能的查询。

#### 2.1.3 集
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
