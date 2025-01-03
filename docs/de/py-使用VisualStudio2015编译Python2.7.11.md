---
layout: post
title: Verwenden Sie Visual Studio 2015 zum Kompilieren von Python 2.7.11.
categories:
- python
catalog: true
tags:
- dev
description: Die offizielle Version von Python 2.7 unterstützt das Übersetzen mit
  Versionen von Visual Studio 2010 und früher. Wenn du Python unter Windows selbst
  kompilieren möchtest, zum Beispiel um eine Debug-Version zu erstellen oder den Quellcode
  zu ändern, dann ist das einfachste Vorgehen, Visual Studio 2010 zu installieren.
  Persönlich bevorzuge ich jedoch, Python mit Visual Studio 2015 zu kompilieren, hauptsächlich
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

Die offizielle Version von Python 2.7 unterstützt die Kompilierung unter Visual Studio 2010 und älteren Versionen. Siehe `PCbuild\readme.txt` für weitere Informationen:


	1.  Install Microsoft Visual Studio 2008, any edition.
	2.  Install Microsoft Visual Studio 2010, any edition, or Windows SDK 7.1 and any version of Microsoft Visual Studio newer than 2010.


Wenn Sie Python unter Windows selbst einrichten möchten, zum Beispiel um eine Debug-Version zu kompilieren oder den Quellcode anzupassen, ist der einfachste Weg die Installation von VS2010.
Für mich persönlich bevorzuge ich es, Python mit VS2015 zu kompilieren, aus folgenden Gründen:


