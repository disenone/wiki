---
layout: post
title: C/C++의 명령줄 인수 처리 요약
categories:
- c++
catalog: true
tags:
- dev
description: 얼마 전에 리눅스 커널 코드를 살펴보다 모듈 파라미터에 대한 내용을 보게 되었는데, 정말 뛰어난 것 같아서 C 언어에서의 명령행
  매개변수를 어떻게 더 효과적으로 처리할 수 있는지 공부하고 싶게 만들었어.
figures:
- assets/post_assets/2016-11-19-aparsing/aparsing.png
---

<meta property="og:title" content="C/C++ 的命令行参数处理总结" />

![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/gcc-4.9-blue.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/clang-3.7-birghtgreen.svg){:style="display: inline-block"}

![](assets/img/2016-11-19-aparsing/aparsing.png)

얼마 전에 Linux 커널 코드를 살펴보다가 모듈 파라미터(moduleparam)에 대한 커널 처리를 보게 되었는데, 정말 멋진 것 같아서 C 언어에서 명령행 인수를 더 잘 처리하는 방법을 연구하고 싶어졌어요. 이 문서에서 사용된 모든 코드는 여기에 있습니다 [aparsing](https://github.com/disenone/aparsing)Windows, Linux, Mac OS X에서 컴파일 및 실행을 지원하는 코드이며, 자세한 컴파일 가이드는 README.md 파일에 있습니다.

## getenv

(https://github.com/disenone/aparsing/blob/master/getenv/getenv_test.c)제목：해당 내용을 한국어로 번역해주십시오.

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

`getenv` 함수 선언은 [4](#__codelineno-0-5)(#__codelineno-0-10)(#__codelineno-0-15)`行` means getting the values of two environment variables separately, and if the variables are valid, print their values. It is important to note that the `getenv` function returns strings, so the user needs to manually convert them to numerical types, making it less convenient to use. Compile and run:

Windows 하에서:

``` bat
set GETENV_ADD=abc & set GETENV_NUM=1 & .\getenv_test.exe
```

리눅스에서:

``` shell
GETENV_ADD=abc GETENV_NUM=2 ./getenv_test 
```

출력:

```
GETENV_ADD = abc
GETENV_NUM = 2
```

## getopt

Linux provides us with a set of functions `getopt, getopt_long, getopt_long_only` to handle the command line arguments passed to the program. The declarations of these three functions are as follows:

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

`getopt` handles only short options (i.e., single-character options), while `getopt_long` and `getopt_long_only` can handle long options. For detailed function explanations, you can refer to the manual in Linux. Here, we will explain how to use `getopt` and `getopt_long` through examples.

(https://github.com/disenone/aparsing/tree/master/getopt)I'm sorry, but there is no text to translate. Can you please provide the content you need translation for?

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

우리는 `getopt_long`의 사용법을 중점적으로 분석할 것입니다. `getopt_long`의 처음 세 개의 매개변수는 `getopt`과 동일합니다. 각각은: 명령행 인수 개수 `argc`, 명령행 인수 배열 `argv`, 짧은 옵션 문자열 `optstring`입니다. `optstring`의 형식은 각각의 짧은 옵션 문자 뒤에 콜론 `:`을 추가하여 매개변수가 있는 것을 나타내고, 두 개의 콜론 `::`은 선택적 매개변수를 나타냅니다. 예를 들어, 19번째 줄은 짧은 옵션의 형태를 선언하는 것입니다. `b` 옵션은 추가 매개변수가 없고, `a` 옵션은 추가 매개변수가 있으며, `c`는 선택적 매개변수가 있습니다.

`getopt_long` function의 마지막 두 매개변수는 긴 옵션을 다루는 데 사용되며, `option` 구조체는 다음과 같습니다:

```c
struct option {
const char *name;       // 長한 이름
int has_arg; // Extra parameter included or not
int        *flag;       // 함수 호출 결과를 반환하는 방법을 설정합니다
int val;        // The returned value
};
```
긴 매개변수라고 하지만 `name`은 여전히 한 글자로 설정할 수 있습니다.

`has_arg` can be set to `no_argument, required_argument, optional_argument`, which respectively indicate no argument, required argument, optional argument.

`flag`和`val`는 함께 사용되며, `flag = NULL`이면 `getopt_long`은 직접 `val`을 반환합니다. 그러나 유효한 포인터인 경우 `flag`가 `*flag = val`과 유사한 작업을 실행하여 `flag`가 가리키는 변수를 `val` 값으로 설정합니다.

만약 `getopt_long`가 짧은 옵션과 일치하는 경우 해당 짧은 옵션의 문자 값을 반환하고, 긴 옵션과 일치하는 경우 `val`을 반환합니다(`flag = NULL`인 경우) 또는 `0`을 반환합니다(`flag != NULL; *flag = val;`의 경우)；옵션이 아닌 문자를 만나면 `?`을 반환합니다. 모든 옵션이 처리된 경우, `-1`을 반환합니다.

반환값의 특성을 활용하여 우리는 장 단축어의 의미가 동일한 효과를 내도록 만들 수 있습니다. 예를 들어 `long_options`의 첫 번째 매개변수 `add`의 `val` 값을 단축어 문자인 `'a'`로 설정하면, 결과적으로 `--add`와 `-a`는 동일한 처리 분기로 이동하여 동일한 의미로 처리됩니다.

퍼즐의 마지막 조각은 `optind`와 `optarg`의 사용 방법입니다. `optind`는 `argv`에서 다음 처리할 매개변수의 위치이며, `optarg`는 추가 매개변수 문자열을 가리킵니다.

소스 코드를 컴파일하고 실행하십시오:

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

`-a` 와 `--add`는 같은 의미이며, 짧은 매개변수의 선택적 매개변수는 바로 뒤에 따라옵니다. 예를 들어 `-c4`처럼요. 그러나 긴 매개변수의 선택적 매개변수는 등호가 필요합니다. 예를 들어 `--verbose=3` 같은 경우입니다.

## mobuleparam

ok, 이제 이 글의 시작점인 방법에 도착했다. Linux 커널은 모듈에 파라미터를 전달하기 위해 굉장히 편리한 방법을 사용했는데, 그것이 바로 `moduleparam`이다. 여기서 간단히 설명하고, 더 자세한 내용은 코드를 확인하시기 바랍니다. `moduleparam`의 처리 방법을 차용했지만 Linux 커널의 `moduleparam`과는 약간 다른 점이 있습니다. 구분하기 위해서 제 방법을 `small moduleparam`이라고 부르고, Linux 커널의는 여전히 `moduleparam`이라고 할 것입니다.

모듈parameter의 사용법을 먼저 살펴보겠습니다. 모듈 내에서 선언해주세요:

```c
int enable_debug = 0;
module_param(enable_debug, int, 0);
```

모듈을 로드할 때 입력 매개변수를 입력합니다:

```shell
$ insmod mod enable_debug=1
```

변수 `enable_debug`가 정확히 `1`로 설정되어 있으면 사용하기 편하고 추가해야 할 코드도 적고, 코드를 매우 간결하고 우아하게 작성할 수 있습니다. `getenv` 및 `getopt`와 같이 많은 반복 조건문을 작성할 필요도 없고, 자체적인 형 변환 기능도 갖추고 있어서 이 방식을 명령행 인수 처리에 활용할 수 있다는 생각이 듭니다.

`moduleparam` 의 핵심 구현을 살펴보겠습니다:

```cpp linenums="1"
struct kernel_param {
name이라는 const char 형 변수입니다.
u16 perm;                   // 변수 접근 권한
u16 플래그;                  // 변수가 부울 유형인지 여부
param_set_fn set;           // str -> 변수 값
get 변수의 값 반환 함수를 가져옵니다.
	union {
void *arg;              // Variable pointer
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

`module_param` 라는 매크로는 실제로 전달된 변수에 반영할 수 있는 `kernel_param` 구조체를 설정하는 작업을 수행합니다. 이 구조체에는 변수에 액세스하고 설정하는 데 필요한 정보가 포함되어 있습니다. 이 구조체는 20-24번째 줄에 위치하며 `__param`이라는 섹션에 배치됩니다(`__section__("__param")`). 이 구조체가 설정되면 커널은 모듈을 로드할 때 elf 파일 내 `section __param`의 위치와 구조체 수를 찾은 다음 이름과 `param_set_fn`에 따라 각 매개변수의 값을 설정합니다. 특정 이름의 `section`을 찾는 방법은 플랫폼에 따라 다르며, 리눅스 커널은 elf 파일을 처리하는 방식으로 이를 구현합니다. 리눅스는 elf 파일 정보를 확인하기 위해 `readelf` 지시문을 제공하며, 관심이 있다면 `readelf`의 도움말을 확인할 수 있습니다.

위에서 언급했듯이 Linux 커널의 접근 방식은 플랫폼에 따라 다릅니다. 하지만 저는 플랫폼과 무관한 매개변수 처리 방식을 원합니다. 그래서 우리는 `moduleparam`을 수정하여 '`__section__("__param")` 선언을 제거해야 합니다. 우리는 ELF 파일의 섹션을 복잡하게 다루길 원하지 않으니까요. 수정된 사용법을 살펴보겠습니다:

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

각 반영된 구조를 보존하기 위해, `init_module_param(num)` 매크로를 추가하여 구조를 보존하는 공간을 선언하였다. `num`은 매개변수 개수이며, 실제 선언된 매개변수 개수가 `num`을 초과하면 프로그램은 어설션 오류를 발생시킨다. `module_param`의 선언은 원래 것과 약간 다르며, 접근 권한을 나타내는 마지막 매개변수를 제거하여 권한 제어를 하지 않는다. 또한 `module_param_bool` 매크로가 추가되어 `bool`을 처리하며, 이는 Linux 버전에서는 필요 없는데 gcc 내장 함수 `__builtin_types_compatible_p`를 사용하여 변수 유형을 확인하기 때문이다. 안타깝게도 MSVC는 이 함수를 지원하지 않기 때문에 이 기능을 제거하고 매크로를 추가했다. `module_param_array`와 `module_param_string`은 배열과 문자열을 처리하는 것으로, 이 두 기능은 원래 버전에도 있었다.

매개 변수가 선언되었으니 이제 전달된 매개 변수를 처리해야 합니다. 매크로 `parse_params`를 사용하여 `argc, argv`를 전달하고, 세 번째 매개 변수는 알 수 없는 매개 변수를 처리하는 콜백 함수 포인터입니다. 이를 `NULL`로 전달하면 위치 매개 변수에 도달하면 매개 변수 처리가 중단되고 오류 코드가 반환됩니다.

소스 코드를 컴파일하고 실행하십시오：

```
.\moduleparam_test.exe error=0 test=101 btest=1 latest=1,2,3 strtest=\"Hello World!\"
Parsing ARGS: error=0 test=101 btest=1 latest=1,2,3 strtest="Hello World!"
find unknown param: error
test = 101
btest = Y
latest = 1,2,3
strtest = Hello World!
```

수치, 배열 및 문자열이 모두 올바르게 읽혀들여지고 형식이 변환됨을 볼 수 있습니다. 형식을 변환할 수 없는 매개변수를 만나게 되면, 오류 코드를 반환하고 관련 정보를 출력합니다. 우리는 몇 줄의 코드를 간단히 추가함으로써 매개변수를 읽고 변환하는 처리를 완료할 수 있습니다. 매우 우아하게 사용할 수 있습니다. 더 자세한 구현은 직접 코드를 확인하시기 바랍니다. [여기서 확인하세요](https://github.com/disenone/aparsing)"."

##요약

이번에는 C/C++에서 명령행 인수를 처리하는 세 가지 방법을 요약했습니다. `getenv`, `getopt` 및 `moduleparam` 입니다. 세 가지 방법은 각각의 특징이 있으며, 필요에 따라 실제 요구 사항에 맞는 방법을 선택할 수 있습니다.

`getenv`は、ネイティブでマルチプラットフォームをサポートしているため、直接使用できますが、あまりにも原始的であり、環境変数を使用しており、環境に一定程度の汚染をもたらします。不要な環境変数を削除して前回の設定が残っている汚染を防ぐために、使用前にクリーンアップすることをお勧めします。
`getopt`는 리눅스 플랫폼에서 기본 지원되지만 윈도우를 지원하지 않으므로 이식 가능하게 사용하려면 코드를 포함해야 합니다. 매개변수 전달은 리눅스의 명령 인수 표준을 준수하며 선택적 매개변수를 지원하지만 다소 번거롭게 사용됩니다. 일반적으로 다른 매개변수를 처리하기 위해 반복문과 조건문을 사용하고 숫자 유형의 매개변수 처리가 어렵습니다.
- `moduleparam`는 Linux 커널의 `moduleparam` 구현을 참고하여 만들어진 명령행 인자 처리 도구이며, 여러 플랫폼에서 사용할 수 있고 간단하게 사용할 수 있으며 다양한 유형의 인자에 대해 형변환을 수행할 수 있습니다. 단점은 각 인자마다 해당하는 변수가 필요하다는 것입니다.

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT를 사용하여 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)어떤 미흡한 부분도 지적해 주세요. 
