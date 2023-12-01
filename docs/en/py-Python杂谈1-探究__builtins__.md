---
layout: post
title: Python Chat 1 - Exploring __builtins__
categories:
- c++
- python
catalog: true
tags:
- dev
- game
description: What is the difference between __builtin__ and __builtins__? Is __builtins__
  different in the main module compared to other modules? Why is it set to be different?
  Where is __builtins__ defined? In this article, we will explore some lesser-known
  facts about __builtins__ and delve into some related topics that you should not
  miss.
figures: []
---


## Introduction

We know that `__builtins__` is an object that exists in the global namespace. It is intentionally exposed by Python to the code layer and can be used directly anywhere in the code. However, a little-known fact is that in the `main` module (also known as `__main__`, referring to the same module, which may be used interchangeably later), `__builtins__` refers to the `__builtin__` module. But in other modules, it represents `__builtin__.__dict__`, which is a bit puzzling. Although it is not recommended to use `__builtins__` directly, why are there two different situations? In this article, we will discuss the origin of this setting and find answers to these questions: what is the difference between `__builtin__` and `__builtins__`? Why are `__builtins__` different in the `main` module and other modules? Where is `__builtins__` defined?


## `__builtin__`

Before discussing `__builtins__`, we need to take a look at what `__builtin__` is. `__builtin__` is a module that holds all the built-in objects. The Python built-in objects that we commonly use are essentially objects in the `__builtin__` module, which are stored in `__builtin__.__dict__`, corresponding to Python's built-in namespace. Remember this key point: `__builtin__` is a module. We can find the definition and usage of the `__builtin__` module in the Python source code (note that the Python source code mentioned below refers to CPython-2.7.18 source code):

