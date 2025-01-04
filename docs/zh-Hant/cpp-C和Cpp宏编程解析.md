---
layout: post
title: C/C++ 宏編程解析
categories:
- c++
catalog: true
tags:
- dev
description: 本文的目的是要講清楚 C/C++ 宏編程的規則和實現方法，讓你不再畏懼看到程式碼裡面的宏。
figures: []
---

<meta property="og:title" content="C/C++ 宏编程解析" />

本文的目的是要說明 C/C++ 的巨集編程規則和實作方法，讓你不再害怕看到程式碼中的巨集。我將首先說明 C++ 標準 14 中關於巨集展開的規則，接著通過修改 Clang 的原始碼來觀察巨集展開，最後根據這些知識來討論巨集編程的實現。

這裡是本文的所有程式碼：[下載](assets/img/2021-3-31-cpp-preprocess/macros.cpp)，[線上展示](https://godbolt.org/z/coWvc5Pse)抱歉，我無法為你提供翻譯。

##前言

我地可以透過執行指令 `gcc -P -E a.cpp -o a.cpp.i` 令編譯器只對文件 `a.cpp` 進行預處理並將結果保存到 `a.cpp.i`。

首先讓我們來看一些例子：

####递归重入（Reentrancy）

``` cpp
#define ITER(arg0, arg1) ITER(arg1, arg0)

ITER(1, 2)          // -> ITER(2, 1)
```

這個巨集 `ITER` 交換了 `arg0` 和 `arg1` 的位置。展開這個巨集後，得到的結果是 `ITER(2, 1)`。

可以看到，`arg0` `arg1` 的位置成功交換，在這裡巨集成功展開了一次，但也只展開了一次，不再遞歸重入。換言之，巨集的展開過程中，是不可自身遞歸重入的，如果在遞歸的過程中發現相同的巨集在之前的遞歸中已經展開過，則不再展開，這是巨集展開的其中一條重要的規則。禁止遞歸重入的原因也很簡單，就是為了避免無限遞歸。

####字串串組合

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                // -> HelloWorld
結合(你好, 結合(世界, !))     // ->　你好結合(世界, !)
```

宏 `CONCAT` 的目的是拼接 `arg0` `arg1`。展開之後，`CONCAT(Hello, World)` 可以得到正確的結果 `HelloWorld`。但是 `CONCAT(Hello, CONCAT(World, !))` 卻只展開了外層的宏，內層的 `CONCAT(World, !)` 並沒有展開，直接跟 `Hello` 拼接在一起，與預期不同，真正想要的結果應為 `HelloWorld!`。這就是展開宏的另一個重要規則：緊接在 `##` 操作符後面的宏參數不會被展開，而是直接與前面的內容拼接。

通過上述兩個例子，我們可以看出，宏展開的規則中有一些是違反直覺的。如果不清楚具體的規則，有可能原本想要的效果與最後的宏定義結果不一致。

##擴展規則

透過引子裡的兩個例子，我們了解到巨集展開有一套標準的規則，這套規則定義在 C/C++ 標準裡面，內容不多，建議先仔細讀幾遍，我這裡順帶給下標準 n4296 版本的連結，巨集展開在 16.3 節：[傳送門](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4296.pdf)我挑出 n4296 版本中幾條重要的規則，這些規則會決定如何正確編寫巨集（還是建議抽時間把標準裡面的巨集展開細讀下）。

####參數分隔

宏的參數要求是用逗號分隔，而且參數的個數需要跟宏定義的個數一致，傳遞給宏的參數中，額外用括號包住的內容視為一個參數，參數允許為空：

``` cpp
#define ADD_COMMA(arg1, arg2) arg1, arg2

ADD_COMMA(a, b)             // -> a, b
ADD_COMMA(a) // 錯誤：宏“MACRO”要求有2個參數，但只給出了1個。
ADD_COMMA((a, b), c)        // -> (a, b), c
ADD_COMMA(, b)              // -> , b
```

`ADD_COMMA((a, b), c)` 中的`(a, b)`被視為第一個參數。在`ADD_COMMA(, b)`中，第一個參數為空，所以展開為`, b`。

####宏參數展開

在展開宏的時候，如果宏的參數也是可以展開的宏，會先將參數完全展開，再展開宏，例如

``` cpp
ADD_COMMA(ADD_COMMA(1, 2), ADD_COMMA(3, 4))     // -> 1, 2, 3, 4
```

一般情況下的巨集展開，都可以認為是先對參數求值，再對巨集求值，除非遇到了 `#` 和 `##` 操作符。

####`#` 運算符

`#` 符號後跟的巨集參數不會被展開，會直接轉換為字串，例如：

``` cpp
#define STRINGIZE(arg0) # arg0

STRINGIZE(a)                // -> "a"
STRINGIZE(STRINGIZE(a))     // -> "STRINGIZE(a)"
```

根據這條規則 `STRINGIZE(STRINGIZE(a))` 只能展開為 `"STRINGIZE(a)"`。

####`##` 運算子

`##`運算子前後的巨集參數不會被展開，而是直接拼接在一起，例如：

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                        // -> HelloWorld
CONCAT(Hello, CONCAT(World, !))             // -> HelloCONCAT(World, !)
CONCAT(CONCAT(Hello, World) C, ONCAT(!))    // -> CONCAT(Hello, World) CONCAT(!)
```

將這段文字翻譯為繁體中文:

`CONCAT(CONCAT(Hello, World) C, ONCAT(!))` 它應該先連接在一起，得到 `CONCAT(Hello, World) CONCAT(!)`。

####重複掃描

預處理器執行完一次巨集展開後，會重新掃描獲得的內容，繼續展開，直到沒有可以展開的內容為止。

一次宏展開，可以理解為先把參數完全展開（除非遇到 `#` 和 `##`），再根據宏的定義，把宏和完全展開後的參數按照定義進行替換，再處理定義中的所有 `#` 和 `##` 操作符。

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define STRINGIZE(arg0) # arg0

CONCAT(STRING, IZE(Hello))        // -> STRINGIZE(Hello) -> "Hello"
```

`CONCAT(STRING, IZE(Hello))` 首次掃描展開得到 `STRINGIZE(Hello)`，然後執行第二次掃描，發現 `STRINGIZE` 可以繼續展開，最終得到 `"Hello"`。

####禁止遞迴重入

在重複掃描的過程中，禁止遞歸展開相同的巨集。可以將巨集展開理解為樹狀結構，根節點就是一開始要展開的巨集，每個巨集展開之後的內容作為該巨集的子節點連接到樹上，那麼禁止遞歸就是在展開子節點的巨集時，如果該巨集跟任意祖先節點的巨集相同，則禁止展開。來看一些例子：

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define CONCAT_SPACE(arg0, arg1) arg0 arg1
#define IDENTITY(arg0) IDENTITY_IMPL(arg0)
#define IDENTITY_IMPL(arg0) arg0

CONCAT(CON, CAT(a, b))                  // -> CONCAT(a, b)
IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))   // -> CONCAT(a, b)
IDENTITY(CONCAT(CON, CAT(a, b)))        // -> IDENTITY_IMPL(CONCAT(a, b)) -> CONCAT(a, b)
```

`CONCAT(CON, CAT(a, b))`：因為 `CONCAT` 是使用 `##` 連接兩個參數，根據 `##` 的規則，不會展開參數，直接連接。所以第一次展開得到了 `CONCAT(a, b)`，由於 `CONCAT` 已經展開過了不會再遞歸展開，所以停止。

`IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))`：`IDENTITY_IMPL` 可以視為對參數 `arg0` 進行求值，這裡的參數 `arg0` 求值後得到了 `CONCAT(a, b)`，並由於遞歸被標記為禁止重入，之後 `IDENTITY_IMPL` 展開完成，進行第二次掃描時，發現禁止重入的 `CONCAT(a, b)`，因此停止展開。在這裡 `CONCAT(a, b)` 是由參數 `arg0` 展開而得到的，但在後續展開時，也會保持禁止重入的標記，可以視為父節點是參數 `arg0`，一直保持著禁止重入的標記。

`IDENTITY(CONCAT(CON, CAT(a, b)))`：這個例子主要是為了強化對父子節點的理解，當參數自己展開時，它自身作為父節點，展開的內容則作為子節點進行遞歸判斷。展開後的參數傳遞到巨集定義之後，禁止重入的標記將繼續保留（如果巨集定義後未更改展開後的參數）。可以將參數的展開過程視為另一顆樹，展開結果即為樹的最底層子節點，這子節點傳給巨集執行展開時，仍然保有禁止重入的特性。

例如這裡，當第一次完全展開後獲得 `IDENTITY_IMPL(CONCAT(a, b))`，`CONCAT(a, b)` 被標記為禁止重入，即使 `IDENTITY_IMPL` 是對參數求值的，但參數已經禁止展開，所以參數就原封不動地傳到定義裡，最後我們還是得到 `CONCAT(a, b)`。

我只列出一些我認為重要或是不太容易理解的規則，若要深入了解規則，建議花點時間直接閱讀標準文件。

##通過 Clang 觀察展開過程

我哋可以喺 Clang 嘅原始碼度加啲印信息嚟觀察宏展開嘅過程，我無意深入解釋 Clang 嘅原始碼，喺呢度畀一份修改過嘅檔案 diff，有興趣嘅可以自己編譯 Clang 嚟研究。呢度我係用嘅 llvm 版本 11.1.0（[傳送門](https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-11.1.0.tar.gz)），修改過的檔案（[傳送門](assets/img/2021-3-31-cpp-preprocess/clang-modify.zip)）。下面簡單透過例子來驗證我們之前介紹的巨集展開規則：

####例子1

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(C, ONCAT(a, b))      // CONCAT(a, b)
```

使用修改過的 Clang 來預處理以上程式碼：`clang -P -E a.cpp -o a.cpp.i`，獲得以下的輸出訊息：

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

(#__codelineno-9-1)當處理 `HandleIdentifier` 時遇到巨集時會列印，然後列印巨集的資訊（第[2-4](#__codelineno-9-2)已解決。

真正執行巨集展開的函數是 `ExpandFunctionArguments`，之後再次列印待展開的巨集資訊，注意到此時巨集已經被標記為 `used`（第 [9](#__codelineno-9-9)根据宏的定義，依序展開每個「Token」（「Token」是在「Clang」預處理器中的概念，這裡不深入說明）。

第 0 個「Token」為形參數「arg0」，對應的實參數是「C」，判斷不需要展開，因此直接複製到結果上（第 [11-13](#__codelineno-9-11)行）。

第 1 個 `Token` 是 `hashhash`，也就是 `##` 操作符，繼續複製到結果上（第 [14-15](#__codelineno-9-14)請問您需要將這些文字翻譯成繁體中文嗎？

第2個`Token`是形參`arg1`，對應的實參是`ONCAT(a, b)`，預處理器也會把實參處理成一個個的`Token`，所以可以看到列印的結果用中括號包住了實參的每個`Token`（第18行），由於`##`的原因這個實參依然不需要展開，所以還是直接複製到結果上（第[16-18](#__codelineno-9-16)行）。

最後 `Leave ExpandFunctionArguments` 印出此次掃描展開後得到的結果（第 [19](#__codelineno-9-19)進行時，將結果中的 `Token` 都翻譯為 `C ## ONCAT(a, b)`，然後預處理器會執行 `##` 運算子來生成新的內容。

`##` 執行之後得到 `CONCAT(a, b)`，遇到巨集 `CONCAT`，預處理還是先進入 `HandleIdentifier`，打印巨集的資訊，發現該巨集狀態是 `disable used`，是已經展開過的，禁止再重入了，顯示 `Macro is not ok to expand`，預處理器不再展開，最終得到的結果就是 `CONCAT(a, b)`。

####範例2

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define IDENTITY(arg0) arg0

IDENTITY(CONCAT(C, ONCAT(a, b)))
```

<details>
<概要> <字體> Clang 打印資訊（點擊展開）：</字體> </概要>
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

(#__codelineno-11-12)在開始擴展`IDENTITY`行時，發現參數`Token 0`是`CONCAT(...)`，同時也算是一個巨集，因此先對該參數進行求值。

(#__codelineno-11-27)行开始展开参数宏 `CONCAT(...)`，跟例子 1 一样，多次扫描展开完成后得到 `CONCAT(a, b)` （第 [46](#__codelineno-11-46)行）。

第 [47](#__codelineno-11-47)結束對 `IDENTITY` 的展開，得到的結果是 `CONCAT(a, b)`。

第 [51](#__codelineno-11-51)重新掃描 `CONCAT(a, b)` 行，發現雖然是巨集，但在先前的參數展開過程中已經被設置為 `used`，不再遞歸展開，直接作為最終結果。

####範例 3

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

(#__codelineno-13-16)隨著 "IDENTITY" 開始展開，預處理器發現 "Token 2"（即為 arg0）是一個宏，因此先展開 CONCAT(C, ONCAT(a, b))。

* 展開 `arg0` 後獲得 `CONCAT(a, b)` （第 [23-54](#__codelineno-13-23)行）

`IDENTITY` 最終展開為 `IDENTITY_IMPL(CONCAT(a, b))`（第 [57](#__codelineno-13-57)行）

重新掃描，繼續展開 `IDENTITY_IMPL`（第 [61-72](#__codelineno-13-61)(#__codelineno-13-85)行）。

重新掃描結果，發現宏 `CONCAT(a, b)` 的狀態是 `used`，停止展開並得到最終的結果。

通過以上三個簡單的例子，我們可以大致理解預處理器展開巨集的過程，這裡不再深入探討預處理器，有興趣的話可以參照我提供的修改文件來研究。

##宏編程實現

以下開始進入主題（前面那一大段目的是為了更好地理解宏展開規則），宏編程實現。

####基本符號

首先可以先定義宏的特殊符號，做求值和拼接的時候會用到。

``` cpp
#define PP_LPAREN() (
#define PP_RPAREN() )
#define PP_COMMA() ,
#define PP_EMPTY()
#定義 PP_HASHHASH # ## #      // 表示 ## 字串，但只是作為字串，不會當作 ## 運算子來處理
```

####求值

利用參數優先展開的規則，可以撰寫一個求值巨集：

``` cpp
#define PP_IDENTITY(arg0) arg0

PP_COMMA PP_LPAREN() PP_RPAREN()                // -> PP_COMMA ( )
PP_IDENTITY(PP_COMMA PP_LPAREN() PP_RPAREN())   // -> PP_COMMA() -> ,
```

如果只寫 `PP_COMMA PP_LPAREN() PP_RPAREN()`，預處理器只會分別處理每個巨集，對展開的結果不會再合併處理。加上 `PP_IDENTITY` 之後，預處理器可以對展開得到的 `PP_COMMA()` 再進行求值，得到 `,`。


####拼接

由於 `##` 拼接時，不會展開左右兩邊的參數，為了讓參數可以先求值再拼接，可以這樣寫：

``` cpp
#define PP_CONCAT(arg0, arg1) PP_CONCAT_IMPL(arg0, arg1)
#define PP_CONCAT_IMPL(arg0, arg1) arg0 ## arg1

PP_CONCAT(PP_IDENTITY(1), PP_IDENTITY(2))         // -> 12
PP_CONCAT_IMPL(PP_IDENTITY(1), PP_IDENTITY(2))    // -> PP_IDENTITY(1)PP_IDENTITY(2) -> Error
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

使用 `PP_CONCAT` 先將 `PP_BOOL_` 與 `arg0` 拼接在一起，然後對拼接結果進行求值。這裡的 `arg0` 要求是求值之後得到 `[0, 256]` 範圍的數字，拼接在 `PP_BOOL_` 後面求值，就能得到布林值。與或非運算：

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

先用 `PP_BOOL` 對參數求值，之後再根據 `0 1` 的組合來拼接邏輯運算的結果。如果不用 `PP_BOOL` 來求值，那麼參數就只能支持 `0 1` 兩種數值，適用性大大降低。同理也可以寫出異或、或非等操作，有興趣的話可以自己嘗試。

####條件選擇

利用 `PP_BOOL` 和 `PP_CONCAT`，還可以撰寫條件選擇語句：

``` cpp
#define PP_IF(if, then, else) PP_CONCAT(PP_IF_, PP_BOOL(if))(then, else)
#define PP_IF_1(then, else) then
#define PP_IF_0(then, else) else

PP_IF(1, 2, 3)      // -> PP_IF_1(2, 3) -> 2
PP_IF(0, 2, 3)      // -> PP_IF_0(2, 3) -> 3
```

若`if`的值為`1`，則使用`PP_CONCAT`組合成`PP_IF_1`，最後展開為`then`的值；同樣地，如果`if`求值為`0`，則會得到`PP_IF_0`。

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

與 `PP_BOOL` 相似，整數的递增递减也是有範圍限制的，這裡範圍設定為 `[0, 256]`，递增到 `256` 之後，為了安全起見，`PP_INC_256` 會返回自身 `256` 作為邊界，同理 `PP_DEC_0` 也是返回 `0`。

####可變參數

宏可以接受不定长参数，格式如下：

```cpp
#define LOG(format, ...) printf("log: " format, __VA_ARGS__)

LOG("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG("Hello World") // -> printf("log: " "Hello World", ); 多了個逗號，編譯報錯
```

由於變長參數有可能為空，空的情況下會導致編譯失敗，因此 C++ 20 引入了 `__VA_OPT__`，如果變長參數是空，則返回空，否則返回原參數：

```cpp
#define LOG2(format, ...) printf("log: " format __VA_OPT__(,) __VA_ARGS__)

LOG2("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG2("Hello World")              // -> printf("log: " "Hello World" ); 沒有逗號，正常編譯
```

可惜的是，只有 C++ 20 或更高版本的標準才包含這個巨集，在後文中我們將提供 `__VA_OPT__` 的實作方法。

####惰性求值

考慮這種情況：

``` cpp
PP_IF(1, PP_COMMA(), PP_LPAREN())     // -> PP_IF_1(,,)) -> 报错 unterminated argument list invoking macro "PP_IF_1"
```

我們知道，當巨集展開時會對先參數進行求值。`PP_COMMA()` 和 `PP_LPAREN()` 求值之後再傳給 `PP_IF_1`，得到 `PP_IF_1(,,))`，導致預處理錯誤。此時，可以採用一種叫做惰性求值方法：

``` cpp
PP_IF(1, PP_COMMA, PP_LPAREN)()       // -> PP_IF_1(PP_COMMA, PP_LPAREN)() -> PP_COMMA() -> ,
```

將這樣寫，僅傳遞宏的名稱，讓 `PP_IF` 選出所需的宏名後，再與括號 `()` 結合為完整的宏，最終再展開。在宏編程中，惰性評估也是相當常見的。

####從括號開始

判斷可變長參數是否以括號開始：

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

`PP_IS_BEGIN_PARENS` 可以用來判斷傳入的參數是否以括號開始，在需要處理括號參數的時候會需要用到（譬如後面提到的 `__VA_OPT__` 實現）。看起來有點複雜，核心思想就是構建出一個巨集，若變長參數以括號開始，則可以跟括號連在一起求值得到一種結果，否則就另外求值得到另一種結果。讓我們來慢慢看：

以 `PP_IS_BEGIN_PARENS_PROCESS` 和 `PP_IS_BEGIN_PARENS_PROCESS_0` 所組成的巨集功能為先評估傳入的可變參數，接著取第 0 個參數。

`PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__)` 先對 `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` 進行求值，然後將該值與 `PP_IS_BEGIN_PARENS_PRE_` 結合在一起。

`PP_IS_BEGIN_PARENS_EAT(...)`宏會吞掉所有參數，返回1。如果在上一步`PP_IS_BEGIN_PARENS_EAT __VA_ARGS__`中，`__VA_ARGS__`是以括號開頭的，則會匹配到對`PP_IS_BEGIN_PARENS_EAT(...)`的求值，然後返回1；反之，如果不是以括號開頭，則沒有匹配上，`PP_IS_BEGIN_PARENS_EAT __VA_ARGS__`會保持不變。

若 `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` 求值得到 `1`，`PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, 1) -> PP_IS_BEGIN_PARENS_PRE_1 -> 1,`，注意 `1` 后面是有個逗號的，將 `1, ` 傳給 `PP_IS_BEGIN_PARENS_PROCESS_0`，取第 0 個參數，最後得到 `1`，表示參數是以括號開始。

若 `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` 求值得到不是 `1`，而是保持不變，則 `PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__) -> PP_IS_BEGIN_PARENS_PRE_PP_IS_BEGIN_PARENS_EAT __VA_ARGS__ -> 0, __VA_ARGS__`，傳給 `PP_IS_BEGIN_PARENS_PROCESS_0` 得到的是 `0`，表示參數不是以括號開始。

####可變參數空閒

判斷變長參數是否為空也是一個常用的巨集，在實現 `__VA_OPT__` 的時候需要用到，我們在這裡利用 `PP_IS_BEGIN_PARENS`，可以先寫出不完整的版本：

``` cpp
#define PP_IS_EMPTY_PROCESS(...) \
    PP_IS_BEGIN_PARENS(PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ())
#define PP_IS_EMPTY_PROCESS_EAT(...) ()

PP_IS_EMPTY_PROCESS()       // -> 1
PP_IS_EMPTY_PROCESS(1)      // -> 0
PP_IS_EMPTY_PROCESS(1, 2)   // -> 0
PP_IS_EMPTY_PROCESS(())     // -> 1
```

`PP_IS_EMPTY_PROCESS` 的功能是檢查 `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ()` 是否以括號開頭。

如果 `__VA_ARGS__` 是空，`PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ () -> PP_IS_EMPTY_PROCESS_EAT() -> ()`，得到的是一對括號 `()`，再傳給 `PP_IS_BEGIN_PARENS` 返回 `1`，表示參數是空。

否則，`PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ()`會保持不變地傳遞給`PP_IS_BEGIN_PARENS`，並返回 0，表示非空。

請注意第 4 個例子 `PP_IS_EMPTY_PROCESS(()) -> 1`，`PP_IS_EMPTY_PROCESS` 不能正確處理以括號開始的可變參數，這是因為當可變參數以括號開始時，括號會被 `PP_IS_EMPTY_PROCESS_EAT` 消耗導致評估結果為 `()`。為了解決這個問題，我們需要區分參數是否以括號開始的情況：

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

若 `PP_IS_EMPTY_IF` 回傳 `PP_IS_EMPTY_PROCESS`，最終由 `PP_IS_EMPTY_PROCESS` 來判斷變長參數是否非空。

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

`PP_ARGS_ELEM` 的第一個參數是元素下標 `I`，後面是變長參數。利用 `PP_CONCAT` 拼接 `PP_ARGS_ELEM_` 和 `I`，即可以得到返回相應位置元素的巨集 `PP_ARGS_ELEM_0..8`，再把變長參數傳給該巨集，展開返回下標對應位置的元素。

#### PP_IS_EMPTY2

利用 `PP_ARGS_ELEM` 也可以實現另一版本的 `PP_IS_EMPTY`：

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

利用 `PP_ARGS_ELEM` 來實現判斷參數是否包含逗號的 `PP_HAS_COMMA`。`PP_COMMA_ARGS` 會接收任意傳入的參數，並返回一個逗號。

判斷變長參數是否為空的基礎邏輯是 `PP_COMMA_ARGS __VA_ARGS__ ()` 返回一個逗號，也就是 `__VA_ARGS__` 為空，`PP_COMMA_ARGS` 和 `()` 拼接在一起求值，具體的寫法就是 `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ())`。

然而在某些情況下會有特例：

`__VA_ARGS__` itself may potentially bring commas;
`__VA_ARGS__()` 放在一起時，會產生逗號引起的求值。
`PP_COMMA_ARGS __VA_ARGS__` 組合在一起時會產生逗號的值求取；

針對上述提及的三種例外情況，需要進行排除，因此最終的寫法相當於對以下 4 個條件執行「與」邏輯：

* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__))` &&
* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__()))` &&
* `PP_NOT(PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__))` &&
* `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ())`

#### `__VA_OPT__`

透過 `PP_IS_EMPTY` 最終可以實現類似 `__VA_OPT__` 的巨集：

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

`PP_ARGS_OPT` 接受兩個固定參數和可變參數，若可變參數非空則返回 `data`，否則返回 `empty`。為了讓 `data` 和 `empty` 支援逗號，要求兩者都需以括號包覆實際參數，最後使用 `PP_REMOVE_PARENS` 來移除外層的括號。

憑借 `PP_ARGS_OPT` ，可以實現 `LOG3` 以模擬 `LOG2` 的功能：

``` cpp
#define LOG3(format, ...) \
    printf("log: " format PP_ARGS_OPT((,), (), __VA_ARGS__) __VA_ARGS__)

