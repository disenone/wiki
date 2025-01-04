---
layout: post
title: Python 閒談 1 - 探究 __builtins__
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
description: __builtins__ 與 __builtins__ 有什麼區別？__builtins__ 在 main 模組跟其他模組是不同的？為什麼會設定成不同？__builtins__
  是在哪裡定義的？本文我們來探討一下關於 __builtins__ 的冷知識，並且還有一些引申的內容，不容錯過。
figures: []
---

<meta property="og:title" content="Python 杂谈 1 - 探究 __builtins__ - Disenone" />

##前言

我們知道，`__builtins__` 本身就是全域命名空間中的一個物件，是 `Python` 故意曝露出來給程式碼層級使用的，在程式的任何地方都可以直接使用。但有點冷門的資訊是，`__builtins__` 在 `main` 模組（也就是 `__main__`，指的都是同一個模組，後文可能會混用）裡面是 `__builtin__` 這個模組，但在其他模組裡面，它代表的是 `__builtin__.__dict__`，這點有點令人摸不著頭腦。雖然官方不建議直接使用 `__builtins__`，但你給我搞兩種情況是怎麼回事？本文我們就來盤一盤這個設定的由來，在這個過程中，我們還可以找到這些問題的答案：`__builtin__` 跟 `__builtins__` 有什麼區別？`__builtins__` 在 `main` 模組跟其他模組為什麼會設定成不同？`__builtins__` 是在哪裡定義的？


## `__builtin__`

在討論 `__builtins__` 之前，我們需要先看看 `__builtin__` 是什麼。`__builtin__` 是存放所有內建物件的模組，我們平常可以直接使用的 Python 內建物件，本質上都是 `__builtin__` 模組裡的物件，即放在 `__builtin__.__dict__` 裡，對應著的是 Python 的內建命名空間。記住這個關鍵知識點：`__builtin__` 是一個模組 module。我們可以在 Python 源碼中找到 `__builtin__` 模組的定義和使用（注意，下文提到的 Python 源碼，都是指 CPython-2.7.18 源碼）：

