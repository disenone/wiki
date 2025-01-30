---
layout: post
title: Schreiben Sie einen Memory Leak Detector für Windows.
categories:
- c++
tags:
- dev
description: 'In letzter Zeit habe ich das Buch „Die Selbstverbesserung von Programmierern:
  Linken, Laden und Bibliotheken“ (kurz „Linken“) gelesen und dabei viel gelernt.
  Ich überlege, ob ich einige dazugehörige kleine Codes erstellen kann. Zufällig habe
  ich erfahren, dass es unter Windows ein Werkzeug zur Erkennung von Speicherlecks
  gibt: [Visual Leak Detector](https://vld.codeplex.com/)Dieses Tool realisiert das
  Verfolgen der Speicherzuweisungen und -freigaben durch den Austausch der DLL-Schnittstellen,
  die in Windows für das Speichermanagement verantwortlich sind. Daher wurde beschlossen,
  sich an dem Visual Leak Detector (im Folgenden VLD genannt) zu orientieren, um ein
  einfaches Tool zur Erkennung von Speicherlecks zu entwickeln und das Verständnis
  der DLL-Verknüpfung zu fördern.'
figures:
- assets/post_assets/2016-6-11-memory-leak-detector/depends.png
---

<meta property="og:title" content="编写 Windows 下的 Memory Leak Detector" />

![](https://img.shields.io/badge/windows-10-blue.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}

##Vorwort

(https://vld.codeplex.com/)Dieses Tool wird durch den Austausch der DLL-Schnittstellen, die unter Windows für das Speicher-Management verantwortlich sind, implementiert, um die Speicherzuweisungen und -freigaben zu verfolgen. Daher entschieden wir uns, uns an Visual Leak Detector (im Folgenden VLD genannt) zu orientieren, um ein einfaches Werkzeug zur Erkennung von Speicherlecks zu erstellen und das Verständnis der DLL-Verlinkung zu fördern.

##Vorwissen
Das Buch "Linking" erklärt ausführlich die Prinzipien der Verknüpfung von ausführbaren Dateien unter Linux und Windows, wobei das Dateiformat für ausführbare Dateien unter Windows als PE (Portable Executable) bezeichnet wird. Die Erklärung für DLL-Dateien lautet wie folgt:

> DLL steht für Dynamic-Link Library, was so viel wie dynamische Linkbibliothek bedeutet, und entspricht dem gemeinsamen Objekt unter Linux. In Windows-Systemen wird dieses DLL-Mechanismus in großem Umfang verwendet, sogar die Struktur des Windows-Kernels ist stark auf das DLL-Mechanismus angewiesen. DLL-Dateien und EXE-Dateien unter Windows sind im Grunde dasselbe Konzept, da sie beide binäre Dateien im PE-Format sind. Der einzige Unterschied besteht darin, dass im PE-Dateikopf ein Symbol vorhanden ist, das angibt, ob es sich um eine EXE- oder eine DLL-Datei handelt. Zudem ist die Dateierweiterung einer DLL-Datei nicht unbedingt .dll; sie kann auch andere Formate wie .ocx (OCX-Steuerelement) oder .CPL (Systemsteuerungsprogramm) haben.

Es gibt zum Beispiel Erweiterungsdateien für Python wie .pyd. In DLL haben wir hier das Konzept der **Symbol-Export- und -Importtabelle** im Zusammenhang mit der Speicherlecküberwachung.

####Symbol Export Table

> Wenn ein PE einige Funktionen oder Variablen für andere PE-Dateien freigeben muss, bezeichnen wir dieses Verhalten als **Symbol Exporting**.

Einfach gesagt werden in Windows PE alle exportierten Symbole in einer Struktur gespeichert, die als **Exporttabelle (Export Table)** bezeichnet wird. Diese bietet eine Zuordnung zwischen Symbolnamen und Symboladressen. Symbole, die exportiert werden sollen, müssen mit dem Modifizierer `__declspec(dllexport)` versehen werden.

####Symbolimporttabelle

Die Symbol-Import-Tabelle ist das Schlüsselkonzept hier, das im Gegensatz zur Symbol-Export-Tabelle steht. Lassen Sie uns zuerst die Konzepterklärung betrachten:

> Wenn wir in einem Programm Funktionen oder Variablen aus einer DLL verwenden, nennen wir dieses Verhalten **Symbolimport**.

In Windows PE, the structure that stores the symbols of variables and functions that modules need to import, along with information about their location, is called the **Import Table**. When Windows loads a PE file, one of the tasks is to determine all the function addresses that need to be imported, and adjust the elements in the import table to the correct addresses. This allows the program, at runtime, to locate the actual address of functions by querying the import table and making the necessary calls. The most crucial structure in the import table is the **Import Address Table (IAT)**, which stores the actual addresses of the imported functions.

Wenn du bis hierher gelesen hast, hast du vielleicht schon eine Ahnung davon, wie wir den Memory-Leak-Detektor implementieren werden :) Richtig, wir hacken die Importtabelle, genauer gesagt, wir ändern die Adressen der Funktionen für Speicherzuweisung und -freigabe in der Importtabelle des Moduls, das wir überwachen möchten, so dass sie auf von uns definierte Funktionen verweisen. Auf diese Weise können wir jedes Mal, wenn das Modul Speicher anfordert oder freigibt, überprüfen, was vor sich geht, und die gewünschten Überprüfungen durchführen.

Für weitere detaillierte Informationen über DLL-Verknüpfungen können Sie "Linkage" oder andere Quellen konsultieren.

## Memory Leak Detector

Nachdem ich das Prinzip verstanden habe, folgt nun die Umsetzung der Erkennung von Speicherlecks basierend auf diesem Prinzip. Die folgende Erklärung wird auf meiner eigenen Implementierung basieren, die ich auf meinem GitHub veröffentlicht habe: [LeakDetector](https://github.com/disenone/LeakDetector)。

####Ersatzfunktion

Lassen Sie uns zunächst die entscheidenden Funktionen betrachten, die sich in [RealDetector.cpp](https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp)Bitte geben Sie den Text an, den Sie ins Deutsche übersetzen möchten.

```cpp linenums="1"
Ersetzen Sie in importModule eine Funktion der IAT (Import Address Table) durch eine andere Funktion.
importModule ruft Funktionen aus anderen Modulen auf, diese Funktion muss gepatcht werden.
Was wir tun müssen, ist das Importieren des Moduls durch den Aufruf unserer benutzerdefinierten Funktion zu ersetzen.
 *
* - importModule (IN): Zu verarbeitendes Modul, dieses Modul ruft Funktionen anderer Module auf, die patched werden müssen.
 *
* - exportModuleName (IN): Der Name des Moduls, aus dem die zu patchende Funktion stammt.
 *
* - exportModulePath (IN): Der Pfad, an dem sich das Exportmodul befindet, zunächst versuchen, das Exportmodul mit dem Pfad zu laden.
Wenn fehlgeschlagen, dann mit Name laden.
* - importName (IN): Funktionsname
 *
- Ersatz (IN): Funktion Pointer
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

Lass uns diese Funktion analysieren. Wie im Kommentar erwähnt, besteht die Funktion darin, die Adresse einer bestimmten Funktion im IAT in die Adresse einer anderen Funktion zu ändern. Schauen wir uns zunächst die Zeilen 34-35 an:

``` cpp
idte = (IMAGE_IMPORT_DESCRIPTOR*)ImageDirectoryEntryToDataEx((PVOID)importModule, 
	TRUE, IMAGE_DIRECTORY_ENTRY_IMPORT, &size, &section);
```

Die Funktion `ImageDirectoryEntryToDataEx` gibt die Adresse einer bestimmten Struktur im Dateikopf eines Moduls zurück. `IMAGE_DIRECTORY_ENTRY_IMPORT` bestimmt die Importtabellestruktur, daher zeigt `idte`, das zurückgegeben wird, auf die Importtabelle des Moduls.

In Zeile 36-40 wird überprüft, ob "idte" gültig ist. In Zeile 41 zeigt "idte->FirstThunk" auf die tatsächliche IAT. Daher werden in den Zeilen 41-48 die Funktionen des Moduls gesucht, die ersetzt werden müssen, wenn das Modul anhand des Modulnamens nicht gefunden werden kann, bedeutet das, dass die Funktionen dieses Moduls nicht aufgerufen wurden, es wird ein Fehler gemeldet und zurückgegeben.

Nachdem das Modul gefunden wurde, muss natürlich die zu ersetzende Funktion gefunden werden. In den Zeilen 55-62 wird das Modul geöffnet, zu dem die Funktion gehört, und in Zeile 64 die Adresse der Funktion gefunden. Da das IAT keine Namen speichert, muss zunächst die Funktion anhand der ursprünglichen Adresse lokalisiert und dann die Adresse dieser Funktion geändert werden. In den Zeilen 68-80 wird genau das gemacht. Nach erfolgreichem Auffinden der Funktion wird die Adresse einfach in die Adresse des `Ersatzes` geändert.

Bis hierhin haben wir erfolgreich die Funktion im IAT ersetzt.

####Modul- und Funktionsnamen

Obwohl wir die Ersetzung der IAT-Funktion `patchImport` bereits umgesetzt haben, benötigt diese Funktion die Angabe des Modul- und Funktionsnamens. Aber wie können wir herausfinden, welche Module und Funktionen für die Speicherzuweisung und -freigabe des Programms verwendet werden? Um dieses Problem zu klären, müssen wir das Tool [Dependency Walker](http://www.dependencywalker.com/)Erstellen Sie in Visual Studio ein neues Projekt und verwenden Sie im `main`-Funktion `new`, um Speicher anzufordern. Kompilieren Sie die Debug-Version und öffnen Sie dann die kompilierte exe-Datei mit `depends.exe`, um eine ähnliche Benutzeroberfläche zu sehen (zum Beispiel mein Projekt [LeakDetectorTest](https://github.com/disenone/LeakDetector/tree/master/LeakDetectorTest)Um das zu illustrieren:

![](assets/img/2016-6-11-memory-leak-detector/depends.png)

You can see that LeakDetectorTest.exe uses `malloc` and `_free_dbg` from uscrtbased.dll (not shown in the image), these are the functions we need to replace. Please note that the actual module function names may vary depending on your Windows and Visual Studio versions. In my case, I am using Windows 10 and Visual Studio 2015. What you need to do is to use depends.exe to check which functions are actually being called.

####Analyse des Aufrufstacks

(https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp)。

####Speicherleck-Überprüfung

Bis hierhin haben wir alle Drachenbälle gesammelt, jetzt rufen wir offiziell Shenlong herbei.

Ich möchte eine Lösung entwickeln, die eine partielle Erkennung von Speicherlecks ermöglicht (dies unterscheidet sich von VLD, das eine globale Erkennung durchführt und Mehrfach-Threads unterstützt). Daher habe ich auf der Klasse `RealDetector`, die die Funktionen tatsächlich ersetzt, eine weitere Schicht in Form von `LeakDetector` hinzugefügt und die Schnittstelle von `LeakDetector` den Benutzern zugänglich gemacht. Bei der Verwendung muss man lediglich `LeakDetector` instanziieren, um die Funktion zu ersetzen und mit der Erkennung von Speicherlecks zu beginnen. Bei der Zerstörung von `LeakDetector` wird die ursprüngliche Funktion wiederhergestellt, die Erkennung von Speicherlecks eingestellt und die Ergebnisse der Speicherleck-Erkennung ausgegeben.

Testen Sie es mit dem folgenden Code:

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

Der Code hat direkt Speicher mit `new` allokiert, wurde aber nicht freigegeben und ist dann ohne Freigabe beendet, was zu folgendem Programmausdruck führte:

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

The program successfully identified the two memory allocations that were not released, printed the complete call stack information, and thus the required functionality has been completed.

###Schlussfolgerung

Wenn du noch nicht mit Programmverlinkung, Laden und Bibliotheken vertraut bist, könntest du verwirrt sein, wie man die Funktionen einer gemeinsamen Linkbibliothek findet, ganz zu schweigen davon, diese Funktionen durch unsere eigenen Funktionen zu ersetzen. Hier nehmen wir als Beispiel die Erkennung von Speicherlecks, um zu erörtern, wie man die Funktionen einer Windows DLL ersetzt. Detailliertere Implementierungen können im Quellcode von VLD nachgelesen werden.

Außerdem möchte ich sagen, dass "Die Selbstverbesserung des Programmierers: Verlinkung, Laden und Bibliotheken" wirklich ein gutes Buch ist, ich äußere lediglich meine Gedanken, ohne Werbung zu machen.

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt, bitte geben Sie Ihr [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Bitte weisen Sie auf etwaige Auslassungen hin. 
