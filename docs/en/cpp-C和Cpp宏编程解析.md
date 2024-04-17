---
layout: post
title: C/C++ Macro Programming Analysis
categories:
- c++
catalog: true
tags:
- dev
description: The purpose of this article is to explain the rules and implementation
  methods of C/C++ macro programming, so that you will no longer be afraid when encountering
  macros in code.
figures: []
---

<meta property="og:title" content="C/C++ 宏编程解析" />

The purpose of this article is to explain the rules and implementation methods of macro programming in C/C++, so that you no longer fear seeing macros in code. I will first talk about the macro expansion rules mentioned in C++ Standard 14, and then observe macro expansion by modifying Clang's source code. Finally, based on this knowledge, we will discuss the implementation of macro programming.

All the code for this document is available here: [Download](assets/img/2021-3-31-cpp-preprocess/macros.cpp), [Online Demo](https://godbolt.org/z/coWvc5Pse).

##Introduction

We can use the command `gcc -P -E a.cpp -o a.cpp.i` to make the compiler only perform preprocessing on the file `a.cpp` and save the results to `a.cpp.i`.

First, let's take a look at some examples:

####Recursive Reentrancy

``` cpp
#define ITER(arg0, arg1) ITER(arg1, arg0)

ITER(1, 2)          // -> ITER(2, 1)
```

Macro `ITER` swaps the positions of `arg0` and `arg1`. After Macro expansion, it becomes `ITER(2, 1)`.

It can be seen that the positions of `arg0` and `arg1` have been successfully swapped. Here, the macro is expanded once and only once, without further recursion. In other words, during the macro expansion process, it is not allowed to recursively re-enter itself. If it is found that the same macro has already been expanded in a previous recursion, it will not be expanded again. This is one of the important rules of macro expansion. The reason for prohibiting recursive re-entry is also simple, which is to avoid infinite recursion.

####String concatenation

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                // -> HelloWorld
CONCAT(Hello, CONCAT(World, !))     // ->　HelloCONCAT(World, !)
```

The purpose of the macro `CONCAT` is to concatenate `arg0` and `arg1`. After expansion, `CONCAT(Hello, World)` gives the correct result `HelloWorld`. However, `CONCAT(Hello, CONCAT(World, !))` only expands the outer macro, and the inner `CONCAT(World, !)` is not expanded but concatenated directly with `Hello`, which is different from what we expected. The desired result is `HelloWorld!`. This is another important rule of macro expansion: macro parameters following the `##` operator are not expanded, but directly concatenated with the preceding content.

Through the two examples above, it can be seen that there are some counterintuitive rules for macro expansion. If we are not clear about the specific rules, it is possible to write macros that do not produce the desired effect.

##Expansion rules

Through the two examples in the preamble, we learned that macro expansion has a set of standard rules. These rules are defined in the C/C++ standard and are not extensive in content. It is recommended to read them carefully a few times. By the way, here is a link to the standard n4296 version that includes the definition of macro expansion in section 16.3: [Link](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4296.pdf). Below, I have selected several important rules from the n4296 version, which will determine how to correctly write macros (I recommend taking the time to carefully read and expand the macros in the standard).

####Parameter Separation

The requirements for macro parameters are to be separated by commas, and the number of parameters needs to match the number of macro definitions. In the parameters passed to the macro, any content enclosed in parentheses is considered as one parameter, and parameters are allowed to be empty.

``` cpp
#define ADD_COMMA(arg1, arg2) arg1, arg2

ADD_COMMA(a, b)             // -> a, b
ADD_COMMA(a)                // Error: "macro "MACRO" requires 2 arguments, but only 1 given"
ADD_COMMA((a, b), c)        // -> (a, b), c
ADD_COMMA(, b)              // -> , b
```

In the expression `ADD_COMMA((a, b), c)`, `(a, b)` is considered the first argument. In `ADD_COMMA(, b)`, the first argument is empty, so it expands to `, b`.

####Macro parameter expansion

When expanding macros, if the parameters of the macro can also be expanded macros, the parameters will be fully expanded first before expanding the macro. For example,

``` cpp
ADD_COMMA(ADD_COMMA(1, 2), ADD_COMMA(3, 4))     // -> 1, 2, 3, 4
```

In general, the expansion of macros can be understood as evaluating the parameters first, and then evaluating the macros, unless the `#` and `##` operators are encountered.

####`#` Operator

`#` The macro parameter following the operator will not be expanded, it will be directly converted into a string, for example:

``` cpp
#define STRINGIZE(arg0) # arg0

STRINGIZE(a)                // -> "a"
STRINGIZE(STRINGIZE(a))     // -> "STRINGIZE(a)"
```

According to this rule, `STRINGIZE(STRINGIZE(a))` can only be expanded as `"STRINGIZE(a)"`.

###### Operators

## Macro parameters before and after the operator will not be expanded, they will be directly concatenated, for example:

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                        // -> HelloWorld
CONCAT(Hello, CONCAT(World, !))             // -> HelloCONCAT(World, !)
CONCAT(CONCAT(Hello, World) C, ONCAT(!))    // -> CONCAT(Hello, World) CONCAT(!)
```

`CONCAT(CONCAT(Hello, World) C, ONCAT(!))` can only be concatenated together to obtain `CONCAT(Hello, World) CONCAT(!)`.

####Repetition scanning

After the preprocessor completes one macro expansion, it will re-scan the resulting content and continue expanding it until there is no more content to expand.

A macro expansion can be understood as first fully expanding the parameters (unless encountering `#` and `##`), then replacing the macro and fully expanded parameters according to the definition of the macro, and finally handling all `#` and `##` operators in the definition.

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define STRINGIZE(arg0) # arg0

CONCAT(STRING, IZE(Hello))        // -> STRINGIZE(Hello) -> "Hello"
```

`CONCAT(STRING, IZE(Hello))` is expanded to `STRINGIZE(Hello)` during the first scan, and then it goes through the second scan. `STRINGIZE` is further expanded, resulting in `"Hello"`.

####No recursive reentrant calls allowed.

During the process of repeated scanning, it is forbidden to recursively expand the same macro. The expansion of macros can be understood as a tree-like structure, where the root node is the macro to be expanded initially, and the content after each macro expansion becomes a child node connected to the tree. Therefore, prohibiting recursion means that when expanding a child node macro, if it is the same as any ancestor node macro, expansion is prohibited. Let's look at some examples:

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define CONCAT_SPACE(arg0, arg1) arg0 arg1
#define IDENTITY(arg0) IDENTITY_IMPL(arg0)
#define IDENTITY_IMPL(arg0) arg0

CONCAT(CON, CAT(a, b))                  // -> CONCAT(a, b)
IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))   // -> CONCAT(a, b)
IDENTITY(CONCAT(CON, CAT(a, b)))        // -> IDENTITY_IMPL(CONCAT(a, b)) -> CONCAT(a, b)
```

`CONCAT(CON, CAT(a, b))`: Since `CONCAT` concatenates two parameters using `##`, according to the rules of `##`, the parameters will not be expanded, but directly concatenated. So the first expansion results in `CONCAT(a, b)`. Since `CONCAT` has already been expanded, it will not be recursively expanded again, so it stops.

`IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))`: `IDENTITY_IMPL` can be understood as evaluating the argument `arg0`. In this case, the argument `arg0` evaluates to `CONCAT(a, b)`. Since it is marked as non-reentrant due to recursion, `IDENTITY_IMPL` completes its expansion. During the second scan, it encounters the non-reentrant `CONCAT(a, b)` and stops expanding. Here, `CONCAT(a, b)` is expanded from the argument `arg0`. However, in subsequent expansions, the non-reentrant marking is maintained, which means that the parent node is the argument `arg0` and the non-reentrant marking is always preserved.

`IDENTITY(CONCAT(CON, CAT(a, b)))`: This example is primarily designed to enhance the understanding of parent-child nodes. When the parameter is expanded, it acts as the parent node, with the expanded content serving as the child node for recursive evaluation. Once the expanded parameter is passed to the macro definition, the flag for prohibiting reentry will continue to be retained (if the expanded macro does not alter the passed parameter). The process of expanding the parameter can be likened to another tree, with the expansion result of the parameter being the bottommost child node of the tree. This child node is passed to the macro for execution, while still preserving the characteristic of prohibiting reentry.

For example, here, after the first complete expansion, we obtain `IDENTITY_IMPL(CONCAT(a, b))`. `CONCAT(a, b)` is marked as non-reentrant, even though `IDENTITY_IMPL` evaluates its arguments. Since the arguments are prohibited from expanding, they are passed as they are into the definition, and we ultimately get `CONCAT(a, b)`.

Above I just listed some rules that I think are more important or rules that I find difficult to understand. For detailed macro expansion rules, I still recommend taking some time to directly refer to the standard documentation.

##Observe the expansion process through Clang.

We can add some print statements to the Clang source code to observe the macro expansion process. I have no intention of delving into the explanation of the Clang source code here. Here is a modified file diff, for those who are interested, you can compile Clang yourself for research. Here I used LLVM version 11.1.0 ([link](https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-11.1.0.tar.gz)），modified file ([link](assets/img/2021-3-31-cpp-preprocess/clang-modify.zip)}). Next, let's verify the macro expansion rules we introduced earlier through some simple examples:

####Example 1

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(C, ONCAT(a, b))      // CONCAT(a, b)
```

Preprocess the above code using a modified version of Clang: `clang -P -E a.cpp -o a.cpp.i`. The following printout is obtained:

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

Chapter [1](#__codelineno-9-1)When the `HandleIdentifier` function encounters a macro, it will print and then print the macro information (line [2-4](#__codelineno-9-2)(Macro is ok to expand), since macros are not disabled, we can proceed to expand the defined macros, `EnterMacro`.

The function that actually performs the macro expansion is `ExpandFunctionArguments`. After that, the macro information to be expanded is printed again, noting that the macro is now marked as `used` (line [9](#__codelineno-9-9)After that, according to the definition of the macro, expand each `Token` one by one (a `Token` is a concept in the `Clang` preprocessor, which will not be elaborated here).

The 0th `Token` is the formal parameter `arg0`, and its corresponding actual argument is `C`. Since no expansion is required for the condition, it is directly copied to the result (lines [11-13](#__codelineno-9-11)行）。

(End).

The first `Token` is `hashhash`, which is the `##` operator, continue copying it to the result (from [14-15](#__codelineno-9-14)(Line).

(#__codelineno-9-16)行）。
行）.

Finally, `Leave ExpandFunctionArguments` prints the result obtained from expanding the scan this time (page [19](#__codelineno-9-19)In the code snippet above, the `Token` that represents the result is translated as `C##ONCAT(a, b)`. Then, the preprocessor executes the `##` operator to generate a new content.

After executing, we get `CONCAT(a, b)`. When encountering the macro `CONCAT`, the preprocessor still enters the `HandleIdentifier` first. The macro information is printed and it is found that the macro status is `disable used`, indicating that it has already been expanded and re-entry is prohibited. The message "Macro is not ok to expand" is displayed. The preprocessor no longer expands, and the final result obtained is `CONCAT(a, b)`.

####Example 2

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define IDENTITY(arg0) arg0

IDENTITY(CONCAT(C, ONCAT(a, b)))
```

<details>
<summary> <font> Clang print information (click to expand): </font> </summary>
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

[12](#__codelineno-11-12)Start by expanding `IDENTITY`. We discover that the `Token 0` parameter is `CONCAT(...)`, which is also a macro. Therefore, we evaluate this parameter first.

Chapter [27](#__codelineno-11-27)Start expanding the parameter macro `CONCAT(...)` as in example 1. After multiple scans of expansion, it results in `CONCAT(a, b)` (the 46th [46](#__codelineno-11-46)(行).

Chapter [47](#__codelineno-11-47)End the expansion of `IDENTITY` and obtain the result `CONCAT(a, b)`.

[51](#__codelineno-11-51)Re-scan `CONCAT(a, b)` and it is found that although it is a macro, it has already been set as `used` during the previous parameter expansion process. It will no longer be recursively expanded and will directly serve as the final result.

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

* Chapter [16](#__codelineno-13-16)When processing starts, the preprocessor sees that `IDENTITY` is being expanded. Similarly, when it encounters `Token 2` (which is `arg0`), being a macro, it first expands `CONCAT(C, ONCAT(a, b))`.

Expand `arg0` to obtain `CONCAT(a, b)` (page [23-54](#__codelineno-13-23)行）

* `IDENTITY` ultimately expands to `IDENTITY_IMPL(CONCAT(a, b))` (page [57](#__codelineno-13-57)(行)

* Rescan, continue expanding `IDENTITY_IMPL` (from [61-72](#__codelineno-13-61)(#__codelineno-13-85)行）。

(End of line).

Re-scanning the results, it was found that the status of the macro `CONCAT(a, b)` is `used`, so the expansion is stopped and the final result is obtained.

By using the three simple examples above, we can roughly understand the process of macro expansion by the preprocessor. We won't delve further into the preprocessor here, but if you're interested, you can study it by comparing the modified files I provided.

##Macro programming implementation

Now let's move on to the topic (the previous paragraph was meant to provide a better understanding of macro expansion rules), macro programming implementation.

####Basic Symbols

First, you can define the special symbols of macros, which will be used for evaluation and concatenation.

``` cpp
#define PP_LPAREN() (
#define PP_RPAREN() )
#define PP_COMMA() ,
#define PP_EMPTY()
#define PP_HASHHASH # ## #      // Represents the string "##", without being treated as the ## operator
```

####Evaluate

Using the rule of parameter precedence, you can write an evaluation macro:

``` cpp
#define PP_IDENTITY(arg0) arg0

PP_COMMA PP_LPAREN() PP_RPAREN()                // -> PP_COMMA ( )
PP_IDENTITY(PP_COMMA PP_LPAREN() PP_RPAREN())   // -> PP_COMMA() -> ,
```

If you only write `PP_COMMA PP_LPAREN() PP_RPAREN()`, the preprocessor will only process each macro separately, and will not merge the results of the expansion. With the addition of `PP_IDENTITY`, the preprocessor can evaluate the expanded `PP_COMMA()` to obtain `,`.


####Splicing

Due to the fact that when `##` is used for concatenation, it does not expand the parameters on both sides, in order to allow the parameters to be evaluated before concatenation, you can write it like this:

``` cpp
#define PP_CONCAT(arg0, arg1) PP_CONCAT_IMPL(arg0, arg1)
#define PP_CONCAT_IMPL(arg0, arg1) arg0 ## arg1

PP_CONCAT(PP_IDENTITY(1), PP_IDENTITY(2))         // -> 12
`PP_CONCAT_IMPL(PP_IDENTITY(1), PP_IDENTITY(2))    // -> PP_IDENTITY(1)PP_IDENTITY(2) -> 报错`

`PP_CONCAT_IMPL(PP_IDENTITY(1), PP_IDENTITY(2))    // -> PP_IDENTITY(1)PP_IDENTITY(2) -> Error`
```

The method used here by `PP_CONCAT` is called delayed concatenation. When it is expanded as `PP_CONCAT_IMPL`, both `arg0` and `arg1` will be expanded and evaluated first, and then the actual concatenation operation will be performed by `PP_CONCAT_IMPL`.

####Logical Operations

With the help of `PP_CONCAT`, logical operations can be achieved. First, define the `BOOL` value:


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

First, use `PP_CONCAT` to concatenate `PP_BOOL_` and `arg0` together, and then evaluate the concatenated result. Here, `arg0` is required to be a number within the range of `[0, 256]` after evaluation. By evaluating the concatenation after `PP_BOOL_`, we can obtain a boolean value. This applies to logical AND, OR, and NOT operations:

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

First, evaluate the parameter using `PP_BOOL`, and then concatenate the results of logical operations based on the combination of `0` and `1`. If `PP_BOOL` is not used for evaluation, the parameter will only support the two values `0` and `1`, greatly reducing its versatility. Similarly, you can also write XOR, OR, NOT operations. If interested, you can try it yourself.

####Conditional selection

By utilizing `PP_BOOL` and `PP_CONCAT`, it is also possible to write conditional selection statements:

``` cpp
#define PP_IF(if, then, else) PP_CONCAT(PP_IF_, PP_BOOL(if))(then, else)
#define PP_IF_1(then, else) then
#define PP_IF_0(then, else) else

PP_IF(1, 2, 3)      // -> PP_IF_1(2, 3) -> 2
PP_IF(0, 2, 3)      // -> PP_IF_0(2, 3) -> 3
```

If the evaluation of `if` is `1`, it is concatenated with `PP_CONCAT` to form `PP_IF_1`, and finally expanded to the value of `then`. Similarly, if the evaluation of `if` is `0`, `PP_IF_0` is obtained.

####Increment and decrement.

Integer Increment and Decrement:

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

Similar to `PP_BOOL`, the increment and decrement of integers are also subject to range restrictions. Here, the range is set to `[0, 256]`. After reaching `256` during the increment operation, for safety reasons, `PP_INC_256` returns itself as the boundary value (`256`). Similarly, `PP_DEC_0` returns `0`.

####Variable-length parameters

Macros can accept variable-length parameters, in the following format:

```cpp
#define LOG(format, ...) printf("log: " format, __VA_ARGS__)

LOG("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG("Hello World")  // -> printf("log: " "Hello World", ); There is an extra comma, causing a compilation error.
```

Because variable-length parameters may be empty, this can lead to compilation failure. Therefore, C++ 20 introduced `__VA_OPT__`. If the variable-length parameters are empty, it returns empty; otherwise, it returns the original parameters:

```cpp
#define LOG2(format, ...) printf("log: " format __VA_OPT__(,) __VA_ARGS__)

LOG2("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG2("Hello World")              // -> printf("log: " "Hello World" ); No comma, compiles normally
```

But unfortunately, only standard C++ 20 and above have this macro. In the following sections, we will provide the implementation method of `__VA_OPT__`.

####Lazy evaluation

Consider this situation:

``` cpp
PP_IF(1, PP_COMMA(), PP_LPAREN())     // -> PP_IF_1(,,)) -> Error: unterminated argument list invoking macro "PP_IF_1"
```

We know that when macro expansion occurs, the first parameter is evaluated. After evaluating `PP_COMMA()` and `PP_LPAREN()`, they are passed to `PP_IF_1`, resulting in `PP_IF_1(,,))`, causing a preprocessing error. At this time, we can use a method called lazy evaluation:

``` cpp
PP_IF(1, PP_COMMA, PP_LPAREN)()       // -> PP_IF_1(PP_COMMA, PP_LPAREN)() -> PP_COMMA() -> ,
```

Change it to this writing method, only pass the name of the macro, let `PP_IF` select the desired macro name, then concatenate it with parentheses `()` to form a complete macro, and finally expand it. Lazy evaluation is also very common in macro programming.

####Start with parentheses.

Check if the variable length parameters start with parentheses:

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

`PP_IS_BEGIN_PARENS` can be used to determine whether the incoming parameters start with parentheses. It is needed when dealing with parentheses parameters (like the `__VA_OPT__` implementation mentioned later). It looks a bit complicated, but the core idea is to construct a macro. If the variable-length parameters start with parentheses, they can be evaluated together with the parentheses to obtain one result. Otherwise, they can be evaluated separately to obtain another result. Let's take a closer look:

The macro composed of `PP_IS_BEGIN_PARENS_PROCESS` and `PP_IS_BEGIN_PARENS_PROCESS_0` is used to first evaluate the variable-length arguments that are passed in, and then retrieve the 0-th argument.

Translate these text into English language:

`PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__)` is evaluating `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` first, then concatenating the evaluation result with `PP_IS_BEGIN_PARENS_PRE_`.

The `PP_IS_BEGIN_PARENS_EAT(...)` macro will consume all its parameters and return 1. If in the previous step, `__VA_ARGS__` begins with parentheses, it will match the evaluation of `PP_IS_BEGIN_PARENS_EAT(...)`, and then return 1. Conversely, if it does not begin with parentheses, there will be no match, and `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` will remain unchanged.

If `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` evaluates to `1`,  `PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, 1) -> PP_IS_BEGIN_PARENS_PRE_1 -> 1`, note that there is a comma after `1`, pass `1, ` to `PP_IS_BEGIN_PARENS_PROCESS_0`, take the 0th argument, and finally obtain `1`, which indicates that the parameter is starting with parentheses.

If `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` evaluates to something other than `1`, but remains unchanged, then `PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__) -> PP_IS_BEGIN_PARENS_PRE_PP_IS_BEGIN_PARENS_EAT __VA_ARGS__ -> 0, __VA_ARGS__`, passed to `PP_IS_BEGIN_PARENS_PROCESS_0`, will result in `0`, indicating that the argument does not begin with parentheses.

####Variadic parameter void

Judging whether the variable-length parameter is empty is also a commonly used macro, which is needed when implementing `__VA_OPT__`. Here, we can use `PP_IS_BEGIN_PARENS` to write an incomplete version first:

``` cpp
#define PP_IS_EMPTY_PROCESS(...) \
    PP_IS_BEGIN_PARENS(PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ())
#define PP_IS_EMPTY_PROCESS_EAT(...) ()

PP_IS_EMPTY_PROCESS()       // -> 1
PP_IS_EMPTY_PROCESS(1)      // -> 0
PP_IS_EMPTY_PROCESS(1, 2)   // -> 0
PP_IS_EMPTY_PROCESS(())     // -> 1
```

The function of `PP_IS_EMPTY_PROCESS` is to determine whether `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ()` begins with parentheses.

If `__VA_ARGS__` is empty, `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ () -> PP_IS_EMPTY_PROCESS_EAT() -> ()`, it results in a pair of parentheses `()`, which is then passed to `PP_IS_BEGIN_PARENS` returning `1`, indicating that the argument is empty.

Otherwise, `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ()` is passed unchanged to `PP_IS_BEGIN_PARENS`, which returns 0 indicating non-empty.

Pay attention to the 4th example `PP_IS_EMPTY_PROCESS(()) -> 1`, `PP_IS_EMPTY_PROCESS` cannot handle variable arguments that start with parentheses correctly, because in this case, the parentheses brought by the variable arguments will match `PP_IS_EMPTY_PROCESS_EAT`, resulting in the evaluation of `()`. To solve this problem, we need to handle the case where the arguments start with parentheses differently:

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

`PP_IS_EMPTY_IF` returns the 0th or 1st argument based on the `if` condition.

If the variable-length parameters passed in start with parentheses, `PP_IS_EMPTY_IF` returns `PP_IS_EMPTY_ZERO`, and finally returns `0`, indicating that the variable-length parameters are not empty.

On the contrary, `PP_IS_EMPTY_IF` returns `PP_IS_EMPTY_PROCESS`, and finally `PP_IS_EMPTY_PROCESS` is responsible for determining whether the variable-length parameters are empty.

####Subscript access

Get the element at the specified position in a variable-length parameter:

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

The first argument of `PP_ARGS_ELEM` is the index `I`, followed by a variable number of arguments. By using `PP_CONCAT` to concatenate `PP_ARGS_ELEM_` and `I`, we can obtain the macro `PP_ARGS_ELEM_0..8` that returns the element at the respective position. Then we pass the variable arguments to this macro, expanding it to return the element corresponding to the index.

#### PP_IS_EMPTY2

You can also achieve another version of `PP_IS_EMPTY` by using `PP_ARGS_ELEM`:

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

Use `PP_ARGS_ELEM` to implement the judgement of whether the argument contains a comma `PP_HAS_COMMA`. `PP_COMMA_ARGS` will consume any passed arguments and return a comma.

The basic logic to determine if the variable-length parameters are empty is `PP_COMMA_ARGS __VA_ARGS__ ()`, which returns a comma, meaning `__VA_ARGS__` is empty. `PP_COMMA_ARGS` and `()` are concatenated and evaluated together, specifically written as `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ())`.

But there will be exceptions:

The `__VA_ARGS__` itself may contain commas.
* `__VA_ARGS__ ()` concatenates the arguments causing an evaluation with a comma.
* `PP_COMMA_ARGS __VA_ARGS__` concatenates and evaluates with a comma occurring in-between;

In order to address the three exceptional scenarios mentioned above, exclusions need to be made. Therefore, the final expression is equivalent to executing the AND logic on the following four conditions:

* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__))` &&
* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__()))` &&
* `PP_NOT(PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__))` &&
* `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ())`

#### `__VA_OPT__`

Finally, with the help of `PP_IS_EMPTY`, it is possible to implement macros similar to `__VA_OPT__`.

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

`PP_ARGS_OPT` accepts two fixed parameters and a variable number of parameters. If the variable parameters are not empty, it returns `data`; otherwise, it returns `empty`. To support commas in `data` and `empty`, both need to be enclosed in parentheses with the actual parameters, and finally use `PP_REMOVE_PARENS` to remove the outer parentheses.

With `PP_ARGS_OPT`, it is possible to achieve the functionality of `LOG2` through the simulation of `LOG3`.

``` cpp
#define LOG3(format, ...) \
    printf("log: " format PP_ARGS_OPT((,), (), __VA_ARGS__) __VA_ARGS__)

