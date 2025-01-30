---
layout: post
title: C/C++ Macro Programming Analysis
categories:
- c++
catalog: true
tags:
- dev
description: The purpose of this article is to clarify the rules and implementation
  methods of C/C++ macro programming, so that you no longer fear seeing macros in
  code.
figures: []
---

<meta property="og:title" content="C/C++ 宏编程解析" />

The purpose of this article is to explain the rules and implementation methods of macro programming in C/C++, so that you no longer fear encountering macros in code. I will first discuss the rules for macro expansion mentioned in the C++ Standard 14, then observe macro expansion by modifying the Clang source code, and finally delve into the implementation of macro programming based on this knowledge.

The code from this article can be found here: [Download](assets/img/2021-3-31-cpp-preprocess/macros.cpp),[Online Demo](https://godbolt.org/z/coWvc5Pse).

##Prologue

We can use the command `gcc -P -E a.cpp -o a.cpp.i` to make the compiler only perform preprocessing on the file `a.cpp` and save the result to `a.cpp.i`.

First, let's take a look at some examples:

####Reentrancy

``` cpp
#define ITER(arg0, arg1) ITER(arg1, arg0)

ITER(1, 2)          // -> ITER(2, 1)
```

The macro `ITER` swapped the positions of `arg0` and `arg1`. After the macro was expanded, it resulted in `ITER(2, 1)`.

It can be seen that the positions of `arg0` and `arg1` have been successfully swapped; the macro has unfolded successfully once here, but it does not unfold recursively. In other words, during the macro expansion process, it is not allowed to recursively re-enter itself. If during recursion it detects that the same macro has already been unfolded in a previous recursion, it will not unfold again. This is one of the important rules of macro expansion. The reason for prohibiting recursive re-entry is quite simple: it is to avoid infinite recursion.

####String concatenation

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                // -> HelloWorld
CONCAT(Hello, CONCAT(World, !))     // -> HelloCONCAT(World, !)
```

The `CONCAT` macro is used to concatenate `arg0` and `arg1`. When the macro is expanded, `CONCAT(Hello, World)` will correctly result in `HelloWorld`. However, if we try `CONCAT(Hello, CONCAT(World, !))`, only the outer macro will expand. The inner `CONCAT(World, !)` will not expand, and will end up directly concatenated with `Hello`, which is not what we expected. The desired outcome is actually `HelloWorld!`. This is another important rule of macro expansion: macro arguments followed by the `##` operator will not be expanded, but will instead be concatenated directly with the previous content.

Through the two examples above, it can be seen that there are some rules for macro expansion that are counterintuitive. If the specific rules are not clear, the macros written may not achieve the desired effect.

##Macro development rules

Through the two examples in the introduction, we learned that macro expansion follows a set of standard rules, which are defined in the C/C++ standard. The rules are not extensive, so I recommend reading them carefully a few times. Here is the link to the n4296 version of the standard, where macro expansion is discussed in section 16.3: [link](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4296.pdf)Below, I have selected a few important rules from the n4296 version, which will determine how to correctly write macros (it is recommended to take some time to carefully read through the macros in the standard).

####Parameter separator

The macro's parameters must be separated by commas, and the number of parameters must match the number of macro definitions. Any content enclosed in parentheses within the parameters passed to the macro is considered as one parameter. Parameters are allowed to be empty:

``` cpp
#define ADD_COMMA(arg1, arg2) arg1, arg2

ADD_COMMA(a, b)             // -> a, b
ADD_COMMA(a)                // Error "macro 'MACRO' requires 2 arguments, but only 1 given"
ADD_COMMA((a, b), c)        // -> (a, b), c
ADD_COMMA(, b)              // -> , b
```

In `ADD_COMMA((a, b), c)`, `(a, b)` is considered as the first argument. In `ADD_COMMA(, b)`, the first argument is empty, so it unfolds as `, b`.

####Macro Expansion

When expanding a macro, if the parameters of the macro are also macros that can be expanded, the parameters will be fully expanded first, and then the macro will be expanded. For example,

``` cpp
ADD_COMMA(ADD_COMMA(1, 2), ADD_COMMA(3, 4))     // -> 1, 2, 3, 4
```

In general, macro expansion can be viewed as evaluating the parameters first, then evaluating the macro, unless encountering the `#` and `##` operators.

####`#` Operator

The macro parameters following the `#` operator will not be expanded, but will be directly converted into strings, for example:

``` cpp
#define STRINGIZE(arg0) # arg0

STRINGIZE(a)                // -> "a"
STRINGIZE(STRINGIZE(a))     // -> "STRINGIZE(a)"
```

According to this rule, `STRINGIZE(STRINGIZE(a))` can only be expanded as `"STRINGIZE(a)"`.

####`##` operator

The macro parameters on both sides of the `##` operator will not be expanded, they will be directly concatenated first, for example:

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                        // -> HelloWorld
CONCAT(Hello, CONCAT(World, !))             // -> HelloCONCAT(World, !)
CONCAT(CONCAT(Hello, World) C, ONCAT(!))    // -> CONCAT(Hello, World) CONCAT(!)
```

The text `CONCAT(CONCAT(Hello, World) C, ONCAT(!))` has to be concatenated first to get `CONCAT(Hello, World) CONCAT(!)`.

####Repeated scanning

After the preprocessor completes one round of macro expansion, it will rescan the obtained content, continue to expand it, until there is no content left to expand.

Expanding a macro once can be understood as fully expanding the parameters first (unless encountering `#` and `##`), then based on the macro definition, replacing the macro and the fully expanded parameters according to the definition, then handling all `#` and `##` operators in the definition.

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define STRINGIZE(arg0) # arg0

CONCAT(STRING, IZE(Hello))        // -> STRINGIZE(Hello) -> "Hello"
```

`CONCAT(STRING, IZE(Hello))` is first scanned and expands to `STRINGIZE(Hello)`, then a second scan is performed, revealing that `STRINGIZE` can be expanded further, ultimately resulting in `"Hello"`.

####Reentrant recursion is prohibited.

During the process of repeated scanning, recursive expansion of the same macro is prohibited. The expansion of a macro can be understood as a tree structure, where the root node is the macro to be expanded initially, and the content after expanding each macro is connected to the tree as child nodes of that macro. Thus, prohibiting recursion means that when expanding child node macros, if a macro is the same as any of its ancestor macros, expansion is disallowed. Let's look at some examples:

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define CONCAT_SPACE(arg0, arg1) arg0 arg1
#define IDENTITY(arg0) IDENTITY_IMPL(arg0)
#define IDENTITY_IMPL(arg0) arg0

CONCAT(CON, CAT(a, b))                  // -> CONCAT(a, b)
IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))   // -> CONCAT(a, b)
IDENTITY(CONCAT(CON, CAT(a, b)))        // -> IDENTITY_IMPL(CONCAT(a, b)) -> CONCAT(a, b)
```

`CONCAT(CON, CAT(a, b))`: Since `CONCAT` concatenates two parameters using `##`, and according to the rules of `##`, parameters are not expanded but directly concatenated. Therefore, the first expansion results in `CONCAT(a, b)`, and since `CONCAT` has already been expanded, it will not be recursively expanded again, so it stops.

`IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))`: `IDENTITY_IMPL` can be understood as evaluating the parameter `arg0`, where the value of `arg0` is `CONCAT(a, b)`. Due to recursion, it has been marked as non-reentrant. After `IDENTITY_IMPL` completes its expansion, during the second scan, it identifies `CONCAT(a, b)` as non-reentrant, hence it stops expanding. Here, `CONCAT(a, b)` is derived from the expansion of the parameter `arg0`, but in subsequent expansions, it will also retain the non-reentrant mark. One can understand that the parent node is parameter `arg0`, which continuously maintains the non-reentrant label.

`IDENTITY(CONCAT(CON, CAT(a, b)))`: This example is primarily to strengthen the understanding of parent-child nodes. When the parameters are expanded on their own, the self is used as the parent node, and the expanded content is used as the child node to determine recursion. After the expansion of the parameters is passed to the macro definition, the prohibition of reentry flag will continue to be retained (if the macro-defined parameters do not change after the expansion). The expansion process of the parameters can be seen as another tree, where the expansion result of the parameters is the bottom-most child node of the tree. This child node is passed to the macro for execution expansion, while still maintaining the feature of prohibiting reentry.

For example, here, after the first complete expansion, we get `IDENTITY_IMPL(CONCAT(a, b))`, where `CONCAT(a, b)` is marked as non-reentrant. Even though `IDENTITY_IMPL` evaluates the parameter, the parameter has already been prohibited from expansion, so it is passed unchanged into the definition, and we ultimately still obtain `CONCAT(a, b)`.

Above, I have only listed some rules that I consider to be important or difficult to understand. For detailed macro expansion rules, I still recommend taking some time to refer to the standard documentation directly.

##Observing the expansion process through Clang

We can add some print statements to the Clang source code to observe the macro expansion process. I don't intend to delve into explaining the Clang source code. Here is a diff of the modified file. If you're interested, you can compile Clang yourself for further study. Here, I'm using llvm version 11.1.0 ([link](https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-11.1.0.tar.gz)), modified file ([link](assets/img/2021-3-31-cpp-preprocess/clang-modify.zip)In the following, we will validate the macro expansion rules we introduced earlier with a simple example.

####Example 1

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(C, ONCAT(a, b))      // CONCAT(a, b)
```

Preprocess the code above using a modified version of Clang: `clang -P -E a.cpp -o a.cpp.i`, obtaining the following printout:

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

Number [1](#__codelineno-9-1)When `HandleIdentifier` encounters a macro, it will first print, then print the macro information (2-4](#__codelineno-9-2)After the new line of code, the macro is not disabled, so it can be expanded according to the definition `Macro is ok to expand`, and then the program enters the macro `EnterMacro`.

The function that actually performs macro expansion is `ExpandFunctionArguments`. After that, the macro information to be expanded is printed again, and it is noted that the macro has now been marked as `used` (line [9](#__codelineno-9-9)After the macros are defined, the expansion of each `Token` is carried out (a `Token` is a concept within the `Clang` preprocessor, not elaborated here).

(#__codelineno-9-11)行).

The first `Token` is `hashhash`, which is the `##` operator, and continue to copy it to the result (lines [14-15](#__codelineno-9-14)行）。

The second `Token` is the parameter `arg1`, and the corresponding actual argument is `ONCAT(a, b)`. The preprocessor will also process the actual argument into individual `Tokens`, so the printed result shows each `Token` of the actual argument enclosed in square brackets (line 18). Due to the `##` operator, this actual argument still does not need to be expanded, so it is directly copied to the result (lines [16-18](#__codelineno-9-16)行).

Finally, `Leave ExpandFunctionArguments` prints the results obtained from this scan expansion (No. [19](#__codelineno-9-19)Once this is processed, all the resulting `Token` will be translated as `C ## ONCAT(a, b)`, and then the preprocessor will perform the `##` operator to generate new content.

After execution, `CONCAT(a, b)` is obtained. Upon encountering the macro `CONCAT`, the preprocessor first enters `HandleIdentifier`, prints out the macro information, and discovers that the macro's status is `disable used`, meaning it has already been expanded and re-entry is prohibited. It displays `Macro is not ok to expand`, and the preprocessor does not expand it again, resulting in the final output being `CONCAT(a, b)`.

####Example 2

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define IDENTITY(arg0) arg0

IDENTITY(CONCAT(C, ONCAT(a, b)))
```

<details>
<summary><font>Clang print information (click to expand):</font></summary>
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

No. [12](#__codelineno-11-12)It is time to initiate the expansion of the 'IDENTITY'. Upon inspection, it was revealed that the parameter 'Token 0' is a 'CONCAT(...)', which is also a macro. Therefore, it is necessary to first evaluate this parameter.

Number [27](#__codelineno-11-27)The line begins to expand the parameter macro `CONCAT(...)`. Similar to Example 1, after multiple scans, it completes the expansion to obtain `CONCAT(a, b)` (line [46](#__codelineno-11-46)（行）.

Number [47](#__codelineno-11-47)The expansion of `IDENTITY` ends with the result being `CONCAT(a, b)`.

(#__codelineno-11-51)After rescan, `CONCAT(a, b)` was found to be a macro, but during the previous parameter expansion process, it had already been set to `used`, so it was no longer recursively expanded and was directly taken as the final result.

####Example 3

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define IDENTITY_IMPL(arg0) arg0
#define IDENTITY(arg0) IDENTITY_IMPL(arg0)

IDENTITY(CONCAT(C, ONCAT(a, b)))
```

<details>
<summary> <font>Clang print information (click to expand):</font> </summary>
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

The [16](#__codelineno-13-16)At the beginning of the execution, `IDENTITY` unfolds. Similarly, when the preprocessor encounters `Token 2` (also known as `arg0`) as a macro, it first expands `CONCAT(C, ONCAT(a, b))`.

* Expanding `arg0` yields `CONCAT(a, b)` (lines [23-54](#__codelineno-13-23)行）

* `IDENTITY` ultimately unfolds to `IDENTITY_IMPL(CONCAT(a, b))` (see [57](#__codelineno-13-57)行）

Re-scan and proceed with unfolding `IDENTITY_IMPL` (from [61-72](#__codelineno-13-61)(#__codelineno-13-85)行).

Re-scan the results and discover that the macro `CONCAT(a, b)` is in the `used` state, stop expanding and obtain the final result.

Through the three simple examples above, we can roughly understand the process of the preprocessor expanding macros. There is no need to delve deeper into the preprocessor here; those interested can refer to the modified files I provided for study.

##Macro programming implementation.

Now, let's move on to the main topic (the purpose of the previous lengthy paragraph was to provide a better understanding of macro expansion rules) - macro programming implementation.

####Basic symbols

First, you can start by defining special symbols for macros, which will be used for evaluation and concatenation.

``` cpp
#define PP_LPAREN() (
#define PP_RPAREN() )
#define PP_COMMA() ,
#define PP_EMPTY()
#Define PP_HASHHASH # ## # // Represents ## as a string, it will not be treated as the ## operator.
```

####Valuation

By utilizing the rule of parameter expansion priority, one can create a evaluation macro:

``` cpp
#define PP_IDENTITY(arg0) arg0

PP_COMMA PP_LPAREN() PP_RPAREN()                // -> PP_COMMA ( )
PP_IDENTITY(PP_COMMA PP_LPAREN() PP_RPAREN())   // -> PP_COMMA() -> ,
```

If you only write `PP_COMMA PP_LPAREN() PP_RPAREN()`, the preprocessor will only process each macro separately, without further merging the expanded results. By adding `PP_IDENTITY`, the preprocessor can evaluate the expanded `PP_COMMA()` to yield `,`.


####Splicing

When concatenating with `##`, the parameters on both sides will not be expanded. To allow the parameters to be evaluated before concatenation, you can write it like this:

``` cpp
#define PP_CONCAT(arg0, arg1) PP_CONCAT_IMPL(arg0, arg1)
#define PP_CONCAT_IMPL(arg0, arg1) arg0 ## arg1

PP_CONCAT(PP_IDENTITY(1), PP_IDENTITY(2))         // -> 12
PP_CONCAT_IMPL(PP_IDENTITY(1), PP_IDENTITY(2))    // -> PP_IDENTITY(1)PP_IDENTITY(2) -> Error
```

The method used here is called delayed concatenation. When expanded into `PP_CONCAT_IMPL`, both `arg0` and `arg1` will be evaluated first, and then the actual concatenation operation will be performed by `PP_CONCAT_IMPL`.

####Logical operation

With the help of `PP_CONCAT`, logical operations can be performed. First, define the `BOOL` value:


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

Use `PP_CONCAT` to concatenate `PP_BOOL_` and `arg0` first, then evaluate the concatenated result. Here, `arg0` is required to evaluate to a number in the range `[0, 256]` after evaluation. By evaluating the concatenation with `PP_BOOL_`, you can obtain a boolean value. Operations include AND, OR, and NOT:

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

First evaluate the parameter using `PP_BOOL`, and then combine the results of logical operations based on the combination of `0` and `1`. If `PP_BOOL` is not used for evaluation, then the parameter can only support the values `0` and `1`, significantly reducing its versatility. Similarly, you can also write operations like XOR, OR, and NOT, if interested, you can try them yourself.

####Selective conditions

Using `PP_BOOL` and `PP_CONCAT`, you can also write conditional selection statements:

``` cpp
#define PP_IF(if, then, else) PP_CONCAT(PP_IF_, PP_BOOL(if))(then, else)
#define PP_IF_1(then, else) then
#define PP_IF_0(then, else) else

PP_IF(1, 2, 3)      // -> PP_IF_1(2, 3) -> 2
PP_IF(0, 2, 3)      // -> PP_IF_0(2, 3) -> 3
```

If the value of `if` is `1`, concatenate it with `PP_CONCAT` to form `PP_IF_1` and finally expand it to the value of `then`; similarly, if the value of `if` is `0`, you get `PP_IF_0`.

####Increment and decrement

Integer increasing and decreasing:

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

Similar to `PP_BOOL`, the increment and decrement of integers also have limitations. Here, the range is set to `[0, 256]`. After reaching `256`, for safety reasons, `PP_INC_256` will return `256` itself as a boundary, similarly `PP_DEC_0` will return `0`.

####Variable-length parameters

Macro can accept variable-length arguments, the format is:

```cpp
#define LOG(format, ...) printf("log: " format, __VA_ARGS__)

LOG("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG("Hello World")              // -> printf("log: " "Hello World", ); A comma is missing, causing a compile error.
```

Due to the possibility of variadic arguments being empty, which could lead to compilation failure, C++ 20 introduced `__VA_OPT__`. If the variadic arguments are empty, it returns empty; otherwise, it returns the original arguments:

```cpp
#define LOG2(format, ...) printf("log: " format __VA_OPT__(,) __VA_ARGS__)

LOG2("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG2("Hello World") // -> printf("log: " "Hello World" ); No comma, compiles correctly
```

Unfortunately, this macro is only available in C++20 and later standards. In the following text, we will provide the implementation method for `__VA_OPT__`.

####Lazy evaluation.

Consider this situation:

``` cpp
PP_IF(1, PP_COMMA(), PP_LPAREN())     // -> PP_IF_1(,,)) -> Error: unterminated argument list invoking macro "PP_IF_1"
```

We know that when macros are expanded, the parameters are evaluated first. After evaluating `PP_COMMA()` and `PP_LPAREN()`, they are passed to `PP_IF_1`, resulting in `PP_IF_1(,,))`, which leads to a preprocessor error. At this point, a method called lazy evaluation can be employed:

``` cpp
PP_IF(1, PP_COMMA, PP_LPAREN)()       // -> PP_IF_1(PP_COMMA, PP_LPAREN)() -> PP_COMMA() -> ,
```

Change the writing style to only pass the macro's name. After `PP_IF` selects the required macro name, it is then concatenated with parentheses `()` to form a complete macro, and finally expanded. Lazy evaluation is also common in macro programming.

####Begins with a bracket.

Determine if the variable-length parameter starts with parentheses:

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

`PP_IS_BEGIN_PARENS` can be used to determine whether the incoming parameters start with parentheses. This is needed when dealing with parenthesized parameters (such as in the implementation of `__VA_OPT__` mentioned later). It may seem a bit complex, but the core idea is to construct a macro that, if the variable-length parameter starts with parentheses, can be evaluated together with the parentheses to yield one result; otherwise, it will be evaluated separately to yield another result. Let's dissect this gradually:

The macro formed by `PP_IS_BEGIN_PARENS_PROCESS` and `PP_IS_BEGIN_PARENS_PROCESS_0` functions to evaluate the incoming variable arguments first, and then take the 0th parameter.

`PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__)` first evaluates `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__`, and then concatenates the evaluation result with `PP_IS_BEGIN_PARENS_PRE_`.

The macro `PP_IS_BEGIN_PARENS_EAT(...)` will consume all arguments and return 1. If `__VA_ARGS__` in the previous step `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` starts with parentheses, it will match the evaluation of `PP_IS_BEGIN_PARENS_EAT(...)` and return 1; otherwise, if it does not start with parentheses, there will be no match, and `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` will remain unchanged.

If `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` evaluates to `1`, then `PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, 1) -> PP_IS_BEGIN_PARENS_PRE_1 -> 1`, note that there is a comma after `1`, pass `1,` to `PP_IS_BEGIN_PARENS_PROCESS_0`, retrieve the 0th argument, and finally obtain `1`, indicating that the argument begins with parentheses.

If `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` evaluates to something other than `1`, and remains unchanged, then `PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__) -> PP_IS_BEGIN_PARENS_PRE_PP_IS_BEGIN_PARENS_EAT __VA_ARGS__ -> 0, __VA_ARGS__`, passing this to `PP_IS_BEGIN_PARENS_PROCESS_0` results in `0`, indicating that the argument does not start with parentheses.

####Variable length parameter is empty

Determining whether the variable-length parameters are empty is also a commonly used macro, which is needed when implementing `__VA_OPT__`. Here, we can utilize `PP_IS_BEGIN_PARENS` to initially write an incomplete version:

``` cpp
#define PP_IS_EMPTY_PROCESS(...) \
    PP_IS_BEGIN_PARENS(PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ())
#define PP_IS_EMPTY_PROCESS_EAT(...) ()

PP_IS_EMPTY_PROCESS()       // -> 1
PP_IS_EMPTY_PROCESS(1)      // -> 0
PP_IS_EMPTY_PROCESS(1, 2)   // -> 0
PP_IS_EMPTY_PROCESS(())     // -> 1
```

The purpose of `PP_IS_EMPTY_PROCESS` is to determine whether `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ()` starts with a parenthesis.

If `__VA_ARGS__` is empty, `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ () -> PP_IS_EMPTY_PROCESS_EAT() -> ()`, we will get a pair of parentheses `()`. When passed to `PP_IS_BEGIN_PARENS`, it returns `1`, indicating that the argument is empty.

Otherwise, `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__()` is passed unchanged to `PP_IS_BEGIN_PARENS`, returning 0 to indicate non-empty.

Pay attention to the 4th example `PP_IS_EMPTY_PROCESS(()) -> 1`, `PP_IS_EMPTY_PROCESS` cannot handle variable arguments starting with parentheses correctly, as the parentheses brought by the variable arguments would match `PP_IS_EMPTY_PROCESS_EAT` and lead to `()`. To solve this issue, we need to treat cases where the argument starts with parentheses differently:

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

`PP_IS_EMPTY_IF` returns the 0th or 1st parameter based on the `if` condition.

If the variable-length arguments begin with parentheses, `PP_IS_EMPTY_IF` returns `PP_IS_EMPTY_ZERO`, and finally returns `0`, indicating that the variable-length arguments are not empty.

On the contrary, `PP_IS_EMPTY_IF` returns `PP_IS_EMPTY_PROCESS`, and ultimately `PP_IS_EMPTY_PROCESS` determines if the variable arguments are not empty.

####Subscript access

Access the element specified at a variable position in the variable-length parameter.

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

The first parameter of `PP_ARGS_ELEM` is the element index `I`, followed by variable-length parameters. By using `PP_CONCAT` to concatenate `PP_ARGS_ELEM_` and `I`, we can obtain the macro `PP_ARGS_ELEM_0..8` that returns the element at the corresponding position, and then pass the variable-length parameters to this macro to expand and return the element at the specified index.

#### PP_IS_EMPTY2

Using `PP_ARGS_ELEM` can also achieve another version of `PP_IS_EMPTY`:

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

Using `PP_ARGS_ELEM` to implement determining whether the parameter contains a comma `PP_HAS_COMMA`. `PP_COMMA_ARGS` will consume any incoming parameters and return a comma.

The basic logic for determining whether variadic arguments are empty is that `PP_COMMA_ARGS __VA_ARGS__ ()` returns a comma, which means `__VA_ARGS__` is empty. The `PP_COMMA_ARGS` is evaluated together with `()`, and the specific way to write this is `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ())`.

However, there may be exceptions:

`__VA_ARGS__` itself may contain commas;
`__VA_ARGS__()` concatenates and evaluates the values with commas.
Concatenating `PP_COMMA_ARGS __VA_ARGS__` results in the evaluation with a comma in between.

Regarding the three exceptions mentioned above, exclusions need to be made. Therefore, the final expression is equivalent to executing a logical conjunction on the following four conditions:

* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__))` &&
* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__()))` &&
* `PP_NOT(PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__))` &&
* `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ())`

#### `__VA_OPT__`

With the use of `PP_IS_EMPTY`, it is finally possible to implement macros similar to `__VA_OPT__`:

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

`PP_ARGS_OPT` accepts two fixed parameters and variable-length parameters. When the variable-length parameters are non-empty, it returns `data`; otherwise, it returns `empty`. To ensure that `data` and `empty` support commas, both must have their actual parameters enclosed in parentheses, and finally, `PP_REMOVE_PARENS` is used to remove the outer parentheses.

With `PP_ARGS_OPT`, it is possible to implement `LOG3` to simulate the functionality achieved by `LOG2`:

``` cpp
#define LOG3(format, ...) \
    printf("log: " format PP_ARGS_OPT((,), (), __VA_ARGS__) __VA_ARGS__)

LOG3("Hello");                  // -> printf("log: " "Hello" );
LOG3("Hello %s", "World");      // -> printf("log: " "Hello %s" , "World");
```

`data_tuple` is `(,)`, and if the variable-length arguments are not empty, it will return all elements in `data_tuple`, which in this case is the comma `,`.

####Request for the number of parameters.

Get the number of variable-length parameters:

``` cpp
#define PP_ARGS_SIZE_IMCOMPLETE(...) \
    PP_ARGS_ELEM(8, __VA_ARGS__, 8, 7, 6, 5, 4, 3, 2, 1, 0)

PP_ARGS_SIZE_IMCOMPLETE(a)             // -> 1
PP_ARGS_SIZE_IMCOMPLETE(a, b)          // -> 2
PP_ARGS_SIZE_IMCOMPLETE(PP_COMMA())    // -> 2
PP_ARGS_SIZE_IMCOMPLETE()              // -> 1
```

Calculating the number of variable-length arguments is determined by their positions. `__VA_ARGS__` causes all subsequent arguments to shift to the right. Use the macro `PP_ARGS_ELEM` to access the 8th argument position. If `__VA_ARGS__` has only one argument, then the 8th argument will be `1`. Similarly, if `__VA_ARGS__` has two arguments, then the 8th argument becomes `2`, which is equal to the number of variable-length arguments.

The examples provided here only support a maximum of 8 variable arguments, which depends on the maximum length supported by 'PP_ARGS_ELEM'.

However, this macro is not complete; in the case where the variable-length parameters are empty, it will incorrectly return `1`. If you need to handle empty variable-length parameters, you will need to use the `PP_ARGS_OPT` macro we mentioned earlier:

``` cpp
#define PP_COMMA_IF_ARGS(...) PP_ARGS_OPT((,), (), __VA_ARGS__)
#define PP_ARGS_SIZE(...) PP_ARGS_ELEM(8, __VA_ARGS__ PP_COMMA_IF_ARGS(__VA_ARGS__) 8, 7, 6, 5, 4, 3, 2, 1, 0, 0, 0)

PP_ARGS_SIZE(a)             // -> 1
PP_ARGS_SIZE(a, b)          // -> 2
PP_ARGS_SIZE(PP_COMMA())    // -> 2
PP_ARGS_SIZE()              // -> 0
PP_ARGS_SIZE(,,,)           // -> 4
```

The key issue lies in the comma `,` - by omitting the comma when `__VA_ARGS__` is empty, it will correctly return `0`.

####Traverse access

Similar to C++'s `for_each`, we can implement the macro `PP_FOR_EACH`:

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

`PP_FOR_EACH` takes two fixed parameters: `macro`, which can be understood as the macro called during the iteration, and `contex`, which can serve as a fixed value parameter passed to `macro`. `PP_FOR_EACH` first retrieves the length `N` of the variable-length parameters using `PP_ARGS_SIZE`, then concatenates to obtain `PP_FOR_EACH_N` using `PP_CONCAT`. After that, `PP_FOR_EACH_N` will iteratively call `PP_FOR_EACH_N-1` to achieve the same number of iterations as the count of the variable-length parameters.

In the example, we have declared `DECLARE_EACH` as a parameter for the `macro`. The purpose of `DECLARE_EACH` is to return `context arg`, where `context` is the type name and `arg` is the variable name. With `DECLARE_EACH`, we can declare variables.

####Conditional Loop

With the `FOR_EACH` in place, we can also use a similar approach to write `PP_WHILE`:

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

`PP_WHILE` accepts three parameters: `pred`, the condition checking function; `op`, the operation function; and `val`, the initial value. During the loop, it continuously uses `pred(val)` to perform the loop termination check and passes the value obtained from `op(val)` to the subsequent macros, which can be understood as executing the following code:

``` cpp
while (pred(val)) {
    val = op(val);
}
```

First, use `pred(val)` to obtain the condition evaluation result, then pass the condition result `cond` along with the remaining parameters to `PP_WHILE_N_IMPL`.
`PP_WHILE_N_IMPL` can be viewed in two parts: the latter part `(pred, op, PP_IF(cond, op, PP_EMPTY_EAT)(val))` serves as a parameter for the former part, where `PP_IF(cond, op, PP_EMPTY_EAT)(val)` evaluates `op(val)` if `cond` is true, and evaluates `PP_EMPTY_EAT(val)` to produce an empty result if `cond` is false. The first part `PP_IF(cond, PP_WHILE_N+1, val PP_EMPTY_EAT)` returns `PP_WHILE_N+1` if `cond` is true, allowing the loop to continue with the latter part's parameters; otherwise, it returns `val PP_EMPTY_EAT`, where `val` becomes the final calculated result, and `PP_EMPTY_EAT` will discard the result from the latter part.

The function `SUM` calculates `N + N-1 + ... + 1`. It starts with the values `(max_num, origin_num)`. `SUM_PRED` selects the first element `x` from the values, then checks if it is greater than 0. `SUM_OP` decrements `x` by 1 and adds this value to `y`, updating `y` as `y = y + x`. Pass `SUM_PRED` and `SUM_OP` directly to `PP_WHILE`, the returned result is a tuple, and we are interested in the second element of this tuple. To obtain this, use `SUM` to retrieve the value of the second element.

####Recursive reentry.

So far, our traversal access and conditional loops have been functioning well, and the results meet our expectations. Do you remember when we talked about the macro expansion rules and mentioned the prohibition of recursive reentry? Unfortunately, we encountered the prohibition of recursive reentry when we wanted to execute double loops.

``` cpp
#define SUM_OP2(xy_tuple) SUM_OP_OP_IMPL2 xy_tuple
#define SUM_OP_OP_IMPL2(x, y) (PP_DEC(x), y + SUM(x, 0))

#define SUM2(max_num, origin_num) \
    PP_IDENTITY(SUM_IMPL PP_WHILE(SUM_PRED, SUM_OP2, (max_num, origin_num)))

SUM2(1, a)      // -> a + SUM_IMPL PP_WHILE_1(SUM_PRED, SUM_OP, (1, a))
```

`SUM2` changes the parameter `op` to `SUM_OP2`, which will call `SUM` within `SUM_OP2`, and the expansion of `SUM` will still lead to `PP_WHILE_1`. This is equivalent to `PP_WHILE_1` recursively calling itself, causing the preprocessor to stop expanding.

To solve this problem, we can use a method of automatic recursion.

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

`PP_AUTO_WHILE` is the automatic inference recursive version of `PP_WHILE`, with the core macro being `PP_AUTO_REC(PP_WHILE_PRED)`, which can identify the current available number `N` of the `PP_WHILE_N` version.

The principle of deducing is quite simple. It involves searching through all versions to identify the one that can unfold correctly. Once found, it returns the number associated with that version. To boost the search speed, the usual approach is to employ binary search, which is precisely what `PP_AUTO_REC` does. `PP_AUTO_REC` takes a parameter called `check` responsible for verifying version availability. In this case, the supported search range is `[1, 4]`. Initially, `PP_AUTO_REC` examines `check(2)`. If it evaluates to true, it triggers `PP_AUTO_REC_12` to search within the range `[1, 2]`; otherwise, it will proceed with `PP_AUTO_REC_34` and explore `[3, 4]`. In the same manner, `PP_AUTO_REC_12` evaluates `check(1)`. When true, it means version `1` is available; otherwise, it defaults to version `2`. The process is mirrored in `PP_AUTO_REC_34`.

How should the `check` macro be written to determine if a version is available? Here, `PP_WHILE_PRED` will be expanded into two concatenated parts. Let's focus on the latter part `PP_WHILE_## n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`: if `PP_WHILE_## n` is available, since `PP_WHILE_FALSE` always returns `0`, this part will expand to the value of the `val` parameter, which is `PP_WHILE_FALSE`. Otherwise, this part of the macro will remain unchanged, still being `PP_WHILE_n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`.

Concatenate the results from the latter part with the prefix `PP_WHILE_CHECK_` to obtain two outcomes: `PP_WHILE_CHECK_PP_WHILE_FALSE` or `PP_WHILE_CHECK_PP_WHILE_n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`. Therefore, we set `PP_WHILE_CHECK_PP_WHILE_FALSE` to return `1` to indicate availability, while `PP_WHILE_CHECK_PP_WHILE_n` returns `0` to signify unavailability. With this, we have completed the functionality of automatic recursive inference.

####Arithmetic comparison

Not equal:

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

To determine whether two values are equal, a feature that prevents recursive re-entry is utilized. The values `x` and `y` are recursively concatenated into the `PP_NOT_EQUAL_x PP_NOT_EQUAL_y` macros. If `x == y`, the `PP_NOT_EQUAL_y` macro will not be expanded, resulting in `PP_NOT_EQUAL_CHECK_PP_NOT_EQUAL_y` returning `0`. Conversely, if both expansions succeed, the final outcome is `PP_EQUAL_NIL`, which concatenates to `PP_NOT_EQUAL_CHECK_PP_EQUAL_NIL`, returning `1`.

Equality:

``` cpp
#define PP_EQUAL(x, y) PP_NOT(PP_NOT_EQUAL(x, y))

PP_EQUAL(1, 1)              // -> 1
PP_EQUAL(1, 3)              // -> 0

```

Less than or equal to:

``` cpp
#define PP_LESS_EQUAL(x, y) PP_NOT(PP_SUB(x, y))

PP_LESS_EQUAL(2, 1)         // -> 0
PP_LESS_EQUAL(1, 1)         // -> 1
PP_LESS_EQUAL(1, 2)         // -> 1
```

Less than:

``` cpp
#define PP_LESS(x, y) PP_AND(PP_LESS_EQUAL(x, y), PP_NOT_EQUAL(x, y))

PP_LESS(2, 1)               // -> 0
PP_LESS(1, 2)               // -> 1
PP_LESS(2, 2)               // -> 0
```

Additionally, there are comparisons such as greater than, greater than or equal to, etc., which will not be elaborated on here.

####Arithmetic operation

Using `PP_AUTO_WHILE`, we can implement basic arithmetic operations and support nested operations.

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

Subtraction:

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

Multiplication:

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

The multiplication implementation here has added a parameter `ret`, initialized to `0`, which will execute `ret = ret + x` in each iteration.

Division:

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

Division utilizes `PP_LESS_EQUAL`, only continuing the loop when `y <= x`.

####Data Structure

Macros can also have data structures. In fact, we have already touched on a type of data structure called `tuple` earlier. `PP_REMOVE_PARENS` is a macro that can remove the outer parentheses of a `tuple` and return its elements. Here, we will take `tuple` as an example to discuss the related implementations. For other data structures like `list`, `array`, etc., you can refer to the implementations in `Boost` if you're interested.

A `tuple` is defined as a collection of elements separated by commas and enclosed in parentheses: `(a, b, c)`.

``` cpp
#define PP_TUPLE_REMOVE_PARENS(tuple) PP_REMOVE_PARENS(tuple)

Get the element at the specified index.
#define PP_TUPLE_ELEM(i, tuple) PP_ARGS_ELEM(i, PP_TUPLE_REMOVE_PARENS(tuple))

Swallowing the entire tuple returns empty.
#define PP_TUPLE_EAT() PP_EMPTY_EAT

Get size
#define PP_TUPLE_SIZE(tuple) PP_ARGS_SIZE(PP_TUPLE_REMOVE_PARENS(tuple))

// Add elements
#define PP_TUPLE_PUSH_BACK(elem, tuple) \
    PP_TUPLE_PUSH_BACK_IMPL(PP_TUPLE_SIZE(tuple), elem, tuple)
#define PP_TUPLE_PUSH_BACK_IMPL(size, elem, tuple) \
    (PP_TUPLE_REMOVE_PARENS(tuple) PP_IF(size, PP_COMMA, PP_EMPTY)() elem)

// Insert element
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

Remove the last element.
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

// Delete element
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

Here’s a brief explanation of the implementation of inserting elements; similar principles are applied to other operations like deleting elements. `PP_TUPLE_INSERT(i, elem, tuple)` can insert the element `elem` at position `i` in the `tuple`. To accomplish this, we first use `PP_TUPLE_PUSH_BACK` to place all elements with positions less than `i` into a new `tuple` (referred to as `ret`). Then, we insert the element `elem` at position `i`, and finally, we add all elements from the original `tuple` with positions greater than or equal to `i` to the back of `ret`. In the end, `ret` contains the result we desire.

##Summary

(https://github.com/pfultz2/Cloak/wiki/C-Preprocessor-tricks,-tips,-and-idioms#deferred-expression)In BOOST_PP, the macros related to `REPEAT`, among others, can be referenced in available materials for those who are interested.

Debugging macro programming is a painful process, we can:

Output the preprocessed result using the `-P -E` option.
Carefully studying the unfolding process using the self-modified version of `clang` mentioned earlier.
* Break down complex macros and examine the expansion results of the intermediate macros;
Filter out irrelevant header files and macros;
* Finally, you need to visualize the macro expansion process; after becoming familiar with macro expansion, your debugging efficiency will also improve.

The macros in this article are my own reimplementation after understanding the principles. Some of the macros draw inspiration from the implementation of `Boost` and the articles referenced within. If there are any mistakes, please feel free to point them out, and I'm open to discussing related issues.

All the code for this article is available here: [Download](assets/img/2021-3-31-cpp-preprocess/macros.cpp),[Online Demo](https://godbolt.org/z/coWvc5Pse)。

##Quote

* [Boost.Preprocessor](https://www.boost.org/doc/libs/1_75_0/libs/preprocessor/doc/)
* [The Art of C/C++ Macro Programming](https://bot-man-jl.github.io/articles/?post=2020/Macro-Programming-Art)

--8<-- "footer_en.md"


> This post was translated using ChatGPT, please provide feedback in [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Please point out any omissions. 
