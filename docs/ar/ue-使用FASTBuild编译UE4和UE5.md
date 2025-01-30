---
layout: post
title: استخدام FASTBuild في تجميع UE4 و UE5
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
description: دعم UE الأصلي لـ FASTBuild ليس متكاملاً بالشكل المطلوب. من أجل جعل UE4
  و UE5 يدعمان FASTBuild بشكل مثالي، نحتاج إلى إجراء بعض التهيئات وتعديلات على الشيفرة
  المصدرية. سنوضح لك ذلك واحدة تلو الأخرى.
figures: []
---

<meta property="og:title" content="使用 FASTBuild 编译 UE4 和 UE5" />

> تم اختبار أسلوب النص هذا وتوافق مع الإصدارات من UE4.27 إلى UE5.3. لم يتم اختباره مع الإصدارات الأخرى، ولكن يُمكن تجربتها.

##مقدمة

[FASTBuild](https://www.fastbuild.org/docs/home.html)هو أداة ترجمة موزعة مجانية ومفتوحة المصدر، إن عملية ترجمة UE تستغرق وقتًا طويلاً، وإذا تم استخدام FASTBuild، يمكن أن تقلل بشكل كبير من الوقت المستغرق.

UE ابتداءً من الإصدار 4.x يدعم FASTBuild، ويأتي مع الشفرة الأصلية أداة FASTBuild المعدلة بشكل سحري، ذات الاعتماد على إصدار 0.99 من FASTBuild، توجد في المسار `Engine\Extras\ThirdPartyNotUE\FASTBuild`. يستخدم UE5.3 نفس الإصدار أيضًا. هذا الإصدار قديم نسبيًا، وإلى تاريخ إنشاء هذا المقال، آخر إصدار رسمي لـ FASTBuild هو 1.11، يوفر المزيد من الوظائف الجديدة وإصلاحات الأخطاء. يهدف هذا المقال بشكل خاص إلى توثيق كيفية استخدام الإصدار 1.11 بدعم متزامن لـ UE4 و UE5.

##إعداد سهل

لتحقيق الهدف، نحتاج إلى إجراء بعض التعديلات على FASTBuild 1.11 وشفرة UE. في الواقع، لقد قمت بجميع التعديلات هنا، لذا يمكننا استخدام النسخة التي قمت بتعديلها مباشرة.

قم بتنزيل الإصدار [الأحدث](https://github.com/disenone/fastbuild/releases)ترجمة النص إلى اللغة العربية:

الملفات التنفيذية الداخلية are FBuild.exe، FBuildCoordinator.exe، FBuildWorker.exe. لتوضيح الأمور، سأشير إلى الجهاز الذي يستخدم FBuild.exe في البرمجة بـ "جهاز المضيف"، وأشير إلى الأجهزة البعيدة التي تقدم معالجاتها للمساعدة في التحرير بـ "الأجهزة البعيدة".

###تكوين الجهاز

أضف مسار دليل FBuild.exe إلى متغير البيئة النظامي Path، لضمان إمكانية تنفيذ FBuild.exe مباشرة في cmd.

تكوين دليل المشاركة للذاكرة المخبأة (إذا لم يكن من الضروري إنشاء الذاكرة المخبأة، يمكن عدم التكوين): اجعل دليلًا فارغًا مسارًا مشتركًا، وتأكد من أن الجهاز البعيد يمكنه الوصول إليه.

افتح مشروع المصدر لـ UE4 / UE5 على هذا الجهاز، وقم بتعديل ملف تكوين التجميع Engine\Saved\UnrealBuildTool\BuildConfiguration.xml كما يلي:

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

قم بتشغيل FBuildCoordinator.exe الذي تم تنزيله قبل تشغيل هذا الجهاز.

###تكوين الجهاز عن بُعد

نفس إعدادات Cache، فقط يجب تحديد عنوان الـ ip إلى عنوان الـ ip المحلي، وهنا نفترض أنه 192.168.1.100.

- FASTBUILD_CACHE_PATH: \\192.168.1.100\Cache
- FASTBUILD_CACHE_MODE: rw

نفس تكوين عنوان IP للتنسيق

- FASTBUILD_COORDINATOR: 192.168.1.100

يرجى ترتيب كما هو موضح في الصورة أدناه.

![](assets/img/2023-ue-fastbuild/remote_vars.png)

قم بتشغيل FBuildWorker.exe على الجهاز عن بُعد. إذا تم الضبط بنجاح، يجب أن ترى سجلات على FBuildCoordinator.exe على الجهاز المحلي (حيث أن 192.168.1.101 هو عنوان الآي بي للجهاز عن بُعد).

```
FBuildCoordinator - v1.11-UE
[2023-12-01-20:06:38] Listening on port 31392
[2023-12-01-20:06:38] current [0] workers: []
[2023-12-01-20:06:42] New worker available: 192.168.1.101
[2023-12-01-20:06:42] current [1] workers: [192.168.1.101]
```

###اختبار UE التجميع

افتح مشروع كود مصدر UE باستخدام VisualStudio، واختر مشروع C++، ثم انقر على "إعادة البناء". إذا كانت الإعدادات صحيحة، يمكنك رؤية سجلات مشابهة لما يلي.

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

يمكن لـ FASTBuild العثور على عنوان IP للجهاز عن بُعد وبدء إرسال الترجمة إليه. يمكن رؤية المهام التي تجري الترجمة حاليًا على FBuildWorker الخاص بالجهاز عن بُعد.

##تحسين التكوين

###دعم الإصدارات الأقدم لـ UE

إذا وجدت أن محرك UE الخاص بك لا يحتوي على أداة FASTBuild (Engine\Extras\ThirdPartyNotUE\FASTBuild)، وأن مشروع UnrealBuildTool لا يحتوي على ملف FASTBuild.cs، فمن المحتمل جداً أن إصدار UE الخاص بك لا يدعم FASTBuild بعد.

إذا كنت بحاجة إلى المرجع المصدري لـ UE4.27 ، قم بإنشاء ملف FASTBuild.cs مماثل وأضف التعديلات اللازمة على أكواد البرنامج الأخرى. لن أقوم بتوضيح ذلك هنا.


###قم بتجميع FastBuild الخاص بك.

إذا كنت مهتمًا بـ FASTBuild نفسه، أو ترغب في إجراء بعض التعديلات، يمكنك محاولة استخدام FASTBuild لتجميع FASTBuild.

- تحميل [الكود المصدري الأحدث](https://github.com/disenone/fastbuild/releases)，解压 
- قم بتعديل External\SDK\VisualStudio\VS2019.bff، وأعد كتابة .VS2019_BasePath و .VS2019_Version لتتوافق مع المحتوى الموجود على جهازك المحلي. يمكنك العثور على النسخة في الدليل .VS2019_BasePath\Tools\MSVC، على سبيل المثال.
    ```
    .VS2019_BasePath        = 'C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC'    // <-- Set path here
    .VS2019_Version         = '14.29.30133' // <-- Set version here
    .VS2019_MSC_VER         = '1929' // <-- Set MSC_VER here
    ```

قم بتعديل .Windows10_SDKBasePath و .Windows10_SDKVersion في ملف External\SDK\Windows\Windows10SDK.bff، يمكنك العثور على الإصدار في مسار .Windows10_SDKBasePath/bin.
    ```
    .Windows10_SDKBasePath        = 'C:\Program Files (x86)\Windows Kits/10'    // <-- Set path here
    .Windows10_SDKVersion         = '10.0.19041.0' // <-- Set version here
    ```

قم بتعديل الملف External\SDK\Clang\Windows\Clang11.bff الخاص بالمسار الأساسي لـ .Clang11_BasePath و .Clang11_Version، حيث يكون المسار في .VS2019_BasePath\Tools\Tools/LLVM/x64.
    ```
    .Clang11_BasePath = 'C:/Program Files (x86)/Microsoft Visual Studio/2019/Professional/VC/Tools/LLVM/x64'    // <-- Set path here
    .Clang11_Version  = '12.x.x'
    ```

ادخل إلى دليل Code ، وقم بتنفيذ `FBuild.exe All-x64-Release` في cmd ، إذا كانت الإعدادات صحيحة ، يجب أن ترى أن البناء قد نجح ، وبإمكانك أن تجد FBuild.exe في tmp\x64-Release\Tools\FBuild\FBuild.

`FBuild.exe All-x64-Release -dist -coordinator=127.0.0.1` يمكن أن يُشغّل الترجمة الموزعة.

###بناء علامة تِجاريّة المزيد من الخيارات

أنا أقدم FBuild الذي يدعم الخيارات الشائعة التالية:

- المنسق: تحديد عنوان IP الخاص بالمنسق (يمكن أن يتجاوز قيمة متغير البيئة النظامية)
- الوساطة: تحديد عنوان الوساطة (يمكن أن يتجاوز قيمة متغيرات البيئة النظامية)
- nocache: اجبار على عدم استخدام الكاش
- dist: تمكين الترجمة الموزعة
- forceremote: إجبار على التجميع على الجهاز البعيد
ملخص: بعد انتهاء التحرير، يتم إخراج تقرير الإحصاءات.

انتظر، يمكن تشغيل المزيد من الخيارات باستخدام `FBuild.exe -help` للعرض.

FBuildWorker الخيارات الشائعة الاستخدام هي:

- المنسق: تحديد عنوان IP للمنسق (يمكن أن يتجاوز قيمة متغيرات البيئة في النظام)
- brokerage: تحديد عنوان Brokerage (يمكنه تغطية قيمة متغيرات بيئة النظام)
- nocache: اجبار على عدم استخدام التخزين المؤقت
- cpus: تحديد عدد الأنوية المتاحة للمشاركة في عملية الترجمة

يمكن تشغيل المزيد من الخيارات باستخدام `FBuildWorder.exe -help` للاطلاع.

###تعديل ملف FASTBuild.cs المرفق مع UE

ترجمة النص إلى اللغة العربية:

الملف FASTBuild.cs المضمّن في UE لا يعامل المتغيرات البيئية للنظام بشكل جيد، حيث يتم من خلاله تفضيل العديد من المعلمات المحددة في ملف BuildConfiguration.xml مقارنة بالمتغيرات البيئية للنظام، وهذا بوضوح يخالف منطق استخدام ملف BuildConfiguration.xml.

لذلك ، يمكن تغيير الشفرة ذات الصلة إلى هذا الشكل ، هنا نأخذ UE5.3 كمثال:

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

###تكوين البناء.xml تكوين متقدم

```xml
<?xml version="1.0" encoding="utf-8" ?>
<Configuration xmlns="https://www.unrealengine.com/BuildConfiguration">
    <ProjectFileGenerator>
<!-- تحديد إصدار VS -->
        <Format>VisualStudio2022</Format>
    </ProjectFileGenerator>
    <BuildConfiguration>
<!-- تشغيل FASTBuild -->
        <bAllowFASTBuild>true</bAllowFASTBuild>
<!-- حدد عدد أنوية معالج الـ CPU المشاركة في عملية الترجمة الخاصة بالجهاز الحالي -->
        <MaxParallelActions>12</MaxParallelActions>
<!-- إغلاق Incredibuild -->
        <bAllowXGE>false</bAllowXGE>
    </BuildConfiguration>
    <FASTBuild>
<!-- تحديد مسار FBuild -->
        <FBuildExecutablePath>d:\libs\FASTBuild\bin\FBuild.exe</FBuildExecutablePath>
<!-- فتح الترجمة الموزعة -->
        <bEnableDistribution>true</bEnableDistribution>
<!-- حدد مسار الوساطة -->
        <FBuildBrokeragePath>\\127.0.0.1\Brokerage\</FBuildBrokeragePath>
<!-- تحديد مسار التخزين المؤقت -->
        <FBuildCachePath>\\127.0.0.1\Cache\</FBuildCachePath>
<!-- تمكين الذاكرة المؤقتة -->
        <bEnableCaching>true</bEnableCaching>
<!-- إذن القراءة والكتابة للذاكرة Read/Write/ReadWrite -->
        <CacheMode>ReadWrite</CacheMode>
<!-- تحديد عنوان IP للمنسق -->
        <FBuildCoordinator>127.0.0.1</FBuildCoordinator>
<!-- إجبار الترجمة عن بُعد -->
        <!-- <bForceRemote>true</bForceRemote> -->
    </FASTBuild>
</Configuration>
```

--8<-- "footer_ar.md"


> هذه المشاركة تمت ترجمتها باستخدام ChatGPT، يرجى تقديم [**ردود**](https://github.com/disenone/wiki_blog/issues/new)يرجى الإشارة إلى أي نقاط مفقودة. 