LOG3("Hello");                  // -> printf("log: " "Hello" );
LOG3("Hello %s", "World");      // -> printf("log: " "Hello %s" , "World");
```

`data_tuple` is `(,)`. If the variable-length argument is not empty, it will return all the elements in `data_tuple`, which in this case is a comma `,`.

####Number of parameters needed

Obtaining the quantity of variable arguments:

``` cpp
#define PP_ARGS_SIZE_IMCOMPLETE(...) \
    PP_ARGS_ELEM(8, __VA_ARGS__, 8, 7, 6, 5, 4, 3, 2, 1, 0)

PP_ARGS_SIZE_IMCOMPLETE(a)             // -> 1
PP_ARGS_SIZE_IMCOMPLETE(a, b)          // -> 2
PP_ARGS_SIZE_IMCOMPLETE(PP_COMMA())    // -> 2
PP_ARGS_SIZE_IMCOMPLETE()              // -> 1
```

The number of variable-length parameters is obtained by counting the positions of the parameters. `__VA_ARGS__` will cause all subsequent parameters to shift to the right. Use the macro `PP_ARGS_ELEM` to retrieve the parameter in the 8th position. If `__VA_ARGS__` only has one parameter, then the 8th parameter is equal to `1`. Similarly, if `__VA_ARGS__` has two parameters, then the 8th parameter will be `2`, which conveniently represents the number of variable-length parameters.

The examples given here only support a maximum number of 8 variable arguments, which is dependent on the maximum length supported by `PP_ARGS_ELEM`.

But this macro is still incomplete. In the case where the variable argument is empty, this macro will mistakenly return `1`. If you need to handle empty variable arguments, you will need to use the `PP_ARGS_OPT` macro we mentioned earlier.

``` cpp
#define PP_COMMA_IF_ARGS(...) PP_ARGS_OPT((,), (), __VA_ARGS__)
#define PP_ARGS_SIZE(...) PP_ARGS_ELEM(8, __VA_ARGS__ PP_COMMA_IF_ARGS(__VA_ARGS__) 8, 7, 6, 5, 4, 3, 2, 1, 0, 0, 0)