LOG3("Hello");                  // -> printf("log: " "Hello" );
LOG3("Hello %s", "World");      // -> printf("log: " "Hello %s" , "World");
```

`data_tuple` 是 `(,)`，如果變長參數非空，則會返回 `data_tuple` 裡面的所有元素，在這裡就是逗號 `,`。

####求參數個數

獲取可變長參數的個數：

``` cpp
#define PP_ARGS_SIZE_IMCOMPLETE(...) \
    PP_ARGS_ELEM(8, __VA_ARGS__, 8, 7, 6, 5, 4, 3, 2, 1, 0)

PP_ARGS_SIZE_IMCOMPLETE(a)             // -> 1
PP_ARGS_SIZE_IMCOMPLETE(a, b)          // -> 2
PP_ARGS_SIZE_IMCOMPLETE(PP_COMMA())    // -> 2
PP_ARGS_SIZE_IMCOMPLETE()              // -> 1
```

計算變長參數的個數，是通過數參數的位置來獲取的。`__VA_ARGS__` 會導致後續的參數全體往右移動，用宏 `PP_ARGS_ELEM` 來獲取第 8 個位置的參數，如果 `__VA_ARGS__` 只有一個參數，則第 8 個參數等於 `1`；同理如果 `__VA_ARGS__` 有兩個參數，則第 8 個參數就變為 `2`，剛好等於變長參數的個數。

這裡提供的範例只支持最多 8 個變長參數，這是基於 `PP_ARGS_ELEM` 能夠支持的最大長度。

這個宏還沒有完成，在變長參數為空的情況下，這個宏會錯誤地返回 `1`。如果需要處理空的變長參數，則需要使用我們之前提到的 `PP_ARGS_OPT` 宏：

``` cpp
#define PP_COMMA_IF_ARGS(...) PP_ARGS_OPT((,), (), __VA_ARGS__)
#define PP_ARGS_SIZE(...) PP_ARGS_ELEM(8, __VA_ARGS__ PP_COMMA_IF_ARGS(__VA_ARGS__) 8, 7, 6, 5, 4, 3, 2, 1, 0, 0, 0)

