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
- python
- __builtins__
- builtins
description: What's the difference between __builtin__ and __builtins__? Is __builtins__
  different in the main module compared to other modules? Why is it set to be different?
  Where is __builtins__ defined? In this article, we will explore some lesser-known
  facts about __builtins__ and discuss some related content that shouldn't be missed.
figures: []
---

<meta property="og:title" content="Python 杂谈 1 - 探究 __builtins__ - Disenone" />

##Introduction

We know that `__builtins__` itself is an object that exists in the global namespace, intentionally exposed by Python at the code level, and can be directly used anywhere in the code. But a little-known fact is that in the `main` module (also known as `__main__`, referring to the same module, which may be used interchangeably later), it refers to the `__builtin__` module, whereas in other modules, it represents `__builtin__.__dict__`, which is a bit perplexing. Although it's not recommended to use `__builtins__` directly, why do you bring up two scenarios? In this article, we will explore the origin of this setting and find answers to these questions: What is the difference between `__builtin__` and `__builtins__`? Why are `__builtins__` different in the `main` module and other modules? Where is `__builtins__` defined?


## `__builtin__`

Before discussing `__builtins__`, we need to take a look at what `__builtin__` is. `__builtin__` is the module that contains all the built-in objects. The built-in objects that we can directly use in Python are essentially objects in the `__builtin__` module, which are located in `__builtin__.__dict__`, corresponding to Python's built-in namespace. Remember this key point: `__builtin__` is a module. We can find the definition and usage of the `__builtin__` module in the Python source code (note that the Python source code mentioned below refers to the CPython-2.7.18 source code):