PP_ARGS_SIZE(a)             // -> 1
PP_ARGS_SIZE(a, b)          // -> 2
PP_ARGS_SIZE(PP_COMMA())    // -> 2
PP_ARGS_SIZE()              // -> 0
PP_ARGS_SIZE(,,,)           // -> 4
```

The key issue here is the comma `,`. When `__VA_ARGS__` is empty, removing the comma will enable the correct return value of `0`.

####Traversal Access

Similar to C++ `for_each`, we can implement the macro `PP_FOR_EACH`:

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

`PP_FOR_EACH` accepts two fixed parameters: `macro`, which can be understood as the macro called during iteration, and `contex`, which can be passed as a constant parameter to `macro`. First, `PP_FOR_EACH` uses `PP_ARGS_SIZE` to obtain the length `N` of the variable-length parameters, and then concatenates it with `PP_CONCAT` to obtain `PP_FOR_EACH_N`. Afterwards, `PP_FOR_EACH_N` will iteratively call `PP_FOR_EACH_N-1` to achieve the same number of iterations as the number of variable-length parameters.

In the example, we declare `DECLARE_EACH` as a `macro` parameter. The purpose of `DECLARE_EACH` is to return `contex arg`, where `contex` is the name of a type and `arg` is the name of a variable. By using `DECLARE_EACH`, we can declare variables.

####Conditional loop

With `FOR_EACH`, we can also use a similar syntax to write `PP_WHILE`:

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

The `PP_WHILE` macro accepts three parameters: `pred` as the condition evaluation function, `op` as the operation function, and `val` as the initial value. During the looping process, the termination condition is continuously checked using `pred(val)`. The value obtained from `op(val)` is passed to the subsequent macros, which can be understood as executing the following code:

``` cpp
while (pred(val)) {
    val = op(val);
}
```

`PP_WHILE_N` first uses `pred(val)` to obtain the condition evaluation result, and then passes the condition result `cond` and the remaining parameters to `PP_WHILE_N_IMPL`.
The `PP_WHILE_N_IMPL` can be divided into two parts: the latter half `(pred, op, PP_IF(cond, op, PP_EMPTY_EAT)(val))` is used as the parameter for the former half, and `PP_IF(cond, op, PP_EMPTY_EAT)(val)` evaluates `op(val)` if `cond` is true, otherwise it evaluates `PP_EMPTY_EAT(val)` to obtain an empty result. The former half, `PP_IF(cond, PP_WHILE_N+1, val PP_EMPTY_EAT)`, returns `PP_WHILE_N+1` if `cond` is true, and continues the loop by combining it with the parameters of the latter half. Otherwise, it returns `val PP_EMPTY_EAT`, where `val` becomes the final result, and `PP_EMPTY_EAT` consumes the result of the latter half.

`SUM` implements `N + N-1 + ... + 1`. The initial values are `(max_num, origin_num)`; `SUM_PRED` takes the first element of the value, `x`, and checks if it is greater than 0; `SUM_OP` performs the decrement operation on `x`, `x = x - 1`, and the addition operation on `y`, `y = y + x`. We directly pass `SUM_PRED` and `SUM_OP` to `PP_WHILE`, and the result returned is a tuple. The desired result is the second element of the tuple, so we then use `SUM` to retrieve the value of the second element.

####Recursive reentry

So far, our traversal visits and conditional loops have been working well and producing the expected results. Do you remember when we mentioned the prohibition of recursive reentry when discussing macro expansion rules? Unfortunately, we have encountered this prohibition of recursive reentry when we wanted to perform nested loops.

``` cpp
#define SUM_OP2(xy_tuple) SUM_OP_OP_IMPL2 xy_tuple
#define SUM_OP_OP_IMPL2(x, y) (PP_DEC(x), y + SUM(x, 0))

