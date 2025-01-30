---
layout: post
title: C/C++ 宏編程解析
categories:
- c++
catalog: true
tags:
- dev
description: 本文的目的是要講清楚 C/C++ 宏編程的規則和實現方法，讓你不再懼怕看到代碼裡面的宏。
figures: []
---

<meta property="og:title" content="C/C++ 宏编程解析" />

本文的目的是要講清楚 C/C++ 的宏編程的規則和實現方法，讓你不再懼怕看到程式碼裡面的宏。我會首先說說 C++ 標準 14 裡面提到的關於宏展開的規則，然後通過修改 Clang 的源碼來觀察宏展開，最後基於這些知識來聊聊宏編程的實現。

這篇文章的程式碼都可以在這裡找到：[下載](assets/img/2021-3-31-cpp-preprocess/macros.cpp)，[線上展示](https://godbolt.org/z/coWvc5Pse)Sorry, already translated into Turnodinese.

##引子

我們可以藉由執行指令 `gcc -P -E a.cpp -o a.cpp.i` 讓編譯器對檔案 `a.cpp` 僅執行預處理並將結果保存到 `a.cpp.i` 中。

首先我們先來看一些例子：

####遞迴重入（Reentrancy）

``` cpp
#define ITER(arg0, arg1) ITER(arg1, arg0)

ITER(1, 2)          // -> ITER(2, 1)
```

宏 `ITER` 交換了 `arg0`、`arg1` 的位置。宏展開之後，得到的是 `ITER(2, 1)`。

您可以看到，`arg0` 和 `arg1` 的位置已成功交換。在這裡，巨集已成功展開一次，但僅限一次，不再進一步遞迴。換句話說，在巨集展開過程中，不可自我遞迴。若在遞迴過程中發現先前已展開過相同的巨集，則不會再次展開，這是巨集展開的其中一條重要規則。禁止遞迴遞迴的原因非常簡單，即避免無窮遞迴。

####字符串拼接

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                // -> HelloWorld
CONCAT(你好, CONCAT(世界, !))     // ->　你好CONCAT(世界, !)
```

宏 `CONCAT` 的用意是將 `arg0` 與 `arg1` 進行串接。宏展開後，`CONCAT(Hello, World)` 將正確得到 `HelloWorld` 的結果。然而，`CONCAT(Hello, CONCAT(World, !))` 則僅展開外層的宏，內層的 `CONCAT(World, !)` 並未展開，而是直接與 `Hello` 串接在一起。這與我們預期的不同，我們真正想要的結果是 `HelloWorld!`。這即是宏展開的另一重要規則：跟在 `##` 運算符後面的宏參數，不會被展開，而是直接與前面的內容進行串接。

通過上述兩個例子可以看出，宏展開的規則有一些是反直覺的，如果不清楚具體的規則，有可能寫出來的宏跟我們想要的效果不一致。

##宏展開規則

透過引子的兩個例子，我們了解到了宏展開是有一套標準的規則的，這套規則定義在 C/C++ 標準裡面，內容不多，建議先仔細讀幾遍，我這裡順帶給下標準 n4296 版本的連結，宏展開在 16.3 節：[傳送門](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4296.pdf)在這裡，我挑出了 n4296 版本中幾條重要的規則。這些規則將決定如何正確編寫巨集（建議花時間展開閱讀標準中的巨集）。

####參數分隔

宏的參數要求是用逗號分隔，而且參數的個數需要跟宏定義的個數一致，傳遞給宏的參數中，額外用括號包住的內容視為一個參數，參數允許為空：

``` cpp
#define ADD_COMMA(arg1, arg2) arg1, arg2

ADD_COMMA(a, b)             // -> a, b
新增逗號(a)                // 錯誤提示：宏 "MACRO" 需要 2 個引數，但只提供了 1 個"
ADD_COMMA((a, b), c)        // -> (a, b), c
ADD_COMMA(, b)              // -> , b
```

將這些文字翻譯為繁體中文：

將 `ADD_COMMA((a, b), c)` 中的 `(a, b)` 視為第一個參數。而在 `ADD_COMMA(, b)` 中，第一個參數為空，因此展開為 `, b`。

####宏參數展開

在展開巨集時，如果巨集的參數也是可展開的巨集，將會先完全展開參數，然後再展開巨集，例如

``` cpp
ADD_COMMA(ADD_COMMA(1, 2), ADD_COMMA(3, 4))     // -> 1, 2, 3, 4
```

一般情況下的巨集展開，都可以認為是先對參數求值，再對巨集求值，除非遇到了 `#` 和 `##` 運算符。

####`#` 操作符

`#` 操作符後面跟的宏參數，不會進行展開，會直接字符串化，例如：

``` cpp
#define STRINGIZE(arg0) # arg0

STRINGIZE(a)                // -> "a"
STRINGIZE(STRINGIZE(a))     // -> "STRINGIZE(a)"
```

根據這個規則 `STRINGIZE(STRINGIZE(a))` 只能展開為`"STRINGIZE(a)"`。

####`##` 操作符

`##` 操作符前後的宏參數，都不會進行展開，會先直接拼接起來，例如：

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                        // -> HelloWorld
CONCAT(Hello, CONCAT(World, !))             // -> HelloCONCAT(World, !)
CONCAT(CONCAT(Hello, World) C, ONCAT(!))    // -> CONCAT(Hello, World) CONCAT(!)
```

將這段文字翻譯為繁體中文：

`CONCAT(CONCAT(Hello, World) C, ONCAT(!))` 只能是先拼接在一起，得到 `CONCAT(Hello, World) CONCAT(!)`。

####重複掃描

預處理器執行完一次宏展開之後，會重新掃描得到的內容，繼續展開，直到沒有可以展開的內容為止。

一次宏展開，可以理解為先把參數完全展開（除非遇到 `#` 和 `##`），再根據宏的定義，把宏和完全展開後的參數按照定義進行替換，再處理定義中的所有 `#` 和 `##` 操作符。

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define STRINGIZE(arg0) # arg0

CONCAT(STRING, IZE(Hello))        // -> STRINGIZE(Hello) -> "Hello"
```

`CONCAT(STRING, IZE(Hello))` 第一次掃描展開得到 `STRINGIZE(Hello)`，然後執行第二次掃描，發現 `STRINGIZE` 可以繼續展開，最後得到 `"Hello"`。

####禁止递归重入

在重複掃描的過程中，禁止遞歸展開相同的宏。可以把宏展開理解為樹形的結構，根節點就是一開始要展開的宏，每個宏展開之後的內容作為該宏的子節點連接到樹上，那麼禁止遞歸就是在展開子節點的宏時，如果該宏跟任意祖先節點的宏相同，則禁止展開。來看一些例子：

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define CONCAT_SPACE(arg0, arg1) arg0 arg1
#define IDENTITY(arg0) IDENTITY_IMPL(arg0)
#define IDENTITY_IMPL(arg0) arg0

CONCAT(CON, CAT(a, b))                  // -> CONCAT(a, b)
IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))   // -> CONCAT(a, b)
IDENTITY(CONCAT(CON, CAT(a, b)))        // -> IDENTITY_IMPL(CONCAT(a, b)) -> CONCAT(a, b)
```

`CONCAT(CON, CAT(a, b))`：由於 `CONCAT` 是用 `##` 拼接兩個參數，根據 `##` 的規則，不會展開參數，直接拼接。所以第一次展開得到了 `CONCAT(a, b)`，由於 `CONCAT` 已經展開過了不會再遞迴展開，所以停止。

`IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))`：`IDENTITY_IMPL` 可以理解為對參數 `arg0` 求值，這裡的參數 `arg0` 求值得到了 `CONCAT(a, b)`，並由於遞歸被標記為了禁止重入，之後 `IDENTITY_IMPL` 展開完成，進行第二次掃描的時候，發現是禁止重入的 `CONCAT(a, b)`，於是停止展開。在這裡 `CONCAT(a, b)` 是由參數 `arg0` 展開而得到的，但在後續展開的時候，也會保持禁止重入的標記，可以理解為父節點是參數 `arg0`，一直保持著禁止重入的標記。

`IDENTITY(CONCAT(CON, CAT(a, b)))`: 這個範例的主要目的是加強對父子節點的理解。當參數自我展開時，它本身作為父節點，展開的內容則視為子節點進行遞迴判斷。展開後的參數傳遞到巨集定義後，禁止重入的標記將繼續保留（若展開後的巨集在傳遞到定義後未被更改）。可以將參數的展開過程視為另一棵樹，而展開的結果則是樹的最底層子節點。這個子節點在傳遞給巨集執行展開的同時，仍將保持禁止重入的特性。

例如這裡，在第一次完全展開之後得到 `IDENTITY_IMPL(CONCAT(a, b))`，`CONCAT(a, b)` 被標記為禁止重入，即使 `IDENTITY_IMPL` 是對參數求值的，但參數已經禁止展開，所以參數就原封不動地傳到定義裡，最後我們還是得到 `CONCAT(a, b)`。

我以上只列出一些我認為比較重要或較難理解的規則。若想要深入了解詳細內容，建議直接花點時間閱讀標準文件。

##通過 Clang 觀察展開過程

我們可以給 Clang 源碼加上一些打印信息來觀察宏展開的過程，我無意深入解釋 Clang 的源碼，在這裡給一份修改過的文件 diff，有興趣的可以自己編譯 Clang 來研究。這裡我使用的 llvm 版本 11.1.0 （[傳送門](https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-11.1.0.tar.gz)），修改過的檔案（[傳送門](assets/img/2021-3-31-cpp-preprocess/clang-modify.zip)）。下面简单通过例子来验证我们之前介绍的宏展开规则：

####Example 1

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(C, ONCAT(a, b))      // CONCAT(a, b)
```

使用修改過的 Clang 來預處理以上程式碼： `clang -P -E a.cpp -o a.cpp.i`，得到下面的印出資訊：

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

(#__codelineno-9-1)處理 `HandleIdentifier` 時遇到巨集時會印出，接著列印巨集資訊（第 [2-4](#__codelineno-9-2)行），宏沒有禁用，所以可以按照定義來展開 `Macro is ok to expand`，之後進入宏 `EnterMacro`。

真正執行宏展開的函數是 `ExpandFunctionArguments`，之後再次列印待展開的宏資訊，注意到此時宏已經被標記為 `used` （第 [9](#__codelineno-9-9)行）。之後根據宏的定義，進行逐個 `Token` 的展開 （`Token` 是 `Clang` 預處理裡面的概念，這裡不深入說明）。

第 0 個 `Token` 是形參 `arg0`，對應的實參是 `C`，判斷不需要展開，於是直接複製到結果上（第 [11-13](#__codelineno-9-11)行）。

第 1 個 `Token` 是 `hashhash`，也就是 `##` 操作符，繼續複製到結果上（第 [14-15](#__codelineno-9-14)行）。

第 2 個 `Token` 是形式參數 `arg1`，對應的實際參數是 `ONCAT(a, b)`，預處理器也會將實際參數處理成一個個的 `Token`，所以可以看到列印的結果用中括號包住了實際參數的每個 `Token`（第 18 行），由於 `##` 的原因這個實際參數依然不需要展開，所以還是直接複製到結果上（第 [16-18](#__codelineno-9-16)請注明合適的訊息（本行）。

最後 `Leave ExpandFunctionArguments` 印出本次掃描展開得到的結果（第 [19](#__codelineno-9-19)行），把结果的 `Token` 都翻译过来就是 `C ## ONCAT(a, b)`，之後預處理器就執行 `##` 操作符來生成新的內容。

## 执行之后得到 `CONCAT(a, b)`，遇到宏 `CONCAT`，预处理器先进入 `HandleIdentifier`，打印宏的信息，发现该宏状态是 `disable used`，已被展开，禁止再重入，显示 `Macro is not ok to expand`，预处理器不再展开，最后得到的结果就是 `CONCAT(a, b)`。

####例子2

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define IDENTITY(arg0) arg0

IDENTITY(CONCAT(C, ONCAT(a, b)))
```

<details>
<summary> <font> Clang 打印資訊（點擊展開）：</font> </summary>
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

第[12](#__codelineno-11-12)行開始展開 `IDENTITY`，發現參數 `Token 0` 是 `CONCAT(...)`，也是一個宏，於是先對該參數進行求值。

第 [27](#__codelineno-11-27)行開始展開參數宏 `CONCAT(...)`，跟例子 1 一樣，多次掃描展開完成後得到 `CONCAT(a, b)` （第 [46](#__codelineno-11-46)行）。

第 [47](#__codelineno-11-47)結束對 `IDENTITY` 的展開，得到的結果是 `CONCAT(a, b)`。

第 [51](#__codelineno-11-51)重新掃描 `CONCAT(a, b)` 行時發現，儘管它是一個宏，但在先前的參數展開過程中已經設置為 `used`，因此不再進行遞迴展開，直接作為最終結果。

####例子 3

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define IDENTITY_IMPL(arg0) arg0
#define IDENTITY(arg0) IDENTITY_IMPL(arg0)

IDENTITY(CONCAT(C, ONCAT(a, b)))
```

<details>
<summary> <font>Clang 打印信息（點擊展開）：</font> </summary>
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

第 [16](#__codelineno-13-16)行开始展开 `IDENTITY`，同理預處理器看到 `Token 2`（也即是 `arg0`）是宏，於是先展開 `CONCAT(C, ONCAT(a, b))`。

* 展開 `arg0` 後得到 `CONCAT(a, b)` （第 [23-54](#__codelineno-13-23)行）

* `IDENTITY` 最終展開為 `IDENTITY_IMPL(CONCAT(a, b))`（第 [57](#__codelineno-13-57)行）

* 重新掃描，繼續展開 `IDENTITY_IMPL`（第 [61-72](#__codelineno-13-61)根據以上內容進行翻譯：
行），發現此時的 `Token 0` 是宏 `CONCAT(a, b)`，但處於`used`狀態，中止展開並返回（第 75-84 行），最終得到的結果還是`CONCAT(a, b)`（第 [85](#__codelineno-13-85)行）。

重新掃描結果，發現宏 `CONCAT(a, b)` 的狀態是 `used`，停止展開並得到最終的結果。

透過以上三個簡單的例子，我們可以大致理解預處理器展開宏的過程，這裡不再對預處理器進行更深入的探討，有興趣可以對照我提供的修改文件來研究。

##宏編程實現

下面我們開始進入主題（前面那一大段的目的是為了更好地理解宏展開規則），宏編程實現。

####基本符號

首先可以先定義宏的特殊符號，做求值和拼接的時候會用到。

``` cpp
#define PP_LPAREN() (
#define PP_RPAREN() )
#define PP_COMMA() ,
#define PP_EMPTY()
#define PP_HASHHASH # ## #      // 表示 ## 字符串，但只是作为字符串，不会当作 ## 操作符来处理
```

####請問你有甚麼事需要幫忙？

利用參數優先展開的規則，可以寫出一個求值宏：

``` cpp
#define PP_IDENTITY(arg0) arg0

PP_COMMA PP_LPAREN() PP_RPAREN()                // -> PP_COMMA ( )
PP_IDENTITY(PP_COMMA PP_LPAREN() PP_RPAREN())   // -> PP_COMMA() -> ,
```

如果只是寫 `PP_COMMA PP_LPAREN() PP_RPAREN()`，預處理器只會分別處理每個宏，對展開的結果不會再合併處理。加上 `PP_IDENTITY` 之後，預處理器可以對展開得到的 `PP_COMMA()` 再進行求值，得到 `,`。


####拼接

由於 `##` 拼接時，並不會展開左右兩邊的參數，為了讓參數可以先求值再拼接，可以這樣寫：

``` cpp
#define PP_CONCAT(arg0, arg1) PP_CONCAT_IMPL(arg0, arg1)
#define PP_CONCAT_IMPL(arg0, arg1) arg0 ## arg1

PP_CONCAT(PP_IDENTITY(1), PP_IDENTITY(2))         // -> 12
PP_CONCAT_IMPL(PP_IDENTITY(1), PP_IDENTITY(2))    // -> PP_IDENTITY(1)PP_IDENTITY(2) -> 錯誤
```

這裡 `PP_CONCAT` 用到的方法叫做延遲拼接，在展開為 `PP_CONCAT_IMPL` 的時候，`arg0` 和 `arg1` 都會先展開求值，之後再由 `PP_CONCAT_IMPL` 執行真正的拼接操作。

####邏輯運算

利用 `PP_CONCAT` 可以實現邏輯運算。首先定義 `BOOL` 值：


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

用`PP_CONCAT`先把`PP_BOOL_`和`arg0`拼接在一起，再對拼接結果進行求值。這裡的`arg0`要求是求值之後得到`[0, 256]`範圍的數字，拼接在`PP_BOOL_`後面求值，就能得到布爾值。與或非運算：

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

先用 `PP_BOOL` 對參數求值，之後再根據 `0 1` 的組合來拼接邏輯運算的結果。如果不用 `PP_BOOL` 來求值，那麼參數就只能支持 `0 1` 兩種數值，適用性大大降低。同理也可以寫出異或、或非等操作，有興趣可以自己嘗試。

####條件選擇

利用 `PP_BOOL` 和 `PP_CONCAT`，還可以寫出條件選擇語句：

``` cpp
#define PP_IF(if, then, else) PP_CONCAT(PP_IF_, PP_BOOL(if))(then, else)
#define PP_IF_1(then, else) then
#define PP_IF_0(then, else) else

PP_IF(1, 2, 3)      // -> PP_IF_1(2, 3) -> 2
PP_IF(0, 2, 3)      // -> PP_IF_0(2, 3) -> 3
```

如果 `if` 的求值是 `1`，則用 `PP_CONCAT` 拼接成 `PP_IF_1`，最後展開為 `then` 的值；同理若 `if` 的求值為 `0`，則得到 `PP_IF_0`。

####遞增遞減

整數遞增遞減：

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

與 `PP_BOOL` 相似，整數的遞增遞減也有範圍限制，這裡範圍設定為 `[0, 256]`。在增加到 `256` 之後，為確保安全，`PP_INC_256` 會返回自身的 `256` 作為邊界，同樣地，`PP_DEC_0` 也會返回 `0`。

####可變參數

宏可以接受不固定參數，格式為：

```cpp
#define LOG(format, ...) printf("log: " format, __VA_ARGS__)

LOG("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG("Hello World")              // -> printf("log: " "Hello World", ); 多了個逗號，編譯報錯
```

由於變長參數有可能為空，空的情況下會導致編譯失敗，因此 C++ 20 引入了 `__VA_OPT__`，如果變長參數是空，則返回空，否則返回原參數：

```cpp
#define LOG2(format, ...) printf("log: " format __VA_OPT__(,) __VA_ARGS__)

LOG2("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG2("Hello World")              // -> printf("log: " "Hello World" ); 沒有逗號，正常編譯
```

但可惜只有 C++ 20 以上標準才有這個宏，下文中我們將會給出 `__VA_OPT__` 的實現方法。

####惰性求值

考虑这种情况：

``` cpp
PP_IF(1, PP_COMMA(), PP_LPAREN())     // -> PP_IF_1(,,)) -> 报错 unterminated argument list invoking macro "PP_IF_1"
```

我們知道，宏展開的時候會對先參數進行求值。`PP_COMMA()` 和 `PP_LPAREN()` 求值之後再傳給 `PP_IF_1`，得到 `PP_IF_1(,,))`，導致預處理出錯。此時，可以採用一種叫做惰性求值的方法：

``` cpp
PP_IF(1, PP_COMMA, PP_LPAREN)()       // -> PP_IF_1(PP_COMMA, PP_LPAREN)() -> PP_COMMA() -> ,
```

改成這種寫法，只傳宏的名字，讓 `PP_IF` 選出需要的宏名字之後，再跟括號 `()` 拼接在一起組成完成的宏，最後再展開。惰性求值在宏編程裡面也是很常見的。

####開始以括號。

判斷可變參數是否以括號開頭：

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

`PP_IS_BEGIN_PARENS` 可以用來判斷傳入的參數是否以括號開始，在需要處理括號參數的時候會需要用到（譬如後面說到的 `__VA_OPT__` 實現）。看起來有點複雜，核心思想就是構建出一個宏，若變長參數以括號開始，則可以跟括號連在一起求值得到一種結果，否則就另外求值得到另一種結果。我們來慢慢看：

`PP_IS_BEGIN_PARENS_PROCESS` 和 `PP_IS_BEGIN_PARENS_PROCESS_0` 组成的宏功能是先對傳入的不定參數求值，然後取第 0 個參數。

`PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__)` 是先對 `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` 求值，再將求值結果與 `PP_IS_BEGIN_PARENS_PRE_` 拼接在一起。

`PP_IS_BEGIN_PARENS_EAT(...)` 宏會吞掉所有參數，返回1，如果上一步 `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` 中，`__VA_ARGS__` 以括號開始，那麼就會匹配到對 `PP_IS_BEGIN_PARENS_EAT(...)` 的求值，然後返回 `1`；相反，如果不是以括號開始，則沒有匹配上，`PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` 會保留不變。

若 `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` 求值得到 `1`，`PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, 1) -> PP_IS_BEGIN_PARENS_PRE_1 -> 1`，注意 `1` 後面是有個逗號的，把 `1, ` 傳給 `PP_IS_BEGIN_PARENS_PROCESS_0`，取第 0 個參數，最後得到 `1`，表示參數是以括號開始。

若 `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` 求值得到不是 `1`，而是保持不变，則 `PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__) -> PP_IS_BEGIN_PARENS_PRE_PP_IS_BEGIN_PARENS_EAT __VA_ARGS__ -> 0, __VA_ARGS__`，傳給 `PP_IS_BEGIN_PARENS_PROCESS_0` 得到的是 `0`，表示參數不是以括號開始。

####可變長參數空

判斷可變長參數是否為空也是一個常見的巨集，在實現 `__VA_OPT__` 時需要使用，我們可以在這裡利用 `PP_IS_BEGIN_PARENS`，可以先撰寫出不完整的版本：

``` cpp
#define PP_IS_EMPTY_PROCESS(...) \
    PP_IS_BEGIN_PARENS(PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ())
#define PP_IS_EMPTY_PROCESS_EAT(...) ()

PP_IS_EMPTY_PROCESS()       // -> 1
PP_IS_EMPTY_PROCESS(1)      // -> 0
PP_IS_EMPTY_PROCESS(1, 2)   // -> 0
PP_IS_EMPTY_PROCESS(())     // -> 1
```

`PP_IS_EMPTY_PROCESS` 的功能是判斷 `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__() ` 是否以括號開始。

如果 `__VA_ARGS__` 是空，`PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ () -> PP_IS_EMPTY_PROCESS_EAT() -> ()`，得到的是一對括號 `()`，再傳給 `PP_IS_BEGIN_PARENS` 返回 `1`，表示參數是空。

否則，`PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ()` 會保持不變地傳給 `PP_IS_BEGIN_PARENS`，返回 0，表示非空。

留意第 4 個例子 `PP_IS_EMPTY_PROCESS(()) -> 1`，`PP_IS_EMPTY_PROCESS` 不能正確處理以括號開始的變長參數，因為這時變長參數帶來的括號會匹配 `PP_IS_EMPTY_PROCESS_EAT`，導致求值得到 `()`。為了解決這個問題，我們需要區別對待參數是否以括號開始的情況：

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

`PP_IS_EMPTY_IF` 根據 `if` 條件來返回第 0 或者第 1 個參數。

如果傳入的變長參數以括號開始，`PP_IS_EMPTY_IF` 返回 `PP_IS_EMPTY_ZERO`，最後返回 `0`，表示變長參數非空。

反之 `PP_IS_EMPTY_IF` 返回 `PP_IS_EMPTY_PROCESS`，最後由 `PP_IS_EMPTY_PROCESS` 來判斷變長參數是否非空。

####下標訪問

獲取變長參數指定位置的元素：

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

將文本翻譯成繁體中文：

`PP_ARGS_ELEM` 的第一個參數是元素下標 `I`，後面是變長參數。利用 `PP_CONCAT` 拼接 `PP_ARGS_ELEM_` 和 `I`，即可以得到返回相應位置元素的巨集 `PP_ARGS_ELEM_0..8`，再把變長參數傳給該巨集，展開返回下標對應位置的元素。

#### PP_IS_EMPTY2

利用“PP_ARGS_ELEM”也可以實現另一版本的“PP_IS_EMPTY”：

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

利用 'PP_ARGS_ELEM' 實現判斷參數是否包含逗號 'PP_HAS_COMMA'。 'PP_COMMA_ARGS' 會吸收任何傳入的參數，並返回一個逗號。

判斷變長參數是否為空的基礎邏輯是 `PP_COMMA_ARGS __VA_ARGS__ ()` 返回一個逗號，也就是 `__VA_ARGS__` 為空，`PP_COMMA_ARGS` 和 `()` 拼接在一起求值，具體的寫法就是 `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ())`。

但是會有例外的情況：

* `__VA_ARGS__` 本身有可能會帶來逗號；
`__VA_ARGS__()` 會將所有參數連接在一起，並在求值時加入逗號；
`PP_COMMA_ARGS __VA_ARGS__` 拼接在一起時將產生一個包含逗號的表達式；

針對上面提到的三種例外情況，需要進行排除，因此最後寫法等價於對以下四個條件執行與邏輯：

* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__))` &&
* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__()))` &&
* `PP_NOT(PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__))` &&
* `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ())`

#### `__VA_OPT__`

利用`PP_IS_EMPTY`終於可以來實現類似`__VA_OPT__`的巨集：

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

使用 `PP_ARGS_OPT`，您可以實現類似於 `LOG2` 的功能來模擬 `LOG3` 的實現：

``` cpp
#define LOG3(format, ...) \
    printf("log: " format PP_ARGS_OPT((,), (), __VA_ARGS__) __VA_ARGS__)

LOG3("Hello");                  // -> printf("log: " "Hello" );
LOG3("Hello %s", "World");      // -> printf("log: " "Hello %s" , "World");
```

`data_tuple` 是 `(,)`，如果变长参数非空，则会返回 `data_tuple` 里面的所有元素，在这里就是逗号 `,`。

####求參數個數

獲取變長參數的個數：

``` cpp
#define PP_ARGS_SIZE_IMCOMPLETE(...) \
    PP_ARGS_ELEM(8, __VA_ARGS__, 8, 7, 6, 5, 4, 3, 2, 1, 0)

PP_ARGS_SIZE_IMCOMPLETE(a)             // -> 1
PP_ARGS_SIZE_IMCOMPLETE(a, b)          // -> 2
PP_ARGS_SIZE_IMCOMPLETE(PP_COMMA())    // -> 2
PP_ARGS_SIZE_IMCOMPLETE()              // -> 1
```

計算可變長參數的數量是通過索引位置來確定的。`__VA_ARGS__` 會導致後續參數整體右移，使用宏 `PP_ARGS_ELEM` 可以獲取第 8 個位置的參數。如果 `__VA_ARGS__` 只有一個參數，那麼第 8 個參數就等於 `1`；同樣地，如果 `__VA_ARGS__` 有兩個參數，那麼第 8 個參數就會變為 `2`，恰好等於可變長參數的數量。

這裡給的例子只最高支持個數 8 的變長參數，這是依賴於 `PP_ARGS_ELEM` 所能支持的最大長度。

但是這個宏還不完整，在變長參數為空的情況下，這個宏會錯誤返回 `1`。如果需要處理空的變長參數，則需要用到我們前面提到的 `PP_ARGS_OPT` 宏：

``` cpp
#define PP_COMMA_IF_ARGS(...) PP_ARGS_OPT((,), (), __VA_ARGS__)
#define PP_ARGS_SIZE(...) PP_ARGS_ELEM(8, __VA_ARGS__ PP_COMMA_IF_ARGS(__VA_ARGS__) 8, 7, 6, 5, 4, 3, 2, 1, 0, 0, 0)

PP_ARGS_SIZE(a)             // -> 1
PP_ARGS_SIZE(a, b)          // -> 2
PP_ARGS_SIZE(PP_COMMA())    // -> 2
PP_ARGS_SIZE()              // -> 0
PP_ARGS_SIZE(,,,)           // -> 4
```

問題的關鍵就是逗號 `,`，在 `__VA_ARGS__` 為空的時候，把逗號隱去就能正確返回 `0`。

####遍歷訪問

類似 C++ 的 `for_each`，我們可以實現巨集的 `PP_FOR_EACH`：

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

`PP_FOR_EACH` 接收兩個固定參數： `macro` 可以理解為遍歷時候調用的宏，`contex` 可以作為固定值參數傳給 `macro`。`PP_FOR_EACH` 先通過 `PP_ARGS_SIZE` 獲取變長參數的長度 `N`，再用 `PP_CONCAT` 拼接得到 `PP_FOR_EACH_N`，之後 `PP_FOR_EACH_N` 會迭代調用 `PP_FOR_EACH_N-1` 來實現跟變長參數個數相同的遍歷次數。

在這個範例中，我們定義了 `DECLARE_EACH` 作為 `macro` 函式的參數。`DECLARE_EACH` 的功能是返回 `contex arg`，如果 `contex` 是型別名，而 `arg` 是變數名，透過 `DECLARE_EACH` 就能夠宣告變數。

####條件循環

有了 `FOR_EACH` 之后，我们還可以用類似的寫法寫出 `PP_WHILE`：

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

`PP_WHILE` 接受三個參數： `pred` 條件判斷函數，`op` 操作函數，`val` 初始值；在循環的過程中不斷用 `pred(val)` 來做循環終止判斷，把 `op(val)` 得到的值傳給後續的宏，可以理解為執行以下代碼：

``` cpp
while (pred(val)) {
    val = op(val);
}
```

首先使用 `pred(val)` 取得條件判斷結果，然後將條件結果 `cond` 和其餘參數再傳遞給 `PP_WHILE_N_IMPL`。
`PP_WHILE_N_IMPL` 可以分為兩部分來看：後半部分 `(pred, op, PP_IF(cond, op, PP_EMPTY_EAT)(val))` 是作為前半部分的參數，`PP_IF(cond, op, PP_EMPTY_EAT)(val)` 是如果 `cond` 為真，則求值 `op(val)`，否則求值 `PP_EMPTY_EAT(val)` 得到空。前半部分 `PP_IF(cond, PP_WHILE_N+1, val PP_EMPTY_EAT)`，如果 `cond` 為真，則返回 `PP_WHILE_N+1`，結合後半部分的參數繼續執行循環；否則返回 `val PP_EMPTY_EAT`，此時 `val` 就是最終的計算結果，而 `PP_EMPTY_EAT` 會吞掉後半部分的結果。

`SUM` 實現 `N + N-1 + ... + 1`。初始值 `(max_num, origin_num)`；`SUM_PRED` 取值的第一個元素 `x`，判斷是否大於 0；`SUM_OP` 對 `x` 執行遞減操作 `x = x - 1`，對 `y` 執行 `+ x` 操作 `y = y + x`。直接用 `SUM_PRED` 和 `SUM_OP` 傳給 `PP_WHILE`，返回的結果是一個元組，我們真正想要的結果是元組的第 2 個元素，於是再用 `SUM` 取第 2 個元素的值。

####遞迴重入

到目前為止，我們的遍歷訪問和條件循環都運作得很好，結果符合預期。還記得我們在講宏展開規則的時候提到的禁止遞歸重入嗎？當我們想要執行兩重循環的時候就不幸遇到了禁止遞歸重入：

``` cpp
#define SUM_OP2(xy_tuple) SUM_OP_OP_IMPL2 xy_tuple
#define SUM_OP_OP_IMPL2(x, y) (PP_DEC(x), y + SUM(x, 0))

#define SUM2(max_num, origin_num) \
    PP_IDENTITY(SUM_IMPL PP_WHILE(SUM_PRED, SUM_OP2, (max_num, origin_num)))

SUM2(1, a)      // -> a + SUM_IMPL PP_WHILE_1(SUM_PRED, SUM_OP, (1, a))
```

`SUM2` 把參數 `op` 改用 `SUM_OP2`，`SUM_OP2` 裡面會調用到 `SUM`，而 `SUM` 展開還會是 `PP_WHILE_1`，相當於 `PP_WHILE_1` 遞迴調用到了自身，預處理器停止展開。

為了解決這個問題，我們可以用一種自動推導遞歸的方法（Automatic Recursion）：

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

`PP_AUTO_WHILE` 是 `PP_WHILE` 的自動推導遞迴版本，核心的巨集是 `PP_AUTO_REC(PP_WHILE_PRED)`，這個巨集可以找出當前可用的 `PP_WHILE_N` 版本的數字 `N`。

推導的原理很簡單，就是搜索所有版本，找出能夠正確展開的版本，返回該版本的數字。為了提升搜索的速度，一般的做法是使用二分查找，這就是 `PP_AUTO_REC` 在做的事情。`PP_AUTO_REC` 接受一個參數 `check`，`check` 負責檢查版本可用性，這裡給出的是支持搜索版本範圍 `[1, 4]`。`PP_AUTO_REC` 會首先檢查 `check(2)`，如果 `check(2)` 為真，則調用 `PP_AUTO_REC_12` 搜索範圍 `[1, 2]`，否則用 `PP_AUTO_REC_34` 搜索 `[3, 4]`。`PP_AUTO_REC_12` 檢查 `check(1)` 如果為真，說明版本 `1` 可用，否則用版本 `2`，`PP_AUTO_REC_34` 同理。

`check` 宏要怎麼寫才能知道版本是否可用呢？在這裡，`PP_WHILE_PRED` 會展開成兩部分的拼接，我們來看後部分 `PP_WHILE_ ## n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`：如果 `PP_WHILE_ ## n` 可用，由於 `PP_WHILE_FALSE` 固定返回 `0`，這部分會展開得到 `val` 參數的值，也就是 `PP_WHILE_FALSE`；否則這部分宏會保持不變，依然是 `PP_WHILE_n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`。

把後部分的結果跟前部分 `PP_WHILE_CHECK_` 拼接起來，得到兩種結果：`PP_WHILE_CHECK_PP_WHILE_FALSE` 或者 `PP_WHILE_CHECK_PP_WHILE_n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`，於是我們讓 `PP_WHILE_CHECK_PP_WHILE_FALSE` 返回 `1` 表明可用，`PP_WHILE_CHECK_PP_WHILE_n` 返回 `0` 表示不可用。至此，我們完成了自動推導遞歸的功能。

####算術比較

不相等：

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

判斷數值是否相等，使用了禁止遞歸重入的特性，將 `x` 和 `y` 遞歸拼接成 `PP_NOT_EQUAL_x PP_NOT_EQUAL_y` 宏，如果 `x == y`，則不會展開 `PP_NOT_EQUAL_y` 宏，與 `PP_NOT_EQUAL_CHECK_` 拼接成 `PP_NOT_EQUAL_CHECK_PP_NOT_EQUAL_y` 返回 `0`；反之，兩次都成功展開最後得到 `PP_EQUAL_NIL`，拼接得到 `PP_NOT_EQUAL_CHECK_PP_EQUAL_NIL` 返回 `1`。

相等：

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

另外還有大於、大於等於等等算術比較，這裡不再赘述。

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

乘法的實現這裡增加了一個參數 `ret`，初始值為 `0`，每次迭代會執行 `ret = ret + x`。

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

除法利用了 `PP_LESS_EQUAL`，只有 `y <= x` 的情況下才繼續迴圈。

####資料結構

宏也可以有資料結構，事實上我們之前稍微使用了一種資料結構 `tuple`，`PP_REMOVE_PARENS` 就是可以去掉 `tuple` 的外層括號，並返回其中的元素。在這裡以 `tuple` 為例子討論相關的實作，對於其他資料結構如 `list, array` 等有興趣的話，可以去查看 `Boost` 的實作。

`tuple` 定義為用括號包住的逗號分開的元素集合：`(a, b, c)`。

``` cpp
#define PP_TUPLE_REMOVE_PARENS(tuple) PP_REMOVE_PARENS(tuple)

獲取指定索引的元素
#define PP_TUPLE_ELEM(i, tuple) PP_ARGS_ELEM(i, PP_TUPLE_REMOVE_PARENS(tuple))

// 吞掉整個 tuple 返回空
#define PP_TUPLE_EAT() PP_EMPTY_EAT

// 獲取大小
#define PP_TUPLE_SIZE(tuple) PP_ARGS_SIZE(PP_TUPLE_REMOVE_PARENS(tuple))

添加元素
#define PP_TUPLE_PUSH_BACK(elem, tuple) \
    PP_TUPLE_PUSH_BACK_IMPL(PP_TUPLE_SIZE(tuple), elem, tuple)
#define PP_TUPLE_PUSH_BACK_IMPL(size, elem, tuple) \
    (PP_TUPLE_REMOVE_PARENS(tuple) PP_IF(size, PP_COMMA, PP_EMPTY)() elem)

// 插入元素
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

// 刪除末尾元素
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

// 刪除元素
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

##結論

這篇文章的目的是要清楚闡述 C/C++ 宏編程的原理和基本實現，同時記錄了一些我自己的理解和認識，希望能對其他人有所幫助和啟發。需要注意的是，雖然這篇文章有點長，但仍有一些關於宏編程的技巧和用法並未涉及到，比如 CHAOS_PP 提出的[基於延遲展開的遞歸調用方法](https://github.com/pfultz2/Cloak/wiki/C-Preprocessor-tricks,-tips,-and-idioms#deferred-expression)，BOOST_PP 里面的 `REPEAT` 相關宏等等，有興趣的可以自行查閱資料。

宏編程的調試是一個痛苦的過程，我們可以：

使用 `-P -E` 選項輸出預處理結果；
使用我自己修改過的 `clang` 版本，仔細研究展開過程。
* 將複雜的宏拆解，查看中間宏的展開結果；
過濾無關的標頭檔和巨集；
最後就是要腦補宏展開的過程了，熟悉宏展開之後調試的效率也會提升。

本文中的宏是我自己在理解了原理之後重新實現出來的，有部分宏借鑒了 `Boost` 的實現和引用裡面的文章，有任何錯誤之處，歡迎隨時指正，也歡迎找我來討論相關的問題。

這篇文章的程式碼都可以在這裡找到：[下載](assets/img/2021-3-31-cpp-preprocess/macros.cpp)，[線上演示](https://godbolt.org/z/coWvc5Pse)。

##引用

* [Boost.Preprocessor](https://www.boost.org/doc/libs/1_75_0/libs/preprocessor/doc/)
* [C/C++ 宏編程的藝術](https://bot-man-jl.github.io/articles/?post=2020/Macro-Programming-Art)

--8<-- "footer_tc.md"


> 這篇帖文是由 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
