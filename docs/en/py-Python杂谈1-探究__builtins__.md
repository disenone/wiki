---
layout: post
title: Python Talk 1 - Exploring __builtins__
categories:
- c++
- python
catalog: true
tags:
- dev
- game
- python
- __builtins__
- builtins
description: What's the difference between `__builtin__` and `__builtins__`? Are `__builtins__`
  in the main module different from other modules? Why are they set differently? Where
  is `__builtins__` defined? In this article, we will explore some lesser-known facts
  about `__builtins__`, along with some related content that you shouldn't miss.
figures: []
---

<meta property="og:title" content="Python 杂谈 1 - 探究 __builtins__ - Disenone" />

##Preface

We know that `__builtins__` is an object that exists in the global namespace, intentionally exposed by Python for use in the code, so it can be accessed directly from anywhere in the code. However, a somewhat obscure piece of information is that within the `main` module (which refers to `__main__`, both terms indicate the same module and may be used interchangeably later), `__builtins__` corresponds to the `__builtin__` module, while in other modules, it represents `__builtin__.__dict__`, which can be quite perplexing. Although it's not recommended by the official documentation to use `__builtins__` directly, why do you present me with two different situations? In this article, we will explore the origins of this setting, during which we can also find answers to the following questions: What is the difference between `__builtin__` and `__builtins__`? Why are `__builtins__` in the main module and other modules set differently? Where is `__builtins__` defined?


## `__builtin__`

Before discussing `__builtins__`, we need to first understand what `__builtin__` is. `__builtin__` is the module that stores all the built-in objects, which are the objects in Python that we can normally use directly. Essentially, all the Python built-in objects are objects in the `__builtin__` module, which are contained in `__builtin__.__dict__`, corresponding to Python's built-in namespace. Remember this key point: `__builtin__` is a module. We can find the definition and usage of the `__builtin__` module in the Python source code (note that the Python source code mentioned below refers to the CPython-2.7.18 source code):

``` c
// pythonrun.c
void
Py_InitializeEx(int install_sigs)
{
    PyInterpreterState *interp;
    ...
Initialize the __builtin__
    bimod = _PyBuiltin_Init();
    // interp->builtins = __builtin__.__dict__
    interp->builtins = PyModule_GetDict(bimod);
    ...
}

// bltinmodule.c
PyObject *
_PyBuiltin_Init(void)
{
    PyObject *mod, *dict, *debug;
    mod = Py_InitModule4("__builtin__", builtin_methods,
                         builtin_doc, (PyObject *)NULL,
                         PYTHON_API_VERSION);
    if (mod == NULL)
        return NULL;
    dict = PyModule_GetDict(mod);

Add built-in objects to the dictionary.
    ...
}

// ceval.c
// Get builtins
PyObject *
PyEval_GetBuiltins(void)
{
    PyFrameObject *current_frame = PyEval_GetFrame();
    if (current_frame == NULL)
        return PyThreadState_GET()->interp->builtins;
    else
        return current_frame->f_builtins;
}
```

During initialization, `Python` calls `_PyBuiltin_Init` to create the `__builtin__` module and adds built-in objects to it. The interpreter itself maintains a reference to `interp->builtins = __builtin__.__dict__`, and the currently executing frame structure also references `current_frame->f_builtins`. So naturally, when the code needs to find an object by name, `Python` will search inside `current_frame->f_builtins` to access all built-in objects.

```c
// ceval.c
TARGET(LOAD_NAME)
{
Search first in the f->f_locals namespace.
    ...
    if (x == NULL) {
Search for the global space again.
        x = PyDict_GetItem(f->f_globals, w);
        if (x == NULL) {
// Here we go to find it in the built-in space.
            x = PyDict_GetItem(f->f_builtins, w);
            if (x == NULL) {
                format_exc_check_arg(
                            PyExc_NameError,
                            NAME_ERROR_MSG, w);
                break;
            }
        }
        Py_INCREF(x);
    }
    PUSH(x);
    DISPATCH();
}
```

