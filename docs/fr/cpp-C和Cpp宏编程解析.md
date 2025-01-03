---
layout: post
title: Analyse de la programmation de macros en C/C++
categories:
- c++
catalog: true
tags:
- dev
description: Le but de ce texte est d'expliquer les règles et les méthodes de mise
  en œuvre de la programmation de macros en C/C++, pour que vous ne craigniez plus
  de voir des macros dans le code.
figures: []
---

<meta property="og:title" content="C/C++ 宏编程解析" />

Le but de ce texte est d'expliquer les règles et les méthodes de programmation de macros en C/C++, pour que vous ne redoutiez plus de voir des macros dans le code. Je vais d'abord aborder les règles d'expansion de macros mentionnées dans la norme C++ 14, puis observer l'expansion des macros en modifiant le code source de Clang, pour enfin discuter de la mise en œuvre de la programmation de macros sur la base de ces connaissances.

Le code complet de cet article se trouve ici : [Télécharger](assets/img/2021-3-31-cpp-preprocess/macros.cpp)，[démonstration en ligne](https://godbolt.org/z/coWvc5Pse)Je vous remercie pour votre demande, mais il semble qu'il n'y ait aucun texte à traduire. Pouvez-vous vérifier et me fournir le contenu à traduire ?

##Prélude

Nous pouvons utiliser la commande `gcc -P -E a.cpp -o a.cpp.i` pour demander au compilateur d'effectuer uniquement la précompilation du fichier `a.cpp` et de sauvegarder le résultat dans `a.cpp.i`.

Tout d'abord, commençons par examiner quelques exemples :

####Réentrance

``` cpp
#define ITER(arg0, arg1) ITER(arg1, arg0)

ITER(1, 2)          // -> ITER(2, 1)
```

Le macro 'ITER' a échangé les positions de 'arg0' et 'arg1'. Après expansion de la macro, on obtient 'ITER(2, 1)'.

On peut voir que les positions de `arg0` et `arg1` ont été échangées avec succès. Ici, la macro a été déroulée une fois avec succès, mais une seule fois, sans réentrée récursive. En d'autres termes, pendant le déroulement de la macro, il n'est pas possible de se réinsérer de manière récursive. Si, au cours de la récursion, il est constaté que la même macro a déjà été déroulée lors d'une récursion antérieure, elle ne sera pas déroulée à nouveau. Ceci constitue l'une des règles importantes du déroulement des macros. La raison de l'interdiction de la récursion récursive est également très simple, c'est pour éviter la récursion infinie.

####Concaténation de chaînes.

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                // -> HelloWorld
CONCAT(Bonjour, CONCAT(Monde, !))     // -> BonjourCONCAT(Monde, !)
```

Le but de la macro `CONCAT` est de concaténer `arg0` et `arg1`. Une fois la macro développée, `CONCAT(Bonjour, Monde)` peut obtenir le résultat correct `BonjourMonde`. Cependant, `CONCAT(Bonjour, CONCAT(Monde, !))` ne développe que la macro externe. La macro interne `CONCAT(Monde, !)` n'est pas développée mais est directement concaténée avec `Bonjour`, ce qui est différent de ce que nous avons anticipé. Ce que nous voulons vraiment comme résultat est `BonjourMonde!`. C'est une autre règle importante de l'expansion des macros : les paramètres de la macro qui suivent l'opérateur `##` ne seront pas développés, mais seront directement concaténés avec le contenu précédent.

En observant les deux exemples ci-dessus, on peut remarquer que certaines règles de développement des macros peuvent sembler contre-intuitives. Sans une compréhension claire des règles spécifiques, il est possible d'écrire des macros qui ne produisent pas l'effet désiré.

##Dérouler les règlements Macro-Expansion

À travers les deux exemples donnés dans l'introduction, nous comprenons que l'expansion des macros obéit à un ensemble de règles standard définies dans les normes C/C++. Le contenu de ces règles est assez succinct, je vous recommande donc de les lire attentivement à plusieurs reprises. En passant, voici le lien vers la version N4296 des normes, où l'expansion des macros est traitée à la section 16.3 : [lien](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4296.pdf)Je vais extraire quelques règles importantes de la version n4296 ci-dessous, ces règles détermineront comment écrire correctement les macros (il est recommandé de prendre le temps de lire attentivement les macros à l'intérieur de la norme).

####Séparation des paramètres

Les exigences des paramètres de la macro sont qu'ils doivent être séparés par des virgules, et le nombre de paramètres doit être égal au nombre de définitions de macro. Dans les paramètres transmis à la macro, tout contenu supplémentaire encadré de parenthèses est considéré comme un paramètre, et les paramètres sont autorisés à être vides.

``` cpp
#define ADD_COMMA(arg1, arg2) arg1, arg2

ADD_COMMA(a, b)             // -> a, b
AJOUTER_VIRGULE(a)                // Erreur "la macro "MACRO" nécessite 2 arguments, mais seulement 1 donné"
ADD_COMMA((a, b), c)        // -> (a, b), c
ADD_COMMA(, b)              // -> , b
```

Ajoutez une virgule entre les éléments `(a, b)` et `c`. Dans `ADD_COMMA(, b)`, le premier argument est vide, donc cela se développe en `, b`.

####Développement des macros.

Lors de l'expansion d'une macro, si les arguments de la macro sont également des macros expansibles, les arguments seront d'abord entièrement développés, puis la macro sera dépliée, par exemple

``` cpp
ADD_COMMA(ADD_COMMA(1, 2), ADD_COMMA(3, 4))     // -> 1, 2, 3, 4
```

Dans la plupart des cas, l'expansion des macros peut être considérée comme l'évaluation des paramètres d'abord, puis l'évaluation de la macro, sauf en présence des opérateurs `#` et `##`.

####Opérateur `#`

Le paramètre macro suivi de l'opérateur `#` ne sera pas étendu, mais sera directement converti en chaîne, par exemple :

