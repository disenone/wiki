---
layout: post
title: C/C++ 的命令列參數處理總結
categories:
- c++
catalog: true
tags:
- dev
description: 前陣子翻 Linux 內核程式碼的時候看到了內核對模組參數（moduleparam）的處理，覺得挺精妙，讓我不禁想研究下 C 下的命令行參數要怎樣更好地處理。
figures:
- assets/post_assets/2016-11-19-aparsing/aparsing.png
---

<meta property="og:title" content="C/C++ 的命令行参数处理总结" />

![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/gcc-4.9-blue.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/clang-3.7-birghtgreen.svg){:style="display: inline-block"}

![](assets/img/2016-11-19-aparsing/aparsing.png)

前一阵子翻看 Linux 內核程式碼時，看到內核對模組參數 (moduleparam) 的處理，覺得非常精妙，令我不禁想研究一下 C 語言中如何更好地處理命令行參數。本文所用的程式碼都在這裡 [aparsing](https://github.com/disenone/aparsing)程式碼支援在 Windows、Linux、Mac OS X 下編譯運行，詳細的編譯指南在 README.md 裡面。

## getenv

標準庫為我們提供了一個函數 `getenv` ，按照字面意思，這個函數是用來獲取環境變量的，那麼只要我們預先設置好需要的環境變量，在程式裡面拿出來，就間接地把參數傳到程式裡面啦。我們來看下面這段[代碼](https://github.com/disenone/aparsing/blob/master/getenv/getenv_test.c)抱歉，我無法提供翻譯。

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

`getenv` 函數聲明如第 [4](#__codelineno-0-5)傳進你想獲取的變數名稱，回傳該變數的值，如果找不到變數，則回傳0。[10](#__codelineno-0-10)和 [15](#__codelineno-0-15)行就是分别获取兩個環境變量的值，如果變量有效則列印變量值。需要注意的是 `getenv` 返回的都是字串，需要使用者手動轉換數值類型的，所以使用起來不夠方便。編譯運行:

在 Windows 系統下：

``` bat
set GETENV_ADD=abc & set GETENV_NUM=1 & .\getenv_test.exe
```

Linux 下：

``` shell
GETENV_ADD=abc GETENV_NUM=2 ./getenv_test 
```

輸出：

```
GETENV_ADD = abc
GETENV_NUM = 2
```

## getopt

Linux 提供了一組函數 `getopt, getopt_long, getopt_long_only` 來處理傳入的命令列參數，這三個函數的宣告分別為：

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

`getopt` 只能處理短參數（即單字符參數），`getopt_long, getopt_long_only` 則可以處理長參數。詳細的函數解釋可以去翻 Linux 下的手冊，下面我們透過例子來說明 `getopt` 和 `getopt_long` 的用法。

需要注意的是，Windows下並沒有提供這一組函數，因此我找了一份可以在Windows下編譯的源碼，做了一些小改動，代碼都在[這裡](https://github.com/disenone/aparsing/tree/master/getopt)。

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

我們來著重分析 `getopt_long` 的用法，`getopt_long` 的前三個參數跟 `getopt` 是一樣的，分別是：命令行參數個數 `argc`，命令行參數數組 `argv`，短參數具體形式 `optstring`。`optstring` 的格式就是一個個的短參數字符，後面加冒號 `:` 表示帶參數，兩個冒號 `::` 表示可選參數，譬如第 19 行，就是聲明短參數的形式，`b` 參數不帶額外參數，`a` 參數帶額外參數，`c` 帶可選參數。

`getopt_long` 後兩個參數是用來處理長參數的，其中 `option` 的結構是：

```c
struct option {
const char *name;       // 長參數名字
    int         has_arg;    // 是否帶額外參數
int        *flag;       // 設置如何返回函數調用結果
int         val;        // 返回的數值
};
```
雖然說是長參數，但 `name` 還是可以設置為單字符長度的。

`has_arg` 可以設置為 `no_argument, required_argument, optional_argument`，分別表示不帶參數，帶參數，帶可選參數。

`flag` 和 `val` 是配合使用的，如果 `flag = NULL`，`getopt_long` 會直接返回 `val`，否則如果 `flag` 為有效指針，`getopt_long` 會執行類似 `*flag = val` 的操作，把 `flag` 指向的變數設置為 `val` 的數值。

如果 `getopt_long` 找到匹配的短參數，會返回該短參數的字元值，如果找到匹配的長參數，會返回 `val`（`flag = NULL`）或者返回 `0`（`flag != NULL; *flag = val;`）；如果遇到非參數的字元，會返回 `?`；如果所有參數都處理完畢，則返回 `-1`。

利用返回值的特性，我們可以實現用長參數和短參數具有相同效果，例如 `long_options` 的第一個參數 `add`，其 `val` 值設置為短參數的字符 `'a'`，那麼在判斷返回時，`--add` 和 `-a` 會進入相同的處理分支，被當作相同的含義來處理。

拼圖的最後一塊就是 `optind` 和 `optarg` 的用法，`optind` 是下一個待處理參數在 `argv` 中的位置，`optarg` 則指向額外參數字串。

翻譯這段文字為：編譯運行程式碼：

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

`-a` 和 `--add` 的意思是一样的，短參數的選擇性參數直接接在後面，比如 `-c4`，而長參數的選擇性參數需要有等號，比如 `--verbose=3`。

## mobuleparam

好的，終於到達這篇文章最初啟發的主題了，Linux 內核使用了一個非常巧妙的方式來傳遞內核模組的參數，這個方法就是 `moduleparam`。我在這裡先簡單解釋一下 Linux 內核的 `moduleparam` 做法，更詳細的解釋可以參考程式碼。雖然我參考了一些 `moduleparam` 的處理方法，但和 Linux 內核的 `moduleparam` 有一些不同，為了區分，我會把我的方法稱為 `small moduleparam`，Linux 內核的依然稱為 `moduleparam`。

讓我們先來看看`moduleparam`的使用方法，在模組中宣告：

```c
int enable_debug = 0;
module_param(enable_debug, int, 0);
```

然後加載模組時輸入參數：

```shell
$ insmod mod enable_debug=1
```

變量 `enable_debug` 就被正確地設置為 `1`，使用起來很方便，需要增加的代碼也很少，代碼可以寫得很簡短優雅，不用像 `getenv` 和 `getopt` 那樣寫很多循環判斷，而且還自帶類型轉換，所以我看到就想，要是能把這個方法拿來處理命令行參數，那就更好了。

請繼續查看 `moduleparam` 的核心實現：

```cpp linenums="1"
struct kernel_param {
	const char *name;           // 變量名字
u16 perm;                   // 變數存取權限
	u16 標誌;                  // 變量是否 bool 類型
	param_set_fn set;           // 字串 -> 變數值
	param_get_fn get;           // 變數值 -> str
	union {
void *arg;              // 變數指標
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

`module_param` 是一個宏，它實際做的事情是建立了一個可以反射到傳入變量的結構 `kernel_param`，該結構保存了足夠訪問和設置變量的信息，即第 20-24 行，並且把結構放在叫做 `__param` 的 `section` 中（`__section__ ("__param")`）。結構保存好之後，內核會在加載模塊時，找出 elf 文件的 `section __param` 的位置和結構數量，然後根據名字和 `param_set_fn` 分別設置每個參數的數值。找出特定名字 `section` 的方法是平台相關的，Linux 內核實現的是對 elf 文件的處理，Linux 提供了指令 `readelf` 來查看 elf 文件的信息，有興趣的可以查看 `readelf` 的幫助信息。

上面提到 Linux 內核的做法是平台相關的，但我所需的是平台無關的處理參數的方式，因此我們需要修改原始的 `moduleparam` 做法，去掉 `__section__ ("__param")` 的聲明，畢竟我們不想要費事地讀取 elf 檔案的 `section`。讓我們先看看修改後的用法：

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

為了保存每個反射結構，我新增了一個宏`init_module_param(num)`，來聲明保存結構的空間，`num`是參數的個數，如果實際聲明的參數個數超出`num`，程序會觸發斷言錯誤。`module_param`的聲明跟原始的稍有不同，去掉了最後一個表示訪問權限的參數，不做權限的控制。另外新增了宏`module_param_bool`來處理表示`bool`的變量，這在Linux的版本是不需要的，因為它用到了gcc內建函數`__builtin_types_compatible_p`來判斷變量的類型，很遺憾，MSVC是沒有這個函數的，所以我只能把這個功能去掉，增加一個宏。`module_param_array`和`module_param_string`就是對數組和字符串的處理，這兩個功能在原始的版本也是有的。

聲明參數完畢，就是處理傳入的參數了，使用宏 `parse_params`，傳入 `argc, argv`，第三個參數是對未知參數的處理回調函數指針，可以傳 `NULL`，則位置參數會中斷處理參數，返回錯誤碼。

翻譯為繁體中文：

編譯執行程式碼：

```
.\moduleparam_test.exe error=0 test=101 btest=1 latest=1,2,3 strtest=\"Hello World!\"
Parsing ARGS: error=0 test=101 btest=1 latest=1,2,3 strtest="Hello World!"
find unknown param: error
test = 101
btest = Y
latest = 1,2,3
strtest = Hello World!
```

(https://github.com/disenone/aparsing)I'm sorry, but I can't provide a translation for this text as it does not contain any content to be translated.

##總結

這次我們總結了一下 C/C++ 下三種處理命令行參數的方法，分別是 `getenv` 、`getopt` 和 `moduleparam`。三種方法各有其特點，未來如有需要可以根據實際需求來選擇合適的方法：

`getenv` 是原生多平台就支持的，可以直接使用，但也過於原始，並使用的是環境變數，對環境有一定的汙染，每次使用前最好清除不必要的環境變數防止上次的設定存留汙染
`getopt` 在 Linux 平台內建支援，但在 Windows 平台則不被支援，因此需要包含自己的程式碼才能跨平台使用。參數的傳遞符合 Linux 的指令參數標準，支援選擇性參數，但使用起來稍微複雜，通常需要迴圈和條件判斷來處理不同的參數，並且對數值類型的參數不友善。
`moduleparam` 是參考 Linux 核心的 `moduleparam` 實現的命令行參數處理工具，支持跨平台使用，使用簡單，能對不同類型的參數進行類型轉換，缺點就是每個參數都需要一個相應的變量存儲。

--8<-- "footer_tc.md"


> 此貼文是由 ChatGPT 翻譯的，如有 [**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
