---
layout: post
title: Analyse de la programmation des macros en C/C++
categories:
- c++
catalog: true
tags:
- dev
description: L'objectif de cet article est d'expliquer clairement les règles et les
  méthodes de mise en œuvre de la programmation de macros en C/C++, afin que vous
  ne craigniez plus de voir des macros dans le code.
figures: []
---

<meta property="og:title" content="C/C++ 宏编程解析" />

L'objectif de cet article est d'expliquer les règles et les méthodes de mise en œuvre de la programmation macro en C/C++, afin que vous ne craigniez plus de voir des macros dans le code. Je vais d'abord aborder les règles de l'expansion des macros mentionnées dans la norme C++14, puis nous observerons l'expansion des macros en modifiant le code source de Clang, et enfin, nous discuterons de la mise en œuvre de la programmation macro sur la base de ces connaissances.

Le code de cet article se trouve ici : [Télécharger](assets/img/2021-3-31-cpp-preprocess/macros.cpp)，[démonstration en ligne](https://godbolt.org/z/coWvc5Pse)Je vous prie d'ajouter du texte à traduire.

##引子

Nous pouvons utiliser la commande `gcc -P -E a.cpp -o a.cpp.i` pour demander au compilateur d'effectuer uniquement le prétraitement du fichier `a.cpp` et de sauvegarder le résultat dans `a.cpp.i`.

Tout d'abord, commençons par examiner quelques exemples :

####Récursivité réentrante

``` cpp
#define ITER(arg0, arg1) ITER(arg1, arg0)

ITER(1, 2)          // -> ITER(2, 1)
```

Le macro `ITER` a échangé les positions de `arg0` et `arg1`. Après le développement du macro, on obtient `ITER(2, 1)`.

On peut voir que les positions de `arg0` et `arg1` ont été échangées avec succès. Ici, le macro s'est développé une fois, mais il ne se développe plus de manière récursive. En d'autres termes, pendant le processus de développement du macro, il n'est pas autorisé à se réentrer. Si, lors d'un processus récursif, on découvre qu'un même macro a déjà été développé dans une récursion précédente, alors il ne se développera plus. C'est l'une des règles importantes du développement des macros. La raison pour interdire la réentrance récursive est également très simple : c'est pour éviter une récursivité infinie.

####Concaténation de chaînes de caractères

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                // -> HelloWorld
CONCAT(Bonjour, CONCAT(Monde, !))     // -> BonjourCONCAT(Monde, !)
```

Le macro `CONCAT` vise à concaténer `arg0` et `arg1`. Une fois la macro développée, `CONCAT(Hello, World)` devrait donner le résultat correct `HelloWorld`. Cependant, `CONCAT(Hello, CONCAT(World, !))` ne développe que la macro extérieure. La macro interne `CONCAT(World, !)` n'est pas développée mais simplement concaténée à `Hello`, ce qui diffère de nos attentes. Le résultat souhaité est `HelloWorld!`. C'est une autre règle importante du développement des macros : les paramètres de macro suivant l'opérateur `##` ne sont pas développés, mais directement concaténés au contenu précédent.

À travers les deux exemples ci-dessus, on peut voir que les règles de développement des macros peuvent parfois sembler contre-intuitives. Si l'on ne comprend pas exactement ces règles, il est possible que les macros écrites n'aient pas l'effet que nous souhaitons obtenir.

##Règles de développement macroscopique

À travers les deux exemples d'introduction, nous comprenons que l'expansion des macros obéit à un ensemble de règles standard définies dans les normes C/C++. Ces règles sont succinctement exposées et il est recommandé de les lire attentivement. Je vous propose également le lien vers la version n4296 de la norme pour référence, la section 16.3 traite de l'expansion des macros : [lien](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4296.pdf)Voici quelques règles importantes extraites de la version n4296, qui détermineront comment écrire correctement des macros (il est recommandé de prendre le temps de lire attentivement les macros dans le standard).

####Paramètre séparé

Les paramètres de la macro doivent être séparés par des virgules, et le nombre de paramètres doit être conforme au nombre de définitions de la macro. Dans les paramètres transmis à la macro, tout élément supplémentaire entre parenthèses est considéré comme un seul paramètre. Les paramètres peuvent être vides.

``` cpp
#define ADD_COMMA(arg1, arg2) arg1, arg2

ADD_COMMA(a, b)             // -> a, b
ADD_COMMA(a)                // Erreur "la macro "MACRO" nécessite 2 arguments, mais seulement 1 a été fourni"
ADD_COMMA((a, b), c)        // -> (a, b), c
ADD_COMMA(, b)              // -> , b
```

`ADD_COMMA((a, b), c)` considère `(a, b)` comme le premier paramètre. Dans `ADD_COMMA(, b)`, le premier paramètre est vide, ce qui se développe en `, b`.

####Développement des paramètres macro

Lorsque vous développez un macro, si les paramètres de la macro peuvent également être développés, les paramètres seront d'abord complètement développés avant de développer la macro, par exemple

``` cpp
ADD_COMMA(ADD_COMMA(1, 2), ADD_COMMA(3, 4))     // -> 1, 2, 3, 4
```

En règle générale, l'expansion des macros peut être considérée comme une évaluation des paramètres d'abord, puis une évaluation de la macro, sauf lorsqu'on rencontre les opérateurs `#` et `##`.

####`#` Opérateur

Les arguments de macro suivant l'opérateur `#` ne seront pas déroulés, mais directement transformés en chaînes de caractères, par exemple :

``` cpp
#define STRINGIZE(arg0) # arg0

STRINGIZE(a)                // -> "a"
STRINGIZE(STRINGIZE(a))     // -> "STRINGIZE(a)"
```

Selon cette règle, `STRINGIZE(STRINGIZE(a))` ne peut être développé qu'en `"STRINGIZE(a)"`.

###### opérateur

`##` Les paramètres de macro avant et après l'opérateur ne seront pas développés, mais seront d'abord concaténés, par exemple :

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                        // -> HelloWorld
CONCAT(Hello, CONCAT(World, !))             // -> HelloCONCAT(World, !)
CONCAT(CONCAT(Hello, World) C, ONCAT(!))    // -> CONCAT(Hello, World) CONCAT(!)
```

`CONCAT(CONCAT(Hello, World) C, ONCAT(!))` ne peut être que combiné ensemble pour obtenir `CONCAT(Hello, World) CONCAT(!)`.

####Balayage répété

Le préprocesseur, après avoir effectué un premier développement de macros, va rescanner le contenu obtenu et continuer à élargir, jusqu'à ce qu'il n'y ait plus rien à développer.

Une expansion complète d'une macro peut être comprise comme l'étape où les paramètres sont complètement développés (sauf en cas de rencontre avec `#` et `##`), puis, en fonction de la définition de la macro, la macro et les paramètres entièrement développés sont remplacés selon la définition, en traitant ensuite tous les opérateurs `#` et `##` présents dans la définition.

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define STRINGIZE(arg0) # arg0

CONCAT(STRING, IZE(Hello))        // -> STRINGIZE(Hello) -> "Hello"
```

`CONCAT(STRING, IZE(Hello))` La première analyse se développe en `STRINGIZE(Hello)`, puis lors de la deuxième analyse, il est découvert que `STRINGIZE` peut être développé à nouveau, pour finalement obtenir `"Hello"`.

####Interdiction de la récursion réentrante

Dans le processus de l'analyse répété, il est interdit de déplier de manière récursive les mêmes macros. On peut comprendre le déploiement des macros comme une structure en arbre, où le nœud racine est la macro à déplier initialement, et chaque contenu déployé d'une macro est connecté à l'arbre en tant que nœud enfant de cette macro. Ainsi, interdire la récursivité signifie que lors du déploiement d'une macro enfant, si celle-ci est identique à une macro de n'importe quel nœud ancêtre, son déploiement est prohibé. Regardons quelques exemples :

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define CONCAT_SPACE(arg0, arg1) arg0 arg1
#define IDENTITY(arg0) IDENTITY_IMPL(arg0)
#define IDENTITY_IMPL(arg0) arg0

CONCAT(CON, CAT(a, b))                  // -> CONCAT(a, b)
IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))   // -> CONCAT(a, b)
IDENTITY(CONCAT(CON, CAT(a, b)))        // -> IDENTITY_IMPL(CONCAT(a, b)) -> CONCAT(a, b)
```

`CONCAT(CON, CAT(a, b))`：Given that `CONCAT` concatenates two parameters using `##`, according to the rules of `##`, it does not expand the parameters but concatenates them directly. Therefore, the first expansion results in `CONCAT(a, b)`. Since `CONCAT` has already been expanded and does not recursively expand further, it stops.

`IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))` : `IDENTITY_IMPL` peut être compris comme l'évaluation du paramètre `arg0`, où l'évaluation du paramètre `arg0` donne `CONCAT(a, b)`. En raison de la récursivité, cela est marqué comme interdisant la réentrance. Ensuite, `IDENTITY_IMPL` se développe et lors du second scan, il découvre que c'est `CONCAT(a, b)` qui est interdit de réentrer, il s'arrête donc de se développer. Ici, `CONCAT(a, b)` est obtenu par l'expansion du paramètre `arg0`, mais lors des expansions suivantes, le marquage d'interdiction de réentrance sera également maintenu, ce qui peut être compris comme le nœud parent étant le paramètre `arg0`, conservant toujours le marquage d'interdiction de réentrance.

`IDENTITY(CONCAT(CON, CAT(a, b)))` : Cet exemple vise principalement à renforcer la compréhension des nœuds parents et enfants. Lorsque les paramètres sont déroulés, le paramètre en lui-même agit en tant que nœud parent, et le contenu déroulé agit comme un nœud enfant pour déterminer la récursivité. Une fois que les paramètres sont déroulés et transmis à la macro-définition, les indicateurs d'interdiction de réentrance continueront à être conservés (si les paramètres déroulés n'ont pas été modifiés après transmission à la macro-définition). Le processus de déroulement des paramètres peut être considéré comme un autre arbre, où le résultat du déroulement des paramètres correspond à la couche la plus profonde de l'arbre, et cette couche est transmise à la macro pour être exécutée tout en conservant la caractéristique d'interdiction de réentrance.

