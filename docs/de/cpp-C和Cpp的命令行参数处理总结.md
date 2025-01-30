---
layout: post
title: Zusammenfassung zur Verarbeitung von Befehlszeilenparametern in C/C++
categories:
- c++
catalog: true
tags:
- dev
description: In letzter Zeit, als ich den Linux-Kernelcode durchgesehen habe, bin
  ich auf die Verarbeitung der Kernelmoduleparameter gestoßen und fand sie ziemlich
  raffiniert. Das hat mich dazu angeregt, herauszufinden, wie man die Befehlszeilenparameter
  in C besser handhaben kann.
figures:
- assets/post_assets/2016-11-19-aparsing/aparsing.png
---

<meta property="og:title" content="C/C++ 的命令行参数处理总结" />

![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/gcc-4.9-blue.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/clang-3.7-birghtgreen.svg){:style="display: inline-block"}

![](assets/img/2016-11-19-aparsing/aparsing.png)

Vor einiger Zeit habe ich beim Durchsehen des Linux-Kernel-Codes die Verarbeitung von Modulparametern (moduleparam) im Kernel gesehen und fand sie ziemlich raffiniert. Das hat mich dazu angeregt, zu untersuchen, wie man Kommandozeilenparameter in C besser handhaben kann. Der gesamte verwendete Code ist hier zu finden [aparsing](https://github.com/disenone/aparsing)Der Code kann unter Windows, Linux und Mac OS X kompiliert und ausgeführt werden. Eine detaillierte Anleitung zur Kompilierung finden Sie in der README.md.

## getenv

Die Standardbibliothek stellt uns eine Funktion `getenv` zur Verfügung, die wörtlich genommen dazu dient, Umgebungsvariablen abzurufen. Wenn wir die benötigten Umgebungsvariablen im Voraus festlegen, können wir sie im Programm abrufen und damit indirekt Parameter an das Programm übergeben. Schauen wir uns den folgenden [Code](https://github.com/disenone/aparsing/blob/master/getenv/getenv_test.c)请提供要翻译的文本。

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

`getenv` Funktionserklärung siehe Punkt [4](#__codelineno-0-5)Gehe, übergebe den gewünschten Variablennamen und erhalte den Wert dieser Variable zurück. Wenn die Variable nicht gefunden wird, wird 0 zurückgegeben. [10](#__codelineno-0-10)和 [15](#__codelineno-0-15)Die Aktion besteht darin, die Werte von zwei Umgebungsvariablen getrennt abzurufen. Wenn die Variablen gültig sind, wird der Wert der Variablen ausgegeben. Es ist zu beachten, dass `getenv` nur Strings zurückgibt, weshalb der Benutzer die numerischen Typen manuell umwandeln muss, was die Handhabung etwas umständlich macht. Kompilieren und ausführen:

Unter Windows:

``` bat
set GETENV_ADD=abc & set GETENV_NUM=1 & .\getenv_test.exe
```

Unter Linux:

``` shell
GETENV_ADD=abc GETENV_NUM=2 ./getenv_test 
```

Translate these text into German language:

Ausgabe:

```
GETENV_ADD = abc
GETENV_NUM = 2
```

## getopt

Linux bietet uns eine Reihe von Funktionen `getopt, getopt_long, getopt_long_only`, um die über die Befehlszeile übergebenen Argumente zu verarbeiten. Die Deklarationen dieser drei Funktionen sind:

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

`getopt` kann nur kurze Parameter (d.h. einzeilige Parameter) verarbeiten, während `getopt_long` und `getopt_long_only` lange Parameter verarbeiten können. Eine detaillierte Funktionsbeschreibung finden Sie im Handbuch unter Linux. Im Folgenden erklären wir die Verwendung von `getopt` und `getopt_long` anhand von Beispielen.

Es ist zu beachten, dass diese Funktion in Windows nicht angeboten wird, daher habe ich einen Quellcode gefunden, der unter Windows kompiliert werden kann, und einige kleine Änderungen vorgenommen. Der Code ist [hier](https://github.com/disenone/aparsing/tree/master/getopt).

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

Lassen Sie uns die Verwendung von `getopt_long` genauer analysieren. Die ersten drei Parameter von `getopt_long` sind dieselben wie bei `getopt`, nämlich: die Anzahl der Befehlszeilenargumente `argc`, das Array der Befehlszeilenargumente `argv` und die spezifische Form der kurzen Parameter `optstring`. Das Format von `optstring` besteht aus den einzelnen Zeichen der kurzen Parameter, wobei ein Doppelpunkt `:` bedeutet, dass ein Parameter erforderlich ist, und zwei Doppelpunkte `::` anzeigen, dass der Parameter optional ist. Zum Beispiel in Zeile 19 wird die Form der kurzen Parameter erklärt: Der Parameter `b` erfordert keine zusätzlichen Parameter, der Parameter `a` benötigt zusätzliche Parameter, und `c` ist ein optionaler Parameter.

Die letzten beiden Parameter von `getopt_long` dienen der Verarbeitung von langen Parametern, wobei die Struktur von `option` wie folgt aussieht:

```c
struct option {
const char *name;       // Long parameter name
int has_arg; // Whether an additional argument is included
int        *flag;       // Setzt, wie das Ergebnis des Funktionsaufrufs zurückgegeben wird
int val; // The returned value
};
```
Obwohl es sich um lange Parameter handelt, kann `name` dennoch auf eine einzeichige Länge gesetzt werden.

`has_arg` kann auf `no_argument, required_argument, optional_argument` gesetzt werden, was jeweils bedeutet, dass keine Argumente, erforderliche Argumente oder optionale Argumente übergeben werden.

`flag` und `val` werden zusammen verwendet. Wenn `flag = NULL` ist, gibt `getopt_long` direkt `val` zurück. Andernfalls, wenn `flag` ein gültiger Zeiger ist, führt `getopt_long` eine ähnliche Operation wie `*flag = val` aus und setzt die Variable, auf die `flag` zeigt, auf den Wert von `val`.

Wenn `getopt_long` ein passendes kurzes Argument findet, gibt es den Zeichenwert dieses kurzen Arguments zurück. Wenn ein passendes langes Argument gefunden wird, gibt es `val` zurück (wenn `flag = NULL`) oder `0` (wenn `flag != NULL; *flag = val;`). Wenn es auf ein Zeichen stößt, das kein Argument ist, gibt es `?` zurück. Wenn alle Argumente verarbeitet wurden, gibt es `-1` zurück.

Nutzen wir die Eigenschaften eines Rückgabewerts, können wir eine vergleichbare Wirkung erzielen, indem wir lange Parameter mit kurzen Parametern gleichsetzen. Zum Beispiel wird beim ersten Parameter `add` von `long_options` der `val` Wert auf das Zeichen `'a'` des kurzen Parameters gesetzt. Bei der Rückgabewertprüfung werden `--add` und `-a` in denselben Verarbeitungszweig geleitet und als gleichwertig behandelt.

Die letzte Aufgabe des Puzzles ist die Verwendung von `optind` und `optarg`. `optind` zeigt auf die Position des nächsten zu verarbeitenden Arguments in `argv`, während `optarg` auf zusätzliche Argumente verweist.

Kompilieren und Ausführen von Code:

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

Die Bedeutungen von `-a` und `--add` sind identisch. Bei kurzen Parametern folgt der optionale Parameter direkt danach, zum Beispiel `-c4`, während bei langen Parametern der optionale Parameter mit einem Gleichheitszeichen verbunden sein muss, zum Beispiel `--verbose=3`.

## mobuleparam

Ok, finally we come to the method that originally sparked this article. The Linux kernel cleverly uses a method called `moduleparam` to pass parameters to kernel modules. Let me briefly explain the practice of `moduleparam` in the Linux kernel here, for a more detailed explanation you can refer to the code. Although I have borrowed some of the handling methods from `moduleparam`, there are some differences compared to the Linux kernel's `moduleparam`. To distinguish, I will refer to my method as `small moduleparam`, while the Linux kernel's method will continue to be referred to as `moduleparam`.

Lass uns zunächst die Verwendung von `moduleparam` anschauen, indem wir es im Modul deklarieren:

```c
int enable_debug = 0;
module_param(enable_debug, int, 0);
```

Then enter the input parameters when loading the module:

```shell
$ insmod mod enable_debug=1
```

Die Variable `enable_debug` ist korrekt auf `1` gesetzt, was die Verwendung bequem macht und nur wenig zusätzlichen Code erfordert. Der Code kann kurz und elegant geschrieben werden, ohne viele Schleifenüberprüfungen wie bei `getenv` und `getopt`, und er hat sogar integrierte Typumwandlung. Deshalb dachte ich mir, wenn man diese Methode verwenden könnte, um Befehlszeilenargumente zu verarbeiten, wäre das noch besser.

Weiter geht es mit dem Kern der Implementierung von `moduleparam`:

```cpp linenums="1"
struct kernel_param {
	const char *name;           // Variablenname
u16 perm;                   // Variable Zugriffsberechtigung
u16 flags;                  // Variable ist vom Typ bool
	param_set_fn set;           // str -> Variablenwert
param_get_fn get;           // Variablewert -> str
	union {
void *arg;              // Variablenzeiger
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

Die `module_param` ist eine Makrofunktion, die tatsächlich ein Struktur `kernel_param` erstellt, die auf die übergebene Variable reflektieren kann. Diese Struktur speichert ausreichende Informationen zum Zugriff und Setzen der Variablen, wie in den Zeilen 20-24. Die Struktur wird im `section` namens `__param` platziert (`__section__ ("__param")`). Nachdem die Struktur erstellt wurde, sucht der Kernel beim Laden des Moduls die Position und Anzahl der Strukturen im elf-Dateibereich `section __param` und setzt die Werte für jeden Parameter entsprechend Namen und `param_set_fn`. Die Methode zum Auffinden einer spezifischen `section` nach Namen ist plattformspezifisch. Der Linux-Kernel implementiert das Handling von elf-Dateien, und Linux bietet das Kommando `readelf` an, um Informationen über elf-Dateien anzuzeigen. Interessierte können die Hilfeinformationen von `readelf` einsehen.

Oben wurde erwähnt, dass die Vorgehensweise des Linux-Kernels plattformspezifisch ist. Ich suche jedoch eine plattformunabhängige Methode zur Behandlung von Parametern. Deshalb müssen wir die ursprüngliche Methode von `moduleparam` etwas anpassen und die Deklaration von `__section__("__param")` entfernen, schließlich wollen wir nicht unnötig kompliziert auf die `Sektion` der elf-Datei zugreifen. Schauen wir uns nun die Verwendung nach der Änderung an:

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

Um jede reflektierte Struktur zu erhalten, habe ich ein Makro `init_module_param(num)` hinzugefügt, um den Speicherplatz für die Struktur zu deklarieren. `num` ist die Anzahl der Parameter. Wenn die tatsächlich deklarierte Parameteranzahl `num` überschreitet, wird ein Assertionsfehler im Programm ausgelöst. Die Deklaration von `module_param` unterscheidet sich leicht von der Originalversion, da der letzte Parameter, der den Zugriff darstellt, entfernt wurde und keine Zugriffskontrolle stattfindet. Darüber hinaus wurde ein Makro `module_param_bool` hinzugefügt, um Variable vom Typ `bool` zu behandeln. Dies ist in den Linux-Versionen nicht notwendig, da es die gcc-internen Funktionen `__builtin_types_compatible_p` zur Bestimmung des Variablentyps verwendet. Leider hat MSVC diese Funktion nicht, sodass ich diese Funktion entfernen musste und ein Makro hinzufügen musste. `module_param_array` und `module_param_string` sind die Behandlung von Arrays und Zeichenketten. Diese beiden Funktionen waren bereits in der ursprünglichen Version vorhanden.

Nachdem die Parameter deklariert sind, geht es darum, die übergebenen Parameter zu verarbeiten. Verwenden Sie das Makro `parse_params`, geben Sie `argc, argv` an und als dritten Argument den Funktionszeiger für den Umgang mit unbekannten Parametern an. Sie können auch `NULL` übergeben, dann wird die Verarbeitung der Parameter an der Stelle von Positionalparametern abgebrochen und ein Fehlercode zurückgegeben.

Kompilieren und Ausführen von Code:

```
.\moduleparam_test.exe error=0 test=101 btest=1 latest=1,2,3 strtest=\"Hello World!\"
Parsing ARGS: error=0 test=101 btest=1 latest=1,2,3 strtest="Hello World!"
find unknown param: error
test = 101
btest = Y
latest = 1,2,3
strtest = Hello World!
```

Es sind Werte sichtbar, Arrays und Strings können korrekt eingelesen und formatiert werden. Wenn ein nicht konvertierbares Argument auftritt, wird ein Fehlercode zurückgegeben und relevante Informationen ausgedruckt. Wir können ganz einfach ein paar Zeilen Code hinzufügen, um das Einlesen und die Umwandlung der Parameter abzuschließen, was sehr elegant ist. Eine detailliertere Implementierung kann direkt im Code angesehen werden, [hier](https://github.com/disenone/aparsing)I'm sorry, but I can't provide a translation without any text to work with. Could you please provide the content you'd like me to translate into German?

##Zusammenfassung

Dieses Mal haben wir drei Methoden zur Verarbeitung von Befehlszeilenparametern in C/C++ zusammengefasst: `getenv`, `getopt` und `moduleparam`. Jede Methode hat ihre eigenen Merkmale, sodass Sie je nach Bedarf die geeignete Methode auswählen können.

- `getenv` ist nativ plattformübergreifend unterstützt und kann direkt verwendet werden, ist jedoch etwas rudimentär und nutzt Umgebungsvariablen, was die Umgebung in gewissem Maße belastet. Es ist ratsam, vor jeder Verwendung unnötige Umgebungsvariablen zu bereinigen, um zu verhindern, dass die Einstellungen vom letzten Mal Rückstände hinterlassen.
`getopt` is native to the Linux platform and not supported on Windows, so code implementation is required for cross-platform usage. The parameter passing follows the standard command line parameter format in Linux, supporting optional parameters. However, it can be slightly cumbersome to use, usually requiring loops and conditional statements to handle different parameters, and is not very user-friendly for numerical parameters.
`moduleparam` ist ein Befehlszeilenparameterverarbeitungstool, das an der Implementierung von `moduleparam` im Linux-Kernel orientiert ist. Es unterstützt plattformübergreifende Nutzung, ist einfach zu bedienen und kann Typkonvertierungen für verschiedene Parameterarten durchführen. Der Nachteil besteht darin, dass jeder Parameter eine entsprechende Variable zur Speicherung benötigt.

--8<-- "footer_de.md"


> Dieser Text wurde mit ChatGPT übersetzt. Bitte geben Sie Ihr [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)darauf hin, dass es irgendwelche Auslassungen gibt. 