``` cpp
#define STRINGIZE(arg0) # arg0

STRINGIZE(a)                // -> "a"
STRINGIZE(STRINGIZE(a))     // -> "STRINGIZE(a)"
```

Selon cette règle, `STRINGIZE(STRINGIZE(a))` peut uniquement être développé en `"STRINGIZE(a)"`.

####`##` Opérateur

Les paramètres de macro avant et après l'opérateur `##` ne seront pas développés, ils seront directement concaténés, par exemple :

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                        // -> HelloWorld
CONCAT(Hello, CONCAT(World, !))             // -> HelloCONCAT(World, !)
CONCAT(CONCAT(Hello, World) C, ONCAT(!))    // -> CONCAT(Hello, World) CONCAT(!)
```

Concaténer ces textes en français :

`CONCAT(CONCAT(Hello, World) C, ONCAT(!))` ne peut être concaténé qu'en premier pour obtenir `CONCAT(Hello, World) CONCAT(!)`.

####Répétition de balayage

Une fois que le préprocesseur a effectué une fois l'expansion des macros, il re-scanne le contenu obtenu pour continuer l'expansion, jusqu'à ce qu'il n'y ait plus de contenu à développer.

Une fois l'expansion macro effectuée, on peut la comprendre comme le fait de déployer entièrement les paramètres (sauf en cas de rencontre avec `#` et `##`), puis en fonction de la définition de la macro, de remplacer la macro et les paramètres complètement déployés conformément à la définition, puis de traiter tous les opérateurs `#` et `##` dans la définition.

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define STRINGIZE(arg0) # arg0

CONCAT(STRING, IZE(Hello))        // -> STRINGIZE(Hello) -> "Hello"
```

`CONCAT(STRING, IZE(Hello))` is initially expanded to `STRINGIZE(Hello)` on the first scan. Then, on the second scan, it is found that `STRINGIZE` can be further expanded, resulting in `"Hello"`.

####Interdiction de réentrer récursivement

Pendant le processus de balayage répété, il est interdit de dérouler de manière récursive les mêmes macros. On peut comprendre le déroulement des macros comme une structure arborescente, où le nœud racine est la macro à dérouler initialement, et où le contenu de chaque macro déroulée est connecté comme un nœud enfant à l'arbre. Par conséquent, interdire la récursivité signifie que lors du déroulement des macros des nœuds enfants, si cette macro est identique à n'importe quelle macro des nœuds ancestraux, son déroulement est interdit. Voici quelques exemples :

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define CONCAT_SPACE(arg0, arg1) arg0 arg1
#define IDENTITY(arg0) IDENTITY_IMPL(arg0)
#define IDENTITY_IMPL(arg0) arg0

CONCAT(CON, CAT(a, b))                  // -> CONCAT(a, b)
IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))   // -> CONCAT(a, b)
IDENTITY(CONCAT(CON, CAT(a, b)))        // -> IDENTITY_IMPL(CONCAT(a, b)) -> CONCAT(a, b)
```

`CONCAT(CON, CAT(a, b))` : Comme `CONCAT` joint deux paramètres avec `##`, selon la règle de `##`, elle ne déroule pas les paramètres, elle les joint directement. Ainsi, lors du premier déroulement, on obtient `CONCAT(a, b)`. Comme `CONCAT` a déjà été déroulé, il ne sera pas déroulé de nouveau, donc il s'arrête là.

`IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))`： `IDENTITY_IMPL` can be understood as evaluating the parameter `arg0`, where the parameter `arg0` evaluates to `CONCAT(a, b)`. Due to recursive being marked as non-reentrant, the subsequent expansion of `IDENTITY_IMPL` is terminated. Upon the second scan, encountering the non-reentrant `CONCAT(a, b)`, the expansion is halted. Here, `CONCAT(a, b)` is obtained through the expansion of the parameter `arg0`, maintaining the non-reentrant marking during subsequent expansions, thus akin to the parent node being the parameter `arg0`, consistently holding the non-reentrant marking.

`IDENTITY(CONCAT(CON,CAT(a,b)))`: Cet exemple vise principalement à renforcer la compréhension des nœuds parent-enfant. Lorsque les paramètres sont développés par eux-mêmes, le paramètre lui-même agit en tant que nœud parent, et le contenu développé agit comme nœud enfant pour déterminer la récursivité. Une fois les paramètres développés transmis à la définition de la macro, le marquage d'interdiction de réentrance restera en place (si les paramètres développés n'ont pas été modifiés après avoir été transmis à la définition de la macro). On peut considérer le processus de développement des paramètres comme un autre arbre, où le résultat du développement des paramètres correspond aux nœuds enfants les plus bas de l'arbre. Ce nœud enfant est transmis à la macro pour exécuter le déploiement tout en conservant toujours la propriété d'interdiction de réentrance.

Par exemple ici, après avoir complètement déroulé `IDENTITY_IMPL(CONCAT(a, b))` pour la première fois, `CONCAT(a, b)` est marqué comme non réentrant. Même si `IDENTITY_IMPL` évalue les paramètres, ceux-ci sont interdits de déploiement, donc les paramètres sont transmis tels quels à la définition, aboutissant finalement à `CONCAT(a, b)`.

J'ai simplement énuméré quelques règles que je considère importantes ou difficiles à comprendre. Pour une explication détaillée des règles, je vous conseille de prendre le temps de consulter directement le document standard.

##Observer le processus de déploiement via Clang.

(https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-11.1.0.tar.gz)Les fichiers modifiés sont accessibles ici : [lien](assets/img/2021-3-31-cpp-preprocess/clang-modify.zip)Veuillez traduire ce texte en français :

"）。下面简单通过例子来验证我们之前介绍的宏展开规则："

####Translate these text into French language: 

