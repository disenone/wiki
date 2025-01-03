---
layout: post
title: Zusammenfassung zur Verarbeitung von Befehlszeilenargumenten in C/C++
categories:
- c++
catalog: true
tags:
- dev
description: Vor einiger Zeit, als ich den Linux-Kernel-Code durchgesehen habe, bin
  ich auf die Behandlung von Modulparametern im Kernel gestoßen und fand sie ziemlich
  raffiniert. Das hat mich dazu gebracht, darüber nachzudenken, wie man die Befehlszeilenparameter
  in C besser handhaben könnte.
figures:
- assets/post_assets/2016-11-19-aparsing/aparsing.png
---

<meta property="og:title" content="C/C++ 的命令行参数处理总结" />

![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/gcc-4.9-blue.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/clang-3.7-birghtgreen.svg){:style="display: inline-block"}

![](assets/img/2016-11-19-aparsing/aparsing.png)

In letzter Zeit, als ich den Linux-Kernel-Code durchgearbeitet habe, bin ich auf die Art und Weise gestoßen, wie der Kernel mit Modulparametern umgeht. Es war wirklich raffiniert und hat mich dazu inspiriert, zu untersuchen, wie man Befehlszeilenargumente unter C noch besser verarbeiten kann. Alle im Artikel verwendeten Codes sind hier zu finden [aparsing](https://github.com/disenone/aparsing)Der Code unterstützt das Kompilieren und Ausführen unter Windows, Linux und Mac OS X. Eine ausführliche Anleitung zum Kompilieren finden Sie in der Datei README.md.

## getenv

Die Standardbibliothek bietet uns eine Funktion namens `getenv`. Wörtlich genommen ist diese Funktion dazu da, Umgebungsvariablen abzurufen. Wenn wir also die erforderlichen Umgebungsvariablen im Voraus einstellen und sie dann im Programm abrufen, können wir die Parameter indirekt an das Programm übergeben. Schauen wir uns nun den folgenden [Code](https://github.com/disenone/aparsing/blob/master/getenv/getenv_test.c)Bitte geben Sie Text ein, den Sie übersetzen möchten.

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

Das Kommando `getenv` ist in Zeile [4](#__codelineno-0-5)Funktion, die den Wert der angegebenen Variablen zurückgibt. Gibt 0 zurück, wenn die Variable nicht gefunden wurde. [10](#__codelineno-0-10)Translate these text into German language:

和 [15](#__codelineno-0-15)Die Zeile ruft die Werte von zwei Umgebungsvariablen ab, zeigt den Wert der Variablen an, wenn sie gültig sind. Beachten Sie, dass `getenv` immer Zeichenketten zurückgibt, daher muss der Benutzer die Werte manuell in numerische Typen umwandeln, was die Verwendung etwas umständlich macht. Kompilieren und ausführen:

Unter Windows:

``` bat
set GETENV_ADD=abc & set GETENV_NUM=1 & .\getenv_test.exe
```

Unter Linux:

``` shell
GETENV_ADD=abc GETENV_NUM=2 ./getenv_test 
```

Ausgabe:

```
GETENV_ADD = abc
GETENV_NUM = 2
```

## getopt

Linux provides us with a set of functions `getopt, getopt_long, getopt_long_only` to handle command-line arguments passed into functions. The declarations of these three functions are as follows:

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

`getopt` can only handle short options (i.e., single character options), while `getopt_long` and `getopt_long_only` can handle long options. For a detailed explanation of the functions, you can refer to the manual in Linux. Now, let's demonstrate the usage of `getopt` and `getopt_long` through examples.

Es ist zu beachten, dass diese Funktionen unter Windows nicht verfügbar sind. Daher habe ich eine Quellcodedatei gefunden, die unter Windows kompiliert werden kann, und habe einige kleine Anpassungen vorgenommen. Der gesamte Code befindet sich [hier](https://github.com/disenone/aparsing/tree/master/getopt)I'm sorry, but I can't provide a translation for non-text characters.

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

Wir werden uns hier hauptsächlich mit der Verwendung von `getopt_long` beschäftigen. Die ersten drei Parameter von `getopt_long` sind identisch mit denen von `getopt`: die Anzahl der Befehlszeilenargumente `argc`, das Array der Befehlszeilenargumente `argv` und die spezifische Form der Kurzparameter `optstring`. Das Format von `optstring` besteht aus einzelnen Kurzparameter-Zeichen, gefolgt von einem Doppelpunkt `:`, um anzuzeigen, dass ein Parameter erwartet wird, und zwei Doppelpunkten `::`, um einen optionalen Parameter anzugeben. Zum Beispiel in Zeile 19 wird die Form der Kurzparameter deklariert: Das Argument `b` erwartet keine zusätzlichen Parameter, das Argument `a` erwartet einen zusätzlichen Parameter und `c` erwartet einen optionalen Parameter.

Die beiden letzten Parameter von `getopt_long` dienen zur Behandlung von Langoptionen, wobei die Struktur von `option` wie folgt aussieht:

```c
struct option {
const char *name;       // Long parameter name
int has_arg; // Indicates whether additional arguments are included.
int *flag; // Define how to return the result of a function call
int val; // The returned value
};
```
Auch wenn es als langer Parameter bezeichnet wird, kann `name` immer noch auf die Länge eines einzelnen Zeichens eingestellt werden.

`has_arg` kann auf `no_argument, required_argument, optional_argument` gesetzt werden, um jeweils keine Argumente, erforderliche Argumente oder optionale Argumente anzugeben.

`flag` und `val` werden gemeinsam verwendet. Wenn `flag = NULL` ist, `getopt_long` gibt direkt `val` zurück. Andernfalls, wenn `flag` ein gültiger Zeiger ist, wird `getopt_long` eine Operation wie `*flag = val` ausführen und die Variable, auf die `flag` zeigt, auf den Wert von `val` setzen.

Wenn `getopt_long` eine Übereinstimmung mit einem Kurzparameter findet, wird der Zeichenwert dieses Kurzparameters zurückgegeben. Wenn ein Übereinstimmung mit einem Langparameter gefunden wird, wird `val` zurückgegeben (`flag = NULL`) oder `0` (`flag != NULL; *flag = val;`). Wenn ein nicht-parameterbezogenes Zeichen gefunden wird, wird `?` zurückgegeben. Wenn alle Parameter abgearbeitet sind, wird `-1` zurückgegeben.

Durch die Verwendung der Rückgabeeigenschaft können wir einen Effekt erzielen, bei dem lange und kurze Argumente die gleiche Bedeutung haben, zum Beispiel beim ersten Argument `add` von `long_options`, dessen `val`-Wert auf das Zeichen des kurzen Arguments `'a'` gesetzt ist. Wenn dann überprüft wird, betreten `--add` und `-a` denselben Verarbeitungszweig und werden als dieselbe Bedeutung behandelt.

Das letzte Puzzlestück ist die Verwendung von `optind` und `optarg`. `optind` zeigt auf die Position des nächsten zu verarbeitenden Arguments in `argv`, während `optarg` auf zusätzliche Argumente zeigt.

Compile and run the code:

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

`-a` und `--add` haben die gleiche Bedeutung, bei kurzen optionalen Parametern folgt dieser direkt dahinter, z.B. `-c4`, während bei langen optionalen Parametern ein Gleichheitszeichen erforderlich ist, z.B. `--verbose=3`.

## mobuleparam

Ok, we have finally reached the method that initially sparked this article – Linux kernel cleverly utilizes a technique called `moduleparam` to pass parameters to kernel modules. I will briefly explain the approach of the `moduleparam` in the Linux kernel here, for a more detailed explanation you can refer to the code. While I have borrowed some processing methods from `moduleparam`, there are certain differences compared to Linux kernel's `moduleparam`. To distinguish, I will refer to my method as `small moduleparam`, while Linux kernel's method remains as `moduleparam`.

Schauen wir uns zuerst an, wie `moduleparam` verwendet wird. Es wird innerhalb des Moduls deklariert:

```c
int enable_debug = 0;
module_param(enable_debug, int, 0);
```

Danach bei der Modulbeladung Eingabeparameter angeben:

```shell
$ insmod mod enable_debug=1
```

Die Variable `enable_debug` wird korrekt auf `1` gesetzt, was die Verwendung sehr praktisch macht. Es erfordert nur wenig zusätzlichen Code und ermöglicht es, den Code kurz und elegant zu halten, ohne viele Schleifenabfragen wie bei `getenv` und `getopt` schreiben zu müssen. Zudem bietet es bereits Typumwandlung. So dachte ich mir, es wäre großartig, wenn diese Methode auch zur Verarbeitung von Befehlszeilenparametern verwendet werden könnte.

Weiter geht es mit der Kernimplementierung von `moduleparam`:

```cpp linenums="1"
struct kernel_param {
const char *name; // Variable name
u16 perm;                   // Variable Zugriffsberechtigung
u16 flags;                  // Variable, ob es sich um ein boolsches Typ handelt
param_set_fn set;           // str -> variable value
param_get_fn get;           // Variablewert -> str
	union {
void *arg;              // Variable-Zeiger
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

`module_param` is a macro that basically creates a structure `kernel_param` which can reflect the incoming variables, as described in lines 20-24. This structure holds the necessary information to access and set the variables and is placed within a `section` called `__param` (`__section__ ("__param")`). Once the structure is set up, the kernel will locate the position and number of structures in the elf file's `section __param` during module loading. It then proceeds to set the value for each parameter based on its name and `param_set_fn`. The method to locate a specific named `section` is platform-dependent. The Linux kernel handles elf file processing, and Linux provides the `readelf` command to view elf file information. Those interested can refer to the `readelf` command's help documentation.

Oben wurde erwähnt, dass die Vorgehensweise des Linux-Kernels plattformabhängig ist. Ich suche jedoch nach einer plattformunabhängigen Methode zur Behandlung von Parametern. Daher müssen wir die ursprüngliche Verwendung von `moduleparam` anpassen, indem wir die Deklaration von `__section__ ("__param")` entfernen. Immerhin möchten wir nicht aufwändig Abschnitte der elf Datei lesen. Schauen wir uns nun an, wie die Verwendung nach der Modifikation aussieht:

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

Um jede Reflektionsstruktur zu speichern, habe ich eine Makro namens `init_module_param(num)` hinzugefügt, um den Speicherplatz für die Struktur zu deklarieren. `num` ist die Anzahl der Parameter. Wenn die tatsächliche Anzahl der deklarierten Parameter größer ist als `num`, löst das Programm einen Assertionsfehler aus. Die Deklaration von `module_param` unterscheidet sich leicht von der Originalversion und entfernt den letzten Parameter, der den Zugriff darstellt, um die Zugriffskontrolle nicht zu berücksichtigen. Darüber hinaus wurde eine Makro namens `module_param_bool` hinzugefügt, um Variablen vom Typ `bool` zu behandeln. In Linux ist dies nicht erforderlich, da es die gcc-internen Funktionen `__builtin_types_compatible_p` verwendet, um den Typ der Variablen zu überprüfen. Leider hat MSVC diese Funktion nicht, daher musste ich diese Funktionalität entfernen und ein Makro hinzufügen. `module_param_array` und `module_param_string` sind einfach die Behandlung von Arrays und Zeichenfolgen. Diese beiden Funktionen sind auch in der Originalversion vorhanden.

Nachdem die Parameter deklariert wurden, muss man sie verarbeiten. Verwende das Makro `parse_params`, gebe `argc, argv` an. Der dritte Parameter ist ein Zeiger auf eine Callback-Funktion zur Behandlung unbekannter Parameter. Du kannst `NULL` übergeben, um die Verarbeitung der Positionsaufheberparameter zu unterbrechen und einen Fehlercode zurückzugeben.

Kompilieren und Ausführen des Codes:

```
.\moduleparam_test.exe error=0 test=101 btest=1 latest=1,2,3 strtest=\"Hello World!\"
Parsing ARGS: error=0 test=101 btest=1 latest=1,2,3 strtest="Hello World!"
find unknown param: error
test = 101
btest = Y
latest = 1,2,3
strtest = Hello World!
```

Sie können sehen, dass Zahlen, Arrays und Zeichenfolgen alle korrekt gelesen und umgewandelt werden können. Wenn ein nicht umwandelbarer Parameter auftritt, wird ein Fehlercode zurückgegeben und relevante Informationen werden gedruckt. Es ist sehr einfach, einige Zeilen Code hinzuzufügen, um das Einlesen und die Umwandlung der Parameter abzuschließen. Es lässt sich sehr elegant nutzen. Weitere detaillierte Implementierungen können direkt im Code gefunden werden, [hier](https://github.com/disenone/aparsing)I am sorry, but there is nothing to translate in the text provided.

##Zusammenfassung

In diesem Fall haben wir drei Methoden zur Behandlung von Befehlszeilenparametern in C/C++ zusammengefasst: `getenv`, `getopt` und `moduleparam`. Jede Methode hat ihre eigenen Merkmale, und man kann je nach Bedarf die geeignete Methode auswählen.

`getenv` is native multi-platform supported so you can use it directly, but it's too primitive and uses environment variables, causing a certain degree of pollution to the environment. It's best to clear unnecessary environment variables before each use to prevent the pollution from previous settings.
`getopt` is natively supported on Linux systems, but not on Windows, so it requires the inclusion of implemented code to enable cross-platform use. The parameter passing follows the standard of command line arguments on Linux, supporting optional parameters; however, its usage is a bit cumbersome. Typically, it necessitates loops and conditional statements to handle different parameters, and it is not particularly user-friendly when it comes to numerical types of parameters.
`moduleparam` is a command line parameter processing tool inspired by the `moduleparam` implementation in the Linux kernel. It is cross-platform compatible, easy to use, and can perform type conversions for different types of parameters. The downside is that each parameter requires a corresponding variable for storage.

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt. Bitte [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Führen Sie alle Übersehenen aus. 
