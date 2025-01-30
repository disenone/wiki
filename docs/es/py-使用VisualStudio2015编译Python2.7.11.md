---
layout: post
title: Compilando Python 2.7.11 con Visual Studio 2015
categories:
- python
catalog: true
tags:
- dev
description: La versión oficial de Python 2.7 solo es compatible con Visual Studio
  2010 y versiones anteriores para compilar. Si quieres trastear con Python en Windows,
  como compilar una versión de depuración o modificar el código fuente, la forma más
  sencilla es instalar el VS2010. Sin embargo, personalmente, preferiría compilar
  Python con el VS2015, principalmente por razones como...
figures:
- https://img.shields.io/badge/python-2.7.11-brightgreen.svg
- https://img.shields.io/badge/vs-2015-68217A.svg
nowidth: 1
---

<meta property="og:title" content="使用 Visual Studio 2015 编译 Python 2.7.11" />

![](https://img.shields.io/badge/python-2.7.11-brightgreen.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}

##Razón

La versión oficial de Python 2.7 es compatible con versiones anteriores a Visual Studio 2010 para compilar. Consulte `PCbuild\readme.txt`.


	1.  Install Microsoft Visual Studio 2008, any edition.
	2.  Install Microsoft Visual Studio 2010, any edition, or Windows SDK 7.1 and any version of Microsoft Visual Studio newer than 2010.


Si deseas jugar con Python en Windows, como compilar una versión de depuración o modificar el código fuente, la forma más sencilla es instalar un VS2010.
Sin embargo, personalmente prefiero compilar Python con VS2015, principalmente por las siguientes razones:


- VS2010 está realmente un poco desactualizado, su funcionalidad y experiencia de uso son mucho peores que las de VS2015. He estado usando VS2015, no tengo ganas de instalar VS2010.
- Debido a que has estado utilizando VS2015, lo usarás para escribir algunos de tus propios programas. Si deseas incrustar Python, necesitarás usar la misma versión de VS para compilar tu programa. Si usas una versión diferente de VS, pueden surgir diversos problemas impredecibles. [Aquí hay una explicación más detallada](http://siomsystems.com/mixing-visual-studio-versions/)Lo siento, pero no hay texto visible para traducir. ¿Puedo ayudarte con algo más?

Así que empecé a trabajar con VS2015 para resolver la versión 2.7.11 de Python (la versión más reciente de Python 2.7).

Es importante tener en cuenta que **Python 3.x ya es compatible con la compilación en VS2015**.

##Descarga del código fuente

La versión de Python es, por supuesto, la 2.7.11, además hay varios módulos de terceros, puedes ejecutar el script `PCbuild\get_externals.bat` en el directorio de código fuente de Python para obtener todos los módulos necesarios para la compilación, ten en cuenta que necesitarás instalar svn y añadir svn.exe al PATH del sistema.

La descarga puede ser bastante inestable y todo el proceso puede verse interrumpido debido a problemas de red, por lo que se recomienda descargar directamente el directorio externals desde mi github: [mi versión de Python](https://github.com/disenone/wpython-2.7.11/tree/e13f43a3b72ae2bdf4d2950c6364750ae668cbf4/externals)

##Proceso de compilación

###Módulo de terceros

El primer paso es abordar los módulos de terceros, principalmente tcl, tk, tcltk.

Modifica el archivo `externals/tcl-8.5.15.0/win/makefile.vc`, y cambia la línea 434 a

	- cdebug = -Zi -WX $(DEBUGFLAGS)
	+ cdebug = -Zi -WX- $(DEBUGFLAGS)

Sobre la opción `WX`, puedes consultar la documentación oficial de Microsoft: [/WX (Tratar advertencias del enlazador como errores)](https://msdn.microsoft.com/en-us/library/ms235592.aspx)

Editar `PCbuild/tk.vcxproj` de nuevo, abre con un editor de texto y modifica las líneas 63 y 64.

	- <TkOpts>msvcrt</TkOpts>
	- <TkOpts Condition="$(Configuration) == 'Debug'">symbols,msvcrt</TkOpts>
	+ <TkOpts>msvcrt,noxp</TkOpts>
	+ <TkOpts Condition="$(Configuration) == 'Debug'">symbols,msvcrt,noxp</TkOpts>

Modifica `PCbuild/tcltk.props`, ábrelo con un editor de texto y cambia la línea 41.

	- <BuildDirTop>$(BuildDirTop)_VC9</BuildDirTop>
	+ <BuildDirTop>$(BuildDirTop)_VC13</BuildDirTop>

Debido a que en VS2015 se eliminó la definición de `timezone` y se reemplazó por `_timezone`, es necesario modificar todas las referencias a `timezone` en el código por `_timezone`. Para ello, solo es necesario editar el archivo `externals/tcl-8.5.15.0/win/tclWinTime.c` y agregar lo siguiente al inicio del archivo:

	#if defined _MSC_VER && _MSC_VER >= 1900
	#define timezone _timezone
	#endif

###Modificar el código fuente de Python.

El problema de `timezone` también está presente en el módulo `time` de Python, modifica la línea 767.

	- #ifdef __CYGWIN__
	+ #if defined(__CYGWIN__) || defined(_MSC_VER) && _MSC_VER >= 1900

Además, debido a que en Windows Python utiliza un método especial para verificar la validez del identificador de archivo, el cual ha sido completamente prohibido en VS2015, se producirán errores de compilación, por lo que primero hay que corregirlo. Archivo `Include/fileobject.h`, líneas 73 y 80:

	73 - #if defined _MSC_VER && _MSC_VER >= 1400
	73 + #if defined _MSC_VER && _MSC_VER >= 1400 && _MSC_VER < 1900

	80 - #elif defined _MSC_VER && _MSC_VER >= 1200
	80 + #elif defined _MSC_VER && _MSC_VER >= 1200 && _MSC_VER < 1400

Archivo `Modules/posixmodule.c`, línea 532:

	- #if defined _MSC_VER && _MSC_VER >= 1400
	+ #if defined _MSC_VER && _MSC_VER >= 1400 && _MSC_VER < 1900

Hasta aquí, Python puede compilarse correctamente. Para ver modificaciones más específicas, revisa el contenido de mi commit: [modify to build by vs2015](https://github.com/disenone/wpython-2.7.11/commit/4037e2d806518dbf06ffb8ee5c46f419ef8d7edf)


###Verifique si el identificador es inválido.

Aunque la compilación fue exitosa, el hecho de ignorar de manera brusca los manejadores de archivos inválidos tiene como consecuencia directa que, al intentar acceder a un manejador inválido (por ejemplo, cerrar el mismo archivo `close` dos veces), Python simplemente fallará con un assert, haciendo que el programa se bloquee. Un Python así es completamente inutilizable. Python utiliza un método muy especial para evitar esta situación, pero desafortunadamente no se puede usar en VS2015; la anotación lo explica de la siguiente manera:

	Microsoft CRT in VS2005 and higher will verify that a filehandle is valid and raise an assertion if it isn't.


Afortunadamente ya se ha encontrado una solución, la vi en la sección de problemas de Python, aquí está el enlace: [issue23524](http://psf.upfronthosting.co.za/roundup/tracker/issue23524), [issue25759](http://psf.upfronthosting.co.za/roundup/tracker/issue25759)Este método también se utiliza en la actualidad en Python 3.x.


Traduce este texto al español:

En concreto, se trata de desactivar el mecanismo de fallo de assert de Windows al usar el identificador de archivo, y cambiarlo por la comprobación de códigos de error. ¿Cómo se puede desactivar el mecanismo de assert de Windows? La respuesta es utilizar una función de manejo de errores propia en lugar de la predeterminada de Windows. El código clave es:


Crea el archivo `PC/invalid_parameter_handler.c`, donde definimos nuestra propia función de manejo de errores, la cual puede ignorar temporalmente los errores que ocurran.

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

Definir dos macros para facilitar el cambio de la función de manejo de errores; hay que tener en cuenta que es un cambio temporal y que luego es necesario volver a la predeterminada del sistema.

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

Agrega el macro `_Py_BEGIN_SUPPRESS_IPH` antes y `_Py_END_SUPPRESS_IPH` después de lugares donde pueda desencadenar un error de manejador de archivos de Windows. Luego, simplemente revisa el código de error. Será necesario ajustar varios puntos, puedes guiarte por los commits de otros para hacerlo.
[En este lugar](https://github.com/kovidgoyal/cpython/commit/a9ec814d466d3c0139d10b69666f88eed10e4940)

##Finalizar

A partir de ahora, Python 2.7.11 se puede compilar y ejecutar correctamente en VS2015, aunque Python oficial no recomienda esta configuración.

	***WARNING***
	Building Python 2.7 for Windows using any toolchain that doesn't link
	against MSVCRT90.dll is *unsupported* as the resulting python.exe will
	not be able to use precompiled extension modules that do link against
	MSVCRT90.dll.

Así que es mejor prestar atención al usarlo.

--8<-- "footer_es.md"


> Este post fue traducido utilizando ChatGPT, por favor en [**retroalimentación**](https://github.com/disenone/wiki_blog/issues/new)Indique cualquier omisión. 
