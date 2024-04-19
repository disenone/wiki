---
layout: post
title: Resumen del manejo de los argumentos de línea de comandos en C/C++
categories:
- c++
catalog: true
tags:
- dev
description: Hace un tiempo, mientras estaba revisando el código fuente del kernel
  de Linux, me encontré con el manejo de los parámetros de módulos (moduleparam) y
  me pareció bastante ingenioso. Esto me ha llevado a querer investigar cómo se pueden
  manejar de manera más eficiente los argumentos de línea de comandos en C.
figures:
- assets/post_assets/2016-11-19-aparsing/aparsing.png
---

<meta property="og:title" content="C/C++ 的命令行参数处理总结" />

![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/gcc-4.9-blue.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/clang-3.7-birghtgreen.svg){:style="display: inline-block"}

![](assets/img/2016-11-19-aparsing/aparsing.png)

En el pasado, cuando estaba revisando el código del kernel de Linux, me encontré con el manejo de los parámetros del módulo (moduleparam), y me pareció muy ingenioso. Esto me llevó a reflexionar sobre cómo se podrían manejar de manera más efectiva los argumentos de línea de comandos en C. Todo el código utilizado en este artículo se encuentra aquí [aparsing](https://github.com/disenone/aparsing). El código es compatible con la compilación y ejecución en Windows, Linux y Mac OS X. Las instrucciones detalladas de compilación se encuentran en el archivo README.md.

## getenv

La biblioteca estándar nos proporciona una función `getenv`, que literalmente se utiliza para obtener las variables de entorno. Entonces, siempre y cuando hayamos configurado previamente las variables de entorno necesarias, podemos obtenerlas en el programa y, de esta manera, pasar los parámetros indirectamente al programa. Echemos un vistazo al siguiente [código](https://github.com/disenone/aparsing/blob/master/getenv/getenv_test.c):

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

La función `getenv` se declara en el número [4](#__codelineno-0-5)La función `getVarValue()` toma como argumento el nombre de la variable que se desea obtener y devuelve el valor de dicha variable. Si la variable no se encuentra, devuelve 0. [10](#__codelineno-0-10)(#__codelineno-0-15)El código que tienes aquí se encarga de obtener los valores de dos variables de entorno y, si las variables son válidas, imprime sus valores. Hay que tener en cuenta que `getenv` siempre devuelve una cadena de texto, por lo que el usuario debe convertir manualmente el valor a un tipo numérico si es necesario. Esto hace que el uso de esta función no sea especialmente conveniente. Para compilar y ejecutar este código, debes

Windows abajo:

``` bat
set GETENV_ADD=abc & set GETENV_NUM=1 & .\getenv_test.exe
```

Linux bajo el sistema operativo:

``` shell
GETENV_ADD=abc GETENV_NUM=2 ./getenv_test 
```

Salida:

```
GETENV_ADD = abc
GETENV_NUM = 2
```

## getopt

Linux nos proporciona un conjunto de funciones `getopt, getopt_long, getopt_long_only` para manejar argumentos pasados por la línea de comandos. Las declaraciones de estas tres funciones son respectivamente:

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

El comando `getopt` solo puede manejar argumentos cortos (es decir, argumentos de un solo carácter), mientras que `getopt_long` y `getopt_long_only` pueden manejar argumentos largos. Para obtener una explicación más detallada de las funciones, puedes consultar el manual de Linux. A continuación, te mostraremos ejemplos de cómo utilizar `getopt` y `getopt_long`.

Se debe tener en cuenta que estas funciones no están disponibles en Windows, así que busqué el código fuente que se puede compilar en Windows y hice algunos pequeños cambios. El código está disponible [aquí](https://github.com/disenone/aparsing/tree/master/getopt).

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

Vamos a analizar en detalle el uso de `getopt_long`.  Los primeros tres parámetros de `getopt_long` son iguales a los de `getopt`: el número de argumentos de línea de comandos `argc`, el array de argumentos de línea de comandos `argv`, y la especificación de formato de los argumentos cortos `optstring`. El formato de `optstring` consiste en caracteres que representan cada uno de los argumentos cortos, seguidos de dos puntos `:` para indicar que llevan un argumento adicional, o dos puntos dobles `::` para indicar que el argumento es opcional. Por ejemplo, en la línea 19 se declara la forma de los argumentos cortos: el argumento `b` no lleva argumento adicional, el argumento `a` sí lo lleva, y el argumento `c` lleva un argumento opcional.

`getopt_long` es una función utilizada para procesar argumentos largos en la línea de comandos. Los dos últimos parámetros se utilizan para este propósito, donde la estructura del parámetro `option` es la siguiente:

```c
struct option {
    const char *name;       // Nombre de parámetro largo
    int         has_arg;    // ¿Tiene argumento adicional?
    `int *flag; // Define cómo se devuelve el resultado de la llamada a la función`
    int         val;        // Valor devuelto
};
```
Aunque se diga que es un parámetro largo, `name` aún puede tener una longitud de un solo carácter.

La opción `has_arg` puede configurarse como `no_argument, required_argument, optional_argument`, lo que representa respectivamente no tener argumentos, tener argumentos requeridos y tener argumentos opcionales.

`flag` y`val` se utilizan en conjunto. Si `flag = NULL`, `getopt_long` devuelve directamente `val`. Si `flag` es un puntero válido, `getopt_long` realiza una operación similar a `* flag = val`, estableciendo el valor de la variable apuntada por`flag` a `val`.

Si `getopt_long` encuentra una coincidencia con un argumento corto, devolverá el valor del carácter de ese argumento corto. Si encuentra una coincidencia con un argumento largo, devolverá `val` (si `flag = NULL`) o devolverá `0` (si `flag != NULL; *flag = val`). Si encuentra un carácter que no es un argumento, devolverá `?`. Si se han procesado todos los argumentos, devolverá `-1`.

Usando la característica de los valores de retorno, podemos lograr el mismo efecto con diferentes significados usando argumentos largos y cortos, como en el caso del primer parámetro `add` de `long_options`, cuyo valor `val` está establecido como el carácter `'a'` del argumento corto. De esta manera, al hacer una comprobación al retornar, tanto `--add` como `-a` entrarán en la misma rama de procesamiento y serán tratados como de igual significado.

La última pieza del rompecabezas es el uso de `optind` y `optarg`. `optind` es la ubicación del siguiente argumento a procesar en `argv`, mientras que `optarg` apunta a una cadena adicional de argumentos.

$ gcc -o programa programa.c
$ ./programa

En la traducción al español, el texto queda de la siguiente manera:

$ gcc -o programa programa.c
$ ./programa

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

`-a` y `--add` tienen el mismo significado. Para los argumentos cortos, el argumento opcional va directamente después, por ejemplo `-c4`. Mientras que para los argumentos largos, el argumento opcional debe ir seguido de un signo igual, por ejemplo `--verbose=3`.

## mobuleparam

Ok, finalmente llegamos al método que desencadenó este artículo originalmente, el kernel de Linux utiliza un método bastante ingenioso para pasar parámetros a los módulos del kernel, este método se llama `moduleparam`. Aquí explicaré brevemente cómo funciona el `moduleparam` en el kernel de Linux, para una explicación más detallada, puedes consultar el código. Aunque he tomado algunas ideas del manejo de `moduleparam`, hay algunas diferencias entre mi enfoque y el `moduleparam` del kernel de Linux. Para distinguirlos, llamaré a mi método "small moduleparam", mientras que al del kernel de Linux seguirá llamándose `moduleparam`.

Primero veamos cómo se utiliza `moduleparam`, lo declaramos dentro de un módulo:

```c
int enable_debug = 0;
module_param(enable_debug, int, 0);
```

Entonces, al cargar el módulo, ingrese los parámetros:

```shell
$ insmod mod enable_debug=1
```

La variable `enable_debug` está configurada correctamente como `1`, lo que la hace muy conveniente de usar. También se necesita muy poco código adicional y se puede escribir de forma concisa y elegante, sin necesidad de escribir bucles de condición como se hace con `getenv` y `getopt`. Además, proporciona conversiones de tipos incorporadas. Entonces, pensé que sería genial poder utilizar este método para procesar los argumentos de la línea de comandos.

A continuación, veamos la implementación principal de `moduleparam`:

```cpp linenums="1"
struct kernel_param {
const char *name;           // Nombre de la variable
	u16 perm;                   // Permiso de acceso a la variable
	u16 flags;                  // Variable es de tipo bool
	set param_set_fn;           // str -> variable value
get_fn param_get;           // valor de la variable -> str
	union {
		```spanish
		void *arg;              // Puntero a variable
		```
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

`module_param` es una macro que en realidad crea una estructura llamada `kernel_param` que refleja la variable pasada como argumento. Esta estructura guarda la información necesaria para acceder y modificar la variable, como se muestra en las líneas 20-24. Luego, la estructura se coloca en una sección llamada `__param` mediante `__section__ ("__param")`. Una vez que la estructura está guardada, el kernel, al cargar el módulo, busca la ubicación de la sección `__param` en el archivo ELF y la cantidad de estructuras en ella, y establece los valores de cada parámetro según su nombre y la función `param_set_fn`. El método para encontrar una sección de nombre específico depende de la plataforma, pero en la implementación del kernel de Linux se realiza a través del procesamiento del archivo ELF. Linux proporciona el comando `readelf` para ver la información del archivo ELF, si estás interesado puedes consultar la ayuda de `readelf`.

Arriba se menciona que el enfoque del núcleo de Linux es específico de la plataforma, pero yo quiero un método para manejar los parámetros sin importar la plataforma, por lo que debemos modificar el enfoque original de `moduleparam`, eliminando la declaración `__section__("__param")`, después de todo, no queremos tener la molestia de leer la sección `section` del archivo elf. Echemos un vistazo a la forma modificada de uso:

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

Entonces, para preservar la estructura de cada reflejo, he agregado una macro `init_module_param(num)` para declarar el espacio de almacenamiento de la estructura. `num` es el número de parámetros y si se declara un número de parámetros que excede `num`, el programa generará un error de afirmación. La declaración de `module_param` es un poco diferente de la original, se elimina el último parámetro que representa los permisos de acceso, sin control de permisos. Además, se agregó la macro `module_param_bool` para manejar variables de tipo `bool`, esto no es necesario en las versiones de Linux, ya que utiliza la función interna de GCC `__builtin_types_compatible_p` para determinar el tipo de la variable. Lamentablemente, MSVC no tiene esta función, por lo que tuve que eliminar esta funcionalidad e agregar una macro en su lugar. `module_param_array` y `module_param_string` son las funciones para manejar arreglos y cadenas, estas dos funcionalidades también están presentes en la versión original.

Una vez que se han declarado los parámetros, es hora de manejar los argumentos pasados. Utiliza la macro `parse_params`, pasando `argc, argv` como argumentos. El tercer parámetro es un puntero a una función de devolución de llamada para manejar los argumentos desconocidos. Puedes pasar `NULL` para interrumpir el procesamiento de argumentos en caso de que haya argumentos posicionales y devolver un código de error.

**Ejecutar código compilado:**



```
.\moduleparam_test.exe error=0 test=101 btest=1 latest=1,2,3 strtest=\"Hello World!\"
Parsing ARGS: error=0 test=101 btest=1 latest=1,2,3 strtest="Hello World!"
find unknown param: error
test = 101
btest = Y
latest = 1,2,3
strtest = Hello World!
```

Se puede ver que los valores numéricos, arrays y cadenas se leen e interpretan correctamente. Si se encuentran parámetros que no se pueden interpretar, retornará un código de error e imprimirá la información relevante. Podemos agregar fácilmente unas líneas de código para llevar a cabo la lectura y conversión de los parámetros, lo cual resulta muy elegante al utilizarlo. Para una implementación más detallada, puede ver directamente el código [aquí](https://github.com/disenone/aparsing).

##**Resumen**

Esta vez hemos resumido tres métodos para el manejo de argumentos de línea de comando en C/C++, que son `getenv`, `getopt` y `moduleparam`. Cada uno de estos métodos tiene sus propias características, y en el futuro se puede elegir el método adecuado según las necesidades reales.

`getenv` es una función nativa compatible con múltiples plataformas, por lo que se puede utilizar directamente. Sin embargo, es muy primitiva y utiliza variables de entorno, lo cual puede contaminar el entorno. Antes de usarla, se recomienda limpiar las variables de entorno innecesarias para evitar que se queden configuraciones anteriores contaminando.
- `getopt` es compatible de forma nativa en la plataforma Linux, pero no en Windows, por lo que se necesita incluir código de implementación para poder utilizarlo en diferentes plataformas. La forma de pasar parámetros sigue el estándar de paso de comandos en Linux, admite parámetros opcionales, pero puede resultar un poco tedioso de usar, generalmente requiere bucles y condicionales para manejar diferentes parámetros, y no es muy amigable con los parámetros de tipo numérico.
`moduleparam` es una herramienta de procesamiento de argumentos de línea de comandos que está basada en la implementación de "moduleparam" del kernel Linux. Es compatible con el uso en múltiples plataformas y es fácil de utilizar. Permite convertir los diferentes tipos de parámetros, sin embargo, la desventaja es que cada parámetro requiere una variable de almacenamiento correspondiente.

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
