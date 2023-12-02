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

The purpose of this text is to explain the rules and implementation methods of macro programming in C/C++, so that you no longer fear seeing macros in code. First, I will talk about the rules for macro expansion mentioned in C++ standard 14, then observe macro expansion by modifying Clang's source code, and finally discuss the implementation of macro programming based on this knowledge.

The code for this article is available here: [Download](assets/img/2021-3-31-cpp-preprocess/macros.cpp), [Online Demo](https://godbolt.org/z/coWvc5Pse).

## Introduction

We can execute the command `gcc -P -E a.cpp -o a.cpp.i` to instruct the compiler to perform only the preprocessing stage on the file `a.cpp` and save the result to `a.cpp.i`.

First, let's look at some examples:

#### Recursive Reentrancy (递归重入)

``` cpp
#define ITER(arg0, arg1) ITER(arg1, arg0) 

ITER(1, 2)          // -> ITER(2, 1)
```

Macro `ITER` swaps the positions of `arg0` and `arg1`. After expanding the macro, we get `ITER(2, 1)`.

It can be seen that the positions of `arg0` and `arg1` are successfully swapped here. The macro is expanded successfully once here, but only once, without further recursive re-entry. In other words, during the expansion process of the macro, it is not allowed to recursively re-enter itself. If it is found that the same macro has been expanded in a previous recursion, it will not be expanded again. This is one of the important rules of macro expansion. The reason for prohibiting recursive re-entry is also very simple, which is to avoid infinite recursion.

#### String Concatenation

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                // -> HelloWorld
CONCAT(Hello, CONCAT(World, !))     // ->　HelloCONCAT(World, !)

CONCAT(Hello, CONCAT(World, !))     // ->　HelloCONCAT(World, !)
```

The macro `CONCAT` is designed to concatenate `arg0` and `arg1`. After expanding the macro, `CONCAT(Hello, World)` will yield the correct result `HelloWorld`. However, when we use `CONCAT(Hello, CONCAT(World, !))`, only the outer macro is expanded, and the inner `CONCAT(World, !)` is not expanded but directly concatenated with `Hello`. This is different from what we expected. The desired result should be `HelloWorld!`. This is another important rule of macro expansion: macro arguments following the `##` operator will not be expanded, but will be directly concatenated with the preceding content.

Through the above two examples, it can be seen that there are some counter-intuitive rules for macro expansion. If the specific rules are not clear, it is possible to write macros that do not achieve the desired effect.

## Macro Expansion Rules

Through the two examples in the preface, we have learned that macro expansion follows a set of standard rules, which are defined in the C/C++ standard. The content is not extensive, but I recommend reading it carefully a few times. Here, I also provide a link to the n4296 version of the standard, where macro expansion is discussed in Section 16.3: [Link](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4296.pdf). Now, let me highlight a few important rules from the n4296 version. These rules will determine how to correctly write macros (I still suggest taking the time to thoroughly read about macro expansion in the standard).

#### Parameter Separation

The parameters of the macro should be separated by commas, and the number of parameters should match the number of macro definitions. In the parameters passed to the macro, any content enclosed in parentheses is considered as one parameter, and parameters are allowed to be empty.

``` cpp
#define ADD_COMMA(arg1, arg2) arg1, arg2

ADD_COMMA(a, b)             // -> a, b
ADD_COMMA(a)                // Error: "macro 'MACRO' requires 2 arguments, but only 1 given"
ADD_COMMA((a, b), c)        // -> (a, b), c
ADD_COMMA(, b)              // -> , b
```

In the expression `ADD_COMMA((a, b), c)`, `(a, b)` is considered as the first argument. In `ADD_COMMA(, b)`, the first argument is empty, so it expands to `, b`.

#### Macro Parameter Expansion

When expanding a macro, if the macro's parameters are also macros that can be expanded, the parameters will be fully expanded first before expanding the macro itself. For example:

``` cpp
ADD_COMMA(ADD_COMMA(1, 2), ADD_COMMA(3, 4))     // -> 1, 2, 3, 4
```

In general, macro expansion can be understood as evaluating the arguments first, and then evaluating the macro, unless encountering the `#` and `##` operators.

#### `#` Operator

`#` The macro parameter followed by the operator will not be expanded, but will be directly stringized. For example:

``` cpp
#define STRINGIZE(arg0) # arg0

STRINGIZE(a)                // -> "a"
STRINGIZE(STRINGIZE(a))     // -> "STRINGIZE(a)"
```

According to this rule `STRINGIZE(STRINGIZE(a))` can only be expanded to `"STRINGIZE(a)"`.

#### `##` Operator

`##` Macro parameters before and after the `##` operator will not be expanded, they will be directly concatenated. For example:

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                        // -> HelloWorld
CONCAT(Hello, CONCAT(World, !))             // -> HelloCONCAT(World, !)
CONCAT(CONCAT(Hello, World) C, ONCAT(!))    // -> CONCAT(Hello, World) CONCAT(!)
```

`CONCAT(CONCAT(Hello, World) C, ONCAT(!))` can only be concatenated first to obtain `CONCAT(Hello, World) CONCAT(!)`.

#### Repeat Scanning

After the preprocessor completes one round of macro expansion, it will rescan the resulting content and continue to expand it until there is no further expansion possible.

One-level macro expansion can be understood as first fully expanding the parameters (unless encountering `#` and `##`), then based on the macro definition, replacing the macro and fully expanded parameters according to the definition, and then processing all `#` and `##` operators in the definition.

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define STRINGIZE(arg0) # arg0

CONCAT(STRING, IZE(Hello))        // -> STRINGIZE(Hello) -> "Hello"
```

`CONCAT(STRING, IZE(Hello))` is expanded to `STRINGIZE(Hello)` during the first scan, and then during the second scan it is found that `STRINGIZE` can be further expanded, resulting in `"Hello"`.

#### Recursion Reentry Prohibited

In the process of repeated scanning, it is prohibited to recursively expand the same macros. The expansion of macros can be understood as a tree-like structure, where the root node is the macro to be expanded initially. The content after expanding each macro serves as a child node connected to the tree. Therefore, prohibiting recursion means that when expanding the macros of the child nodes, if any of these macros are the same as any ancestor node's macro, the expansion is prohibited. Let's take a look at some examples:

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define CONCAT_SPACE(arg0, arg1) arg0 arg1
#define IDENTITY(arg0) IDENTITY_IMPL(arg0)
#define IDENTITY_IMPL(arg0) arg0

CONCAT(CON, CAT(a, b))                  // -> CONCAT(a, b)
IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))   // -> CONCAT(a, b)
IDENTITY(CONCAT(CON, CAT(a, b)))        // -> IDENTITY_IMPL(CONCAT(a, b)) -> CONCAT(a, b)
```

`CONCAT(CON, CAT(a, b))`: Since `CONCAT` concatenates two arguments using `##`, according to the rules of `##`, the arguments will not be expanded and will be concatenated directly. Therefore, the first expansion results in `CONCAT(a, b)`. Since `CONCAT` has already been expanded, it will not be expanded recursively, and the process stops.

`IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))`: `IDENTITY_IMPL` can be understood as evaluating the argument `arg0`. Here, the argument `arg0` is evaluated as `CONCAT(a, b)`. Because it is marked as non-reentrant due to recursion, the expansion of `IDENTITY_IMPL` is completed, and during the second scan, it is found that `CONCAT(a, b)` is non-reentrant, so the expansion stops. In this case, `CONCAT(a, b)` is obtained by expanding the argument `arg0`, and during subsequent expansions, it will also maintain the non-reentrant flag. It can be understood that the parent node is the argument `arg0` and it always maintains the non-reentrant flag.

`IDENTITY(CONCAT(CON, CAT(a, b)))`: This example is mainly intended to enhance understanding of parent and child nodes. When the parameters are expanded, the self is regarded as the parent node, and the expanded content is treated as the child node for recursive evaluation. After the expanded parameters are passed to the macro definition, the indication of non-reentrancy will continue to be retained (if the macro does not modify the expanded parameters after being passed). The expansion process of the parameters can be likened to another tree, and the result of parameter expansion is the bottom-most child node of the tree. This child node, when passed to the macro for execution, still maintains the non-reentrant characteristic.

For example, here, after the first complete expansion, `IDENTITY_IMPL(CONCAT(a, b))` is obtained. `CONCAT(a, b)` is marked as non-reentrant, even though `IDENTITY_IMPL` evaluates its arguments, but the arguments have been forbidden to expand, so the arguments are passed unchanged into the definition, and in the end, we still get `CONCAT(a, b)`.

The above is just a list of some rules that I think are important or that may be difficult to understand. For detailed macro expansion rules, I recommend taking some time to directly read the standard documentation.

## Observing the expansion process through Clang

We can add some print statements to the Clang source code to observe the process of macro expansion. I don't intend to deeply explain the Clang source code here. Instead, I provide a modified file diff for those interested, who can compile Clang themselves for further study. The version of LLVM I used here is 11.1.0 ([link](https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-11.1.0.tar.gz)). You can find the modified files [here](assets/img/2021-3-31-cpp-preprocess/clang-modify.zip). Now let's validate the macro expansion rules we previously introduced through some examples.

#### Example 1

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(C, ONCAT(a, b))      // CONCAT(a, b)
```

Use the modified Clang to preprocess the above code: `clang -P -E a.cpp -o a.cpp.i`, and you will get the following output:

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

In the `[1](#__codelineno-9-1)` line, when `HandleIdentifier` encounters a macro, it will print and then print the macro information (lines `[2-4](#__codelineno-9-2)`). Since the macro is not disabled, it can be expanded as defined, and then enter the macro `EnterMacro`.

The function that actually performs macro expansion is `ExpandFunctionArguments`. Afterwards, the macro information to be expanded is printed again, noting that at this point the macro has been marked as `used` (line [9](#__codelineno-9-9)). Then, according to the definition of the macro, each `Token` is expanded individually (`Token` is a concept in Clang preprocessing, which will not be explained in detail here).

The 0th `Token` is the formal parameter `arg0`, which corresponds to the actual argument `C`. It is determined that no expansion is needed, so it is directly copied to the result (line 11-13).

The first `Token` is `hashhash`, which is the `##` operator, continue to copy it to the result (lines [14-15](#__codelineno-9-14)).

The second `Token` is the formal parameter `arg1`, and its corresponding actual argument is `ONCAT(a, b)`. The preprocessor will also process the actual argument into individual `Tokens`, so you can see that the printed result is surrounded by brackets, representing each `Token` of the actual argument (line 18). Due to the usage of `##`, this actual argument does not need to be expanded, so it is directly copied to the result (lines [16-18](#__codelineno-9-16)).

Finally, `Leave ExpandFunctionArguments` prints the result obtained from expanding the scan this time (line [19](#__codelineno-9-19)). Translating all the `Token` results gives us `C ## ONCAT(a, b)`, and then the preprocessor executes the `##` operator to generate new content.

`##` After execution, we obtain `CONCAT(a, b)`. When encountering the macro `CONCAT`, the preprocessor enters `HandleIdentifier` first and prints the information of the macro. It's found that the macro state is "disable used", indicating that it has already been expanded and further re-entry is prohibited. Thus, the message "Macro is not ok to expand" is displayed. The preprocessor stops expanding and the final result is `CONCAT(a, b)`.

#### Example 2

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define IDENTITY(arg0) arg0

IDENTITY(CONCAT(C, ONCAT(a, b)))
```

<details>
<summary> <font>Clang Print Information (Click to expand):</font> </summary>
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

Start expanding `IDENTITY` from line [12](#__codelineno-11-12), and it is found that the parameter `Token 0` is `CONCAT(...)`, which is also a macro. Therefore, the evaluation of this parameter is performed first.

The parameter macro `CONCAT(...)` starts to expand from line [27](#__codelineno-11-27), similar to example 1. After multiple scans of expansion, `CONCAT(a, b)` is obtained (line [46](#__codelineno-11-46)).

Finish expanding `IDENTITY` at [47](#__codelineno-11-47) and obtain the result `CONCAT(a, b)`.

Redefine line [51](#__codelineno-11-51) to rescan `CONCAT(a, b)`. It is recognized as a macro, but it has already been set as `used` during the previous parameter expansion process. Therefore, it will no longer be recursively expanded and will be directly used as the final result.

#### Example 3

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define IDENTITY_IMPL(arg0) arg0
#define IDENTITY(arg0) IDENTITY_IMPL(arg0)

IDENTITY(CONCAT(C, ONCAT(a, b)))
```

<details>
<summary> <font>Clang Print Information (Click to expand):</font> </summary>
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

The expansion of `IDENTITY` begins at line [16](#__codelineno-13-16), similarly, the preprocessor sees that `Token 2` (i.e., `arg0`) is a macro, so it expands `CONCAT(C, ONCAT(a, b))` first.

Expand `arg0` to get `CONCAT(a, b)` (lines [23-54](#__codelineno-13-23)).

* `IDENTITY` eventually expands to `IDENTITY_IMPL(CONCAT(a, b))` (line [57](#__codelineno-13-57)).

Re-scan and continue expanding `IDENTITY_IMPL` (lines [61-72](#__codelineno-13-61)), it is found that `Token 0` at this point is the macro `CONCAT(a, b)`, but it is in the `used` state. Stop expanding and return (lines 75-84), and the final result is still `CONCAT(a, b)` (line [85](#__codelineno-13-85)).

Rescan the results and find that the status of the macro `CONCAT(a, b)` is `used`. Stop expansion and obtain the final result.

Through the above three simple examples, we can roughly understand the process of macro expansion by the preprocessor. There will be no further discussion on the preprocessor here. If you are interested, you can study it by referring to the modified files I have provided.

## Macro Programming Implementation

Next, let's move on to the main topic (the purpose of the lengthy previous paragraph was to provide a better understanding of macro expansion rules). Macro programming implementation.

#### Basic Symbols

First, let's define the special symbols for macros, which will be used for evaluation and concatenation purposes.

``` cpp
#define PP_LPAREN() (
#define PP_RPAREN() )
#define PP_COMMA() ,
#define PP_EMPTY() 
#define PP_HASHHASH # ## #      // Represents the string "##", but only as a string, it will not be treated as the ## operator
```

#### Evaluate

By utilizing the rule of parameter expansion, it is possible to write a macro for evaluation:

``` cpp
#define PP_IDENTITY(arg0) arg0

PP_COMMA PP_LPAREN() PP_RPAREN()                // -> PP_COMMA ( )
PP_IDENTITY(PP_COMMA PP_LPAREN() PP_RPAREN())   // -> PP_COMMA() -> ,
```

If you simply write `PP_COMMA PP_LPAREN() PP_RPAREN()`, the preprocessor will only process each macro separately and will not merge the results of expansion. By adding `PP_IDENTITY`, the preprocessor can evaluate the expanded result of `PP_COMMA()` to obtain `,`.


#### Concatenate

To ensure that the parameters are evaluated before concatenation when using `##`, you can write it like this:

``` cpp
#define PP_CONCAT(arg0, arg1) PP_CONCAT_IMPL(arg0, arg1)
#define PP_CONCAT_IMPL(arg0, arg1) arg0 ## arg1

PP_CONCAT(PP_IDENTITY(1), PP_IDENTITY(2))         // -> 12
PP_CONCAT_IMPL(PP_IDENTITY(1), PP_IDENTITY(2))    // -> PP_IDENTITY(1)PP_IDENTITY(2) -> Error
```

The method used here by `PP_CONCAT` is called delayed concatenation. When expanded to `PP_CONCAT_IMPL`, both `arg0` and `arg1` are first expanded and evaluated before being concatenated by `PP_CONCAT_IMPL` for the actual concatenation operation.

#### Logical Operations

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

Use `PP_CONCAT` to concatenate `PP_BOOL_` and `arg0` together, then evaluate the concatenated result. Here, `arg0` needs to be a number in the range of `[0, 256]` after evaluation. By evaluating it after concatenating with `PP_BOOL_`, a boolean value can be obtained. The operations include logical AND, OR, and NOT:

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

First, evaluate the parameter using `PP_BOOL`, and then concatenate the results of logical operations based on the combination of `0` and `1`. If `PP_BOOL` is not used for evaluation, the parameter will only support the values `0` and `1`, greatly reducing its usability. Similarly, you can also write operations such as XOR, OR, and NOT. If you are interested, you can try it yourself.

#### Conditions Selection

By using `PP_BOOL` and `PP_CONCAT`, we can also write conditional selection statements:

``` cpp
#define PP_IF(if, then, else) PP_CONCAT(PP_IF_, PP_BOOL(if))(then, else)
#define PP_IF_1(then, else) then
#define PP_IF_0(then, else) else

PP_IF(1, 2, 3)      // -> PP_IF_1(2, 3) -> 2
PP_IF(0, 2, 3)      // -> PP_IF_0(2, 3) -> 3
```

If the evaluation of `if` is `1`, it is concatenated with `PP_CONCAT` to form `PP_IF_1`, and finally expands to the value of `then`. Similarly, if the evaluation of `if` is `0`, it results in `PP_IF_0`.

#### Increment and Decrement

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

Similar to `PP_BOOL`, the increment and decrement of integers also have range restrictions. Here, the range is set to `[0, 256]`. After reaching `256`, for safety reasons, `PP_INC_256` will return itself `256` as the boundary. Similarly, `PP_DEC_0` will also return `0`.

#### Variable-length arguments

Macros can accept variable-length parameters in the following format:

```cpp 
#define LOG(format, ...) printf("log: " format, __VA_ARGS__)

LOG("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG("Hello World") // -> printf("log: " "Hello World", ); An extra comma is added, resulting in a compilation error.
```

Due to the possibility of variable-length parameters being empty, their emptiness can lead to compilation failures. Therefore, C++ 20 introduced `__VA_OPT__`. If the variable-length parameters are empty, it will return empty; otherwise, it will return the original parameters.

```cpp 
#define LOG2(format, ...) printf("log: " format __VA_OPT__(,) __VA_ARGS__)

LOG2("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG2("Hello World")              // -> printf("log: " "Hello World" ); No comma, compiles normally
```

Unfortunately, this macro is only available in the C++ 20 standard or higher. In the following text, we will provide the implementation method for `__VA_OPT__`.

#### Lazy Evaluation

Consider this situation:

``` cpp
PP_IF(1, PP_COMMA(), PP_LPAREN())     // -> PP_IF_1(,,)) -> Error: unterminated argument list invoking macro "PP_IF_1"
```

We know that when macro expansion occurs, the initial arguments are evaluated. After the evaluation of `PP_COMMA()` and `PP_LPAREN()`, the result is then passed to `PP_IF_1` as `PP_IF_1(,,))`, resulting in a preprocessing error. In this situation, a method called lazy evaluation can be used.

``` cpp
PP_IF(1, PP_COMMA, PP_LPAREN)()       // -> PP_IF_1(PP_COMMA, PP_LPAREN)() -> PP_COMMA() -> ,
```

Change it to this writing style, only pass the name of the macro. Let `PP_IF` select the necessary macro name, then concatenate it with parentheses `()` to form a complete macro, and finally expand it. Lazy evaluation is also common in macro programming.

#### Starts with a bracket

Check if the variable-length parameters start with parentheses:

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

The `PP_IS_BEGIN_PARENS` can be used to determine if the incoming parameter starts with parentheses. It is useful when dealing with parentheses parameters, as mentioned later with the `__VA_OPT__` implementation. It may seem a bit complex, but the main idea is to construct a macro that evaluates a certain result when the variadic parameters start with parentheses and a different result when they don't. Let's take a closer look:

The macro formed by `PP_IS_BEGIN_PARENS_PROCESS` and `PP_IS_BEGIN_PARENS_PROCESS_0` is used to evaluate the variadic arguments that are passed in, and then retrieve the 0th argument.

Translate these text into English language:

`PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__)` is first evaluated by applying `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__`, then the evaluation result is concatenated with `PP_IS_BEGIN_PARENS_PRE_`.

The macro `PP_IS_BEGIN_PARENS_EAT(...)` will consume all its arguments and return 1. If in the previous step, `__VA_ARGS__` starts with parentheses, it will match the evaluation of `PP_IS_BEGIN_PARENS_EAT(...)`, and then return 1. On the other hand, if it does not start with parentheses, it will not match and `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` will remain unchanged.

If `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` evaluates to `1`, `PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, 1) -> PP_IS_BEGIN_PARENS_PRE_1 -> 1,` note that there is a comma after `1`, pass `1,` to `PP_IS_BEGIN_PARENS_PROCESS_0`, take the 0th argument, and finally obtain `1`, indicating that the argument starts with parentheses.

If `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` evaluates to something other than `1`, but remains unchanged, then `PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__) -> PP_IS_BEGIN_PARENS_PRE_PP_IS_BEGIN_PARENS_EAT __VA_ARGS__ -> 0, __VA_ARGS__` is passed to `PP_IS_BEGIN_PARENS_PROCESS_0` and yields `0`, indicating that the argument does not begin with parentheses.

#### Variable-length parameter null

To determine if variable arguments are empty is also a common macro, which is required when implementing `__VA_OPT__`. Here we can utilize `PP_IS_BEGIN_PARENS` to write an incomplete version:

``` cpp
#define PP_IS_EMPTY_PROCESS(...) \
    PP_IS_BEGIN_PARENS(PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ())
#define PP_IS_EMPTY_PROCESS_EAT(...) ()

PP_IS_EMPTY_PROCESS()       // -> 1
PP_IS_EMPTY_PROCESS(1)      // -> 0
PP_IS_EMPTY_PROCESS(1, 2)   // -> 0
PP_IS_EMPTY_PROCESS(())     // -> 1
```

The purpose of `PP_IS_EMPTY_PROCESS` is to determine whether `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ()` starts with parentheses.

If `__VA_ARGS__` is empty, `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ () -> PP_IS_EMPTY_PROCESS_EAT() -> ()`, the result is a pair of parentheses `()`, which is then passed to `PP_IS_BEGIN_PARENS` to return `1`, indicating that the parameter is empty.

Otherwise, `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__()` passes unchanged to `PP_IS_BEGIN_PARENS`, returning 0 indicating non-empty.

Pay attention to the fourth example `PP_IS_EMPTY_PROCESS(()) -> 1`, `PP_IS_EMPTY_PROCESS` cannot handle variable-length arguments that start with parentheses correctly, because in this case the parentheses introduced by the variable-length arguments will match `PP_IS_EMPTY_PROCESS_EAT` and result in the evaluation of `()`. To solve this problem, we need to differentiate the cases where the arguments start with parentheses:

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

If the variable-length parameter passed in begins with parentheses, `PP_IS_EMPTY_IF` returns `PP_IS_EMPTY_ZERO`, and finally returns `0` to indicate that the variable-length parameter is not empty.

On the other hand, `PP_IS_EMPTY_IF` returns `PP_IS_EMPTY_PROCESS`, and finally `PP_IS_EMPTY_PROCESS` determines whether the variable-length parameter is empty.

#### Subscript Access

Accessing elements at specified positions in variable-length parameters:

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

The first argument of `PP_ARGS_ELEM` is the element index `I`, followed by a variable number of arguments. By using `PP_CONCAT` to concatenate `PP_ARGS_ELEM_` and `I`, we can obtain the macro `PP_ARGS_ELEM_0..8` that returns the element at the corresponding position. Then, pass the variable arguments to this macro to expand and return the element corresponding to the index.

#### PP_IS_EMPTY2

With `PP_ARGS_ELEM`, it is also possible to implement another version of `PP_IS_EMPTY`:

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

Use `PP_ARGS_ELEM` to implement the judgment of whether a parameter contains a comma `PP_HAS_COMMA`. `PP_COMMA_ARGS` will swallow any arguments passed in and return a comma.

The basic logic for determining whether a variable-length parameter is empty is `PP_COMMA_ARGS __VA_ARGS__ ()`, which returns a comma, indicating that `__VA_ARGS__` is empty. `PP_COMMA_ARGS` and `()` are concatenated and evaluated together, and the specific syntax is `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ())`.

However, there may be exceptions:

* `__VA_ARGS__` itself may bring commas;
* `__VA_ARGS__ ()` concatenates together causing comma during evaluation;
* `PP_COMMA_ARGS __VA_ARGS__` concatenates together causing comma during evaluation;

The above-mentioned three exceptional cases need to be excluded, so the final expression is equivalent to executing the logical AND operation on the following four conditions:

* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__))` &&
* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__()))` &&
* `PP_NOT(PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__))` &&
* `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ())`

#### `__VA_OPT__`

Finally, `PP_IS_EMPTY` can be used to implement macros similar to `__VA_OPT__`:

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

`PP_ARGS_OPT` accepts two fixed arguments and a variable number of arguments. When the variable arguments are not empty, it returns `data`; otherwise, it returns `empty`. To support commas in `data` and `empty`, both of them need to be enclosed in parentheses with actual arguments, and finally, `PP_REMOVE_PARENS` is used to remove the outer parentheses.

With `PP_ARGS_OPT`, it is possible to achieve the functionality implemented by `LOG2` using `LOG3`.

``` cpp
#define LOG3(format, ...) \
    printf("log: " format PP_ARGS_OPT((,), (), __VA_ARGS__) __VA_ARGS__)

LOG3("Hello");                  // -> printf("log: " "Hello" );
LOG3("Hello %s", "World");      // -> printf("log: " "Hello %s" , "World");
```

`data_tuple` is `(,)`, if the variable-length arguments are not empty, it will return all the elements in `data_tuple`, which in this case is the comma `,`.

#### Requesting the number of parameters

Get the number of variable arguments:

``` cpp
#define PP_ARGS_SIZE_IMCOMPLETE(...) \
    PP_ARGS_ELEM(8, __VA_ARGS__, 8, 7, 6, 5, 4, 3, 2, 1, 0)

PP_ARGS_SIZE_IMCOMPLETE(a)             // -> 1
PP_ARGS_SIZE_IMCOMPLETE(a, b)          // -> 2
PP_ARGS_SIZE_IMCOMPLETE(PP_COMMA())    // -> 2
PP_ARGS_SIZE_IMCOMPLETE()              // -> 1
```

The number of variable length parameters is obtained by counting the position of the parameters. `__VA_ARGS__` will cause all subsequent parameters to shift to the right. To retrieve the 8th positional parameter, use the macro `PP_ARGS_ELEM`. If `__VA_ARGS__` has only one parameter, then the 8th parameter is equal to `1`; similarly, if `__VA_ARGS__` has two parameters, then the 8th parameter becomes `2`, which coincidentally equals the number of variable length parameters.

The examples provided here only support a maximum number of 8 variable arguments, which depends on the maximum length supported by `PP_ARGS_ELEM`.

But this macro is not complete yet. In the case where the variable-length arguments are empty, this macro will incorrectly return `1`. If it is required to handle empty variable-length arguments, the `PP_ARGS_OPT` macro mentioned earlier needs to be used.

``` cpp
#define PP_COMMA_IF_ARGS(...) PP_ARGS_OPT((,), (), __VA_ARGS__)
#define PP_ARGS_SIZE(...) PP_ARGS_ELEM(8, __VA_ARGS__ PP_COMMA_IF_ARGS(__VA_ARGS__) 8, 7, 6, 5, 4, 3, 2, 1, 0, 0, 0)

PP_ARGS_SIZE(a)             // -> 1
PP_ARGS_SIZE(a, b)          // -> 2
PP_ARGS_SIZE(PP_COMMA())    // -> 2
PP_ARGS_SIZE()              // -> 0
PP_ARGS_SIZE(,,,)           // -> 4
```

The key issue lies in the comma `,` which, when `__VA_ARGS__` is empty, should be omitted in order to correctly return `0`.

#### Traversal Access

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

`PP_FOR_EACH` receives two fixed parameters: `macro`, which can be understood as the macro to be called during the iteration, and `context`, which can be passed as a fixed value parameter to `macro`. `PP_FOR_EACH` first obtains the length `N` of the variable arguments using `PP_ARGS_SIZE`, and then concatenates it with `PP_CONCAT` to obtain `PP_FOR_EACH_N`. Afterwards, `PP_FOR_EACH_N` iteratively calls `PP_FOR_EACH_N-1` to achieve the same number of iterations as the number of variable arguments.

In the example, we declare `DECLARE_EACH` as the `macro` parameter. The purpose of `DECLARE_EACH` is to return `contex arg`, where `contex` is the name of a type and `arg` is the name of a variable. `DECLARE_EACH` can be used to declare variables.

#### Conditional Loop

After having `FOR_EACH`, we can also write `PP_WHILE` using a similar syntax.

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

The `PP_WHILE` macro accepts three parameters: `pred` as the condition checking function, `op` as the operation function, and `val` as the initial value. During the loop, the termination condition is checked by continuously using `pred(val)`. The value obtained from `op(val)` is passed to the subsequent macro, which can be understood as executing the following code:

``` cpp
while (pred(val)) {
    val = op(val);
}
```

First use `pred(val)` to get the result of the condition check, and pass the condition result `cond` and the remaining parameters to `PP_WHILE_N_IMPL`.
`PP_WHILE_N_IMPL` can be divided into two parts: the latter part `(pred, op, PP_IF(cond, op, PP_EMPTY_EAT)(val))` is used as the parameter of the former part. `PP_IF(cond, op, PP_EMPTY_EAT)(val)` evaluates to `op(val)` if `cond` is true, otherwise it evaluates to `PP_EMPTY_EAT(val)` and returns empty. The former part `PP_IF(cond, PP_WHILE_N+1, val PP_EMPTY_EAT)` returns `PP_WHILE_N+1` if `cond` is true, and continues the loop by combining it with the parameters of the latter part; otherwise, it returns `val PP_EMPTY_EAT`, in which `val` is the final calculation result, and `PP_EMPTY_EAT` will consume the result of the latter part.

`SUM` implements `N + N-1 + ... + 1`. The initial values are `(max_num, origin_num)`. `SUM_PRED` takes the first element of the value, `x`, and checks if it is greater than 0. `SUM_OP` performs the decrement operation `x = x - 1` on `x` and the addition operation `y = y + x` on `y`. We can directly pass `SUM_PRED` and `SUM_OP` to `PP_WHILE`, and the returned result is a tuple. The desired result is the second element of the tuple, so we use `SUM` to retrieve the value of the second element.

#### Recursive Reentrancy

So far, our traversal access and conditional loops have been working well, producing the expected results. Do you remember when we mentioned the prohibition of recursive re-entry when discussing macro expansion rules? Unfortunately, we encountered this prohibition when attempting to execute nested loops.

``` cpp
#define SUM_OP2(xy_tuple) SUM_OP_OP_IMPL2 xy_tuple
#define SUM_OP_OP_IMPL2(x, y) (PP_DEC(x), y + SUM(x, 0))

#define SUM2(max_num, origin_num) \
    PP_IDENTITY(SUM_IMPL PP_WHILE(SUM_PRED, SUM_OP2, (max_num, origin_num)))

SUM2(1, a)      // -> a + SUM_IMPL PP_WHILE_1(SUM_PRED, SUM_OP, (1, a))
```

`SUM2` modifies the parameter `op` to use `SUM_OP2`. Within `SUM_OP2`, it will make a call to `SUM`, which, when expanded, will be equivalent to `PP_WHILE_1`. This means that `PP_WHILE_1` recursively calls itself until the preprocessor stops expansion.

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

`PP_AUTO_WHILE` is the automatically deduced recursive version of `PP_WHILE`, and the core macro is `PP_AUTO_REC(PP_WHILE_PRED)`. This macro can identify the current available version number `N` of `PP_WHILE_N`.

The principle of deduction is very simple, which is to search all versions and find the version that can be correctly expanded, and return the number of that version. In order to improve the speed of the search, the common practice is to use binary search, which is what `PP_AUTO_REC` does. `PP_AUTO_REC` takes a parameter `check`, which is responsible for checking the availability of versions. Here, the supported search version range is given as `[1, 4]`. `PP_AUTO_REC` will first check `check(2)`. If `check(2)` is true, it will call `PP_AUTO_REC_12` to search the range `[1, 2]`, otherwise it will use `PP_AUTO_REC_34` to search `[3, 4]`. `PP_AUTO_REC_12` checks `check(1)`. If it is true, it means that version `1` is available, otherwise version `2` is used. The same applies to `PP_AUTO_REC_34`.

To know whether the `check` macro is available, how should it be written? Here, the `PP_WHILE_PRED` will expand into the concatenation of two parts. Let's take a look at the latter part `PP_WHILE_ ## n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`: if `PP_WHILE_ ## n` is available, since `PP_WHILE_FALSE` always returns `0`, this part will expand and obtain the value of the `val` parameter, which is `PP_WHILE_FALSE`. Otherwise, this macro will remain unchanged and still be `PP_WHILE_n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`.

Concatenate the result of the latter part with the prefix `PP_WHILE_CHECK_`, resulting in two possible outcomes: `PP_WHILE_CHECK_PP_WHILE_FALSE` or `PP_WHILE_CHECK_PP_WHILE_n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`. We then make `PP_WHILE_CHECK_PP_WHILE_FALSE` return `1` to indicate availability, while `PP_WHILE_CHECK_PP_WHILE_n` returns `0` to indicate unavailability. With this, we have completed the functionality of automated recursive deduction.

#### Arithmetic Comparison

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

To determine if two values are equal, we utilize the feature of prohibiting recursive reentry. We concatenate `x` and `y` recursively into the `PP_NOT_EQUAL_x PP_NOT_EQUAL_y` macro. If `x` is equal to `y`, the `PP_NOT_EQUAL_y` macro will not be expanded, and it will be concatenated with `PP_NOT_EQUAL_CHECK_` to form `PP_NOT_EQUAL_CHECK_PP_NOT_EQUAL_y` which returns `0`. Conversely, if both are successfully expanded, we will ultimately obtain `PP_EQUAL_NIL`, which is then concatenated with `PP_NOT_EQUAL_CHECK_` to form `PP_NOT_EQUAL_CHECK_PP_EQUAL_NIL` which returns `1`.

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

In addition, there are arithmetic comparisons such as "greater than" and "greater than or equal to", etc. I will not go into further detail here.

#### Arithmetic Operations

Using `PP_AUTO_WHILE`, we can implement basic arithmetic operations, and it also supports nested operations.

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

To implement multiplication here, an additional parameter `ret` is added, with an initial value of `0`. During each iteration, the code executes `ret = ret + x`.

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

The division uses `PP_LESS_EQUAL`, and only continues the loop when `y <= x`.

#### Data Structures

Macro can also have data structures. In fact, we have briefly used a data structure called `tuple` in the previous section. `PP_REMOVE_PARENS` is used to remove the outer parentheses of `tuple` and return its elements. Here we take `tuple` as an example to discuss its implementation. If you are interested in other data structures like `list` and `array`, you can check out the implementation in `Boost`.

A `tuple` is defined as a collection of elements separated by commas and enclosed in parentheses: `(a, b, c)`.

``` cpp
#define PP_TUPLE_REMOVE_PARENS(tuple) PP_REMOVE_PARENS(tuple)

// Get the element at the specified index
#define PP_TUPLE_ELEM(i, tuple) PP_ARGS_ELEM(i, PP_TUPLE_REMOVE_PARENS(tuple))

// Swallow the entire tuple and return nothing
#define PP_TUPLE_EAT() PP_EMPTY_EAT

// Get size
#define PP_TUPLE_SIZE(tuple) PP_ARGS_SIZE(PP_TUPLE_REMOVE_PARENS(tuple))

// Add element
#define PP_TUPLE_PUSH_BACK(elem, tuple) \
    PP_TUPLE_PUSH_BACK_IMPL(PP_TUPLE_SIZE(tuple), elem, tuple)
#define PP_TUPLE_PUSH_BACK_IMPL(size, elem, tuple) \
    (PP_TUPLE_REMOVE_PARENS(tuple) PP_IF(size, PP_COMMA, PP_EMPTY)() elem)

// Insert Element
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

// Remove the last element
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

// Remove element
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

Here's a brief explanation of how the insertion of elements is implemented, similar principles are used for other operations such as deleting elements. `PP_TUPLE_INSERT(i, elem, tuple)` allows you to insert the element `elem` at position `i` in the `tuple`. To accomplish this, we first use `PP_TUPLE_PUSH_BACK` to move all elements with a position smaller than `i` onto a new `tuple` called `ret`. Then we place the element `elem` at position `i`, and finally move all the elements in the original `tuple` with positions greater than or equal to `i` to the end of `ret`. In the end, `ret` will contain the desired result.

## Summary

The purpose of this article is to clarify the principles and basic implementation of C/C++ macro programming, while recording my own understanding and knowledge, hoping to provide some clarification and inspiration to others. It should be noted that although this article is a bit long, there are still some macro programming techniques and usage that have not been covered, such as the [recursive calling method based on delayed expansion proposed by CHAOS_PP](https://github.com/pfultz2/Cloak/wiki/C-Preprocessor-tricks,-tips,-and-idioms#deferred-expression), and the `REPEAT` macro in BOOST_PP, etc. If you are interested, please refer to the relevant materials on your own.

Debugging macro programming is a painful process, and we can:

* Use the `-P -E` options to output the preprocessed result.
* Use the modified version of `clang` mentioned earlier to carefully study the expansion process.
* Break down complex macros and examine the expansion results of intermediate macros.
* Exclude irrelevant header files and macros.
* Finally, it is necessary to mentally simulate the process of macro expansion. Familiarity with macro expansion will also improve debugging efficiency.

The macros in this article are my own implementation after understanding the principles. Some of the macros draw inspiration from the implementation in Boost and the referenced articles. If there are any errors, please feel free to point them out at any time. You are also welcome to reach out to me for discussions on related issues.

The code for this article is all here: [Download](assets/img/2021-3-31-cpp-preprocess/macors.cpp), [Live Demo](https://godbolt.org/z/coWvc5Pse).

## Quote

* [Boost.Preprocessor](https://www.boost.org/doc/libs/1_75_0/libs/preprocessor/doc/)
* [The Art of C/C++ Macro Programming](https://bot-man-jl.github.io/articles/?post=2020/Macro-Programming-Art)

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
