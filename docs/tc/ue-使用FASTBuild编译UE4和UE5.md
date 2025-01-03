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

> 本文方法經過測試支援 UE4.27 - UE5.3，其他版本未經測試，可嘗試。

##前言

[FASTBuild](https://www.fastbuild.org/docs/home.html)FASTBuild 是一個免費開源的分散式編譯工具，UE 本身的編譯比較耗時，如果能夠應用 FASTBuild，將大幅縮短編譯時間。

UE從4.x版本開始支持FASTBuild，官方原始碼自帶修改過的FASTBuild工具，基於FASTBuild 0.99版本，在 `Engine\Extras\ThirdPartyNotUE\FASTBuild` 資料夾中，UE5.3亦使用這個版本。此為較早的版本，截至本文創建時，FASTBuild 官方最新版本為1.11，帶來更多新功能和錯誤修復。本文重點記錄如何使用1.11版本同時支持UE4和UE5。

##簡易配置

為了達成目標，我們需要對 FASTBuild 1.11 和 UE 的原始碼做一些修改。其實，我已經完成了這些修改，因此我們可以直接使用我修改過的版本。

FASTBuild 下載我提交的[最新版本](https://github.com/disenone/fastbuild/releases)裡面的執行檔 FBuild.exe、FBuildCoordinator.exe 和 FBuildWorker.exe。為了表達清晰，以下將使用 FBuild.exe 進行編程的機器稱為「本機」，其他提供 CPU 參與編輯的遠端機器則稱為「遠端機」。

###本機配置

將 FBuild.exe 所在目錄加入系統環境變數 Path 中，確保在 cmd 裡可以直接執行 FBuild.exe。

設置 Cache 共享目錄（如果不需要生成 Cache 的話，可以不配置）：將一個空目錄設置為共享路徑，並確認遠端機器可以訪問。

打開本機 UE4 / UE5 的源碼專案，修改編譯配置文件 Engine\Saved\UnrealBuildTool\BuildConfiguration.xml 如下：

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

請安裝 FBuildCoordinator.exe，此為本機上運行所需的程式。

###遠程機配置

同樣配置Cache，只是 IP 需要指定到本機 IP，這裡假定為 192.168.1.100。

- FASTBUILD_CACHE_PATH: \\192.168.1.100\Cache
- FASTBUILD_CACHE_MODE: rw

同樣配置 Coordinator IP

- FASTBUILD_COORDINATOR: 192.168.1.100

配置完如下圖

![](assets/img/2023-ue-fastbuild/remote_vars.png)

在遠端機器上運行 FBuildWorker.exe，若設定成功，您可以在本機的 FBuildCoordinator.exe 上看到日誌輸出（這裡 192.168.1.101 是遠端機器的 IP）：

```
FBuildCoordinator - v1.11-UE
[2023-12-01-20:06:38] Listening on port 31392
[2023-12-01-20:06:38] current [0] workers: []
[2023-12-01-20:06:42] New worker available: 192.168.1.101
[2023-12-01-20:06:42] current [1] workers: [192.168.1.101]
```

###測試 UE 編譯

使用 VisualStudio 開啟 UE 源碼專案的sln檔案，選擇其中一個 C++ 專案，然後點擊 Rebuild。如果配置正確，您將會看到類似以下的日誌信息。

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

FASTBuild 能夠找到遠端機器的 IP，並開始傳送編譯任務至遠端機器。在遠端機器的 FBuildWorker 上也可以看到目前正在執行的編譯任務。

##升級設定

###支持更老的 UE 版本。

若您發現自己的 UE 沒有 FASTBuild 工具（Engine\Extras\ThirdPartyNotUE\FASTBuild），且在專案 UnrealBuildTool 裡找不到 FASTBuild.cs 檔案，很可能是由於您的 UE 版本尚未支援 FASTBuild。

您需要參考 UE4.27 的原始碼，同時建立一個類似的 FASTBuild.cs 檔案，並對其他相關代碼進行修改。這裡不詳述。


###編譯自己的 FASTBuild

如果你對 FASTBuild 本身也感興趣，或者想要做一些修改，可以嘗試用 FASTBuild 來編譯 FASTBuild。

下載我的[最新源碼](https://github.com/disenone/fastbuild/releases)請解壓縮
- 修改 External\SDK\VisualStudio\VS2019.bff，將 .VS2019_BasePath 和 .VS2019_Version 修改為您本機對應的內容，Version 可以在 .VS2019_BasePath\Tools\MSVC 目錄下面看，例如
    ```
    .VS2019_BasePath        = 'C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC'    // <-- Set path here
    .VS2019_Version         = '14.29.30133' // <-- Set version here
    .VS2019_MSC_VER         = '1929' // <-- Set MSC_VER here
    ```

請修改 External\SDK\Windows\Windows10SDK.bff 檔案中的 .Windows10_SDKBasePath 和 .Windows10_SDKVersion，版本可以在 .Windows10_SDKBasePath/bin 目錄中找到：
    ```
    .Windows10_SDKBasePath        = 'C:\Program Files (x86)\Windows Kits/10'    // <-- Set path here
    .Windows10_SDKVersion         = '10.0.19041.0' // <-- Set version here
    ```

請修改 External\SDK\Clang\Windows\Clang11.bff 的 .Clang11_BasePath 和 .Clang11_Version，路徑位置在 .VS2019_BasePath\Tools\Tools/LLVM/x64。
    ```
    .Clang11_BasePath = 'C:/Program Files (x86)/Microsoft Visual Studio/2019/Professional/VC/Tools/LLVM/x64'    // <-- Set path here
    .Clang11_Version  = '12.x.x'
    ```

進入 Code 目錄，在 cmd 執行 `FBuild.exe All-x64-Release`，如果配置正常，可以看到編譯成功，在 tmp\x64-Release\Tools\FBuild\FBuild 能看到 FBuild.exe。

執行 `FBuild.exe All-x64-Release -dist -coordinator=127.0.0.1` 可以啟動分佈式編譯。

###擴展更多選項

我提供的 FBuild 本身支援以下常用的選項：

- coordinator: 指定協調者 IP 地址（可覆蓋系統環境變數的值）
- brokerage: 指定 Brokerage 地址（可以覆盖系統環境變量的值）
- nocache: 強制不使用快取
- dist：啟用分散式編譯
- forceremote: 強制在遠程機編譯
總結：編輯完成後輸出統計報告

請稍等，您可以運行 `FBuild.exe -help` 來查看更多選項。

FBuildWorker 常用的選項有：

協調者: 指定 Coordinator IP 位址（可以覆蓋系統環境變數的值）
- brokerage: 指定 Brokerage 地址（可以覆蓋系統環境變數的值）
- nocache: 強制不使用快取
- cpus: 指定分配多少個核心參與編譯

運行 `FBuildWorder.exe -help` 以查看更多選項。

###修改 UE 自帶的 FASTBuild.cs

UE 自帶的 FASTBuild.cs 並沒有很好地處理系統環境變數，跟 BuildConfiguration.xml 指定的參數的關係，很多參數是優先讀取了系統環境變數，這顯然跟 BuildConfiguration.xml 的使用邏輯是相反的。

因此，您可以將相關的程式碼更改為以下形式，這裡以UE5.3為例：

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

###繁體中文翻譯：BuildConfiguration.xml 進階配置

```xml
<?xml version="1.0" encoding="utf-8" ?>
<Configuration xmlns="https://www.unrealengine.com/BuildConfiguration">
    <ProjectFileGenerator>
<!-- 指定輸入版本 -->
        <Format>VisualStudio2022</Format>
    </ProjectFileGenerator>
    <BuildConfiguration>
<!-- 啟用FASTBuild -->
        <bAllowFASTBuild>true</bAllowFASTBuild>
<!-- 指定本機參與編譯的 CPU 核心數 -->
        <MaxParallelActions>12</MaxParallelActions>
<!-- 關閉 Incredibuild -->
        <bAllowXGE>false</bAllowXGE>
    </BuildConfiguration>
    <FASTBuild>
<!-- 指定 FBuild 路徑 -->
        <FBuildExecutablePath>d:\libs\FASTBuild\bin\FBuild.exe</FBuildExecutablePath>
<!--啟用分散式編譯-->
        <bEnableDistribution>true</bEnableDistribution>
<!-- 指定券商路徑 -->
        <FBuildBrokeragePath>\\127.0.0.1\Brokerage\</FBuildBrokeragePath>
指定快取路徑
        <FBuildCachePath>\\127.0.0.1\Cache\</FBuildCachePath>
<!--啟用快取-->
        <bEnableCaching>true</bEnableCaching>
<!-- 快取的讀寫權限 Read/Write/ReadWrite -->
        <CacheMode>ReadWrite</CacheMode>
<!-- 指定協調器 IP -->
        <FBuildCoordinator>127.0.0.1</FBuildCoordinator>
<!-- 強制遠端編譯 -->
        <!-- <bForceRemote>true</bForceRemote> -->
    </FASTBuild>
</Configuration>
```

--8<-- "footer_tc.md"


> 此貼文是透過 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
