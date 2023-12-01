---
layout: post
title: test2
categories: [c++]
catalog: true
tags: [dev]
description: |
    本文的目的是要讲清楚 C/C++ 宏编程的规则和实现方法，让你不再惧怕看到代码里面的宏。
figures: []
---

本文的目的是要讲清楚 C/C++ 的宏编程的规则和实现方法，让你不再惧怕看到代码里面的宏。我会首先说说 C++ 标准 14 里面提到的关于宏展开的规则，然后通过修改 Clang 的源码来观察宏展开，最后基于这些知识来聊聊宏编程的实现。

本文的代码全部都在这里：[下载](assets/img/2021-3-31-cpp-preprocess/macros.cpp)，[在线演示](https://godbolt.org/z/coWvc5Pse)。

## 引子

我们可以通过执行命令 `gcc -P -E a.cpp -o a.cpp.i` 来让编译器对文件 `a.cpp` 只执行预处理并保存结果到 `a.cpp.i` 中。

首先我们先来看一些例子:

#### 递归重入（Reentrancy）

``` cpp
#define ITER(arg0, arg1) ITER(arg1, arg0) 

ITER(1, 2)          // -> ITER(2, 1)
```
