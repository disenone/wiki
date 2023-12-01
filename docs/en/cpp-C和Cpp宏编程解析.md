---
layout: post
title: C/C++ Macro Programming Analysis
categories:
- c++
catalog: true
tags:
- dev
description: The purpose of this text is to explain the rules and implementation methods
  of C/C++ macro programming, so that you will no longer be afraid of seeing macros
  inside the code.
figures: []
---


The purpose of this article is to explain the rules and implementation methods of macro programming in C/C++, so that you no longer feel afraid when you see macros in the code. First, I will talk about the rules of macro expansion mentioned in C++ Standard 14, and then observe macro expansion by modifying the source code of Clang. Finally, I will discuss the implementation of macro programming based on this knowledge.

The code for this article is all here: [Download](assets/img/2021-3-31-cpp-preprocess/macros.cpp), [Online demo](https://godbolt.org/z/coWvc5Pse).

## Introduction

We can use the command `gcc -P -E a.cpp -o a.cpp.i` to instruct the compiler to only perform preprocessing on the file `a.cpp` and save the result to `a.cpp.i`.

First, let's take a look at some examples:

```

#### Recursive Reentrancy

``` cpp
#define ITER(arg0, arg1) ITER(arg1, arg0) 

ITER(1, 2)          // -> ITER(2, 1)
```

Macro `ITER` swaps the positions of `arg0` and `arg1`. After macro expansion, it becomes `ITER(2, 1)`.

You can see that the positions of `arg0` and `arg1` have been successfully swapped. Here the macro has been expanded once, but only once, without further recursive re-entry.In other words, during the expansion process of the macro, it is not allowed to recursively re-enter itself. If the same macro is found to have been expanded in a previous recursion, it will not be expanded again. This is one of the important rules of macro expansion. The reason for prohibiting recursive re-entry is also simple, which is to avoid infinite recursion.

#### String Concatenation

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                // -> HelloWorld
`CONCAT(Hello, CONCAT(World, !))     // ->　HelloCONCAT(World, !)`

--------------
**Translation:**

`CONCAT(Hello, CONCAT(World, !))     // ->　HelloCONCAT(World, !)`
```

The macro `CONCAT` is used to concatenate `arg0` and `arg1`. After the macro is expanded, `CONCAT(Hello, World)` will give the correct result `HelloWorld`. However, `CONCAT(Hello, CONCAT(World, !))` only expands the outer macro, and the inner `CONCAT(World, !)` is not expanded, but is directly concatenated with `Hello`. This is different from what we expected. What we really want is `HelloWorld!`. This is another important rule of macro expansion: macro parameters after the `##` operator will not be expanded, but will be directly concatenated with the preceding content.

Through the two examples above, it can be seen that there are some counter-intuitive rules for macro expansion. If we are not clear about the specific rules, it is possible to write macros that do not achieve the desired effect.

## Macro Expansion Rules

Through the two examples in the introduction, we have learned that macro expansion follows a set of standard rules. These rules are defined in the C/C++ standard and are not extensive. I suggest reading them carefully a few times. Here, I also provide a link to the n4296 version of the standard, which covers macro expansion in section 16.3: [link](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4296.pdf). Next, I will highlight several important rules from the n4296 version, as these rules will determine how macros should be properly written. However, I still recommend taking the time to thoroughly read the macro expansion section in the standard.

#### Parameter Separation

The requirements for macro parameters are to be separated by commas and the number of parameters needs to be consistent with the number defined in the macro. Additional content enclosed in parentheses when passing parameters to the macro is considered a single parameter, and parameters are allowed to be empty.

``` cpp
#define ADD_COMMA(arg1, arg2) arg1, arg2

ADD_COMMA(a, b)             // -> a, b
ADD_COMMA(a)                // Error: "macro "MACRO" requires 2 arguments, but only 1 given"
ADD_COMMA((a, b), c)        // -> (a, b), c
ADD_COMMA(, b)              // -> , b
```

In the expression `ADD_COMMA((a, b), c)`, `(a, b)` is considered as the first argument. In `ADD_COMMA(, b)`, since the first argument is empty, it expands to `, b`.

#### Macro Parameter Expansion

When expanding macros, if the macro's arguments are also expandable macros, the arguments will be fully expanded first, and then the macro will be expanded. For example,

``` cpp
ADD_COMMA(ADD_COMMA(1, 2), ADD_COMMA(3, 4))     // -> 1, 2, 3, 4
```

In general, the macro expansion can be understood as evaluating the parameters first, and then evaluating the macro, unless encountering `#` and `##` operators.

#### `#` Operator

`#` The macro parameter following the operator will not be expanded and will be directly converted into a string, for example:

``` cpp
#define STRINGIZE(arg0) # arg0

STRINGIZE(a)                // -> "a"
STRINGIZE(STRINGIZE(a))     // -> "STRINGIZE(a)"
```

According to this rule, `STRINGIZE(STRINGIZE(a))` can only be expanded as `"STRINGIZE(a)"`.

#### `##` Operator

## Macro parameters before and after the operator `[to_be_replace[x]]` will not be expanded and will be directly concatenated, for example:

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                        // -> HelloWorld
CONCAT(Hello, CONCAT(World, !))             // -> HelloCONCAT(World, !)
CONCAT(CONCAT(Hello, World) C, ONCAT(!))    // -> CONCAT(Hello, World) CONCAT(!)
```

`CONCAT(CONCAT(Hello, World) C, ONCAT(!))` can only be concatenated together first, to obtain `CONCAT(Hello, World) CONCAT(!)`.

#### Repeated Scanning

After the preprocessor completes one round of macro expansion, it will rescan the resulting content and continue expanding it until there is no more content left to expand.

A macro expansion can be understood as fully expanding the parameters (except when encountering `#` and `##`), and then replacing the macro and fully expanded parameters according to the macro definition, and finally processing all `#` and `##` operators in the definition.

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define STRINGIZE(arg0) # arg0

CONCAT(STRING, IZE(Hello))        // -> STRINGIZE(Hello) -> "Hello"
```

The text `CONCAT(STRING, IZE(Hello))` is first scanned and expands to `STRINGIZE(Hello)`, then it goes through a second scan and finds that `STRINGIZE` can be further expanded, resulting in `"Hello"`.

#### Prohibit recursive re-entry

In the process of repeated scanning, it is forbidden to recursively expand the same macros. The expansion of macros can be understood as a tree-like structure, with the root node being the macro to be expanded initially. The content of each macro after expansion is connected to the tree as a child node of that macro. Therefore, to prohibit recursion is to prohibit the expansion of a macro if it is the same as any ancestor macro when expanding the child nodes of that macro. Let's look at some examples:

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define CONCAT_SPACE(arg0, arg1) arg0 arg1
#define IDENTITY(arg0) IDENTITY_IMPL(arg0)
#define IDENTITY_IMPL(arg0) arg0

CONCAT(CON, CAT(a, b))                  // -> CONCAT(a, b)
IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))   // -> CONCAT(a, b)
IDENTITY(CONCAT(CON, CAT(a, b)))        // -> IDENTITY_IMPL(CONCAT(a, b)) -> CONCAT(a, b)
```

`CONCAT(CON, CAT(a, b))`: Since `CONCAT` concatenates two parameters using `##`, according to the rules of `##`, the parameters are not expanded and are concatenated directly. Therefore, the first expansion results in `CONCAT(a, b)`. Since `CONCAT` has already been expanded, it will not be recursively expanded again, thus stopping the process.

`IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))`: `IDENTITY_IMPL` can be understood as evaluating the parameter `arg0`. In this case, the parameter `arg0` is evaluated to `CONCAT(a, b)`. Since it is marked as non-reentrant due to recursion, `IDENTITY_IMPL` completes its expansion and stops when it encounters the non-reentrant `CONCAT(a, b)` during the second scan. Here, `CONCAT(a, b)` is obtained by expanding the parameter `arg0`, and in subsequent expansions, it will also maintain the non-reentrant flag. You can think of the parent node as the parameter `arg0`, which always keeps the non-reentrant flag.

`IDENTITY(CONCAT(CON, CAT(a, b)))`: This example is mainly for strengthening the understanding of parent and child nodes. When the parameter is expanded, itself acts as the parent node, and the expanded content acts as the child node to determine recursion. After the expanded parameter is passed to the macro definition, the marker for non-reentrancy will continue to be retained (if the macro after the parameter expansion does not change). The expansion process of the parameter can be seen as another tree, and the expansion result of the parameter is the bottom-level child node of the tree. This child node is passed to the macro for execution, while still retaining the non-reentrancy feature.

For example, here, after fully expanding for the first time, we get `IDENTITY_IMPL(CONCAT(a, b))`, `CONCAT(a, b)` is marked as non-reentrant, even though `IDENTITY_IMPL` evaluates its arguments, the arguments are already prohibited from expanding, so the arguments are passed to the definition as they are, and in the end, we still get `CONCAT(a, b)`.

Above, I have just listed some rules that I consider to be important, or that I find difficult to understand. For the detailed rules of macro expansion, I still recommend taking some time to directly refer to the standard documentation.

## Observing the expansion process through Clang

We can add some print information to the Clang source code to observe the macro expansion process. I don't intend to delve into the Clang source code, but here is a modified file diff. If you are interested, you can compile Clang yourself for further study. I used LLVM version 11.1.0 ([link](https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-11.1.0.tar.gz)) and the modified files ([link](assets/img/2021-3-31-cpp-preprocess/clang-modify.zip)). Below, we will briefly verify the macro expansion rules we introduced earlier through examples.

#### Example 1

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(C, ONCAT(a, b))      // CONCAT(a, b)
```

Use the modified Clang to preprocess the code above: `clang -P -E a.cpp -o a.cpp.i` and obtain the following printed information:

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

In line [1](#__codelineno-9-1), `HandleIdentifier` will print when encountering a macro, and then print the information of the macro (lines [2-4](#__codelineno-9-2)). The macro is not disabled, so it can be expanded according to the definition `Macro is ok to expand`, and then enter the macro `EnterMacro`.

The function that actually performs macro expansion is `ExpandFunctionArguments`. After that, the macro information to be expanded is printed again, noting that the macro has been marked as `used` (line [9](#__codelineno-9-9)). Then, according to the macro definition, the tokens are expanded one by one (a token is a concept in `Clang` preprocessor, not explained in detail here).

The 0th `Token` is the formal parameter `arg0`, and its corresponding actual parameter is `C`. Since there is no need to expand the judgment, it is directly copied to the result (lines [11-13](#__codelineno-9-11)).

The first `[Token]` is `hashhash`, also known as the `##` operator, copy it to the result (line [14-15](#__codelineno-9-14) ).

The second `Token` is the formal parameter `arg1`, and its corresponding actual argument is `ONCAT(a, b)`. The preprocessor will also process the actual argument into individual `Tokens`, so you can see that the printed result is enclosed in square brackets for each `Token` of the actual argument (line 18). Due to the `##` operator, this actual argument still does not need to be expanded, so it is directly copied to the result (lines [16-18](#__codelineno-9-16)).

Finally, `Leave ExpandFunctionArguments` prints the result of the expansion obtained from this scan (line [19](#__codelineno-9-19)). The `Token` of the result is translated as `C ## ONCAT(a, b)`, and then the preprocessor performs the `##` operator to generate new content.

## After execution, we get `CONCAT(a, b)`. When encountering the macro `CONCAT`, the preprocessor first enters `HandleIdentifier`, prints the macro information, and finds that the macro state is `disable used`, indicating that it has already been expanded and it is not allowed to be re-entered. The message "Macro is not ok to expand" is displayed. The preprocessor does not expand further, and the final result is `CONCAT(a, b)`.

#### Example 2

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

From line [12](#__codelineno-11-12) onward, the `IDENTITY` expansion begins. It is found that the parameter `Token 0` is `CONCAT(...)`, which is also a macro. Therefore, the evaluation of this parameter is performed first.

The parameter macro `CONCAT(...)` is expanded starting from line [27](#__codelineno-11-27), similar to example 1. After multiple expansions, `CONCAT(a, b)` is obtained (line [46](#__codelineno-11-46)).

End the expansion of `IDENTITY` at line [47](#__codelineno-11-47), and the result obtained is `CONCAT(a, b)`.

Re-scan line [51](#__codelineno-11-51) and find that although `CONCAT(a, b)` is a macro, it has been set to `used` during the previous parameter expansion process, so it is no longer recursively expanded and is directly used as the final result.

#### Example 3

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define IDENTITY_IMPL(arg0) arg0
#define IDENTITY(arg0) IDENTITY_IMPL(arg0)

IDENTITY(CONCAT(C, ONCAT(a, b)))
```

<details>
<summary> <font>Clang printing information (click to expand):</font> </summary>
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

The preprocessing starts expanding `IDENTITY` from line [16](#__codelineno-13-16), Similarly, the preprocessor sees that `Token 2` (which is `arg0`) is a macro, so it first expands `CONCAT(C, ONCAT(a, b))`.

Expand `arg0` to obtain `CONCAT(a, b)` (lines [23-54])

* `IDENTITY` is ultimately expanded to `IDENTITY_IMPL(CONCAT(a, b))` (line [57](#__codelineno-13-57))

Rescan, continue expanding `IDENTITY_IMPL` (lines [61-72](#__codelineno-13-61)), and find that `Token 0` at this point is the macro `CONCAT(a, b)`, but it is in the `used` state. Abort the expansion and return (lines 75-84), resulting in `CONCAT(a, b)` as the final result (line [85](#__codelineno-13-85)).

Rescan results and find that the status of macro `CONCAT(a, b)` is `used`. Stop expansion and obtain the final result.

Through the above three simple examples, we can roughly understand the process of macro expansion by the preprocessor. We will not further discuss the preprocessor here. If interested, you can study it by comparing the modified files I have provided.

## Macro Programming Implementation

Below we will start delving into the topic (the purpose of the previous long paragraph was to better understand macro expansion rules) and the implementation of macro programming.

#### Basic Symbols

First, we can define the special symbols of macros, which will be used for evaluation and concatenation.

``` cpp
#define PP_LPAREN() (
#define PP_RPAREN() )
#define PP_COMMA() ,
#define PP_EMPTY() 
```cpp
#define PP_HASHHASH # ## #      // Represents the string "##", but is only treated as a string and not as the ## operator.
```
```

#### Evaluation

By utilizing the rule of parameter prioritization expansion, it is possible to write an evaluation macro.

``` cpp
#define PP_IDENTITY(arg0) arg0

PP_COMMA PP_LPAREN() PP_RPAREN()                // -> PP_COMMA ( )
PP_IDENTITY(PP_COMMA PP_LPAREN() PP_RPAREN())   // -> PP_COMMA() -> ,
```

If you only write `PP_COMMA PP_LPAREN() PP_RPAREN()`, the preprocessor will handle each macro separately and will not merge the results of expansion. When `PP_IDENTITY` is added, the preprocessor can evaluate the expanded `PP_COMMA()` to get `,`.


#### Concatenate

Since `##` does not expand the arguments on both sides when concatenating them, to evaluate the arguments before concatenation, you can write it like this:

``` cpp
#define PP_CONCAT(arg0, arg1) PP_CONCAT_IMPL(arg0, arg1)
#define PP_CONCAT_IMPL(arg0, arg1) arg0 ## arg1

PP_CONCAT(PP_IDENTITY(1), PP_IDENTITY(2))         // -> 12
PP_CONCAT_IMPL(PP_IDENTITY(1), PP_IDENTITY(2))    // -> PP_IDENTITY(1)PP_IDENTITY(2) -> Error
```

Here the method used by `PP_CONCAT` is called delayed concatenation. When expanded to `PP_CONCAT_IMPL`, both `arg0` and `arg1` will be expanded and evaluated first, and then the real concatenation operation will be performed by `PP_CONCAT_IMPL`.

#### Logical Operations

With the help of `PP_CONCAT`, logical operations can be implemented. First, define the `BOOL` value:


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

Use `PP_CONCAT` to concatenate `PP_BOOL_` and `arg0` together, then evaluate the concatenated result. Here, `arg0` is required to be a number within the range of `[0, 256]`. By evaluating the concatenation after `PP_BOOL_`, a boolean value can be obtained. The operations include logical AND, logical OR, and logical NOT:

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

First, use `PP_BOOL` to evaluate the parameters, and then concatenate the logical operation results based on the combination of `0` and `1`. If `PP_BOOL` is not used to evaluate the parameters, then the parameters can only support the values `0` and `1`, greatly reducing versatility. Similarly, you can also write XOR, OR, NOT, and other operations. If you are interested, you can try it yourself.

#### Conditional Selection

By using `PP_BOOL` and `PP_CONCAT`, you can also write conditional selection statements:

``` cpp
#define PP_IF(if, then, else) PP_CONCAT(PP_IF_, PP_BOOL(if))(then, else)
#define PP_IF_1(then, else) then
#define PP_IF_0(then, else) else

PP_IF(1, 2, 3)      // -> PP_IF_1(2, 3) -> 2
PP_IF(0, 2, 3)      // -> PP_IF_0(2, 3) -> 3
```

`if` evaluates to `1`, concatenates with `PP_CONCAT` to form `PP_IF_1`, and finally expands to the value of `then`. Similarly, if `if` evaluates to `0`, it results in `PP_IF_0`.

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

Similar to `PP_BOOL`, the increment or decrement of integers also has a limited range. Here, the range is set to `[0, 256]`. After incrementing to `256`, for safety reasons, `PP_INC_256` will return itself, `256`, as the boundary. Similarly, `PP_DEC_0` will also return `0`.

#### Variable-length parameters

Macros can accept variable-length arguments, the format is:

```cpp 
#define LOG(format, ...) printf("log: " format, __VA_ARGS__)

LOG("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG("Hello World")              // -> printf("log: " "Hello World", ); A comma is missing, causing a compilation error.
```

Due to the possibility of variable-length parameters being empty, which can lead to compilation failure, C++ 20 has introduced `__VA_OPT__`. If the variable-length parameters are empty, it will return empty; otherwise, it will return the original parameters.

```cpp 
#define LOG2(format, ...) printf("log: " format __VA_OPT__(,) __VA_ARGS__)

LOG2("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG2("Hello World")              // -> printf("log: " "Hello World" ); No comma, compiled successfully.
```

But unfortunately, only C++ 20 or higher standards have this macro. In the following text, we will provide the implementation method for `__VA_OPT__`.

#### Lazy evaluation

Consider this situation:

``` cpp
PP_IF(1, PP_COMMA(), PP_LPAREN())     // -> PP_IF_1(,,)) -> Error: unterminated argument list invoking macro "PP_IF_1"
```

We know that during macro expansion, the first parameter is evaluated. After evaluating `PP_COMMA()` and `PP_LPAREN()`, they are passed to `PP_IF_1`, resulting in `PP_IF_1(,,))` and causing a preprocessing error. In this case, we can use a method called lazy evaluation:

``` cpp
PP_IF(1, PP_COMMA, PP_LPAREN)()       // -> PP_IF_1(PP_COMMA, PP_LPAREN)() -> PP_COMMA() -> ,
```

Change it to this writing style, only pass the name of the macro, let `PP_IF` select the required macro name, then concatenate it with parentheses `()` to form a complete macro, and finally expand it. Lazy evaluation is also very common in macro programming.

#### Start with parentheses

Check if the variable-length parameter starts with a parenthesis:

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

`PP_IS_BEGIN_PARENS` can be used to determine if the incoming parameter starts with parentheses. It is often used when dealing with parenthesized arguments (such as the implementation of `__VA_OPT__` mentioned later). It may seem a bit complicated, but the core idea is to build a macro that, if the variadic parameter starts with parentheses, can be evaluated together with the parentheses to obtain one result; otherwise, it can be evaluated separately to obtain another result. Let's take a closer look:

The macro functionality composed of `PP_IS_BEGIN_PARENS_PROCESS` and `PP_IS_BEGIN_PARENS_PROCESS_0` is to first evaluate the incoming variadic arguments, and then take the 0th argument.

`PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__)` evaluates `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` first, then concatenates the evaluated result with `PP_IS_BEGIN_PARENS_PRE_`.

`PP_IS_BEGIN_PARENS_EAT(...)` the macro will consume all its arguments and return 1. If in the previous step `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__`, `__VA_ARGS__` starts with parentheses, it will match the evaluation of `PP_IS_BEGIN_PARENS_EAT(...)` and return 1. On the other hand, if it does not start with parentheses, there is no match, and `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` will remain unchanged.

If `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` evaluates to `1`, `PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, 1) -> PP_IS_BEGIN_PARENS_PRE_1 -> 1` should be noted that there is a comma after `1`, pass `1,` to `PP_IS_BEGIN_PARENS_PROCESS_0`, take the 0th argument, and finally obtain `1`, which indicates that the argument begins with a parenthesis.

If `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` evaluates to something other than `1` and remains unchanged, then `PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__) -> PP_IS_BEGIN_PARENS_PRE_PP_IS_BEGIN_PARENS_EAT __VA_ARGS__ -> 0, __VA_ARGS__` is passed to `PP_IS_BEGIN_PARENS_PROCESS_0`, which results in `0`, indicating that the argument does not begin with parentheses.

#### Variable-length parameter null

To judge whether variable-length parameters are empty is also a commonly used macro. This is required when implementing `__VA_OPT__`. Here, we can make use of `PP_IS_BEGIN_PARENS` to write an incomplete version first.

``` cpp
#define PP_IS_EMPTY_PROCESS(...) \
    PP_IS_BEGIN_PARENS(PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ())
#define PP_IS_EMPTY_PROCESS_EAT(...) ()

PP_IS_EMPTY_PROCESS()       // -> 1
PP_IS_EMPTY_PROCESS(1)      // -> 0
PP_IS_EMPTY_PROCESS(1, 2)   // -> 0
PP_IS_EMPTY_PROCESS(())     // -> 1
```

The function of `PP_IS_EMPTY_PROCESS` is to determine if `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__()` starts with parentheses.

If `__VA_ARGS__` is empty, `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ () -> PP_IS_EMPTY_PROCESS_EAT() -> ()`, it will result in a pair of parentheses `()`, which will then be passed to `PP_IS_BEGIN_PARENS` and return `1`, indicating that the argument is empty.

Otherwise, `PP_IS_EMPTY_PROCESS_EAT__VA_ARGS__ ()` remains unchanged and is passed to `PP_IS_BEGIN_PARENS`, returning 0 to indicate non-empty content.

Pay attention to the 4th example `PP_IS_EMPTY_PROCESS(()) -> 1`, `PP_IS_EMPTY_PROCESS` cannot correctly handle variadic arguments that begin with parentheses, because in this case the parentheses brought by the variadic arguments will match `PP_IS_EMPTY_PROCESS_EAT` and result in `()`. To solve this problem, we need to differentiate between cases where the arguments begin with parentheses.

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

If the variable-length parameters are enclosed in parentheses, `PP_IS_EMPTY_IF` returns `PP_IS_EMPTY_ZERO`, and finally returns `0`, indicating that the variable-length parameters are not empty.

On the contrary, `PP_IS_EMPTY_IF` returns `PP_IS_EMPTY_PROCESS`, and finally `PP_IS_EMPTY_PROCESS` is responsible for determining if the variable-length parameter is not empty.

#### Index access

Get the element specified by the position of the variable-length arguments:

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

The first argument of `PP_ARGS_ELEM` is the index of the element `I`, followed by a variable-length argument. By using `PP_CONCAT` to concatenate `PP_ARGS_ELEM_` and `I`, we can obtain the macro `PP_ARGS_ELEM_0..8` which returns the element at the corresponding position. Then, we pass the variable-length argument to this macro to expand and return the element at the specified index.

#### PP_IS_EMPTY2

By using `PP_ARGS_ELEM`, another version of `PP_IS_EMPTY` can be achieved:

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

Using `PP_ARGS_ELEM` to implement the detection of whether the argument contains a comma, `PP_HAS_COMMA`. `PP_COMMA_ARGS` will consume any passed-in arguments and return a comma.

The basic logic to determine whether variable arguments are empty is `PP_COMMA_ARGS __VA_ARGS__ ()` returns a comma, which means `__VA_ARGS__` is empty. `PP_COMMA_ARGS` and `()` are concatenated together for evaluation, and the specific notation is `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ())`.

However, there will be exceptions:

* `__VA_ARGS__` may potentially contain commas;
* `__VA_ARGS__ ()` concatenation together results in the evaluation of a comma;
* `PP_COMMA_ARGS __VA_ARGS__` concatenation together results in the evaluation of a comma;

In response to the three exceptional cases mentioned above, exclusions need to be made, so the final expression is equivalent to applying logical "AND" to the following four conditions:

* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__))` &&
* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__()))` &&
* `PP_NOT(PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__))` &&
* `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ())`

#### `__VA_OPT__`

With the help of `PP_IS_EMPTY`, it is finally possible to achieve macros similar to `__VA_OPT__`.

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

`PP_ARGS_OPT` accepts two fixed parameters and a variable number of parameters. When the variable parameters are not empty, it returns `data`; otherwise, it returns `empty`. In order to support commas in `data` and `empty`, it is required that both of them are enclosed in parentheses with the actual parameters, and the outer parentheses are removed using `PP_REMOVE_PARENS`.

With `PP_ARGS_OPT`, it is possible to achieve the functionality of simulating `LOG2` by using `LOG3`.

``` cpp
#define LOG3(format, ...) \
    printf("log: " format PP_ARGS_OPT((,), (), __VA_ARGS__) __VA_ARGS__)

LOG3("Hello");                  // -> printf("log: " "Hello" );
LOG3("Hello %s", "World");      // -> printf("log: " "Hello %s" , "World");
```

`data_tuple` is `(,)`. If the variable-length argument is not empty, it will return all the elements in `data_tuple`, which in this case is a comma `,`.

#### Number of Parameters Requested

Get the number of variable arguments:

``` cpp
#define PP_ARGS_SIZE_IMCOMPLETE(...) \
    PP_ARGS_ELEM(8, __VA_ARGS__, 8, 7, 6, 5, 4, 3, 2, 1, 0)

PP_ARGS_SIZE_IMCOMPLETE(a)             // -> 1
PP_ARGS_SIZE_IMCOMPLETE(a, b)          // -> 2
PP_ARGS_SIZE_IMCOMPLETE(PP_COMMA())    // -> 2
PP_ARGS_SIZE_IMCOMPLETE()              // -> 1
```

The number of variable arguments is calculated by counting their positions. `__VA_ARGS__` causes all subsequent arguments to shift to the right. Use the macro `PP_ARGS_ELEM` to obtain the argument at the 8th position. If `__VA_ARGS__` only has one argument, then the 8th argument is equal to `1`. Similarly, if `__VA_ARGS__` has two arguments, then the 8th argument becomes `2`, exactly equal to the number of variable arguments.

The examples given here only support a maximum number of 8 variable arguments, which is based on the maximum length supported by `PP_ARGS_ELEM`.

However, this macro is not complete. In the case where the variable arguments are empty, this macro will incorrectly return `1`. If it is necessary to handle empty variable arguments, the `PP_ARGS_OPT` macro mentioned earlier needs to be used.

``` cpp
#define PP_COMMA_IF_ARGS(...) PP_ARGS_OPT((,), (), __VA_ARGS__)
#define PP_ARGS_SIZE(...) PP_ARGS_ELEM(8, __VA_ARGS__ PP_COMMA_IF_ARGS(__VA_ARGS__) 8, 7, 6, 5, 4, 3, 2, 1, 0, 0, 0)

PP_ARGS_SIZE(a)             // -> 1
PP_ARGS_SIZE(a, b)          // -> 2
PP_ARGS_SIZE(PP_COMMA())    // -> 2
PP_ARGS_SIZE()              // -> 0
PP_ARGS_SIZE(,,,)           // -> 4
```

The key to the problem lies in the comma `,`. When `__VA_ARGS__` is empty, the comma should be hidden to correctly return `0`.

#### Traversal Access

Similar to C++'s `for_each`, we can implement the `PP_FOR_EACH` macro.

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

`PP_FOR_EACH` receives two fixed parameters: `macro`, which can be understood as the macro called during iteration, and `context`, which can be passed as a fixed value parameter to `macro`. `PP_FOR_EACH` first uses `PP_ARGS_SIZE` to obtain the length `N` of the variable-length parameters, and then concatenates `PP_FOR_EACH_N` using `PP_CONCAT`. Afterwards, `PP_FOR_EACH_N` will iteratively call `PP_FOR_EACH_N-1` to achieve the same number of iterations as the variable-length parameters.

In the example, we declare `DECLARE_EACH` as a parameter `macro`, the purpose of `DECLARE_EACH` is to return `contex arg`, if `contex` is a type name and `arg` is a variable name, `DECLARE_EACH` can be used to declare variables.

#### Conditional Loop

With the introduction of `FOR_EACH`, we can also use a similar approach to write `PP_WHILE`:

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

`PP_WHILE` accepts three parameters: `pred` as the conditional function, `op` as the operation function, and `val` as the initial value; during the loop, it continuously uses `pred(val)` as the termination condition and passes the value obtained from `op(val)` to the subsequent macro. It can be understood as executing the following code:

``` cpp
while (pred(val)) {
    val = op(val);
}
```

First, use `pred(val)` to obtain the condition evaluation result, and pass the condition result `cond` and other arguments to `PP_WHILE_N_IMPL`.
`PP_WHILE_N_IMPL` can be divided into two parts: the latter part `(pred, op, PP_IF(cond, op, PP_EMPTY_EAT)(val))` is used as the parameter of the former part. `PP_IF(cond, op, PP_EMPTY_EAT)(val)` evaluates `op(val)` if `cond` is true, otherwise evaluates `PP_EMPTY_EAT(val)` to obtain an empty result. The former part `PP_IF(cond, PP_WHILE_N+1, val PP_EMPTY_EAT)` returns `PP_WHILE_N+1` if `cond` is true, and continues the loop with the combined parameters of the latter part. Otherwise, it returns `val PP_EMPTY_EAT`, in which case `val` is the final calculation result, and `PP_EMPTY_EAT` will discard the result of the latter part.

`SUM` implements `N + N-1 + ... + 1`. The initial values are `(max_num, origin_num)`. For `SUM_PRED` it takes the first element `x` of the value and checks if it is greater than 0. `SUM_OP` performs the decrement operation `x = x - 1` on `x`, and the `+ x` operation `y = y + x` on `y`. Directly pass `SUM_PRED` and `SUM_OP` to `PP_WHILE`, the result returned is a tuple. The desired result is the second element of the tuple, so we use `SUM` to get the value of the second element.

#### Recursive Reentry

So far, our traversal visits and conditional loops have been working well and producing the expected results. Remember when we talked about the prohibition of recursive reentry in macro expansion rules? Unfortunately, we encountered this prohibition of recursive reentry when we wanted to perform nested loops.

``` cpp
#define SUM_OP2(xy_tuple) SUM_OP_OP_IMPL2 xy_tuple
#define SUM_OP_OP_IMPL2(x, y) (PP_DEC(x), y + SUM(x, 0))

#define SUM2(max_num, origin_num) \
    PP_IDENTITY(SUM_IMPL PP_WHILE(SUM_PRED, SUM_OP2, (max_num, origin_num)))

SUM2(1, a)      // -> a + SUM_IMPL PP_WHILE_1(SUM_PRED, SUM_OP, (1, a))
```

`SUM2` changes the parameter `op` to `SUM_OP2`, and inside `SUM_OP2` it will call `SUM`, and when `SUM` expands, it will become `PP_WHILE_1`, which is equivalent to `PP_WHILE_1` recursively calling itself. The preprocessor stops expanding.

To solve this problem, we can use a method called Automatic Recursion.

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

`PP_AUTO_WHILE` is an automatically deduced recursive version of `PP_WHILE`, the core macro being `PP_AUTO_REC(PP_WHILE_PRED)`, which can determine the number `N` of the current available version of `PP_WHILE_N`.

The principle of deduction is very simple. It searches through all versions, finds the version that can be correctly expanded, and returns the number of that version. In order to improve the speed of the search, the usual practice is to use binary search, which is what `PP_AUTO_REC` does. `PP_AUTO_REC` takes a parameter called `check`, which is responsible for checking the availability of versions. Here, the supported range for version search is specified as `[1, 4]`. `PP_AUTO_REC` will first check `check(2)`. If `check(2)` is true, it will call `PP_AUTO_REC_12` to search the range `[1, 2]`, otherwise it will use `PP_AUTO_REC_34` to search `[3, 4]`. `PP_AUTO_REC_12` checks `check(1)`, if it is true, it means that version `1` is available, otherwise it uses version `2`. `PP_AUTO_REC_34` follows the same logic.

`check` How can we write the macro to check if the version is available? Here, `PP_WHILE_PRED` will be expanded into two parts of concatenation. Let's take a look at the latter part, `PP_WHILE_ ## n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`: if `PP_WHILE_ ## n` is available, since `PP_WHILE_FALSE` always returns `0`, this part will be expanded to the value of the `val` parameter, which is `PP_WHILE_FALSE`; otherwise, this part of the macro will remain unchanged, still `PP_WHILE_n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`.

Concatenate the result of the latter part with the prefix `PP_WHILE_CHECK_` to obtain two possible results: `PP_WHILE_CHECK_PP_WHILE_FALSE` or `PP_WHILE_CHECK_PP_WHILE_n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`. Therefore, we make `PP_WHILE_CHECK_PP_WHILE_FALSE` return `1` to indicate availability and `PP_WHILE_CHECK_PP_WHILE_n` return `0` to indicate unavailability. With this, we have completed the automatic deduction of recursion.

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

The judgment of whether the values are equal uses the feature of prohibiting recursive re-entry. The `x` and `y` are recursively concatenated into the `PP_NOT_EQUAL_x PP_NOT_EQUAL_y` macro. If `x == y`, the `PP_NOT_EQUAL_y` macro will not be expanded, and it will be concatenated with `PP_NOT_EQUAL_CHECK_` to form `PP_NOT_EQUAL_CHECK_PP_NOT_EQUAL_y`, returning `0`. On the other hand, if it successfully expands twice, the final result will be `PP_EQUAL_NIL`, concatenated with `PP_NOT_EQUAL_CHECK_` to form `PP_NOT_EQUAL_CHECK_PP_EQUAL_NIL`, returning `1`.

Equal:

``` cpp
#define PP_EQUAL(x, y) PP_NOT(PP_NOT_EQUAL(x, y))

PP_EQUAL(1, 1)              // -> 1
PP_EQUAL(1, 3)              // -> 0

```

<=

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

In addition, there are arithmetic comparisons such as greater than, greater than or equal to, and so on. No more details will be elaborated here.

#### Arithmetic Operations

With the use of `PP_AUTO_WHILE`, we can achieve basic arithmetic operations and also support nested operations.

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

Multiplication function adds an additional parameter `ret` here, with an initial value of `0`, and in each iteration `ret` is updated as `ret = ret + x`.

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

Division uses `PP_LESS_EQUAL`, only continue the loop if `y <= x`.

#### Data Structures

Macros can also have data structures. In fact, we have briefly used a data structure called `tuple` earlier, where `PP_REMOVE_PARENS` can remove the outer parentheses of a `tuple` and return its elements. Here, we will use `tuple` as an example to discuss the relevant implementation. If you are interested, you can also look at the implementation of other data structures like `list` and `array` in `Boost`.

A `tuple` is defined as a collection of elements separated by commas and enclosed in parentheses: `(a, b, c)`.

``` cpp
#define PP_TUPLE_REMOVE_PARENS(tuple) PP_REMOVE_PARENS(tuple)

// Get the element at the specified index
#define PP_TUPLE_ELEM(i, tuple) PP_ARGS_ELEM(i, PP_TUPLE_REMOVE_PARENS(tuple))

// Swallow the entire tuple and return empty
#define PP_TUPLE_EAT() PP_EMPTY_EAT

// Get Size
#define PP_TUPLE_SIZE(tuple) PP_ARGS_SIZE(PP_TUPLE_REMOVE_PARENS(tuple))

// Add element
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

Here's a brief explanation of how the insertion of elements is implemented here, and similar principles are used for other operations like element deletion. `PP_TUPLE_INSERT(i, elem, tuple)` can insert element `elem` at position `i` in `tuple`. To accomplish this, we first use `PP_TUPLE_PUSH_BACK` to place all elements with positions less than `i` onto a new `tuple` called `ret`. Then, we place element `elem` at position `i`. After that, we append the original elements from `tuple` with positions greater than or equal to `i` to the end of `ret`. Finally, `ret` gives us the desired result.

## Summary

The purpose of this document is to explain the principles and basic implementation of C/C++ macro programming. While recording my own understanding and knowledge, I hope to clarify and inspire others. It is worth noting that although this document is a bit long, there are still some macro programming techniques and usages that have not been covered, such as the [recursive call method based on delayed expansion proposed by CHAOS_PP](https://github.com/pfultz2/Cloak/wiki/C-Preprocessor-tricks,-tips,-and-idioms#deferred-expression), and the `REPEAT` related macros in BOOST_PP, etc. Interested readers can search for information on their own.

Debugging macro programming is a painful process. We can:

* Use the `-P -E` options to output the preprocessing result;
* Use the `clang` version that I modified as mentioned earlier to carefully study the expansion process;
* Break down complex macros and examine the expansion results of intermediate macros;
* Block irrelevant header files and macros;
* Finally, it is necessary to mentally simulate the process of macro expansion. Familiarity with macro expansion will also improve debugging efficiency.

The macros in this article are my own reimplementation after understanding the principles. Some of the macros were inspired by the implementation in `Boost` and referenced articles. If there are any errors, feel free to correct them at any time. I am also open to discussing related issues with you.

The code for this article is available here: [Download](assets/img/2021-3-31-cpp-preprocess/macors.cpp), [Online Demo](https://godbolt.org/z/coWvc5Pse).

## Quote

* [Boost.Preprocessor](https://www.boost.org/doc/libs/1_75_0/libs/preprocessor/doc/)
[C/C++ Macro Programming Art](https://bot-man-jl.github.io/articles/?post=2020/Macro-Programming-Art)

> Original: <https://disenone.github.io/wiki>  
> This post is protected by [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by/4.0/deed.en) agreement, should be reproduced with attribution.


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
