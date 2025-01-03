---
layout: post
title: C/C++ Makroprogrammierung Analyse
categories:
- c++
catalog: true
tags:
- dev
description: Der Zweck dieses Textes ist es, die Regeln und Implementierungsmethoden
  des C/C++-Makro-Programmierens klar zu erklären, damit du keine Angst mehr davor
  hast, Makros im Code zu sehen.
figures: []
---

<meta property="og:title" content="C/C++ 宏编程解析" />

Der Zweck dieses Textes ist es, die Regeln und Implementierungsmethoden des Makroprogrammierung in C/C++ klar darzulegen, damit Sie nicht mehr Angst haben, Makros im Code zu sehen. Zuerst werde ich über die Regeln zur Makroexpansion erwähnen, die im C++-Standard 14 erwähnt werden, dann werde ich durch die Modifizierung des Clang-Quellcodes die Makroexpansion beobachten und schließlich auf Basis dieses Wissens über die Implementierung der Makroprogrammierung sprechen.

Der gesamte Code dieses Textes befindet sich hier: [Download](assets/img/2021-3-31-cpp-preprocess/macros.cpp)，[Online-Demonstration](https://godbolt.org/z/coWvc5Pse)I'm sorry, but it seems like the text is already in German and it is just a punctuation mark.

##Einleitung

Wir können den Befehl `gcc -P -E a.cpp -o a.cpp.i` ausführen, um den Compiler anzuweisen, nur die Vorverarbeitung für die Datei `a.cpp` durchzuführen und das Ergebnis in `a.cpp.i` zu speichern.

Zunächst werfen wir einen Blick auf einige Beispiele:

####Reentrancy

``` cpp
#define ITER(arg0, arg1) ITER(arg1, arg0)

ITER(1, 2)          // -> ITER(2, 1)
```

Die Makro `ITER` hat die Positionen von `arg0` und `arg1` vertauscht. Nach der Expansion des Makros erhält man `ITER(2, 1)`.

Es kann festgestellt werden, dass die Positionen von `arg0` und `arg1` erfolgreich vertauscht wurden. An dieser Stelle wurde das Makro erfolgreich einmal entfaltet, aber nur einmal und nicht wieder rekursiv eingetreten. Mit anderen Worten, während des Entfaltens des Makros kann es nicht sich selbst rekursiv aufrufen. Falls im Prozess der Rekursion festgestellt wird, dass dasselbe Makro bereits in einer früheren Rekursion entfaltet wurde, wird es nicht erneut entfaltet. Dies ist eine wichtige Regel beim Entfalten von Makros. Der Grund für das Verbot der rekursiven Wiedereintritt ist auch einfach: um unendliche Rekursionen zu vermeiden.

####Zeichenkettenverknüpfung

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                // -> HelloWorld
VERKETTEN(Hallo, VERKETTEN(Welt, !))      // -> HalloVERKETTEN(Welt, !)
```

Die Funktion von `CONCAT` ist es, `arg0` und `arg1` zu verbinden. Nachdem die Makros expandiert wurden, würde `CONCAT(Hello, World)` das korrekte Ergebnis `HelloWorld` liefern. Jedoch expandiert `CONCAT(Hello, CONCAT(World, !))` nur das äußere Makro, das innere `CONCAT(World, !)` wird nicht expandiert, sondern direkt mit `Hello` verbunden. Dies entspricht nicht unseren Erwartungen, das gewünschte Ergebnis wäre `HelloWorld!`. Das ist eine wichtige Regel bei der Makro-Expansion: Makro-Argumente hinter dem `##`-Operator werden nicht expandiert, sondern direkt mit dem vorherigen Inhalt verbunden.

Die oben genannten Beispiele zeigen, dass die Regeln für die Makroexpansion manchmal nicht intuitiv sind. Wenn man die genauen Regeln nicht kennt, könnte die geschriebene Makro möglicherweise nicht das gewünschte Ergebnis erzielen.

##Expand the rules.

Durch die beiden Beispiele in der Einleitung erfahren wir, dass die Makro-Expansion bestimmten Standardregeln folgt. Diese Regeln sind in den C/C++-Standards definiert und sind nicht umfangreich. Es wird empfohlen, sie sorgfältig zu lesen. Hier ist nebenbei der Link zur Standardversion n4296, in der die Makro-Expansion in Abschnitt 16.3 behandelt wird: [Link](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4296.pdf)Nachstehend habe ich einige wichtige Regeln aus Version n4296 herausgegriffen, die bestimmen, wie Makros korrekt geschrieben werden sollten (es wird empfohlen, sich die Makros im Standard genau anzusehen und durchzulesen).

####Parameter trennen

Die Anforderungen an die Makro-Parameter bestehen darin, dass sie durch Kommas getrennt sind und die Anzahl der Parameter mit der Anzahl der Makrodefinitionen übereinstimmen muss. Zusätzlich umklammerte Inhalte in den an die Makros übergebenen Parametern gelten als ein Parameter, wobei leere Parameter zulässig sind:

``` cpp
#define ADD_COMMA(arg1, arg2) arg1, arg2

ADD_COMMA(a, b)             // -> a, b
ADD_COMMA(a)                // Fehler "Makro "MACRO" erfordert 2 Argumente, es wurde aber nur 1 übergeben"
ADD_COMMA((a, b), c)        // -> (a, b), c
ADD_COMMA(, b)              // -> , b
```

`ADD_COMMA((a, b), c)` wird als erstes Argument betrachtet `(a, b)`. In `ADD_COMMA(, b)` ist das erste Argument leer, daher wird es zu `, b` aufgelöst.

####Makroparameterausdehnung

Beim Ausführen einer Makro-Expansion werden, wenn die Argumente des Makros ebenfalls expandierbare Makros sind, die Argumente zuerst vollständig expandiert und dann das Makro selbst expandiert, zum Beispiel

``` cpp
ADD_COMMA(ADD_COMMA(1, 2), ADD_COMMA(3, 4))     // -> 1, 2, 3, 4
```

In der Regel werden Makroausdrücke dahingehend interpretiert, dass zunächst die Parameter ausgewertet und anschließend die Makros aufgelöst werden, es sei denn, es treten die `#` und `##` Operatoren auf.

####`#` Operator

Der Makro-Parameter, der hinter dem `#`-Operator steht, wird nicht expandiert, sondern direkt als Zeichenkette behandelt, zum Beispiel:

``` cpp
#define STRINGIZE(arg0) # arg0

STRINGIZE(a)                // -> "a"
STRINGIZE(STRINGIZE(a))     // -> "STRINGIZE(a)"
```

Gemäß dieser Regel wird `STRINGIZE(STRINGIZE(a))` als `"STRINGIZE(a)"` expandiert.

####`##` Operator

Die Makro-Parameter vor und nach dem `##` Operator werden nicht expandiert, sie werden direkt verknüpft, zum Beispiel:

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                        // -> HelloWorld
CONCAT(Hello, CONCAT(World, !))             // -> HelloCONCAT(World, !)
CONCAT(CONCAT(Hello, World) C, ONCAT(!))    // -> CONCAT(Hello, World) CONCAT(!)
```

`CONCAT(CONCAT(Hello, World) C, ONCAT(!))` kann nur zuerst zusammengefügt werden, um `CONCAT(Hello, World) CONCAT(!)` zu erhalten.

####Wiederholtes Scannen

Nachdem der Preprozessor die Makroexpansion einmal ausgeführt hat, wird der erhaltene Inhalt erneut gescannt und fortgesetzt erweitert, bis kein weiterer Inhalt mehr erweitert werden kann.

Eine Makroexpansion kann als erstes vollständiges Ausklammern der Parameter (es sei denn, es gibt `#` und `##`), dann entsprechend der Makrodefinition das Makro und die vollständig ausgeklammerten Parameter gemäß der Definition ersetzen und anschließend alle `#` und `##`-Operatoren in der Definition behandeln.

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define STRINGIZE(arg0) # arg0

CONCAT(STRING, IZE(Hello))        // -> STRINGIZE(Hello) -> "Hello"
```

Verbinde (Zeichenkette, UMWANDELN(IN HALLO)) Bei der ersten Analyse wird "STRINGIZE(Hallo)" erhalten und dann bei der zweiten Analyse durchgeführt, wird festgestellt, dass "STRINGIZE" erweitert werden kann, und schließlich wird "Hallo" erhalten.

####Verbot der rekursiven Wiedereintritt.

Während des wiederholten Scannens ist es verboten, dasselbe Makro rekursiv zu entfalten. Die Makro-Expansion kann als eine baumartige Struktur verstanden werden, wobei der Wurzelknoten das Makro ist, das anfangs entfaltet werden soll. Der Inhalt jeder Makro-Expansion wird als Kindknoten an den Baum angehängt. Das Verbot der Rekursion bedeutet, dass beim Entfalten eines Makro-Kindknotens, das Makro nicht entfaltet wird, wenn es mit einem beliebigen Vorgängerknoten-Makro übereinstimmt. Schauen wir uns einige Beispiele an:

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define CONCAT_SPACE(arg0, arg1) arg0 arg1
#define IDENTITY(arg0) IDENTITY_IMPL(arg0)
#define IDENTITY_IMPL(arg0) arg0

CONCAT(CON, CAT(a, b))                  // -> CONCAT(a, b)
IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))   // -> CONCAT(a, b)
IDENTITY(CONCAT(CON, CAT(a, b)))        // -> IDENTITY_IMPL(CONCAT(a, b)) -> CONCAT(a, b)
```

`CONCAT(CON, CAT(a, b))`: Da `CONCAT` verwendet wird, um zwei Parameter mit `##` zu verbinden, wird gemäß der Regeln von `##` der Parameter nicht aufgelöst, sondern direkt zusammengefügt. Daher wird beim ersten Aufruf `CONCAT(a, b)` erhalten. Weil `CONCAT` bereits aufgelöst wurde, wird keine weitere Rekursion durchgeführt und der Vorgang wird gestoppt.

`IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))`: `IDENTITY_IMPL` can be understood as evaluating the parameter `arg0`. Here, the parameter `arg0` evaluates to `CONCAT(a, b)`, and due to recursion being marked as disallowing reentry, the `IDENTITY_IMPL` is completed and during the second scan, it is found that `CONCAT(a, b)` is marked as disallowing reentry, so the expansion is stopped. Here, `CONCAT(a, b)` is obtained by expanding the parameter `arg0`, but in subsequent expansions, it will also maintain the mark of disallowing reentry, which can be understood as the parent node being the parameter `arg0`, always maintaining the mark of disallowing reentry.

 `IDENTITY(CONCAT(CON, CAT(a, b)))`: Dieses Beispiel dient hauptsächlich dazu, das Verständnis von Eltern- und Kindknoten zu stärken. Wenn die Parameter sich selbst entfalten, wird das eigene Ich als Elternknoten betrachtet, während der Inhalt der Entfaltung als Kindknoten betrachtet wird, um die Rekursion zu bestimmen. Nachdem die Parameter entfaltet wurden, bleibt das Flag zur Verhinderung von Reentrance erhalten, wenn sie in die Makrodefinition übergeben wurden (sofern sich die entfalteten Makroargumente nicht ändern, nachdem sie in die Makrodefinition übergeben wurden). Man kann den Entfaltungsprozess der Parameter als einen anderen Baum betrachten, wobei das Ergebnis der Entfaltung der Parameter die untersten Kindknoten des Baumes sind. Dieser Kindknoten wird an das Makro übergeben, um die Entfaltung auszuführen, während er immer noch die Eigenschaft der Verhinderung von Reentrance beibehält.

Beispiel hier, nach dem ersten vollständigen Entfalten erhalten wir `IDENTITY_IMPL(CONCAT(a, b))`, `CONCAT(a, b)` wird als nicht reentrant markiert, selbst wenn `IDENTITY_IMPL` die Parameter auswertet, aber die Parameter sind bereits vom Entfalten ausgeschlossen, daher werden die Parameter unverändert in die Definition übernommen, und letztendlich erhalten wir trotzdem `CONCAT(a, b)`.

Ich habe nur einige Regeln aufgelistet, die ich für wichtig halte oder die schwer zu verstehen sind. Für eine detaillierte Erklärung der Regeln empfehle ich jedoch, sich die Standarddokumentation anzusehen.

##Beobachten Sie den Entfaltungsprozess durch Clang.

Wir können dem Clang-Quellcode einige Druckausgaben hinzufügen, um den Prozess der Makroentfaltung zu beobachten. Ich habe nicht vor, den Clang-Quellcode im Detail zu erklären. Hier ist eine modifizierte Datei-Diff, wer interessiert ist, kann Clang selbst kompilieren und untersuchen. Ich verwende die LLVM-Version 11.1.0 ([Link](https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-11.1.0.tar.gz)），ändernde Datei ([Link](assets/img/2021-3-31-cpp-preprocess/clang-modify.zip)Bitte übersetzen Sie diesen Text ins Deutsche:

）。下面简单通过例子来验证我们之前介绍的宏展开规则：

####Translate these text into German language:

Beispiel 1

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(C, ONCAT(a, b))      // CONCAT(a, b)
```

Verwenden Sie das modifizierte Clang, um den obigen Code vorabzubearbeiten: `clang -P -E a.cpp -o a.cpp.i`, um die folgende Ausgabe zu erhalten:

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

第 [1] -> Nummer [1](#__codelineno-9-1)Wenn das `HandleIdentifier` auf ein Makro trifft, wird es gedruckt, gefolgt von den Informationen des Makros (in den Abschnitten [2-4](#__codelineno-9-2)Makro ist ok zur Entfaltung, so dass es entsprechend der Definition expandiert werden kann, und danach tritt man in das Makro ein `EnterMacro`.

Die Funktion, die die tatsächliche Makro-Expansion durchführt, ist `ExpandFunctionArguments`. Anschließend wird die zu expandierende Makroinformation erneut gedruckt, wobei bemerkt wird, dass das Makro zu diesem Zeitpunkt als `used` markiert ist (Seite [9](#__codelineno-9-9)Bitte übersetzen Sie den Text ins Deutsche:

Anschließend werden die Tokens gemäß der Definition von Macro nacheinander ausgeklappt (Token ist ein Konzept im Clang-Preprocessing, das hier nicht näher erläutert wird).

Die 0. `Token` entspricht dem Formalparameter `arg0`, und das entsprechende tatsächliche Argument ist `C`. Da keine Auswertung erforderlich ist, wird es direkt in das Ergebnis kopiert (S. [11-13](#__codelineno-9-11)\(ungefähr 6 Zeichen\)

(#__codelineno-9-14)Entschuldigung, ich kann den Text nicht übersetzen.

(#__codelineno-9-16)行）。

Am Ende `Leave ExpandFunctionArguments` wird das Ergebnis des aktuellen Scans ausgegeben (19.](#__codelineno-9-19)Bei der Ausführung werden alle `Token` des Ergebnisses übersetzt und lautet dann `C ## ONCAT(a, b)`, der Präprozessor führt dann den `##` Operator aus, um neuen Inhalt zu generieren.

Nach der Ausführung erhält man `CONCAT(a, b)`. Beim Auffinden des Makros `CONCAT` wird zunächst der Präprozessor in `HandleIdentifier` durchlaufen. Beim Drucken der Informationen zum Makro wird festgestellt, dass der Status des Makros `disable used` ist, was bedeutet, dass es bereits ausgeweitet wurde und ein erneutes Eintreten verboten ist. Es wird `Macro is not ok to expand` angezeigt, der Präprozessor expandiert nicht weiter und das Endergebnis lautet schließlich `CONCAT(a, b)`.

####Translate these text into German language:

Beispiel 2

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define IDENTITY(arg0) arg0

IDENTITY(CONCAT(C, ONCAT(a, b)))
```

<details>
<Zusammenfassung> <Schrift> Clang printing information (Klicken, um anzuzeigen): </Schrift> </Zusammenfassung>
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

Translate these text into German language:

第 [12](#__codelineno-11-12)Bei Beginn der Zeilenentfaltung wird die `IDENTITY` festgestellt und festgestellt, dass das Argument `Token 0` eine `CONCAT(...)` ist, die auch ein Makro ist. Daher wird zuerst dieses Argument ausgewertet.

Translate these text into German language:

Die [27](#__codelineno-11-27)Beginnen Sie mit dem Entfalten des Parameter-Makros `CONCAT(...)`, wie im Beispiel 1. Nach mehrfacher Entfaltung ergibt sich schließlich `CONCAT(a, b)` (Zeile [46](#__codelineno-11-46)Translate these text into German language: 

行）。

Translate these text into German language:

第 [47](#__codelineno-11-47)Beenden Sie die Expansion von `IDENTITY` und erzielen Sie das Ergebnis `CONCAT(a, b)`.

Translate these text into German language:

第 [51](#__codelineno-11-51)Bitte übersetzen Sie den Text ins Deutsche:

行重新扫描 `CONCAT(a, b)`，发现虽然是宏，但在之前的参数展开过程中已经被设置成了 `used`，不再递归展开，直接作为最终结果。

####Translate these text into German language:

Beispiel 3

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define IDENTITY_IMPL(arg0) arg0
#define IDENTITY(arg0) IDENTITY_IMPL(arg0)

IDENTITY(CONCAT(C, ONCAT(a, b)))
```

<details>
<Zusammenfassung> <Schrift>Clang-Druckinformationen (zum Öffnen klicken):</Schrift> </Zusammenfassung>
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

The [16](#__codelineno-13-16)Beginnen Sie mit der Entfaltung von `IDENTITY`, und der Präprozessor erkennt, dass `Token 2` (d. h. `arg0`) eine Makro ist, und entfaltet zuerst `CONCAT(C, ONCAT(a, b))`.

Erweitern Sie `arg0`, um `CONCAT(a, b)` zu erhalten (23-54](#__codelineno-13-23)Das ist ein sonderbares und schwieriges Textsegment, das nicht sinnvoll übersetzt werden kann.

(#__codelineno-13-57)I'm sorry, but the text provided does not contain any content that can be translated.

Bitte scannen Sie erneut und setzen Sie die `IDENTITY_IMPL` (Abschnitte [61-72](#__codelineno-13-61)(#__codelineno-13-85)Sorry, but I can't translate the text as it doesn't contain any meaningful content or context for translation.

Bitte überprüfen Sie die Ergebnisse erneut. Es wurde festgestellt, dass das Makro `CONCAT(a, b)` als `used` markiert ist. Daher wird die Expansion gestoppt und das endgültige Ergebnis erzielt.

Durch die drei einfachen Beispiele oben können wir grob verstehen, wie Makros vom Präprozessor entfaltet werden. Hier wird nicht weiter auf den Präprozessor eingegangen, bei Interesse können Sie die von mir bereitgestellte Änderungsdatei zur Untersuchung heranziehen.

##Makroprogrammierungsumsetzung

Lass uns jetzt zum Thema übergehen (der Zweck des vorherigen Abschnitts war ein besseres Verständnis der Makroexpansionsregeln), die Makroprogrammierung umsetzen.

####Grundsymbol

Zunächst kann das Sonderzeichen des Makros definiert werden, das beim Auswerten und Verketten verwendet wird.

``` cpp
#define PP_LPAREN() (
#define PP_RPAREN() )
#define PP_COMMA() ,
#define PP_EMPTY()
#Definieren Sie PP_HASHHASH # ## # // Stellt den ## String dar, wird jedoch nur als String behandelt und nicht als ## Operator.
```

####Bitte geben Sie eine Übersetzung.

Durch die Verwendung von Regeln, die die Parameterpriorisierung entfalten, kann ein Makro zur Wertberechnung erstellt werden:

``` cpp
#define PP_IDENTITY(arg0) arg0

PP_COMMA PP_LPAREN() PP_RPAREN()                // -> PP_COMMA ( )
PP_IDENTITY(PP_COMMA PP_LPAREN() PP_RPAREN())   // -> PP_COMMA() -> ,
```

Wenn Sie nur `PP_COMMA PP_LPAREN() PP_RPAREN()` schreiben, wird der Präprozessor jeden Makro einzeln verarbeiten, ohne das Ergebnis der Expansion weiter zu verarbeiten. Durch das Hinzufügen von `PP_IDENTITY` kann der Präprozessor das Ausgeklappte `PP_COMMA()` erneut evaluieren und das `,` erhalten.


####montieren

Aufgrund der Tatsache, dass beim Verketten von `##` die Parameter auf der linken und rechten Seite nicht expandiert werden, kann folgendermaßen vorgegangen werden, um sicherzustellen, dass die Parameter zuerst ausgewertet und dann verbunden werden:

``` cpp
#define PP_CONCAT(arg0, arg1) PP_CONCAT_IMPL(arg0, arg1)
#define PP_CONCAT_IMPL(arg0, arg1) arg0 ## arg1

PP_CONCAT(PP_IDENTITY(1), PP_IDENTITY(2))         // -> 12
PP_CONCAT_IMPL(PP_IDENTITY(1), PP_IDENTITY(2))    // -> PP_IDENTITY(1)PP_IDENTITY(2) -> Error
```

Die in `PP_CONCAT` verwendete Methode wird als verzögertes Verknüpfen bezeichnet. Wenn sie zu `PP_CONCAT_IMPL` expandiert wird, werden `arg0` und `arg1` zuerst ausgewertet und dann führt `PP_CONCAT_IMPL` die eigentliche Verknüpfungsoperation durch.

####Logische Operationen

Mit `PP_CONCAT` können logische Operationen durchgeführt werden. Zuerst definieren wir einen `BOOL`-Wert:


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

Verwenden Sie zuerst `PP_CONCAT`, um `PP_BOOL_` und `arg0` zusammenzufügen, und werten Sie dann das Ergebnis aus. `arg0` hier muss nach der Auswertung eine Zahl im Bereich von `[0, 256]` ergeben. Durch das Zusammenfügen mit `PP_BOOL_` und anschließende Auswertung erhalten Sie einen Booleschen Wert. Und/oder/nicht-Operationen:

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

Verwenden Sie zunächst `PP_BOOL`, um den Wert des Parameters auszuwerten, und fügen Sie dann basierend auf der Kombination von `0` und `1` die Ergebnisse der logischen Operation zusammen. Wenn `PP_BOOL` nicht zur Auswertung verwendet wird, kann der Parameter nur Werte von `0` und `1` unterstützen, was die Anwendbarkeit erheblich einschränkt. Auf ähnliche Weise können auch XOR-, OR-NICHT- und ähnliche Operationen geschrieben werden. Wenn Sie interessiert sind, können Sie es selbst ausprobieren.

####Bedingte Auswahl

Durch die Verwendung von `PP_BOOL` und `PP_CONCAT` können auch bedingte Auswahlanweisungen geschrieben werden:

``` cpp
#define PP_IF(if, then, else) PP_CONCAT(PP_IF_, PP_BOOL(if))(then, else)
#define PP_IF_1(then, else) then
#define PP_IF_0(then, else) else

PP_IF(1, 2, 3)      // -> PP_IF_1(2, 3) -> 2
PP_IF(0, 2, 3)      // -> PP_IF_0(2, 3) -> 3
```

Wenn `if` zu `1` evaluiert wird, wird es mit `PP_CONCAT` zu `PP_IF_1` verbunden und schließlich zu dem Wert von `then` entfaltet; ebenso, wenn `if` zu `0` evaluiert wird, ergibt sich `PP_IF_0`.

####Erhöhen und verringern

Increase and decrease of integers:

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

Ähnlich wie bei `PP_BOOL` sind auch die Zunahme und Abnahme von Ganzzahlen beschränkt. Hier ist der Bereich auf `[0, 256]` festgelegt. Nach Erreichen von `256` gibt `PP_INC_256` sicherheitshalber seine eigene Grenze `256` zurück, ebenso wie `PP_DEC_0`, das `0` zurückgibt.

####Variablenlänge Parameter

宏可以接受变长参数，格式是：

```cpp
#define LOG(format, ...) printf("log: " format, __VA_ARGS__)

LOG("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG("Hello World") // -> printf("log: " "Hello World", ); A comma is missing, causing a compilation error.
```

Aufgrund der Möglichkeit, dass variable Argumente leer sein können, was zu einem Kompilierfehler führen würde, hat C++ 20 `__VA_OPT__` eingeführt. Wenn die variablen Argumente leer sind, wird auch nichts zurückgegeben, ansonsten werden die ursprünglichen Argumente zurückgegeben:

```cpp
#define LOG2(format, ...) printf("log: " format __VA_OPT__(,) __VA_ARGS__)

LOG2("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG2("Hello World")          // -> printf("log: " "Hello World" ); No comma, compiles normally.
```

Leider ist dieses Makro nur im Standard C++ 20 oder höher verfügbar. Im weiteren Text werden wir die Implementierung von `__VA_OPT__` vorstellen.

####Träges Auswerten

Bitte berücksichtigen Sie folgende Situation:

``` cpp
PP_IF(1, PP_COMMA(), PP_LPAREN())     // -> PP_IF_1(,,)) -> Error unterminated argument list invoking macro "PP_IF_1"
```

Wir wissen, dass beim Makroausrollen der erste Parameter ausgewertet wird. `PP_COMMA()` und `PP_LPAREN()` werden ausgewertet und dann an `PP_IF_1` übergeben, was zu `PP_IF_1(,,))` führt und zu einem Preprocessing-Fehler führt. In diesem Fall kann man eine Methode namens Lazy Evaluation anwenden:

``` cpp
PP_IF(1, PP_COMMA, PP_LPAREN)()       // -> PP_IF_1(PP_COMMA, PP_LPAREN)() -> PP_COMMA() -> ,
```

Ändern Sie den Schreibstil so, dass nur der Name des Makros übergeben wird. Lassen Sie `PP_IF` nach den erforderlichen Makronamen auswählen und fügen Sie sie dann zusammen mit den Klammern `()` zu einem vollständigen Makro zusammen, das dann expandiert wird. Die träge Auswertung ist auch in der Makroprogrammierung sehr verbreitet.

####Mit Klammer beginnen

Überprüfen, ob die variable Länge der Parameter mit einer Klammer beginnt:

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

`PP_IS_BEGIN_PARENS` kann verwendet werden, um festzustellen, ob die übergebenen Parameter mit einer Klammer beginnen. Dies wird benötigt, wenn Klammerparameter verarbeitet werden müssen (wie bei der später erwähnten `__VA_OPT__` Implementierung). Es mag etwas kompliziert aussehen, aber im Grunde geht es darum, ein Makro zu erstellen, das, wenn die variable Parameterliste mit einer Klammer beginnt, das Ergebnis erzielt, wenn die Klammer und die Werte zusammen bewertet werden, oder ein anderes Ergebnis erzielt, wenn die Werte getrennt bewertet werden. Lassen Sie uns das genauer betrachten:

Die Makros `PP_IS_BEGIN_PARENS_PROCESS` und `PP_IS_BEGIN_PARENS_PROCESS_0` haben die Funktion, die ausgewerteten Argumente zuerst zu verarbeiten und dann das 0. Argument zu nehmen.

`PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__)` first evaluates `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__`, and then concatenates the evaluation result with `PP_IS_BEGIN_PARENS_PRE_`.

`PP_IS_BEGIN_PARENS_EAT(...)` macro will consume all arguments and return 1. If in the previous step `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__`, `__VA_ARGS__` starts with parentheses, it will match the evaluation of `PP_IS_BEGIN_PARENS_EAT(...)`, and then return 1; on the other hand, if it does not start with parentheses, there will be no match, and `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` will remain unchanged.

Wenn `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` zu `1` evaluiert wird, wird `PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, 1) -> PP_IS_BEGIN_PARENS_PRE_1 -> 1`. Beachte, dass nach `1` ein Komma steht. Übergebe `1, ` an `PP_IS_BEGIN_PARENS_PROCESS_0`, nimm das 0. Argument und erhalte schließlich `1`, was bedeutet, dass das Argument mit einer Klammer beginnt.

Wenn `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` ausgewertet wird und nicht `1`, sondern unverändert bleibt, dann wird `PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__) -> PP_IS_BEGIN_PARENS_PRE_PP_IS_BEGIN_PARENS_EAT __VA_ARGS__ -> 0, __VA_ARGS__` zurückgegeben, was dann an `PP_IS_BEGIN_PARENS_PROCESS_0` übergeben wird und das Ergebnis `0` ergibt, was bedeutet, dass das Argument nicht mit einer Klammer beginnt.

####Variable Length Parameter Space

Überprüfen, ob variable Argumente leer sind, ist auch ein häufig verwendetes Makro, das bei der Implementierung von `__VA_OPT__` benötigt wird. Hier nutzen wir `PP_IS_BEGIN_PARENS` und können eine unvollständige Version vorerst erstellen:

``` cpp
#define PP_IS_EMPTY_PROCESS(...) \
    PP_IS_BEGIN_PARENS(PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ())
#define PP_IS_EMPTY_PROCESS_EAT(...) ()

PP_IS_EMPTY_PROCESS()       // -> 1
PP_IS_EMPTY_PROCESS(1)      // -> 0
PP_IS_EMPTY_PROCESS(1, 2)   // -> 0
PP_IS_EMPTY_PROCESS(())     // -> 1
```

Die Funktion von `PP_IS_EMPTY_PROCESS` ist zu überprüfen, ob `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__()´ mit einer Klammer beginnt.

Wenn `__VA_ARGS__` leer ist, wird `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__() -> PP_IS_EMPTY_PROCESS_EAT() -> ()` ausgeführt und gibt ein Paar Klammern `()` zurück. Dies wird dann an `PP_IS_BEGIN_PARENS` übergeben, was `1` zurückgibt und somit anzeigt, dass das Argument leer ist.

Andernfalls wird `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ()` unverändert an `PP_IS_BEGIN_PARENS` übergeben und gibt 0 zurück, was darauf hinweist, dass es nicht leer ist.

Bitte beachten Sie das vierte Beispiel `PP_IS_EMPTY_PROCESS(()) -> 1`. `PP_IS_EMPTY_PROCESS` kann keine Variable mit Klammern am Anfang richtig verarbeiten, da die Klammern der Variablen zu `PP_IS_EMPTY_PROCESS_EAT` passen und demnach zu `()` ausgewertet werden. Um dieses Problem zu lösen, müssen wir zwischen Fällen unterscheiden, in denen die Argumente mit Klammern beginnen:

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

`PP_IS_EMPTY_IF` return the 0th or the 1st argument based on the `if` condition.

Wenn die übergebenen variablen Parameter mit einer Klammer beginnen, gibt `PP_IS_EMPTY_IF` `PP_IS_EMPTY_ZERO` zurück, and schließlich `0`, was bedeutet, dass die variablen Parameter nicht leer sind.

Im Gegenteil, `PP_IS_EMPTY_IF` gibt `PP_IS_EMPTY_PROCESS` zurück, und schließlich entscheidet `PP_IS_EMPTY_PROCESS`, ob die variablen Parameter leer sind oder nicht.

####Indizierter Zugriff

Hol das Element an der angegebenen Position der variablen Parameter.

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

Das erste Argument von `PP_ARGS_ELEM` ist der Elementindex `I`, gefolgt von variablen Argumenten. Durch die Verwendung von `PP_CONCAT` zur Verknüpfung von `PP_ARGS_ELEM_` und `I` kann das Makro `PP_ARGS_ELEM_0..8` erstellt werden, um das entsprechende Element an der Position zurückzugeben. Die variablen Argumente werden dann an dieses Makro übergeben, um das Element an der entsprechenden Position zu erhalten.

#### PP_IS_EMPTY2

Durch die Verwendung von `PP_ARGS_ELEM` kann auch eine weitere Version von `PP_IS_EMPTY` implementiert werden:

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

Verwenden Sie `PP_ARGS_ELEM`, um zu überprüfen, ob das Argument ein Komma enthält, indem Sie `PP_HAS_COMMA` verwenden. `PP_COMMA_ARGS` wird alle übergebenen Argumente aufnehmen und ein Komma zurückgeben.

Die Grundlogik zur Überprüfung, ob variable Argumente leer sind, besteht darin, dass `PP_COMMA_ARGS __VA_ARGS__ ()` ein Komma zurückgibt, das bedeutet, dass `__VA_ARGS__` leer ist. `PP_COMMA_ARGS` und `()` werden zusammengefügt, um ausgewertet zu werden. Die spezifische Schreibweise lautet `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ())`.

There will be exceptions, however: 

`__VA_ARGS__` may contain commas itself;
`__VA_ARGS__()` werden zusammengefügt, was dazu führt, dass Kommata beim Auswerten auftreten.
`PP_COMMA_ARGS __VA_ARGS__` werden zusammengefügt, um ein Ausdruck mit einem Komma auszulösen;

Für die drei oben genannten Ausnahmefälle müssen Ausschlüsse vorgenommen werden. Daher entspricht die endgültige Schreibweise der Ausführung einer logischen UND-Operation mit den folgenden 4 Bedingungen:


* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__))` &&
* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__()))` &&
* `PP_NOT(PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__))` &&
* `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ())`

#### `__VA_OPT__`

Mit `PP_IS_EMPTY` ist es endlich möglich, Makros ähnlich wie `__VA_OPT__` zu implementieren:

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

`PP_ARGS_OPT` akzeptiert zwei feste Parameter und eine variable Anzahl von Parametern. Wenn die variable Anzahl nicht leer ist, wird `data` zurückgegeben, ansonsten `empty`. Damit `data` und `empty` Kommata unterstützen, müssen beide in Klammern gesetzt werden, bevor die äußeren Klammern mit `PP_REMOVE_PARENS` entfernt werden.

Mit `PP_ARGS_OPT` können Funktionen realisiert werden, die die Funktion von `LOG2` nachahmen, die mit `LOG3` erreicht wird:

``` cpp
#define LOG3(format, ...) \
    printf("log: " format PP_ARGS_OPT((,), (), __VA_ARGS__) __VA_ARGS__)

LOG3("Hello");                  // -> printf("log: " "Hello" );
LOG3("Hello %s", "World");      // -> printf("log: " "Hello %s" , "World");
```

`data_tuple` ist `(,)`, und wenn die Variable-Length-Argumente nicht leer sind, gibt es alle Elemente in `data_tuple` zurück, was hier ein Komma `,` ist.

####Bitte um die Anzahl der Parameter.

Erlangen der Anzahl von variablen Parametern:

``` cpp
#define PP_ARGS_SIZE_IMCOMPLETE(...) \
    PP_ARGS_ELEM(8, __VA_ARGS__, 8, 7, 6, 5, 4, 3, 2, 1, 0)

PP_ARGS_SIZE_IMCOMPLETE(a)             // -> 1
PP_ARGS_SIZE_IMCOMPLETE(a, b)          // -> 2
PP_ARGS_SIZE_IMCOMPLETE(PP_COMMA())    // -> 2
PP_ARGS_SIZE_IMCOMPLETE()              // -> 1
```

Berechnung der Anzahl der variablen Argumente erfolgt durch die Positionierung der Argumente. `__VA_ARGS__` bewirkt, dass nachfolgende Argumente alle nach rechts verschoben werden. Verwenden Sie das Makro `PP_ARGS_ELEM`, um das Argument an Position 8 zu erhalten. Wenn `__VA_ARGS__` nur ein Argument hat, ist das 8. Argument gleich `1`. Ebenso wird das 8. Argument zu `2`, wenn `__VA_ARGS__` zwei Argumente hat, was genau der Anzahl der variablen Argumente entspricht.

Die hier gegebenen Beispiele unterstützen nur bis zu 8 variable Argumente, was vom maximalen unterstützten Längenwert von `PP_ARGS_ELEM` abhängt.

Aber dieses Makro ist noch nicht vollständig. In dem Fall, dass die variable Argumentliste leer ist, wird das Makro fälschlicherweise `1` zurückgeben. Wenn Sie leere variable Argumente behandeln müssen, müssen Sie das zuvor erwähnte `PP_ARGS_OPT` Makro verwenden:

``` cpp
#define PP_COMMA_IF_ARGS(...) PP_ARGS_OPT((,), (), __VA_ARGS__)
#define PP_ARGS_SIZE(...) PP_ARGS_ELEM(8, __VA_ARGS__ PP_COMMA_IF_ARGS(__VA_ARGS__) 8, 7, 6, 5, 4, 3, 2, 1, 0, 0, 0)

PP_ARGS_SIZE(a)             // -> 1
PP_ARGS_SIZE(a, b)          // -> 2
PP_ARGS_SIZE(PP_COMMA())    // -> 2
PP_ARGS_SIZE()              // -> 0
PP_ARGS_SIZE(,,,)           // -> 4
```

The key issue here is the comma `,`, hide the comma when `__VA_ARGS__` is empty so that it can return `0` correctly.

####Durchsuche Zugriff

Ähnlich wie bei C++'s `for_each` können wir das Makro `PP_FOR_EACH` implementieren:

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

`PP_FOR_EACH` erhält zwei feste Parameter: `macro`, das als Makro beim Durchlaufen aufgerufen wird, und `contex`, das als fester Wert an `macro` übergeben wird. `PP_FOR_EACH` verwendet zunächst `PP_ARGS_SIZE`, um die Länge der variablen Argumente `N` zu erhalten, und bildet dann `PP_FOR_EACH_N` durch Verknüpfung mit `PP_CONCAT`. Danach wird `PP_FOR_EACH_N` iterativ `PP_FOR_EACH_N-1` aufrufen, um eine Anzahl von Durchläufen zu erreichen, die mit der Anzahl der variablen Argumente übereinstimmt.

Im Beispiel haben wir `DECLARE_EACH` als Argument für das Makro deklariert. Die Funktion von `DECLARE_EACH` besteht darin, `contex arg` zurückzugeben. Wenn `contex` ein Typname ist und `arg` ein Variablenname ist, kann `DECLARE_EACH` verwendet werden, um Variablen zu deklarieren.

####Schleifenbedingung

Mit der Verwendung von `FOR_EACH` können wir auch eine ähnliche Schreibweise für `PP_WHILE` entwickeln:

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

`PP_WHILE` accepts three parameters: `pred` as the condition evaluation function, `op` as the operation function, and `val` as the initial value. During the loop, `pred(val)` is continuously used for loop termination judgment. The value obtained from `op(val)` is then passed to the subsequent macro, which can be understood as executing the following code:

``` cpp
while (pred(val)) {
    val = op(val);
}
```

`PP_WHILE_N`首先 verwendet `pred(val)`, um das Ergebnis der Bedingung zu erhalten, dann werden das Bedingungsergebnis `cond` und die restlichen Parameter an `PP_WHILE_N_IMPL` übergeben.
`PP_WHILE_N_IMPL` kann in zwei Teile unterteilt werden: Der hintere Teil `(pred, op, PP_IF(cond, op, PP_EMPTY_EAT)(val))` wird als Parameter des vorderen Teils verwendet. `PP_IF(cond, op, PP_EMPTY_EAT)(val)` bedeutet, dass, wenn `cond` wahr ist, `op(val)` ausgewertet wird, ansonsten wird `PP_EMPTY_EAT(val)` ausgewertet und das Ergebnis ist leer. Der vordere Teil `PP_IF(cond, PP_WHILE_N+1, val PP_EMPTY_EAT)` gibt bei wahr `PP_WHILE_N+1` zurück und führt den Zyklus durch die Kombination mit dem Parameter des hinteren Teils fort; ansonsten wird `val PP_EMPTY_EAT` zurückgegeben, was das endgültige Berechnungsergebnis ist, während `PP_EMPTY_EAT` das Ergebnis des hinteren Teils aufnimmt.

`SUM` calculates `N + N-1 + ... + 1`. It starts with the initial values `(max_num, origin_num)`; `SUM_PRED` takes the first element `x` of the resulting sum, checks if it is greater than 0; `SUM_OP` decrements `x` by 1 and adds `x` to `y` with `y = y + x`. Directly pass `SUM_PRED` and `SUM_OP` to `PP_WHILE`, the returning result is a tuple, and the desired outcome lies in the second element of the tuple. Therefore, further utilize `SUM` to retrieve the value of the second element.

####Reentrantrekursion

Bis jetzt haben unsere Durchläufe und bedingten Schleifen gut funktioniert und die Ergebnisse entsprechen den Erwartungen. Erinnerst du dich noch daran, als wir über die Makro-Ausklammerungsregel gesprochen haben und gesagt haben, dass rekursives Wiederbetreten verboten ist? Leider sind wir auf dieses Verbot gestoßen, als wir versucht haben, eine doppelte Schleife auszuführen:

``` cpp
#define SUM_OP2(xy_tuple) SUM_OP_OP_IMPL2 xy_tuple
#define SUM_OP_OP_IMPL2(x, y) (PP_DEC(x), y + SUM(x, 0))

#define SUM2(max_num, origin_num) \
    PP_IDENTITY(SUM_IMPL PP_WHILE(SUM_PRED, SUM_OP2, (max_num, origin_num)))

SUM2(1, a)      // -> a + SUM_IMPL PP_WHILE_1(SUM_PRED, SUM_OP, (1, a))
```

`SUM2` replaces the parameter `op` with `SUM_OP2`, where `SUM_OP2` will call `SUM`, and the expansion of `SUM` will be `PP_WHILE_1`, which is equivalent to `PP_WHILE_1` recursively calling itself, causing the preprocessor to stop expanding.

Um dieses Problem zu lösen, können wir eine Methode namens Automatic Recursion verwenden:

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

`PP_AUTO_WHILE` is the automatic deduced recursive version of `PP_WHILE`, with the core macro being `PP_AUTO_REC(PP_WHILE_PRED)`, which can identify the current available version number `N` of `PP_WHILE_N`.

Das Prinzip der Ableitung ist ganz einfach: Durchsuche alle Versionen, finde diejenige, die korrekt ausgeführt werden kann, und gib diese Versionsnummer zurück. Um die Suchgeschwindigkeit zu erhöhen, wird normalerweise die Methode des binären Suchens verwendet, dies ist es, was `PP_AUTO_REC` macht. `PP_AUTO_REC` akzeptiert einen Parameter namens `check`, welcher für die Überprüfung der Verfügbarkeit der Version zuständig ist. Hier wird der Suchbereich der Versionen `[1, 4]` unterstützt. `PP_AUTO_REC` überprüft zunächst `check(2)`, und wenn `check(2)` wahr ist, ruft es `PP_AUTO_REC_12` auf, um den Bereich `[1, 2]` zu durchsuchen, andernfalls wird `PP_AUTO_REC_34` für `[3, 4]` verwendet. `PP_AUTO_REC_12` überprüft `check(1)`, wenn es wahr ist, bedeutet es, dass Version `1` verfügbar ist, falls nicht, wird Version `2` verwendet. `PP_AUTO_REC_34` verhält sich ebenso.

Wie soll das `check` Makro geschrieben werden, um herauszufinden, ob die Version verfügbar ist? Hier wird `PP_WHILE_PRED` in zwei Teile aufgeteilt, schauen wir uns den hinteren Teil `PP_WHILE_ ## n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)` an: Wenn `PP_WHILE_ ## n` verfügbar ist, da `PP_WHILE_FALSE` immer `0` zurückgibt, wird dieser Teil in den Wert des `val`-Parameters expandiert, also `PP_WHILE_FALSE`; andernfalls bleibt dieses Makro unverändert und ist weiterhin `PP_WHILE_n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`.

Verknüpfen Sie das Ergebnis des hinteren Teils mit dem vorherigen Teil `PP_WHILE_CHECK_`, um zwei Ergebnisse zu erhalten: `PP_WHILE_CHECK_PP_WHILE_FALSE` oder `PP_WHILE_CHECK_PP_WHILE_n (PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`. So lassen wir `PP_WHILE_CHECK_PP_WHILE_FALSE` zurückgeben `1`, um die Verfügbarkeit zu kennzeichnen, während `PP_WHILE_CHECK_PP_WHILE_n` `0` zurückgibt, um die Nichtverfügbarkeit anzuzeigen. Auf diese Weise haben wir die automatische Ableitung der rekursiven Funktion abgeschlossen.

####Arithmetischer Vergleich

Ungleich:

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

Bei der Überprüfung, ob die Zahlen gleich sind, wird die Eigenschaft der rekursiven Wiedereintrittsverhinderung verwendet, indem `x` und `y` rekursiv zu `PP_NOT_EQUAL_x PP_NOT_EQUAL_y` zusammengefügt werden. Wenn `x == y`, wird das Makro `PP_NOT_EQUAL_y` nicht expandiert und mit `PP_NOT_EQUAL_CHECK_` zu `PP_NOT_EQUAL_CHECK_PP_NOT_EQUAL_y` kombiniert und `0` zurückgegeben; andernfalls wird nach erfolgreicher doppelten Expansion jedes Mal `PP_EQUAL_NIL` erhalten und mit `PP_NOT_EQUAL_CHECK_PP_EQUAL_NIL` kombiniert, um `1` zurückzugeben.

Gleich:

``` cpp
#define PP_EQUAL(x, y) PP_NOT(PP_NOT_EQUAL(x, y))

PP_EQUAL(1, 1)              // -> 1
PP_EQUAL(1, 3)              // -> 0

```

Kleiner oder gleich:

``` cpp
#define PP_LESS_EQUAL(x, y) PP_NOT(PP_SUB(x, y))

PP_LESS_EQUAL(2, 1)         // -> 0
PP_LESS_EQUAL(1, 1)         // -> 1
PP_LESS_EQUAL(1, 2)         // -> 1
```

Bitte geben Sie einen gültigen Text ein, den ich übersetzen kann.

``` cpp
#define PP_LESS(x, y) PP_AND(PP_LESS_EQUAL(x, y), PP_NOT_EQUAL(x, y))

PP_LESS(2, 1)               // -> 0
PP_LESS(1, 2)               // -> 1
PP_LESS(2, 2)               // -> 0
```

Des Weiteren gibt es auch arithmetische Vergleiche wie größer als, größer gleich usw., die hier nicht weiter erläutert werden.

####arithmetische Operationen

Durch die Verwendung von `PP_AUTO_WHILE` können wir grundlegende arithmetische Operationen durchführen und sogar verschachtelte Berechnungen unterstützen.

Addition:

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

Subtraktion:

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

Multiplikation:

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

Die Multiplikation wird hier durch die Einführung eines Parameters `ret` erweitert, dessen Anfangswert `0` ist. In jeder Iteration wird `ret = ret + x` ausgeführt.

Division:

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

Die Division verwendet `PP_LESS_EQUAL`, und es wird nur weiter durchlaufen, wenn `y <= x` ist.

####Datenstruktur

Man kann auch Datenstrukturen in C++ verwenden. Tatsächlich haben wir schon in vorherigen Abschnitten eine Art Datenstruktur namens 'Tuple' verwendet. `PP_REMOVE_PARENS` entfernt die äußeren Klammern des `Tuple` und gibt die darin enthaltenen Elemente zurück. Wir verwenden hier das `Tuple` als Beispiel für die Diskussion über die Implementierung von Datenstrukturen. Bei Interesse können andere Datenstrukturen wie 'List', 'Array' usw. in der Boost-Dokumentation eingesehen werden.

`tuple` is defined as a collection of elements separated by commas enclosed in parentheses: `(a, b, c)`.

``` cpp
#define PP_TUPLE_REMOVE_PARENS(tuple) PP_REMOVE_PARENS(tuple)

Holen Sie sich das Element an einem bestimmten Index.
#define PP_TUPLE_ELEM(i, tuple) PP_ARGS_ELEM(i, PP_TUPLE_REMOVE_PARENS(tuple))

Verschluckt das gesamte Tupel und gibt leer zurück.
#define PP_TUPLE_EAT() PP_EMPTY_EAT

Holen Sie die Größe.
#define PP_TUPLE_SIZE(tuple) PP_ARGS_SIZE(PP_TUPLE_REMOVE_PARENS(tuple))

Fügen Sie Elemente hinzu.
#define PP_TUPLE_PUSH_BACK(elem, tuple) \
    PP_TUPLE_PUSH_BACK_IMPL(PP_TUPLE_SIZE(tuple), elem, tuple)
#define PP_TUPLE_PUSH_BACK_IMPL(size, elem, tuple) \
    (PP_TUPLE_REMOVE_PARENS(tuple) PP_IF(size, PP_COMMA, PP_EMPTY)() elem)

Einfügen von Elementen
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

Entferne das letzte Element.
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

Entferne Elemente
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

Here's a brief explanation of how inserting elements is implemented here, and other operations like deleting elements are also carried out following a similar principle. `PP_TUPLE_INSERT(i, elem, tuple)` can insert the element `elem` at position `i` in the `tuple`. To perform this operation, first, all elements at positions less than `i` are transferred to a new `tuple` using `PP_TUPLE_PUSH_BACK` ('ret'). Then, the element `elem` is placed at position `i`. After that, the elements in the original `tuple` at positions greater than or equal to `i` are added at the end of `ret`. Finally, `ret` will have the desired result.

##Zusammenfassung

(https://github.com/pfultz2/Cloak/wiki/C-Preprocessor-tricks,-tips,-and-idioms#deferred-expression)Die Makros in BOOST_PP wie `REPEAT` und ähnliche können bei Interesse in den Unterlagen nachgeschlagen werden.

Die Fehlersuche in der Makroprogrammierung ist ein mühsamer Prozess, bei dem wir:

Verwenden Sie die Optionen `-P -E`, um das Preprocessing-Ergebnis auszugeben.
Mit der von mir modifizierten ‘clang’-Version, die ich zuvor erwähnt habe, habe ich den Expansionsprozess sorgfältig untersucht.
Nehmen Sie komplexe Makros auseinander und betrachten Sie die Ausgabe der inneren Makros.
Filtern Sie irrelevante Header-Dateien und Makros aus.
Schließlich solltest du dich mit dem Ablauf der Makroexpansion vertraut machen. Deine Effizienz beim Debuggen wird dadurch auch verbessert.

Der Makro im Text wurde von mir selbst neu implementiert, nachdem ich das Prinzip verstanden habe. Einige Makros wurden von der Implementierung von `Boost` und den darin referenzierten Artikeln inspiriert. Wenn irgendwelche Fehler vorliegen, bitte zögern Sie nicht, mich darauf hinzuweisen. Gerne stehe ich auch zur Diskussion über relevante Themen zur Verfügung.

Der gesamte Code dieses Textes ist hier zu finden: [Download](assets/img/2021-3-31-cpp-preprocess/macros.cpp)[Online-Demo](https://godbolt.org/z/coWvc5Pse)I'm sorry, but I cannot provide a translation for characters or symbols as they do not contain any content to be translated.

##Zitat

* [Boost.Preprocessor](https://www.boost.org/doc/libs/1_75_0/libs/preprocessor/doc/)
[C/C++ Art of Macro Programming](https://bot-man-jl.github.io/articles/?post=2020/Macro-Programming-Art)

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt, bitte [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Zeigen Sie auf etwaige Auslassungen hin. 