PP_ARGS_SIZE(a)             // -> 1
PP_ARGS_SIZE(a, b)          // -> 2
PP_ARGS_SIZE(PP_COMMA())    // -> 2
PP_ARGS_SIZE()              // -> 0
PP_ARGS_SIZE(,,,)           // -> 4
```

問題的關鍵就是逗號「`,`」在 `__VA_ARGS__` 為空的時候，把逗號隱去就能正確返回 `0`。

####遍歷訪問

類似C++的`for_each`，我們可以實現巨集的`PP_FOR_EACH`：

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

`PP_FOR_EACH` 接收兩個固定參數：`macro` 可以理解為在遍歷時呼叫的巨集，`contex` 可以作為固定值參數傳遞給 `macro`。`PP_FOR_EACH` 先通過 `PP_ARGS_SIZE` 獲取可變參數的長度 `N`，再用 `PP_CONCAT` 拼接得到 `PP_FOR_EACH_N`，之後 `PP_FOR_EACH_N` 會迭代呼叫 `PP_FOR_EACH_N-1` 來實現與可變參數數量相同的遍歷次數。

在這個例子中，我們宣告了 `DECLARE_EACH` 作為 `macro` 的參數，`DECLARE_EACH` 的功能是返回 `contex arg`，如果 `contex` 是類型名稱，`arg` 是變數名稱，`DECLARE_EACH` 就可以用來宣告變數。

####條件迴圈

有了 `FOR_EACH` 之後，我們還可以用類似的寫法寫出 `PP_WHILE`：

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

`PP_WHILE` 接受三個參數：`pred` 條件判斷函數，`op` 操作函數，`val` 初始值；循環的過程中不斷用 `pred(val)` 來做循環終止判斷，把 `op(val)` 得到的值傳給後續的宏，可以理解為執行以下代碼：

``` cpp
while (pred(val)) {
    val = op(val);
}
```

首先使用 `pred(val)` 得到條件判斷結果，將條件結果 `cond` 和其他參數再傳遞給 `PP_WHILE_N_IMPL`。
`PP_WHILE_N_IMPL` 可以分成兩個部分觀看：後半部分 `(pred, op, PP_IF(cond, op, PP_EMPTY_EAT)(val))` 被當作前半部分的參數，`PP_IF(cond, op, PP_EMPTY_EAT)(val)` 如果 `cond` 為真則求值 `op(val)`，否則求值 `PP_EMPTY_EAT(val)` 會得到空。前半部分 `PP_IF(cond, PP_WHILE_N+1, val PP_EMPTY_EAT)`，如果 `cond` 為真，則返回 `PP_WHILE_N+1`，並結合後半部分的參數繼續執行循環；否則返回 `val PP_EMPTY_EAT`，此時 `val` 就是最終的計算結果，而 `PP_EMPTY_EAT` 會吞掉後半部分的結果。

`SUM` 實現 `N + N-1 + ... + 1`。初始值 `(max_num, origin_num)`；`SUM_PRED` 取值的第一個元素 `x`，判斷是否大於 0；`SUM_OP` 對 `x` 執行遞減操作 `x = x - 1`，對 `y` 執行 `+ x` 操作 `y = y + x`。直接用 `SUM_PRED` 和 `SUM_OP` 傳給 `PP_WHILE`，返回的結果是一個元組，我們真正想要的結果是元組的第 2 個元素，於是再用 `SUM` 取第 2 個元素的值。

####遞迴重入

迄今為止，我們的遍歷訪問和條件循環都運作得很好，結果符合預期。還記得我們在講宏展開規則的時候提到的禁止遞歸重入嗎，當我們想要執行兩重循環的時候就不幸遇到到了禁止遞歸重入：

``` cpp
#define SUM_OP2(xy_tuple) SUM_OP_OP_IMPL2 xy_tuple
#define SUM_OP_OP_IMPL2(x, y) (PP_DEC(x), y + SUM(x, 0))

