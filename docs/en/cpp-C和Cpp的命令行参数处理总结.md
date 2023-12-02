---
layout: post
title: Summary of command line parameter handling in C/C++
categories:
- c++
catalog: true
tags:
- dev
description: Some time ago, when I was going through the Linux kernel code, I came
  across the handling of module parameters (moduleparam) in the kernel, and I found
  it quite ingenious. It made me want to study how command-line arguments in C can
  be handled better.
figures:
- assets/post_assets/2016-11-19-aparsing/aparsing.png
---

<meta property="og:title" content="C/C++ 的命令行参数处理总结" />

![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/gcc-4.9-blue.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/clang-3.7-birghtgreen.svg){:style="display: inline-block"}

![](assets/img/2016-11-19-aparsing/aparsing.png)

Some time ago, when I was going through the Linux kernel code, I came across the way the kernel handles module parameters (moduleparam), and I found it quite ingenious. It made me curious about how command-line arguments in C could be better handled. The code used in this article can be found here [aparsing](https://github.com/disenone/aparsing). The code can be compiled and run on Windows, Linux, and Mac OS X. Detailed compilation instructions can be found in the README.md file.

## getenv

The standard library provides us with a function `getenv`. Literally, this function is used to retrieve environment variables. So as long as we set the required environment variables in advance and retrieve them in the program, we indirectly pass the parameters to the program. Let's take a look at the following [code](https://github.com/disenone/aparsing/blob/master/getenv/getenv_test.c):

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

The `getenv` function is declared on line [4](#__codelineno-0-5). It takes the name of the variable you want to retrieve as input and returns the value of that variable. If the variable is not found, it returns 0. Lines [10](#__codelineno-0-10) and [15](#__codelineno-0-15) are used to retrieve the values of two environment variables respectively. If the variables are valid, their values are printed. It is worth noting that `getenv` always returns a string, so the user needs to manually convert it to the desired data type. Therefore, it may not be very convenient to use. Compile and run:

Under Windows:

``` bat
set GETENV_ADD=abc & set GETENV_NUM=1 & .\getenv_test.exe
```

Under Linux:

 


``` shell
GETENV_ADD=abc GETENV_NUM=2 ./getenv_test 
```

Output:

```
GETENV_ADD = abc
GETENV_NUM = 2
```

## getopt

Linux provides us with a set of functions `getopt, getopt_long, getopt_long_only` to handle command-line arguments. The declarations of these three functions are as follows:

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

`getopt` can only handle short options (i.e., single character options), while `getopt_long` and `getopt_long_only` can handle long options. For a detailed explanation of the functions, you can refer to the manual in Linux. Now, let's illustrate the usage of `getopt` and `getopt_long` through examples.

It should be noted that these functions are not available on Windows, so I found a source code that can be compiled on Windows and made some minor modifications. The code can be found [here](https://github.com/disenone/aparsing/tree/master/getopt).

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

Let's focus on analyzing the usage of `getopt_long`. The first three parameters of `getopt_long` are the same as `getopt`: the number of command-line arguments `argc`, the array of command-line arguments `argv`, and the exact format of short parameters `optstring`. The format of `optstring` consists of individual short parameter characters, followed by a colon `:` to indicate a parameter is required, and two colons `::` to indicate an optional parameter. For example, in line 19, the declaration of the short parameters is as follows: the `b` parameter does not take any extra arguments, the `a` parameter requires an extra argument, and the `c` parameter takes an optional argument.

The last two arguments of `getopt_long` are used to handle long options, and the structure of `option` is:

```c
struct option {
const char *name;       // Long parameter name
int         has_arg;    // Whether it takes an additional argument
int        *flag;       // Specify how to return the function call result
int         val;        // The returned value
};
```
Although it is called a long parameter, the `name` can still be set to a single character length.

`has_arg` can be set to `no_argument, required_argument, optional_argument`, which respectively indicate no argument, required argument, optional argument.

`flag` and `val` are used together. If `flag = NULL`, `getopt_long` will directly return `val`. Otherwise, if `flag` is a valid pointer, `getopt_long` will perform an operation similar to `*flag = val`, which sets the variable pointed to by `flag` to the value of `val`.

If `getopt_long` finds a match for a short option, it will return the character value of that option. If it finds a match for a long option, it will return `val` (`flag = NULL`) or return `0` (`flag != NULL; *flag = val;`); if it encounters a non-option character, it will return `?`; if all options have been processed, it will return `-1`.

By utilizing the feature of return values, we can achieve the same effect of having the same meaning for long options and short options. For example, the first parameter of `long_options` is set to `add` with `val` value as the character `'a'`. In this case, when checking the return value, both `--add` and `-a` will enter the same processing branch and be treated as having the same meaning.

The last piece of the jigsaw puzzle is the usage of `optind` and `optarg`. `optind` represents the position of the next argument to be processed in `argv`, while `optarg` points to the additional argument string.

Compile and run the code:

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

The meanings of `-a` and `--add` are the same. For short parameters, the optional parameter follows immediately after, for example `-c4`. For long parameters, the optional parameter needs to be specified with an equal sign, for example `--verbose=3`.

## mobuleparam

Okay, finally we have come to the method that triggered this article in the first place. The Linux kernel uses a clever technique to pass parameters to kernel modules, and that technique is called `moduleparam`. Here, I'll explain briefly how `moduleparam` works in the Linux kernel, but for a more detailed explanation, you can refer to the code. Although I have borrowed some handling techniques from `moduleparam`, there are some differences between my method, which I'll refer to as `small moduleparam`, and the one used in the Linux kernel, which will still be called `moduleparam`.

First, let's take a look at the usage of `moduleparam`, which is declared inside the module:

```c
int enable_debug = 0;
module_param(enable_debug, int, 0);
```

Then enter parameters when loading the module:

```shell
$ insmod mod enable_debug=1
```

The variable `enable_debug` has been correctly set to `1`, making it convenient to use. There is also very little additional code that needs to be added, and the code can be written in a concise and elegant manner. There is no need to write multiple loop conditions like `getenv` and `getopt`, and it also includes built-in type conversion. So, when I see it, I think it would be even better if we can use this method to handle command-line arguments.

Now let's take a look at the core implementation of `moduleparam`:

```cpp linenums="1"
struct kernel_param {
const char *name;           // Variable name
u16 perm;                   // Variable access permission
u16 flags;                  // Variable is bool type or not
param_set_fn set;           // str -> variable value
param_get_fn get;           // variable value -> str
	union {
void *arg;              // variable pointer
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

`module_param` is a macro that actually establishes a structure called `kernel_param` that reflects the incoming variable. This structure, which contains enough information to access and set the variable, is stored in a section called `__param`, as shown in lines 20-24. Once the structure is saved, the kernel will locate the position and number of structures in the elf file's `section __param` when loading the module. The parameters are then individually set based on their names and `param_set_fn`. The method of locating a specific named section is platform-specific, and the Linux kernel implements it by processing the elf file. In Linux, the `readelf` command can be used to view information about elf files. If interested, you can refer to the `readelf` help information.

The above mentioned method of the Linux kernel is platform-specific, but I am looking for a platform-independent way to handle parameters. So we need to make some changes to the original `moduleparam` approach by removing the `__section__ ("__param")` declaration, as we don't want to read the `section` of the elf file in a complicated way. Let's take a look at the modified usage below:

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

To preserve the structure of each reflection, I have added a macro `init_module_param(num)` to declare the space for storing the structure. `num` is the number of parameters, and if the actual number of parameters declared exceeds `num`, the program will trigger an assertion error. The declaration of `module_param` is slightly different from the original, removing the last parameter that represents access permissions, so no access control is done. In addition, a macro `module_param_bool` has been added to handle variables that represent `bool`. This is not necessary in the Linux version, as it uses the gcc built-in function `__builtin_types_compatible_p` to determine the variable type. Unfortunately, MSVC does not have this function, so I had to remove this functionality and add a macro instead. `module_param_array` and `module_param_string` are used to handle arrays and strings, which were already present in the original version.

After declaring the parameters, it's time to process the incoming arguments. Use the macro `parse_params` and pass in `argc, argv`. The third parameter is a pointer to the callback function for handling unknown parameters. You can pass `NULL`, which will interrupt the processing of positional arguments and return an error code.

Compile and run code:

```
.\moduleparam_test.exe error=0 test=101 btest=1 latest=1,2,3 strtest=\"Hello World!\"
Parsing ARGS: error=0 test=101 btest=1 latest=1,2,3 strtest="Hello World!"
find unknown param: error
test = 101
btest = Y
latest = 1,2,3
strtest = Hello World!
```

You can see that numerical values, arrays, and strings can all be read and converted correctly. If there are parameters that cannot be converted, an error code will be returned and relevant information will be printed. We can easily add a few lines of code to handle parameter reading and conversion, which makes it very elegant to use. For more detailed implementation, you can directly refer to the code [here](https://github.com/disenone/aparsing).

## Summary

This time we summarized three methods for handling command line arguments in C/C++: `getenv`, `getopt`, and `moduleparam`. Each method has its own characteristics, and you can choose the appropriate method based on the actual needs in the future.

- `getenv` is a native multi-platform function that can be used directly. However, it is too primitive and utilizes environment variables, which can cause some pollution to the environment. It is recommended to clear unnecessary environment variables before each use to avoid contamination from previous settings.

- `getopt` is natively supported on Linux platforms, but not on Windows. Therefore, it requires code implementation to achieve cross-platform usage. The parameter passing follows the standard command line argument format of Linux and supports optional parameters. However, it can be slightly cumbersome to use, often requiring loops and conditional statements to handle different parameters, and it is not particularly friendly to numerical types of parameters.

- `moduleparam` is a command line argument processing tool inspired by the `moduleparam` implementation in the Linux kernel. It supports cross-platform usage and is easy to use. It can perform type conversion on different types of parameters. The drawback is that each parameter requires a corresponding variable for storage.

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
