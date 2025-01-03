---
layout: post
title: ملخص معالجة معلمات سطر الأوامر في C/C++
categories:
- c++
catalog: true
tags:
- dev
description: في الوقت السابق قبل كم يوم شفت كود النواة في لينكس، ولفت انتباهي كيفية
  التعامل مع متغيرات الوحدة النواة (moduleparam)، شدني بصراحة، صار عندي رغبة أدرس
  أكثر عن كيفية التعامل بشكل أفضل مع معاملات سطر الأوامر في لغة السي.
figures:
- assets/post_assets/2016-11-19-aparsing/aparsing.png
---

<meta property="og:title" content="C/C++ 的命令行参数处理总结" />

![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/gcc-4.9-blue.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/clang-3.7-birghtgreen.svg){:style="display: inline-block"}

![](assets/img/2016-11-19-aparsing/aparsing.png)

حينما كنت أتصفح شفرة نواة Linux مؤخرًا، لفت انتباهي كيفية معالجة النواة لمعلمات الوحدات (moduleparam)، ووجدتها بارعة للغاية، مما دفعني للتفكير في كيفية معالجة معلمات سطر الأوامر في لغة C بشكل أفضل. يمكن العثور على جميع الشفرات المستخدمة في هذه المقالة [هنا](https://github.com/disenone/aparsing)يدعم الكود تشغيل وتصحيح الأخطاء على نظامي Windows وLinux وMac OS X ، وتوجد إرشادات تفصيلية لعملية الترجمة في ملف README.md.

## getenv

المكتبة القياسية توفّر لنا دالة `getenv`، من واحدة تعنيها بالحرف، هذه الدالة تُستخدم للحصول على المتغيّرات البيئية، لذا بمجرد أن نقوم بتعيين المتغيّرات البيئية المطلوبة مسبقًا ، نستطيع استرجاعها في البرنامج، مما يمكننا من تمرير البارامترات إلى البرنامج غير مباشرة. دعونا ننظر إلى هذا المقطع [الكود](https://github.com/disenone/aparsing/blob/master/getenv/getenv_test.c)عفوًا، لم أستطع فهم النص الذي قمت بإرساله. هل يمكنكم إعادة صياغته أو تقديم سياق إضافي للمساعدة في ترجمته؟

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

ترجمة النص إلى اللغة العربية:

إعلان وظيفة `getenv` كما هو موجود في [4](#__codelineno-0-5)(#__codelineno-0-10)(#__codelineno-0-15)المهمة تتمثل في الحصول على قيمتي متغيري بيئة مختلفين، وإذا كان المتغير صالحًا فإنه يُطبع قيمة المتغير. يجب مراعاة أن `getenv` يُرجع دائمًا سلاسل نصية، ويتعين على المستخدم تحويل أنواع القيم الرقمية يدويًا، لذا فإن الاستخدام ليس مرنًا بما فيه الكفاية. اُجرِ الترجمة واستعرض النتائج:

لا يوجد ترجمة محددة لـ "Windows 下" في هذا السياق.

``` bat
set GETENV_ADD=abc & set GETENV_NUM=1 & .\getenv_test.exe
```

Linux 下：

``` shell
GETENV_ADD=abc GETENV_NUM=2 ./getenv_test 
```

الناتج:

```
GETENV_ADD = abc
GETENV_NUM = 2
```

## getopt

لينكس يوفر لنا مجموعة من الوظائف `getopt، getopt_long، getopt_long_only` لمعالجة الوظائف التي تم تمريرها عبر سطر الأوامر، تصريحات هذه الوظائف الثلاثة هي:

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

`getopt` لا يمكنه معالجة الوسائط القصيرة (أي الوسائط من حرف واحد)، أما `getopt_long, getopt_long_only` فيمكنهما معالجة الوسائط الطويلة. يمكنك العثور على شرح مفصل للدوال في دليل Linux. الآن سنشرح استخدام `getopt` و `getopt_long` من خلال الأمثلة.

الملاحظة الهامة هي أنه لا توجد هذه الدالة في نظام Windows، لذا بحثت عن نسخة من الشفرة المصدرية يمكن ترجمتها على نظام Windows، وأجريت بعض التعديلات البسيطة عليها. يمكن العثور على الشفرة في [هذا الرابط](https://github.com/disenone/aparsing/tree/master/getopt)I'm sorry, but the text you provided does not contain any content to be translated.

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

لنركز الآن على تحليل كيفية استخدام `getopt_long`، حيث تكون البارميترات الثلاثة الأولى لـ `getopt_long` مطابقة تماما لـ `getopt`، وهي عبارة عن: عدد معلمات سطر الأوامر `argc`، مصفوفة معلمات سطر الأوامر `argv`، وصيغة البارميترات القصيرة `optstring`. صيغة `otpstring` تحتوي على أحرف بارميترات قصيرة واحدة تلو الأخرى، وتضاف بعدها نقطة وفاصلة `:` للإشارة إلى وجود بارميتر، ونقطتان وفاصلتان `::` للإشارة إلى بارميتر اختياري. على سبيل المثال، في السطر رقم 19، نجد تعريف لصيغة البارميترات القصيرة، حيث إن البارميتر `b` لا يحتاج إلى بارميتر إضافي، والبارميتر `a` يتطلب بارميترًا إضافيًا، والبارميتر `c` قابل للاختيار.

المعلمات الأخيرتان لدالة `getopt_long` تستخدمان للتعامل مع الخيارات الطويلة، حيث يكون هيكل `option` كالتالي:

```c
struct option {
const char *name;       // الاسم الطويل للمعلمة
int has_arg; // 是否带额外参数
ترجمة النص إلى اللغة العربية:

    int        *flag;       // تحديد كيفية إرجاع نتيجة استدعاء الدالة
int val ؛ // القيمة المُرجعة
};
```
على الرغم من أنه يُقال إنه معرف طويل، إلا أنه يمكن تعيين `الاسم` بطول حرف واحد.

`has_arg` يمكن تعيينها ل`no_argument، required_argument، optional_argument`، تُعنى على التوالي بدون مُعطى، مع مُعطى، مع مُعطى إختياري.

`flag` و `val` يتم استخدامهما معًا. إذا كان `flag = NULL`, ستقوم `getopt_long` بإرجاع `val` مباشرة، وإذا كان `flag` يشير إلى عنوان صحيح، سيقوم `getopt_long` بتنفيذ عملية مماثلة لـ `*flag = val`, تعيين قيمة المتغير الذي يشير إليه `flag` إلى قيمة `val`.

إذا وُجدت `getopt_long` المعلمات القصيرة المُطابقة، سيُعيد قيمة الحرف لتلك المُعلمة القصيرة. إذا تم العثور على مُعلمات طويلة مُطابقة، سيُعيد `val` (`flag = NULL`) أو `0` (`flag != NULL؛ *flag = val;`). إذا واجه حرفًا ليس بمُعلمة، سيُرجع `?`. وفي حال تم معالجة جميع المُعلمات، سيُرجع `-1`.

من خلال استغلال خاصية قيم العودة، يمكننا إنشاء تأثير يجعل القيم الطويلة والقصيرة تحمل نفس المعنى، على سبيل المثال، عندما نقوم بتعيين القيمة الأولى لـ `long_options` إلى `add`، ونقوم بتعيين قيمة `val` لتكون الحرف القصير للمعامل `'a'`، فيمكن لـ `--add` و`-a` أن يُعالَجا ضمن نفس الفرع البرمجي عند العودة، ويتم معاملتهما كمعنى واحد.

القطعة الأخيرة من اللغز هي استخدام `optind` و `optarg` ، حيث `optind` هو موقع العامل التالي في `argv` الذي يجب معالجته ، بينما يشير `optarg` إلى سلسلة العوامل الإضافية.

لتحميل وتشغيل الشيفرات:

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

يشير `-a` و`--add` إلى المعنى نفسه، حيث يتم وضع الوسيطات الاختيارية للوسائط القصيرة مباشرة بعد الوسيطة، مثل `-c4`، بينما تحتاج الوسيطات الطويلة للوسائط الاختيارية إلى وجود علامة يساوي، مثل `--verbose=3`.

## mobuleparam

حسنًا، وصلنا أخيرًا إلى الطريقة التي قامت بإثارة هذه المقالة، حيث استخدم نواة Linux طريقة ذكية جدًا لتمرير المعلمات لوحدات النواة، وهذه الطريقة تُسمى `moduleparam`. سأشرح هنا بإيجاز كيفية عمل `moduleparam` في نواة Linux، ولشرح مفصل يُمكن الرجوع إلى الشيفرة البرمجية. على الرغم من أنني اقتبست بعض طرق التعامل مع `moduleparam`، إلا أن هناك بعض الاختلافات بينها وبين `moduleparam` في نواة Linux، وللتمييز سأشير إلى طريقتي بـ `small moduleparam`، أما النواة الخاصة بنظام Linux فستظل تسمى `moduleparam`.

لنلقَ نظرة على كيفية استخدام `moduleparam`، ابدأ بتعريفه في الوحدة:

```c
int enable_debug = 0;
module_param(enable_debug, int, 0);
```

ثم عند تحميل الوحدة ، أدخل المعلمات:

```shell
$ insmod mod enable_debug=1
```

تم تعيين المتغير `enable_debug` بشكل صحيح إلى `1`، مما يجعل استخدامه سهلًا جدًا، ويتطلب قليلًا من الشفرة الإضافية. يمكن كتابة الشفرة بطريقة قصيرة وأنيقة، دون الحاجة لكتابة العديد من التكرارات والتحققات الشرطية كما في `getenv` و `getopt`. بالإضافة إلى ذلك، يتضمن تحويل الأنواع تلقائيًا. لذلك، عندما رأيته، تساءلت إذا كان بإمكاني استخدام هذه الطريقة في معالجة معلمات سطر الأوامر، سيكون ذلك أفضل بكثير.

لنلق نظرة على تنفيذ وحدة المعلمة النواة:

```cpp linenums="1"
struct kernel_param {
const char *name;           // 变量名字
u16 perm;                   // مستوى إذن المتغير
u16 flags;                  // متغير ما إذا كان من نوع bool
الجملة "param_set_fn set; // str -> 变量值" ستترجم لتصبح:

متغيّر set من نوع param_set_fn؛           // str -> 变量值
تحصل_fn get على قيمة المتغير -> نص
	union {
void *arg;              // مؤشر المتغير
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

"module_param" هو ماكرو، يقوم في الحقيقة بإنشاء هيكل `kernel_param` يمكن إرجاعه للمتغير المُدخل، وهذا الهيكل يحتوي على المعلومات الكافية للوصول وضبط المتغير، مثلا في السطور 20-24، ومن ثم يتم وضع الهيكل ضمن قسم يُسمى `__param` (باستخدام `__section__("__param")`). بعد حفظ الهيكل بشكل صحيح، يقوم النواة بالبحث عن مكان قسم `__param` في ملف elf وعدد الهياكل فيه، ثم ضبط قيم كل معلمة بناءً على الاسم و `param_set_fn` خلال تحميل الوحدة. كيفية العثور على قسم مُحدد بالاسم تعتمد على النظام الأساسي، ففي نواة Linux يتم التعامل مع ملفات elf، وتوفر Linux أمر `readelf` لعرض معلومات ملفات elf، ويمكن للمهتمين الاطلاع على معلومات تعليمات الاستخدام لـ `readelf`.

النص المُراد ترجمته إلى اللغة العربية هو:

يُقال أعلاه أن التعامل مع نواة Linux يعتمد على النظام الأساسي، ولكنني أريد أسلوبًا للتعامل مع المعلمات غير المتعلق بالنظام، لذا يجب علينا تغيير طريقة `moduleparam` الأصلية بشكل بسيط، عن طريق إزالة إعلان `__section(" __param")`، حيث أننا لا نرغب في عملية قراءة ملف `elf section` بشكل معقد. دعونا نلقي نظرة على كيفية الاستخدام بعد التعديل:

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

للحفاظ على هيكلية كل انعكاس، قمت بإضافة ماكرو `init_module_param(num)` لتعريف مساحة حفظ الهيكل، حيث يُعتبر `num` عدد المعلمات. إذا تجاوز عدد المعلمات المعلن عنها `num`، سيُشعر البرنامج بحدوث خطأ تأكيد. تم حذف المعلمة الأخيرة التي تُعبر عن صلاحيات الوصول في تعريف `module_param`، على عكس النسخة الأصلية. تمت إضافة الـماكرو `module_param_bool` لمعالجة المتغيرات من نوع `bool`، وهذا الأمر غير ضروري في نظام Linux لأنه يستخدم وظيفة المضمنة `__builtin_types_compatible_p` في مترجم gcc للتحقق من نوع المتغيرات. للأسف، لا يتوفر هذا الدالة في MSVC، لذا تمت إزالتها واستبدالها بماكرو جديد. أما الـماكرو `module_param_array` و `module_param_string`، فيتعاملان مع مصفوفات وسلاسل نصوص، وكانت هاتان الوظيفتان متاحتان في النسخة الأصلية أيضًا.

بمجرد إكمال تعريف المعلمات، يتعين معالجة المعلمات الواردة عن طريق استخدام الوسيط `parse_params` مع إدخال `argc، argv`، حيث يكون البرمتر الثالث مؤشر دالة رد الاستدعاء للمعلمات غير المعروفة، يمكن تمرير قيمة `NULL`، وبذلك ستُنهى معالجة المعلمات في حدود المعلمات الموجودة، ثم يُرجع رمز الخطأ.

ترجمة النص إلى اللغة العربية:

تشغيل وتنفيذ الشيفرة:

```
.\moduleparam_test.exe error=0 test=101 btest=1 latest=1,2,3 strtest=\"Hello World!\"
Parsing ARGS: error=0 test=101 btest=1 latest=1,2,3 strtest="Hello World!"
find unknown param: error
test = 101
btest = Y
latest = 1,2,3
strtest = Hello World!
```

يمكن رؤية أن القيم الرقمية والمصفوفات والسلاسل يمكن قراءتها بشكل صحيح وتحويل تنسيقها، في حال واجهت أي من الباراميترات صعوبة في التحويل، سيتم إرجاع رمز الخطأ وطباعة المعلومات ذات الصلة. يمكننا بسهولة إضافة بضعة أسطر من الشيفرة، لإكمال قراءة الباراميترات ومعالجة التحويل، وستكون العملية أنيقة للغاية. يمكن الإطلاع على التنفيذ التفصيلي مباشرة من خلال الشيفرة [هنا](https://github.com/disenone/aparsing)I'm sorry, but I can't provide a translation for that text as it does not contain any content to be translated.

##ملخص

لقد قمنا هذه المرة بتلخيص ثلاث طرق لمعالجة معاملات سطر الأوامر في C/C++، وهي `getenv`، `getopt`، و `moduleparam`. لكل من هذه الطرق خصائصها الخاصة، ونستطيع اختيار الطريقة المناسبة بناءً على احتياجاتنا الفعلية في المستقبل.

`getenv` هي وظيفة مدمجة متعددة المنصات ويمكن استخدامها مباشرة، ومع ذلك فهي قديمة نوعًا ما، وتستخدم المتغيرات البيئية، مما يؤدي إلى تلويث البيئة بشكل معين. من الأفضل تنظيف المتغيرات البيئية غير الضرورية قبل كل استخدام لتجنب ترك بقايا الإعدادات السابقة وتلويث البيئة.
`getopt` مدعوم بشكل أصلي في منصة Linux وليس في Windows. لذلك، يتطلب تضمين الشفرة التنفيذية ليمكن استخدامه على منصات مختلفة. عملية تمرير المعلمات متوافقة مع معايير تمرير الأوامر في Linux، تدعم المعلمات الاختيارية. ولكن استخدامه يعتبر معقدًا قليلا، حيث يتطلب عادةً حلقات وشروط لمعالجة المعلمات المختلفة، ولا يتفاعل بشكل جيد مع المعلمات من نوع الأرقام.
"moduleparam" هو أداة لمعالجة معلمات سطر الأوامر مستوحاة من تنفيذ "moduleparam" في نواة Linux. تدعم الاستخدام عبر الأنظمة الأساسية، سهلة الاستخدام، وتسمح بتحويل أنواع مختلفة من المعلمات، لكن العيب هو أن كل معلمة تتطلب متغيرًا مقابلاً.

--8<-- "footer_ar.md"


> هذه المشاركة تمت ترجمتها باستخدام ChatGPT، يرجى تقديم [**ردود فعل**](https://github.com/disenone/wiki_blog/issues/new)يرجى إشارة إلى أية نقص أو تفاصيل غير مذكورة. 
