---
layout: post
title: استخدام FASTBuild لتجميع UE4 و UE5
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
description: تم دعم FASTBuild بشكل غير كامل في محرك التطوير الأساسي UE. لضمان دعم
  FASTBuild بشكل مثالي لكل من UE4 و UE5 ، يجب علينا تهيئة بعض الإعدادات وتعديل الشفرة
  المصدرية. سأقدم لك الخطوات بالتفصيل أدناه.
figures: []
---

<meta property="og:title" content="使用 FASTBuild 编译 UE4 和 UE5" />

> تم اختبار طريقة هذا المقال مع UE4.27 - UE5.3، ولم يتم اختبارها مع الإصدارات الأخرى، يمكنك تجربتها.

##مقدمة

[FASTBuild](https://www.fastbuild.org/docs/home.html)هو أداة ترجمة موزعة مفتوحة المصدر ومجانية، تستهلك عملية ترجمة UE الذاتية الكثير من الوقت، إذا تم استخدام FASTBuild، ستقلل بشكل كبير من الوقت المستهلك.

UE تدعم FASTBuild اعتبارًا من الإصدار 4.x، ويتضمن الكود المصدري الرسمي أداة FASTBuild المعدلة بشكل ساحر، مستندة إلى الإصدار 0.99 من FASTBuild، وتوجد في `Engine\Extras\ThirdPartyNotUE\FASTBuild`، يستخدم UE5.3 نفس الإصدار أيضًا. هذا إصدار قديم نسبيًا بالفعل، آخر إصدار رسمي حتى إنشاء هذا المستند هو 1.11، ويتضمن المزيد من الوظائف الجديدة وإصلاحات الأخطاء. يركز هذا المستند بشكل خاص على كيفية استخدام الإصدار 1.11 ودعم UE4 و UE5 في نفس الوقت.

##تكوين بسيط

لتحقيق الهدف، نحتاج إلى إجراء بعض التعديلات على FASTBuild 1.11 وشفرة مصدر UE. في الواقع، لقد أجريت جميع التعديلات بالفعل هنا، لذا يمكننا استخدام النسخة التي قمت بتعديلها مباشرة.

(https://github.com/disenone/fastbuild/releases)يحتوي على ملفات التنفيذ FBuild.exe، FBuildCoordinator.exe، FBuildWorker.exe. لتعبيرًا واضحًا، سيُشار إلى الجهاز الذي يستخدم FBuild.exe للبرمجة باسم "المحلي"، بينما سيُشار إلى الآلة البعيدة التي تشارك في التحرير باستخدام وحدة المعالجة المركزية باسم "البعيد".

###تكوين الجهاز

أضف مسار المجلد الذي يحتوي على ملف FBuild.exe إلى متغير البيئة Path في النظام، لضمان قدرة تشغيل FBuild.exe مباشرة من خلال سطر الأوامر.

قم بتهيئة مجلد المشاركة Cache (إذا لم يكن هناك حاجة لإنشاء Cache، يمكنك عدم تهيئته): قم بتعيين مجلد فارغ كمسار مشاركة وتأكد من أن الجهاز البعيد يمكنه الوصول إليه.

افتح مشروع UE4 / UE5 المصدري على هذا الجهاز وقم بتعديل ملف تكوين البناء Engine\Saved\UnrealBuildTool\BuildConfiguration.xml كما يلي:

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

تشغيل ملف FBuildCoordinator.exe الذي تم تنزيله قبل تشغيل الجهاز.

###تكوين الجهاز عن بُعد

مع تكوين Cache نفسه، ولكن يجب تحديد عنوان IP إلى عنوان IP المحلي، هنا نفترض أن يكون 192.168.1.100

- FASTBUILD_CACHE_PATH: \\192.168.1.100\Cache
- FASTBUILD_CACHE_MODE: rw

ترجمة النص إلى اللغة العربية:

تكوين محدد لـ عنوان Coordinator IP

- FASTBUILD_COORDINATOR: 192.168.1.100

يرجى ترتيبه كما في الصورة التالية

![](assets/img/2023-ue-fastbuild/remote_vars.png)

قم بتشغيل ملف FBuildWorker.exe على الجهاز عن بُعد. إذا نجحت الإعدادات، يمكن رؤية سجلات النشاط على FBuildCoordinator.exe الموجود على الجهاز الخاص بك (هنا 192.168.1.101 هو عنوان الآي بي الخاص بالجهاز عن بُعد).

```
FBuildCoordinator - v1.11-UE
[2023-12-01-20:06:38] Listening on port 31392
[2023-12-01-20:06:38] current [0] workers: []
[2023-12-01-20:06:42] New worker available: 192.168.1.101
[2023-12-01-20:06:42] current [1] workers: [192.168.1.101]
```

###امرأة UE_COMPILATION

افتح مشروع الشفرة المصدرية لـ UE في VisualStudio ، اختر مشروع C++ ثم انقر فوق إعادة الإنشاء. إذا كانت الإعدادات صحيحة ، يمكنك رؤية سجل مشابه لما يلي:

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

FASTBuild يمكنه العثور على عنوان IP الخاص بالجهاز عن بعد وبدء إرسال عملية الترجمة إليه. يمكن رؤية المهام التي تجري الترجمة حاليًا على FBuildWorker الخاص بالجهاز البعيد.

##تحسين التكوين

###دعم الإصدارات الأقدم لـ UE

إذا وجدت أن UE الخاص بك ليس به أداة FASTBuild (Engine\Extras\ThirdPartyNotUE\FASTBuild)، ولا يحتوي مشروع UnrealBuildTool على ملف FASTBuild.cs، ثم من المحتمل بشكل كبير أن إصدار UE الذي تستخدمه لا يدعم بعد FASTBuild.

من الضروري الرجوع إلى مصدر UE4.27 وإنشاء ملف FASTBuild.cs مماثل، وإضافة التعديلات الأخرى المتعلقة بالشفرة، دون ذكرها هنا.


###قم بترجمة هذا النص إلى اللغة العربية: 

ترجمة "Compile your own FASTBuild"

إذا كنت مهتمًا بـ FASTBuild بشكل ذاتي أو ترغب في إجراء بعض التعديلات، يمكنك محاولة استخدام FASTBuild لتجميع FASTBuild.

قم بتحميل [الشيفرة البرمجية الخاصة بي](https://github.com/disenone/fastbuild/releases)وفك الضغط
قم بتعديل ملف External\SDK\VisualStudio\VS2019.bff، حيث تقوم بتغيير .VS2019_BasePath و .VS2019_Version إلى المحتوى المقابل على جهازك، يمكنك العثور على الإصدار في المسار .VS2019_BasePath\Tools\MSVC، على سبيل المثال.
    ```
    .VS2019_BasePath        = 'C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC'    // <-- Set path here
    .VS2019_Version         = '14.29.30133' // <-- Set version here
    .VS2019_MSC_VER         = '1929' // <-- Set MSC_VER here
    ```

قم بتعديل .Windows10_SDKBasePath و .Windows10_SDKVersion في External\SDK\Windows\Windows10SDK.bff، يمكنك العثور على الإصدار في .Windows10_SDKBasePath/bin:
    ```
    .Windows10_SDKBasePath        = 'C:\Program Files (x86)\Windows Kits/10'    // <-- Set path here
    .Windows10_SDKVersion         = '10.0.19041.0' // <-- Set version here
    ```

قم بتعديل .Clang11_BasePath و .Clang11_Version في ملف External\SDK\Clang\Windows\Clang11.bff، حيث يتواجد المسار في .VS2019_BasePath\Tools\LLVM/x64.
    ```
    .Clang11_BasePath = 'C:/Program Files (x86)/Microsoft Visual Studio/2019/Professional/VC/Tools/LLVM/x64'    // <-- Set path here
    .Clang11_Version  = '12.x.x'
    ```

أدخل إلى دليل Code، وقم بتنفيذ `FBuild.exe All-x64-Release` في cmd. إذا كانت الإعدادات صحيحة، يمكنك رؤية نجاح الترجمة تحت tmp\x64-Release\Tools\FBuild\FBuild وستجد FBuild.exe هناك.

`FBuild.exe All-x64-Release -dist -coordinator=127.0.0.1` يمكن أن يفتح الترجمة الموزعة.

###FBuild المزيد من الخيارات

أنا أقدم FBuild الذي يدعم بشكل طبيعي الخيارات الشائعة التالية:

قم بتعيين عنوان IP للمنسق (يمكن أن يغطي قيم متغيرات البيئة النظام)
- وساطة: تشير إلى عنوان السمسرة (الذي يمكن أن يغطي قيم متغيرات النظام)
nocache: تحدي الموقع بعدم استخدام ذاكرة التخزين المؤقت
- dist: تمكين الترجمة الموزعة
قوم بترجمة هذه النص إلى اللغة العربية:

- forceremote：فرض الترجمة على الجهاز عن بُعد
ملخص: بعد انتهاء التحرير، يتم إخراج تقرير الإحصاءات.

انتظر، يمكن تشغيل المزيد من الخيارات بتشغيل `FBuild.exe -help` للعرض.

الخيارات الشائعة المستخدمة لـ FBuildWorker هي:

قاموس: تحديد عنوان Coordinator ip (يمكن أن يغطي قيم متغيرات البيئة النظامية)
- وساطة: عنوان السمسرة المحدد (يمكن أن يغطي قيم متغيرات البيئة في النظام)
- nocache: يُجبر على عدم استخدام الذاكرة المؤقتة
- cpus: تحديد عدد النوى المشاركة في البناء

يمكنك تشغيل المزيد من الخيارات عند تشغيل `FBuildWorder.exe -help`.

###قم بتعديل ملف FASTBuild.cs المضمن مع UE.

الFASTBuild.cs الذي يأتي مدمجًا مع UE لا يتعامل بشكل جيد مع متغيرات البيئة النظامية المحددة في BuildConfiguration.xml، حيث يتم قراءة العديد من المتغيرات بأولوية من متغيرات البيئة النظامية، وهذا بوضوح يتنافى مع منطق استخدام BuildConfiguration.xml.

لهذا الغرض، يمكن تعديل الشيفرات ذات الصلة إلى هذا الشكل، وهنا نأخذ UE5.3 كمثال:

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

###بناء BuildConfiguration.xml المتقدم

```xml
<?xml version="1.0" encoding="utf-8" ?>
<Configuration xmlns="https://www.unrealengine.com/BuildConfiguration">
    <ProjectFileGenerator>
<!-- حدد إصدار نظام التشغيل -->
        <Format>VisualStudio2022</Format>
    </ProjectFileGenerator>
    <BuildConfiguration>
Translate these text into Arabic language:

        <!-- فتح FASTBuild -->
        <bAllowFASTBuild>true</bAllowFASTBuild>
<!-- تحديد عدد أنوية وحدة المعالجة المركزية التي تشارك في الترجمة على هذا الجهاز -->
        <MaxParallelActions>12</MaxParallelActions>
<!-- إيقاف Incredibuild -->
        <bAllowXGE>false</bAllowXGE>
    </BuildConfiguration>
    <FASTBuild>
<!-- حدد مسار FBuild -->
        <FBuildExecutablePath>d:\libs\FASTBuild\bin\FBuild.exe</FBuildExecutablePath>
<!-- فتح الترجمة الموزعة -->
        <bEnableDistribution>true</bEnableDistribution>
<!-- حدد مسار الوساطة -->
        <FBuildBrokeragePath>\\127.0.0.1\Brokerage\</FBuildBrokeragePath>
<!-- حدد مسار الذاكرة المؤقتة -->
        <FBuildCachePath>\\127.0.0.1\Cache\</FBuildCachePath>
<!-- تمكين التخزين المؤقت -->
        <bEnableCaching>true</bEnableCaching>
<!-- إذن القراءة/الكتابة/القراءة والكتابة للتخزين المؤقت --> 
        <CacheMode>ReadWrite</CacheMode>
قم بتحديد عنوان الـIP للمنسق.
        <FBuildCoordinator>127.0.0.1</FBuildCoordinator>
<!-- إعادة ترجمة إجبارية عن بُعد -->
        <!-- <bForceRemote>true</bForceRemote> -->
    </FASTBuild>
</Configuration>
```

--8<-- "footer_ar.md"


> تمت ترجمة هذه المشاركة باستخدام ChatGPT، يرجى تقديم [**تعليقات**](https://github.com/disenone/wiki_blog/issues/new)يرجى تحديد أي نقص. 