Exemple 1

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(C, ONCAT(a, b))      // CONCAT(a, b)
```

Utilisez Clang modifié pour prétraiter le code ci-dessus : `clang -P -E a.cpp -o a.cpp.i`, vous obtenez les informations imprimées ci-dessous:

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

第 [1](#__codelineno-9-1)Lorsque la fonction `HandleIdentifier` rencontre une macro, elle va l'imprimer, puis afficher les informations de la macro (de [2-4](#__codelineno-9-2)Le macro est OK pour se développer, puis entrez dans le macro `EnterMacro`.

La fonction qui effectue réellement le déroulement des macros est `ExpandFunctionArguments`, qui imprime ensuite à nouveau les informations sur la macro à développer, en notant que la macro est désormais marquée comme `utilisée` (line [9](#__codelineno-9-9)Après cela, procédez à l'expansion de chaque "token" successivement en fonction de la définition du macro (un "token" est un concept dans le préprocesseur Clang, mais je ne rentre pas dans les détails ici).

Le premier `Token` est le paramètre `arg0`, et son argument correspondant est `C`. Comme aucune expansion n'est nécessaire pour l'évaluation, il est directement copié dans le résultat (lignes [11-13](#__codelineno-9-11)(Pas de traduction appropriée disponible，veuillez fournir un autre texte à traduire).

(#__codelineno-9-14)(Veuillez fournir plus de contexte pour mieux comprendre le texte à traduire. Merci.)

Le deuxième `Token` est le paramètre formel `arg1`, avec l'argument correspondant `ONCAT(a, b)`. Le préprocesseur traitera également l'argument en une série de `Token`, ce qui explique que le résultat imprimé est entouré de crochets, délimitant chaque `Token` de l'argument (ligne 18). En raison de `##`, cet argument n'a pas besoin d'être développé, il est donc directement copié dans le résultat (lignes [16-18](#__codelineno-9-16)(Vierge).

