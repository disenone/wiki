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
description: UE native support for FASTBuild is not very complete. In order to make
  UE4 and UE5 fully compatible with FASTBuild, we need to make some configuration
  and source code modifications. Let me guide you through the process.
figures: []
---

<meta property="og:title" content="使用 FASTBuild 编译 UE4 和 UE5" />

> Ce texte a été testé avec succès sur UE4.27 - UE5.3, les autres versions n'ont pas été testées, mais peuvent être essayées.

##Préface.

[FASTBuild](https://www.fastbuild.org/docs/home.html)C'est un outil de compilation distribuée open source gratuit. Le processus de compilation de l'UE consomme beaucoup de temps, mais avec FASTBuild, on peut grandement réduire ce temps.

À partir de la version 4.x, l'UE prend en charge FASTBuild. Le code source officiel contient un outil FASTBuild modifié, basé sur la version 0.99 de FASTBuild, situé dans `Engine\Extras\ThirdPartyNotUE\FASTBuild`. UE5.3 utilise également cette version. C'est une version assez ancienne maintenant. Au moment de la rédaction de cet article, la dernière version officielle de FASTBuild est la 1.11, offrant de nouvelles fonctionnalités et correctifs de bugs. Cet article se concentre sur la manière d'utiliser la version 1.11 pour prendre en charge à la fois UE4 et UE5.

##Configuration légère

Pour atteindre notre objectif, nous devons apporter quelques modifications au FASTBuild 1.11 et au code source d'UE. En fait, j'ai déjà effectué toutes les modifications nécessaires ici, donc nous pouvons utiliser directement la version modifiée que j'ai préparée.

Téléchargez le [dernière version](https://github.com/disenone/fastbuild/releases)Les fichiers exécutables à l'intérieur sont FBuild.exe, FBuildCoordinator.exe, FBuildWorker.exe. Pour clarifier, ci-dessous, l'utilisation de FBuild.exe pour la programmation est appelée "l'hôte local", tandis que les autres machines distantes qui fournissent une assistance CPU pour l'édition sont appelées "machines distantes".

###Configuration de cet appareil.

Ajoutez le répertoire où se trouve FBuild.exe au chemin d'accès de l'environnement système (Path) pour vous assurer que vous pouvez exécuter directement FBuild.exe dans l'invite de commandes (cmd).

Configurer le répertoire de cache partagé (si le cache n'est pas nécessaire, vous pouvez ne pas le configurer) : définir un répertoire vide comme chemin partagé et vérifier que la machine distante peut y accéder.

Ouvrez le projet source de UE4 / UE5 sur cette machine et modifiez le fichier de configuration de compilation Engine\Saved\UnrealBuildTool\BuildConfiguration.xml comme suit :

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

Exécuter le fichier FBuildCoordinator.exe téléchargé précédemment sur cette machine.

###Configuration à distance de la machine

Configurez la même mémoire cache, mais spécifiez l'adresse IP vers l'adresse IP locale, supposons ici qu'elle soit 192.168.1.100.

- FASTBUILD_CACHE_PATH: \\192.168.1.100\Cache
- FASTBUILD_CACHE_MODE: rw

Configurer de manière identique l'adresse IP du coordinateur

- FASTBUILD_COORDINATOR: 192.168.1.100

Configurer comme indiqué dans l'image ci-dessous.

![](assets/img/2023-ue-fastbuild/remote_vars.png)

Exécutez FBuildWorker.exe sur la machine distante. Si la configuration est réussie, vous verrez des journaux imprimés sur FBuildCoordinator.exe de votre machine locale (où l'adresse IP de la machine distante est 192.168.1.101) :

```
FBuildCoordinator - v1.11-UE
[2023-12-01-20:06:38] Listening on port 31392
[2023-12-01-20:06:38] current [0] workers: []
[2023-12-01-20:06:42] New worker available: 192.168.1.101
[2023-12-01-20:06:42] current [1] workers: [192.168.1.101]
```

###Vérification de la compilation de l'UE

Ouvrez le projet source UE avec VisualStudio en ouvrant le fichier sln, sélectionnez un projet C++, puis cliquez sur Rebuild. Si la configuration est correcte, vous devriez voir des journaux similaires à ceux-ci.

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

FASTBuild peut trouver l'adresse IP de la machine distante et commencer à envoyer le processus de compilation à distance. Sur le FBuildWorker de la machine distante, on peut également voir qu'une tâche de compilation est en cours.

##Configuration avancée

###Soutenir des versions plus anciennes d'UE.

Si vous constatez que votre UE ne dispose pas de l'outil FASTBuild (Engine\Extras\ThirdPartyNotUE\FASTBuild) et qu'il n'y a pas de fichier FASTBuild.cs dans le projet UnrealBuildTool, il est très probable que la version de votre UE ne prend pas encore en charge FASTBuild.

Alors, vous devez vous référer au code source de l'UE4.27, créer également un fichier FASTBuild.cs similaire, et apporter les modifications nécessaires au reste du code. Je n'entrerai pas dans les détails ici.


###Compiler votre propre FASTBuild.

Si FASTBuild t'intéresse également, ou si tu souhaites apporter des modifications, tu peux essayer de compiler FASTBuild avec FASTBuild.

Téléchargez mon [dernier code source](https://github.com/disenone/fastbuild/releases)Et décompresser
Modifier le fichier External\SDK\VisualStudio\VS2019.bff en remplaçant les valeurs de .VS2019_BasePath et .VS2019_Version par celles correspondant à votre machine locale. Vous pouvez trouver la version dans le répertoire .VS2019_BasePath\Tools\MSVC, par exemple.
    ```
    .VS2019_BasePath        = 'C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC'    // <-- Set path here
    .VS2019_Version         = '14.29.30133' // <-- Set version here
    .VS2019_MSC_VER         = '1929' // <-- Set MSC_VER here
    ```

Veuillez modifier les valeurs de .Windows10_SDKBasePath et .Windows10_SDKVersion dans External\SDK\Windows\Windows10SDK.bff. Vous pouvez trouver la version dans .Windows10_SDKBasePath/bin.
    ```
    .Windows10_SDKBasePath        = 'C:\Program Files (x86)\Windows Kits/10'    // <-- Set path here
    .Windows10_SDKVersion         = '10.0.19041.0' // <-- Set version here
    ```

Veuillez modifier les valeurs de .Clang11_BasePath et .Clang11_Version dans External\SDK\Clang\Windows\Clang11.bff, situées dans le chemin .VS2019_BasePath\Tools\Tools/LLVM/x64.
    ```
    .Clang11_BasePath = 'C:/Program Files (x86)/Microsoft Visual Studio/2019/Professional/VC/Tools/LLVM/x64'    // <-- Set path here
    .Clang11_Version  = '12.x.x'
    ```

Allez dans le répertoire Code, puis exécutez `FBuild.exe All-x64-Release` dans cmd. Si la configuration est correcte, vous devriez voir une compilation réussie. Vous pourrez trouver FBuild.exe dans tmp\x64-Release\Tools\FBuild\FBuild.

- `FBuild.exe All-x64-Release -dist -coordinator=127.0.0.1` allows you to enable distributed compilation.

###Afficher plus d'options sur FBuild.

Je propose des options couramment utilisées prises en charge par FBuild :

- coordinate: Specify the Coordinator IP address (which can override the value of system environment variables)
- brokerage: Adresse de courtage spécifiée (pouvant remplacer les valeurs des variables d'environnement du système)
- nocache: force à ne pas utiliser le cache
- dist: Activer la compilation distribuée
forceremote: obligé à compiler sur la machine distante
résumé: Émettre un rapport statistique après l'édition.

Attendez, pour plus d'options, vous pouvez exécuter `FBuild.exe -help` pour les consulter.

Les options couramment utilisées par FBuildWorker sont:

- coordinate: Assigner l'adresse IP du coordinateur (pouvant remplacer la valeur des variables d'environnement du système)
- courtage: Adresse de courtage spécifiée (pouvant écraser les valeurs des variables d'environnement du système)
nocache: force à ne pas utiliser le cache
- cpus: spécifie le nombre de cœurs à utiliser pour la compilation

Plus d'options peuvent être consultées en exécutant `FBuildWorder.exe -help`.

###Modifier le FASTBuild.cs intégré à l'UE.

Le fichier FASTBuild.cs fourni par l'UE ne gère pas correctement les variables d'environnement système par rapport aux paramètres spécifiés dans BuildConfiguration.xml. De nombreux paramètres sont d'abord lus à partir des variables d'environnement système, ce qui va à l'encontre de la logique d'utilisation de BuildConfiguration.xml.

Pour ce faire, vous pouvez modifier le code pertinent comme ceci, en prenant UE5.3 comme exemple :

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

###Le fichier BuildConfiguration.xml est une configuration avancée.

```xml
<?xml version="1.0" encoding="utf-8" ?>
<Configuration xmlns="https://www.unrealengine.com/BuildConfiguration">
    <ProjectFileGenerator>
<!-- Spécifier la version de Visual Studio -->
        <Format>VisualStudio2022</Format>
    </ProjectFileGenerator>
    <BuildConfiguration>
<!-- Activer FASTBuild -->
        <bAllowFASTBuild>true</bAllowFASTBuild>
<!-- Spécifie le nombre de cœurs CPU utilisés pour la compilation sur cette machine locale -->
        <MaxParallelActions>12</MaxParallelActions>
<!-- Fermer Incredibuild -->  
        <bAllowXGE>false</bAllowXGE>
    </BuildConfiguration>
    <FASTBuild>
<!-- Spécifier le chemin FBuild -->
        <FBuildExecutablePath>d:\libs\FASTBuild\bin\FBuild.exe</FBuildExecutablePath>
<!-- Activer la compilation distribuée -->
        <bEnableDistribution>true</bEnableDistribution>
<!-- Spécifiez le chemin du courtage -->
        <FBuildBrokeragePath>\\127.0.0.1\Brokerage\</FBuildBrokeragePath>
<!-- Spécifie le chemin du cache -->
        <FBuildCachePath>\\127.0.0.1\Cache\</FBuildCachePath>
<!-- Activer le cache -->
        <bEnableCaching>true</bEnableCaching>
<!-- Droits de lecture/écriture/droit de lecture-écriture du cache -->
        <CacheMode>ReadWrite</CacheMode>
<!-- Specify the coordinator IP -->
        <FBuildCoordinator>127.0.0.1</FBuildCoordinator>
<!-- Compilation distante forcée -->
        <!-- <bForceRemote>true</bForceRemote> -->
    </FASTBuild>
</Configuration>
```

--8<-- "footer_fr.md"


> (https://github.com/disenone/wiki_blog/issues/new)S'il vous plaît signaler tout oubli. 
