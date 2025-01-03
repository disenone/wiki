---
layout: post
title: C/C++ 的命令行參數處理總結
categories:
- c++
catalog: true
tags:
- dev
description: 前一陣子翻 Linux 內核程式碼的時候看到了內核對模組參數 (moduleparam) 的處理，覺得挺精妙，讓我不禁想研究下 C 下的命令行參數要怎樣更好地處理。
figures:
- assets/post_assets/2016-11-19-aparsing/aparsing.png
---

<meta property="og:title" content="C/C++ 的命令行参数处理总结" />

![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/gcc-4.9-blue.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/clang-3.7-birghtgreen.svg){:style="display: inline-block"}

![](assets/img/2016-11-19-aparsing/aparsing.png)

最近閱讀 Linux 內核程式碼時，看到內核處理模組參數（moduleparam）的方式很巧妙，讓我忍不住想深入研究如何更好地處理 C 語言的命令列參數。該文章中所使用的所有程式碼都在這裡[aparsing](https://github.com/disenone/aparsing)代碼支援在 Windows、Linux、Mac OS X 下編譯運行，詳細的編譯指南在 README.md 裡面。

## getenv

標準庫為我們提供了一個函數 `getenv` ，按照字面意思，這個函數是用來獲取環境變量的，那麼只要我們預先設定好需要的環境變量，在程序裡面拿出來，就間接地把參數傳到程序裡面啦。我們來看下面這段[代碼](https://github.com/disenone/aparsing/blob/master/getenv/getenv_test.c)對不起，請提供需要翻譯的文本。

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

`getenv` 函式宣告如第 [4](#__codelineno-0-5)請傳入欲取得之變數名稱，將回傳該變數的數值，若未找到該變數，則將回傳 0。[10](#__codelineno-0-10)和 [15](#__codelineno-0-15)行為獲取兩個環境變數值並分別打印它們，如果變數有效。請注意 `getenv` 返回的是字串，需要使用者手動轉換數值類型，所以使用起來並不十分方便。進行編譯和運行：

在Windows操作系统中：

``` bat
set GETENV_ADD=abc & set GETENV_NUM=1 & .\getenv_test.exe
```

Linux 平臺下：

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

需要注意的是，Windows 下沒有提供這一組功能，因此我找到了一份可以在 Windows 下編譯的源碼，做了一些微小的修改，程式碼都在[這裡](https://github.com/disenone/aparsing/tree/master/getopt)這些文字翻譯成繁體中文：

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

我們專注分析 `getopt_long` 的用法，`getopt_long` 的前三個參數跟 `getopt` 是一樣的，分別是：命令行參數個數 `argc`，命令行參數陣列 `argv`，短參數具體形式 `optstring`。`optstring` 的格式就是一個個的短參數字元，後面加冒號 `:` 表示帶參數，兩個冒號 `::` 表示可選參數，譬如第 19 行，就是宣告短參數的形式，`b` 參數不帶額外參數， `a` 參數帶額外參數，`c` 帶可選參數。

`getopt_long` 函式的最後兩個參數是用來處理長選項的，其中 `option` 結構的定義如下：

```c
struct option {
const char *name;       // 長參數名稱
int has_arg; // 是否有附加參數
int *flag;       // 設置如何返回函數調用結果
    
    int         val;        // 返回的數值
};
```
雖然長度參數是長的，但 `name` 還是可以設置為單個字符的。

`has_arg` 可以設置為 `no_argument, required_argument, optional_argument`，分別表示不帶參數，帶參數，帶可選參數。

`flag` 和 `val` 是用來搭配的，如果 `flag = NULL`，`getopt_long` 會直接返回 `val`，否則如果 `flag` 為有效指標，`getopt_long` 會執行類似 `*flag = val` 的操作，將 `flag` 指向的變數設置為 `val` 的數值。

如果 `getopt_long` 找到匹配的短參數，會返回該短參數的字符值，如果找到匹配的長參數，會返回 `val`（`flag = NULL`）或者返回 `0`（`flag != NULL; *flag = val;`）；如果遇到非參數的字符，會返回 `?`；如果所有參數都處理完畢，則返回 `-1`。

透過返回值的特性，我們可以實現長參數和短參數具有相同意義的效果，例如 `long_options` 的第一個參數 `add`，將其 `val` 值設置為短參數的字符 `'a'`，這樣在判斷返回時，`--add` 和 `-a` 會進入相同的處理分支，被視為具有相同的意義進行處理。

拼圖的最後一塊就是 `optind` 和 `optarg` 的用法，`optind` 是下一個待處理參數在 `argv` 中的位置，`optarg` 則指向額外參數字串。

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

`-a` 和 `--add` 的意思是一样的，短參數的可選參數直接跟在後面，例如 `-c4`，而長參數的可選參數需要有等號，例如 `--verbose=3`。

## mobuleparam

好的，終於到達引發這篇文章的方法了，Linux 內核使用了一種非常巧妙的方式來傳遞內核模塊的參數，這個方法就是 `moduleparam`。我先在這裡簡單解釋一下 Linux 內核的 `moduleparam` 的做法，更詳細的解釋可以參考程式碼。雖然我參考了一些 `moduleparam` 的處理方法，但與 Linux 內核的 `moduleparam` 有一些不同，為了區分，我會將我的方法稱為 `small moduleparam`，Linux 內核的依然稱為 `moduleparam`。

先來看看 `moduleparam` 的用法，在模塊裡面宣告：

```c
int enable_debug = 0;
module_param(enable_debug, int, 0);
```

請輸入參數以加載模組：

```shell
$ insmod mod enable_debug=1
```

變數 `enable_debug` 就被正確地設置為 `1`，使用起來很方便，需要增加的程式碼也很少，程式碼可以寫得很簡短優雅，不用像 `getenv` 和 `getopt` 那樣寫很多迴圈判斷，而且還自帶類型轉換，所以我看到就想，要是能把這個方法拿來處理命令行參數，那就更好了。

接下來讓我們看一下 `moduleparam` 的核心實現：

```cpp linenums="1"
struct kernel_param {
const char *name;           // 變數名稱
u16 perm;                   // Variable access permission
`u16 flags;                  // Variable indicating whether it is of type bool`
param_set_fn set;           // str -> 變量值
param_get_fn get;           // 將變量轉換為字串
	union {
void *arg;              // 變量指標
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

`module_param` 是一個巨集，它的實際作用是建立了一個能夠映射到傳入變數的結構 `kernel_param`。這個結構保存了足夠訪問和設置變數的信息，即第 20-24 行，並且將結構放在一個名為 `__param` 的 `section` 中（ `__section__ ("__param")` ）。結構保存完畢後，內核在加載模塊時，會找出 elf 檔案中 `section __param` 的位置和結構數量，再根據名字和 `param_set_fn` 分別設置每個參數的數值。找出特定名字 `section` 的方法是平台相關的，Linux 內核實現的是對 elf 檔案的處理，Linux 提供了指令 `readelf` 來查看 elf 檔案的信息，有興趣的可以查看 `readelf` 的幫助訊息。

上面提到 Linux 內核的作法是平台相關的，而我想要的是平台無關的處理參數的方法，所以我們需要修改原始的 `moduleparam` 作法，刪除 `__section__("__param")` 的宣告，畢竟我們並不想要去麻煩地讀取 elf 檔案的 `section`。現在來看看修改後的用法：

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

為了保存每個設定的結構，我新增了一個巨集 `init_module_param(num)`，來宣告存放結構的空間，`num` 是參數的數量，如果實際宣告的參數數量超過 `num`，程式會觸發斷言錯誤。`module_param` 的宣告跟原始的略有不同，去掉了最後一個表示訪問權限的參數，不做權限的控制。另外新增了巨集 `module_param_bool` 來處理表示 `bool` 的變數，這在 Linux 的版本是不需要的，因為它使用了 gcc 內建函數 `__builtin_types_compatible_p` 來判斷變數的類型，很遺憾，MSVC 是沒有這個函數的，所以我只能將此功能移除，並增加一個巨集。`module_param_array` 和 `module_param_string` 就是對陣列和字串的處理，這兩個功能在原始版本中也有。

聲明參數完畢，接下來就是處理傳入的參數了，使用宏 `parse_params`，將 `argc, argv` 傳入，第 3 個參數是對未知參數的處理回調函數指針，可以傳入 `NULL`，這樣未知參數的位置將中斷處理，並返回錯誤碼。

編譯運行程式碼：

```
.\moduleparam_test.exe error=0 test=101 btest=1 latest=1,2,3 strtest=\"Hello World!\"
Parsing ARGS: error=0 test=101 btest=1 latest=1,2,3 strtest="Hello World!"
find unknown param: error
test = 101
btest = Y
latest = 1,2,3
strtest = Hello World!
```

可以看到數值，陣列和字串都能正確讀入並轉換格式，如果遇到不能轉換格式的參數，會返回錯誤碼並列印相關信息。我們可以很簡單地添加幾行程式碼，就完成參數的讀入和轉換處理，使用起來非常優雅。更詳細的實現可以直接看程式碼，[在這裡](https://github.com/disenone/aparsing)。

##總結

這次我們總結了一下 C/C++ 下三種處理命令行參數的方法，分別是 `getenv` ，`getopt` 和 `moduleparam`。三種方法有各自的特點，以後有需要可以根據實際的需求來選擇合適的方法：

`getenv` 是原生多平台就支持的，可以直接使用，但也過於原始，並使用的是環境變量，對環境有一定的污染，每次使用前最好清除不必要的環境變量防止上次的設置存留污染
`getopt` 在 Linux 平台的支援是原生的，但 Windows 無法支援。因此要跨平台使用，需要加入自行實作的程式碼。參數的傳遞符合 Linux 的指令傳遞標準，支持選擇性參數，但實際操作稍微複雜，通常需要透過迴圈和條件判斷來處理不同的參數，對於數值型態的參數則不夠友善。
`moduleparam` 是參考 Linux 內核的 `moduleparam` 實現的命令列參數處理工具，支持跨平台使用，操作容易，能針對不同類型的參數進行類型轉換，不足之處在於每個參數都需要一個相應的變量來存儲。

--8<-- "footer_tc.md"


> 此篇文章是由ChatGPT進行翻譯的，如有[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
