---
layout: post
title: Build UE4 and UE5 using FASTBuild.
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
description: The native support of FASTBuild in UE is not very complete. In order
  to perfectly support FASTBuild in both UE4 and UE5, we need to make some configurations
  and source code modifications. Let me explain them to you one by one.
figures: []
---

<meta property="og:title" content="使用 FASTBuild 编译 UE4 和 UE5" />

> This method has been tested and supports UE4.27 - UE5.3. Other versions have not been tested, but you can give it a try.

##Preface

[FASTBuild](https://www.fastbuild.org/docs/home.html)FASTBuild is a free and open-source distributed compilation tool. The compilation process of UE itself is quite time-consuming. By using FASTBuild, it is possible to significantly reduce the time spent.

UE 4.x and later versions can support FASTBuild. The official source code comes with a modified version of FASTBuild tools, based on version 0.99 of FASTBuild. It is located in `Engine\Extras\ThirdPartyNotUE\FASTBuild`. UE5.3 also uses this version. However, this is a relatively old version. As of the time of writing this article, the latest official version of FASTBuild is 1.11, which provides more new features and bug fixes. This article focuses on how to use version 1.11 to support both UE4 and UE5 at the same time.

##Easy Setup

To achieve our goal, we need to make some modifications to FASTBuild 1.11 and UE source code. Here, I have already made all the necessary modifications, so we can directly use the version that I have modified.

Download the [latest version](https://github.com/disenone/fastbuild/releases)Inside are the executable files FBuild.exe, FBuildCoordinator.exe, and FBuildWorker.exe. For clarity, we will refer to the machine that uses FBuild.exe for programming as "local machine," and the remote machines that provide CPU involvement in the editing process as "remote machines."

###Local Configuration

Add the directory where FBuild.exe is located to the system environment variable Path to ensure that FBuild.exe can be executed directly in the cmd.

Configure the shared directory for Cache (If Cache generation is not needed, it can be left unconfigured): Set an empty directory as the shared path and ensure that the remote machine has access to it.

Open the source code project for UE4 / UE5 on this machine and modify the compilation configuration file Engine\Saved\UnrealBuildTool\BuildConfiguration.xml as follows:

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

Download the FBuildCoordinator.exe that was previously run on this machine.

###Remote Machine Configuration

When configuring Cache with the same settings, just specify the IP address to be the local IP address, assuming it is 192.168.1.100.

- FASTBUILD_CACHE_PATH: \\192.168.1.100\Cache
- FASTBUILD_CACHE_MODE: rw

Configure the Coordinator IP in the same manner.

- FASTBUILD_COORDINATOR: 192.168.1.100

Configured as shown in the following figure.

![](assets/img/2023-ue-fastbuild/remote_vars.png)

Run FBuildWorker.exe on a remote machine. If the configuration is successful, logs will be printed on FBuildCoordinator.exe on your local machine (where 192.168.1.101 is the IP address of the remote machine).

```
FBuildCoordinator - v1.11-UE
[2023-12-01-20:06:38] Listening on port 31392
[2023-12-01-20:06:38] current [0] workers: []
[2023-12-01-20:06:42] New worker available: 192.168.1.101
[2023-12-01-20:06:42] current [1] workers: [192.168.1.101]
```

###Test UE Compilation

Open the UE source code project sln using VisualStudio, select a C++ project, and click on Rebuild. If the configuration is correct, you should see logs similar to the following:

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

FASTBuild can find the IP address of the remote machine and start sending the compilation to the remote machine. The FBuildWorker on the remote machine can also see that there is currently a compilation task being executed.

##Advanced Configuration

###Support for older versions of UE

If you find that your UE does not have the FASTBuild tool (Engine\Extras\ThirdPartyNotUE\FASTBuild), and there is no FASTBuild.cs file in the UnrealBuildTool project, it is highly likely that your UE version does not yet support FASTBuild.

Then you need to refer to the UE4.27 source code and create a similar FASTBuild.cs file, and make the necessary modifications to other related code. I won't go into detail here.


###Compile your own FASTBuild

If you are also interested in FASTBuild itself, or want to make some modifications, you can try using FASTBuild to compile FASTBuild.

- Download my [latest source code](https://github.com/disenone/fastbuild/releases), and decompress
- Modify External\SDK\VisualStudio\VS2019.bff, and change .VS2019_BasePath and .VS2019_Version to the corresponding content on your local machine. You can find the Version in the .VS2019_BasePath\Tools\MSVC directory, for example:
    ```
    .VS2019_BasePath        = 'C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC'    // <-- Set path here
    .VS2019_Version         = '14.29.30133' // <-- Set version here
    .VS2019_MSC_VER         = '1929' // <-- Set MSC_VER here
    ```

- Update the `.Windows10_SDKBasePath` and `.Windows10_SDKVersion` in `External\SDK\Windows\Windows10SDK.bff`, you can check the version in `.Windows10_SDKBasePath/bin`.
    ```
    .Windows10_SDKBasePath        = 'C:\Program Files (x86)\Windows Kits/10'    // <-- Set path here
    .Windows10_SDKVersion         = '10.0.19041.0' // <-- Set version here
    ```

- Update the .Clang11_BasePath and .Clang11_Version in External\SDK\Clang\Windows\Clang11.bff file, the path is in .VS2019_BasePath\Tools\LLVM\x64.
    ```
    .Clang11_BasePath = 'C:/Program Files (x86)/Microsoft Visual Studio/2019/Professional/VC/Tools/LLVM/x64'    // <-- Set path here
    .Clang11_Version  = '12.x.x'
    ```

- Enter the Code directory and execute `FBuild.exe All-x64-Release` in the command prompt. If the configuration is correct, you should see a successful compilation. You can find FBuild.exe in tmp\x64-Release\Tools\FBuild\FBuild.

`FBuild.exe All-x64-Release -dist -coordinator=127.0.0.1` enables distributed compilation.

###More Options

The FBuild that I provide supports the following commonly used options:

- coordinator: Specify the Coordinator IP address (can override the value of the system's environment variable)
- brokerage: Specifies the address of the brokerage (which can override the value of the system environment variable)
- nocache: Force not to use cache
- dist: Enable distributed compilation
- forceremote: Force compilation on the remote machine.
- summary: After editing, output a summary report.

Wait a moment, for more options you can run `FBuild.exe -help` to check.

The commonly used options for FBuildWorker are:

- coordinator: Specify the Coordinator IP address (can override the value of system environment variables)
- brokerage: Specify the Brokerage address (can override the value of system environment variables).
- nocache: Force to not use cache.
- cpus: Specify the number of cores allocated for compilation.

To see more options, you can run `FBuildWorder.exe -help`.

###Modify the FASTBuild.cs file that comes with UE.

The built-in FASTBuild.cs in UE does not handle system environment variables very well in relation to the parameters specified in BuildConfiguration.xml. Many parameters prioritize reading the system environment variables, which clearly contradicts the logic of using BuildConfiguration.xml.

To do this, you can modify the relevant code like this, using UE5.3 as an example:

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

###**BuildConfiguration.xml** Advanced Configuration

```xml
<?xml version="1.0" encoding="utf-8" ?>
<Configuration xmlns="https://www.unrealengine.com/BuildConfiguration">
    <ProjectFileGenerator>
<!-- Specify VS version -->
        <Format>VisualStudio2022</Format>
    </ProjectFileGenerator>
    <BuildConfiguration>
<!-- Enable FASTBuild -->
        <bAllowFASTBuild>true</bAllowFASTBuild>
<!-- Specifies the number of CPU cores used for compilation on the local machine -->
        <MaxParallelActions>12</MaxParallelActions>
<!-- Close Incredibuild -->
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
<!-- Cache read and write permissions: Read/Write/ReadWrite -->
        <CacheMode>ReadWrite</CacheMode>
<!-- Specify coordinator IP -->
        <FBuildCoordinator>127.0.0.1</FBuildCoordinator>
<!-- Force remote compilation -->
        <!-- <bForceRemote>true</bForceRemote> -->
    </FASTBuild>
</Configuration>
```

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki_blog/issues/new) if any omissions.
