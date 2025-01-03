---
layout: post
title: C/C++ マクロプログラミング解析
categories:
- c++
catalog: true
tags:
- dev
description: 本文の目的は、C/C++のマクロプログラミングのルールと実装方法を明確に説明し、コード内のマクロを見ても恐れることがないようにすることです。
figures: []
---

<meta property="og:title" content="C/C++ 宏编程解析" />

本文の目的は、C/C++のマクロプログラミングのルールと実装方法を明確に説明し、コード内のマクロを恐れなくて済むようにすることです。まずは、C++標準14で述べられているマクロ展開のルールについて説明し、次にClangのソースコードを修正してマクロ展開を観察し、最後にこれらの知識を元にマクロプログラミングの実装について話し合います。

The entire code of the main text is right here: [Download](assets/img/2021-3-31-cpp-preprocess/macros.cpp)(https://godbolt.org/z/coWvc5Pse)申し訳ございませんが、そのテキストは翻訳できません。

##序文

`gcc -P -E a.cpp -o a.cpp.i` というコマンドを実行することで、コンパイラにファイル `a.cpp` のみ事前処理を行わせ、その結果を `a.cpp.i` に保存することができます。

最初に、いくつかの例を見てみましょう:

####再帰的再入（再起動性）

``` cpp
#define ITER(arg0, arg1) ITER(arg1, arg0)

ITER(1, 2)          // -> ITER(2, 1)
```

マクロ`ITER`が`arg0`と`arg1`の位置を交換しました。マクロが展開されると、`ITER(2, 1)`になります。

`arg0` `arg1` の位置が正常に交換されました。この部分でマクロは一度展開されましたが、その後は展開されず、再帰的に入れ子にはなりません。つまり、マクロの展開中に自身の再帰を行わないようになっており、再帰中に同じマクロが以前の再帰で展開されたことがある場合は再度展開されません。これがマクロ展開の重要なルールの一つです。再帰的に入れ子にならない理由は、無限の再帰を避けるためです。

####文字列の連結

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                // -> HelloWorld
CONCAT(Hello, CONCAT(World, !))     // ->　HelloCONCAT(World, !)
```

マクロ `CONCAT` は `arg0` と `arg1` を結合するためのものです。マクロが展開された後、`CONCAT(Hello, World)` は正しい結果 `HelloWorld` を得ることができます。しかし、`CONCAT(Hello, CONCAT(World, !))` は外側のマクロだけが展開され、内側の `CONCAT(World, !)` は展開されず、直接 `Hello` に連結されてしまいます。これは予想と異なる結果であり、本来望んでいたのは `HelloWorld!` です。これがマクロ展開のもう一つの重要なルールであり、`##` 演算子に続くマクロパラメータは展開されず、前の内容とまず連結されます。

上記の2つの例から、マクロの展開ルールには直感に反するものがいくつかあることがわかります。具体的なルールを把握していないと、思い描いている効果とは異なるマクロを書いてしまう可能性があります。

##規則の展開

引子の2つの例を通して、マクロ展開には標準のルールがあることが理解できます。このルールはC/C++標準に定義されており、内容はそれほど多くありません。何度か注意深く読むことをお勧めします。こちらにn4296標準のリンクも添付しております。マクロ展開に関するセクションは16.3です：[リンク](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4296.pdf)私はn4296バージョンからいくつかの重要な規則を選んでみました、これらの規則が正しくマクロを書く方法を決定します（標準のマクロを詳しく読む時間を取ることをお勧めします）。

####パラメーターの区切り

マクロのパラメータ要件はコンマで区切られ、パラメータの数はマクロの定義と一致する必要があります。マクロに渡されるパラメータの中で、括弧で囲まれた追加の内容は1つのパラメータと見なされます。パラメータは空白でも構いません。

``` cpp
#define ADD_COMMA(arg1, arg2) arg1, arg2

ADD_COMMA(a, b)             // -> a, b
ADD_COMMA(a)                // マクロ "MACRO" は2つの引数が必要ですが、1つしか指定されていません"
ADD_COMMA((a, b), c)        // -> (a, b), c
ADD_COMMA(, b)              // -> , b
```

`ADD_COMMA((a, b), c)` では`(a, b)`が最初の引数と見なされます。`ADD_COMMA(, b)` では、最初の引数が空なので、`, b`に展開されます。

####広パラメータ展開

マクロを展開する際、マクロの引数も展開可能なマクロである場合、まず引数を完全に展開してからマクロを展開します。例えば、

``` cpp
ADD_COMMA(ADD_COMMA(1, 2), ADD_COMMA(3, 4))     // -> 1, 2, 3, 4
```

通常、マクロ展開は、パラメーターを最初に評価してからマクロを評価すると考えられていますが、`#`や`##`演算子に出会うと進め方が変わります。

####`#` 操作子

操作符後面跟的巨集參數，不會進行展開，會直接字串化，例如：

``` cpp
#define STRINGIZE(arg0) # arg0

STRINGIZE(a)                // -> "a"
STRINGIZE(STRINGIZE(a))     // -> "STRINGIZE(a)"
```

この規則 `STRINGIZE(STRINGIZE(a))` によると、展開結果は`"STRINGIZE(a)"`だけです。

####`##` 操作子

`##` 演算子の前後にあるマクロの引数は展開されません、まずは直接連結されます。例えば：

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                        // -> HelloWorld
CONCAT(Hello, CONCAT(World, !))             // -> HelloCONCAT(World, !)
CONCAT(CONCAT(Hello, World) C, ONCAT(!))    // -> CONCAT(Hello, World) CONCAT(!)
```

`CONCAT(CONCAT(Hello, World) C, ONCAT(!))` というテキストを日本語に翻訳すると、`CONCAT(Hello, World) CONCAT(!)` という正しい連結内容が得られます。

####繰り返しスキャン

プリプロセッサーは、一度マクロ展開を行った後、取得した内容を再スキャンして展開を継続し、展開できる内容がなくなるまで行います。

一次宏展開は、パラメータを完全に展開してから（`#`と`##`に出会うまで）、マクロの定義に従って、マクロと完全に展開されたパラメータを定義に従って置き換えし、定義のすべての `#` と `##`演算子を処理することを意味します。

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define STRINGIZE(arg0) # arg0

CONCAT(STRING, IZE(Hello))        // -> STRINGIZE(Hello) -> "Hello"
```

`CONCAT(STRING, IZE(Hello))` is first scanned and expanded to `STRINGIZE(Hello)`, then in the second scan, it is discovered that `STRINGIZE` can be further expanded, resulting in `"Hello"`.

####再帰呼び出しを禁止します。

再帰的マクロ展開を繰り返すプロセス中では、同じマクロを展開することは禁止されています。マクロの展開は木構造として理解できます。ルートノードは最初に展開するマクロであり、各マクロの展開後のコンテンツはそのマクロの子ノードとしてツリーに接続されます。したがって、再帰を禁止するとは、子ノードのマクロを展開する際に、そのマクロが任意の祖先ノードのマクロと同じである場合は展開を禁止することです。いくつかの例を見てみましょう：

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define CONCAT_SPACE(arg0, arg1) arg0 arg1
#define IDENTITY(arg0) IDENTITY_IMPL(arg0)
#define IDENTITY_IMPL(arg0) arg0

CONCAT(CON, CAT(a, b))                  // -> CONCAT(a, b)
IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))   // -> CONCAT(a, b)
IDENTITY(CONCAT(CON, CAT(a, b)))        // -> IDENTITY_IMPL(CONCAT(a, b)) -> CONCAT(a, b)
```

`CONCAT(CON, CAT(a, b))`: `CONCAT` は2つのパラメータを `##` で連結するものなので、`##` のルールによりパラメータは展開されず、直接連結されます。したがって、最初の展開では`CONCAT(a, b)`が得られます。`CONCAT` はすでに展開されているので再帰的展開は停止します。

`IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))`: `IDENTITY_IMPL` can be understood as evaluating argument `arg0`, where argument `arg0` evaluates to `CONCAT(a, b)`. Due to being marked as not allowing re-entry recursively, `IDENTITY_IMPL` finishes expanding. During the second scan, it is noticed that the `CONCAT(a, b)` is marked as not allowing re-entry, so the expansion stops. Here, `CONCAT(a, b)` is obtained by expanding argument `arg0`, but during subsequent expansions, it maintains the mark of not allowing re-entry, which can be understood as the parent node being argument `arg0`, consistently holding the mark of not allowing re-entry.

`IDENTITY(CONCAT(CON, CAT(a, b)))`：この例は親子ノードの理解を強化するために使用されます。引数を展開する際、自身が親ノードとして、展開された内容が子ノードとして再帰的に評価されます。展開された引数がマクロ定義に渡されると、再帰を禁止するマークが引き続き適用されます（引数がマクロ定義内で変更されない場合）。引数の展開プロセスは別の木と見なすことができ、展開された結果は木の最下層の子ノードとなります。この子ノードはマクロに渡され、展開された際に再帰を禁止する特性が依然として維持されます。

例えばここでは、初めて完全に展開された後に `IDENTITY_IMPL(CONCAT(a, b))` が得られます。`CONCAT(a, b)` は再入不可とマークされており、`IDENTITY_IMPL` が引数を評価する場合でも、引数は展開が禁止されているため、引数が定義にそのまま渡されます。最終的には `CONCAT(a, b)` が得られます。

上記の内容は、私が重要だと思うものや理解しづらいと感じる規則をいくつか挙げただけです。詳細な展開規則については、標準文書を直接参照することをお勧めします。

##Clangを使用して展開プロセスを観察する

Clangのソースコードにいくつかのプリント情報を追加してマクロ展開の過程を観察することができます。私はClangのソースコードを詳しく説明するつもりはありません。興味のある方は、こちらの修正済みのファイルのdiffを使って、Clangをコンパイルして研究してみてください。こちらでは、llvmバージョン11.1.0を使用しています。（[リンク](https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-11.1.0.tar.gz)修正されたファイル（[こちら](assets/img/2021-3-31-cpp-preprocess/clang-modify.zip)以下通过示例简要验证我们之前介绍的宏展开规则：

####I'm sorry, but I can't provide a translation without any content to work with. Could you please provide more information or context for the text you'd like me to translate?

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(C, ONCAT(a, b))      // CONCAT(a, b)
```

上記のコードをプリプロセスするために調整された Clang を使用します： `clang -P -E a.cpp -o a.cpp.i`。以下の出力が得られます：

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

第 [1](#__codelineno-9-1)(#__codelineno-9-2)「マクロは展開できる」、「EnterMacro」に入る。

マクロ展開を実行する本当の関数は `ExpandFunctionArguments` であり、その後に再度展開するマクロ情報をプリントします。この時点で、マクロが `used` としてマークされていることに注意してください（第 [9](#__codelineno-9-9)その後、マクロの定義に従って、1つずつの`Token`を展開します（`Token`は`Clang`のプリプロセッサ内で使用される概念ですが、ここでは詳細な説明は省略します）。

(#__codelineno-9-11)公式な契約の内容は未定（行）。

第1个 `Token` 是 `hashhash`，也就是 `##` 操作符，继续复制到结果上（第[14-15](#__codelineno-9-14)行）。

(#__codelineno-9-16)行）。

最後、`Leave ExpandFunctionArguments` は、このスキャンで展開された結果を出力します（[19](#__codelineno-9-19)（行），結果の `Token` はすべて `C ## ONCAT(a, b)` に翻訳され、その後プリプロセッサは `##` 演算子を実行して新しい内容を生成します。

`##` を実行した後、`CONCAT(a, b)` が得られ、マクロ `CONCAT` に遭遇した場合、プリプロセッサは先に `HandleIdentifier` に入って、マクロの情報を表示します。そのマクロの状態が `disable used` であり、すでに展開されたので再入することは禁止され、`Macro is not ok to expand` と表示され、プリプロセッサは展開を続けず、最終的には `CONCAT(a, b)` が得られます。

####サンプル2

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define IDENTITY(arg0) arg0

IDENTITY(CONCAT(C, ONCAT(a, b)))
```

<details>
<summary> <font> Clang printing information (click to expand): </font> </summary>
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

(#__codelineno-11-12)`IDENTITY`を展開し始めると、パラメータ`Token 0`が`CONCAT(...)`であることがわかります。これはマクロでもありますので、まずこのパラメータを評価します。

(#__codelineno-11-27)`CONCAT(...)` マクロのパラメーター展開が開始され、例 1 と同様に、複数回のスキャン展開後に `CONCAT(a, b)` が得られます。 （[46](#__codelineno-11-46)Translate these text into Japanese language:

行）。

第 [47](#__codelineno-11-47)'IDENTITY' の展開を終了し、結果は `CONCAT(a, b)` です。

(#__codelineno-11-51)再度 `CONCAT(a, b)` をスキャンしたところ、これはマクロではあるが、以前のパラメータ展開プロセスで `used` として設定されており、再帰展開は行われず、直接最終結果として扱われることが分かりました。

####例子3

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define IDENTITY_IMPL(arg0) arg0
#define IDENTITY(arg0) IDENTITY_IMPL(arg0)

IDENTITY(CONCAT(C, ONCAT(a, b)))
```

<details>
<summary> <font>Clang プリント情報（クリックして展開）：</font> </summary>
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

第 [16](#__codelineno-13-16)`IDENTITY` を展開するために行が始まり、プリプロセッサは `Token 2`（つまり `arg0`）がマクロであることを認識し、`CONCAT(C, ONCAT(a, b))`を最初に展開します。

`arg0` を展開すると、`CONCAT(a, b)` が得られます（[23-54](#__codelineno-13-23)行）

(#__codelineno-13-57)「行」

再度スキャンして、`IDENTITY_IMPL`（第 [61-72](#__codelineno-13-61)これらのテキストを日本語に翻訳します:

行），発見された`Token 0`はマクロ`CONCAT(a, b)`であることがわかりますが、`used`状態にあるため、展開を中止して（75-84行目）、最終的な結果はやはり`CONCAT(a, b)`になります（[85](#__codelineno-13-85)行）。

再スキャンした結果、マクロ `CONCAT(a, b)` の状態が `used` であることが分かり、展開を停止して最終結果を得ました。

上記の3つの簡単な例を通じて、私たちはおおまかにプリプロセッサがマクロを展開するプロセスを理解できます。ここでは、プリプロセッサについてさらに掘り下げることはしません。興味のある方は、私が提供した修正ファイルを参照して研究してみてください。

##広いプログラミングの実現

以下、我々はテーマに入っていきます（前述の大きなセグメントは、マクロ展開ルールをよりよく理解するためのものでした）、マクロプログラミングの実施。

####基本符号

まず、マクロの特別なシンボルを定義できます。評価や連結を行う際に使用されます。

``` cpp
#define PP_LPAREN() (
#define PP_RPAREN() )
#define PP_COMMA() ,
#define PP_EMPTY()
#PP_HASHHASHを# ## #と定義する。
// 表示 ## 文字列，但只是作为字符串，不会当作 ## 操作符来处理
```

####評価

利用パラメータを優先的に展開するルールに基づいて、値を計算するマクロを記述することができます：

``` cpp
#define PP_IDENTITY(arg0) arg0

PP_COMMA PP_LPAREN() PP_RPAREN()                // -> PP_COMMA ( )
PP_IDENTITY(PP_COMMA PP_LPAREN() PP_RPAREN())   // -> PP_COMMA() -> ,
```

`PP_COMMA PP_LPAREN() PP_RPAREN()` と書くだけだと、プリプロセッサは各マクロを個別に処理し、展開した結果を再度結合することはしません。`PP_IDENTITY` を追加すると、プリプロセッサは展開した `PP_COMMA()` に対して評価を行い、`,` を得ることができます。


####接合

`##` を連結する際、左右の引数を展開しないため、引数を先に評価してから連結するには、次のように書くことができます：

``` cpp
#define PP_CONCAT(arg0, arg1) PP_CONCAT_IMPL(arg0, arg1)
#define PP_CONCAT_IMPL(arg0, arg1) arg0 ## arg1

PP_CONCAT(PP_IDENTITY(1), PP_IDENTITY(2))         // -> 12
PP_CONCAT_IMPL(PP_IDENTITY(1), PP_IDENTITY(2))    // -> PP_IDENTITY(1)PP_IDENTITY(2) -> Error
```

`PP_CONCAT` で使用されるメソッドは遅延結合と呼ばれ、`PP_CONCAT_IMPL` に展開される際、`arg0`と`arg1`は、最初に展開および評価され、その後に`PP_CONCAT_IMPL`が実際の結合操作を実行します。

####論理演算

`PP_CONCAT` を使えば論理演算ができます。まず、`BOOL` 値を定義します：


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

`PP_CONCAT` マクロは、まず`PP_BOOL_`と`arg0`を連結し、その結果を評価します。ここでの`arg0`は、評価後に `[0, 256]` の範囲内の数値を取得する必要があります。`PP_BOOL_` に続けて評価を行うことで、ブール値が得られます。論理演算子 AND、OR、NOT：

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

`PP_BOOL` を使ってパラメーターを評価し、その後に `0 1` の組み合わせに基づいて論理演算の結果を組み立てます。もし `PP_BOOL` を使用しないと、パラメーターは `0 1` の2つの数字しかサポートしないため、使用範囲が大幅に制限されます。同様に、排他的論理和や否定論理和などの操作も書けますので、興味があれば是非試してみてください。

####条件选择

`PP_BOOL` および `PP_CONCAT` を利用して、条件分岐文を記述することもできます。

``` cpp
#define PP_IF(if, then, else) PP_CONCAT(PP_IF_, PP_BOOL(if))(then, else)
#define PP_IF_1(then, else) then
#define PP_IF_0(then, else) else

PP_IF(1, 2, 3)      // -> PP_IF_1(2, 3) -> 2
PP_IF(0, 2, 3)      // -> PP_IF_0(2, 3) -> 3
```

「if」が評価され、結果が「1」である場合には、「PP_CONCAT」で「PP_IF_1」に結合し、最終的に「then」の値に展開します。同様に、もし「if」が「0」と評価された場合は、「PP_IF_0」となります。

####増加減少

整数递增递减： -> 整数の増加および減少：

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

`PP_BOOL` に類似して、整数の増減にも制限があります。ここでは範囲が `[0, 256]` に設定されており、`256` に増加すると、安全のために`PP_INC_256` は自体の `256` を範囲として返します。同様に、`PP_DEC_0` も `0` を返します。

####可変長パラメータ

宏は可変長引数を受け入れることができます。フォーマットは以下の通りです：

```cpp
#define LOG(format, ...) printf("log: " format, __VA_ARGS__)

LOG("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG("Hello World")              // -> printf("log: " "Hello World", ); Extra comma added, causing a compilation error.
```

可変長引数が空の可能性があるため、空の場合にコンパイルエラーが発生する可能性があるため、C++ 20では`__VA_OPT__`が導入されました。可変長引数が空の場合は空を返し、それ以外の場合は元の引数を返します。

```cpp
#define LOG2(format, ...) printf("log: " format __VA_OPT__(,) __VA_ARGS__)

LOG2("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG2("Hello World") // -> printf("log: " "Hello World" ); There is no comma, compiles normally
```

ただ、残念ながら、このマクロはC++ 20以降の標準でのみ利用可能です。以下では、`__VA_OPT__`の実装方法を説明します。

####There is nothing to translate.

この状況を考慮してください：

``` cpp
PP_IF(1, PP_COMMA(), PP_LPAREN())     // -> PP_IF_1(,,)) -> "PP_IF_1" マクロを呼び出す際の引数リストが終了していないため、エラーが発生します".
```

我々は、マクロ展開される際に最初の引数が評価されることを知っています。`PP_COMMA()`および`PP_LPAREN()`が評価された後、`PP_IF_1`に渡され、`PP_IF_1(,,))`が得られ、プリプロセスエラーが発生します。この場合、遅延評価と呼ばれるメソッドを使用することができます：

``` cpp
PP_IF(1, PP_COMMA, PP_LPAREN)()       // -> PP_IF_1(PP_COMMA, PP_LPAREN)() -> PP_COMMA() -> ,
```

この方法で修正すると、単にマクロの名前を渡して、`PP_IF` が必要なマクロ名を選択し、それを括弧 `()` と一緒に連結して完成したマクロを作成し、最後に展開します。 
マクロプログラミングでは、遅延評価も非常に一般的です。

####かぎかっこで始まります

長さ可変引数がかっこで始まっているかどうかを判断します：

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

'PP_IS_BEGIN_PARENS' は、渡された引数が括弧で始まるかどうかを判断するために使用できます。括弧で始まる引数を処理する必要がある場合には、後述する `__VA_OPT__` 実装で使用されます。見た目はやや複雑ですが、核心的な考え方は、マクロを構築して、可変長引数が括弧で始まる場合には括弧と連結して評価し、結果を得ることが可能であり、そうでない場合には別の結果を得ることができます。詳しく見てみましょう：

`PP_IS_BEGIN_PARENS_PROCESS` and `PP_IS_BEGIN_PARENS_PROCESS_0` macros are designed to first evaluate the incoming variable arguments, and then retrieve the 0th argument.

`PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__)`は、`PP_IS_BEGIN_PARENS_EAT __VA_ARGS__`を評価し、評価結果を`PP_IS_BEGIN_PARENS_PRE_`と結合する。

`PP_IS_BEGIN_PARENS_EAT(...)` マクロは全ての引数を吸収し、1を返します。もし一つ前の `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` の中で、`__VA_ARGS__` が括弧で始まっていたら、`PP_IS_BEGIN_PARENS_EAT(...)` の評価にマッチし、1を返します。逆に、括弧で始まっていない場合はマッチしないので、`PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` は変わらずに残ります。

`PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` の評価結果は `1` 、 `PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, 1) -> PP_IS_BEGIN_PARENS_PRE_1 -> 1,` に注意し、 `1` の後にコンマがあることに注意して `1, ` を `PP_IS_BEGIN_PARENS_PROCESS_0` に渡し、0 番目の引数を取得すると最終的に `1` という結果が得られ、これは引数が括弧で始まることを示しています。

`PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` が `1` でなく変わらない場合、`PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__) -> PP_IS_BEGIN_PARENS_PRE_PP_IS_BEGIN_PARENS_EAT __VA_ARGS__ -> 0, __VA_ARGS__` を使って `PP_IS_BEGIN_PARENS_PROCESS_0` に渡すと、`0` が得られ、引数が括弧で始まっていないことを示します。

####可変長パラメータ空

可変長引数が空かどうかを判断するのはよく使われるマクロです。`__VA_OPT__`を実装する際に必要とされます。ここでは、`PP_IS_BEGIN_PARENS`を利用して、不完全なバージョンを書いてみましょう：

``` cpp
#define PP_IS_EMPTY_PROCESS(...) \
    PP_IS_BEGIN_PARENS(PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ())
#define PP_IS_EMPTY_PROCESS_EAT(...) ()

PP_IS_EMPTY_PROCESS()       // -> 1
PP_IS_EMPTY_PROCESS(1)      // -> 0
PP_IS_EMPTY_PROCESS(1, 2)   // -> 0
PP_IS_EMPTY_PROCESS(())     // -> 1
```

`PP_IS_EMPTY_PROCESS` の機能は、`PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__()` が括弧で始まるかどうかを判断することです。

もし `__VA_ARGS__` が空であれば、`PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ () -> PP_IS_EMPTY_PROCESS_EAT() -> ()` のように、`()` という括弧のペアが返され、それが `PP_IS_BEGIN_PARENS` に渡されて `1` が返ってきます。これは引数が空であることを示しています。

その場合、`PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ()`は変更せずに`PP_IS_BEGIN_PARENS`に渡し、0を返して空でないことを示します。

例えば、第4の例`PP_IS_EMPTY_PROCESS(()) -> 1`について、`PP_IS_EMPTY_PROCESS`は、かぎかっこ `(` で始まる可変引数を適切に処理できません。なぜなら、この場合、かぎかっこの影響で可変引数が`PP_IS_EMPTY_PROCESS_EAT`にマッチし、結果的に`()`となってしまうためです。この問題を解決するために、かぎかっこで始まるか否かで引数を別々に扱う必要があります：

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

`PP_IS_EMPTY_IF` は、`if` 条件に基づいて、0番目または1番目の引数を返します。

もし可変長パラメータが括弧で始まる場合、`PP_IS_EMPTY_IF` は `PP_IS_EMPTY_ZERO` を返し、最終的には `0` を返して、可変長パラメータが空でないことを示す。

これらのテキストを日本語に翻訳してください:

反之 `PP_IS_EMPTY_IF` 返回 `PP_IS_EMPTY_PROCESS`，最后由 `PP_IS_EMPTY_PROCESS` 来判断变长参数是否非空。

####インデックスアクセス

指定された位置の可変長引数の要素を取得する:

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

`PP_ARGS_ELEM` の最初の引数は要素のインデックス `I` であり、その後は可変引数です。`PP_CONCAT` を使用して `PP_ARGS_ELEM_` と `I` を連結することで、該当する位置の要素を返すマクロ `PP_ARGS_ELEM_0..8` が得られます。そのマクロに可変引数を渡し、インデックスに対応する位置の要素を展開します。

#### PP_IS_EMPTY2

`PP_ARGS_ELEM` を使用すると、別バージョンの `PP_IS_EMPTY` を実現することもできます：

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

`PP_ARGS_ELEM` を借りて、パラメータにコンマが含まれているかどうかを判定する `PP_HAS_COMMA` を実装します。 `PP_COMMA_ARGS` は与えられた任意の引数を取り込み、コンマを返します。

可変長引数が空かどうかを判断する基本的なロジックは、「PP_COMMA_ARGS __VA_ARGS__()」がコンマを返すことです。つまり、「__VA_ARGS__」が空の場合、「PP_COMMA_ARGS」と「()」が連結されて評価されます。具体的な書き方は、「PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__())」です。

ただし、例外が発生する可能性もあります：

`__VA_ARGS__` itself may introduce commas;
`__VA_ARGS__()` は、一緒に連結されて評価され、コンマが発生します。
`PP_COMMA_ARGS __VA_ARGS__` マクロを結合すると、カンマが評価されます。

前述三つの例外に対処するため、最終的な記述は以下の4つの条件に対して論理積を実行していると見なすことができます：

* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__))` &&
* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__()))` &&
* `PP_NOT(PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__))` &&
* `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ())`

#### `__VA_OPT__`

`PP_IS_EMPTY`を使用すると、`__VA_OPT__`のようなマクロを実現できるようになります。

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

`PP_ARGS_OPT`関数は、2つの固定引数と可変引数を受け入れ、可変引数が空でない場合は`data`を返し、空の場合は`empty`を返します。 `data`と`empty`にカンマをサポートさせるために、実際の引数を両方とも括弧で囲み、最後に`PP_REMOVE_PARENS`を使用して外側の括弧を削除します。

`PP_ARGS_OPT` を使用すると、`LOG3` が `LOG2` の機能を模倣できます：

``` cpp
#define LOG3(format, ...) \
    printf("log: " format PP_ARGS_OPT((,), (), __VA_ARGS__) __VA_ARGS__)

LOG3("Hello");                  // -> printf("log: " "Hello" );
LOG3("Hello %s", "World");      // -> printf("log: " "Hello %s" , "World");
```

`data_tuple`は`(,)`であり、可変長引数が空でない場合、`data_tuple`のすべての要素が返されます。ここでは、カンマ`,`です。

####パラメータの数を求める

可変長引数の数を取得します：

``` cpp
#define PP_ARGS_SIZE_IMCOMPLETE(...) \
    PP_ARGS_ELEM(8, __VA_ARGS__, 8, 7, 6, 5, 4, 3, 2, 1, 0)

PP_ARGS_SIZE_IMCOMPLETE(a)             // -> 1
PP_ARGS_SIZE_IMCOMPLETE(a, b)          // -> 2
PP_ARGS_SIZE_IMCOMPLETE(PP_COMMA())    // -> 2
PP_ARGS_SIZE_IMCOMPLETE()              // -> 1
```

可変引数の数を計算するには、引数の位置を数えることで行います。`__VA_ARGS__` を使用すると、後続の引数がすべて右に移動し、マクロ `PP_ARGS_ELEM` を使って8番目の引数を取得します。もし`__VA_ARGS__` に1つの引数しかない場合、8番目の引数は`1`に等しくなります。同様に、`__VA_ARGS__` に2つの引数がある場合、8番目の引数は`2`になり、ちょうど可変引数の個数と一致します。

ここでは、与えられた例は、8つの最高サポート数を持つ可変引数に依存しています。これは、`PP_ARGS_ELEM` がサポートする最大長に依存しています。

ただし、このマクロはまだ完全ではありません。可変長パラメータが空の場合、このマクロは誤って `1` を返します。空の可変長パラメータを処理する必要がある場合は、前述の `PP_ARGS_OPT` マクロが必要です。

``` cpp
#define PP_COMMA_IF_ARGS(...) PP_ARGS_OPT((,), (), __VA_ARGS__)
#define PP_ARGS_SIZE(...) PP_ARGS_ELEM(8, __VA_ARGS__ PP_COMMA_IF_ARGS(__VA_ARGS__) 8, 7, 6, 5, 4, 3, 2, 1, 0, 0, 0)

PP_ARGS_SIZE(a)             // -> 1
PP_ARGS_SIZE(a, b)          // -> 2
PP_ARGS_SIZE(PP_COMMA())    // -> 2
PP_ARGS_SIZE()              // -> 0
PP_ARGS_SIZE(,,,)           // -> 4
```

重点在于逗号 `,`，当`__VA_ARGS__`为空时，去掉逗号就可以正确返回`0`。

####遍歴訪問

C++ の `for_each` に似たものとして、マクロの `PP_FOR_EACH` を実装することができます。

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

`PP_FOR_EACH` は2つの固定パラメータを受け取ります：`macro` は繰り返し時に呼び出されるマクロと解釈できます。`contex` は`macro` に渡される固定値パラメータとして機能します。`PP_FOR_EACH` はまず`PP_ARGS_SIZE` を使用して可変長パラメータの長さ `N` を取得し、次に`PP_CONCAT` を使用して`PP_FOR_EACH_N` を生成します。その後`PP_FOR_EACH_N` は、可変長パラメータの個数と同じ数の反復処理を実現するために、`PP_FOR_EACH_N-1` を反復的に呼び出します。

例において、私たちはマクロのパラメーターとして `DECLARE_EACH` を宣言しました。`DECLARE_EACH` の役割は `contex arg` を返すことです。ここで、`contex` が型の名前であり、`arg` が変数の名前である場合、`DECLARE_EACH` は変数を宣言するために使用できます。

####条件循环

`FOR_EACH` を使用した後、同様の書き方で `PP_WHILE` を記述することもできます。

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

`PP_WHILE` 関数は3つのパラメーターを受け取ります：`pred` 条件判定関数、`op` 操作関数、`val` 初期値；ループ中に繰り返し `pred(val)` を使用してループを終了判定し、`op(val)` の結果を後続のマクロに渡し、以下のコードを実行します：

``` cpp
while (pred(val)) {
    val = op(val);
}
```

`PP_WHILE_N` は最初に `pred(val)` を使用して条件判断結果を取得し、その結果 `cond` と残りのパラメータを `PP_WHILE_N_IMPL` に再度渡します。
`PP_WHILE_N_IMPL` は2つの部分に分けることができる：後半部分 `(pred, op, PP_IF(cond, op, PP_EMPTY_EAT)(val))` は前半部分の引数として使用され、`PP_IF(cond, op, PP_EMPTY_EAT)(val)` は `cond` が真である場合に `op(val)` を評価し、それ以外の場合には空の結果を得ます。前半部分は `PP_IF(cond, PP_WHILE_N+1, val PP_EMPTY_EAT)` であり、`cond` が真である場合には `PP_WHILE_N+1` を返し、後半部分の引数と組み合わせてループを継続します。そうでない場合には `val PP_EMPTY_EAT` を返し、この時点で `val` が最終的な計算結果となり、`PP_EMPTY_EAT` が後半部分の結果を吸収します。

`SUM`関数は `N + N-1 + ... + 1`を実現します。初期値は `(max_num, origin_num)` であり、`SUM_PRED`関数は取得された最初の要素 `x` が0より大きいかどうかを判定します。`SUM_OP`関数は、`x`に対して `x = x - 1` の操作を行い、`y`には `+ x` の操作 `y = y + x` を実行します。`SUM_PRED`と`SUM_OP`を直接 `PP_WHILE`に渡し、返された結果はタプルです。我々が実際に必要なのはそのタプルの第2要素であるため、再度 `SUM`関数を用いて第2要素の値を取得します。

####再帰的な再入り

これまでに、当社の繰り返し訪問と条件付きループは非常に順調に機能し、期待通りの結果をもたらしています。マクロ展開規則についてお話しする際に再帰的な再入を禁止することを言及しましたが、2重ループを実行しようとしたときに再帰的な再入を禁止する問題が発生しました。

``` cpp
#define SUM_OP2(xy_tuple) SUM_OP_OP_IMPL2 xy_tuple
#define SUM_OP_OP_IMPL2(x, y) (PP_DEC(x), y + SUM(x, 0))

#define SUM2(max_num, origin_num) \
    PP_IDENTITY(SUM_IMPL PP_WHILE(SUM_PRED, SUM_OP2, (max_num, origin_num)))

SUM2(1, a)      // -> a + SUM_IMPL PP_WHILE_1(SUM_PRED, SUM_OP, (1, a))
```

`SUM2` のパラメータ `op` を `SUM_OP2` に変更し、`SUM_OP2` では `SUM` が呼び出され、`SUM` は `PP_WHILE_1` に展開され、`PP_WHILE_1` が自身を再帰的に呼び出すことになり、プリプロセッサは展開を停止します。

この問題を解決するためには、自動再帰法（Automatic Recursion）を使用することができます：

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

`PP_AUTO_WHILE` は、`PP_WHILE` の自動推論再帰バージョンであり、中核となるマクロは `PP_AUTO_REC(PP_WHILE_PRED)` です。このマクロは、現在利用可能な `PP_WHILE_N` バージョンの数字 `N` を見つけることができます。

推論の原則は非常に簡単で、すべてのバージョンを検索し、正しく展開できるバージョンを見つけ、そのバージョンの番号を返すことです。検索速度を向上させるため、通常はバイナリ検索を使用します。これが `PP_AUTO_REC` が行っていることです。`PP_AUTO_REC` は `check` というパラメータを受け入れます。`check` はバージョンの可用性を確認します。ここでは、サポートされる検索バージョン範囲 `[1, 4]` が指定されています。`PP_AUTO_REC` はまず `check(2)` をチェックします。もし `check(2)` が真ならば、`PP_AUTO_REC_12` を呼び出して範囲 `[1, 2]` を検索し、そうでなければ `PP_AUTO_REC_34` で `[3, 4]` を検索します。`PP_AUTO_REC_12` は `check(1)` を調べます。真であれば、バージョン `1` が利用可能であることを意味し、そうでなければバージョン `2` を使用します。`PP_AUTO_REC_34` も同様に行います。

「check」は、どのように書かれるとバージョンが利用可能かどうかがわかりますか？ ここでは、「PP_WHILE_PRED」は2つの部分に展開されます。 後半部分「PP_WHILE_## n（PP_WHILE_FALSE、PP_WHILE_FALSE、PP_WHILE_FALSE）」を見てみましょう：もし「PP_WHILE_## n」が利用可能な場合、PP_WHILE_FALSEが常に「0」を返すため、この部分は「val」パラメーターの値、つまり「PP_WHILE_FALSE」に展開されます。 それ以外の場合、この部分のマクロは変わらず、「PP_WHILE_n（PP_WHILE_FALSE、PP_WHILE_FALSE、PP_WHILE_FALSE）」のままです。

後部分の結果を前部分の `PP_WHILE_CHECK_` に連結して、2つの結果が得られます：`PP_WHILE_CHECK_PP_WHILE_FALSE` または `PP_WHILE_CHECK_PP_WHILE_n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`。それで、`PP_WHILE_CHECK_PP_WHILE_FALSE` が `1` を返すことで有効であることを示し、`PP_WHILE_CHECK_PP_WHILE_n` が `0` を返すことで無効であることを示します。これにより、再帰的な機能の自動推論が完了します。

####算術比較

不等:

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

数値を比較して、再帰を禁止する特性を使用しています。 `x` と `y` を再帰的に組み合わせて `PP_NOT_EQUAL_x PP_NOT_EQUAL_y` マクロにします。 `x == y` であれば、 `PP_NOT_EQUAL_y` マクロは展開されず、`PP_NOT_EQUAL_CHECK_` と組み合わされて `PP_NOT_EQUAL_CHECK_PP_NOT_EQUAL_y` が `0` を返します。それ以外の場合、両方が正常に展開され最終的に `PP_EQUAL_NIL` が得られます。それを組み合わせて `PP_NOT_EQUAL_CHECK_PP_EQUAL_NIL` が `1` を返します。

相等：Equality:

``` cpp
#define PP_EQUAL(x, y) PP_NOT(PP_NOT_EQUAL(x, y))

PP_EQUAL(1, 1)              // -> 1
PP_EQUAL(1, 3)              // -> 0

```

以下のテキストを日本語に翻訳してください：

小于等于：

``` cpp
#define PP_LESS_EQUAL(x, y) PP_NOT(PP_SUB(x, y))

PP_LESS_EQUAL(2, 1)         // -> 0
PP_LESS_EQUAL(1, 1)         // -> 1
PP_LESS_EQUAL(1, 2)         // -> 1
```

小于:

``` cpp
#define PP_LESS(x, y) PP_AND(PP_LESS_EQUAL(x, y), PP_NOT_EQUAL(x, y))

PP_LESS(2, 1)               // -> 0
PP_LESS(1, 2)               // -> 1
PP_LESS(2, 2)               // -> 0
```

その他にも、より大きい、以上などの算術比較がありますが、ここでは詳細は省略します。

####算術演算

`PP_AUTO_WHILE` を使用すると、基本的な算術演算を実行でき、ネストされた演算もサポートされます。

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

引き算:

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

掛け算：

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

掛算法 、 ここで新しいパラメータ `ret` が追加されました。初期値は `0` であり、各反復で `ret = ret + x` が実行されます。

除法：División:

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

割り算に `PP_LESS_EQUAL` が使われていて、`y <= x` の場合にだけループが続行されます。

####データ構造

宏也可以有データ構造、実際には前にもう少し `tuple` というデータ構造を使っていました。 `PP_REMOVE_PARENS` は `tuple` の外側の括弧を取り除き、中の要素を返すことができます。ここでは `tuple` を例にして関連する実装を考えますが、他のデータ構造、例えば `list, array` などに興味がある場合は、`Boost` の実装を見てみると良いでしょう。

`tuple` 定义为用括号包住的逗号分开的元素集合：`(a, b, c)`。

``` cpp
#define PP_TUPLE_REMOVE_PARENS(tuple) PP_REMOVE_PARENS(tuple)

指定されたインデックスの要素を取得します。
#define PP_TUPLE_ELEM(i, tuple) PP_ARGS_ELEM(i, PP_TUPLE_REMOVE_PARENS(tuple))

タプル全体を消去して空に戻す
#define PP_TUPLE_EAT() PP_EMPTY_EAT

サイズを取得する
#define PP_TUPLE_SIZE(tuple) PP_ARGS_SIZE(PP_TUPLE_REMOVE_PARENS(tuple))

// 要素を追加
#define PP_TUPLE_PUSH_BACK(elem, tuple) \
    PP_TUPLE_PUSH_BACK_IMPL(PP_TUPLE_SIZE(tuple), elem, tuple)
#define PP_TUPLE_PUSH_BACK_IMPL(size, elem, tuple) \
    (PP_TUPLE_REMOVE_PARENS(tuple) PP_IF(size, PP_COMMA, PP_EMPTY)() elem)

要求されたテキストを日本語に翻訳します。

// 要素を挿入
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

末尾の要素を削除します。
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

要素を削除します。
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

ここでは、要素の挿入方法を少し説明しますが、他の要素の削除なども同様の原理で実現されます。`PP_TUPLE_INSERT(i, elem, tuple)`は、位置`i`に要素`elem`を挿入することができます。この操作を行うには、まず位置`i`より小さい要素をすべて新しい`tuple`（`ret`）に`PP_TUPLE_PUSH_BACK`を使用して移動し、次に位置`i`に要素`elem`を挿入し、その後、元の`tuple`で位置`i`以上の要素を`ret`の後ろに移動させます。最終的に`ret`には、求めていた結果が得られます。

##総括

(https://github.com/pfultz2/Cloak/wiki/C-Preprocessor-tricks,-tips,-and-idioms#deferred-expression)BOOST_PP内の`REPEAT`関連のマクロなどに興味がある方は、自分で情報を調べてみてください。

マクロプログラムのデバッグは、つらいプロセスですが、次のような方法があります：

`-P -E`オプションを使用して、前処理結果を出力します。
前述の私が修正した `clang` のバージョンを詳細に調査しました。
複雑なマクロを分解して、中間マクロの展開結果を表示します。
関係のないヘッダーファイルやマクロを非表示にします。
与规划的过程是的要理解宏扩展的步骤，一旦熟悉了宏扩展，调节程序的效率也会提高。

本文中のマクロは、私が原理を理解した後に再実装したものです。一部のマクロは、Boostの実装や参照記事から着想を得ています。もし間違いがあれば、いつでも指摘してください。また、関連する問題について議論したい場合は、お気軽にお知らせください。

こちらに本文のコードがすべてあります：[ダウンロード](assets/img/2021-3-31-cpp-preprocess/macros.cpp)[オンラインデモ](https://godbolt.org/z/coWvc5Pse)I'm sorry, but there is nothing to translate in the text you provided.

##引用

* [Boost.Preprocessor](https://www.boost.org/doc/libs/1_75_0/libs/preprocessor/doc/)
*[C/C++ Macro Programming Art](https://bot-man-jl.github.io/articles/?post=2020/Macro-Programming-Art)

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されました。[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。 