(#__codelineno-9-19)Dans ce cas, une fois que le préprocesseur a terminé son travail, tous les tokens résultants sont traduits en `C ## ONCAT(a, b)`, et ensuite le préprocesseur exécute l'opérateur `##` pour générer du nouveau contenu.

Après exécution, on obtient `CONCAT(a, b)`. En rencontrant le macro `CONCAT`, le prétraitement passe d'abord par `HandleIdentifier`, où les informations du macro sont affichées. On constate que l'état de ce macro est `disable used`, ce qui signifie qu'il a déjà été développé et ne peut plus être réutilisé. Ainsi, le message `Macro is not ok to expand` est affiché, indiquant que le préprocesseur ne le développera pas davantage. En conséquence, le résultat final reste `CONCAT(a, b)`.

####Translate these text into French language:

Exemple 2

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define IDENTITY(arg0) arg0

IDENTITY(CONCAT(C, ONCAT(a, b)))
```

<details>
<summary> <font> Clang printing information (click to expand):</font> </summary>
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

第 [12](#__codelineno-11-12)Commencez l'exécution de `IDENTITY`, en constatant que le paramètre `Token 0` est une fonction `CONCAT(...)`, qui est également une macro. Par conséquent, évaluez d'abord ce paramètre.

Translate these text into French language:

第 [27](#__codelineno-11-27)Commencez à dérouler le paramètre de macro `CONCAT(...)` et, comme dans l'exemple 1, une fois qu'il est déroulé plusieurs fois, vous obtiendrez `CONCAT(a, b)` à la fin du processus (voir [46](#__codelineno-11-46)(Pas de traduction disponible)

(#__codelineno-11-47)Terminer le déploiement de `IDENTITY`, le résultat obtenu est `CONCAT(a, b)`.

(#__codelineno-11-51)Veuillez renumériser `CONCAT(a, b)` et remarquer qu' bien que ce soit une macro, elle a été préalablement configurée en tant que `utilisée` lors de l'expansion des paramètres précédents, elle ne sera donc pas développée de manière récursive mais directement utilisée comme résultat final.

####Translate these text into French language:

Exemple 3

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

Seize [16](#__codelineno-13-16)Commencez à développer `IDENTITY`, puisque le préprocesseur voit que `Token 2` (c'est-à-dire `arg0`) est une macro, il procède d'abord à développer `CONCAT(C, ONCAT(a, b))`.

Déployez `arg0` pour obtenir `CONCAT(a, b)` (de la [23-54](#__codelineno-13-23)(The text cannot be translated as it does not contain any meaningful content in any language)

* `IDENTITY` is eventually expanded to `IDENTITY_IMPL(CONCAT(a, b))` (page [57](#__codelineno-13-57)Je vous remercie de votre demande.

Re-scan, continue expanding `IDENTITY_IMPL` (from [61-72](#__codelineno-13-61)Veuillez traduire ce texte en français :

 行），发现此时的 `Token 0` 是宏 `CONCAT(a, b)`，但处于 `used` 状态，中止展开并返回（第 75-84行），最终得到的结果还是 `CONCAT(a, b)`（第 [85](#__codelineno-13-85)Veuillez traduire ce texte en français :

行） 。

Re-scan results, it turns out that the macro `CONCAT(a, b)` is in a `used` state, so we stop expanding it and get the final result.

En utilisant les trois exemples simples ci-dessus, on peut avoir une idée générale du processus de développement des macros par le préprocesseur. Nous n'allons pas approfondir davantage le sujet du préprocesseur ici, mais si vous êtes intéressé, vous pouvez étudier en comparant les fichiers modifiés que j'ai fournis.

##Programmation macroscopique mise en œuvre

Nous allons maintenant passer au sujet (la grande partie précédente visait à mieux comprendre les règles de l'expansion des macros), la programmation de macros.

####Symboles de base

Tout d'abord, nous pouvons définir les symboles spéciaux des macros, qui seront utilisés lors de l'évaluation et de la concaténation.

``` cpp
#define PP_LPAREN() (
#define PP_RPAREN() )
#define PP_COMMA() ,
#define PP_EMPTY()
#Définir PP_HASHHASH # ## # // Représente une chaîne ##, mais seulement en tant que chaîne, et non pas comme un opérateur ## à traiter
```

####Évaluation demandée

En utilisant une règle de priorité des paramètres, il est possible d'écrire une macro d'évaluation :

``` cpp
#define PP_IDENTITY(arg0) arg0

PP_COMMA PP_LPAREN() PP_RPAREN()                // -> PP_COMMA ( )
PP_IDENTITY(PP_COMMA PP_LPAREN() PP_RPAREN())   // -> PP_COMMA() -> ,
```

Si vous écrivez simplement "PP_COMMA PP_LPAREN() PP_RPAREN()", le préprocesseur traitera chaque macro séparément sans fusionner les résultats des expansions. En ajoutant "PP_IDENTITY", le préprocesseur peut évaluer le résultat de l'expansion de "PP_COMMA()" pour obtenir ",".


####Assemblage

Lors de la concaténation avec `##`, les paramètres des côtés ne sont pas développés. Pour permettre l'évaluation préalable des paramètres avant la concaténation, vous pouvez écrire de la sorte :

``` cpp
#define PP_CONCAT(arg0, arg1) PP_CONCAT_IMPL(arg0, arg1)
#define PP_CONCAT_IMPL(arg0, arg1) arg0 ## arg1

PP_CONCAT(PP_IDENTITY(1), PP_IDENTITY(2))         // -> 12
PP_CONCAT_IMPL(PP_IDENTITY(1), PP_IDENTITY(2))    // -> PP_IDENTITY(1)PP_IDENTITY(2) -> Error
```

Ici, la méthode utilisée pour `PP_CONCAT` est appelée la concaténation différée. Lorsqu'elle est déployée en `PP_CONCAT_IMPL`, à la fois `arg0` et `arg1` seront évalués et déployés en premier, puis `PP_CONCAT_IMPL` effectuera l'opération de concaténation réelle.

####Opération logique

Avec l'aide de `PP_CONCAT`, il est possible d'effectuer des opérations logiques. Commencez par définir des valeurs `BOOL` :


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

Utilisez d'abord `PP_CONCAT` pour combiner `PP_BOOL_` et `arg0`, puis évaluez le résultat de cette combinaison. Ici, `arg0` doit être évalué pour obtenir un nombre dans la plage `[0, 256]`, en évaluant après son ajout à `PP_BOOL_`, vous obtiendrez une valeur booléenne. Opérations logiques ET, OU et NON :

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

Utilisez d'abord `PP_BOOL` pour évaluer les paramètres, puis assemblez les résultats des opérations logiques en fonction des combinaisons `0 1`. Si vous n'utilisez pas `PP_BOOL` pour évaluer, les paramètres ne prendront en charge que les valeurs `0 1`, ce qui réduirait considérablement leur adaptabilité. De la même manière, vous pouvez également écrire des opérations telles que XOR, OR, NOT, etc. Si vous êtes intéressé, vous pouvez essayer par vous-même.

####Sélection de critères

En utilisant `PP_BOOL` et `PP_CONCAT`, il est également possible d'écrire des instructions de sélection conditionnelle :

``` cpp
#define PP_IF(if, then, else) PP_CONCAT(PP_IF_, PP_BOOL(if))(then, else)
#define PP_IF_1(then, else) then
#define PP_IF_0(then, else) else

PP_IF(1, 2, 3)      // -> PP_IF_1(2, 3) -> 2
PP_IF(0, 2, 3)      // -> PP_IF_0(2, 3) -> 3
```

`if` is evaluated to `1`, concatenate with `PP_CONCAT` to form `PP_IF_1`, and finally expand to the value of `then`; similarly, if `if` is evaluated to `0`, `PP_IF_0` is obtained.

####Incrément décroissant

Nombres entiers croissants décroissants :

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

Similaire à `PP_BOOL`, l'incrémentation et la décrémentation des entiers ont également des limites. Ici, la plage est définie comme `[0, 256]`, après avoir atteint `256`, par mesure de sécurité, `PP_INC_256` renverra lui-même `256` comme limite, de même que `PP_DEC_0` renverra `0`.

####Les paramètres variables

Hong Kong accepte les arguments variables, le format est :

```cpp
#define LOG(format, ...) printf("log: " format, __VA_ARGS__)

LOG("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG("Hello World")              // -> printf("log: " "Hello World", ); An additional comma was added, causing a compilation error
```

En raison du risque que les paramètres variables soient vides et entraînent une erreur de compilation, C++ 20 a introduit `__VA_OPT__`, qui renvoie une chaîne vide si les paramètres variables sont vides, sinon il renvoie les paramètres d'origine :

```cpp
#define LOG2(format, ...) printf("log: " format __VA_OPT__(,) __VA_ARGS__)

LOG2("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG2("Hello World") // -> printf("log: " "Hello World" ); No commas, compiles correctly
```

Malheureusement, seul le standard C++ 20 et supérieur dispose de ce macro. Dans la suite du texte, nous présenterons la méthode de mise en œuvre de `__VA_OPT__`.

####évaluation paresseuse

Considérez ce scénario :

``` cpp
PP_IF(1, PP_COMMA(), PP_LPAREN())     // -> PP_IF_1(,,)) -> Error unterminated argument list invoking macro "PP_IF_1"
```

Nous savons que lors de l'expansion macro, l'évaluation se fait d'abord sur les paramètres. `PP_COMMA()` et `PP_LPAREN()` sont évalués avant d'être transmis à `PP_IF_1`, ce qui donne `PP_IF_1(,,))`, entraînant une erreur de prétraitement. À ce stade, on peut utiliser une méthode appelée évaluation paresseuse :

``` cpp
PP_IF(1, PP_COMMA, PP_LPAREN)()       // -> PP_IF_1(PP_COMMA, PP_LPAREN)() -> PP_COMMA() -> ,
```

Modifier de cette manière, transmettez uniquement le nom de la macro, permettez à `PP_IF` de sélectionner le nom de la macro requis, puis assemblez-le avec des parenthèses `()` pour former une macro complète, puis expandez-la. Dans la programmation des macros, l'évaluation paresseuse est également très courante.

####Commence par parenthèse.

Vérifier si les arguments de longueur variable commencent par une parenthèse :

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

`PP_IS_BEGIN_PARENS` est utilisé pour vérifier si les arguments passés commencent par une parenthèse. Cela peut être utile lors du traitement d'arguments entre parenthèses (comme l'implémentation de `__VA_OPT__` mentionnée plus tard). Cela peut sembler complexe, mais l'idée principale est de créer une macro qui, si les arguments variables commencent par une parenthèse, peut les évaluer avec cette parenthèse pour obtenir un résultat, sinon les évaluer séparément pour obtenir un autre résultat. Examinons cela en détail :

