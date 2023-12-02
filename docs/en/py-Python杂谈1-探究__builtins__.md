---
layout: post
title: Python Rambles 1 - Exploring __builtins__
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
  facts about __builtins__ and also touch upon some related topics. Don't miss out.
figures: []
---

<meta property="og:title" content="Python 杂谈 1 - 探究 __builtins__ - Disenone" />

## Prologue

We know that `__builtins__` itself is an object already present in the global namespace, intentionally exposed by Python to the code level, and can be directly used anywhere in the code. However, a somewhat obscure fact is that in the `main` module (also known as `__main__`, referring to the same module, which may be used interchangeably later on), `__builtins__` refers to the module `__builtin__`. But in other modules, it represents `__builtin__.__dict__`, which is a bit puzzling. Although it is not recommended by the official documentation to use `__builtins__` directly, why are there two different situations? In this article, we will delve into the origins of this design and find answers to these questions: What is the difference between `__builtin__` and `__builtins__`? Why are `__builtins__` different in the `main` module compared to other modules? Where is `__builtins__` defined?


## `__builtin__`

Before discussing `__builtins__`, we need to take a look at what `__builtin__` is. `__builtin__` is a module that contains all the built-in objects. The built-in objects we can directly use in Python are essentially objects in the `__builtin__` module, which are stored in `__builtin__.__dict__`, corresponding to Python's built-in namespace. Remember this key point: `__builtin__` is a module. We can find the definition and usage of the `__builtin__` module in the Python source code (please note that the Python source code mentioned below refers to CPython-2.7.18 source code):

