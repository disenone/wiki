---
layout: post
title: Análisis de programación macro en C/C++
categories:
- c++
catalog: true
tags:
- dev
description: El propósito de este texto es explicar las reglas y métodos de implementación
  de la programación de macros en C/C++, para que ya no tengas miedo de ver macros
  en el código.
figures: []
---

<meta property="og:title" content="C/C++ 宏编程解析" />

El objetivo de este texto es explicar las reglas y métodos de implementación de la programación de macros en C/C++, para que ya no temas al encontrarte con macros en el código. En primer lugar, hablaré de las reglas de expansión de macros mencionadas en el estándar C++ 14. Luego, observaremos la expansión de macros mediante la modificación del código fuente de Clang. Por último, utilizando este conocimiento, hablaremos sobre la implementación de la programación de macros.

El código completo de este texto está aquí: [descargar](assets/img/2021-3-31-cpp-preprocess/macros.cpp), [Demo en línea](https://godbolt.org/z/coWvc5Pse).

##Introducción

Podemos utilizar el comando `gcc -P -E a.cpp -o a.cpp.i` para que el compilador procese el archivo `a.cpp` solo con la etapa de preprocesamiento y guarde el resultado en `a.cpp.i`.

Primero, echemos un vistazo a algunos ejemplos:

####**递归重入** (**Reentrancy**)

La **recursividad** es una propiedad importante en la programación, y se refiere al proceso mediante el cual una función se llama a sí misma durante su ejecución. Sin embargo, la **recursividad** puede volverse problemática cuando se trata de la **reentrancia**.

La **reentrancia** se produce cuando una función en un programa se llama a sí misma antes de que la llamada inicial haya terminado. Esto puede llevar a resultados inesperados o incluso a errores en el programa. 

Es importante tener en cuenta la **reentrancia** al diseñar y desarrollar software, para evitar posibles problemas y garantizar un funcionamiento adecuado. Esto implica tomar medidas para evitar conflictos de datos y asegurarse de que cada llamada recursiva se realice en su propio contexto.

En resumen, la **recursividad** es una característica valiosa, pero debemos tener cuidado con la **reentrancia** para garantizar un funcionamiento correcto y evitar posibles complicaciones.

``` cpp
#define ITER(arg0, arg1) ITER(arg1, arg0)

ITER(1, 2)          // -> ITER(2, 1)
```

La macro `ITER` intercambia la posición de `arg0` y `arg1`. Después de expandir la macro, se obtiene `ITER(2, 1)`.

Se puede observar que la posición de `arg0` y `arg1` se intercambian con éxito. Aquí, la macro se expande correctamente una vez, pero solo una vez, sin recursión adicional. En otras palabras, durante el proceso de expansión de la macro, no se permite la recursión para sí misma. Si se detecta que la misma macro se ha expandiado en una recursión anterior, no se expandirá nuevamente. Esta es una regla importante en la expansión de macros. La razón para prohibir la recursión es simple, se evita la recursión infinita.

####La concatenación de cadenas.

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                // -> HelloWorld
CONCAT(¡Hola, CONCAT(Mundo, !))     // -> ¡HolaCONCAT(Mundo, !)
```

La macro `CONCAT` tiene como objetivo concatenar `arg0` y `arg1`. Después de la expansión de la macro, `CONCAT(Hello, World)` producirá el resultado correcto `HelloWorld`. Sin embargo, `CONCAT(Hello, CONCAT(World, !))` solo expandirá la macro externa, la macro interna `CONCAT(World, !)` no se expandirá y se concatenará directamente con `Hello`, lo cual no es lo que esperamos. El resultado que queremos es `HelloWorld!`. Esta es otra regla importante en la expansión de macros: los argumentos de macros seguidos del operador `##` no se expandirán, sino que se concatenarán directamente con el contenido anterior.

A través de los dos ejemplos anteriores podemos notar que las reglas de expansión de macros pueden ser contraintuitivas en algunos casos. Si no se conocen claramente las reglas específicas, es posible que la macro resultante no sea consistente con el efecto deseado.

##**宏展开规则**

A través de los dos ejemplos del preámbulo, hemos comprendido que la expansión de macros tiene su propio conjunto de reglas estándar. Estas reglas están definidas en el estándar de C/C++, y aconsejo leerlas detenidamente varias veces. Además, adjunto el enlace de la versión n4296 del estándar [aquí](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4296.pdf)A continuación, selecciono algunas reglas importantes de la versión n4296, estas reglas determinarán cómo se debe escribir correctamente una macro (se recomienda tomar un tiempo para desplegar y leer detenidamente las macros en el estándar).

####Parámetros Separados

**宏的参数要求是用逗号分隔，而且参数的个数需要跟宏定义的个数一致，传递给宏的参数中，额外用括号包住的内容视为一个参数，参数允许为空：**

Los parámetros de la macro deben separarse por comas, y la cantidad de parámetros debe ser igual a la cantidad definida en la macro. Cualquier contenido adicional entre paréntesis se considera un parámetro independiente al pasarlos a la macro. Los parámetros pueden estar vacíos.

``` cpp
#define ADD_COMMA(arg1, arg2) arg1, arg2

ADD_COMMA(a, b)             // -> a, b
ADD_COMMA(a)                // Error "la macro "MACRO" requiere 2 argumentos pero solo se ha dado 1"
ADD_COMMA((a, b), c)        // -> (a, b), c
ADD_COMMA(, b)              // -> , b
```

`ADD_COMMA((a, b), c)` se considera que `(a, b)` es el primer parámetro. En `ADD_COMMA(, b)`, el primer parámetro está vacío, por lo que se expande a `, b`.

####**宏参数展开**

El proceso de expansión de los parámetros de una macro.

Al expandir una macro, si los parámetros de la macro también son macros expandibles, primero se expandirán completamente los parámetros y luego se expandirá la macro. Por ejemplo,

``` cpp
ADD_COMMA(ADD_COMMA(1, 2), ADD_COMMA(3, 4))     // -> 1, 2, 3, 4
```

En general, la expansión de macros puede considerarse como la evaluación de los parámetros seguida de la evaluación de la macro, a menos que se encuentre con los operadores `#` y `##`.

####El operador `#`

`#` La macro que sigue al operador no se expandirá, se convertirá directamente en una cadena de caracteres, por ejemplo:

``` cpp
#define STRINGIZE(arg0) # arg0

STRINGIZE(a)                // -> "a"
STRINGIZE(STRINGIZE(a))     // -> "STRINGIZE(a)"
```

根据这个规则 `STRINGIZE(STRINGIZE(a))` 只能展开为 `"STRINGIZE(a)"`。

###### Operador

`##` El parámetro de la macro antes y después del operador no se expandirá, se concatenará directamente, por ejemplo:

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                        // -> HelloWorld
CONCAT(Hello, CONCAT(World, !))             // -> HelloCONCAT(World, !)
CONCAT(CONCAT(Hello, World) C, ONCAT(!))    // -> CONCAT(Hello, World) CONCAT(!)
```

`CONCAT(CONCAT(Hello, World) C, ONCAT(!))` solo se puede concatenar primero para obtener `CONCAT(Hello, World) CONCAT(!)`.

####**重复扫描**

Repetición de exploración

Una vez que el preprocesador ha completado una expansión macro, volverá a escanear el contenido obtenido y continuará expandiéndolo hasta que no quede nada más por expandirse.

La expansión macro de una vez puede entenderse como la expansión completa de los parámetros (a menos que se encuentren con `#` y `##`), luego, de acuerdo con la definición de la macro, reemplaza la macro y los parámetros completamente expandidos según la definición, y luego maneja todos los operadores `#` y `##` en la definición.

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define STRINGIZE(arg0) # arg0

CONCAT(STRING, IZE(Hello))        // -> STRINGIZE(Hello) -> "Hello"
```

`CONCAT(STRING, IZE(Hello))` se expande por primera vez a `STRINGIZE(Hello)`, luego se realiza una segunda escaneo y se encuentra que `STRINGIZE` se puede expandir aún más, dando como resultado `"Hello"`.

####**禁止递归重入**

Prohibido el reingreso recursivo.

Durante el proceso de escaneo repetido, está prohibido expandir recursivamente las mismas macros. Puedes pensar en la expansión de las macros como una estructura en forma de árbol, donde el nodo raíz es la macro que se expandirá inicialmente, y cada contenido de la macro expandida se conecta como un nodo hijo en el árbol. Por lo tanto, prohibir la recursividad significa que al expandir una macro hija, si esa macro es igual a cualquier macro ancestro, se prohíbe la expansión. Veamos algunos ejemplos:

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define CONCAT_SPACE(arg0, arg1) arg0 arg1
#define IDENTITY(arg0) IDENTITY_IMPL(arg0)
#define IDENTITY_IMPL(arg0) arg0

CONCAT(CON, CAT(a, b))                  // -> CONCAT(a, b)
IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))   // -> CONCAT(a, b)
IDENTITY(CONCAT(CON, CAT(a, b)))        // -> IDENTITY_IMPL(CONCAT(a, b)) -> CONCAT(a, b)
```

`CONCAT(CON, CAT(a, b))`: Debido a que `CONCAT` une dos parámetros usando `##`, según las reglas de `##`, no se expandirán los parámetros y se unirán directamente. Por lo tanto, en la primera expansión se obtiene `CONCAT(a, b)`, ya que `CONCAT` ya se ha expandido, no se expandirá de forma recursiva y se detendrá.

`IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))`：`IDENTITY_IMPL` can be understood as evaluating the parameter `arg0`. Here, the parameter `arg0` is evaluated to `CONCAT(a, b)`. And because it is marked as non-reentrant due to recursion, `IDENTITY_IMPL` finishes expanding. During the second scan, it is found that `CONCAT(a, b)` is non-reentrant, so the expansion is stopped. Here, `CONCAT(a, b)` is expanded from the parameter `arg0`, and in subsequent expansions, the non-reentrant flag is also maintained. It can be understood as the parent node is the parameter `arg0`, always maintaining the non-reentrant flag.

`IDENTITY(CONCAT(CON, CAT(a, b)))`: Este ejemplo tiene como objetivo reforzar la comprensión de los nodos padre e hijo. Cuando se expande el parámetro, el propio parámetro actúa como nodo padre y el contenido expandido actúa como nodo hijo para evaluar la recursión. Después de que los parámetros se expanden y se pasan a la definición de la macro, la marca de no reentrancia sigue siendo preservada (si no se cambian los parámetros expandidos de la macro después de pasar a la definición de la misma). Podemos ver el proceso de expansión de los parámetros como otro árbol, donde el resultado de la expansión del parámetro es el hijo más profundo del árbol. Este hijo es pasado a la macro para realizar la expansión, y aún mantiene la característica de no reentrancia.

Por ejemplo, aquí, después de expandir completamente por primera vez `IDENTITY_IMPL(CONCAT(a, b))`, `CONCAT(a, b)` se marca como no reentrant, aunque `IDENTITY_IMPL` se evalúa en los argumentos, pero los argumentos están prohibidos de expandir, así que los argumentos se pasan sin cambios a la definición, y al final obtenemos `CONCAT(a, b)`.

**以上我只是列出了一些我认为比较重要的，或者觉得不太好理解的规则，详细的宏展开规则，还是建议花点时间直接去看标准文档。**

Arriba he enumerado algunas reglas que considero importantes o que pueden resultar difíciles de entender. Para conocer en detalle las reglas de expansión de macros, te recomendaría dedicar un poco de tiempo a leer directamente el documento estándar.

##Observing the expansion process through Clang.

Podemos añadir algunas impresiones de información al código fuente de Clang para observar el proceso de expansión de macros. No tengo la intención de explicar en profundidad el código fuente de Clang, aquí hay un archivo de modificación diferencial. Si estás interesado, puedes compilar Clang por ti mismo y estudiarlo. Aquí estoy usando la versión 11.1.0 de LLVM. ([Enlace](https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-11.1.0.tar.gz)），archivo modificado ([enlace](assets/img/2021-3-31-cpp-preprocess/clang-modify.zip)）。A continuación, vamos a validar las reglas de expansión de macros que presentamos anteriormente mediante algunos ejemplos:

####例子1

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(C, ONCAT(a, b))      // CONCAT(a, b)
```

Utilice Clang modificado para preprocesar el código anterior: `clang -P -E a.cpp -o a.cpp.i`, obtenga la siguiente información impresa:

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

Translate these text into Spanish language:

Página [1](#__codelineno-9-1)行 `HandleIdentifier` 遇到宏的时候会打印，接着打印宏的信息（第 [2-4](#__codelineno-9-2)\(`Macro` es válido para expandir\), después, vamos a entrar en la macro `EnterMacro`.

La función que realiza la expansión real de la macro es `ExpandFunctionArguments`, luego se imprime nuevamente la información de la macro a ser expandida, se observa que en este punto la macro ya ha sido marcada como `usada` (linea [9](#__codelineno-9-9)行）。之后根据宏的定义，进行逐个 `Token` 的展开 （`Token` 是 `Clang` 预处理里面的概念，这里不深入说明）。

El `Token` número 0 es el parámetro formal `arg0`, cuyo argumento real es `C`. No es necesario expandir la evaluación, por lo que se copia directamente al resultado (párrafo [11-13](#__codelineno-9-11)行）。

(not applicable)

El primer `Token` es `hashhash`, también conocido como el operador `##`, continúa copiándolo al resultado (del [14-15](#__codelineno-9-14)（Finalizar la traducción.

El segundo `Token` es el parámetro formal `arg1`, correspondiente al argumento real `ONCAT(a, b)`. El preprocesador también procesará el argumento real como una serie de `Token`, por lo que se puede observar que el resultado impreso envuelve cada `Token` del argumento real entre corchetes (línea 18). Debido a la presencia de `##`, este argumento real aún no necesita ser expandido, por lo que se copia directamente en el resultado (línea [16-18](#__codelineno-9-16)行）.

Al final, `Leave ExpandFunctionArguments` imprime los resultados obtenidos al expandir el escaneo esta vez (página [19](#__codelineno-9-19)Al traducir los `Token` resultantes, `C ## ONCAT(a, b)` sería la expresión generada por el operador `##` en el preprocesador.

Después de ejecutarlo, obtenemos `CONCAT(a, b)`. Cuando encontramos la macro `CONCAT`, el preprocesador entra primero en `HandleIdentifier`, se imprime la información de la macro y se descubre que el estado de la misma es `disable used`, es decir, ya ha sido expandida y se impide su reentrada. Se muestra el mensaje `Macro is not ok to expand` y el preprocesador no la expande más, por lo que el resultado final es `CONCAT(a, b)`.

####La traducción al español del texto sería: "Ejemplo 2"

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define IDENTITY(arg0) arg0

IDENTITY(CONCAT(C, ONCAT(a, b)))
```

<details>
<summary> <font> Clang Print Message (Click to Expand): </font> </summary>
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

Traduce este texto al idioma español:

第 [12](#__codelineno-11-12)行开始展开 `IDENTITY`，发现参数 `Token 0` 是 `CONCAT(...)`，也是一个宏，于是先对该参数进行求值。

La [27](#__codelineno-11-27)行开始展开参数宏 `CONCAT(...)`，跟例子 1 一样，多次扫描展开完成后得到 `CONCAT(a, b)` （第 [46] 

El código comienza a expandir la macro de parámetros `CONCAT (...)`, al igual que en el ejemplo 1, después de varias iteraciones de expansión, se obtiene `CONCAT(a, b)` (página [46](#__codelineno-11-46)行）。

第 [47](#__codelineno-11-47)Finaliza la expansión de `IDENTITY` y se obtiene el resultado `CONCAT(a, b)`.

**第 [51](#__codelineno-11-51)Vuelva a escanear `CONCAT(a, b)` en línea, y encontrará que, aunque sea un macro, ha sido establecido como `utilizado` durante el proceso de expansión de parámetros anteriores. Ya no se expandirá de forma recursiva, sino que se tomará como resultado final.

####**Ejemplo 3**

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

* Décimo [16](#__codelineno-13-16)行开始展开 `IDENTITY`，同理预处理器看到 `Token 2` （也即是 `arg0`）是宏，于是先展开 `CONCAT(C, ONCAT(a, b))`。

行开始展开 `IDENTITY`, y de manera similar el preprocesador ve que `Token 2` (es decir, `arg0`) es una macro, por lo tanto primero se expande `CONCAT(C, ONCAT(a, b))`.

* Al expandir `arg0` se obtiene `CONCAT(a, b)` (página [23-54](#__codelineno-13-23)（行）

* `IDENTITY` se expande finalmente como `IDENTITY_IMPL(CONCAT(a, b))` (página [57](#__codelineno-13-57)（行）

* Vuelve a escanear y continúa expandiendo `IDENTITY_IMPL` (secciones [61-72](#__codelineno-13-61)En el código, se observa que en este punto (`Token 0`) se encuentra la macro `CONCAT(a, b)`, pero está en un estado de "usada" (`used`). Por lo tanto, se detiene la expansión y se retorna (`return`) en las líneas 75-84. Como resultado, se obtiene `CONCAT(a, b)` nuevamente en la línea [85](#__codelineno-13-85)(Este contenido está en japonés y no puede ser traducido. El texto original se mantiene tal cual)

*Se volvió a escanear el resultado y se encontró que el estado de la macro `CONCAT(a, b)` es `usado`, por lo que se detiene la expansión y se obtiene el resultado final.*

A través de los tres ejemplos simples anteriores, podemos tener una idea general del proceso de expansión de macros por parte del preprocesador. Aquí no profundizaremos más en el tema del preprocesador, si estás interesado, puedes utilizar los archivos de modificación que proporciono para investigar por tu cuenta.

##La implementación de la programación macros

## Translate these text into Spanish language:

A continuación, pasamos a nuestro tema principal (la sección anterior tenía como objetivo comprender mejor las reglas de expansión de macros), la implementación de programación de macros.

####**基本符号**

**首先** podemos definir los **símbolos especiales** de la **macro**, los cuales serán utilizados para **evaluación** y **concatenación**.

``` cpp
#define PP_LPAREN() (
#define PP_RPAREN() )
#define PP_COMMA() ,
#define PP_EMPTY()
#define PP_HASHHASH # ## #      // Representa el string ##, pero solo como un string, no se interpretará como el operador ##

```

####求值 (evaluación)

Utilizando la regla de expansión de parámetros prioritarios, se puede escribir una macro de evaluación:

``` cpp
#define PP_IDENTITY(arg0) arg0

PP_COMMA PP_LPAREN() PP_RPAREN()                // -> PP_COMMA ( )
PP_IDENTITY(PP_COMMA PP_LPAREN() PP_RPAREN())   // -> PP_COMMA() -> ,
```

Si solo se escribe `PP_COMMA PP_LPAREN() PP_RPAREN()`, el preprocesador solo procesará cada macro por separado y no combinará el resultado expandido. Pero al agregar `PP_IDENTITY`, el preprocesador puede evaluar la expansión resultante de `PP_COMMA()` y obtener `,`.


####**拼接**

Debido a que al concatenar `##`, no se expanden los parámetros de ambos lados, para permitir que los parámetros se evalúen antes de la concatenación, se puede escribir de la siguiente manera:

``` cpp
#define PP_CONCAT(arg0, arg1) PP_CONCAT_IMPL(arg0, arg1)
#define PP_CONCAT_IMPL(arg0, arg1) arg0 ## arg1

PP_CONCAT(PP_IDENTITY(1), PP_IDENTITY(2))         // -> 12
PP_CONCAT_IMPL(PP_IDENTITY(1), PP_IDENTITY(2))    // -> PP_IDENTITY(1)PP_IDENTITY(2) -> 报错

PP_CONCAT_IMPL(PP_IDENTITY(1), PP_IDENTITY(2))    // -> PP_IDENTITY(1)PP_IDENTITY(2) -> Error 

(Note: The translation uses a neutral and colloquial tone to convey the meaning accurately)
```

Este método utilizado aquí, llamado `PP_CONCAT`, se llama concatenación diferida. Cuando se expande a `PP_CONCAT_IMPL`, tanto `arg0` como `arg1` se expandirán y evaluarán primero, y luego `PP_CONCAT_IMPL` realizará la operación de concatenación real.

####**逻辑运算**

La traducción al español de "逻辑运算" es "operaciones lógicas".

Con el uso de `PP_CONCAT` se puede realizar operaciones lógicas. Primero se define un valor `BOOL`:


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

Usando `PP_CONCAT`, primero concatenamos `PP_BOOL_` y `arg0`, luego evaluamos el resultado de la concatenación. Aquí, `arg0` debe ser un número que se evalúe en el rango de `[0, 256]`, después de evaluarlo, lo concatenamos después de `PP_BOOL_` y evaluamos para obtener un valor booleano. Operaciones de 'and', 'or' y 'not':

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

Primero se evalúa el argumento utilizando `PP_BOOL` y luego se concatenan los resultados de las operaciones lógicas en base a las combinaciones de `0` y `1`. Si no se utiliza `PP_BOOL` para la evaluación, el argumento solo puede aceptar los valores `0` y `1`, lo que reduce significativamente su aplicabilidad. Del mismo modo, se pueden escribir operaciones de exclusión mutua, inclusión o exclusión, si estás interesado, puedes intentarlo por ti mismo.

####**Condiciones de selección**

Utilizando `PP_BOOL` y `PP_CONCAT`, también se puede escribir una declaración de selección condicional:

``` cpp
#define PP_IF(if, then, else) PP_CONCAT(PP_IF_, PP_BOOL(if))(then, else)
#define PP_IF_1(then, else) then
#define PP_IF_0(then, else) else

PP_IF(1, 2, 3)      // -> PP_IF_1(2, 3) -> 2
PP_IF(0, 2, 3)      // -> PP_IF_0(2, 3) -> 3
```

Si el valor de `if` es evaluado como `1`, se concatena con `PP_CONCAT` para formar `PP_IF_1`, y finalmente se expande con el valor de `then`. Del mismo modo, si el valor de `if` es evaluado como `0`, se obtiene `PP_IF_0`.

####**递增递减** se traduce al español como **incremento y decremento**.

**整数递增递减：**

En el campo de las matemáticas, la secuencia de números enteros puede incrementarse o decrecer.

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

Al igual que con `PP_BOOL`, también hay restricciones en los incrementos y decrementos de los números enteros. Aquí, el rango está establecido en `[0, 256]`. Después de alcanzar `256` en el incremento, por precaución, `PP_INC_256` devolverá el límite de `256` como valor límite. De manera similar, `PP_DEC_0` también devolverá `0`.

####**变长参数** se traduce al español como **parámetros variables**.

`Macro` puede aceptar argumentos variables, en el siguiente formato:

```cpp
#define LOG(format, ...) printf("log: " format, __VA_ARGS__)

LOG("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG("Hello World")              // -> printf("log: " "Hello World", ); 多了个逗号，编译报错

LOG("Hola Mundo")               // -> printf("log: " "Hola Mundo", ); 多了个逗号，编译报错
```

Debido a que los argumentos de longitud variable pueden estar vacíos, en caso de estar vacíos, pueden ocasionar errores de compilación. Por lo tanto, C++ 20 introdujo `__VA_OPT__`, que devuelve un valor vacío si los argumentos de longitud variable están vacíos, y de lo contrario devuelve los argumentos originales:

```cpp
#define LOG2(format, ...) printf("log: " format __VA_OPT__(,) __VA_ARGS__)

LOG2("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG2("Hola Mundo")  // -> printf("registro: " "Hola Mundo" ); Sin comas, se compila normalmente
```

Pero lamentablemente, solo las estándares de C++ 20 en adelante tienen esta macro, a continuación daremos el método de implementación de `__VA_OPT__`.

####惰性求值

La expresión "惰性求值" en español se traduce como "evaluación perezosa".

Consider this scenario:

``` cpp
PP_IF(1, PP_COMMA(), PP_LPAREN())     // -> PP_IF_1(,,)) -> Error: lista de argumentos incompleta al invocar la macro "PP_IF_1"
```

Sabemos que al expandirse una macro se evalúan los primeros argumentos. Después de evaluar `PP_COMMA()` y `PP_LPAREN()`, se pasan a `PP_IF_1` obteniendo `PP_IF_1(,,))`, lo que causa un error en el preprocesamiento. En este caso, se puede utilizar un enfoque llamado evaluación perezosa:

``` cpp
PP_IF(1, PP_COMMA, PP_LPAREN)()       // -> PP_IF_1(PP_COMMA, PP_LPAREN)() -> PP_COMMA() -> ,
```

Cambie este estilo de escritura, solo pase el nombre de la macro, permita que `PP_IF` elija el nombre de macro necesario y luego concaténelo con paréntesis `()` para formar la macro completa, luego expándala. La evaluación perezosa también es muy común en la programación de macros.

####\(以括号开始\)

Verifica si los parámetros variables comienzan con paréntesis:

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

`PP_IS_BEGIN_PARENS` se puede utilizar para determinar si los argumentos pasados comienzan con paréntesis. Se necesita usar esto cuando se manejan argumentos entre paréntesis (como se explica más adelante en la implementación de `__VA_OPT__`). Parece un poco complicado, pero la idea principal es construir una macro que evalúe si los argumentos variables comienzan con paréntesis, para obtener un resultado en un escenario, y si no, obtener otro resultado. Veamos con más detalle:

La funcionalidad de la macro formada por `PP_IS_BEGIN_PARENS_PROCESS` y `PP_IS_BEGIN_PARENS_PROCESS_0` es evaluar los argumentos variables que se le pasan y luego tomar el primer argumento.

`PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__)` implica que primero se evalúa `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__`, y luego se concatena el resultado de la evaluación con `PP_IS_BEGIN_PARENS_PRE_`.

`PP_IS_BEGIN_PARENS_EAT(...)` La macro devora todos los parámetros y devuelve 1. Si en el paso anterior `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__`, `__VA_ARGS__` comienza con un paréntesis, entonces habrá una coincidencia en la evaluación de `PP_IS_BEGIN_PARENS_EAT(...)` y devolverá 1. En cambio, si no comienza con un paréntesis, no habrá coincidencia y `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` permanecerá sin cambios.

Si el valor de `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` es evaluado como `1`, entonces `PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, 1) -> PP_IS_BEGIN_PARENS_PRE_1 -> 1`, ten en cuenta que después de `1` hay una coma, se pasa `1,` a `PP_IS_BEGIN_PARENS_PROCESS_0`, se toma el primer argumento y finalmente se obtiene `1`, lo que indica que el argumento comienza con paréntesis.

Si `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` evalúa a algo diferente de `1` y se mantiene sin cambios, entonces `PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__) -> PP_IS_BEGIN_PARENS_PRE_PP_IS_BEGIN_PARENS_EAT __VA_ARGS__ -> 0, __VA_ARGS__`, cuando se pasa a `PP_IS_BEGIN_PARENS_PROCESS_0`, se obtiene `0`, lo que indica que los parámetros no comienzan con un paréntesis.

####`变长参数空` se traduce al español como `parámetro variable vacío`.

Comprobar si los argumentos variables son nulos también es una macro común que se utiliza al implementar `__VA_OPT__`. Podemos utilizar `PP_IS_BEGIN_PARENS` aquí para escribir una versión incompleta:

``` cpp
#define PP_IS_EMPTY_PROCESS(...) \
    PP_IS_BEGIN_PARENS(PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ())
#define PP_IS_EMPTY_PROCESS_EAT(...) ()

PP_IS_EMPTY_PROCESS()       // -> 1
PP_IS_EMPTY_PROCESS(1)      // -> 0
PP_IS_EMPTY_PROCESS(1, 2)   // -> 0
PP_IS_EMPTY_PROCESS(())     // -> 1
```

La función de `PP_IS_EMPTY_PROCESS` es verificar si `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ()` comienza con paréntesis.

Si `__VA_ARGS__` está vacío, `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ () -> PP_IS_EMPTY_PROCESS_EAT() -> ()`, se obtiene un paréntesis `()`, que luego se pasa a `PP_IS_BEGIN_PARENS` que devuelve `1`, lo que indica que el argumento está vacío.

De lo contrario, `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ()` se pasa sin cambios a `PP_IS_BEGIN_PARENS`, devolviendo 0 para indicar que no está vacío.

Ten en cuenta el cuarto ejemplo `PP_IS_EMPTY_PROCESS(()) -> 1`, `PP_IS_EMPTY_PROCESS` no puede manejar correctamente los argumentos de longitud variable que comienzan con paréntesis, debido a que los paréntesis de los argumentos de longitud variable coinciden con `PP_IS_EMPTY_PROCESS_EAT` y se evalúa como `()`. Para resolver este problema, debemos tratar de manera diferente los casos en los que el argumento comienza con paréntesis.

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

`PP_IS_EMPTY_IF` devuelve el primer o segundo parámetro según la condición especificada por `if`.

Si los argumentos variables pasados comienzan con paréntesis, `PP_IS_EMPTY_IF` devuelve `PP_IS_EMPTY_ZERO` y finalmente devuelve `0`, lo que indica que los argumentos variables no están vacíos.

Por el contrario, `PP_IS_EMPTY_IF` devuelve `PP_IS_EMPTY_PROCESS`, y finalmente `PP_IS_EMPTY_PROCESS` se encargará de determinar si los argumentos variables están vacíos.

####Acceso a través de subíndices

Obtener el elemento en la posición especificada de los parámetros de longitud variable:

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

El primer argumento de `PP_ARGS_ELEM` es el índice del elemento `I`, seguido de los argumentos variables. Utilizando `PP_CONCAT`, se puede concatenar `PP_ARGS_ELEM_` y `I` para obtener la macro `PP_ARGS_ELEM_0..8` que devuelve el elemento en la posición correspondiente. Luego se deben pasar los argumentos variables a esa macro para expandir y obtener el elemento en el índice especificado.

#### PP_IS_EMPTY2

Utilizando `PP_ARGS_ELEM` también se puede implementar otra versión de `PP_IS_EMPTY`:

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

Utilizar `PP_ARGS_ELEM` para determinar si un argumento contiene una coma `PP_HAS_COMMA`. `PP_COMMA_ARGS` consumirá cualquier argumento proporcionado y devolverá una coma.

La lógica básica para verificar si los parámetros variables son nulos es `PP_COMMA_ARGS __VA_ARGS__ ()`, que devuelve una coma si `__VA_ARGS__` está vacío. `PP_COMMA_ARGS` y `()` se unen y se evalúan juntos, la manera específica de escribirlo es `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ())`.

Sin embargo, puede haber excepciones:

* `__VA_ARGS__` en sí mismo puede contener comas;
* La concatenación de `__VA_ARGS__ ()` dará lugar a la evaluación de la coma.
* `PP_COMMA_ARGS __VA_ARGS__` se concatena para evaluar y producir una coma;

Para abordar las tres excepciones mencionadas anteriormente, es necesario hacer una exclusión, por lo que la forma final es equivalente a realizar una operación lógica AND en las siguientes 4 condiciones:

* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__))` &&
* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__()))` &&
* `PP_NOT(PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__))` &&
* `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ())`

#### `__VA_OPT__`

La utilización de `PP_IS_EMPTY` finalmente permite implementar macros similar a `__VA_OPT__`:

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

`PP_ARGS_OPT` acepta dos argumentos fijos y argumentos variables. Si los argumentos variables no están vacíos, devuelve `data`; de lo contrario, devuelve `empty`. Para permitir el uso de comas en `data` y `empty`, se requiere que ambos estén entre paréntesis con los argumentos reales, y luego se utiliza `PP_REMOVE_PARENS` para eliminar los paréntesis exteriores.

Con el uso de `PP_ARGS_OPT`, es posible lograr la funcionalidad de emular `LOG2` mediante `LOG3`:

``` cpp
#define LOG3(format, ...) \
    printf("log: " format PP_ARGS_OPT((,), (), __VA_ARGS__) __VA_ARGS__)

LOG3("Hello");                  // -> printf("log: " "Hello" );
LOG3("Hello %s", "World");      // -> printf("log: " "Hello %s" , "World");
```

`data_tuple` es `(,)`, si los argumentos variables no están vacíos, se devolverán todos los elementos de `data_tuple`, que en este caso es la coma `,`.

####Solicitar el número de parámetros

Obtener la cantidad de argumentos variables:

``` cpp
#define PP_ARGS_SIZE_IMCOMPLETE(...) \
    PP_ARGS_ELEM(8, __VA_ARGS__, 8, 7, 6, 5, 4, 3, 2, 1, 0)

PP_ARGS_SIZE_IMCOMPLETE(a)             // -> 1
PP_ARGS_SIZE_IMCOMPLETE(a, b)          // -> 2
PP_ARGS_SIZE_IMCOMPLETE(PP_COMMA())    // -> 2
PP_ARGS_SIZE_IMCOMPLETE()              // -> 1
```

Contar el número de argumentos variables se obtiene a través del conteo de la posición de los parámetros. `__VA_ARGS__` hace que todos los argumentos subsiguientes se muevan hacia la derecha. Usar la macro `PP_ARGS_ELEM` para obtener el argumento en la posición 8. Si `__VA_ARGS__` solo tiene un argumento, entonces el octavo argumento será igual a `1`; de manera similar, si `__VA_ARGS__` tiene dos argumentos, entonces el octavo argumento será igual a `2`, exactamente igual al número de argumentos variables.

Aquí se proporciona un ejemplo que solo admite un máximo de 8 argumentos variables, esto depende de la longitud máxima que `PP_ARGS_ELEM` pueda soportar.

Pero este macro aún no está completo. En caso de que los argumentos variables sean nulos, este macro devolverá incorrectamente `1`. Si se desea manejar argumentos variables nulos, es necesario utilizar el macro `PP_ARGS_OPT` que mencionamos anteriormente:

``` cpp
#define PP_COMMA_IF_ARGS(...) PP_ARGS_OPT((,), (), __VA_ARGS__)
#define PP_ARGS_SIZE(...) PP_ARGS_ELEM(8, __VA_ARGS__ PP_COMMA_IF_ARGS(__VA_ARGS__) 8, 7, 6, 5, 4, 3, 2, 1, 0, 0, 0)

PP_ARGS_SIZE(a)             // -> 1
PP_ARGS_SIZE(a, b)          // -> 2
PP_ARGS_SIZE(PP_COMMA())    // -> 2
PP_ARGS_SIZE()              // -> 0
PP_ARGS_SIZE(,,,)           // -> 4
```

El problema clave radica en la coma `,` ya que cuando `__VA_ARGS__` está vacío, al omitir la coma se puede devolver correctamente `0`.

####遍历访问 significa "recorrer y acceder".

Similar a C++ `for_each`, podemos implementar el macro `PP_FOR_EACH`:

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

`PP_FOR_EACH` recibe dos parámetros fijos: `macro`, que se puede entender como la macro que se llama durante el recorrido, y `context`, que se puede pasar como un parámetro de valor fijo a `macro`. `PP_FOR_EACH` primero obtiene la longitud de los argumentos variables utilizando `PP_ARGS_SIZE`, luego utiliza `PP_CONCAT` para concatenar y obtener `PP_FOR_EACH_N`. A continuación, `PP_FOR_EACH_N` itera llamando a `PP_FOR_EACH_N-1` para lograr el mismo número de iteraciones que la cantidad de argumentos variables.

En el ejemplo, declaramos `DECLARE_EACH` como parámetro `macro`. La función de `DECLARE_EACH` es devolver `contex arg`, donde `contex` es el nombre del tipo y `arg` es el nombre de la variable. Con `DECLARE_EACH`, se puede declarar una variable.

####**Bucle condicional**

Con la introducción de `FOR_EACH`, también podemos escribir el `PP_WHILE` de manera similar:

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

`PP_WHILE` acepta tres parámetros: `pred` para la función de condición, `op` para la función de operación, `val` como valor inicial; durante el proceso del bucle, se utiliza constantemente `pred(val)` para evaluar la condición de terminación del bucle, y se pasa el valor obtenido de `op(val)` a la macro siguiente. Se puede entender como la ejecución del siguiente código:

``` cpp
while (pred(val)) {
    val = op(val);
}
```

`PP_WHILE_N` Primero se utiliza `pred(val)` para obtener el resultado de la evaluación de la condición, a continuación se pasa el resultado de la condición `cond` y los demás parámetros a `PP_WHILE_N_IMPL`.
`PP_WHILE_N_IMPL` se puede dividir en dos partes: la segunda mitad `(pred, op, PP_IF(cond, op, PP_EMPTY_EAT)(val))` se utiliza como argumento de la primera mitad, donde `PP_IF(cond, op, PP_EMPTY_EAT)(val)` evalúa `op(val)` si `cond` es verdadero, de lo contrario, se evalúa `PP_EMPTY_EAT(val)` para obtener un resultado vacío. La primera mitad `PP_IF(cond, PP_WHILE_N+1, val PP_EMPTY_EAT)` devuelve `PP_WHILE_N+1` si `cond` es verdadero, combinado con los argumentos de la segunda mitad para continuar ejecutando el bucle. De lo contrario, devuelve `val PP_EMPTY_EAT`, donde `val` es el resultado final del cálculo y `PP_EMPTY_EAT` elimina el resultado de la segunda mitad.

`SUM` realiza la suma de `N + N-1 + ... + 1`. Inicializa con los valores `(max_num, origin_num)`; `SUM_PRED` toma el primer elemento del valor `x` y verifica si es mayor que 0; `SUM_OP` realiza la operación de decremento en `x = x - 1` y la operación de suma en `y = y + x` . Simplemente pasa `SUM_PRED` y `SUM_OP` a `PP_WHILE`, el resultado devuelto es una tupla, el resultado que realmente queremos es el segundo elemento de la tupla, así que usamos `SUM` para obtener el valor del segundo elemento.

####递归重入

Hasta ahora, nuestras operaciones de recorrido y bucles condicionales han funcionado correctamente, los resultados han sido los esperados. ¿Recuerdan cuando hablamos de la regla de expansión de macros y mencionamos la prohibición de la recursión? Desafortunadamente, nos encontramos con esa prohibición cuando intentamos ejecutar un bucle anidado.

``` cpp
#define SUM_OP2(xy_tuple) SUM_OP_OP_IMPL2 xy_tuple
#define SUM_OP_OP_IMPL2(x, y) (PP_DEC(x), y + SUM(x, 0))

#define SUM2(max_num, origin_num) \
    PP_IDENTITY(SUM_IMPL PP_WHILE(SUM_PRED, SUM_OP2, (max_num, origin_num)))

SUM2(1, a)      // -> a + SUM_IMPL PP_WHILE_1(SUM_PRED, SUM_OP, (1, a))
```

`SUM2` cambia el parámetro `op` por `SUM_OP2`, dentro de `SUM_OP2` se llamará a `SUM`, y cuando `SUM` se expanda será `PP_WHILE_1`, lo que equivale a una llamada recursiva de `PP_WHILE_1` a sí misma, y el preprocesador dejará de expandirlo.

Para resolver este problema, podemos utilizar un método de recursión automática conocido como "Recursive Automático".

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

`PP_AUTO_WHILE` es la versión recursiva deducida automáticamente de `PP_WHILE`, la macro principal es `PP_AUTO_REC(PP_WHILE_PRED)`, esta macro puede encontrar el número `N` de la versión actualmente disponible de  `PP_WHILE_N`.

El principio de inferencia es muy sencillo, consiste en buscar todas las versiones y encontrar aquella que se pueda expandir correctamente, devolviendo el número correspondiente a esa versión. Para mejorar la velocidad de búsqueda, se suele utilizar la búsqueda binaria, que es exactamente lo que hace `PP_AUTO_REC`. `PP_AUTO_REC` recibe un parámetro llamado `check`, encargado de verificar la disponibilidad de la versión. Aquí se muestra el rango de versiones que se pueden buscar: `[1, 4]`. `PP_AUTO_REC` primero verifica `check(2)`, si devuelve verdadero, llama a `PP_AUTO_REC_12` para buscar en el rango `[1, 2]`, de lo contrario utiliza `PP_AUTO_REC_34` para buscar en el rango `[3, 4]`. `PP_AUTO_REC_12` verifica `check(1)`, si es verdadero significa que la versión `1` está disponible, de lo contrario utiliza la versión `2`. Lo mismo aplica para `PP_AUTO_REC_34`.

`check` ¿Cómo se debe escribir la macro para saber si la versión está disponible? Aquí, `PP_WHILE_PRED` se expandirá en dos partes concatenadas. Veamos la parte posterior `PP_WHILE_ ## n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`: si `PP_WHILE_ ## n` está disponible, debido a que `PP_WHILE_FALSE` siempre devuelve `0`, esta parte se expandirá para obtener el valor del parámetro `val`, que es `PP_WHILE_FALSE`; de lo contrario, esta macro se mantendrá inalterada y seguirá siendo `PP_WHILE_n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`.

Unimos los resultados de la parte posterior con el prefijo `PP_WHILE_CHECK_`, obteniendo dos posibles resultados: `PP_WHILE_CHECK_PP_WHILE_FALSE` o `PP_WHILE_CHECK_PP_WHILE_n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`. Por lo tanto, hacemos que `PP_WHILE_CHECK_PP_WHILE_FALSE` devuelva `1` para indicar su disponibilidad, mientras que `PP_WHILE_CHECK_PP_WHILE_n` devuelve `0` para indicar su no disponibilidad. De esta manera, hemos completado la funcionalidad de derivación automática de recursión.

####**算术比较**

No son iguales:

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

Para determinar si dos valores son iguales, se utiliza la propiedad de prohibir la reentrada recursiva. Los valores `x` e `y` se concatenan recursivamente para formar la macro `PP_NOT_EQUAL_x PP_NOT_EQUAL_y`. Si `x == y`, entonces no se expandirá la macro `PP_NOT_EQUAL_y` y se concatenará con `PP_NOT_EQUAL_CHECK_`, formando `PP_NOT_EQUAL_CHECK_PP_NOT_EQUAL_y` que devuelve `0`. Por otro lado, si ambas expansiones tienen éxito, se obtiene finalmente `PP_EQUAL_NIL`, el cual se concatena con `PP_NOT_EQUAL_CHECK_` para formar `PP_NOT_EQUAL_CHECK_PP_EQUAL_NIL` que devuelve `1`.

**相等：**

La palabra "相等" se traduce al español como "igual".

``` cpp
#define PP_EQUAL(x, y) PP_NOT(PP_NOT_EQUAL(x, y))

PP_EQUAL(1, 1)              // -> 1
PP_EQUAL(1, 3)              // -> 0

```

Menor o igual que:

``` cpp
#define PP_LESS_EQUAL(x, y) PP_NOT(PP_SUB(x, y))

PP_LESS_EQUAL(2, 1)         // -> 0
PP_LESS_EQUAL(1, 1)         // -> 1
PP_LESS_EQUAL(1, 2)         // -> 1
```

Menor que:

``` cpp
#define PP_LESS(x, y) PP_AND(PP_LESS_EQUAL(x, y), PP_NOT_EQUAL(x, y))

PP_LESS(2, 1)               // -> 0
PP_LESS(1, 2)               // -> 1
PP_LESS(2, 2)               // -> 0
```

Además, hay comparaciones aritméticas como mayor que, mayor o igual, y así sucesivamente, las cuales no serán explicadas aquí nuevamente.

####Las operaciones aritméticas

Utilizando `PP_AUTO_WHILE`, podemos realizar operaciones aritméticas básicas y admitir operaciones anidadas.

**Suma:**



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

Resta:

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

La multiplicación es una operación matemática que consiste en combinar dos números para obtener un producto. Se representa con el símbolo "×" o el punto ".". En esta operación, el primer número se llama multiplicando y el segundo número se llama multiplicador. El resultado de la multiplicación se llama producto.

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

La multiplicación aquí ha añadido un parámetro `ret`, con un valor inicial de `0`. En cada iteración, se ejecuta `ret = ret + x`.

La división:

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

La división utiliza `PP_LESS_EQUAL`, solo continuará el bucle si `y <= x`.

####**数据结构**

Incluso los macros pueden tener estructuras de datos, de hecho, en ejemplos anteriores hemos utilizado una estructura de datos llamada `tuple` para eliminar los paréntesis externos y obtener los elementos internos. Tomemos `tuple` como ejemplo para discutir su implementación relacionada, si tienes interés, puedes buscar la implementación de otras estructuras de datos como `list`, `array` en `Boost`.

`tuple` se define como una colección de elementos separados por comas y encerrados en paréntesis: `(a, b, c)`.

``` cpp
#define PP_TUPLE_REMOVE_PARENS(tuple) PP_REMOVE_PARENS(tuple)

// Obtener el elemento en el índice especificado
#define PP_TUPLE_ELEM(i, tuple) PP_ARGS_ELEM(i, PP_TUPLE_REMOVE_PARENS(tuple))

// Devuelve vacío después de tragar toda la tupla.
#define PP_TUPLE_EAT() PP_EMPTY_EAT

// Obtener tamaño
#define PP_TUPLE_SIZE(tuple) PP_ARGS_SIZE(PP_TUPLE_REMOVE_PARENS(tuple))

// Añadir elemento
#define PP_TUPLE_PUSH_BACK(elem, tuple) \
    PP_TUPLE_PUSH_BACK_IMPL(PP_TUPLE_SIZE(tuple), elem, tuple)
#define PP_TUPLE_PUSH_BACK_IMPL(size, elem, tuple) \
    (PP_TUPLE_REMOVE_PARENS(tuple) PP_IF(size, PP_COMMA, PP_EMPTY)() elem)

// Insertar elementos
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

// Eliminar el último elemento
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

// Eliminar elemento
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

Aquí explicaré un poco la implementación de la inserción de elementos, y las operaciones de eliminación de elementos u otras se implementan utilizando un principio similar. `PP_TUPLE_INSERT(i, elem, tuple)` permite insertar el elemento `elem` en la posición `i` de `tuple`. Para llevar a cabo esta operación, primero se colocan todos los elementos con posiciones menores a `i` en un nuevo `tuple` (`ret`) utilizando `PP_TUPLE_PUSH_BACK`. Luego, se coloca `elem` en la posición `i`. Después, se añaden los elementos del `tuple` original con posiciones mayores o iguales a `i` al final de `ret`. Finalmente, obtenemos el resultado deseado en `ret`.

##**小结**

Un resumen.

(https://github.com/pfultz2/Cloak/wiki/C-Preprocessor-tricks,-tips,-and-idioms#deferred-expression)，BOOST_PP 里面的 `REPEAT` 相关宏等等，有兴趣的可以自行查阅资料。

El depurado de la programación macro es un proceso doloroso, podemos:

Utilice la opción `-P -E` para imprimir los resultados de la preprocesamiento;
* Utilicé la versión modificada de `clang` que mencioné anteriormente para analizar detenidamente el proceso de expansión;
* Desglosar los macros complicados y ver los resultados de expansión de los macros intermedios;
* Filtra los archivos de encabezado y macros no relacionados;
* Por último, se trata del proceso de expansión de macros, familiarizarse con la expansión de macros también mejorará la eficiencia de depuración.

El código de macro en este texto fue reescrito por mí mismo después de comprender los principios. Algunas de las macros se inspiraron en la implementación de `Boost` y en artículos de referencia. Si encuentras algún error, por favor házmelo saber y también estaré encantado de discutir cualquier problema relacionado.

El código completo de este texto se encuentra aquí: [Descargar](assets/img/2021-3-31-cpp-preprocess/macros.cpp), [Demo en línea](https://godbolt.org/z/coWvc5Pse).

##> Cita

* [Boost.Preprocessor](https://www.boost.org/doc/libs/1_75_0/libs/preprocessor/doc/)
* [Arte de la programación de macros en C/C++](https://bot-man-jl.github.io/articles/?post=2020/Macro-Programming-Art)

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