``` c
// pythonrun.c
void
Py_InitializeEx(int install_sigs)
{
    PyInterpreterState *interp;
    ...
初始化 __builtin__
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

為 dict 添加內置對象
    ...
}

// ceval.c
獲取內建功能
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

Python 初始化時會呼叫 `_PyBuiltin_Init` 來建立 `__builtin__` 模組，並在其中加入內建的物件，直譯器本身會參考 `interp->builtins = __buintin__.__dict__`，目前執行的堆疊框架結構同時也會參考一份 `current_frame->f_builtins`。因此，當執行程式碼需要根據名稱尋找物件時，Python 就會查找 `current_frame->f_builtins` ，自然就能取得所有的內建物件：

```c
// ceval.c
TARGET(LOAD_NAME)
{
// 優先在 f->f_locals 命名空間中尋找
    ...
    if (x == NULL) {
// 尋找全域空間
        x = PyDict_GetItem(f->f_globals, w);
        if (x == NULL) {
請到內部空間尋找。
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

最後，由於 `__builtin__` 這個名字實在是太具誤導性，`Python3` 中已經更名為 `builtins`。


## `__builtins__`

`__builtins__` 的表現有點奇怪：
在 `main` 模組中（`main` 模組，或者叫`最高層級程式碼執行所在環境`，是使用者指定最先啟動執行的 `Python` 模組，也就是通常我們在命令列執行 `python xxx.py` 時，`xxx.py` 這個模組），`__builtins__ = __builtin__`；
在其他模塊中 `__builtins__ = __builtin__.__dict__`。

相同的名字，在不同的模組裡卻表現出不同的特性，這樣的安排常讓人感到疑惑。但只要理解了這個機制，就能夠安心在 `Python` 中使用 `__builtins__`，疑惑並不會影響你寫出足夠安全的程式碼，舉例如下：

``` python
def SetBuiltins(builtins, key, val):
    if isinstance(builtins, dict):
        builtins[key] = val
    else:
        setattr(builtins, key, val)

SetBuiltins(__builtins__, 'test', 1)
```

需要注意，實際上並不建議使用 `__builtins__`：

> CPython 實作細節：使用者不應該觸碰 `__builtins__`；這僅是一個實作細節。想要覆蓋內建命名空間中的數值的使用者應該導入 `__builtin__`（無 's'）模組並適當修改其屬性。

當然，這樣的疑惑，總有一天會讓你心癢難耐，我這裡就決定繼續探究下去，也因為這樣，才有了這篇文章。我們接下來的內容會深入到 __CPython implementation detail__ 中去。

## Restricted Execution

受限執行可視為有限制地執行不安全的程式碼，限制可能包括網絡、輸入輸出等，將程式碼限制在特定的執行環境中，控制程式執行權限，防止程式影響外部環境和系統。常見的使用案例是一些線上程式執行網站，例如這個：[pythonsandbox](https://pythonsandbox.dev/)I cannot translate the characters because they do not contain any meaningful content.

與你推測的一樣，`Python` 對 `__builtins__` 的設定與受限制執行有關。在 `Python` 2.3 版本之前，曾經提供過類似功能 [Restricted Execution](https://docs.python.org/2.7/library/restricted.html)由於後來確認是不可行的，這項功能只好停用，但在 2.7.18 版本中仍保留著代碼，因此我們可以對其進行考古。

首先看看Python源碼中對`__builtins__`設置的部分：

``` c
// pythonrun.c
static void initmain(void)
{
    PyObject *m, *d;
獲取 __main__ 模組
    m = PyImport_AddModule("__main__");
    if (m == NULL)
        Py_FatalError("can't create __main__ module");

    // d = __main__.__dict__
    d = PyModule_GetDict(m);

設置 __main__.__dict__['__builtins__']，如果已有，則跳過
    if (PyDict_GetItemString(d, "__builtins__") == NULL) {
        PyObject *bimod = PyImport_ImportModule("__builtin__");
        if (bimod == NULL ||
            PyDict_SetItemString(d, "__builtins__", bimod) != 0)
            Py_FatalError("can't add __builtins__ to __main__");
        Py_XDECREF(bimod);
    }
}
```

在`initmain`中，`Python`會給`__main__`模塊設置`__builtins__`屬性，默認等於`__builtin__`模塊，但如果已有，則跳過不會重新設置。利用這個特點，我們就可以通過修改`__main__.__builtins__`來修改內建的一些功能，以達到限制程式碼執行權限的目的，具體的方法先按下不表，我們看看`__builtins__`是怎麼被傳遞的。

##`__builtins__` 的傳遞

在建立新的堆疊框架時：

```c
PyFrameObject *
PyFrame_New(PyThreadState *tstate, PyCodeObject *code, PyObject *globals,
            PyObject *locals)
{
    ...
    if (back == NULL || back->f_globals != globals) {
// 以 globals['__builtins__'] 為新 stack frame 的 __builtins__
// 內建物件就是字串 '__builtins__'
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
或者直接繼承上一層堆疊框架的 f_builtins
        builtins = back->f_builtins;
        assert(builtins != NULL && PyDict_Check(builtins));
        Py_INCREF(builtins);
    }
    ...
    f->f_builtins = builtins;
    f->f_globals = globals;
}
```

在創建新的函數框架時，對於 `__builtins__` 的處理主要有兩種情況：一種是沒有上層函數框架的情況下，會取 `globals['__builtins__']`；另一種是直接取上層函數框架的 `f_builtins`。綜合來看，可以理解為，一般情況下，在 `__main__` 中設置的 `__builtins__`，會一直被後續的函數框架所繼承，相當於共用同一份。

當導入 `import` 模組時：

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

在這裡設置新載入模組的 __builtins__ 屬性
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

在`import`其他模塊時，會將該模塊的`__builtins__`設置為`PyEval_GetBuiltins()`的返回結果，這個函數我們已經提到過，大部分情況下相當於`current_frame->f_builtins`。對於`__main__`模塊裡的`import`，`current_frame`就是`__main__`模塊的棧幀，`current_frame->f_builtins = __main__.__dict__['__builtins__']`（上文`PyFrame_New`的第一種情況）。

新加載的模組將使用 `PyEval_EvalCode` 執行其中的程式碼。可以看到，傳遞給 `PyEval_EvalCode` 的 `globals` 和 `locals` 參數實際上是模組自身的 `__dict__`，而且模組 `m.__dict__['__builtins__'] = PyEval_GetBuiltins()`。

綜合來看，我們可以得知，從`__main__`模組開始`import`的模組，也會繼承`__main__`中的`__builtins__，並會在內部的`import`中傳遞下去，這樣就可以確保，所有從`__main__`加載的模組和子模組，都能共用同一份來自`__main__`的`__builtins__`。

那麼如果是在模組中調用的函數呢？對於模組中的函數，創建和調用時：

```c
// ceval.c
建立函數
TARGET(MAKE_FUNCTION)
{
    v = POP(); /* code object */

在這裡，f->f_globals 相當於模組自身的全域變數，根據上下文可知，也相當於 m.__dict__。
    x = PyFunction_New(v, f->f_globals);
    ...
}

PyObject *
PyFunction_New(PyObject *code, PyObject *globals)
{
    PyFunctionObject *op = PyObject_GC_New(PyFunctionObject,
                                        &PyFunction_Type);
    ...
// 這裡相當於 op->func_globals = globals = f->f_globals
    op->func_globals = globals;
}

呼叫函數
static PyObject *
fast_function(PyObject *func, PyObject ***pp_stack, int n, int na, int nk)
{
    PyCodeObject *co = (PyCodeObject *)PyFunction_GET_CODE(func);
    // globals = func->func_globals
    PyObject *globals = PyFunction_GET_GLOBALS(func);
    ...
全局變數會被傳遞給 PyEval_EvalCodeEx，然後這些變數會被傳給 PyFrame_New 來建立新的堆疊框架。
    return PyEval_EvalCodeEx(co, globals,
                             (PyObject *)NULL, (*pp_stack)-n, na,
                             (*pp_stack)-2*nk, nk, d, nd,
                             PyFunction_GET_CLOSURE(func));
}
```

在創建函數時，會將 `f->f_globals` 存到函數結構體變量 `func_globals` 裡面，而對於模塊 `m`，`f->f_globals = m.__dict__`。函數執行的時候，傳給 `PyFrame_New` 的 `globals` 參數，就是創建時保存起來的 `func_globals`，`__builtins__` 自然就可以在 `func_globals` 中獲取。

迄今為止，`__builtins__` 的傳遞已經確保了一致性，所有的模組、子模組、函數，堆疊框架等都能引用到同一個，也就是擁有相同的內建命名空間。

##指定 `__main__` 模組執行

我們已經知道 `__main__` 模塊自身的 `__builtins__` 可以傳遞給所有子模塊、函數和堆疊幀，而在命令行執行 `python a.py` 時，Python 會把 `a.py` 作為 `__main__` 模塊來執行，那這是如何做到的呢：

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
嘗試使用模組的 importer 來執行程式碼
    if (filename != NULL) {
        sts = RunMainFromImporter(filename);
    }
    ...
// 通常我們自己的 py 檔案會使用這個來執行
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
設置 __file__ 屬性
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
從 pyc 檔案讀取代碼物件 co，並執行代碼
// PyEval_EvalCode will also call PyFrame_New to create a new frame inside.
    v = PyEval_EvalCode(co, globals, locals);
    ...
}
```

執行 `python a.py` 時，通常會進入 `PyRun_SimpleFileExFlags` 函數，在這裡會存取 `__main__.__dict__`，並用作程式碼執行時的 `globals` 和 `locals`，最終會傳遞到 `PyFrame_New` 中以建立新的堆疊框架來執行 `a.py`。藉由前文提到的 `__builtins__` 在模組和函式間的傳遞，後續執行的程式碼都能共用 `current_frame->f_builtins = __main__.__builtins__.__dict__`。


##再探討 限制執行

`Python` 在 2.3 版本之前，曾經提供過的 [Restricted Execution](https://docs.python.org/2.7/library/restricted.html)這個標誌是基於 `__builtins__` 的功能而製作的。或者可以認為，`__builtins__` 之所以被設計成在 `__main__` 模組中是一個模組物件，在其他模組中是一個 `dict` 物件，這樣就可以實現限制執行。

考慮這種情況：如果我們能夠自由定製我們自己的 `__builtin__` 模塊，並設置為 `__main__.__builtins__`，那就相當於後續所有執行的程式碼，都會使用我們定製的模塊，我們可以定製特定版本的 `open`、`__import__`、`file` 等內建函數和類型，更進一步，這種方式是不是可以幫助我們限制執行程式碼的權限，防止程式碼執行一些不安全的函數調用，或者訪問一些不安全的檔案？

`Python` 當時就做過這種嘗試，實現這個功能的模組就叫做: `rexec`。

### `rexec`

我無意太深入講解 `rexec` 的實現，因為原理其實上文已經講清楚了，並且這個模組本身就已經廢棄，我這些僅簡單做一些關鍵代碼的摘要，方便查閱。


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

`r_execfile` 函數會將檔案當作 `__main__` 模塊來執行，只是 `__main__` 是定制過的。`self.add_module('__main__')` 裡面，會設置模塊的 `m.__builtins__ = self.modules['__builtin__']`，這個 `__builtin__` 是由 `make_builtin` 來定制生成的，在裡面替換了 `__import__`、`reload`、`open` 函數，並刪除了 `file` 類型。這樣，我們就能控制要執行的程式碼對內建命名空間的存取了。

對於一些內建模組，`rexec` 也做了定制，保護不安全的訪問，譬如 `sys` 模組，只保留了一部分的對象，並且透過定制的 `self.loader`、`self.importer`，來實現 `import` 的時候，優先加載定制的模組。

如果你對程式碼細節感興趣，請自行查閱相關原始碼。

###`rexec` 的失敗

前文提到，自 `Python 2.3` 以後，`rexec` 功能早已廢棄，因其被證實為不可行。讓我們滿懷好奇，簡單來追溯一下：

在社區中有人報告了 [Bug](https://mail.python.org/pipermail/python-dev/2002-December/031160.html)並引發了開發者之間的討論：

    > it's never going to be safe, and I doubt it's very useful as long as it's not safe.

    > Every change is a potential security hole.

    > it's hard to predict what change is going to break it.

    > I don't expect you'll ever reach the point where it'll be wise to advertise this as safe.  I certainly won't.

    >  this is only a useful occupation if you expect to eventually reach a point where you expect that there aren't any security flaws left.  Jeremy & I both doubt that Python will ever reach that level, meaning that the whole exercise of fixing security flaws is a waste of time (if you know you *can't* make it safe, don't waste time trying).

    > I agree (but I have said that in past) the best thing is to deprecate/rip out rexec.

    > The code will still be in older versions if someone decides to pick it up and work on it as a separate project.

這個 Bug 的來源是因為 `Python` 引入了新式類型 `object`，導致 `rexec` 無法正常運作。因此開發者表示，在可預見的未來，很難避免這種情況，任何更改都有可能導致 `rexec` 出現漏洞，無法正常運作，或者被破解權限的限制，基本上無法實現一個沒有漏洞的安全環境。開發者需要不斷修正，花費大量時間。最終，`rexec` 這個模組就被廢棄了，`Python` 也沒有再提供類似的功能。但是關於 `__builtins__` 的設定，因為兼容性等問題，就繼續保留下來了。

在大概2010年的時候，有位程式設計師推出了[pysandbox](https://github.com/vstinner/pysandbox)致力於提供能夠替代 `rexec` 的 `Python` 沙盒環境。然而 3 年後，作者主動放棄了這個項目，並詳細說明了為何作者認為這個項目失敗了：[The pysandbox project is broken](https://mail.python.org/pipermail/python-dev/2013-November/130132.html)也有其他作者撰文總結了這個項目的失敗：[The failure of pysandbox](https://lwn.net/Articles/574215/)如果您對此感興趣，可以具體參考原文，我這裡也提供了一些摘要以協助理解：

> After having work during 3 years on a pysandbox project to sandbox untrusted code, I now reached a point where I am convinced that pysandbox is broken by design. Different developers tried to convinced me before that pysandbox design is unsafe, but I had to experience it myself to be convineced.

> I now agree that putting a sandbox in CPython is the wrong design. There are too many ways to escape the untrusted namespace using the various introspection features of the Python language. To guarantee the [safety] of a security product, the code should be [carefully] audited and the code to review must be as small as possible. Using pysandbox, the "code" is the whole Python core which is a really huge code base. For example, the Python and Objects directories of Python 3.4 contain more than 126,000 lines of C code.

> The security of pysandbox is the security of its weakest part. A single bug is enough to escape the whole sandbox.

> pysandbox cannot be used in practice. To protect the untrusted namespace, pysandbox installs a lot of different protections. Because of all these protections, it becomes hard to write Python code. Basic features like "del dict[key]" are denied. Passing an object to a sandbox is not possible to sandbox, pysandbox is unable to proxify arbitary objects. For something more complex than evaluating "1+(2*3)", pysandbox cannot be used in practice, because of all these protections.

__pysandbox__ 的作者認為，在 `Python` 裡面放一個沙盒環境是錯誤的設計，有太多的方式可以從沙盒中逃逸出去，`Python` 提供的語言特性很豐富，`CPython` 源碼的程式碼量很大，基本不可能保證有足夠的安全性。而 __pysandbox__ 的開發過程就是在不斷地打補丁，補丁太多，限制太多，以至於作者認為 __pysandbox__ 已經沒法實際使用，因為很多的語法特性和功能都被限制不能使用了，譬如簡單的 `del dict[key]`。

##受限制的執行，出路在哪？

既然 `rexec` 和 __pysandbox__ 這種透過 Patch Python 來提供沙盒環境的方法已經行不通了，那我不禁好奇：要怎麼樣才能為 Python 提供一個可用的沙盒環境呢？

我在這裡繼續收集了一些其他的實現方法或者案例，方便參考和查閱：

* [PyPy](https://doc.pypy.org/en/latest/sandbox.html)(https://foss.heptapod.net/pypy/pypy/-/tree/branch/sandbox-2)提供了沙盒的功能，结合额外的 [sandboxlib](https://foss.heptapod.net/pypy/sandboxlib)可以自行編譯出帶沙盒環境版本的 PyPy。如果感興趣，可以嘗試自行配置，參考這裡的一些[說明](https://foss.heptapod.net/pypy/pypy/-/issues/3192)PyPy 實現的原理是創建一個子進程，子進程的所有輸入輸出和系統調用，都會重定向到外部進程，由外部進程控制這些權限，另外也可以控制記憶體和 CPU 的使用量。需要注意的是，這個分支也有段時間沒有新的提交了，請謹慎使用。

利用操作系统所提供的沙盒環境工具。[seccomp](https://en.wikipedia.org/wiki/Seccomp)是由Linux內核提供的安全計算工具，[libseccomp](https://github.com/seccomp/libseccomp/tree/main/src/python)提供了 Python 綁定，可以內嵌到程式碼中使用；或者使用基於 seccomp 實現的工具來執行程式碼，譬如 [Firejail](https://firejail.wordpress.com/)(https://apparmor.net/)這是一個 Linux 內核安全模組，讓管理者能夠控制程式可以存取的系統資源和功能，以保護作業系統。[codejail](https://github.com/openedx/codejail)這是基於 AppArmor 實現的 Python 沙盒環境，有興趣可以嘗試。還有許多類似的工具，這裡就不一一列舉了。

* 使用沙盒虛擬環境或容器。[Windows 沙盒](https://learn.microsoft.com/zh-cn/windows/security/threat-protection/windows-sandbox/windows-sandbox-overview)，[LXC](https://linuxcontainers.org/), [Docker](https://www.docker.com/)抱歉，我無法繼續提供翻譯。

##總結

這篇文章有點長，謝謝您閱讀到這裡，相信文章一開始所提出的問題都已經得到了解答。

--8<-- "footer_tc.md"


> 這篇帖子是由 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
