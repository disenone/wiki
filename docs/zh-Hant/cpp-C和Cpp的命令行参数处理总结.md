---
layout: post
title: C/C++ 的命令列參數處理總結
categories:
- c++
catalog: true
tags:
- dev
description: 前一陣子翻 Linux 內核碼的時候看到了內核對模組參數（moduleparam）的處理，覺得挺精妙，讓我不禁想研究下 C 下的命令行參數要怎樣更好地處理。
figures:
- assets/post_assets/2016-11-19-aparsing/aparsing.png
---

<meta property="og:title" content="C/C++ 的命令行参数处理总结" />

![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/gcc-4.9-blue.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/clang-3.7-birghtgreen.svg){:style="display: inline-block"}

![](assets/img/2016-11-19-aparsing/aparsing.png)

最近看了一些 Linux 內核程式碼，發現內核是如何處理模組參數(moduleparam)的，覺得非常巧妙，讓我忍不住想深入研究如何更有效地處理 C 語言下的命令列參數。本文所使用的程式碼都在這裡[aparsing](https://github.com/disenone/aparsing)代碼支持在 Windows、Linux、Mac OS X 下編譯運行，詳細的編譯指南在 README.md 裡面。

## getenv

標準庫為我們提供了一個函數 `getenv` ，按照字面意思，這個函數是用來獲取環境變量的，那麼只要我們預先設置好需要的環境變量，在程序裡面拿出來，就間接地把參數傳到程序裡面啦。我們來看下面這段[程式碼](https://github.com/disenone/aparsing/blob/master/getenv/getenv_test.c)抱歉，無法翻譯沒有任何文字內容的指示。請提供需要翻譯的具體內容或詢問。感謝理解。

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

`getenv` 函數聲明如第 [4](#__codelineno-0-5)請传入欲獲取之變數名稱，將傳回該變數的值，若未找到變數則返回0。[10](#__codelineno-0-10)(#__codelineno-0-15)行動就是從兩個環境變數中取得值，若變數有效則列印其值。需注意 `getenv` 返回的皆為字串，使用者需手動轉換數值類型，因此使用起來不夠便利。請編譯並執行：

在Windows系統下：

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

Linux 提供了一組函數 `getopt, getopt_long, getopt_long_only` 來處理從命令列傳入的參數，這三個函數的宣告分別是：

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

`getopt` 只能處理短參數（即單字符參數），`getopt_long`、`getopt_long_only` 則可以處理長參數。詳細的函數解釋請參考 Linux 下的手冊。以下我們將透過範例來說明 `getopt` 和 `getopt_long` 的使用方式。

需要注意的是，Windows下並沒有提供這組函數，所以我找到了一份在Windows下編譯的原始碼，稍微修改了一下，程式碼都在[這裡](https://github.com/disenone/aparsing/tree/master/getopt)I'm sorry, but I can't translate the characters "。" as they do not contain any meaningful content. If you have any other text you would like me to translate, please feel free to provide it.

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

我們專注討論 `getopt_long` 的用法，`getopt_long` 的前三個參數與 `getopt` 相同，分別為：命令列參數數量 `argc`，命令列參數陣列 `argv`，短參數具體格式 `optstring`。`optstring` 的格式就是一個個短參數字元，後面加上冒號 `:` 表示帶參數，兩個冒號 `::` 表示可選參數，例如第 19 行，宣告了短參數的形式，`b` 參數沒有額外參數，`a` 參數有額外參數，`c` 則是可選參數。

`getopt_long` 的後兩個參數用於處理長選項，其中 `option` 結構如下：

```c
struct option {
const char *name;       // 長參數名稱
int         has_arg;    // Whether to have additional parameters
int *flag；// 設置如何返回函數調用結果
int         val;        // 返回的数值
};
```
雖然這是長參數，但 `name` 還是可以設置為單字符長度的。

`has_arg` 可以設置為 `no_argument, required_argument, optional_argument`，分別表示不帶參數，帶參數，帶可選參數。

`flag` 和 `val` 是一對應用的變數，如果 `flag = NULL`，`getopt_long` 會直接返回 `val` ，否則如果 `flag` 為有效指標，`getopt_long` 會執行類似 `*flag = val` 的操作，將 `flag` 指向的變數設定為 `val` 的數值。

如果 `getopt_long` 找到匹配的短參數，會返回該短參數的字元值，如果找到匹配的長參數，會返回 `val`（ `flag = NULL` ）或者返回 `0` （ `flag != NULL; *flag = val;` ）；如果遇到非參數的字元，會返回 `?`；如果所有參數都處理完畢，則返回 `-1` 。

利用返回值的特性，我們可以將長參數與短參數的含義做成相同的效果，比如 `long_options` 的第一個參數 `add`，其 `val` 值設置為短參數的字符 `'a'`，這樣判斷返回時，`--add` 和 `-a` 會進入相同的處理分支，被當作相同的含義來處理了。

拼圖的最後一塊就是 `optind` 和 `optarg` 的用法，`optind` 是下一個待處理參數在 `argv` 中的位置， `optarg` 則指向額外參數字串。

編譯運行程式碼：

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

`-a` 和 `--add` 的含意相同，短參數的選擇性參數直接跟在後面，例如 `-c4`，而長參數的選擇性參數需要有等號，例如 `--verbose=3`。

## mobuleparam

好的，終於來到最初引發這篇文章的方法。Linux 內核用了一種非常巧妙的方式來給內核模組傳遞參數，這個方式就是 `moduleparam`。我在這裡先簡單解釋一下 Linux 內核的 `moduleparam` 做法，更詳細的解釋可以參考原始碼。雖然我借鑑了一些 `moduleparam` 的處理方式，但和 Linux 內核的 `moduleparam` 有一些不同。為了區分，我會把我的方法稱做 `small moduleparam`，Linux 內核的依然稱為 `moduleparam`。

請看一下 `moduleparam` 的用法，在模組中宣告：

```c
int enable_debug = 0;
module_param(enable_debug, int, 0);
```

請輸入以下參數以加載模組：

```shell
$ insmod mod enable_debug=1
```

變數 `enable_debug` 就被正確地設置為 `1`，使用起來很方便，需要增加的程式碼也很少，程式碼可以寫得很簡短優雅，不用像 `getenv` 和 `getopt` 那樣寫很多迴圈判斷，而且還自帶類型轉換，所以我看到就想，要是能把這個方法拿來處理命令行參數，那就更好了。

繼續看看 `moduleparam` 的核心實作方式：

```cpp linenums="1"
struct kernel_param {
名稱為常量字符指針； // 變數名稱
u16 perm;                   // Variable access permission
u16 flags;                  // 變數是否 bool 型別
param_set_fn set;           // str -> 變數值
param_get_fn get;           // 取得變數值 -> 字串
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

`module_param` 是一個巨集，實際上建立了一個可以反映到傳入變數的結構 `kernel_param`，該結構保存了足夠存取和設置變數的信息，即第 20-24 行，並且把結構放在名為 `__param` 的 `section` 中（`__section__("__param")`）。結構保存好之後，內核會在加載模組時，找出 elf 檔案的 `section __param` 的位置和結構數量，再根據名字和 `param_set_fn` 分別設置每個參數的數值。找出特定名字 `section` 的方法是平台相關的，Linux 內核實現的是對 elf 檔案的處理，Linux 提供了指令 `readelf` 來查看 elf 檔案的信息，有興趣的人可以查看 `readelf` 的幫助資訊。

上述提及Linux核心採取的方法是與平台相關的，而我需要的是與平台無關的處理參數的方式，因此我們需要對原始的 `moduleparam` 方法做一些修改，將 `__section__("__param")` 聲明移除，畢竟我們並不想要費事地讀取 elf 文件的 `section` 。現在讓我們來看一下修改後的用法：

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

為了保存每個反射結構，我增加了一個宏 `init_module_param(num)`，用來聲明儲存結構的空間，`num` 是參數的個數，如果實際聲明的參數個數超出 `num`，程序會觸發斷言錯誤。`module_param`的聲明稍有不同，刪除了最後一個表示訪問權限的參數，不做權限控制。此外，新增了宏 `module_param_bool` 來處理表示 `bool` 變量，在 Linux 版本中是不需要的，因為它使用了 gcc 內建函數 `__builtin_types_compatible_p` 來判斷變量類型。遺憾的是，在MSVC中沒有這個函數，因此我不得不去掉這個功能，並增加一個宏。`module_param_array` 和 `module_param_string` 則是針對數組和字符串的處理，這兩個功能在原始版本中也是存在的。

宣告參數結束，現在要處理傳入的參數了，使用巨集 `parse_params`，將 `argc, argv` 當作參數傳入，第三個參數是處理未知參數的回調函數指標，可傳入 `NULL`，這樣遇到位置參數會中斷處理參數並返回錯誤碼。

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

您可以看到數值、陣列和字串都能正確讀取並轉換格式。如果遇到無法轉換格式的參數，系統會回傳錯誤碼並列印相關資訊。只需簡單添加幾行程式碼，便能完成參數的讀取和轉換處理，操作起來非常優雅。更詳細的實作內容可以直接參考程式碼，[在這裡](https://github.com/disenone/aparsing)譯文：。

##總結

這次我們總結了一下 C/C++ 下三種處理命令行參數的方法，分別是 `getenv`，`getopt`和`moduleparam`。三種方法有各自的特點，以後有需要可以根據實際的需求來選擇合適的方法：

`getenv` 是原生多平台就支持的，可以直接使用，但也過於原始，並使用的是環境變數，對環境有一定的污染，每次使用前最好清除不必要的環境變數防止上次的設置存留污染。
`getopt`是Linux平台原生支援的，Windows不支援，所以需要包含實現的程式碼才能跨平台使用。參數的傳遞符合Linux的指令參數標準，支援可選參數，但使用起來略微麻煩，通常需要迴圈和條件判斷來處理不同的參數，並對數值類型的參數不友好。
`moduleparam` 是參考 Linux 內核的 `moduleparam` 實現的命令行參數處理工具，支持跨平台使用，操作簡單，可將不同類型的參數進行類型轉換，缺點在於每個參數都需要對應的變數儲存。

--8<-- "footer_tc.md"


> 此帖文乃透過 ChatGPT 翻譯完成，如有[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
