---
layout: post
title: Utiliser FASTBuild pour compiler UE4 et UE5
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
description: Le support de FASTBuild par UE n'est pas très complet. Pour permettre
  à UE4 et UE5 de prendre en charge FASTBuild de manière optimale, nous devons effectuer
  quelques configurations et modifications dans le code source. Voici les détails
  pour vous.
figures: []
---

<meta property="og:title" content="使用 FASTBuild 编译 UE4 和 UE5" />

> La méthode présentée dans cet article a été testée et prend en charge UE4.27 - UE5.3. Les autres versions n'ont pas été testées, mais vous pouvez essayer.

##Préface

[FASTBuild](https://www.fastbuild.org/docs/home.html)C'est un outil de compilation distribuée open source gratuit. La compilation dans UE prend du temps, mais en utilisant FASTBuild, on peut réduire considérablement le temps nécessaire.

UE à partir de la version 4.x prend en charge FASTBuild, le code source officiel inclut un outil FASTBuild modifié, basé sur la version 0.99 de FASTBuild, situé dans `Engine\Extras\ThirdPartyNotUE\FASTBuild`, la version 5.3 d'UE utilise également cette version. C'est une version relativement ancienne, à la date de création de cet article, la dernière version officielle de FASTBuild est 1.11, qui propose de nouvelles fonctionnalités et des corrections de bugs. Cet article met l'accent sur la manière d'utiliser la version 1.11 tout en prenant en charge UE4 et UE5.

##Configuration simple

Pour atteindre cet objectif, nous devons apporter quelques modifications à FASTBuild 1.11 et au code source d'UE. En fait, j'ai déjà terminé toutes les modifications, donc nous pouvons directement utiliser ma version modifiée.

Téléchargez la [dernière version](https://github.com/disenone/fastbuild/releases)Les fichiers exécutables à l'intérieur sont FBuild.exe, FBuildCoordinator.exe, FBuildWorker.exe. Pour simplifier les choses, on appellera les machines qui utilisent FBuild.exe pour la programmation "Machine Locale", et les machines distantes qui fournissent la participation du CPU pour l'édition "Machine Distante".


###La configuration de cet appareil

Intégrez le répertoire contenant FBuild.exe dans la variable d'environnement du système Path pour vous assurer que FBuild.exe peut être directement exécuté dans l'invite de commandes (cmd).

Configurer le répertoire partagé pour le Cache (si vous n'avez pas besoin de générer le Cache, vous pouvez ne pas le configurer) : définissez un répertoire vide comme chemin partagé et assurez-vous que la machine distante peut y accéder.

Ouvrez le projet source UE4 / UE5 sur cette machine, puis modifiez le fichier de configuration de compilation Engine\Saved\UnrealBuildTool\BuildConfiguration.xml comme suit :

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

Exécutez le FBuildCoordinator.exe téléchargé précédemment sur cette machine.

###Configuration distante de la machine

Configurer le cache avec la même configuration, mais spécifier l'adresse IP sur l'adresse IP locale, supposée ici être 192.168.1.100.

- FASTBUILD_CACHE_PATH: \\192.168.1.100\Cache
- FASTBUILD_CACHE_MODE: rw

Configuration identique de l'IP du Coordinateur

- FASTBUILD_COORDINATOR: 192.168.1.100

Configuration terminée comme illustré ci-dessous.

![](assets/img/2023-ue-fastbuild/remote_vars.png)

Exécutez FBuildWorker.exe sur la machine distante. Si la configuration est réussie, des journaux seront affichés sur FBuildCoordinator.exe de votre ordinateur local (ici 192.168.1.101 est l'adresse IP de la machine distante) :

```
FBuildCoordinator - v1.11-UE
[2023-12-01-20:06:38] Listening on port 31392
[2023-12-01-20:06:38] current [0] workers: []
[2023-12-01-20:06:42] New worker available: 192.168.1.101
[2023-12-01-20:06:42] current [1] workers: [192.168.1.101]
```

###Test UE Compilation

Ouvrez le projet de code source UE dans Visual Studio en utilisant le fichier sln. Sélectionnez un projet en C++, puis cliquez sur Rebuild. Si la configuration est correcte, vous devriez voir des journaux semblables à ceux-ci :

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

FASTBuild peut trouver l'IP de la machine distante et commencer à envoyer la compilation à la machine distante. Sur le FBuildWorker de la machine distante, on peut également voir qu'il y a une tâche de compilation en cours.

##Configuration avancée

###Support de versions UE plus longues

Si tu remarques que ta UE n'a pas l'outil FASTBuild (Engine\Extras\ThirdPartyNotUE\FASTBuild) et qu'il n'y a pas de fichier FASTBuild.cs dans le projet UnrealBuildTool, il est très probable que ta version d'UE ne prend pas encore en charge FASTBuild.

Vous devez vous référer au code source de l'UE4.27, créer un fichier FASTBuild.cs similaire et apporter les modifications nécessaires aux autres codes connexes, mais je ne rentre pas dans les détails ici.


###Compiler votre propre FASTBuild.

Si vous êtes également intéressé par FASTBuild en lui-même, ou si vous souhaitez apporter des modifications, vous pouvez essayer de compiler FASTBuild avec FASTBuild.

Téléchargez mon [dernier code source](https://github.com/disenone/fastbuild/releases)Et décompressez
Veuillez traduire ce texte en français :

- Modifier External\SDK\VisualStudio\VS2019.bff en remplaçant les éléments .VS2019_BasePath et .VS2019_Version par les valeurs correspondant à votre machine locale. Vous pouvez trouver la version dans le répertoire .VS2019_BasePath\Tools\MSVC, par exemple.
    ```
    .VS2019_BasePath        = 'C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC'    // <-- Set path here
    .VS2019_Version         = '14.29.30133' // <-- Set version here
    .VS2019_MSC_VER         = '1929' // <-- Set MSC_VER here
    ```

- Modifiez External\SDK\Windows\Windows10SDK.bff pour .Windows10_SDKBasePath et .Windows10_SDKVersion, la version peut être consultée dans .Windows10_SDKBasePath/bin :
    ```
    .Windows10_SDKBasePath        = 'C:\Program Files (x86)\Windows Kits/10'    // <-- Set path here
    .Windows10_SDKVersion         = '10.0.19041.0' // <-- Set version here
    ```

Veuillez modifier les .Clang11_BasePath et .Clang11_Version du fichier External\SDK\Clang\Windows\Clang11.bff, le chemin se trouvant dans .VS2019_BasePath\Tools\Tools/LLVM/x64.
    ```
    .Clang11_BasePath = 'C:/Program Files (x86)/Microsoft Visual Studio/2019/Professional/VC/Tools/LLVM/x64'    // <-- Set path here
    .Clang11_Version  = '12.x.x'
    ```

- Accédez au répertoire Code, puis dans cmd exécutez `FBuild.exe All-x64-Release`. Si la configuration est réussie, vous verrez la compilation réussie. Vous pourrez trouver FBuild.exe dans tmp\x64-Release\Tools\FBuild\FBuild.

- `FBuild.exe All-x64-Release -dist -coordinator=127.0.0.1` permet de lancer la compilation distribuée.

###FBuild Plus d'options

Je propose les options couramment utilisées suivantes prises en charge par FBuild :

- coordinate: Specify the Coordinator IP address (which can override the values ​​of system environment variables)
- brokerage : Adresse de courtage spécifiée (peut remplacer la valeur des variables d'environnement système)
- nocache : forcer l'utilisation sans cache
- dist : activer la compilation distribuée
forceremote: Compile obligatoirement sur la machine distante
- résumé : Générer un rapport statistique après la fin de l'édition.

Attendez, plus d'options peuvent être trouvées en exécutant `FBuild.exe -help`.

Les options couramment utilisées par FBuildWorker sont :

- coordinator : Spécifiez l'adresse IP du coordinateur (peut remplacer la valeur de la variable d'environnement du système)
- courtage : Spécifiez l'adresse du courtage (peut remplacer les valeurs des variables d'environnement système)
- nocache : forcer à ne pas utiliser le cache
- cpus : spécifie le nombre de cœurs à allouer pour la compilation

Pour plus d'options, exécutez `FBuildWorder.exe -help`.

###Modifier le FASTBuild.cs fourni par UE.

Le FASTBuild.cs fourni par l'UE ne gère pas bien les variables d'environnement du système, et la relation avec les paramètres spécifiés dans le BuildConfiguration.xml. De nombreux paramètres sont prioritaires sur les variables d'environnement du système, ce qui est clairement contraire à la logique d'utilisation de BuildConfiguration.xml.

Pour ce faire, le code pertinent peut être modifié comme suit, en prenant UE5.3 comme exemple :

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

###BuildConfiguration.xml Configuration avancée

```xml
<?xml version="1.0" encoding="utf-8" ?>
<Configuration xmlns="https://www.unrealengine.com/BuildConfiguration">
    <ProjectFileGenerator>
<!-- Spécifiez la version de Visual Studio -->
        <Format>VisualStudio2022</Format>
    </ProjectFileGenerator>
    <BuildConfiguration>
        <!-- Activer FASTBuild -->
        <bAllowFASTBuild>true</bAllowFASTBuild>
<!-- Spécifie le nombre de cœurs CPU utilisés pour la compilation sur la machine locale -->
        <MaxParallelActions>12</MaxParallelActions>
        <!-- Fermer Incredibuild -->
        <bAllowXGE>false</bAllowXGE>
    </BuildConfiguration>
    <FASTBuild>
<!-- Spécifiez le chemin de FBuild -->
        <FBuildExecutablePath>d:\libs\FASTBuild\bin\FBuild.exe</FBuildExecutablePath>
<!-- Activer la compilation distribuée -->
        <bEnableDistribution>true</bEnableDistribution>
<!-- Spécifiez le chemin du courtage -->
        <FBuildBrokeragePath>\\127.0.0.1\Brokerage\</FBuildBrokeragePath>
<!-- Spécifier le chemin du cache -->
        <FBuildCachePath>\\127.0.0.1\Cache\</FBuildCachePath>
<!-- Activer le cache -->
        <bEnableCaching>true</bEnableCaching>
<!-- Les autorisations de lecture/écriture de cache Read/Write/ReadWrite -->
        <CacheMode>ReadWrite</CacheMode>
<!-- Spécifiez l'adresse IP du coordinateur -->
        <FBuildCoordinator>127.0.0.1</FBuildCoordinator>
<!-- Compilation à distance forcée -->
        <!-- <bForceRemote>true</bForceRemote> -->
    </FASTBuild>
</Configuration>
```

--8<-- "footer_fr.md"


> Ce post a été traduit par ChatGPT, veuillez [**nous faire part de vos retours**](https://github.com/disenone/wiki_blog/issues/new)S'il vous plaît signaler tout manquement. 
