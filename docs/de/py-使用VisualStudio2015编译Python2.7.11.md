---
layout: post
title: Visual Studio 2015 verwenden, um Python 2.7.11 zu kompilieren
categories:
- python
catalog: true
tags:
- dev
description: Die offizielle Version von Python 2.7 unterstützt die Kompilierung mit
  Visual Studio 2010 und älteren Versionen. Wenn du Python unter Windows selbst kompilieren
  möchtest, zum Beispiel eine Debug-Version erstellen oder den Quellcode bearbeiten
  möchtest, dann ist die einfachste Methode, Visual Studio 2010 zu installieren. Aber
  für mich persönlich möchte ich Python lieber mit VS2015 kompilieren, hauptsächlich
  aus folgenden Gründen...
figures:
- https://img.shields.io/badge/python-2.7.11-brightgreen.svg
- https://img.shields.io/badge/vs-2015-68217A.svg
nowidth: 1
---

<meta property="og:title" content="使用 Visual Studio 2015 编译 Python 2.7.11" />

![](https://img.shields.io/badge/python-2.7.11-brightgreen.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}

##Ursache

Die offizielle Version von Python 2.7 unterstützt zur Kompilierung Versionen von Visual Studio 2010 und älter. Siehe `PCbuild\readme.txt`:


	1.  Install Microsoft Visual Studio 2008, any edition.
	2.  Install Microsoft Visual Studio 2010, any edition, or Windows SDK 7.1 and any version of Microsoft Visual Studio newer than 2010.


Wenn Sie mit Python auf Windows herumspielen möchten, zum Beispiel Debug-Versionen kompilieren oder den Quellcode ändern möchten, ist die einfachste Methode die Installation von VS2010.
Aber persönlich möchte ich lieber Python mit VS2015 kompilieren, aus folgenden Gründen:


VS2010 ist wirklich etwas veraltet und bietet im Vergleich zu VS2015 viel weniger Funktionen und eine schlechtere Benutzererfahrung. Ich benutze schon lange VS2015 und möchte wirklich nicht wieder auf VS2010 umsteigen.
- Da du immer mit VS2015 gearbeitet hast, wirst du es nutzen, um einige eigene Programme zu schreiben. Wenn du Python einbetten möchtest, musst du die gleiche Version von VS verwenden, um dein Programm zu kompilieren. Wenn du eine andere Version von VS verwendest, können verschiedene unvorhersehbare Probleme auftreten. [Hier gibt es eine detailliertere Erklärung](http://siomsystems.com/mixing-visual-studio-versions/)。

Also habe ich angefangen, mit VS2015 die Version 2.7.11 von Python zu lösen (die aktuellste Version von Python 2.7).

Bitte beachten Sie, dass **Python 3.x bereits die Kompilierung mit VS2015 unterstützt**.

##Quellcode-Download

Die Version von Python ist natürlich 2.7.11, außerdem gibt es einige Drittanbieter-Module. Genauere Informationen kannst du erhalten, indem du das Skript `PCbuild\get_externals.bat` im Quellverzeichnis von Python ausführst, um alle für die Kompilierung benötigten Module herunterzuladen. Beachte, dass du svn installieren und svn.exe zum System-PATH hinzufügen musst.

Der Download kann instabil sein und der gesamte Prozess kann aufgrund von Netzwerkproblemen abgebrochen werden. Es wird daher empfohlen, das "externals"-Verzeichnis direkt von meinem GitHub herunterzuladen: [Meine Python-Version](https://github.com/disenone/wpython-2.7.11/tree/e13f43a3b72ae2bdf4d2950c6364750ae668cbf4/externals)

##Compile process

###Drittanbieter-Modul

Zuerst müssen wir uns mit den Modulen von Drittanbietern befassen, hauptsächlich tcl, tk und tcltk.

Ändern Sie die Datei `externals/tcl-8.5.15.0/win/makefile.vc`, ändern Sie die Zeile 434 in

	- cdebug = -Zi -WX $(DEBUGFLAGS)
	+ cdebug = -Zi -WX- $(DEBUGFLAGS)

In Bezug auf die Option `WX` können Sie die offizielle Dokumentation von Microsoft einsehen: [/WX (Behandle Linker-Warnungen als Fehler)](https://msdn.microsoft.com/en-us/library/ms235592.aspx)

Ändern Sie erneut `PCbuild/tk.vcxproj`, öffnen Sie es mit einem Texteditor und bearbeiten Sie die Zeilen 63 und 64.

	- <TkOpts>msvcrt</TkOpts>
	- <TkOpts Condition="$(Configuration) == 'Debug'">symbols,msvcrt</TkOpts>
	+ <TkOpts>msvcrt,noxp</TkOpts>
	+ <TkOpts Condition="$(Configuration) == 'Debug'">symbols,msvcrt,noxp</TkOpts>

Ändere `PCbuild/tcltk.props`, öffne es mit einem Texteditor und ändere die Zeile 41.

	- <BuildDirTop>$(BuildDirTop)_VC9</BuildDirTop>
	+ <BuildDirTop>$(BuildDirTop)_VC13</BuildDirTop>

Da VS2015 die Definition von `timezone` aufgehoben hat und nun `_timezone` verwendet wird, müssen alle Stellen im Code, an denen `timezone` verwendet wird, in `_timezone` geändert werden. Für das Drittanbieter-Modul muss nur die Datei `externals/tcl-8.5.15.0/win/tclWinTime.c` geändert werden, indem am Anfang der Datei Folgendes hinzugefügt wird:

	#if defined _MSC_VER && _MSC_VER >= 1900
	#define timezone _timezone
	#endif

###Python-Quellcode ändern

Das Problem mit `timezone` gibt es auch im Python-Modul `time`, ändere Zeile 767.

	- #ifdef __CYGWIN__
	+ #if defined(__CYGWIN__) || defined(_MSC_VER) && _MSC_VER >= 1900

Außerdem wurde in Windows eine spezielle Methode verwendet, um die Gültigkeit von Dateihandles in Python zu überprüfen, die in VS2015 vollständig deaktiviert ist, was zu Kompilierungsfehlern führt. Daher muss dies zuerst geändert werden. Datei `Include/fileobject.h`, Zeilen 73 und 80:

	73 - #if defined _MSC_VER && _MSC_VER >= 1400
	73 + #if defined _MSC_VER && _MSC_VER >= 1400 && _MSC_VER < 1900

	80 - #elif defined _MSC_VER && _MSC_VER >= 1200
	80 + #elif defined _MSC_VER && _MSC_VER >= 1200 && _MSC_VER < 1400

Datei `Modules/posixmodule.c`, Zeile 532:

	- #if defined _MSC_VER && _MSC_VER >= 1400
	+ #if defined _MSC_VER && _MSC_VER >= 1400 && _MSC_VER < 1900

An dieser Stelle sollte Python erfolgreich kompiliert werden. Weitere spezifische Änderungen finden Sie in meinen Commit-Inhalten: [modify to build by vs2015](https://github.com/disenone/wpython-2.7.11/commit/4037e2d806518dbf06ffb8ee5c46f419ef8d7edf)


###Überprüfung ungültiger Handles

Obwohl die Kompilierung erfolgreich war, führt das grobe Ignorieren ungültiger Datei-Handles dazu, dass beim Zugriff auf ungültige Handles (zum Beispiel beim zweimaligen Schließen derselben Datei) ein direkter Assertion-Fehler auftritt und das Programm abstürzt. So kann Python einfach nicht verwendet werden. Python verwendet eine sehr spezielle Methode, um dieses Szenario zu vermeiden, aber leider funktioniert sie nicht mehr in VS2015. Dies wird in den Kommentaren erklärt:

	Microsoft CRT in VS2005 and higher will verify that a filehandle is valid and raise an assertion if it isn't.


Gelukkig is er al een oplossing gevonden, ik heb het gezien in het Python-issue, het adres is hier: [issue23524](http://psf.upfronthosting.co.za/roundup/tracker/issue23524), [issue25759](http://psf.upfronthosting.co.za/roundup/tracker/issue25759)Diese Methode wird auch in der aktuellen Python 3.x Version verwendet.


Konkret bedeutet das, dass beim Umgang mit Datei-Handles die Assert-Crash-Mechanismus von Windows deaktiviert wird und stattdessen der Fehlercode überprüft wird. Wie deaktiviert man also den Assert-Mechanismus von Windows? Die Antwort ist, dass man seine eigene Fehlerbehandlungsfunktion anstelle der standardmäßigen Behandlungsfunktion von Windows verwendet. Der entscheidende Code:


Neue Datei `PC/invalid_parameter_handler.c` erstellen, um unsere eigene Fehlerbehandlungsfunktion zu definieren; vorübergehend können die aufgetretenen Fehler ignoriert werden.

```c++
#ifdef _MSC_VER

#include <stdlib.h>

#if _MSC_VER >= 1900
/* pyconfig.h uses this function in the _Py_BEGIN_SUPPRESS_IPH/_Py_END_SUPPRESS_IPH
 * macros. It does not need to be defined when building using MSVC
 * earlier than 14.0 (_MSC_VER == 1900).
 */

static void __cdecl _silent_invalid_parameter_handler(
    wchar_t const* expression,
    wchar_t const* function,
    wchar_t const* file,
    unsigned int line,
	uintptr_t pReserved) 
{}

_invalid_parameter_handler _Py_silent_invalid_parameter_handler = _silent_invalid_parameter_handler;

#endif

#endif
```

Definieren Sie zwei Makros zur bequemen Änderung der Fehlerbehandlungsfunktion. Beachten Sie, dass es sich um eine vorübergehende Änderung handelt, die später auf das Standard-System zurückgesetzt werden muss.

```c++
#if defined _MSC_VER && _MSC_VER >= 1900

extern _invalid_parameter_handler _Py_silent_invalid_parameter_handler;
#define _Py_BEGIN_SUPPRESS_IPH { _invalid_parameter_handler _Py_old_handler = \
    _set_thread_local_invalid_parameter_handler(_Py_silent_invalid_parameter_handler);
#define _Py_END_SUPPRESS_IPH _set_thread_local_invalid_parameter_handler(_Py_old_handler); }

#else

#define _Py_BEGIN_SUPPRESS_IPH
#define _Py_END_SUPPRESS_IPH

#endif /* _MSC_VER >= 1900 */
```

Danach fügen Sie an Stellen, an denen ein Windows-Dateihandlesfehler auftreten könnte, jeweils die Makros `_Py_BEGIN_SUPPRESS_IPH` und `_Py_END_SUPPRESS_IPH` hinzu. Anschließend können Sie den Fehlercode überprüfen. Es gibt viele Stellen, die geändert werden müssen; orientieren Sie sich an den Commits anderer zur Modifikation.
Translate these text into German language:

[Hier](https://github.com/kovidgoyal/cpython/commit/a9ec814d466d3c0139d10b69666f88eed10e4940)

##Ende

Bis hierhin kann Python 2.7.11 in VS2015 normal kompiliert und ausgeführt werden, jedoch wird von der Python-Organisation nicht empfohlen, diese Einstellung so vorzunehmen.

	***WARNING***
	Building Python 2.7 for Windows using any toolchain that doesn't link
	against MSVCRT90.dll is *unsupported* as the resulting python.exe will
	not be able to use precompiled extension modules that do link against
	MSVCRT90.dll.

Daher ist es am besten, darauf zu achten, wenn man es benutzt.

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt worden. Bitte im [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Bitte weisen Sie auf etwaige Auslassungen hin. 
