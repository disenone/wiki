---
layout: post
title: C/C++ 宏編程解析
categories:
- c++
catalog: true
tags:
- dev
description: 本文的目的是要講清楚 C/C++ 宏編程的規則和實現方法，讓你不再懼怕看到程式碼裡面的巨集。
figures: []
---

<meta property="og:title" content="C/C++ 宏编程解析" />

這篇文章的目的在於清楚解釋 C/C++ 的巨集編程規則與實現方法，讓您不再害怕看到程式碼中的巨集。我將首先談談 C++標準 14 中提到的有關巨集展開的規則，然後通過修改 Clang 的原始碼來觀察巨集展開，最後基於這些知識來討論巨集編程的實現。

這裡是本文的所有程式碼：[下載](assets/img/2021-3-31-cpp-preprocess/macros.cpp)，[線上展示](https://godbolt.org/z/coWvc5Pse)抱歉，這個輸入太短了，無法翻譯。

##序言

我們可以透過執行指令 `gcc -P -E a.cpp -o a.cpp.i` 讓編譯器僅執行預處理過程並將結果保存在 `a.cpp.i` 檔案中。

首先讓我們來看一些例子：

####重入递归（Reentrancy）

``` cpp
#define ITER(arg0, arg1) ITER(arg1, arg0)

ITER(1, 2)          // -> ITER(2, 1)
```

宏 `ITER` 交換了 `arg0`, `arg1` 的位置。宏展開後，得到的是 `ITER(2, 1)`。

可以看到，`arg0` `arg1` 的位置成功交換，在這裡巨集成功展開了一次，但也只展開了一次，不再遞歸重入。換言之，巨集的展開過程中，是不可自身遞歸重入的，如果在遞歸的過程中發現相同的巨集在之前的遞歸中已經展開過，則不再展開，這是巨集展開的其中一條重要的規則。禁止遞歸重入的原因也很簡單，就是為了避免無限遞歸。

####字串串連

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                // -> HelloWorld
CONCAT(Hello, CONCAT(World, !))     // ->　HelloCONCAT(World, !)
```

宏 `CONCAT` 的目的是拼接 `arg0` 和 `arg1`。當展開這個宏時，`CONCAT(Hello, World)` 會正確得到結果 `HelloWorld`。然而，`CONCAT(Hello, CONCAT(World, !))` 則只展開了外層的宏，內層的 `CONCAT(World, !)` 沒有被展開，而是直接與 `Hello` 拼接在一起。這與預期不同，我們真正想要的結果是 `HelloWorld!`。這也是另一條宏展開的重要規則：跟著 `##` 操作符的宏參數不會被展開，會直接與前面的內容拼接在一起。

透過上述兩個例子，可以看出，宏展開的規則有一些是違背直覺的。假如不了解具體規則，可能寫出來的宏與我們期望的效果不一致。

##擴展規則

透過引子中的兩個例子，我們了解到宏展開具有一套標準的規則，這套規則定義在C/C++標準中，內容並不多，建議先細讀幾遍，我也順便提供了標準版本n4296的連結，宏展開在第16.3節：[傳送門](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4296.pdf)我選取n4296版本中一些重要的規則，這些規則將決定如何正確撰寫宏（建議花點時間展開細讀標準中的宏部分）。

####參數分隔

宏的參數要求是用逗號分隔，而且參數的個數需要跟宏定義的個數一致，傳遞給宏的參數中，額外用括號包圍的內容視為一個參數，參數允許為空：

``` cpp
#define ADD_COMMA(arg1, arg2) arg1, arg2

ADD_COMMA(a, b)             // -> a, b
ADD_COMMA(a)                // 錯誤：宏"MACRO"需要2個參數，但只提供了1個。
ADD_COMMA((a, b), c)        // -> (a, b), c
ADD_COMMA(, b)              // -> , b
```

在 `ADD_COMMA((a, b), c)` 中，將 `(a, b)` 視為第一個參數。 在 `ADD_COMMA(, b)` 中，由於第一個參數為空，因此展開為 `, b`。

####宏參數展開

在展開宏時，如果宏的參數也是可展開的宏，會先將參數完全展開，再展開宏，例如。

``` cpp
ADD_COMMA(ADD_COMMA(1, 2), ADD_COMMA(3, 4))     // -> 1, 2, 3, 4
```

一般情況下的宏展開，都可以認為是先對參數求值，再對宏求值，除非遇到了 `#` 和 `##` 操作符。

####`#` 操作符

`#` 操作符後面跟的巨集參數，不會進行展開，會直接字串化，例如：

``` cpp
#define STRINGIZE(arg0) # arg0

STRINGIZE(a)                // -> "a"
STRINGIZE(STRINGIZE(a))     // -> "STRINGIZE(a)"
```

根據這條規則 `STRINGIZE(STRINGIZE(a))` 只能展開為 `"STRINGIZE(a)"`。

####`##` 運算子

`##`操作符前后的宏參數，都不會進行展開，會先直接拼接起來，例如：

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                        // -> HelloWorld
CONCAT(Hello, CONCAT(World, !))             // -> HelloCONCAT(World, !)
CONCAT(CONCAT(Hello, World) C, ONCAT(!))    // -> CONCAT(Hello, World) CONCAT(!)
```

`CONCAT(CONCAT(Hello, World) C, ONCAT(!))` 只能是先拼接在一起，得到 `CONCAT(Hello, World) CONCAT(!)`。

####重複掃描

預處理器執行完一次巨集展開之後，將重新掃描獲得的內容，持續展開直到無法再展開為止。

一次宏展开，可以理解為先把參數完全展開（除非遇到 `#` 和 `##`），再根據巨集的定義，把巨集和完全展開後的參數按照定義進行替換，再處理定義中的所有 `#` 和 `##` 操作符。

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define STRINGIZE(arg0) # arg0

CONCAT(STRING, IZE(Hello))        // -> STRINGIZE(Hello) -> "Hello"
```

`CONCAT(STRING, IZE(Hello))` 第一次掃描展開得到 `STRINGIZE(Hello)`，然後執行第二次掃描，發現 `STRINGIZE` 可以繼續展開，最後得到 `"Hello"`。

####禁止遞歸重入

在重覆掃描的過程中，禁止遞迴展開相同的巨集。可以把巨集展開理解為樹形的結構，根節點就是一開始要展開的巨集，每個巨集展開之後的內容作為該巨集的子節點連接到樹上，那麼禁止遞迴就是在展開子節點的巨集時，如果該巨集跟任意祖先節點的巨集相同，則禁止展開。來看一些例子：

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define CONCAT_SPACE(arg0, arg1) arg0 arg1
#define IDENTITY(arg0) IDENTITY_IMPL(arg0)
#define IDENTITY_IMPL(arg0) arg0

CONCAT(CON, CAT(a, b))                  // -> CONCAT(a, b)
IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))   // -> CONCAT(a, b)
IDENTITY(CONCAT(CON, CAT(a, b)))        // -> IDENTITY_IMPL(CONCAT(a, b)) -> CONCAT(a, b)
```

`CONCAT(CON, CAT(a, b))`：因為 `CONCAT` 是用 `##` 拼接兩個參數，根據 `##` 的規則，不會展開參數，直接拼接。所以第一次展開得到了 `CONCAT(a, b)`，由於 `CONCAT` 已經展開過了不會再遞歸展開，所以停止。

`IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))`：`IDENTITY_IMPL` 可以被理解為對參數 `arg0` 求值，這裡的參數 `arg0` 求值後得到了 `CONCAT(a, b)`，由於遞歸被標記為禁止重入，完成 `IDENTITY_IMPL` 展開後，在第二次掃描時發現是被標記為禁止重入的 `CONCAT(a, b)`，因此停止展開。在這裡 `CONCAT(a, b)` 是由參數 `arg0` 展開而來，但在後續展開時，也將保持禁止重入標記，可理解為父節點為參數 `arg0`，持續保持著禁止重入的標記。

`IDENTITY(CONCAT(CON, CAT(a, b)))`：這個範例的目的在於強化對父子節點之間關係的理解。當參數展開時，本身作為父節點，展開後的內容則作為子節點進行遞迴判斷。展開後的參數傳遞到巨集定義後，禁止重入的標記將繼續保留（如果傳遞後未改變展開後的參數）。可以將參數的展開過程視為另一棵樹，展開後的結果是該樹的最底層子節點，當這個子節點傳遞給巨集執行展開時，仍然保留著禁止重入的特性。

例如在這個情況下，當第一次完全展開後獲得 `IDENTITY_IMPL(CONCAT(a, b))`，`CONCAT(a, b)` 被標記為禁止重入，即使`IDENTITY_IMPL` 是對參數求值的，但由於參數已經被禁止展開，所以參數最終原模原樣地傳遞到定義裡，最終我們仍然得到 `CONCAT(a, b)`。

我只列了一些我覺得比較重要或較難理解的規則，若想更詳細了解規則，建議花時間直接閱讀標準文件。

##透過 Clang 觀察展開過程

(https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-11.1.0.tar.gz)修改過的文件（請參閱[傳送門](assets/img/2021-3-31-cpp-preprocess/clang-modify.zip)通過下面的例子簡單驗證之前介紹的宏展開規則：

####例子1

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(C, ONCAT(a, b))      // CONCAT(a, b)
```

使用修改過的 Clang 來預處理以上程式碼：`clang -P -E a.cpp -o a.cpp.i`，得到下面的列印訊息：

``` text linenums="1"
HandleIdentifier:
MacroInfo 0x559e57496900
    #define <macro>[2813:CONCAT](arg0, arg1) arg0 ## arg1
Macro is ok to expand

EnterMacro: 0

Enter ExpandFunctionArguments:
MacroInfo 0x559e57496900 used
    #define <macro>[2813:CONCAT](arg0, arg1) arg0 ## arg1
Token: 0
identifier: arg0
Args: [identifier: C]
Token: 1
hashhash:
Token: 2
identifier: arg1
Args: [identifier: ONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ]
Leave ExpandFunctionArguments: [identifier: C][hashhash: ][identifier: ONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ]

LeaveMacro: 0

HandleIdentifier:
MacroInfo 0x559e57496900 disabled used
    #define <macro>[2813:CONCAT](arg0, arg1) arg0 ## arg1
Macro is not ok to expand
```

(#__codelineno-9-1)當處理`HandleIdentifier`時遇到宏時，會進行列印，然後列印宏的訊息（第[2-4](#__codelineno-9-2)按照定义，宏可以展开，因此可以继续 `Macro is ok to expand`，然后进入宏 `EnterMacro`。

真正執行宏展開的函數是 `ExpandFunctionArguments`，之後再次打印待展開的宏資訊，注意到此時宏已經被標記為 `used` （第 [9](#__codelineno-9-9)根據所定義的宏，逐一展開 `Token` （`Token` 在 `Clang` 預處理中的概念，這裡不深入說明）。

第0個`Token`是形參`arg0`，對應的實參是`C`，判斷不需要展開，於是直接複製到結果上（第[11-13](#__codelineno-9-11)行）。

第1個`Token`是`hashhash`，也就是`##`操作符，繼續複製到結果上（第[14-15](#__codelineno-9-14)（行）。

第2個`Token`是形參`arg1`，對應的實參是`ONCAT(a, b)`，預處理器也會把實參處理成一個個的`Token`，所以可以看到列印的結果用中括號包住了實參的每個`Token`（第18行），由於`##`的原因這個實參依然不需要展開，所以還是直接複製到結果上（第[16-18](#__codelineno-9-16)行）。

最後 `Leave ExpandFunctionArguments` 列印本次掃描展開得到的結果（第 [19](#__codelineno-9-19)請將這些文字翻譯成繁體中文：

行），把結果的 `Token` 都翻譯過來就是 `C ## ONCAT(a, b)`，之後預處理器就執行 `##` 運算子來生成新的內容。  

執行後獲得 `CONCAT(a, b)`，遇到巨集 `CONCAT`，預處理仍然先進入 `HandleIdentifier`，列印巨集資訊，發現該巨集狀態為 `disable used`，已經擴展過了，禁止再次進入，顯示 `Macro is not ok to expand`，預處理器不再擴展，最終獲得的結果就是 `CONCAT(a, b)`。

####範例2

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define IDENTITY(arg0) arg0

IDENTITY(CONCAT(C, ONCAT(a, b)))
```

<details>
<summary> <font> Clang 印出資訊（點擊展開）：</font> </summary>
``` test linenums="1"
HandleIdentifier:
MacroInfo 0x562a148f5a60
    #define <macro>[2853:IDENTITY](arg0) arg0
Macro is ok to expand

HandleIdentifier:
MacroInfo 0x562a148f5930
    #define <macro>[2813:CONCAT](arg0, arg1) arg0 ## arg1

EnterMacro: 0

Enter ExpandFunctionArguments:
MacroInfo 0x562a148f5a60 used
    #define <macro>[2853:IDENTITY](arg0) arg0
Token: 0
identifier: arg0
Args: [identifier: CONCAT][l_paren: ][identifier: C][comma: ][identifier: ONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ][r_paren: ]
getPreExpArgument: [identifier: CONCAT][l_paren: ][identifier: C][comma: ][identifier: ONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ][r_paren: ][eof: ]

HandleIdentifier:
MacroInfo 0x562a148f5930
    #define <macro>[2813:CONCAT](arg0, arg1) arg0 ## arg1
Macro is ok to expand

EnterMacro: 1

Enter ExpandFunctionArguments:
MacroInfo 0x562a148f5930 used
    #define <macro>[2813:CONCAT](arg0, arg1) arg0 ## arg1
Token: 0
identifier: arg0
Args: [identifier: C]
Token: 1
hashhash:
Token: 2
identifier: arg1
Args: [identifier: ONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ]
Leave ExpandFunctionArguments: [identifier: C][hashhash: ][identifier: ONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ]

LeaveMacro: 1

HandleIdentifier:
MacroInfo 0x562a148f5930 disabled used
    #define <macro>[2813:CONCAT](arg0, arg1) arg0 ## arg1
Macro is not ok to expand
ResultArgToks: [identifier: CONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ]
Leave ExpandFunctionArguments: [identifier: CONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ]

LeaveMacro: 0

HandleIdentifier:
MacroInfo 0x562a148f5930 used
    #define <macro>[2813:CONCAT](arg0, arg1) arg0 ## arg1
Macro is not ok to expand
```

</details>

第 [12](#__codelineno-11-12)根據開始展開`IDENTITY`時，發現參數`Token 0`是`CONCAT(...)`，同時也是一個巨集，因此首先對該參數進行評值。

(#__codelineno-11-27)行開始展開參數宏 `CONCAT(...)`，跟例子 1 一樣，多次掃描展開完成後得到 `CONCAT(a, b)` （第 [46](#__codelineno-11-46)行）。

第 [47](#__codelineno-11-47)結束對 `IDENTITY` 的展開，得到的結果是 `CONCAT(a, b)`。

(#__codelineno-11-51)重新掃描`CONCAT(a, b)`時發現，儘管它是一個巨集，在之前的參數展開過程中已被設置為`used`，無需再進行遞歸展開，直接作為最終結果。

####範例 3

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define IDENTITY_IMPL(arg0) arg0
#define IDENTITY(arg0) IDENTITY_IMPL(arg0)

IDENTITY(CONCAT(C, ONCAT(a, b)))
```

<details>
<摘要> <字型>Clang 打印資訊（點擊展開）：</字型> </摘要>
``` test linenums="1"
HandleIdentifier:
MacroInfo 0x55e824457a80
    #define <macro>[2853:IDENTITY_IMPL](arg0) arg0

HandleIdentifier:
MacroInfo 0x55e824457ba0
    #define <macro>[2886:IDENTITY](arg0) IDENTITY_IMPL(arg0)
Macro is ok to expand

HandleIdentifier:
MacroInfo 0x55e824457950
    #define <macro>[2813:CONCAT](arg0, arg1) arg0 ## arg1

EnterMacro: 0

Enter ExpandFunctionArguments:
MacroInfo 0x55e824457ba0 used
    #define <macro>[2886:IDENTITY](arg0) IDENTITY_IMPL(arg0)
Token: 0
identifier: IDENTITY_IMPL
Token: 1
l_paren:
Token: 2
identifier: arg0
Args: [identifier: CONCAT][l_paren: ][identifier: C][comma: ][identifier: ONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ][r_paren: ]
getPreExpArgument: [identifier: CONCAT][l_paren: ][identifier: C][comma: ][identifier: ONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ][r_paren: ][eof: ]

HandleIdentifier:
MacroInfo 0x55e824457950
    #define <macro>[2813:CONCAT](arg0, arg1) arg0 ## arg1
Macro is ok to expand

EnterMacro: 1

Enter ExpandFunctionArguments:
MacroInfo 0x55e824457950 used
    #define <macro>[2813:CONCAT](arg0, arg1) arg0 ## arg1
Token: 0
identifier: arg0
Args: [identifier: C]
Token: 1
hashhash:
Token: 2
identifier: arg1
Args: [identifier: ONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ]
Leave ExpandFunctionArguments: [identifier: C][hashhash: ][identifier: ONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ]

LeaveMacro: 1

HandleIdentifier:
MacroInfo 0x55e824457950 disabled used
    #define <macro>[2813:CONCAT](arg0, arg1) arg0 ## arg1
Macro is not ok to expand
ResultArgToks: [identifier: CONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ]
Token: 3
r_paren:
Leave ExpandFunctionArguments: [identifier: IDENTITY_IMPL][l_paren: ][identifier: CONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ][r_paren: ]

LeaveMacro: 0

HandleIdentifier:
MacroInfo 0x55e824457a80
    #define <macro>[2853:IDENTITY_IMPL](arg0) arg0
Macro is ok to expand

HandleIdentifier:
MacroInfo 0x55e824457950 used
    #define <macro>[2813:CONCAT](arg0, arg1) arg0 ## arg1

EnterMacro: 2

Enter ExpandFunctionArguments:
MacroInfo 0x55e824457a80 used
    #define <macro>[2853:IDENTITY_IMPL](arg0) arg0
Token: 0
identifier: arg0
Args: [identifier: CONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ]
getPreExpArgument: [identifier: CONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ][eof: ]

HandleIdentifier:
MacroInfo 0x55e824457950 used
    #define <macro>[2813:CONCAT](arg0, arg1) arg0 ## arg1
Macro is not ok to expand
ResultArgToks: [identifier: CONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ]
Leave ExpandFunctionArguments: [identifier: CONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ]

LeaveMacro: 2

HandleIdentifier:
MacroInfo 0x55e824457950 used
    #define <macro>[2813:CONCAT](arg0, arg1) arg0 ## arg1
Macro is not ok to expand
```

</details>

第[16](#__codelineno-13-16)請開始展開 `IDENTITY`，同時預處理器看到 `Token 2`（也就是 `arg0`）是個巨集，因此先展開 `CONCAT(C, ONCAT(a, b))`。

展開 `arg0` 後得到 `CONCAT(a, b)` （第 [23-54](#__codelineno-13-23)工作。

`IDENTITY` 最終展開為 `IDENTITY_IMPL(CONCAT(a, b))`（第 [57](#__codelineno-13-57)行）

重新扫描，继续展开 `IDENTITY_IMPL`（第 [61-72](#__codelineno-13-61)(#__codelineno-13-85)（尚未翻譯）

重新掃描結果，發現宏 `CONCAT(a, b)` 的狀態是 `used`，停止展開並得到最終的結果。

通過以上三個簡單的例子，我們可以大致地理解預處理器展開巨集的過程，這裡不再對預處理器進行更深入的探討，有興趣可以對照我提供的修改文件來研究。

##宏編程實現

讓我們現在進入主題（前文段落的目的是為了更好理解宏展開規則），開始實現宏編程。

####基本符號

首先可以先定義巨集的特殊符號，做求值和拼接的時候會用到

``` cpp
#define PP_LPAREN() (
#define PP_RPAREN() )
#define PP_COMMA() ,
#define PP_EMPTY()
#定義 PP_HASHHASH # ## #      // 表示 ## 字符串，但只是作為字符串，不會當作 ## 操作符來處理
```

####求值

透過優先展開參數的規則，可以撰寫一個求值巨集：

``` cpp
#define PP_IDENTITY(arg0) arg0

PP_COMMA PP_LPAREN() PP_RPAREN()                // -> PP_COMMA ( )
PP_IDENTITY(PP_COMMA PP_LPAREN() PP_RPAREN())   // -> PP_COMMA() -> ,
```

如果只是寫 `PP_COMMA PP_LPAREN() PP_RPAREN()`，預處理器只會分別處理每個巨集，對展開的結果不會再合併處理。加上 `PP_IDENTITY` 之後，預處理器可以對展開得到的 `PP_COMMA()` 再進行求值，得到 `,`。


####拼接

在`##`連接時，不會展開兩邊的參數。為了讓參數在連接之前先進行求值，可以這樣寫：

``` cpp
#define PP_CONCAT(arg0, arg1) PP_CONCAT_IMPL(arg0, arg1)
#define PP_CONCAT_IMPL(arg0, arg1) arg0 ## arg1

PP_CONCAT(PP_IDENTITY(1), PP_IDENTITY(2))         // -> 12
PP_CONCAT_IMPL(PP_IDENTITY(1), PP_IDENTITY(2))    // -> PP_IDENTITY(1)PP_IDENTITY(2) -> Error
```

這裡 `PP_CONCAT` 用到的方法叫做延遲拼接，在展開為 `PP_CONCAT_IMPL` 的時候，`arg0` 和 `arg1` 都會先展開求值，之後再由 `PP_CONCAT_IMPL` 執行真正的拼接操作。

####邏輯運算

利用`PP_CONCAT`可以實現邏輯運算。首先定義`BOOL`值：


``` cpp
#define PP_BOOL(arg0) PP_CONCAT(PP_BOOL_, arg0)
#define PP_BOOL_0 0
#define PP_BOOL_1 1
#define PP_BOOL_2 1
#define PP_BOOL_3 1
// ...
#define PP_BOOL_256 1

PP_BOOL(3)              // -> PP_BOOL_3 -> 1
```

使用 `PP_CONCAT` 將 `PP_BOOL_` 和 `arg0` 先連接在一起，然後對連接結果進行求值。此處的 `arg0` 要求在求值後產生介於 `[0, 256]` 範圍內的數字，將其連接在 `PP_BOOL_` 後進行求值，便可獲得布爾值。並且可以進行與、或、非運算：

``` cpp
#define PP_NOT(arg0) PP_CONCAT(PP_NOT_, PP_BOOL(arg0))
#define PP_NOT_0 1
#define PP_NOT_1 0

#define PP_AND(arg0, arg1) PP_CONCAT(PP_AND_, PP_CONCAT(PP_BOOL(arg0), PP_BOOL(arg1)))
#define PP_AND_00 0
#define PP_AND_01 0
#define PP_AND_10 0
#define PP_AND_11 1

#define PP_OR(arg0, arg1) PP_CONCAT(PP_OR_, PP_CONCAT(PP_BOOL(arg0), PP_BOOL(arg1)))
#define PP_OR_00 0
#define PP_OR_01 1
#define PP_OR_10 1
#define PP_OR_11 1

PP_NOT(PP_BOOL(2))      // -> PP_CONCAT(PP_NOT_, 1) -> PP_NOT_1 -> 0
PP_AND(2, 3)            // -> PP_CONCAT(PP_AND_, 11) -> PP_AND_11 -> 1
PP_AND(2, 0)            // -> PP_CONCAT(PP_AND_, 10) -> PP_AND_10 -> 0
PP_OR(2, 0)             // -> PP_CONCAT(PP_OR_, 10) -> PP_OR_10, -> 1
```

先用 `PP_BOOL` 對參數求值，之後再根據 `0 1` 的組合來拼接邏輯運算的結果。如果不用 `PP_BOOL` 來求值，那麼參數就只能支持 `0 1` 兩種數值，適用性大幅降低。同理也可以撰寫出互斥或、或非等操作，有興趣的話可以自行嘗試。

####條件選擇

利用 `PP_BOOL` 和 `PP_CONCAT`，還能夠撰寫條件選擇語句：

``` cpp
#define PP_IF(if, then, else) PP_CONCAT(PP_IF_, PP_BOOL(if))(then, else)
#define PP_IF_1(then, else) then
#define PP_IF_0(then, else) else

PP_IF(1, 2, 3)      // -> PP_IF_1(2, 3) -> 2
PP_IF(0, 2, 3)      // -> PP_IF_0(2, 3) -> 3
```

若`if`求值為`1`，則使用`PP_CONCAT`來拼接成`PP_IF_1`，最後展開為`then`的值；同理若`if`求值為`0`，則得到`PP_IF_0`。

####遞增遞減

整数遞增遞減：

``` cpp
#define PP_INC(arg0) PP_CONCAT(PP_INC_, arg0)
#define PP_INC_0 1
#define PP_INC_1 2
#define PP_INC_2 3
#define PP_INC_3 4
// ...
#define PP_INC_255 256
#define PP_INC_256 256

#define PP_DEC(arg0) PP_CONCAT(PP_DEC_, arg0)
#define PP_DEC_0 0
#define PP_DEC_1 0
#define PP_DEC_2 1
#define PP_DEC_3 2
// ...
#define PP_DEC_255 254
#define PP_DEC_256 255

PP_INC(2)                   // -> PP_INC_2 -> 3
PP_DEC(3)                   // -> PP_DEC_3 -> 2
```

與 `PP_BOOL` 相似，整數的遞增遞減也存在著範圍限制，這裡將範圍設定為 `[0, 256]`。當遞增至 `256` 後，為確保安全，`PP_INC_256` 會返回自身的 `256` 作為邊界，同樣地，`PP_DEC_0` 也會返回 `0`。

####不變長參數

宏可以接受變長參數，格式是：

```cpp
#define LOG(format, ...) printf("log: " format, __VA_ARGS__)

LOG("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG("Hello World")              // -> printf("log: " "Hello World", ); 多了個逗號，編譯報錯
```

由於變長參數有可能為空，空的情況下會導致編譯失敗，因此 C++ 20 引入了 `__VA_OPT__`，如果變長參數是空，則返回空，否則返回原參數：

```cpp
#define LOG2(format, ...) printf("log: " format __VA_OPT__(,) __VA_ARGS__)

LOG2("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG2("Hello World") //-> printf("log: " "Hello World"); No comma, compiles without errors
```

不幸的是，只有 C++ 20 以上的標準才支援這個巨集，在下文中我們將會提供 `__VA_OPT__` 的實現方法。

####惰性求值

考慮這種情況：

``` cpp
PP_IF(1, PP_COMMA(), PP_LPAREN())     // -> PP_IF_1(,,)) -> 报错 unterminated argument list invoking macro "PP_IF_1"
```

我們知道，宏展開的時候會對先參數進行求值。`PP_COMMA()` 和 `PP_LPAREN()` 求值之後再傳給 `PP_IF_1`，得到 `PP_IF_1(,,))`，導致預處理出錯。此時，可以採用一種叫做惰性求值方法：

``` cpp
PP_IF(1, PP_COMMA, PP_LPAREN)()       // -> PP_IF_1(PP_COMMA, PP_LPAREN)() -> PP_COMMA() -> ,
```

將這種寫法修改為僅傳遞宏的名稱，讓 `PP_IF` 從所需的宏名稱中選擇後，再與括號 `()` 組合在一起形成完整的宏，最後再展開。惰性求值在宏編程中也很常見。

####以括號開始

判斷變長參數是否以括號開始：

``` cpp
#define PP_IS_BEGIN_PARENS(...) \
    PP_IS_BEGIN_PARENS_PROCESS( \
        PP_IS_BEGIN_PARENS_CONCAT( \
            PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__ \
        ) \
    )

#define PP_IS_BEGIN_PARENS_PROCESS(...) PP_IS_BEGIN_PARENS_PROCESS_0(__VA_ARGS__)
#define PP_IS_BEGIN_PARENS_PROCESS_0(arg0, ...) arg0

#define PP_IS_BEGIN_PARENS_CONCAT(arg0, ...) PP_IS_BEGIN_PARENS_CONCAT_IMPL(arg0, __VA_ARGS__)
#define PP_IS_BEGIN_PARENS_CONCAT_IMPL(arg0, ...) arg0 ## __VA_ARGS__

#define PP_IS_BEGIN_PARENS_PRE_1 1,
#define PP_IS_BEGIN_PARENS_PRE_PP_IS_BEGIN_PARENS_EAT 0,
#define PP_IS_BEGIN_PARENS_EAT(...) 1

PP_IS_BEGIN_PARENS(())              // -> 1
PP_IS_BEGIN_PARENS((()))            // -> 1
PP_IS_BEGIN_PARENS(a, b, c)         // -> 0
PP_IS_BEGIN_PARENS(a, ())           // -> 0
PP_IS_BEGIN_PARENS(a())             // -> 0
PP_IS_BEGIN_PARENS(()aa(bb()cc))    // -> 1
PP_IS_BEGIN_PARENS(aa(bb()cc))      // -> 0
```

"PP_IS_BEGIN_PARENS" 可用於判斷傳入的參數是否以括號開始，在需要處理括號參數的時候會需要用到（例如後面提到的 "__VA_OPT__" 實現）。看起來有點複雜，核心思想就是構建一個巨集，若變長參數以括號開始，則可以跟括號連在一起求值得到一種結果，否則就另外求值得到另一種結果。讓我們來慢慢看：

`PP_IS_BEGIN_PARENS_PROCESS` 和 `PP_IS_BEGIN_PARENS_PROCESS_0` 組成的巨集功能是先對傳入的不定參數求值，然後取第 0 個參數。

`PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__)`指的是先對`PP_IS_BEGIN_PARENS_EAT __VA_ARGS__`進行求值，再將求值結果與`PP_IS_BEGIN_PARENS_PRE_`拼接在一起。

`PP_IS_BEGIN_PARENS_EAT(...)` 宏將吞噬所有參數，返回1。在上述 `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` 中，若`__VA_ARGS__` 以括號開始，則會與 `PP_IS_BEGIN_PARENS_EAT(...)` 宏匹配，並返回1；反之，若未以括號開始，則無法匹配，`PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` 將保持不變。

如果 `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` 計算結果為 `1`，則 `PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, 1) -> PP_IS_BEGIN_PARENS_PRE_1 -> 1`，請注意 `1` 後面有一個逗號，將 `1, ` 傳遞給 `PP_IS_BEGIN_PARENS_PROCESS_0`，提取第 0 個參數，最終得到 `1`，表示參數以括號開始。

若 `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` 求值得到不是 `1`，而是保持不變，則 `PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__) -> PP_IS_BEGIN_PARENS_PRE_PP_IS_BEGIN_PARENS_EAT __VA_ARGS__ -> 0, __VA_ARGS__`，傳給 `PP_IS_BEGIN_PARENS_PROCESS_0` 得到的是 `0`，表示參數不是以括號開始。

####可變長的參數空間

判斷變長參數是否為空也是常見的巨集之一，在實現 `__VA_OPT__` 時需要使用，我們可以借助 `PP_IS_BEGIN_PARENS`，先撰寫出不完整的版本：

``` cpp
#define PP_IS_EMPTY_PROCESS(...) \
    PP_IS_BEGIN_PARENS(PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ())
#define PP_IS_EMPTY_PROCESS_EAT(...) ()

PP_IS_EMPTY_PROCESS()       // -> 1
PP_IS_EMPTY_PROCESS(1)      // -> 0
PP_IS_EMPTY_PROCESS(1, 2)   // -> 0
PP_IS_EMPTY_PROCESS(())     // -> 1
```

`PP_IS_EMPTY_PROCESS` 的功能是判斷 `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__()`, 是否從括號開始。

若 `__VA_ARGS__` 為空，`PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ () -> PP_IS_EMPTY_PROCESS_EAT() -> ()`，將得到一對括號 `()`，再經由傳遞給 `PP_IS_BEGIN_PARENS` 並返回 `1`，代表參數為空。

否則， `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS __（）` 會無變地傳遞給 `PP_IS_BEGIN_PARENS`，並返回 0，表示非空。

請注意第 4 個例子 `PP_IS_EMPTY_PROCESS(()) -> 1`，`PP_IS_EMPTY_PROCESS` 不能正確處理以括號開始的變長參數，因為這時變長參數帶來的括號會配對到 `PP_IS_EMPTY_PROCESS_EAT` 導致求值結果為 `()`。為了解決這個問題，我們需要區別對待參數是否以括號開始的情況：

``` cpp
#define PP_IS_EMPTY(...) \
    PP_IS_EMPTY_IF(PP_IS_BEGIN_PARENS(__VA_ARGS__)) \
        (PP_IS_EMPTY_ZERO, PP_IS_EMPTY_PROCESS)(__VA_ARGS__)

#define PP_IS_EMPTY_IF(if) PP_CONCAT(PP_IS_EMPTY_IF_, if)
#define PP_IS_EMPTY_IF_1(then, else) then
#define PP_IS_EMPTY_IF_0(then, else) else

#define PP_IS_EMPTY_ZERO(...) 0

PP_IS_EMPTY()       // -> 1
PP_IS_EMPTY(1)      // -> 0
PP_IS_EMPTY(1, 2)   // -> 0
PP_IS_EMPTY(())     // -> 0
```

基於 `if` 條件，返回第 0 或第 1 參數的 `PP_IS_EMPTY_IF` 函數。

如果傳入的可變參數以括號開始，`PP_IS_EMPTY_IF` 返回 `PP_IS_EMPTY_ZERO`，最後返回 `0`，表示可變參數非空。

反之 `PP_IS_EMPTY_IF` 返回 `PP_IS_EMPTY_PROCESS`，最後由 `PP_IS_EMPTY_PROCESS` 來判断變長參數是否非空。

####下標訪問

獲取在可變參數中指定位置的元素：

``` cpp
#define PP_ARGS_ELEM(I, ...) PP_CONCAT(PP_ARGS_ELEM_, I)(__VA_ARGS__)
#define PP_ARGS_ELEM_0(a0, ...) a0
#define PP_ARGS_ELEM_1(a0, a1, ...) a1
#define PP_ARGS_ELEM_2(a0, a1, a2, ...) a2
#define PP_ARGS_ELEM_3(a0, a1, a2, a3, ...) a3
// ...
#define PP_ARGS_ELEM_7(a0, a1, a2, a3, a4, a5, a6, a7, ...) a7
#define PP_ARGS_ELEM_8(a0, a1, a2, a3, a4, a5, a6, a7, a8, ...) a8

PP_ARGS_ELEM(0, "Hello", "World")   // -> PP_ARGS_ELEM_0("Hello", "World") -> "Hello"
PP_ARGS_ELEM(1, "Hello", "World")   // -> PP_ARGS_ELEM_1("Hello", "World") -> "World"
```

`PP_ARGS_ELEM` 的第一個參數是元素下標 `I`，後面是變長參數。利用 `PP_CONCAT` 拼接 `PP_ARGS_ELEM_` 和 `I`，即可以得到返回相應位置元素的巨集 `PP_ARGS_ELEM_0..8`，再把變長參數傳給該巨集，展開返回下標對應位置的元素。

#### PP_IS_EMPTY2

使用`PP_ARGS_ELEM`也能實現另一版本的`PP_IS_EMPTY`：

``` cpp
#define PP_IS_EMPTY2(...) \
    PP_AND( \
        PP_AND( \
            PP_NOT(PP_HAS_COMMA(__VA_ARGS__)), \
            PP_NOT(PP_HAS_COMMA(__VA_ARGS__())) \
        ), \
        PP_AND( \
            PP_NOT(PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__)), \
            PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ()) \
        ) \
    )

#define PP_HAS_COMMA(...) PP_ARGS_ELEM(8, __VA_ARGS__, 1, 1, 1, 1, 1, 1, 1, 0)
#define PP_COMMA_ARGS(...) ,

PP_IS_EMPTY2()              // -> 1
PP_IS_EMPTY2(a)             // -> 0
PP_IS_EMPTY2(a, b)          // -> 0
PP_IS_EMPTY2(())            // -> 0
PP_IS_EMPTY2(PP_COMMA)      // -> 0
```

利用 `PP_ARGS_ELEM` 實現判斷參數是否包含逗號 `PP_HAS_COMMA`。`PP_COMMA_ARGS` 會吞掉傳入的任意參數，並返回一個逗號。

判斷變長參數是否為空的基礎邏輯是 `PP_COMMA_ARGS __VA_ARGS__ ()` 返回一個逗號，也就是 `__VA_ARGS__` 為空，`PP_COMMA_ARGS` 和 `()` 拼接在一起求值，具體的寫法就是 `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ())`。

然而，有時候也會有特殊情況：

`__VA_ARGS__` itself may come with commas;
`__VA_ARGS__() ` 拼接在一起時會導致逗號表達式被求值；
`PP_COMMA_ARGS __VA_ARGS__` 在拼接在一起时，会因为触发求值而产生逗号；

針對上述提到的三種例外情況，需要進行排除，因此最後的寫法等同於對以下4個條件執行AND邏輯：

* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__))` &&
* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__()))` &&
* `PP_NOT(PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__))` &&
* `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ())`

#### `__VA_OPT__`

使用 `PP_IS_EMPTY` 終於可以實現類似 `__VA_OPT__` 的巨集：

``` cpp
#define PP_REMOVE_PARENS(tuple) PP_REMOVE_PARENS_IMPL tuple
#define PP_REMOVE_PARENS_IMPL(...) __VA_ARGS__

#define PP_ARGS_OPT(data_tuple, empty_tuple, ...) \
    PP_ARGS_OPT_IMPL(PP_IF(PP_IS_EMPTY(__VA_ARGS__), empty_tuple, data_tuple))
#define PP_ARGS_OPT_IMPL(tuple) PP_REMOVE_PARENS(tuple)

PP_ARGS_OPT((data), (empty))        // -> empty
PP_ARGS_OPT((data), (empty), 1)     // -> data
PP_ARGS_OPT((,), (), 1)             // -> ,
```

`PP_ARGS_OPT` 接受兩個固定參數和變長參數，變長參數非空時返回 `data`，否則返回 `empty`。為了讓 `data` 和 `empty` 支持逗號，要求兩者都要用括號包住實際的參數，最後用 `PP_REMOVE_PARENS` 來移除外層的括號。

擁有了 `PP_ARGS_OPT`，可以實現 `LOG3` 來模擬 `LOG2` 實現的功能：

``` cpp
#define LOG3(format, ...) \
    printf("log: " format PP_ARGS_OPT((,), (), __VA_ARGS__) __VA_ARGS__)

LOG3("Hello");                  // -> printf("log: " "Hello" );
LOG3("Hello %s", "World");      // -> printf("log: " "Hello %s" , "World");
```

`data_tuple`是`(,)`，如果變長參數非空，則會返回`data_tuple`裡面的所有元素，在這裡就是逗號`,`。

####請求參數個數

獲取可變參數的個數：

``` cpp
#define PP_ARGS_SIZE_IMCOMPLETE(...) \
    PP_ARGS_ELEM(8, __VA_ARGS__, 8, 7, 6, 5, 4, 3, 2, 1, 0)

PP_ARGS_SIZE_IMCOMPLETE(a)             // -> 1
PP_ARGS_SIZE_IMCOMPLETE(a, b)          // -> 2
PP_ARGS_SIZE_IMCOMPLETE(PP_COMMA())    // -> 2
PP_ARGS_SIZE_IMCOMPLETE()              // -> 1
```

計算可變參數的個數是通過參數的位置來獲取的。`__VA_ARGS__` 會導致後續的參數全體往右移動，用宏 `PP_ARGS_ELEM` 來獲取第 8 個位置的參數，如果 `__VA_ARGS__` 只有一個參數，則第 8 個參數等於 `1`；同理如果 `__VA_ARGS__` 有兩個參數，則第 8 個參數就變為 `2`，剛好等於可變參數的個數。

這裡提供的範例僅支持長度最多為 8 的變長參數，這是基於 `PP_ARGS_ELEM` 所能支持的最大長度。

但這個巨集還不完整，在變長參數為空的情況下，這個巨集會錯誤返回 `1`。如果需要處理空的變長參數，則需要使用我們前面提到的 `PP_ARGS_OPT` 巨集：

``` cpp
#define PP_COMMA_IF_ARGS(...) PP_ARGS_OPT((,), (), __VA_ARGS__)
#define PP_ARGS_SIZE(...) PP_ARGS_ELEM(8, __VA_ARGS__ PP_COMMA_IF_ARGS(__VA_ARGS__) 8, 7, 6, 5, 4, 3, 2, 1, 0, 0, 0)

PP_ARGS_SIZE(a)             // -> 1
PP_ARGS_SIZE(a, b)          // -> 2
PP_ARGS_SIZE(PP_COMMA())    // -> 2
PP_ARGS_SIZE()              // -> 0
PP_ARGS_SIZE(,,,)           // -> 4
```

關鍵在於逗號 `,`，當`__VA_ARGS__`為空時，省略逗號即可正確返回`0`。

####遍歷訪問

與 C++ 中的 `for_each` 類似，我們可以實現巨集的 `PP_FOR_EACH`：

``` cpp
#define PP_FOR_EACH(macro, contex, ...) \
    PP_CONCAT(PP_FOR_EACH_, PP_ARGS_SIZE(__VA_ARGS__))(0, macro, contex, __VA_ARGS__)

#define PP_FOR_EACH_0(index, macro, contex, ...)
#define PP_FOR_EACH_1(index, macro, contex, arg, ...) macro(index, contex, arg)

#define PP_FOR_EACH_2(index, macro, contex, arg, ...) \
    macro(index, contex, arg) \
    PP_FOR_EACH_1(PP_INC(index), macro, contex, __VA_ARGS__)

#define PP_FOR_EACH_3(index, macro, contex, arg, ...) \
    macro(index, contex, arg) \
    PP_FOR_EACH_2(PP_INC(index), macro, contex, __VA_ARGS__)
// ...
#define PP_FOR_EACH_8(index, macro, contex, arg, ...) \
    macro(index, contex, arg) \
    PP_FOR_EACH_7(PP_INC(index), macro, contex, __VA_ARGS__)

#define DECLARE_EACH(index, contex, arg)    PP_IF(index, PP_COMMA, PP_EMPTY)() contex arg

PP_FOR_EACH(DECLARE_EACH, int, x, y, z);    // -> int x, y, z;
PP_FOR_EACH(DECLARE_EACH, bool, a, b);      // -> bool a, b;
```

`PP_FOR_EACH` 接收兩個固定參數：`macro` 可以理解為遍歷時呼叫的巨集，`contex` 可以作為固定值參數傳遞給`macro`。`PP_FOR_EACH` 先通過`PP_ARGS_SIZE` 獲取變長參數的長度 `N`，再用`PP_CONCAT` 拼接得到`PP_FOR_EACH_N`，之後`PP_FOR_EACH_N` 會迭代呼叫`PP_FOR_EACH_N-1` 來實現跟變長參數個數相同的遍歷次數。

在這個例子中，我們定義了 `DECLARE_EACH` 作為 `macro` 函數的參數，`DECLARE_EACH` 的作用是返回 `contex arg`，如果 `contex` 是類型名稱，`arg` 是變數名稱，那麼 `DECLARE_EACH` 就可以用來宣告變數。

####條件迴圈

有了`FOR_EACH`之後，我們還可以用類似的寫法寫出`PP_WHILE`：

``` cpp
#define PP_WHILE PP_WHILE_1

#define PP_WHILE_1(pred, op, val) PP_WHILE_1_IMPL(PP_BOOL(pred(val)), pred, op, val)
#define PP_WHILE_1_IMPL(cond, pred, op, val) \
    PP_IF(cond, PP_WHILE_2, val PP_EMPTY_EAT)(pred, op, PP_IF(cond, op, PP_EMPTY_EAT)(val))

#define PP_WHILE_2(pred, op, val) PP_WHILE_2_IMPL(PP_BOOL(pred(val)), pred, op, val)
#define PP_WHILE_2_IMPL(cond, pred, op, val) \
    PP_IF(cond, PP_WHILE_3, val PP_EMPTY_EAT)(pred, op, PP_IF(cond, op, PP_EMPTY_EAT)(val))

#define PP_WHILE_3(pred, op, val) PP_WHILE_3_IMPL(PP_BOOL(pred(val)), pred, op, val)
#define PP_WHILE_3_IMPL(cond, pred, op, val) \
    PP_IF(cond, PP_WHILE_4, val PP_EMPTY_EAT)(pred, op, PP_IF(cond, op, PP_EMPTY_EAT)(val))

#define PP_WHILE_4(pred, op, val) PP_WHILE_4_IMPL(PP_BOOL(pred(val)), pred, op, val)
#define PP_WHILE_4_IMPL(cond, pred, op, val) \
    PP_IF(cond, PP_WHILE_5, val PP_EMPTY_EAT)(pred, op, PP_IF(cond, op, PP_EMPTY_EAT)(val))
// ...

#define PP_WHILE_8(pred, op, val) PP_WHILE_8_IMPL(PP_BOOL(pred(val)), pred, op, val)
#define PP_WHILE_8_IMPL(cond, pred, op, val) \
    PP_IF(cond, PP_WHILE_8, val PP_EMPTY_EAT)(pred, op, PP_IF(cond, op, PP_EMPTY_EAT)(val))

#define PP_EMPTY_EAT(...)

#define SUM_OP(xy_tuple) SUM_OP_OP_IMPL xy_tuple
#define SUM_OP_OP_IMPL(x, y) (PP_DEC(x), y + x)

#define SUM_PRED(xy_tuple) SUM_PRED_IMPL xy_tuple
#define SUM_PRED_IMPL(x, y) x

#define SUM(max_num, origin_num) \
    PP_IDENTITY(SUM_IMPL PP_WHILE(SUM_PRED, SUM_OP, (max_num, origin_num)))
#define SUM_IMPL(ignore, ret) ret

PP_WHILE(SUM_PRED, SUM_OP, (2, a))      // -> (0, a + 2 + 1)
SUM(2, a)                               // -> a + 2 + 1
```

`PP_WHILE` 接受三個參數：`pred` 條件判斷函數，`op` 操作函數，`val` 初始值；循環的過程中不斷用 `pred(val)` 來做循環終止判斷，把 `op(val)` 得到的值傳給後續的巨集，可以理解為執行以下程式碼：

``` cpp
while (pred(val)) {
    val = op(val);
}
```

首先使用 `pred(val)` 運算出條件判斷結果，然後將這個判斷結果 `cond` 和其他參數一起傳遞給 `PP_WHILE_N_IMPL`。
`PP_WHILE_N_IMPL` 可以看成是兩部分：後半部分 `(pred, op, PP_IF(cond, op, PP_EMPTY_EAT)(val))` 作為前半部分的參數，`PP_IF(cond, op, PP_EMPTY_EAT)(val)` 則是若 `cond` 為真，則求值 `op(val)`；否則求值 `PP_EMPTY_EAT(val)` 得到空。前半部分 `PP_IF(cond, PP_WHILE_N+1, val PP_EMPTY_EAT)` 若 `cond` 為真，則回傳 `PP_WHILE_N+1`，與後半部分的參數繼續執行循環；反之回傳 `val PP_EMPTY_EAT`，此時 `val` 就是最終的計算結果，而 `PP_EMPTY_EAT` 會吞掉後半部分的結果。

`SUM` 實現 `N + N-1 + ... + 1`。初始值 `(max_num, origin_num)`；`SUM_PRED` 取值的第一個元素 `x`，判斷是否大於 0；`SUM_OP` 對 `x` 執行遞減操作 `x = x - 1`，對 `y` 執行 `+ x` 操作 `y = y + x`。直接用 `SUM_PRED` 和 `SUM_OP` 傳給 `PP_WHILE`，返回的結果是一個元組，我們真正想要的結果是元組的第 2 個元素，於是再用 `SUM` 取第 2 個元素的值。

####递归重入

迄今為止，我們的遍歷訪問和條件循環都運作得很好，結果符合預期。還記得我們在談宏展開規則時提到的禁止遞迴重入嗎，當我們想要執行雙重循環時就不幸遇到了禁止遞迴重入：

``` cpp
#define SUM_OP2(xy_tuple) SUM_OP_OP_IMPL2 xy_tuple
#define SUM_OP_OP_IMPL2(x, y) (PP_DEC(x), y + SUM(x, 0))

#define SUM2(max_num, origin_num) \
    PP_IDENTITY(SUM_IMPL PP_WHILE(SUM_PRED, SUM_OP2, (max_num, origin_num)))

SUM2(1, a)      // -> a + SUM_IMPL PP_WHILE_1(SUM_PRED, SUM_OP, (1, a))
```

將`SUM2`中的參數`op`改為`SUM_OP2`，`SUM_OP2`將會呼叫`SUM`，而這個`SUM`展開後還是`PP_WHILE_1`，相當於`PP_WHILE_1`遞迴調用了自身，預處理器停止展開。

為了解決這問題，我們可以使用自動遞迴的方法（Automatic Recursion）：

``` cpp
#define PP_AUTO_WHILE PP_CONCAT(PP_WHILE_, PP_AUTO_REC(PP_WHILE_PRED))

#define PP_AUTO_REC(check) PP_IF(check(2), PP_AUTO_REC_12, PP_AUTO_REC_34)(check)
#define PP_AUTO_REC_12(check) PP_IF(check(1), 1, 2)
#define PP_AUTO_REC_34(check) PP_IF(check(3), 3, 4)

#define PP_WHILE_PRED(n) \
    PP_CONCAT(PP_WHILE_CHECK_, PP_WHILE_ ## n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE))
#define PP_WHILE_FALSE(...) 0

#define PP_WHILE_CHECK_PP_WHILE_FALSE 1

#define PP_WHILE_CHECK_PP_WHILE_1(...) 0
#define PP_WHILE_CHECK_PP_WHILE_2(...) 0
#define PP_WHILE_CHECK_PP_WHILE_3(...) 0
#define PP_WHILE_CHECK_PP_WHILE_4(...) 0
// ...
#define PP_WHILE_CHECK_PP_WHILE_8(...) 0

PP_AUTO_WHILE       // -> PP_WHILE_1

#define SUM3(max_num, origin_num) \
    PP_IDENTITY(SUM_IMPL PP_AUTO_WHILE(SUM_PRED, SUM_OP, (max_num, origin_num)))

#define SUM_OP4(xy_tuple) SUM_OP_OP_IMPL4 xy_tuple
#define SUM_OP_OP_IMPL4(x, y) (PP_DEC(x), y + SUM3(x, 0))

#define SUM4(max_num, origin_num) \
    PP_IDENTITY(SUM_IMPL PP_AUTO_WHILE(SUM_PRED, SUM_OP4, (max_num, origin_num)))

SUM4(2, a)          // -> a + 0 + 2 + 1 + 0 + 1
```

`PP_AUTO_WHILE` 就是 `PP_WHILE` 的自動推導遞歸版本，核心的巨集是 `PP_AUTO_REC(PP_WHILE_PRED)`，這個巨集可以找出當前可用的 `PP_WHILE_N` 版本的數字 `N`。

推導的原理很簡單，就是搜索所有版本，找出能夠正確展開的版本，返回該版本的數字，為了提升搜索的速度，一般的做法是使用二分查找，這就是 `PP_AUTO_REC` 在做的事情。`PP_AUTO_REC` 接受一個參數 `check`，`check` 負責檢查版本可用性，這裡給出的是支持搜索版本範圍 `[1, 4]`。`PP_AUTO_REC` 會首先檢查 `check(2)`，如果 `check(2)` 為真，則調用 `PP_AUTO_REC_12` 搜索範圍 `[1, 2]`，否則用 `PP_AUTO_REC_34` 搜索 `[3, 4]`。`PP_AUTO_REC_12` 檢查 `check(1)` 如果為真，說明版本 `1` 可用，否則用版本 `2`，`PP_AUTO_REC_34` 同理。

檢查一下在哪裡要怎麼寫才能知道版本是否可用呢？在這裡，`PP_WHILE_PRED` 會展開成兩部分的拼接，我們來看後部分 `PP_WHILE_ ## n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`：如果 `PP_WHILE_ ## n` 可用，由於 `PP_WHILE_FALSE` 固定返回 `0`，這部分會展開得到 `val` 參數的值，也就是 `PP_WHILE_FALSE`；否則這部分宏會保持不變，依然是 `PP_WHILE_n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`。

將後半部分的結果與前半部分的 `PP_WHILE_CHECK_` 組合在一起，得到兩種結果：`PP_WHILE_CHECK_PP_WHILE_FALSE` 或 `PP_WHILE_CHECK_PP_WHILE_n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`。因此，我們讓 `PP_WHILE_CHECK_PP_WHILE_FALSE` 返回 `1` 表示可用，而讓 `PP_WHILE_CHECK_PP_WHILE_n` 返回 `0` 表示不可用。至此，我們成功實現了自動推導遞迴的功能。

####數學比較

不相等：Unequal:

``` cpp
#define PP_NOT_EQUAL(x, y) PP_NOT_EQUAL_IMPL(x, y)
#define PP_NOT_EQUAL_IMPL(x, y) \
    PP_CONCAT(PP_NOT_EQUAL_CHECK_, PP_NOT_EQUAL_ ## x(0, PP_NOT_EQUAL_ ## y))

#define PP_NOT_EQUAL_CHECK_PP_EQUAL_NIL 1
#define PP_NOT_EQUAL_CHECK_PP_NOT_EQUAL_0(...) 0
#define PP_NOT_EQUAL_CHECK_PP_NOT_EQUAL_1(...) 0
#define PP_NOT_EQUAL_CHECK_PP_NOT_EQUAL_2(...) 0
#define PP_NOT_EQUAL_CHECK_PP_NOT_EQUAL_3(...) 0
#define PP_NOT_EQUAL_CHECK_PP_NOT_EQUAL_4(...) 0
// ...
#define PP_NOT_EQUAL_CHECK_PP_NOT_EQUAL_8(...) 0

#define PP_NOT_EQUAL_0(cond, y) PP_IF(cond, PP_EQUAL_NIL, y(1, PP_EQUAL_NIL))
#define PP_NOT_EQUAL_1(cond, y) PP_IF(cond, PP_EQUAL_NIL, y(1, PP_EQUAL_NIL))
#define PP_NOT_EQUAL_2(cond, y) PP_IF(cond, PP_EQUAL_NIL, y(1, PP_EQUAL_NIL))
#define PP_NOT_EQUAL_3(cond, y) PP_IF(cond, PP_EQUAL_NIL, y(1, PP_EQUAL_NIL))
#define PP_NOT_EQUAL_4(cond, y) PP_IF(cond, PP_EQUAL_NIL, y(1, PP_EQUAL_NIL))
// ...
#define PP_NOT_EQUAL_8(cond, y) PP_IF(cond, PP_EQUAL_NIL, y(1, PP_EQUAL_NIL))

PP_NOT_EQUAL(1, 1)          // -> 0
PP_NOT_EQUAL(3, 1)          // -> 1
```

判斷數值是否相等時，利用了禁止遞迴重入的特性，將 `x` 和 `y` 遞迴拼接成 `PP_NOT_EQUAL_x PP_NOT_EQUAL_y` 宏。若 `x == y`，則不會展開 `PP_NOT_EQUAL_y` 宏，最終會拼接成 `PP_NOT_EQUAL_CHECK_PP_NOT_EQUAL_y` 並返回 `0`；反之，兩者皆成功展開後將得到 `PP_EQUAL_NIL`，進而拼接成 `PP_NOT_EQUAL_CHECK_PP_EQUAL_NIL` 並返回 `1`。

Equality:

``` cpp
#define PP_EQUAL(x, y) PP_NOT(PP_NOT_EQUAL(x, y))

PP_EQUAL(1, 1)              // -> 1
PP_EQUAL(1, 3)              // -> 0

```

小於等於：

``` cpp
#define PP_LESS_EQUAL(x, y) PP_NOT(PP_SUB(x, y))

PP_LESS_EQUAL(2, 1)         // -> 0
PP_LESS_EQUAL(1, 1)         // -> 1
PP_LESS_EQUAL(1, 2)         // -> 1
```

小於：

``` cpp
#define PP_LESS(x, y) PP_AND(PP_LESS_EQUAL(x, y), PP_NOT_EQUAL(x, y))

PP_LESS(2, 1)               // -> 0
PP_LESS(1, 2)               // -> 1
PP_LESS(2, 2)               // -> 0
```

此外，還有大於、大於等於等算術比較，這裡不再贅述。

####算術運算

利用 `PP_AUTO_WHILE` 我們可以實現基礎的算術運算了，而且支持嵌套運算。

加法：

``` cpp
#define PP_ADD(x, y) \
    PP_IDENTITY(PP_ADD_IMPL PP_AUTO_WHILE(PP_ADD_PRED, PP_ADD_OP, (x, y)))
#define PP_ADD_IMPL(x, y) x

#define PP_ADD_PRED(xy_tuple) PP_ADD_PRED_IMPL xy_tuple
#define PP_ADD_PRED_IMPL(x, y) y

#define PP_ADD_OP(xy_tuple) PP_ADD_OP_IMPL xy_tuple
#define PP_ADD_OP_IMPL(x, y) (PP_INC(x), PP_DEC(y))

PP_ADD(1, 2)                  // -> 3
PP_ADD(1, PP_ADD(1, 2))       // -> 4
```

減法：

``` cpp
#define PP_SUB(x, y) \
    PP_IDENTITY(PP_SUB_IMPL PP_AUTO_WHILE(PP_SUB_PRED, PP_SUB_OP, (x, y)))
#define PP_SUB_IMPL(x, y) x

#define PP_SUB_PRED(xy_tuple) PP_SUB_PRED_IMPL xy_tuple
#define PP_SUB_PRED_IMPL(x, y) y

#define PP_SUB_OP(xy_tuple) PP_SUB_OP_IMPL xy_tuple
#define PP_SUB_OP_IMPL(x, y) (PP_DEC(x), PP_DEC(y))

PP_SUB(2, 1)                // -> 1
PP_SUB(3, PP_ADD(2, 1))     // -> 0
```

乘法：

``` cpp
#define PP_MUL(x, y) \
    IDENTITY(PP_MUL_IMPL PP_AUTO_WHILE(PP_MUL_PRED, PP_MUL_OP, (0, x, y)))
#define PP_MUL_IMPL(ret, x, y) ret

#define PP_MUL_PRED(rxy_tuple) PP_MUL_PRED_IMPL rxy_tuple
#define PP_MUL_PRED_IMPL(ret, x, y) y

#define PP_MUL_OP(rxy_tuple) PP_MUL_OP_IMPL rxy_tuple
#define PP_MUL_OP_IMPL(ret, x, y) (PP_ADD(ret, x), x, PP_DEC(y))

PP_MUL(1, 1)                // -> 1
PP_MUL(2, PP_ADD(0, 1))     // -> 2
```

乘法實現這裡增加了一個參數 `ret`，初始值為 `0`，每次迭代會執行 `ret = ret + x`。

除法：

``` cpp
#define PP_DIV(x, y) \
    IDENTITY(PP_DIV_IMPL PP_AUTO_WHILE(PP_DIV_PRED, PP_DIV_OP, (0, x, y)))
#define PP_DIV_IMPL(ret, x, y) ret

#define PP_DIV_PRED(rxy_tuple) PP_DIV_PRED_IMPL rxy_tuple
#define PP_DIV_PRED_IMPL(ret, x, y) PP_LESS_EQUAL(y, x)

#define PP_DIV_OP(rxy_tuple) PP_DIV_OP_IMPL rxy_tuple
#define PP_DIV_OP_IMPL(ret, x, y) (PP_INC(ret), PP_SUB(x, y), y)

PP_DIV(1, 2)                // -> 0
PP_DIV(2, 1)                // -> 2
PP_DIV(2, PP_ADD(1, 1))     // -> 1
```

除法利用了 `PP_LESS_EQUAL`，只有 `y <= x` 的情况下才繼續循環。

####資料結構

`tuple` 的特質使其成為一種資料結構。舉例來說，`PP_REMOVE_PARENS` 可以移除 `tuple` 的外圍括號，並傳回其中的元素。讓我們以 `tuple` 為例，探討相關的實作細節，對於其他資料結構如 `list`、`array` 等，若你感興趣，不妨查閱 `Boost` 的實作方式。

"tuple" 被定義為由括號包裹並以逗號分隔的元素集合：`(a, b, c)`。

``` cpp
#define PP_TUPLE_REMOVE_PARENS(tuple) PP_REMOVE_PARENS(tuple)

獲取指定索引的元素
#define PP_TUPLE_ELEM(i, tuple) PP_ARGS_ELEM(i, PP_TUPLE_REMOVE_PARENS(tuple))

吞掉整個tuple返回空
#define PP_TUPLE_EAT() PP_EMPTY_EAT

獲取大小
#define PP_TUPLE_SIZE(tuple) PP_ARGS_SIZE(PP_TUPLE_REMOVE_PARENS(tuple))

// Add element
#define PP_TUPLE_PUSH_BACK(elem, tuple) \
    PP_TUPLE_PUSH_BACK_IMPL(PP_TUPLE_SIZE(tuple), elem, tuple)
#define PP_TUPLE_PUSH_BACK_IMPL(size, elem, tuple) \
    (PP_TUPLE_REMOVE_PARENS(tuple) PP_IF(size, PP_COMMA, PP_EMPTY)() elem)

插入元素
#define PP_TUPLE_INSERT(i, elem, tuple) \
    PP_TUPLE_ELEM( \
        3, \
        PP_AUTO_WHILE( \
            PP_TUPLE_INSERT_PRED, \
            PP_TUPLE_INSERT_OP, \
            (0, i, elem, (), tuple) \
        ) \
    )
#define PP_TUPLE_INSERT_PRED(args) PP_TUPLE_INSERT_PERD_IMPL args
#define PP_TUPLE_INSERT_PERD_IMPL(curi, i, elem, ret, tuple) \
    PP_NOT_EQUAL(PP_TUPLE_SIZE(ret), PP_INC(PP_TUPLE_SIZE(tuple)))
#define PP_TUPLE_INSERT_OP(args) PP_TUPLE_INSERT_OP_IMPL args
#define PP_TUPLE_INSERT_OP_IMPL(curi, i, elem, ret, tuple) \
    ( \
    PP_IF(PP_NOT_EQUAL(PP_TUPLE_SIZE(ret), i), PP_INC(curi), curi), \
    i, elem, \
    PP_TUPLE_PUSH_BACK(\
        PP_IF( \
            PP_NOT_EQUAL(PP_TUPLE_SIZE(ret), i), \
            PP_TUPLE_ELEM(curi, tuple), elem \
        ), \
        ret \
    ), \
    tuple \
    )

刪除末尾元素
#define PP_TUPLE_POP_BACK(tuple) \
    PP_TUPLE_ELEM( \
        1, \
        PP_AUTO_WHILE( \
            PP_TUPLE_POP_BACK_PRED, \
            PP_TUPLE_POP_BACK_OP, \
            (0, (), tuple) \
        ) \
    )
#define PP_TUPLE_POP_BACK_PRED(args) PP_TUPLE_POP_BACK_PRED_IMPL args
#define PP_TUPLE_POP_BACK_PRED_IMPL(curi, ret, tuple) \
    PP_IF( \
        PP_TUPLE_SIZE(tuple), \
        PP_NOT_EQUAL(PP_TUPLE_SIZE(ret), PP_DEC(PP_TUPLE_SIZE(tuple))), \
        0 \
    )
#define PP_TUPLE_POP_BACK_OP(args) PP_TUPLE_POP_BACK_OP_IMPL args
#define PP_TUPLE_POP_BACK_OP_IMPL(curi, ret, tuple) \
    (PP_INC(curi), PP_TUPLE_PUSH_BACK(PP_TUPLE_ELEM(curi, tuple), ret), tuple)

刪除元素
#define PP_TUPLE_REMOVE(i, tuple) \
    PP_TUPLE_ELEM( \
        2, \
        PP_AUTO_WHILE( \
            PP_TUPLE_REMOVE_PRED, \
            PP_TUPLE_REMOVE_OP, \
            (0, i, (), tuple) \
        ) \
    )
#define PP_TUPLE_REMOVE_PRED(args) PP_TUPLE_REMOVE_PRED_IMPL args
#define PP_TUPLE_REMOVE_PRED_IMPL(curi, i, ret, tuple) \
    PP_IF( \
        PP_TUPLE_SIZE(tuple), \
        PP_NOT_EQUAL(PP_TUPLE_SIZE(ret), PP_DEC(PP_TUPLE_SIZE(tuple))), \
        0 \
    )
#define PP_TUPLE_REMOVE_OP(args) PP_TUPLE_REMOVE_OP_IMPL args
#define PP_TUPLE_REMOVE_OP_IMPL(curi, i, ret, tuple) \
    ( \
    PP_INC(curi), \
    i, \
    PP_IF( \
        PP_NOT_EQUAL(curi, i), \
        PP_TUPLE_PUSH_BACK(PP_TUPLE_ELEM(curi, tuple), ret), \
        ret \
    ), \
    tuple \
    )

PP_TUPLE_SIZE(())               // -> 0

PP_TUPLE_PUSH_BACK(2, (1))      // -> (1, 2)
PP_TUPLE_PUSH_BACK(2, ())       // -> (2)

PP_TUPLE_INSERT(1, 2, (1, 3))   // -> (1, 2, 3)

PP_TUPLE_POP_BACK(())           // -> ()
PP_TUPLE_POP_BACK((1))          // -> ()
PP_TUPLE_POP_BACK((1, 2, 3))    // -> (1, 2)

PP_TUPLE_REMOVE(1, (1, 2, 3))   // -> (1, 3)
PP_TUPLE_REMOVE(0, (1, 2, 3))   // -> (2, 3)
```

這裡稍微解釋一下插入元素的實現，其他刪除元素等操作也是通過類似的原理來實現的。`PP_TUPLE_INSERT(i, elem, tuple)` 可以在 `tuple` 的位置 `i` 插入元素 `elem`，為了完成這個操作，先把位置小於 `i` 的元素都先用 `PP_TUPLE_PUSH_BACK` 放到一個新的 `tuple` 上（`ret`），然後在位置 `i` 放入元素 `elem`，之後再把原 `tuple` 位置大於等於 `i` 的元素放到 `ret` 後面，最後 `ret` 就得到我們想要的結果。

##結語

本文旨在說明清楚 C/C++ 宏編程的原理和基本實現。我將記錄一些自己的理解和認識，並希望能為他人提供一些幫助和啟發。值得注意的是，儘管本文有些長，但仍有一些有關宏編程的技巧和用法未涉及，例如 CHAOS_PP 提出的[基於延遲展開的遞歸調用方法](https://github.com/pfultz2/Cloak/wiki/C-Preprocessor-tricks,-tips,-and-idioms#deferred-expression)BOOST_PP 中的 `REPEAT` 相關巨集等等，有興趣的人可以自行查閱資料。

宏編程的調試是一個痛苦的過程，我們可以：

使用 `-P -E` 選項來輸出預處理結果；
使用我自己修改過的 `clang` 版本來仔細研究展開過程。
將複雜的宏拆解，查看中間宏的展開結果；
過濾不相關的標頭檔和巨集；
最後就是要腦補宏展開的過程了，熟悉宏展開之後調試的效率也會提升。

本文中的宏是我自己在理解了原理之後重新實現出來的，有部分宏借鑑了 `Boost` 的實現和引用裡面的文章，有任何錯誤之處，歡迎隨時指正，也歡迎找我來討論相關的問題。

這裡是本文的所有程式碼：[下載](assets/img/2021-3-31-cpp-preprocess/macros.cpp)，[線上展示](https://godbolt.org/z/coWvc5Pse)抱歉，原始的訊息無法翻譯，因為它不包含任何可供翻譯的內容。

##引文

* [Boost.Preprocessor](https://www.boost.org/doc/libs/1_75_0/libs/preprocessor/doc/)
(https://bot-man-jl.github.io/articles/?post=2020/Macro-Programming-Art)

--8<-- "footer_tc.md"


> 此文章是使用ChatGPT翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
