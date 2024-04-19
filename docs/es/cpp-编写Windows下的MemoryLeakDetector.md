---
layout: post
title: Escribir un Detector de Fugas de Memoria para Windows.
categories:
- c++
tags:
- dev
description: (https://vld.codeplex.com/)Este herramienta funciona reemplazando las
  interfaces dll responsables de la gestión de memoria en Windows para rastrear la
  asignación y liberación de memoria. Por lo tanto, he decidido hacer una herramienta
  sencilla de detección de fugas de memoria basada en Visual Leak Detector (VLD en
  adelante) para comprender la enlace con las dll.
figures:
- assets/post_assets/2016-6-11-memory-leak-detector/depends.png
---

<meta property="og:title" content="编写 Windows 下的 Memory Leak Detector" />

![](https://img.shields.io/badge/windows-10-blue.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}

#### Prefacio

Esta vez he terminado de leer "El autodesarrollo del programador: enlace, carga y biblioteca" (a partir de ahora abreviado como "Enlace"). He aprendido mucho y estoy pensando en hacer algunos códigos pequeños relacionados. Justo tengo conocimiento de una herramienta de detección de pérdida de memoria en Windows llamada [Visual Leak Detector](https://vld.codeplex.com/), esta herramienta realiza el seguimiento de la asignación y liberación de memoria al reemplazar las interfaces del dll responsables de la gestión de memoria en Windows. Por lo tanto, decidí basarme en Visual Leak Detector (abreviado como VLD) para crear una herramienta sencilla de detección de fugas de memoria, entendiendo la conexión con dll.

#### Preparación previa


El libro "Linking" explica detalladamente los principios de enlace de los archivos ejecutables en Linux y Windows, donde el formato de archivo ejecutable en Windows se conoce como PE (Portable Executable). La explicación de los archivos DLL es la siguiente:

> DLL es la abreviatura de Dynamic-Link Library, que es el equivalente de los objetos compartidos en Linux. En el sistema operativo Windows, se utiliza ampliamente el mecanismo de las DLL, incluso la estructura del núcleo de Windows depende en gran medida de las DLL. Los archivos DLL y los archivos EXE en Windows son conceptos similares: ambos son archivos binarios con formato PE. La diferencia radica en que el encabezado del archivo PE tiene un bit de símbolo que indica si el archivo es un EXE o una DLL. El nombre de extensión de un archivo DLL no necesariamente es .dll, también puede ser .ocx (control OCX) o .CPL (programa del Panel de control), u otro.

También hay archivos de extensión de Python, como .pyd. Y en las DLL, el concepto de detección de fugas de memoria aquí se llama **tabla de exportación e importación de símbolos**.

####Tabla de exportación de símbolos

> Cuando un archivo PE necesita proporcionar algunas funciones o variables para ser utilizadas por otros archivos PE, llamamos a este comportamiento **exportación de símbolos (Symbol Exporting)**.

Para entenderlo de manera sencilla, en Windows PE, todos los símbolos exportados se almacenan en una estructura llamada "tabla de exportación" (Export Table), que proporciona una relación de mapeo entre el nombre del símbolo y su dirección. Los símbolos que se deseen exportar deben ser marcados con el modificador `__declspec(dllexport)`.

####**符号导入表**.

La tabla de importación de símbolos es un concepto clave aquí, que se corresponde con la tabla de exportación de símbolos. Veamos primero la explicación del concepto:

> Si en un programa utilizamos funciones o variables provenientes de una DLL, a esto se le llama **importación de símbolos (Symbol Importing)**.

Windows PE guarda la información sobre los símbolos de las variables y funciones que necesita importar, así como la información sobre el módulo al que pertenecen en una estructura llamada **Tabla de Importación (Import Table)**. Al cargar un archivo PE en Windows, una de las tareas es determinar las direcciones de todas las funciones que deben importarse y ajustar los elementos de la tabla de importación a las direcciones correctas. Esto permite que, durante la ejecución del programa, se consulte la tabla de importación para ubicar las direcciones reales de las funciones y realizar las llamadas correspondientes. La estructura más importante en la tabla de importación es la **Tabla de Direcciones de Importación (Import Address Table, IAT)**, donde se almacenan las direcciones reales de las funciones importadas.

Visto hasta aquí, ¿no te has dado cuenta de cómo vamos a realizar la detección de fugas de memoria? :) Sí, es mediante un hack en la tabla de importación, específicamente modificando las direcciones de las funciones de asignación y liberación de memoria en la tabla de importación de los módulos que deseamos analizar, reemplazándolas por nuestras propias funciones personalizadas. Así, podremos conocer el estado de asignación y liberación de memoria de cada instancia del módulo y realizar las pruebas de detección que deseemos.

Puedes encontrar más información detallada sobre la vinculación de DLL en el libro "Enlace" o en otros recursos.

## Memory Leak Detector

Una vez que se comprende el principio, a continuación se procederá a implementar la detección de fuga de memoria basándose en dicho principio. La explicación que sigue se basará en mi propia implementación, la cual está disponible en mi repositorio de Github: [LeakDetector](https://github.com/disenone/LeakDetector)¡Hola! Parece que solo escribiste un punto en tu texto. ¿Hay algo más que te gustaría traducir o podemos ayudarte con algo más? Estamos aquí para ayudarte en lo que necesites. ¡Gracias!

####`替换函数` traducido al español es `Función de reemplazo`.

Primero, veamos la función clave, ubicada en [RealDetector.cpp](https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp):

```cpp linenums="1"
/* Reemplazar una función específica de la IAT (Import Address Table) en importModule por otra función,
* importModule will call the function of another module, and this function is the one that needs to be patched.
Lo que debemos hacer es cambiar `import module` por llamar a nuestra función personalizada.
 *
 * - importModule (IN): El módulo que se debe procesar, este módulo llama a funciones de otros módulos que necesitan ser modificadas.
 *
* - exportModuleName (IN): El nombre del módulo del cual se necesita parchear la función.
 *
* - exportModulePath (IN): La ruta donde se encuentra el módulo exportado. Se intentará cargar el módulo exportado utilizando la ruta proporcionada.

* Si falla, carga usando name
 * - importName (IN): Nombre de la función
 *
* - reemplazo (IN): puntero a una función reemplazante
 *
* Valor de retorno: verdadero si es exitoso, de lo contrario falso
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

Vamos a analizar esta función, como se describe en el comentario, su función es cambiar la dirección de una determinada función en la IAT por la dirección de otra función. Veamos las líneas 34-35:

``` cpp
idte = (IMAGE_IMPORT_DESCRIPTOR*)ImageDirectoryEntryToDataEx((PVOID)importModule, 
	TRUE, IMAGE_DIRECTORY_ENTRY_IMPORT, &size, &section);
```

La función `ImageDirectoryEntryToDataEx` puede devolver la dirección de una estructura específica en la cabecera de archivos de un módulo. `IMAGE_DIRECTORY_ENTRY_IMPORT` especifica la estructura de la tabla de importación, por lo que el valor devuelto `idte` apunta a la tabla de importación del módulo.

36-40 líneas para verificar la validez de `idte`. En la línea 41, `idte->FirstThunk` apunta a la IAT real. Por lo tanto, las líneas 41-48 se utilizan para buscar el módulo que contiene las funciones que deben ser reemplazadas según su nombre. Si no se encuentra, significa que no se está llamando a ninguna función de ese módulo, por lo que se mostrará un mensaje de error y se retornará.

Después de encontrar el módulo, naturalmente, necesitamos encontrar la función que se va a reemplazar. En las líneas 55-62 se abre el módulo al que pertenece la función, y en la línea 64 se localiza la dirección de la función. Debido a que la IAT no guarda el nombre, es necesario ubicar la función primero según su dirección original, para luego modificar esa dirección en las líneas 68-80. Una vez que se ha encontrado la función con éxito, simplemente se modifica la dirección por la dirección de `replacement`.

Hasta aquí, hemos reemplazado exitosamente la función en IAT.

####**模块和函数名字**

Traducción al español:

**Nombres de módulos y funciones**

Aunque ya hemos logrado reemplazar la función IAT `patchImport`, esta función requiere especificar el nombre del módulo y la función. ¿Entonces cómo sabemos qué módulo y función se utilizan para la asignación y liberación de memoria del programa? Para resolver este problema, necesitamos utilizar la herramienta [Dependency Walker](http://www.dependencywalker.com/). En Visual Studio, crea un nuevo proyecto y utiliza `new` en la función `main` para solicitar memoria. Compila la versión de depuración y luego utiliza `depends.exe` para abrir el archivo ejecutable generado. Podrás ver una interfaz similar a la siguiente (en mi proyecto [LeakDetectorTest](https://github.com/disenone/LeakDetector/tree/master/LeakDetectorTest)Para ilustrar):


![](assets/img/2016-6-11-memory-leak-detector/depends.png)

Se puede ver que LeakDetectorTest.exe utiliza las funciones `malloc` y `_free_dbg` del archivo uscrtbased.dll (que no se muestra en la imagen). Estas dos funciones son las que necesitamos reemplazar. Ten en cuenta que los nombres reales de las funciones pueden depender de tu versión de Windows y Visual Studio. En mi caso, tengo Windows 10 y Visual Studio 2015, así que lo que necesitas hacer es usar depends.exe para verificar qué funciones se están llamando en realidad.

####**分析调用栈**

El análisis de una pila de llamadas.

Para registrar la asignación de memoria, es necesario registrar la información de la pila de llamadas en ese momento. Aquí no tengo la intención de explicar en detalle cómo obtener la información actual de la pila de llamadas en Windows. La función relacionada es `RtlCaptureStackBackTrace`, hay mucha información relacionada en Internet, también puede revisar la función [`printTrace`](https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp).

####**检测内存泄露**

"Investigación de fugas de memoria"

Hasta aquí, hemos recolectado todas las Esferas del Dragón, ahora es hora de invocar formalmente al Dragón Shenlong.

我 quiero poder detectar fugas de memoria de forma local (esto es diferente a VLD, que realiza una detección global y admite múltiples hilos). Por lo tanto, envolví la clase "RealDetector" que realiza la sustitución de funciones en una capa adicional llamada "LeakDetector" y expuse la interfaz de "LeakDetector" al usuario. Para utilizarlo, sólo necesitas construir un "LeakDetector", con esto se completará la sustitución de funciones y comenzará la detección de fugas de memoria. Cuando el "LeakDetector" se destruye, se restauran las funciones originales, se interrumpe la detección de fugas de memoria y se imprime el resultado de la detección.

print("Hola Mundo!")

Este es un código simple en Python para imprimir "Hola Mundo". Puedes probarlo copiando el código y ejecutándolo en tu ambiente de desarrollo de Python. ¡Espero que lo encuentres útil!

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

El código asignó directamente algo de memoria utilizando `new`, pero no la liberó antes de salir directamente. El resultado impreso por el programa es:

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

La aplicación ha identificado correctamente dos lugares donde se solicita memoria sin liberarla y ha imprimido toda la información de la pila de llamadas. Hasta aquí, se ha completado la funcionalidad que necesitábamos.

###**结语**

Cuando aún no entiendes las conexiones de programas, la carga de bibliotecas y las funciones de enlace compartido, es posible que te encuentres confundido sobre cómo encontrar las funciones de las bibliotecas compartidas, y mucho menos reemplazar las funciones de la biblioteca con nuestras propias funciones. Aquí se tomará como ejemplo la detección de pérdida de memoria para discutir cómo reemplazar las funciones de DLL de Windows. Para obtener una implementación más detallada, se puede consultar el código fuente de VLD.

Otra cosa que me gustaría mencionar es que "Programación Autodidacta: Enlaces, Cargas y Bibliotecas" es realmente un buen libro, sin ningún tipo de publicidad encubierta, solo pura admiración.

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
