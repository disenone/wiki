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
description: UE 原生對 FASTBuild 支援不太完善，為了讓 UE4 和 UE5 完美支援 FASTBuild，我們需要做一些配置和源碼修改，下面為你一一道來。
figures: []
---

<meta property="og:title" content="使用 FASTBuild 编译 UE4 和 UE5" />

> 本文方法經過測試支援 UE4.27 - UE5.3，其他版本尚未測試，您可以嘗試一下。

##前言

[FASTBuild](https://www.fastbuild.org/docs/home.html)是一個免費開源的分佈式編譯工具，UE 本身編譯比較耗時，如果可以使用 FASTBuild，能夠大大減少耗時。

UE 從 4.x 開始能夠支持 FASTBuild，官方原始碼內建了經過改良的 FASTBuild 工具，基於 FASTBuild 0.99 版本，位於 `Engine\Extras\ThirdPartyNotUE\FASTBuild`，UE5.3 同樣使用這個版本。這已經是相當久以前的版本了，截至本文建立時間，FASTBuild 官方最新版本是 1.11，具備更多新功能支援和錯誤修復。本文著重記錄如何使用 1.11 版本同時支援 UE4 和 UE5。

##簡易配置

為了達到目標，我們需要對FASTBuild 1.11和UE源碼進行一些修改。其實，這些修改我已經完成了，所以我們可以直接使用我修改過的版本。

FASTBuild 下載我提交的 [最新版本](https://github.com/disenone/fastbuild/releases)裡面的執行檔 FBuild.exe, FBuildCoordinator.exe, FBuildWorker.exe。為了清晰表達，下面把使用 FBuild.exe 來進行編程的機器叫做`本機`，其他提供 CPU 參與編輯的遠端機器叫做`遠端機`。

###本機配置

將 FBuild.exe 所在目錄添加到系統環境變量 Path 中，以確保可以在 cmd 中直接執行 FBuild.exe。

配置 Cache 共享目錄（如果不需要生成 Cache 的話，可以不配置）：把一個空目錄設置成共享路徑，並確認遠端機可以訪問。

開啟本地的 UE4 / UE5 源碼項目，並修改編譯配置文件 Engine\Saved\UnrealBuildTool\BuildConfiguration.xml 如下：

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

在執行本機之前，請下載 FBuildCoordinator.exe。

###遠程機配置

同樣配置 Cache，只是 ip 需要指定到本機 ip，這裡假定為 192.168.1.100

- FASTBUILD_CACHE_PATH: \\192.168.1.100\Cache
- FASTBUILD_CACHE_MODE: rw

同樣配置 協調器 IP

- FASTBUILD_COORDINATOR: 192.168.1.100

配置完成如下圖

![](assets/img/2023-ue-fastbuild/remote_vars.png)

在遠端機器上運行 FBuildWorker.exe，若設定成功，可以在本機的 FBuildCoordinator.exe 上看到日誌輸出（這裡的 192.168.1.101 為遠端機器的 IP）：

```
FBuildCoordinator - v1.11-UE
[2023-12-01-20:06:38] Listening on port 31392
[2023-12-01-20:06:38] current [0] workers: []
[2023-12-01-20:06:42] New worker available: 192.168.1.101
[2023-12-01-20:06:42] current [1] workers: [192.168.1.101]
```

###測試 UE 編譯

用 VisualStudio 打開 UE 源碼工程 sln，選擇一個 C++ 的項目，點擊 Rebuild。如果配置正常，可以看到類似如下的日誌

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

FASTBuild 能找到遠程機的 IP，並開始給遠程機發送編譯。在遠程機的 FBuildWorker 上也能看到當前有編譯任務在執行。

##進階配置

###支持更舊版本的 UE

如果你發現自己的 UE 沒有 FASTBuild 工具（Engine\Extras\ThirdPartyNotUE\FASTBuild），並且項目 UnrealBuildTool 裡面沒有 FASTBuild.cs 文件，那麼很大概率是你的 UE 版本還不支持 FASTBuild。

那麼你需要參考 UE4.27 的源碼，也創建一個類似的 FASTBuild.cs，並補上其他相關代碼的修改，這裡不詳述。


###編譯自己的 FASTBuild

如果你對 FASTBuild 本身也感興趣，或者想要做一些修改，可以嘗試用 FASTBuild 來編譯 FASTBuild。

- 下載我的 [最新源碼](https://github.com/disenone/fastbuild/releases)，並解壓
- 修改 External\SDK\VisualStudio\VS2019.bff，把 .VS2019_BasePath 和 .VS2019_Version 修改成你本機對應的內容，Version 可以在 .VS2019_BasePath\Tools\MSVC 目錄下面查看，例如
    ```
    .VS2019_BasePath        = 'C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC'    // <-- Set path here
    .VS2019_Version         = '14.29.30133' // <-- Set version here
    .VS2019_MSC_VER         = '1929' // <-- Set MSC_VER here
    ```

- 修改 External\SDK\Windows\Windows10SDK.bff 的 .Windows10_SDKBasePath 和 .Windows10_SDKVersion，版本可以在 .Windows10_SDKBasePath/bin 裡面看：
    ```
    .Windows10_SDKBasePath        = 'C:\Program Files (x86)\Windows Kits/10'    // <-- Set path here
    .Windows10_SDKVersion         = '10.0.19041.0' // <-- Set version here
    ```

- 修改 External\SDK\Clang\Windows\Clang11.bff 的 .Clang11_BasePath 和 .Clang11_Version，路徑在 .VS2019_BasePath\Tools\Tools/LLVM/x64
    ```
    .Clang11_BasePath = 'C:/Program Files (x86)/Microsoft Visual Studio/2019/Professional/VC/Tools/LLVM/x64'    // <-- Set path here
    .Clang11_Version  = '12.x.x'
    ```

進入 Code 目錄，透過 cmd 執行 `FBuild.exe All-x64-Release`。如果配置正常，將看到編譯成功的訊息，並且在 tmp\x64-Release\Tools\FBuild\FBuild 資料夾中會看到 FBuild.exe。

`FBuild.exe All-x64-Release -dist -coordinator=127.0.0.1` 可以啟動分布式編譯。

###FBuild 更多選項

我提供的FBuild本身支持以下常用的選項：

- coordinator: 指定 Coordinator IP 地址（可以覆蓋系統環境變數的值）
- brokerage: 指定 Brokerage 地址（可以覆蓋系統環境變量的值）
nocache：強制不使用快取
- dist：開啟分佈式編譯
- forceremote：強制在遠程機編譯
- summary: 編輯結束後輸出統計報告

等等，您可以运行 `FBuild.exe -help` 来查看更多选项。

FBuildWorker常見的選項有：

- coordinator: 指定協調器 Coordinator IP 地址（可以覆蓋系統環境變數的值）
- brokerage: 指定經紀商地址（可以覆蓋系統環境變數的值）
- nocache：強制不使用快取
- cpus: 指定分配多少個核心參與編譯

運行 `FBuildWorder.exe -help` 可以查看更多選項。

###修改 UE 自帶的 FASTBuild.cs

UE 自帶的 FASTBuild.cs 並沒有很好的處理系統環境變數，跟 BuildConfiguration.xml 指定的參數的關係，很多參數是優先讀取了系統環境變數，這顯然跟 BuildConfiguration.xml 的使用邏輯是相反的。

為此，可以將相關的程式碼修改為這樣，這裡以UE5.3為例：

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

###BuildConfiguration.xml 進階配置

```xml
<?xml version="1.0" encoding="utf-8" ?>
<Configuration xmlns="https://www.unrealengine.com/BuildConfiguration">
    <ProjectFileGenerator>
<!-- 指定vs版本 -->
        <Format>VisualStudio2022</Format>
    </ProjectFileGenerator>
    <BuildConfiguration>
<!-- 啟用 FASTBuild -->
        <bAllowFASTBuild>true</bAllowFASTBuild>
指定本機參與編譯的 CPU 核數
        <MaxParallelActions>12</MaxParallelActions>
<!-- 關閉Incredibuild -->
        <bAllowXGE>false</bAllowXGE>
    </BuildConfiguration>
    <FASTBuild>
<!-- 指定 FBuild 路徑 -->
        <FBuildExecutablePath>d:\libs\FASTBuild\bin\FBuild.exe</FBuildExecutablePath>
<!-- 啟用分散式編譯 -->
        <bEnableDistribution>true</bEnableDistribution>
<!-- 指定經紀公司路徑 -->
        <FBuildBrokeragePath>\\127.0.0.1\Brokerage\</FBuildBrokeragePath>
<!-- 指定快取路徑 -->
        <FBuildCachePath>\\127.0.0.1\Cache\</FBuildCachePath>
<!-- 啟用快取 -->
        <bEnableCaching>true</bEnableCaching>
<!-- 快取的讀寫權限 Read/Write/ReadWrite -->
        <CacheMode>ReadWrite</CacheMode>
<!-- 指定協調器 IP -->
        <FBuildCoordinator>127.0.0.1</FBuildCoordinator>
        <!-- 強制遠程編譯 -->
        <!-- <bForceRemote>true</bForceRemote> -->
    </FASTBuild>
</Configuration>
```

--8<-- "footer_tc.md"


> 此帖文乃透過 ChatGPT 翻譯，煩請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遺漏之處。 
