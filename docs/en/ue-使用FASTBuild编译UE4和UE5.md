---
layout: post
title: Compile UE4 and UE5 using FASTBuild.
date: 2023-12-01
categories:
- c++
- python
catalog: true
tags: [dev, game, ue, UnreanEngine]
description: The native support for FASTBuild in UE is not quite perfect. In order
  to ensure flawless FASTBuild support for both UE4 and UE5, we need to make some
  configuration and source code modifications. Let me guide you through them one by
  one.
figures: []
---

<meta property="og:title" content="使用 FASTBuild 编译 UE4 和 UE5" />

This method has been tested and supports UE4.27 - UE5.3. Other versions have not been tested, but you can give it a try.

## Preface

[FASTBuild](https://www.fastbuild.org/docs/home.html) is a free and open-source distributed compilation tool. The compilation process of UE itself is quite time-consuming, but by using FASTBuild, it is possible to significantly reduce the time required.

Starting from UE 4.x, it is able to support FASTBuild. The official source code comes with a modified version of FASTBuild tool, based on version 0.99 of FASTBuild. Its location is `Engine\Extras\ThirdPartyNotUE\FASTBuild`. UE5.3 also uses this version. However, this is a relatively old version. As of the creation time of this article, the latest official version of FASTBuild is 1.11, which provides more new features and bug fixes. This article focuses on how to use version 1.11 to support both UE4 and UE5 simultaneously.

## Easy Configuration

To achieve the goal, we need to make some modifications to FASTBuild 1.11 and the UE source code. Here, in fact, I have already made all the modifications, so we can directly use the version I have modified.

Download the executable files FBuild.exe, FBuildCoordinator.exe, and FBuildWorker.exe from the [latest version](https://github.com/disenone/fastbuild/releases) that I submitted. In order to better illustrate, the machine that uses FBuild.exe for programming will be referred to as `local machine`, while the remote machines that provide CPU participation for editing will be referred to as `remote machines`.

### Local Configuration

Add the directory where FBuild.exe is located to the system environment variable `Path`, to ensure that FBuild.exe can be executed directly in the `cmd` command prompt.

Configure Cache Shared Directory (If Cache generation is not needed, this configuration can be skipped): Set an empty directory as a shared path and ensure that the remote machine has access to it.

Open the source code project of your local UE4/UE5. Modify the compilation configuration file Engine\Saved\UnrealBuildTool\BuildConfiguration.xml as follows:


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

Run the downloaded FBuildCoordinator.exe on this machine.

### Remote Machine Configuration

With the same configuration as Cache, only the IP needs to be set to the local IP, assuming it is 192.168.1.100.
  - FASTBUILD_CACHE_PATH: \\192.168.1.100\Cache
  - FASTBUILD_CACHE_MODE: rw

[Same configuration Coordinator IP]
  - FASTBUILD_COORDINATOR: 192.168.1.100

After configuring, it should look like the following image.

![](assets/img/2023-ue-fastbuild/remote_vars.png)

Run FBuildWorker.exe on the remote machine. If the configuration is successful, logs will be printed on the FBuildCoordinator.exe of the local machine (here, 192.168.1.101 is the IP address of the remote machine):

```
FBuildCoordinator - v1.11-UE
[2023-12-01-20:06:38] Listening on port 31392
[2023-12-01-20:06:38] current [0] workers: []
[2023-12-01-20:06:42] New worker available: 192.168.1.101
[2023-12-01-20:06:42] current [1] workers: [192.168.1.101]
```

### Test UE Compilation

Open the UE source code project sln with VisualStudio, select a C++ project, and click Rebuild. If the configuration is correct, you will see logs similar to the following:

```
11>FBuild Command Line Arguments: '-monitor -summary -dist -cache -ide -j12 -clean -config "E:\UE\ue5.3_git\Engine\Intermediate\Build\fbuild.bff" -nostoponerror
11>FBuild Executable: 'd:\libs\FASTBuild\bin\FBuild.exe
11>FBuild Coordinator: '127.0.0.1
11>FBuild BrokeragePath: '\\127.0.0.1\Brokerage\
11>FBuild CachePath: '\\127.0.0.1\Cache\
11>BFF file 'E:\UE\ue5.3_git\Engine\Intermediate\Build\fbuild.bff' has changed (reparsing will occur).
11>Using Coordinator: 192.168.88.187
11>Requesting worker list from Corrdinator
11>Get Worker List from Coordinator.
11>2 workers in payload: [192.168.1.101]
11>Worker list received: 1 workers
11>Distributed Compilation : 1 Workers in pool '127.0.0.1'
```

FASTBuild can find the IP address of the remote machine and start sending the compilation tasks to it. On the FBuildWorker of the remote machine, you can also see that there are currently compilation tasks being executed.

## Advanced Configuration

### Support for older versions of UE

If you find that your UE doesn't have the FASTBuild tool (Engine\Extras\ThirdPartyNotUE\FASTBuild), and there is no FASTBuild.cs file in the UnrealBuildTool project, it's highly likely that your UE version does not support FASTBuild yet.

So you need to refer to the source code of UE4.27 and create a similar FASTBuild.cs file, and make the necessary modifications to other related code. No further details will be provided here.


### Compile your own FASTBuild

If you are also interested in FASTBuild itself, or want to make some modifications, you can try using FASTBuild to compile FASTBuild.

- Download my [latest source code](https://github.com/disenone/fastbuild/releases) and unzip it.
- Modify External\SDK\VisualStudio\VS2019.bff, change .VS2019_BasePath and .VS2019_Version to the corresponding values on your machine. You can find the Version in the .VS2019_BasePath\Tools\MSVC directory, for example...
    ```
    .VS2019_BasePath        = 'C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC'    // <-- Set path here
    .VS2019_Version         = '14.29.30133' // <-- Set version here
    .VS2019_MSC_VER         = '1929' // <-- Set MSC_VER here
    ```

- Modify the .Windows10_SDKBasePath and .Windows10_SDKVersion in External\SDK\Windows\Windows10SDK.bff file. The version can be found inside .Windows10_SDKBasePath/bin folder.
    ```
    .Windows10_SDKBasePath        = 'C:\Program Files (x86)\Windows Kits/10'    // <-- Set path here
    .Windows10_SDKVersion         = '10.0.19041.0' // <-- Set version here
    ```

- Update the `.Clang11_BasePath` and `.Clang11_Version` in `External\SDK\Clang\Windows\Clang11.bff`, the path is located in `.VS2019_BasePath\Tools\Tools/LLVM/x64`.
    ```
    .Clang11_BasePath = 'C:/Program Files (x86)/Microsoft Visual Studio/2019/Professional/VC/Tools/LLVM/x64'    // <-- Set path here
    .Clang11_Version  = '12.x.x'
    ```

- Go to the Code directory and execute `FBuild.exe All-x64-Release` in the cmd. If the configuration is correct, you should see a successful compilation. You can find the FBuild.exe in tmp\x64-Release\Tools\FBuild\FBuild.

The command `FBuild.exe All-x64-Release -dist -coordinator=127.0.0.1` enables distributed compilation.

### FBuild More Options

The FBuild I provide itself supports the following commonly used options:

- coordinator: Specify the Coordinator IP address (can override the value of system environment variables)
- brokerage: Specify the Brokerage address (can override the value of system environment variables)
- nocache: Force to not use cache
- dist: Enable distributed compilation
- forceremote: Force to compile on a remote machine
- summary: Output a statistical report after editing is finished

Wait, you can run `FBuild.exe -help` to see more options.

The commonly used options for FBuildWorker are:

- coordinator: Specify the Coordinator IP address (can override the value of the system environment variable).
- brokerage: Specify the Brokerage address (can override the value of the system environment variable).
- nocache: Forcefully disable the use of cache.
- cpus: Specify the number of cores to allocate for compilation.

To see more options, you can run `FBuildWorder.exe -help`.

### Modify the built-in FASTBuild.cs in UE

The built-in FASTBuild.cs provided by UE does not handle system environment variables well in relation to the parameters specified in BuildConfiguration.xml. Many parameters prioritize reading system environment variables, which clearly contradicts the logic of using BuildConfiguration.xml.

To do this, you can modify the relevant code like this, taking UE5.3 as an example here:

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

### Advanced Configuration of BuildConfiguration.xml

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
<!-- Specify the number of CPU cores that will participate in the compilation on the local machine -->
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
<!-- cache read/write permissions Read/Write/ReadWrite -->
        <CacheMode>ReadWrite</CacheMode>
<!-- Specify coordinator ip -->
        <FBuildCoordinator>192.168.88.187</FBuildCoordinator>
<!-- Force remote compilation -->
        <!-- <bForceRemote>true</bForceRemote> -->
    </FASTBuild>
</Configuration>
```

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki_blog/issues/new) if any omissions.
