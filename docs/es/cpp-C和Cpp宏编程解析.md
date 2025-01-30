---
layout: post
title: C/C++ Análisis de programación con macros
categories:
- c++
catalog: true
tags:
- dev
description: El objetivo de este artículo es aclarar las reglas y métodos de implementación
  de la programación macro en C/C++, para que no tengas miedo de ver macros en el
  código.
figures: []
---

<meta property="og:title" content="C/C++ 宏编程解析" />

El propósito de este texto es explicar las reglas y métodos de implementación de la programación de macros en C/C++, para que ya no tengas miedo de encontrar macros dentro del código. Primero hablaré sobre las reglas de expansión de macros mencionadas en el estándar C++ 14, luego observaremos la expansión de macros modificando el código fuente de Clang, y finalmente discutiré la implementación de la programación de macros basada en este conocimiento.

Todo el código de este artículo se encuentra aquí: [Descargar](assets/img/2021-3-31-cpp-preprocess/macros.cpp)，[Demo en línea](https://godbolt.org/z/coWvc5Pse)Lo siento, pero no hay texto en el que pueda trabajar. Por favor, proporcione algo que pueda traducir.

##引子

Podemos hacer que el compilador ejecute solo el preprocesamiento del archivo `a.cpp` y guarde el resultado en `a.cpp.i` mediante el comando `gcc -P -E a.cpp -o a.cpp.i`.

Primero, echemos un vistazo a algunos ejemplos:

####Recursividad de entrada (Reentrancy)

``` cpp
#define ITER(arg0, arg1) ITER(arg1, arg0)

ITER(1, 2)          // -> ITER(2, 1)
```

La macro `ITER` intercambia la posición de `arg0` y `arg1`. Después de expandir la macro, obtenemos `ITER(2, 1)`.

Se puede observar que se ha intercambiado con éxito la posición de `arg0` y `arg1`. En este punto, la macro se ha expandido con éxito una vez, pero solo una vez, sin volver a recursividad. En otras palabras, durante la expansión de la macro, no se permite la recursividad de sí misma. Si durante el proceso recursivo se detecta que la misma macro ya se ha expandido en una recursión anterior, no se expandirá nuevamente. Esta es una regla importante en la expansión de macros. La prohibición de la recursividad tiene una razón muy simple, que es evitar la recursión infinita.

####Concatenación de cadenas

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                // -> HelloWorld
CONCAT(Hola, CONCAT(Mundo, !))     // ->　HolaCONCAT(Mundo, !)
```

La función `CONCAT` tiene como objetivo unir `arg0` con `arg1`. Después de la expansión de la macro, `CONCAT(Hello, World)` obtiene el resultado correcto `HelloWorld`. Sin embargo, `CONCAT(Hello, CONCAT(World, !))` solo expande la macro externa, y la macro interna `CONCAT(World, !)` no se expande y se une directamente a `Hello`. Esto difiere de lo que esperábamos, ya que el resultado deseado es `HelloWorld!`. Este es otro importante principio de expansión de macros: los argumentos de macro que siguen al operador `##` no se expandirán, sino que se unirán directamente al contenido anterior.

A través de los dos ejemplos anteriores se puede observar que las reglas de expansión de macros pueden resultar contraintuitivas. Si no se tiene claro el conjunto de reglas específicas, es posible que la macro escrita no produzca el efecto deseado.

##Desplegar reglas de expansión.

A través de los dos ejemplos introductorios, hemos comprendido que la expansión de macros sigue un conjunto estándar de reglas, estas reglas están definidas en el estándar de C/C++, no son extensas, se recomienda leerlas detenidamente varias veces. Aquí les adjunto el enlace a la versión del estándar n4296, donde se define la expansión de macros en la sección 16.3: [enlace](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4296.pdf)A continuación, señalaré algunas reglas importantes de la versión n4296, las cuales determinarán cómo escribir correctamente macros (aunque se recomienda tomarse un tiempo para leer detenidamente las macros en el estándar).

####Parámetro de separación

Los requisitos de los parámetros de la macro son separados por comas, y el número de parámetros debe coincidir con el número de definiciones de la macro. En los parámetros pasados a la macro, los contenidos adicionales entre paréntesis se consideran como un solo parámetro, y se permite que los parámetros estén vacíos.

``` cpp
#define ADD_COMMA(arg1, arg2) arg1, arg2

ADD_COMMA(a, b)             // -> a, b
ADD_COMMA(a)                // Error "la macro "MACRO" requiere 2 argumentos, pero solo se ha dado 1"
ADD_COMMA((a, b), c)        // -> (a, b), c
ADD_COMMA(, b)              // -> , b
```

`ADD_COMMA((a, b), c)` donde `(a, b)` se considera el primer parámetro. En `ADD_COMMA(, b)`, el primer parámetro está vacío, por lo que se expande a `, b`.

####Expansión de macros

Al expandir un macro, si los parámetros del macro también son macros que se pueden expandir, primero se expandirán completamente los parámetros y luego se expandirá el macro, por ejemplo.

``` cpp
ADD_COMMA(ADD_COMMA(1, 2), ADD_COMMA(3, 4))     // -> 1, 2, 3, 4
```

En términos generales, la expansión de macros se puede considerar como primero evaluar los parámetros y luego evaluar la macro, a menos que se encuentren los operadores `#` y `##`.

####Operador `#`

Los parámetros de macro que siguen al operador `#` no se expandirán, se convertirán directamente en cadenas de texto, por ejemplo:

``` cpp
#define STRINGIZE(arg0) # arg0

STRINGIZE(a)                // -> "a"
STRINGIZE(STRINGIZE(a))     // -> "STRINGIZE(a)"
```

Según esta regla, `STRINGIZE(STRINGIZE(a))` solo puede expandirse a `"STRINGIZE(a)"`.

####`##` Operador

Los parámetros de la macro antes y después del operador `##` no se expandirán, se concatenarán directamente, por ejemplo:

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                        // -> HelloWorld
CONCAT(Hello, CONCAT(World, !))             // -> HelloCONCAT(World, !)
CONCAT(CONCAT(Hello, World) C, ONCAT(!))    // -> CONCAT(Hello, World) CONCAT(!)
```

Debes concatenar "Hello, World" y luego añadirle "!" para obtener "Hello, World!".

####Escaneo repetido

Una vez que el preprocesador realiza la expansión de macro una vez, volverá a escanear el contenido obtenido y continuará expandiéndolo hasta que ya no haya más contenido por expandir.

Una vez que una macro se expande, se puede entender como la completa expansión de sus argumentos (a menos que se encuentren `#` y `##`), luego, de acuerdo con la definición de la macro, se sustituyen la macro y sus argumentos completamente expandidos según la definición, y luego se aplican todos los operadores `#` y `##` presentes en la definición.

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define STRINGIZE(arg0) # arg0

CONCAT(STRING, IZE(Hello))        // -> STRINGIZE(Hello) -> "Hello"
```

`CONCAT(STRING, IZE(Hello))` la primera vez se expande a `STRINGIZE(Hello)`, luego, al realizar una segunda expansión, se descubre que `STRINGIZE` puede seguir expandiéndose, y al final se obtiene `"Hello"`.

####Prohibición de recursión reentrante

Durante el proceso de escaneo repetido, se prohíbe la expansión recursiva de la misma macro. Se puede entender la expansión de macros como una estructura en forma de árbol, donde el nodo raíz es la macro que se va a expandir inicialmente, y cada contenido que surge tras la expansión de una macro se conecta como un nodo hijo a dicho árbol. Por lo tanto, la prohibición de la recursividad implica que al expandir las macros de los nodos hijos, si alguna macro es igual a cualquier macro de un nodo antecesor, se prohíbe la expansión. Veamos algunos ejemplos:

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define CONCAT_SPACE(arg0, arg1) arg0 arg1
#define IDENTITY(arg0) IDENTITY_IMPL(arg0)
#define IDENTITY_IMPL(arg0) arg0

CONCAT(CON, CAT(a, b))                  // -> CONCAT(a, b)
IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))   // -> CONCAT(a, b)
IDENTITY(CONCAT(CON, CAT(a, b)))        // -> IDENTITY_IMPL(CONCAT(a, b)) -> CONCAT(a, b)
```

`CONCAT(CON, CAT(a, b))`: Debido a que `CONCAT` concatena dos parámetros con `##`, según las reglas de `##`, no expandirá los parámetros y los concatenará directamente. Por lo tanto, expandiríamos primero obteniendo `CONCAT(a, b)`. Dado que `CONCAT` ya se ha expandido, no lo hará de manera recursiva, lo que detendrá el proceso.

`IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))`: `IDENTITY_IMPL` can be understood as evaluating the parameter `arg0`, where the parameter `arg0` evaluates to `CONCAT(a, b)`, and due to recursion being marked as not reentrant, `IDENTITY_IMPL` completes its expansion. During the second scan, it is found that `CONCAT(a, b)` is marked as not reentrant, and the expansion is stopped. Here, `CONCAT(a, b)` is obtained from expanding the parameter `arg0`, but in subsequent expansions, it will also maintain the not reentrant marking, which can be understood as the parent node being the parameter `arg0`, continuously maintaining the not reentrant marking.

`IDENTITY(CONCAT(CON, CAT(a, b)))`: Este ejemplo tiene como objetivo reforzar la comprensión de los nodos padre e hijo. Cuando los parámetros se expanden por sí mismos, se consideran a sí mismos como nodos padre, y el contenido expandido se utiliza como nodos hijo para evaluar la recursión. Los parámetros expandidos que se envían a la macro mantienen la marca de prohibición de reentrada (si no se modifica el parámetro después de enviarlo a la macro). Se puede ver el proceso de expansión de los parámetros como otro árbol, donde el resultado de la expansión de los parámetros es el nodo hijo más bajo del árbol. Este nodo hijo se envía a la macro para realizar la expansión, manteniendo al mismo tiempo la característica de prohibición de reentrada.

Por ejemplo aquí, después de la primera expansión completa se obtiene `IDENTITY_IMPL(CONCAT(a, b))`, `CONCAT(a, b)` se marca como prohibido para la reinvocación, aunque `IDENTITY_IMPL` evalúa los parámetros, los parámetros ya están prohibidos para la expansión, por lo que se pasan tal cual a la definición y al final seguimos obteniendo `CONCAT(a, b)`.

Above, I have only listed some rules that I deem important or that I find somewhat difficult to understand. For detailed macro expansion rules, I still recommend spending some time to directly consult the standard documentation.

##Observando el proceso de expansión a través de Clang

Podemos agregar algunas declaraciones de impresión al código fuente de Clang para observar el proceso de expansión de macros. No tengo la intención de profundizar en la explicación del código fuente de Clang, así que aquí presento un archivo diff modificado. Los interesados pueden compilar Clang por su cuenta para investigarlo. Aquí estoy usando la versión 11.1.0 de llvm ([enlace](https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-11.1.0.tar.gz)），修改过的文件（[link](assets/img/2021-3-31-cpp-preprocess/clang-modify.zip)A continuación, validamos brevemente las reglas de expansión de macros que presentamos anteriormente mediante un ejemplo:

####Translate these text into Spanish language:

Ejemplo 1

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(C, ONCAT(a, b))      // CONCAT(a, b)
```

Utilice Clang modificado para preprocesar el código anterior: `clang -P -E a.cpp -o a.cpp.i`, obteniendo la siguiente información impresa:

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

第 [1](#__codelineno-9-1)El `HandleIdentifier` imprime cuando encuentra un macro, y luego imprime la información del macro (número [2-4](#__codelineno-9-2)行），宏没有禁用，所以可以按照定义来展开 `Macro is ok to expand`，之后进入宏 `EnterMacro`。

La función que realmente realiza la expansión de macros es `ExpandFunctionArguments`, luego se imprime de nuevo la información de la macro a expandir, notando que en este momento la macro ya ha sido marcada como `utilizada` (página [9](#__codelineno-9-9)Después, se procede a expandir uno a uno los `Token` de acuerdo con la definición del macro (`Token` es un concepto dentro del preprocesador de `Clang`, el cual no se profundizará aquí).

El `Token` número 0 es el parámetro formal `arg0`, cuyo argumento real es `C`, se determina que no es necesario expandir, por lo que se copia directamente al resultado (número [11-13](#__codelineno-9-11)Lo siento, no hay texto para traducir. 

(#__codelineno-9-14)行）。

El segundo `Token` es el parámetro `arg1`, y el argumento correspondiente es `ONCAT(a, b)`. El preprocesador también procesa los argumentos en `Token`s individuales, por lo que podemos ver que el resultado impreso encierra cada `Token` del argumento entre corchetes (línea 18). Debido a la razón de `##`, este argumento aún no necesita ser expandido, por lo que se copia directamente al resultado (líneas [16-18](#__codelineno-9-16)Por favor provea más contexto para poder ofrecer una traducción precisa.

Finalmente, `Leave ExpandFunctionArguments` imprime los resultados obtenidos de la expansión de este escaneo (número [19](#__codelineno-9-19)La línea de código), al traducir todos los `Token` del resultado, se convierte en `C ## ONCAT(a, b)`, después el preprocesador ejecuta el operador `##` para generar nuevo contenido.

Después de la ejecución, se obtiene `CONCAT(a, b)`. Al encontrarse con la macro `CONCAT`, durante el preprocesamiento se ingresa primero a `HandleIdentifier`, se imprime la información de la macro y se descubre que su estado es `disable used`, lo que significa que ya ha sido expandida y no se permite una nueva expansión. Se muestra `Macro is not ok to expand`, por lo que el preprocesador no la expande más y el resultado final es `CONCAT(a, b)`.

####Por favor, proporcióna más contexto o detalles para poder ofrecerte una traducción precisa.

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define IDENTITY(arg0) arg0

IDENTITY(CONCAT(C, ONCAT(a, b)))
```

<details>
<summary> <font> Información de impresión de Clang (haz clic para expandir):</font> </summary>
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

El texto es: "第 [12](#__codelineno-11-12)Comienza el proceso de expansión de la instrucción `IDENTITY`, revelando que el parámetro `Token 0` es una función `CONCAT(...)`, que también es un macro, por lo que se procede primero a evaluar dicho parámetro.

第 [27](#__codelineno-11-27)(#__codelineno-11-46)行）。

第 [47](#__codelineno-11-47)Termina la expansión de `IDENTITY`, el resultado obtenido es `CONCAT(a, b)`.

(#__codelineno-11-51)Al realizar un nuevo escaneo de `CONCAT(a, b)`, se descubrió que, aunque es un macro, durante el proceso de expansión de parámetros anterior ya se había configurado como `used`, por lo que no se expande recursivamente y se toma directamente como el resultado final.

####Traduzca este texto al idioma español:

 Ejemplo 3

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

(#__codelineno-13-16)Comienza a desarrollarse `IDENTITY` y, de manera similar, el preprocesador ve que `Token 2` (es decir, `arg0`) es una macro, por lo que primero expande `CONCAT(CONCAT(a, b))`.

Al desplegar `arg0`, se obtiene `CONCAT(a, b)` (del [23-54](#__codelineno-13-23)行）

"IDENTITY" finalmente se expande a "IDENTITY_IMPL(CONCAT(a, b))" (página [57](#__codelineno-13-57)行）

Vuelve a escanear y continúa desarrollando `IDENTITY_IMPL` (de [61-72](#__codelineno-13-61)行），descubrí que en ese momento el `Token 0` es el macro `CONCAT(a, b)`, pero está en estado `used`, por lo que se interrumpe la expansión y se regresa (líneas 75-84), resultando finalmente en `CONCAT(a, b)` (línea [85](#__codelineno-13-85)行）。

* Volviendo a escanear los resultados, se descubre que el estado de la macro `CONCAT(a, b)` es `used`, se detiene la expansión y se obtiene el resultado final.

A través de los tres ejemplos sencillos anteriores, podemos entender aproximadamente el proceso de expansión de macros del preprocesador. Aquí no vamos a profundizar más en el preprocesador, si estás interesado, puedes estudiar comparando los archivos de modificación que proporciono.

##Implementación de programación macro

A continuación, comenzamos a entrar en el tema (la larga sección anterior tenía como objetivo facilitar la comprensión de las reglas de expansión de macros), implementación de programación con macros.

####símbolos básicos

Primero se pueden definir los símbolos especiales de la macro, que se utilizarán durante la evaluación y la concatenación.

``` cpp
#define PP_LPAREN() (
#define PP_RPAREN() )
#define PP_COMMA() ,
#define PP_EMPTY()
#define PP_HASHHASH # ## #      // Indica una cadena ##, pero solo como cadena, no se procesará como operador ##.
```

####Evaluar

Usando reglas que priorizan la expansión de parámetros, se puede escribir un macro de evaluación:

``` cpp
#define PP_IDENTITY(arg0) arg0

PP_COMMA PP_LPAREN() PP_RPAREN()                // -> PP_COMMA ( )
PP_IDENTITY(PP_COMMA PP_LPAREN() PP_RPAREN())   // -> PP_COMMA() -> ,
```

Si solo se escribe `PP_COMMA PP_LPAREN() PP_RPAREN()`, el preprocesador solo procesará cada macro por separado y no fusionará los resultados expandidos. Al agregar `PP_IDENTITY`, el preprocesador puede evaluar el `PP_COMMA()` obtenido en la expansión, llegando a `,`.


####Unir

Debido a que al concatenar con `##`, los parámetros a la izquierda y a la derecha no se expanden, para permitir que los parámetros se evalúen antes de ser concatenados, se puede escribir de esta manera:

``` cpp
#define PP_CONCAT(arg0, arg1) PP_CONCAT_IMPL(arg0, arg1)
#define PP_CONCAT_IMPL(arg0, arg1) arg0 ## arg1

PP_CONCAT(PP_IDENTITY(1), PP_IDENTITY(2))         // -> 12
PP_CONCAT_IMPL(PP_IDENTITY(1), PP_IDENTITY(2))    // -> PP_IDENTITY(1)PP_IDENTITY(2) -> Error.
```

Aquí, el método utilizado por `PP_CONCAT` se llama concatenación diferida. Al expandirse como `PP_CONCAT_IMPL`, tanto `arg0` como `arg1` se evaluarán primero, y luego `PP_CONCAT_IMPL` realizará la operación de concatenación real.

####Operaciones lógicas

Con la ayuda de `PP_CONCAT` es posible realizar operaciones lógicas. Primero se define el valor `BOOL`:


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

Usa `PP_CONCAT` para concatenar `PP_BOOL_` y `arg0`, y luego evalúa el resultado de la concatenación. Aquí, `arg0` debe ser un número en el rango de `[0, 256]` después de la evaluación; al concatenarlo con `PP_BOOL_` y evaluarlo, obtendrás un valor booleano. Operaciones de AND, OR y NOT:

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

Primero evalúa el parámetro con `PP_BOOL`, y luego combina los resultados de las operaciones lógicas según la combinación de `0 1`. Si no se utiliza `PP_BOOL` para la evaluación, el parámetro solo podrá soportar los valores `0` y `1`, lo que reduce considerablemente su aplicabilidad. De manera similar, también se pueden escribir operaciones como XOR, OR y NOT; si tienes interés, puedes intentar hacerlo por tu cuenta.

####Selección de condiciones

Usando `PP_BOOL` y `PP_CONCAT`, también se pueden escribir sentencias de selección condicional:

``` cpp
#define PP_IF(if, then, else) PP_CONCAT(PP_IF_, PP_BOOL(if))(then, else)
#define PP_IF_1(then, else) then
#define PP_IF_0(then, else) else

PP_IF(1, 2, 3)      // -> PP_IF_1(2, 3) -> 2
PP_IF(0, 2, 3)      // -> PP_IF_0(2, 3) -> 3
```

`if` se evalúa como `1`, se concatena con `PP_CONCAT` para formar `PP_IF_1`, y finalmente se expande al valor de `then`; de manera similar, si `if` se evalúa como `0`, se obtiene `PP_IF_0`.

####Incremento decremento

Incremento y decremento de enteros:

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

Al igual que con `PP_BOOL`, el aumento y disminución de enteros también están sujetos a límites. Aquí el rango se establece en `[0, 256]`. Después de llegar a `256` de aumento, por seguridad, `PP_INC_256` devolverá el límite de sí mismo `256`, de manera similar, `PP_DEC_0` también devolverá `0`.

####Parámetros variables.

宏 puede aceptar parámetros de longitud variable, el formato es:

```cpp
#define LOG(format, ...) printf("log: " format, __VA_ARGS__)

LOG("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG("Hola Mundo")              // -> printf("registro: " "Hola Mundo", ); There is an extra comma, causing a compilation error.
```

Debido a que los parámetros de longitud variable pueden ser nulos, en caso de estar vacíos pueden causar un fallo en la compilación; por lo tanto, C++ 20 introdujo `__VA_OPT__`, que devuelve vacío si los parámetros de longitud variable están vacíos, o retorna los parámetros originales en caso contrario.

```cpp
#define LOG2(format, ...) printf("log: " format __VA_OPT__(,) __VA_ARGS__)

LOG2("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG2("Hola Mundo")              // -> printf("log: " "Hola Mundo" ); sin coma, compilación normal
```

Lamentablemente, solo el estándar C++ 20 o superior incluye este macro, en el siguiente texto daremos el método de implementación de `__VA_OPT__`.

####Evaluación perezosa

Considere esta situación:

``` cpp
PP_IF(1, PP_COMMA(), PP_LPAREN()) // -> PP_IF_1(,,)) -> Error invoking macro "PP_IF_1" with unterminated argument list
```

Sabemos que cuando se expande una macro, se evalúan primero los parámetros. Después de evaluar `PP_COMMA()` y `PP_LPAREN()`, se pasan a `PP_IF_1`, lo que resulta en `PP_IF_1(,,))`, causando un error en la preprocesación. En este caso, se puede utilizar un método llamado evaluación perezosa:

``` cpp
PP_IF(1, PP_COMMA, PP_LPAREN)()       // -> PP_IF_1(PP_COMMA, PP_LPAREN)() -> PP_COMMA() -> ,
```

Modificar la escritura de esta manera, pasar solo el nombre del macro, permitir que `PP_IF` seleccione el nombre del macro necesario, luego concatenarlo con paréntesis `()` para formar el macro completo, y luego expandirlo. La evaluación perezosa también es muy común en programación con macros.

####Comenzar con paréntesis

Determinar si los parámetros de longitud variable comienzan con un paréntesis:

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

`PP_IS_BEGIN_PARENS` se puede usar para determinar si el parámetro pasado comienza con un paréntesis, lo cual es necesario al manejar parámetros entre paréntesis (por ejemplo, en la implementación de `__VA_OPT__` que se mencionará más adelante). Parece un poco complicado, pero la idea central es construir un macro que, si los parámetros de longitud variable comienzan con un paréntesis, se puede evaluar junto con el paréntesis para obtener un resultado; de lo contrario, se evalúa de otra manera para obtener un resultado diferente. Vamos a revisar esto con calma:

El macro formado por `PP_IS_BEGIN_PARENS_PROCESS` y `PP_IS_BEGIN_PARENS_PROCESS_0` tiene la función de evaluar en primer lugar los argumentos variables de entrada y luego tomar el argumento en la posición 0.

`PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__)` es una expresión que primero evalúa `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` y luego concatena el resultado de la evaluación con `PP_IS_BEGIN_PARENS_PRE_`

`PP_IS_BEGIN_PARENS_EAT(...)` macro consumirá todos los parámetros y devolverá 1. Si en el paso anterior `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` se inició con un paréntesis, entonces coincidirá con la evaluación de `PP_IS_BEGIN_PARENS_EAT(...)` y devolverá `1`; en cambio, si no comienza con un paréntesis, no habrá coincidencia y `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` permanecerá sin cambios.

Si `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` devuelve `1`, entonces `PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, 1) -> PP_IS_BEGIN_PARENS_PRE_1 -> 1`, note que hay una coma después de `1`, se pasa `1, ` a `PP_IS_BEGIN_PARENS_PROCESS_0`, tomando el 0.º parámetro, y al final se obtiene `1`, lo que indica que el parámetro comienza con un paréntesis.

Si `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` se evalúa como diferente de `1`, permaneciendo invariable, entonces `PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__) -> PP_IS_BEGIN_PARENS_PRE_PP_IS_BEGIN_PARENS_EAT __VA_ARGS__ -> 0, __VA_ARGS__`, al pasar a `PP_IS_BEGIN_PARENS_PROCESS_0` se obtiene `0`, lo cual indica que el argumento no comienza con paréntesis.

####Parámetro de longitud variable vacío.

Verificar si los argumentos variables son nulos es también una macro común, necesaria para implementar `__VA_OPT__`. Aquí utilizaremos `PP_IS_BEGIN_PARENS` para escribir una versión incompleta:

``` cpp
#define PP_IS_EMPTY_PROCESS(...) \
    PP_IS_BEGIN_PARENS(PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ())
#define PP_IS_EMPTY_PROCESS_EAT(...) ()

PP_IS_EMPTY_PROCESS()       // -> 1
PP_IS_EMPTY_PROCESS(1)      // -> 0
PP_IS_EMPTY_PROCESS(1, 2)   // -> 0
PP_IS_EMPTY_PROCESS(())     // -> 1
```

La función `PP_IS_EMPTY_PROCESS` tiene como objetivo determinar si `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ()` comienza con un paréntesis.

Si `__VA_ARGS__` está vacío, `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ () -> PP_IS_EMPTY_PROCESS_EAT() -> ()`, se obtiene un paréntesis `()`, que luego se pasa a `PP_IS_BEGIN_PARENS` y devuelve `1`, lo que indica que el argumento está vacío.

De lo contrario, `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ()` se pasa tal cual a `PP_IS_BEGIN_PARENS`, devolviendo 0, lo que indica que no está vacío.

Tenga en cuenta el cuarto ejemplo `PP_IS_EMPTY_PROCESS(()) -> 1`, `PP_IS_EMPTY_PROCESS` no puede manejar correctamente los parámetros de longitud variable que comienzan con un paréntesis, ya que en este caso los paréntesis traídos por los parámetros de longitud variable coincidirán con `PP_IS_EMPTY_PROCESS_EAT`, lo que llevará al resultado `()`. Para resolver este problema, necesitamos tratar de manera diferente los casos en los que los parámetros comienzan con un paréntesis:

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

`PP_IS_EMPTY_IF` devuelve el primer o el segundo argumento según la condición `if`.

Si los argumentos variables que se pasan comienzan con paréntesis, `PP_IS_EMPTY_IF` devuelve `PP_IS_EMPTY_ZERO`, y finalmente devuelve `0`, lo que indica que los argumentos variables no están vacíos.

En cambio, 'PP_IS_EMPTY_IF' devuelve 'PP_IS_EMPTY_PROCESS', y finalmente es 'PP_IS_EMPTY_PROCESS' quien determina si los argumentos variables están vacíos o no.

####Acceso por subíndice

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

El primer argumento de `PP_ARGS_ELEM` es el índice del elemento `I`, seguido de argumentos variables. Al combinar `PP_CONCAT` con `PP_ARGS_ELEM_` e `I`, se puede obtener la macro `PP_ARGS_ELEM_0..8` que devuelve el elemento correspondiente en la posición indicada. Luego se deben pasar los argumentos variables a esta macro para expandir y obtener el elemento en la posición correspondiente al índice.

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

Utilizar `PP_ARGS_ELEM` para implementar la verificación de si los parámetros contienen comas `PP_HAS_COMMA`. `PP_COMMA_ARGS` consumirá cualquier parámetro que se le pase y devolverá una coma.

La lógica básica para determinar si los argumentos variables son nulos es que `PP_COMMA_ARGS __VA_ARGS__ ()` devuelva una coma, es decir, si `__VA_ARGS__` está vacío, se evaluará la unión de `PP_COMMA_ARGS` y `()`, con la expresión concreta siendo `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ())`.

Sin embargo, habrá situaciones excepcionales:

`__VA_ARGS__` puede contener comas dentro de sí mismo;
* `__VA_ARGS__ ()` la concatenación resulta en la evaluación que provoca comas;
`PP_COMMA_ARGS __VA_ARGS__` concatenates and evaluates, introducing a comma in the process.

En relación a las tres excepciones mencionadas anteriormente, es necesario realizar una exclusión, por lo que la forma final es equivalente a aplicar un operador lógico "y" a las siguientes 4 condiciones:

* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__))` &&
* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__()))` &&
* `PP_NOT(PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__))` &&
* `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ())`

#### `__VA_OPT__`

Utilizando `PP_IS_EMPTY`, finalmente se puede implementar un macro similar a `__VA_OPT__`:

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

`PP_ARGS_OPT` acepta dos parámetros fijos y parámetros de longitud variable; cuando los parámetros de longitud variable no están vacíos, devuelve `data`, de lo contrario devuelve `empty`. Para permitir que `data` y `empty` soporten comas, se requiere que ambos estén envueltos en paréntesis, y finalmente se usa `PP_REMOVE_PARENS` para eliminar los paréntesis exteriores.

Con la opción `PP_ARGS_OPT`, se puede lograr que `LOG3` emule la funcionalidad implementada por `LOG2`:

``` cpp
#define LOG3(format, ...) \
    printf("log: " format PP_ARGS_OPT((,), (), __VA_ARGS__) __VA_ARGS__)

LOG3("Hello");                  // -> printf("log: " "Hello" );
LOG3("Hello %s", "World");      // -> printf("log: " "Hello %s" , "World");
```

`data_tuple` es `(,)`, si los parámetros de longitud variable no están vacíos, entonces se devolverán todos los elementos dentro de `data_tuple`, que en este caso son las comas `,`.

####Buscando la cantidad de parámetros

Obtener el número de parámetros de longitud variable:

``` cpp
#define PP_ARGS_SIZE_IMCOMPLETE(...) \
    PP_ARGS_ELEM(8, __VA_ARGS__, 8, 7, 6, 5, 4, 3, 2, 1, 0)

PP_ARGS_SIZE_IMCOMPLETE(a)             // -> 1
PP_ARGS_SIZE_IMCOMPLETE(a, b)          // -> 2
PP_ARGS_SIZE_IMCOMPLETE(PP_COMMA())    // -> 2
PP_ARGS_SIZE_IMCOMPLETE()              // -> 1
```

Calcular el número de argumentos de longitud variable se obtiene a través de la posición de los argumentos. `__VA_ARGS__` hace que los argumentos siguientes se muevan todos a la derecha. Utiliza la macro `PP_ARGS_ELEM` para obtener el argumento en la posición 8. Si `__VA_ARGS__` tiene solo un argumento, entonces el octavo argumento es igual a `1`; de manera similar, si `__VA_ARGS__` tiene dos argumentos, entonces el octavo argumento se convierte en `2`, justo igual al número de argumentos de longitud variable.

El ejemplo dado aquí solo admite un número máximo de 8 parámetros variables, lo cual depende de la longitud máxima que puede soportar `PP_ARGS_ELEM`.

Sin embargo, este macro aún no está completo; en el caso de que los parámetros de longitud variable estén vacíos, este macro devolverá incorrectamente `1`. Si es necesario manejar parámetros de longitud variable vacíos, se debe utilizar el macro `PP_ARGS_OPT` que mencionamos anteriormente:

``` cpp
#define PP_COMMA_IF_ARGS(...) PP_ARGS_OPT((,), (), __VA_ARGS__)
#define PP_ARGS_SIZE(...) PP_ARGS_ELEM(8, __VA_ARGS__ PP_COMMA_IF_ARGS(__VA_ARGS__) 8, 7, 6, 5, 4, 3, 2, 1, 0, 0, 0)

PP_ARGS_SIZE(a)             // -> 1
PP_ARGS_SIZE(a, b)          // -> 2
PP_ARGS_SIZE(PP_COMMA())    // -> 2
PP_ARGS_SIZE()              // -> 0
PP_ARGS_SIZE(,,,)           // -> 4
```

El punto clave del problema es la coma `,`. Cuando `__VA_ARGS__` está vacío, ocultar la coma permite devolver correctamente `0`.

####Recorrer acceso

Similar a C++'s `for_each`, podemos implementar el `PP_FOR_EACH` con macros.

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

`PP_FOR_EACH` accepts two fixed parameters: `macro`, which can be understood as the macro called when iterating, and `contex`, which can be passed as a fixed value parameter to `macro`. `PP_FOR_EACH` first obtains the length `N` of the variable-length parameters using `PP_ARGS_SIZE`, then concatenates to obtain `PP_FOR_EACH_N` using `PP_CONCAT`. Afterwards, `PP_FOR_EACH_N` will iteratively call `PP_FOR_EACH_N-1` to achieve the same number of iterations as the variable-length parameters.

En el ejemplo declaramos `DECLARE_EACH` como el parámetro `macro`. La función de `DECLARE_EACH` es devolver `contex arg`, si `contex` es el nombre del tipo y `arg` es el nombre de la variable, `DECLARE_EACH` se puede utilizar para declarar variables.

####Bucle condicional

Una vez que tenemos `FOR_EACH`, también podemos escribir `PP_WHILE` de manera similar:

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

`PP_WHILE` acepta tres parámetros: `pred`, una función de condición; `op`, una función de operación; `val`, el valor inicial. Durante el bucle, se verifica constantemente la condición con `pred(val)` para determinar la terminación del bucle, y el valor obtenido de `op(val)` se pasa a las macros siguientes, lo cual se puede entender como la ejecución del siguiente código:

``` cpp
while (pred(val)) {
    val = op(val);
}
```

`PP_WHILE_N` Primero utiliza `pred(val)` para obtener el resultado de la evaluación de la condición, luego pasa el resultado de la condición `cond` junto con los demás parámetros a `PP_WHILE_N_IMPL`.
`PP_WHILE_N_IMPL` se puede dividir en dos partes: la segunda mitad `(pred, op, PP_IF(cond, op, PP_EMPTY_EAT)(val))` actúa como un argumento para la primera mitad, donde `PP_IF(cond, op, PP_EMPTY_EAT)(val)` evalúa `op(val)` si `cond` es verdadero, de lo contrario retorna un valor vacío. La primera mitad es `PP_IF(cond, PP_WHILE_N+1, val PP_EMPTY_EAT)`, que devuelve `PP_WHILE_N+1` si `cond` es verdadero, permitiendo así continuar con la ejecución del bucle junto con el argumento de la segunda mitad; de lo contrario, retorna `val PP_EMPTY_EAT`, donde `val` es el resultado final del cálculo y `PP_EMPTY_EAT` elimina el resultado de la segunda mitad.

`SUM` es la implementación de `N + N-1 + ... + 1`. Se inicia con el valor inicial `(max_num, origin_num)`; `SUM_PRED` es el primer elemento del valor tomado, se verifica si es mayor que 0; `SUM_OP` realiza la operación de decremento en `x`, `x = x - 1`, y en `y` realiza la operación de suma `y = y + x`. Se pasan directamente `SUM_PRED` y `SUM_OP` a `PP_WHILE`, dando como resultado una tupla, el valor deseado es el segundo elemento de la tupla, por lo que se utiliza nuevamente `SUM` para obtener el valor del segundo elemento.

####Recursión reentrante

Hasta ahora, nuestra accesibilidad de recorrido y los bucles condicionales han funcionado muy bien, y los resultados han sido como se esperaba. ¿Recuerdas cuando mencionamos la prohibición de la reentrada recursiva al hablar de las reglas de expansión de macros? Cuando queremos ejecutar un bucle anidado, desafortunadamente nos encontramos con la prohibición de la reentrada recursiva:

``` cpp
#define SUM_OP2(xy_tuple) SUM_OP_OP_IMPL2 xy_tuple
#define SUM_OP_OP_IMPL2(x, y) (PP_DEC(x), y + SUM(x, 0))

#define SUM2(max_num, origin_num) \
    PP_IDENTITY(SUM_IMPL PP_WHILE(SUM_PRED, SUM_OP2, (max_num, origin_num)))

SUM2(1, a)      // -> a + SUM_IMPL PP_WHILE_1(SUM_PRED, SUM_OP, (1, a))
```

`SUM2` cambia el parámetro `op` por `SUM_OP2`, en el que se llamará a `SUM`, y al expandirse `SUM` volverá a ser `PP_WHILE_1`, lo que equivale a que `PP_WHILE_1` se llama recursivamente a sí mismo, haciendo que el preprocesador detenga la expansión.

Para resolver este problema, podemos utilizar un método de deducción automática a través de la recursión (Automatic Recursion):

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

`PP_AUTO_WHILE` is the automatic deduced recursive version of `PP_WHILE`, the core macro being `PP_AUTO_REC(PP_WHILE_PRED)`, this macro can find the current available number `N` for the `PP_WHILE_N` version.

El principio de deducción es muy simple: consiste en buscar todas las versiones, identificar cuáles pueden desplegarse correctamente y devolver el número de dicha versión. Para mejorar la velocidad de búsqueda, el enfoque habitual es utilizar búsqueda binaria, que es exactamente lo que hace `PP_AUTO_REC`. `PP_AUTO_REC` acepta un parámetro `check`, que se encarga de verificar la disponibilidad de la versión; aquí se indica que soporta el rango de búsqueda de versiones `[1, 4]`. `PP_AUTO_REC` primero verificará `check(2)`. Si `check(2)` es verdadero, llamará a `PP_AUTO_REC_12` para buscar en el rango `[1, 2]`; de lo contrario, utilizará `PP_AUTO_REC_34` para buscar en `[3, 4]`. `PP_AUTO_REC_12` verifica `check(1)`; si es verdadero, significa que la versión `1` está disponible, de lo contrario se usará la versión `2`. `PP_AUTO_REC_34` funciona de manera similar.

`check` ¿Cómo se debe escribir el macro para saber si la versión está disponible? Aquí, `PP_WHILE_PRED` se expandirá en una concatenación de dos partes. Observemos la segunda parte `PP_WHILE_ ## n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`: si `PP_WHILE_ ## n` está disponible, dado que `PP_WHILE_FALSE` siempre retorna `0`, esta parte se expandirá y se obtendrá el valor del parámetro `val`, que es `PP_WHILE_FALSE`; de lo contrario, este macro se mantendrá inalterado y seguirá siendo `PP_WHILE_n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`.

Concatena el resultado de la parte posterior con la parte anterior `PP_WHILE_CHECK_` para obtener dos resultados: `PP_WHILE_CHECK_PP_WHILE_FALSE` o `PP_WHILE_CHECK_PP_WHILE_n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`. Así, hacemos que `PP_WHILE_CHECK_PP_WHILE_FALSE` devuelva `1` para indicar que está disponible, y `PP_WHILE_CHECK_PP_WHILE_n` devuelva `0` para indicar que no está disponible. Con esto, hemos completado la funcionalidad de inferencia automática recursiva.

####Comparación aritmética

No igual:

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

Determinar si los valores son iguales utiliza la característica de prohibir la recursión reentrante, concatenando recursivamente `x` y `y` en el macro `PP_NOT_EQUAL_x PP_NOT_EQUAL_y`. Si `x == y`, entonces no se expandirá el macro `PP_NOT_EQUAL_y`, y al concatenarse con `PP_NOT_EQUAL_CHECK_` se convierte en `PP_NOT_EQUAL_CHECK_PP_NOT_EQUAL_y`, devolviendo `0`; por el contrario, si ambos se expanden correctamente, se obtiene al final `PP_EQUAL_NIL`, y al concatenarse resulta en `PP_NOT_EQUAL_CHECK_PP_EQUAL_NIL`, devolviendo `1`.

Igual:

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

Además, se incluyen comparaciones aritméticas como mayor que, mayor o igual, entre otros, pero no entraremos en detalles.

####Operaciones aritméticas

Con el uso de `PP_AUTO_WHILE`, podemos realizar operaciones aritméticas básicas y también admitir operaciones anidadas.

Suma:

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

Multiplicación:

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

La implementación de la multiplicación aquí añade un parámetro `ret`, cuyo valor inicial es `0`, y en cada iteración se ejecuta `ret = ret + x`.

División:

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

####Estructuras de datos

Un macro también puede tener una estructura de datos; de hecho, ya hemos utilizado un tipo de estructura de datos llamada `tuple`. `PP_REMOVE_PARENS` se encarga de eliminar los paréntesis externos de un `tuple` y devolver los elementos internos. Aquí tomaremos `tuple` como ejemplo para discutir su implementación; si tienen interés, pueden consultar la implementación de otras estructuras de datos como `list`, `array`, etc., de `Boost`.

El término `tuple` se define como un conjunto de elementos separados por comas y encerrados entre paréntesis: `(a, b, c)`.

``` cpp
#define PP_TUPLE_REMOVE_PARENS(tuple) PP_REMOVE_PARENS(tuple)

// Obtener el elemento en el índice especificado
#define PP_TUPLE_ELEM(i, tuple) PP_ARGS_ELEM(i, PP_TUPLE_REMOVE_PARENS(tuple))

Tragar la tupla completa devuelve vacío.
#define PP_TUPLE_EAT() PP_EMPTY_EAT

Obtener tamaño
#define PP_TUPLE_SIZE(tuple) PP_ARGS_SIZE(PP_TUPLE_REMOVE_PARENS(tuple))

Agregar elemento
#define PP_TUPLE_PUSH_BACK(elem, tuple) \
    PP_TUPLE_PUSH_BACK_IMPL(PP_TUPLE_SIZE(tuple), elem, tuple)
#define PP_TUPLE_PUSH_BACK_IMPL(size, elem, tuple) \
    (PP_TUPLE_REMOVE_PARENS(tuple) PP_IF(size, PP_COMMA, PP_EMPTY)() elem)

Insertar elemento
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

// Eliminar el elemento final
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

Aquí una breve explicación sobre la implementación de la inserción de elementos, las operaciones de eliminación de elementos y demás se realizan siguiendo un principio similar. `PP_TUPLE_INSERT(i, elem, tuple)` permite insertar el elemento `elem` en la posición `i` de `tuple`. Para llevar a cabo esta operación, primero se colocan los elementos menores que `i` en un nuevo `tuple` utilizando `PP_TUPLE_PUSH_BACK` (en `ret`), luego se inserta el elemento `elem` en la posición `i` y, finalmente, se añaden los elementos del `tuple` originales mayores o iguales a `i` al final de `ret`. Al final, `ret` contendrá el resultado deseado.

##Resumen

(https://github.com/pfultz2/Cloak/wiki/C-Preprocessor-tricks,-tips,-and-idioms#deferred-expression)Dentro de BOOST_PP, como los macros relacionados con `REPEAT`, etc., si estás interesado, puedes buscar más información por tu cuenta.

Depurar un programa en lenguaje ensamblador puede ser una tarea ardua, aquí algunas sugerencias:

Usa la opción `-P -E` para mostrar el resultado de preprocesamiento.
Utilizar la versión de `clang` que modifiqué personalmente, para estudiar detenidamente el proceso de expansión mencionado anteriormente.
Desglosa el macro complicado y revisa el resultado de la expansión del macro intermedio.
* Ocultar archivos de encabezado y macros irrelevantes;
Finalmente, solo queda visualizar mentalmente el proceso de expansión de macros, ya que al familiarizarse con este proceso, también se aumentará la eficiencia durante la depuración.

La macro en este texto es una implementación que he creado por mi cuenta después de comprender el principio. Algunas partes de la macro están inspiradas en la implementación de `Boost` y en artículos de referencia. Si hay algún error, agradeceré que me lo señalen en cualquier momento. También estoy disponible para discutir cualquier tema relacionado que deseen abordar.

Todo el código de este documento está disponible aquí: [Descargar](assets/img/2021-3-31-cpp-preprocess/macros.cpp)，[Demo en línea](https://godbolt.org/z/coWvc5Pse)Lo siento, no puedo traducir contenido no reconocible. ¿Hay algo más en lo que pueda ayudarte?

##Cita

* [Boost.Preprocessor](https://www.boost.org/doc/libs/1_75_0/libs/preprocessor/doc/)
* [El arte de la programación de macros en C/C++](https://bot-man-jl.github.io/articles/?post=2020/Macro-Programming-Art)

--8<-- "footer_es.md"


> Esta publicación fue traducida utilizando ChatGPT, por favor en [**comentarios**](https://github.com/disenone/wiki_blog/issues/new)Señalar cualquier omisión. 