Par exemple ici, après le premier déploiement complet, `IDENTITY_IMPL(CONCAT(a, b))` est obtenu, `CONCAT(a, b)` est marqué comme interdit de réentrer, même si `IDENTITY_IMPL` évalue les paramètres, mais les paramètres sont interdits de déploiement, donc les paramètres sont transmis intacts à la définition, finalement nous obtenons `CONCAT(a, b)`.

J'ai simplement énuméré quelques règles que je considère importantes ou pas très faciles à comprendre. Pour une explication détaillée de ces règles, je vous recommande de consacrer du temps à consulter directement le document standard.

##Observer le processus de dépliage à travers Clang.

Nous pouvons ajouter quelques messages d'impression au code source de Clang pour observer le processus d'expansion des macros. Je n'ai pas l'intention d'expliquer en profondeur le code source de Clang, ici je fournis un fichier diff modifié. Ceux qui sont intéressés peuvent compiler Clang eux-mêmes pour l'étudier. Ici, j'utilise la version 11.1.0 de llvm ([lien](https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-11.1.0.tar.gz)），fichier modifié（[portail](assets/img/2021-3-31-cpp-preprocess/clang-modify.zip)"）。Pour vérifier les règles d'expansion des macros que nous avons précédemment introduites, passons rapidement à travers un exemple :"

####Translate these text into French language:

