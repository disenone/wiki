---
layout: post
title: Verwenden von FASTBuild zum Kompilieren von UE4 und UE5
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
description: Um FASTBuild in UE (Unreal Engine) 4 und UE5 optimal zu unterstützen,
  sind einige Konfigurationen und Änderungen am Quellcode erforderlich, da die native
  Unterstützung von FASTBuild nicht perfekt ist. Im Folgenden werde ich dir die Schritte
  einzeln erklären.
figures: []
---

<meta property="og:title" content="使用 FASTBuild 编译 UE4 和 UE5" />

> Die beschriebene Methode wurde getestet und unterstützt UE4.27 - UE5.3; andere Versionen wurden nicht getestet, können aber ausprobiert werden.

##Vorwort

[FASTBuild](https://www.fastbuild.org/docs/home.html)Es handelt sich um ein kostenloses, Open-Source verteiltes Kompilierungstool. Die Kompilierung von UE selbst kann zeitaufwendig sein. Wenn FASTBuild genutzt werden kann, kann dies die benötigte Zeit erheblich reduzieren.

UE unterstützt seit Version 4.x FASTBuild. Der offizielle Quellcode enthält ein modifiziertes FASTBuild-Tool, basierend auf Version 0.99, das sich im Verzeichnis `Engine\Extras\ThirdPartyNotUE\FASTBuild` befindet. Auch UE5.3 verwendet diese Version. Dies ist bereits eine etwas veraltete Version; zum Zeitpunkt der Erstellung dieses Dokuments ist die neueste offizielle Version von FASTBuild 1.11, die viele neue Funktionen und Fehlerbehebungen bietet. Dieser Artikel konzentriert sich darauf, wie man die Version 1.11 sowohl mit UE4 als auch mit UE5 nutzen kann.

##Einfache Konfiguration

Um das Ziel zu erreichen, müssen wir einige Änderungen an FASTBuild 1.11 und dem UE-Quellcode vornehmen. Ich habe diese Änderungen bereits vorgenommen, sodass wir direkt meine bearbeitete Version verwenden können.

FASTBuild download der von mir eingereichten [latest version](https://github.com/disenone/fastbuild/releases)Die ausführbaren Dateien im Inneren sind FBuild.exe, FBuildCoordinator.exe und FBuildWorker.exe. Um die Dinge klarzustellen, werden die Maschinen, die FBuild.exe zum Programmieren verwenden, als `lokale Maschine` bezeichnet, während die anderen Maschinen, die CPU-Ressourcen für die Bearbeitung bereitstellen, als `remote Maschine` bezeichnet werden.

###Gerätekonfiguration

Fügen Sie das Verzeichnis, in dem sich FBuild.exe befindet, zur Systemumgebungsvariable Path hinzu, damit FBuild.exe direkt in der Eingabeaufforderung (cmd) ausgeführt werden kann.

Richten Sie das Cache-Shared-Verzeichnis ein (wenn kein Cache generiert werden soll, kann dies ignoriert werden): Legen Sie ein leeres Verzeichnis als Freigabepfad fest und stellen Sie sicher, dass der Remote-Maschine darauf zugreifen kann.

Bitte öffnen Sie das Quellcodeprojekt von UE4 / UE5 auf diesem Rechner und ändern Sie die Buildkonfigurationsdatei Engine\Saved\UnrealBuildTool\BuildConfiguration.xml wie folgt:

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

FBuildCoordinator.exe, das zuvor heruntergeladen wurde, auf diesem Gerät ausführen.

###Remote machine configuration

Die gleiche Konfiguration des Caches, nur dass die IP auf die lokale IP festgelegt werden muss, die hier als 192.168.1.100 angenommen wird.

- FASTBUILD_CACHE_PATH: \\192.168.1.100\Cache
- FASTBUILD_CACHE_MODE: rw

Bitte übersetzen Sie den Text ins Deutsche:

同样配置 Koordinator-IP

- FASTBUILD_COORDINATOR: 192.168.1.100

Die Konfiguration ist wie im folgenden Bild abgeschlossen.

![](assets/img/2023-ue-fastbuild/remote_vars.png)

FBuildWorker.exe läuft auf dem Remote-Rechner. Wenn die Konfiguration erfolgreich ist, wird auf dem lokalen FBuildCoordinator.exe Protokolle angezeigt (hier ist 192.168.1.101 die IP des Remote-Rechners):

```
FBuildCoordinator - v1.11-UE
[2023-12-01-20:06:38] Listening on port 31392
[2023-12-01-20:06:38] current [0] workers: []
[2023-12-01-20:06:42] New worker available: 192.168.1.101
[2023-12-01-20:06:42] current [1] workers: [192.168.1.101]
```

###Test UE Kompilierung

Öffnen Sie das UE-Quellcodeprojekt sln mit Visual Studio, wählen Sie ein C++-Projekt aus und klicken Sie auf "Rebuild". Wenn die Konfiguration korrekt ist, sehen Sie ähnliche Protokolle wie folgt:

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

FASTBuild kann die IP-Adresse des Remote-Rechners finden und mit dem Kompilieren auf dem Remote-Rechner beginnen. Auf dem FBuildWorker des Remote-Rechners kann man auch sehen, dass gerade ein Kompiliervorgang läuft.

##Fortgeschrittene Konfiguration

###Unterstützung für ältere Versionen von UE.

Wenn du feststellst, dass dein UE keine FASTBuild-Tool (Engine\Extras\ThirdPartyNotUE\FASTBuild) hat und im Projekt UnrealBuildTool keine FASTBuild.cs-Datei vorhanden ist, ist es sehr wahrscheinlich, dass deine UE-Version FASTBuild noch nicht unterstützt.

Sie müssen sich auf den Quellcode von UE4.27 beziehen und eine ähnliche FASTBuild.cs-Datei erstellen sowie die entsprechenden Code-Änderungen vornehmen. Weitere Details werden hier nicht erläutert.


###Kompilieren Sie Ihr eigenes FASTBuild.

Wenn Sie auch am FASTBuild selbst interessiert sind oder einige Änderungen vornehmen möchten, können Sie versuchen, den FASTBuild mit dem FASTBuild zu kompilieren.

Bitte lade meinen [neuesten Quellcode](https://github.com/disenone/fastbuild/releases)，und entpacken
Bearbeiten Sie External\SDK\VisualStudio\VS2019.bff und ändern Sie .VS2019_BasePath und .VS2019_Version entsprechend auf Ihre lokal gespeicherten Informationen. Die Version kann im Verzeichnis .VS2019_BasePath\Tools\MSVC gefunden werden, zum Beispiel.
    ```
    .VS2019_BasePath        = 'C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC'    // <-- Set path here
    .VS2019_Version         = '14.29.30133' // <-- Set version here
    .VS2019_MSC_VER         = '1929' // <-- Set MSC_VER here
    ```

- Ändern Sie .Windows10_SDKBasePath und .Windows10_SDKVersion in External\SDK\Windows\Windows10SDK.bff, die Version kann in .Windows10_SDKBasePath/bin eingesehen werden:
    ```
    .Windows10_SDKBasePath        = 'C:\Program Files (x86)\Windows Kits/10'    // <-- Set path here
    .Windows10_SDKVersion         = '10.0.19041.0' // <-- Set version here
    ```

Ändern Sie .Clang11_BasePath und .Clang11_Version in External\SDK\Clang\Windows\Clang11.bff, der Pfad befindet sich in .VS2019_BasePath\Tools\Tools/LLVM/x64.
    ```
    .Clang11_BasePath = 'C:/Program Files (x86)/Microsoft Visual Studio/2019/Professional/VC/Tools/LLVM/x64'    // <-- Set path here
    .Clang11_Version  = '12.x.x'
    ```

Gehen Sie in das Verzeichnis "Code", führen Sie "FBuild.exe All-x64-Release" in der Eingabeaufforderung aus. Wenn die Konfiguration korrekt ist, sehen Sie eine erfolgreiche Kompilierung. In "tmp\x64-Release\Tools\FBuild\FBuild" sollte die Datei FBuild.exe zu sehen sein.

- `FBuild.exe All-x64-Release -dist -coordinator=127.0.0.1` kann die verteilte Kompilierung aktivieren.

###"FBuild More Options" - "FBuild Weitere Optionen"

Das von mir bereitgestellte FBuild unterstützt selbst die folgenden gängigen Optionen:

- coordinator: Geben Sie die Coordinator-IP-Adresse an (kann den Wert von Umgebungsvariablen überschreiben)
- brokerage: Geben Sie die Brokerage-Adresse an (kann den Wert der Systemumgebungsvariablen überschreiben)
- nocache: Cache nicht verwenden erzwingen
- dist: Aktiviere verteiltes Kompilieren.
forceremote: compile auf dem Remote-Computer erzwingen
Zusammenfassung: Erstellen Sie nach Abschluss der Bearbeitung einen statistischen Bericht.

Warte, mehr Optionen können durch das Ausführen von `FBuild.exe -help` angezeigt werden.

Die gängigen Optionen für FBuildWorker sind:

- Koordinator: Angegebene Koordinator-IP-Adresse (kann den Wert von Umgebungsvariablen überschreiben)
- brokerage: Specified Brokerage-Adresse (kann den Wert von Umgebungsvariablen überschreiben)
- nocache: Erzwingt die Nichtnutzung des Cache
- cpus: Angeben, wie viele Kerne für die Kompilierung zugewiesen werden sollen.

Weitere Optionen können durch das Ausführen von `FBuildWorder.exe -help` angezeigt werden.

###Ändere die standardmäßige FASTBuild.cs von UE.

Die mit UE mitgelieferte FASTBuild.cs verarbeitet die Systemumgebungsvariablen nicht optimal und steht im Widerspruch zu den in BuildConfiguration.xml festgelegten Parametern. Viele Parameter werden vorrangig aus den Systemumgebungsvariablen gelesen, was offensichtlich der Logik der Verwendung von BuildConfiguration.xml entgegensteht.

Dazu kann der entsprechende Code folgendermaßen geändert werden, hier am Beispiel von UE5.3:

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

###BuildConfiguration.xml Erweiterte Konfiguration

```xml
<?xml version="1.0" encoding="utf-8" ?>
<Configuration xmlns="https://www.unrealengine.com/BuildConfiguration">
    <ProjectFileGenerator>
<!-- Vorgesehene vs-Version -->
        <Format>VisualStudio2022</Format>
    </ProjectFileGenerator>
    <BuildConfiguration>
<!-- Aktiviere FASTBuild -->
        <bAllowFASTBuild>true</bAllowFASTBuild>
Bitte übersetzen Sie den Text ins Deutsche:

        <!-- 指定本机参与编译的 cpu 核数 -->
        <MaxParallelActions>12</MaxParallelActions>
<!-- Incredibuild schließen -->
        <bAllowXGE>false</bAllowXGE>
    </BuildConfiguration>
    <FASTBuild>
<!-- FBuild-Pfad angeben -->
        <FBuildExecutablePath>d:\libs\FASTBuild\bin\FBuild.exe</FBuildExecutablePath>
<!-- Aktiviere verteiltes Kompilieren -->
        <bEnableDistribution>true</bEnableDistribution>
<!-- Geben Sie den Broker-Pfad an -->
        <FBuildBrokeragePath>\\127.0.0.1\Brokerage\</FBuildBrokeragePath>
<!-- Angeben des Cache-Pfads -->
        <FBuildCachePath>\\127.0.0.1\Cache\</FBuildCachePath>
<!-- Activate cache -->
        <bEnableCaching>true</bEnableCaching>
<!-- Cache-Berechtigungen Lesen/Schreiben/Lesen und Schreiben -->
        <CacheMode>ReadWrite</CacheMode>
Bitte übersetzen Sie diesen Text ins Deutsche:

        <!-- Specifying Coordinator-IP -->
        <FBuildCoordinator>127.0.0.1</FBuildCoordinator>
<!-- Zwangsweise Remote-Kompilierung -->
        <!-- <bForceRemote>true</bForceRemote> -->
    </FASTBuild>
</Configuration>
```

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt, bitte bei [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Es wird auf etwaige Auslassungen hingewiesen. 
