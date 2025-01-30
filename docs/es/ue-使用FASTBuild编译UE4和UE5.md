---
layout: post
title: Uso de FASTBuild para compilar UE4 y UE5
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
description: UE 原生对 FASTBuild 支持不太完善, 为了让 UE4 和 UE5 完美支持 FASTBuild, 我们需要做一些配置和源码修改,
  下面为你一一道来.
figures: []
---

<meta property="og:title" content="使用 FASTBuild 编译 UE4 和 UE5" />

> Este método ha sido probado para ser compatible con UE4.27 - UE5.3, otras versiones no han sido probadas, puedes intentarlo.

##Introducción

[FASTBuild](https://www.fastbuild.org/docs/home.html)Se trata de una herramienta de compilación distribuida de código abierto y gratuita. La compilación en UE puede ser bastante lenta, pero si se utiliza FASTBuild, se puede reducir significativamente el tiempo de compilación.

UE ha podido admitir FASTBuild desde la versión 4.x, el código fuente oficial viene con una versión modificada de la herramienta FASTBuild, basada en la versión 0.99 de FASTBuild, ubicada en `Engine\Extras\ThirdPartyNotUE\FASTBuild`. UE5.3 también utiliza esta versión. Esta es una versión bastante antigua, ya que hasta la fecha de creación de este texto, la versión más reciente de FASTBuild es la 1.11, que ofrece más funciones nuevas y correcciones de errores. Este texto se centra en cómo utilizar la versión 1.11 para admitir tanto UE4 como UE5 al mismo tiempo.

##Configuración sencilla

Para lograr nuestros objetivos, necesitamos hacer algunas modificaciones en FASTBuild 1.11 y en el código fuente de UE. De hecho, ya he realizado todas las modificaciones aquí, por lo que podemos usar directamente la versión que he modificado.

Descarga la [última versión](https://github.com/disenone/fastbuild/releases)Los archivos ejecutables dentro son FBuild.exe, FBuildCoordinator.exe, FBuildWorker.exe. Para expresar con claridad, a la máquina que utiliza FBuild.exe para programar la llamaremos `máquina local`, y a las otras máquinas remotas que proporcionan CPU para participar en la edición las llamaremos `máquinas remotas`.

###Configuración de esta máquina

Agrega el directorio donde se encuentra FBuild.exe al entorno de variables de sistema Path, para asegurarte de que puedas ejecutar FBuild.exe directamente desde la ventana de comandos (cmd).

Configurar el directorio compartido de Cache (si no se necesita generar Cache, se puede omitir esta configuración): establecer un directorio vacío como ruta compartida y confirmar que la máquina remota pueda acceder.

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

Ejecutar el archivo FBuildCoordinator.exe descargado anteriormente en esta máquina.

###Configuración de máquina remota

La misma configuración de Cache, solo que la IP debe especificarse a la IP local, suponiendo aquí que sea 192.168.1.100.

- FASTBUILD_CACHE_PATH: \\192.168.1.100\Cache
- FASTBUILD_CACHE_MODE: rw

Configuración de Coordinador con la misma dirección IP.

- FASTBUILD_COORDINATOR: 192.168.1.100

La configuración es la siguiente:

![](assets/img/2023-ue-fastbuild/remote_vars.png)

Ejecuta FBuildWorker.exe en la máquina remota; si la configuración es exitosa, podrás ver que se imprimen registros en FBuildCoordinator.exe de esta máquina (aquí 192.168.1.101 es la dirección IP de la máquina remota):

```
FBuildCoordinator - v1.11-UE
[2023-12-01-20:06:38] Listening on port 31392
[2023-12-01-20:06:38] current [0] workers: []
[2023-12-01-20:06:42] New worker available: 192.168.1.101
[2023-12-01-20:06:42] current [1] workers: [192.168.1.101]
```

###Prueba de compilación de UE

Abre el proyecto de código fuente de Unreal Engine en Visual Studio, selecciona un proyecto de C++, y haz clic en Rebuild. Si la configuración es correcta, verás registros similares a los siguientes.

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

FASTBuild puede encontrar la IP de la máquina remota y comenzar a enviar compilaciones a la máquina remota. También se puede ver en el FBuildWorker de la máquina remota que hay tareas de compilación en ejecución.

##Configuración avanzada

###Soporte para versiones más antiguas de UE

Si descubres que tu UE no tiene la herramienta FASTBuild (Engine\Extras\ThirdPartyNotUE\FASTBuild) y que no hay un archivo FASTBuild.cs en el proyecto UnrealBuildTool, es muy probable que tu versión de UE aún no sea compatible con FASTBuild.

Necesitarás consultar el código fuente de UE4.27, y también crear un archivo FASTBuild.cs similar, además de realizar los cambios necesarios en otros códigos relacionados, pero no entraré en detalles aquí.


###Compilar tu propio FASTBuild

Si también estás interesado en FASTBuild o deseas hacer algunas modificaciones, puedes intentar compilar FASTBuild con FASTBuild.

- Descarga mi [último código fuente](https://github.com/disenone/fastbuild/releases)，并解压
- Modifica External\SDK\VisualStudio\VS2019.bff, cambiando .VS2019_BasePath y .VS2019_Version por el contenido correspondiente en tu máquina; la versión se puede ver en el directorio .VS2019_BasePath\Tools\MSVC, por ejemplo.
    ```
    .VS2019_BasePath        = 'C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC'    // <-- Set path here
    .VS2019_Version         = '14.29.30133' // <-- Set version here
    .VS2019_MSC_VER         = '1929' // <-- Set MSC_VER here
    ```

Por favor, traduce el siguiente texto al idioma español:

- Modify External\SDK\Windows\Windows10SDK.bff's .Windows10_SDKBasePath and .Windows10_SDKVersion, puedes encontrar la versión en .Windows10_SDKBasePath/bin:
    ```
    .Windows10_SDKBasePath        = 'C:\Program Files (x86)\Windows Kits/10'    // <-- Set path here
    .Windows10_SDKVersion         = '10.0.19041.0' // <-- Set version here
    ```

- Modificar el .Clang11_BasePath y .Clang11_Version en External\SDK\Clang\Windows\Clang11.bff, la ruta está en .VS2019_BasePath\Tools\Tools/LLVM/x64.
    ```
    .Clang11_BasePath = 'C:/Program Files (x86)/Microsoft Visual Studio/2019/Professional/VC/Tools/LLVM/x64'    // <-- Set path here
    .Clang11_Version  = '12.x.x'
    ```

- Accede al directorio de Code y ejecuta `FBuild.exe All-x64-Release` en cmd. Si la configuración es correcta, podrás ver que la compilación fue exitosa. En tmp\x64-Release\Tools\FBuild\FBuild podrás encontrar FBuild.exe.

`FBuild.exe All-x64-Release -dist -coordinator=127.0.0.1` can enable distributed compilation.

###FBuild Más opciones

El FBuild que proporciono soporta las siguientes opciones comunes:

- coordinator: Especificar la dirección IP del Coordinator (puede sobrescribir el valor de la variable de entorno del sistema)
- brokerage: dirección de corredor (brokerage) designada (puede sobrescribir el valor de las variables de entorno del sistema)
nocache: forcing to not use cache.
- dist: Activar la compilación distribuida
- forceremote：Forzar la compilación en el equipo remoto
- resumen: generar informe estadístico después de la edición

Espera, puedes ver más opciones ejecutando `FBuild.exe -help`.

Las opciones más comunes de FBuildWorker son:

- coordinador: Specifique la dirección IP del coordinador (puede cubrir los valores de las variables de entorno del sistema)
- brokerage: dirección de corretaje especificada (puede superponer el valor de las variables de entorno del sistema)
- nocache: forzar no usar caché
- cpus: Especifica cuántos núcleos se asignarán para la compilación.

Para ver más opciones, puedes ejecutar `FBuildWorder.exe -help`.

###Modificar el FASTBuild.cs incorporado de UE.

El FASTBuild.cs que viene con UE no maneja adecuadamente las variables de entorno del sistema y su relación con los parámetros especificados en BuildConfiguration.xml; muchos parámetros se leen prioritariamente desde las variables de entorno del sistema, lo cual es claramente opuesto a la lógica de uso de BuildConfiguration.xml.

Para ello, se puede modificar el código correspondiente de la siguiente manera, tomando como ejemplo UE5.3:

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

###BuildConfiguration.xml Configuración Avanzada

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
Indique el número de núcleos de CPU que participan en la compilación en esta máquina.
        <MaxParallelActions>12</MaxParallelActions>
<!-- Desactivar Incredibuild -->
        <bAllowXGE>false</bAllowXGE>
    </BuildConfiguration>
    <FASTBuild>
<!-- Especificar la ruta de FBuild -->
        <FBuildExecutablePath>d:\libs\FASTBuild\bin\FBuild.exe</FBuildExecutablePath>
<!-- Activar la compilación distribuida -->
        <bEnableDistribution>true</bEnableDistribution>
<!-- Especificar la ruta de brokerage -->
        <FBuildBrokeragePath>\\127.0.0.1\Brokerage\</FBuildBrokeragePath>
Por favor traduce este texto al español:

        <!-- Especificar la ruta de la caché -->
        <FBuildCachePath>\\127.0.0.1\Cache\</FBuildCachePath>
<!-- Activar caché -->
        <bEnableCaching>true</bEnableCaching>
<!-- permisos de lectura/escritura del caché Read/Write/ReadWrite -->
        <CacheMode>ReadWrite</CacheMode>
<!-- Especificar la ip del coordinador -->
        <FBuildCoordinator>127.0.0.1</FBuildCoordinator>
<!-- Forzar compilación remota -->
        <!-- <bForceRemote>true</bForceRemote> -->
    </FASTBuild>
</Configuration>
```

--8<-- "footer_es.md"


> Este post fue traducido usando ChatGPT, por favor en [**comentarios**](https://github.com/disenone/wiki_blog/issues/new)Señale cualquier omisión. 
