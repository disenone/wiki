---
layout: post
title: Using FASTBuild to Compile UE4 and UE5
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
description: The native support for FASTBuild in UE is not very complete. In order
  to make UE4 and UE5 fully support FASTBuild, we need to make some configurations
  and source code modifications. Let me explain to you one by one.
figures: []
---

<meta property="og:title" content="使用 FASTBuild 编译 UE4 和 UE5" />

> This method in this article has been tested and supports UE4.27 - UE5.3. Other versions have not been tested, but feel free to give it a try.

##Preface

[FASTBuild](https://www.fastbuild.org/docs/home.html)It is a free and open-source distributed compilation tool. Compiling UE itself can be time-consuming, but using FASTBuild can significantly reduce the time spent.

Starting from version 4.x, UE is able to support FASTBuild. The official source code comes with a modified version of the FASTBuild tool, based on FASTBuild version 0.99, located at `Engine\Extras\ThirdPartyNotUE\FASTBuild`. UE5.3 also uses this version. This is quite an old version; as of the creation of this article, the latest official version of FASTBuild is 1.11, which has more new feature support and bug fixes. This article focuses on how to use version 1.11 to support both UE4 and UE5.

##Simple setup

To achieve our goal, we need to make some modifications to FASTBuild 1.11 and the UE source code. Here, I have already completed all the modifications, so we can directly use the version I've modified.

Download the [latest version](https://github.com/disenone/fastbuild/releases)The execution files inside are FBuild.exe, FBuildCoordinator.exe, FBuildWorker.exe. To be clear, the machine using FBuild.exe for programming will be referred to as the “local machine,” while other machines participating in editing via CPU will be referred to as “remote machines.”

###This machine configuration

Add the directory where FBuild.exe is located to the system environment variable Path, to ensure that FBuild.exe can be directly executed in the command prompt (cmd).

Configure the Cache shared directory (if there’s no need to generate Cache, this step can be omitted): set up an empty directory as the shared path and ensure that the remote machine can access it.

Open the source code project of Unreal Engine 4/5 on this machine, and modify the compilation configuration file Engine\Saved\UnrealBuildTool\BuildConfiguration.xml as follows:

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

Run the FBuildCoordinator.exe downloaded before on this machine.

###Remote machine configuration

The same configuration for Cache, just that the IP needs to be set to the local IP, assumed here to be 192.168.1.100.

- FASTBUILD_CACHE_PATH: \\192.168.1.100\Cache
- FASTBUILD_CACHE_MODE: rw

Coordinator IP with the same configuration

- FASTBUILD_COORDINATOR: 192.168.1.100

The setup is as shown in the following illustration.

![](assets/img/2023-ue-fastbuild/remote_vars.png)

Run FBuildWorker.exe on the remote machine. If configured successfully, you will see logs printed on FBuildCoordinator.exe of the local machine (where 192.168.1.101 is the IP address of the remote machine):

```
FBuildCoordinator - v1.11-UE
[2023-12-01-20:06:38] Listening on port 31392
[2023-12-01-20:06:38] current [0] workers: []
[2023-12-01-20:06:42] New worker available: 192.168.1.101
[2023-12-01-20:06:42] current [1] workers: [192.168.1.101]
```

###Test UE compilation.

Open the UE source code project sln in VisualStudio, select a C++ project, and click Rebuild. If the configuration is correct, you should see logs similar to the following.

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

FASTBuild can find the IP address of remote machines and start sending compilation tasks to them. On the remote machine's FBuildWorker, you can also see the current compilation tasks being executed.

##Advanced configuration

###Support for older versions of Unreal Engine

If you find that your UE does not have the FASTBuild tool (Engine\Extras\ThirdPartyNotUE\FASTBuild), and there is no FASTBuild.cs file in the UnrealBuildTool project, then it is very likely that your UE version does not yet support FASTBuild.

You will need to refer to the UE4.27 source code and create a similar FASTBuild.cs, as well as make the necessary modifications to other related code, which will not be elaborated here.


###Compile your own FASTBuild

If you are interested in FASTBuild itself or want to make some modifications, you can try compiling FASTBuild with FASTBuild.

- Download my [latest source code](https://github.com/disenone/fastbuild/releases)Extract and decompress
- Modify External\SDK\VisualStudio\VS2019.bff, change .VS2019_BasePath and .VS2019_Version to correspond to the content on your machine. You can check the Version in the .VS2019_BasePath\Tools\MSVC directory, for example.
    ```
    .VS2019_BasePath        = 'C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC'    // <-- Set path here
    .VS2019_Version         = '14.29.30133' // <-- Set version here
    .VS2019_MSC_VER         = '1929' // <-- Set MSC_VER here
    ```

Please modify .Windows10_SDKBasePath and .Windows10_SDKVersion in External\SDK\Windows\Windows10SDK.bff file. You can find the version in .Windows10_SDKBasePath/bin.
    ```
    .Windows10_SDKBasePath        = 'C:\Program Files (x86)\Windows Kits/10'    // <-- Set path here
    .Windows10_SDKVersion         = '10.0.19041.0' // <-- Set version here
    ```

- Modify .Clang11_BasePath and .Clang11_Version in External\SDK\Clang\Windows\Clang11.bff. The path is located at .VS2019_BasePath\Tools\Tools/LLVM/x64.
    ```
    .Clang11_BasePath = 'C:/Program Files (x86)/Microsoft Visual Studio/2019/Professional/VC/Tools/LLVM/x64'    // <-- Set path here
    .Clang11_Version  = '12.x.x'
    ```

Go to the Code directory, and run `FBuild.exe All-x64-Release` in the command prompt. If the configuration is correct, you should see a successful compilation. You can find the FBuild.exe in tmp\x64-Release\Tools\FBuild\FBuild.

`FBuild.exe All-x64-Release -dist -coordinator=127.0.0.1` can enable distributed compilation.

###FBuild More Options

The FBuild I provide supports the following common options:

- coordinator: Specify the Coordinator IP address (can override the value of system environment variables)
- brokerage: Specify the Brokerage address (which can override the value of system environment variables)
nocache: Force not to use cache
- dist: Enable distributed compilation
Compelling remote: Compiling on a remote machine
- summary: Output statistical report after editing is complete

Wait, for more options you can run 'FBuild.exe -help'.

Common options for FBuildWorker include:

- coordinator: Specify Coordinator IP address (which can override the values of system environment variables)
- brokerage: Refers to the specified Brokerage address (it can override the value of system environment variables)
nocache: Force not to use cache
- cpus: Specify how many cores to allocate for compilation.

To see more options, you can run `FBuildWorder.exe -help`.

###Modify the default FASTBuild.cs of UE.

The FASTBuild.cs that comes with UE does not handle system environment variables effectively, especially regarding their relationship with the parameters specified in BuildConfiguration.xml. Many parameters are prioritized from system environment variables, which is obviously contrary to the logic of using BuildConfiguration.xml.

To achieve this, the relevant code can be modified as follows, using UE5.3 as an example:

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

###BuildConfiguration.xml Advanced Configuration

```xml
<?xml version="1.0" encoding="utf-8" ?>
<Configuration xmlns="https://www.unrealengine.com/BuildConfiguration">
    <ProjectFileGenerator>
<!-- Specify vs version -->
        <Format>VisualStudio2022</Format>
    </ProjectFileGenerator>
    <BuildConfiguration>
<!-- Enable FASTBuild -->
        <bAllowFASTBuild>true</bAllowFASTBuild>
<!-- Specify the number of CPU cores on this machine to participate in the compilation -->
        <MaxParallelActions>12</MaxParallelActions>
<!-- Disable Incredibuild -->
        <bAllowXGE>false</bAllowXGE>
    </BuildConfiguration>
    <FASTBuild>
<!-- Specify the FBuild path -->
        <FBuildExecutablePath>d:\libs\FASTBuild\bin\FBuild.exe</FBuildExecutablePath>
<!-- Enable distributed compilation -->
        <bEnableDistribution>true</bEnableDistribution>
<!-- Specify the brokerage path -->
        <FBuildBrokeragePath>\\127.0.0.1\Brokerage\</FBuildBrokeragePath>
<!-- Specify cache path -->
        <FBuildCachePath>\\127.0.0.1\Cache\</FBuildCachePath>
<!-- Enable cache -->
        <bEnableCaching>true</bEnableCaching>
<!-- cache read and write permissions Read/Write/ReadWrite -->
        <CacheMode>ReadWrite</CacheMode>
<!-- Specify coordinator IP -->
        <FBuildCoordinator>127.0.0.1</FBuildCoordinator>
<!-- Force remote compilation -->
        <!-- <bForceRemote>true</bForceRemote> -->
    </FASTBuild>
</Configuration>
```

--8<-- "footer_en.md"


> This post was translated using ChatGPT, please provide [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions. 
