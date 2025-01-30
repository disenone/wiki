---
layout: post
title: C/C++ マクロプログラミング解析
categories:
- c++
catalog: true
tags:
- dev
description: 本文の目的は、C/C++ マクロプログラミングのルールと実装方法を明確に説明し、コード内のマクロを見ることに対する恐怖を感じなくさせることです。
figures: []
---

<meta property="og:title" content="C/C++ 宏编程解析" />

本文の目的は、C/C++のマクロプログラミングの規則と実装方法を明確に説明し、コード内のマクロを見ても恐れる必要がなくなるようにすることです。ますは、C++標準14で述べられているマクロ展開の規則について説明し、次にClangのソースコードを変更してマクロ展開を観察し、最後にこれらの知識を基にマクロプログラミングの実装について話し合います。

本文のコードはすべてここにあります：[ダウンロード](assets/img/2021-3-31-cpp-preprocess/macros.cpp)(https://godbolt.org/z/coWvc5Pse)。

##引子

コマンド `gcc -P -E a.cpp -o a.cpp.i` を実行することで、コンパイラが`a.cpp`ファイルをプリプロセスのみ実行し、その結果を`a.cpp.i`に保存できます。

まずはいくつかの例を見てみましょう。

####再帰的再入（Reentrancy）

``` cpp
#define ITER(arg0, arg1) ITER(arg1, arg0)

ITER(1, 2)          // -> ITER(2, 1)
```

マクロ `ITER` は `arg0`、`arg1` の位置を交換しました。マクロを展開すると、`ITER(2, 1)` が得られます。

`arg0` と `arg1` の位置が成功裡に交換されたことが見てとれます。ここではマクロが一度成功裏に展開されましたが、再帰的に再び展開されることはありません。言い換えれば、マクロの展開過程では、自身を再帰的に再び入ることはできません。再帰の過程で、同じマクロが以前の再帰で既に展開されていることが発見された場合、再展開は行われません。これはマクロ展開に関する重要なルールの一つです。再帰的な再入を禁止する理由は非常に単純で、無限再帰を回避するためです。

####文字列の結合

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                // -> HelloWorld
CONCAT(Hello, CONCAT(World, !))     // ->　HelloCONCAT(World, !)
```

宏`CONCAT`の目的は`arg0`と`arg1`を連結することです。マクロが展開されると、`CONCAT(Hello, World)`は`HelloWorld`と正しくなる。しかし、`CONCAT(Hello, CONCAT(World, !))`は外側のマクロしか展開されず、内側の`CONCAT(World, !)`は展開されず、直接`Hello`と連結されました。これは私たちの予想とは異なり、本当に欲しい結果は`HelloWorld!`です。これはマクロの展開のもう一つ重要なルールで、`##`演算子の後に続くマクロ引数は展開されず、直接前の内容と連結されることです。

上の二つの例からわかるように、マクロ展開のルールの中には直感に反するものもあり、具体的なルールがはっきりしていないと、意図した効果とは異なるマクロを書く可能性があります。

##拡張ルールを開発します。

引数の2つの例を通じて、マクロ展開には一連の標準的な規則があることを理解しました。この規則はC/C++標準に定義されており、内容は少ないため、まずは何度かしっかり読んでおくことをお勧めします。こちらに標準n4296バージョンのリンクを添えておきます。マクロ展開は16.3節にあります：[リンク](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4296.pdf)。ここで、n4296バージョンの中からいくつかの重要なルールを挙げます。これらのルールは、マクロを正しく記述する方法を決定します（標準のマクロをじっくり読み込む時間を取ることをお勧めします）。

####パラメーター分割

マクロのパラメータ要件は、カンマで区切られ、そしてパラメータの数はマクロ定義と一致する必要があります。 マクロに渡されるパラメータでは、括弧で囲まれた追加の内容は1つのパラメータと見なされ、パラメータは空であっても構いません:

``` cpp
#define ADD_COMMA(arg1, arg2) arg1, arg2

ADD_COMMA(a, b)             // -> a, b
ADD_COMMA(a)                // エラー "マクロ "MACRO" は2つの引数を必要としますが、1つしか指定されていません"
ADD_COMMA((a, b), c)        // -> (a, b), c
ADD_COMMA(, b)              // -> , b
```

`ADD_COMMA((a, b), c)` の中で `(a, b)` は最初の引数と見なされます。 `ADD_COMMA(, b)` の場合、第一个参数が空であるため、展開すると `, b` になります。

####マクロ展開

マクロを展開する際に、もしマクロのパラメータが展開可能なマクロである場合、パラメータを完全に展開してからマクロを展開します。例えば、

``` cpp
ADD_COMMA(ADD_COMMA(1, 2), ADD_COMMA(3, 4))     // -> 1, 2, 3, 4
```

一般的な状況でのマクロ展開は、通常、パラメータの評価を先に行い、その後にマクロの評価を行うと考えられます。ただし、`#` および `##` 演算子に遭遇した場合は除きます。

####`#` 操作符

`#` 操作符の後に続くマクロ引数は展開されず、直接文字列化されます。例えば：

``` cpp
#define STRINGIZE(arg0) # arg0

STRINGIZE(a)                // -> "a"
STRINGIZE(STRINGIZE(a))     // -> "STRINGIZE(a)"
```

この規則に従って `STRINGIZE(STRINGIZE(a))` は `"STRINGIZE(a)"` にしか展開できません。

####`##` Operator

`##`マクロパラメータの前後に操作がある場合、展開されることはなく、まず直接連結されます。例えば：

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                        // -> HelloWorld
CONCAT(Hello, CONCAT(World, !))             // -> HelloCONCAT(World, !)
CONCAT(CONCAT(Hello, World) C, ONCAT(!))    // -> CONCAT(Hello, World) CONCAT(!)
```

`CONCAT(CONCAT(Hello, World) C, ONCAT(!))` はまず一つに結合されて、`CONCAT(Hello, World) CONCAT(!)` になります。

####重複スキャン

プリプロセッサは、1度のマクロ展開を完了すると、取得したコンテンツを再スキャンして展開を継続し、展開できる内容がなくなるまで続けます。

一次マクロ展開は、パラメータを完全に展開（`#` および `##` に出会わない限り）し、その後マクロの定義に基づいて、マクロと完全に展開されたパラメータを定義に従って置き換え、定義内のすべての `#` および `##` 演算子を処理することと理解できます。

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define STRINGIZE(arg0) # arg0

CONCAT(STRING, IZE(Hello))        // -> STRINGIZE(Hello) -> "Hello"
```

`CONCAT(STRING, IZE(Hello))` 第一次スキャン展開して `STRINGIZE(Hello)` となり、次に第二次スキャンを実行すると、`STRINGIZE` がさらに展開可能で、最終的に `"Hello"` になります。

####再帰的な再入を禁止します。

繰り返しスキャンの過程では、同じマクロの再帰的な展開は禁止されています。マクロの展開をツリー構造として理解することができ、根ノードは最初に展開するマクロであり、各マクロ展開後の内容はそのマクロの子ノードとしてツリーに接続されます。このように、再帰を禁止するということは、子ノードのマクロを展開する際に、そのマクロが任意の祖先ノードのマクロと同じであれば展開を禁止するということです。いくつかの例を見てみましょう：

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define CONCAT_SPACE(arg0, arg1) arg0 arg1
#define IDENTITY(arg0) IDENTITY_IMPL(arg0)
#define IDENTITY_IMPL(arg0) arg0

CONCAT(CON, CAT(a, b))                  // -> CONCAT(a, b)
IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))   // -> CONCAT(a, b)
IDENTITY(CONCAT(CON, CAT(a, b)))        // -> IDENTITY_IMPL(CONCAT(a, b)) -> CONCAT(a, b)
```

`CONCAT(CON, CAT(a, b))`：`CONCAT`は`##`を使用して2つの引数を連結するため、`##`のルールに従い、引数は展開されずに直接連結されます。したがって、最初の展開で`CONCAT(a, b)`が得られますが、`CONCAT`はすでに展開されたため、再帰的な展開は行われず、停止します。

`IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))`：`IDENTITY_IMPL` というのは引数 `arg0` を評価するということであり、ここでは引数 `arg0` を評価すると `CONCAT(a, b)` を得る。そして再帰的に再入力を禁止するとマークされた後、`IDENTITY_IMPL` が展開されていく。2回目のスキャンが行われると、再入力を禁止されている `CONCAT(a, b)` が見つかり、展開が停止される。ここで `CONCAT(a, b)` は引数 `arg0` を展開して得られたものであり、後続の展開でも再入力が禁止されている。親ノードが引数 `arg0` であり、一貫して再入力が禁止されていると解釈できる。

`IDENTITY(CONCAT(CON, CAT(a, b)))`: この例は親子ノードの理解を強化するためにあります。パラメータが展開される際、自身が親ノードとして、展開される内容が子ノードとして再帰的に判断されます。マクロ定義に渡された展開後のパラメータには、再入を禁止するフラグが引き続き保持されます（展開後のマクロがパラメータを変更しない場合）。パラメータの展開プロセスは別の木として考えることができ、展開結果は木の最も下位の子ノードです。この子ノードがマクロに渡され展開される際、再入を禁止する特性はそのまま維持されます。

例えばここでは、最初の完全な展開後に `IDENTITY_IMPL(CONCAT(a, b))` が得られます。`CONCAT(a, b)` は再入禁止としてマークされており、`IDENTITY_IMPL` がパラメータを評価しても、パラメータが展開禁止されているため、パラメータはそのまま定義に渡されます。最終的には `CONCAT(a, b)` が得られます。

以上は、私が重要だと思う、または理解しづらいと思ういくつかのルールを挙げただけです。詳細なマクロ展開ルールについては、標準文書を直接見ることをお勧めします。

##Clangを通じて展開プロセスを観察する

(https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-11.1.0.tar.gz)）, 修正されたファイル（[リンク](assets/img/2021-3-31-cpp-preprocess/clang-modify.zip)下記は、以前に紹介したマクロ展開規則を簡単な例を通じて検証します。

####例子1

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(C, ONCAT(a, b))      // CONCAT(a, b)
```

修正された Clang を使用して上記のコードをプリプロセスします： `clang -P -E a.cpp -o a.cpp.i`、以下の出力情報が得られます：

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

第 [1](#__codelineno-9-1)行 `HandleIdentifier` がマクロに遭遇した際に、次にマクロの情報を印刷します（第 [2-4](#__codelineno-9-2)訳してください。

実際に展開関数を実行するのは `ExpandFunctionArguments` であり、その後に展開待ちのマクロ情報を再度表示します。この時点でマクロは `used` としてマークされていることに注意してください（第 [9](#__codelineno-9-9)これらのテキストを日本語に翻訳します：

行）。之后根据宏的定义，进行逐个 `Token` 的展开 （`Token` 是 `Clang` 预处理里面的概念，这里不深入说明）。

第0の`Token`は形状引数`arg0`であり、対応する実引数は`C`です。展開の必要がないため、結果に直接コピーされます（第[11-13](#__codelineno-9-11)I'm sorry, but I can't translate the text as it is not written in any identifiable language.

(#__codelineno-9-14)そのテキストは日本語に次のように翻訳されます： 

行）。

(#__codelineno-9-16)行）。

最後に `Leave ExpandFunctionArguments` が今回のスキャンで展開された結果を印刷します（第 [19](#__codelineno-9-19)行），結果の `Token` をすべて翻訳すると `C ## ONCAT(a, b)` になり、その後、プリプロセッサは `##` 演算子を実行して新しい内容を生成します。

`##`を実行した後、`CONCAT(a, b)`が得られ、マクロ`CONCAT`に遭遇すると、プリプロセッサはまず`HandleIdentifier`に入り、マクロの情報を出力する。そのマクロの状態が`disable used`であることが分かり、すでに展開済みで再入禁止されていることがわかる。そのため`Macro is not ok to expand`と表示され、プリプロセッサは展開を行わず、最終的に得られる結果は`CONCAT(a, b)`となる。

####例子2

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define IDENTITY(arg0) arg0

IDENTITY(CONCAT(C, ONCAT(a, b)))
```

<details>
<summary> <font> Clang printing information (click to expand):</font> </summary>
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

以上のテキストを日本語に翻訳してください：

第 [12](#__codelineno-11-12)`IDENTITY`の展開を開始すると、パラメータ`Token 0`が`CONCAT(...)`であることがわかります。これもマクロですので、まずこのパラメータを評価します。

(#__codelineno-11-27)行開始展開參數宏 `CONCAT(...)`，跟例子 1 一樣，多次掃描展開完成後得到 `CONCAT(a, b)` （第 [46](#__codelineno-11-46)行）。

(#__codelineno-11-47)`IDENTITY` に対する展開を終了し、得られる結果は `CONCAT(a, b)` です。

第 [51](#__codelineno-11-51)行重新スキャン `CONCAT(a, b)` を行い、マクロではあるものの以前のパラメータ展開の過程で既に `used` として設定されていたため、再帰的に展開されず、最終結果として直接扱われることを発見しました。

####例子 3

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define IDENTITY_IMPL(arg0) arg0
#define IDENTITY(arg0) IDENTITY_IMPL(arg0)

IDENTITY(CONCAT(C, ONCAT(a, b)))
```

<details>
<summary> <font>Clangの印刷情報（クリックで展開）：</font> </summary>
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

(#__codelineno-13-16)行が開始されると `IDENTITY` が展開され、同様にプリプロセッサは `Token 2`（すなわち `arg0`）がマクロであることを認識し、まず `CONCAT(C, ONCAT(a, b))` を展開します。

* `arg0` を展開すると `CONCAT(a, b)` が得られます （第 [23-54](#__codelineno-13-23)（行）

* `IDENTITY` は最終的に `IDENTITY_IMPL(CONCAT(a, b))` に展開されます（第 [57](#__codelineno-13-57)申し訳ございませんが、そのテキストは意思を持たない文字のため翻訳できません。

* 再スキャンし、`IDENTITY_IMPL`を引き続き展開します（第 [61-72](#__codelineno-13-61)行），この時点での `Token 0` はマクロ `CONCAT(a, b)` ですが、`used` 状態にあるため、展開を中止し、戻ります（第 75-84行）。最終的に得られる結果は依然として `CONCAT(a, b)` です（第 [85](#__codelineno-13-85)（行）。

* 再スキャンの結果、マクロ `CONCAT(a, b)` の状態が `used` であることが確認され、展開を停止して最終結果を得ました。

上記の3つの簡単な例を通じて、プリプロセッサがマクロを展開する過程を大まかに理解することができます。ここではプリプロセッサについてさらに深く探求することはしませんが、興味があれば私が提供した修正ファイルを参照して研究してください。

##マクロプログラミングの実現

では、テーマに入ります（前の大部分はマクロ展開ルールをより良く理解するためのものでした）、マクロプログラミングの実現です。

####基本符号

まず、マクロの特殊記号を定義しておくと、評価や連結の際に使用されます。

``` cpp
#define PP_LPAREN() (
#define PP_RPAREN() )
#define PP_COMMA() ,
#define PP_EMPTY()
#PP_HASHHASH を # ## # として定義します。// 表示 ##文字列，但只是作为字符串，不会当作##操作符来处理
```

####評価

利用パラメータを優先的に展開するルールを利用して、値を求めるマクロを記述できます：

``` cpp
#define PP_IDENTITY(arg0) arg0

PP_COMMA PP_LPAREN() PP_RPAREN()                // -> PP_COMMA ( )
PP_IDENTITY(PP_COMMA PP_LPAREN() PP_RPAREN())   // -> PP_COMMA() -> ,
```

もし単に `PP_COMMA PP_LPAREN() PP_RPAREN()` と書くだけなら、プリプロセッサはそれぞれのマクロを個別に処理するだけで、展開された結果を再度統合して処理することはありません。`PP_IDENTITY` を加えることで、プリプロセッサは展開された `PP_COMMA()` に再評価を行い、`,` を得ることができます。


####結合

`##`を結合する際に、左右のパラメータを展開しないため、パラメータが先に評価されてから結合されるようにするには、次のように書くことができます：

``` cpp
#define PP_CONCAT(arg0, arg1) PP_CONCAT_IMPL(arg0, arg1)
#define PP_CONCAT_IMPL(arg0, arg1) arg0 ## arg1

PP_CONCAT(PP_IDENTITY(1), PP_IDENTITY(2))         // -> 12
PP_CONCAT_IMPL(PP_IDENTITY(1), PP_IDENTITY(2))    // -> PP_IDENTITY(1)PP_IDENTITY(2) -> エラー
```

ここで `PP_CONCAT` で使用されている方法は、遅延連結と呼ばれ、`PP_CONCAT_IMPL` に展開される際に、`arg0` と `arg1` はどちらも最初に展開され評価され、その後 `PP_CONCAT_IMPL` が実際の連結操作を実行します。

####論理演算

`PP_CONCAT` を使うことで論理演算を実現できます。まず `BOOL` 値を定義します：


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

`PP_CONCAT` を使って `PP_BOOL_` と `arg0` を先に連結し、その後連結結果を評価します。ここでの `arg0` は評価後に `[0, 256]` の範囲の数値を得る必要があり、`PP_BOOL_` の後に連結して評価することでブーリアン値を得ることができます。論理和・論理積・否定演算：

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

`PP_BOOL`を使用してパラメーターを評価し、その後`0 1`の組み合わせに基づいて論理演算の結果を組み立てます。`PP_BOOL`を使用しない場合、パラメーターは`0 1`の2つの数値のサポートに制限され、適用範囲が大幅に狭まります。同様に、排他的論理和、論理和、否定なども実装可能です。興味があれば、ぜひお試しください。

####条件選択

`PP_BOOL`と`PP_CONCAT`を使って、条件分岐文を書くこともできます：

``` cpp
#define PP_IF(if, then, else) PP_CONCAT(PP_IF_, PP_BOOL(if))(then, else)
#define PP_IF_1(then, else) then
#define PP_IF_0(then, else) else

PP_IF(1, 2, 3)      // -> PP_IF_1(2, 3) -> 2
PP_IF(0, 2, 3)      // -> PP_IF_0(2, 3) -> 3
```

`if` が `1` に評価された場合、`PP_CONCAT` を使って `PP_IF_1` に結合し、最後に `then` の値に展開されます。同様に、`if` が `0` に評価された場合は、`PP_IF_0` が得られます。

####増減

整数递增递减：数値の増減：

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

「PP_BOOL」と同様に、整数の増加と減少も範囲制限があります。ここでは、範囲は「0から256」に設定されています。256に増加した後、安全のため、「PP_INC_256」は自身の「256」を境界として返します。同様に、「PP_DEC_0」も「0」を返します。

####可変長引数

宏は可変長引数を受け入れることができます。フォーマットは以下の通りです：

```cpp
#define LOG(format, ...) printf("log: " format, __VA_ARGS__)

LOG("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG("Hello World")              // -> printf("log: " "Hello World", ); 多了个逗号，编译报错
```

可変引数が空である可能性があるため、空の場合にはコンパイルエラーが発生する可能性があるため、C++ 20 では `__VA_OPT__` が導入されました。可変引数が空の場合は空を返し、それ以外の場合は元の引数を返します。

```cpp
#define LOG2(format, ...) printf("log: " format __VA_OPT__(,) __VA_ARGS__)

LOG2("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG2("Hello World")              // -> printf("log: " "Hello World" ); カンマなし、正常にコンパイルされる
```

しかし残念ながら、このマクロは C++ 20 以上の標準でしか利用できません。以下に `__VA_OPT__` の実装方法を示します。

####惰性求值

この状況を考慮してください：

``` cpp
PP_IF(1, PP_COMMA(), PP_LPAREN())     // -> PP_IF_1(,,)) -> マクロ "PP_IF_1" の呼び出し時に未終了の引数リストのエラー
```

私たちは、マクロが展開される際に最初の引数が評価されることを知っています。`PP_COMMA()`と`PP_LPAREN()`が評価された後に`PP_IF_1`に渡され、`PP_IF_1(,,))`が得られ、プリプロセッサがエラーを引き起こします。この場合、遅延評価と呼ばれる方法を採用することができます。

``` cpp
PP_IF(1, PP_COMMA, PP_LPAREN)()       // -> PP_IF_1(PP_COMMA, PP_LPAREN)() -> PP_COMMA() -> ,
```

この書き方に変更して、マクロの名前だけを渡し、`PP_IF` が必要なマクロ名を選択した後、カッコ `()` を付けて完成したマクロを作成し、最後に展開します。遅延評価は、マクロプログラミングでもよく見られます。

####以括号开始

変長パラメーターが括弧で始まっているかどうかを判断する：

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

`PP_IS_BEGIN_PARENS`は、渡された引数が括弧で始まるかどうかを判断するために使用できます。括弧で渡されるパラメータを処理する必要がある場合に利用され（たとえば後述の `__VA_OPT__` の実装など）、やや複雑に見えるかもしれませんが、その中核となる考え方は、括弧で始まる可変長引数を処理して、括弧と連結して評価を行い一つの結果を得るか、別の結果を得るかを決定するマクロを構築するというものです。詳しく見ていきましょう：

`PP_IS_BEGIN_PARENS_PROCESS` と `PP_IS_BEGIN_PARENS_PROCESS_0` から成るマクロの機能は、まず渡された可変引数の評価を行い、その後第 0 引数を取得することです。

`PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__)`は、まず`PP_IS_BEGIN_PARENS_EAT __VA_ARGS__`を評価し、その評価結果を`PP_IS_BEGIN_PARENS_PRE_`と結合する。

`PP_IS_BEGIN_PARENS_EAT(...)` マクロはすべての引数を飲み込み、1 を返します。前のステップ `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` で、`__VA_ARGS__` が括弧で始まっている場合、`PP_IS_BEGIN_PARENS_EAT(...)` の評価に一致し、1 を返します。逆に、括弧で始まっていない場合には一致せず、`PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` はそのまま保持されます。

若 `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` 求值得到 `1`，`PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, 1) -> PP_IS_BEGIN_PARENS_PRE_1 -> 1,`，注意 `1` 后面是有个逗号的，把 `1, ` 传给 `PP_IS_BEGIN_PARENS_PROCESS_0`，取第 0 个参数，最后得到 `1`，表示参数是以括号开始。

もし `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` が `1` ではなく変化しない場合、`PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__) -> PP_IS_BEGIN_PARENS_PRE_PP_IS_BEGIN_PARENS_EAT __VA_ARGS__ -> 0, __VA_ARGS__` となり、`PP_IS_BEGIN_PARENS_PROCESS_0` に渡される値は `0` となり、引数が括弧で始まっていないことを示します。

####可変長引数空

可変長引数が空かどうかを判断するのも一般的なマクロであり、`__VA_OPT__` を実現する際に必要です。ここでは `PP_IS_BEGIN_PARENS` を利用して、不完全なバージョンを先に書いてみます：

``` cpp
#define PP_IS_EMPTY_PROCESS(...) \
    PP_IS_BEGIN_PARENS(PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ())
#define PP_IS_EMPTY_PROCESS_EAT(...) ()

PP_IS_EMPTY_PROCESS()       // -> 1
PP_IS_EMPTY_PROCESS(1)      // -> 0
PP_IS_EMPTY_PROCESS(1, 2)   // -> 0
PP_IS_EMPTY_PROCESS(())     // -> 1
```

`PP_IS_EMPTY_PROCESS`の作用は、`PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ()`が括弧で始まるかどうかを判断することです。

もし `__VA_ARGS__` が空であれば、`PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ () -> PP_IS_EMPTY_PROCESS_EAT() -> ()` となり、得られるのは一対の括弧 `()` です。これを `PP_IS_BEGIN_PARENS` に渡すと `1` が返され、パラメータが空であることを示します。

そうでなければ、`PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ()`は変更されずに`PP_IS_BEGIN_PARENS`に渡され、0を返して非空を示します。

第4の例 `PP_IS_EMPTY_PROCESS(()) -> 1` に注意してください。`PP_IS_EMPTY_PROCESS` は、括弧で始まる可変引数を適切に処理できません。なぜなら、この場合、括弧を持つ可変引数が `PP_IS_EMPTY_PROCESS_EAT` に一致し、`()` が評価されるからです。この問題を解決するには、引数が括弧で始まるかどうかを区別する必要があります：

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

`PP_IS_EMPTY_IF` は、`if` 条件に基づいて第1引数または第2引数を返します。

もし可変長引数が括弧で始まる場合、`PP_IS_EMPTY_IF` は `PP_IS_EMPTY_ZERO` を返し、最終的に `0` を返すことで、可変長引数が空でないことを示します。

反之 `PP_IS_EMPTY_IF` は `PP_IS_EMPTY_PROCESS` を返し、最終的に `PP_IS_EMPTY_PROCESS` が可変長引数が非空かどうかを判断します。

####添えるするアクセス

可変長パラメータ指定位置の要素を取得する：

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

`PP_ARGS_ELEM` の最初の引数は要素のインデックス `I` で、その後に可変長引数が続きます。 `PP_CONCAT` を利用して `PP_ARGS_ELEM_` と `I` を結合することで、対応する位置の要素を返すマクロ `PP_ARGS_ELEM_0..8` を得ることができ、可変長引数をそのマクロに渡すことで、インデックスに対応する位置の要素を展開して返します。

#### PP_IS_EMPTY2

`PP_ARGS_ELEM` を利用することでも、別のバージョンの `PP_IS_EMPTY` を実現できます：

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

`PP_ARGS_ELEM`を借りて、引数にコンマが含まれているかどうかを判断する `PP_HAS_COMMA` を実装しています。`PP_COMMA_ARGS` は渡された任意の引数を取り込んで、コンマを返します。

判断変長パラメータが空かどうかの基本ロジックは `PP_COMMA_ARGS __VA_ARGS__ ()` がコンマを返すこと、つまり `__VA_ARGS__` が空であることです。`PP_COMMA_ARGS` と `()` を結合して評価する具体的な書き方は `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ())` です。

ただし、例外があります：

* `__VA_ARGS__` 自体がカンマを含む可能性があります；
`__VA_ARGS__()` はカンマ区切りで評価される結果が連結されます。
`PP_COMMA_ARGS __VA_ARGS__` は、評価された際にカンマが表示されるように一緒に連結されます。 

上記の3つの例外状況については、除外処理が必要ですので、最終的な書き方は以下の4つの条件についてAND論理演算を実行することと同等です：

* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__))` &&
* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__()))` &&
* `PP_NOT(PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__))` &&
* `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ())`

#### `__VA_OPT__`

`PP_IS_EMPTY` を利用して、ようやく `__VA_OPT__` に似たマクロを実現できます：

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

`PP_ARGS_OPT` は、2つの固定パラメータと可変長パラメータを受け入れます。可変長パラメータが空でない場合は `data` を返し、そうでなければ `empty` を返します。`data` と `empty` の両方がカンマに対応できるように、実際のパラメータはどちらも括弧で包む必要があります。最後に `PP_REMOVE_PARENS` を使って外側の括弧を取り除きます。

`PP_ARGS_OPT` を使うことで、`LOG3` が `LOG2` によって実現された機能を模倣することができます：

``` cpp
#define LOG3(format, ...) \
    printf("log: " format PP_ARGS_OPT((,), (), __VA_ARGS__) __VA_ARGS__)

LOG3("Hello");                  // -> printf("log: " "Hello" );
LOG3("Hello %s", "World");      // -> printf("log: " "Hello %s" , "World");
```

`data_tuple` is `(,)`, and if the variable-length parameter is not empty, it will return all the elements inside `data_tuple`, which in this case is a comma `,`.

####パラメータの数をお知らせください。

可変長引数の数を取得する：

``` cpp
#define PP_ARGS_SIZE_IMCOMPLETE(...) \
    PP_ARGS_ELEM(8, __VA_ARGS__, 8, 7, 6, 5, 4, 3, 2, 1, 0)

PP_ARGS_SIZE_IMCOMPLETE(a)             // -> 1
PP_ARGS_SIZE_IMCOMPLETE(a, b)          // -> 2
PP_ARGS_SIZE_IMCOMPLETE(PP_COMMA())    // -> 2
PP_ARGS_SIZE_IMCOMPLETE()              // -> 1
```

可変長引数の数を計算するには、引数の位置にアクセスします。`__VA_ARGS__` は後続の引数をすべて右にずらします。マクロ `PP_ARGS_ELEM` を使用して、8 番目の引数を取得します。`__VA_ARGS__` に引数が1つしかない場合、8 番目の引数は `1` になります。同様に、`__VA_ARGS__` に2つの引数がある場合、8 番目の引数は `2` になり、ちょうど可変長引数の数と一致します。

ここで示された例は、最大で8個の可変長引数のみをサポートしています。これは、`PP_ARGS_ELEM` がサポートできる最大の長さに依存しています。

しかし、このマクロはまだ不完全で、可変長引数が空の場合、このマクロは誤って `1` を返します。空の可変長引数を処理する必要がある場合は、前述の `PP_ARGS_OPT` マクロを使用する必要があります。

``` cpp
#define PP_COMMA_IF_ARGS(...) PP_ARGS_OPT((,), (), __VA_ARGS__)
#define PP_ARGS_SIZE(...) PP_ARGS_ELEM(8, __VA_ARGS__ PP_COMMA_IF_ARGS(__VA_ARGS__) 8, 7, 6, 5, 4, 3, 2, 1, 0, 0, 0)

PP_ARGS_SIZE(a)             // -> 1
PP_ARGS_SIZE(a, b)          // -> 2
PP_ARGS_SIZE(PP_COMMA())    // -> 2
PP_ARGS_SIZE()              // -> 0
PP_ARGS_SIZE(,,,)           // -> 4
```

問題の鍵はカンマ `,` です。 `__VA_ARGS__` が空のとき、カンマを省略することで正しく `0` を返すことができます。

####遍历访问 translates to "トラバースアクセス" in Japanese.

C++ と似たような `for_each` のように、マクロの `PP_FOR_EACH` を実装することができます：

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

`PP_FOR_EACH` は2つの固定パラメータを受け取ります： `macro` は繰り返しの際に呼び出されるマクロと考えることができ、`contex` は `macro` に渡す固定値のパラメータとして使えます。`PP_FOR_EACH` はまず `PP_ARGS_SIZE` を使用して可変長引数の長さ `N` を取得し、次に `PP_CONCAT` を用いて `PP_FOR_EACH_N` を結合します。その後、`PP_FOR_EACH_N` は `PP_FOR_EACH_N-1` を繰り返し呼び出すことで、可変長引数の個数と同じ回数の繰り返しを実現します。

例中では、`DECLARE_EACH` を `macro` のパラメータとして宣言しています。`DECLARE_EACH` は `contex arg` を返す役割を果たし、`contex` が型名、`arg` が変数名である場合、`DECLARE_EACH` は変数を宣言するために使用できます。

####条件循环

`FOR_EACH` を使うことで、同様の書き方で `PP_WHILE` を作成することができます：

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

`PP_WHILE` は三つの引数を受け取ります： `pred` 条件判定関数、`op` 操作関数、`val` 初期値；ループの過程で `pred(val)` を使ってループの終了判定を行い、 `op(val)` から得られた値を次のマクロに渡します。以下のコードを実行するものと理解できます：

``` cpp
while (pred(val)) {
    val = op(val);
}
```

`PP_WHILE_N` 最初に `pred(val)` を使用して条件判断の結果を取得し、条件結果 `cond` と残りのパラメータを `PP_WHILE_N_IMPL` に渡します。
`PP_WHILE_N_IMPL` は、2つのパートに分けることができます：後半部分 `(pred, op, PP_IF(cond, op, PP_EMPTY_EAT)(val))` が前半部分のパラメータとして機能し、`PP_IF(cond, op, PP_EMPTY_EAT)(val)` は `cond` が真である場合に `op(val)` を評価し、そうでない場合は空の結果を得ることです。前半部分は `PP_IF(cond, PP_WHILE_N+1, val PP_EMPTY_EAT)` であり、`cond` が真であれば `PP_WHILE_N+1` を返し、後半部分のパラメータと結合してループを継続します。そうでない場合は `val PP_EMPTY_EAT` を返し、この時点で `val` が最終的な計算結果となり、`PP_EMPTY_EAT` は後半部分の結果を無視します。

`SUM` を実現する`N + N-1 + ... + 1`。初期値`(max_num, origin_num)`；`SUM_PRED` の値の最初の要素`x`、0より大きいかどうかを判断します；`SUM_OP` は`x` に対してデクリメント操作`x = x - 1` を実行し、`y`に対して`+ x` 操作`y = y + x`を実行します。`SUM_PRED` と`SUM_OP` を`PP_WHILE`に直接渡し、結果はタプルです。求める実際の結果はタプルの2番目の要素ですので、再び`SUM`を使って2番目の要素の値を取得します。

####再帰的再入

現時点まで、われわれの反復訪問と条件ループはうまく機能し、結果も予想通りです。マクロ展開規則において再帰呼び出しを禁止すると述べたことを覚えていますか。二重ループを実行しようとした際に再帰呼び出しの禁止に遭遇してしまいました：

``` cpp
#define SUM_OP2(xy_tuple) SUM_OP_OP_IMPL2 xy_tuple
#define SUM_OP_OP_IMPL2(x, y) (PP_DEC(x), y + SUM(x, 0))

#define SUM2(max_num, origin_num) \
    PP_IDENTITY(SUM_IMPL PP_WHILE(SUM_PRED, SUM_OP2, (max_num, origin_num)))

SUM2(1, a)      // -> a + SUM_IMPL PP_WHILE_1(SUM_PRED, SUM_OP, (1, a))
```

`SUM2` の引数 `op` を `SUM_OP2` に変更し、`SUM_OP2` では `SUM` を呼び出します。そして、`SUM` の展開は `PP_WHILE_1` になり、`PP_WHILE_1` は実質的に自分自身を再帰的に呼び出しており、プリプロセッサが展開を停止します。

この問題を解決するために、自動再帰の方法を使うことができます：

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

`PP_AUTO_WHILE` は `PP_WHILE` の自動推導再帰バージョンであり、核心となるマクロは `PP_AUTO_REC(PP_WHILE_PRED)` です。このマクロは、現在利用可能な `PP_WHILE_N` バージョンの数字 `N` を見つけ出すことができます。

推導の原理は非常に単純で、すべてのバージョンを検索し、正しく展開できるバージョンを見つけ、そのバージョンの数字を返すことです。検索速度を向上させるために一般的に行われる方法は、二分探索を使用することです。これが `PP_AUTO_REC` が行っていることです。 `PP_AUTO_REC` は `check` というパラメータを受け取り、バージョンの利用可能性をチェックします。ここでは、検索バージョンの範囲が `[1, 4]` であるとされています。 `PP_AUTO_REC` はまず `check(2)` をチェックし、もし `check(2)` が真であれば、`PP_AUTO_REC_12` を呼び出して範囲 `[1, 2]` を検索し、そうでなければ `PP_AUTO_REC_34` を使用して `[3, 4]` を検索します。 `PP_AUTO_REC_12` は `check(1)` をチェックし、もし真であれば、バージョン `1` が利用可能であることを示し、そうでなければバージョン `2` を利用します。 `PP_AUTO_REC_34` についても同様です。

`check` How should I write to know if the version is available? Here, `PP_WHILE_PRED` will be expanded into two parts concatenated. Let's focus on the latter part `PP_WHILE_ ## n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`: if `PP_WHILE_ ## n` is available, since `PP_WHILE_FALSE` always returns `0`, this part will expand to the value of the `val` parameter, which is `PP_WHILE_FALSE`; otherwise, this part of the macro will remain unchanged, still as `PP_WHILE_n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`.

後半部分の結果と前半部分の `PP_WHILE_CHECK_` を結合して、2つの結果が得られます：`PP_WHILE_CHECK_PP_WHILE_FALSE` または `PP_WHILE_CHECK_PP_WHILE_n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`。このため、`PP_WHILE_CHECK_PP_WHILE_FALSE` を `1` で返し、利用可能を示し、`PP_WHILE_CHECK_PP_WHILE_n` を `0` で返し、利用不可を示します。ここで、我々は再帰の機能を自動的に導出することができました。

####算術の比較

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

判断数値が等しいかどうかを確認するために、再帰的な再入を禁止する特性を利用し、`x` と `y` を再帰的に結合して `PP_NOT_EQUAL_x PP_NOT_EQUAL_y` マクロを生成します。もし `x == y` の場合、`PP_NOT_EQUAL_y` マクロは展開されず、`PP_NOT_EQUAL_CHECK_` と結合して `PP_NOT_EQUAL_CHECK_PP_NOT_EQUAL_y` となり、`0` を返します。一方、逆に両方が成功裏に展開されると、最終的に `PP_EQUAL_NIL` が得られ、結合して `PP_NOT_EQUAL_CHECK_PP_EQUAL_NIL` となり、`1` を返します。

相等：

``` cpp
#define PP_EQUAL(x, y) PP_NOT(PP_NOT_EQUAL(x, y))

PP_EQUAL(1, 1)              // -> 1
PP_EQUAL(1, 3)              // -> 0

```

小なり等しい：

``` cpp
#define PP_LESS_EQUAL(x, y) PP_NOT(PP_SUB(x, y))

PP_LESS_EQUAL(2, 1)         // -> 0
PP_LESS_EQUAL(1, 1)         // -> 1
PP_LESS_EQUAL(1, 2)         // -> 1
```

小于：

``` cpp
#define PP_LESS(x, y) PP_AND(PP_LESS_EQUAL(x, y), PP_NOT_EQUAL(x, y))

PP_LESS(2, 1)               // -> 0
PP_LESS(1, 2)               // -> 1
PP_LESS(2, 2)               // -> 0
```

また、大なり、大なりイコールなどの算術比較もありますが、ここでは詳細は省略します。

####算術演算

`PP_AUTO_WHILE` を使用すると、基本的な算術演算を実装して、ネストされた演算をサポートすることができます。

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

乗法実現にはここでパラメーター `ret` が追加され、初期値は `0` で、毎回のイテレーションで `ret = ret + x` が実行されます。

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

除法は `PP_LESS_EQUAL` を利用しており、`y <= x` の場合のみループを継続します。

####データ構造

宏也可能使用数据结构，实际上我们在前面稍微使用了一种数据结构`tuple`，`PP_REMOVE_PARENS`可以去除`tuple`外层的括号，返回其中的元素。在这里我们以`tuple`为例讨论相关的实现，对于其他的数据结构如`list, array`等，有兴趣的话可以看一下`Boost`的实现。

`tuple` はカンマで区切られた要素の集合を括弧で囲んだもので定義されます：`(a, b, c)`。

``` cpp
#define PP_TUPLE_REMOVE_PARENS(tuple) PP_REMOVE_PARENS(tuple)

指定されたインデックスの要素を取得します。
#define PP_TUPLE_ELEM(i, tuple) PP_ARGS_ELEM(i, PP_TUPLE_REMOVE_PARENS(tuple))

// 全体のタプルを飲み込み、空を返す
#define PP_TUPLE_EAT() PP_EMPTY_EAT

// サイズを取得する
#define PP_TUPLE_SIZE(tuple) PP_ARGS_SIZE(PP_TUPLE_REMOVE_PARENS(tuple))

要素を追加
#define PP_TUPLE_PUSH_BACK(elem, tuple) \
    PP_TUPLE_PUSH_BACK_IMPL(PP_TUPLE_SIZE(tuple), elem, tuple)
#define PP_TUPLE_PUSH_BACK_IMPL(size, elem, tuple) \
    (PP_TUPLE_REMOVE_PARENS(tuple) PP_IF(size, PP_COMMA, PP_EMPTY)() elem)

// 要素を挿入する
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

// 末尾の要素を削除する
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

要素を削除
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

ここでは、要素の挿入方法について少し説明します。要素の削除など他の操作も同様の原理で実装されています。`PP_TUPLE_INSERT(i, elem, tuple)` は、位置 `i` に要素 `elem` を挿入することができます。この操作を完了するには、位置 `i` よりも小さい位置にある要素をまずすべて、`PP_TUPLE_PUSH_BACK` を使用して新しい `tuple` に移動します（`ret`）。その後、位置 `i` に要素 `elem` を挿入し、最後に元の `tuple` の位置が `i` 以上である要素を `ret` の後ろに移動させます。これで、`ret` には目的の結果が得られます。

##小结

本文の目的は、C/C++のマクロプログラミングの原理と基本的な実装を明確に説明することです。私自身の理解と認識を記録しつつ、他の人々にとって何らかの啓発や解惑をもたらせることを望んでいます。注意が必要なのは、この記事のボリュームは少し長いですが、マクロプログラミングに関するいくつかのテクニックや使用法には触れていない点です。例えば、CHAOS_PPが提唱する[遅延展開に基づく再帰呼び出し方法](https://github.com/pfultz2/Cloak/wiki/C-Preprocessor-tricks,-tips,-and-idioms#deferred-expression)BOOST_PP の `REPEAT` に関連するマクロなどについて、興味がある方は自分で資料を調べてみてください。

宏編程のデバッグは辛いプロセスですが、私たちは：

* `-P -E` オプションを使用してプリプロセッサ結果を出力します；
* 前述の自分が修正した `clang` バージョンを使って、展開プロセスを詳しく研究する。
複雑なマクロを分解して、中間マクロの展開結果を確認してください。
関連のないヘッダーファイルとマクロを削除します。
その後はマクロの展開プロセスを想像してみる必要があります。マクロの展開に慣れると、デバッグの効率も向上します。

本文中のマクロは、私自身が原理を理解した上で再実装したものであり、一部のマクロは `Boost` の実装や引用されている記事を参考にしています。誤りがあればいつでも指摘していただけると幸いですし、関連する問題についてのディスカッションも歓迎します。

本文的代码全部都在这里：[ダウンロード](assets/img/2021-3-31-cpp-preprocess/macros.cpp)，[オンラインデモ](https://godbolt.org/z/coWvc5Pse)I'm sorry, but there is no text to translate. If you provide me with the content you need translated, I will be happy to assist you.

##引用

* [Boost.Preprocessor](https://www.boost.org/doc/libs/1_75_0/libs/preprocessor/doc/)
* [C/C++ マクロプログラミングの芸術](https://bot-man-jl.github.io/articles/?post=2020/Macro-Programming-Art)

--8<-- "footer_ja.md"


> この投稿は ChatGPT を使って翻訳されました。ご意見は[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。 