``` c
// pythonrun.c
void
Py_InitializeEx(int install_sigs)
{
    PyInterpreterState *interp;
    ...
// Initialize __builtin__
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

// Add built-in objects to the dictionary
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

When Python initializes, it calls `_PyBuiltin_Init` to create the `__builtin__` module and adds the built-in objects to it. The interpreter itself will refer to `interp->builtins = __buintin__.__dict__`, and the currently executing stack frame structure will also refer to `current_frame->f_builtins`. So, naturally, when executing code needs to find an object based on its name, Python will look in `current_frame->f_builtins` and be able to access all the built-in objects.

```c
// ceval.c
TARGET(LOAD_NAME)
{
// First look in the f->f_locals namespace
    ...
    if (x == NULL) {
    // Look for the global scope again
        x = PyDict_GetItem(f->f_globals, w);
        if (x == NULL) {
// Look for it in the built-in space
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

Finally, due to the name `__builtin__` being too confusing, it has been renamed to `builtins` in `Python3`.


## `__builtins__`

The behavior of `__builtins__` is a bit strange:
*In the `main` module (the `main` module, also known as the `environment where the top-level code is executed`, is the Python module specified by the user to run first. This is typically the module that we run from the command line using `python xxx.py`. Here, `xxx.py` is the module), `__builtins__ = __builtin__`.*
In other modules, `__builtins__ = __builtin__.__dict__`.

The same name, but behaving differently in different modules, can easily be confusing. However, as long as you understand this setup, it's enough to support you in using `__builtins__` in Python, and confusion will not affect your ability to write sufficiently secure code, such as:

``` python
def SetBuiltins(builtins, key, val):
    if isinstance(builtins, dict):
        builtins[key] = val
    else:
        setattr(builtins, key, val)

SetBuiltins(__builtins__, 'test', 1)
```

It's worth noting that it's actually not recommended to use `__builtins__`:

> __CPython implementation detail__: Users should not touch `__builtins__`; it is strictly an implementation detail. Users wanting to override values in the builtins namespace should import the `__builtin__` (no ‘s’) module and modify its attributes appropriately.

Of course, such doubts will eventually make you curious. That's why I've decided to continue exploring, which is also the reason for this article. The following content will delve deeply into the *CPython implementation detail*.

## Restricted Execution

Restricted Execution can be understood as executing unsafe code with limitations. The so-called restrictions can include limiting access to the network, I/O, and so on, to confine the code within a certain execution environment, controlling the code's execution permissions, and preventing it from impacting the external environment and system. A common use case is online code execution websites, such as this one: [pythonsandbox](https://pythonsandbox.dev/)。

As you guessed, the setting of `__builtins__` in Python is related to Restricted Execution. Python provided similar functionality prior to version 2.3 [Restricted Execution] as expected.(https://docs.python.org/2.7/library/restricted.html)Just because it was later confirmed to be unworkable, this feature had to be disabled. However, the code is still preserved in version 2.7.18, so we can go back and take a look.

First, let's take a look at the setting of `__builtins__` in the `Python` source code:

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

Set `__builtins__` in `__main__.__dict__`, if it does not exist already.
    if (PyDict_GetItemString(d, "__builtins__") == NULL) {
        PyObject *bimod = PyImport_ImportModule("__builtin__");
        if (bimod == NULL ||
            PyDict_SetItemString(d, "__builtins__", bimod) != 0)
            Py_FatalError("can't add __builtins__ to __main__");
        Py_XDECREF(bimod);
    }
}
```

In `initmain`, `Python` will set the `__builtins__` attribute for the `__main__` module by default to be equal to the `__builtin__` module, but if it already exists, it will be skipped and not reset. Taking advantage of this characteristic, we can modify `__main__.__builtins__` to change some built-in functionalities, in order to restrict the execution permissions of the code. The specific method is not mentioned for now, but let's take a look at how `__builtins__` is propagated.

##Passing `__builtins__`

When creating a new stack frame:

```c
PyFrameObject *
PyFrame_New(PyThreadState *tstate, PyCodeObject *code, PyObject *globals,
            PyObject *locals)
{
    ...
    if (back == NULL || back->f_globals != globals) {
// Use globals['__builtins__'] as the __builtins__ for the new stack frame
The `builtin_object` is the string '__builtins__'.
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
// Or directly inherit f_builtins from the upper stack frame
        builtins = back->f_builtins;
        assert(builtins != NULL && PyDict_Check(builtins));
        Py_INCREF(builtins);
    }
    ...
    f->f_builtins = builtins;
    f->f_globals = globals;
}
```

When creating a new stack frame, there are mainly two ways to handle `__builtins__`: one is when there is no upper-level stack frame, you take `globals['__builtins__']`; the other is to directly take `f_builtins` from the upper-level stack frame. In summary, under normal circumstances, the `__builtins__` set in `__main__` will be inherited by subsequent stack frames as if they were shared.

When importing the `import` module:

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

// Set the __builtins__ property for the new loaded module here
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

When `import`ing other modules, the `__builtins__` of that module will be set to the return value of `PyEval_GetBuiltins()`, which we have already mentioned, in most cases it is equivalent to `current_frame->f_builtins`. For `import` within the `__main__` module, `current_frame` is the stack frame of the `__main__` module, and `current_frame->f_builtins = __main__.__dict__['__builtins__']` (the first case mentioned in the previous section about `PyFrame_New`).

The newly loaded module will use `PyEval_EvalCode` to execute the code in the new module. You can see that the arguments `globals` and `locals` passed to `PyEval_EvalCode` are actually the module's own `__dict__`, and the module `m.__dict__['__builtins__'] = PyEval_GetBuiltins()`.

From a comprehensive view, we can infer that the modules imported starting from the `__main__` module will also inherit the `__builtins__` in `__main__` and pass it down in internal imports. This ensures that all modules and submodules loaded from `__main__` can share the same `__builtins__` from `__main__.

So what if the function is called within a module? For functions within a module, when creating and calling them:

```c
// ceval.c
// Create function
TARGET(MAKE_FUNCTION)
{
    v = POP(); /* code object */

// The `f->f_globals` here is equivalent to the module's own globals, as mentioned above, it is also equivalent to `m.__dict__`.
    x = PyFunction_New(v, f->f_globals);
    ...
}

PyObject *
PyFunction_New(PyObject *code, PyObject *globals)
{
    PyFunctionObject *op = PyObject_GC_New(PyFunctionObject,
                                        &PyFunction_Type);
    ...
// This is equivalent to op->func_globals = globals = f->f_globals
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
// Global variables are passed to PyEval_EvalCodeEx, which in turn passes them to PyFrame_New to create a new stack frame.
    return PyEval_EvalCodeEx(co, globals,
                             (PyObject *)NULL, (*pp_stack)-n, na,
                             (*pp_stack)-2*nk, nk, d, nd,
                             PyFunction_GET_CLOSURE(func));
}
```

When creating a function, the variable `f->f_globals` is stored in the function structure variable `func_globals`, and for the module `m`, `f->f_globals = m.__dict__`. When the function is executed, the `globals` parameter passed to `PyFrame_New` is the `func_globals` that was saved during creation, and `__builtins__` can naturally be obtained in `func_globals`.

So far, the propagation of `__builtins__` can ensure consistency. All modules, submodules, functions, stack frames, etc. can refer to the same one, which means they have the same built-in namespace.

##Specify execution of the `__main__` module.

We already know that the `__builtins__` of the `__main__` module can be passed to all submodules, functions, and stack frames. When executing `python a.py` from the command line, Python will execute `a.py` as the `__main__` module. How is this achieved?

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
// Typically, we use this to execute our own py files.
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
// Read code object co from pyc file and execute the code.
// PyEval_EvalCode also calls PyFrame_New to create a new frame.
    v = PyEval_EvalCode(co, globals, locals);
    ...
}
```

When executing `python a.py`, in general, it will reach `PyRun_SimpleFileExFlags`. Inside `PyRun_SimpleFileExFlags`, it will fetch `__main__.__dict__` as the `globals` and `locals` when executing the code, eventually passing it to `PyFrame_New` to create a new stack frame to execute `a.py`. Combined with what we mentioned earlier about passing `__builtins__` in modules and functions, this allows subsequent code executions to share the same `current_frame->f_builtins = __main__.__builtins__.__dict__`.


##Revisiting Restricted Execution

`Python` has provided [Restricted Execution] before version 2.3.(https://docs.python.org/2.7/library/restricted.html)It is made based on the characteristics of `__builtins__`. Alternatively, one can consider that the reason `__builtins__` is designed as a module object in the `__main__` module and as a `dict` object in other modules is to achieve __Restricted Execution__.

Consider this scenario: if we could freely customize our `__builtin__` module and set it as `__main__.__builtins__`, then all subsequent executed code would use our customized module. We would be able to customize specific versions of built-in functions and types such as `open`, `__import__`, `file`, and so on. Furthermore, could this approach help us restrict the permissions for executing code, preventing it from making unsafe function calls or accessing unsafe files?

`Python` had already made this attempt at that time, and the module that implements this functionality is called `rexec`.

### `rexec`

I don't intend to go into too much detail about the implementation of `rexec`, because the principle has already been explained in the previous text, and this module itself is deprecated. I will simply provide a brief summary of some key code snippets for easy reference.


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

The `r_execfile` function executes the file as the `__main__` module, except `__main__` is customized. In the `self.add_module('__main__')` code, the module's `m.__builtins__` is set to `self.modules['__builtin__']`. The `__builtin__` is custom-generated by `make_builtin`, replacing the `__import__`, `reload`, and `open` functions and deleting the `file` type. This way, we can control the access to the built-in namespace by the code to be executed.

For some built-in modules, `rexec` has also been customized to protect against unsafe access. For example, the `sys` module only keeps a portion of its objects and uses the customized `self.loader` and `self.importer` to prioritize loading the customized modules when importing.

If you are interested in the details of the code, please refer to the relevant source code yourself.

###The failure of `rexec`

The previous mentioned, `Python 2.3` and later, `rexec` has been deprecated, because this approach has been proven to be unfeasible. With curiosity, let's briefly trace the origin:

* Someone reported a [Bug] in the community.(https://mail.python.org/pipermail/python-dev/2002-December/031160.html)And triggered a discussion among developers:

    > it's never going to be safe, and I doubt it's very useful as long as it's not safe.

    > Every change is a potential security hole.

    > it's hard to predict what change is going to break it.

    > I don't expect you'll ever reach the point where it'll be wise to advertise this as safe.  I certainly won't.

    >  this is only a useful occupation if you expect to eventually reach a point where you expect that there aren't any security flaws left.  Jeremy & I both doubt that Python will ever reach that level, meaning that the whole exercise of fixing security flaws is a waste of time (if you know you *can't* make it safe, don't waste time trying).

    > I agree (but I have said that in past) the best thing is to deprecate/rip out rexec.

    > The code will still be in older versions if someone decides to pick it up and work on it as a separate project.

The cause of this bug was that `Python` introduced the new-style class `object`, which resulted in `rexec` not functioning properly. As a result, developers expressed that in the foreseeable future, it would be difficult to avoid this situation, as any changes might lead to `rexec` vulnerabilities, malfunctioning, or breaches of permission restrictions, making it practically impossible to provide a secure environment without vulnerabilities. Developers would constantly need to fix and patch, wasting a considerable amount of time. In the end, the `rexec` module was abandoned, and `Python` did not provide similar functionality again. However, the setting of `__builtins__` was retained due to compatibility issues and other reasons.

In the back, around 2010, a programmer launched [pysandbox].(https://github.com/vstinner/pysandbox)，dedicated to providing a `Python` sandbox environment that can replace `rexec`. However, after 3 years, the author voluntarily abandoned this project and detailed why the author believed the project had failed: [The pysandbox project is broken](https://mail.python.org/pipermail/python-dev/2013-November/130132.html)，other authors have also written articles summarizing the failure of this project: [The failure of pysandbox](https://lwn.net/Articles/574215/)If you're interested, you can take a look at the original text for more details. I'll also provide some excerpts here to help you understand:

> After having work during 3 years on a pysandbox project to sandbox untrusted code, I now reached a point where I am convinced that pysandbox is broken by design. Different developers tried to convinced me before that pysandbox design is unsafe, but I had to experience it myself to be convineced.

> I now agree that putting a sandbox in CPython is the wrong design. There are too many ways to escape the untrusted namespace using the various introspection features of the Python language. To guarantee the [safety] of a security product, the code should be [carefully] audited and the code to review must be as small as possible. Using pysandbox, the "code" is the whole Python core which is a really huge code base. For example, the Python and Objects directories of Python 3.4 contain more than 126,000 lines of C code.

> The security of pysandbox is the security of its weakest part. A single bug is enough to escape the whole sandbox.

> pysandbox cannot be used in practice. To protect the untrusted namespace, pysandbox installs a lot of different protections. Because of all these protections, it becomes hard to write Python code. Basic features like "del dict[key]" are denied. Passing an object to a sandbox is not possible to sandbox, pysandbox is unable to proxify arbitary objects. For something more complex than evaluating "1+(2*3)", pysandbox cannot be used in practice, because of all these protections.

The author of **pysandbox** believes that creating a sandbox environment within `Python` is a flawed design. There are too many ways to escape from the sandbox, `Python` offers rich language features, and the extensive codebase of `CPython` makes it nearly impossible to ensure sufficient security. The development of **pysandbox** has involved continuously patching the system with so many restrictions that the author now believes it is no longer practical to use. Many syntax features and functionalities, such as simple operations like `del dict[key]`, have been restricted and cannot be used.

##**Restricted Execution** Where is the way out

Since methods like `rexec` and __pysandbox__ that provide sandbox environments by patching Python are no longer feasible, I can't help but wonder: How can Python be provided with a usable sandbox environment?

Here I continue to collect some other implementation methods or cases for easy reference and consultation:

* [PyPy](https://doc.pypy.org/en/latest/sandbox.html)There is a [branch](https://foss.heptapod.net/pypy/pypy/-/tree/branch/sandbox-2)Provided sandbox functionality, combined with additional [sandboxlib](https://foss.heptapod.net/pypy/sandboxlib), you can compile a version of PyPy with a sandbox environment by yourself. If you are interested, you can try to configure it on your own, referring to some [instructions] here.(https://foss.heptapod.net/pypy/pypy/-/issues/3192)The principle behind PyPy’s implementation is to create a subprocess, where all the input, output, and system calls are redirected to an external process, which controls those permissions. Additionally, it can also control the usage of memory and CPU. It's worth noting that this branch has not had any new commits for some time, so please use it with caution.

*By using the sandbox environment tool provided by the operating system. [seccomp]*(https://en.wikipedia.org/wiki/Seccomp)It is a security tool provided by the Linux kernel, [libseccomp].(https://github.com/seccomp/libseccomp/tree/main/src/python)Provided Python bindings, which can be embedded into code for use; or use tools based on seccomp to execute code, such as [Firejail].(https://firejail.wordpress.com/). [AppArmor](https://apparmor.net/)It is a Linux kernel security module that allows administrators to control the system resources and functionality that programs can access, thus protecting the operating system. [codejail](https://github.com/openedx/codejail)It's a Python sandbox environment based on AppArmor. Feel free to give it a try. There are many similar tools out there, but I won't list them all here.

* Use sandbox virtual environment or containers. [Windows Sandbox](https://learn.microsoft.com/zh-cn/windows/security/threat-protection/windows-sandbox/windows-sandbox-overview)`,`[LXC](https://linuxcontainers.org/), [Docker](https://www.docker.com/)等等，这里不再详述。

##Summary

This article is a bit long, thank you for reading this far, I believe all the questions raised at the beginning of the article have been fully answered.

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki_blog/issues/new) if any omissions.
