---
layout: post
title: C/C++のコマンドライン引数の処理についてまとめました。
categories:
- c++
catalog: true
tags:
- dev
description: 前一陣子翻 Linux 內核碼的時候看到了內核對模組參數 (moduleparam) 的處理，覺得挺精妙，讓我不禁想研究下 C 下的命令行參數要怎樣更好地處理。
figures:
- assets/post_assets/2016-11-19-aparsing/aparsing.png
---

<meta property="og:title" content="C/C++ 的命令行参数处理总结" />

![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/gcc-4.9-blue.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/clang-3.7-birghtgreen.svg){:style="display: inline-block"}

![](assets/img/2016-11-19-aparsing/aparsing.png)

最近、Linux カーネルのコードを見ていたときに、モジュールパラメータ（moduleparam）の処理について面白いものを発見しました。その仕組みはなかなか優れていると感じ、さらに C 言語でのコマンドライン引数の取り扱いについても探求してみたくなりました。本文で使用したコードはこちらにあります [aparsing](https://github.com/disenone/aparsing)Windows、Linux、Mac OS Xでコンパイルおよび実行するためのコードサポートが提供されており、詳細なコンパイルガイドはREADME.mdに記載されています。

## getenv

(https://github.com/disenone/aparsing/blob/master/getenv/getenv_test.c)I'm sorry, but there is no text for me to translate into Japanese.

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

「getenv」関数の宣言は第[4](#__codelineno-0-5)指定した変数名を取得して、その値を返します。変数が見つからない場合は、0を返します。[10](#__codelineno-0-10)和 [15](#__codelineno-0-15)`行` とは、2つの環境変数の値を取得することを意味します。変数が有効であれば、その値を出力します。 `getenv` が返すすべては文字列であり、数値型に手動で変換する必要があることに注意してください。そのため、使い勝手があまりよくありません。コンパイルして実行してください。

Windows 下：

``` bat
set GETENV_ADD=abc & set GETENV_NUM=1 & .\getenv_test.exe
```

リナックス 下：

``` shell
GETENV_ADD=abc GETENV_NUM=2 ./getenv_test 
```

出力：

```
GETENV_ADD = abc
GETENV_NUM = 2
```

## getopt

Linux has provided us with a set of functions `getopt, getopt_long, getopt_long_only` to handle the command-line arguments passed into the program. The declarations of these three functions are:

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

`getopt`関数は短い引数（つまり1文字の引数）のみを処理できます。一方、`getopt_long`と`getopt_long_only`関数は長い引数も処理できます。関数の詳細についてはLinuxのマニュアルを参照してください。以下では、`getopt`と`getopt_long`の使い方を例を通じて説明します。

(https://github.com/disenone/aparsing/tree/master/getopt)I apologize, but I cannot provide a translation for single punctuation marks or characters. If you have more text to translate, please provide it. Thank you for your understanding.

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

`getopt_long` の使い方に焦点を当てて分析してみましょう。`getopt_long` の最初の3つの引数は、`getopt` と同じです。それぞれ、コマンドライン引数の数である `argc`、コマンドライン引数の配列 `argv`、短いオプションの具体的な形式を示す `optstring` です。`optstring` の形式は、短いオプション文字を一つずつ並べ、その後にコロン `:` を付け加えることで、引数を伴うことを示し、二つのコロン `::` を付け加えることで、オプションの引数が省略可能であることを示します。例えば、19行目では、短いオプションの形式を宣言しており、`b` オプションは追加の引数を取らず、`a` オプションは追加の引数を取り、`c` オプションはオプションの引数が省略可能であることを表します。

`getopt_long` functionのlast two argumentsは、longオプションを処理するためのもので、`option`構造体は以下のようになります：

```c
struct option {
const char *name;       // 長いパラメータ名
int has_arg; // Whether to have additional arguments
int *flag; // 関数呼び出し結果を返す方法を設定
int val;        // Returned numerical value
};
```
長い引数と言っても、 `name` は1文字の長さに設定できます。

`has_arg` can be set to `no_argument, required_argument, optional_argument`, which respectively indicate no argument, required argument, optional argument.

`flag` 和 `val` 是一起使用的，如果 `flag = NULL`，`getopt_long` 将直接返回 `val`，否则如果 `flag` 是有效指针，`getopt_long` 将执行类似 `*flag = val` 的操作，将 `flag` 指向的变量设为 `val` 的值。

`getopt_long` が短い引数と一致する場合、その引数の文字値が返され、一致する長い引数が見つかると `val`（ `flag=NULL`）または` 0`が返されます（ `flag != NULL; *flag = val;`）。 引数以外の文字に遭遇すると `?` が返され、すべての引数が処理された後に `-1` が返されます。

返り値の特性を活用することで、長いオプションと短いオプションの意味が同じになるような効果を実現できます。例えば、`long_options`の最初の引数を`add`とし、`val`の値を短いオプションの文字`'a'`に設定すると、`--add`と`-a`の判断では、同じ処理枝に入り、同じ意味として処理されることになります。

最後のピースとなるのは、`optind`と`optarg`の使い方です。`optind`は次に処理される引数の`argv`内での位置を示し、`optarg`は追加の引数文字列を指します。

コードをコンパイルして実行します：

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

`-a` と `--add` は同じ意味です。短いパラメータのオプション引数は直接後に続けて記述します。例えば、`-c4` のようにです。一方、長いパラメータのオプション引数は等号を使用して指定します。例えば、`--verbose=3` のようにです。

## mobuleparam

ok、最初にこの記事を引き起こした方法に到達しました。Linuxカーネルは、カーネルモジュールにパラメータを渡すために非常に巧妙な方法を取りました、それが `moduleparam` です。ここではまず、Linuxカーネルの `moduleparam` の方法を簡単に説明しますが、詳細な説明はコードを参照してください。私は一部 `moduleparam` の処理方法を借用しましたが、それとLinuxカーネルの `moduleparam` にはいくつかの違いがあります。区別するため、私の方法を `small moduleparam` と呼び、Linuxカーネルのものは引き続き `moduleparam` と呼びます。

まずは、`moduleparam`の使用方法を見てみましょう。モジュール内で宣言します：

```c
int enable_debug = 0;
module_param(enable_debug, int, 0);
```

その後、モジュールをロードする際に入力パラメータを指定してください：

```shell
$ insmod mod enable_debug=1
```

変数 `enable_debug` が正しく `1` に設定されると、利用しやすく、追加するコードも少なく、コードを短くエレガントに書くことができます。`getenv` や `getopt` のように多くのループ判定を書く必要はありませんし、型変換も自動で行われるので、この方法を使ってコマンドライン引数を処理できればなお良いと感じました。

`moduleparam` のコア実装を見てみましょう：

```cpp linenums="1"
struct kernel_param {
const char *name; の翻訳は以下の通りです：

const char *name;           // 変数名
u16 perm;                   // Variable access permission
u16 flags;                  // Whether the variable is of bool type.
param_set_fn set;           // str -> variable value
param_get_fn get;           // Retrieve variable value and convert it to a string.
	union {
変数ポインタ、void *arg;
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

`module_param` はマクロであり、実際に行われることは、受け取った変数に反映できる `kernel_param` 構造体を構築することです。この構造体は、変数にアクセスして設定するための十分な情報を保持しています、具体的には、20-24行目で、そして構造体を `__param` という名前の `section` に配置します（`__section__("__param")`）。構造体が保存された後、カーネルはモジュールを読み込む際に、elfファイル内の `section __param` の場所と構造の数を特定し、名前と `param_set_fn` に基づいて各パラメータの値を設定します。特定の名前の `section` を見つける方法はプラットフォームに依存しており、Linuxカーネルの実装ではelfファイルの処理が行われます。Linuxはelfファイルの情報を表示するための `readelf` 命令を提供しており、興味のある方は `readelf` のヘルプ情報をご覧いただけます。

「Linuxカーネルのアプローチはプラットフォームに依存していると言っていましたが、私はプラットフォームに依存しないパラメータ処理方法が欲しいので、元の`moduleparam`のアプローチを変更する必要があります。`__section__("__param")`の宣言を削除してみましょう。要するに、elfファイルの`section`を手間暇かけて読み取りたくありません。では、変更後の使い方を見てみましょう。」

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

それでは、すべての構造体を保存するために、 `init_module_param(num)` というマクロを追加しました。これにより、構造体の保存スペースを宣言します。 `num` はパラメータの数で、宣言されたパラメータの数が `num` を超えると、プログラムはアサーションエラーを発生させます。`module_param` の宣言はわずかに元の宣言と異なり、アクセス権を表す最後のパラメータが削除され、アクセス権の制御は行われません。さらに、 `module_param_bool` というマクロが追加され、 `bool` を表す変数を扱いますが、これはLinuxのバージョンでは必要ありません。なぜなら、それは変数のタイプを判断するためにgccのビルトイン関数 `__builtin_types_compatible_p` を使用しているからです。残念ながら、MSVCにはこの関数がないので、この機能を削除し、マクロを追加しました。`module_param_array` および `module_param_string` は配列と文字列を処理するためのもので、これらの機能は元のバージョンでも使用されています。

引数の宣言が完了したら、次は受け取った引数を処理することです。`parse_params` マクロを使用して、`argc, argv` を渡します。第3引数は未知の引数を処理するコールバック関数のポインタであり、`NULL` を渡すこともできます。これにより、位置引数に入力された場合に引数処理が中断され、エラーコードが返されます。

コードをコンパイルして実行します：

```
.\moduleparam_test.exe error=0 test=101 btest=1 latest=1,2,3 strtest=\"Hello World!\"
Parsing ARGS: error=0 test=101 btest=1 latest=1,2,3 strtest="Hello World!"
find unknown param: error
test = 101
btest = Y
latest = 1,2,3
strtest = Hello World!
```

数値、配列、文字列が正しく読み込まれ、形式が変換されることが分かります。形式を変換できないパラメータがある場合、エラーコードが返され、関連情報が出力されます。数行のコードを追加するだけで、パラメータの読み込みと変換処理を簡単に完了でき、スマートに使用できます。詳細な実装はコードを直接確認してください。[こちら](https://github.com/disenone/aparsing)I'm sorry, but the text you provided is not clear and cannot be translated.

##要求的日语翻译：“概括”

今回は、C/C++ でコマンドライン引数を処理する3つの方法についてまとめました。それぞれ、`getenv`、`getopt`、`moduleparam`という方法です。これら3つの方法にはそれぞれ特長があり、将来必要に応じて適切な方法を選択できます。

`getenv`はネイティブでマルチプラットフォームをサポートしており、直接使用することができますが、やや原始的すぎる場合があり、環境変数を使用しているため、環境に一定程度の影響を与えます。使用する前には不要な環境変数をクリアして、前回の設定が残っているのを防ぐことが望ましいです。
`getopt`はLinuxプラットフォームでネイティブにサポートされており、Windowsではサポートされていないため、クロスプラットフォームで使用するには実装コードを含める必要があります。パラメータの渡し方はLinuxのコマンドライン引数の標準に準拠しており、オプションパラメータをサポートしていますが、使い方は少々面倒であり、通常、異なるパラメータを処理するためにループや条件分岐が必要であり、数値型のパラメータには対応していません。
- `moduleparam` は Linux カーネルの `moduleparam` の実装を参考にしたコマンドラインパラメータ処理ツールで、クロスプラットフォームで使用可能で、使いやすく、異なるタイプのパラメータを型変換できますが、欠点は各パラメータに対応する変数が必要です。

--8<-- "footer_ja.md"


> この投稿はChatGPTによって翻訳されました。[**反馈**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。 