In the end, due to the confusing nature of the name `__builtin__`, it has been renamed to `builtins` in `Python3`.


## `__builtins__`

The behavior of `__builtins__` is somewhat strange:
In the `main` module (the `main` module, also known as the `environment where the top-level code runs`, is the Python module specified by the user to be run first when executing `python xxx.py` in the command line), `__builtins__ = __builtin__`.
* In other modules, `__builtins__ = __builtin__.__dict__`.

The same name, but under different modules, the behavior can be quite different, which can easily lead to confusion. However, as long as you understand this setup, it is sufficient to support your use of `__builtins__` in `Python`. This confusion will not affect your ability to write sufficiently safe code, such as:

``` python
def SetBuiltins(builtins, key, val):
    if isinstance(builtins, dict):
        builtins[key] = val
    else:
        setattr(builtins, key, val)

SetBuiltins(__builtins__, 'test', 1)
```

It is important to note that the use of `__builtins__` is not actually recommended:

> __CPython implementation detail__: Users should not touch `__builtins__`; it is strictly an implementation detail. Users wanting to override values in the builtins namespace should import the `__builtin__` (no ‘s’) module and modify its attributes appropriately.

Of course, such doubts will inevitably make you curious one day, so I have decided to continue exploring further, which is why this article exists. The following content will delve into CPython implementation details.

## Restricted Execution

