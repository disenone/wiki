---
layout: post
title: 'C/C++ : résumé de la gestion des paramètres de ligne de commande'
categories:
- c++
catalog: true
tags:
- dev
description: Pendant un moment, en parcourant le code source du noyau Linux, j'ai
  remarqué le traitement des paramètres de module (moduleparam) dans le noyau, et
  j'ai trouvé ça assez ingénieux, ce qui m'a donné envie d'étudier comment gérer de
  manière plus efficace les paramètres de ligne de commande en C.
figures:
- assets/post_assets/2016-11-19-aparsing/aparsing.png
---

<meta property="og:title" content="C/C++ 的命令行参数处理总结" />

![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/gcc-4.9-blue.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/clang-3.7-birghtgreen.svg){:style="display: inline-block"}

![](assets/img/2016-11-19-aparsing/aparsing.png)

Pendant une récente fouille du code source du noyau Linux, j'ai remarqué le traitement des paramètres de module (moduleparam) et l'ai trouvé très ingénieux. Cela m'a donné envie d'explorer comment améliorer la gestion des paramètres en ligne de commande en C. Vous pouvez trouver le code utilisé dans cet article [aparsing](https://github.com/disenone/aparsing)Le code peut être compilé et exécuté sous Windows, Linux et Mac OS X. Des instructions de compilation détaillées se trouvent dans le fichier README.md.

## getenv

(https://github.com/disenone/aparsing/blob/master/getenv/getenv_test.c)Please provide the text you would like to have translated into French.

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

La déclaration de la fonction `getenv` est comme suit [4](#__codelineno-0-5)(#__codelineno-0-10)和 [15](#__codelineno-0-15)Il s'agit de récupérer les valeurs de deux variables d'environnement séparément et, si les variables sont valides, d'imprimer leur valeur. Il est important de noter que `getenv` retourne toujours des chaînes de caractères, et il incombe à l'utilisateur de convertir manuellement ces valeurs en types numériques, ce qui n'est pas très pratique. Compilation et exécution :

Sous Windows :

``` bat
set GETENV_ADD=abc & set GETENV_NUM=1 & .\getenv_test.exe
```

Sous Linux :

``` shell
GETENV_ADD=abc GETENV_NUM=2 ./getenv_test 
```

Traduire ces textes en français :

```
GETENV_ADD = abc
GETENV_NUM = 2
```

## getopt

Linux provides us with a set of functions `getopt, getopt_long, getopt_long_only` to handle command line arguments passed to a program, the declarations of these three functions are:

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

Le programme `getopt` only works with short options (i.e., single-character options), whereas `getopt_long` and `getopt_long_only` can handle long options. For a detailed explanation of these functions, you can refer to the manual in Linux. Next, let's illustrate how to use `getopt` and `getopt_long` through examples.

Il est à noter que ces fonctions ne sont pas disponibles sous Windows. J'ai donc trouvé un code source compilable sous Windows, apporté quelques modifications mineures et tout le code se trouve [ici](https://github.com/disenone/aparsing/tree/master/getopt)I am sorry, but I am unable to translate the characters provided.

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

Analysons en détail l'utilisation de `getopt_long`. Les trois premiers paramètres de `getopt_long` sont identiques à ceux de `getopt`, à savoir : le nombre de paramètres en ligne de commande `argc`, le tableau des paramètres en ligne de commande `argv` et la forme spécifique des paramètres courts `optstring`. Le format de `optstring` consiste en des caractères de paramètres courts, suivis d'un deux-points `:` pour indiquer que le paramètre a un argument, et de deux deux-points `::` pour indiquer que l'argument est optionnel. Par exemple, à la ligne 19, nous déclarons la forme des paramètres courts : le paramètre `b` n'a pas d'argument supplémentaire, le paramètre `a` en a un, et le paramètre `c` a un argument optionnel.

Les deux derniers arguments de `getopt_long` sont utilisés pour gérer les options longues, où la structure de `option` est :

```c
struct option {
const char *name;       // Long nom de paramètre
int has_arg; // Indicates whether it has an additional parameter
int *flag;       // Specify how to return the function call result.
int         val;        // valeur retournée
};
```
Bien que ce soit un long paramètre, `name` peut toujours être défini avec une longueur de caractère unique.

`has_arg` peut être défini sur `no_argument, required_argument, optional_argument`, qui respectivement indiquent l'absence d'argument, un argument requis, un argument facultatif.

`flag` et `val` sont utilisés ensemble. Si `flag = NULL`, `getopt_long` retournera directement `val`. Sinon, si `flag` est un pointeur valide, `getopt_long` exécutera une opération similaire à `*flag = val`, en attribuant la valeur de `val` à la variable pointée par `flag`.

Si `getopt_long` trouve une correspondance avec un argument court, il renverra la valeur caractère de cet argument court. Si une correspondance est trouvée avec un argument long, il renverra `val` ( `flag = NULL` ) ou `0` ( `flag != NULL; *flag = val;` ) ; s'il rencontre un caractère qui n'est pas un argument, il renverra `?` ; une fois tous les arguments traités, il renverra `-1`.

En utilisant les caractéristiques des valeurs de retour, nous pouvons obtenir un effet équivalent entre les paramètres longs et courts. Par exemple, pour le premier paramètre `add` de `long_options`, si sa valeur `val` est définie sur le caractère du paramètre court `'a'`, alors lors de la vérification du retour, `--add` et `-a` entreront dans la même branche de traitement et seront considérés comme ayant le même sens.

Le dernier morceau du puzzle est l'utilisation de `optind` et `optarg`. `optind` indique la position du prochain paramètre à traiter dans `argv`, tandis que `optarg` pointe vers la chaîne de caractères des paramètres supplémentaires.

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

Les significations de `-a` et `--add` sont identiques. Les arguments optionnels des paramètres courts sont directement placés après, par exemple `-c4`, tandis que les arguments optionnels des paramètres longs doivent être suivis d'un signe égal, par exemple `--verbose=3`.

## mobuleparam

D'accord, nous voici enfin à la méthode initiale qui a déclenché cet article. Le noyau Linux utilise une approche plutôt astucieuse pour transmettre des paramètres aux modules du noyau, cette méthode est appelée `moduleparam`. Ici, je vais d'abord expliquer brièvement la manière dont le `moduleparam` du noyau Linux fonctionne ; une explication plus détaillée peut être trouvée dans le code. Bien que j'aie emprunté certaines méthodes de traitement du `moduleparam`, il y a quelques différences avec le `moduleparam` du noyau Linux. Pour faire la distinction, je vais appeler ma méthode `small moduleparam`, tandis que le noyau Linux continuera d’être désigné par `moduleparam`.

Voyons d'abord l'utilisation de `moduleparam`, en le déclarant dans le module :

```c
int enable_debug = 0;
module_param(enable_debug, int, 0);
```

Ensuite, entrez les paramètres lors du chargement du module :

```shell
$ insmod mod enable_debug=1
```

La variable `enable_debug` est correctement définie à `1`, ce qui la rend très pratique à utiliser. Peu de code supplémentaire est nécessaire, ce qui permet d'écrire un code concis et élégant. Plus besoin d'écrire de nombreuses boucles de conditions comme avec `getenv` et `getopt`, et en plus, elle effectue la conversion des types automatiquement. Alors, quand je la vois, je me dis que ce serait encore mieux si on pouvait l'utiliser pour traiter les arguments de ligne de commande.

Voyons maintenant l'implémentation principale de `moduleparam` :

```cpp linenums="1"
struct kernel_param {
const char *name;           // Variable name
u16 perm;                   // Variable access permission
u16 drapeaux;              // Variable de type booléen
param_set_fn set;           // str -> variable value
param_get_fn get;           // Value de la variable -> str
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

`module_param`' is a macro that actually creates a structure `kernel_param` which can reflect the incoming variables. This structure stores enough information to access and set the variables, around lines 20-24, and places the structure in a section called `__param` (`__section__ ("__param")`). Once the structure is saved, the kernel will, upon loading the module, locate the position of the `section __param` in the elf file and the number of structures, and then set the value of each parameter based on the name and `param_set_fn`. The method to locate a specific named section is platform-specific. The Linux kernel implementation involves processing elf files. Linux provides the `readelf` command to view information in elf files. Those interested can consult the `readelf` help information.

Le texte en question dit que l'approche du noyau Linux est spécifique à la plateforme, alors que je recherche une méthode qui soit indépendante de la plateforme pour gérer les paramètres. C'est pourquoi nous devons modifier légèrement l'approche originale de `moduleparam`, en supprimant la déclaration `__section__ ("__param")`, car nous n'avons pas besoin de lire les sections des fichiers elf de manière compliquée. Regardons donc comment utiliser la version modifiée :

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

Pour préserver la structure de chaque réflexion, j'ai ajouté une macro `init_module_param(num)` pour déclarer l'espace de stockage de la structure. `num` représente le nombre de paramètres. Si le nombre de paramètres déclarés dépasse `num`, le programme déclenchera une assertion d'erreur. La déclaration de `module_param` est légèrement différente de l'originale, le dernier paramètre représentant les autorisations d'accès est supprimé, aucune restriction d'autorisation n'est imposée. De plus, une nouvelle macro `module_param_bool` est ajoutée pour traiter les variables booléennes, ce qui n'est pas nécessaire dans les versions de Linux car elles utilisent la fonction intégrée de gcc `__builtin_types_compatible_p` pour déterminer le type de variable. Malheureusement, cette fonction n'est pas présente dans MSVC, donc j'ai dû supprimer cette fonctionnalité et ajouter une macro à la place. `module_param_array` et `module_param_string` sont utilisés pour traiter les tableaux et les chaînes de caractères respectivement. Ces deux fonctionnalités étaient également présentes dans la version originale.

La déclaration des paramètres est terminée, il s'agit maintenant de traiter les paramètres entrants. Utilisez la macro `parse_params` et passez `argc, argv`. Le troisième paramètre est un pointeur vers une fonction de rappel pour le traitement des paramètres inconnus ; vous pouvez passer `NULL`, auquel cas les paramètres positionnels interrompront le traitement des paramètres et renverront un code d'erreur.

Compiler et exécuter le code :

```
.\moduleparam_test.exe error=0 test=101 btest=1 latest=1,2,3 strtest=\"Hello World!\"
Parsing ARGS: error=0 test=101 btest=1 latest=1,2,3 strtest="Hello World!"
find unknown param: error
test = 101
btest = Y
latest = 1,2,3
strtest = Hello World!
```

On peut voir que les valeurs numériques, les tableaux et les chaînes de caractères peuvent être correctement lues et converties au bon format. Si un paramètre ne peut pas être converti au bon format, un code d'erreur sera renvoyé et les informations pertinentes seront affichées. Il est très simple d'ajouter quelques lignes de code pour lire et traiter les paramètres, ce qui rend son utilisation élégante. Pour une implémentation plus détaillée, vous pouvez directement consulter le code [ici](https://github.com/disenone/aparsing).

##Résumé

Cette fois-ci, nous avons récapitulé les trois méthodes de traitement des arguments de ligne de commande sous C/C++ : `getenv`, `getopt` et `moduleparam`. Chaque méthode a ses propres caractéristiques, vous pourrez donc choisir la méthode appropriée en fonction de vos besoins réels à l'avenir.

La fonction `getenv` est native, compatible avec plusieurs plates-formes, et peut être utilisée directement. Cependant, elle est assez primitive car elle utilise des variables d'environnement, ce qui peut polluer l'environnement. Il est préférable de nettoyer les variables d'environnement inutiles avant chaque utilisation pour éviter la pollution causée par les réglages précédents.
`getopt` is natively supported on the Linux platform but not on Windows, so including implementation code is necessary for cross-platform usage. The parameter passing follows the standard of Linux command line parameters, supporting optional parameters, but it is slightly cumbersome to use. Typically, it requires looping and conditional statements to handle different parameters and is not very friendly with numerical parameters.
Le `moduleparam` est un outil de gestion des paramètres en ligne de commande inspiré de l'implémentation `moduleparam` du noyau Linux. Il est compatible avec plusieurs plates-formes, facile à utiliser, capable de convertir des paramètres de différents types, mais nécessite une variable de stockage pour chaque paramètre.

--8<-- "footer_fr.md"


> Ce post a été traduit avec ChatGPT, merci de donner votre [**retour**](https://github.com/disenone/wiki_blog/issues/new)Veuillez indiquer toute omission. 
