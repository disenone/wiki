---
layout: post
title: 使用 FASTBuild 编译 UE4 和 UE5
date: 2023-12-01
categories: [c++, python]
catalog: true
tags: [dev, game, ue, UnreanEngine]
description: |
    UE 原生对 FASTBuild 支持不太完善，为了让 UE4 和 UE5 完美支持 FASTBuild，我们需要做一些配置和源码修改，下面为你一一道来。
figures: []
---
<meta property="og:title" content="使用 FASTBuild 编译 UE4 和 UE5" />
<!-- no translate -->

> 本文方法经测试支持 UE4.27 - UE5.3，其他版本未测试过，可以尝试。

## 前言

[FASTBuild](https://www.fastbuild.org/docs/home.html) 是一个免费开源的分布式编译工具，UE 本身编译比较耗时，如果可以用上 FASTBuild，能够大大减少耗时。

UE 从 4.x 开始能够支持 FASTBuild，官方源码自带了魔改过的 FASTBuild 工具，基于 FASTBuild 0.99 版本，位置在 `Engine\Extras\ThirdPartyNotUE\FASTBuild`，UE5.3 同样使用的是这个版本。这个已经是比较久以前的版本了，截止本文创建时间，FASTBuild 官方最新版本是 1.11，有了更多新的功能支持和 bug 修复。本文着重记录如何使用 1.11 版本同时支持 UE4 和 UE5。

## 简易配置

要达到目的，我们需要对 FASTBuild 1.11 和 UE 源码做一些修改。在这里，其实我已经都修改完了，于是我们可以直接用我修改完的版本来使用。

FASTBuild 下载我提交的 [最新版本](https://github.com/disenone/fastbuild/releases) 里面的执行文件 FBuild.exe, FBuildCoordinator.exe, FBuildWorker.exe。为了清晰表达，下面把使用 FBuild.exe 来进行编程的机器叫做`本机`，其他提供 CPU 参与编辑的远程机器叫做`远程机`。

### 本机配置

把 FBuild.exe 所在目录加入系统环境变量 Path 中，保证 cmd 里面能直接执行 FBuild.exe。

配置 Cache 共享目录（如果不需要生成 Cache 的话，可以不配置）：把一个空目录设置成共享路径，并确认远程机可以访问。

打开本机 UE4 / UE5 的源码项目，修改编译配置文件 Engine\Saved\UnrealBuildTool\BuildConfiguration.xml 如下：

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

本机运行之前下载的 FBuildCoordinator.exe。

### 远程机配置

同样配置 Cache，只是 ip 需要指定到本机 ip，这里假定为 192.168.1.100
  - FASTBUILD_CACHE_PATH: \\192.168.1.100\Cache
  - FASTBUILD_CACHE_MODE: rw

同样配置 Coordinator ip
  - FASTBUILD_COORDINATOR: 192.168.1.100

配置完如下图

![](assets/img/2023-ue-fastbuild/remote_vars.png)

远程机上运行 FBuildWorker.exe，如果配置成功，可以看到本机的 FBuildCoordinator.exe 上会打印日志（这里 192.168.1.101 是远程机的 ip）：

```
FBuildCoordinator - v1.11-UE
[2023-12-01-20:06:38] Listening on port 31392
[2023-12-01-20:06:38] current [0] workers: []
[2023-12-01-20:06:42] New worker available: 192.168.1.101
[2023-12-01-20:06:42] current [1] workers: [192.168.1.101]
```

### 测试 UE 编译

用 VisualStudio 打开 UE 源码工程 sln，选一个 C++ 的项目，点击 Rebuild。如果配置正常，可以看到类似如下的日志

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

FASTBuild 能找到远程机的 ip，并开始给远程机发送编译。在远程机的 FBuildWorker 上也能看到当前有编译任务在执行。

## 进阶配置

### 支持更久版本的 UE

如果你发现自己的 UE 没有 FASTBuild 工具（Engine\Extras\ThirdPartyNotUE\FASTBuild），并且项目 UnrealBuildTool 里面没有 FASTBuild.cs 文件，那么很大概率是你的 UE 版本还不支持 FASTBuild。

那么你需要参考 UE4.27 的源码，也创建一个类似的 FASTBuild.cs，并补上其他相关代码的修改，这里不详述。


### 编译自己的 FASTBuild

如果你对 FASTBuild 本身也感兴趣，或者想要做一些修改，可以尝试用 FASTBuild 来编译 FASTBuild。

- 下载我的 [最新源码](https://github.com/disenone/fastbuild/releases)，并解压
- 修改 External\SDK\VisualStudio\VS2019.bff，把 .VS2019_BasePath 和 .VS2019_Version 修改成你本机对应的内容，Version 可以在 .VS2019_BasePath\Tools\MSVC 目录下面看，例如
    ```
    .VS2019_BasePath        = 'C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC'    // <-- Set path here
    .VS2019_Version         = '14.29.30133' // <-- Set version here
    .VS2019_MSC_VER         = '1929' // <-- Set MSC_VER here
    ```

- 修改 External\SDK\Windows\Windows10SDK.bff 的 .Windows10_SDKBasePath 和 .Windows10_SDKVersion，版本可以在 .Windows10_SDKBasePath/bin 里面看：
    ```
    .Windows10_SDKBasePath        = 'C:\Program Files (x86)\Windows Kits/10'    // <-- Set path here
    .Windows10_SDKVersion         = '10.0.19041.0' // <-- Set version here
    ```

- 修改 External\SDK\Clang\Windows\Clang11.bff 的 .Clang11_BasePath 和 .Clang11_Version，路径在 .VS2019_BasePath\Tools\Tools/LLVM/x64
    ```
    .Clang11_BasePath = 'C:/Program Files (x86)/Microsoft Visual Studio/2019/Professional/VC/Tools/LLVM/x64'    // <-- Set path here
    .Clang11_Version  = '12.x.x'
    ```

- 进入 Code 目录，在 cmd 执行 `FBuild.exe All-x64-Release`，如果配置正常，可以看到编译成功，在 tmp\x64-Release\Tools\FBuild\FBuild 能看到 FBuild.exe。

- `FBuild.exe All-x64-Release -dist -coordinator=127.0.0.1` 可以开启分布式编译。

### FBuild 更多选项

我提供的 FBuild 本身支持以下常用的选项：

- coordinator: 指定 Coordinator ip 地址（可以覆盖系统环境变量的值）
- brokerage: 指定 Brokerage 地址（可以覆盖系统环境变量的值）
- nocache：强制不使用 cache
- dist：开启分布式编译
- forceremote：强制在远程机编译
- summary: 编辑结束后输出统计报告

等等，更多选项可以运行 `FBuild.exe -help` 来看。

FBuildWorker 常用的选项有：

- coordinator: 指定 Coordinator ip 地址（可以覆盖系统环境变量的值）
- brokerage: 指定 Brokerage 地址（可以覆盖系统环境变量的值）
- nocache：强制不使用 cache
- cpus: 指定分配多少个核参与编译

更多选项可以运行 `FBuildWorder.exe -help` 来看。

### 修改 UE 自带的 FASTBuild.cs

UE 自带的 FASTBuild.cs 并没有很好的处理系统环境变量，跟 BuildConfiguration.xml 指定的参数的关系，很多参数是优先读取了系统环境变量，这显然跟 BuildConfiguration.xml 的使用逻辑是相反的。

为此，可以把相关的代码改成这样，这里以 UE5.3 为例：

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

### BuildConfiguration.xml 进阶配置

```xml
<?xml version="1.0" encoding="utf-8" ?>
<Configuration xmlns="https://www.unrealengine.com/BuildConfiguration">
    <ProjectFileGenerator>
        <!-- 指定vs版本 -->
        <Format>VisualStudio2022</Format>   
    </ProjectFileGenerator>
    <BuildConfiguration>
        <!-- 开启 FASTBuild -->
        <bAllowFASTBuild>true</bAllowFASTBuild>
        <!-- 指定本机参与编译的 cpu 核数 -->
        <MaxParallelActions>12</MaxParallelActions>
        <!-- 关闭 Incredibuild -->
        <bAllowXGE>false</bAllowXGE>
    </BuildConfiguration>
    <FASTBuild>
        <!-- 指定 FBuild 路径 -->
        <FBuildExecutablePath>d:\libs\FASTBuild\bin\FBuild.exe</FBuildExecutablePath>
        <!-- 开启分布式编译 -->
        <bEnableDistribution>true</bEnableDistribution>
        <!-- 指定 brokerage 路径 -->
        <FBuildBrokeragePath>\\127.0.0.1\Brokerage\</FBuildBrokeragePath>
        <!-- 指定 cache 路径 -->
        <FBuildCachePath>\\127.0.0.1\Cache\</FBuildCachePath>
        <!-- 开启 cache -->
        <bEnableCaching>true</bEnableCaching>
        <!-- cache 的读写权限 Read/Write/ReadWrite -->
        <CacheMode>ReadWrite</CacheMode>
        <!-- 指定 coordinator ip -->
        <FBuildCoordinator>192.168.88.187</FBuildCoordinator>
        <!-- 强制远程编译 -->
        <!-- <bForceRemote>true</bForceRemote> -->
    </FASTBuild>
</Configuration>
```

--8<-- "footer.md"