Les macros `PP_IS_BEGIN_PARENS_PROCESS` et `PP_IS_BEGIN_PARENS_PROCESS_0` fonctionnent ensemble pour évaluer d'abord les arguments variables passés en entrée, puis récupérer le 0ème argument.

`PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__)` consiste à évaluer d'abord `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__`, puis à concaténer le résultat de l'évaluation avec `PP_IS_BEGIN_PARENS_PRE_`.

La macro `PP_IS_BEGIN_PARENS_EAT(...)` va absorber tous les arguments, et retourner 1 si dans l'étape précédente `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__`, `__VA_ARGS__` commence par une parenthèse. Dans ce cas, cela correspondra à l'évaluation de `PP_IS_BEGIN_PARENS_EAT(...)` et renverra 1. Sinon, s'il ne commence pas par une parenthèse, il n'y aura pas de correspondance et `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` restera inchangé.

Si `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` évalue à` 1`, `PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, 1) -> PP_IS_BEGIN_PARENS_PRE_1 -> 1`, attention il y a une virgule après `1`, transmettez `1,` à `PP_IS_BEGIN_PARENS_PROCESS_0`, prenez le 0ème argument, pour finalement obtenir `1`, indiquant que l'argument commence par une parenthèse.

Si 'PP_IS_BEGIN_PARENS_EAT __VA_ARGS__' évalue non pas à '1', mais reste inchangé, alors 'PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__) -> PP_IS_BEGIN_PARENS_PRE_PP_IS_BEGIN_PARENS_EAT __VA_ARGS__ -> 0, __VA_ARGS__', en passant à 'PP_IS_BEGIN_PARENS_PROCESS_0', obtiendra '0', ce qui signifie que l'argument ne commence pas par une parenthèse.

####Paramètre variable vide

Vérifier si les paramètres de longueur variable sont vides est également une macro couramment utilisée, notamment lors de la mise en œuvre de `__VA_OPT__`. En utilisant `PP_IS_BEGIN_PARENS` ici, nous pouvons commencer par ébaucher une version incomplète :

``` cpp
#define PP_IS_EMPTY_PROCESS(...) \
    PP_IS_BEGIN_PARENS(PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ())
#define PP_IS_EMPTY_PROCESS_EAT(...) ()

PP_IS_EMPTY_PROCESS()       // -> 1
PP_IS_EMPTY_PROCESS(1)      // -> 0
PP_IS_EMPTY_PROCESS(1, 2)   // -> 0
PP_IS_EMPTY_PROCESS(())     // -> 1
```

La fonction de `PP_IS_EMPTY_PROCESS` est de vérifier si `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__()` commence par une parenthèse.

Si `__VA_ARGS__` est vide, `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ () -> PP_IS_EMPTY_PROCESS_EAT() -> ()`, on obtient une paire de parenthèses `()`, qu'on transmet ensuite à `PP_IS_BEGIN_PARENS` pour obtenir `1`, indiquant que le paramètre est vide.

Sinon, `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__()` est transmis tel quel à `PP_IS_BEGIN_PARENS`, renvoyant 0 pour indiquer que ce n'est pas vide.

Notez le quatrième exemple  `PP_IS_EMPTY_PROCESS(()) -> 1`, `PP_IS_EMPTY_PROCESS` ne peut pas traiter correctement les arguments de longueur variable commençant par des parenthèses car les parenthèses introduites par ces arguments correspondent à `PP_IS_EMPTY_PROCESS_EAT`, ce qui entraîne une évaluation de `()`. Pour résoudre ce problème, il est nécessaire de distinguer les cas où les arguments commencent par des parenthèses.

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

La fonction `PP_IS_EMPTY_IF` renvoie le premier ou le deuxième argument en fonction de la condition `if`.

Si les arguments variables entrants commencent par des parenthèses, `PP_IS_EMPTY_IF` renvoie `PP_IS_EMPTY_ZERO`, puis renvoie finalement `0`, ce qui indique que les arguments variables ne sont pas vides.

Inversément, `PP_IS_EMPTY_IF` renvoie `PP_IS_EMPTY_PROCESS`, puis finalement `PP_IS_EMPTY_PROCESS` détermine si les arguments variables ne sont pas vides.

####Accès en indice

Obtenir l'élément spécifié à une position donnée des arguments à longueur variable :

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

Le premier argument de `PP_ARGS_ELEM` est l'indice de l'élément `I`, suivi par des arguments de longueur variable. En utilisant `PP_CONCAT` pour concaténer `PP_ARGS_ELEM_` et `I`, on peut ainsi obtenir la macro `PP_ARGS_ELEM_0..8` qui renvoie l'élément correspondant à la position donnée, en lui transmettant les arguments de longueur variable pour déplier et retourner l'élément correspondant à l'indice.

#### PP_IS_EMPTY2

Utilisez `PP_ARGS_ELEM` pour créer une autre version de `PP_IS_EMPTY` :

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

Utilisez `PP_ARGS_ELEM` pour déterminer si un argument contient une virgule avec `PP_HAS_COMMA`. `PP_COMMA_ARGS` absorbera n'importe quel argument passé, puis renverra une virgule.