VS2010 ist wirklich ein bisschen veraltet und die Funktionen und das Benutzererlebnis sind im Vergleich zu VS2015 viel schlechter. Ich benutze immer noch VS2015 und möchte wirklich nicht noch einmal VS2010 installieren.
Aufgrund der Verwendung von VS2015 schreibst du deine eigenen Programme damit. Wenn du Python einbetten möchtest, musst du die gleiche Version von VS verwenden, um deine Programme zu kompilieren. Die Verwendung einer anderen VS-Version könnte unvorhergesehene Probleme verursachen. [Hier gibt es eine ausführlichere Erklärung](http://siomsystems.com/mixing-visual-studio-versions/)I am sorry, but there is no text to translate in your request.

Deshalb habe ich angefangen, mit VS2015 die Python-Version 2.7.11 (die neueste Version von Python 2.7) zu bewältigen.

Bitte beachten Sie, dass **Python 3.x die Verwendung von VS2015 zum Kompilieren unterstützt**.

##Quellcode herunterladen.

Die Version von Python ist natürlich 2.7.11. Es gibt auch einige Drittanbieter-Module. Du kannst das Skript `PCbuild\get_externals.bat` im Python-Quellcodeverzeichnis ausführen, um alle erforderlichen Kompilierungsmodelle zu erhalten. Beachte, dass du svn installieren und svn.exe zum System-PATH hinzufügen musst.

Das Herunterladen kann sehr instabil sein, und der gesamte Prozess könnte aufgrund von Netzwerkproblemen abbrechen. Daher empfehle ich Ihnen, das Verzeichnis "Externals" direkt von meinem Github herunterzuladen: [Meine Python-Version](https://github.com/disenone/wpython-2.7.11/tree/e13f43a3b72ae2bdf4d2950c6364750ae668cbf4/externals)

##Der Kompilierungsprozess.

###Drittanbietermodul

Zunächst müssen die Third-Party-Module gelöst werden, hauptsächlich tcl, tk, tcltk.

Bearbeiten Sie die Datei `externals/tcl-8.5.15.0/win/makefile.vc` und ändern Sie Zeile 434.

	- cdebug = -Zi -WX $(DEBUGFLAGS)
	+ cdebug = -Zi -WX- $(DEBUGFLAGS)

In Bezug auf die Option 'WX' können Sie das offizielle Microsoft-Dokument einsehen: [/WX (Behandle Linker-Warnungen als Fehler)](https://msdn.microsoft.com/en-us/library/ms235592.aspx)

Bearbeiten Sie die Datei `PCbuild/tk.vcxproj` erneut, öffnen Sie sie mit einem Texteditor und ändern Sie die Zeilen 63 und 64.

	- <TkOpts>msvcrt</TkOpts>
	- <TkOpts Condition="$(Configuration) == 'Debug'">symbols,msvcrt</TkOpts>
	+ <TkOpts>msvcrt,noxp</TkOpts>
	+ <TkOpts Condition="$(Configuration) == 'Debug'">symbols,msvcrt,noxp</TkOpts>

Ändern Sie `PCbuild/tcltk.props`, öffnen Sie es mit einem Texteditor und bearbeiten Sie Zeile 41.

	- <BuildDirTop>$(BuildDirTop)_VC9</BuildDirTop>
	+ <BuildDirTop>$(BuildDirTop)_VC13</BuildDirTop>

Due to the cancellation of the definition of `timezone` in VS2015, it is changed to `_timezone`. Therefore, all occurrences of `timezone` in the code need to be changed to `_timezone`. Third-party modules only need to modify the file `externals/tcl-8.5.15.0/win/tclWinTime.c` by adding the following at the beginning of the file:

	#if defined _MSC_VER && _MSC_VER >= 1900
	#define timezone _timezone
	#endif

###Ändern Sie den Python-Quellcode.

Das Problem mit der `timezone` ist auch im Python-Modul` time` existent, bitte ändern Sie Zeile 767.

	- #ifdef __CYGWIN__
	+ #if defined(__CYGWIN__) || defined(_MSC_VER) && _MSC_VER >= 1900

Des Weiteren wurde eine spezielle Methode von Python unter Windows verwendet, um die Gültigkeit von Datei-Handles zu prüfen. Diese Methode wurde jedoch in VS2015 komplett verboten, was zu Kompilierfehlern führt. Daher sollte sie zuerst angepasst werden. In der Datei `Include/fileobject.h`, Zeilen 73 und 80:

	73 - #if defined _MSC_VER && _MSC_VER >= 1400
	73 + #if defined _MSC_VER && _MSC_VER >= 1400 && _MSC_VER < 1900

	80 - #elif defined _MSC_VER && _MSC_VER >= 1200
	80 + #elif defined _MSC_VER && _MSC_VER >= 1200 && _MSC_VER < 1400

Die Datei `Modules/posixmodule.c`, Zeile 532:

	- #if defined _MSC_VER && _MSC_VER >= 1400
	+ #if defined _MSC_VER && _MSC_VER >= 1400 && _MSC_VER < 1900

An diesem Punkt kann Python nun kompiliert werden. Weitere spezifische Änderungen können in meinem Commit-Verlauf unter [modify to build by vs2015](https://github.com/disenone/wpython-2.7.11/commit/4037e2d806518dbf06ffb8ee5c46f419ef8d7edf)


###"Überprüfen Sie den ungültigen Handle."

Obwohl der Code erfolgreich kompiliert wurde, führt das brutale Ignorieren ungültiger Datei-Handles dazu, dass bei Zugriff auf solche ungültigen Handles (zum Beispiel beim zweimaligen Schließen derselben Datei) Python einfach einen Assert-Fehler auslöst und das Programm abstürzt. So kann man Python überhaupt nicht verwenden. Python verwendet normalerweise eine spezielle Methode, um diese Situation zu vermeiden, aber leider funktioniert sie nicht in VS2015. Der Kommentar erklärt dies wie folgt:

	Microsoft CRT in VS2005 and higher will verify that a filehandle is valid and raise an assertion if it isn't.


Zum Glück gibt es bereits eine Lösungsmethode, die ich im Python-Problembericht gefunden habe. Die Adresse lautet hier: [issue23524](http://psf.upfronthosting.co.za/roundup/tracker/issue23524), [issue25759](http://psf.upfronthosting.co.za/roundup/tracker/issue25759)Diese Methode wird auch in der aktuellen Version Python 3.x verwendet.


Um Missverständnisse zu vermeiden, übersetze ich den Text ins Deutsche:

Genauer gesagt geht es darum, beim Verwenden von Datei-Handgriffen das assert crash Mechanismus von Windows zu deaktivieren und stattdessen den Fehlercode zu prüfen. Wie kann man also den assert Mechanismus von Windows deaktivieren? Die Antwort besteht darin, seine eigene Fehlerbehandlungsfunktion anstelle der Standardfunktion von Windows zu verwenden. Der entscheidende Code:  


Erstellen Sie die Datei `PC/invalid_parameter_handler.c` und definieren Sie unsere eigene Fehlerbehandlungsfunktion, die auftretende Fehler vorübergehend ignorieren kann.

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

Definieren Sie zwei Makros zur einfachen Änderung der Fehlerbehandlungsfunktion. Bitte beachten Sie, dass dies vorübergehende Änderungen sind und anschließend wieder auf die Standardsystemeinstellungen zurückgesetzt werden müssen.

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

Nachfolgend fügen Sie an Stellen, die möglicherweise einen Windows-Datei-Handle-Fehler auslösen könnten, das Makro`_Py_BEGIN_SUPPRESS_IPH` und `_Py_END_SUPPRESS_IPH` vor und nach dem jeweiligen Code ein. Anschließend können Sie den Fehlercode überprüfen. Es müssen viele Stellen geändert werden, orientieren Sie sich an Commits anderer Personen, um Änderungen vorzunehmen:
[Hier](https://github.com/kovidgoyal/cpython/commit/a9ec814d466d3c0139d10b69666f88eed10e4940)

##Ende

An dieser Stelle kann Python 2.7.11 erfolgreich in VS2015 kompiliert und ausgeführt werden. Allerdings wird dies von den offiziellen Python-Entwicklern nicht empfohlen.

	***WARNING***
	Building Python 2.7 for Windows using any toolchain that doesn't link
	against MSVCRT90.dll is *unsupported* as the resulting python.exe will
	not be able to use precompiled extension modules that do link against
	MSVCRT90.dll.

Es ist am besten, darauf zu achten, wenn Sie es verwenden.

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt, bitte im [Feedback](https://github.com/disenone/wiki_blog/issues/new)Zeigen Sie alle Unklarheiten auf. 