#define SUM2(max_num, origin_num) \
    PP_IDENTITY(SUM_IMPL PP_WHILE(SUM_PRED, SUM_OP2, (max_num, origin_num)))

SUM2(1, a)      // -> a + SUM_IMPL PP_WHILE_1(SUM_PRED, SUM_OP, (1, a))
```

將`SUM2`中的參數`op`改為`SUM_OP2`，`SUM_OP2`中述又會呼叫`SUM`，而`SUM`展開後將會是`PP_WHILE_1`，這相當於`PP_WHILE_1`遞迴地呼叫了它自己，預處理器展開停止。

為了解決這個問題，我們可以使用一種自動遞歸的方法（Automatic Recursion）：

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

`PP_AUTO_WHILE` 是 `PP_WHILE` 的自動推導遞歸版本，核心的巨集是 `PP_AUTO_REC(PP_WHILE_PRED)`，這個巨集可以找出當前可用的 `PP_WHILE_N` 版本的數字 `N`。

推導的原理很簡單，就是搜索所有版本，找出能夠正確展開的版本，返回該版本的數字，為了提升搜索的速度，一般的做法是使用二分查找，這就是 `PP_AUTO_REC` 在做的事情。`PP_AUTO_REC` 接受一個參數 `check`，`check` 負責檢查版本可用性，這裡給出的是支持搜索版本範圍 `[1, 4]`。`PP_AUTO_REC` 會首先檢查 `check(2)`，如果 `check(2)` 為真，則調用 `PP_AUTO_REC_12` 搜索範圍 `[1, 2]`，否則用 `PP_AUTO_REC_34` 搜索 `[3, 4]`。`PP_AUTO_REC_12` 檢查 `check(1)` 如果為真，說明版本 `1` 可用，否則用版本 `2`，`PP_AUTO_REC_34` 同理。

檢查 這裡的 `PP_WHILE_PRED` 要怎樣寫才能知道版本是否可用呢？在這裡，`PP_WHILE_PRED` 會展開成兩部分的拼接,接著再看後面的 `PP_WHILE_ ## n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`：如果 `PP_WHILE_ ## n` 可用, 由於 `PP_WHILE_FALSE` 固定返回 `0`, 這部分會展開得到 `val` 參數的值, 就是 `PP_WHILE_FALSE`; 否則這部分宏會保持不變, 依然是 `PP_WHILE_n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`。

