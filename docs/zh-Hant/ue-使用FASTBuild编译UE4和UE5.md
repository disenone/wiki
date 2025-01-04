---
layout: post
title: 使用 FASTBuild 編譯 UE4 和 UE5
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
description: UE 原生支持 FASTBuild 的程度不太完善，為了讓 UE4 和 UE5 完美支持 FASTBuild，我們需要進行一些設定和原始碼修改，以下將一一為您解說。
figures: []
---

<meta property="og:title" content="使用 FASTBuild 编译 UE4 和 UE5" />

> 本文方法經過測試支持UE4.27 - UE5.3，其他版本未經測試，建議可嘗試。

##前言

[FASTBuild](https://www.fastbuild.org/docs/home.html)FASTBuild是一個免費開源的分散式編譯工具，UE本身的編譯非常耗時，如果能夠使用FASTBuild，將會大大減少所需時間。

UE 從 4.x 版本開始就支援 FASTBuild 了，官方原始碼已經包含了經過修改過的 FASTBuild 工具，基於 FASTBuild 0.99 版本，位置在 `Engine\Extras\ThirdPartyNotUE\FASTBuild`，UE5.3 也同樣使用這個版本。這已經是相當舊的版本了，在本文創建時，FASTBuild 官方最新版本為 1.11，帶來了更多新功能支持和 bug 修復。本文重點記錄如何使用 1.11 版本同時支援 UE4 和 UE5。

##簡易配置

為了達成目標，我們需要對 FASTBuild 1.11 和 UE 源碼做一些修改。在這裡，事實上我已經完成所有修改，因此我們可以直接使用我修改過的版本。

FASTBuild 下載我提交的 [最新版本](https://github.com/disenone/fastbuild/releases)裡面的執行檔 FBuild.exe、FBuildCoordinator.exe、FBuildWorker.exe。為了清晰表達，下面把使用 FBuild.exe 來進行編程的機器叫做`本機`，其他提供 CPU 參與編輯的遠程機器叫做`遠程機`。

###本機配置

將 FBuild.exe 的檔案路徑加入系統環境變數 Path 中，確保在 cmd 中可以直接執行 FBuild.exe。

設置 Cache 共享目錄（若不需要生成 Cache，則可不設置）：將一個空目錄設為共享路徑，確保遠端機器能夠訪問。

打開本機 UE4 / UE5 的源碼項目，修改編譯配置文件 Engine\Saved\UnrealBuildTool\BuildConfiguration.xml 如下：

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

請執行先前下載的 FBuildCoordinator.exe 檔案。

###遠程機配置

同樣配置 Cache，只是 ip 需要指定到本機 ip，這裡假定為 192.168.1.100.

- FASTBUILD_CACHE_PATH: \\192.168.1.100\Cache
- FASTBUILD_CACHE_MODE: rw

同樣配備協調器 IP

- FASTBUILD_COORDINATOR: 192.168.1.100

請見下圖所示的配置。

![](assets/img/2023-ue-fastbuild/remote_vars.png)

在遠端機器上運行 FBuildWorker.exe，如果設置成功，可以看到本機的 FBuildCoordinator.exe 會印出日誌（這裡 192.168.1.101 是遠端機器的 IP）：

```
FBuildCoordinator - v1.11-UE
[2023-12-01-20:06:38] Listening on port 31392
[2023-12-01-20:06:38] current [0] workers: []
[2023-12-01-20:06:42] New worker available: 192.168.1.101
[2023-12-01-20:06:42] current [1] workers: [192.168.1.101]
```

###測試 UE 編譯

使用 VisualStudio 開啟 UE 源碼專案的sln檔案，選擇一個 C++ 專案，然後按下 Rebuild。如果配置正確，便可看到類似以下的日誌信息。

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

FASTBuild 能夠找到遠端機器的 IP，並開始向遠端機器發送編譯任務。在遠端機器的 FBuildWorker 上也能看到目前正在執行的編譯任務。

##提升設定

###支援較舊的 UE 版本

如果你發現自己的 UE 沒有 FASTBuild 工具（Engine\Extras\ThirdPartyNotUE\FASTBuild），並且專案 UnrealBuildTool 裡面沒有 FASTBuild.cs 檔案，那麼很大機率是你的 UE 版本還不支持 FASTBuild。

你需要參考UE4.27的原始碼，同時建立一個類似的FASTBuild.cs檔案，並進行其他相關程式碼的修改。這裡不做詳細說明。


###編譯自己的 FASTBuild

如果你對 FASTBuild 本身也感興趣，或者想要做一些修改，可以嘗試用 FASTBuild 來編譯 FASTBuild。

- 您可以下載我的[最新原始碼](https://github.com/disenone/fastbuild/releases)請稍等片刻，馬上為您翻譯。
請修改 External\SDK\VisualStudio\VS2019.bff，將 .VS2019_BasePath 和 .VS2019_Version 修改為您本機對應的內容，Version 可以在 .VS2019_BasePath\Tools\MSVC 目錄中找到，例如
    ```
    .VS2019_BasePath        = 'C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC'    // <-- Set path here
    .VS2019_Version         = '14.29.30133' // <-- Set version here
    .VS2019_MSC_VER         = '1929' // <-- Set MSC_VER here
    ```

修改 External\SDK\Windows\Windows10SDK.bff 的 .Windows10_SDKBasePath 和 .Windows10_SDKVersion，版本可以在 .Windows10_SDKBasePath/bin 里面看：
    ```
    .Windows10_SDKBasePath        = 'C:\Program Files (x86)\Windows Kits/10'    // <-- Set path here
    .Windows10_SDKVersion         = '10.0.19041.0' // <-- Set version here
    ```

請修改 External\SDK\Clang\Windows\Clang11.bff 中的 .Clang11_BasePath 和 .Clang11_Version，路徑位於 .VS2019_BasePath\Tools\Tools/LLVM/x64。
    ```
    .Clang11_BasePath = 'C:/Program Files (x86)/Microsoft Visual Studio/2019/Professional/VC/Tools/LLVM/x64'    // <-- Set path here
    .Clang11_Version  = '12.x.x'
    ```

進入 Code 目錄，在 cmd 執行 `FBuild.exe All-x64-Release`，如果配置正常，可以看到編譯成功，可以在 tmp\x64-Release\Tools\FBuild\FBuild 看到 FBuild.exe。

使用`FBuild.exe All-x64-Release -dist -coordinator=127.0.0.1`命令可啟用分佈式編譯。

###FBuild 更多選項

我提供的 FBuild 本身支持以下常用的选項：

- coordinator: 指定 Coordinator IP 地址（可以覆蓋系統環境變數的值）
- brokerage: 指定 Brokerage 地址（可以覆蓋系統環境變量的值）
- nocache: 強制不使用快取
- dist：啟用分散式編譯
- forceremote: 強制在遠程機編譯
- 摘要: 編輯完成後輸出統計報告

請稍等，您可以執行 `FBuild.exe -help` 以查看更多選項。

FBuildWorker常用的選項有：

- coordinator: 指定協調者 IP 地址（可以覆蓋系統環境變量的值）
- brokerage: 指定 Brokerage 地址（可以覆蓋系統環境變量的值）
- nocache: 強制不使用快取
- cpus: 指定分配多少個核心參與編譯

可以運行 `FBuildWorder.exe -help` 以查看更多選項。

###修改 UE 自帶的 FASTBuild.cs

UE 自帶的 FASTBuild.cs 並沒有很好的處理系統環境變量，跟 BuildConfiguration.xml 指定的參數的關係，很多參數是優先讀取了系統環境變量，這顯然跟 BuildConfiguration.xml 的使用邏輯是相反的。

為此，可以將相關的程式碼修改如下，這裡以 UE5.3 為例：

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

###建置設定檔案 BuildConfiguration.xml 追加設定

```xml
<?xml version="1.0" encoding="utf-8" ?>
<Configuration xmlns="https://www.unrealengine.com/BuildConfiguration">
    <ProjectFileGenerator>
<!-- 指定 Visual Studio 版本 -->
        <Format>VisualStudio2022</Format>
    </ProjectFileGenerator>
    <BuildConfiguration>
<!-- 啟用 FASTBuild -->
        <bAllowFASTBuild>true</bAllowFASTBuild>
指定本機參與編譯的 CPU 核心數。
        <MaxParallelActions>12</MaxParallelActions>
<!-- 關閉 Incredibuild -->
        <bAllowXGE>false</bAllowXGE>
    </BuildConfiguration>
    <FASTBuild>
<!-- 指定 FBuild 路徑 -->
        <FBuildExecutablePath>d:\libs\FASTBuild\bin\FBuild.exe</FBuildExecutablePath>
<!-- 啟用分散式編譯 -->
        <bEnableDistribution>true</bEnableDistribution>
<!-- 指定經紀商路徑 -->
        <FBuildBrokeragePath>\\127.0.0.1\Brokerage\</FBuildBrokeragePath>
<!-- 指定快取路徑 -->
        <FBuildCachePath>\\127.0.0.1\Cache\</FBuildCachePath>
<!-- 啟用快取 -->
        <bEnableCaching>true</bEnableCaching>
<!-- 緩存的讀寫權限 Read/Write/ReadWrite -->
        <CacheMode>ReadWrite</CacheMode>
<!-- 指定協調器 IP -->
        <FBuildCoordinator>127.0.0.1</FBuildCoordinator>
<!-- 強制遠端編譯 -->
        <!-- <bForceRemote>true</bForceRemote> -->
    </FASTBuild>
</Configuration>
```

--8<-- "footer_tc.md"


> 此文是由 ChatGPT 翻譯，請在 [**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
