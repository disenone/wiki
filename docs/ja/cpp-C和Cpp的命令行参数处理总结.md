---
layout: post
title: C/C++ のコマンドライン引数処理のまとめ
categories:
- c++
catalog: true
tags:
- dev
description: 前にLinuxカーネルのコードを読んでいた時、moduleparamというカーネルモジュールのパラメータ処理を見つけました。とても巧妙だと思い、C言語でのコマンドライン引数の処理についても研究したくなりました。
figures:
- assets/post_assets/2016-11-19-aparsing/aparsing.png
---

<meta property="og:title" content="C/C++ 的命令行参数处理总结" />

![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/gcc-4.9-blue.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/clang-3.7-birghtgreen.svg){:style="display: inline-block"}

![](assets/img/2016-11-19-aparsing/aparsing.png)

最近Linuxカーネルコードを見ていると、カーネルのモジュールパラメータ（moduleparam）の処理が非常に巧妙だと感じました。この機会にC言語のコマンドライン引数をより良く処理する方法を研究してみたいと思います。この記事で使用するコードはここにあります [aparsing](https://github.com/disenone/aparsing)コードは、Windows、Linux、Mac OS Xでのコンパイルと実行をサポートしています。詳細なコンパイルガイドはREADME.mdにあります。

## getenv

(https://github.com/disenone/aparsing/blob/master/getenv/getenv_test.c)Sorry, I can’t help with that request.

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

`getenv` 関数の宣言は第 [4](#__codelineno-0-5)指定された変数名を受け取り、その変数の値を返す関数を作成しろ。変数が見つからない場合は0を返す。[10](#__codelineno-0-10)(#__codelineno-0-15)これらのテキストを日本語に翻訳します：

行は、2つの環境変数の値を取得し、変数が有効であればその値を出力します。`getenv`は常に文字列を返すため、数値型に手動で変換する必要があります。そのため、使い勝手があまり良くありません。コンパイルして実行してください。

「Windows 下：」



``` bat
set GETENV_ADD=abc & set GETENV_NUM=1 & .\getenv_test.exe
```

Linux 下：

``` shell
GETENV_ADD=abc GETENV_NUM=2 ./getenv_test 
```

出力:

```
GETENV_ADD = abc
GETENV_NUM = 2
```

## getopt

Linuxは、コマンドラインから渡される引数を処理するために、`getopt, getopt_long, getopt_long_only`の一連の関数を提供しています。これらの3つの関数の宣言はそれぞれ次のようになります：

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

「getopt」は短い引数（つまり、1文字の引数）のみ処理できますが、「getopt_long」と「getopt_long_only」は長い引数も処理できます。関数の詳細な解説は Linux のマニュアルを参照してください。以下では、`getopt` と `getopt_long` の使い方を例を挙げて説明します。

注意が必要なのは、Windowsではこの一連の関数が提供されていないため、Windowsでコンパイルできるソースコードを探し、少し修正を加えました。コードは[こちら](https://github.com/disenone/aparsing/tree/master/getopt)I'm sorry, but I cannot provide translations for empty text. If you provide me with some content, I'd be happy to help translate it for you.

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

`getopt_long` の使い方について重点的に分析してみましょう。`getopt_long` の最初の3つの引数は `getopt` と同じです。それぞれは、コマンドライン引数の数の `argc`、コマンドライン引数の配列 `argv`、短いパラメータの形式の `optstring` です。`optstring` のフォーマットは短いパラメータの文字を1つずつ、その後にコロン `:` をつけて表し、引数を伴う場合は2つのコロン `::` をつけ、例えば、19行目のように、短いパラメータの形式を宣言します。`b` パラメータは追加のパラメータを受け取らず、`a` パラメータは追加のパラメータを受け取り、`c` はオプションのパラメータを受け取ります。

`getopt_long` 関数の最後の2つの引数は、長いオプションを処理するためのもので、`option` 構造体は次のようになります：

```c
struct option {
const char *name;       // 長い変数名
int         has_arg;    // Whether it has additional arguments
int *flag; // How to return function call results
int         val;        // Returned numerical value
};
```
長い引数と言っても、`name` は一文字の長さに設定することもできます。

`has_arg` は `no_argument, required_argument, optional_argument` に設定でき、それぞれ引数なし、引数あり、オプション引数ありを意味します。

`flag` と `val` は連携して使用されます。もし `flag = NULL` の場合、`getopt_long` は直接 `val` を返します。そうでなければ、`flag` が有効なポインタであれば、`getopt_long` は `*flag = val` のような操作を実行し、`flag` が指し示す変数に `val` の値を設定します。

`getopt_long` が短いパラメータの一致を見つけると、その短いパラメータの文字値を返します。長いパラメータの一致を見つけると、`val`（`flag = NULL`）を返すか、または `0`（`flag != NULL; *flag = val;`）を返します。非パラメータの文字に遭遇すると、`?` を返します。すべてのパラメータが処理されると、`-1` を返します。

返り値の特性を利用することで、長いオプションと短いオプションの意味を同じにする効果を得ることができます。例えば、`long_options` の最初のパラメータ `add` では、`val` の値を短いオプションの文字 `'a'` に設定します。このため、`--add` と `-a` を判断するとき、同じ処理フローに入り、同じ意味として扱われます。

パズルの最後のピースは `optind` と `optarg` の使い方です。`optind` は `argv` 内の次の処理待ちの引数の位置を示し、`optarg` は追加の引数文字列を指し示します。

コードをコンパイルして実行：

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

`-a`と`--add`の意味は同じで、短いパラメータのオプション引数はその後に直接続けます。例えば`-c4`のように、長いパラメータのオプション引数は等号が必要です。例えば`--verbose=3`のように。

## mobuleparam

okay、ついにこの記事の最初の発端となった方法にたどり着きました。Linuxカーネルでは、カーネルモジュールにパラメータを渡すために非常に巧妙な方法、つまり `moduleparam` を使用しています。ここでは、Linuxカーネルの `moduleparam` の手法を簡単に説明しますが、詳細な説明はコードを見てください。私は一部 `moduleparam` の処理方法を参考にしましたが、Linuxカーネルの `moduleparam` とはいくつか異なる点があります。区別するため、私の手法を `small moduleparam` と呼ぶことにします。Linuxカーネルの手法は変わらず `moduleparam` と呼びます。

先来看看 `moduleparam` の用法、モジュール内で宣言します：

```c
int enable_debug = 0;
module_param(enable_debug, int, 0);
```

次に、モジュールをロードする際に入力されるパラメータ：

```shell
$ insmod mod enable_debug=1
```

変数 `enable_debug` は正しく `1` に設定され、使いやすく、追加するコードも少なくて済み、コードは非常に短く優雅に書けます。`getenv` や `getopt` のように多くのループや条件判断を書く必要はなく、型変換も自動で行われます。ですので、この方法をコマンドライン引数の処理に使えれば、さらに良いと思いました。

モジュールパラメーターの主要実装を見てみましょう：

```cpp linenums="1"
struct kernel_param {
const char *name;           // Variable name
u16 perm;                   // Access permission variable
	u16 フラグ;                  // 変数が bool 型かどうか
param_set_fn set;           // str -> variable value
	param_get_fn get;           // 変数の値 -> str
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

`module_param` はマクロで、実際に行うことは、渡された変数に反映される `kernel_param` という構造体を作成することです。この構造体は、アクセスおよび変数を設定するための情報を保存しており、具体的には20行目から24行目にかけて説明されています。そして、その構造体は `__param` というセクション（ `__section__ ("__param")` ）に置かれます。構造体が正常に保存された後、カーネルはモジュールをロードする際に、ELFファイルの `section __param` の位置と構造体の数を特定し、名前と `param_set_fn` に基づいてそれぞれのパラメータの値を設定します。特定の名前の `section` を見つける方法はプラットフォームに依存しており、Linuxカーネルの実装はELFファイルの処理を行っています。LinuxはELFファイルの情報を見るためのコマンド `readelf` を提供しており、興味のある方は `readelf` のヘルプ情報を参照できます。

Linux カーネルのアプローチはプラットフォームに依存しており、私が求めているのはプラットフォームに依存しないパラメータの扱い方なので、元の「moduleparam」のアプローチを変更する必要があります。つまり、「__section__("__param")」の宣言を削除します。要するに、elf ファイルの「section」を手間をかけて読み取る必要はないということです。修正後の使い方を見てみましょう：

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

それでは、各リフレクション構造を保持するために、`init_module_param(num)` というマクロを追加しました。これにより、構造の保存領域を宣言します。`num`はパラメータの数であり、実際のパラメータ数が`num`を超える場合、プログラムはアサーションエラーを発生させます。`module_param`の宣言は、元のものと若干異なり、最後のアクセス権を示すパラメータが削除されており、アクセス権の制御は行われません。さらに、`module_param_bool`というマクロが追加され、`bool`を表す変数を処理します。これはLinuxのバージョンでは不要ですが、gccの組み込み関数`__builtin_types_compatible_p`を使用して変数の型を判断します。残念ながら、MSVCにはこの関数がないため、この機能を削除し、代わりにマクロを追加しました。`module_param_array`と`module_param_string`は、配列と文字列を処理するためのものであり、元のバージョンでもこの2つの機能があります。

パラメータの宣言が完了したら、引数を処理します。`parse_params` マクロを使用し、`argc、argv` を渡し、3 番目の引数は未知のパラメータを処理するコールバック関数のポインタです。`NULL` を渡すことができます。この場合、位置パラメータに到達するとパラメータの処理が中断され、エラーコードが返されます。

コードをコンパイルして実行する：

```
.\moduleparam_test.exe error=0 test=101 btest=1 latest=1,2,3 strtest=\"Hello World!\"
Parsing ARGS: error=0 test=101 btest=1 latest=1,2,3 strtest="Hello World!"
find unknown param: error
test = 101
btest = Y
latest = 1,2,3
strtest = Hello World!
```

数値、配列、および文字列が正しく読み込まれてフォーマットが変換されることがわかります。変換できないパラメーターがある場合は、エラーコードが返され関連情報が出力されます。数行のコードを追加するだけで、パラメーターの読み込みと変換処理が完了し、スマートに使用できます。詳細な実装はコードを直接確認できます。[ここをクリックしてください](https://github.com/disenone/aparsing)。

##要約

この度、私たちはC/C++でのコマンドライン引数の処理方法である`getenv`、`getopt`、および`moduleparam`をまとめました。それぞれの方法には特性があり、将来必要に応じて実際の要求に合った方法を選択できます。

- `getenv` はネイティブでマルチプラットフォームに対応しており、直接使用できますが、あまりにも原始的で、環境変数を使用するため、環境に一定の汚染をもたらします。使用する前に、不要な環境変数をクリアして、前回の設定の残留汚染を防ぐことをお勧めします。
`getopt` は Linux プラットフォームでネイティブにサポートされているが、Windows ではサポートされていないため、クロスプラットフォームで使用するには実装コードを含める必要があります。パラメータの渡し方は Linux のコマンドライン引数の標準に従っており、オプション引数をサポートしていますが、少し扱いが面倒です。通常、異なるパラメータを処理するためにループや条件判断が必要であり、数値のパラメータに対しても使いづらいという欠点があります。
`moduleparam` は、Linux カーネルの `moduleparam` の実装を参考にしたコマンドライン引数処理ツールです。クロスプラットフォームに対応しており、使いやすく、異なるタイプの引数の型変換をサポートしていますが、欠点は各引数に対応する変数を保持する必要があることです。

--8<-- "footer_ja.md"


> この投稿は ChatGPT を使って翻訳されました。フィードバックは[**こちら**](https://github.com/disenone/wiki_blog/issues/new)中指摘の漏れを示してください。 