將後半部份的結果與前半部份的 `PP_WHILE_CHECK_` 串接在一起，得到兩種結果：`PP_WHILE_CHECK_PP_WHILE_FALSE` 或者 `PP_WHILE_CHECK_PP_WHILE_n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`，因此我們讓 `PP_WHILE_CHECK_PP_WHILE_FALSE` 回傳 `1` 表示可用，`PP_WHILE_CHECK_PP_WHILE_n` 回傳 `0` 表示不可用。如此一來，我們成功完成自動推導遞迴的功能。

####算術比較

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

判斷數值是否相等時，利用了禁止遞迴重入的特性，將 `x` 和 `y` 遞迴拼接成 `PP_NOT_EQUAL_x PP_NOT_EQUAL_y` 巨集。若 `x == y`，則不會展開 `PP_NOT_EQUAL_y` 巨集，將其與 `PP_NOT_EQUAL_CHECK_` 拼接成 `PP_NOT_EQUAL_CHECK_PP_NOT_EQUAL_y` 並返回 `0`；反之，兩者均成功展開最終獲得 `PP_EQUAL_NIL`，拼接而成 `PP_NOT_EQUAL_CHECK_PP_EQUAL_NIL` 返回 `1`。

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

另外還包括大於、大於等於等算術比較，這裡就不再贅述。

