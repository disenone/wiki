---
layout: post
title: 编写 Windows 下的 Memory Leak Detector
categories: [c++]
tags: [dev]
---

#### 检测内存泄露

至此，我们已经把龙珠都收集全了，下面正式召唤神龙。

我想做成可以局部检测内存泄露（这是跟 VLD 不同的地方，VLD 做的是全局的检测，并支持多线程）。所以我在实际替换函数的类`RealDetector`上又封装了一层`LeakDetector`，并把`LeakDetector`的接口暴露给使用者。使用时只需构造`LeakDetector`，即完成函数的替换并开始检测内存泄露，`LeakDetector`析构时会恢复原来的函数，中止内存泄露检测，并打印内存泄露检测结果。

用下面代码测试一下：

```cpp
#include "LeakDetector.h"
#include <iostream>
using namespace std;

void new_some_mem()
{
	char* c = new char[12];
	int* i = new int[4];
}

int main()
{
	auto ld = LDTools::LeakDetector("LeakDetectorTest.exe");
	new_some_mem();
    return 0;
}

```
