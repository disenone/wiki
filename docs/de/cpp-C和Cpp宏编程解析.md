---
layout: post
title: C/C++ Makroprogrammierung Analyse
categories:
- c++
catalog: true
tags:
- dev
description: Der Zweck dieses Artikels ist es, die Regeln und Implementierungsmethoden
  der C/C++-Makroprogrammierung zu erläutern, damit du keine Angst mehr hast, Makros
  im Code zu sehen.
figures: []
---

<meta property="og:title" content="C/C++ 宏编程解析" />

Der Zweck dieses Textes ist es, die Regeln und Implementierungsmethoden der Makroprogrammierung in C/C++ klar zu erklären, damit du nicht mehr Angst hast, Makros im Code zu sehen. Ich werde zunächst die Regeln für die Makroexpansion erwähnen, die im C++ Standard 14 definiert sind, dann werde ich durch die Modifikation des Quellcodes von Clang die Makroexpansion beobachten und schließlich werde ich auf Basis dieses Wissens über die Implementierung der Makroprogrammierung sprechen.

Der gesamte Code dieses Artikels befindet sich hier: [Herunterladen](assets/img/2021-3-31-cpp-preprocess/macros.cpp)，[Online-Demo](https://godbolt.org/z/coWvc5Pse)I'm sorry, but I can't provide a translation without any text. Could you please provide the text you would like me to translate into German?

##Einleitung

You can execute the command `gcc -P -E a.cpp -o a.cpp.i` to make the compiler only perform preprocessing on the file `a.cpp` and save the result in `a.cpp.i`.

Zunächst werfen wir einen Blick auf einige Beispiele:

####Reentrancy

``` cpp
#define ITER(arg0, arg1) ITER(arg1, arg0)

ITER(1, 2)          // -> ITER(2, 1)
```

Die `ITER`-Makro tauscht die Positionen von `arg0` und `arg1` aus. Nach dem Ausklappen des Makros erhält man `ITER(2, 1)`.

Man kann sehen, dass `arg0` und `arg1` erfolgreich ausgetauscht wurden. An dieser Stelle wurde das Makro einmal erfolgreich ausgeführt, aber nur einmal und nicht rekursiv wieder aufgerufen. Anders ausgedrückt, im Prozess des Makro-Aufrollens ist es nicht erlaubt, sich selbst rekursiv zu wiederholen. Wenn festgestellt wird, dass dasselbe Makro bereits in vorherigen Rekursionen aufgerollt wurde, wird es nicht noch einmal aufgerollt. Das ist eine wichtige Regel beim Makro-Aufrollen. Der Grund für das Verbot der rekursiven Wiedereingabe ist ebenfalls sehr einfach: Es soll unendliche Rekursionen vermeiden.

####Stringverkettung

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                // -> HelloWorld
VERKETTEN(Hello, VERKETTEN(World, !))     // ->　HelloVERKETTEN(World, !)
```

Das Ziel des Makros `CONCAT` ist es, `arg0` und `arg1` zu verketten. Nach der Makroerweiterung ergibt `CONCAT(Hello, World)` das korrekte Ergebnis `HelloWorld`. Allerdings wird bei `CONCAT(Hello, CONCAT(World, !))` nur das äußere Makro erweitert, während das innere `CONCAT(World, !)` nicht erweitert wird, sondern direkt an `Hello` angefügt wird, was nicht dem entspricht, was wir uns vorgestellt haben. Das Ergebnis, das wir tatsächlich wollen, ist `HelloWorld!`. Dies ist eine weitere wichtige Regel für die Makroerweiterung: Die Makroparameter, die direkt nach dem `##`-Operator stehen, werden nicht erweitert, sondern direkt mit dem vorhergehenden Inhalt verknüpft.

Anhand der beiden obigen Beispiele lässt sich erkennen, dass einige Regeln der Makroerweiterung kontraintuitiv sind. Wenn die spezifischen Regeln nicht klar sind, könnte das geschriebene Makro nicht mit dem gewünschten Effekt übereinstimmen.

##Makroerweiterungsregeln

Durch die beiden Beispiele im Vorwort haben wir erfahren, dass die Makro-Expansion bestimmten Standardregeln folgt, die im C/C++-Standard definiert sind. Es ist nicht viel Text, daher empfehle ich, ihn sorgfältig mehrmals zu lesen. Hier ist nebenbei der Link zur Standardversion n4296, Abschnitt 16.3 über die Makro-Expansion: [Link](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4296.pdf)Ich habe hier einige wichtige Regeln aus der Version n4296 ausgewählt, die entscheiden, wie man Makros korrekt schreibt (es wird empfohlen, sich die Zeit zu nehmen und die Makros im Standard gründlich zu lesen).

####Parameter separieren

Die Anforderungen der Makro-Parameter sind durch Kommas getrennt und die Anzahl der Parameter muss mit der Anzahl der Makrodefinitionen übereinstimmen. Zusätzlich durch Klammern eingeschlossene Inhalte in den an das Makro übergebenen Parametern gelten als ein Parameter. Die Parameter können leer sein.

``` cpp
#define ADD_COMMA(arg1, arg2) arg1, arg2

ADD_COMMA(a, b)             // -> a, b
ADD_COMMA(a)                // Fehler "Makro "MACRO" erfordert 2 Argumente, aber nur 1 gegeben"
ADD_COMMA((a, b), c)        // -> (a, b), c
ADD_COMMA(, b)              // -> , b
```

`ADD_COMMA((a, b), c)` betrachtet `(a, b)` als ersten Parameter. In `ADD_COMMA(, b)` ist der erste Parameter leer, daher wird es zu `, b` erweitert.

####Makroparametererweiterung

Beim Entpacken eines Makros, wenn die Parameter des Makros ebenfalls entpackbare Makros sind, werden die Parameter zuerst vollständig entpackt, bevor das Makro selbst entpackt wird, zum Beispiel

``` cpp
ADD_COMMA(ADD_COMMA(1, 2), ADD_COMMA(3, 4))     // -> 1, 2, 3, 4
```

In der Regel wird die Makroexpansion so verstanden, dass zuerst die Parameter ausgewertet und dann die Makros ausgewertet werden, es sei denn, es treten die `#` und `##` Operatoren auf.

####`#` Operatoren

Der Makro-Parameter, der nach dem `#`-Operator steht, wird nicht expandiert, sondern direkt als Zeichenkette behandelt. Zum Beispiel:

``` cpp
#define STRINGIZE(arg0) # arg0

STRINGIZE(a)                // -> "a"
STRINGIZE(STRINGIZE(a))     // -> "STRINGIZE(a)"
```

Nach dieser Regel kann `STRINGIZE(STRINGIZE(a))` nur zu `"STRINGIZE(a)"` entrollt werden.

####`##` Operator

`##` Die Makroparameter vor und nach dem Operator werden nicht expandiert, sondern direkt zusammengefügt, zum Beispiel:

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                        // -> HelloWorld
CONCAT(Hello, CONCAT(World, !))             // -> HelloCONCAT(World, !)
CONCAT(CONCAT(Hello, World) C, ONCAT(!))    // -> CONCAT(Hello, World) CONCAT(!)
```

`CONCAT(CONCAT(Hello, World) C, ONCAT(!))` kann nur zuerst zusammengefügt werden, um `CONCAT(Hello, World) CONCAT(!)` zu erhalten.

####Wiederholtes Scannen

Nachdem der Preprozessor eine Makroausdehnung abgeschlossen hat, durchläuft er den erhaltenen Inhalt erneut und setzt die Ausdehnung fort bis keine weiteren Ausdehnungen möglich sind.

Eine Makroexpansion kann so verstanden werden, dass die Parameter zunächst vollständig entpackt werden (es sei denn, es treten `#` und `##` auf), dann werden das Makro und die vollständig entpackten Parameter gemäß der Definition ersetzt, und schließlich werden alle `#` und `##` Operatoren in der Definition bearbeitet.

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define STRINGIZE(arg0) # arg0

CONCAT(STRING, IZE(Hello))        // -> STRINGIZE(Hello) -> "Hello"
```

`CONCAT(STRING, IZE(Hello))` Bei der ersten Auswertung erhält man `STRINGIZE(Hello)`, und bei der zweiten Auswertung stellt man fest, dass `STRINGIZE` weiterhin expanded werden kann, wodurch schließlich `"Hello"` entsteht.

####Verbot von rekursivem Eindringen

Während des wiederholten Scannens ist es verboten, dieselben Makros rekursiv zu expandieren. Die Makro-Expansion kann als baumartige Struktur verstanden werden, wobei der Wurzelknoten das zu Beginn zu expandierende Makro ist, und der Inhalt jeder Makro-Expansion als Kindknoten mit dem Baum verbunden wird. Daher bedeutet das Verbot der Rekursion beim Expandieren von Kindknoten-Makros, dass die Expansion verboten ist, wenn das Makro mit einem Makro eines beliebigen Vorfahrenknotens übereinstimmt. Lassen Sie uns einige Beispiele betrachten:

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define CONCAT_SPACE(arg0, arg1) arg0 arg1
#define IDENTITY(arg0) IDENTITY_IMPL(arg0)
#define IDENTITY_IMPL(arg0) arg0

CONCAT(CON, CAT(a, b))                  // -> CONCAT(a, b)
IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))   // -> CONCAT(a, b)
IDENTITY(CONCAT(CON, CAT(a, b)))        // -> IDENTITY_IMPL(CONCAT(a, b)) -> CONCAT(a, b)
```

`CONCAT(CON, CAT(a, b))`: Da `CONCAT` zwei Parameter mit `##` verknüpft, wird gemäß der Regel von `##` kein Parameter expandiert, sondern direkt verknüpft. Daher erhalten wir beim ersten Mal die Expansion zu `CONCAT(a, b)`. Da `CONCAT` bereits einmal expandiert wurde, erfolgt keine rekursive Expansion mehr, und der Vorgang wird gestoppt.

`IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))`：`IDENTITY_IMPL` kann als Auswertung des Parameters `arg0` verstanden werden, wobei hier der Parameter `arg0` ausgewertet wurde und `CONCAT(a, b)` ergibt. Aufgrund der Rekursion wurde es mit einem Flag für die Verhinderung von Mehrfachaufrufen versehen, und danach wurde `IDENTITY_IMPL` vollständig ausgeweitet. Bei der zweiten Überprüfung stellte sich heraus, dass `CONCAT(a, b)` mit dem Flag für die Verhinderung von Mehrfachaufrufen versehen ist, also stoppt die Ausweitung. Hier wurde `CONCAT(a, b)` durch die Ausweitung des Parameters `arg0` erhalten, behält jedoch bei der nachfolgenden Ausweitung das Flag für die Verhinderung von Mehrfachaufrufen bei. Es kann verstanden werden, dass der Elternknoten der Parameter `arg0` ist, der kontinuierlich das Flag zur Verhinderung von Mehrfachaufrufen beibehält.

`IDENTITY(CONCAT(CON, CAT(a, b)))`: Dieses Beispiel soll hauptsächlich das Verständnis von Eltern- und Kindknoten verbessern. Wenn die Argumente expandiert werden, wird das eigene Selbst als Elternknoten betrachtet, während der Inhalt der Expansion als Kindknoten betrachtet wird, um die Rekursion zu bestimmen. Nachdem die Argumente expandiert wurden und an die Makrodefinition übergeben wurden, wird das Kennzeichen für die Verhinderung von Reentry weiterhin beibehalten (falls die expandierten Makros nach der Übergabe an die Makrodefinition unverändert bleiben). Der Expansionsprozess der Argumente kann als ein weiterer Baum betrachtet werden, wobei das Ergebnis der Expansion der Argumente die untersten Kindknoten des Baumes darstellt. Diese Kindknoten werden der Makrofunktion übergeben, um die Expansion durchzuführen, wobei die Eigenschaft der Verhinderung von Reentry weiterhin beibehalten wird.

Nach dem vollständigen Entfalten erhalten wir hier `IDENTITY_IMPL(CONCAT(a, b))`, wobei `CONCAT(a, b)` als nicht rekursionsfähig markiert wird. Selbst wenn `IDENTITY_IMPL` die Parameter auswertet, sind die Parameter bereits vom Entfalten ausgeschlossen, sodass sie unverändert in die Definition übertragen werden, und am Ende bekommen wir immer noch `CONCAT(a, b)`.

Ich habe nur einige Regeln aufgelistet, die ich für wichtig halte oder die schwer zu verstehen sind. Es wird empfohlen, sich die detaillierten Regeln direkt im offiziellen Dokument anzusehen.

##Beobachten Sie den Entfaltungsprozess mit Clang.

Wir können dem Clang-Quellcode einige Druckausgaben hinzufügen, um den Prozess der Makroexpansion zu beobachten. Ich habe nicht vor, den Clang-Quellcode im Detail zu erklären. Hier ist eine modifizierte Datei-Differenz, diejenigen, die interessiert sind, können Clang selbst kompilieren und untersuchen. Ich benutze hier die LLVM-Version 11.1.0 ([Link](https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-11.1.0.tar.gz)），editierte Dateien ([Link](assets/img/2021-3-31-cpp-preprocess/clang-modify.zip)). Im Folgenden werden wir anhand eines Beispiels die zuvor vorgestellten Makroerweiterungsregeln überprüfen:

####Beispiel 1

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(C, ONCAT(a, b))      // CONCAT(a, b)
```

Verwenden Sie die modifizierte Version von Clang, um den obigen Code vorzubehandeln: `clang -P -E a.cpp -o a.cpp.i`, um die folgenden Druckinformationen zu erhalten:

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

Translate these text into German language:

第 [1](#__codelineno-9-1)(#__codelineno-9-2)Die Makroerweiterung wurde von Hong nicht deaktiviert, daher kann gemäß der Definition `Macro is ok to expand` ausgeführt werden, bevor in das Makro `EnterMacro` gewechselt wird.

Die Funktion, die tatsächlich das Makro-Expandieren ausführt, ist `ExpandFunctionArguments`. Danach werden die Informationen des Makros, das expandiert werden soll, erneut ausgedruckt. Es ist zu beachten, dass das Makro zu diesem Zeitpunkt bereits als `used` markiert wurde (siehe [9](#__codelineno-9-9)Nachdem der Präprozessor die Quellcodedatei gelesen hat, wird die Datei Zeile für Zeile verarbeitet. Anschließend erfolgt die Entfaltung der einzelnen `Token` gemäß der Makrodefinition (Ein `Token` ist ein Konzept im Präprozessor von `Clang`, hier wird nicht näher darauf eingegangen).

Der 0. 'Token' entspricht dem formalen Parameter 'arg0', der tatsächliche Parameter ist 'C'. Da keine Auswertung erforderlich ist, wird der Wert direkt in das Ergebnis kopiert (Abschnitt [11-13](#__codelineno-9-11)（Keine Übersetzung verfügbar）.

Das erste `Token` ist `hashhash`, was auch der `##` Operator ist, und wird dem Ergebnis hinzugefügt (Nr. [14-15](#__codelineno-9-14)行）。

Das zweite `Token` ist das Formalelement `arg1`, das entsprechende tatsächliche Element ist `ONCAT(a, b)`. Der Präprozessor wird auch die tatsächlichen Elemente in einzelne `Token` transformieren, daher wird das Ergebnis in eckigen Klammern mit jedem `Token` des tatsächlichen Elements dargestellt (Zeile 18). Aufgrund des `##` Operators muss dieses tatsächliche Element nicht erweitert werden, daher wird es direkt in das Ergebnis kopiert (Zeilen [16-18](#__codelineno-9-16)行）。

Zuletzt druckt `Leave ExpandFunctionArguments` die Ergebnisse des aktuellen Scans aus, die erhalten wurden (siehe [19](#__codelineno-9-19)Übersetze den Text ins Deutsche:

行)，把结果的 `Token` 都翻译过来就是 `C ## ONCAT(a, b)`，之后预处理器就执行 `##` 操作符来生成新的内容。

Nach der Ausführung ist `CONCAT(a, b)` erreicht worden. Als die Makro `CONCAT` erreicht wurde, wird die Vorverarbeitung zuerst `HandleIdentifier` betreten, um die Informationen des Makros zu drucken. Es wurde festgestellt, dass der Status dieses Makros `disable used` ist, was bedeutet, dass es bereits ausgebreitet wurde und ein Re-Entry verboten ist. Daher wird `Macro is not ok to expand` angezeigt und der Preprozessor wird nicht weiter expandieren. Letztendlich ist das Ergebnis `CONCAT(a, b)`.

####Beispiel 2

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define IDENTITY(arg0) arg0

IDENTITY(CONCAT(C, ONCAT(a, b)))
```

<details>
<Zusammenfassung> <Schriftart> Clang-Druckinformationen (zum Anzeigen klicken):</Schriftart> </Zusammenfassung>
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

第 [12](#__codelineno-11-12)Beginnen Sie mit der Ausführung von `IDENTITY`, stellen Sie fest, dass das Argument `Token 0` `CONCAT(...)` ist, also ein Makro. Bitte werten Sie dieses Argument zuerst aus.

Nr. [27](#__codelineno-11-27)(#__codelineno-11-46)Translate these text into German language:

行）.

Translate these text into German language:

第 [47](#__codelineno-11-47)Beenden Sie die Ausdehnung auf 'IDENTITY' und erhalten Sie das Ergebnis 'CONCAT(a, b)'.

第 [51](#__codelineno-11-51)Bei der erneuten Prüfung von `CONCAT(a, b)` wurde festgestellt, dass es sich zwar um ein Makro handelt, es jedoch im vorherigen Parameterexpandierungsprozess bereits auf `used` gesetzt wurde und daher nicht weiter rekursiv expandiert wird, sondern direkt als Endergebnis dient.

####Beispiel 3

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define IDENTITY_IMPL(arg0) arg0
#define IDENTITY(arg0) IDENTITY_IMPL(arg0)

IDENTITY(CONCAT(C, ONCAT(a, b)))
```

<details>
<Zusammenfassung> <Schrift>Clang-Druckinformationen (zum Anzeigen anklicken):</Schrift> </Zusammenfassung>
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

* 第 [16](#__codelineno-13-16)Der Prozess beginnt mit der Entfaltung von `IDENTITY`. In ähnlicher Weise erkennt der Vorverarbeiter, dass `Token 2` (also `arg0`) ein Makro ist und entfaltet zunächst `CONCAT(C, ONCAT(a, b))`.

* Nachdem `arg0` entfaltet wurde, erhält man `CONCAT(a, b)` (Zeile [23-54](#__codelineno-13-23)行）

* `IDENTITY` entfaltet sich schließlich zu `IDENTITY_IMPL(CONCAT(a, b))` (siehe [57](#__codelineno-13-57)（　行）

* Erneut scannen, weiter entfalten `IDENTITY_IMPL` (Abschnitt [61-72](#__codelineno-13-61)Beim Durchlaufen der Zeilen stellt sich heraus, dass sich `Token 0` zu diesem Zeitpunkt in der Makroform `CONCAT(a, b)` befindet, jedoch im `used` Zustand ist. Daher wird die Entfaltung abgebrochen und es wird zurückgegeben (Zeilen 75-84). Das endgültige Ergebnis bleibt somit `CONCAT(a, b)` (Zeile [85](#__codelineno-13-85)行）。

Überprüfen Sie die Ergebnisse erneut und stellen Sie fest, dass das Makro `CONCAT(a, b)` den Status "verwendet" hat. Stoppen Sie die Auflösung und erhalten Sie das endgültige Ergebnis.

Durch die obigen drei einfachen Beispiele können wir den Prozess des Entfaltens von Makros durch den Präprozessor grob verstehen. An dieser Stelle werden wir nicht weiter auf den Präprozessor eingehen, aber wer Interesse hat, kann zur Untersuchung meine bereitgestellte modifizierte Datei heranziehen.

##Makroprogrammierung implementieren

Nun beginnen wir mit dem eigentlichen Thema (Der vorangegangene Absatz diente dazu, die Regeln für die Makroexpansion besser zu verstehen) - Die Umsetzung von Makroprogrammierung.

####Grundsymbole

Zunächst können wir die speziellen Symbole für Makros definieren, die beim Auswerten und Verketten verwendet werden.

``` cpp
#define PP_LPAREN() (
#define PP_RPAREN() )
#define PP_COMMA() ,
#define PP_EMPTY()
#definieren PP_HASHHASH # ## #      // Dies zeigt die ## Zeichenfolge an, wird jedoch nur als Zeichenfolge behandelt und nicht als ## Operator.
```

####求值 translates to "Bewertung" in German.

Durch die Verwendung einer Regel, bei der Parameter priorisiert werden, kann ein Makro zur Wertermittlung erstellt werden:

``` cpp
#define PP_IDENTITY(arg0) arg0

PP_COMMA PP_LPAREN() PP_RPAREN()                // -> PP_COMMA ( )
PP_IDENTITY(PP_COMMA PP_LPAREN() PP_RPAREN())   // -> PP_COMMA() -> ,
```

Wenn man nur `PP_COMMA PP_LPAREN() PP_RPAREN()` schreibt, wird der Präprozessor jede Makro einzeln verarbeiten und die Ergebnisse der Entfaltung nicht weiter zusammenfassen. Mit `PP_IDENTITY` kann der Präprozessor das resultierende `PP_COMMA()` erneut werten und erhält `,`.


####Zusammenfügen

Aufgrund dessen, dass bei der Verknüpfung von `##` die Argumente links und rechts nicht expandiert werden, um sicherzustellen, dass die Argumente zuerst ausgewertet und dann verknüpft werden, kann wie folgt geschrieben werden:

``` cpp
#define PP_CONCAT(arg0, arg1) PP_CONCAT_IMPL(arg0, arg1)
#define PP_CONCAT_IMPL(arg0, arg1) arg0 ## arg1

PP_CONCAT(PP_IDENTITY(1), PP_IDENTITY(2))         // -> 12
PP_CONCAT_IMPL(PP_IDENTITY(1), PP_IDENTITY(2))    // -> PP_IDENTITY(1)PP_IDENTITY(2) -> Fehlermeldung
```

Hierbei handelt es sich um eine Methode namens "Delayed Concatenation", die von `PP_CONCAT` verwendet wird. Beim Ausrollen zu `PP_CONCAT_IMPL` werden sowohl `arg0` als auch `arg1` zuerst ausgerollt und ausgewertet, bevor `PP_CONCAT_IMPL` die eigentliche Verknüpfungsoperation ausführt.

####Logische Operationen

Mit `PP_CONCAT` können logische Operationen durchgeführt werden. Zuerst wird ein `BOOL`-Wert definiert:


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

Verwenden Sie `PP_CONCAT`, um zuerst `PP_BOOL_` und `arg0` zusammenzufügen, und werten Sie dann das Ergebnis aus. Hier sollte `arg0` nach der Auswertung eine Zahl im Bereich von `[0, 256]` ergeben. Durch das Zusammenfügen mit `PP_BOOL_` und der anschließenden Auswertung erhält man einen booleschen Wert. Benutzen Sie die Logikoperatoren: Und, Oder, Nicht:

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

Zuerst die Parameter mit `PP_BOOL` auswerten und danach die logischen Ergebnisse anhand der Kombinationen von `0` und `1` zusammenstellen. Wenn `PP_BOOL` nicht zur Auswertung verwendet wird, unterstützen die Parameter nur die beiden Werte `0` und `1`, was die Anwendbarkeit erheblich einschränkt. Ebenso können auch Operationen wie XOR oder NOR verfasst werden; Interessierte können dies selbst ausprobieren.

####Bedingte Auswahl

Durch die Verwendung von `PP_BOOL` und `PP_CONCAT` kann auch eine bedingte Auswahlanweisung geschrieben werden:

``` cpp
#define PP_IF(if, then, else) PP_CONCAT(PP_IF_, PP_BOOL(if))(then, else)
#define PP_IF_1(then, else) then
#define PP_IF_0(then, else) else

PP_IF(1, 2, 3)      // -> PP_IF_1(2, 3) -> 2
PP_IF(0, 2, 3)      // -> PP_IF_0(2, 3) -> 3
```

Wertet `if` aus, wenn es `1` ist, wird es mit `PP_CONCAT` zu `PP_IF_1` verbunden und schließlich als Wert von `then` expandiert; ebenso ergibt sich `PP_IF_0`, wenn `if` den Wert `0` ergibt.

####Zunehmend Abnehmend

Ganzzahliger Inkrement und Dekrement:

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

Ähnlich wie bei `PP_BOOL` ist auch die inkrementelle und dekrementale Änderung von Ganzzahlen durch einen Bereich begrenzt. Hier ist der Bereich auf `[0, 256]` festgelegt. Nach dem Inkrementieren auf `256` gibt `PP_INC_256` sicherheitshalber `256` als Grenze zurück. Ebenso gibt `PP_DEC_0` `0` zurück.

####variatische Parameter

宏可以接受变长参数，格式是：

```cpp
#define LOG(format, ...) printf("log: " format, __VA_ARGS__)

LOG("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG("Hallo Welt")              // -> printf("log: " "Hallo Welt", ); 多了个逗号，编译报错
```

Aufgrund der Möglichkeit, dass variable Parameter leer sein können, was zu einem Kompilierfehler führen könnte, hat C++ 20 `__VA_OPT__` eingeführt. Wenn die variable Parameterliste leer ist, wird nichts zurückgegeben, ansonsten werden die ursprünglichen Parameter zurückgegeben:

```cpp
#define LOG2(format, ...) printf("log: " format __VA_OPT__(,) __VA_ARGS__)

LOG2("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG2("Hallo Welt")              // -> printf("log: " "Hallo Welt" ); ohne Komma, normale Kompilierung
```

Leider ist dieses Makro nur in der C++ 20 oder höheren Standardversion verfügbar. Im Folgenden werden wir die Implementierungsmethode von `__VA_OPT__` vorstellen.

####Trägheitsbewertung

Considering this situation:

``` cpp
PP_IF(1, PP_COMMA(), PP_LPAREN())     // -> PP_IF_1(,,)) -> Fehler: unvollständige Argumentliste beim Aufruf des Makros "PP_IF_1"
```

Wir wissen, dass Makros beim Expandieren zuerst die Argumente auswerten. Nach der Auswertung von `PP_COMMA()` und `PP_LPAREN()` wird es an `PP_IF_1` übergeben, was zu `PP_IF_1(,,))` führt und einen Fehler bei der Vorverarbeitung verursacht. Zu diesem Zeitpunkt kann eine Methode namens lazive Auswertung verwendet werden:

``` cpp
PP_IF(1, PP_COMMA, PP_LPAREN)()       // -> PP_IF_1(PP_COMMA, PP_LPAREN)() -> PP_COMMA() -> ,
```

Ändern Sie die Schreibweise so, dass nur der Name des Makros übergeben wird, und lassen Sie `PP_IF` den benötigten Makronamen auswählen und dann mit Klammern `()` zusammenfügen, um das vollständige Makro zu bilden, das dann schließlich ausgeweitet wird. Lazy Evaluation ist auch in der Makroprogrammierung sehr verbreitet.

####Mit Klammern beginnen

Überprüfen, ob die variablen Argumente mit einer Klammer beginnen:

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

`PP_IS_BEGIN_PARENS` can be used to determine if the incoming parameter begins with parentheses, which will be needed when dealing with parenthesized parameters (such as the `__VA_OPT__` implementation mentioned later). It may seem a bit complex, but the core idea is to construct a macro that, if the variable-length parameter begins with parentheses, can be concatenated with the parentheses to evaluate a certain result, otherwise, another result will be obtained by a separate evaluation. Let's take a closer look:

Das Makro, das aus `PP_IS_BEGIN_PARENS_PROCESS` und `PP_IS_BEGIN_PARENS_PROCESS_0` besteht, evaluiert zuerst die übergebenen variablen Argumente und gibt dann das 0. Argument aus.

`PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__)` bedeutet, dass zunächst der Ausdruck `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` ausgewertet wird, und dann wird das Ergebnis der Auswertung mit `PP_IS_BEGIN_PARENS_PRE_` zusammengesetzt.

`PP_IS_BEGIN_PARENS_EAT(...)` Macro schluckt alle Argumente und gibt 1 zurück. Wenn in der vorherigen Instanz von `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` `__VA_ARGS__` mit einer Klammer beginnt, dann wird der Ausdruck von `PP_IS_BEGIN_PARENS_EAT(...)` übereinstimmen und 1 zurückgeben. Andernfalls, wenn es nicht mit einer Klammer beginnt, wird kein Übereinstimmung gefunden und `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` bleibt unverändert.

Wenn `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` den Wert `1` ergibt, dann ergibt `PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, 1) -> PP_IS_BEGIN_PARENS_PRE_1 -> 1`, wobei zu beachten ist, dass nach dem `1` ein Komma steht. Dieses `1,` wird an `PP_IS_BEGIN_PARENS_PROCESS_0` übergeben, um das erste Argument zu ziehen, und letztendlich erhält man `1`, was bedeutet, dass das Argument mit einer Klammer beginnt.

Wenn `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` den Wert nicht `1` ergibt, sondern unverändert bleibt, dann `PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__) -> PP_IS_BEGIN_PARENS_PRE_PP_IS_BEGIN_PARENS_EAT __VA_ARGS__ -> 0, __VA_ARGS__`, und wenn dies an `PP_IS_BEGIN_PARENS_PROCESS_0` übergeben wird, erhält man `0`, was bedeutet, dass die Parameter nicht mit einer Klammer beginnen.

####Variable Parameter leer

Das Überprüfen, ob die variablen Längenparameter leer sind, ist ebenfalls ein gängiges Makro, das bei der Implementierung von `__VA_OPT__` benötigt wird. Hier nutzen wir `PP_IS_BEGIN_PARENS` und können zunächst eine unvollständige Version schreiben:

``` cpp
#define PP_IS_EMPTY_PROCESS(...) \
    PP_IS_BEGIN_PARENS(PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ())
#define PP_IS_EMPTY_PROCESS_EAT(...) ()

PP_IS_EMPTY_PROCESS()       // -> 1
PP_IS_EMPTY_PROCESS(1)      // -> 0
PP_IS_EMPTY_PROCESS(1, 2)   // -> 0
PP_IS_EMPTY_PROCESS(())     // -> 1
```

Die Funktion `PP_IS_EMPTY_PROCESS` dient dazu festzustellen, ob `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ()` mit einer Klammer beginnt.

Wenn `__VA_ARGS__` leer ist, `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ () -> PP_IS_EMPTY_PROCESS_EAT() -> ()`, erhalten Sie ein Paar Klammern `()`, die dann an `PP_IS_BEGIN_PARENS` übergeben werden, um `1` zurückzugeben, was darauf hinweist, dass das Argument leer ist.

Andernfalls wird `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ()` unverändert an `PP_IS_BEGIN_PARENS` übergeben, was 0 zurückgibt und anzeigt, dass es nicht leer ist.

Beachten Sie das 4. Beispiel `PP_IS_EMPTY_PROCESS(()) -> 1`. `PP_IS_EMPTY_PROCESS` kann variable Argumente, die mit einer Klammer beginnen, nicht korrekt verarbeiten, da die durch die variablen Argumente verursachte Klammer `PP_IS_EMPTY_PROCESS_EAT` entspricht, was dazu führt, dass das Ergebnis `()` ist. Um dieses Problem zu lösen, müssen wir die Argumente, die mit einer Klammer beginnen, unterschiedlich behandeln:

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

Die Funktion `PP_IS_EMPTY_IF` gibt je nach `if`-Bedingung den ersten oder zweiten Parameter zurück.

Wenn die übergebenen variablen Argumente mit einer Klammer beginnen, gibt `PP_IS_EMPTY_IF` `PP_IS_EMPTY_ZERO` zurück und schließlich `0`, was bedeutet, dass die variablen Argumente nicht leer sind.

Im Gegenteil, `PP_IS_EMPTY_IF` gibt `PP_IS_EMPTY_PROCESS` zurück, und schließlich wird von `PP_IS_EMPTY_PROCESS` entschieden, ob die Variable mit variabler Länge leer ist oder nicht.

####Unterstützter Zugriff

Elemente an einer bestimmten Position im variablen Längenparameter abrufen:

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

Der erste Parameter von `PP_ARGS_ELEM` ist der Element-Index `I`, gefolgt von einer variablen Anzahl an Parametern. Mit `PP_CONCAT` kann `PP_ARGS_ELEM_` und `I` zusammengefügt werden, um das Makro `PP_ARGS_ELEM_0..8` zu erhalten, das dann die variablen Parameter entgegennehmen kann, um das entsprechende Element an der angegebenen Indexposition zurückzugeben.

#### PP_IS_EMPTY2

Durch die Verwendung von `PP_ARGS_ELEM` kann auch eine andere Version von `PP_IS_EMPTY` implementiert werden:

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

Die Verwendung von `PP_ARGS_ELEM` ermöglicht die Überprüfung, ob ein Parameter ein Komma enthält, `PP_HAS_COMMA`. `PP_COMMA_ARGS` schluckt alle übergebenen Parameter und gibt ein Komma zurück.

Die Grundlogik zur Feststellung, ob variable Argumente leer sind, besteht darin, dass `PP_COMMA_ARGS __VA_ARGS__ ()` ein Komma zurückgibt, was bedeutet, dass `__VA_ARGS__` leer ist. Die spezifische Syntax lautet `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ())`.

Es wird jedoch Ausnahmen geben:

* `__VA_ARGS__` kann selbst Kommas enthalten;
`__VA_ARGS__()` wird zusammengefügt und evaluiert, was zu einem Komma führt;
* `PP_COMMA_ARGS __VA_ARGS__` wird zusammengefügt und führt zur Auswertung und erzeugt Kommas;

In Bezug auf die drei oben genannten Ausnahmefälle müssen diese ausgeschlossen werden, sodass die endgültige Formulierung äquivalent zur Ausführung einer logischen Verknüpfung der folgenden vier Bedingungen ist:

* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__))` &&
* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__()))` &&
* `PP_NOT(PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__))` &&
* `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ())`

#### `__VA_OPT__`

Mit `PP_IS_EMPTY` lässt sich endlich ein Makro ähnlich `__VA_OPT__` realisieren:

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

`PP_ARGS_OPT` akzeptiert zwei feste Parameter und variable Parameter. Wenn die variablen Parameter nicht leer sind, wird `data` zurückgegeben, andernfalls wird `empty` zurückgegeben. Damit `data` und `empty` Kommas unterstützen, müssen beide den tatsächlichen Parameter in Klammern setzen, und schließlich wird `PP_REMOVE_PARENS` verwendet, um die äußeren Klammern zu entfernen.

Mit `PP_ARGS_OPT` kann `LOG3` die Funktionalität von `LOG2` simulieren:

``` cpp
#define LOG3(format, ...) \
    printf("log: " format PP_ARGS_OPT((,), (), __VA_ARGS__) __VA_ARGS__)

LOG3("Hello");                  // -> printf("log: " "Hello" );
LOG3("Hello %s", "World");      // -> printf("log: " "Hello %s" , "World");
```

`data_tuple` ist `(,)`, und wenn die variablen Längenparameter nicht leer sind, werden alle Elemente in `data_tuple` zurückgegeben, in diesem Fall das Komma `,`.

####Bitte geben Sie die Anzahl der Parameter an.

Die Anzahl der variablen Parameter abrufen:

``` cpp
#define PP_ARGS_SIZE_IMCOMPLETE(...) \
    PP_ARGS_ELEM(8, __VA_ARGS__, 8, 7, 6, 5, 4, 3, 2, 1, 0)

PP_ARGS_SIZE_IMCOMPLETE(a)             // -> 1
PP_ARGS_SIZE_IMCOMPLETE(a, b)          // -> 2
PP_ARGS_SIZE_IMCOMPLETE(PP_COMMA())    // -> 2
PP_ARGS_SIZE_IMCOMPLETE()              // -> 1
```

Die Anzahl der variablen Parameter wird durch die Position der Parameter ermittelt. `__VA_ARGS__` führt dazu, dass alle nachfolgenden Parameter nach rechts verschoben werden. Mit dem Makro `PP_ARGS_ELEM` wird der Parameter an der achten Stelle abgerufen. Wenn `__VA_ARGS__` nur einen Parameter enthält, entspricht der achte Parameter `1`; similarly, wenn `__VA_ARGS__` zwei Parameter hat, wird der achte Parameter zu `2`, was genau der Anzahl der variablen Parameter entspricht.

Hier gegebene Beispiele unterstützen nur eine maximale Anzahl von 8 variablen Parametern, was von der maximalen Länge abhängt, die `PP_ARGS_ELEM` unterstützen kann.

Aber dieser Makro ist noch nicht vollständig. In dem Fall, dass die variable Anzahl von Argumenten leer ist, gibt dieses Makro fälschlicherweise `1` zurück. Wenn leere variable Argumente verarbeitet werden müssen, sollte das zuvor erwähnte `PP_ARGS_OPT`-Makro verwendet werden:

``` cpp
#define PP_COMMA_IF_ARGS(...) PP_ARGS_OPT((,), (), __VA_ARGS__)
#define PP_ARGS_SIZE(...) PP_ARGS_ELEM(8, __VA_ARGS__ PP_COMMA_IF_ARGS(__VA_ARGS__) 8, 7, 6, 5, 4, 3, 2, 1, 0, 0, 0)

PP_ARGS_SIZE(a)             // -> 1
PP_ARGS_SIZE(a, b)          // -> 2
PP_ARGS_SIZE(PP_COMMA())    // -> 2
PP_ARGS_SIZE()              // -> 0
PP_ARGS_SIZE(,,,)           // -> 4
```

Der Schlüssel zum Problem liegt im Komma `,`. Wenn `__VA_ARGS__` leer ist, kann das Weglassen des Kommas den richtigen Rückgabewert `0` liefern.

####Durchlaufzugriff

Ähnlich wie das `for_each` in C++ können wir das Makro `PP_FOR_EACH` implementieren:

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

`PP_FOR_EACH` erhält zwei feste Parameter: `macro`, das als das Makro verstanden werden kann, das während der Iteration aufgerufen wird, und `contex`, das als fester Wert an `macro` übergeben werden kann. `PP_FOR_EACH` ermittelt zunächst die Länge der variablen Parameter `N` mit `PP_ARGS_SIZE`, und verwendet dann `PP_CONCAT`, um `PP_FOR_EACH_N` zu erstellen. Danach wird `PP_FOR_EACH_N` die `PP_FOR_EACH_N-1` iterativ aufrufen, um dieselbe Anzahl von Iterationen wie die Anzahl der variablen Parameter zu erreichen.

Im Beispiel haben wir `DECLARE_EACH` als Parameter `macro` deklariert. Die Funktion von `DECLARE_EACH` besteht darin, `contex arg` zurückzugeben. Wenn `contex` ein Typname ist und `arg` ein Variablenname, kann `DECLARE_EACH` verwendet werden, um eine Variable zu deklarieren.

####Schleifenbedingung

Mit `FOR_EACH` können wir auch eine ähnliche Schreibweise für `PP_WHILE` verwenden:

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

`PP_WHILE` accepts three parameters: `pred` as the condition evaluation function, `op` as the operation function, and `val` as the initial value. During the loop, it continuously checks the condition with `pred(val)` to determine loop termination. The value obtained from `op(val)` is then passed to the subsequent macro, which can be understood as executing the following code:

``` cpp
while (pred(val)) {
    val = op(val);
}
```

`PP_WHILE_N` starts by using `pred(val)` to obtain the condition evaluation result, then passes the condition result `cond` and the remaining parameters to `PP_WHILE_N_IMPL`.
`PP_WHILE_N_IMPL` kann in zwei Teile unterteilt werden: Der hintere Teil `(pred, op, PP_IF(cond, op, PP_EMPTY_EAT)(val))` wird als Parameter des vorderen Teils verwendet. `PP_IF(cond, op, PP_EMPTY_EAT)(val)` wertet `op(val)` aus, wenn `cond` wahr ist, andernfalls wird durch Auswertung von `PP_EMPTY_EAT(val)` ein Leerwert erzeugt. Der vordere Teil `PP_IF(cond, PP_WHILE_N+1, val PP_EMPTY_EAT)` gibt `PP_WHILE_N+1` zurück, wenn `cond` wahr ist, um mit dem kombinierten Parameter des hinteren Teils den Schleifendurchlauf fortzusetzen. Andernfalls wird `val PP_EMPTY_EAT` zurückgegeben, wobei `val` das endgültige Ergebnis ist und `PP_EMPTY_EAT` das Ergebnis des hinteren Teils schluckt.

`SUM` implementiert `N + N-1 + ... + 1`. Ausgangswerte `(max_num, origin_num)`; `SUM_PRED` nimmt das erste Element `x`, um zu überprüfen, ob es größer als 0 ist; `SUM_OP` führt die Dekrementoperation `x = x - 1` auf `x` aus und die `+ x` Operation `y = y + x` auf `y`. Direkt `SUM_PRED` und `SUM_OP` an `PP_WHILE` übergeben, das Ergebnis ist ein Tupel, und das, was wir wirklich wollen, ist das zweite Element des Tupels, also verwenden wir `SUM`, um den Wert des zweiten Elements zu erhalten.

####Rekursive Wiederaufnahme

Bis jetzt haben unser Traversierungszugriff und die bedingten Schleifen gut funktioniert, und die Ergebnisse entsprechen den Erwartungen. Erinnern Sie sich an die Regel zur Makroerweiterung, die wir erwähnt haben und die rekursive Wiederholung verhindert? Leider sind wir auf das Verbot der rekursiven Wiederholung gestoßen, als wir zwei Schleifen ausführen wollten:

``` cpp
#define SUM_OP2(xy_tuple) SUM_OP_OP_IMPL2 xy_tuple
#define SUM_OP_OP_IMPL2(x, y) (PP_DEC(x), y + SUM(x, 0))

#define SUM2(max_num, origin_num) \
    PP_IDENTITY(SUM_IMPL PP_WHILE(SUM_PRED, SUM_OP2, (max_num, origin_num)))

SUM2(1, a)      // -> a + SUM_IMPL PP_WHILE_1(SUM_PRED, SUM_OP, (1, a))
```

`SUM2` ändert den Parameter `op` in `SUM_OP2`, wobei `SUM_OP2` `SUM` aufruft, und `SUM` sich weiter zu `PP_WHILE_1` entfaltet, was bedeutet, dass `PP_WHILE_1` sich rekursiv selbst aufruft, und der Präprozessor die Entfaltung stoppt.

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

`PP_AUTO_WHILE` ist die automatisch abgeleitete rekursive Version von `PP_WHILE`. Der zentrale Makro ist `PP_AUTO_REC(PP_WHILE_PRED)`, dieser Makro kann die aktuell verfügbare Zahl `N` der Version `PP_WHILE_N` ermitteln.

The principle of inference is quite simple: search through all versions, identify the version that can be correctly expanded, and return the number of that version. To enhance the search speed, the common practice is to employ binary search, which is exactly what `PP_AUTO_REC` does. `PP_AUTO_REC` takes a parameter `check`, responsible for verifying version availability within the specified range [1, 4]. Initially, `PP_AUTO_REC` will check `check(2)`; if it returns true, it will call `PP_AUTO_REC_12` to search within the range [1, 2]; otherwise, it will utilize `PP_AUTO_REC_34` to search within [3, 4]. Subsequently, `PP_AUTO_REC_12` will evaluate `check(1)`: if it's true, version `1` is deemed available; if not, version `2` will be selected. Similar logic applies to `PP_AUTO_REC_34`.

Wie schreibt man das `check` Makro, um zu überprüfen, ob die Version verfügbar ist? Hier wird `PP_WHILE_PRED` in zwei Teile aufgeteilt, wir betrachten den hinteren Teil `PP_WHILE_ ## n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)` : Wenn `PP_WHILE_ ## n` verfügbar ist, wird dieser Teil, da `PP_WHILE_FALSE` immer `0` zurückgibt, den Wert des `val` Parameters ergeben, also `PP_WHILE_FALSE`; andernfalls bleibt dieser Teil des Makros unverändert, weiterhin `PP_WHILE_n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`.

Verbinde das Ergebnis des hinteren Teils mit dem vorherigen Teil `PP_WHILE_CHECK_` und erhalte zwei Ergebnisse: `PP_WHILE_CHECK_PP_WHILE_FALSE` oder `PP_WHILE_CHECK_PP_WHILE_n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`. Dadurch wird `PP_WHILE_CHECK_PP_WHILE_FALSE` auf `1` gesetzt, um die Verfügbarkeit anzuzeigen, während `PP_WHILE_CHECK_PP_WHILE_n` auf `0` gesetzt wird, um die Nichtverfügbarkeit anzuzeigen. Auf diese Weise haben wir die automatische Ableitung der Rekursion abgeschlossen.

####Arithmetic comparison

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

Bestimmen, ob Werte gleich sind, nutzt die Eigenschaft der Verhinderung der rekursiven Wiederverwendung, indem `x` und `y` rekursiv zu den Makros `PP_NOT_EQUAL_x` und `PP_NOT_EQUAL_y` zusammengefügt werden. Wenn `x == y`, wird das Makro `PP_NOT_EQUAL_y` nicht entwickelt, wodurch sich `PP_NOT_EQUAL_CHECK_` zu `PP_NOT_EQUAL_CHECK_PP_NOT_EQUAL_y` verbindet und `0` zurückgibt; im anderen Fall werden beide erfolgreich entwickelt, was letztendlich zu `PP_EQUAL_NIL` führt und die Verbindung zu `PP_NOT_EQUAL_CHECK_PP_EQUAL_NIL` ergibt, das `1` zurückgibt.

gleichwertig:

``` cpp
#define PP_EQUAL(x, y) PP_NOT(PP_NOT_EQUAL(x, y))

PP_EQUAL(1, 1)              // -> 1
PP_EQUAL(1, 3)              // -> 0

```

kleiner gleich:

``` cpp
#define PP_LESS_EQUAL(x, y) PP_NOT(PP_SUB(x, y))

PP_LESS_EQUAL(2, 1)         // -> 0
PP_LESS_EQUAL(1, 1)         // -> 1
PP_LESS_EQUAL(1, 2)         // -> 1
```

Kleiner als:

``` cpp
#define PP_LESS(x, y) PP_AND(PP_LESS_EQUAL(x, y), PP_NOT_EQUAL(x, y))

PP_LESS(2, 1)               // -> 0
PP_LESS(1, 2)               // -> 1
PP_LESS(2, 2)               // -> 0
```

Außerdem gibt es auch größere, größer oder gleich usw. arithmetische Vergleiche, die hier nicht weiter erläutert werden.

####Arithmetic operations

Durch die Nutzung von `PP_AUTO_WHILE` können wir grundlegende arithmetische Operationen durchführen, und es werden auch geschachtelte Berechnungen unterstützt.

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

Die Implementierung der Multiplikation hat hier einen Parameter `ret` hinzugefügt, dessen Anfangswert `0` ist. Bei jeder Iteration wird `ret = ret + x` ausgeführt.

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

Die Division nutzt `PP_LESS_EQUAL`, und der Schleifenprozess wird nur fortgesetzt, wenn `y <= x` gilt.

####Datenstruktur

Makros können ebenfalls Datenstrukturen haben. Tatsächlich haben wir in den vorherigen Abschnitten bereits eine Datenstruktur, `tuple`, verwendet. `PP_REMOVE_PARENS` entfernt die äußeren Klammern von `tuple` und gibt die darin enthaltenen Elemente zurück. Hier verwenden wir `tuple` als Beispiel, um über die entsprechenden Implementierungen zu diskutieren. Für andere Datenstrukturen wie `list`, `array` usw. kann man sich die Implementierungen von `Boost` anschauen, wenn man interessiert ist.

`Tuple` is defined as a collection of elements separated by commas enclosed in parentheses: `(a, b, c)`.

``` cpp
#define PP_TUPLE_REMOVE_PARENS(tuple) PP_REMOVE_PARENS(tuple)

Hol dir das Element an einer bestimmten Indexposition.
#define PP_TUPLE_ELEM(i, tuple) PP_ARGS_ELEM(i, PP_TUPLE_REMOVE_PARENS(tuple))

// Den gesamten Tuple aufnehmen und leer zurückgeben
#define PP_TUPLE_EAT() PP_EMPTY_EAT

Erhalten Sie die Größe.
#define PP_TUPLE_SIZE(tuple) PP_ARGS_SIZE(PP_TUPLE_REMOVE_PARENS(tuple))

// Elemente hinzufügen
#define PP_TUPLE_PUSH_BACK(elem, tuple) \
    PP_TUPLE_PUSH_BACK_IMPL(PP_TUPLE_SIZE(tuple), elem, tuple)
#define PP_TUPLE_PUSH_BACK_IMPL(size, elem, tuple) \
    (PP_TUPLE_REMOVE_PARENS(tuple) PP_IF(size, PP_COMMA, PP_EMPTY)() elem)

// Elemente einfügen
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

// Entferne das letzte Element
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

// Element entfernen
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

Hier ist eine kurze Erklärung zur Implementierung des Einfügens von Elementen; andere Operationen wie das Löschen von Elementen werden nach einem ähnlichen Prinzip durchgeführt. `PP_TUPLE_INSERT(i, elem, tuple)` kann das Element `elem` an der Position `i` im `tuple` einfügen. Um diese Operation abzuschließen, werden zunächst alle Elemente mit einer Position kleiner als `i` mit `PP_TUPLE_PUSH_BACK` in ein neues `tuple` (genannt `ret`) eingefügt. Dann wird das Element `elem` an der Position `i` platziert, gefolgt von den Elementen aus dem ursprünglichen `tuple`, die an einer Position größer oder gleich `i` sind, die hinter `ret` eingefügt werden. Schließlich erhalten wir mit `ret` das gewünschte Ergebnis.

##Zusammenfassung

Der Zweck dieses Artikels besteht darin, die Prinzipien und grundlegenden Implementierungen der Makroprogrammierung in C/C++ klar darzulegen. Während ich einige meiner eigenen Einsichten und Verständnis festhalte, hoffe ich, anderen damit auch einige Erklärungen und Anregungen bieten zu können. Es ist zu beachten, dass der Artikel zwar etwas länger ist, jedoch nicht alle Techniken und Anwendungen der Makroprogrammierung behandelt werden, wie zum Beispiel die von CHAOS_PP vorgeschlagene [basierte Methode für rekursive Aufrufe durch verzögertes Entfalten](https://github.com/pfultz2/Cloak/wiki/C-Preprocessor-tricks,-tips,-and-idioms#deferred-expression)„BOOST_PP“ enthält unter anderem Makros, die mit `REPEAT` zusammenhängen. Interessierte können selbstständig weitere Informationen dazu nachschlagen.

Das Debuggen von Makroprogrammierung ist ein schmerzhafter Prozess, bei dem wir können:

* Verwenden Sie die Optionen `-P -E`, um das Präprozessierergebnis auszugeben;
Verwenden Sie die von mir angepasste `clang`-Version, die oben diskutiert wurde, um den Entfaltungsprozess sorgfältig zu untersuchen.
* Zerlege komplexe Makros und sieh dir die Zwischenergebnisse der Makroerweiterung an;
* Irrelevante Header-Dateien und Makros ausblenden;
Zum Schluss muss man sich den Prozess der Makroexpansion vorstellen; nachdem man mit der Makroexpansion vertraut ist, wird auch die Effizienz beim Debuggen steigen.

Die Makros in diesem Text wurden von mir selbst entwickelt, nachdem ich das Konzept verstanden hatte. Einige Makros wurden durch die Implementierung von 'Boost' sowie durch Artikel in Verwendungsbeispielen inspiriert. Wenn irgendwelche Fehler vorhanden sind, zögern Sie nicht, mich darauf hinzuweisen. Gerne stehe ich auch für Diskussionen zu relevanten Themen zur Verfügung.

Der gesamte Code dieses Textes befindet sich hier: [Download](assets/img/2021-3-31-cpp-preprocess/macros.cpp)，[Online-Demo](https://godbolt.org/z/coWvc5Pse)I'm sorry, but the text provided contains no content to be translated.

##Zitat

* [Boost.Preprocessor](https://www.boost.org/doc/libs/1_75_0/libs/preprocessor/doc/)
* [Die Kunst der Makroprogrammierung in C/C++](https://bot-man-jl.github.io/articles/?post=2020/Macro-Programming-Art)

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt, bitte [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Bitte zeigen Sie alle übersehenen Punkte auf. 