La logique de base pour déterminer si les arguments variables sont vides est que `PP_COMMA_ARGS __VA_ARGS__()` renvoie une virgule, c'est-à-dire que `__VA_ARGS__` est vide, `PP_COMMA_ARGS` et `()` sont concaténés pour être évalués, la formulation exacte est `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__())`.

Cependant, il peut y avoir des exceptions :

`__VA_ARGS__` itself may bring commas;
`__VA_ARGS__ ()` 拼接在一起发生求值带来逗号；
`PP_COMMA_ARGS __VA_ARGS__` Joindre ensemble provoque une évaluation avec une virgule;

Pour les trois cas d'exception mentionnés ci-dessus, il convient de les exclure, de sorte que la formulation finale équivaut à l'application de l'opérateur logique "ET" à quatre conditions suivantes :

* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__))` &&
* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__()))` &&
* `PP_NOT(PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__))` &&
* `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ())`

#### `__VA_OPT__`

En utilisant `PP_IS_EMPTY`, il est enfin possible de mettre en œuvre des macros similaires à `__VA_OPT__` :

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

`PP_ARGS_OPT` takes two fixed parameters and a variable number of parameters. It returns `data` if the variable parameters are not empty, otherwise it returns `empty`. To support commas in both `data` and `empty`, it is required that both are enclosed in parentheses with the actual parameters, and finally `PP_REMOVE_PARENS` is used to remove the outer parentheses.

Avec `PP_ARGS_OPT`, vous pouvez simuler la fonctionnalité implémentée par `LOG2` en utilisant `LOG3` :

``` cpp
#define LOG3(format, ...) \
    printf("log: " format PP_ARGS_OPT((,), (), __VA_ARGS__) __VA_ARGS__)

LOG3("Hello");                  // -> printf("log: " "Hello" );
LOG3("Hello %s", "World");      // -> printf("log: " "Hello %s" , "World");
```

Le `data_tuple` est `(,)`, et s'il y a des arguments variables, il renverra tous les éléments de `data_tuple`, qui sont simplement des virgules `,`.

####Demander le nombre de paramètres.

Obtenir le nombre de paramètres variables :

``` cpp
#define PP_ARGS_SIZE_IMCOMPLETE(...) \
    PP_ARGS_ELEM(8, __VA_ARGS__, 8, 7, 6, 5, 4, 3, 2, 1, 0)

PP_ARGS_SIZE_IMCOMPLETE(a)             // -> 1
PP_ARGS_SIZE_IMCOMPLETE(a, b)          // -> 2
PP_ARGS_SIZE_IMCOMPLETE(PP_COMMA())    // -> 2
PP_ARGS_SIZE_IMCOMPLETE()              // -> 1
```

Calculer le nombre d'arguments variables se fait en fonction de leur position. `__VA_ARGS__` décale tous les arguments suivants vers la droite, en utilisant la macro `PP_ARGS_ELEM` pour obtenir le 8ᵉ argument. Si `__VA_ARGS__` a un seul argument, le 8ᵉ argument est égal à `1`; de même, avec deux arguments, le 8ᵉ argument devient `2`, correspondant donc au nombre d'arguments variables.

Les exemples fournis ici n'acceptent qu'un maximum de 8 arguments variables, car cela dépend de la longueur maximale prise en charge par `PP_ARGS_ELEM`.

Cependant, cette macro n'est pas complète. Lorsque les paramètres variables sont vides, cette macro renverra incorrectement `1`. Si vous devez traiter des paramètres variables vides, vous aurez besoin de la macro `PP_ARGS_OPT` mentionnée précédemment.

``` cpp
#define PP_COMMA_IF_ARGS(...) PP_ARGS_OPT((,), (), __VA_ARGS__)
#define PP_ARGS_SIZE(...) PP_ARGS_ELEM(8, __VA_ARGS__ PP_COMMA_IF_ARGS(__VA_ARGS__) 8, 7, 6, 5, 4, 3, 2, 1, 0, 0, 0)

PP_ARGS_SIZE(a)             // -> 1
PP_ARGS_SIZE(a, b)          // -> 2
PP_ARGS_SIZE(PP_COMMA())    // -> 2
PP_ARGS_SIZE()              // -> 0
PP_ARGS_SIZE(,,,)           // -> 4
```

Le point clé du problème réside dans la virgule `,` ; lorsque `__VA_ARGS__` est vide, en supprimant la virgule, on peut renvoyer correctement `0`.

####Parcourir l'accès

Similaire au `for_each` en C++, nous pouvons mettre en œuvre le `PP_FOR_EACH` en tant que macro.

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

`PP_FOR_EACH` accepts two fixed parameters: `macro`, which can be understood as the macro called during iteration, and `context`, which can be passed as a fixed value parameter to `macro`. First, `PP_FOR_EACH` uses `PP_ARGS_SIZE` to obtain the length `N` of the variable parameters, then concatenates using `PP_CONCAT` to obtain `PP_FOR_EACH_N`. Afterwards, `PP_FOR_EACH_N` will iteratively call `PP_FOR_EACH_N-1` to achieve the same number of iterations as the variable parameter count.

Dans l'exemple, nous déclarons `DECLARE_EACH` en tant que paramètre de la macro, la fonction de `DECLARE_EACH` est de renvoyer `contex arg`, si `contex` est le nom du type et `arg` est le nom de la variable, `DECLARE_EACH` peut alors être utilisé pour déclarer des variables.

####Boucle conditionnelle

Avec `FOR_EACH`, il est également possible d'écrire `PP_WHILE` de manière similaire :

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

`PP_WHILE` accepts three parameters: `pred` for the conditional check function, `op` for the operation function, and `val` as the initial value; during the loop, it continuously uses `pred(val)` for the loop termination check, passing the value obtained from `op(val)` to the subsequent macro, which can be understood as executing the following code:

``` cpp
while (pred(val)) {
    val = op(val);
}
```

Tout d'abord, utilisez `pred(val)` pour obtenir le résultat de la condition, puis transmettez ce résultat de la condition et les autres paramètres à `PP_WHILE_N_IMPL`.
`PP_WHILE_N_IMPL` peut être divisé en deux parties : la seconde moitié `(pred, op, PP_IF(cond, op, PP_EMPTY_EAT)(val))` est passée en tant qu'argument à la première moitié, `PP_IF(cond, op, PP_EMPTY_EAT)(val)` évalue `op(val)` si `cond` est vrai, sinon renvoie un résultat vide avec `PP_EMPTY_EAT(val)`. La première moitié `PP_IF(cond, PP_WHILE_N+1, val PP_EMPTY_EAT)` renvoie `PP_WHILE_N+1` si `cond` est vrai, poursuivant ainsi la boucle avec les paramètres de la seconde moitié. Sinon elle renvoie `val PP_EMPTY_EAT`, qui devient le résultat final, tandis que `PP_EMPTY_EAT` absorbera le résultat de la seconde moitié.

La fonction `SUM` réalise la somme de `N + N-1 + ... + 1`. Elle démarre avec les valeurs initiales `(max_num, origin_num)` ; `SUM_PRED` prend le premier élément de la valeur `x` et vérifie s'il est supérieur à 0 ; `SUM_OP` opère une diminution de `x` avec l'opération `x = x - 1` et une addition de `y` avec l'opération `y = y + x`. Ces éléments sont directement transmis à la fonction `PP_WHILE` en utilisant `SUM_PRED` et `SUM_OP`, le résultat renvoyé est un tuple, et ce que l'on veut vraiment est le deuxième élément de ce tuple, pour cela nous utilisons à nouveau `SUM` pour obtenir la valeur du deuxième élément.

####Rentrée récursive

Jusqu'à présent, nos boucles de parcours et nos boucles conditionnelles ont bien fonctionné, les résultats correspondent à nos attentes. Vous vous souvenez de notre mention de l'interdiction de la réentrance récursive lors de l'exposé des règles de développement macro ? Malheureusement, nous avons rencontré cette interdiction lors de notre tentative d'exécution de boucles imbriquées.

``` cpp
#define SUM_OP2(xy_tuple) SUM_OP_OP_IMPL2 xy_tuple
#define SUM_OP_OP_IMPL2(x, y) (PP_DEC(x), y + SUM(x, 0))

#define SUM2(max_num, origin_num) \
    PP_IDENTITY(SUM_IMPL PP_WHILE(SUM_PRED, SUM_OP2, (max_num, origin_num)))

SUM2(1, a)      // -> a + SUM_IMPL PP_WHILE_1(SUM_PRED, SUM_OP, (1, a))
```

Remplacer le paramètre `op` par `SUM_OP2` dans `SUM2`, `SUM_OP2` fera appel à `SUM`, qui se déroulera en `PP_WHILE_1`, donc `PP_WHILE_1` se rappelle de lui-même de manière récursive, et le préprocesseur arrête le déroulement.

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

`PP_AUTO_WHILE` is the recursive automatic deduction version of `PP_WHILE`, with the core macro being `PP_AUTO_REC(PP_WHILE_PRED)`, which can identify the current available version number `N` of `PP_WHILE_N`.

Le principe de déduction est très simple : recherche de toutes les versions pour trouver celle qui peut se dérouler correctement, renvoie le numéro de cette version. Pour accélérer la recherche, on utilise généralement une recherche binaire, c'est ce que fait `PP_AUTO_REC`. `PP_AUTO_REC` prend un paramètre `check` qui est chargé de vérifier la disponibilité de la version. Ici, la plage de versions recherchée est `[1, 4]`. `PP_AUTO_REC` vérifiera d'abord `check(2)`. Si `check(2)` est vrai, alors il appellera `PP_AUTO_REC_12` pour rechercher dans la plage `[1, 2]`, sinon il utilisera `PP_AUTO_REC_34` pour rechercher dans `[3, 4]`. `PP_AUTO_REC_12` vérifie `check(1)`. Si c'est vrai, alors la version `1` est disponible sinon ce sera la version `2`. Même fonctionnement pour `PP_AUTO_REC_34`.

Vérification de la façon dont vous devez écrire le méta-programme pour savoir si la version est disponible. Ici, `PP_WHILE_PRED` sera décomposé en deux parties concaténées. Regardons la partie arrière `PP_WHILE_ ## n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`: si `PP_WHILE_ ## n` est disponible, cette partie sera décomposée pour obtenir la valeur de l'argument `val`, qui est `PP_WHILE_FALSE` car `PP_WHILE_FALSE` renvoie toujours `0`. Sinon, ce méta-programme restera inchangé, restant donc `PP_WHILE_n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`.

Concatenez le résultat de la seconde partie avec `PP_WHILE_CHECK_` de la première partie pour obtenir deux résultats possibles : `PP_WHILE_CHECK_PP_WHILE_FALSE` ou `PP_WHILE_CHECK_PP_WHILE_n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`. Ainsi, on fait en sorte que `PP_WHILE_CHECK_PP_WHILE_FALSE` renvoie `1` pour signaler que c'est utilisable, tandis que `PP_WHILE_CHECK_PP_WHILE_n` renvoie `0` pour dire que ce n'est pas utilisable. Avec cela, nous avons achevé la fonction de déduction automatique de la récursivité.

####Comparaison arithmétique

Non égal :

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