####算術運算

透過 `PP_AUTO_WHILE`，我們可以實現基礎的算術運算，並支援巢狀運算。

Addition:

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

除法利用了 `PP_LESS_EQUAL`，只有 `y <= x` 的情況下才繼續循環。

####數據結構

宏也可以有資料結構，其實我們在前面的也稍微用到了一種資料結構 `tuple`，`PP_REMOVE_PARENS` 就是可以去掉 `tuple` 的外層括號，返回裡面的元素。我們這裡就以 `tuple` 為例子討論相關的實現，其他的資料結構 `list, array` 等有興趣可以去看 `Boost` 的實現。

"tuple" 定義為用括號包住的逗號分開的元素集合：`(a, b, c)`。 

``` cpp
#define PP_TUPLE_REMOVE_PARENS(tuple) PP_REMOVE_PARENS(tuple)

獲取指定索引的元素
#define PP_TUPLE_ELEM(i, tuple) PP_ARGS_ELEM(i, PP_TUPLE_REMOVE_PARENS(tuple))

吞掉整個 tuple 返回空
#define PP_TUPLE_EAT() PP_EMPTY_EAT

獲取大小
#define PP_TUPLE_SIZE(tuple) PP_ARGS_SIZE(PP_TUPLE_REMOVE_PARENS(tuple))

新增元素
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

##小結

(https://github.com/pfultz2/Cloak/wiki/C-Preprocessor-tricks,-tips,-and-idioms#deferred-expression)在BOOST_PP中的`REPEAT`相關巨集等等，對此有興趣的人可以自行查閱相關資料。

宏編程的除錯是一個痛苦的過程，我們可以：

使用 `-P -E` 選項輸出預處理結果；
使用我之前修改過的 `clang` 版本，仔細研究展開過程。
將複雜的巨集解構，查看中間巨集的展開結果；
遮蔽不相關的標頭檔案和巨集；
最後就是要腦補宏展開的過程了，熟悉宏展開之後調試的效率也會提升。

本文中的宏是我自己在理解了原理之後重新實現出來的，有部分宏借鑒了`Boost`的實現和引用裡面的文章，有任何錯誤之處，歡迎隨時指正，也歡迎找我來討論相關的問題。

這篇文章的程式碼都可在這裡找到：[下載](assets/img/2021-3-31-cpp-preprocess/macros.cpp)，[線上示範](https://godbolt.org/z/coWvc5Pse)抱歉，我無法翻譯這句話，因為它沒有內容。

##引用

* [Boost.Preprocessor](https://www.boost.org/doc/libs/1_75_0/libs/preprocessor/doc/)
(https://bot-man-jl.github.io/articles/?post=2020/Macro-Programming-Art)

--8<-- "footer_tc.md"


> 這篇文章是由ChatGPT翻譯的，如果有任何[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遗漏之处。 
