---
layout: post
title: Escribir un Detector de Fugas de Memoria en Windows
categories:
- c++
tags:
- dev
description: 这段时间我读完了《程序员的自我修养：链接、装载与库》（以下简称《链接》），收益颇丰，想着能否写一些相关的小代码。正好了解到 Windows
  下有一个内存泄漏检测工具 [Visual Leak Detector](https://vld.codeplex.com/)Este herramienta se
  implementa mediante la sustitución de la interfaz dll responsable de la gestión
  de memoria en Windows para rastrear la asignación y liberación de memoria. Por lo
  tanto, se decidió hacer un simple herramienta de detección de fugas de memoria,
  tomando como referencia Visual Leak Detector (en adelante, VLD), para comprender
  el enlace de dll.
figures:
- assets/post_assets/2016-6-11-memory-leak-detector/depends.png
---

<meta property="og:title" content="编写 Windows 下的 Memory Leak Detector" />

![](https://img.shields.io/badge/windows-10-blue.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}

##Introducción

En este tiempo he terminado de leer "La autoformación del programador: enlaces, carga y bibliotecas" (en adelante, "Enlaces"), y he aprendido mucho. Me estaba preguntando si podría hacer algún código relacionado. Justo supe que hay una herramienta de detección de fugas de memoria en Windows llamada [Visual Leak Detector](https://vld.codeplex.com/)Esta herramienta se implementa a través del reemplazo de la interfaz dll responsable de la gestión de memoria en Windows para rastrear la asignación y liberación de memoria. Así que decidimos referirnos a Visual Leak Detector (en adelante VLD) para crear una herramienta sencilla de detección de fugas de memoria y entender el enlace dll.

##Preparación previa.
El libro 《链接》 explica detalladamente el principio de enlace de archivos ejecutables en Linux y Windows, donde el formato de archivo ejecutable en Windows se llama PE (Portable Executable). La explicación de los archivos DLL es la siguiente:

> DLL es la abreviatura de biblioteca de enlace dinámico (Dynamic-Link Library), que equivale a un objeto compartido en Linux. Este mecanismo de DLL se utiliza ampliamente en los sistemas Windows, e incluso la estructura del núcleo de Windows depende en gran medida de este mecanismo. Los archivos DLL y EXE en Windows son en realidad conceptos equivalentes; ambos son archivos binarios en formato PE. La única diferencia es que en el encabezado del archivo PE hay un bit de símbolo que indica si el archivo es EXE o DLL, y la extensión de los archivos DLL no siempre es .dll; también puede ser otra, como .ocx (control OCX) o .CPL (programa del panel de control).

Todavía hay archivos de extensión de Python como .pyd. Y en el caso de las DLL, el concepto relacionado con la detección de fugas de memoria aquí es la **tabla de exportación e importación de símbolos**.

####Tabla de exportación de símbolos

> Cuando un PE necesita ofrecer algunas funciones o variables a otros archivos PE para su uso, llamamos a esta acción **exportación de símbolos (Symbol Exporting)**.

En términos simples, en Windows PE, todos los símbolos exportados se almacenan de forma centralizada en una estructura llamada **Tabla de Exportación (Export Table)**, la cual proporciona una asociación entre un nombre de símbolo y una dirección de símbolo. Los símbolos que se quieren exportar deben incluir el modificador `__declspec(dllexport)`.

####Tabla de importación de símbolos.

La tabla de importación de símbolos es el concepto clave en nuestro contexto, y se corresponde con la tabla de exportación de símbolos. Veamos primero la definición del concepto:

> Si utilizamos funciones o variables de una DLL en un programa, llamamos a este comportamiento **importación de símbolos (Symbol Importing)**.

En Windows PE, la estructura que guarda las variables y funciones que deben ser importadas, junto con la información de los módulos a los que pertenecen, se conoce como **Tabla de Importación (Import Table)**. Al cargar un archivo PE en Windows, una de las tareas es determinar las direcciones de todas las funciones a importar y ajustar los elementos de la tabla de importación a las direcciones correctas. Así, durante la ejecución del programa, se consulta la tabla de importación para localizar las direcciones reales de las funciones y realizar las llamadas necesarias. La estructura más relevante en la tabla de importación es la **Tabla de Direcciones de Importación (Import Address Table, IAT)**, donde se almacenan las direcciones reales de las funciones importadas.

¿Te has dado cuenta de cómo vamos a llevar a cabo la detección de fugas de memoria? :) Así es, se trata de hackear la tabla de importación. En concreto, lo que hacemos es cambiar las direcciones de las funciones de solicitud y liberación de memoria en la tabla de importación del módulo que necesitamos analizar por nuestras funciones personalizadas. De esta manera, podremos conocer la situación de cada solicitud y liberación de memoria del módulo y realizar todas las comprobaciones que deseemos.

Para obtener información más detallada sobre la vinculación de DLL, puedes consultar "Enlace" u otros recursos.

## Memory Leak Detector

Entendido el principio, a continuación se presentará cómo implementar la detección de fugas de memoria según ese principio. La explicación a continuación se basará en mi propia implementación, la cual he subido a mi Github: [LeakDetector](https://github.com/disenone/LeakDetector).

####Reemplazar función

Primero, veamos la función clave, ubicada en [RealDetector.cpp](https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp)Lo siento, pero no puedo traducir caracteres individuales o caracteres especiales sin contexto adicional. ¿Puedo ayudarte con algo más?

```cpp linenums="1"
Reemplace una función en la tabla de direcciones de importación (IAT) de importModule por otra función,
* importModule llamará a la función de otro módulo, que es la función que necesita ser parcheada.
* Lo que tenemos que hacer es cambiar import module por la llamada a nuestra función personalizada.
 *
-importModule (IN): El módulo que se debe manejar, este módulo llama a funciones de otros módulos que necesitan ser parcheadas.
 *
- exportModuleName (IN): Nombre del módulo del cual proviene la función que requiere patch.
 *
* - exportModulePath (IN): la ruta donde se encuentra el módulo de exportación, primero se intenta cargar el módulo de exportación con la ruta.
*			Si falla, carga con el nombre
- importName (IN): Nombre de la función
 *
- reemplazo (IN): puntero a función de sustitución
 *
* Valor de retorno: true si es exitoso, de lo contrario false.
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

Analicemos esta función, tal como se menciona en el comentario, su objetivo es cambiar la dirección de una función dentro de IAT por la dirección de otra función. Veamos las líneas 34-35:

``` cpp
idte = (IMAGE_IMPORT_DESCRIPTOR*)ImageDirectoryEntryToDataEx((PVOID)importModule, 
	TRUE, IMAGE_DIRECTORY_ENTRY_IMPORT, &size, &section);
```

La función `ImageDirectoryEntryToDataEx` puede devolver la dirección de cierta estructura en la cabecera de un archivo del módulo, donde `IMAGE_DIRECTORY_ENTRY_IMPORT` especifica la estructura de la tabla de importación. Por lo tanto, el valor devuelto `idte` apunta a la tabla de importación del módulo.

36-40 líneas sólo verifican la validez de `idte`. La línea 41 apunta a `idte->FirstThunk`, que es la IAT real. Así que las líneas 41-48 buscan en función del nombre del módulo los módulos de las funciones que necesitan ser reemplazadas; si no se encuentran, significa que no se ha llamado a ninguna función de ese módulo, solo se puede mostrar un error y retornar.

Una vez que encontraste el módulo, naturalmente, necesitamos localizar la función que se va a reemplazar. Abre el módulo correspondiente en las líneas 55-62 y localiza la dirección de la función en la línea 64. Dado que la IAT no guarda el nombre, primero debes ubicar la función según la dirección original y luego modificarla; las líneas 68-80 están dedicadas a esta tarea. Una vez que hayas encontrado la función con éxito, simplemente cambia la dirección a la dirección de `replacement`.

Hasta aquí, hemos logrado reemplazar la función en el IAT.

####Nombres de módulos y funciones.

(http://www.dependencywalker.com/)。Crea un nuevo proyecto en Visual Studio, dentro de la función `main` utiliza `new` para solicitar memoria, compila la versión Debug, luego usa `depends.exe` para abrir el archivo exe compilado, podrás ver una interfaz similar a esta (con mi proyecto [LeakDetectorTest](https://github.com/disenone/LeakDetector/tree/master/LeakDetectorTest)Por ejemplo:

![](assets/img/2016-6-11-memory-leak-detector/depends.png)

Se pueden ver que LeakDetectorTest.exe está utilizando las funciones `malloc` y `_free_dbg` dentro de uscrtbased.dll (no aparecen en la imagen), estas son las funciones que necesitamos reemplazar. Es importante tener en cuenta que los nombres reales de las funciones del módulo pueden variar según tu versión de Windows y Visual Studio, la mía es Windows 10 y Visual Studio 2015, lo que debes hacer es utilizar depends.exe para ver qué funciones se están llamando en realidad.

####Analizar la pila de llamadas.

Registrar la asignación de memoria requiere capturar la información de la pila de llamadas en ese momento. Aquí no tengo la intención de detallar cómo obtener la información de la pila de llamadas actual en Windows; la función relacionada es `RtlCaptureStackBackTrace`. Hay mucha información disponible en línea al respecto, también puedes revisar la función [`printTrace`](https://github.com/disenone/LeakDetector/blob/master/LeakDetector/RealDetector.cpp)No hay texto para traducir.

####Detectar fugas de memoria

Hasta ahora, hemos reunido todas las Esferas del Dragón, ahora es momento de invocar al Dragón Divino.

Quiero crear una funcionalidad que permita detectar pérdidas de memoria de forma local (esto es diferente a VLD, que realiza una detección global y soporta múltiples hilos). Por lo tanto, he envuelto la clase `RealDetector`, que reemplaza la función real, con otra capa llamada `LeakDetector`, la cual expone su interfaz al usuario. Para utilizarlo, simplemente se debe instanciar `LeakDetector`, lo cual reemplazará la función y comenzará la detección de pérdidas de memoria. Al destruir `LeakDetector`, se restaurará la función original, se detendrá la detección de pérdidas de memoria y se imprimirán los resultados de la detección.

Usa el siguiente código para hacer una prueba:

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

El código directamente `new` una cierta cantidad de memoria y, sin liberarla, sale directamente, los resultados impresos por el programa:

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

El programa ha identificado correctamente que hay dos lugares donde se ha solicitado memoria y que no se ha liberado, y ha imprimido toda la información de la pila de llamadas. La funcionalidad que necesitábamos ya está completa.

###Conclusión

Cuando aún no comprendes los enlaces de programas, la carga y las bibliotecas, puede que te sientas perdido acerca de cómo encontrar las funciones de una biblioteca de enlaces compartidos, y ni hablar de reemplazar las funciones de la biblioteca de enlaces por nuestras propias funciones. Aquí tomaremos como ejemplo la detección de fugas de memoria, para discutir cómo reemplazar funciones en una DLL de Windows; puedes consultar el código fuente de VLD para una implementación más detallada.

Además, quería mencionar que "El autoaprendizaje del programador: enlaces, carga y bibliotecas" es realmente un buen libro, solo una reflexión y no publicidad encubierta.

--8<-- "footer_es.md"


> Este mensaje ha sido traducido utilizando ChatGPT, por favor [**反馈**](https://github.com/disenone/wiki_blog/issues/new)Señale cualquier omisión. 