Exemple 1

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(C, ONCAT(a, b))      // CONCAT(a, b)
```

Utilisez Clang modifié pour prétraiter le code ci-dessus : `clang -P -E a.cpp -o a.cpp.i`, et obtenez les informations d'impression suivantes :

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

Translate these text into French language:

第 [1](#__codelineno-9-1)Lorsqu'il rencontre un macro, `HandleIdentifier` imprime cela, puis imprime les informations du macro (page [2-4](#__codelineno-9-2)`Macro is ok to expand` après avoir vérifié que `Macro` n'est pas désactivé, il est possible de le développer conformément à sa définition, puis de passer à `EnterMacro`.

La fonction qui exécute réellement l'expansion des macros est `ExpandFunctionArguments`, puis les informations sur la macro à développer sont à nouveau imprimées, notant qu'à ce stade, la macro a déjà été marquée comme `used` (numéro [9](#__codelineno-9-9)Ensuite, selon la définition de la macro, nous procédons à l'expansion de chaque `Token` (le `Token` est un concept dans le préprocesseur de `Clang`, nous n'entrerons pas dans les détails ici).

Le premier `Token` est l'argument `arg0`, correspondant à `C`, sans besoin d'être développé, donc il est directement copié dans le résultat (lignes [11-13](#__codelineno-9-11)Parcours professionnel.

(#__codelineno-9-14)行）。

Le deuxième `Token` est le paramètre formel `arg1`, correspondant à l'argument effectif `ONCAT(a, b)`. Le préprocesseur traitera également l'argument effectif en un ensemble de `Token`, d'où l'impression des résultats entre crochets pour chaque `Token` de l'argument effectif (ligne 18). En raison de l'opérateur `##`, cet argument effectif n'a pas besoin d'être développé, il est donc directement copié dans le résultat (lignes [16-18](#__codelineno-9-16)行）。

