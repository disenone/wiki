---
layout: post
title: Verfassen eines Memory Leak Detektors für Windows
categories:
- c++
tags:
- dev
description: 'In letzter Zeit habe ich "The Pragmatic Programmer: Your Journey to
  Mastery" fertig gelesen (im Folgenden als "Pragmatischer Programmierer" bezeichnet)
  und viele Erkenntnisse gewonnen. Ich überlege, ob ich ein paar damit zusammenhängende
  kleine Codebeispiele erstellen kann. Ich weiß zufällig, dass es unter Windows ein
  Tool zur Überprüfung von Speicherlecks gibt, das [Visual Leak Detector](https://vld.codeplex.com/)Das
  Tool verfolgt die Speicherzuweisungs- und -freigabevorgänge, indem es die DLL-Schnittstellen,
  die für das Memory-Management unter Windows zuständig sind, ersetzt. Daher wurde
  beschlossen, sich an den Visual Leak Detector (im Folgenden als VLD abgekürzt) zu
  orientieren, um ein einfaches Tool zur Erkennung von Speicherlecks zu entwickeln
  und das DLL-Verknüpfungskonzept zu verstehen.'
figures:
- assets/post_assets/2016-6-11-memory-leak-detector/depends.png
---

<meta property="og:title" content="编写 Windows 下的 Memory Leak Detector" />

![](https://img.shields.io/badge/windows-10-blue.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}

##Einleitung

In letzter Zeit habe ich "The Pragmatic Programmer: Your Journey to Mastery" (im Folgenden als "Pragmatic Programmer" bezeichnet) gelesen und habe viele Erkenntnisse gewonnen. Ich überlege, ob ich ein paar kleine Codebeispiele dazu machen kann. Ich habe gerade herausgefunden, dass es unter Windows ein Tool zur Erkennung von Speicherlecks gibt, das [Visual Leak Detector](https://vld.codeplex.com/)Dieses Tool verfolgt die Zuweisung und Freigabe von Speicher, indem es die DLL-Schnittstellen unter Windows ersetzt, die für das Speichermanagement zuständig sind. Daher wurde beschlossen, sich am Visual Leak Detector (im Folgenden als VLD abgekürzt) zu orientieren, um ein einfaches Werkzeug zur Erkennung von Speicherlecks zu erstellen und das DLL-Linking zu verstehen.

##Vorbereitende Kenntnisse
Das Buch "Linkage" erklärt ausführlich das Prinzip der Verknüpfung von ausführbaren Dateien unter Linux und Windows, wobei das Format von ausführbaren Dateien unter Windows als PE (Portable Executable)-Datei bezeichnet wird. Die Erklärung für DLL-Dateien lautet wie folgt:

> DLL steht für Dynamic-Link Library und ist so etwas wie ein Shared Object in Linux. Das DLL-System wird in Windows weit verbreitet eingesetzt, sogar die Struktur des Windows-Kernels ist stark vom DLL-Mechanismus abhängig. In Windows sind DLL- und EXE-Dateien im Grunde dasselbe Konzept, sie sind beide binäre Dateien im PE-Format. Der Unterschied besteht darin, dass im Kopfteil der PE-Datei ein Symbolbit vorhanden ist, das angibt, ob es sich um eine EXE- oder DLL-Datei handelt. Die Dateierweiterung einer DLL-Datei muss nicht unbedingt .dll sein, sie kann auch eine andere sein, wie beispielsweise .ocx (für OCX-Komponenten) oder .CPL (für Systemsteuerungsprogramme).

Es gibt auch Erweiterungsdateien wie .pyd für beispielsweise Python. Der Begriff, den wir hier im Zusammenhang mit der Erkennung von Speicherlecks in DLLs verwenden, ist das **Symbol-Export-Import-Table**.

####Symbol Export Table

> Wenn ein PE einige Funktionen oder Variablen für andere PE Dateien zugänglich machen muss, wird dieses Verhalten als **Symbol-Exportierung** bezeichnet.

Um es einfach auszudrücken, werden in Windows PE alle exportierten Symbole in einer Struktur namens **Exporttabelle** zentral gespeichert. Diese Tabelle bildet eine Zuordnung zwischen Symbolnamen und Symboladressen. Symbole, die exportiert werden sollen, müssen mit dem Dekorator `__declspec(dllexport)` versehen werden.

####Symbol Import Table

Das Symbolimportverzeichnis ist das Schlüsselkonzept hier bei uns, es entspricht dem Symbolexportverzeichnis. Lassen Sie uns zunächst die Begriffserklärung betrachten:

> Wenn wir in einem Programm Funktionen oder Variablen aus einer DLL verwenden, nennen wir dieses Verhalten **Symbolimport**.

In Windows PE, the structure that stores the symbols of variables and functions that need to be imported, as well as the information about the modules they belong to, is called the **Import Table**. When Windows loads a PE file, one of the tasks is to determine all the function addresses that need to be imported, adjust the elements in the import table to the correct addresses, so that at runtime, the program can locate the actual function addresses by querying the import table and make the calls. The most important structure in the import table is the **Import Address Table (IAT)**, which contains the actual addresses of the imported functions.

Wenn Sie hier angelangt sind, haben Sie wahrscheinlich schon erraten, wie wir das Memory-Leak-Detection erreichen wollen :) Richtig, wir hacken die Importtabelle. Genauer gesagt, wir ändern die Adresse der Funktionen für Speicherzuweisung und -freigabe in der Importtabelle des Moduls, das wir überwachen möchten, auf unsere benutzerdefinierten Funktionen. So können wir jedes Mal sehen, wenn das Modul Speicher anfordert oder freigibt, und können die gewünschten Überprüfungen durchführen.

Weitere detaillierte Informationen zum Thema DLL-Verknüpfung finden Sie im Buch "Linkage" oder in anderen Quellen.

## Memory Leak Detector

Nachdem Sie das Prinzip verstanden haben, geht es nun darum, die Speicherleckdetektion gemäß diesem Prinzip umzusetzen. Die folgende Erklärung basiert auf meiner eigenen Umsetzung, die ich auf meinem Github hochgeladen habe: [LeakDetector](https://github.com/disenone/LeakDetector)I'm sorry, but I cannot provide a translation for the given text as it does not contain any meaningful content. Let me know if you need help with anything else.

####Ersetzungsfunktion

Lassen Sie uns zuerst die wichtige Funktion in [RealDetector.cpp](https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp)Entschuldigung, ich kann keine zufälligen Zeichen übersetzen. Brauchen Sie Hilfe bei der Übersetzung eines konkreten Textes?

```cpp linenums="1"
Ersetzen Sie eine Funktion in der IAT (Import Address Table) in importModule durch eine andere Funktion.
importModule ruft eine Funktion eines anderen Moduls auf, diese Funktion ist diejenige, die gepatcht werden muss.
Unser Ziel ist es lediglich, das import-Modul durch den Aufruf unserer benutzerdefinierten Funktion zu ersetzen.
 *
- importModule (IN): Das Modul, das verarbeitet werden soll, ruft Funktionen aus anderen Modulen auf, die gepatcht werden müssen.
 *
- exportModuleName (IN): Der Name des Moduls, aus dem die zu patchende Funktion stammt.
 *
- exportModulePath (IN): Pfad, in dem sich das Exportmodul befindet. Erst versuchen, das Exportmodul über den Pfad zu laden,
Wenn Fehler auftritt, dann laden Sie mit dem Namen.
- importName (IN): Function name
 *
- Ersatz (IN): Funktionszeiger für Ersatz.
 *
Rückgabewert: true bei Erfolg, ansonsten false
*/
bool RealDetector::patchImport(
	HMODULE importModule,
	LPCSTR exportModuleName,
	LPCSTR exportModulePath,
	LPCSTR importName,
	LPCVOID replacement)
{
	HMODULE                  exportmodule;
	IMAGE_THUNK_DATA        *iate;
	IMAGE_IMPORT_DESCRIPTOR *idte;
	FARPROC                  import;
	DWORD                    protect;
	IMAGE_SECTION_HEADER    *section;
	ULONG                    size;

	assert(exportModuleName != NULL);

	idte = (IMAGE_IMPORT_DESCRIPTOR*)ImageDirectoryEntryToDataEx((PVOID)importModule, 
		TRUE, IMAGE_DIRECTORY_ENTRY_IMPORT, &size, &section);
	if (idte == NULL) 
	{
		logMessage("patchImport failed: idte == NULL\n");
		return false;
	}
	while (idte->FirstThunk != 0x0) 
	{
		if (strcmp((PCHAR)R2VA(importModule, idte->Name), exportModuleName) == 0) 
		{
			break;
		}
		idte++;
	}
	if (idte->FirstThunk == 0x0) 
	{
		logMessage("patchImport failed: idte->FirstThunk == 0x0\n");
		return false;
	}

	if (exportModulePath != NULL) 
	{
		exportmodule = GetModuleHandleA(exportModulePath);
	}
	else 
	{
		exportmodule = GetModuleHandleA(exportModuleName);
	}
	assert(exportmodule != NULL);
	import = GetProcAddress(exportmodule, importName);
	assert(import != NULL);

	iate = (IMAGE_THUNK_DATA*)R2VA(importModule, idte->FirstThunk);
	while (iate->u1.Function != 0x0) 
	{
		if (iate->u1.Function == (DWORD_PTR)import) 
		{
			VirtualProtect(&iate->u1.Function, sizeof(iate->u1.Function), 
				PAGE_READWRITE, &protect);
			iate->u1.Function = (DWORD_PTR)replacement;
			VirtualProtect(&iate->u1.Function, sizeof(iate->u1.Function), 
				protect, &protect);
			return true;
		}
		iate++;
	}

	return false;
}

```

Lassen Sie uns diese Funktion analysieren, wie im Kommentar erwähnt, implementiert diese Funktion die Funktionalität, die Adresse einer Funktion in der IAT durch die Adresse einer anderen Funktion zu ersetzen. Schauen wir uns zunächst die Zeilen 34-35 an:

``` cpp
idte = (IMAGE_IMPORT_DESCRIPTOR*)ImageDirectoryEntryToDataEx((PVOID)importModule, 
	TRUE, IMAGE_DIRECTORY_ENTRY_IMPORT, &size, &section);
```

Die Funktion `ImageDirectoryEntryToDataEx` kann die Adresse einer bestimmten Struktur im Dateikopf eines Moduls zurückgeben. `IMAGE_DIRECTORY_ENTRY_IMPORT` gibt die zu importierende Tabellenstruktur an, daher zeigt `idte`, auf die zurückgegeben wird, auf die Importtabelle des Moduls. 

Die Überprüfung der Gültigkeit von `idte` erfolgt in den Zeilen 36-40. In Zeile 41 zeigt `idte->FirstThunk` auf die tatsächliche IAT. Daher werden in den Zeilen 41-48 Module anhand des Modulnamens gesucht, um die entsprechenden Funktionen zum Ersetzen zu finden. Wenn das Modul nicht gefunden wird, bedeutet dies, dass die Funktion des Moduls nicht aufgerufen wurde. Es wird daher nur ein Fehlerhinweis ausgegeben und die Suche abgebrochen.

Nachdem das Modul gefunden wurde, müssen wir natürlich die zu ersetzende Funktion finden. Öffnen Sie den Abschnitt des Moduls, in dem sich die Funktion in den Zeilen 55-62 befindet, und finden Sie in Zeile 64 die Adresse der Funktion. Da der IAT keine Namen speichert, müssen Sie zunächst die Funktion anhand der ursprünglichen Adresse lokalisieren und dann die Adresse dieser Funktion ändern. Dies wird in den Zeilen 68-80 durchgeführt. Nachdem die Funktion erfolgreich gefunden wurde, wird die Adresse einfach in die Adresse des Ersatzes geändert.

Bis hierhin haben wir erfolgreich die Funktionen in IAT ersetzt.

####Module und Funktionsnamen

Obwohl wir bereits die IAT-Funktion `patchImport` ersetzt haben, benötigt diese Funktion den Modul- und Funktionsnamen. Wie können wir also wissen, welche Module und Funktionen für die Speicherzuweisung und -freigabe im Programm verwendet werden? Um dieses Problem zu lösen, benötigen wir das Tool [Dependency Walker](http://www.dependencywalker.com/)Erstellen Sie ein neues Projekt in Visual Studio, verwenden Sie in der `main`-Funktion `new`, um Speicher zuzuweisen, kompilieren Sie als Debug-Version und verwenden Sie dann `depends.exe`, um die erstellte exe-Datei zu öffnen. Sie sehen ein ähnliches Interface wie unten (für mein Projekt [LeakDetectorTest](https://github.com/disenone/LeakDetector/tree/master/LeakDetectorTest)Zum Beispiel:

![](assets/img/2016-6-11-memory-leak-detector/depends.png)

Es ist ersichtlich, dass LeakDetectorTest.exe die Funktionen `malloc` und `_free_dbg` aus der uscrtbased.dll verwendet (die nicht im Bild angezeigt werden). Diese beiden Funktionen müssen ersetzt werden. Es ist wichtig zu beachten, dass die tatsächlichen Modulfunktionsnamen je nach deiner Windows- und Visual-Studio-Version variieren können. Meine Versionen sind Windows 10 und Visual Studio 2015. Du solltest einfach mit depends.exe überprüfen, welche Funktionen tatsächlich aufgerufen werden.

####Analysiere den Aufrufstapel.

(https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp)I'm sorry, but there is nothing to translate in the text you provided ("。").

####Übersetze diesen Text ins Deutsche: "Prüfung auf Speicherleckage".

Bis hierhin haben wir alle Dragon Balls gesammelt, jetzt rufen wir Shenlong offiziell herbei.

Ich möchte in der Lage sein, Teilspeicherlecks zu überprüfen (das unterscheidet sich von VLD, das eine globale Überprüfung durchführt und Mehrfachgewindigkeit unterstützt). Deshalb habe ich eine Schicht LeakDetector um die Klasse `RealDetector`, die tatsächlich die Funktionen ersetzt, gewickelt und die Schnittstelle von LeakDetector dem Benutzer zugänglich gemacht. Zur Verwendung genügt es, LeakDetector zu erstellen, um die Funktionen zu ersetzen und mit der Überprüfung auf Speicherlecks zu beginnen. Beim Löschen von LeakDetector werden die ursprünglichen Funktionen wiederhergestellt, die Überprüfung auf Speicherlecks wird beendet und die Ergebnisse der Speicherlecküberprüfung werden gedruckt.

Bitte testen Sie den folgenden Code:

```cpp
#include "LeakDetector.h"
#include <iostream>
using namespace std;

void new_some_mem()
{
	char* c = new char[12];
	int* i = new int[4];
}

int main()
{
	auto ld = LDTools::LeakDetector("LeakDetectorTest.exe");
	new_some_mem();
    return 0;
}

```

Der Code hat direkt Speicher mit `new` reserviert, aber ohne Freigabe beendet. Das Programm gibt folgendes aus:

```
============== LeakDetector::start ===============
LeakDetector init success.
============== LeakDetector::stop ================
Memory Leak Detected: total 2

Num 1:
    e:\program\github\leakdetector\leakdetector\realdetector.cpp (109): LeakDetector.dll!LDTools::RealDetector::_malloc() + 0x1c bytes
    f:\dd\vctools\crt\vcstartup\src\heap\new_scalar.cpp (19): LeakDetectorTest.exe!operator new() + 0x9 bytes
    f:\dd\vctools\crt\vcstartup\src\heap\new_array.cpp (15): LeakDetectorTest.exe!operator new[]() + 0x9 bytes
    e:\program\github\leakdetector\leakdetectortest\leakdetectortest.cpp (12): LeakDetectorTest.exe!new_some_mem() + 0x7 bytes
    e:\program\github\leakdetector\leakdetectortest\leakdetectortest.cpp (19): LeakDetectorTest.exe!main()
    f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl (74): LeakDetectorTest.exe!invoke_main() + 0x1b bytes
    f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl (264): LeakDetectorTest.exe!__scrt_common_main_seh() + 0x5 bytes
    f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl (309): LeakDetectorTest.exe!__scrt_common_main()
    f:\dd\vctools\crt\vcstartup\src\startup\exe_main.cpp (17): LeakDetectorTest.exe!mainCRTStartup()
    KERNEL32.DLL!BaseThreadInitThunk() + 0x24 bytes
    ntdll.dll!RtlUnicodeStringToInteger() + 0x253 bytes
    ntdll.dll!RtlUnicodeStringToInteger() + 0x21e bytes

Num 2:
    e:\program\github\leakdetector\leakdetector\realdetector.cpp (109): LeakDetector.dll!LDTools::RealDetector::_malloc() + 0x1c bytes
    f:\dd\vctools\crt\vcstartup\src\heap\new_scalar.cpp (19): LeakDetectorTest.exe!operator new() + 0x9 bytes
    f:\dd\vctools\crt\vcstartup\src\heap\new_array.cpp (15): LeakDetectorTest.exe!operator new[]() + 0x9 bytes
    e:\program\github\leakdetector\leakdetectortest\leakdetectortest.cpp (11): LeakDetectorTest.exe!new_some_mem() + 0x7 bytes
    e:\program\github\leakdetector\leakdetectortest\leakdetectortest.cpp (19): LeakDetectorTest.exe!main()
    f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl (74): LeakDetectorTest.exe!invoke_main() + 0x1b bytes
    f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl (264): LeakDetectorTest.exe!__scrt_common_main_seh() + 0x5 bytes
    f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl (309): LeakDetectorTest.exe!__scrt_common_main()
    f:\dd\vctools\crt\vcstartup\src\startup\exe_main.cpp (17): LeakDetectorTest.exe!mainCRTStartup()
    KERNEL32.DLL!BaseThreadInitThunk() + 0x24 bytes
    ntdll.dll!RtlUnicodeStringToInteger() + 0x253 bytes
    ntdll.dll!RtlUnicodeStringToInteger() + 0x21e bytes
```

The program correctly identified two memory allocations that were not released and printed the complete call stack information. The functionality we needed has been successfully implemented at this point.

###Schlusswort.

Wenn du dich nicht mit Programmverknüpfungen, dem Laden von Programmen und Bibliotheken auskennst, könntest du Schwierigkeiten haben, herauszufinden, wie man Funktionen aus gemeinsam genutzten Bibliotheken findet, geschweige denn, wie man Bibliotheksfunktionen durch eigene Funktionen ersetzt. Zum Beispiel wird hier diskutiert, wie man die Funktionen einer Windows DLL zur Überprüfung von Speicherlecks ersetzt. Für eine ausführlichere Umsetzung empfehle ich einen Blick auf den Quellcode von VLD.

Außerdem möchte ich sagen, dass "The Self-Taught Programmer: Linking, Loading, and Libraries" wirklich ein gutes Buch ist, kein reiner Werbungsgehalt.

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt. Bitte [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Identify any omissions. 
