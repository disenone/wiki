---
layout: post
title: Résumé du traitement des arguments de ligne de commande en C/C++
categories:
- c++
catalog: true
tags:
- dev
description: Il y a quelque temps, en parcourant le code source du noyau Linux, j'ai
  vu comment le noyau gérait les paramètres de module (moduleparam), et j'ai trouvé
  ça plutôt ingénieux. Cela m'a donné envie d'étudier comment bien gérer les arguments
  de la ligne de commande en C.
figures:
- assets/post_assets/2016-11-19-aparsing/aparsing.png
---

<meta property="og:title" content="C/C++ 的命令行参数处理总结" />

![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/gcc-4.9-blue.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/clang-3.7-birghtgreen.svg){:style="display: inline-block"}

![](assets/img/2016-11-19-aparsing/aparsing.png)

Il y a quelque temps, en parcourant le code source du noyau Linux, j'ai remarqué la façon dont le noyau gère les paramètres de module (moduleparam), j'ai trouvé ça plutôt ingénieux, ce qui m'a donné envie d'étudier plus en détail comment traiter de manière plus efficace les paramètres de ligne de commande en C. Le code utilisé dans cet article se trouve ici : [aparsing](https://github.com/disenone/aparsing)Le code peut être compilé et exécuté sous Windows, Linux et Mac OS X. Les instructions détaillées de compilation se trouvent dans README.md.

## getenv

(https://github.com/disenone/aparsing/blob/master/getenv/getenv_test.c)Veuillez traduire ce texte en français :

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

La fonction `getenv` est déclarée comme indiqué au [4](#__codelineno-0-5)Prends le nom de la variable que tu veux obtenir en argument, renvoie la valeur de cette variable. Si la variable n'est pas trouvée, renvoie 0. [10](#__codelineno-0-10)Translate these text into French language:

Et [15](#__codelineno-0-15)Le code consiste à récupérer les valeurs de deux variables d'environnement différentes, puis à afficher la valeur de chaque variable si elle est valide. Il est important de noter que la fonction `getenv` renvoie toujours des chaînes de caractères, donc l'utilisateur doit convertir manuellement les valeurs en types numériques, ce qui peut rendre l'utilisation moins pratique. Compilez et exécutez :

Sous Windows :

``` bat
set GETENV_ADD=abc & set GETENV_NUM=1 & .\getenv_test.exe
```

Sous Linux :

``` shell
GETENV_ADD=abc GETENV_NUM=2 ./getenv_test 
```

Veuillez traduire ce texte en langue française :

```
GETENV_ADD = abc
GETENV_NUM = 2
```

## getopt

Linux provides us with a set of functions `getopt, getopt_long, getopt_long_only` to handle command line arguments passed into the program. The declarations of these three functions are:

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

La commande `getopt` ne peut traiter que les options courtes (c'est-à-dire les options d'un seul caractère), tandis que `getopt_long` et `getopt_long_only` peuvent traiter les options longues. Pour une explication détaillée des fonctions, veuillez consulter le manuel de Linux. Nous allons maintenant expliquer l'utilisation de `getopt` et `getopt_long` à l'aide d'exemples.

Il convient de noter que ces fonctions ne sont pas disponibles sous Windows. J'ai donc recherché une version du code source compilable sous Windows, apporté quelques ajustements mineurs et le code est disponible [ici](https://github.com/disenone/aparsing/tree/master/getopt)I'm sorry, but it seems that there is no text to translate.

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

Nous allons nous concentrer sur l'analyse de l'utilisation de `getopt_long`. Les trois premiers paramètres de `getopt_long` sont les mêmes que pour `getopt`: le nombre d'arguments de la ligne de commande `argc`, le tableau des arguments de la ligne de commande `argv`, et la forme spécifique des options courtes `optstring`. Le format de `optstring` est composé de caractères d'options courts, suivis d'un deux points `:` pour indiquer une option avec argument, de deux deux points `::` pour indiquer une option avec argument facultatif. Par exemple, à la ligne 19, la déclaration des options courtes est la suivante: l'option `b` n'a pas d'argument supplémentaire, l'option `a` a un argument supplémentaire, et l'option `c` a un argument facultatif.

Les deux derniers paramètres de `getopt_long` sont utilisés pour traiter les options longues, avec la structure `option` étant :

```c
struct option {
const char *nom; // Long name of the parameter
int has_arg;    // Whether it has additional arguments
int *flag; // Establishes how to return the function call result
int         val;        // La valeur renvoyée
};
```
Bien que cela soit considéré comme un paramètre long, le champ `name` peut toujours être défini à une longueur d'un seul caractère.

Le terme `has_arg` peut être défini comme `no_argument, required_argument, optional_argument`, qui respectivement signifient sans argument, avec argument requis, avec argument facultatif.

Les `flag` et `val` sont utilisés ensemble. Si `flag = NULL`, `getopt_long` retournera directement `val`. Sinon, si `flag` est un pointeur valide, `getopt_long` effectuera une opération similaire à `*flag = val`, en définissant la variable pointée par `flag` avec la valeur de `val`.

Si `getopt_long` trouve une correspondance avec un argument court, il renverra la valeur de ce court argument. S'il trouve une correspondance avec un argument long, il renverra `val` (`flag = NULL`) ou renverra `0` (`flag != NULL; *flag = val;`). Si un caractère qui n'est pas un argument est rencontré, il renverra `?`. Lorsque tous les arguments ont été traités, il renverra `-1`.

En utilisant les propriétés de la valeur de retour, nous pouvons créer un effet où les longues options et les courtes options ont la même signification, par exemple, en prenant le premier argument de `long_options` `add`, en définissant sa valeur `val` comme le caractère de l'option courte `'a'`, alors lors de la vérification du retour, `--add` et `-a` seront traités dans la même branche de traitement, et seront considérés comme ayant la même signification.

Le dernier morceau du puzzle est l'utilisation de `optind` et `optarg`. `optind` indique la position du prochain argument à traiter dans `argv`, tandis que `optarg` pointe vers la chaîne de caractères des arguments supplémentaires.

Compiler et exécuter le code :

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

Les significations de `-a` et `--add` sont identiques. Les arguments optionnels des options courtes sont directement placés après, par exemple `-c4`, tandis que les arguments optionnels des options longues doivent être précédés d'un signe égal, par exemple `--verbose=3`.

## mobuleparam

D'accord, enfin arrivé à la méthode qui a été à l'origine de cet article, le noyau Linux utilise une méthode très astucieuse pour transmettre des paramètres aux modules noyaux, il s'agit de `moduleparam`. Je vais d'abord expliquer brièvement la méthode `moduleparam` du noyau Linux ici, pour des explications plus détaillées, vous pouvez consulter le code. Bien que j'aie emprunté certaines méthodes de traitement de `moduleparam`, il existe quelques différences avec celle du noyau Linux, pour les distinguer, je vais appeler ma méthode `small moduleparam`, tandis que celle du noyau Linux continuera d'être appelée `moduleparam`.

Consultez d'abord l'utilisation de `moduleparam`, déclarez-le dans le module :

```c
int enable_debug = 0;
module_param(enable_debug, int, 0);
```

Ensuite, lorsque vous chargez le module, saisissez les paramètres d'entrée :

```shell
$ insmod mod enable_debug=1
```

La variable `enable_debug` est correctement définie à `1`, ce qui la rend facile à utiliser. Il nécessite peu de code supplémentaire, permettant ainsi d'écrire un code concis et élégant. Il n'est pas nécessaire de faire de nombreux boucles de vérification comme avec `getenv` et `getopt`, en plus, il inclut déjà la conversion de types. En voyant cela, je me suis dis que si cette méthode pouvait être utilisée pour gérer les arguments de ligne de commande, ce serait encore mieux.

Continuons en examinant la mise en œuvre principale de `moduleparam`:

```cpp linenums="1"
struct kernel_param {
const char *name;           // Variable name
u16 perm;                   // Variable access permission
Drapeaux u16; // Variable si c'est un type booléen
set_fn set;           // str -> variable value
param_get_fn get;           // Fonction de récupération de paramètre;           // 变量值 -> str
	union {
void *arg;              // Variable pointer
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

`module_param` is a macro that essentially creates a `kernel_param` structure that reflects the incoming variable, storing enough information to access and set the variable, as stated in lines 20-24. This structure is placed in a section called `__param` (`__section__("__param")`). Once the structure is saved, the kernel will locate the position and number of structures in the elf file's `section __param` when loading the module, and then set the value of each parameter based on the name and `param_set_fn`. The method to locate a specific `section` by name is platform-specific. The Linux kernel handles elf files, and Linux provides the `readelf` command to view information about elf files. Those interested can refer to the `readelf` help documentation.

Traduisez ce texte en langue française :

Le texte ci-dessus mentionne que l'approche du noyau Linux est spécifique à la plate-forme, mais je cherche une méthode qui soit indépendante de la plate-forme pour gérer les paramètres. Par conséquent, nous devons modifier légèrement l'approche initiale de `moduleparam` en supprimant la déclaration `__section__ ("__param")`, car nous ne souhaitons pas extraire laborieusement la section d'un fichier elf. Regardons maintenant comment utiliser la version modifiée :

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

Afin de conserver la structure de chaque réflexion, j'ai ajouté une macro `init_module_param(num)` pour déclarer l'espace de stockage de la structure, où `num` représente le nombre de paramètres. Si le nombre réel de paramètres déclaré dépasse `num`, une erreur d'assertion sera déclenchée. La déclaration de `module_param` diffère légèrement de l'original, le dernier paramètre indiquant les permissions d'accès a été supprimé, éliminant ainsi le contrôle d'accès. De plus, une nouvelle macro `module_param_bool` a été ajoutée pour gérer les variables de type `bool`. Cela n'est pas nécessaire dans les versions Linux où le compilateur gcc utilise la fonction intégrée `__builtin_types_compatible_p` pour déterminer le type de variable. Malheureusement, cette fonction n'existe pas dans MSVC, donc j'ai dû supprimer cette fonctionnalité et ajouter une macro à la place. `module_param_array` et `module_param_string` sont utilisés pour traiter respectivement les tableaux et les chaînes de caractères. Ces fonctionnalités existaient déjà dans la version d'origine.

Une fois que les paramètres de la déclaration sont prêts, il est temps de les traiter, en utilisant la macro `parse_params`, en passant `argc, argv` en arguments. Le troisième paramètre est un pointeur de fonction de rappel pour le traitement des paramètres inconnus, vous pouvez passer `NULL`, ce qui interrompra le traitement des paramètres positionnels et renverra un code d'erreur.

Compiler et exécute le code :

```
.\moduleparam_test.exe error=0 test=101 btest=1 latest=1,2,3 strtest=\"Hello World!\"
Parsing ARGS: error=0 test=101 btest=1 latest=1,2,3 strtest="Hello World!"
find unknown param: error
test = 101
btest = Y
latest = 1,2,3
strtest = Hello World!
```

On peut voir que les nombres, les tableaux et les chaînes de caractères peuvent être lus et convertis correctement en format. Si un paramètre ne peut pas être converti en format, une erreur sera renvoyée avec des informations pertinentes affichées. En ajoutant simplement quelques lignes de code, nous pouvons facilement lire et traiter les paramètres, ce qui le rend très élégant à utiliser. Pour une mise en œuvre plus détaillée, vous pouvez directement consulter le code [ici](https://github.com/disenone/aparsing)。

##Résumé

Cette fois-ci, nous avons récapitulé les trois méthodes de gestion des arguments de ligne de commande en C/C++ : `getenv`, `getopt` et `moduleparam`. Chaque méthode a ses propres caractéristiques, il sera possible de choisir la méthode appropriée en fonction des besoins réels à l'avenir.

`getenv` is a native cross-platform function that can be used directly, but it is also quite primitive and uses environment variables, which may contaminate the environment. It is advisable to clear unnecessary environment variables before each use to prevent contamination from previous settings.
`getopt` is natively supported on Linux platforms, not on Windows. To achieve cross-platform usability, inclusion of implementation code is necessary. The parameter passing adheres to Linux's standard command line parameter format, supporting optional parameters. However, its usage can be slightly cumbersome, usually requiring loops and conditional statements to handle different parameters, and it is not very friendly when dealing with numerical parameters.
Le `moduleparam` est un outil de traitement des paramètres en ligne de commande inspiré de l'implémentation des `moduleparam` dans le noyau Linux. Il est utilisable sur plusieurs plateformes, facile à utiliser, permet la conversion de différents types de paramètres, mais l'inconvénient est que chaque paramètre nécessite une variable correspondante pour le stockage.

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT, merci de laisser vos [**commentaires**](https://github.com/disenone/wiki_blog/issues/new)Pointer les éventuels oublis. 
