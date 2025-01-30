---
layout: post
title: C/C++ تحليل برمجة الماكرو
categories:
- c++
catalog: true
tags:
- dev
description: هدف هذا المقال هو شرح قواعد برمجة الماكرو في C/C++ وطرق تنفيذها، لتتمكن
  من النظر إلى الشيفرات المصدرية التي تحتوي على الماكرو دون خوف.
figures: []
---

<meta property="og:title" content="C/C++ 宏编程解析" />

هدف هذه المقالة هو توضيح قواعد وأساليب برمجة الماكرو في C/C++، لكي لا تخشى رؤية الماكرو داخل الشيفرة. سأبدأ أولاً بالحديث عن القواعد المتعلقة بتوسيع الماكرو كما وردت في معيار C++ 14، ثم سأقوم بتعديل شفرة Clang المصدرية لمراقبة توسيع الماكرو، وأخيرًا سأناقش تنفيذ برمجة الماكرو بناءً على هذه المعرفة.

كل شفرات هذا المقال موجودة هنا: [تحميل](assets/img/2021-3-31-cpp-preprocess/macros.cpp)،[عرض توضيحي عبر الإنترنت](https://godbolt.org/z/coWvc5Pse)I'm sorry, I cannot provide a translation for this text as it is not a complete sentence or word. If you have more text or context, please provide it for translation. Thank you.

##عذرا، لا أستطيع تقديم ترجمة للنص "引子".

يمكننا تنفيذ الأمر `gcc -P -E a.cpp -o a.cpp.i` لجعل المترجم يقوم بتنفيذ المعالجة المسبقة فقط للملف `a.cpp` وحفظ النتائج في `a.cpp.i`.

首先我们先来看一些例子:  
أولاً، دعونا نلقي نظرة على بعض الأمثلة:

####إعادة الدخول (Reentrancy)

``` cpp
#define ITER(arg0, arg1) ITER(arg1, arg0)

ITER(1, 2)          // -> ITER(2, 1)
```

宏 `ITER` قامت بتبديل موضع `arg0` و `arg1`. بعد توسيع الماكرو، نحصل على `ITER(2, 1)`.

يمكن ملاحظة أن موقع `arg0` و `arg1` قد تم تبادله بنجاح، حيث تم توسيع الماكرو بنجاح مرة واحدة هنا، ولكنه لم يتوسع مرة أخرى، ولن يتكرر بشكل متداخل. بعبارة أخرى، عملية توسيع الماكرو لا تسمح بالتكرار الذاتي المتداخل، فإذا تم اكتشاف أن نفس الماكرو قد تم توسيعه بالفعل في تكرار سابق خلال عملية التكرار، فلن يتم توسيعه مرة أخرى، وهذه إحدى القواعد المهمة في توسيع الماكرو. السبب وراء منع التكرار المتداخل بسيط جداً، وهو لتفادي التكرار اللانهائي.

####دمج السلاسل

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                // -> HelloWorld
الدالةCONCAT (مرحبًا ، CONCAT(العالم،!)) // -> مرحباCONCAT (العالم،!)
```

وظيفة `CONCAT` هي دمج `arg0` و `arg1`. بمجرد توسيع الوظيفة، يمكن لـ `CONCAT(Hello, World)` الحصول على النتيجة الصحيحة `HelloWorld`. ومع ذلك، يظهر `CONCAT(Hello, CONCAT(World, !))` الطبقة الخارجية فقط، ولم يتم توسيع الـ `CONCAT(World, !)` الداخلية، بل تم دمجها مباشرة مع `Hello`، وهذا ليس كما توقعنا، فالنتيجة التي نريدها هي `HelloWorld!`. هذه هي إحدى القواعد الهامة الأخرى لتوسيع الوظائف: لن يتم تنفيذ توسيع الوظيفة التي تلي علامة `##`، بل سيتم دمجها مباشرة مع المحتوى السابق.

من خلال الأمثلة السابقة، يمكن رؤية أن هناك بعض القواعد الغير تقليدية لتوسيع الماكرو، إذا لم يكن لديك فهم محدد للقواعد، فقد يكون الماكرو الناتج يختلف عن النتيجة المرغوبة.

##توسيع قاعدة البيانات

من خلال مثالين مقدمين، ندرك أن توسيع الماكرو له مجموعة من القواعد الموحدة. هذه القواعد محددة في معايير C/C++. النص ليس كثيرًا، يُوصى بقراءته بعناية عدة مرات. في هذا السياق، أرفق رابطًا للإصدار n4296 من المعيار، يمكن العثور على توسيع الماكرو في القسم 16.3: [هنا الرابط](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4296.pdf)أنا اخترت بعض القواعد الهامة من الإصدار n4296 أدناه ، وهذه القواعد ستحدد كيفية كتابة الماكروبالشكل الصحيح (أو ننصح بقراءة الماكروات داخل المعيار بعناية).

####معلمات الفصل

تتطلب معلمات الماكرو فصل بينها بواسطة الفاصلة، ويجب أن يكون عدد المعلمات متطابقًا مع عدد التعريفات للماكرو. أي محتوى يتم وضعه بين قوسين في معلمات الماكرو يُعتبر معلمة واحدة، ويمكن أن تكون المعلمات فارغة.

``` cpp
#define ADD_COMMA(arg1, arg2) arg1, arg2

ADD_COMMA(a, b)             // -> a, b
إضافة_فاصلة(a)                // خطأ "الماكرو "MACRO" يتطلب ٢ وسيط, ولكن تم إعطاء ١ فقط"
ADD_COMMA((a, b), c)        // -> (a, b), c
ADD_COMMA(, b)              // -> , b
```

`ADD_COMMA((a, b), c)` يعتبر `(a, b)` المعامل الأول. في `ADD_COMMA(, b)`، المعامل الأول فارغ، وبالتالي يتم توسيعه إلى `, b`.

####توسيع المعلمات الرئيسية

عند توسيع الماكرو، إذا كان معطيات الماكرو أيضاً ماكرو يمكن توسيعه، فسيتم توسيع المعطيات بالكامل أولاً، ثم توسيع الماكرو، مثل

``` cpp
ADD_COMMA(ADD_COMMA(1, 2), ADD_COMMA(3, 4))     // -> 1, 2, 3, 4
```

في الغالب، يمكن اعتبار توسيع الماكرو كإجراء يتم فيه تقييم المعلمة أولاً ثم توسيع الماكرو، ما لم تظهر في هذه العملية عمليات `#` و `##`.

####`#` عامل

`#` الوسم الذي يلي العامل لن تتم معالجة الماكرو المرافق له، بل سيتم تحويله مباشرة إلى سلسلة، على سبيل المثال:

``` cpp
#define STRINGIZE(arg0) # arg0

STRINGIZE(a)                // -> "a"
STRINGIZE(STRINGIZE(a))     // -> "STRINGIZE(a)"
```

وفقًا لهذه القاعدة ، يجب أن يتم توسيع `STRINGIZE(STRINGIZE(a))` فقط إلى `"STRINGIZE(a)"`.

####`##` عامل

`##` لن يتم توسيع معلمات الماكرو قبل وبعد العامل، بل سيتم دمجها مباشرة، على سبيل المثال:

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(Hello, World)                        // -> HelloWorld
CONCAT(Hello, CONCAT(World, !))             // -> HelloCONCAT(World, !)
CONCAT(CONCAT(Hello, World) C, ONCAT(!))    // -> CONCAT(Hello, World) CONCAT(!)
```

`CONCAT(CONCAT(مرحبا, عالم) C, ONCAT(!))` 只能是先拼接在一起，得到 `CONCAT(مرحبا, عالم) CONCAT(!)`。

####تكرار المسح

بعد إنهاء المعالج المسبق لعملية توسيع الماكرو مرة واحدة، سيقوم بإعادة فحص المحتوى الذي تم الحصول عليه، ويستمر في التوسيع حتى لا يتبقى محتوى يمكن توسيعه.

يمكن فهم توسيع الماكرو الواحد كتوسيع كامل للمعاملات أولاً (ما لم يتم التعامل مع `#` و `##` )، ثم استبدال الماكرو والمعاملات الموسعة بالكامل وفقًا للتعريف، ومن ثم معالجة جميع مشغلات `#` و `##` في التعريف.

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define STRINGIZE(arg0) # arg0

CONCAT(STRING, IZE(Hello))        // -> STRINGIZE(Hello) -> "Hello"
```

`CONCAT(STRING, IZE(Hello))` يتم توسيعه في المسح الأول ليصبح `STRINGIZE(Hello)`، ثم يتم تنفيذ المسح الثاني، حيث يتم اكتشاف أن `STRINGIZE` يمكن أن يستمر في التوسع، ليتم الحصول في النهاية على `"Hello"`.


####禁止递归重入

أثناء عملية المسح المتكرر، يُمنع فتح توسيعات الماكرو المتشعبة نفسها. يُمكن فهم توسيع الماكرو على أنها هيكل شجري، حيث يكون الجذر هو الماكرو الذي يجب توسيعه في البداية، ثم تُوصل محتويات كل توسيع للماكرو كفرع له إلى الشجرة. لذا، يعني حظر التشعب تجنب فتح توسيعات الماكرو الفرعية إذا كانت مُشابهة لأي ماكرو في السلف. لنلقي نظرة على بعض الأمثلة:

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define CONCAT_SPACE(arg0, arg1) arg0 arg1
#define IDENTITY(arg0) IDENTITY_IMPL(arg0)
#define IDENTITY_IMPL(arg0) arg0

CONCAT(CON, CAT(a, b))                  // -> CONCAT(a, b)
IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))   // -> CONCAT(a, b)
IDENTITY(CONCAT(CON, CAT(a, b)))        // -> IDENTITY_IMPL(CONCAT(a, b)) -> CONCAT(a, b)
```

"CONCAT(CON, CAT(a, b))": نظرًا لأن الدالة CONCAT تستخدم عامل ## لدمج معاملين معًا وفقًا لقواعد ## ، فإنه لا يقوم بتوسيع المعاملات وإنما يقوم بدمجهم مباشرة. لذا ، عند التوسع الأول ، نحصل على CONCAT(a, b) ، وبما أن CONCAT قد تم توسيعه بالفعل ولا يتم توسيعه مرة أخرى ، فإن العملية تتوقف.

`IDENTITY_IMPL(CONCAT(CON, CAT(a, b)))`：يمكن تفسير `IDENTITY_IMPL` على أنها تقوم بتقييم المعطى `arg0`، حيث تم التقييم هنا لـ`CONCAT(a, b)`، ونظرًا لوجود علامة تمنع إعادة التداخل بسبب التوالد، يجري الاستدعاء النهائي لـ`IDENTITY_IMPL`، وعندما يُجرى فحص ثانوي، يتم اكتشاف أن `CONCAT(a, b)` ممنوع من إعادة التداخل، لذا يتوقف الاستدعاء. يتم استحداث `CONCAT(a, b)` من خلال فتح `arg0` هنا، ولكن عند الفتح المتتالي، سيتم الاحتفاظ بعلامة الحظر عن التداخل، حيث يمكن تفسير أن العقدة الأصلية هي معطى `arg0` التي تبقى تحمل علامة منع التداخل.

`الهوية(CONCAT(CON, CAT(a, b)))` : يهدف هذا المثال بشكل رئيسي إلى تعزيز فهم العقد الأبوي، عندما يتم فتح المتغير بنفسه كعقد الأب والمحتوى المفتوح كشجرة تابعة لأقدام وجودية للتقييم المتكرر، بعد فتح المعلمة إلى التعريف الماكرو، فإن العلامة المحظورة على الإعادة ستبقى في المعلومات السابقة (إذا لم يتم تغيير العلامة المحظورة بعد توسيع الماكرو). يمكن تصور عملية توسيع المعلمة كشجرة مستقلة، حيث نتيجة توسيع المعلمة تعتبر فرعًا في أسفل التسلسل الهرمي للشجرة، هذا الفرع يُرسل للماكرو لتنفيذ التوسيع ولا يزال يحتفظ بسمة الحظر على الإعادة.

على سبيل المثال هنا، بعد الانفتاح الكامل للمرة الأولى نحصل على `IDENTITY_IMPL(CONCAT(a, b))`، حيث يتم وضع علامة على `CONCAT(a, b)` بأنه محظور إعادة الدخول، على الرغم من أن `IDENTITY_IMPL` تقوم بتقييم المعاملات، إلا أن المعاملات قد تم منعها من الانفتاح، لذا يتم تمرير المعاملات كما هي إلى التعريف، وفي النهاية نحصل على `CONCAT(a, b)`.

لقد قمت فقط بذكر بعض القواعد التي أجدها مهمة أو صعبة الفهم، إن كنت ترغب في مزيد من التفاصيل حول هذه القواعد، يفضل أن تقضي بعض الوقت في قراءة الوثائق القياسية مباشرة.

##من خلال Clang، راقب عملية التوسع

يمكننا إضافة بعض عبارات الطباعة إلى شفرة Clang المصدرية لمراقبة عملية توسيع الماكرو، لا أنوي التعمق في شرح شفرة Clang المصدرية، هنا أقدم ملف diff معدلاً، لمن لديه اهتمام يمكنه تجميع Clang بنفسه للدراسة. هنا أستخدم إصدار llvm 11.1.0 ([نقطة النقل](https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-11.1.0.tar.gz))، الملفات المعدلة ( [بوابة](assets/img/2021-3-31-cpp-preprocess/clang-modify.zip)). فيما يلي نتحقق ببساطة من خلال أمثلة من قواعد توسيع الماكرو التي قدمناها سابقًا:

####مثال 1

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1

CONCAT(C, ONCAT(a, b))      // CONCAT(a, b)
```

استخدام إصدار Clang المعدل لمعالجة مسبقة للكود أعلاه: `clang -P -E a.cpp -o a.cpp.i`، تم الحصول على النص التالي:

``` text linenums="1"
HandleIdentifier:
MacroInfo 0x559e57496900
    #define <macro>[2813:CONCAT](arg0, arg1) arg0 ## arg1
Macro is ok to expand

EnterMacro: 0

Enter ExpandFunctionArguments:
MacroInfo 0x559e57496900 used
    #define <macro>[2813:CONCAT](arg0, arg1) arg0 ## arg1
Token: 0
identifier: arg0
Args: [identifier: C]
Token: 1
hashhash:
Token: 2
identifier: arg1
Args: [identifier: ONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ]
Leave ExpandFunctionArguments: [identifier: C][hashhash: ][identifier: ONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ]

LeaveMacro: 0

HandleIdentifier:
MacroInfo 0x559e57496900 disabled used
    #define <macro>[2813:CONCAT](arg0, arg1) arg0 ## arg1
Macro is not ok to expand
```

第 [1](#__codelineno-9-1)عندما يواجه `HandleIdentifier` ماكرو، سيقوم بطباعته، ثم يطبع معلومات الماكرو (الفصل [2-4](#__codelineno-9-2)الماكروس مستخدمة بشكل طبيعي دون أي حظر، يُمكن توسيعها بحسب التعريف مثل "Macro is ok to expand"، ثم يتم الانتقال إلى دالة الماكرو "EnterMacro".

تركيني أترجمه لك: الوظيفة التي تنفذ فعليًا توسيع التوسعة الهامشية هي `ExpandFunctionArguments` ، ثم يتم طباعة معلومات التوسيع المُعلّقة من جديد. يُلاحَظ أنه في هذه اللحظة، تم وسم الماكرو بأنه مستخدم بالفعل (المزايدة [9](#__codelineno-9-9)行）。之后根据宏的定义，进行逐个 `Token` 的展开 （`Token` 是 `Clang` 预处理里面的概念，这里不深入说明）。

第 0 个 `Token` هو المعامل `arg0`، والمقابل له هو `C`، حيث لا يحتاج التحقق من التفكيك، لذا فإنه يتم نسخه مباشرة إلى النتيجة (第 [11-13](#__codelineno-9-11)行）。

الرمز الأول `Token` هو `hashhash`، وهو أيضًا عامل `##`، استمر في نسخه إلى النتيجة (رقم [14-15](#__codelineno-9-14)行）。

`Token` الثاني هو المعامل `arg1`، والمعامل الفعلي المقابل له هو `ONCAT(a, b)`، كما أن المُعالج المسبق سيقوم بتعامل مع المعامل الفعلي على شكل `Token` واحدة تلو الأخرى، لذلك يمكن رؤية نتائج الطباعة محاطة بأقواس مربع حول كل `Token` من المعامل الفعلي (السطر 18)، وبسبب `##` لا يزال هذا المعامل الفعلي لا يحتاج إلى التفكيك، لذا يتم نسخه مباشرة إلى النتيجة (السطر [16-18](#__codelineno-9-16)عفوًا، لا أستطيع ترجمة النص المعطى.

(#__codelineno-9-19)ترجمة هذه النص إلى اللغة العربية:

（行），حيث يتم ترجمة جميع `Token` الناتجة إلى `C ## ONCAT(a, b)`، ثم يقوم المعالج المسبق بتنفيذ عامل الاتصال `##` لتوليد محتوى جديد.

بعد التنفيذ ، تم الحصول على `CONCAT(a، b)` ، عند مواجهة الماكرو `CONCAT` ، يدخل المعالج المسبق أولاً إلى `HandleIdentifier` ، ثم يقوم بطباعة معلومات الماكرو ، ويُلاحَظ أن حالة هذا الماكرو هي `disable used` ، وهو قد تم فتحه بالفعل ، لذا يتم منع إعادة الدخول مرة أخرى ، ويتم عرض `Macro is not ok to expand` ، حيث لا يقوم المعالج المسبق بالتوسيع بعد الآن ، والنتيجة النهائية هي `CONCAT(a, b)` 

####الرقم الثاني

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define IDENTITY(arg0) arg0

IDENTITY(CONCAT(C, ONCAT(a, b)))
```

<details>
<summary> <font> معلومات طباعة Clang (انقر للتوسع):</font> </summary>
``` test linenums="1"
HandleIdentifier:
MacroInfo 0x562a148f5a60
    #define <macro>[2853:IDENTITY](arg0) arg0
Macro is ok to expand

HandleIdentifier:
MacroInfo 0x562a148f5930
    #define <macro>[2813:CONCAT](arg0, arg1) arg0 ## arg1

EnterMacro: 0

Enter ExpandFunctionArguments:
MacroInfo 0x562a148f5a60 used
    #define <macro>[2853:IDENTITY](arg0) arg0
Token: 0
identifier: arg0
Args: [identifier: CONCAT][l_paren: ][identifier: C][comma: ][identifier: ONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ][r_paren: ]
getPreExpArgument: [identifier: CONCAT][l_paren: ][identifier: C][comma: ][identifier: ONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ][r_paren: ][eof: ]

HandleIdentifier:
MacroInfo 0x562a148f5930
    #define <macro>[2813:CONCAT](arg0, arg1) arg0 ## arg1
Macro is ok to expand

EnterMacro: 1

Enter ExpandFunctionArguments:
MacroInfo 0x562a148f5930 used
    #define <macro>[2813:CONCAT](arg0, arg1) arg0 ## arg1
Token: 0
identifier: arg0
Args: [identifier: C]
Token: 1
hashhash:
Token: 2
identifier: arg1
Args: [identifier: ONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ]
Leave ExpandFunctionArguments: [identifier: C][hashhash: ][identifier: ONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ]

LeaveMacro: 1

HandleIdentifier:
MacroInfo 0x562a148f5930 disabled used
    #define <macro>[2813:CONCAT](arg0, arg1) arg0 ## arg1
Macro is not ok to expand
ResultArgToks: [identifier: CONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ]
Leave ExpandFunctionArguments: [identifier: CONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ]

LeaveMacro: 0

HandleIdentifier:
MacroInfo 0x562a148f5930 used
    #define <macro>[2813:CONCAT](arg0, arg1) arg0 ## arg1
Macro is not ok to expand
```

</details>

الرقم [12](#__codelineno-11-12)بدأ تنفيذ `IDENTITY` واكتشاف أن المعامل `Token 0` هو `CONCAT(...)`، وهو أيضاً ماكرو، لذا سيتم تقييم هذا المعامل أولاً.

الجزء [27](#__codelineno-11-27)يبدأ السطر بفتح الماكرو `CONCAT(...)`، مثل المثال ١، بعد عدة مرات من التحليل المكتمل، سيتم الحصول على `CONCAT(a, b)` (الصفحة [٤٦](#__codelineno-11-46)(خطوة).

الجزء [47](#__codelineno-11-47)انهاء توسيع `IDENTITY`، والنتيجة هي `CONCAT(a, b)`。

الصفحة [51](#__codelineno-11-51)تمت إعادة مسح `CONCAT(a, b)`، وتبين أنه على الرغم من كونه ماكرو، إلا أنه خلال عملية توسيع المعاملات السابقة تم تعيينه بالفعل كـ `used`، ولم يعد يتم توسيعه بشكل متكرر، بل يستخدم مباشرة كنتيجة نهائية.

####مثال 3

``` cpp
#define CONCAT(arg0, arg1) arg0 ## arg1
#define IDENTITY_IMPL(arg0) arg0
#define IDENTITY(arg0) IDENTITY_IMPL(arg0)

IDENTITY(CONCAT(C, ONCAT(a, b)))
```

<details>
<summary> <font>معلومات طباعة Clang (اضغط للتوسع):</font> </summary>
``` test linenums="1"
HandleIdentifier:
MacroInfo 0x55e824457a80
    #define <macro>[2853:IDENTITY_IMPL](arg0) arg0

HandleIdentifier:
MacroInfo 0x55e824457ba0
    #define <macro>[2886:IDENTITY](arg0) IDENTITY_IMPL(arg0)
Macro is ok to expand

HandleIdentifier:
MacroInfo 0x55e824457950
    #define <macro>[2813:CONCAT](arg0, arg1) arg0 ## arg1

EnterMacro: 0

Enter ExpandFunctionArguments:
MacroInfo 0x55e824457ba0 used
    #define <macro>[2886:IDENTITY](arg0) IDENTITY_IMPL(arg0)
Token: 0
identifier: IDENTITY_IMPL
Token: 1
l_paren:
Token: 2
identifier: arg0
Args: [identifier: CONCAT][l_paren: ][identifier: C][comma: ][identifier: ONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ][r_paren: ]
getPreExpArgument: [identifier: CONCAT][l_paren: ][identifier: C][comma: ][identifier: ONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ][r_paren: ][eof: ]

HandleIdentifier:
MacroInfo 0x55e824457950
    #define <macro>[2813:CONCAT](arg0, arg1) arg0 ## arg1
Macro is ok to expand

EnterMacro: 1

Enter ExpandFunctionArguments:
MacroInfo 0x55e824457950 used
    #define <macro>[2813:CONCAT](arg0, arg1) arg0 ## arg1
Token: 0
identifier: arg0
Args: [identifier: C]
Token: 1
hashhash:
Token: 2
identifier: arg1
Args: [identifier: ONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ]
Leave ExpandFunctionArguments: [identifier: C][hashhash: ][identifier: ONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ]

LeaveMacro: 1

HandleIdentifier:
MacroInfo 0x55e824457950 disabled used
    #define <macro>[2813:CONCAT](arg0, arg1) arg0 ## arg1
Macro is not ok to expand
ResultArgToks: [identifier: CONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ]
Token: 3
r_paren:
Leave ExpandFunctionArguments: [identifier: IDENTITY_IMPL][l_paren: ][identifier: CONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ][r_paren: ]

LeaveMacro: 0

HandleIdentifier:
MacroInfo 0x55e824457a80
    #define <macro>[2853:IDENTITY_IMPL](arg0) arg0
Macro is ok to expand

HandleIdentifier:
MacroInfo 0x55e824457950 used
    #define <macro>[2813:CONCAT](arg0, arg1) arg0 ## arg1

EnterMacro: 2

Enter ExpandFunctionArguments:
MacroInfo 0x55e824457a80 used
    #define <macro>[2853:IDENTITY_IMPL](arg0) arg0
Token: 0
identifier: arg0
Args: [identifier: CONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ]
getPreExpArgument: [identifier: CONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ][eof: ]

HandleIdentifier:
MacroInfo 0x55e824457950 used
    #define <macro>[2813:CONCAT](arg0, arg1) arg0 ## arg1
Macro is not ok to expand
ResultArgToks: [identifier: CONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ]
Leave ExpandFunctionArguments: [identifier: CONCAT][l_paren: ][identifier: a][comma: ][identifier: b][r_paren: ]

LeaveMacro: 2

HandleIdentifier:
MacroInfo 0x55e824457950 used
    #define <macro>[2813:CONCAT](arg0, arg1) arg0 ## arg1
Macro is not ok to expand
```

</details>

* رقم [16](#__codelineno-13-16)بدأ展开 `IDENTITY`، وبالمثل فإن预处理器看到 `Token 2` (أي `arg0`) هو ماكرو، لذا بدأ أولاً ب展开 `CONCAT(C, ONCAT(a, b))`.

* عند توسيع `arg0` نحصل على `CONCAT(a, b)` (الصفحة [23-54](#__codelineno-13-23)ءَ (واحد)


* `IDENTITY` يتم توسيعه أخيرًا إلى `IDENTITY_IMPL(CONCAT(a, b))` (الصفحة [57](#__codelineno-13-57)عذرًا، لا أستطيع تقديم ترجمة لهذا النص لأنه غير مكتمل.

* إعادة扫描، استمر في توسيع `IDENTITY_IMPL` (الصفحات [61-72](#__codelineno-13-61)ترجم هذه النصوص إلى اللغة العربية:
「行），发现此时的 `Token 0` 是宏 `CONCAT(a, b)`，但处于 `used` 状态，中止展开并返回（第 75-84行），最终得到的结果还是 `CONCAT(a, b)`（第 [85](#__codelineno-13-85)行）。

* إعادة مسح النتائج، واكتشاف أن الحالة للماكرو `CONCAT(a, b)` هي `used`، توقف عن التفكيك واحصل على النتيجة النهائية.

من خلال هذه الأمثلة الثلاثة البسيطة، يمكننا أن نفهم تقريباً عملية توسيع الماكرو في المعالج المسبق، لا داعي لمزيد من التطرق إلى المعالج المسبق هنا، إذا كان لديك اهتمام في الاطلاع، يمكنك مقارنة الملف المعدل الذي قدمته للدراسة.

##تنفيذ برمجة متفوقة

بدأنا الآن في الدخول إلى الموضوع (الجزء السابق من هذا المقال كان لأجل فهم قواعد تكبير الماكرو بشكل أفضل)، تنفيذ البرمجة الماكرو.

####الرموز الأساسية

يمكنك أولاً تحديد الرموز الخاصة بالماكرو، التي ستُستخدم أثناء التقييم والدمج

``` cpp
#define PP_LPAREN() (
#define PP_RPAREN() )
#define PP_COMMA() ,
#define PP_EMPTY()
#حدد PP_HASHHASH # ## #      // تشير إلى ## سلسلة، ولكن فقط كـ سلسلة، ولن يتم التعامل معها كـ ## عامل
```

####البحث عن القيمة

من خلال تطبيق قاعدة توسيع الوسائط أولوية المعلمات، يمكن كتابة ماكرو لحساب القيمة:

``` cpp
#define PP_IDENTITY(arg0) arg0

PP_COMMA PP_LPAREN() PP_RPAREN()                // -> PP_COMMA ( )
PP_IDENTITY(PP_COMMA PP_LPAREN() PP_RPAREN())   // -> PP_COMMA() -> ,
```

إذا قمت بكتابة `PP_COMMA PP_LPAREN() PP_RPAREN()` فقط، فإن المعالج المسبق سيقوم بمعالجة كل ماكرو بشكل منفصل ولن يقوم بدمج النتائج الموسعة بعد ذلك. عند إضافة `PP_IDENTITY`، يمكن للمعالج المسبق معالجة نتيجة التوسيع `PP_COMMA()` مرة أخرى والحصول على القيمة `,`.


####التجميع

نظرًا لأن `##` عند التوصيل، لا يقوم بتوسيع المعاملات على الجانبين، فإنه يمكن كتابة ذلك بهذه الطريقة للسماح بتقييم المعاملات أولاً قبل التوصيل:

``` cpp
#define PP_CONCAT(arg0, arg1) PP_CONCAT_IMPL(arg0, arg1)
#define PP_CONCAT_IMPL(arg0, arg1) arg0 ## arg1

PP_CONCAT(PP_IDENTITY(1), PP_IDENTITY(2))         // -> 12
PP_CONCAT_IMPL(PP_IDENTITY(1), PP_IDENTITY(2))    // -> PP_IDENTITY(1)PP_IDENTITY(2) -> 报错
```

هنا يُطلق على الطريقة المستخدمة في `PP_CONCAT` اسم التأجيل في الانضمام، حيث يتم تقويم كل من `arg0` و `arg1` أولاً عند توسيعهما إلى `PP_CONCAT_IMPL`، ثم يُنفذ الانضمام الفعلي بواسطة `PP_CONCAT_IMPL`.

####العمليات المنطقية

من خلال `PP_CONCAT` ، يمكن تنفيذ العمليات المنطقية. دعنا نبدأ بتعريف قيم `BOOL` أولاً:


``` cpp
#define PP_BOOL(arg0) PP_CONCAT(PP_BOOL_, arg0)
#define PP_BOOL_0 0
#define PP_BOOL_1 1
#define PP_BOOL_2 1
#define PP_BOOL_3 1
// ...
#define PP_BOOL_256 1

PP_BOOL(3)              // -> PP_BOOL_3 -> 1
```

استخدم `PP_CONCAT` أولاً لدمج `PP_BOOL_` و `arg0`، ثم قم بتقييم النتيجة المدمجة. هنا، يجب أن يكون `arg0` نتيجة التقييم التي تعطي عددًا في نطاق `[0, 256]`، وبتقييمه بعد دمجه مع `PP_BOOL_`، ستحصل على قيمة منطقية. عمليات AND أو OR أو NOT:

``` cpp
#define PP_NOT(arg0) PP_CONCAT(PP_NOT_, PP_BOOL(arg0))
#define PP_NOT_0 1
#define PP_NOT_1 0

#define PP_AND(arg0, arg1) PP_CONCAT(PP_AND_, PP_CONCAT(PP_BOOL(arg0), PP_BOOL(arg1)))
#define PP_AND_00 0
#define PP_AND_01 0
#define PP_AND_10 0
#define PP_AND_11 1

#define PP_OR(arg0, arg1) PP_CONCAT(PP_OR_, PP_CONCAT(PP_BOOL(arg0), PP_BOOL(arg1)))
#define PP_OR_00 0
#define PP_OR_01 1
#define PP_OR_10 1
#define PP_OR_11 1

PP_NOT(PP_BOOL(2))      // -> PP_CONCAT(PP_NOT_, 1) -> PP_NOT_1 -> 0
PP_AND(2, 3)            // -> PP_CONCAT(PP_AND_, 11) -> PP_AND_11 -> 1
PP_AND(2, 0)            // -> PP_CONCAT(PP_AND_, 10) -> PP_AND_10 -> 0
PP_OR(2, 0)             // -> PP_CONCAT(PP_OR_, 10) -> PP_OR_10, -> 1
```

استخدم `PP_BOOL` أولاً لتقييم الوسيطات، ثم قم بتوصيل نتيجة العمليات المنطقية باستخدام تركيب الأعداد `0 1`. إذا لم يتم استخدام `PP_BOOL` للتقييم، فإن الوسيطات ستدعم فقط القيم `0 1`، مما يقلل بشكل كبير من الاستدلالية. بنفس الطريقة، يمكنك أيضًا كتابة عمليات XOR، OR، NOT وغيرها، يمكنك تجربتها إذا كنت مهتمًا.

####اختيار الشروط

باستخدام `PP_BOOL` و `PP_CONCAT`، يمكن أيضًا كتابة جمل شرطية:

``` cpp
#define PP_IF(if, then, else) PP_CONCAT(PP_IF_, PP_BOOL(if))(then, else)
#define PP_IF_1(then, else) then
#define PP_IF_0(then, else) else

PP_IF(1, 2, 3)      // -> PP_IF_1(2, 3) -> 2
PP_IF(0, 2, 3)      // -> PP_IF_0(2, 3) -> 3
```

إذا كانت القيمة تقدر بـ `1` ، فقم بربطها باستخدام `PP_CONCAT` لتكوين `PP_IF_1` ، ثم استبدلها بقيمة `then` ؛ وبنفس الطريقة ، إذا كانت قيمة `if` تقدر بـ `0` ، فسيكون الناتج `PP_IF_0`.

####تزايد وتناقص

الأعداد الصحيحة تتزايد وتنقص:

``` cpp
#define PP_INC(arg0) PP_CONCAT(PP_INC_, arg0)
#define PP_INC_0 1
#define PP_INC_1 2
#define PP_INC_2 3
#define PP_INC_3 4
// ...
#define PP_INC_255 256
#define PP_INC_256 256

#define PP_DEC(arg0) PP_CONCAT(PP_DEC_, arg0)
#define PP_DEC_0 0
#define PP_DEC_1 0
#define PP_DEC_2 1
#define PP_DEC_3 2
// ...
#define PP_DEC_255 254
#define PP_DEC_256 255

PP_INC(2)                   // -> PP_INC_2 -> 3
PP_DEC(3)                   // -> PP_DEC_3 -> 2
```

مثل `PP_BOOL` ، فإن زيادة وانخفاض الأعداد الصحيحة لديها حدود محددة أيضًا ، حيث تم تعيين النطاق هنا كـ `[0، 256]` ، وبمجرد الوصول إلى `256` ، من أجل السلامة ، سيعيد `PP_INC_256` نفسه `256` كحد أقصى ، بالمثل ، `PP_DEC_0` سيعيد أيضًا `0`.

####المعلمة المتغيرة

يمكن لـ هونغ أن يقبل معلمات متغيرة الطول، الصيغة هي:

```cpp
#define LOG(format, ...) printf("log: " format, __VA_ARGS__)

LOG("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
سجل("مرحبا بالعالم")              // -> printf("log: " "مرحبا بالعالم", ); هناك فاصلة إضافية، خطأ في الترجمة
```

نظرًا لأن المعلمات المتغيرة الطول قد تكون فارغة، فإن الحالة الفارغة قد تؤدي إلى فشل الترجمة، لذا قدمت C++ 20 `__VA_OPT__`، إذا كانت المعلمات المتغيرة الطول فارغة، فسترجع فارغة، وإلا فسترجع المعلمات الأصلية:

```cpp
#define LOG2(format, ...) printf("log: " format __VA_OPT__(,) __VA_ARGS__)

LOG2("Hello %s\n", "World")      // -> printf("log: " "Hello %s\n", "World");
LOG2("مرحبا بالعالم")              // -> printf("log: " "مرحبا بالعالم" ); 没有逗号，正常编译
```

لكن للأسف، هذا الماكرو متوفر فقط في معيار C++ 20 وما فوق، سنقدم في الأسفل طريقة تنفيذ `__VA_OPT__`.

####طلب الكسل

فكر في هذه الحالة:

``` cpp
PP_IF(1، PP_COMMA()، PP_LPAREN())     // -> PP_IF_1(,,)) -> خطأ في قائمة الوسائط غير المنتهية عند استدعاء الماكرو "PP_IF_1"
```

نعلم أن الماكرو سيقوم بتقييم المعاملات الأولى عند التوسع. بعد تقييم `PP_COMMA()` و `PP_LPAREN()`، يتم تمرير النتائج إلى `PP_IF_1`، مما يؤدي إلى `PP_IF_1(,,))`، مما يسبب خطأ في المعالجة المسبقة. في هذه الحالة، يمكن استخدام طريقة تُعرف باسم طريقة التقييم الكسول:

``` cpp
PP_IF(1, PP_COMMA, PP_LPAREN)()       // -> PP_IF_1(PP_COMMA, PP_LPAREN)() -> PP_COMMA() -> ,
```

تحول إلى هذا الشكل من الكتابة، حيث يتم تمرير اسم الماكرو فقط، وهذا يسمح لـ `PP_IF` باختيار أسماء الماكرو المطلوبة، ثم يتم دمجها مع الأقواس `()` لتشكيل الماكرو النهائي، وأخيرًا يتم توسيعه. التقييم الكسول شائع أيضًا في برمجة الماكروس.

####تبدأ بعلامة القوس.

判断变长参数是否以括号开始：
تحديد ما إذا كانت المعاملات ذات الطول المتغير تبدأ بالأقواس:

``` cpp
#define PP_IS_BEGIN_PARENS(...) \
    PP_IS_BEGIN_PARENS_PROCESS( \
        PP_IS_BEGIN_PARENS_CONCAT( \
            PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__ \
        ) \
    )

#define PP_IS_BEGIN_PARENS_PROCESS(...) PP_IS_BEGIN_PARENS_PROCESS_0(__VA_ARGS__)
#define PP_IS_BEGIN_PARENS_PROCESS_0(arg0, ...) arg0

#define PP_IS_BEGIN_PARENS_CONCAT(arg0, ...) PP_IS_BEGIN_PARENS_CONCAT_IMPL(arg0, __VA_ARGS__)
#define PP_IS_BEGIN_PARENS_CONCAT_IMPL(arg0, ...) arg0 ## __VA_ARGS__

#define PP_IS_BEGIN_PARENS_PRE_1 1,
#define PP_IS_BEGIN_PARENS_PRE_PP_IS_BEGIN_PARENS_EAT 0,
#define PP_IS_BEGIN_PARENS_EAT(...) 1

PP_IS_BEGIN_PARENS(())              // -> 1
PP_IS_BEGIN_PARENS((()))            // -> 1
PP_IS_BEGIN_PARENS(a, b, c)         // -> 0
PP_IS_BEGIN_PARENS(a, ())           // -> 0
PP_IS_BEGIN_PARENS(a())             // -> 0
PP_IS_BEGIN_PARENS(()aa(bb()cc))    // -> 1
PP_IS_BEGIN_PARENS(aa(bb()cc))      // -> 0
```

`PP_IS_BEGIN_PARENS` يمكن استخدامها لتحديد ما إذا كانت المعلمات المدخلة تبدأ بأقواس، وعندما يكون من الضروري معالجة معلمات الأقواس سيتم استخدامها (مثلما هو مذكور لاحقاً في تنفيذ `__VA_OPT__`). يبدو الأمر معقداً قليلاً، لكن الفكرة الأساسية هي بناء ماكرو، إذا كانت المعلمات المتغيرة الطول تبدأ بأقواس، فيمكن دمجها مع الأقواس للحصول على نتيجة معينة، وإلا فستتم معالجتها بطريقة أخرى للحصول على نتيجة مختلفة. دعنا نتابع ببطء:

الوظيفة الماكروية المكونة من `PP_IS_BEGIN_PARENS_PROCESS` و`PP_IS_BEGIN_PARENS_PROCESS_0` هي أولاً تقييم المعلمات غير المحددة التي تم تمريرها، ثم اختيار المعلمة رقم 0.

`PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__)` تبدأ بتقييم `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` أولاً، ثم تقوم بدمج نتيجة التقييم مع `PP_IS_BEGIN_PARENS_PRE_`.

`PP_IS_BEGIN_PARENS_EAT(...)` ماكرو سيبتلع جميع المعاملات ويعيد القيمة 1، إذا كانت `__VA_ARGS__` في الخطوة السابقة `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` تبدأ بفتح قوس، فإنه سيتم تطابقها مع تقييم `PP_IS_BEGIN_PARENS_EAT(...)` ثم يعيد القيمة `1`؛ على النقيض، إذا لم تبدأ بفتح قوس، فلن يحدث تطابق، وستبقى `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` بلا تغيير.

إذا تمَ تقييم `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` للحصول على القيمة `1`، فإن `PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, 1) -> PP_IS_BEGIN_PARENS_PRE_1 -> 1`، يُرجى الملاحظة أن هناك فاصلة بعد الرقم `1`، قُم بتمرير `1, ` إلى `PP_IS_BEGIN_PARENS_PROCESS_0`، استرجع الوسيطة رقم 0، وفي النهاية ستحصل على `1`، مما يُظهر أن المعامل يبدأ بفتح القوس.

إذا كانت `PP_IS_BEGIN_PARENS_EAT __VA_ARGS__` لا تعطي القيمة `1`، بل تبقى كما هي، فإن `PP_IS_BEGIN_PARENS_CONCAT(PP_IS_BEGIN_PARENS_PRE_, PP_IS_BEGIN_PARENS_EAT __VA_ARGS__) -> PP_IS_BEGIN_PARENS_PRE_PP_IS_BEGIN_PARENS_EAT __VA_ARGS__ -> 0, __VA_ARGS__`، وعند تمريرها إلى `PP_IS_BEGIN_PARENS_PROCESS_0` نتحصل على `0`، مما يدل على أن المعاملات لا تبدأ بأقواس.

####باراميتر فارغ

判断变长参数是否为空也是一个常用的宏，在实现 `__VA_OPT__` 的时候需要用到，我们在这里利用 `PP_IS_BEGIN_PARENS`，可以先写出不完整的版本：

تحديد ما إذا كانت المعاملات ذات الطول المتغير فارغة هو أيضًا ماكرو شائع الاستخدام، ويحتاج إلى استخدامه عند تنفيذ `__VA_OPT__`. هنا نستفيد من `PP_IS_BEGIN_PARENS`، ويمكننا أولاً كتابة نسخة غير مكتملة:

``` cpp
#define PP_IS_EMPTY_PROCESS(...) \
    PP_IS_BEGIN_PARENS(PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ())
#define PP_IS_EMPTY_PROCESS_EAT(...) ()

PP_IS_EMPTY_PROCESS()       // -> 1
PP_IS_EMPTY_PROCESS(1)      // -> 0
PP_IS_EMPTY_PROCESS(1, 2)   // -> 0
PP_IS_EMPTY_PROCESS(())     // -> 1
```

`PP_IS_EMPTY_PROCESS` هو وظيفة تتحقق مما إذا كان `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ()` يبدأ بالأقواس.

إذا كان `__VA_ARGS__` فارغًا، فإنه عند تمرير `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ () -> PP_IS_EMPTY_PROCESS_EAT() -> ()`، سيتم الحصول على زوج من الأقواس `()`، وعند تمرير ذلك إلى `PP_IS_BEGIN_PARENS` ستعود قيمة `1`، مما يعني أن المعامل فارغ.

إلا إن ذلك، يتم تمرير `PP_IS_EMPTY_PROCESS_EAT __VA_ARGS__ ()` بشكل ثابت إلى `PP_IS_BEGIN_PARENS`، مما يعيد القيمة 0 للإشارة إلى عدم الفراغ.

خذ عين الاعتبار النموذج الرابع `PP_IS_EMPTY_PROCESS(()) ->1`، لا يمكن لـ `PP_IS_EMPTY_PROCESS` أن يعالج بشكل صحيح الوسائط المتغيرة التي تبدأ بقوسين، لأن قوسين الوسائط المتغيرة في هذه الحالة ستتطابق مع `PP_IS_EMPTY_PROCESS_EAT` وتؤدي إلى الحصول على `()` كقيمة. لحل هذه المشكلة، نحن بحاجة إلى التعامل بشكل مختلف مع حالة بداية الوسيطة بقوسين أم لا:

``` cpp
#define PP_IS_EMPTY(...) \
    PP_IS_EMPTY_IF(PP_IS_BEGIN_PARENS(__VA_ARGS__)) \
        (PP_IS_EMPTY_ZERO, PP_IS_EMPTY_PROCESS)(__VA_ARGS__)

#define PP_IS_EMPTY_IF(if) PP_CONCAT(PP_IS_EMPTY_IF_, if)
#define PP_IS_EMPTY_IF_1(then, else) then
#define PP_IS_EMPTY_IF_0(then, else) else

#define PP_IS_EMPTY_ZERO(...) 0

PP_IS_EMPTY()       // -> 1
PP_IS_EMPTY(1)      // -> 0
PP_IS_EMPTY(1, 2)   // -> 0
PP_IS_EMPTY(())     // -> 0
```

`PP_IS_EMPTY_IF` استنادًا إلى شرط `if` لإرجاع المعلمات 0 أو 1.

إذا برزت المعلمة المتغيرة ذات الطول المتغير بأقواس، فإن `PP_IS_EMPTY_IF` سيُرجع `PP_IS_EMPTY_ZERO`، ثم يُرجع `0` في النهاية، ليدل على أن المعلمة ذات الطول المتغير ليست فارغة.

على العكس من ذلك، فإن `PP_IS_EMPTY_IF` تعيد `PP_IS_EMPTY_PROCESS`، والتي يتم من خلالها أخيراً判断 ما إذا كانت المعاملات المتغيرة الطول غير فارغة.

####访问 تحت

احصل على عنصر محدد في قائمة الوسائط المتغيرة:

``` cpp
#define PP_ARGS_ELEM(I, ...) PP_CONCAT(PP_ARGS_ELEM_, I)(__VA_ARGS__)
#define PP_ARGS_ELEM_0(a0, ...) a0
#define PP_ARGS_ELEM_1(a0, a1, ...) a1
#define PP_ARGS_ELEM_2(a0, a1, a2, ...) a2
#define PP_ARGS_ELEM_3(a0, a1, a2, a3, ...) a3
// ...
#define PP_ARGS_ELEM_7(a0, a1, a2, a3, a4, a5, a6, a7, ...) a7
#define PP_ARGS_ELEM_8(a0, a1, a2, a3, a4, a5, a6, a7, a8, ...) a8

PP_ARGS_ELEM(0, "Hello", "World")   // -> PP_ARGS_ELEM_0("Hello", "World") -> "Hello"
PP_ARGS_ELEM(1, "Hello", "World")   // -> PP_ARGS_ELEM_1("Hello", "World") -> "World"
```

المعامل الأول لـ `PP_ARGS_ELEM` هو فهرس العنصر `I`، تليه عدة متغيرة. بالاستفادة من `PP_CONCAT`، يمكن دمج `PP_ARGS_ELEM_` و `I` معاً، لذا يمكن الحصول على الماكرو الذي يعيد العنصر الموجود في الموضع المحدد `PP_ARGS_ELEM_0..8`، بعد ذلك، يتم تمرير الأجزاء المتغيرة إلى هذا الماكرو، ويتم فحص العنصر الموجود في الموضع المطلوب.

#### PP_IS_EMPTY2

يمكنك أيضًا تحقيق إصدار آخر من `PP_IS_EMPTY` باستخدام `PP_ARGS_ELEM` 

``` cpp
#define PP_IS_EMPTY2(...) \
    PP_AND( \
        PP_AND( \
            PP_NOT(PP_HAS_COMMA(__VA_ARGS__)), \
            PP_NOT(PP_HAS_COMMA(__VA_ARGS__())) \
        ), \
        PP_AND( \
            PP_NOT(PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__)), \
            PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ()) \
        ) \
    )

#define PP_HAS_COMMA(...) PP_ARGS_ELEM(8, __VA_ARGS__, 1, 1, 1, 1, 1, 1, 1, 0)
#define PP_COMMA_ARGS(...) ,

PP_IS_EMPTY2()              // -> 1
PP_IS_EMPTY2(a)             // -> 0
PP_IS_EMPTY2(a, b)          // -> 0
PP_IS_EMPTY2(())            // -> 0
PP_IS_EMPTY2(PP_COMMA)      // -> 0
```

借用 `PP_ARGS_ELEM` 实现判断参数是否含有逗号 `PP_HAS_COMMA`。`PP_COMMA_ARGS` 会吞掉传入的任意参数，返回一个逗号。

المنطق الأساسي للتحقق مما إذا كانت معلمة الطول المتغيرة فارغة هو استرجاع فاصلة عند استدعاء `PP_COMMA_ARGS __VA_ARGS__ ()`، أي إذا كانت `__VA_ARGS__` فارغة، سيتم دمج `PP_COMMA_ARGS` و `()` معًا للتحقق منها، الطريقة الدقيقة لتحقق من ذلك هي `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ())`.

لكن قد تكون هناك حالات استثنائية:

`__VA_ARGS__` يمكن أن يحتوي بحد ذاته على فاصلة؛
`__VA_ARGS__()` يتم دمجها معًا لتسبب تقديم قيمة مع فاصلة.
`PP_COMMA_ARGS __VA_ARGS__` يتم دمجها معًا مما يؤدي إلى تقديم التقويم مع الفاصلة؛

بالنسبة للحالات الثلاث الاستثنائية المذكورة أعلاه، يجب استبعادها، لذا فإن الطريقة النهائية تعادل تنفيذ المنطق "و" على الشروط الأربعة التالية:

* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__))` &&
* `PP_NOT(PP_HAS_COMMA(__VA_ARGS__()))` &&
* `PP_NOT(PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__))` &&
* `PP_HAS_COMMA(PP_COMMA_ARGS __VA_ARGS__ ())`

#### `__VA_OPT__`

استخدام `PP_IS_EMPTY` يمكن أخيرًا تحقيق ما يشبه ماكرو `__VA_OPT__` باللغة العربية.

``` cpp
#define PP_REMOVE_PARENS(tuple) PP_REMOVE_PARENS_IMPL tuple
#define PP_REMOVE_PARENS_IMPL(...) __VA_ARGS__

#define PP_ARGS_OPT(data_tuple, empty_tuple, ...) \
    PP_ARGS_OPT_IMPL(PP_IF(PP_IS_EMPTY(__VA_ARGS__), empty_tuple, data_tuple))
#define PP_ARGS_OPT_IMPL(tuple) PP_REMOVE_PARENS(tuple)

PP_ARGS_OPT((data), (empty))        // -> empty
PP_ARGS_OPT((data), (empty), 1)     // -> data
PP_ARGS_OPT((,), (), 1)             // -> ,
```

يقبل `PP_ARGS_OPT` معلماتٍ ثابتتين ومعلماتٍ غير ثابتة، وعندما تكون المعلمات غير الثابتة غير فارغة، يتم إرجاع `data`؛ وإلا يتم إرجاع `empty`. لجعل `data` و `empty` يدعمان الفواصل، يُطلب أن يُحيط كل منهما بأقواس لتضمين المعطيات الفعلية، ثم يتم استخدام `PP_REMOVE_PARENS` لإزالة الأقواس الخارجية في النهاية.

باستخدام `PP_ARGS_OPT` يمكن تحقيق وظائف `LOG2` بواسطة `LOG3` بشكل واقعي.

``` cpp
#define LOG3(format, ...) \
    printf("log: " format PP_ARGS_OPT((,), (), __VA_ARGS__) __VA_ARGS__)

LOG3("Hello");                  // -> printf("log: " "Hello" );
LOG3("Hello %s", "World");      // -> printf("log: " "Hello %s" , "World");
```

`data_tuple` هو `(,)`، وإذا كانت متغيرات الطول غير فارغة، فسيتم إرجاع جميع العناصر الموجودة في `data_tuple`، وهنا هو الفاصلة `,`.

####الرجاء تحديد عدد المعلمات

الحصول على عدد المعاملات المتغيرة الطول:

``` cpp
#define PP_ARGS_SIZE_IMCOMPLETE(...) \
    PP_ARGS_ELEM(8, __VA_ARGS__, 8, 7, 6, 5, 4, 3, 2, 1, 0)

PP_ARGS_SIZE_IMCOMPLETE(a)             // -> 1
PP_ARGS_SIZE_IMCOMPLETE(a, b)          // -> 2
PP_ARGS_SIZE_IMCOMPLETE(PP_COMMA())    // -> 2
PP_ARGS_SIZE_IMCOMPLETE()              // -> 1
```

حساب عدد معلمات الطول المتغير يتم من خلال موقع المعلمات. `__VA_ARGS__` سيؤدي إلى تحريك جميع المعلمات اللاحقة إلى اليمين، ويتم استخدام الماكرو `PP_ARGS_ELEM` للحصول على المعلمة في الموضع الثامن، فإذا كان `__VA_ARGS__` يحتوي على معلمة واحدة فقط، فإن المعلمة الثامنة تساوي `1`؛ وبالمثل، إذا كانت هناك معلمان في `__VA_ARGS__`، فإن المعلمة الثامنة تصبح `2`، مما يتوافق بالضبط مع عدد معلمات الطول المتغير.

الأمثلة المقدمة هنا تدعم فقط عددًا متغيرًا يصل إلى 8، وهذا يعتمد على الحد الأقصى للطول الذي يمكن دعمه بواسطة `PP_ARGS_ELEM`.

ولكن هذا الماكرو لا يزال غير مكتمل، ففي حالة كون المعاملات المتغيرة الطول فارغة، سيقوم هذا الماكرو بإرجاع `1` بشكل خاطئ. إذا كان من الضروري معالجة المعاملات المتغيرة الطول الفارغة، فسنحتاج إلى استخدام الماكرو الذي ذكرناه سابقًا `PP_ARGS_OPT`:

``` cpp
#define PP_COMMA_IF_ARGS(...) PP_ARGS_OPT((,), (), __VA_ARGS__)
#define PP_ARGS_SIZE(...) PP_ARGS_ELEM(8, __VA_ARGS__ PP_COMMA_IF_ARGS(__VA_ARGS__) 8, 7, 6, 5, 4, 3, 2, 1, 0, 0, 0)

PP_ARGS_SIZE(a)             // -> 1
PP_ARGS_SIZE(a, b)          // -> 2
PP_ARGS_SIZE(PP_COMMA())    // -> 2
PP_ARGS_SIZE()              // -> 0
PP_ARGS_SIZE(,,,)           // -> 4
```

مفتاح المشكلة هو الفاصلة `,`، فعندما تكون `__VA_ARGS__` فارغة، يمكن إخفاء الفاصلة للحصول على نتيجة صحيحة وهي `0`.

####التصفح访问

نحو for_each في C++، يمكننا تحقيق PP_FOR_EACH كما تعاونية ماكرو:

``` cpp
#define PP_FOR_EACH(macro, contex, ...) \
    PP_CONCAT(PP_FOR_EACH_, PP_ARGS_SIZE(__VA_ARGS__))(0, macro, contex, __VA_ARGS__)

#define PP_FOR_EACH_0(index, macro, contex, ...)
#define PP_FOR_EACH_1(index, macro, contex, arg, ...) macro(index, contex, arg)

#define PP_FOR_EACH_2(index, macro, contex, arg, ...) \
    macro(index, contex, arg) \
    PP_FOR_EACH_1(PP_INC(index), macro, contex, __VA_ARGS__)

#define PP_FOR_EACH_3(index, macro, contex, arg, ...) \
    macro(index, contex, arg) \
    PP_FOR_EACH_2(PP_INC(index), macro, contex, __VA_ARGS__)
// ...
#define PP_FOR_EACH_8(index, macro, contex, arg, ...) \
    macro(index, contex, arg) \
    PP_FOR_EACH_7(PP_INC(index), macro, contex, __VA_ARGS__)

#define DECLARE_EACH(index, contex, arg)    PP_IF(index, PP_COMMA, PP_EMPTY)() contex arg

PP_FOR_EACH(DECLARE_EACH, int, x, y, z);    // -> int x, y, z;
PP_FOR_EACH(DECLARE_EACH, bool, a, b);      // -> bool a, b;
```

`PP_FOR_EACH` يستقبل اثنين من المعطيات الثابتة: `macro` يمكن فهمه على أنه الماكرو الذي يتم استدعاؤه أثناء التكرار، و `contex` يمكن اعتباره قيمة ثابتة تُمرر إلى `macro`. `PP_FOR_EACH` أولاً يستخدم `PP_ARGS_SIZE` للحصول على طول المعطيات المتغيرة `N`، ثم يستخدم `PP_CONCAT` لدمجها للحصول على `PP_FOR_EACH_N`، بعد ذلك سيقوم `PP_FOR_EACH_N` باستدعاء `PP_FOR_EACH_N-1` بشكل متكرر لتحقيق عدد التكرارات المتساوي مع عدد المعطيات المتغيرة.

في هذا المثال، قمنا بتعريف `DECLARE_EACH` كمعلمة للـ `macro`، ودور `DECLARE_EACH` هو إعادة `contex arg`، وإذا كانت `contex` اسم نوع البيانات، و`arg` اسم المتغير، فإن `DECLARE_EACH` يمكن استخدامه لتعريف المتغيرات.

####حلقة شرطية

بعد وجود `FOR_EACH`، يمكننا أيضًا استخدام صيغة مشابهة لكتابة `PP_WHILE`:

``` cpp
#define PP_WHILE PP_WHILE_1

#define PP_WHILE_1(pred, op, val) PP_WHILE_1_IMPL(PP_BOOL(pred(val)), pred, op, val)
#define PP_WHILE_1_IMPL(cond, pred, op, val) \
    PP_IF(cond, PP_WHILE_2, val PP_EMPTY_EAT)(pred, op, PP_IF(cond, op, PP_EMPTY_EAT)(val))

#define PP_WHILE_2(pred, op, val) PP_WHILE_2_IMPL(PP_BOOL(pred(val)), pred, op, val)
#define PP_WHILE_2_IMPL(cond, pred, op, val) \
    PP_IF(cond, PP_WHILE_3, val PP_EMPTY_EAT)(pred, op, PP_IF(cond, op, PP_EMPTY_EAT)(val))

#define PP_WHILE_3(pred, op, val) PP_WHILE_3_IMPL(PP_BOOL(pred(val)), pred, op, val)
#define PP_WHILE_3_IMPL(cond, pred, op, val) \
    PP_IF(cond, PP_WHILE_4, val PP_EMPTY_EAT)(pred, op, PP_IF(cond, op, PP_EMPTY_EAT)(val))

#define PP_WHILE_4(pred, op, val) PP_WHILE_4_IMPL(PP_BOOL(pred(val)), pred, op, val)
#define PP_WHILE_4_IMPL(cond, pred, op, val) \
    PP_IF(cond, PP_WHILE_5, val PP_EMPTY_EAT)(pred, op, PP_IF(cond, op, PP_EMPTY_EAT)(val))
// ...

#define PP_WHILE_8(pred, op, val) PP_WHILE_8_IMPL(PP_BOOL(pred(val)), pred, op, val)
#define PP_WHILE_8_IMPL(cond, pred, op, val) \
    PP_IF(cond, PP_WHILE_8, val PP_EMPTY_EAT)(pred, op, PP_IF(cond, op, PP_EMPTY_EAT)(val))

#define PP_EMPTY_EAT(...)

#define SUM_OP(xy_tuple) SUM_OP_OP_IMPL xy_tuple
#define SUM_OP_OP_IMPL(x, y) (PP_DEC(x), y + x)

#define SUM_PRED(xy_tuple) SUM_PRED_IMPL xy_tuple
#define SUM_PRED_IMPL(x, y) x

#define SUM(max_num, origin_num) \
    PP_IDENTITY(SUM_IMPL PP_WHILE(SUM_PRED, SUM_OP, (max_num, origin_num)))
#define SUM_IMPL(ignore, ret) ret

PP_WHILE(SUM_PRED, SUM_OP, (2, a))      // -> (0, a + 2 + 1)
SUM(2, a)                               // -> a + 2 + 1
```

`PP_WHILE` تقبل ثلاثة معايير: `pred` دالة شرطية، `op` دالة عملية، `val` قيمة ابتدائية؛ خلال التكرار، يتم استخدام `pred(val)` لإجراء تحقق من إنهاء الحلقة، ويتم تمرير القيمة الناتجة من `op(val)` إلى الماكرو التالي، ويمكن فهم ذلك على أنه تنفيذ الكود التالي:

``` cpp
while (pred(val)) {
    val = op(val);
}
```

`PP_WHILE_N` أولاً استخدم `pred(val)` للحصول على نتيجة شرطية، ثم قم بتمرير نتيجة الشرط `cond` والمعاملات الأخرى إلى `PP_WHILE_N_IMPL`.
`PP_WHILE_N_IMPL` يمكن تقسيمها إلى جزئين: الجزء الخلفي `(pred, op, PP_IF(cond, op, PP_EMPTY_EAT)(val))` هو الذي يُمرر كمعلمة للجزء الأمامي، `PP_IF(cond, op, PP_EMPTY_EAT)(val)` هو في حال كان `cond` صحيحًا، فسيتم تقييم `op(val)`، وإلا سيتم الحصول على النتيجة كـ `PP_EMPTY_EAT(val)`، الجزء الأمامي `PP_IF(cond, PP_WHILE_N+1, val PP_EMPTY_EAT)`، إذا كان `cond` صحيحًا، سيُرجع `PP_WHILE_N+1`، وسيستمر في تنفيذ الحلقة من خلال مرور الجزء الخلفي، وإلا سيُرجع `val PP_EMPTY_EAT`، وهنا `val` هو النتيجة النهائية، و`PP_EMPTY_EAT` سيعمل على استيعاب نتيجة الجزء الخلفي.

'`SUM`' تنفذ '`N + N-1 + ... + 1`'. القيم الابتدائية هي `(max_num، origin_num)`؛ '`SUM_PRED`' تأخذ القيمة الأولى `x` وتتحقق مما إذا كانت أكبر من 0؛ '`SUM_OP`' يقوم بتنفيذ عملية الانخفاض على `x` `x = x - 1`، ويقوم بإجراء عملية الجمع `+ x` على `y` `y = y + x`. انتقل مباشرة بـ '`SUM_PRED`' و '`SUM_OP`' إلى `PP_WHILE`، النتيجة المُعادة هي tuple، الناتج الفعلي الذي نريده هو العنصر الثاني في tuple، لذا نستخدم '`SUM`' مرة أخرى للحصول على قيمة العنصر الثاني.

####التكرار المتداخل

حتى الآن، تمت العمليات الدورية والحلقات الشرطية بنجاح، وكانت النتائج تتفق مع التوقعات. هل تتذكرنا بمنع إعادة التداخل عند مناقشة قواعد توسيع الماكرو؟ للأسف، واجهنا حظر إعادة التداخل عندما حاولنا تنفيذ حلقة دوران مزدوجة.

``` cpp
#define SUM_OP2(xy_tuple) SUM_OP_OP_IMPL2 xy_tuple
#define SUM_OP_OP_IMPL2(x, y) (PP_DEC(x), y + SUM(x, 0))

#define SUM2(max_num, origin_num) \
    PP_IDENTITY(SUM_IMPL PP_WHILE(SUM_PRED, SUM_OP2, (max_num, origin_num)))

SUM2(1, a)      // -> a + SUM_IMPL PP_WHILE_1(SUM_PRED, SUM_OP, (1, a))
```

`SUM2` تغيير معامل `op` إلى `SUM_OP2`، حيث يتم استدعاء `SUM` داخل `SUM_OP2`، و`SUM` سوف يتوسع ليكون `PP_WHILE_1`، مما يعني أن `PP_WHILE_1` يتم استدعاؤه بشكل تكراري لنفسه، ويتوقف المعالج المسبق عن التوسع.

لحل هذه المشكلة، يمكننا استخدام طريقة الاستنتاج التلقائي التكرارية (Automatic Recursion):

``` cpp
#define PP_AUTO_WHILE PP_CONCAT(PP_WHILE_, PP_AUTO_REC(PP_WHILE_PRED))

#define PP_AUTO_REC(check) PP_IF(check(2), PP_AUTO_REC_12, PP_AUTO_REC_34)(check)
#define PP_AUTO_REC_12(check) PP_IF(check(1), 1, 2)
#define PP_AUTO_REC_34(check) PP_IF(check(3), 3, 4)

#define PP_WHILE_PRED(n) \
    PP_CONCAT(PP_WHILE_CHECK_, PP_WHILE_ ## n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE))
#define PP_WHILE_FALSE(...) 0

#define PP_WHILE_CHECK_PP_WHILE_FALSE 1

#define PP_WHILE_CHECK_PP_WHILE_1(...) 0
#define PP_WHILE_CHECK_PP_WHILE_2(...) 0
#define PP_WHILE_CHECK_PP_WHILE_3(...) 0
#define PP_WHILE_CHECK_PP_WHILE_4(...) 0
// ...
#define PP_WHILE_CHECK_PP_WHILE_8(...) 0

PP_AUTO_WHILE       // -> PP_WHILE_1

#define SUM3(max_num, origin_num) \
    PP_IDENTITY(SUM_IMPL PP_AUTO_WHILE(SUM_PRED, SUM_OP, (max_num, origin_num)))

#define SUM_OP4(xy_tuple) SUM_OP_OP_IMPL4 xy_tuple
#define SUM_OP_OP_IMPL4(x, y) (PP_DEC(x), y + SUM3(x, 0))

#define SUM4(max_num, origin_num) \
    PP_IDENTITY(SUM_IMPL PP_AUTO_WHILE(SUM_PRED, SUM_OP4, (max_num, origin_num)))

SUM4(2, a)          // -> a + 0 + 2 + 1 + 0 + 1
```

`PP_AUTO_WHILE` هو النسخة التلقائية المستندة إلى الاستدعاء الذاتي لـ `PP_WHILE`، وماكرو الأساسي هو `PP_AUTO_REC(PP_WHILE_PRED)`، هذا الماكرو يمكنه العثور على الرقم `N` للنسخة المتاحة حاليًا من `PP_WHILE_N`.

المبدأ المستخرج بسيط للغاية، وهو البحث عن جميع الإصدارات، واكتشاف الإصدارات القابلة للتوسيع بشكل صحيح، وإرجاع رقم تلك الإصدارة. لتعزيز سرعة البحث، من الممارسات الشائعة استخدام البحث الثنائي، وهذا ما يقوم به `PP_AUTO_REC`. يقبل `PP_AUTO_REC` معلمة `check`، التي تُعنى بالتحقق من صلاحية الإصدارات. هنا، يتم تقديم نطاق الإصدارات القابلة للبحث وهو `[1, 4]`. سيتحقق `PP_AUTO_REC` أولاً من `check(2)`، وإذا كانت `check(2)` صحيحة، فسيستدعي `PP_AUTO_REC_12` للبحث في النطاق `[1, 2]`، وإلا سيستخدم `PP_AUTO_REC_34` للبحث في `[3, 4]`. يتحقق `PP_AUTO_REC_12` من `check(1)`، وإذا كانت صحيحة، فهذا يعني أن الإصدارة `1` متاحة، وإلا يتم استخدام الإصدارة `2`، وبالمثل بالنسبة لـ `PP_AUTO_REC_34`.

كيف يمكننا كتابة ماكرو `check` لمعرفة ما إذا كانت النسخة متاحة أم لا؟ هنا، سيتم توسيع `PP_WHILE_PRED` إلى جزئين متصلين، دعونا نلقي نظرة على الجزء الأخير `PP_WHILE_ ## n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`: إذا كان `PP_WHILE_ ## n` متاحًا، وبما أن `PP_WHILE_FALSE` يعود دائمًا بـ `0`، فإن هذه الجزء سيتم توسيعه ليحصل على قيمة معلمة `val`، وهي `PP_WHILE_FALSE`؛ أما إذا لم يكن هذا الجزء من الماكرو متاحًا، فسوف يبقى كما هو، أي `PP_WHILE_n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`.

قم بدمج نتائج الجزء الخلفي مع الجزء الأمامي `PP_WHILE_CHECK_` لتحصل على نتيجتين: `PP_WHILE_CHECK_PP_WHILE_FALSE` أو `PP_WHILE_CHECK_PP_WHILE_n(PP_WHILE_FALSE, PP_WHILE_FALSE, PP_WHILE_FALSE)`، وبذلك نجعل `PP_WHILE_CHECK_PP_WHILE_FALSE` يُعيد `1` للدلالة على التوافر، و`PP_WHILE_CHECK_PP_WHILE_n` يُعيد `0` للدلالة على عدم التوفر. بهذا نكون قد أتممنا وظيفة التوصل التلقائي للتكرار.

####المقارنة الحسابية

غير متساوي:

``` cpp
#define PP_NOT_EQUAL(x, y) PP_NOT_EQUAL_IMPL(x, y)
#define PP_NOT_EQUAL_IMPL(x, y) \
    PP_CONCAT(PP_NOT_EQUAL_CHECK_, PP_NOT_EQUAL_ ## x(0, PP_NOT_EQUAL_ ## y))

#define PP_NOT_EQUAL_CHECK_PP_EQUAL_NIL 1
#define PP_NOT_EQUAL_CHECK_PP_NOT_EQUAL_0(...) 0
#define PP_NOT_EQUAL_CHECK_PP_NOT_EQUAL_1(...) 0
#define PP_NOT_EQUAL_CHECK_PP_NOT_EQUAL_2(...) 0
#define PP_NOT_EQUAL_CHECK_PP_NOT_EQUAL_3(...) 0
#define PP_NOT_EQUAL_CHECK_PP_NOT_EQUAL_4(...) 0
// ...
#define PP_NOT_EQUAL_CHECK_PP_NOT_EQUAL_8(...) 0

#define PP_NOT_EQUAL_0(cond, y) PP_IF(cond, PP_EQUAL_NIL, y(1, PP_EQUAL_NIL))
#define PP_NOT_EQUAL_1(cond, y) PP_IF(cond, PP_EQUAL_NIL, y(1, PP_EQUAL_NIL))
#define PP_NOT_EQUAL_2(cond, y) PP_IF(cond, PP_EQUAL_NIL, y(1, PP_EQUAL_NIL))
#define PP_NOT_EQUAL_3(cond, y) PP_IF(cond, PP_EQUAL_NIL, y(1, PP_EQUAL_NIL))
#define PP_NOT_EQUAL_4(cond, y) PP_IF(cond, PP_EQUAL_NIL, y(1, PP_EQUAL_NIL))
// ...
#define PP_NOT_EQUAL_8(cond, y) PP_IF(cond, PP_EQUAL_NIL, y(1, PP_EQUAL_NIL))

PP_NOT_EQUAL(1, 1)          // -> 0
PP_NOT_EQUAL(3, 1)          // -> 1
```

تحديد ما إذا كانت القيم متساوية، استخدم خاصية منع إعادة الدخول التكرارية، حيث يتم ربط `x` و `y` بشكل تكراري لتكوين ماكرو `PP_NOT_EQUAL_x PP_NOT_EQUAL_y`، إذا كانت `x == y`، فلن يتم توسيع ماكرو `PP_NOT_EQUAL_y`، ليصبح مع `PP_NOT_EQUAL_CHECK_` متصلاً على أنه `PP_NOT_EQUAL_CHECK_PP_NOT_EQUAL_y` ويعيد `0`؛ أما العكس، فعند التوسيع مرتين بنجاح نحصل في النهاية على `PP_EQUAL_NIL`، وعند الربط نحصل على `PP_NOT_EQUAL_CHECK_PP_EQUAL_NIL` ويعيد `1`.

الترجمة إلى اللغة العربية:

متساوٍ:

``` cpp
#define PP_EQUAL(x, y) PP_NOT(PP_NOT_EQUAL(x, y))

PP_EQUAL(1, 1)              // -> 1
PP_EQUAL(1, 3)              // -> 0

```

أقل من أو يساوي:

``` cpp
#define PP_LESS_EQUAL(x, y) PP_NOT(PP_SUB(x, y))

PP_LESS_EQUAL(2, 1)         // -> 0
PP_LESS_EQUAL(1, 1)         // -> 1
PP_LESS_EQUAL(1, 2)         // -> 1
```

أقل من:

``` cpp
#define PP_LESS(x, y) PP_AND(PP_LESS_EQUAL(x, y), PP_NOT_EQUAL(x, y))

PP_LESS(2, 1)               // -> 0
PP_LESS(1, 2)               // -> 1
PP_LESS(2, 2)               // -> 0
```

بالإضافة إلى ذلك، هناك عمليات حسابية أخرى مثل "أكبر من" و"أكبر من أو يساوي" وغيرها، ولن نعود لذكرها هنا.

####العمليات الحسابية

باستخدام `PP_AUTO_WHILE` يمكننا تنفيذ العمليات الرياضية الأساسية، كما أنها تدعم العمليات المتداخلة.

الجمع:

``` cpp
#define PP_ADD(x, y) \
    PP_IDENTITY(PP_ADD_IMPL PP_AUTO_WHILE(PP_ADD_PRED, PP_ADD_OP, (x, y)))
#define PP_ADD_IMPL(x, y) x

#define PP_ADD_PRED(xy_tuple) PP_ADD_PRED_IMPL xy_tuple
#define PP_ADD_PRED_IMPL(x, y) y

#define PP_ADD_OP(xy_tuple) PP_ADD_OP_IMPL xy_tuple
#define PP_ADD_OP_IMPL(x, y) (PP_INC(x), PP_DEC(y))

PP_ADD(1, 2)                  // -> 3
PP_ADD(1, PP_ADD(1, 2))       // -> 4
```

طرح:

``` cpp
#define PP_SUB(x, y) \
    PP_IDENTITY(PP_SUB_IMPL PP_AUTO_WHILE(PP_SUB_PRED, PP_SUB_OP, (x, y)))
#define PP_SUB_IMPL(x, y) x

#define PP_SUB_PRED(xy_tuple) PP_SUB_PRED_IMPL xy_tuple
#define PP_SUB_PRED_IMPL(x, y) y

#define PP_SUB_OP(xy_tuple) PP_SUB_OP_IMPL xy_tuple
#define PP_SUB_OP_IMPL(x, y) (PP_DEC(x), PP_DEC(y))

PP_SUB(2, 1)                // -> 1
PP_SUB(3, PP_ADD(2, 1))     // -> 0
```

ضرب:

``` cpp
#define PP_MUL(x, y) \
    IDENTITY(PP_MUL_IMPL PP_AUTO_WHILE(PP_MUL_PRED, PP_MUL_OP, (0, x, y)))
#define PP_MUL_IMPL(ret, x, y) ret

#define PP_MUL_PRED(rxy_tuple) PP_MUL_PRED_IMPL rxy_tuple
#define PP_MUL_PRED_IMPL(ret, x, y) y

#define PP_MUL_OP(rxy_tuple) PP_MUL_OP_IMPL rxy_tuple
#define PP_MUL_OP_IMPL(ret, x, y) (PP_ADD(ret, x), x, PP_DEC(y))

PP_MUL(1, 1)                // -> 1
PP_MUL(2, PP_ADD(0, 1))     // -> 2
```

تم إضافة معامل جديد `ret` إلى تنفيذ الضرب هنا، حيث تكون القيمة الأولية `0`، وفي كل تكرار يتم تنفيذ `ret = ret + x`.

القسمة:

``` cpp
#define PP_DIV(x, y) \
    IDENTITY(PP_DIV_IMPL PP_AUTO_WHILE(PP_DIV_PRED, PP_DIV_OP, (0, x, y)))
#define PP_DIV_IMPL(ret, x, y) ret

#define PP_DIV_PRED(rxy_tuple) PP_DIV_PRED_IMPL rxy_tuple
#define PP_DIV_PRED_IMPL(ret, x, y) PP_LESS_EQUAL(y, x)

#define PP_DIV_OP(rxy_tuple) PP_DIV_OP_IMPL rxy_tuple
#define PP_DIV_OP_IMPL(ret, x, y) (PP_INC(ret), PP_SUB(x, y), y)

PP_DIV(1, 2)                // -> 0
PP_DIV(2, 1)                // -> 2
PP_DIV(2, PP_ADD(1, 1))     // -> 1
```

يستخدم القسمة `PP_LESS_EQUAL` ، ويستمر الحلقة فقط في حالة `y <= x`.

####هيكل البيانات

يمكن أيضًا لـ `宏` أن يحتوي على هيكل بيانات. في الواقع ، قمنا بتطبيق نوع من هيكل البيانات `tuple` قليلاً في الأمام ،`PP_REMOVE_PARENS` يمكن أن يقوم بإزالة القوسين الخارجيين لـ `tuple` ، وإرجاع العناصر الداخلية. سنستخدم `tuple` هنا كمثال لمناقشة التنفيذ ذات الصلة ، ويمكن لمن يهتم بالهياكل البيانية الأخرى مثل `list، array` المراجعة لتنفيذ `Boost`.

`tuple` يُعرَّف بأنه مجموعة من العناصر مفصولة بفواصل ومحيطة بأقواس: `(a, b, c)`。

``` cpp
#define PP_TUPLE_REMOVE_PARENS(tuple) PP_REMOVE_PARENS(tuple)

// الحصول على العنصر الموجود في الفهرس المحدد
#define PP_TUPLE_ELEM(i, tuple) PP_ARGS_ELEM(i, PP_TUPLE_REMOVE_PARENS(tuple))

// التهام كامل tuple وإرجاع فارغ
#define PP_TUPLE_EAT() PP_EMPTY_EAT

// الحصول على الحجم
#define PP_TUPLE_SIZE(tuple) PP_ARGS_SIZE(PP_TUPLE_REMOVE_PARENS(tuple))

// إضافة العناصر
#define PP_TUPLE_PUSH_BACK(elem, tuple) \
    PP_TUPLE_PUSH_BACK_IMPL(PP_TUPLE_SIZE(tuple), elem, tuple)
#define PP_TUPLE_PUSH_BACK_IMPL(size, elem, tuple) \
    (PP_TUPLE_REMOVE_PARENS(tuple) PP_IF(size, PP_COMMA, PP_EMPTY)() elem)

// إدراج عنصر
#define PP_TUPLE_INSERT(i, elem, tuple) \
    PP_TUPLE_ELEM( \
        3, \
        PP_AUTO_WHILE( \
            PP_TUPLE_INSERT_PRED, \
            PP_TUPLE_INSERT_OP, \
            (0, i, elem, (), tuple) \
        ) \
    )
#define PP_TUPLE_INSERT_PRED(args) PP_TUPLE_INSERT_PERD_IMPL args
#define PP_TUPLE_INSERT_PERD_IMPL(curi, i, elem, ret, tuple) \
    PP_NOT_EQUAL(PP_TUPLE_SIZE(ret), PP_INC(PP_TUPLE_SIZE(tuple)))
#define PP_TUPLE_INSERT_OP(args) PP_TUPLE_INSERT_OP_IMPL args
#define PP_TUPLE_INSERT_OP_IMPL(curi, i, elem, ret, tuple) \
    ( \
    PP_IF(PP_NOT_EQUAL(PP_TUPLE_SIZE(ret), i), PP_INC(curi), curi), \
    i, elem, \
    PP_TUPLE_PUSH_BACK(\
        PP_IF( \
            PP_NOT_EQUAL(PP_TUPLE_SIZE(ret), i), \
            PP_TUPLE_ELEM(curi, tuple), elem \
        ), \
        ret \
    ), \
    tuple \
    )

// حذف العنصر الأخير
#define PP_TUPLE_POP_BACK(tuple) \
    PP_TUPLE_ELEM( \
        1, \
        PP_AUTO_WHILE( \
            PP_TUPLE_POP_BACK_PRED, \
            PP_TUPLE_POP_BACK_OP, \
            (0, (), tuple) \
        ) \
    )
#define PP_TUPLE_POP_BACK_PRED(args) PP_TUPLE_POP_BACK_PRED_IMPL args
#define PP_TUPLE_POP_BACK_PRED_IMPL(curi, ret, tuple) \
    PP_IF( \
        PP_TUPLE_SIZE(tuple), \
        PP_NOT_EQUAL(PP_TUPLE_SIZE(ret), PP_DEC(PP_TUPLE_SIZE(tuple))), \
        0 \
    )
#define PP_TUPLE_POP_BACK_OP(args) PP_TUPLE_POP_BACK_OP_IMPL args
#define PP_TUPLE_POP_BACK_OP_IMPL(curi, ret, tuple) \
    (PP_INC(curi), PP_TUPLE_PUSH_BACK(PP_TUPLE_ELEM(curi, tuple), ret), tuple)

// حذف العنصر
#define PP_TUPLE_REMOVE(i, tuple) \
    PP_TUPLE_ELEM( \
        2, \
        PP_AUTO_WHILE( \
            PP_TUPLE_REMOVE_PRED, \
            PP_TUPLE_REMOVE_OP, \
            (0, i, (), tuple) \
        ) \
    )
#define PP_TUPLE_REMOVE_PRED(args) PP_TUPLE_REMOVE_PRED_IMPL args
#define PP_TUPLE_REMOVE_PRED_IMPL(curi, i, ret, tuple) \
    PP_IF( \
        PP_TUPLE_SIZE(tuple), \
        PP_NOT_EQUAL(PP_TUPLE_SIZE(ret), PP_DEC(PP_TUPLE_SIZE(tuple))), \
        0 \
    )
#define PP_TUPLE_REMOVE_OP(args) PP_TUPLE_REMOVE_OP_IMPL args
#define PP_TUPLE_REMOVE_OP_IMPL(curi, i, ret, tuple) \
    ( \
    PP_INC(curi), \
    i, \
    PP_IF( \
        PP_NOT_EQUAL(curi, i), \
        PP_TUPLE_PUSH_BACK(PP_TUPLE_ELEM(curi, tuple), ret), \
        ret \
    ), \
    tuple \
    )

PP_TUPLE_SIZE(())               // -> 0

PP_TUPLE_PUSH_BACK(2, (1))      // -> (1, 2)
PP_TUPLE_PUSH_BACK(2, ())       // -> (2)

PP_TUPLE_INSERT(1, 2, (1, 3))   // -> (1, 2, 3)

PP_TUPLE_POP_BACK(())           // -> ()
PP_TUPLE_POP_BACK((1))          // -> ()
PP_TUPLE_POP_BACK((1, 2, 3))    // -> (1, 2)

PP_TUPLE_REMOVE(1, (1, 2, 3))   // -> (1, 3)
PP_TUPLE_REMOVE(0, (1, 2, 3))   // -> (2, 3)
```

هنا سأوضح قليلاً تنفيذ إدراج العناصر ، كما تم تنفيذ عمليات حذف العناصر وغيرها باستخدام نفس المبدأ. يمكنك استخدام `PP_TUPLE_INSERT(i، elem، tuple)` لإدراج العنصر `elem` في الموضع `i` داخل `tuple`. لتنفيذ هذا العمل ، علينا أولاً نقل العناصر التي تأتي قبل الموضع `i` باستخدام `PP_TUPLE_PUSH_BACK` إلى `tuple` جديد (المسمى `ret`) ، ثم نقوم بإدراج العنصر `elem` في الموضع `i` ، ومن ثم نقوم بنقل العناصر في `tuple` الأصلي التي تأتي بعد أو تكون مساوية للموضع `i` إلى الخلف في `ret`. وبهذا نحصل أخيراً على `ret` الذي يحتوي على النتيجة المطلوبة.

##خلاصة

تهدف هذه المقالة إلى توضيح مبادئ البرمجة باستخدام الماكرو في C/C++ وطريقة تنفيذها الأساسية. بينما أسجل بعض فهمي وإدراكي، آمل أن أكون قادرًا على تقديم بعض الإيضاحات والإلهام للآخرين. يجدر بالذكر أنه على الرغم من أن المقالة طويلة بعض الشيء، إلا أن هناك بعض التقنيات وطرق الاستخدام المتعلقة بالبرمجة بالماكرو التي لم تُتناول، مثل [طريقة الاستدعاء العائد المبنية على التوسع المتأخر](https://github.com/pfultz2/Cloak/wiki/C-Preprocessor-tricks,-tips,-and-idioms#deferred-expression)ترجمة هذه النص إلى اللغة العربية:
إلى الأشخاص المهتمين، يمكنكم البحث بأنفسكم عن المعلومات المتعلقة بالماكروات في `BOOST_PP`، مثل `REPEAT`.

ترجمة النص إلى اللغة العربية:
عملية تصحيح أخطاء برمجة تطبيقات ماكرو هي عملية مؤلمة، يمكننا:

استخدم الخيارات `-P -E` لإخراج نتائج المعالجة المسبق.
* استخدم النسخة المعدلة من `clang` التي ذكرتها سابقاً لدراسة عملية التفكيك بعناية؛
* قم بتفكيك الماكرو المعقد، وا查看 نتائج توسع الماكرو الوسيط؛
قم بحجب الملفات الرأسية والتعريفات الماكرة غير المتعلقة.
وأخيرًا، من الضروري تخيل عملية توسيع الماكرو، فبعد تعرفك على توسيع الماكرو، سيزيد كفاءة عملية تصحيح الأخطاء.

محتوى هذا النص يتعلق بما قمت بإعادة تنفيذه بنفسي بعد فهم المبدأ الأساسي، وقد استوحيت بعض الأفكار من تنفيذ ومقالات `Boost`. إذا كان هناك أي أخطاء، يُرجى إبلاغي في أي وقت، كما أنني متاح لمناقشة أي مسائل ذات صلة.

كود هذا النص موجود بالكامل هنا: [تنزيل](assets/img/2021-3-31-cpp-preprocess/macros.cpp)،[عرض عبر الإنترنت](https://godbolt.org/z/coWvc5Pse)I'm sorry, but there is no text to translate.

##اقتباس

* [Boost.Preprocessor](https://www.boost.org/doc/libs/1_75_0/libs/preprocessor/doc/)
(https://bot-man-jl.github.io/articles/?post=2020/Macro-Programming-Art)

--8<-- "footer_ar.md"


> هذا المنشور تمت ترجمته باستخدام ChatGPT, يرجى تقديم [**ردود فعل**](https://github.com/disenone/wiki_blog/issues/new)وسيتم تحديد أي شواغر. 
