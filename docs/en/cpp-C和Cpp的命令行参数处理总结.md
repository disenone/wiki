---
layout: post
title: Summary of Command-Line Argument Processing in C/C++
categories:
- c++
catalog: true
tags:
- dev
description: Some time ago, while flipping through the Linux kernel code, I came across
  the handling of module parameters (moduleparam) in the kernel. I found it quite
  ingenious and couldn't help but wonder how command line arguments in C can be better
  handled.
figures:
- assets/post_assets/2016-11-19-aparsing/aparsing.png
---


![](https://img.shields.io/badge/vs-2015-68217A.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/gcc-4.9-blue.svg){:style="display: inline-block"}
![](https://img.shields.io/badge/clang-3.7-birghtgreen.svg){:style="display: inline-block"}

![](assets/img/2016-11-19-aparsing/aparsing.png)

Some time ago, when I was browsing the Linux kernel code, I came across the handling of module parameters (moduleparam) in the kernel. I found it quite ingenious, which made me curious about how command line parameters are handled in C. The code used in this article can be found here [aparsing](https://github.com/disenone/aparsing). The code can be compiled and run on Windows, Linux, and Mac OS X, and detailed compilation instructions can be found in the README.md file.

## getenv

The standard library provides us with a function `getenv` which, as its literal meaning suggests, is used to retrieve environment variables. Therefore, as long as we set the required environment variables in advance and retrieve them in our program, we can indirectly pass the parameters to the program. Let's take a look at the following [code](https://github.com/disenone/aparsing/blob/master/getenv/getenv_test.c):

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

The `getenv` function is declared in line [4](#__codelineno-0-5). It takes the variable name as input and returns the value of that variable. If the variable is not found, it returns 0. In lines [10](#__codelineno-0-10) and [15](#__codelineno-0-15), we are getting the values of two environment variables and if they are valid, we print their values. It's important to note that `getenv` always returns a string, so the user needs to manually convert it into the desired data type. This makes it less convenient to use. Compile and run the code.

On Windows:

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

Linux provides us with a set of functions `getopt, getopt_long, getopt_long_only` to handle command line arguments. The declarations of these three functions are respectively:

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

`getopt` can only handle short options (i.e., single-character options), while `getopt_long` and `getopt_long_only` can handle long options. For detailed function explanations, you can refer to the manual in Linux. Below, we will illustrate the usage of `getopt` and `getopt_long` through examples.

It should be noted that these functions are not available in Windows. Therefore, I found a piece of source code that can be compiled on Windows and made a small modification. The code can be found [here](https://github.com/disenone/aparsing/tree/master/getopt).

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

We will focus on the usage of `getopt_long`, the first three parameters of `getopt_long` are the same as `getopt`. They are the number of command line arguments `argc`, the array of command line arguments `argv`, and the specific format of short parameters `optstring`. The format of `optstring` consists of individual short parameter characters, followed by a colon `:` to indicate that it takes a required parameter, and two colons `::` to indicate that it takes an optional parameter. For example, in line 19, we declare the format of short parameters: the `b` parameter does not take any additional parameter, the `a` parameter takes an additional parameter, and the `c` parameter takes an optional parameter.

The last two arguments of `getopt_long` are used to handle long options, and the structure of `option` is as follows:

```c
struct option {
```markdown
```
`const char *name;       // 长参数名字`

`int         has_arg;    // 是否带额外参数`

`int        *flag;       // 设置如何返回函数调用结果`

`int         val;        // 返回的数值`

```markdown
```
};
```
Although it is called a long parameter, `name` can still be set to a single character length.

`[has_arg]` can be set to `[no_argument]`, `[required_argument]`, `[optional_argument]`, which respectively mean without argument, with argument, with optional argument.

`flag` and `val` are used together. If `flag = NULL`, `getopt_long` will directly return `val`. Otherwise, if `flag` is a valid pointer, `getopt_long` will perform an operation similar to `*flag = val`, setting the variable pointed to by `flag` to the value of `val`.

If `getopt_long` finds a matching short option, it returns the character value of that short option. If it finds a matching long option, it returns `val` (`flag = NULL`) or `0` (`flag != NULL; *flag = val;`). If it encounters a non-option character, it returns `?`. If all options have been processed, it returns `-1`.

By utilizing the characteristics of the return value, we can achieve the same effect as using long and short parameters with equivalent meanings. For example, in the `long_options` first parameter `add`, if the `val` value is set to the character `'a'` for the short parameter, then when the return is evaluated, `--add` and `-a` will enter the same processing branch and be treated as having the same meaning.

The last piece of the puzzle is the usage of `optind` and `optarg`. `optind` represents the position of the next argument to be processed in `argv`, while `optarg` points to the additional argument string.

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

-the meaning of `-a` and `--add` is the same, for short parameters the optional parameter is followed directly afterwards, for example `-c4`, while for long parameters the optional parameter needs to be preceded by an equal sign, for example `--verbose=3`.

## mobuleparam

Ok, finally we come to the method that initially triggered this article. The Linux kernel uses a clever method to pass parameters to kernel modules, and this method is called `moduleparam`. Here, I will briefly explain the approach of `moduleparam` in the Linux kernel, for a more detailed explanation, you can refer to the code. Although I have borrowed some handling methods from `moduleparam`, there are some differences between my method and the `moduleparam` in the Linux kernel. To distinguish them, I will refer to my method as "small moduleparam", while the one in the Linux kernel will still be called "moduleparam".

First, let's take a look at the usage of `moduleparam`. Declare it inside the module:

```c
int enable_debug = 0;
module_param(enable_debug, int, 0);
```

And then input the parameters when loading the module:

```shell
$ insmod mod enable_debug=1
```

The variable `enable_debug` is correctly set to `1`, making it very convenient to use. There is also very little additional code required. The code can be written in a concise and elegant manner, without the need for extensive loop conditions like those used in `getenv` and `getopt`. Furthermore, it comes with built-in type conversion. So, when I saw it, I thought it would be even better if this method could be used to handle command-line parameters.

Next, let's take a look at the core implementation of `moduleparam`:

```cpp linenums="1"
struct kernel_param {
```cpp
const char * name;          // Variable name
u16 perm;                    // Variable access permission
u16 flags;                   // Variable whether of type bool
param_set_fn set;            // str -> Variable value
param_get_fn get;            // Variable value -> str
```
	union {
        `void *arg;`  - Variable pointer
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

`module_param` is a macro that actually creates a structure `kernel_param` which can be reflected into the variable passed in. The structure holds enough information to access and set the variable, which can be seen from lines 20-24. It then puts the structure in a `section` called `__param` (`__section__ ("__param")`). Once the structure is saved, the kernel will locate the position of the `__param` section and the number of structures in the elf file when loading the module. The kernel will then set the values for each parameter based on their names and `param_set_fn`. The method to locate a specific name `section` is platform-dependent. In the Linux kernel implementation, it involves processing the elf file. Linux provides the command `readelf` to view information about elf files. Those who are interested can refer to the `readelf` help information.

The above mentioned method of the Linux kernel is platform-specific, but I want a platform-independent approach for handling parameters. So, we need to modify the original method of `moduleparam` a bit by removing the `__section__("__param")` declaration, since we don't want to read the `section` of the elf file in a complicated way. Let's take a look at the modified usage below:

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

So in order to preserve the structure of each reflection, I added a macro `init_module_param(num)` to declare the space to save the structure. `num` is the number of parameters, and if the actual number of declared parameters exceeds `num`, the program will trigger an assertion error. The declaration of `module_param` is slightly different from the original, removing the last parameter that represents access permissions, and no longer controls permissions. In addition, a macro `module_param_bool` is added to handle variables representing `bool`. This is not needed in the Linux version because it uses the gcc built-in function `__builtin_types_compatible_p` to determine the variable's type. Unfortunately, MSVC does not have this function, so I can only remove this functionality and add a macro. `module_param_array` and `module_param_string` are for handling arrays and strings, which were also present in the original version.

Statement parameters are completed, it's time to process the incoming parameters. Use the macro `parse_params` and pass `argc, argv` as arguments. The third argument is a pointer to the callback function for handling unknown parameters. You can pass `NULL` to interrupt the handling of positional arguments and return an error code.

Compile and run the code:

```
.\moduleparam_test.exe error=0 test=101 btest=1 latest=1,2,3 strtest=\"Hello World!\"
Parsing ARGS: error=0 test=101 btest=1 latest=1,2,3 strtest="Hello World!"
find unknown param: error
test = 101
btest = Y
latest = 1,2,3
strtest = Hello World!
```

It can be seen that numerical values, arrays, and strings can be read and format-converted correctly. If encountering parameters that cannot be format-converted, an error code will be returned and relevant information will be printed. We can easily add a few lines of code to complete the parameter reading and format conversion process, making it very elegant to use. For a more detailed implementation, you can directly refer to the code [here](https://github.com/disenone/aparsing).

## Summary

This time we summarized three methods for handling command-line arguments in C/C++, which are `getenv`, `getopt`, and `moduleparam`. Each of these methods has its own characteristics, and in the future, you can choose the appropriate method based on the actual requirements.

- `getenv` is natively supported on multiple platforms, so it can be used directly. However, it is too primitive and uses environment variables, which can pollute the environment. It is best to clear unnecessary environment variables before each use to prevent lingering pollution from previous settings.
- `getopt` is natively supported on Linux platforms, but not supported on Windows, so it needs to include implementation code to use it cross-platform. The parameter passing follows the standard of Linux command line arguments, supports optional parameters, but it is slightly cumbersome to use. Usually, it requires looping and conditional statements to handle different parameters, and it is not friendly to numeric parameters.
- `moduleparam` is a command line parameter handling tool implemented based on the `moduleparam` in the Linux kernel. It supports cross-platform usage and is easy to use. It can perform type conversion on different types of parameters. The disadvantage is that each parameter requires a corresponding variable for storage.

> Original: <https://disenone.github.io/wiki>  
> This post is protected by [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by/4.0/deed.en) agreement, should be reproduced with attribution.


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