#define SUM2(max_num, origin_num) \
    PP_IDENTITY(SUM_IMPL PP_WHILE(SUM_PRED, SUM_OP2, (max_num, origin_num)))

SUM2(1, a)      // -> a + SUM_IMPL PP_WHILE_1(SUM_PRED, SUM_OP, (1, a))
```

`SUM2` changes the parameter `op` to `SUM_OP2`, and inside `SUM_OP2`, it will call `SUM`, and the expansion of `SUM` will be `PP_WHILE_1`, which is effectively a recursive call to itself. This causes the preprocessor to stop expanding.

To solve this problem, we can use a method called Automatic Recursion:

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

`PP_AUTO_WHILE` is the automatically deduced recursive version of `PP_WHILE`, and the central macro is `PP_AUTO_REC(PP_WHILE_PRED)`. This macro can determine the current available `PP_WHILE_N` version number, `N`.

The principle of deduction is very simple, it is to search all versions and find the version that can be correctly expanded, returning the number of that version. In order to improve the speed of the search, the usual practice is to use binary search, which is what `PP_AUTO_REC` is doing. `PP_AUTO_REC` accepts a parameter called `check`, which is responsible for checking the availability of versions. Here, the supported range of versions to be searched is given as `[1, 4]`. `PP_AUTO_REC` will first check `check(2)`. If `check(2)` is true, it will call `PP_AUTO_REC_12` to search the range `[1, 2]`; otherwise, it will use `PP_AUTO_REC_34` to search `[3, 4]`. `PP_AUTO_REC_12` checks `check(1)`. If it is true, it means version `1` is available; otherwise, version `2` is used. Similarly, `PP_AUTO_REC_34` operates.

To write the `check` macro and determine whether the version is available, how should we do it? Here, `PP_WHILE_PRED` will be expanded into two parts of concatenation. Let's take a look at the latter part, `PP_WHILE_ ## n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`: if `PP_WHILE_ ## n` is available, since `PP_WHILE_FALSE` always returns `0`, this part will be expanded to obtain the value of the `val` parameter, which is `PP_WHILE_FALSE`; otherwise, this macro will remain unchanged and still be `PP_WHILE_n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`.

