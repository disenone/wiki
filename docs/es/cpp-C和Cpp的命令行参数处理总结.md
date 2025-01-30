---
layout: post
title: Resumen del manejo de argumentos de línea de comandos en C/C++
categories:
- c++
catalog: true
tags:
- dev
description: 前一阵子翻 Linux 内核代码的时候看到了内核对模块参数 (moduleparam) 的处理，觉得挺精妙，让我不禁想研究下 C 下的命令行参数要怎样更好地处理。
figures:
- assets/post_assets/2016-11-19-aparsing/aparsing.png
---

<meta property="og:title" content="C/C++ 的命令行参数处理总结" />

![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/gcc-4.9-blue.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/clang-3.7-birghtgreen.svg){:style="display: inline-block"}

![](assets/img/2016-11-19-aparsing/aparsing.png)

Hace un tiempo, al revisar el código del núcleo de Linux, vi cómo se manejan los parámetros de módulo (moduleparam) y me pareció bastante ingenioso. No pude evitar pensar en cómo manejar mejor los parámetros de línea de comandos en C. El código utilizado en este artículo está aquí [aparsing](https://github.com/disenone/aparsing)El código es compatible con Windows, Linux y Mac OS X para compilar y ejecutar. Las instrucciones detalladas de compilación se encuentran en el archivo README.md.

## getenv

La biblioteca estándar nos proporciona una función `getenv`, que literalmente se utiliza para obtener variables de entorno. Así que, siempre que configuremos previamente las variables de entorno necesarias, podemos sacarlas dentro del programa y, de este modo, pasarlas indirectamente como parámetros al programa. Veamos el siguiente [código](https://github.com/disenone/aparsing/blob/master/getenv/getenv_test.c)Lo siento, no hay contenido para traducir. 

``` cpp linenums="1"
#include <stdlib.h>
#include <stdio.h>

//char *getenv( const char *name );
//GETENV_ADD=abc GETENV_NUM=2 ./getenv_test 

int main (int argc, char **argv)
{
    char *add, *num;
    if((add = getenv("GETENV_ADD")))
        printf("GETENV_ADD = %s\n", add);
    else
        printf("GETENV_ADD not found\n");

    if((num = getenv("GETENV_NUM")))
    {
        int numi = atoi(num);
        printf("GETENV_NUM = %d\n", numi);
    }
    else
        printf("GETENV_NUM not found\n");
}
```

La declaración de la función `getenv` se encuentra en la referencia [4](#__codelineno-0-5)Toma como entrada el nombre de la variable que desea obtener y devuelve el valor de esa variable; si la variable no se encuentra, devuelve 0. [10](#__codelineno-0-10)和 [15](#__codelineno-0-15)La acción consiste en obtener los valores de dos variables de entorno, y si las variables son válidas, se imprimen sus valores. Es importante notar que `getenv` devuelve todos los valores como cadenas de texto, lo que requiere que el usuario convierta manualmente los tipos numéricos, por lo que su uso no es del todo conveniente. Compilar y ejecutar:

Bajo Windows:

``` bat
set GETENV_ADD=abc & set GETENV_NUM=1 & .\getenv_test.exe
```

Linux 下：Linux operating system:

``` shell
GETENV_ADD=abc GETENV_NUM=2 ./getenv_test 
```

Documentos:

```
GETENV_ADD = abc
GETENV_NUM = 2
```

## getopt

Linux nos proporciona un conjunto de funciones `getopt, getopt_long, getopt_long_only` para manejar los argumentos pasados a través de la línea de comandos. Las declaraciones de estas tres funciones son:

```cpp linenums="1"
extern char *optarg;
extern int optind, opterr, optopt;

int getopt(int argc, char * const argv[],
                  const char *optstring);

int getopt_long(int argc, char * const argv[],
            const char *optstring,
            const struct option *longopts, int *longindex);

int getopt_long_only(int argc, char * const argv[],
            const char *optstring,
            const struct option *longopts, int *longindex);
```

`getopt` solo puede manejar parámetros cortos (es decir, parámetros de un solo carácter), mientras que `getopt_long` y `getopt_long_only` pueden manejar parámetros largos. Para una explicación detallada de las funciones, puedes consultar el manual en Linux. A continuación, explicaremos el uso de `getopt` y `getopt_long` a través de ejemplos.

Es importante tener en cuenta que estas funciones no están disponibles en Windows, así que busqué una versión del código fuente que pueda compilar en Windows y realicé algunas modificaciones menores. Puedes encontrar todo el código [aquí](https://github.com/disenone/aparsing/tree/master/getopt)Lo siento, no hay texto para traducir. ¿Puedo ayudarte con algo más?

```cpp linenums="1"
// test getopt

#include <getopt.h>
#include <stdio.h>
#include <string.h>

static struct option long_options[] =
{
    {"add", required_argument, 0, 'a'},
    {"append", no_argument, 0, 0},
    {"delete", required_argument, 0, 0},
    {"verbose", optional_argument, 0, 0},
    {"create", no_argument, 0, 0},
    {"file", required_argument, 0, 0},
    {"help", no_argument, 0, 0},
    {0, 0, 0, 0}
};

static char simple_options[] = "a:bc::d:0123456789";

int main (int argc, char **argv)
{

    int c;
    int digit_optind = 0;

    while (1)
    {
        int this_option_optind = optind ? optind : 1;
        int longindex = -1;

        c = getopt_long(argc, argv, simple_options, long_options, &longindex);
        if (c == -1)
        break;

        switch (c)
        {
            // long option
            case 0:
                   printf("option %s", long_options[longindex].name);
                   if (optarg)
                       printf(" with arg %s", optarg);
                   printf("\n");
                   break;

                break;

            case '0':
            case '1':
            case '2':
            case '3':
            case '4':
            case '5':
            case '6':
            case '7':
            case '8':
            case '9':
                if(digit_optind != 0 && digit_optind != this_option_optind)
                    printf("digits occur in two different argv-elements.\n");

                digit_optind = this_option_optind;
                printf("option %c\n", c);
                break;

            case 'a':
                printf("option a with value '%s'\n", optarg);
                break;

            case 'b':
                printf("option b\n");
                break;

            case 'c':
                if(optarg)
                    printf("option c with value '%s'\n", optarg);
                else
                    printf("option c\n");
                break;

            case '?':
                break;

            default:
                printf("?? getopt returned character code 0%o ??\n", c);
        } // switch
    } // while

    if (optind < argc)
    {
        printf("non-option ARGV-elements: ");
        while (optind < argc)
        printf("%s ", argv[optind++]);
        printf("\n");
    }

    return 0;
}

```

Vamos a analizar en detalle el uso de `getopt_long`. Los tres primeros parámetros de `getopt_long` son los mismos que los de `getopt`, que son: el número de parámetros de la línea de comandos `argc`, el arreglo de parámetros de la línea de comandos `argv`, y la forma específica de los parámetros cortos `optstring`. El formato de `optstring` consiste en caracteres de parámetros cortos, donde un dos puntos `:` indica que lleva parámetro, y dos puntos `::` indican que el parámetro es opcional. Por ejemplo, en la línea 19, se declara la forma de los parámetros cortos: el parámetro `b` no lleva parámetros adicionales, el parámetro `a` lleva un parámetro adicional, y `c` lleva un parámetro opcional.

Los dos últimos parámetros de `getopt_long` se utilizan para gestionar los argumentos largos, siendo la estructura de `option`:

```c
struct option {
const char *name;       // Nombre de parámetro largo
    int         has_arg;    // Si se requieren parámetros adicionales
int        *bandera;       // Establecer cómo devolver el resultado de la llamada a la función
    int         val;        // Valor devuelto
};
```
Aunque se llame "long parameter", `name` aún puede ser un solo carácter.

El `has_arg` puede establecerse como `no_argument, required_argument, optional_argument`, que respectivamente indican sin argumento, con argumento, con argumento opcional.

`flag` y `val` se utilizan en conjunto; si `flag = NULL`, `getopt_long` devolverá directamente `val`. De lo contrario, si `flag` es un puntero válido, `getopt_long` realizará una operación similar a `*flag = val`, estableciendo el valor de la variable a la que apunta `flag` como el valor de `val`.

Si `getopt_long` encuentra un parámetro corto coincidente, devolverá el valor de carácter de ese parámetro corto; si encuentra un parámetro largo coincidente, devolverá `val` (si `flag = NULL`) o devolverá `0` (si `flag != NULL; *flag = val;`); si se encuentra un carácter que no es un parámetro, devolverá `?`; si se han procesado todos los parámetros, devolverá `-1`.

Utilizando las características del valor de retorno, podemos lograr un efecto en el que los parámetros largos y cortos tienen el mismo significado. Por ejemplo, en el primer parámetro `add` de `long_options`, si el valor `val` se establece como el carácter del parámetro corto `'a'`, entonces al evaluar el retorno, `--add` y `-a` entrarán en la misma rama de procesamiento y se tratarán como significados equivalentes.

La última pieza del rompecabezas es el uso de `optind` y `optarg`. `optind` indica la posición del siguiente parámetro a procesar en `argv`, mientras que `optarg` apunta a la cadena del argumento adicional.

Compilar y ejecutar el código:

```
$ .\getopt_test -a 1 -b -c4 --add 2 --verbose --verbose=3 -123 -e --e
option a with value '1'
option b
option c with value '4'
option a with value '2'
option verbose
option verbose with arg 3
option 1
option 2
option 3
.\getopt_test: invalid option -- e
.\getopt_test: unrecognized option `--e'

```

El significado de `-a` y `--add` es el mismo; los parámetros opcionales de los parámetros cortos se colocan directamente después, por ejemplo `-c4`, mientras que los parámetros opcionales de los parámetros largos deben tener un signo de igual, por ejemplo `--verbose=3`.

## mobuleparam

Vale, finalmente llegamos al método que inició este artículo. El núcleo de Linux utiliza un enfoque muy ingenioso para pasar parámetros a los módulos del núcleo, y ese enfoque es 'moduleparam'. Aquí explicaré brevemente cómo funciona 'moduleparam' en el núcleo de Linux, pero para obtener una explicación más detallada, recomendamos revisar el código. Aunque me he inspirado en algunos métodos de manejo de 'moduleparam', hay algunas diferencias con respecto al 'moduleparam' del núcleo de Linux. Para distinguirlos, voy a llamar a mi método 'small moduleparam', mientras que el del núcleo de Linux seguirá denominándose 'moduleparam'.

Primero, echemos un vistazo al uso de `moduleparam`, declarado dentro del módulo:

```c
int enable_debug = 0;
module_param(enable_debug, int, 0);
```

Luego de cargar los módulos, ingresar los parámetros:

```shell
$ insmod mod enable_debug=1
```

La variable `enable_debug` se ha configurado correctamente como `1`, lo cual simplifica su uso. Requiere muy pocas líneas de código adicionales, lo que permite escribir un código conciso y elegante. No es necesario recurrir a bucles de control extensos como en los casos de `getenv` y `getopt`, además proporciona conversión de tipos incorporada. Por lo tanto, considero que sería muy útil utilizar este enfoque para manejar los argumentos de la línea de comandos.

A continuación, veamos la implementación central de `moduleparam`:

```cpp linenums="1"
struct kernel_param {
Por favor, traduzca el texto al español:

	const char *name;           // Variable name
uint16_t perm;                   // permisos de acceso a la variable
	u16 flags;                  // Variable de tipo bool
param_set_fn set;           // str -> Variable value
	param_get_fn get;           // valor de la variable -> str
	union {
void *arg;              // Pointer variable
		const struct kparam_string *str;
		const struct kparam_array *arr;
	};
};

#define __module_param_call(prefix, name, set, get, arg, isbool, perm)	\
	/* Default value instead of permissions? */			\
	static int __param_perm_check_##name __attribute__((unused)) =	\
	BUILD_BUG_ON_ZERO((perm) < 0 || (perm) > 0777 || ((perm) & 2))	\
	+ BUILD_BUG_ON_ZERO(sizeof(""prefix) > MAX_PARAM_PREFIX_LEN);	\
	static const char __param_str_##name[] = prefix #name;		\
	static struct kernel_param __moduleparam_const __param_##name	\
	__used								\
        __attribute__ ((unused,__section__ ("__param"),aligned(sizeof(void *)))) \
	= { __param_str_##name, perm, isbool ? KPARAM_ISBOOL : 0,	\
	    set, get, { arg } }

#define module_param_call(name, set, get, arg, perm)			      \
	__module_param_call(MODULE_PARAM_PREFIX,			      \
			    name, set, get, arg,			      \
			    __same_type(*(arg), bool), perm)

#define module_param_named(name, value, type, perm)			   \
	param_check_##type(name, &(value));				   \
	module_param_call(name, param_set_##type, param_get_##type, &value, perm); \
	__MODULE_PARM_TYPE(name, #type)

#define module_param(name, type, perm)				\
	module_param_named(name, name, type, perm)

```

`module_param` es un macro que en realidad crea una estructura `kernel_param` que puede reflejarse en la variable proporcionada. Esta estructura almacena suficiente información para acceder y configurar la variable, es decir, en las líneas 20-24, y coloca la estructura en una sección llamada `__param` (`__section__ ("__param")`). Una vez que la estructura está bien definida, el núcleo, al cargar el módulo, determina la ubicación de la sección `__param` del archivo elf y la cantidad de estructuras, y luego, según el nombre y `param_set_fn`, configura el valor de cada parámetro. La forma de encontrar la sección con un nombre específico es dependiente de la plataforma; la implementación en el núcleo de Linux se basa en el procesamiento de archivos elf. Linux proporciona el comando `readelf` para ver la información de los archivos elf, y aquellos interesados pueden consultar la información de ayuda de `readelf`.

En lo anterior se mencionó que el enfoque del núcleo de Linux es específico de la plataforma, mientras que yo busco un método que sea independiente de la plataforma para manejar parámetros. Por lo tanto, debemos modificar un poco el enfoque original de `moduleparam`, eliminando la declaración `__section__ ("__param")`, ya que no queremos complicarnos leyendo la `section` de un archivo elf. Primero echemos un vistazo al uso modificado:

```cpp linenums="1"
#include "moduleparam.h"
#include <stdio.h>

static int test = 0;
static bool btest = 0;
static unsigned int latest_num = 0;
static long latest[10] = {0};
static char strtest[20] = "\0";

void usage()
{
    char *msg = "usage: moduleparam_test [test=int] [btest[=bool]] [latest=int array] [strtest=string]\n";
    printf(msg);
}

int unknown_handler(char *param, char *val)
{
    printf("find unknown param: %s\n", param);
    return 0;
}

int main (int argc, char **argv)
{
    init_module_param(4);
    module_param(test, int);
    module_param_bool(btest);
    module_param_array(latest, long, &latest_num);
    module_param_string(strtest, strtest, sizeof(strtest));

    int ret = parse_params(argc, argv, unknown_handler);

    if(ret != 0)
    {
        usage();
        return 0;
    }

    char buf[1024];
    for(int i=0; i < MODULE_INIT_VARIABLE_NUM; ++i)
    {
        MODULE_INIT_VARIABLE[i].get(buf, &MODULE_INIT_VARIABLE[i]);
        printf("%s = %s\n", MODULE_INIT_VARIABLE[i].name, buf);
    }
    return 0;
}

```

Entonces, para preservar cada estructura de reflexión, agregué un macro `init_module_param(num)` para declarar el espacio de almacenamiento de la estructura, donde `num` es el número de parámetros. Si el número real de parámetros declarados supera `num`, el programa activará un error de aserción. La declaración de `module_param` es ligeramente diferente a la original, eliminando el último parámetro que representa el permiso de acceso, sin control de permisos. Además, se agregó el macro `module_param_bool` para manejar variables tipo `bool`, algo que no es necesario en las versiones de Linux, ya que utiliza la función integrada de gcc `__builtin_types_compatible_p` para determinar el tipo de variable. Lamentablemente, MSVC no tiene esta función, por lo que tuve que quitar esta funcionalidad y agregar un macro. `module_param_array` y `module_param_string` son para el tratamiento de matrices y cadenas, funcionalidades que ya estaban presentes en la versión original.

Una vez declarados los parámetros, es hora de manejar los parámetros entrantes. Usa la macro `parse_params`, con `argc, argv` como argumentos. El tercer parámetro es un puntero a una función de callback para manejar los parámetros desconocidos. Puedes pasar `NULL` para interrumpir el procesamiento de argumentos y devolver un código de error.

Compilar y ejecutar el código:

```
.\moduleparam_test.exe error=0 test=101 btest=1 latest=1,2,3 strtest=\"Hello World!\"
Parsing ARGS: error=0 test=101 btest=1 latest=1,2,3 strtest="Hello World!"
find unknown param: error
test = 101
btest = Y
latest = 1,2,3
strtest = Hello World!
```

Se puede ver que los números, arrays y cadenas se pueden leer y convertir de forma correcta. Si se encuentra un parámetro que no se puede convertir, se devolverá un código de error y se imprimirá información relacionada. Podemos agregar unas pocas líneas de código de manera sencilla para completar la lectura y el procesamiento de parámetros, lo que resulta muy elegante. Para una implementación más detallada, se puede consultar el código [aquí](https://github.com/disenone/aparsing)。

##Resumen

Esta vez hemos hecho un resumen de tres métodos para manejar los argumentos de la línea de comandos en C/C++, que son `getenv`, `getopt` y `moduleparam`. Cada método tiene sus propias características, por lo que en el futuro se puede elegir el método adecuado según las necesidades reales.

La función `getenv` está soportada de forma nativa en múltiples plataformas y se puede utilizar directamente, pero es bastante primitiva y utiliza variables de entorno, lo que puede contaminar el entorno. Antes de cada uso, es mejor limpiar variables de entorno innecesarias para evitar que la configuración anterior se quede y cause contaminación.
`getopt` is natively supported on the Linux platform, but not on Windows, so it requires including implemented code to be used across platforms. The parameter passing conforms to the command-line parameter standard on Linux, supports optional parameters, but it is a bit cumbersome to use. Usually, it requires looping and conditional statements to handle different parameters and is not user-friendly for numerical data types.
El `moduleparam` es una herramienta de procesamiento de parámetros de línea de comandos inspirada en la implementación de `moduleparam` del kernel de Linux. Es fácil de usar, soporta diferentes plataformas y puede convertir fácilmente parámetros de distintos tipos. La desventaja es que requiere una variable correspondiente para cada parámetro.

--8<-- "footer_es.md"


> Este mensaje ha sido traducido utilizando ChatGPT. Por favor, comparte tus [**comentarios**](https://github.com/disenone/wiki_blog/issues/new)Señale cualquier omisión. 
