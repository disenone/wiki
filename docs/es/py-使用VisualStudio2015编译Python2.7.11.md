---
layout: post
title: Usa Visual Studio 2015 para compilar Python 2.7.11.
categories:
- python
catalog: true
tags:
- dev
description: La versión oficial de Python 2.7 tiene soporte para compilar con versiones
  anteriores a Visual Studio 2010. Si quieres trastear con Python en Windows, por
  ejemplo, compilar una versión de depuración o modificar el código fuente, la forma
  más sencilla es instalar Visual Studio 2010. Sin embargo, personalmente preferiría
  utilizar Visual Studio 2015 para compilar Python, principalmente por las siguientes
  razones...
figures:
- https://img.shields.io/badge/python-2.7.11-brightgreen.svg
- https://img.shields.io/badge/vs-2015-68217A.svg
nowidth: 1
---

<meta property="og:title" content="使用 Visual Studio 2015 编译 Python 2.7.11" />

![](https://img.shields.io/badge/python-2.7.11-brightgreen.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}

##**原因**

La versión oficial de Python 2.7 admite la compilación con versiones anteriores a Visual Studio 2010. Consulte `PCbuild\readme.txt` para obtener más información.


	1.  Install Microsoft Visual Studio 2008, any edition.
	2.  Install Microsoft Visual Studio 2010, any edition, or Windows SDK 7.1 and any version of Microsoft Visual Studio newer than 2010.


Si quieres jugar con Python en Windows, como compilar una versión de depuración, modificar el código fuente, etc., entonces la forma más sencilla es instalar VS2010.
Pero para mí personalmente, prefiero compilar Python con VS2015, principalmente por las siguientes razones:


- **VS2010** está un poco desactualizado, su funcionalidad y experiencia de uso son mucho peores que los de **VS2015**. He estado usando **VS2015** todo este tiempo, no quiero ni pensar en instalar **VS2010** de nuevo.
- Debido a que has estado utilizando VS2015, lo usarás para escribir tus propios programas. Si quieres incorporar Python en ellos, necesitarás utilizar la misma versión de VS para compilar tus programas. Si utilizas una versión diferente de VS, podrían surgir diversas situaciones imprevistas. [aquí hay una explicación más detallada](http://siomsystems.com/mixing-visual-studio-versions/).

Así que comencé a trabajar en la versión 2.7.11 de Python utilizando VS2015 (la última versión de Python 2.7 actualmente).

Debes tener en cuenta que **Python 3.x ya es compatible con la compilación en VS2015**.

##Descarga del código fuente

La versión de Python es, por supuesto, 2.7.11. Además, hay algunos módulos de terceros. Para obtener una lista detallada, puedes ejecutar el script `PCbuild\get_externals.bat` en el directorio de código fuente de Python para obtener todos los módulos necesarios para compilar. Ten en cuenta que debes tener instalado SVN y agregar svn.exe a la variable de entorno PATH del sistema.

Descargar puede ser inestable y todo el proceso podría finalizar debido a problemas de red, por lo tanto, es recomendable descargar directamente el directorio externals desde mi github: [Mi versión de Python](https://github.com/disenone/wpython-2.7.11/tree/e13f43a3b72ae2bdf4d2950c6364750ae668cbf4/externals)

##El proceso de compilación

###**第三方模块**

Los módulos de terceros

Para comenzar, debemos resolver el problema de los módulos de terceros, especialmente tcl, tk y tcltk.

Modificar el archivo `externals/tcl-8.5.15.0/win/makefile.vc`, cambiar la línea 434 a 

	- cdebug = -Zi -WX $(DEBUGFLAGS)
	+ cdebug = -Zi -WX- $(DEBUGFLAGS)

En cuanto a la opción `WX`, puedes consultar la documentación oficial de Microsoft: [/WX (Tratar las advertencias del enlazador como errores)](https://msdn.microsoft.com/en-us/library/ms235592.aspx)

A continuación, modifica `PCbuild/tk.vcxproj` abriendo el archivo en un editor de texto y cambia las líneas 63 y 64.

	- <TkOpts>msvcrt</TkOpts>
	- <TkOpts Condition="$(Configuration) == 'Debug'">symbols,msvcrt</TkOpts>
	+ <TkOpts>msvcrt,noxp</TkOpts>
	+ <TkOpts Condition="$(Configuration) == 'Debug'">symbols,msvcrt,noxp</TkOpts>

Cambiar `PCbuild/tcltk.props`, ábrelo con un editor de texto y modifica la línea 41.

	- <BuildDirTop>$(BuildDirTop)_VC9</BuildDirTop>
	+ <BuildDirTop>$(BuildDirTop)_VC13</BuildDirTop>

Debido a que VS2015 ha eliminado la definición de `timezone` y lo ha reemplazado por `_timezone`, todos los lugares en el código donde se utiliza `timezone` deben cambiar a `_timezone`. Para los módulos de terceros, solo es necesario modificar el archivo `externals/tcl-8.5.15.0/win/tclWinTime.c`, y al inicio del archivo, agregar lo siguiente:

	#if defined _MSC_VER && _MSC_VER >= 1900
	#define timezone _timezone
	#endif

###**改 Python 源码**

El problema de `timezone` también está presente en el módulo `time` de Python. Por favor, modifica la línea 767.

	- #ifdef __CYGWIN__
	+ #if defined(__CYGWIN__) || defined(_MSC_VER) && _MSC_VER >= 1900

Además, debido a que en Windows Python utiliza un método especial para verificar la validez del descriptor de archivo, y este método ha sido completamente prohibido en VS2015, se producirán errores de compilación, por lo que es mejor cambiarlo primero. En el archivo `Include/fileobject.h`, líneas 73 y 80:

	73 - #if defined _MSC_VER && _MSC_VER >= 1400
	73 + #if defined _MSC_VER && _MSC_VER >= 1400 && _MSC_VER < 1900

	80 - #elif defined _MSC_VER && _MSC_VER >= 1200
	80 + #elif defined _MSC_VER && _MSC_VER >= 1200 && _MSC_VER < 1400

Archivo `Modules/posixmodule.c`, línea 532:

	- #if defined _MSC_VER && _MSC_VER >= 1400
	+ #if defined _MSC_VER && _MSC_VER >= 1400 && _MSC_VER < 1900

Hasta aquí, Python se puede compilar correctamente. Puedes ver los cambios más específicos en el contenido de mi confirmación: [modificar la compilación con vs2015](https://github.com/disenone/wpython-2.7.11/commit/4037e2d806518dbf06ffb8ee5c46f419ef8d7edf)


###**检查无效句柄** -> **Verificar el identificador inválido**

Aunque la compilación haya sido exitosa, el resultado directo de ignorar bruscamente los identificadores de archivos inválidos es que una vez que se accede a un identificador inválido (por ejemplo, cerrar el mismo archivo dos veces), Python fallará directamente con un fallo de aserción y el programa se bloqueará. Así que Python simplemente no puede ser utilizado de esta manera. Python utiliza una metodología especial para evitar esta situación, pero desafortunadamente no se puede utilizar en VS2015. La explicación se encuentra en los comentarios.

	Microsoft CRT in VS2005 and higher will verify that a filehandle is valid and raise an assertion if it isn't.


Afortunadamente, ya existe una solución para esto. La vi en los problemas de Python, aquí está el enlace: [issue23524](http://psf.upfronthosting.co.za/roundup/tracker/issue23524), [issue25759](http://psf.upfronthosting.co.za/roundup/tracker/issue25759)Este método también es utilizado en Python 3.x actualmente.


Para desactivar el mecanismo de assert crash de Windows al utilizar un identificador de archivo, en lugar de eso, revisa el código de error. ¿Cómo se puede desactivar el mecanismo de assert de Windows? La respuesta es reemplazar la función de manejo de errores predeterminada de Windows con tu propia función de manejo de errores. Aquí tienes el código clave:



Cree el archivo `PC/invalid_parameter_handler.c`, defina nuestra propia función de manejo de errores, que puede ignorar temporalmente los errores que ocurran.

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

Se definen dos macros para facilitar el cambio temporal de la función de manejo de errores, hay que tener en cuenta que el cambio es temporal y luego se debe volver a la configuración predeterminada del sistema.

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

Después, en los lugares donde sea posible desencadenar un error de handle de archivo de Windows, agrega el macro `_Py_BEGIN_SUPPRESS_IPH` antes y `_Py_END_SUPPRESS_IPH` después. Luego, simplemente verifica el código de error. Hay varios lugares que necesitan ser modificados, consulta el commit de otras personas para hacer las modificaciones.
\[Aquí\](https://github.com/kovidgoyal/cpython/commit/a9ec814d466d3c0139d10b69666f88eed10e4940)

##**结束**

Hasta este punto, Python 2.7.11 se puede compilar y ejecutar correctamente en VS2015. Sin embargo, Python oficialmente no recomienda esta configuración.

	***WARNING***
	Building Python 2.7 for Windows using any toolchain that doesn't link
	against MSVCRT90.dll is *unsupported* as the resulting python.exe will
	not be able to use precompiled extension modules that do link against
	MSVCRT90.dll.

Así que cuando lo uses, es mejor tener un poco de precaución.

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
