---
layout: post
title: ملخص معالجة معاملات سطر الأوامر في C/C++
categories:
- c++
catalog: true
tags:
- dev
description: في فترة سابقة، عندما كنت أبحث في شيفرة نواة Linux، شاهدت كيفية تعامل
  النواة مع معلمات الوحدات (moduleparam)، وشعرت أنها عبقرية، مما دفعني للتفكير في
  كيفية تحسين معالجة معلمات سطر الأوامر في لغة C.
figures:
- assets/post_assets/2016-11-19-aparsing/aparsing.png
---

<meta property="og:title" content="C/C++ 的命令行参数处理总结" />

![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/gcc-4.9-blue.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/clang-3.7-birghtgreen.svg){:style="display: inline-block"}

![](assets/img/2016-11-19-aparsing/aparsing.png)

في المرة السابقة عندما كنت أتصفح رموز نواة Linux, لفت انتباهي كيفية معالجة النواة لمعلمات الوحدات التابعة (moduleparam)، شعرت بأنها ذكية بما فيه الكفاية لتحفيزني على دراسة كيفية معالجة معلمات سطر الأوامر في لغة ++C بشكل أفضل. جميع الشيفرات المستخدمة في هذا المقال متوفرة هنا [aparsing](https://github.com/disenone/aparsing). يدعم الكود الترجمة والتشغيل على أنظمة Windows و Linux و Mac OS X، يوجد دليل الترجمة التفصيلي في ملف README.md.

## getenv

(https://github.com/disenone/aparsing/blob/master/getenv/getenv_test.c)عذرًا، لا يوجد نص لترجمته.

``` cpp linenums="1"
#include <stdlib.h>
#include <stdio.h>

//char *getenv( const char *name );
//GETENV_ADD=abc GETENV_NUM=2 ./getenv_test 

int main (int argc, char **argv)
{
    char *add, *num;
    if((add = getenv("GETENV_ADD")))
        printf("GETENV_ADD = %s\n", add);
    else
        printf("GETENV_ADD not found\n");

    if((num = getenv("GETENV_NUM")))
    {
        int numi = atoi(num);
        printf("GETENV_NUM = %d\n", numi);
    }
    else
        printf("GETENV_NUM not found\n");
}
```

`getenv` وظيفة إعلان كما في رقم [4](#__codelineno-0-5)احرص على إدخال اسم المتغير الذي ترغب في الحصول على قيمته، فإذا لم يتم العثور على المتغير، يتم إرجاع 0. [10](#__codelineno-0-10)和 [15](#__codelineno-0-15)المهمة هي الحصول على قيمتين لمتغيري بيئة مختلفين، ثم طباعة قيمة المتغير إذا كان صالحًا. يجب ملاحظة أن `getenv` يُرجع دائمًا سلاسل نصية، وبالتالي يجب على المستخدم تحويل الأنواع الرقمية يدويًا، مما يجعل الاستخدام غير مريح. حسناً! ابدأ الكود وجربه.

في نظام Windows:

``` bat
set GETENV_ADD=abc & set GETENV_NUM=1 & .\getenv_test.exe
```

في نظام Linux:

``` shell
GETENV_ADD=abc GETENV_NUM=2 ./getenv_test 
```

الناتج:

```
GETENV_ADD = abc
GETENV_NUM = 2
```

## getopt

يقدم لنا Linux مجموعة من الدوال `getopt, getopt_long, getopt_long_only` لمعالجة المعلمات المرسلة عبر سطر الأوامر، والإعلانات عن هذه الدوال هي:

```cpp linenums="1"
extern char *optarg;
extern int optind, opterr, optopt;

int getopt(int argc, char * const argv[],
                  const char *optstring);

int getopt_long(int argc, char * const argv[],
            const char *optstring,
            const struct option *longopts, int *longindex);

int getopt_long_only(int argc, char * const argv[],
            const char *optstring,
            const struct option *longopts, int *longindex);
```

`getopt` يمكنه فقط معالجة الوسائط القصيرة (وهي الوسائط التي تتكون من حرف واحد فقط)، بينما يمكن لـ `getopt_long` و `getopt_long_only` معالجة الوسائط الطويلة. بإمكانك الاطلاع على دليل Linux لمزيد من الشرح حول الدوال. الآن دعونا نستعرض استخدام `getopt` و `getopt_long` من خلال الأمثلة.

ما يجب ملاحظته هو أنه لا توجد هذه المجموعة من الوظائف في نظام Windows، لذا بحثت عن نسخة من الشيفرة المصدرية يمكن تجميعها في نظام Windows، وأدخلت بعض التعديلات البسيطة عليها، الشيفرة متوفرة كاملة على [هذا الرابط](https://github.com/disenone/aparsing/tree/master/getopt)I am sorry, but I cannot provide a translation for the character "。" as it does not contain any text or meaning. If you have any other text that needs translation, feel free to ask!

```cpp linenums="1"
// test getopt

#include <getopt.h>
#include <stdio.h>
#include <string.h>

static struct option long_options[] =
{
    {"add", required_argument, 0, 'a'},
    {"append", no_argument, 0, 0},
    {"delete", required_argument, 0, 0},
    {"verbose", optional_argument, 0, 0},
    {"create", no_argument, 0, 0},
    {"file", required_argument, 0, 0},
    {"help", no_argument, 0, 0},
    {0, 0, 0, 0}
};

static char simple_options[] = "a:bc::d:0123456789";

int main (int argc, char **argv)
{

    int c;
    int digit_optind = 0;

    while (1)
    {
        int this_option_optind = optind ? optind : 1;
        int longindex = -1;

        c = getopt_long(argc, argv, simple_options, long_options, &longindex);
        if (c == -1)
        break;

        switch (c)
        {
            // long option
            case 0:
                   printf("option %s", long_options[longindex].name);
                   if (optarg)
                       printf(" with arg %s", optarg);
                   printf("\n");
                   break;

                break;

            case '0':
            case '1':
            case '2':
            case '3':
            case '4':
            case '5':
            case '6':
            case '7':
            case '8':
            case '9':
                if(digit_optind != 0 && digit_optind != this_option_optind)
                    printf("digits occur in two different argv-elements.\n");

                digit_optind = this_option_optind;
                printf("option %c\n", c);
                break;

            case 'a':
                printf("option a with value '%s'\n", optarg);
                break;

            case 'b':
                printf("option b\n");
                break;

            case 'c':
                if(optarg)
                    printf("option c with value '%s'\n", optarg);
                else
                    printf("option c\n");
                break;

            case '?':
                break;

            default:
                printf("?? getopt returned character code 0%o ??\n", c);
        } // switch
    } // while

    if (optind < argc)
    {
        printf("non-option ARGV-elements: ");
        while (optind < argc)
        printf("%s ", argv[optind++]);
        printf("\n");
    }

    return 0;
}

```

لنركز في تحليل كيفية استخدام `getopt_long`، الذي يتشارك الباراميترات الثلاثة الأولى مع `getopt` وهي: عدد معلمات سطر الأوامر `argc`، مصفوفة معلمات سطر الأوامر `arv`، وشكل تفصيل الباراميترات القصيرة `otpstring`. تتألف صيغة `otpstring` من أحرف باراميترات قصيرة متتالية، تتبعها نقطتان `:` تعني أنها تتطلب باراميتر، بينما نقطتان متتاليتان `::` تعني باراميتر اختياري. كمثال في السطر رقم 19، فإن شكل تعريف الباراميترات القصيرة هو كالتالي: باراميتر `b` لا يتطلب باراميتر إضافي، بينما باراميتر `a` يتطلب باراميتر إضافي، وباراميتر `c` يتطلب باراميتر اختياري.

`getopt_long` البارامتران الأخيران مُستخدمان لمعالجة البارامترات الطويلة، حيث يكون هيكل `option` كالتالي:

```c
struct option {
const char *name;       // اسم المعامل الطويل
int         has_arg;    // هل يحتوي على معلمة إضافية
int *flag; // تعيين كيفية إرجاع نتيجة استدعاء الدالة
int val؛        // القيمة المُرادَة
};
```
على الرغم من أنه يُعتبر معلمة طويلة، يمكن تعيين `name` بطول حرف واحد.

`has_arg` يمكن أن يتم تعيينها إلى `no_argument, required_argument, optional_argument`، والتي تعني على التوالي عدم وجود معطيات، مع معطيات، مع معطيات اختيارية.

`flag` و `val` هما متغيران يُستخدمان معًا، فإذا كان `flag = NULL`، فإن `getopt_long` ستعيد مباشرة `val`، أما إذا كان `flag` مؤشراً صالحاً، فستقوم `getopt_long` بعملية مشابهة لـ `*flag = val`، حيث تضبط المتغير المشار إليه بـ `flag` إلى قيمة `val`.

إذا وجدت `getopt_long` معلمة قصيرة مطابقة، ستعيد القيمة الحرفية لتلك المعلمة القصيرة، وإذا وجدت معلمة طويلة مطابقة، ستعيد `val` (إذا كان `flag = NULL`) أو ستعيد `0` (إذا كان `flag != NULL; *flag = val;`)؛ إذا واجهت حرفًا غير معلمة، ستعيد `؟`؛ وإذا تم معالجة جميع المعلمات، ستعيد `-1`.

من خلال استخدام خاصية القيمة المُرجعة، يُمكننا إنشاء تأثير مماثل بين الوسيط الطويل والوسيط القصير، على سبيل المثال، إذا كان الوسيط الأول في `long_options` إسمه `add` وكانت قيمته `val` مُعينة بحرف الوسيط القصير `'a'`، فإنه عند التحقق من القيمة المُرجعة، سيُعامل كل من `--add` و `-a` بصورة متماثلة وسيتم معاملتهم على أنها تعني الشيء نفسه.

القطعة الأخيرة من اللغز هي استخدام `optind` و `optarg`، حيث `optind` هو موقع البارامتر التالي المراد معالجته في `argv`، بينما `optarg` يشير إلى سلسلة البيانات الإضافية.

قم بترجمة النص إلى اللغة العربية: 

تشغيل وتنفيذ الشفرة:

```
$ .\getopt_test -a 1 -b -c4 --add 2 --verbose --verbose=3 -123 -e --e
option a with value '1'
option b
option c with value '4'
option a with value '2'
option verbose
option verbose with arg 3
option 1
option 2
option 3
.\getopt_test: invalid option -- e
.\getopt_test: unrecognized option `--e'

```

ترجمة النص إلى اللغة العربية:

`-a` و `--add` يعنيان نفس الشيء، حيث يمكن إضافة الوسائط الاختيارية للمعلمات القصيرة مباشرة بعد الحرف، مثل `-c4`، أما الوسائط الاختيارية للمعلمات الطويلة يجب أن تكون متبوعة بعلامة الجمع، مثل `--verbose=3`.

## mobuleparam

حسناً، أخيراً وصلنا إلى الطريقة التي أثارت هذا المقال. استخدم نواة لينكس طريقة مبتكرة لنقل المعلمات إلى وحدات النواة، وهذه الطريقة تُسمى `moduleparam`. سأقوم هنا بشرح بسيط لطريقة `moduleparam` في نواة لينكس، ولمن يرغب في تفاصيل أكثر، يمكنه مراجعة الشيفرة. على الرغم من أنني استوحيت بعضاً من طرق معالجة `moduleparam`، إلا أن هناك بعض الاختلافات مع `moduleparam` في نواة لينكس، ولتجنب الالتباس، سأطلق على طريقتي اسم `small moduleparam`، بينما ستظل نواة لينكس تُسمى `moduleparam`.

دعنا نلقِ نظرة على كيفية استخدام `moduleparam`، بإعلان داخل الوحدة:

```c
int enable_debug = 0;
module_param(enable_debug, int, 0);
```

ثم عند تحميل الوحدة ، أدخل المعلمات:

```shell
$ insmod mod enable_debug=1
```

تم تعيين المتغير `enable_debug` بشكل صحيح على قيمة `1`، مما يجعل الاستخدام سهلًا، والشيفرة التي يجب إضافتها قليلة للغاية. الشيفرة يمكن أن تكون قصيرة وأنيقة، ولا حاجة لكتابة العديد من التكرارات والتحققات مثل `getenv` و `getopt`، بالإضافة إلى أنه يوفر التحويل التلقائي للأنواع. لذلك، عندما رأيته، تساءلت إذا يمكنني استخدام هذه الطريقة لمعالجة مُدخلات سطر الأوامر، سيكون أمرًا رائعًا.

接着来看看 `moduleparam` 的核心实现：  
دعونا نلقي نظرة على التنفيذ الأساسي لـ `moduleparam`:

```cpp linenums="1"
struct kernel_param {
سجل char *name؛           // 变量名字
u16 perm;                   // متغير إذن الوصول
سجل u16؛                  // هل المتغير من نوع بولية
مجموعة الوظيفة param_set_fn set؛  // str -> قيمة المتغير
get; // متغير قيمته -> سلسلة
	union {
سلسلة النص الأصلية: 

void *arg;              // 变量指针

سلسلة النص المترجمة:

void *arg;              // مؤشر للمتغير
		const struct kparam_string *str;
		const struct kparam_array *arr;
	};
};

#define __module_param_call(prefix, name, set, get, arg, isbool, perm)	\
	/* Default value instead of permissions? */			\
	static int __param_perm_check_##name __attribute__((unused)) =	\
	BUILD_BUG_ON_ZERO((perm) < 0 || (perm) > 0777 || ((perm) & 2))	\
	+ BUILD_BUG_ON_ZERO(sizeof(""prefix) > MAX_PARAM_PREFIX_LEN);	\
	static const char __param_str_##name[] = prefix #name;		\
	static struct kernel_param __moduleparam_const __param_##name	\
	__used								\
        __attribute__ ((unused,__section__ ("__param"),aligned(sizeof(void *)))) \
	= { __param_str_##name, perm, isbool ? KPARAM_ISBOOL : 0,	\
	    set, get, { arg } }

#define module_param_call(name, set, get, arg, perm)			      \
	__module_param_call(MODULE_PARAM_PREFIX,			      \
			    name, set, get, arg,			      \
			    __same_type(*(arg), bool), perm)

#define module_param_named(name, value, type, perm)			   \
	param_check_##type(name, &(value));				   \
	module_param_call(name, param_set_##type, param_get_##type, &value, perm); \
	__MODULE_PARM_TYPE(name, #type)

#define module_param(name, type, perm)				\
	module_param_named(name, name, type, perm)

```

`module_param` هو ماكرو يقوم فعليًا بإنشاء بنية `kernel_param` التي يمكن أن تعكس المتغير المدخل، حيث تحتفظ هذه البنية بمعلومات كافية للوصول إلى المتغير وتعيينه، أي من السطور 20-24، وتضع البنية في قسم يسمى `__param` ( `__section__ ("__param")` ). بعد إعداد البنية، سيقوم النواة عند تحميل الوحدة بالبحث عن موقع قسم `__param` في ملف elf وعدد البنى، ثم يقوم بتعيين قيم كل معلمة بناءً على الاسم و `param_set_fn`. الطريقة المحددة للعثور على قسم بالاسم تعتمد على النظام الأساسي، حيث يقوم نواة لينكس بمعالجة ملفات elf، ويوفر لينكس الأمر `readelf` لعرض معلومات حول ملف elf، ويمكنك الاطلاع على معلومات المساعدة لـ `readelf` إذا كنت مهتمًا.

النص المُراد ترجمته هو:

قال أحدهم سابقًا إن كيفية تنفيذ نواة Linux تعتمد على النظام، وأريد طريقة لتنفيذ المعاملات تتعلق بالنظام، لذا علينا تغيير طريقة `moduleparam` الأصلية قليلًا، وحذف إعلان `__section__("__param")`، إذ لسنا بحاجة حقًا لقراءة قسم elf بطريقة مُعقدة. دعنا نلقي نظرة على كيفية الاستخدام بعد التعديل:

```cpp linenums="1"
#include "moduleparam.h"
#include <stdio.h>

static int test = 0;
static bool btest = 0;
static unsigned int latest_num = 0;
static long latest[10] = {0};
static char strtest[20] = "\0";

void usage()
{
    char *msg = "usage: moduleparam_test [test=int] [btest[=bool]] [latest=int array] [strtest=string]\n";
    printf(msg);
}

int unknown_handler(char *param, char *val)
{
    printf("find unknown param: %s\n", param);
    return 0;
}

int main (int argc, char **argv)
{
    init_module_param(4);
    module_param(test, int);
    module_param_bool(btest);
    module_param_array(latest, long, &latest_num);
    module_param_string(strtest, strtest, sizeof(strtest));

    int ret = parse_params(argc, argv, unknown_handler);

    if(ret != 0)
    {
        usage();
        return 0;
    }

    char buf[1024];
    for(int i=0; i < MODULE_INIT_VARIABLE_NUM; ++i)
    {
        MODULE_INIT_VARIABLE[i].get(buf, &MODULE_INIT_VARIABLE[i]);
        printf("%s = %s\n", MODULE_INIT_VARIABLE[i].name, buf);
    }
    return 0;
}

```

لذا، من أجل الحفاظ على هيكل كل انعكاس، أضفت ماكرو `init_module_param(num)` للإعلان عن المساحة المخصصة لحفظ الهيكل، حيث `num` هو عدد المعلمات. إذا تجاوز العدد الفعلي للمعلمات المعلنة `num`، سيثير البرنامج خطأ تأكيد. إعلان `module_param` مختلف بعض الشيء عن النسخة الأصلية، حيث تم إزالة المعلمة الأخيرة التي تشير إلى حقوق الوصول، دون إدارة الحقوق. بالإضافة إلى ذلك، تم إضافة ماكرو `module_param_bool` لمعالجة المتغيرات التي تعبر عن `bool`، وهذا غير مطلوب في إصدار Linux لأنه يستخدم الدالة المدمجة `__builtin_types_compatible_p` لتحديد نوع المتغير، ولكن للأسف، لا تحتوي MSVC على هذه الدالة، لذا لم يكن أمامي سوى إزالة هذه الميزة وإضافة ماكرو. أما `module_param_array` و `module_param_string` فهي تعالج المصفوفات والسلاسل النصية، وكلا هذين الوظيفتين موجودتان أيضًا في النسخة الأصلية.

انتهى تحديد المعلمات، الآن عليك معالجة المعلمات الواردة، استخدم الماكرو `parse_params`، قدم `argc, argv`، الباراميتر الثالث هو مؤشر على وظيفة إرجاع لمعالجة المعلمات غير المعروفة، يمكن تقديم `NULL`، وسيؤدي ذلك إلى قطع معالجة المعلمات إذا دخلت معلمات في وسيط الوضع الجاري، مع إرجاع رمز خطأ.

حسنًا، إليك النص المترجم إلى اللغة العربية:

ترجمة الرموز وتشغيل الشيفرة:

```
.\moduleparam_test.exe error=0 test=101 btest=1 latest=1,2,3 strtest=\"Hello World!\"
Parsing ARGS: error=0 test=101 btest=1 latest=1,2,3 strtest="Hello World!"
find unknown param: error
test = 101
btest = Y
latest = 1,2,3
strtest = Hello World!
```

يمكن رؤية أن القيم الرقمية والمصفوفات والسلاسل يمكن قراءتها بشكل صحيح وتحويل تنسيقها، وإذا واجهنا معلمة لا يمكن تحويل تنسيقها، سيتم إرجاع رمز الخطأ وطباعة المعلومات ذات الصلة. يمكننا ببساطة إضافة بضع سطور من الشيفرة، لاستكمال قراءة وتحويل المعلمات، لتكون سهلة الاستخدام. يمكن الاطلاع على التنفيذ التفصيلي مباشرة من خلال الشيفرة، [هنا](https://github.com/disenone/aparsing)I'm sorry, but I can't provide a translation for just a period "。" as it doesn't contain any meaningful content. If you have a sentence or text you'd like me to translate into Arabic, please provide it and I'll be happy to help.

##لخَتَم الجلسة.

في هذا المقال، قمنا بتلخيص ثلاث طرق لمعالجة معلمات سطر الأوامر في C/C++، وهي `getenv` و `getopt` و `moduleparam`. تتميز كل طريقة بخصائصها الخاصة، ويمكن اختيار الطريقة المناسبة حسب الحاجة في المستقبل.

- `getenv` مدعوم بشكل أصلي عبر منصات متعددة ويمكن استخدامه مباشرة، ولكنه أيضًا بدائي جدًا ويستخدم المتغيرات البيئية، مما يسبب تلوثًا معينًا للبيئة. من الأفضل تنظيف المتغيرات البيئية غير الضرورية قبل كل استخدام لتجنب بقاء إعدادات الجلسة السابقة.
- `getopt` هو مدعوم بشكل أصلي على منصة لينكس، بينما ويندوز لا يدعمه، لذا يجب تضمين شفرة التنفيذ للاستخدام عبر المنصات. تمرير المعلمات يتماشى مع معايير تمرير أوامر لينكس، ويدعم المعلمات الاختيارية، لكن استخدامه قد يكون متعبًا بعض الشيء، حيث يتطلب عادةً حلقات وشروط لمعالجة المعلمات المختلفة، وهو غير صديق للمعلمات ذات الأنواع العددية.
`moduleparam` هو أداة معالجة معاملات سطر الأوامر مستوحاة من تنفيذ `moduleparam` في نواة Linux، تدعم استخدامًا على مستوى الأنظمة المختلفة، سهلة الاستخدام، تدعم تحويل الأنواع المختلفة من المعاملات، العيب الوحيد هو أن كل معامل يحتاج إلى متغير مقابل له.

--8<-- "footer_ar.md"


> هذه المنشورة تمت ترجمتها باستخدام ChatGPT، يرجى تقديم [**ملاحظات**](https://github.com/disenone/wiki_blog/issues/new)إشارة بإظهار أي شيء مفتقد. 
