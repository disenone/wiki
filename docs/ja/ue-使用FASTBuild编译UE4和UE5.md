---
layout: post
title: 使用 FASTBuild 编译 UE4 和 UE5
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
description: UEの原生FASTBuildサポートは完璧ではないので、UE4とUE5がFASTBuildを完全にサポートするためには、いくつかの設定とソースコードの変更が必要です。以下では、それを一つずつ説明します。
figures: []
---

<meta property="og:title" content="使用 FASTBuild 编译 UE4 和 UE5" />

> 本文の手法は、UE4.27からUE5.3までのテストをサポートしています。他のバージョンについてはテストされていませんが、お試しいただけます。

##序文

[FASTBuild](https://www.fastbuild.org/docs/home.html)無料でオープンソースの分散コンパイルツールで、UE のコンパイル自体が時間がかかりますが、FASTBuild を使用すれば大幅な時間短縮が可能です。

UE は 4.x から FASTBuild をサポートするようになりました。 公式のソースコードには改変された FASTBuild ツールが付属しており、FASTBuild の0.99 バージョンに基づいています。場所は `Engine\Extras\ThirdPartyNotUE\FASTBuild` です。UE5.3 も同じバージョンを使用しています。 これは古いバージョンですが、本文作成時点では FASTBuild の公式最新バージョンは1.11 です。より多くの新機能とバグ修正が加わっています。 本文では、1.11 バージョンを使用して UE4 と UE5 の両方をサポートする方法に焦点を当てます。

##簡単な設定

目的を達成するために、FASTBuild 1.11とUEのソースコードをいくつか変更する必要があります。実は、すでにすべて変更を完了しているので、私が変更したバージョンを直接使用することができます。

FASTBuild の[最新バージョン](https://github.com/disenone/fastbuild/releases)FBuild.exe、FBuildCoordinator.exe、FBuildWorker.exeの実行ファイルが含まれています。明確にするために、プログラミングにFBuild.exeを使用するマシンを「ローカルマシン」と呼び、CPUを提供して編集に参加する他のリモートマシンを「リモートマシン」と呼びます。

###機器設定

FBuild.exe の場所をシステムの環境変数 Path に追加してください。これにより、cmd から直接 FBuild.exe を実行できるようになります。

Cache共有ディレクトリの設定（Cacheの生成が不要な場合は設定しなくても構いません）：空のディレクトリを共有パスとして設定し、リモートマシンがアクセスできることを確認してください。

UE4 / UE5のソースコードプロジェクトを開いて、Engine\Saved\UnrealBuildTool\BuildConfiguration.xmlというコンパイル設定ファイルを以下のように変更してください:

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

本机運行する前にダウンロードした FBuildCoordinator.exe を実行します。

###リモートマシンの設定

同じキャッシュ構成で、ただしIPアドレスはローカルIPに設定する必要があります。ここでは、192.168.1.100 と仮定します。

- FASTBUILD_CACHE_PATH: \\192.168.1.100\Cache
- FASTBUILD_CACHE_MODE: rw

同じ構成の Coordinator IP

- FASTBUILD_COORDINATOR: 192.168.1.100

配置完如下の通りです。

![](assets/img/2023-ue-fastbuild/remote_vars.png)

遠隔で FBuildWorker.exe を実行します。構成が成功すると、ローカルの FBuildCoordinator.exe にログが表示されます（ここで 192.168.1.101 は遠隔コンピュータの IP アドレスです）：

```
FBuildCoordinator - v1.11-UE
[2023-12-01-20:06:38] Listening on port 31392
[2023-12-01-20:06:38] current [0] workers: []
[2023-12-01-20:06:42] New worker available: 192.168.1.101
[2023-12-01-20:06:42] current [1] workers: [192.168.1.101]
```

###UEコンパイルのテスト

VisualStudio で UE のソースコードプロジェクトの .sln を開き、C++ プロジェクトを選択して Rebuild をクリックします。正しく構成されている場合、以下のようなログが表示されるはずです。

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

FASTBuildは、リモートマシンのIPアドレスを見つけ、リモートマシンにコンパイルを開始します。リモートマシンのFBuildWorkerでは、現在実行中のコンパイルタスクが表示されます。

##上級設定

###より古いバージョンのUEをサポート

もし自分のUEがFASTBuildツール（Engine\Extras\ThirdPartyNotUE\FASTBuild）を持っていないことに気づき、UnrealBuildToolプロジェクトにFASTBuild.csファイルがない場合、おそらくあなたのUEのバージョンはFASTBuildをサポートしていない可能性が非常に高いです。

UE4.27のソースコードを参照して、FASTBuild.csファイルを作成し、他の必要なコードの変更も加える必要があります。詳細はここでは説明しません。


###自分のFASTBuildをコンパイルする

もしFASTBuild自体に興味があるか、または何か変更をしたい場合は、FASTBuildを使用してFASTBuildをコンパイルしてみてください。

- ダウンロードしてください [最新のソースコード](https://github.com/disenone/fastbuild/releases)ファイルを解凍します。
External\SDK\VisualStudio\VS2019.bff ファイルを編集して、.VS2019_BasePath と .VS2019_Version をローカルマシンに合わせて変更してください。Version は .VS2019_BasePath\Tools\MSVC ディレクトリ内で確認できます。例えば、
    ```
    .VS2019_BasePath        = 'C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC'    // <-- Set path here
    .VS2019_Version         = '14.29.30133' // <-- Set version here
    .VS2019_MSC_VER         = '1929' // <-- Set MSC_VER here
    ```

External\SDK\Windows\Windows10SDK.bff の .Windows10_SDKBasePath と .Windows10_SDKVersion を変更してください。バージョンは .Windows10_SDKBasePath/bin 内で確認できます。
    ```
    .Windows10_SDKBasePath        = 'C:\Program Files (x86)\Windows Kits/10'    // <-- Set path here
    .Windows10_SDKVersion         = '10.0.19041.0' // <-- Set version here
    ```

- External\SDK\Clang\Windows\Clang11.bff の .Clang11_BasePath と .Clang11_Version を変更し、パスは .VS2019_BasePath\Tools\Tools/LLVM/x64 にあります。
    ```
    .Clang11_BasePath = 'C:/Program Files (x86)/Microsoft Visual Studio/2019/Professional/VC/Tools/LLVM/x64'    // <-- Set path here
    .Clang11_Version  = '12.x.x'
    ```

Codeディレクトリに移動し、cmdで`FBuild.exe All-x64-Release`を実行してください。正しく構成されていれば、コンパイルが成功したことが確認でき、tmp\x64-Release\Tools\FBuild\FBuild内にFBuild.exeを見つけることができます。

`FBuild.exe All-x64-Release -dist -coordinator=127.0.0.1`で分散コンパイルを開始できます。

###FBuild 追加のオプション

私が提供する FBuild は、次のよく使用されるオプションをサポートしています：

- coordinator: 指定コーディネーターIPアドレス（システム環境変数の値を上書きできます）
- brokerage: 指定仲介地址（可以覆蓋系統環境變數的值）
- nocache: Cache を使用しないように強制します.
- dist: 分散コンパイルを有効にする
- forceremote: リモートマシンでのコンパイルを強制
要約：編集完了後、統計レポートを出力します。

その他、`FBuild.exe -help` を実行してさらにオプションを確認できます。

FBuildWorkerの一般的な選択肢は次のとおりです：

- coordinator: 指定コーディネーターの IP アドレス（システム環境変数の値を上書きできます）
- brokerage: 指定仲介地的位  （可以覆盖系统环境变量的值）
nocache：キャッシュを使用しないように強制します
- CPUs: コンパイルに割り当てるコアの数を指定します。

追加オプションに関しては、`FBuildWorder.exe -help` を実行してください。

###UEの組み込みFASTBuild.csを編集します。

UE の内蔵 FASTBuild.cs はシステム環境変数をうまく処理しておらず、BuildConfiguration.xml で指定されたパラメータとの関係がうまく取れていません。多くのパラメータはシステム環境変数が優先されて読み込まれるため、これは明らかに BuildConfiguration.xml の使用論理とは逆です。

この場合、関連するコードをこのように変更することができます。ここではUE5.3を例に挙げます。

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

###BuildConfiguration.xmlを向上させる設定

```xml
<?xml version="1.0" encoding="utf-8" ?>
<Configuration xmlns="https://www.unrealengine.com/BuildConfiguration">
    <ProjectFileGenerator>
<!-- バージョン指定 -->
        <Format>VisualStudio2022</Format>
    </ProjectFileGenerator>
    <BuildConfiguration>
<!-- FASTBuildを有効にする -->
        <bAllowFASTBuild>true</bAllowFASTBuild>
指定するマシンがコンパイルに参加するCPUコア数
        <MaxParallelActions>12</MaxParallelActions>
<!-- Incredibuildをオフにする -->
        <bAllowXGE>false</bAllowXGE>
    </BuildConfiguration>
    <FASTBuild>
<!-- FBuildのパスを指定 -->
        <FBuildExecutablePath>d:\libs\FASTBuild\bin\FBuild.exe</FBuildExecutablePath>
<!-- 分散コンパイルを有効にする -->
        <bEnableDistribution>true</bEnableDistribution>
<!--指定された仲介経路-->
        <FBuildBrokeragePath>\\127.0.0.1\Brokerage\</FBuildBrokeragePath>
指定されたキャッシュパス
        <FBuildCachePath>\\127.0.0.1\Cache\</FBuildCachePath>
<!-- キャッシュを有効にする -->
        <bEnableCaching>true</bEnableCaching>
<!-- キャッシュの読み書き権限 読み取り/書き込み/読み書き -->
        <CacheMode>ReadWrite</CacheMode>
<!-- 指定コーディネーターIP -->
        <FBuildCoordinator>127.0.0.1</FBuildCoordinator>
<!-- リモートコンパイルを強制する -->
        <!-- <bForceRemote>true</bForceRemote> -->
    </FASTBuild>
</Configuration>
```

--8<-- "footer_ja.md"


> この投稿はChatGPTによって翻訳されました。[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。 
見落としがないか指摘してください。 