Vérifiez si les valeurs sont égales en utilisant la caractéristique de non-réentrance récursive. Concaténez de manière récursive `x` et `y` en tant que macro `PP_NOT_EQUAL_x PP_NOT_EQUAL_y`. Si `x == y`, alors `PP_NOT_EQUAL_y` ne sera pas développé, et sera concaténé avec `PP_NOT_EQUAL_CHECK_` en `PP_NOT_EQUAL_CHECK_PP_NOT_EQUAL_y` renvoyant ainsi `0`. En revanche, si les deux sont développés avec succès, vous obtiendrez finalement `PP_EQUAL_NIL`, et concaténé en `PP_NOT_EQUAL_CHECK_PP_EQUAL_NIL` renvoyant `1`.

Équivalent :

``` cpp
#define PP_EQUAL(x, y) PP_NOT(PP_NOT_EQUAL(x, y))

PP_EQUAL(1, 1)              // -> 1
PP_EQUAL(1, 3)              // -> 0

```

Inférieur ou égal à :

``` cpp
#define PP_LESS_EQUAL(x, y) PP_NOT(PP_SUB(x, y))

PP_LESS_EQUAL(2, 1)         // -> 0
PP_LESS_EQUAL(1, 1)         // -> 1
PP_LESS_EQUAL(1, 2)         // -> 1
```

Inférieur à :

``` cpp
#define PP_LESS(x, y) PP_AND(PP_LESS_EQUAL(x, y), PP_NOT_EQUAL(x, y))

PP_LESS(2, 1)               // -> 0
PP_LESS(1, 2)               // -> 1
PP_LESS(2, 2)               // -> 0
```

De plus, il existe des comparaisons arithmétiques telles que supérieur à, supérieur ou égal, etc., qui ne seront pas détaillées ici.

####Les opérations arithmétiques

En utilisant `PP_AUTO_WHILE`, nous pouvons réaliser des opérations arithmétiques de base, et même prendre en charge les opérations imbriquées.

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

Multiplication:

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

Dans cette implémentation de la multiplication, un paramètre `ret` a été ajouté, avec une valeur initiale de `0`, et à chaque itération, `ret = ret + x` est exécuté.

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

Hong peut aussi avoir des structures de données, en fait nous avons utilisé légèrement une structure de données `tuple` précédemment, `PP_REMOVE_PARENS` peut enlever les parenthèses extérieures du `tuple`, et renvoyer les éléments à l'intérieur. Nous prenons le `tuple` comme exemple pour discuter de sa mise en œuvre, les autres structures de données comme `list, array`, etc. peuvent être explorées dans les implémentations de `Boost`.

Le terme `tuple` est défini comme un ensemble d'éléments séparés par des virgules et enveloppés entre parenthèses : `(a, b, c)`.

``` cpp
#define PP_TUPLE_REMOVE_PARENS(tuple) PP_REMOVE_PARENS(tuple)

Obtenir l'élément à l'index spécifié
#define PP_TUPLE_ELEM(i, tuple) PP_ARGS_ELEM(i, PP_TUPLE_REMOVE_PARENS(tuple))

Avalez tout le tuple et retournes vide
#define PP_TUPLE_EAT() PP_EMPTY_EAT

Obtenir la taille
#define PP_TUPLE_SIZE(tuple) PP_ARGS_SIZE(PP_TUPLE_REMOVE_PARENS(tuple))

Ajouter un élément
#define PP_TUPLE_PUSH_BACK(elem, tuple) \
    PP_TUPLE_PUSH_BACK_IMPL(PP_TUPLE_SIZE(tuple), elem, tuple)
#define PP_TUPLE_PUSH_BACK_IMPL(size, elem, tuple) \
    (PP_TUPLE_REMOVE_PARENS(tuple) PP_IF(size, PP_COMMA, PP_EMPTY)() elem)

Insérer des éléments
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

Supprimer l'élément de la fin.
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

Voici une brève explication sur l'implémentation de l'insertion d'éléments, les autres opérations comme la suppression d'éléments sont également réalisées selon un principe similaire. `PP_TUPLE_INSERT(i, elem, tuple)` permet d'insérer l'élément `elem` à la position `i` dans le `tuple`. Pour réaliser cette opération, on commence par ajouter tous les éléments de position inférieure à `i` dans un nouveau `tuple` (`ret`) avec `PP_TUPLE_PUSH_BACK`, puis on insère l'élément `elem` à la position `i`, enfin on place les éléments de l'`tuple` initial ayant une position supérieure ou égale à `i` à la suite de `ret`. Enfin, `ret` contiendra le résultat souhaité.

##Résumé

(https://github.com/pfultz2/Cloak/wiki/C-Preprocessor-tricks,-tips,-and-idioms#deferred-expression)Les macros liées à `REPEAT` à l'intérieur de BOOST_PP, etc., peuvent être consultées par ceux qui s'y intéressent.

Le débogage de la programmation macro est une tâche laborieuse, nous pouvons :

Utilisez l'option `-P -E` pour afficher les résultats du prétraitement.
Utilisez la version modifiée de `clang` mentionnée plus tôt par moi-même pour examiner attentivement le processus de déploiement.
Démontez les macros complexes pour examiner les résultats de leur expansion.
Filtrer les fichiers d'en-tête et les macros non pertinents.
Enfin, il est temps de visualiser mentalement le processus de développement des macros. Une fois que vous maîtrisez le développement des macros, votre efficacité de débogage augmentera également.

Les macros dans ce texte ont été réimplémentées par moi-même après avoir compris les principes. Certaines ont été inspirées de la mise en œuvre de `Boost` et des articles référencés. Si vous repérez des erreurs, n'hésitez pas à me les signaler et à me contacter pour discuter de sujets connexes.

Le code de cet article est entièrement disponible ici : [Télécharger](assets/img/2021-3-31-cpp-preprocess/macros.cpp)，[démonstration en ligne](https://godbolt.org/z/coWvc5Pse)Translate these text into French language: "."


##Citation

* [Boost.Preprocessor](https://www.boost.org/doc/libs/1_75_0/libs/preprocessor/doc/)
(https://bot-man-jl.github.io/articles/?post=2020/Macro-Programming-Art)

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT. Veuillez donner votre [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Identifier tout manquement. 
