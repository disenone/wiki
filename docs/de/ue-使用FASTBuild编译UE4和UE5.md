---
layout: post
title: Kompilieren von UE4 und UE5 mit FASTBuild
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
description: Die nativen Unterstützung für FASTBuild in UE ist nicht optimal. Um sicherzustellen,
  dass UE4 und UE5 FASTBuild perfekt unterstützen, sind einige Konfigurationen und
  Quellcode-Änderungen erforderlich. Im Folgenden werde ich dies für dich erläutern.
figures: []
---

<meta property="og:title" content="使用 FASTBuild 编译 UE4 和 UE5" />

> Dieses Verfahren wurde getestet und unterstützt UE4.27 - UE5.3, andere Versionen wurden nicht getestet, aber können ausprobiert werden.

##Vorwort

[FASTBuild](https://www.fastbuild.org/docs/home.html)Es ist ein kostenloses Open-Source-Distributionskompilierungstool, UE selbst ist ziemlich zeitaufwändig zu kompilieren, aber wenn man FASTBuild verwendet, kann die Kompilierzeit erheblich reduziert werden.

UE unterstützt FASTBuild ab Version 4.x und enthält bereits eine modifizierte Version des Tools, basierend auf FASTBuild 0.99, im offiziellen Quellcode. Der Standort ist `Engine\Extras\ThirdPartyNotUE\FASTBuild`. Auch UE5.3 verwendet diese Version. Diese Version ist jedoch schon etwas älter. Zum Zeitpunkt der Erstellung dieses Textes ist die neueste offizielle FASTBuild-Version 1.11, die zusätzliche Funktionen und Fehlerbehebungen bietet. Dieser Text konzentriert sich darauf, wie man Version 1.11 verwendet, um sowohl UE4 als auch UE5 zu unterstützen.

##Einfache Konfiguration

Um das Ziel zu erreichen, müssen wir einige Änderungen am FASTBuild 1.11 und am UE-Quellcode vornehmen. Tatsächlich habe ich sie hier bereits alle geändert, so dass wir direkt die von mir modifizierte Version verwenden können.

Laden Sie die von mir eingereichte [neueste Version](https://github.com/disenone/fastbuild/releases)Die auszuführenden Dateien darin sind FBuild.exe, FBuildCoordinator.exe und FBuildWorker.exe. Um es klar auszudrücken, bezeichnen wir nachfolgend die Maschine, die FBuild.exe für die Programmierung verwendet, als „lokale Maschine“, und andere entfernte Maschinen, die an der Bearbeitung der CPU beteiligt sind, als „remote Maschine“.

###Die aktuelle Konfiguration dieses Gerätes.

Fügen Sie das Verzeichnis, in dem sich die Datei FBuild.exe befindet, der Systemumgebungsvariable Path hinzu, um sicherzustellen, dass FBuild.exe direkt in der Eingabeaufforderung ausgeführt werden kann.

Richten Sie das Cache-Freigabeverzeichnis ein (keine Konfiguration erforderlich, wenn kein Cache generiert werden soll): Legen Sie einen leeren Ordner als Freigabepfad fest und stellen Sie sicher, dass der Remote-Computer darauf zugreifen kann.

Öffnen Sie das Quellcode-Projekt von UE4 / UE5 auf diesem Gerät und ändern Sie die Build-Konfigurationsdatei Engine\Saved\UnrealBuildTool\BuildConfiguration.xml wie folgt:

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

Ausführen der zuvor heruntergeladenen FBuildCoordinator.exe auf diesem Computer.

###Remote Machine Configuration

Same configuration Cache, just IP needs to be set to the local IP, assumed here as 192.168.1.100.

- FASTBUILD_CACHE_PATH: \\192.168.1.100\Cache
- FASTBUILD_CACHE_MODE: rw

Gleiches Setup: Koordinator-IP

- FASTBUILD_COORDINATOR: 192.168.1.100

Die Konfiguration ist wie folgt abgeschlossen.

![](assets/img/2023-ue-fastbuild/remote_vars.png)

Führen Sie FBuildWorker.exe auf dem Remote-Computer aus. Wenn die Konfiguration erfolgreich ist, sollte im Lokalen-Computer die Protokolldatei von FBuildCoordinator.exe angezeigt werden (hier ist 192.168.1.101 die IP-Adresse des Remote-Computers):

```
FBuildCoordinator - v1.11-UE
[2023-12-01-20:06:38] Listening on port 31392
[2023-12-01-20:06:38] current [0] workers: []
[2023-12-01-20:06:42] New worker available: 192.168.1.101
[2023-12-01-20:06:42] current [1] workers: [192.168.1.101]
```

###Testen Sie die UE-Kompilierung.

Öffnen Sie das UE-Quellcodeprojekt sln in VisualStudio, wählen Sie ein C++-Projekt aus und klicken Sie auf "Rebuild". Wenn die Konfiguration korrekt ist, sollten Sie ähnliche Protokolle wie folgt sehen:

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

FASTBuild kann die IP-Adresse des Remote-Computers finden und mit dem Kompilieren auf dem entfernten Computer beginnen. Auf dem FBuildWorker des Remote-Computers kann ebenfalls gesehen werden, dass gerade ein Kompilierungsvorgang durchgeführt wird.

##Erweiterte Konfiguration

###Unterstützung für ältere Versionen von UE.

Wenn Sie feststellen, dass Ihr UE keine FASTBuild-Tool (Engine\Extras\ThirdPartyNotUE\FASTBuild) hat und im Projekt UnrealBuildTool keine FASTBuild.cs-Datei vorhanden ist, besteht eine hohe Wahrscheinlichkeit, dass Ihre UE-Version FASTBuild noch nicht unterstützt.

So, you need to refer to the source code of UE4.27, create a similar FASTBuild.cs, and make the necessary modifications to other related code. Further details are not provided here.


###Kompilieren Sie Ihr eigenes FASTBuild.

Wenn du auch an FASTBuild interessiert bist oder ein paar Änderungen vornehmen möchtest, kannst du versuchen, FASTBuild mit FASTBuild zu kompilieren.

Laden Sie meinen [neuesten Quellcode](https://github.com/disenone/fastbuild/releases)Und entpacken
Bitte ändern Sie External\SDK\VisualStudio\VS2019.bff, um .VS2019_BasePath und .VS2019_Version gemäß Ihres lokalen Systems anzupassen. Die Version kann im Verzeichnis .VS2019_BasePath\Tools\MSVC gefunden werden, zum Beispiel.
    ```
    .VS2019_BasePath        = 'C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC'    // <-- Set path here
    .VS2019_Version         = '14.29.30133' // <-- Set version here
    .VS2019_MSC_VER         = '1929' // <-- Set MSC_VER here
    ```

Ändern Sie die .Windows10_SDKBasePath und .Windows10_SDKVersion in External\SDK\Windows\Windows10SDK.bff. Die Version ist im .Windows10_SDKBasePath/bin Ordner zu finden.
    ```
    .Windows10_SDKBasePath        = 'C:\Program Files (x86)\Windows Kits/10'    // <-- Set path here
    .Windows10_SDKVersion         = '10.0.19041.0' // <-- Set version here
    ```

Bitte ändern Sie .Clang11_BasePath und .Clang11_Version in External\SDK\Clang\Windows\Clang11.bff, der Pfad befindet sich unter .VS2019_BasePath\Tools\Tools/LLVM/x64.
    ```
    .Clang11_BasePath = 'C:/Program Files (x86)/Microsoft Visual Studio/2019/Professional/VC/Tools/LLVM/x64'    // <-- Set path here
    .Clang11_Version  = '12.x.x'
    ```

Gehen Sie zum Code-Verzeichnis und führen Sie in cmd `FBuild.exe All-x64-Release` aus. Wenn die Konfiguration korrekt ist, sollte das erfolgreiche Kompilieren angezeigt werden. Unter tmp\x64-Release\Tools\FBuild\FBuild finden Sie dann FBuild.exe.

`FBuild.exe All-x64-Release -dist -coordinator=127.0.0.1` can start distributed compilation.

###FBuild More Options

Ich biete FBuild an, das standardmäßig folgende Optionen unterstützt:

- Koordinator: Geben Sie die Coordinator-IP-Adresse ein (Sie können den Wert von Systemumgebungsvariablen überschreiben)
- Brokerage: Specified Brokerage-Adresse (kann den Wert von Umgebungsvariablen überschreiben)
- nocache: Erzwingt die Nichtverwendung des Zwischenspeichers.
- dist: Enable distributed compilation
- forceremote: Erzwingt das Kompilieren auf einer entfernten Maschine

Zusammenfassung: Erstellen Sie nach dem Abschluss der Bearbeitung einen statistischen Bericht.

Warten Sie mal, weitere Optionen können mit `FBuild.exe -help` ausgeführt werden.

FBuildWorker常用的選項有：

- coordinator: Specify Coordinator IP-Adresse (kann Werte von Systemumgebungsvariablen überschreiben)
- brokerage: Die angegebene Brokerage-Adresse (kann den Wert von Systemumgebungsvariablen überschreiben)
- nocache: erzwingt das Nichtverwenden des Zwischenspeichers
- cpus: Angeben, wie viele Kerne dem Kompilierungsvorgang zugewiesen werden sollen

Mehr Optionen können durch Ausführen von `FBuildWorder.exe -help` angezeigt werden.

###Ändern Sie die mitgelieferte FASTBuild.cs-Datei von UE.

Die mitgelieferte FASTBuild.cs von UE behandelt die Systemumgebungsvariablen nicht optimal im Zusammenhang mit den in BuildConfiguration.xml angegebenen Parametern. Viele Parameter lesen zuerst die Systemumgebungsvariable, was offensichtlich dem Logik der Verwendung von BuildConfiguration.xml widerspricht.

Zu diesem Zweck können die entsprechenden Codes wie folgt geändert werden, hier am Beispiel von UE5.3:

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

###BuildConfiguration.xml Fortgeschrittenenkonfiguration

```xml
<?xml version="1.0" encoding="utf-8" ?>
<Configuration xmlns="https://www.unrealengine.com/BuildConfiguration">
    <ProjectFileGenerator>
<!-- Specify the VS version -->
        <Format>VisualStudio2022</Format>
    </ProjectFileGenerator>
    <BuildConfiguration>
<!-- Aktiviere FASTBuild -->
        <bAllowFASTBuild>true</bAllowFASTBuild>
Bitte übersetze den folgenden Text ins Deutsche:

<!-- 指定本机参与编译的 cpu 核数 -->
        <MaxParallelActions>12</MaxParallelActions>
<!-- Schließen Incredibuild -->
        <bAllowXGE>false</bAllowXGE>
    </BuildConfiguration>
    <FASTBuild>
<!-- Geben Sie den FBuild-Pfad an -->
        <FBuildExecutablePath>d:\libs\FASTBuild\bin\FBuild.exe</FBuildExecutablePath>
<!-- Start der verteilten Kompilierung -->
        <bEnableDistribution>true</bEnableDistribution>
<!-- Geben Sie den Brokerage-Pfad an -->
        <FBuildBrokeragePath>\\127.0.0.1\Brokerage\</FBuildBrokeragePath>
<!-- Geben Sie den Cache-Pfad an -->
        <FBuildCachePath>\\127.0.0.1\Cache\</FBuildCachePath>
<!-- Aktiviere Cache -->
        <bEnableCaching>true</bEnableCaching>
<!-- Cache permissions for reading/writing: Lesen/Schreiben/Lesen und Schreiben -->
        <CacheMode>ReadWrite</CacheMode>
<!-- Geben Sie die IP-Adresse des Koordinators an -->
        <FBuildCoordinator>127.0.0.1</FBuildCoordinator>
<!-- erzwingt Remote-Kompilierung -->
        <!-- <bForceRemote>true</bForceRemote> -->
    </FASTBuild>
</Configuration>
```

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt. Bitte gib dein Feedback in [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Bitte markieren Sie jegliche Auslassungen mit dem Zeigefinger. 