Join the result of the back section with the front section `PP_WHILE_CHECK_`, and obtain two possible results: `PP_WHILE_CHECK_PP_WHILE_FALSE` or `PP_WHILE_CHECK_PP_WHILE_n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`. Therefore, we let `PP_WHILE_CHECK_PP_WHILE_FALSE` return `1` to indicate availability, and `PP_WHILE_CHECK_PP_WHILE_n` return `0` to indicate unavailability. With this, we have completed the functionality of automatic recursive deduction.

####Arithmetic Comparison

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

The judgment of whether two values are equal utilizes the feature of prohibiting recursive reentry. It combines `x` and `y` recursively to form the macro `PP_NOT_EQUAL_x PP_NOT_EQUAL_y`. If `x == y`, the macro `PP_NOT_EQUAL_y` will not be expanded, and it will be concatenated with `PP_NOT_EQUAL_CHECK_` to form `PP_NOT_EQUAL_CHECK_PP_NOT_EQUAL_y` which returns `0`. On the other hand, if both expansions are successful, `PP_EQUAL_NIL` will be obtained and concatenated with `PP_NOT_EQUAL_CHECK_` to form `PP_NOT_EQUAL_CHECK_PP_EQUAL_NIL`, which returns `1`.

Equal:

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

In addition, there are arithmetic comparisons like "greater than" and "greater than or equal to," among others. I won't go into detail about them here.

