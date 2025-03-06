---
layout: post
title: C/C++ 매크로 프로그래밍 분석
categories:
- c++
catalog: true
tags:
- dev
description: 본문의 목적은 C/C++ 매크로 프로그래밍 규칙과 구현 방법을 명확하게 설명하여 코드 안의 매크로를 더 이상 두려워하지 않도록
  하는 것입니다.
figures: []
---

<meta property="og:title" content="C/C++ 宏编程解析" />

본문의 목적은 C/C++의 매크로 프로그래밍 규칙과 구현 방법을 명확히 설명하여 코드 내 매크로를 두려워하지 않도록 하는 것입니다. 먼저 C++ 표준 14에서 매크로 확장에 관한 규칙을 설명한 후 Clang 소스 코드를 수정하여 매크로 확장을 관찰하고, 마지막으로 이러한 지식을 기반으로 매크로 프로그래밍을 구현하는 방법에 대해 이야기할 것입니다.

해당 텍스트의 코드는 모두 여기 있습니다: [다운로드](assets/img/2021-3-31-cpp-preprocess/macros.cpp)，[온라인 데모](https://godbolt.org/z/coWvc5Pse)I'm sorry, but there is no text to translate.

##서문

우리는 파일 `a.cpp`에 대해 컴파일러가 전처리만 수행하고 결과를 `a.cpp.i`에 저장하도록 하는 명령 `gcc -P -E a.cpp -o a.cpp.i`를 실행하여 가능합니다.

먼저 몇 가지 예시를 살펴보겠습니다:

####재진입(recursion)

``` cpp
#define ITER(arg0, arg1) ITER(arg1, arg0)

ITER(1, 2)          // -> ITER(2, 1)
```

매크로 `ITER`는 `arg0`, `arg1`의 위치를 교환했습니다. 매크로를 펼치면 `ITER(2, 1)`이 됩니다.

`arg0` `arg1`의 위치가 성공적으로 교환되었다는 점을 알 수 있습니다. 여기에서 매크로가 한 번 성공적으로 펼쳐졌지만, 한 번만 펼쳐졌으며 재귀 진입하지 않았습니다. 다시 말해, 매크로가 펼쳐지는 과정에서 자체 재귀 진입이 불가능합니다. 이전 재귀에서 동일한 매크로가 이미 펼쳐졌음을 발견하면 더 이상 펼쳐지지 않습니다. 이것은 매크로 펼침의 중요한 규칙 중 하나입니다. 재귀 진입을 금지하는 이유는 간단합니다. 즉, 무한 재귀를 피하기 위해서입니다.

####문자열 연결

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                // -> HelloWorld
CONCAT(Hello, CONCAT(World, !))     // ->　HelloCONCAT(World, !)
```

`CONCAT` 매크로는 `arg0`와 `arg1`을 연결하는 목적을 가지고 있습니다. 매크로가 펼쳐진 후 `CONCAT(Hello, World)`는 정확한 결과 `HelloWorld`를 반환할 수 있습니다. 그러나 `CONCAT(Hello, CONCAT(World, !))`는 외부 매크로 만 펼쳐지며 내부의 `CONCAT(World, !)`는 펼쳐지지 않고 직접 `Hello`와 결합됩니다. 이는 우리의 예상과 다르며, 우리가 원하는 결과는 실제로 `HelloWorld!`입니다. 이것이 또 다른 중요한 매크로 확장 규칙 중 하나이며, `##` 연산자 뒤에오는 매크로 인수는 확장되지 않고 직접 앞의 내용과 연결됩니다.

위의 두 예시를 통해 확장 매크로 규칙 중에는 직관에 반하는 것도 있음을 알 수 있습니다. 구체적인 규칙을 명확히 이해하지 못하면 우리가 원하는 결과와 일치하지 않을 수 있습니다.

##톈장(宏展)개(開) 규칙(规则)

이 두 예시를 통해 우리는 매크로 확장에는 표준 규칙이 있다는 것을 알 수 있습니다. 이 규칙은 C/C++ 표준에서 정의되어 있으며 내용이 많지 않습니다. 몇 번 정독을 권장합니다. 여기서 표준 n4296 버전 링크를 첨부해 드리며 매크로 확장은 16.3 절에서 다루고 있습니다. [링크](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4296.pdf). 아래에서는 n4296 버전에서 몇 가지 중요한 규칙을 선택했습니다. 이러한 규칙은 매크로를 올바르게 작성하는 방법을 결정합니다(표준에서 매크로를 자세히 읽는 것을 권장합니다).

####매개변수 구분

매크로의 매개변수 요구사항은 쉼표로 구분되며 매크로 정의의 수와 매개변수의 수가 일치해야 합니다. 매크로에 전달되는 매개변수 중 괄호로 묶인 추가 내용은 하나의 매개변수로 간주되며 매개변수는 비어 있을 수 있습니다.

``` cpp
#define ADD_COMMA(arg1, arg2) arg1, arg2

ADD_COMMA(a, b)             // -> a, b
ADD_COMMA(a)                // "MACRO" 매크로는 2개의 인수가 필요하지만 1개만 제공되었습니다.
ADD_COMMA((a, b), c)        // -> (a, b), c
ADD_COMMA(, b)              // -> , b
```

`ADD_COMMA((a, b), c)` 에서는 `(a, b)` 를 첫 번째 인수로 간주합니다. `ADD_COMMA(, b)` 에서 첫 번째 인수가 비어 있기 때문에 `, b`로 전개됩니다.

####매크로 매개변수 전개

매크로를 확장할 때, 매크로의 매개변수도 확장 가능한 매크로인 경우, 매개변수를 먼저 완전히 확장한 후에 매크로를 확장합니다. 예를 들어,

``` cpp
ADD_COMMA(ADD_COMMA(1, 2), ADD_COMMA(3, 4))     // -> 1, 2, 3, 4
```

보통 매크로 전개는 일반적으로 매개변수를 먼저 평가한 후 매크로를 해석한다고 볼 수 있습니다. `#` 및 `##` 연산자를 만나지 않는 한요.

####`#` 연산자

`#` 는 다음에 나오는 매크로 매개변수를 풀지 않고 직접적으로 문자열로 만듭니다. 예를 들어:

``` cpp
#define STRINGIZE(arg0) # arg0

STRINGIZE(a)                // -> "a"
STRINGIZE(STRINGIZE(a))     // -> "STRINGIZE(a)"
```

이 규칙에 따르면 `STRINGIZE(STRINGIZE(a))`는 `"STRINGIZE(a)"`로만 확장될 수 있습니다.

####`##` 연산자

`##` 오퍼랜드 앞뒤의 매크로 매개변수는 펼쳐지지 않고 직접 연결되므로 다음과 같습니다:

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                        // -> HelloWorld
CONCAT(Hello, CONCAT(World, !))             // -> HelloCONCAT(World, !)
CONCAT(CONCAT(Hello, World) C, ONCAT(!))    // -> CONCAT(Hello, World) CONCAT(!)
```

`CONCAT(CONCAT(Hello, World) C, ONCAT(!))` 는 먼저 연결해야 하며, `CONCAT(Hello, World) CONCAT(!)`를 얻습니다.

####반복 스캔

매크로 확장이 한 번 실행된 후, 전처리기는 결과물을 다시 스캔하고 계속해서 확장을 진행합니다. 더 이상 확장할 내용이 없을 때까지.

한번의 매크로 확장은 매개변수를 완전히 확장한 다음에 (`#` 또는 `##`을 만날 때까지), 매크로의 정의에 따라 매크로와 완전히 확장된 매개변수를 정의에 따라 치환하고, 그 정의에서 모든 `#`과 `##` 연산자를 처리한다.

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define STRINGIZE(arg0) # arg0

CONCAT(STRING, IZE(Hello))        // -> STRINGIZE(Hello) -> "Hello"
```

`CONCAT(STRING, IZE(Hello))` 처음 스캔을 통해 `STRINGIZE(Hello)`로 전개되며, 두 번째 스캔에서 `STRINGIZE`를 계속 확장할 수 있다는 것을 발견하여 최종적으로 `"Hello"`를 얻게 됩니다.

####재귀 재진입 금지

반복 스캔 과정에서는 동일한 매크로를 재귀적으로 펼치는 것을 금지합니다. 매크로 펼치기를 트리 구조로 이해할 수 있으며, 루트 노드는 처음에 펼쳐야 하는 매크로이며, 각 매크로 펼친 후의 내용은 해당 매크로의 자식 노드로 연결되어 트리에 추가됩니다. 따라서 재귀를 금지하는 것은 자식 노드의 매크로를 펼칠 때, 해당 매크로가 어떤 조상 노드의 매크로와도 동일하다면 펼치지 않도록 하는 것입니다. 몇 가지 예시를 살펴보겠습니다:

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define CONCAT_SPACE(arg0, arg1) arg0 arg1
#define IDENTITY(arg0) IDENTITY_IMPL(arg0)
#define IDENTITY_IMPL(arg0) arg0

CONCAT(CON, CAT(a, b))                  // -> CONCAT(a, b)
IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))   // -> CONCAT(a, b)
IDENTITY(CONCAT(CON, CAT(a, b)))        // -> IDENTITY_IMPL(CONCAT(a, b)) -> CONCAT(a, b)
```

`CONCAT(CON, CAT(a, b))` : `CONCAT` 함수는 `##`을 사용하여 두 매개변수를 연결하기 때문에, `##` 규칙에 따라 매개변수를 펼치지 않고 직접 연결합니다. 따라서 처음에 `CONCAT(a, b)`로 펼쳐지고, `CONCAT`이 이미 펼쳐졌기 때문에 재귀적으로 더 이상 펼치지 않고 중지합니다.

`IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))`: `IDENTITY_IMPL` can be understood as evaluating the parameter `arg0`, where the parameter `arg0` evaluates to `CONCAT(a, b)`, and because of recursive marking it as non-reentrant, `IDENTITY_IMPL` completes its expansion. When conducting the second scan, it encounters the non-reentrant `CONCAT(a, b)`, and stops expanding. Here, `CONCAT(a, b)` is derived from the expansion of the parameter `arg0`, and in subsequent expansions, it will also maintain the non-reentrant marking. This can be understood as the parent node being the parameter `arg0`, consistently holding the non-reentrant mark.

`IDENTITY(CONCAT(CON, CAT(a, b)))` : 이 예시는 부모-자식 노드들을 이해하기 위해 강조된 것입니다. 매개변수가 펼쳐진다면, 스스로가 부모 노드로 작용하여 펼쳐진 내용을 자식 노드로 판단하여 재귀적으로 처리됩니다. 매크로 정의 후에 전달된 펼쳐진 매개변수는 재진입이 금지된 표시가 계속 유지될 것입니다 (펼쳐진 매크로의 매개변수가 변경되지 않는 한). 매개변수의 펼침 과정을 하나의 별도 트리로 생각할 수 있으며, 펼쳐진 결과는 트리의 가장 하위 자식 노드입니다. 이 자식 노드는 매크로에 전달되어 실행되는 동안 여전히 재진입 금지 특성을 유지합니다.

예를 들어 여기서 처음으로 완전히 펼쳐진 후에 `IDENTITY_IMPL(CONCAT(a, b))`을 얻게 되는데, `CONCAT(a, b)`가 재진입이 금지된 것으로 표시되어 있습니다. 즉, `IDENTITY_IMPL`이 매개변수를 평가하는 함수라 할지라도, 매개변수가 펼쳐지지 못하도록 금지되었기 때문에 매개변수가 그대로 정의로 전달되어 최종적으로 우리는 `CONCAT(a, b)`를 얻게 됩니다.

저는 중요하다고 생각하는 몇 가지 규칙을 나열했거나 이해하기 어려운 규칙을 나열했을 뿐입니다. 더 자세한 규칙 설명은 표준 문서를 직접 참조하는 것이 좋습니다.

##Clang로 풀어지는 과정을 관찰합니다.

Clang 소스 코드에 몇 가지 인쇄 정보를 추가하여 매크로 확장 과정을 관찰할 수 있습니다. 저는 Clang 소스 코드를 깊이 이해하고자 하는 의도가 아닙니다. 여기 수정된 파일 diff가 있습니다. 관심 있는 분들은 직접 Clang을 컴파일하여 연구할 수 있습니다. 여기에서 사용한 llvm 버전은 11.1.0 입니다. [링크](https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-11.1.0.tar.gz)수정된 파일 ([링크](assets/img/2021-3-31-cpp-preprocess/clang-modify.zip)다음은 우리가 이전에 소개한 매크로 펼침 규칙을 검증하기 위해 간단한 예제를 통해 설명하겠습니다:

####예시1

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(C, ONCAT(a, b))      // CONCAT(a, b)
```

위 코드를 전처리하기 위해 수정된 Clang을 사용하면 `clang -P -E a.cpp -o a.cpp.i`와 같이 입력하면 아래와 같은 내용이 출력됩니다:

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

제 [1](#__codelineno-9-1)(#__codelineno-9-2)매크로를 확장할 수 있기 때문에 `Macro is ok to expand`를 정의대로 펼칠 수 있고, 이후 매크로 `EnterMacro`로 들어갈 수 있습니다.

(#__codelineno-9-9)텍스트를 한국어로 번역하십시오:

`Token` 하나씩 펼쳐 나가기 위해 매크로가 정의된 후에 진행됩니다. (`Token`은 `Clang` 전처리 과정에서의 개념으로, 여기서 자세히 설명하지는 않겠습니다.)

(#__codelineno-9-11)정함）.

첫 번째 `Token`은 `hashhash`이며 `##` 연산자입니다. 결과에 계속 복사합니다 (제 [14-15](#__codelineno-9-14)텍스트를 한국어로 번역해주세요:

行）。

(#__codelineno-9-16)대로).

최종으로 `Leave ExpandFunctionArguments`는 이번 스캔으로 얻은 결과를 출력합니다 (제 [19](#__codelineno-9-19)결과적으로 'Token'을 모두 'C ## ONCAT(a, b)'로 번역하면되며, 그런 다음 전처리기가 '##' 연산자를 실행하여 새로운 내용을 생성합니다.

명령어를 실행한 후 `CONCAT(a, b)`가 얻어졌는데, 매크로 `CONCAT`을 만났을 때, 전처리 과정에서 먼저 `HandleIdentifier`에 진입하여 매크로 정보를 출력하였습니다. 해당 매크로의 상태가 `disable used`임을 확인하여 이미 확장된 상태이므로 다시 확장할 수 없다는 메시지인 `매크로를 확장할 수 없습니다`가 표시되었습니다. 전처리기는 더 이상 확장하지 않고, 최종 결과는 `CONCAT(a, b)`가 되었습니다.

####예시 2

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define IDENTITY(arg0) arg0

IDENTITY(CONCAT(C, ONCAT(a, b)))
```

<details>
<요약> <글꼴> Clang 프린팅 정보(클릭하여 펼치기)：</글꼴> </요약>
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

(#__codelineno-11-12)`IDENTITY`를 펼치기 시작했을 때, 매개변수 `Token 0`이 `CONCAT(...)`임을 발견하였습니다. 따라서 먼저 해당 매개변수를 평가합니다.

제 [27](#__codelineno-11-27)(#__codelineno-11-46)行）.

(#__codelineno-11-47)`IDENTITY`에 대한 전개를 종료하고 얻은 결과는 `CONCAT(a, b)`입니다.

제 [51](#__codelineno-11-51)'`CONCAT(a, b)`'를 다시 스캔하면, 매크로이지만 이전 매개변수 확장 중 `used`로 설정되었으므로 더 이상 재귀적으로 확장되지 않고 최종 결과로 처리됩니다.

####예시 3

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

제 [16](#__codelineno-13-16)‘IDENTITY’를 펼치기 시작하고, 전처리기는 'Token 2' (즉, 'arg0')가 매크로라는 것을 인지하여 'CONCAT(C, ONCAT(a, b))'를 먼저 펼칩니다.

`arg0`을 펼치면 `CONCAT(a, b)`를 얻습니다 (23-54](#__codelineno-13-23)행동단위입니다.

`IDENTITY` 最終으로 `IDENTITY_IMPL(CONCAT(a, b))`으로 펼쳐진다.（제 [57](#__codelineno-13-57)텍스트를 한국어로 번역합니다:

行）

(#__codelineno-13-61)이 문구를 한국어로 번역해주세요:

 行），发现此时的 `Token 0` 是宏 `CONCAT(a, b)`，但处于 `used` 状态，中止展开并返回（第 75-84行），最终得到的结果还是 `CONCAT(a, b)`（第 [85](#__codelineno-13-85)영업중입니다).

재검색 결과를 확인하더니 매크로 `CONCAT(a, b)`의 상태가 `used`였다. 전개를 중단하고 최종 결과를 얻었다.

상기 세 가지 간단한 예시를 통해, 우리는 전처리기가 매크로를 풀어내는 과정을 대략적으로 이해할 수 있습니다. 여기서 더 깊이 들어가지 않겠습니다. 관심이 있으면 제가 제공한 수정 파일을 참고해 연구해보세요.

##대규모 프로그래밍 구현

아래에서는 주제에 진입합니다. (앞 부분은 매크로 펼침 규칙을 더 잘 이해하기 위한 것이었습니다.) 매크로 프로그래밍 구현부로 넘어갑니다.

####기본 기호

먼저 매크로의 특수 기호를 정의할 수 있습니다. 평가 및 결합할 때 사용됩니다.

``` cpp
#define PP_LPAREN() (
#define PP_RPAREN() )
#define PP_COMMA() ,
#define PP_EMPTY()
#PP_HASHHASH를 # ## #로 정의합니다. // 문자열 ##을 나타내지만 ## 연산자로 처리되지는 않습니다.
```

####값 신청

매개변수 우선 전개 규칙을 활용하여 평가 매크로를 작성할 수 있습니다:

``` cpp
#define PP_IDENTITY(arg0) arg0

PP_COMMA PP_LPAREN() PP_RPAREN()                // -> PP_COMMA ( )
PP_IDENTITY(PP_COMMA PP_LPAREN() PP_RPAREN())   // -> PP_COMMA() -> ,
```

만약 'PP_COMMA PP_LPAREN() PP_RPAREN()'만 작성한다면, 전처리기는 각 매크로를 별도로 처리하고 펼쳐진 결과를 다시 병합 처리하지 않습니다. 'PP_IDENTITY'를 추가하면 전처리기는 펼쳐진 'PP_COMMA()'에 대해 평가를 계속 진행하여 ','을 얻을 수 있습니다.


####결합

`##`을 결합할 때는 양쪽 매개변수를 확장하지 않습니다. 매개변수를 먼저 계산한 후에 결합하려면 다음과 같이 작성할 수 있습니다:

``` cpp
#define PP_CONCAT(arg0, arg1) PP_CONCAT_IMPL(arg0, arg1)
#define PP_CONCAT_IMPL(arg0, arg1) arg0 ## arg1

PP_CONCAT(PP_IDENTITY(1), PP_IDENTITY(2))         // -> 12
PP_CONCAT_IMPL(PP_IDENTITY(1), PP_IDENTITY(2))    // -> PP_IDENTITY(1)PP_IDENTITY(2) -> Error.
```

여기서 `PP_CONCAT`으로 사용되는 방법은 지연 연결이라고 불립니다. `PP_CONCAT_IMPL`로 확장될 때, `arg0`과 `arg1`은 모두 먼저 확장되어 값이 계산된 후에 `PP_CONCAT_IMPL`에 의해 실제 연결 작업이 수행됩니다.

####논리 연산

`PP_CONCAT`를 사용하면 논리 연산을 수행할 수 있습니다. 먼저 `BOOL` 값을 정의합니다:


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

`PP_CONCAT`을 사용하여 `PP_BOOL_`와 `arg0`을 결합한 다음, 결합된 결과를 평가합니다. 여기서 `arg0`은 `[0, 256]` 범위의 숫자로평가되어야 합니다. `PP_BOOL_` 뒤에 결합하고 평가하면 부울 값이 얻어집니다. AND, OR, NOT 연산:

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

`PP_BOOL`로 매개변수를 평가한 후, `0 1` 조합에 따라 논리 연산 결과를 조합합니다. `PP_BOOL`를 사용하지 않으면 매개변수는 `0 1` 두 가지 값만 지원하게 되어 적용 범위가 크게 줄어듭니다. 마찬가지로 XOR, NOT 등의 작업도 작성할 수 있으니 관심이 있다면 직접 시도해보세요.

####조건 선택

`PP_BOOL`와 `PP_CONCAT`를 활용하여 조건 선택문을 작성할 수도 있습니다:

``` cpp
#define PP_IF(if, then, else) PP_CONCAT(PP_IF_, PP_BOOL(if))(then, else)
#define PP_IF_1(then, else) then
#define PP_IF_0(then, else) else

PP_IF(1, 2, 3)      // -> PP_IF_1(2, 3) -> 2
PP_IF(0, 2, 3)      // -> PP_IF_0(2, 3) -> 3
```

`if` 求值如果是 `1`，用 `PP_CONCAT` 拼接成 `PP_IF_1`，最后展开为 `then` 的值；同理若 `if` 求值为 `0`，得到 `PP_IF_0`。

####증가 감소

정수 증가 감소:

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

`PP_BOOL`와 비슷하게, 정수의 증가와 감소에도 범위 제한이 있습니다. 여기서 범위가 `[0, 256]`으로 설정되었습니다. `256`까지 증가한 후에는 안전을 위해 `PP_INC_256`은 경계로써 자신의 `256`을 반환하며, 마찬가지로 `PP_DEC_0`은 `0`을 반환합니다.

####가변 길이 매개변수

"宏은 가변 길이 매개변수를 받을 수 있으며, 형식은 다음과 같습니다:"

```cpp
#define LOG(format, ...) printf("log: " format, __VA_ARGS__)

LOG("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG("Hello World")              // -> printf("log: " "Hello World", ); 多了个逗号，编译报错
```

변이는 비어 있을 수 있으므로 빈 경우에는 컴파일이 실패할 수 있습니다. 이에 C++ 20에서 `__VA_OPT__`를 도입했습니다. 변이가 비어 있는 경우에는 빈 값을 반환하고, 그렇지 않으면 원래 매개변수를 반환합니다:

```cpp
#define LOG2(format, ...) printf("log: " format __VA_OPT__(,) __VA_ARGS__)

LOG2("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG2("Hello World")              // -> printf("log: " "Hello World" ); 没有逗号，正常编译
```

그러나 유감스럽게도 이 매크로는 C++ 20 이상의 표준에서만 사용할 수 있습니다. 아래에서 `__VA_OPT__` 의 구현 방법을 제시할 것입니다.

####동사를 찾다.

해당 상황을 고려해 보십시오:

``` cpp
PP_IF(1, PP_COMMA(), PP_LPAREN())     // -> PP_IF_1(,,)) -> unterminated argument list invoking macro "PP_IF_1"에서 오류가 발생했습니다.
```

우리는, 매크로가 확장될 때 첫 번째 매개변수를 평가하게 됩니다. `PP_COMMA()`와 `PP_LPAREN()`이 먼저 평가되고 `PP_IF_1`로 전달되어 `PP_IF_1(,,))`이 되면서 전처리 오류가 발생합니다. 이때, 지연 평가 방법이라는 방법을 사용할 수 있습니다:

``` cpp
PP_IF(1, PP_COMMA, PP_LPAREN)()       // -> PP_IF_1(PP_COMMA, PP_LPAREN)() -> PP_COMMA() -> ,
```

이러한 방식으로 변경하여 매크로의 이름만 전달하고, `PP_IF`가 필요한 매크로 이름을 선택한 후 괄호 `()`와 결합하여 완전한 매크로를 형성한 다음 확장합니다. 게으른 평가는 매크로 프로그래밍에서도 매우 흔합니다.

####소괄호로 시작합니다.

변이 파라미터가 괄호로 시작되었는지 판별하십시오:

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

`PP_IS_BEGIN_PARENS`은(는) 전달된 매개변수가 괄호로 시작하는지를 판단하는 데 사용될 수 있으며, 괄호 매개변수를 처리해야 할 때 필요합니다(예: `__VA_OPT__` 구현에서 언급한 것처럼). 조금 복잡해 보이지만 본질은 매크로를 구축하는 것입니다. 만약 가변 길이 매개변수가 괄호로 시작한다면, 괄호와 결합하여 평가하여 한 가지 결과를 얻을 수 있고, 그렇지 않으면 다른 결과를 얻습니다. 천천히 알아보겠습니다:

`PP_IS_BEGIN_PARENS_PROCESS`와 `PP_IS_BEGIN_PARENS_PROCESS_0`로 구성된 매크로 기능은 먼저 전달된 가변 매개변수를 계산한 다음 0번 매개변수를 취합니다.

`PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__)` 은 먼저 `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__`을 평가한 후에 이 평가 결과를 `PP_IS_BEGIN_PARENS_PRE_`와 결합합니다.

`PP_IS_BEGIN_PARENS_EAT(...)` 매크로는 모든 인수를 흡수하여 1을 반환합니다. 이전 단계에서 `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__`에서 `__VA_ARGS__`가 괄호로 시작하는 경우, `PP_IS_BEGIN_PARENS_EAT(...)`의 평가에 일치하고 1을 반환합니다. 반대로, 괄호로 시작하지 않으면 일치하지 않고 `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__`는 그대로 유지됩니다.

만약 `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__`를 평가하면 `1`이 나온다. `PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, 1) -> PP_IS_BEGIN_PARENS_PRE_1 -> 1`이다. 주의할 점은 `1` 뒤에 쉼표가 있다는 것이다. 따라서 `1, `을 `PP_IS_BEGIN_PARENS_PROCESS_0`으로 전달하고, 첫 번째 인자를 취하여 최종적으로 `1`을 얻을 수 있으며 이로써 매개변수가 괄호로 시작됨을 나타낸다.

만약 `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__`가 1이 아니라 원래 값을 유지한다면, `PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__) -> PP_IS_BEGIN_PARENS_PRE_PP_IS_BEGIN_PARENS_EAT __VA_ARGS__ -> 0, __VA_ARGS__`를 거쳐 `PP_IS_BEGIN_PARENS_PROCESS_0`로 전달되며 결과는 0이며, 이는 매개변수가 괄호로 시작되지 않음을 나타낸다.

####가변 길이 매개변수 없음

가변 인수가 비어 있는지 확인하는 것은 일반적인 매크로입니다. `__VA_OPT__`를 구현할 때 필요합니다. 여기서 `PP_IS_BEGIN_PARENS`를 활용하여 미완성 버전을 먼저 작성할 수 있습니다:

``` cpp
#define PP_IS_EMPTY_PROCESS(...) \
    PP_IS_BEGIN_PARENS(PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ())
#define PP_IS_EMPTY_PROCESS_EAT(...) ()

PP_IS_EMPTY_PROCESS()       // -> 1
PP_IS_EMPTY_PROCESS(1)      // -> 0
PP_IS_EMPTY_PROCESS(1, 2)   // -> 0
PP_IS_EMPTY_PROCESS(())     // -> 1
```

"PP_IS_EMPTY_PROCESS" 기능은 "PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__()"이 괄호로 시작하는지를 판단합니다.

만약 `__VA_ARGS__`이 비어 있다면, `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__() -> PP_IS_EMPTY_PROCESS_EAT() -> ()`와 같은 괄호 쌍 `()`이 나오며, 이를 `PP_IS_BEGIN_PARENS`에 전달하여 `1`을 반환하게 됩니다. 이는 인수가 비어있음을 나타냅니다.

그렇지 않은 경우, `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__()`은 그대로 `PP_IS_BEGIN_PARENS`로 전달되고, 비어 있지 않음을 나타내는 0을 반환합니다.

第 4 예시 `PP_IS_EMPTY_PROCESS(()) -> 1`에 주목하십시오. `PP_IS_EMPTY_PROCESS`는 괄호로 시작하는 가변 매개변수를 올바르게 처리할 수 없습니다. 이 경우에는 매개변수 앞에 오는 괄호 때문에 `PP_IS_EMPTY_PROCESS_EAT`와 매치되어 `()`로 해석됩니다. 이 문제를 해결하기 위해 괄호로 시작하는지 여부에 따라 매개변수를 구분하여 처리해야합니다:

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

`PP_IS_EMPTY_IF`은 0번째 또는 1번째 매개변수를 반환하는 `if` 조건에 따라 결정됩니다.

만약 입력된 가변 길이 인수가 괄호로 시작한다면, `PP_IS_EMPTY_IF`는 `PP_IS_EMPTY_ZERO`를 반환하고, 최종적으로 `0`을 반환하여 가변 길이 인수가 비어 있지 않음을 나타냅니다.

`PP_IS_EMPTY_IF` 가 `PP_IS_EMPTY_PROCESS`를 반환하는 경우, 최종적으로 `PP_IS_EMPTY_PROCESS`가 가변 인수가 비어 있는지를 판단합니다.

####하위 스크립트 액세스

변동 길이 매개변수가 지정한 위치의 요소를 가져옵니다:

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

`PP_ARGS_ELEM`의 첫 번째 매개변수는 요소의 인덱스 `I`이며, 그 뒤에 가변 매개변수가 옵니다. `PP_CONCAT`을 활용하여 `PP_ARGS_ELEM_`과 `I`를 결합하면, 해당 위치 요소를 반환하는 매크로인 `PP_ARGS_ELEM_0..8`을 얻을 수 있습니다. 그 후 가변 매개변수를 이 매크로에 전달하여, 해당 인덱스 위치의 요소를 펼칠 수 있습니다.

#### PP_IS_EMPTY2

`PP_ARGS_ELEM`을 활용하면 `PP_IS_EMPTY`의 다른 버전을 구현할 수도 있습니다:

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

`PP_ARGS_ELEM`을 빌려와서 매개변수에 쉼표가 있는지 확인하는 `PP_HAS_COMMA`를 구현합니다. `PP_COMMA_ARGS`는 전달된 임의의 매개변수를 흡수하고 쉼표를 반환합니다.

변동 매개 변수가 비어 있는지 확인하는 기본 논리는 `PP_COMMA_ARGS __VA_ARGS__() `가 쉼표를 반환하는지를 확인하는 것이며, 즉 `__VA_ARGS__`가 비어 있을 때 `PP_COMMA_ARGS`와 `()`가 합쳐져 평가되는 것입니다. 구체적인 표현은 `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__())`입니다.

그러나 예외적인 상황이 발생할 수 있습니다:

`__VA_ARGS__`은 자체적으로 쉼표를 포함할 수 있습니다.
`__VA_ARGS__ ()`는 쉼표가 발생하는 평가를 함께 연결합니다.
`PP_COMMA_ARGS __VA_ARGS__` 합쳐져 평가되면 쉼표가 생깁니다;

상기 언급된 세 가지 예외 상황에 대해 제외 처리가 필요하므로, 최종적인 작성 방식은 다음 4가지 조건에 대해 논리 AND를 수행한 것과 동등하게 됩니다:

* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__))` &&
* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__()))` &&
* `PP_NOT(PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__))` &&
* `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ())`

#### `__VA_OPT__`

`PP_IS_EMPTY`을 활용하여 `__VA_OPT__`와 유사한 매크로를 구현할 수 있습니다.

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

`PP_ARGS_OPT`은 두 개의 고정 매개변수와 가변 매개변수를 허용하며, 가변 매개변수가 비어 있지 않으면 `data`를 반환하고, 그렇지 않으면 `empty`를 반환합니다. `data`와 `empty`가 쉼표를 지원하도록 하기 위해 두 값 모두 실제 매개변수를 괄호로 묶어야 하며, 최종적으로 `PP_REMOVE_PARENS`를 사용하여 외부 괄호를 제거해야 합니다.

`PP_ARGS_OPT` 와 함께 `LOG3`를 구현하여 `LOG2`와 동일한 기능을 모방할 수 있습니다.

``` cpp
#define LOG3(format, ...) \
    printf("log: " format PP_ARGS_OPT((,), (), __VA_ARGS__) __VA_ARGS__)

LOG3("Hello");                  // -> printf("log: " "Hello" );
LOG3("Hello %s", "World");      // -> printf("log: " "Hello %s" , "World");
```

`data_tuple`은 `(,)`이며, 가변 길이 인수가 비어 있지 않으면 `data_tuple` 안에 모든 요소를 반환하며, 여기서는 쉼표 `,`입니다.

####파라미터 개수 요청

가변 길이 인수의 수를 가져옵니다:

``` cpp
#define PP_ARGS_SIZE_IMCOMPLETE(...) \
    PP_ARGS_ELEM(8, __VA_ARGS__, 8, 7, 6, 5, 4, 3, 2, 1, 0)

PP_ARGS_SIZE_IMCOMPLETE(a)             // -> 1
PP_ARGS_SIZE_IMCOMPLETE(a, b)          // -> 2
PP_ARGS_SIZE_IMCOMPLETE(PP_COMMA())    // -> 2
PP_ARGS_SIZE_IMCOMPLETE()              // -> 1
```

변이 가능한 매개변수의 수를 계산하려면 매개변수의 위치를 통해 확인합니다. `__VA_ARGS__`는 뒤이어 오는 모든 매개변수를 오른쪽으로 이동시키므로, 매크로 `PP_ARGS_ELEM`을 사용하여 8번째 위치의 매개변수를 얻을 수 있습니다. 만약 `__VA_ARGS__`에 매개변수가 하나만 있는 경우, 8번째 매개변수는 `1`이 됩니다. 마찬가지로, `__VA_ARGS__`에 두 개의 매개변수가 있는 경우, 8번째 매개변수는 `2`가 되며, 이는 정확히 변이 가능한 매개변수의 수와 일치합니다.

여기 제공된 예시는 최대 8개의 가변 인수를 지원하며, 이는 `PP_ARGS_ELEM`이 지원할 수 있는 최대 길이에 의존합니다.

그러나 이 매크로는 완전하지 않습니다. 가변 매개변수가 비어있는 경우, 이 매크로는 잘못된 결과인 `1`을 반환합니다. 빈 가변 매개변수를 처리해야 한다면, 앞서 언급한 `PP_ARGS_OPT` 매크로를 사용해야 합니다:

``` cpp
#define PP_COMMA_IF_ARGS(...) PP_ARGS_OPT((,), (), __VA_ARGS__)
#define PP_ARGS_SIZE(...) PP_ARGS_ELEM(8, __VA_ARGS__ PP_COMMA_IF_ARGS(__VA_ARGS__) 8, 7, 6, 5, 4, 3, 2, 1, 0, 0, 0)

PP_ARGS_SIZE(a)             // -> 1
PP_ARGS_SIZE(a, b)          // -> 2
PP_ARGS_SIZE(PP_COMMA())    // -> 2
PP_ARGS_SIZE()              // -> 0
PP_ARGS_SIZE(,,,)           // -> 4
```

주요 문제는 쉼표 `,`인데, `__VA_ARGS__`가 비어 있을 때 쉼표를 숨기면 `0`을 올바르게 반환할 수 있습니다.

####방문 순회

C++의 'for_each'와 유사한 것으로, 매크로인 'PP_FOR_EACH'를 구현할 수 있습니다.

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

`PP_FOR_EACH`은 두 개의 고정 매개변수를 받습니다: `macro`는 반복할 때 호출되는 매크로로 이해할 수 있고, `context`는 `macro`에 전달되는 고정값 매개변수로 사용됩니다. `PP_FOR_EACH`는 먼저 가변 매개변수의 길이 `N`을 얻기 위해 `PP_ARGS_SIZE`를 통해 길이를 가져온 후, `PP_CONCAT`을 사용하여 `PP_FOR_EACH_N`을 얻습니다. 그 다음 `PP_FOR_EACH_N`은 가변 매개변수의 개수와 동일한 반복 횟수를 구현하기 위해 `PP_FOR_EACH_N-1`을 순환적으로 호출합니다.

예시에서는 'DECLARE_EACH'를 매크로의 매개변수로 선언했습니다. 'DECLARE_EACH'의 역할은 'contex arg'를 반환하는 것입니다. 여기서 'contex'는 형식 이름이고, 'arg'는 변수 이름이라면, 'DECLARE_EACH'는 변수를 선언하는 데 사용될 수 있습니다.

####조건 반복

`FOR_EACH`가 있으면 `PP_WHILE`을 비슷한 방식으로 작성할 수도 있습니다.

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

`PP_WHILE`은 `pred` 조건 판단 함수, `op` 작업 함수, `val` 초기 값을 세 개의 매개변수로 받습니다. 루프 동안 계속해서 `pred(val)`를 사용하여 루프를 종료하며, `op(val)`로부터 얻은 값을 후속 매크로에 전달하여 아래 코드를 실행하는 것으로 이해할 수 있습니다:

``` cpp
while (pred(val)) {
    val = op(val);
}
```

`PP_WHILE_N` 처음으로 `pred(val)`를 사용하여 조건 평가 결과를 얻고, 조건 결과인 `cond`와 나머지 매개변수를 `PP_WHILE_N_IMPL`에 전달합니다.
`PP_WHILE_N_IMPL` 은 두 부분으로 이해할 수 있습니다: 뒷부분인 `(pred, op, PP_IF(cond, op, PP_EMPTY_EAT)(val))`은 앞부분의 매개변수로 사용되며, `PP_IF(cond, op, PP_EMPTY_EAT)(val)`는 만약 `cond`가 참이라면 `op(val)`을 평가하고, 그렇지 않으면 `PP_EMPTY_EAT(val)`을 평가하여 빈 값을 반환합니다. 앞부분은 `PP_IF(cond, PP_WHILE_N+1, val PP_EMPTY_EAT)`로, `cond`가 참이면 `PP_WHILE_N+1`을 반환하여 뒷부분의 매개변수와 결합하여 계속해서 반복을 수행합니다. 그렇지 않으면 `val PP_EMPTY_EAT`를 반환하며, 이때 `val`은 최종 계산 결과가 되고, `PP_EMPTY_EAT`은 뒷부분 결과를 무시합니다.

`SUM`은 `N + N-1 + ... + 1`을 구현합니다. 초기값은 `(max_num, origin_num)`입니다. `SUM_PRED`는 값이 첫 번째 요소인 `x`를 취하고 0보다 큰지 여부를 판단합니다. `SUM_OP`는 `x`에 대해 감소 연산 `x = x - 1`을 수행하고 `y`에 대해 `+ x` 작업 `y = y + x`을 수행합니다. 이를 직접 `SUM_PRED`와 `SUM_OP`에 전달하여 `PP_WHILE`로 결과를 반환하는데, 반환된 결과는 튜플이며 우리가 실제로 원하는 결과는 튜플의 두 번째 요소입니다. 따라서 `SUM`을 사용하여 두 번째 요소의 값을 취합니다.

####재귀 호출

지금까지 우리의 반복 접근과 조건 순환은 잘 작동되어 예상대로 결과를 내었습니다. 마크로 확장 규칙을 설명할 때 우리가 언급한 재귀적으로 다시 들어가는 것을 금지한다는 것을 기억하시나요? 불행하게도 이중 루프를 실행하려고 시도할 때 재귀적으로 다시 들어가는 상황이 발생하였습니다.

``` cpp
#define SUM_OP2(xy_tuple) SUM_OP_OP_IMPL2 xy_tuple
#define SUM_OP_OP_IMPL2(x, y) (PP_DEC(x), y + SUM(x, 0))

#define SUM2(max_num, origin_num) \
    PP_IDENTITY(SUM_IMPL PP_WHILE(SUM_PRED, SUM_OP2, (max_num, origin_num)))

SUM2(1, a)      // -> a + SUM_IMPL PP_WHILE_1(SUM_PRED, SUM_OP, (1, a))
```

`SUM2`를 `op` 매개변수에서 `SUM_OP2`로 변경하고, `SUM_OP2`에서는 `SUM`을 호출하며, `SUM`을 풀면 `PP_WHILE_1`이 될 것이고, 마치 `PP_WHILE_1`이 자기 자신을 재귀적으로 호출하는 것처럼 전처리기가 펼치는 것을 멈출 것이다.

이 문제를 해결하기 위해, 자동 재귀를 사용하는 방법을 채택할 수 있습니다 (Automatic Recursion):

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

`PP_AUTO_WHILE` 는 `PP_WHILE`의 자동 추론 재귀 버전으로, 핵심 매크로는 `PP_AUTO_REC(PP_WHILE_PRED)` 입니다. 이 매크로는 현재 사용 가능한 `PP_WHILE_N` 버전의 숫자 `N`을 찾을 수 있습니다.

추론의 원리는 매우 간단합니다. 모든 버전을 검색하여 올바르게 펼쳐진 버전을 찾아 해당 버전의 숫자를 반환합니다. 검색 속도를 향상시키기 위해 일반적으로 이진 탐색을 사용하는데, 이것이 `PP_AUTO_REC`이 하는 일입니다. `PP_AUTO_REC`은 `check`라는 매개변수를 받는데, 이것은 버전의 가용성을 검사합니다. 여기서 지원되는 버전 범위는 `[1, 4]`입니다. `PP_AUTO_REC`은 먼저 `check(2)`를 확인한 후, 만약 참이면 `PP_AUTO_REC_12`를 호출하여 `[1, 2]` 범위를 탐색하고, 그렇지 않으면 `PP_AUTO_REC_34`로 `[3, 4]`를 탐색합니다. `PP_AUTO_REC_12`은 `check(1)`을 확인하며, 참이면 버전 `1`을 사용하고, 그렇지 않으면 버전 `2`를 사용합니다. `PP_AUTO_REC_34`도 동일한 방식으로 동작합니다.

`check`를 작성하는 방법은 어떻게 해야 버전을 확인할 수 있는지 알 수 있을까? 여기서 `PP_WHILE_PRED`는 두 부분이 결합된 형태로 펼쳐질 것이다. 뒷부분인 `PP_WHILE_ ## n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`을 살펴보자. 만약 `PP_WHILE_ ## n`이 사용 가능하다면, `PP_WHILE_FALSE`가 항상 `0`을 반환하므로 이 부분은 `val` 매개변수의 값, 즉 `PP_WHILE_FALSE`로 펼쳐질 것이다. 그렇지 않다면 이 매크로 부분은 그대로 유지되어 계속해서 `PP_WHILE_n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`일 것이다.

후반의 결과를 전반 `PP_WHILE_CHECK_`과 결합하여 두 가지 결과를 얻습니다: `PP_WHILE_CHECK_PP_WHILE_FALSE` 또는 `PP_WHILE_CHECK_PP_WHILE_n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`로, 이에 따라 `PP_WHILE_CHECK_PP_WHILE_FALSE`은 `1`을 반환하여 사용 가능함을 나타내며, `PP_WHILE_CHECK_PP_WHILE_n`은 `0`을 반환하여 사용 불가능함을 나타냅니다. 이로써 우리는 재귀 기능을 자동으로 유추하는 작업을 완료했습니다.

####산술 비교

부등하지 않음:

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

동일한 값인지 판단하려면 재귀 호출을 금지하는 특성을 사용했습니다. `x`와 `y`를 재귀적으로 결합하여 `PP_NOT_EQUAL_x PP_NOT_EQUAL_y` 매크로를 생성합니다. 만약 `x == y`이면 `PP_NOT_EQUAL_y` 매크로가 펼쳐지지 않으며, `PP_NOT_EQUAL_CHECK_PP_NOT_EQUAL_y`로 결합되어 `0`을 반환합니다. 그 반대의 경우, 두 번 성공적으로 펼칠 때 최종적으로 `PP_EQUAL_NIL`을 얻어 `PP_NOT_EQUAL_CHECK_PP_EQUAL_NIL`로 결합되어 `1`을 반환합니다.

동등 함:

``` cpp
#define PP_EQUAL(x, y) PP_NOT(PP_NOT_EQUAL(x, y))

PP_EQUAL(1, 1)              // -> 1
PP_EQUAL(1, 3)              // -> 0

```

이하:

``` cpp
#define PP_LESS_EQUAL(x, y) PP_NOT(PP_SUB(x, y))

PP_LESS_EQUAL(2, 1)         // -> 0
PP_LESS_EQUAL(1, 1)         // -> 1
PP_LESS_EQUAL(1, 2)         // -> 1
```

작은 경우:

``` cpp
#define PP_LESS(x, y) PP_AND(PP_LESS_EQUAL(x, y), PP_NOT_EQUAL(x, y))

PP_LESS(2, 1)               // -> 0
PP_LESS(1, 2)               // -> 1
PP_LESS(2, 2)               // -> 0
```

또한, 더 크거나, 크거나 같다는 등 산술 비교도 있지만, 이에 대해서는 더 이상 설명하지 않겠습니다.

####산술 연산

`PP_AUTO_WHILE`를 활용하면 기본 산술 연산을 수행할 수 있으며 중첩된 연산도 지원됩니다.

덧셈:

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

빼기:

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

곱셈:

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

곱셈 구현에는 `ret`이라는 매개변수가 추가되었습니다. 초기값은 `0`이며 각 반복마다 `ret = ret + x`가 실행됩니다.

나눗셈:

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

나눗셈은 `PP_LESS_EQUAL`을 사용하며, `y <= x`인 경우에만 루프가 계속됩니다.

####자료 구조

대한민국에서 번역합니다:

쥰도 데이터 구조를 갖고 있어. 실은 이전에 살짝 데이터 구조인 'tuple'을 사용했었다고.
'PP_REMOVE_PARENS'는 'tuple'의 바깥 괄호를 제거하고 안의 요소를 반환할 수 있는 거야. 여기서는 'tuple'을 예로 들어 관련 구현을 논의할 거야. 다른 데이터 구조로 'list, array' 등이 관심 있는 사람은 'Boost'의 구현을 확인해보도록 해.

`tuple`은 괄호로 묶인 쉼표로 구분된 요소 집합을 말한다: `(a, b, c)`입니다.

``` cpp
#define PP_TUPLE_REMOVE_PARENS(tuple) PP_REMOVE_PARENS(tuple)

지정된 인덱스의 요소를 가져옵니다.
#define PP_TUPLE_ELEM(i, tuple) PP_ARGS_ELEM(i, PP_TUPLE_REMOVE_PARENS(tuple))

튜플 전체를 소멸하고 빈 값을 반환합니다.
#define PP_TUPLE_EAT() PP_EMPTY_EAT

크기 가져오기
#define PP_TUPLE_SIZE(tuple) PP_ARGS_SIZE(PP_TUPLE_REMOVE_PARENS(tuple))

// 요소 추가
#define PP_TUPLE_PUSH_BACK(elem, tuple) \
    PP_TUPLE_PUSH_BACK_IMPL(PP_TUPLE_SIZE(tuple), elem, tuple)
#define PP_TUPLE_PUSH_BACK_IMPL(size, elem, tuple) \
    (PP_TUPLE_REMOVE_PARENS(tuple) PP_IF(size, PP_COMMA, PP_EMPTY)() elem)

요청하신 텍스트를 한국어로 번역합니다:

// 요소 삽입
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

마지막 요소 삭제
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

요소 삭제
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

여기서 간단히 삽입 요소의 구현에 대해 설명하겠습니다. 다른 삭제 요소와 같은 작업도 유사한 원리로 구현됩니다. `PP_TUPLE_INSERT(i, elem, tuple)`은 `tuple`의 `i` 위치에 요소 `elem`을 삽입할 수 있습니다. 이 작업을 완료하기 위해 `i`보다 작은 위치에 있는 요소는 먼저 `PP_TUPLE_PUSH_BACK`을 사용하여 새 `tuple`인 `ret`에 넣은 다음 위치 `i`에 요소 `elem`을 넣고, 그런 다음 기존 `tuple`에서 위치 `i` 이상인 요소를 `ret` 뒤에 넣으면 최종적으로 `ret`이 우리가 원하는 결과를 제공합니다.

##요약

이 문서의 목적은 C/C++ 매크로 프로그래밍의 원리와 기본 구현을 명확히 설명하고, 내 이해와 인식을 기록하면서 다른 사람들에게 몇 가지 통찰과 영감을 주고 싶습니다. 이 문서는 조금 길지만 매크로 프로그래밍에 관련된 몇 가지 기술과 사용법이 누락된 부분이 있으니 주의해야 합니다. 예를 들어 CHAOS_PP가 제안한 [지연 전개를 이용한 재귀 호출 방법](https://github.com/pfultz2/Cloak/wiki/C-Preprocessor-tricks,-tips,-and-idioms#deferred-expression)BOOST_PP 내부의 `REPEAT` 관련 매크로 등에 대해 관심이 있는 경우 자료를 직접 참고하시기 바랍니다.

대규모 프로그래밍의 디버깅은 고통스러운 과정이지만, 우리는 다음과 같은 것들을 할 수 있습니다:

`-P -E` 옵션을 사용하여 전처리 결과를 출력하십시오.
이전에 소개한 내가 직접 수정한 'clang' 버전을 심층적으로 연구하여 전개과정을 조사했다.
복잡한 매크로를 해체하여 중간 매크로의 전개 결과를 확인하십시오.
관련 없는 헤더 파일과 매크로를 필터링하세요.
최종적으로는 매크로의 확장 과정을 상상해야 합니다. 매크로 확장에 익숙해지면 디버깅의 효율도 향상될 것입니다.

본문에서 사용된 매크로는 원리를 이해한 후 직접 다시 구현한 것입니다. 일부 매크로는 `Boost`의 구현 및 인용문을 참고했습니다. 어떤 오류가 있다면 언제든지 지적해 주시고 관련 문제에 대해 토론하고 싶다면 언제든지 저에게 연락해 주세요.

이 텍스트의 코드 전체는 여기에 있습니다: [다운로드](assets/img/2021-3-31-cpp-preprocess/macros.cpp)，[온라인 데모](https://godbolt.org/z/coWvc5Pse)We have received your request. Thank you.

##인용

* [Boost.Preprocessor](https://www.boost.org/doc/libs/1_75_0/libs/preprocessor/doc/)
(https://bot-man-jl.github.io/articles/?post=2020/Macro-Programming-Art)

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT를 사용하여 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)어떤 누락된 부분도 지적하세요. 