``` c
// pythonrun.c
void
Py_InitializeEx(int install_sigs)
{
    PyInterpreterState *interp;
    ...
// Initialize \_\_builtin\_\_
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

// Add built-in objects to the `dict`
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

When `Python` is initialized, it will call `_PyBuiltin_Init` to create the `__builtin__` module and add built-in objects to it. The interpreter itself will reference `interp->builtins = __builtin__.__dict__`. The current execution frame structure will also have a reference to `current_frame->f_builtins`. So, naturally, when executing the code and needing to find an object by name, `Python` will look inside `current_frame->f_builtins` to retrieve all the built-in objects.

```c
// ceval.c
TARGET(LOAD_NAME)
{
// First, find it in the `f->f_locals` namespace.
    ... 
    if (x == NULL) {
// Search in the global namespace again.
        x = PyDict_GetItem(f->f_globals, w);
        if (x == NULL) {
// We'll look for it in the built-in space here.
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

Finally, due to the confusing nature of the name `__builtin__`, it has been renamed to `builtins` in Python 3.


## `__builtins__`

The behavior of `__builtins__` is a bit strange:

* In the `main` module (the `main` module, also known as the `top-level code execution environment`, is the Python module specified by the user to be the first to start running, usually when we execute `python xxx.py` in the command line, `xxx.py` is this module), `__builtins__ = __builtin__`;
* In other modules, `__builtins__ = __builtin__.__dict__`.

The same name is used differently in different modules, and this can be confusing. However, as long as you understand this setup, it is sufficient to support you in using `__builtins__` in Python. Confusion will not affect your ability to write secure code, such as:

``` python
def SetBuiltins(builtins, key, val):
    if isinstance(builtins, dict):
        builtins[key] = val
    else:
        setattr(builtins, key, val)

SetBuiltins(__builtins__, 'test', 1)
```

It should be noted that it is not recommended to use `__builtins__` in practice.

__CPython implementation detail__: Users should not touch `__builtins__`; it is strictly an implementation detail. Users wanting to override values in the builtins namespace should import the `__builtin__` (no 's') module and modify its attributes appropriately.

Of course, such doubts will one day make you impatient. I have decided to continue exploring here and that is why this article exists. The content below will delve into CPython implementation detail.

## Restricted Execution

Restricted Execution can be understood as the limited execution of unsafe code. The term "limited" refers to restrictions on network, I/O, and other factors, keeping the code confined within a specific execution environment. This control over code execution permissions prevents the code from affecting the external environment and system. A common use case for restricted execution is found on online code execution platforms, such as [pythonsandbox](https://pythonsandbox.dev/).

Just like you guessed, the setting of `__builtins__` in Python is related to Restricted Execution. Python used to provide similar functionality called Restricted Execution before version 2.3. However, it was later proven to be unworkable, so the feature was deprecated. Nevertheless, the code for this feature is still present in version 2.7.18, allowing us to dig into it.

First, let's look at the setting of `__builtins__` in the `Python` source code:

``` c
// pythonrun.c
static void initmain(void)
{
    PyObject *m, *d;
```python
// Get the __main__ module
```
    m = PyImport_AddModule("__main__");
    if (m == NULL)
        Py_FatalError("can't create __main__ module");

    // d = __main__.__dict__
    d = PyModule_GetDict(m);

```python
# Set __main__.__dict__['__builtins__'], if it already exists, skip it
```
    if (PyDict_GetItemString(d, "__builtins__") == NULL) {
        PyObject *bimod = PyImport_ImportModule("__builtin__");
        if (bimod == NULL ||
            PyDict_SetItemString(d, "__builtins__", bimod) != 0)
            Py_FatalError("can't add __builtins__ to __main__");
        Py_XDECREF(bimod);
    }
}
```

In `initmain`, `Python` will set the `__builtins__` attribute of the `__main__` module by default, which is equal to the `__builtin__` module. However, if it already exists, it will not be reset. Utilizing this feature, we can modify some built-in functions by modifying `__main__.__builtins__` in order to restrict the execution permissions of the code. As for the specific method, let's not discuss it for now. Let's take a look at how `__builtins__` is passed on.

## `__builtins__` Propagation

When creating a new stack frame:

```c
PyFrameObject *
PyFrame_New(PyThreadState *tstate, PyCodeObject *code, PyObject *globals,
            PyObject *locals)
{
    ...
    if (back == NULL || back->f_globals != globals) {
        // Use `globals['__builtins__']` as the `__builtins__` for the new stack frame
        // `builtin_object` is the string '__builtins__'
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
// Or directly inherit the f_builtins from the upper level stack frame.
        builtins = back->f_builtins;
        assert(builtins != NULL && PyDict_Check(builtins));
        Py_INCREF(builtins);
    }
    ...
    f->f_builtins = builtins;
    f->f_globals = globals;
}
```

When creating a new stack frame, there are mainly two scenarios for handling `__builtins__`: one is when there is no upper stack frame, in which case it takes `globals['__builtins__']`; the other is when it directly takes the `f_builtins` from the upper stack frame. In combination, it can be understood that in general, the `__builtins__` set in `__main__` will be inherited by subsequent stack frames, essentially sharing the same instance.

When `importing` modules:

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

// Set the `__builtins__` attribute for the newly loaded module here
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

When importing other modules, the `__builtins__` of that module will be set to the return value of `PyEval_GetBuiltins()`, which we have already mentioned that in most cases it is equivalent to `current_frame->f_builtins`. For `import` within the `__main__` module, `current_frame` refers to the stack frame of the `__main__` module, and `current_frame->f_builtins = __main__.__dict__['__builtins__']` (as mentioned earlier in the first case of `PyFrame_New`).

The newly loaded module will use `PyEval_EvalCode` to execute the code in the new module. As we can see, the `globals` and `locals` parameters passed to `PyEval_EvalCode` are actually the module's own `__dict__`, and the module sets `m.__dict__['__builtins__'] = PyEval_GetBuiltins()`.

Generally speaking, we can conclude that the modules imported from the `__main__` module will also inherit the `__builtins__` from `__main__`. This inheritance will be passed down in subsequent imports, ensuring that all modules and submodules loaded from `__main__` can share the same `__builtins__` from `__main__`.

So what if the function is called in a module? For functions in a module, when creating and calling them:

```c
// ceval.c
// Create a function
TARGET(MAKE_FUNCTION)
{
    v = POP(); /* code object */
```python
// Here, `f->f_globals` is equivalent to the module's own `globals`, as mentioned earlier, which is also equivalent to `m.__dict__`.
```
    x = PyFunction_New(v, f->f_globals);
    ...
}

PyObject *
PyFunction_New(PyObject *code, PyObject *globals)
{
    PyFunctionObject *op = PyObject_GC_New(PyFunctionObject,
                                        &PyFunction_Type);
    ...
// This is equivalent to `op->func_globals = globals = f->f_globals`
    op->func_globals = globals;     
}

// Call function
static PyObject *
fast_function(PyObject *func, PyObject ***pp_stack, int n, int na, int nk)
{
    PyCodeObject *co = (PyCodeObject *)PyFunction_GET_CODE(func);
    // globals = func->func_globals
    PyObject *globals = PyFunction_GET_GLOBALS(func);
    ...
// The `globals` argument is passed to `PyEval_EvalCodeEx`, which in turn is passed to `PyFrame_New` to create a new frame.
    return PyEval_EvalCodeEx(co, globals,
                             (PyObject *)NULL, (*pp_stack)-n, na,
                             (*pp_stack)-2*nk, nk, d, nd,
                             PyFunction_GET_CLOSURE(func));
}
```

When creating a function, the `f->f_globals` is stored in the `func_globals` variable of the function structure. As for the module `m`, `f->f_globals = m.__dict__`. When the function is executed, the `globals` parameter passed to `PyFrame_New` is the `func_globals` saved during creation, so `__builtins__` can naturally be obtained in `func_globals`.

By now, the passing of `__builtins__` can guarantee consistency. All modules, submodules, functions, stack frames, etc. can reference the same, that is, have the same built-in namespace.

Specify the execution of the `__main__` module.

We already know that the `__builtins__` of the `__main__` module can be passed to all submodules, functions, and stack frames. When executing `python a.py` on the command line, Python will execute `a.py` as the `__main__` module. How is this achieved?

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
// Try executing code using the importer of the module
    if (filename != NULL) {
        sts = RunMainFromImporter(filename);
    }
    ...
```python
// Generally, we use this to execute our own py file
```
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
// Set the __file__ attribute
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
```python
// Read code object `co` from a pyc file and execute the code
// PyEval_EvalCode also calls PyFrame_New to create a new frame
```
    v = PyEval_EvalCode(co, globals, locals);
    ...
}
```

When executing `python a.py`,  it generally goes to `PyRun_SimpleFileExFlags`. Inside `PyRun_SimpleFileExFlags`, `__main__.__dict__` is extracted as the `globals` and `locals` for code execution, and ultimately passed into `PyFrame_New` to create a new stack frame for executing `a.py`. Combining what we mentioned earlier about passing `__builtins__` in modules and functions, it allows the subsequent executed code to share the same `current_frame->f_builtins = __main__.__builtins__.__dict__`.


## Revisiting Restricted Execution

Before version 2.3, Python provided [Restricted Execution](https://docs.python.org/2.7/library/restricted.html) based on the characteristics of `__builtins__`. It can be considered that the reason `__builtins__` is designed as a module object in the `__main__` module and a `dict` object in other modules is to achieve Restricted Execution.

Consider this situation: If we can freely customize our `__builtin__` module and set it as `__main__.__builtins__`, it means that all subsequent code executions will use our customized module. We can customize specific versions of built-in functions and types such as `open`, `__import__`, `file`, etc. Furthermore, can this approach help us restrict the permissions of executing code and prevent it from making unsafe function calls or accessing unsafe files?

`Python` had already made this attempt at that time, and the module that implements this functionality is called `rexec`.

### `rexec`

I have no intention of going into too much detail about the implementation of `rexec` because the principle has already been explained in the previous text, and this module itself has been deprecated. I am just providing a brief summary of the key code here for easy reference.


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

The `r_execfile` function will execute the file as if it were the `__main__` module, with the difference that `__main__` has been customized. Inside `self.add_module('__main__')`, the module's `m.__builtins__` is set to `self.modules['__builtin__']`. The `__builtin__` is generated by `make_builtin` and it replaces the `__import__`, `reload`, `open` functions, and removes the `file` type. This way, we can control the access of the code being executed to the built-in namespace.

For some built-in modules, `rexec` has also been customized to protect against unsafe access, such as the `sys` module, which retains only a portion of its objects, and through the customized `self.loader` and `self.importer`, achieves priority loading of customized modules when `import` is called.

If you are interested in the details of the code, please refer to the relevant source code.

### Failure of `rexec`

In the previous text, it was mentioned that `rexec` has been deprecated since `Python 2.3` because this method has been proven to be unfeasible. With curiosity, let's briefly trace back:

Someone in the community reported a [Bug](https://mail.python.org/pipermail/python-dev/2002-December/031160.html), which triggered a discussion among the developers:

*在社区有人报告了 [Bug](https://mail.python.org/pipermail/python-dev/2002-December/031160.html)，并引发了开发者之间的讨论：*
    > it's never going to be safe, and I doubt it's very useful as long as it's not safe.

    > Every change is a potential security hole.

    > it's hard to predict what change is going to break it.

    > I don't expect you'll ever reach the point where it'll be wise to advertise this as safe.  I certainly won't.

    >  this is only a useful occupation if you expect to eventually reach a point where you expect that there aren't any security flaws left.  Jeremy & I both doubt that Python will ever reach that level, meaning that the whole exercise of fixing security flaws is a waste of time (if you know you *can't* make it safe, don't waste time trying).

    > I agree (but I have said that in past) the best thing is to deprecate/rip out rexec.

    > The code will still be in older versions if someone decides to pick it up and work on it as a separate project.

The cause of this bug is that `Python` introduced the new-style class `object`, which caused `rexec` to not function properly. Therefore, the developers expressed that in the foreseeable future, it will be difficult to avoid such situations, and any modifications may lead to vulnerabilities or breaches of the restrictions of `rexec`. Basically, it is almost impossible to achieve the vision of providing a secure environment without vulnerabilities. Developers will constantly need to patch and fix, wasting a lot of time. Eventually, the `rexec` module was deprecated and `Python` no longer provides similar functionality. However, the setting of `__builtins__` was preserved due to compatibility and other issues.

Later, around 2010, a programmer launched [pysandbox](https://github.com/vstinner/pysandbox), which aimed to provide a Python sandbox environment as an alternative to `rexec`. However, 3 years later, the author voluntarily abandoned this project and provided a detailed explanation of why they considered it a failure: [The pysandbox project is broken](https://mail.python.org/pipermail/python-dev/2013-November/130132.html). Other authors have also written articles summarizing the failure of this project: [The failure of pysandbox](https://lwn.net/Articles/574215/). If you are interested, you can read the original texts for more details. Here are some excerpts to help you understand:

> After having work during 3 years on a pysandbox project to sandbox untrusted code, I now reached a point where I am convinced that pysandbox is broken by design. Different developers tried to convinced me before that pysandbox design is unsafe, but I had to experience it myself to be convineced.

> I now agree that putting a sandbox in CPython is the wrong design. There are too many ways to escape the untrusted namespace using the various introspection features of the Python language. To guarantee the [safety] of a security product, the code should be [carefully] audited and the code to review must be as small as possible. Using pysandbox, the "code" is the whole Python core which is a really huge code base. For example, the Python and Objects directories of Python 3.4 contain more than 126,000 lines of C code.

> The security of pysandbox is the security of its weakest part. A single bug is enough to escape the whole sandbox.

> pysandbox cannot be used in practice. To protect the untrusted namespace, pysandbox installs a lot of different protections. Because of all these protections, it becomes hard to write Python code. Basic features like "del dict[key]" are denied. Passing an object to a sandbox is not possible to sandbox, pysandbox is unable to proxify arbitary objects. For something more complex than evaluating "1+(2*3)", pysandbox cannot be used in practice, because of all these protections.

The author of `pysandbox` believes that it is a flawed design to have a sandbox environment in Python. There are too many ways to escape from the sandbox, and Python provides rich language features. The code base of CPython is large and it is basically impossible to guarantee sufficient security. The development process of `pysandbox` has been constantly patching, with too many restrictions. As a result, the author believes that `pysandbox` is no longer practical to use because many syntax features and functionalities are restricted and cannot be used, such as the simple `del dict[key]`.

## Way out for Restricted Execution

Since methods like `rexec` and __pysandbox__ that use Patch Python to provide a sandbox environment are no longer feasible, I can't help but wonder: how can we provide a usable sandbox environment for Python?

Here, I have continued to gather some other implementation methods or cases for easy reference and consultation:



* [PyPy](https://doc.pypy.org/en/latest/sandbox.html) has a [branch](https://foss.heptapod.net/pypy/pypy/-/tree/branch/sandbox-2) that provides sandbox functionality. Combined with the additional [sandboxlib](https://foss.heptapod.net/pypy/sandboxlib), you can compile your own version of PyPy with a sandbox environment. If you're interested, you can try configuring it yourself. You can refer to some [instructions](https://foss.heptapod.net/pypy/pypy/-/issues/3192) here for guidance. The implementation principle of PyPy is to create a subprocess where all inputs, outputs, and system calls are redirected to an external process. This external process controls these permissions and can also control memory and CPU usage. It's important to note that this branch hasn't had any new commits for a while, so please use it with caution.

* Use sandbox environment tools provided by the operating system. [seccomp](https://en.wikipedia.org/wiki/Seccomp) is a security tool provided by the Linux kernel. [libseccomp](https://github.com/seccomp/libseccomp/tree/main/src/python) provides Python bindings that can be embedded into code for use or use tools like [Firejail](https://firejail.wordpress.com/) that are based on seccomp to execute code. [AppArmor](https://apparmor.net/) is a Linux kernel security module that allows administrators to control the system resources and functionalities that programs can access, providing protection for the operating system. [codejail](https://github.com/openedx/codejail) is a Python sandbox environment based on AppArmor implementation, which you can try if interested. There are many similar tools available, but they are not listed here.

* Use sandbox virtual environments or containers. [Windows Sandbox](https://learn.microsoft.com/zh-cn/windows/security/threat-protection/windows-sandbox/windows-sandbox-overview), [LXC](https://linuxcontainers.org/), [Docker](https://www.docker.com/), etc. are not discussed here.

## Summary

Thank you for getting this far. We believe that all the questions listed at the beginning of the article have been answered. The text is a bit long, but we appreciate your patience.

> Original: <https://disenone.github.io/wiki>  
> This post is protected by [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by/4.0/deed.en) agreement, should be reproduced with attribution.


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