####Arithmetic operations

With `PP_AUTO_WHILE`, we can achieve basic arithmetic operations and even nested calculations.

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

The multiplication implementation here adds a parameter `ret`, initialized to `0`, and each iteration executes `ret = ret + x`.

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

Division utilizes `PP_LESS_EQUAL`, so the loop continues only if `y <= x`.

####Data structures

Macros can also have data structures. In fact, we have already used a data structure called `tuple` earlier, where `PP_REMOVE_PARENS` can remove the outer parentheses of a `tuple` and return its elements. We will use `tuple` as an example here to discuss the relevant implementation. If you are interested in other data structures such as `list`, `array`, etc., you can check out the implementation in `Boost`.

A `tuple` is defined as a collection of elements enclosed in parentheses and separated by commas: `(a, b, c)`.

``` cpp
#define PP_TUPLE_REMOVE_PARENS(tuple) PP_REMOVE_PARENS(tuple)

// Get the element at the specified index
#define PP_TUPLE_ELEM(i, tuple) PP_ARGS_ELEM(i, PP_TUPLE_REMOVE_PARENS(tuple))

// Swallow the entire tuple and return empty
#define PP_TUPLE_EAT() PP_EMPTY_EAT

// Get size
#define PP_TUPLE_SIZE(tuple) PP_ARGS_SIZE(PP_TUPLE_REMOVE_PARENS(tuple))

// Add Element
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

// Delete the last element
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

// Remove Element
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

Let me briefly explain the implementation of inserting elements here. Similar principles are also used to implement other operations such as deleting elements. `PP_TUPLE_INSERT(i, elem, tuple)` can insert element `elem` at position `i` in `tuple`. To complete this operation, we first use `PP_TUPLE_PUSH_BACK` to put all elements smaller than position `i` onto a new `tuple` called `ret`. Then we place element `elem` at position `i`, and later we place all the elements in the original `tuple` that are larger than or equal to position `i` after `ret`. Finally, `ret` will be the desired result.

##Summary

(https://github.com/pfultz2/Cloak/wiki/C-Preprocessor-tricks,-tips,-and-idioms#deferred-expression), the relevant macros inside `BOOST_PP REPEAT` and so on, those who are interested can search for information on their own.

Debugging macro programming is a painful process, and there are several things we can do to make it easier:

Use the `-P -E` options to output the preprocessing results.
Examine the expanding process in detail using the modified `clang` version mentioned earlier.
* Break down complex macros and examine the expansion results of intermediate macros;
* Exclude unnecessary header files and macros;
* Finally, there is the process of mentally simulating macro expansion. Once familiar with macro expansion, the efficiency of debugging will also improve.

The macros mentioned in this text are my own implementation after understanding the principles. Some of the macros are inspired by the implementation and references in Boost articles. If there are any mistakes, please feel free to point them out at any time. I am also open to discussing related issues with you.

All the code for this document is available here: [Download](assets/img/2021-3-31-cpp-preprocess/macros.cpp),[Online Demo](https://godbolt.org/z/coWvc5Pse).

##> Quote

* [Boost.Preprocessor](https://www.boost.org/doc/libs/1_75_0/libs/preprocessor/doc/)
* [The Art of C/C++ Macro Programming](https://bot-man-jl.github.io/articles/?post=2020/Macro-Programming-Art)

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki_blog/issues/new) if any omissions.