``` c
// pythonrun.c
void
Py_InitializeEx(int install_sigs)
{
    PyInterpreterState *interp;
    ...

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

// Add built-in objects to the dict
    ...
}

// ceval.c
// Get built-ins
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

`Python` initializes by calling `_PyBuiltin_Init` to create the `__builtin__` module and add the built-in objects to it. The interpreter itself holds a reference to `interp->builtins = __buintin__.__dict__`, while the current execution frame structure also holds a reference to `current_frame->f_builtins`. Therefore, when executing code and needing to find objects by name, `Python` will naturally look inside `current_frame->f_builtins` and gain access to all the built-in objects:

```c
// ceval.c
TARGET(LOAD_NAME)
{
// First, search in the name space of f->f_locals
    ... 
    if (x == NULL) {
// Look for the global namespace again.
        x = PyDict_GetItem(f->f_globals, w);
        if (x == NULL) {
// Here, we will look up the built-in space.
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

Finally, due to the confusion caused by the name `__builtin__`, it has been renamed to `builtins` in Python 3.


## `__builtins__`

The behavior of `__builtins__` is a bit strange:
* In the `main` module (the module where the highest-level code execution environment is specified by the user), `__builtins__ = __builtin__`;
* In other modules, `__builtins__ = __builtin__.__dict__`.

The same name may have different behaviors in different modules, which can be confusing. However, as long as you understand this concept, it is sufficient to support the use of `__builtins__` in Python. This confusion will not affect your ability to write secure code, such as:

``` python
def SetBuiltins(builtins, key, val):
    if isinstance(builtins, dict):
        builtins[key] = val
    else:
        setattr(builtins, key, val)

SetBuiltins(__builtins__, 'test', 1)
```

It should be noted that it is actually not recommended to use `__builtins__`:

__CPython implementation detail__: Users should not touch `__builtins__`; it is strictly an implementation detail. Users wanting to override values in the builtins namespace should import the `__builtin__` (no ‘s’) module and modify its attributes appropriately.

Of course, such doubts will inevitably make you restless one day. That's why I have decided to continue to explore and consequently, this article came into being. The following content will delve into the *CPython implementation detail*.

## Restricted Execution

Restricted Execution can be understood as executing unsafe code with restrictions. The term "restricted" refers to limitations on aspects such as network and IO operations, which confines the code to a specific execution environment. This control over code execution permissions prevents the code from impacting external environments and systems. A common use case for this is online code execution websites, such as [pythonsandbox](https://pythonsandbox.dev/).

As you guessed, the setting of `__builtins__` in `Python` is related to Restricted Execution. Before version 2.3, `Python` had provided similar functionality called Restricted Execution [Restricted Execution](https://docs.python.org/2.7/library/restricted.html), but it was later proven to be impractical and had to be deprecated. However, the code is still present in version 2.7.18, so we can dig into it.

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

# Set __main__.__dict__['__builtins__'], if it already exists, skip
    if (PyDict_GetItemString(d, "__builtins__") == NULL) {
        PyObject *bimod = PyImport_ImportModule("__builtin__");
        if (bimod == NULL ||
            PyDict_SetItemString(d, "__builtins__", bimod) != 0)
            Py_FatalError("can't add __builtins__ to __main__");
        Py_XDECREF(bimod);
    }
}
```

In `initmain`, `Python` sets the `__builtins__` attribute for the `__main__` module by default, which is equal to the `__builtin__` module. However, if it already exists, it will not be reset. Taking advantage of this feature, we can modify some built-in functionalities by modifying `__main__.__builtins__` in order to restrict the execution permissions of the code. The specific method will not be discussed here. Let's take a look at how `__builtins__` is passed.

## `__builtins__` Passing

When creating a new stack frame:

```c
PyFrameObject *
PyFrame_New(PyThreadState *tstate, PyCodeObject *code, PyObject *globals,
            PyObject *locals)
{
    ...
    if (back == NULL || back->f_globals != globals) {
        // Take globals['__builtins__'] as the __builtins__ of the new stack frame
        // builtin_object is the string '__builtins__'
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
// Or directly inherit f_builtins from the upper-level stack frame
        builtins = back->f_builtins;
        assert(builtins != NULL && PyDict_Check(builtins));
        Py_INCREF(builtins);
    }
    ...
    f->f_builtins = builtins;
    f->f_globals = globals;
}
```

When creating a new stack frame, there are two main cases to consider for handling `__builtins__`: 
- In the case where there is no higher-level stack frame, `globals['__builtins__']` is taken.
- In the other case, the `f_builtins` of the higher-level stack frame is directly taken. 

In summary, under normal circumstances, the `__builtins__` set in `__main__` will be inherited by subsequent stack frames, essentially sharing the same set.

When importing a `module`:

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

// Set the __builtins__ property for newly loaded modules here.
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

When importing other modules, the `__builtins__` of the module is set to the return value of `PyEval_GetBuiltins()` function, which we have mentioned earlier, and in most cases it is equivalent to `current_frame->f_builtins`. For the `import` within the `__main__` module, the `current_frame` refers to the stack frame of the `__main__` module and `current_frame->f_builtins = __main__.__dict__['__builtins__']` (as mentioned in the previous section of `PyFrame_New`).

The newly loaded module will use `PyEval_EvalCode` to execute the code in the new module. As we can see, the `globals` and `locals` parameters passed to `PyEval_EvalCode` are actually the module's own `__dict__`, and the module `m.__dict__['__builtins__'] = PyEval_GetBuiltins()`.

Overall, we can see that modules imported starting from the `__main__` module will also inherit the `__builtins__` from `__main__` and pass it down in internal imports. This ensures that all modules and submodules loaded from `__main__` can share the same `__builtins__` from `__main__`.

So what about functions called within a module? For functions within a module, when creating and calling them:

```c
// ceval.c
// Create a function
TARGET(MAKE_FUNCTION)
{
    v = POP(); /* code object */
// The `f->f_globals` here is equivalent to the module's own globals, as mentioned earlier, it is also equivalent to `m.__dict__`.
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

// Call Function
static PyObject *
fast_function(PyObject *func, PyObject ***pp_stack, int n, int na, int nk)
{
    PyCodeObject *co = (PyCodeObject *)PyFunction_GET_CODE(func);
    // globals = func->func_globals
    PyObject *globals = PyFunction_GET_GLOBALS(func);
    ...
\[to_be_replaced_0\] will be passed to PyEval_EvalCodeEx, and it will be further passed to PyFrame_New to create a new stack frame.
    return PyEval_EvalCodeEx(co, globals,
                             (PyObject *)NULL, (*pp_stack)-n, na,
                             (*pp_stack)-2*nk, nk, d, nd,
                             PyFunction_GET_CLOSURE(func));
}
```

When creating a function, the `f->f_globals` is stored in the `func_globals` variable of the function structure. As for the module `m`, `f->f_globals = m.__dict__`. When the function is executed, the `globals` parameter passed to `PyFrame_New` is the `func_globals` saved during creation, and `__builtins__` can naturally be accessed in `func_globals`.

So far, the passing of `__builtins__` can ensure consistency, all modules, submodules, functions, stack frames, etc. can refer to the same one, that is, they have the same built-in namespace.

## Specify `__main__` module execution

We already know that the `__builtins__` of the `__main__` module can be passed to all submodules, functions, and stack frames. When executing `python a.py` at the command line, Python executes `a.py` as the `__main__` module. So how is this achieved?

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
// Try executing code with the module's importer

    if (filename != NULL) {
        sts = RunMainFromImporter(filename);
    }
    ...
// Generally, we use this to execute our own py files.
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
// Read code object `co` from pyc file and execute the code
// PyEval_EvalCode also calls PyFrame_New to create a new frame inside

    v = PyEval_EvalCode(co, globals, locals);
    ...
}
```

When executing `python a.py`, in general, it will go to `PyRun_SimpleFileExFlags`. Inside `PyRun_SimpleFileExFlags`, it retrieves `__main__.__dict__` as the `globals` and `locals` for code execution. Finally, it is passed to `PyFrame_New` to create a new stack frame for executing `a.py`. Combining with the mention of `__builtins__` in the previous context, we can allow subsequent code to share the same `current_frame->f_builtins = __main__.__builtins__.__dict__`.


## Revisiting Restricted Execution

Before version 2.3, Python previously provided [Restricted Execution](https://docs.python.org/2.7/library/restricted.html), which was based on the feature of `__builtins__`. Alternatively, it can be understood that the reason why `__builtins__` is designed to be a module object in the `__main__` module and a `dict` object in other modules is to enable the implementation of Restricted Execution.

Consider this situation: If we could freely customize our `__builtin__` module and set it as `__main__.__builtins__`, then all subsequent executed code would use our customized module. We could customize specific versions of built-in functions and types such as `open`, `__import__`, and `file`. Furthermore, could this approach help us limit the permissions of executed code, preventing it from making unsafe function calls or accessing unsafe files?

`Python` had already made this attempt at that time, and the module that implements this functionality is called `rexec`.

### `rexec`

I have no intention of going into too much detail about the implementation of `rexec`, because its principles have already been explained in the previous section, and this module itself has been deprecated. I will only provide a brief summary of some key code snippets for easy reference.


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

The `r_execfile` function executes a file as the `__main__` module, except that `__main__` is customized. Inside `self.add_module('__main__')`, the module's `m.__builtins__` is set to `self.modules['__builtin__']`. This `__builtin__` is customized and generated by `make_builtin`, which replaces the `__import__`, `reload`, `open` functions, and removes the `file` type. This way, we can control the access to the built-in namespace by the code being executed.

For some built-in modules, `rexec` has also made customizations to protect against unsafe access, such as the `sys` module, which only retains a portion of its objects. It achieves prioritized loading of custom modules during the `import` process through the customized `self.loader` and `self.importer`.

If you are interested in the details of the code, please refer to the relevant source code on your own.

### Failure of `rexec`

In the previous text, it was mentioned that `rexec` has been deprecated since `Python 2.3` because this approach has been proven to be unworkable. With curiosity, let's briefly trace its origins:

Someone in the community reported a [Bug](https://mail.python.org/pipermail/python-dev/2002-December/031160.html), sparking a discussion among developers.
    > it's never going to be safe, and I doubt it's very useful as long as it's not safe.

    > Every change is a potential security hole.

    > it's hard to predict what change is going to break it.

    > I don't expect you'll ever reach the point where it'll be wise to advertise this as safe.  I certainly won't.

    >  this is only a useful occupation if you expect to eventually reach a point where you expect that there aren't any security flaws left.  Jeremy & I both doubt that Python will ever reach that level, meaning that the whole exercise of fixing security flaws is a waste of time (if you know you *can't* make it safe, don't waste time trying).

    > I agree (but I have said that in past) the best thing is to deprecate/rip out rexec.

    > The code will still be in older versions if someone decides to pick it up and work on it as a separate project.

The cause of this Bug is that `Python` introduced the new-style class `object`, which caused `rexec` to not function properly. As a result, developers expressed that in the foreseeable future, it would be difficult to avoid this situation; any modifications could potentially lead to vulnerabilities in `rexec`, rendering it unable to function properly or breach its permission restrictions. Essentially, it was not feasible to provide a secure environment without vulnerabilities, and developers would have to constantly patch and fix issues, wasting a significant amount of time. Ultimately, the `rexec` module was deprecated, and `Python` no longer provides similar functionality. However, due to compatibility and other issues, the setting for `__builtins__` was kept unchanged.

Afterwards, around 2010, a programmer launched [pysandbox](https://github.com/vstinner/pysandbox), aiming to provide a Python sandbox environment that could replace `rexec`. However, three years later, the author voluntarily abandoned this project and explained in detail why the author considered it a failure: [The pysandbox project is broken](https://mail.python.org/pipermail/python-dev/2013-November/130132.html). Other authors have also written articles summarizing the failure of this project: [The failure of pysandbox](https://lwn.net/Articles/574215/). If you are interested, you can read the original texts for more details. Here are some summaries to help you understand.

> After having work during 3 years on a pysandbox project to sandbox untrusted code, I now reached a point where I am convinced that pysandbox is broken by design. Different developers tried to convinced me before that pysandbox design is unsafe, but I had to experience it myself to be convineced.

> I now agree that putting a sandbox in CPython is the wrong design. There are too many ways to escape the untrusted namespace using the various introspection features of the Python language. To guarantee the [safety] of a security product, the code should be [carefully] audited and the code to review must be as small as possible. Using pysandbox, the "code" is the whole Python core which is a really huge code base. For example, the Python and Objects directories of Python 3.4 contain more than 126,000 lines of C code.

> The security of pysandbox is the security of its weakest part. A single bug is enough to escape the whole sandbox.

> pysandbox cannot be used in practice. To protect the untrusted namespace, pysandbox installs a lot of different protections. Because of all these protections, it becomes hard to write Python code. Basic features like "del dict[key]" are denied. Passing an object to a sandbox is not possible to sandbox, pysandbox is unable to proxify arbitary objects. For something more complex than evaluating "1+(2*3)", pysandbox cannot be used in practice, because of all these protections.

The author of `pysandbox` believes that it is a flawed design to have a sandbox environment in Python, as there are too many ways to escape from the sandbox. Python provides a rich set of language features, and the code base of CPython is so extensive that it is practically impossible to ensure sufficient security. The development process of `pysandbox` has been primarily focused on patching and adding restrictions, to the point where the author believes that `pysandbox` is no longer practical to use. Many syntax features and functionalities, such as simple `del dict[key]`, are restricted and cannot be used.

## Where is the way out for Restricted Execution

Since the methods of providing sandbox environment through Patch Python like `rexec` and `pysandbox` are no longer viable, I can't help but wonder: How can we provide a usable sandbox environment for Python?

Here, I have collected some additional implementation methods or case studies for easy reference and consultation:



* [PyPy](https://doc.pypy.org/en/latest/sandbox.html) has a [branch](https://foss.heptapod.net/pypy/pypy/-/tree/branch/sandbox-2) that provides sandbox functionality. By combining it with additional [sandboxlib](https://foss.heptapod.net/pypy/sandboxlib), you can compile your own version of PyPy with a sandbox environment. If you're interested, you can try configuring it yourself. Refer to some [instructions](https://foss.heptapod.net/pypy/pypy/-/issues/3192) here for guidance. The underlying principle of PyPy's implementation is to create a subprocess that redirects all input, output, and system calls to an external process, which controls these permissions. Additionally, you can also control the memory and CPU usage. It's worth noting that this branch hasn't seen any recent commits, so please use it with caution.

Using sandboxing tools provided by the operating system. [Seccomp](https://en.wikipedia.org/wiki/Seccomp) is a security tool provided by the Linux kernel, and [libseccomp](https://github.com/seccomp/libseccomp/tree/main/src/python) offers Python bindings that can be embedded into the code for use; alternatively, you can use tools based on seccomp to execute the code, such as [Firejail](https://firejail.wordpress.com/). [AppArmor](https://apparmor.net/) is a Linux kernel security module that allows administrators to control the system resources and functionality that a program can access, thus protecting the operating system. [Codejail](https://github.com/openedx/codejail) is a Python sandbox environment based on AppArmor, which you can try if you are interested. There are many similar tools available, but we won't list them all here.

* Use sandbox virtual environments or containers. [Windows Sandbox](https://learn.microsoft.com/en-us/windows/security/threat-protection/windows-sandbox/windows-sandbox-overview), [LXC](https://linuxcontainers.org/), [Docker](https://www.docker.com/), and so on, are not covered in detail here.

## Summary

This text is a bit long, thank you for reading this far, I believe all the questions listed at the beginning of the article have been answered.

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
