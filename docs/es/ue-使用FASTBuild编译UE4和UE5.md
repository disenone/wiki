---
layout: post
title: Utilizar FASTBuild para compilar UE4 y UE5
date: 2023-12-01
categories:
- c++
- python
catalog: true
tags:
- dev
- game
- ue
- UnreanEngine
description: La compatibilidad nativa de la UE con FASTBuild no es del todo completa.
  Para lograr una compatibilidad perfecta de FASTBuild con UE4 y UE5, es necesario
  realizar algunas configuraciones y modificaciones en el código fuente. A continuación,
  te explicaré paso a paso cómo hacerlo.
figures: []
---

<meta property="og:title" content="使用 FASTBuild 编译 UE4 和 UE5" />

> Este método de texto ha sido probado y es compatible con UE4.27 - UE5.3. No se ha probado en otras versiones, pero puedes intentarlo.

##**Introducción**

[FASTBuild](https://www.fastbuild.org/docs/home.html)FASTBuild es una herramienta de compilación distribuida de código abierto y gratuita. El proceso de compilación de UE puede ser bastante largo, pero al utilizar FASTBuild se puede reducir significativamente el tiempo de compilación.

UE a partir de la versión 4.x es capaz de soportar FASTBuild. El código fuente oficial incluye una versión modificada de la herramienta FASTBuild, basada en la versión 0.99 de FASTBuild. Se encuentra en la ubicación `Engine\Extras\ThirdPartyNotUE\FASTBuild`. UE5.3 también utiliza esta versión. Sin embargo, esta es una versión bastante antigua. Hasta la fecha de creación de este documento, la versión más reciente de FASTBuild es la 1.11, que cuenta con nuevas funcionalidades y correcciones de errores. Este documento se centra en cómo utilizar la versión 1.11 para admitir tanto UE4 como UE5.

##**Configuración sencilla**

Para lograr nuestro objetivo, necesitamos hacer algunas modificaciones en FASTBuild 1.11 y el código fuente de UE. Aquí, de hecho, ya he terminado de hacer las modificaciones, por lo que podemos usar directamente la versión que he modificado.

FASTBuild descarga la [última versión](https://github.com/disenone/fastbuild/releases)Los archivos ejecutables en el interior son FBuild.exe, FBuildCoordinator.exe y FBuildWorker.exe. Para mayor claridad, a continuación llamaremos "host local" a la máquina que utiliza FBuild.exe para programar, y "máquinas remotas" a aquellas que participan en la edición de la CPU.

###**本机配置**

Agrega el directorio donde se encuentra FBuild.exe al variable de entorno del sistema Path, para asegurarte de que puedas ejecutar FBuild.exe directamente desde la línea de comandos (cmd).

Configurar el directorio compartido de la caché (si no es necesario generar la caché, puedes omitir esta configuración): establecer un directorio vacío como ruta compartida y asegurarse de que la máquina remota tenga acceso a él.

Abre el proyecto de código fuente de UE4 / UE5 en esta máquina y modifica el archivo de configuración de compilación Engine\Saved\UnrealBuildTool\BuildConfiguration.xml de la siguiente manera:

```xml
<?xml version="1.0" encoding="utf-8" ?>
<Configuration xmlns="https://www.unrealengine.com/BuildConfiguration">
    <BuildConfiguration>
        <bAllowFASTBuild>true</bAllowFASTBuild>
    </BuildConfiguration>
    <FASTBuild>
		<bEnableDistribution>true</bEnableDistribution>
        <bEnableCaching>true</bEnableCaching>
        <FBuildCachePath>\\127.0.0.1\Cache\</FBuildCachePath>
        <FBuildCoordinator>127.0.0.1</FBuildCoordinator>
    </FASTBuild>
</Configuration>
```

Descargar FBuildCoordinator.exe antes de ejecutarlo en esta máquina.

###Remote machine configuration

Al configurar la caché de la misma manera, solo se debe especificar la dirección IP de la máquina local, supongamos que es 192.168.1.100

- FASTBUILD_CACHE_PATH: \\192.168.1.100\Cache
- FASTBUILD_CACHE_MODE: rw

`同样配置 Coordinator ip`
 
`同样配置 Coordinator ip` se traduce al español como: `Configuración de la IP del coordinador igual`

- FASTBUILD_COORDINATOR: 192.168.1.100

**配置完如下图**

Traducción: 

Después de configurar, el resultado se muestra en la siguiente imagen:

![](assets/img/2023-ue-fastbuild/remote_vars.png)

Ejecute FBuildWorker.exe en la máquina remota. Si la configuración es exitosa, se imprimirá un registro en FBuildCoordinator.exe de esta máquina local (donde 192.168.1.101 es la dirección IP de la máquina remota):

```
FBuildCoordinator - v1.11-UE
[2023-12-01-20:06:38] Listening on port 31392
[2023-12-01-20:06:38] current [0] workers: []
[2023-12-01-20:06:42] New worker available: 192.168.1.101
[2023-12-01-20:06:42] current [1] workers: [192.168.1.101]
```

###**测试 UE 编译**

Prueba de compilación de UE.

Usa VisualStudio para abrir el proyecto de código fuente de UE, selecciona un proyecto de C++, haz clic en Rebuild. Si la configuración es correcta, podrás ver registros similares a los que se muestran a continuación:

```
11>FBuild Command Line Arguments: '-monitor -summary -dist -cache -ide -j12 -clean -config "E:\UE\ue5.3_git\Engine\Intermediate\Build\fbuild.bff" -nostoponerror
11>FBuild Executable: 'd:\libs\FASTBuild\bin\FBuild.exe
11>FBuild Coordinator: '127.0.0.1
11>FBuild BrokeragePath: '\\127.0.0.1\Brokerage\
11>FBuild CachePath: '\\127.0.0.1\Cache\
11>BFF file 'E:\UE\ue5.3_git\Engine\Intermediate\Build\fbuild.bff' has changed (reparsing will occur).
11>Using Coordinator: 127.0.0.1
11>Requesting worker list from Corrdinator
11>Get Worker List from Coordinator.
11>2 workers in payload: [192.168.1.101]
11>Worker list received: 1 workers
11>Distributed Compilation : 1 Workers in pool '127.0.0.1'
```

FASTBuild puede encontrar la dirección IP de la máquina remota y comenzar a enviar la compilación a esa máquina remota. También se puede ver en el FBuildWorker de la máquina remota que hay una tarea de compilación en curso.

#### **Configuración avanzada**

###Apoyo a versiones más antiguas de UE

Si te das cuenta de que tu UE no tiene la herramienta FASTBuild (Engine\Extras\ThirdPartyNotUE\FASTBuild), y en el proyecto UnrealBuildTool no hay un archivo FASTBuild.cs, es muy probable que tu versión de UE aún no sea compatible con FASTBuild.

Entonces necesitarás consultar el código fuente de UE4.27, y también crear un FASTBuild.cs similar, además de realizar las modificaciones pertinentes en el resto del código relacionado. No detallaremos aquí los cambios específicos.


###Compilando tu propio FASTBuild

Si estás interesado en FASTBuild en sí mismo, o si quieres hacer algunas modificaciones, puedes intentar compilar FASTBuild con FASTBuild.

- Descarga mi [último código fuente](https://github.com/disenone/fastbuild/releases)Con el fin de lograr lo que estás buscando, sería necesario contar con más contexto o información para garantizar una traducción precisa. "并解压" parece ser una combinación de dos palabras en chino que no tienen un significado claro por sí mismas. Por favor, proporciónanos más detalles para que podamos ayudarte de la manera más adecuada posible.
- Modificar External\SDK\VisualStudio\VS2019.bff, cambiar .VS2019_BasePath y .VS2019_Version por el contenido correspondiente a tu máquina local. Puedes encontrar la versión en el directorio .VS2019_BasePath\Tools\MSVC, por ejemplo:
    ```
    .VS2019_BasePath        = 'C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC'    // <-- Set path here
    .VS2019_Version         = '14.29.30133' // <-- Set version here
    .VS2019_MSC_VER         = '1929' // <-- Set MSC_VER here
    ```

- Modifica el archivo .bff de External\SDK\Windows\Windows10SDK, en los campos .Windows10_SDKBasePath y .Windows10_SDKVersion. Puedes ver la versión en la carpeta .Windows10_SDKBasePath/bin.
    ```
    .Windows10_SDKBasePath        = 'C:\Program Files (x86)\Windows Kits/10'    // <-- Set path here
    .Windows10_SDKVersion         = '10.0.19041.0' // <-- Set version here
    ```

Modifica el archivo External\SDK\Clang\Windows\Clang11.bff, cambiando los valores de .Clang11_BasePath y .Clang11_Version. La ruta se encuentra en .VS2019_BasePath\Tools\Tools/LLVM/x64.
    ```
    .Clang11_BasePath = 'C:/Program Files (x86)/Microsoft Visual Studio/2019/Professional/VC/Tools/LLVM/x64'    // <-- Set path here
    .Clang11_Version  = '12.x.x'
    ```

- Entra en el directorio Code y ejecuta `FBuild.exe All-x64-Release` en el cmd. Si la configuración es correcta, deberías ver la compilación exitosa. En la ruta tmp\x64-Release\Tools\FBuild\FBuild podrás encontrar el archivo FBuild.exe.

`FBuild.exe All-x64-Release -dist -coordinator=127.0.0.1` permite activar la compilación distribuida.

###**FBuild Más opciones**

**我提供的 FBuild 本身支持以下常用的选项：**

El FBuild que ofrezco en sí mismo admite las siguientes opciones comunes:

- coordinator: Especifica la dirección IP del coordinador (puede sobrescribir el valor de la variable de entorno del sistema)
- brokerage: dirección de intermediación designada (puede sobrescribir el valor de las variables de entorno del sistema)
- nocache: Obliga a no usar caché.
- dist: Activar compilación distribuida.
- forceremote: Compilar de forma remota
- summary: Generar informe de estadísticas después de finalizar la edición.

Espera un momento, puedes ejecutar `FBuild.exe -help` para ver más opciones.

FBuildWorker tiene varias opciones comunes:

- coordinator: Especifica la dirección IP del coordinador (puede sobrescribir el valor de la variable de entorno del sistema)
- brokerage: dirección de intermediación designada (puede anular el valor de las variables de entorno del sistema)
- nocache:  Obliga a no utilizar la memoria caché.
- cpus: Especifica cuántos núcleos se utilizarán para la compilación.

Más opciones están disponibles al ejecutar `FBuildWorder.exe -help`.

###Modifica el archivo FASTBuild.cs incorporado en la UE.

El archivo FASTBuild.cs incluido en UE no maneja adecuadamente las variables de entorno del sistema en relación con los parámetros especificados en BuildConfiguration.xml. Muchos de los parámetros leen primero las variables de entorno del sistema, lo cual claramente es contrario a la lógica de uso de BuildConfiguration.xml.

Para ello, puedes modificar el código relevante de la siguiente manera, utilizando como ejemplo UE5.3:

```csharp
private bool ExecuteBffFile(string BffFilePath, ILogger Logger)
{
    string CacheArgument = "";

    if (bEnableCaching)
    {
        switch (CacheMode)
        {
            case FASTBuildCacheMode.ReadOnly:
                CacheArgument = "-cacheread";
                break;
            case FASTBuildCacheMode.WriteOnly:
                CacheArgument = "-cachewrite";
                break;
            case FASTBuildCacheMode.ReadWrite:
                CacheArgument = "-cache";
                break;
        }
    }
    else
    {
        CacheArgument = "-nocache";
    }

    string DistArgument = bEnableDistribution ? "-dist" : "";
    string ForceRemoteArgument = bForceRemote ? "-forceremote" : "";
    string NoStopOnErrorArgument = bStopOnError ? "" : "-nostoponerror";
    string IDEArgument = IsApple() ? "" : "-ide";
    string MaxProcesses = "-j" + ((ParallelExecutor)LocalExecutor).NumParallelProcesses;

    // Interesting flags for FASTBuild:
    // -nostoponerror, -verbose, -monitor (if FASTBuild Monitor Visual Studio Extension is installed!)
    // Yassine: The -clean is to bypass the FASTBuild internal
    // dependencies checks (cached in the fdb) as it could create some conflicts with UBT.
    // Basically we want FB to stupidly compile what UBT tells it to.
    string FBCommandLine = $"-monitor -summary {DistArgument} {CacheArgument} {IDEArgument} {MaxProcesses} -clean -config \"{BffFilePath}\" {NoStopOnErrorArgument} {ForceRemoteArgument}";

    Logger.LogInformation("FBuild Command Line Arguments: '{FBCommandLine}", FBCommandLine);

    string FBExecutable = GetExecutablePath()!;
    Logger.LogInformation("FBuild Executable: '{FBExecutable}", FBExecutable);

    string WorkingDirectory = Path.GetFullPath(Path.Combine(Unreal.EngineDirectory.MakeRelativeTo(DirectoryReference.GetCurrentDirectory()), "Source"));

    ProcessStartInfo FBStartInfo = new ProcessStartInfo(FBExecutable, FBCommandLine);
    FBStartInfo.UseShellExecute = false;
    FBStartInfo.WorkingDirectory = WorkingDirectory;
    FBStartInfo.RedirectStandardError = true;
    FBStartInfo.RedirectStandardOutput = true;

    string? Coordinator = GetCoordinator();
    if (!String.IsNullOrEmpty(Coordinator))
    {
        Logger.LogInformation("FBuild Coordinator: '{Coordinator}", Coordinator);
        FBStartInfo.EnvironmentVariables["FASTBUILD_COORDINATOR"] = Coordinator;
    }

    string? BrokeragePath = GetBrokeragePath();
    if (!String.IsNullOrEmpty(BrokeragePath))
    {
        Logger.LogInformation("FBuild BrokeragePath: '{BrokeragePath}", BrokeragePath);
        FBStartInfo.EnvironmentVariables["FASTBUILD_BROKERAGE_PATH"] = BrokeragePath;
    }

    string? CachePath = GetCachePath();
    if (!String.IsNullOrEmpty(CachePath))
    {
        Logger.LogInformation("FBuild CachePath: '{CachePath}", CachePath);
        FBStartInfo.EnvironmentVariables["FASTBUILD_CACHE_PATH"] = CachePath;
    }
...
```

###BuildConfiguration.xml Configuración avanzada

```xml
<?xml version="1.0" encoding="utf-8" ?>
<Configuration xmlns="https://www.unrealengine.com/BuildConfiguration">
    <ProjectFileGenerator>
<!-- Especificar la versión de Visual Studio -->
        <Format>VisualStudio2022</Format>
    </ProjectFileGenerator>
    <BuildConfiguration>
        <!-- Activar FASTBuild -->
        <bAllowFASTBuild>true</bAllowFASTBuild>
<!-- Especifica el número de núcleos de CPU que deben participar en la compilación en esta máquina -->
        <MaxParallelActions>12</MaxParallelActions>
        <!-- Cerrar Incredibuild -->
        <bAllowXGE>false</bAllowXGE>
    </BuildConfiguration>
    <FASTBuild>
<!-- Especificar la ruta de FBuild -->
        <FBuildExecutablePath>d:\libs\FASTBuild\bin\FBuild.exe</FBuildExecutablePath>
        <!-- Iniciar la compilación distribuida -->
        <bEnableDistribution>true</bEnableDistribution>
<!-- Especifica la ruta del broker -->
        <FBuildBrokeragePath>\\127.0.0.1\Brokerage\</FBuildBrokeragePath>
<!-- Especifica la ruta de la caché -->
        <FBuildCachePath>\\127.0.0.1\Cache\</FBuildCachePath>
        <!-- Activar caché -->
        <bEnableCaching>true</bEnableCaching>
        <!-- permisos de lectura y escritura de cache Leer/Escribir/Leer y Escribir -->
        <CacheMode>ReadWrite</CacheMode>
<!-- Especificar la IP del coordinador -->
        <FBuildCoordinator>127.0.0.1</FBuildCoordinator>
        <!-- Forzar compilación remota -->
        <!-- <bForceRemote>true</bForceRemote> -->
    </FASTBuild>
</Configuration>
```

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