Restricted Execution can be understood as the limited execution of unsafe code. The term "limited" refers to restrictions on network, I/O, etc., confining the code to a specific execution environment while controlling the execution permissions to prevent the code from affecting the external environment and system. A common use case is some online code execution websites, such as this one: [pythonsandbox](https://pythonsandbox.dev/)。

(https://docs.python.org/2.7/library/restricted.html)It was later confirmed to be unfeasible, so this feature had to be abandoned, but the code is still preserved in version 2.7.18, allowing us to do some archaeological digging.

First, let's take a look at the configuration of `__builtins__` in the `Python` source code:

``` c
// pythonrun.c
static void initmain(void)
{
    PyObject *m, *d;
// Get the __main__ module
    m = PyImport_AddModule("__main__");
    if (m == NULL)
        Py_FatalError("can't create __main__ module");

    // d = __main__.__dict__
    d = PyModule_GetDict(m);

Set `__main__.__dict__['__builtins__']`, skip if it already exists.
    if (PyDict_GetItemString(d, "__builtins__") == NULL) {
        PyObject *bimod = PyImport_ImportModule("__builtin__");
        if (bimod == NULL ||
            PyDict_SetItemString(d, "__builtins__", bimod) != 0)
            Py_FatalError("can't add __builtins__ to __main__");
        Py_XDECREF(bimod);
    }
}
```

In `initmain`, `Python` sets the `__builtins__` attribute for the `__main__` module, which defaults to the `__builtin__` module. However, if it already exists, it is not reset. Taking advantage of this feature, we can modify the built-in functions by changing `__main__.__builtins__`, in order to limit the execution permissions of the code. The specific method will be discussed later; for now, let's examine how `__builtins__` is passed.

##Passing `__builtins__`.

When creating a new stack frame:

```c
PyFrameObject *
PyFrame_New(PyThreadState *tstate, PyCodeObject *code, PyObject *globals,
            PyObject *locals)
{
    ...
    if (back == NULL || back->f_globals != globals) {
Use `globals['__builtins__']` as the `__builtins__` for the new stack frame.
// The "builtin_object" is the string '__builtins__'
        builtins = PyDict_GetItem(globals, builtin_object);
        if (builtins) {
            if (PyModule_Check(builtins)) {
                builtins = PyModule_GetDict(builtins);
                assert(!builtins || PyDict_Check(builtins));
            }
            else if (!PyDict_Check(builtins))
                builtins = NULL;
        }
        ...

    }
    else {
        /* If we share the globals, we share the builtins.
           Save a lookup and a call. */
// Or directly inherit the f_builtins from the previous stack frame.
        builtins = back->f_builtins;
        assert(builtins != NULL && PyDict_Check(builtins));
        Py_INCREF(builtins);
    }
    ...
    f->f_builtins = builtins;
    f->f_globals = globals;
}
```

When creating a new stack frame, there are mainly two ways to handle `__builtins__`: one is when there is no upper stack frame, then it takes `globals['__builtins__']`; the other is to directly take the `f_builtins` of the upper stack frame. In combination, it can be understood that in general, the `__builtins__` set in `__main__` will be inherited by subsequent stack frames, effectively shared among them.

When `import`-ing modules:

```c
static PyObject *
load_compiled_module(char *name, char *cpathname, FILE *fp)
{
    long magic;
    PyCodeObject *co;
    PyObject *m;
    ...
    co = read_compiled_module(cpathname, fp);
    ...
    m = PyImport_ExecCodeModuleEx(name, (PyObject *)co, cpathname);
    ...
}


PyObject *
PyImport_ExecCodeModuleEx(char *name, PyObject *co, char *pathname)
{
    ...
    m = PyImport_AddModule(name);
    ...
    // d = m.__dict__
    d = PyModule_GetDict(m);

Set the __builtins__ attribute for the new module being loaded here.
    if (PyDict_GetItemString(d, "__builtins__") == NULL) {
        if (PyDict_SetItemString(d, "__builtins__",
                                 PyEval_GetBuiltins()) != 0)
            goto error;
    }
    ...
    // globals = d, locals = d
    v = PyEval_EvalCode((PyCodeObject *)co, d, d);
    ...
}

PyObject *
PyEval_EvalCode(PyCodeObject *co, PyObject *globals, PyObject *locals)
{
    return PyEval_EvalCodeEx(co,
                      globals, locals,
                      (PyObject **)NULL, 0,
                      (PyObject **)NULL, 0,
                      (PyObject **)NULL, 0,
                      NULL);
}
```

When importing other modules, the module's `__builtins__` is set to the result of `PyEval_GetBuiltins()`, a function we've already discussed, which in most cases corresponds to `current_frame->f_builtins`. In the case of `import` within the `__main__` module, `current_frame` is the stack frame of the `__main__` module, and `current_frame->f_builtins = __main__.__dict__['__builtins__']` (the first scenario of `PyFrame_New` mentioned above).

The newly loaded module will use `PyEval_EvalCode` to execute the code within the new module. As can be seen, the parameters `globals` and `locals` passed to `PyEval_EvalCode` are actually the module's own `__dict__`, and the module `m.__dict__['__builtins__'] = PyEval_GetBuiltins()`.

In summary, we can conclude that modules imported from the `__main__` module will also inherit the `__builtins__` from `__main__`, which will be passed down during internal imports. This ensures that all modules and submodules loaded from `__main__` can share the same `__builtins__` from `__main__`.

So what about functions that are called within a module? Regarding functions in a module, when creating and calling:

```c
// ceval.c
Create function
TARGET(MAKE_FUNCTION)
{
    v = POP(); /* code object */

The 'f->f_globals' here is equivalent to the module's own globals, as mentioned earlier, it is also equivalent to 'm.__dict__'.
    x = PyFunction_New(v, f->f_globals);
    ...
}

PyObject *
PyFunction_New(PyObject *code, PyObject *globals)
{
    PyFunctionObject *op = PyObject_GC_New(PyFunctionObject,
                                        &PyFunction_Type);
    ...
Here is equivalent to op->func_globals = globals = f->f_globals
    op->func_globals = globals;
}

// Call the function
static PyObject *
fast_function(PyObject *func, PyObject ***pp_stack, int n, int na, int nk)
{
    PyCodeObject *co = (PyCodeObject *)PyFunction_GET_CODE(func);
    // globals = func->func_globals
    PyObject *globals = PyFunction_GET_GLOBALS(func);
    ...
// globals is passed to PyEval_EvalCodeEx, which will then pass it to PyFrame_New to create a new stack frame.
    return PyEval_EvalCodeEx(co, globals,
                             (PyObject *)NULL, (*pp_stack)-n, na,
                             (*pp_stack)-2*nk, nk, d, nd,
                             PyFunction_GET_CLOSURE(func));
}
```

When creating a function, `f->f_globals` will be stored in the function structure variable `func_globals`, and for the module `m`, `f->f_globals = m.__dict__`. When the function is executed, the `globals` parameter passed to `PyFrame_New` is the `func_globals` saved during creation, and `__builtins__` can naturally be accessed in `func_globals`.

At this point, the passing of `__builtins__` ensures consistency, so that all modules, submodules, functions, stack frames, etc., can reference the same one, meaning they share the same built-in namespace.

##Specify the execution of the `__main__` module.

We already know that the `__builtins__` of the `__main__` module itself can be passed to all submodules, functions, and stack frames. When executing `python a.py` in the command line, Python will execute `a.py` as the `__main__` module. But how does it do that?

```c
// python.c
int
main(int argc, char **argv)
{
    ...
    return Py_Main(argc, argv);
}

// main.c
int
Py_Main(int argc, char **argv)
{
    ...
Attempt to execute code using the importer of the module.
    if (filename != NULL) {
        sts = RunMainFromImporter(filename);
    }
    ...
Usually, we run our own Python files using this.
    sts = PyRun_AnyFileExFlags(
            fp,
            filename == NULL ? "<stdin>" : filename,
            filename != NULL, &cf) != 0;
    }
    ...
}

// pythonrun.c
int
PyRun_AnyFileExFlags(FILE *fp, const char *filename, int closeit,
                     PyCompilerFlags *flags)
{
    ...
    return PyRun_SimpleFileExFlags(fp, filename, closeit, flags);
}


int
PyRun_SimpleFileExFlags(FILE *fp, const char *filename, int closeit,
                        PyCompilerFlags *flags)
{
    ...
    m = PyImport_AddModule("__main__");
    d = PyModule_GetDict(m);
    ...
// Set __file__ attribute
    if (PyDict_SetItemString(d, "__file__", f) < 0) {
        ...
    }
    ...
    // globals = locals = d = __main__.__dict__
    v = run_pyc_file(fp, filename, d, d, flags);
    ...
}

static PyObject *
run_pyc_file(FILE *fp, const char *filename, PyObject *globals,
             PyObject *locals, PyCompilerFlags *flags)
{
    ...
// Read the code object co from the pyc file and execute the code
// PyEval_EvalCode will also call PyFrame_New to create a new stack frame.
    v = PyEval_EvalCode(co, globals, locals);
    ...
}
```

When executing `python a.py`, it generally proceeds to `PyRun_SimpleFileExFlags`. Inside `PyRun_SimpleFileExFlags`, `__main__.__dict__` will be extracted to be used as the `globals` and `locals` when executing the code, and ultimately passed to `PyFrame_New` to create a new stack frame for executing `a.py`. By combining the aforementioned passing of `__builtins__` in modules and functions, subsequent code executions can all share the same `current_frame->f_builtins = __main__.__builtins__.__dict__`.


##Further Discussion on Restricted Execution

Before version 2.3, `Python` once provided [Restricted Execution](https://docs.python.org/2.7/library/restricted.html)It is based on the characteristic of `__builtins__`. Or it can be considered that `__builtins__` is designed to be a module object in the `__main__` module and a `dict` object in other modules in order to achieve Restricted Execution.

Consider this situation: If we could freely customize our own `__builtin__` module and set it to `__main__.__builtins__`, it would mean that all subsequent executed code would use our customized module. We could customize specific versions of built-in functions and types like `open`, `__import__`, `file`, etc. Furthermore, could this approach help us restrict the permissions of the executing code, preventing it from making unsafe function calls or accessing unsafe files?

`Python` had attempted this before, and the module that implements this functionality is called `rexec`.

### `rexec`

I have no intention of delving too deeply into the explanation of `rexec`'s implementation, as the principles have actually been explained in the preceding text, and this module itself has been deprecated. I will just provide a brief summary of some key code snippets for easy reference.


```python
# rexec.py
class RExec(ihooks._Verbose):
    ...
    nok_builtin_names = ('open', 'file', 'reload', '__import__')

    def __init__(self, hooks = None, verbose = 0):
        ...
        self.modules = {}
        ...
        self.make_builtin()
        self.make_initial_modules()
        self.make_sys()
        self.loader = RModuleLoader(self.hooks, verbose)
        self.importer = RModuleImporter(self.loader, verbose)

    def make_builtin(self):
        m = self.copy_except(__builtin__, self.nok_builtin_names)
        m.__import__ = self.r_import
        m.reload = self.r_reload
        m.open = m.file = self.r_open

    def add_module(self, mname):
        m = self.modules.get(mname)
        if m is None:
            self.modules[mname] = m = self.hooks.new_module(mname)
        m.__builtins__ = self.modules['__builtin__']
        return m

    def r_exec(self, code):
        m = self.add_module('__main__')
        exec code in m.__dict__

    def r_eval(self, code):
        m = self.add_module('__main__')
        return eval(code, m.__dict__)

    def r_execfile(self, file):
        m = self.add_module('__main__')
        execfile(file, m.__dict__)
```

The `r_execfile` function executes a file as if it was the `__main__` module, but with customizations. Inside `self.add_module('__main__')`, the module is set with `m.__builtins__ = self.modules['__builtin__']`, where `__builtin__` is customized and generated by `make_builtin`, replacing the `__import__`, `reload`, `open` functions, and removing the `file` type. This way, we can control the access of the code being executed to the built-in namespace.

For some built-in modules, 'rexec' has also been customized to protect against insecure access, such as the 'sys' module, which only retains a portion of objects. It achieves prioritized loading of customized modules during import through customized 'self.loader' and 'self.importer'.

If you are interested in the code details, please refer to the relevant source code yourself.

###Failure of `rexec`

In the previous text, it was mentioned that `rexec` has been deprecated since `Python 2.3`, as this approach has been proven unfeasible. Let's trace back a bit out of curiosity:

A [bug](https://mail.python.org/pipermail/python-dev/2002-December/031160.html)And sparked a discussion among developers:

    > it's never going to be safe, and I doubt it's very useful as long as it's not safe.

    > Every change is a potential security hole.

    > it's hard to predict what change is going to break it.

    > I don't expect you'll ever reach the point where it'll be wise to advertise this as safe.  I certainly won't.

    >  this is only a useful occupation if you expect to eventually reach a point where you expect that there aren't any security flaws left.  Jeremy & I both doubt that Python will ever reach that level, meaning that the whole exercise of fixing security flaws is a waste of time (if you know you *can't* make it safe, don't waste time trying).

    > I agree (but I have said that in past) the best thing is to deprecate/rip out rexec.

    > The code will still be in older versions if someone decides to pick it up and work on it as a separate project.

The root cause of this bug was the introduction of new-style class `object` in `Python`, which prevented `rexec` from functioning correctly. Developers expressed that in the foreseeable future, it would be difficult to avoid such situations, as any modifications could potentially lead to vulnerabilities in `rexec`, rendering it inoperative or breaching permission restrictions. Essentially, the vision of providing a flawlessly secure environment was unattainable, requiring developers to continuously patch up issues and resulting in significant time wastage. Eventually, the `rexec` module was deprecated, and `Python` no longer offered similar functionalities. However, the setting related to `__builtins__` was retained due to compatibility and other considerations.

In the following years, around 2010, a programmer released [pysandbox](https://github.com/vstinner/pysandbox)Dedicated to providing a Python sandbox environment as an alternative to 'rexec'. However, 3 years later, the author voluntarily abandoned this project and detailed why they considered it a failure: [The pysandbox project is broken](https://mail.python.org/pipermail/python-dev/2013-November/130132.html)There are also other authors who have written to summarize the failure of this project: [The failure of pysandbox](https://lwn.net/Articles/574215/)If you're interested, you can take a look at the original text. I'll also provide some summaries here to help with understanding:

> After having work during 3 years on a pysandbox project to sandbox untrusted code, I now reached a point where I am convinced that pysandbox is broken by design. Different developers tried to convinced me before that pysandbox design is unsafe, but I had to experience it myself to be convineced.

> I now agree that putting a sandbox in CPython is the wrong design. There are too many ways to escape the untrusted namespace using the various introspection features of the Python language. To guarantee the [safety] of a security product, the code should be [carefully] audited and the code to review must be as small as possible. Using pysandbox, the "code" is the whole Python core which is a really huge code base. For example, the Python and Objects directories of Python 3.4 contain more than 126,000 lines of C code.

> The security of pysandbox is the security of its weakest part. A single bug is enough to escape the whole sandbox.

> pysandbox cannot be used in practice. To protect the untrusted namespace, pysandbox installs a lot of different protections. Because of all these protections, it becomes hard to write Python code. Basic features like "del dict[key]" are denied. Passing an object to a sandbox is not possible to sandbox, pysandbox is unable to proxify arbitary objects. For something more complex than evaluating "1+(2*3)", pysandbox cannot be used in practice, because of all these protections.

The author of "pysandbox" believes that setting up a sandbox environment in Python is a flawed design. There are too many ways to escape from the sandbox, Python offers rich language features, and the extensive code base of CPython makes it nearly impossible to ensure sufficient security. The development of "pysandbox" has been mainly about applying patches continuously. However, the excessive patches and restrictions have led the author to conclude that "pysandbox" is not practically usable anymore. Numerous syntax features and functions are restricted from use, such as the simple `del dict[key]`.

##Where is the way out of Restricted Execution?

Since methods like `rexec` and __pysandbox__ that provide sandbox environments by patching Python are no longer feasible, I can't help but wonder: How can we provide Python with a functional sandbox environment now?

Here I have continued to collect some other implementation methods or cases for easy reference and consultation:

* [PyPy](https://doc.pypy.org/en/latest/sandbox.html)There is a [branch](https://foss.heptapod.net/pypy/pypy/-/tree/branch/sandbox-2)Provided sandbox functionality, combined with additional [sandboxlib](https://foss.heptapod.net/pypy/sandboxlib)You can compile a version of PyPy with a sandbox environment on your own. If you're interested, you can try setting it up yourself, referring to some [instructions](https://foss.heptapod.net/pypy/pypy/-/issues/3192)The principle of the PyPy implementation is to create a subprocess, where all input/output and system calls of the subprocess are redirected to an external process, which controls these permissions. Additionally, it can also regulate memory and CPU usage. It is important to note that this branch has not had any new commits for some time, so please use it with caution.

* Utilize the sandbox environment tools provided by the operating system. [seccomp](https://en.wikipedia.org/wiki/Seccomp)It is a computing security tool provided by the Linux kernel, [libsecoomp](https://github.com/seccomp/libseccomp/tree/main/src/python)Provides Python bindings that can be embedded into the code; or use tools based on seccomp to execute code, such as [Firejail](https://firejail.wordpress.com/).[AppArmor](https://apparmor.net/)It is a Linux kernel security module that allows administrators to control the system resources and functionalities that programs can access, thereby protecting the operating system. [codejail](https://github.com/openedx/codejail)It is a Python sandbox environment implemented based on AppArmor. If you're interested, you can give it a try. There are many similar tools, but I won’t list them all here.

Use sandbox virtual environments or containers. [Windows Sandbox](https://learn.microsoft.com/zh-cn/windows/security/threat-protection/windows-sandbox/windows-sandbox-overview),[LXC](https://linuxcontainers.org/), [Docker](https://www.docker.com/)Wait a moment, it will not be elaborated here any further.

##Summary

This article is a bit lengthy; thank you for getting this far. I believe the questions listed at the beginning have all been answered.

--8<-- "footer_en.md"


> This post was translated using ChatGPT, please provide [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions. 