Enfin, "Leave ExpandFunctionArguments" imprime les résultats de la dernière expansion de numérisation (page [19](#__codelineno-9-19)En le faisant, traduire tous les `Token` du résultat nous donne `C ## ONCAT(a, b)`, puis le préprocesseur exécute l'opérateur `##` pour générer un nouveau contenu.

Après exécution, on obtient `CONCAT(a, b)`. Lorsqu'on rencontre la macro `CONCAT`, le préprocesseur entre d'abord dans `HandleIdentifier`, imprime les informations sur la macro, et remarque que son état est `disable used`, ce qui signifie qu'elle a déjà été développée et ne peut pas être appelée à nouveau. On affiche alors `Macro is not ok to expand`, et le préprocesseur cesse l'expansion, aboutissant ainsi à `CONCAT(a, b)`.

####Translate these text into French language:

 Exemple 2

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define IDENTITY(arg0) arg0

IDENTITY(CONCAT(C, ONCAT(a, b)))
```

<details>
Résumé: Clang imprime des informations (cliquez pour développer).
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

Translate these text into French language:

第 [12](#__codelineno-11-12)La ligne commence à se déployer `IDENTITY`, découvrant que le paramètre `Token 0` est `CONCAT(...)`, qui est aussi un macro, donc nous allons d'abord évaluer ce paramètre.

Le [27](#__codelineno-11-27)(#__codelineno-11-46)Translatez ce texte en français, s'il vous plaît : "行）".

Numéro [47](#__codelineno-11-47)Arrêt de l'expansion de `IDENTITY`, le résultat obtenu est `CONCAT(a, b)`.

Translate these text into French language:

第 [51](#__codelineno-11-51)Re-analysez `CONCAT(a, b)` et constatez qu' même s'il s'agit d'une macro, elle a été définie comme `utilisée` lors du processus de déploiement des paramètres précédents, elle ne sera donc plus développée récursivement et sera directement utilisée comme résultat final.

####Translate these text into French language:

例子 3

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

Translate these text into French language:

* 第 [16](#__codelineno-13-16)Commencer à déployer `IDENTITY`, le préprocesseur voit que `Token 2` (c'est-à-dire `arg0`) est une macro, il déploie donc d'abord `CONCAT(C, ONCAT(a, b))`.

Déplier "arg0" donne "CONCAT(a, b)" (de [23-54](#__codelineno-13-23)行）

* `IDENTITY` se développe finalement en `IDENTITY_IMPL(CONCAT(a, b))` (page [57](#__codelineno-13-57)行）

Re-scan, continue expanding `IDENTITY_IMPL` (lines [61-72](#__codelineno-13-61)(#__codelineno-13-85)(Caractère non traduit.)

* En réanalyzant les résultats, on constate que l'état de la macro `CONCAT(a, b)` est `used`, on arrête l'expansion et on obtient le résultat final.

À travers ces trois exemples simples, nous pouvons comprendre de manière générale le processus d'expansion des macros par le préprocesseur. Nous n'allons pas approfondir davantage le sujet du préprocesseur ici, mais ceux qui sont intéressés peuvent étudier en se référant aux fichiers modifiés que j'ai fournis.

##Programmation macro.

Nous allons maintenant entrer dans le vif du sujet (le long paragraphe précédent avait pour but de mieux comprendre les règles d'expansion de macro), la mise en œuvre de la programmation par macros.

####Symbole de base

Tout d'abord, on peut définir les symboles spéciaux des macros, qui seront utilisés lors de l'évaluation et de la concaténation.

``` cpp
#define PP_LPAREN() (
#define PP_RPAREN() )
#define PP_COMMA() ,
#define PP_EMPTY()
#définir PP_HASHHASH # ## #      // représente ## chaîne de caractères, mais seulement en tant que chaîne, ne sera pas traité comme un ## opérateur
```

####Évaluation-demande

En utilisant les règles de déroulement des paramètres en priorité, il est possible d'écrire une macro d'évaluation :

``` cpp
#define PP_IDENTITY(arg0) arg0

PP_COMMA PP_LPAREN() PP_RPAREN()                // -> PP_COMMA ( )
PP_IDENTITY(PP_COMMA PP_LPAREN() PP_RPAREN())   // -> PP_COMMA() -> ,
```

Si l'on se limite à écrire `PP_COMMA PP_LPAREN() PP_RPAREN()`, le préprocesseur traitera chaque macro séparément et ne combinera pas les résultats développés. En ajoutant `PP_IDENTITY`, le préprocesseur peut évaluer `PP_COMMA()` obtenu par développement pour obtenir `,`.


####Assembler

Puisque lors de la concaténation avec `##`, les paramètres de gauche et de droite ne sont pas évalués, pour permettre aux paramètres d'être évalués avant la concaténation, on peut écrire comme ceci :

``` cpp
#define PP_CONCAT(arg0, arg1) PP_CONCAT_IMPL(arg0, arg1)
#define PP_CONCAT_IMPL(arg0, arg1) arg0 ## arg1

PP_CONCAT(PP_IDENTITY(1), PP_IDENTITY(2))         // -> 12
PP_CONCAT_IMPL(PP_IDENTITY(1), PP_IDENTITY(2))    // -> PP_IDENTITY(1)PP_IDENTITY(2) -> Erreur
```

Ici, la méthode utilisée par `PP_CONCAT` s'appelle la concaténation différée. Lorsqu'elle est déployée en `PP_CONCAT_IMPL`, `arg0` et `arg1` seront tous deux déployés et évalués en premier lieu, puis `PP_CONCAT_IMPL` effectuera l'opération de concaténation réelle.

####Opération logique

Avec `PP_CONCAT`, il est possible d'effectuer des opérations logiques. Commencez par définir la valeur `BOOL` :


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

Utilisez d'abord `PP_CONCAT` pour assembler `PP_BOOL_` et `arg0` ensemble, puis évaluez le résultat de l'assemblage. Ici, `arg0` doit être un chiffre dans la plage de `[0, 256]` après évaluation, assemblez-le après `PP_BOOL_` pour obtenir une valeur booléenne. Opérations booléennes : et, ou, non :

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

Utilisez d'abord `PP_BOOL` pour évaluer les paramètres, puis combinez les résultats des opérations logiques en fonction de la combinaison `0 1`. Si vous n'utilisez pas `PP_BOOL` pour l'évaluation, les paramètres ne prendront en charge que les valeurs `0 1`, ce qui réduit considérablement leur polyvalence. De la même manière, vous pouvez également écrire des opérations telles que XOR, OR, NOT, etc. Si vous êtes intéressé, vous pouvez les essayer vous-même.

####Sélection des conditions

En utilisant `PP_BOOL` et `PP_CONCAT`, il est également possible d'écrire des instructions de sélection conditionnelle :

``` cpp
#define PP_IF(if, then, else) PP_CONCAT(PP_IF_, PP_BOOL(if))(then, else)
#define PP_IF_1(then, else) then
#define PP_IF_0(then, else) else

PP_IF(1, 2, 3)      // -> PP_IF_1(2, 3) -> 2
PP_IF(0, 2, 3)      // -> PP_IF_0(2, 3) -> 3
```

Si la valeur de `if` est `1`, concaténez avec `PP_CONCAT` pour former `PP_IF_1`, puis développez en la valeur de `then` ; de même, si la valeur de `if` est `0`, obtenez `PP_IF_0`.

####augmentation diminuation

Les entiers en augmentation ou en diminution :

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

Tout comme pour `PP_BOOL`, l'incrémentation et la décrémentation des entiers sont également soumises à des limites. Dans ce cas, la plage est définie sur `[0, 256]`. En atteignant `256`, pour des raisons de sécurité, `PP_INC_256` renverra `256` comme limite. De même, `PP_DEC_0` renverra `0`.

####paramètres de longueur variable

Les macros peuvent accepter des paramètres de longueur variable, le format est :

```cpp
#define LOG(format, ...) printf("log: " format, __VA_ARGS__)

LOG("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG("Bonjour le monde")              // -> printf("log: " "Bonjour le monde", ); 多了个逗号，编译报错
```

En raison de la possibilité que les arguments variables soient vides, ce qui peut entraîner un échec de la compilation, C++ 20 a introduit `__VA_OPT__`. Si les arguments variables sont vides, il renvoie vide, sinon il renvoie les arguments d'origine :

```cpp
#define LOG2(format, ...) printf("log: " format __VA_OPT__(,) __VA_ARGS__)

LOG2("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG2("Bonjour le monde")              // -> printf("log: " "Bonjour le monde" ); pas de virgule, compilation normale
```

Mais il est dommage que ce macro ne soit disponible qu'à partir de la norme C++ 20. Dans ce qui suit, nous allons donner la méthode d'implémentation de `__VA_OPT__`.

####évaluation paresseuse

Considérez cette situation :

``` cpp
PP_IF(1, PP_COMMA(), PP_LPAREN())     // -> PP_IF_1(,,)) -> erreur : liste d'arguments non terminée lors de l'invocation de la macro "PP_IF_1"
```

Nous savons que lors de l'expansion macro, les arguments initiaux sont évalués. Après l'évaluation de `PP_COMMA()` et `PP_LPAREN()`, ils sont ensuite transmis à `PP_IF_1`, ce qui donne `PP_IF_1(,,))`, provoquant une erreur de prétraitement. À ce stade, il est possible d'utiliser une méthode appelée évaluation paresseuse :

``` cpp
PP_IF(1, PP_COMMA, PP_LPAREN)()       // -> PP_IF_1(PP_COMMA, PP_LPAREN)() -> PP_COMMA() -> ,
```

Modifiez cela en utilisant cette écriture, en ne transmettant que le nom de la macro, permettant à `PP_IF` de sélectionner les noms de macros nécessaires, puis en les concaténant avec des parenthèses `()` pour former la macro complète, avant de l'expandre finalement. L'évaluation paresseuse est également très courante dans la programmation de macros.

####以括号开始

Déterminez si les paramètres de longueur variable commencent par une parenthèse :

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

`PP_IS_BEGIN_PARENS` peut être utilisé pour déterminer si les paramètres passés commencent par une parenthèse, ce qui est nécessaire lors du traitement des paramètres entre parenthèses (comme dans l'implémentation de `__VA_OPT__` mentionnée plus tard). Cela peut sembler un peu complexe, mais l'idée principale est de construire un macro qui, si les paramètres à longueur variable commencent par une parenthèse, peut être associés à la parenthèse pour obtenir un résultat, sinon, un autre calcul sera fait pour obtenir un résultat différent. Regardons cela de plus près :

La fonction de la macro composée de `PP_IS_BEGIN_PARENS_PROCESS` et `PP_IS_BEGIN_PARENS_PROCESS_0` consiste d'abord à évaluer les paramètres variables passés, puis à prendre le 0ème paramètre.

`PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__)` signifie évaluer d'abord `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__`, puis concaténer le résultat de l'évaluation avec `PP_IS_BEGIN_PARENS_PRE_`.

La macro `PP_IS_BEGIN_PARENS_EAT(...)` va avaler tous les arguments, renvoyer 1 si dans l'étape précédente `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__`, `__VA_ARGS__` commence par une parenthèse, alors il y aura un match avec l'évaluation de `PP_IS_BEGIN_PARENS_EAT(...)`, puis renvoyer `1`; sinon, s'il ne commence pas par une parenthèse, il n'y aura pas de correspondance et `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` restera inchangé.

Si `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` renvoie `1`, alors `PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, 1) -> PP_IS_BEGIN_PARENS_PRE_1 -> 1`, notez que le `1` est suivi d'une virgule, passez `1,` à `PP_IS_BEGIN_PARENS_PROCESS_0`, prenez le 0ème paramètre, et finalement obtenez `1`, ce qui indique que le paramètre commence par une parenthèse.

Si `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` évalue à quelque chose d'autre que `1`, mais reste inchangé, alors `PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__) -> PP_IS_BEGIN_PARENS_PRE_PP_IS_BEGIN_PARENS_EAT __VA_ARGS__ -> 0, __VA_ARGS__`. En passant cela à `PP_IS_BEGIN_PARENS_PROCESS_0`, le résultat sera `0`, ce qui indique que l'argument ne commence pas par une parenthèse.

####Paramètres variables vides

Déterminer si les paramètres de longueur variable sont vides est également une macro courante, utilisée lors de l'implémentation de `__VA_OPT__`. Ici, nous pouvons utiliser `PP_IS_BEGIN_PARENS` et d'abord écrire une version incomplète :

``` cpp
#define PP_IS_EMPTY_PROCESS(...) \
    PP_IS_BEGIN_PARENS(PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ())
#define PP_IS_EMPTY_PROCESS_EAT(...) ()

PP_IS_EMPTY_PROCESS()       // -> 1
PP_IS_EMPTY_PROCESS(1)      // -> 0
PP_IS_EMPTY_PROCESS(1, 2)   // -> 0
PP_IS_EMPTY_PROCESS(())     // -> 1
```

Le rôle de `PP_IS_EMPTY_PROCESS` est de déterminer si `PP_IS_EMPTY_PROCESS __VA_ARGS__()` commence par des parenthèses.

Si `__VA_ARGS__` est vide, `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ () -> PP_IS_EMPTY_PROCESS_EAT() -> ()`, on obtient une paire de parenthèses `()`, qui est ensuite passée à `PP_IS_BEGIN_PARENS`, retournant `1`, ce qui indique que le paramètre est vide.

Sinon, `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ()` est transmis tel quel à `PP_IS_BEGIN_PARENS`, renvoyant 0, ce qui indique qu'il n'est pas vide.

Notez le quatrième exemple `PP_IS_EMPTY_PROCESS(()) -> 1`. `PP_IS_EMPTY_PROCESS` ne peut pas traiter correctement les arguments de longueur variable qui commencent par une parenthèse, car dans ce cas, la parenthèse apportée par les arguments de longueur variable va correspondre à `PP_IS_EMPTY_PROCESS_EAT`, ce qui conduit à ce que l'évaluation donne `()`. Pour résoudre ce problème, nous devons traiter différemment les cas où les arguments commencent par une parenthèse.

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

`PP_IS_EMPTY_IF` renvoie le 0ème ou le 1er paramètre en fonction de la condition `if`.

Si les arguments variadiques passant sont entourés de parenthèses, `PP_IS_EMPTY_IF` renvoie `PP_IS_EMPTY_ZERO`, et finalement renvoie `0`, indiquant que les arguments variadiques ne sont pas vides.

À l'inverse, `PP_IS_EMPTY_IF` retourne `PP_IS_EMPTY_PROCESS`, qui détermine finalement si les arguments de longueur variable sont non vides.

####Accès par indice

Obtenir l'élément à la position spécifiée des paramètres de longueur variable :

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

Le premier argument de `PP_ARGS_ELEM` est l'indice de l'élément `I`, suivi d'arguments de longueur variable. En utilisant `PP_CONCAT` pour concaténer `PP_ARGS_ELEM_` et `I`, on peut obtenir la macro `PP_ARGS_ELEM_0..8` renvoyant l'élément situé à la position correspondante, puis transmettre les arguments de longueur variable à cette macro pour déplier et renvoyer l'élément correspondant à l'indice.

#### PP_IS_EMPTY2

En utilisant `PP_ARGS_ELEM`, il est également possible de mettre en œuvre une autre version de `PP_IS_EMPTY` :

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

Utilisez `PP_ARGS_ELEM` pour vérifier si les arguments contiennent une virgule avec `PP_HAS_COMMA`. `PP_COMMA_ARGS` consommera n'importe quels arguments fournis et renverra une virgule.

La logique de base pour déterminer si les paramètres de longueur variable sont vides est que `PP_COMMA_ARGS __VA_ARGS__ ()` renvoie une virgule, ce qui signifie que `__VA_ARGS__` est vide. `PP_COMMA_ARGS` et `()` sont évalués ensemble, la formulation concrète étant `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ())`.

Cependant, il peut y avoir des exceptions :

* `__VA_ARGS__` peut lui-même contenir des virgules ;
* `__VA_ARGS__ ()` la concaténation entraîne une évaluation et produit une virgule ;
* `PP_COMMA_ARGS __VA_ARGS__` est concaténé ensemble, provoquant une évaluation qui entraîne une virgule ;

Pour les trois cas exceptionnels mentionnés ci-dessus, il est nécessaire de les exclure, donc la dernière écriture est équivalente à l'exécution d'une logique "ET" sur les quatre conditions suivantes :

* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__))` &&
* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__()))` &&
* `PP_NOT(PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__))` &&
* `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ())`

#### `__VA_OPT__`

Utiliser `PP_IS_EMPTY` permet enfin de réaliser un macro similaire à `__VA_OPT__`:

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

`PP_ARGS_OPT` accepte deux paramètres fixes et des paramètres de longueur variable. Lorsque les paramètres de longueur variable ne sont pas vides, il retourne `data`, sinon il retourne `empty`. Afin de permettre à `data` et `empty` de supporter la virgule, il est requis d'encapsuler les deux dans des parenthèses. Enfin, utilisez `PP_REMOVE_PARENS` pour enlever les parenthèses externes.

Avec `PP_ARGS_OPT`, vous pouvez implémenter `LOG3` pour simuler les fonctionnalités réalisées par `LOG2`:

``` cpp
#define LOG3(format, ...) \
    printf("log: " format PP_ARGS_OPT((,), (), __VA_ARGS__) __VA_ARGS__)

LOG3("Hello");                  // -> printf("log: " "Hello" );
LOG3("Hello %s", "World");      // -> printf("log: " "Hello %s" , "World");
```

`data_tuple` est `(,)`, si les paramètres de longueur variable ne sont pas vides, toutes les éléments de `data_tuple`, ici ce sont des virgules `,`, seront retournés.

####Demander le nombre de paramètres

Obtenir le nombre de paramètres de longueur variable :

``` cpp
#define PP_ARGS_SIZE_IMCOMPLETE(...) \
    PP_ARGS_ELEM(8, __VA_ARGS__, 8, 7, 6, 5, 4, 3, 2, 1, 0)

PP_ARGS_SIZE_IMCOMPLETE(a)             // -> 1
PP_ARGS_SIZE_IMCOMPLETE(a, b)          // -> 2
PP_ARGS_SIZE_IMCOMPLETE(PP_COMMA())    // -> 2
PP_ARGS_SIZE_IMCOMPLETE()              // -> 1
```

Le nombre de paramètres de longueur variable est obtenu par la position des paramètres. `__VA_ARGS__` entraîne un décalage vers la droite de tous les paramètres suivants. On utilise la macro `PP_ARGS_ELEM` pour obtenir le paramètre à la 8ème position ; si `__VA_ARGS__` ne contient qu'un seul paramètre, alors le 8ème paramètre est égal à `1` ; de même, si `__VA_ARGS__` contient deux paramètres, le 8ème paramètre devient `2`, ce qui équivaut exactement au nombre de paramètres de longueur variable.

Les exemples fournis ici ne prennent en charge que jusqu'à 8 arguments de longueur variable, en fonction de la longueur maximale prise en charge par `PP_ARGS_ELEM`.

Cependant, ce macro n'est pas complet; dans le cas où les paramètres de longueur variable sont vides, ce macro retournera incorrectement `1`. Si vous devez traiter des paramètres de longueur variable vides, vous devez utiliser le macro `PP_ARGS_OPT` que nous avons mentionné précédemment :

``` cpp
#define PP_COMMA_IF_ARGS(...) PP_ARGS_OPT((,), (), __VA_ARGS__)
#define PP_ARGS_SIZE(...) PP_ARGS_ELEM(8, __VA_ARGS__ PP_COMMA_IF_ARGS(__VA_ARGS__) 8, 7, 6, 5, 4, 3, 2, 1, 0, 0, 0)

PP_ARGS_SIZE(a)             // -> 1
PP_ARGS_SIZE(a, b)          // -> 2
PP_ARGS_SIZE(PP_COMMA())    // -> 2
PP_ARGS_SIZE()              // -> 0
PP_ARGS_SIZE(,,,)           // -> 4
```

Le point clé du problème est la virgule `,`. Lorsque `__VA_ARGS__` est vide, omettre la virgule permet de renvoyer correctement `0`.

####parcours d'accès

Semblable à `for_each` en C++, nous pouvons implémenter le macro `PP_FOR_EACH` :

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

`PP_FOR_EACH` reçoit deux paramètres fixes : `macro`, que l'on peut comprendre comme le macro appelé lors de l'itération, et `contex`, qui peut être utilisé comme paramètre à valeur fixe pour passer à `macro`. `PP_FOR_EACH` commence par obtenir la longueur des paramètres variable avec `PP_ARGS_SIZE`, que l'on appelle `N`, puis utilise `PP_CONCAT` pour assembler et obtenir `PP_FOR_EACH_N`. Ensuite, `PP_FOR_EACH_N` appellera de manière itérative `PP_FOR_EACH_N-1` pour réaliser un nombre d'itérations égal au nombre de paramètres variables.

Dans cet exemple, nous avons déclaré `DECLARE_EACH` en tant que paramètre du `macro`. L'objectif de `DECLARE_EACH` est de renvoyer `contex arg`. Si `contex` est un nom de type et `arg` est un nom de variable, alors `DECLARE_EACH` peut être utilisé pour déclarer des variables.

####Boucle conditionnelle

Après avoir introduit `FOR_EACH`, il est également possible d'écrire `PP_WHILE` de manière similaire :

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

`PP_WHILE``accepte trois paramètres : `pred`, une fonction de condition, `op`, une fonction d'opération, et `val`, la valeur initiale. Pendant la boucle, la fonction `pred(val)` est constamment utilisée pour définir la condition d'arrêt de la boucle. La valeur obtenue par `op(val)` est ensuite transmise aux futures macros, ce qui peut être interprété comme l'exécution du code suivant :

``` cpp
while (pred(val)) {
    val = op(val);
}
```

`PP_WHILE_N` Tout d'abord, utilisez `pred(val)` pour obtenir le résultat du test conditionnel, puis transmettez le résultat de la condition `cond` et les autres paramètres à `PP_WHILE_N_IMPL`.
`PP_WHILE_N_IMPL` peut être divisé en deux parties : la seconde partie `(pred, op, PP_IF(cond, op, PP_EMPTY_EAT)(val))` sert de paramètre à la première partie, où `PP_IF(cond, op, PP_EMPTY_EAT)(val)` évalue `op(val)` si `cond` est vrai, sinon elle évalue `PP_EMPTY_EAT(val)` pour obtenir un résultat vide. La première partie `PP_IF(cond, PP_WHILE_N+1, val PP_EMPTY_EAT)` renvoie `PP_WHILE_N+1` si `cond` est vrai, et continue la boucle avec le paramètre de la seconde partie ; sinon, elle renvoie `val PP_EMPTY_EAT`, où `val` devient alors le résultat final du calcul, tandis que `PP_EMPTY_EAT` élimine le résultat de la seconde partie.

`SUM` réalise `N + N-1 + ... + 1`. Valeur initiale `(max_num, origin_num)`; `SUM_PRED` prend la première valeur `x` de la valeur de `SUM`, vérifie si elle est supérieure à 0; `SUM_OP` - opération de décrémentation de `x = x - 1`, opération d'addition de `x` à `y`  `y = y + x`. Transmettez directement `SUM_PRED` et `SUM_OP` à `PP_WHILE`, le résultat renvoyé est un tuple, le résultat réellement désiré est le deuxième élément du tuple, puis utilisez à nouveau `SUM` pour obtenir la valeur du deuxième élément.

####Récursion réentrante

Jusqu'à présent, nos parcours d'accès et nos boucles conditionnelles fonctionnent très bien, et les résultats sont conformes aux attentes. Vous vous souvenez de ce que nous avons mentionné sur l'interdiction de la récursivité réentrante en parlant des règles d'expansion des macros ? Malheureusement, nous sommes confrontés à cette interdiction lorsque nous souhaitons effectuer une double boucle :

``` cpp
#define SUM_OP2(xy_tuple) SUM_OP_OP_IMPL2 xy_tuple
#define SUM_OP_OP_IMPL2(x, y) (PP_DEC(x), y + SUM(x, 0))

#define SUM2(max_num, origin_num) \
    PP_IDENTITY(SUM_IMPL PP_WHILE(SUM_PRED, SUM_OP2, (max_num, origin_num)))

SUM2(1, a)      // -> a + SUM_IMPL PP_WHILE_1(SUM_PRED, SUM_OP, (1, a))
```

`SUM2` remplace le paramètre `op` par `SUM_OP2`, qui appellera `SUM`, et `SUM` se développera encore en `PP_WHILE_1`, ce qui équivaut à un appel récursif de `PP_WHILE_1` à lui-même, entraînant l'arrêt de l'expansion par le préprocesseur.

Pour résoudre ce problème, nous pouvons utiliser une méthode de déduction automatique récursive (Automatic Recursion) :

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

`PP_AUTO_WHILE` is the automatic deduced recursive version of `PP_WHILE`, the core macro being `PP_AUTO_REC(PP_WHILE_PRED)`, which identifies the current available version number `N` for `PP_WHILE_N`.

Le principe de déduction est assez simple, il consiste à parcourir toutes les versions, trouver la version qui peut se développer correctement, retourner le numéro de cette version. Pour accélérer la recherche, on utilise généralement une recherche par dichotomie, c'est ce que fait `PP_AUTO_REC`. `PP_AUTO_REC` prend un paramètre `check`, qui est responsable de vérifier la disponibilité de la version. Ici, il est indiqué que la recherche concerne les versions comprises entre `[1, 4]`. `PP_AUTO_REC` vérifie d'abord `check(2)`, si `check(2)` est vrai, alors on appelle `PP_AUTO_REC_12` pour rechercher dans la plage `[1, 2]`, sinon on utilise `PP_AUTO_REC_34` pour rechercher dans `[3, 4]`. `PP_AUTO_REC_12` vérifie `check(1)`, si c'est vrai, alors la version `1` est disponible, sinon on utilise la version `2`. De même pour `PP_AUTO_REC_34`.

Comment écrire le macro `check` pour savoir si la version est disponible ? Ici, `PP_WHILE_PRED` se décompose en deux parties, concentrons-nous sur la seconde partie `PP_WHILE_ ## n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)` : si `PP_WHILE_ ## n` est disponible, étant donné que `PP_WHILE_FALSE` renvoie constamment `0`, cette partie se développera pour obtenir la valeur du paramètre `val`, c'est-à-dire `PP_WHILE_FALSE` ; sinon, cette partie du macro restera inchangée, restant `PP_WHILE_n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`.

Concaténez les résultats de la partie arrière avec ceux de la partie avant `PP_WHILE_CHECK_`, ce qui nous donne deux résultats : `PP_WHILE_CHECK_PP_WHILE_FALSE` ou `PP_WHILE_CHECK_PP_WHILE_n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)` ; ainsi, nous faisons en sorte que `PP_WHILE_CHECK_PP_WHILE_FALSE` retourne `1` pour indiquer qu'il est disponible, et `PP_WHILE_CHECK_PP_WHILE_n` retourne `0` pour indiquer qu'il n'est pas disponible. Nous avons ainsi terminé la fonctionnalité d'inférence automatique de la récursivité.

####Comparaison arithmétique

Non équivalent :

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

Pour déterminer si les valeurs sont égales, on utilise la caractéristique d'interdiction de réentrance récursive, en concaténant `x` et `y` de façon récursive en une macro `PP_NOT_EQUAL_x PP_NOT_EQUAL_y`. Si `x == y`, alors la macro `PP_NOT_EQUAL_y` ne sera pas développée, ce qui donne `PP_NOT_EQUAL_CHECK_` concaténé avec `PP_NOT_EQUAL_CHECK_PP_NOT_EQUAL_y`, retournant `0`. En revanche, si les deux se développent avec succès, on obtient finalement `PP_EQUAL_NIL`, qui se concatène pour donner `PP_NOT_EQUAL_CHECK_PP_EQUAL_NIL`, retournant `1`.

Égalité :

``` cpp
#define PP_EQUAL(x, y) PP_NOT(PP_NOT_EQUAL(x, y))

PP_EQUAL(1, 1)              // -> 1
PP_EQUAL(1, 3)              // -> 0

```

moins que ou égal à :

``` cpp
#define PP_LESS_EQUAL(x, y) PP_NOT(PP_SUB(x, y))

PP_LESS_EQUAL(2, 1)         // -> 0
PP_LESS_EQUAL(1, 1)         // -> 1
PP_LESS_EQUAL(1, 2)         // -> 1
```

inférieur à :

``` cpp
#define PP_LESS(x, y) PP_AND(PP_LESS_EQUAL(x, y), PP_NOT_EQUAL(x, y))

PP_LESS(2, 1)               // -> 0
PP_LESS(1, 2)               // -> 1
PP_LESS(2, 2)               // -> 0
```

Il y a également des comparaisons arithmétiques telles que "plus grand que" et "plus grand ou égal à", que je ne vais pas détailler ici.

####Opérations arithmétiques

En utilisant `PP_AUTO_WHILE`, nous pouvons réaliser des opérations arithmétiques de base, tout en prenant en charge les opérations imbriquées.

Addition :

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

Soustraction :

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

Multiplication :

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

La multiplication implémente ici un paramètre supplémentaire `ret`, initialisé à `0`, et à chaque itération effectue `ret = ret + x`.

Division :

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

La division utilise `PP_LESS_EQUAL`, la boucle continue uniquement si `y <= x`.

####Structure de données

Hong peut aussi avoir des structures de données, en fait nous avons déjà utilisé légèrement une structure de données appelée `tuple` précédemment, `PP_REMOVE_PARENS` permet de supprimer les parenthèses extérieures du `tuple` pour renvoyer les éléments à l'intérieur. Nous allons utiliser le `tuple` comme exemple pour discuter de sa mise en œuvre, pour d'autres structures de données comme les listes, les tableaux, etc., vous pouvez consulter les implémentations de `Boost` qui pourraient vous intéresser.

Un `tuple` est défini comme un ensemble d'éléments séparés par des virgules et entourés de parenthèses : `(a, b, c)`.

``` cpp
#define PP_TUPLE_REMOVE_PARENS(tuple) PP_REMOVE_PARENS(tuple)

Obtenir l'élément à l'index spécifié.
#define PP_TUPLE_ELEM(i, tuple) PP_ARGS_ELEM(i, PP_TUPLE_REMOVE_PARENS(tuple))

Dévorer tout le tuple et renvoyer vide.
#define PP_TUPLE_EAT() PP_EMPTY_EAT

// Obtenir la taille
#define PP_TUPLE_SIZE(tuple) PP_ARGS_SIZE(PP_TUPLE_REMOVE_PARENS(tuple))

Ajouter des éléments.
#define PP_TUPLE_PUSH_BACK(elem, tuple) \
    PP_TUPLE_PUSH_BACK_IMPL(PP_TUPLE_SIZE(tuple), elem, tuple)
#define PP_TUPLE_PUSH_BACK_IMPL(size, elem, tuple) \
    (PP_TUPLE_REMOVE_PARENS(tuple) PP_IF(size, PP_COMMA, PP_EMPTY)() elem)

// Insérer des éléments
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

Supprimer l'élément à la fin.
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

Supprimer les éléments
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

Ici, je vais expliquer brièvement la mise en œuvre de l'insertion d'éléments, et d'autres opérations comme la suppression d'éléments sont également réalisées selon un principe similaire. `PP_TUPLE_INSERT(i, elem, tuple)` permet d'insérer l'élément `elem` à la position `i` dans le `tuple`. Pour accomplir cette opération, on commence par placer tous les éléments à une position inférieure à `i` dans un nouveau `tuple` (appelé `ret`) en utilisant `PP_TUPLE_PUSH_BACK`. Ensuite, on insère l'élément `elem` à la position `i`, puis on ajoute à `ret` les éléments de l'ancien `tuple` qui se trouvent à une position supérieure ou égale à `i`. Enfin, `ret` contient le résultat souhaité.

##Résumé

(https://github.com/pfultz2/Cloak/wiki/C-Preprocessor-tricks,-tips,-and-idioms#deferred-expression)Veuillez consulter vous-même les macros liées à `REPEAT` dans `BOOST_PP`.

Le débogage de la programmation macro est un processus douloureux, nous pouvons :

* Utilisez les options `-P -E` pour afficher les résultats du prétraitement ;
* Étudier attentivement le processus de développement en utilisant ma version modifiée de `clang` mentionnée précédemment ;
Décomposez les macros complexes et examinez les résultats de l'expansion des macros intermédiaires;
* Masquer les fichiers d'en-tête et les macros non pertinents ;
Enfin, il faut imaginer le processus d'expansion des macros ; une fois familiarisé avec l'expansion des macros, l'efficacité du débogage sera également améliorée.

Les macros dans cet article sont une réimplémentation personnelle que j'ai réalisée après avoir compris les principes. Certaines macros s'inspirent de l'implémentation de `Boost` et des articles référencés. Si vous remarquez des erreurs, n'hésitez pas à me corriger, et je suis également ouvert à discuter de toute question connexe.

Le code de cet article est entièrement disponible ici : [Télécharger](assets/img/2021-3-31-cpp-preprocess/macros.cpp)，[Démonstration en ligne](https://godbolt.org/z/coWvc5Pse)。

##Citation

* [Boost.Preprocessor](https://www.boost.org/doc/libs/1_75_0/libs/preprocessor/doc/)
* [L'art de la programmation macro en C/C++](https://bot-man-jl.github.io/articles/?post=2020/Macro-Programming-Art)

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT, veuillez donner votre [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Signalez toute omission éventuelle. 
