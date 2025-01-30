---
layout: post
title: FASTBuildを使用してUE4とUE5をコンパイルします。
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
description: UEのネイティブサポートはFASTBuildに対してあまり充実していません。UE4とUE5がFASTBuildを完璧にサポートするためには、いくつかの設定とソースコードの変更が必要です。以下に詳しく説明します。
figures: []
---

<meta property="og:title" content="使用 FASTBuild 编译 UE4 和 UE5" />

> テキストは UE4.27 から UE5.3 をサポートし、他のバージョンはテストされていないため、お試しいただけます。

##序文

[FASTBuild](https://www.fastbuild.org/docs/home.html)それは無料のオープンソースの分散コンパイルツールであり、UE そのもののコンパイルにはかなりの時間がかかります。FASTBuild を使えば、時間を大幅に短縮することができます。

UE 4.xから、FASTBuildをサポートするようになりました。公式ソースコードには、改変されたFASTBuildツールが付属しています。これはFASTBuild 0.99バージョンをベースにしており、`Engine\Extras\ThirdPartyNotUE\FASTBuild`フォルダに位置しています。UE5.3も同じバージョンを使用しています。このバージョンはかなり古いものです。この記事作成時点では、FASTBuildの公式最新バージョンは1.11で、新しい機能やバグ修正があります。この記事では、1.11バージョンを使用してUE4とUE5をサポートする方法を重点的に記録します。

##簡易設定

目的を達成するためには、FASTBuild 1.11 と UE ソースコードにいくつかの修正を加える必要があります。実は、ここですでにすべての修正を行っているので、私が修正したバージョンをそのまま使用することができます。

(https://github.com/disenone/fastbuild/releases)FBuild.exe、FBuildCoordinator.exe、FBuildWorker.exe の実行ファイルがあります。わかりやすく説明するため、FBuild.exe を使用してプログラムするマシンを「ローカルマシン」と呼び、CPU を提供して編集に参加する他のリモートマシンを「リモートマシン」と呼びます。

###本機構成

FBuild.exe の所在ディレクトリをシステム環境変数 Path に追加し、cmd で直接 FBuild.exe を実行できるようにします。

キャッシュの共有ディレクトリを配置する（キャッシュを生成する必要がない場合は、設定しなくても構いません）：空のディレクトリを共有パスとして設定し、リモートマシンがアクセスできることを確認してください。

本機のUE4 / UE5のソースプロジェクトを開き、コンパイル構成ファイルEngine\Saved\UnrealBuildTool\BuildConfiguration.xmlを以下のように修正してください：

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

FBuildCoordinator.exe をダウンロードしてから、本機を実行してください。

###遠隔機構成

同じ設定のキャッシュを使用しますが、IPはローカルIPに指定する必要があります。ここでは192.168.1.100と仮定します。

- FASTBUILD_CACHE_PATH: \\192.168.1.100\Cache
- FASTBUILD_CACHE_MODE: rw

同じく、Coordinator IP設定

- FASTBUILD_COORDINATOR: 192.168.1.100

配置が完了しました。以下の図を参照してください。

![](assets/img/2023-ue-fastbuild/remote_vars.png)

リモートマシン上で FBuildWorker.exe を実行します。設定が成功すると、ローカルの FBuildCoordinator.exe にログが表示されます（ここで 192.168.1.101 はリモートマシンの IP です）。

```
FBuildCoordinator - v1.11-UE
[2023-12-01-20:06:38] Listening on port 31392
[2023-12-01-20:06:38] current [0] workers: []
[2023-12-01-20:06:42] New worker available: 192.168.1.101
[2023-12-01-20:06:42] current [1] workers: [192.168.1.101]
```

###テストUEコンパイル

VisualStudioを使用してUEのソースコードプロジェクトslnを開き、C++のプロジェクトを選択し、Rebuildをクリックします。正常に設定されている場合、次のようなログが表示されるはずです。

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

FASTBuild はリモートマシンの IP アドレスを見つけ、リモートマシンにコンパイルを開始します。リモートマシンの FBuildWorker でも、現在実行中のコンパイルタスクを確認できます。

##上級設定

###より長くサポートされるUEバージョン

もしあなたが自分のUEにFASTBuildツール（Engine\Extras\ThirdParty\FASTBuild）がないことに気づき、そしてUnrealBuildToolプロジェクト内にFASTBuild.csファイルが存在しない場合、おそらくあなたのUEのバージョンはまだFASTBuildをサポートしていない可能性が高いです。

UE4.27のソースコードを参照し、FASTBuild.csの類似物を作成する必要があります。他の関連するコードの変更も行いましょう。詳細はここでは述べません。


###自身のFASTBuildをコンパイルする

もしFASTBuild自体にも興味がある場合や、何か変更を加えたい場合は、FASTBuildを使用してFASTBuildをコンパイルしてみることができます。

- ダウンロードしてください [最新ソースコード](https://github.com/disenone/fastbuild/releases)そして展開
- External\SDK\VisualStudio\VS2019.bffを修正し、.VS2019_BasePathと.VS2019_Versionを自分のマシンに対応する内容に変更してください。Versionは.VS2019_BasePath\Tools\MSVCディレクトリの下で確認できます。例えば
    ```
    .VS2019_BasePath        = 'C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC'    // <-- Set path here
    .VS2019_Version         = '14.29.30133' // <-- Set version here
    .VS2019_MSC_VER         = '1929' // <-- Set MSC_VER here
    ```

- External\SDK\Windows\Windows10SDK.bff の .Windows10_SDKBasePath と .Windows10_SDKVersion を修正してください。バージョンは .Windows10_SDKBasePath/bin の中で確認できます：
    ```
    .Windows10_SDKBasePath        = 'C:\Program Files (x86)\Windows Kits/10'    // <-- Set path here
    .Windows10_SDKVersion         = '10.0.19041.0' // <-- Set version here
    ```

- External\SDK\Clang\Windows\Clang11.bff の .Clang11_BasePath と .Clang11_Version を修正してください。パスは .VS2019_BasePath\Tools\Tools/LLVM/x64 にあります。
    ```
    .Clang11_BasePath = 'C:/Program Files (x86)/Microsoft Visual Studio/2019/Professional/VC/Tools/LLVM/x64'    // <-- Set path here
    .Clang11_Version  = '12.x.x'
    ```

- Code ディレクトリに移動し、cmd で `FBuild.exe All-x64-Release` を実行します。設定が正しければ、コンパイルが成功したことが確認でき、tmp\x64-Release\Tools\FBuild\FBuild に FBuild.exe が表示されます。

`FBuild.exe All-x64-Release -dist -coordinator=127.0.0.1` は分散コンパイルを開始できます。

###FBuildの追加オプション

私が提供するFBuild自体は、以下の一般的なオプションをサポートしています：

- coordinator: 指定されたコーディネーターのIPアドレス（システム環境変数の値を上書きできます）
- brokerage: 指定ブローカージアドレス（システム環境変数の値を上書きできます）
- 「nocache」：キャッシュを使用しないように強制します。
- dist: 分散コンパイルを有効にする
- forceremote：强制在远程机编译
- forceremote: リモートマシンでのコンパイルを強制
- summary: 編集終了後に統計レポートを出力する

ちょっと待って、さらに多くのオプションは `FBuild.exe -help` を実行して確認できます。

FBuildWorkerのよく使われるオプションは次の通りです：

- coordinator: 指定されたコーディネーターのIPアドレス（システム環境変数の値を上書きできます）
- brokerage: 指定されたブローカレッジの住所（システム環境変数の値を上書きできます）
- nocache：キャッシュを強制的に使用しない
- cpus: コンパイルに何個のコアを割り当てるかを指定します。

追加のオプションについては、`FBuildWorder.exe -help` を実行してください。

###UEの標準FASTBuild.csを編集します。

UE に付属の FASTBuild.cs は、システム環境変数を適切に処理しておらず、BuildConfiguration.xml で指定されたパラメータとの関係が不明瞭です。多くのパラメータはシステム環境変数が優先的に読み込まれるため、これは明らかに BuildConfiguration.xml の使用ロジックに反しています。

この場合、関連するコードを次のように変更できます。ここではUE5.3を例に挙げます：

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

###BuildConfiguration.xml の高度な設定

```xml
<?xml version="1.0" encoding="utf-8" ?>
<Configuration xmlns="https://www.unrealengine.com/BuildConfiguration">
    <ProjectFileGenerator>
<!-- 指定vs版本 -->
        <Format>VisualStudio2022</Format>
    </ProjectFileGenerator>
    <BuildConfiguration>
<!-- FASTBuild を有効にする -->
        <bAllowFASTBuild>true</bAllowFASTBuild>
本机がコンパイルに参加するCPUコア数を指定します。
        <MaxParallelActions>12</MaxParallelActions>
<!-- Incredibuildを閉じる -->
        <bAllowXGE>false</bAllowXGE>
    </BuildConfiguration>
    <FASTBuild>
<!-- 指定 FBuild パス -->
        <FBuildExecutablePath>d:\libs\FASTBuild\bin\FBuild.exe</FBuildExecutablePath>
<!-- 分散コンパイルを有効にする -->
        <bEnableDistribution>true</bEnableDistribution>
<!-- 指定ブローカーのパス -->
        <FBuildBrokeragePath>\\127.0.0.1\Brokerage\</FBuildBrokeragePath>
<!-- 指定 cache 路径 -->
        <FBuildCachePath>\\127.0.0.1\Cache\</FBuildCachePath>
<!-- キャッシュを有効にする -->
        <bEnableCaching>true</bEnableCaching>
<!-- cacheの読み書き権限 読み/書き/読み書き -->
        <CacheMode>ReadWrite</CacheMode>
<!-- 指定コーディネーターIP -->
        <FBuildCoordinator>127.0.0.1</FBuildCoordinator>
<!-- 強制リモートコンパイル -->
        <!-- <bForceRemote>true</bForceRemote> -->
    </FASTBuild>
</Configuration>
```

--8<-- "footer_ja.md"


> この投稿はChatGPTを使って翻訳されました。フィードバックをお願いします[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)指摘された点を見逃さずにご提出ください。 
