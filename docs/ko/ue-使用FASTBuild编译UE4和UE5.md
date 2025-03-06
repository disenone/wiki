---
layout: post
title: FASTBuild를 사용하여 UE4 및 UE5를 컴파일합니다.
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
description: UE 원조는 FASTBuild 지원이 완벽하지 않습니다. UE4와 UE5가 FASTBuild를 완벽하게 지원하기 위해 구성
  및 소스 코드 수정이 필요합니다. 아래에서 하나씩 안내해 드리겠습니다.
figures: []
---

<meta property="og:title" content="使用 FASTBuild 编译 UE4 和 UE5" />

> 본 텍스트의 방법은 UE4.27 - UE5.3을 지원하는 것을 테스트했습니다. 다른 버전은 테스트되지 않았으며, 시도해 볼 수 있습니다.

##서문

[FASTBuild](https://www.fastbuild.org/docs/home.html)무료 오픈 소스 분산 컴파일 도구입니다. UE 자체 컴파일은 상당히 시간이 소요되는데, FASTBuild를 사용하면 시간을 크게 단축할 수 있습니다.

UE는 4.x부터 FASTBuild를 지원할 수 있게 되었습니다. 공식 소스 코드에는 수정된 FASTBuild 도구가 함께 제공되었는데, 이는 FASTBuild 0.99 버전을 기반으로 하며, 위치는 `Engine\Extras\ThirdPartyNotUE\FASTBuild`에 있습니다. UE5.3도 동일한 버전을 사용합니다. 이는 이미 꽤 오래된 버전이며, 이 문서를 작성하는 시점에서 FASTBuild의 최신 버전은 1.11입니다. 이 버전에는 더 많은 새로운 기능 지원과 버그 수정이 있습니다. 이 문서는 1.11 버전을 사용하여 UE4와 UE5를 동시에 지원하는 방법에 중점을 두고 설명합니다.

##간편한 구성

목표를 달성하기 위해 FASTBuild 1.11 및 UE 소스 코드를 수정해야 합니다. 사실 여기서 이미 모두 수정을 완료했으니, 우리는 내가 수정한 버전을 바로 사용할 수 있습니다.

FASTBuild가 제출한 [최신 버전](https://github.com/disenone/fastbuild/releases)내부에서 실행되는 파일 FBuild.exe, FBuildCoordinator.exe, FBuildWorker.exe입니다. 명확히 설명하기 위해, FBuild.exe를 사용하여 프로그래밍하는 기계를 '로컬'로 지칭하고, CPU를 활용하여 편집에 참여하는 원격 기계는 '원격 기계'라고 합니다.

###기종 설정

FBuild.exe가 있는 디렉토리를 시스템 환경 변수 Path에 추가하여 cmd에서 FBuild.exe를 직접 실행할 수 있도록합니다.

Cache 공유 디렉토리를 설정하십시오. 필요 없는 경우 Cache를 생성할 필요는 없습니다. 빈 디렉토리를 공유 경로로 설정하고 원격 컴퓨터가 액세스할 수 있는지 확인하십시오.

UE4 / UE5의 소스 코드 프로젝트를 열고, Engine\Saved\UnrealBuildTool\BuildConfiguration.xml과 같은 컴파일 구성 파일을 수정하십시오:

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

FBuildCoordinator.exe를 다운로드한 후에 이 기기를 실행하세요.

###원격 컴퓨터 설정

Cache가 동일하게 구성되었지만 ip는 로컬 ip로 지정되어야 합니다. 여기서는 192.168.1.100으로 가정합니다.

- FASTBUILD_CACHE_PATH: \\192.168.1.100\Cache
- FASTBUILD_CACHE_MODE: rw

동일한 설정 Coordinator ip

- FASTBUILD_COORDINATOR: 192.168.1.100

아래 사진처럼 구성하세요.

![](assets/img/2023-ue-fastbuild/remote_vars.png)

원격 컴퓨터에서 FBuildWorker.exe를 실행하세요. 설정이 올바로 되었다면, 로컬 컴퓨터의 FBuildCoordinator.exe에서 로그를 확인할 수 있을 것입니다 (여기서 192.168.1.101은 원격 컴퓨터의 IP 주소입니다):

```
FBuildCoordinator - v1.11-UE
[2023-12-01-20:06:38] Listening on port 31392
[2023-12-01-20:06:38] current [0] workers: []
[2023-12-01-20:06:42] New worker available: 192.168.1.101
[2023-12-01-20:06:42] current [1] workers: [192.168.1.101]
```

###테스트 UE 컴파일

VisualStudio에서 UE 소스 코드 프로젝트 sln을 열고, C++ 프로젝트 중 하나를 선택한 후 'Rebuild'를 클릭하십시오. 설정이 올바르다면 다음과 유사한 로그를 볼 수 있습니다.

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

FASTBuild는 원격 컴퓨터의 IP 주소를 찾아 원격 컴퓨터에 빌드를 시작합니다. 원격 컴퓨터의 FBuildWorker에서 현재 실행 중인 빌드 작업을 볼 수도 있습니다.

##향상된 구성

###장기 지원되는 UE 버전을 지원합니다.

자신의 UE에 FASTBuild 도구(Engine\Extras\ThirdPartyNotUE\FASTBuild)가 없고 프로젝트 UnrealBuildTool 속에 FASTBuild.cs 파일이 없다면, 매우 가능성이 높게 당신의 UE 버전이 아직 FASTBuild를 지원하지 않는 것일지도 모릅니다.

UE4.27의 소스 코드를 참고하여 FASTBuild.cs와 유사한 것을 만들고 기타 관련 코드 변경 사항을 적용해야 합니다. 여기서 자세히 다루지는 않겠습니다.


###자체적으로 FASTBuild를 컴파일하다.

만약 FASTBuild에 관심이 있거나 수정을 하고 싶다면, FASTBuild로 FASTBuild를 컴파일해보세요.

- 제 [최신 소스 코드](https://github.com/disenone/fastbuild/releases)그리고 압축 풀기
외부\SDK\VisualStudio\VS2019.bff 파일을 수정하여 .VS2019_BasePath 및 .VS2019_Version을 컴퓨터에 해당하는 내용으로 변경합니다. 버전은 .VS2019_BasePath\Tools\MSVC 폴더 아래에서 확인할 수 있습니다. 예를 들어,
    ```
    .VS2019_BasePath        = 'C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC'    // <-- Set path here
    .VS2019_Version         = '14.29.30133' // <-- Set version here
    .VS2019_MSC_VER         = '1929' // <-- Set MSC_VER here
    ```

External\SDK\Windows\Windows10SDK.bff 파일에서 .Windows10_SDKBasePath 및 .Windows10_SDKVersion을 수정하십시오. 버전은 .Windows10_SDKBasePath/bin 폴더에서 확인할 수 있습니다.
    ```
    .Windows10_SDKBasePath        = 'C:\Program Files (x86)\Windows Kits/10'    // <-- Set path here
    .Windows10_SDKVersion         = '10.0.19041.0' // <-- Set version here
    ```

External\SDK\Clang\Windows\Clang11.bff 파일의 .Clang11_BasePath 및 .Clang11_Version을 수정하여, 경로는 .VS2019_BasePath\Tools\Tools/LLVM/x64에 있습니다.
    ```
    .Clang11_BasePath = 'C:/Program Files (x86)/Microsoft Visual Studio/2019/Professional/VC/Tools/LLVM/x64'    // <-- Set path here
    .Clang11_Version  = '12.x.x'
    ```

Code 디렉토리로 이동한 후 cmd에서 'FBuild.exe All-x64-Release'를 실행하십시오. 설정이 올바르다면 컴파일 성공 메시지를 확인할 수 있습니다. tmp\x64-Release\Tools\FBuild\FBuild 폴더 안에 FBuild.exe 파일을 확인할 수 있습니다.

`FBuild.exe All-x64-Release -dist -coordinator=127.0.0.1` 명령을 실행하면 분산 컴파일을 시작할 수 있습니다.

###FBuild 더 많은 옵션

제공되는 FBuild는 다음과 같은 일반적으로 사용되는 옵션을 지원합니다:

- coordinator: 지정된 Coordinator IP 주소 (시스템 환경 변수의 값을 덮어쓸 수 있음)
- 중개업: 지정된 중개업 주소(시스템 환경 변수 값 덮어씌움 가능)
- nocache: 캐시를 사용하지 않도록 강제 
- dist: 분산 컴파일 활성화
forceremote: 원격 컴퓨터에서 강제로 컴파일하기
- 요약: 편집이 끝난 후 통계 보고서 출력

좀 기다려, 'FBuild.exe -help'를 실행하면 더 많은 옵션을 볼 수 있어.

FBuildWorker의 주요 옵션은 다음과 같습니다:

- coordinator: 지정된 Coordinator IP 주소 (시스템 환경 변수의 값 덮어쓸 수 있음)
- brokerage: 지정된 중개업체 주소 (시스템 환경 변수의 값으로 대체 가능)
- nocache: 캐시를 사용하지 않도록 강제함
- cpus: 컴파일에 몇 개의 코어를 할당할지 지정합니다.

추가 옵션을 확인하려면 `FBuildWorder.exe -help`를 실행하십시오.

###UE에서 제공하는 FASTBuild.cs 파일을 수정하십시오.

UE의 기본 FASTBuild.cs는 시스템 환경 변수를 제대로 처리하지 못하며 BuildConfiguration.xml에서 지정된 매개 변수와의 관계가 매우 많습니다. 많은 매개 변수가 우선적으로 시스템 환경 변수를 읽기 때문에 이는 명백히 BuildConfiguration.xml의 사용 논리와 반대됩니다.

이를 위해 해당 코드를 다음과 같이 변경할 수 있습니다. 여기서는 예시로 UE5.3를 들겠습니다:

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

###BuildConfiguration.xml 고급 설정

```xml
<?xml version="1.0" encoding="utf-8" ?>
<Configuration xmlns="https://www.unrealengine.com/BuildConfiguration">
    <ProjectFileGenerator>
<!-- 특정한 VS 버전 -->
        <Format>VisualStudio2022</Format>
    </ProjectFileGenerator>
    <BuildConfiguration>
<!-- FASTBuild를 활성화합니다 -->
        <bAllowFASTBuild>true</bAllowFASTBuild>
<!-- 컴파일에 참여하는 로컬 CPU 코어 수 지정 -->
        <MaxParallelActions>12</MaxParallelActions>
<!-- 인크레디빌드 종료 -->
        <bAllowXGE>false</bAllowXGE>
    </BuildConfiguration>
    <FASTBuild>
<!-- FBuild 경로 지정 -->
        <FBuildExecutablePath>d:\libs\FASTBuild\bin\FBuild.exe</FBuildExecutablePath>
<!-- 분산 컴파일링 활성화 -->
        <bEnableDistribution>true</bEnableDistribution>
<!-- brokerage 경로 지정 -->
        <FBuildBrokeragePath>\\127.0.0.1\Brokerage\</FBuildBrokeragePath>
지정된 캐시 경로
        <FBuildCachePath>\\127.0.0.1\Cache\</FBuildCachePath>
<!-- 캐시 활성화 -->
        <bEnableCaching>true</bEnableCaching>
<!-- 캐시 읽기/쓰기/읽기 쓰기 권한 -->
        <CacheMode>ReadWrite</CacheMode>
<!-- 지정된 코디네이터 IP -->
        <FBuildCoordinator>127.0.0.1</FBuildCoordinator>
<!-- 원격 컴파일 강제 실행 -->
        <!-- <bForceRemote>true</bForceRemote> -->
    </FASTBuild>
</Configuration>
```

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT를 사용하여 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)어떠한 빠진 부분도 드러내라. 
