---
layout: post
title: C/C++ Macro Programming Analysis
categories:
- c++
catalog: true
tags:
- dev
description: The purpose of this article is to clarify the rules and implementation
  methods of C/C++ macro programming, so that you no longer fear encountering macros
  in code.
figures: []
---

The purpose of this article is to clarify the rules and implementation methods of macro programming in C/C++, so that you no longer fear macros in code. First, I will discuss the rules for macro expansion mentioned in C++ Standard 14, then observe macro expansion by modifying the Clang source code, and finally discuss the implementation of macro programming based on this knowledge.

All the code in this article is available here: [Download](assets/img/2021-3-31-cpp-preprocess/macros.cpp), [Live Demo](https://godbolt.org/z/coWvc5Pse).

## Introduction

We can use the command `gcc -P -E a.cpp -o a.cpp.i` to let the compiler preprocess the file `a.cpp` and save the result to `a.cpp.i`.

First, let's look at some examples:

#### Recursive Reentrancy

```cpp
#define ITER(arg0, arg1) ITER(arg1, arg0) 

ITER(1, 2)          // -> ITER(2, 1)
```

The macro `ITER` swaps the positions of `arg0` and `arg1`. After macro expansion, we get `ITER(2, 1)`.

As you can see, the positions of `arg0` and `arg1` are successfully swapped. In this case, the macro is expanded once, but not recursively reentrant. In other words, during macro expansion, it is not allowed to recursively reenter itself. If the same macro has been expanded in previous recursion, it will not be expanded again. This is an important rule of macro expansion. The reason for prohibiting recursive reentrancy is simple: to avoid infinite recursion.

#### String Concatenation

```cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                // -> HelloWorld
CONCAT(Hello, CONCAT(World, !))     // -> HelloCONCAT(World, !)
```

The macro `CONCAT` is intended to concatenate `arg0` and `arg1`. After macro expansion, `CONCAT(Hello, World)` obtains the correct result `HelloWorld`. However, `CONCAT(Hello, CONCAT(World, !))` only expands the outer macro. The inner `CONCAT(World, !)` is not expanded and is directly concatenated with `Hello`. This is different from what we expected. The important rule of macro expansion is that macro parameters following the `##` operator are not expanded, but are directly concatenated with the preceding content.

From the above two examples, we can see that there are some rules of macro expansion that are counterintuitive. If we are not clear about the specific rules, we may write macros that do not achieve the desired effect.

## Rules of Macro Expansion

From the two examples in the introduction, we understand that macro expansion follows a set of standard rules, which are defined in the C/C++ standard with a small amount of content. It is recommended to read them carefully. Here, I will provide a link to section 16.3 of the n4296 version of the standard, which covers macro expansion: [Link](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4296.pdf). Below, I will highlight a few important rules from the n4296 version, which determine how to correctly write macros (it is still recommended to take some time to carefully read the macro expansion section in the standard).

#### Parameter Separation

Macro parameters should be separated by commas, and the number of parameters must match the number defined in the macro. Extra content enclosed in parentheses within the passed parameters is considered as one parameter, and parameters are allowed to be empty:

```cpp
#define ADD_COMMA(arg1, arg2) arg1, arg2

ADD_COMMA(a, b)             // -> a, b
ADD_COMMA(a)                // Error: "macro "MACRO" requires 2 arguments, but only 1 given"
ADD_COMMA((a, b), c)        // -> (a, b), c
ADD_COMMA(, b)              // -> , b
```

Translate these text into English language, do not explain them:

In the expression `ADD_COMMA((a, b), c)`, `(a, b)` is considered the first argument. In `ADD_COMMA(, b)`, the first argument is empty, so it expands to `, b`.

#### Macro Argument Expansion

When expanding a macro, if the macro's argument is also a macro that can be expanded, the argument will be completely expanded before expanding the macro. For example:

``` cpp
ADD_COMMA(ADD_COMMA(1, 2), ADD_COMMA(3, 4))     // -> 1, 2, 3, 4
```

In general, macro expansion can be understood as evaluating the arguments first and then evaluating the macro, unless the `#` and `##` operators are encountered.

#### `#` Operator

The macro parameter following the `#` operator is not expanded and will be directly converted into a string. For example:

``` cpp
#define STRINGIZE(arg0) # arg0

STRINGIZE(a)                // -> "a"
STRINGIZE(STRINGIZE(a))     // -> "STRINGIZE(a)"
```

According to this rule, `STRINGIZE(STRINGIZE(a))` will expand to `"STRINGIZE(a)"`.

#### `##` Operator

The macro parameters before and after the `##` operator are not expanded and will be directly concatenated. For example:

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                        // -> HelloWorld
CONCAT(Hello, CONCAT(World, !))             // -> HelloCONCAT(World, !)
CONCAT(CONCAT(Hello, World) C, ONCAT(!))    // -> CONCAT(Hello, World) CONCAT(!)
```

`CONCAT(CONCAT(Hello, World) C, ONCAT(!))` will only concatenate together and become `CONCAT(Hello, World) CONCAT(!)`.

#### Recursive Scanning

After the preprocessor completes one round of macro expansion, it will rescan the resulting content and continue expanding until there is no more content to expand.

A round of macro expansion can be understood as fully expanding the arguments (unless encountering `#` and `##`), then replacing the macro and fully expanded arguments according to the definition, and finally processing all the `#` and `##` operators in the definition.

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define STRINGIZE(arg0) # arg0

CONCAT(STRING, IZE(Hello))        // -> STRINGIZE(Hello) -> "Hello"
```

In `CONCAT(STRING, IZE(Hello))`, it first expands to `STRINGIZE(Hello)` during the first scan, then during the second scan, it finds that `STRINGIZE` can be further expanded, resulting in `"Hello"`.

#### Disallowing Recursive Re-entry

During the process of repetitive scanning, recursive expansion of the same macro is prohibited. Macro expansion can be understood as a tree-like structure, with the root node being the macro to be expanded initially, and each macro-expanded content serving as a child node connected to the tree. Therefore, disallowing recursion means that when expanding the macro of a child node, if the macro is the same as any ancestor node's macro, expansion is prohibited. Let's look at some examples:

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define CONCAT_SPACE(arg0, arg1) arg0 arg1
#define IDENTITY(arg0) IDENTITY_IMPL(arg0)
#define IDENTITY_IMPL(arg0) arg0
```

`CONCAT(CON, CAT(a, b))`: Since `CONCAT` is concatenating two parameters using `##`, according to the rules of `##`, the parameters are not expanded and simply concatenated. So, the first expansion yields `CONCAT(a, b)`. Since `CONCAT` has already been expanded, it will not be recursively expanded again and stops.

`IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))`: `IDENTITY_IMPL` can be understood as evaluating the parameter `arg0`. In this case, the parameter `arg0` evaluates to `CONCAT(a, b)`. Since recursion is marked as disallowed, `IDENTITY_IMPL` completes the expansion and during the second scan, it encounters a disallowed `CONCAT(a, b)` and stops. Here, `CONCAT(a, b)` is expanded from the parameter `arg0`, but in subsequent expansions, the disallowed flag will be maintained, meaning that the parent node is the parameter `arg0` and it will continue to have the disallowed flag.

`IDENTITY(CONCAT(CON, CAT(a, b)))`: This example is mainly to reinforce the understanding of parent-child nodes. When a parameter expands itself, it becomes the parent node, and the expanded content becomes the child node to determine recursion. After the parameter is expanded, it can be regarded as another tree. The expansion result of the parameter is the bottom-most child node of the tree. When this child node is passed to the macro for expansion, it still retains the disallowed recursion feature.

For example, after the first complete expansion, we have `IDENTITY_IMPL(CONCAT(a, b))`. Although `IDENTITY_IMPL` evaluates the parameter, the parameter has already been disallowed from expansion. Therefore, the parameter is passed to the definition as it is, and we still have `CONCAT(a, b)`.

The above are just some important rules or rules that I think are difficult to understand. For a detailed macro expansion rule, I recommend taking some time to read the standard documentation.

## Observing the Expansion Process with Clang

We can add some debug prints to the Clang source code to observe the macro expansion process. I don't intend to dive into the details of the Clang source code, but I will provide a modified diff file. If you are interested, you can compile Clang and study it yourself. I used LLVM version 11.1.0 ([link](https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-11.1.0.tar.gz)). Here is the modified file ([link](assets/img/2021-3-31-cpp-preprocess/clang-modify.zip)). Below, I will briefly verify the macro expansion rules we previously discussed:

#### Example 1

```cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(C, ONCAT(a, b))      // CONCAT(a, b)
```

Using the modified Clang to preprocess the code: `clang -P -E a.cpp -o a.cpp.i`, we get the following debug prints:

``` text linenums="1"
HandleIdentifier: 
MacroInfo 0x559e57496900
    #define <macro>[2813:CONCAT](arg0, arg1) arg0 ## arg1
Macro is ok to expand

EnterMacro: 0
```

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

Example 2

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define IDENTITY(arg0) arg0

IDENTITY(CONCAT(C, ONCAT(a, b)))
```

<details>
<summary> <font> Clang Print Information (click to expand): </font> </summary>
```
test linenums="1"
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
```

HandleIdentifier: 
MacroInfo 0x562a148f5930 used
    #define <macro>[2813:CONCAT](arg0, arg1) arg0 ## arg1
Macro is not ok to expand
```
</details>

Starting from line [12](#__codelineno-11-12), `IDENTITY` is expanded and it is found that parameter `Token 0` is `CONCAT(...)`, which is also a macro. So, evaluate this parameter first.

Starting from line [27](#__codelineno-11-27), the parameter macro `CONCAT(...)` is expanded. Just like example 1, after multiple scans, it becomes `CONCAT(a, b)` (line [46](#__codelineno-11-46)).

The expansion of `IDENTITY` ends at line [47](#__codelineno-11-47), resulting in `CONCAT(a, b)`.

On line [51](#__codelineno-11-51), `CONCAT(a, b)` is rescanned. Although it is a macro, it has already been set as `used` during the parameter expansion process, so it won't be recursively expanded and will be directly used as the final result.

#### Example 3

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define IDENTITY_IMPL(arg0) arg0
#define IDENTITY(arg0) IDENTITY_IMPL(arg0)

IDENTITY(CONCAT(C, ONCAT(a, b)))
```

<details>
<summary> <font>Clang Print Information (Click to Expand)：</font> </summary>
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

**EnterMacro**: 1

**Enter ExpandFunctionArguments**: 
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
**Leave ExpandFunctionArguments**: [identifier: C][hashhash: ][identifier: ONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ]

**LeaveMacro**: 1

**HandleIdentifier**: 
MacroInfo 0x55e824457950 disabled used
    #define <macro>[2813:CONCAT](arg0, arg1) arg0 ## arg1
Macro is not ok to expand
ResultArgToks: [identifier: CONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ]
Token: 3
r_paren: 
**Leave ExpandFunctionArguments**: [identifier: IDENTITY_IMPL][l_paren: ][identifier: CONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ][r_paren: ]

**LeaveMacro**: 0

**HandleIdentifier**: 
MacroInfo 0x55e824457a80
    #define <macro>[2853:IDENTITY_IMPL](arg0) arg0
Macro is ok to expand

**HandleIdentifier**: 
MacroInfo 0x55e824457950 used
    #define <macro>[2813:CONCAT](arg0, arg1) arg0 ## arg1

**EnterMacro**: 2

**Enter ExpandFunctionArguments**: 
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

* Starting from line [16](#__codelineno-13-16), expand `IDENTITY`. The preprocessor sees that `Token 2` (which is `arg0`) is a macro, so it first expands `CONCAT(C, ONCAT(a, b))`.
* After expanding `arg0`, we get `CONCAT(a, b)` (lines [23-54](#__codelineno-13-23)).
* `IDENTITY` is ultimately expanded to `IDENTITY_IMPL(CONCAT(a, b))` (line [57](#__codelineno-13-57)).
* Rescanning, we continue to expand `IDENTITY_IMPL` (lines [61-72](#__codelineno-13-61)). We find that the `Token 0` is the macro `CONCAT(a, b)`, but it is in a `used` state, so we abort the expansion and return (lines 75-84). The final result is still `CONCAT(a, b)` (line [85](#__codelineno-13-85)).
* Upon rescanning the result, we find that the macro `CONCAT(a, b)` is in a `used` state, so we stop the expansion and obtain the final result.

With these three simple examples, we can roughly understand the process of macro expansion by the preprocessor. We will not delve further into the preprocessor here. If you are interested, you can study the modified file I provided.

## Macro Programming Implementation

Now, let's get to the main topic (the previous section was to better understand the macro expansion rules), the implementation of macro programming.

#### Basic Symbols

First, we can define special symbols for macros, which will be used for evaluation and concatenation:

```cpp
#define PP_LPAREN() (
#define PP_RPAREN() )
#define PP_COMMA() ,
#define PP_EMPTY()
#define PP_HASHHASH # ## #      // Represents the string ##, but only as a string, will not be treated as the ## operator
```

#### Evaluation

By utilizing the rule of argument pre-expansion, we can write an evaluation macro:

```cpp
#define PP_IDENTITY(arg0) arg0

PP_COMMA PP_LPAREN() PP_RPAREN()                // -> PP_COMMA ( )
PP_IDENTITY(PP_COMMA PP_LPAREN() PP_RPAREN())   // -> PP_COMMA() -> ,
```

If we only write `PP_COMMA PP_LPAREN() PP_RPAREN()`, the preprocessor will only process each macro separately and will not further consolidate the results of the expansion. By adding `PP_IDENTITY`, the preprocessor can evaluate the expanded `PP_COMMA()` to `,`.

#### Concatenation

Since `##` does not expand the left and right parameters during concatenation, in order to allow the parameters to be evaluated and then concatenated, we can write it like this:

``` cpp
#define PP_IF(cond, true_value, false_value) PP_CONCAT(PP_IF_, PP_BOOL(cond))(true_value, false_value)
// 定义了一个宏 PP_IF，接受三个参数：条件、真值和假值。根据条件的真假来选择返回真值还是假值。

#define PP_IF_0(true_value, false_value) false_value
#define PP_IF_1(true_value, false_value) true_value

PP_IF(1, "yes", "no")       // -> PP_IF_1("yes", "no") -> "yes"
PP_IF(0, "yes", "no")       // -> PP_IF_0("yes", "no") -> "no"
```

当条件为真时，返回真值；当条件为假时，返回假值。

#### 循环展开

通过循环展开，可以重复执行一段代码若干次。

这里定义一个展开一次的宏 `PP_EXPAND_ONCE`：

``` cpp
#define PP_EXPAND_ONCE(...) __VA_ARGS__
```

通过宏展开规则 `__VA_ARGS__`，可以保证在展开时不对传入的参数进行求值。定义一个新的宏 `PP_REPEAT`，它接受两个参数：重复次数和要重复的代码块。

``` cpp
#define PP_REPEAT(count, code_block) PP_REPEAT_IMPL(count, code_block)
#define PP_REPEAT_IMPL(count, code_block) PP_CONCAT(PP_REPEAT_, count)(code_block)

#define PP_REPEAT_0(code_block)
#define PP_REPEAT_1(code_block) PP_EXPAND_ONCE(code_block)
#define PP_REPEAT_2(code_block) PP_REPEAT_1(code_block) PP_EXPAND_ONCE(code_block)
#define PP_REPEAT_3(code_block) PP_REPEAT_2(code_block) PP_EXPAND_ONCE(code_block)
// ...

// 展开若干次，重复执行 code_block
PP_REPEAT(3, printf("Hello, world!\n"))  
// 展开为：printf("Hello, world!\n") printf("Hello, world!\n") printf("Hello, world!\n")
```

`PP_REPEAT_IMPL` 宏根据传入的重复次数，展开对应次数的重复代码块。每次展开都是通过重复展开上一次的代码块再加上一个新的代码块来实现的。

这样就实现了循环展开的效果，可以用来避免手写大量重复的代码。

``` cpp
#define PP_IF(if, then, else) PP_CONCAT(PP_IF_, PP_BOOL(if))(then, else)
#define PP_IF_1(then, else) then
#define PP_IF_0(then, else) else

PP_IF(1, 2, 3)      // -> PP_IF_1(2, 3) -> 2
PP_IF(0, 2, 3)      // -> PP_IF_0(2, 3) -> 3
```

If the value of `if` is `1`, it is concatenated with `PP_CONCAT` to become `PP_IF_1`, and finally expands to the value of `then`. Likewise, if `if` evaluates to `0`, `PP_IF_0` is obtained.

#### Increment and Decrement

Integer increment and decrement:

``` cpp
#define PP_INC(arg0) PP_CONCAT(PP_INC_, arg0)
#define PP_INC_0 1
#define PP_INC_1 2
#define PP_INC_2 3
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

Similar to `PP_BOOL`, there are also limits to the range of integer increment and decrement. Here, the range is set to `[0, 256]`. After incrementing to `256`, for safety reasons, `PP_INC_256` will return itself `256` as a boundary, and likewise `PP_DEC_0` will also return `0`.

#### Variadic Parameters

Macros can accept variadic parameters, in the format:

```cpp 
#define LOG(format, ...) printf("log: " format, __VA_ARGS__)

LOG("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG("Hello World")              // -> printf("log: " "Hello World", ); there is an extra comma, compilation error
```

Since variadic parameters can be empty, an empty scenario can lead to compilation failure. Therefore, C++20 introduced `__VA_OPT__`. If the variadic parameters are empty, it returns nothing; otherwise, it returns the original parameters:

```cpp 
#define LOG2(format, ...) printf("log: " format __VA_OPT__(,) __VA_ARGS__)

LOG2("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG2("Hello World")              // -> printf("log: " "Hello World" ); no comma, compiles correctly
```

Unfortunately, `__VA_OPT__` is only available in C++20 and later standards. In the following discussions, we will provide an implementation method for `__VA_OPT__`.

#### Lazy Evaluation

Consider this situation:

``` cpp
PP_IF(1, PP_COMMA(), PP_LPAREN())     // -> PP_IF_1(,,)) -> error: unterminated argument list invoking macro "PP_IF_1"
```


We know that when macros are expanded, the first parameter is evaluated. After evaluating `PP_COMMA()` and `PP_LPAREN()`, they are passed to `PP_IF_1`, resulting in `PP_IF_1(,,))`, which causes a preprocessing error. In this case, a method called lazy evaluation can be used:

``` cpp
PP_IF(1, PP_COMMA, PP_LPAREN)()       // -> PP_IF_1(PP_COMMA, PP_LPAREN)() -> PP_COMMA() -> ,
```

To modify this syntax, only the macro name is passed, so that `PP_IF` can select the desired macro name and then concatenate it with parentheses `()` to form a complete macro, which is then expanded. Lazy evaluation is also common in macro programming.

#### Begin with parentheses

Determine if the variable arguments start with parentheses:

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

`PP_IS_BEGIN_PARENS` can be used to determine whether the passed arguments start with parentheses, which is necessary when processing parenthesized parameters (such as the `__VA_OPT__` implementation mentioned later). It looks a bit complex, but the core idea is to construct a macro that evaluates to one result if the variable arguments start with parentheses, or evaluates to another result otherwise. Let's take a closer look:

The macro `PP_IS_BEGIN_PARENS_PROCESS` and `PP_IS_BEGIN_PARENS_PROCESS_0` are used to evaluate the variable arguments and then retrieve the 0th argument.

The macro `PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__)` first evaluates `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` and then concatenates the result with `PP_IS_BEGIN_PARENS_PRE_`.

`PP_IS_BEGIN_PARENS_EAT(...)` macro will consume all arguments and return 1 if the previous step `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` has arguments that start with parentheses. In this case, it will match the evaluation of `PP_IS_BEGIN_PARENS_EAT(...)` and return 1. Conversely, if it does not start with parentheses, there is no match and `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` remains unchanged.

If `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` evaluates to 1, `PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, 1) -> PP_IS_BEGIN_PARENS_PRE_1 -> 1,` note that there is a comma after 1, the value `1,` is passed to `PP_IS_BEGIN_PARENS_PROCESS_0`, which takes the 0th argument, resulting in `1`, indicating that the argument starts with parentheses.

If `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` evaluates to a value other than 1 and remains unchanged, `PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__) -> PP_IS_BEGIN_PARENS_PRE_PP_IS_BEGIN_PARENS_EAT __VA_ARGS__ -> 0, __VA_ARGS__`, is passed to `PP_IS_BEGIN_PARENS_PROCESS_0` and the result is `0`, indicating that the argument does not start with parentheses.

#### Variadic Parameters Empty

Determining if variadic parameters are empty is also a common macro, and it is used in implementing `__VA_OPT__`. Here we can use `PP_IS_BEGIN_PARENS` to write an incomplete version:

``` cpp
#define PP_IS_EMPTY_PROCESS(...) \
    PP_IS_BEGIN_PARENS(PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ())
#define PP_IS_EMPTY_PROCESS_EAT(...) ()

PP_IS_EMPTY_PROCESS()       // -> 1
PP_IS_EMPTY_PROCESS(1)      // -> 0
PP_IS_EMPTY_PROCESS(1, 2)   // -> 0
PP_IS_EMPTY_PROCESS(())     // -> 1
```

The purpose of `PP_IS_EMPTY_PROCESS` is to determine if `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ()` starts with parentheses.

If `__VA_ARGS__` is empty, `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ () -> PP_IS_EMPTY_PROCESS_EAT() -> ()`, the result is a pair of parentheses `()`, which is then passed to `PP_IS_BEGIN_PARENS` to return 1, indicating that the argument is empty.

Otherwise, `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ()` is passed unchanged to `PP_IS_BEGIN_PARENS`, which returns 0, indicating non-empty.

Note the fourth example `PP_IS_EMPTY_PROCESS(()) -> 1`, `PP_IS_EMPTY_PROCESS` cannot handle variadic parameters that start with parentheses correctly because in this case, the parentheses introduced by the variadic parameters will match `PP_IS_EMPTY_PROCESS_EAT`, resulting in the evaluation of `()`. To solve this problem, we need to handle the case of whether the argument starts with parentheses or not:

``` cpp
#define PP_IS_EMPTY(...) \
    PP_IS_EMPTY_IF(PP_IS_BEGIN_PARENS(__VA_ARGS__)) \
        (PP_IS_EMPTY_ZERO, PP_IS_EMPTY_PROCESS)(__VA_ARGS__)
```

``` cpp
#define PP_IS_EMPTY_IF(if) PP_CONCAT(PP_IS_EMPTY_IF_, if)
#define PP_IS_EMPTY_IF_1(then, else) then
#define PP_IS_EMPTY_IF_0(then, else) else
    
#define PP_IS_EMPTY_ZERO(...) 0

PP_IS_EMPTY()       // -> 1
PP_IS_EMPTY(1)      // -> 0
PP_IS_EMPTY(1, 2)   // -> 0
PP_IS_EMPTY(())     // -> 0
```

The `PP_IS_EMPTY_IF` macro returns the 0th or the 1st parameter based on the `if` condition.

If the variable arguments start with parentheses, `PP_IS_EMPTY_IF` returns `PP_IS_EMPTY_ZERO` which eventually returns 0, indicating that the variable arguments are not empty.

Otherwise, `PP_IS_EMPTY_IF` returns `PP_IS_EMPTY_PROCESS` and `PP_IS_EMPTY_PROCESS` determines whether the variable arguments are empty.

#### Element Access

Get the element at the specified position in the variable arguments:

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

The first parameter of `PP_ARGS_ELEM` is the element index `I`, followed by the variable arguments. By concatenating `PP_ARGS_ELEM_` and `I` using `PP_CONCAT`, the macro `PP_ARGS_ELEM_0..8` that returns the element at the corresponding position is obtained. Then, the variable arguments are passed to this macro to expand and return the element at the specified index.

#### PP_IS_EMPTY2

Using `PP_ARGS_ELEM`, another version of `PP_IS_EMPTY` can be implemented:

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
```

```cpp
PP_IS_EMPTY2()              // -> 1
PP_IS_EMPTY2(a)             // -> 0
PP_IS_EMPTY2(a, b)          // -> 0
PP_IS_EMPTY2(())            // -> 0
PP_IS_EMPTY2(PP_COMMA)      // -> 0
```

Using `PP_ARGS_ELEM` to determine if the argument contains a comma `PP_HAS_COMMA`. `PP_COMMA_ARGS` will consume any passed arguments and return a comma.

The basic logic for determining if the variable arguments are empty is `PP_COMMA_ARGS __VA_ARGS__ ()`, which returns a comma. In other words, if `__VA_ARGS__` is empty, when `PP_COMMA_ARGS` is concatenated with `()`, it is evaluated as `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ())`.

However, there are exceptions:

* `__VA_ARGS__` itself may contain a comma;
* Concatenation of `__VA_ARGS__ ()` can result in the evaluation producing a comma;
* Concatenation of `PP_COMMA_ARGS __VA_ARGS__` can result in the evaluation producing a comma;

To handle these three exceptions, the final implementation is equivalent to applying a logical AND to the following four conditions:

* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__))` &&
* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__()))` &&
* `PP_NOT(PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__))` &&
* `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ())`

#### `__VA_OPT__`

Using `PP_IS_EMPTY`, we can finally implement a macro similar to `__VA_OPT__`:

```cpp
#define PP_REMOVE_PARENS(tuple) PP_REMOVE_PARENS_IMPL tuple
#define PP_REMOVE_PARENS_IMPL(...) __VA_ARGS__

#define PP_ARGS_OPT(data_tuple, empty_tuple, ...) \
    PP_ARGS_OPT_IMPL(PP_IF(PP_IS_EMPTY(__VA_ARGS__), empty_tuple, data_tuple))
#define PP_ARGS_OPT_IMPL(tuple) PP_REMOVE_PARENS(tuple)

PP_ARGS_OPT((data), (empty))        // -> empty
PP_ARGS_OPT((data), (empty), 1)     // -> data
PP_ARGS_OPT((,), (), 1)             // -> ,

```

`PP_ARGS_OPT` takes two fixed parameters and variable arguments. When the variable arguments are not empty, it returns `data`; otherwise, it returns `empty`. To support commas in `data` and `empty`, both of them need to be enclosed in parentheses, and `PP_REMOVE_PARENS` is used to remove the outer parentheses.

With `PP_ARGS_OPT`, we can implement `LOG3` to achieve the functionality similar to `LOG2`:

```cpp
#define LOG3(format, ...) \
    printf("log: " format PP_ARGS_OPT((,), (), __VA_ARGS__) __VA_ARGS__)

LOG3("Hello");                  // -> printf("log: " "Hello" );
LOG3("Hello %s", "World");      // -> printf("log: " "Hello %s" , "World");
```


`data_tuple` is `()`, if the variable-length parameter is not empty, it will return all the elements in `data_tuple`, which is a comma `,` here.

#### Calculate the number of parameters

To get the number of variable-length parameters:

```cpp
#define PP_ARGS_SIZE_IMCOMPLETE(...) \
    PP_ARGS_ELEM(8, __VA_ARGS__, 8, 7, 6, 5, 4, 3, 2, 1, 0)

PP_ARGS_SIZE_IMCOMPLETE(a)             // -> 1
PP_ARGS_SIZE_IMCOMPLETE(a, b)          // -> 2
PP_ARGS_SIZE_IMCOMPLETE(PP_COMMA())    // -> 2
PP_ARGS_SIZE_IMCOMPLETE()              // -> 1
```

The number of variable-length parameters is calculated by counting the position of the parameters. `__VA_ARGS__` causes the subsequent parameters to shift to the right. Use the macro `PP_ARGS_ELEM` to get the parameter at the 8th position. If `__VA_ARGS__` has only one parameter, the 8th parameter is equal to `1`; similarly, if `__VA_ARGS__` has two parameters, the 8th parameter becomes `2`, which is exactly equal to the number of variable-length parameters.

The example given here only supports a maximum of 8 variable-length parameters, which is dependent on the maximum length supported by `PP_ARGS_ELEM`.

However, this macro is incomplete. In the case of an empty variable-length parameter, this macro will incorrectly return `1`. If you need to handle empty variable-length parameters, you need to use the `PP_ARGS_OPT` macro mentioned earlier:

```cpp
#define PP_COMMA_IF_ARGS(...) PP_ARGS_OPT((,), (), __VA_ARGS__)
#define PP_ARGS_SIZE(...) PP_ARGS_ELEM(8, __VA_ARGS__ PP_COMMA_IF_ARGS(__VA_ARGS__) 8, 7, 6, 5, 4, 3, 2, 1, 0, 0, 0)

PP_ARGS_SIZE(a)             // -> 1
PP_ARGS_SIZE(a, b)          // -> 2
PP_ARGS_SIZE(PP_COMMA())    // -> 2
PP_ARGS_SIZE()              // -> 0
PP_ARGS_SIZE(,,,)           // -> 4
```

The key to the problem is the comma `,`. When `__VA_ARGS__` is empty, removing the comma can correctly return `0`.

#### Iterate through access

Similar to C++'s `for_each`, we can implement the macro `PP_FOR_EACH`:

```cpp
#define PP_FOR_EACH(macro, contex, ...) \
    PP_CONCAT(PP_FOR_EACH_, PP_ARGS_SIZE(__VA_ARGS__))(0, macro, contex, __VA_ARGS__)

#define PP_FOR_EACH_0(index, macro, contex, ...)
#define PP_FOR_EACH_1(index, macro, contex, arg, ...) macro(index, contex, arg)

#define PP_FOR_EACH_2(index, macro, contex, arg, ...) \
    macro(index, contex, arg) \
    PP_FOR_EACH_1(PP_INC(index), macro, contex, __VA_ARGS__)


```cpp
#define PP_FOR_EACH_3(index, macro, context, arg, ...) \
    macro(index, context, arg) \
    PP_FOR_EACH_2(PP_INC(index), macro, context, __VA_ARGS__)
// ...
#define PP_FOR_EACH_8(index, macro, context, arg, ...) \
    macro(index, context, arg) \
    PP_FOR_EACH_7(PP_INC(index), macro, context, __VA_ARGS__)

#define DECLARE_EACH(index, context, arg)    PP_IF(index, PP_COMMA, PP_EMPTY)() context arg

PP_FOR_EACH(DECLARE_EACH, int, x, y, z);    // -> int x, y, z;
PP_FOR_EACH(DECLARE_EACH, bool, a, b);      // -> bool a, b;
```

`PP_FOR_EACH` function takes two fixed parameters: `macro`, which can be understood as the macro to be invoked during traversal, and `context`, which can be used as a predetermined value passed to `macro`. `PP_FOR_EACH` first gets the length `N` of the variable-length parameters using `PP_ARGS_SIZE`, then concatenates with `PP_CONCAT` to obtain `PP_FOR_EACH_N`, after which `PP_FOR_EACH_N` will recursively call `PP_FOR_EACH_N-1` to achieve the same number of iterations as the variable-length parameters.

In the example, we declare `DECLARE_EACH` as the `macro` parameter. The purpose of `DECLARE_EACH` is to return `context arg`. If `context` is a type name and `arg` is a variable name, `DECLARE_EACH` can be used to declare variables.

#### Conditional Loop

With `FOR_EACH`, we can also write `PP_WHILE` in a similar way:

```cpp
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
```

```cpp
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

`PP_WHILE` accepts three arguments: `pred` for the conditional function, `op` for the operation function, and `val` as the initial value. During the loop, `pred(val)` is repeated to check if the loop should terminate, and the value obtained from `op(val)` is passed to the subsequent macros. It can be understood as executing the following code:

```cpp
while (pred(val)) {
    val = op(val);
}
```

`PP_WHILE_N` first uses `pred(val)` to obtain the result of the conditional check, and passes the condition result `cond` and the remaining parameters to `PP_WHILE_N_IMPL`.
`PP_WHILE_N_IMPL` can be divided into two parts: the latter half `(pred, op, PP_IF(cond, op, PP_EMPTY_EAT)(val))` is used as the parameter for the former part. `PP_IF(cond, op, PP_EMPTY_EAT)(val)` evaluates to `op(val)` if `cond` is true, otherwise it evaluates to `PP_EMPTY_EAT(val)` and returns an empty value. The former part `PP_IF(cond, PP_WHILE_N+1, val PP_EMPTY_EAT)` returns `PP_WHILE_N+1` if `cond` is true, continuing the loop in combination with the parameters of the latter half; otherwise it returns `val PP_EMPTY_EAT`, where `val` is the final result of the calculation, and `PP_EMPTY_EAT` will discard the result of the latter half.

`SUM` calculates `N + N-1 + ... + 1`. The initial value is `(max_num, origin_num)`; `SUM_PRED` takes the first element `x` and checks whether it is greater than 0; `SUM_OP` decrements `x` by `x = x - 1` and adds `x` to `y` by `y = y + x`. `SUM_PRED` and `SUM_OP` are passed directly to `PP_WHILE`, and the result returned is a tuple. The desired result is the second element of the tuple, so we use `SUM` again to get the value of the second element.

#### Recursion

So far, our traversal access and conditional loop have been working well, producing the expected results. Do you remember when we mentioned the prohibition of recursive reentry when we talked about macro expansion rules? Unfortunately, we encounter the prohibition of recursive reentry when we want to perform nested loops:

```cpp
#define SUM_OP2(xy_tuple) SUM_OP_OP_IMPL2 xy_tuple
#define SUM_OP_OP_IMPL2(x, y) (PP_DEC(x), y + SUM(x, 0))

#define SUM2(max_num, origin_num) \
    PP_IDENTITY(SUM_IMPL PP_WHILE(SUM_PRED, SUM_OP2, (max_num, origin_num)))

SUM2(1, a)      // -> a + SUM_IMPL PP_WHILE_1(SUM_PRED, SUM_OP, (1, a))
```

In `SUM2`, the parameter `op` is replaced by `SUM_OP2`, and `SUM_OP2` calls `SUM`, which in turn expands to `PP_WHILE_1`, effectively causing `PP_WHILE_1` to call itself recursively, causing the preprocessor to stop expanding.

To solve this problem, we can use a method called Automatic Recursion:

```cpp
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

`PP_AUTO_WHILE` is an automatic recursion version of `PP_WHILE`, and the core macro is `PP_AUTO_REC(PP_WHILE_PRED)`, which can find the current available version number `N` of `PP_WHILE_N`.

The principle of deduction is very simple, that is, to search all versions and find the version that can be expanded correctly, and return the number of that version. In order to improve the search speed, the common practice is to use binary search, which is what `PP_AUTO_REC` does. `PP_AUTO_REC` accepts a parameter `check`, which is responsible for checking the availability of versions. Here, the support for searching version range `[1, 4]` is given. `PP_AUTO_REC` will first check `check(2)`. If `check(2)` is true, it will call `PP_AUTO_REC_12` to search the range `[1, 2]`, otherwise it will use `PP_AUTO_REC_34` to search `[3, 4]`. `PP_AUTO_REC_12` checks `check(1)`. If it is true, it means that version `1` is available, otherwise it uses version `2`. `PP_AUTO_REC_34` works the same way.

How should the `check` macro be written to determine the availability of versions? Here, `PP_WHILE_PRED` will be expanded into two parts of concatenation. Let's look at the latter part `PP_WHILE_ ## n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`: if `PP_WHILE_ ## n` is available, because `PP_WHILE_FALSE` always returns `0`, this part will be expanded to the value of the `val` parameter, which is `PP_WHILE_FALSE`; otherwise, this macro will remain unchanged and still be `PP_WHILE_n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`.

Concatenate the result of the latter part with the front part `PP_WHILE_CHECK_` to get two results: `PP_WHILE_CHECK_PP_WHILE_FALSE` or `PP_WHILE_CHECK_PP_WHILE_n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`. Therefore, we let `PP_WHILE_CHECK_PP_WHILE_FALSE` return `1` to indicate availability, and `PP_WHILE_CHECK_PP_WHILE_n` returns `0` to indicate unavailability. Thus, we have completed the functionality of automatic deduction.

#### Arithmetic comparison

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

```cpp

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

It determines whether the values are equal. It uses the feature of forbidding recursive entry to concatenate `x` and `y` recursively into the macro `PP_NOT_EQUAL_x PP_NOT_EQUAL_y`. If `x == y`, the `PP_NOT_EQUAL_y` macro will not be expanded, and it will be concatenated with `PP_NOT_EQUAL_CHECK_` to form `PP_NOT_EQUAL_CHECK_PP_NOT_EQUAL_y` which returns `0`; conversely, if both are expanded successfully, they will ultimately obtain `PP_EQUAL_NIL`, which is concatenated to obtain `PP_NOT_EQUAL_CHECK_PP_EQUAL_NIL` and returns `1`.

Equal:

```cpp
#define PP_EQUAL(x, y) PP_NOT(PP_NOT_EQUAL(x, y))

PP_EQUAL(1, 1)              // -> 1
PP_EQUAL(1, 3)              // -> 0

```

Less than or equal to:

```cpp
#define PP_LESS_EQUAL(x, y) PP_NOT(PP_SUB(x, y))

PP_LESS_EQUAL(2, 1)         // -> 0
PP_LESS_EQUAL(1, 1)         // -> 1
PP_LESS_EQUAL(1, 2)         // -> 1
```

Less than:

```cpp
#define PP_LESS(x, y) PP_AND(PP_LESS_EQUAL(x, y), PP_NOT_EQUAL(x, y))

PP_LESS(2, 1)               // -> 0
PP_LESS(1, 2)               // -> 1
PP_LESS(2, 2)               // -> 0
```

In addition, there are arithmetic comparisons such as greater than, greater than or equal to, and so on. They are not discussed here.

#### Arithmetic operations

Using `PP_AUTO_WHILE`, we can now implement basic arithmetic operations, supporting nested operations.

Addition:

```cpp
#define PP_ADD(x, y) \
    PP_IDENTITY(PP_ADD_IMPL PP_AUTO_WHILE(PP_ADD_PRED, PP_ADD_OP, (x, y)))
#define PP_ADD_IMPL(x, y) x

#define PP_ADD_PRED(xy_tuple) PP_ADD_PRED_IMPL xy_tuple
#define PP_ADD_PRED_IMPL(x, y) y

#define PP_ADD_OP(xy_tuple) PP_ADD_OP_IMPL xy_tuple
#define PP_ADD_OP_IMPL(x, y) (PP_INC(x), PP_DEC(y))
```

```
Addition:
```cpp
#define PP_ADD(x, y) \
    PP_IDENTITY(PP_ADD_IMPL PP_AUTO_WHILE(PP_ADD_PRED, PP_ADD_OP, (x, y)))
#define PP_ADD_IMPL(x, y) x

#define PP_ADD_PRED(xy_tuple) PP_ADD_PRED_IMPL xy_tuple
#define PP_ADD_PRED_IMPL(x, y) y

#define PP_ADD_OP(xy_tuple) PP_ADD_OP_IMPL xy_tuple
#define PP_ADD_OP_IMPL(x, y) (PP_INC(x), PP_DEC(y))

PP_ADD(1, 2)                // -> 3
PP_ADD(1, PP_ADD(1, 2))     // -> 4
```

Subtraction:
```cpp
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
```cpp
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

In the multiplication implementation, an additional parameter `ret` is added with an initial value of `0`. It is updated by `ret = ret + x` in each iteration.

Division:
```cpp
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

The division operation utilizes `PP_LESS_EQUAL`, which continues the loop only if `y <= x`.

#### Data Structures

Macros can also have data structures. In fact, we have already used a data structure called `tuple` in the earlier examples. `PP_REMOVE_PARENS` is used to remove the outer parentheses of the `tuple` and return the elements inside. Here, we will use `tuple` as an example to discuss its implementation. If you are interested in other data structures like `list` or `array`, you can take a look at the implementation in Boost library.

A `tuple` is defined as a collection of elements enclosed in parentheses and separated by commas: `(a, b, c)`.
```


```cpp
#define PP_TUPLE_REMOVE_PARENS(tuple) PP_REMOVE_PARENS(tuple)

// Obtain the element at the specified index
#define PP_TUPLE_ELEM(i, tuple) PP_ARGS_ELEM(i, PP_TUPLE_REMOVE_PARENS(tuple))

// Consume the entire tuple and return empty
#define PP_TUPLE_EAT() PP_EMPTY_EAT

// Obtain the size
#define PP_TUPLE_SIZE(tuple) PP_ARGS_SIZE(PP_TUPLE_REMOVE_PARENS(tuple))

// Add an element
#define PP_TUPLE_PUSH_BACK(elem, tuple) \
    PP_TUPLE_PUSH_BACK_IMPL(PP_TUPLE_SIZE(tuple), elem, tuple)
#define PP_TUPLE_PUSH_BACK_IMPL(size, elem, tuple) \
    (PP_TUPLE_REMOVE_PARENS(tuple) PP_IF(size, PP_COMMA, PP_EMPTY)() elem)

// Insert an element
#define PP_TUPLE_INSERT(i, elem, tuple) \
    PP_TUPLE_ELEM( \
        3, \
        PP_AUTO_WHILE( \
            PP_TUPLE_INSERT_PRED, \
            PP_TUPLE_INSERT_OP, \
            (0, i, elem, (), tuple) \
        ) \
    )
#define PP_TUPLE_INSERT_PRED(args) PP_TUPLE_INSERT_PRED_IMPL args 
#define PP_TUPLE_INSERT_PRED_IMPL(curi, i, elem, ret, tuple) \
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
```

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

// Remove an element
#define PP_TUPLE_REMOVE(i, tuple) \
    PP_TUPLE_ELEM( \
        2, \
        PP_AUTO_WHILE( \
            PP_TUPLE_REMOVE_PRED, \
            PP_TUPLE_REMOVE_OP, \
            (0, i, (), tuple) \
        ) \
    )

PP_TUPLE_SIZE(())               // -> 0

PP_TUPLE_PUSH_BACK(2, (1))      // -> (1, 2)
PP_TUPLE_PUSH_BACK(2, ())       // -> (2)

PP_TUPLE_INSERT(1, 2, (1, 3))   // -> (1, 2, 3)

PP_TUPLE_POP_BACK(())           // -> ()
PP_TUPLE_POP_BACK((1))          // -> ()
PP_TUPLE_POP_BACK((1, 2, 3))    // -> (1, 2)

```
PP_TUPLE_REMOVE(1, (1, 2, 3))   // -> (1, 3)
PP_TUPLE_REMOVE(0, (1, 2, 3))   // -> (2, 3)
```

Let me give a brief explanation of the implementation of inserting elements. Similar principles are used to implement other operations such as removing elements. `PP_TUPLE_INSERT(i, elem, tuple)` allows us to insert the element `elem` at position `i` in the `tuple`. To accomplish this, we first use `PP_TUPLE_PUSH_BACK` to move all the elements with positions less than `i` to a new `tuple` called `ret`. Then we place the element `elem` at position `i` in `ret`, and finally append the elements in the original `tuple` with positions greater than or equal to `i` to `ret`. As a result, `ret` gives us the desired outcome.

## Conclusion

The purpose of this article is to explain the principles and basic implementation of C/C++ macro programming. While documenting my own understanding and insights, I hope it can also provide some clarification and inspiration to others. It should be noted that although this article has been a bit lengthy, it still does not cover some macro programming techniques and usages, such as the recursive calling method based on delayed expansion proposed by CHAOS_PP, or the `REPEAT` macro in BOOST_PP. For those interested, further reading is recommended.

Debugging macro programming can be a painful process. Here are some approaches:

* Use the `-P -E` options to output the preprocessed result.
* Carefully study the expansion process using the modified version of `clang` mentioned earlier.
* Break down complex macros and examine the intermediate results of macro expansion.
* Shield irrelevant headers and macros.
* Ultimately, it is necessary to mentally simulate the macro expansion process. Familiarity with macro expansion will improve debugging efficiency.

The macros in this article are my own implementation after understanding the principles. Some macros are inspired by the implementation in Boost and referenced articles. If there are any errors, please feel free to point them out and reach out to me for further discussion.

All the code in this article can be found here: [Download](assets/img/2021-3-31-cpp-preprocess/macors.cpp), [Online Demo](https://godbolt.org/z/coWvc5Pse).

## References

* [Boost.Preprocessor](https://www.boost.org/doc/libs/1_75_0/libs/preprocessor/doc/)
* [The Art of Macro Programming in C/C++](https://bot-man-jl.github.io/articles/?post=2020/Macro-Programming-Art)

> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.