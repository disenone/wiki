---
layout: post
title: Python 閒談 1 - 探究 \_\_builtins\_\_
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
description: __builtin__ 跟 __builtins__ 有什麼區別？__builtins__ 在 main 模塊跟其他模塊是不同的？為什麼會設定成不同？__builtins__
  是在哪裡定義的？本文我們來探討一下關於 __builtins__ 的冷知識，並且還有一些引申的內容，不容錯過。
figures: []
---

<meta property="og:title" content="Python 杂谈 1 - 探究 __builtins__ - Disenone" />

##Prelude

我們知道，`__builtins__` 本身就是在全域命名空間中一個存在的物件，是 `Python` 故意公開給程式碼層級使用的，在程式的任何地方都可以直接使用。不過有點冷門的知識是，`__builtins__` 在 `main` 模組（也就是 `__main__`，指的都是同一個模組，後文可能會混用）裡面是 `__builtin__` 這個模組，但在其他模組裡面，它代表的是 `__builtin__.__dict__`，這就有點讓人莫名其妙了。雖然官方不推薦直接使用 `__builtins__`，但你給我搞兩種情況是怎麼回事？本文我們就來盤一盤這個設定的由來，在這個過程中，我們還可以找到這些問題的答案：`__builtin__` 跟 `__builtins__` 有什麼區別？`__builtins__` 在 `main` 模組跟其他模組為什麼會設定成不同？`__builtins__` 是在哪裡定義的？


## `__builtin__`

在探討 `__builtins__` 之前，我們需要先看看 `__builtin__` 是什麼。`__builtin__` 是存放所有內建物件的模組，我們平常可以直接使用的 `Python` 內建物件，本質上都是 `__builtin__` 模組裡的物件，即放在 `__builtin__.__dict__` 裡，對應著的是 `Python` 的內建名字空間。記住這個關鍵知識點：`__buintin__` 是一個模組 `module`。我們可以在 `Python` 原始碼中找到 `__builtin__` 模組的定義和使用（注意，下文提到的 `Python` 原始碼，都是指 CPython-2.7.18 原始碼）：

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

// 為字典加入內建對象
    ...
}

// ceval.c
獲取內建函數
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

Python 的初始化過程會執行 _PyBuiltin_Init 來建立 __builtin__ 模組，在其中添加內建物件。直譯器本身會參考 interp->builtins = __buintin__.__dict__，而當前執行的堆疊框架同時會參考 current_frame->f_builtins。因此，當 Python 執行代碼需要根據名稱尋找物件時，會在 current_frame->f_builtins 中尋找，從而獲取所有內建物件。

```c
// ceval.c
TARGET(LOAD_NAME)
{
// 先在 f->f_locals 名字空間裡面找
    ...
    if (x == NULL) {
再找找全局空間
        x = PyDict_GetItem(f->f_globals, w);
        if (x == NULL) {
這裡就去內建空間找。
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

最後，由於 `__builtin__` 這個名字實在是太有迷惑性了，`Python3` 中已經改名為 `builtins`。


## `__builtins__`

`__builtins__` 的行為有些奇怪：
在 `main` 模块中（`main` 模块，或者叫做 `最高層級碼運行所在環境`，是用戶指定最先啟動運行的 `Python` 模塊，也就是通常我們在命令行執行 `python xxx.py` 時，`xxx.py` 這個模塊），`__builtins__ = __builtin__`；
在其他模組中 `__builtins__ = __builtin__.__dict__`。

相同的名稱，但在不同的模組下表現卻是不相同的，這樣的設定很容易讓人疑惑。不過只要知道這個設定，就足夠支持你在 `Python` 中使用 `__builtins__`，疑惑並不會影響你寫出足夠安全的程式碼，諸如：

``` python
def SetBuiltins(builtins, key, val):
    if isinstance(builtins, dict):
        builtins[key] = val
    else:
        setattr(builtins, key, val)

SetBuiltins(__builtins__, 'test', 1)
```

有人提醒，實際上並不建議使用 `__builtins__`：

> CPython 實作細節：使用者不應該直接操作 `__builtins__`；這是嚴格的實作細節。想要覆蓋內建命名空間中的值的使用者應該導入 `__builtin__`（沒有 's'）模組並適當修改其屬性。

當然，這樣的疑惑，總有一天會讓你心癢難耐，我這裡就決定繼續探究下去，也因為這樣，才有了這篇文章。我們接下來會深入探討 __CPython implementation detail__ 中的內容。

## Restricted Execution

Restricted Execution 可以理解為有限制地執行不安全的程式碼，所謂有限制，可以是限制網路、io 等等，把程式碼限制在一定的執行環境中，控制程式碼的執行權限，防止影響外部環境和系統。常見的用例就是一些線上程式碼執行網站，譬如這個：[pythonsandbox](https://pythonsandbox.dev/)抱歉，我無法為您翻譯這個訊息，因為它是空白的。如果您需要任何幫助，請隨時告訴我！

與你猜想的一致，Python 對 __builtins__ 的設定與 Restricted Execution 相關。在 Python 2.3 版本之前，曾提供過類似的功能[Restricted Execution](https://docs.python.org/2.7/library/restricted.html)由於後來證實是不可行的，這個功能只好被廢棄了，但代碼在 2.7.18 版本仍保留著，所以我們可以進行考古。

首先看看 `Python` 源碼中對 `__builtins__` 的設置：

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

設置\_\_main\_\_.\_\_dict\_\_\['\_\_builtins\_\_'\]，如果已有，則跳過
    if (PyDict_GetItemString(d, "__builtins__") == NULL) {
        PyObject *bimod = PyImport_ImportModule("__builtin__");
        if (bimod == NULL ||
            PyDict_SetItemString(d, "__builtins__", bimod) != 0)
            Py_FatalError("can't add __builtins__ to __main__");
        Py_XDECREF(bimod);
    }
}
```

在`initmain`中，`Python`會給`__main__`模組設置`__builtins__`屬性，預設等於`__builtin__`模組，但如果已有則跳過不會重新設置。利用這個特點，我們就可以通過修改`__main__.__builtins__`來修改內建的一些功能，以達到限制程式碼執行權限的目的，具體的方法先按下不表，我們看看`__builtins__`是怎麼被傳遞的。

##內建函式的傳遞

在創建新的堆疊框架時：

```c
PyFrameObject *
PyFrame_New(PyThreadState *tstate, PyCodeObject *code, PyObject *globals,
            PyObject *locals)
{
    ...
    if (back == NULL || back->f_globals != globals) {
將 globals['__builtins__'] 擷取為新堆疊框架的 __builtins__。
// 內建對象就是字串 '__builtins__'
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
// Alternatively, inherit f_builtins from the next higher stack frame.
        builtins = back->f_builtins;
        assert(builtins != NULL && PyDict_Check(builtins));
        Py_INCREF(builtins);
    }
    ...
    f->f_builtins = builtins;
    f->f_globals = globals;
}
```

創建新的堆疊框架時，對於 `__builtins__` 的處理主要有兩種情況：一種是沒有上層堆疊框架的情況下，取 `globals['__builtins__']`；另一種是直接取上層堆疊框架的 `f_builtins`。聯合起來看的話，可以理解為，一般情況下，在 `__main__` 中設定好的 `__builtins__`，會一直繼承給後面的堆疊框架，相當於共用同一份。

在載入 `import` 模組時：

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

在這裡設置新加載模塊的__builtins__屬性
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

在導入其他模塊時，系統會將該模塊的 `__builtins__` 設置為 `PyEval_GetBuiltins()` 的返回結果，這個函數通常相當於 `current_frame->f_builtins`。對於 `__main__` 模塊中的導入操作，`current_frame` 就是 `__main__` 模塊的堆棧框架，而 `current_frame->f_builtins = __main__.__dict__['__builtins__']`（見 `PyFrame_New` 的第一種情況）。

新模組的載入將使用 `PyEval_EvalCode` 來執行新模組的程式碼。可以看出，傳遞給 `PyEval_EvalCode` 的 `globals` 和 `locals` 參數實際上都是模組本身的 `__dict__`，並且模組 `m.__dict__['__builtins__'] = PyEval_GetBuiltins()`。

綜合來看，我們可以得知，從 `__main__` 模組開始 `import` 的模組，也會繼承 `__main__` 中的 `__builtins__`，並會在內部的 `import` 中傳遞下去，這樣就可以確保，所有從 `__main__` 載入的模組和子模組，都能共用同一份來自 `__main__` 的 `__builtins__`。

在模塊中調用的功能的話又是怎樣呢？對於模塊中的函數，在創建和調用時：

```c
// ceval.c
建立函數
TARGET(MAKE_FUNCTION)
{
    v = POP(); /* code object */

這裡的 f->f_globals，相當於模組自身的 globals，由上文可知，也相當於 m.__dict__
    x = PyFunction_New(v, f->f_globals);
    ...
}

PyObject *
PyFunction_New(PyObject *code, PyObject *globals)
{
    PyFunctionObject *op = PyObject_GC_New(PyFunctionObject,
                                        &PyFunction_Type);
    ...
這裡相當於 op->func_globals = globals = f->f_globals
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
將這些文本翻譯成繁體中文：

// 全域變數被傳遞給 PyEval_EvalCodeEx，然後被傳遞到 PyFrame_New 以建立新的堆疊框架
    return PyEval_EvalCodeEx(co, globals,
                             (PyObject *)NULL, (*pp_stack)-n, na,
                             (*pp_stack)-2*nk, nk, d, nd,
                             PyFunction_GET_CLOSURE(func));
}
```

當創建函數時，會將 `f->f_globals` 存入函數結構變數 `func_globals` 中，對於模組 `m`，`f->f_globals = m.__dict__`。當函數執行時，傳遞給 `PyFrame_New` 的 `globals` 參數，就是在創建時保存下來的 `func_globals`，`__builtins__` 自然就可以在 `func_globals` 中獲取。

到了這裡，`__builtins__` 的傳遞能確保一致性，所有模組、子模組、函數、堆疊框架等都能參照到同一個，也就是擁有相同的內建名稱空間。

##指定 `__main__` 模組執行

我們已經知道 `__main__` 模組自身的 `__builtins__` 可以傳遞給所有子模組、函數和堆疊幀，而在命令列執行 `python a.py` 時，Python 會把 `a.py` 作為 `__main__` 模組來執行，那這是如何做到的呢：

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
嘗試使用模塊的導入器來執行程式碼
    if (filename != NULL) {
        sts = RunMainFromImporter(filename);
    }
    ...
通常我們會使用這個來執行我們自己的 py 檔案。
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
從 pyc 檔案讀取程式碼對象 co，並執行程式。
// PyEval_EvalCode 里面也同樣會呼叫 PyFrame_New 創建新棧框
    v = PyEval_EvalCode(co, globals, locals);
    ...
}
```

當執行 `python a.py` 時，一般情況下會走到 `PyRun_SimpleFileExFlags`，`PyRun_SimpleFileExFlags` 裡面會取出來 `__main__.__dict__`，作為程式碼執行時的 `globals` 和 `locals`，最終也會傳到 `PyFrame_New` 中創建新的堆疊框架來執行 `a.py`。結合我們上文提到的 `__builtins__` 在模組和函數中傳遞，就可以讓後續執行的程式碼都能共用同一份 `current_frame->f_builtins = __main__.__builtins__.__dict__`。


##再論限制執行

在 2.3 版本之前，Python 曾經提供過的 [Restricted Execution](https://docs.python.org/2.7/library/restricted.html)這段文字是基於 `__builtins__` 的特性而製作的。或者可以認為，`__builtins__` 之所以在 `__main__` 模塊中被設計為一個模塊對象，在其他模塊中被設計為一個 `dict` 對象，是為了實現 __Restricted Execution__。

考慮這種情況：如果我們可以自由定製我們的 `__builtin__` 模組，並設置為 `__main__.__builtins__`，那麼後續所有執行的程式碼都將使用我們定製的模組。我們可以定製特定版本的 `open`、`__import__`、`file` 等內建函數和類型。進一步來說，這種方式是否能夠幫助我們限制代碼的執行權限，防止代碼執行一些不安全的函數呼叫，或者訪問一些不安全的檔案？

`Python` 當時就做過這種嘗試，實現這個功能的模塊就叫做: `rexec`。

### `rexec`

我無意深入探討「rexec」的實現，因為原理已在先前文中交代清楚，且該模組本身已被廢棄。我這裡只是做了一些關鍵程式碼的摘要，便於查閱。


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

`r_execfile` 函數會將檔案當作 `__main__` 模組來執行，只是 `__main__` 是經過定制的。在 `self.add_module('__main__')` 中，會設置模組的 `m.__builtins__ = self.modules['__builtin__']`，這個 `__builtin__` 是由 `make_builtin` 來定制生成的，在其中替換了 `__import__`、`reload`、`open` 函數，並刪除了 `file` 類型。這樣，我們就能控制要執行的代碼對內建命名空間的訪問了。

針對某些內建模塊，`rexec` 也進行了定制，保護不安全的訪問，例如 `sys` 模塊，只保留了部分對象，並且通過定制的 `self.loader`、`self.importer`，在執行 `import` 時，優先加載定制的模塊。

如果你對程式碼中的細節感興趣，請自行查閱相關原始碼。

###`rexec` 的失敗

前述內容提及，自`Python 2.3`起，`rexec`已被淘汰，因為其方法已被證實無法實現。讓我們帶著好奇心，簡單來追溯一下：

在社群裡有人回報了 [缺陷](https://mail.python.org/pipermail/python-dev/2002-December/031160.html)引發了開發者之間的討論：

    > it's never going to be safe, and I doubt it's very useful as long as it's not safe.

    > Every change is a potential security hole.

    > it's hard to predict what change is going to break it.

    > I don't expect you'll ever reach the point where it'll be wise to advertise this as safe.  I certainly won't.

    >  this is only a useful occupation if you expect to eventually reach a point where you expect that there aren't any security flaws left.  Jeremy & I both doubt that Python will ever reach that level, meaning that the whole exercise of fixing security flaws is a waste of time (if you know you *can't* make it safe, don't waste time trying).

    > I agree (but I have said that in past) the best thing is to deprecate/rip out rexec.

    > The code will still be in older versions if someone decides to pick it up and work on it as a separate project.

該 Bug 的起因是 `Python` 引入了新式類(new-style class) `object`，導致 `rexec` 不能正常運作。於是開發者表示，在可預見的未來，這種情況都很難避免，任意的修改都有可能導致 `rexec` 出現漏洞，無法正常運作，或者被突破權限的限制，基本上無法實現沒有漏洞地提供一個安全環境的願景，開發者需要不斷地修補 Bug，浪費大量的時間。最終，`rexec` 這個模組就被廢棄，`Python` 也沒有再提供類似的功能。但關於 `__builtins__` 的設定，由於兼容性等問題，就繼續保留下來了。

在約2010年左右，有一位程式設計師推出了[pysandbox](https://github.com/vstinner/pysandbox)致力於提供可替代「rexec」的「Python」沙盒環境。然而，3年後，作者主動放棄了這個專案，並詳細說明為何作者認為這個專案失敗了：[The pysandbox project is broken](https://mail.python.org/pipermail/python-dev/2013-November/130132.html)也有其他作者總結了這個項目的失敗：[The failure of pysandbox](https://lwn.net/Articles/574215/)如果你感興趣的話，可以具體去翻翻原文，我這裡也給一些摘要來幫助了解：

> After having work during 3 years on a pysandbox project to sandbox untrusted code, I now reached a point where I am convinced that pysandbox is broken by design. Different developers tried to convinced me before that pysandbox design is unsafe, but I had to experience it myself to be convineced.

> I now agree that putting a sandbox in CPython is the wrong design. There are too many ways to escape the untrusted namespace using the various introspection features of the Python language. To guarantee the [safety] of a security product, the code should be [carefully] audited and the code to review must be as small as possible. Using pysandbox, the "code" is the whole Python core which is a really huge code base. For example, the Python and Objects directories of Python 3.4 contain more than 126,000 lines of C code.

> The security of pysandbox is the security of its weakest part. A single bug is enough to escape the whole sandbox.

> pysandbox cannot be used in practice. To protect the untrusted namespace, pysandbox installs a lot of different protections. Because of all these protections, it becomes hard to write Python code. Basic features like "del dict[key]" are denied. Passing an object to a sandbox is not possible to sandbox, pysandbox is unable to proxify arbitary objects. For something more complex than evaluating "1+(2*3)", pysandbox cannot be used in practice, because of all these protections.

__pysandbox__ 的作者覺得，在 `Python` 裡設置沙盒環境並不是一個好的設計，因為有太多逃逸出沙盒的方法。 `Python` 提供了非常豐富的語言特性，`CPython` 的原始碼非常龐大，基本上無法保證足夠的安全性。 __pysandbox__ 的開發過程一直在不斷修補問題，但修補了太多，限制了太多，以至於作者認為 __pysandbox__ 已經無法實際應用，因為許多語法特性和功能都被限制了，例如簡單的 `del dict[key]`。

##受限制的執行：出路在哪裡

既然 `rexec` 和 __pysandbox__ 這種透過 Patch Python 來提供沙盒環境的方法（這裡姑且稱為 Patch Python）已經行不通了，那我不禁好奇：要怎樣才能給 Python 提供一個可用的沙盒環境？

我在這裡繼續收集了一些其他的實現方法或案例，方便參考和查閱：

* [PyPy](https://doc.pypy.org/en/latest/sandbox.html)有一個[分支](https://foss.heptapod.net/pypy/pypy/-/tree/branch/sandbox-2)提供了沙盒的功能，结合额外的 [sandboxlib](https://foss.heptapod.net/pypy/sandboxlib)您可以自行編譯帶沙盒環境版本的 PyPy。如有興趣，可嘗試自行配置，參考這裡的一些[說明](https://foss.heptapod.net/pypy/pypy/-/issues/3192)PyPy 實現的原理是創建一個子進程，子進程的所有輸入輸出和系統調用，都會重新導向到外部進程，由外部進程控制這些權限，另外也可以控制內存和 CPU 的使用量。需要注意的是，這個分支也有段時間沒有新的提交了，請謹慎使用。

利用操作系統提供的沙箱環境工具。[seccomp](https://en.wikipedia.org/wiki/Seccomp)由 Linux 內核提供的計算安全工具，[libseccomp](https://github.com/seccomp/libseccomp/tree/main/src/python)提供了 Python 綁定，可以內嵌到程式碼中使用；或者使用基於 seccomp 實現的工具來執行程式碼，譬如 [Firejail](https://firejail.wordpress.com/)(https://apparmor.net/)這是一個 Linux 內核安全模組，允許管理員控制程式能存取的系統資源和功能，以保護作業系統。[codejail](https://github.com/openedx/codejail)這是基於 AppArmor 實現的 Python 沙盒環境，有興趣可以嘗試。還有許多類似的工具，這裡不一一列舉。

使用沙盒虛擬環境或容器。[Windows 沙盒](https://learn.microsoft.com/zh-cn/windows/security/threat-protection/windows-sandbox/windows-sandbox-overview)，[LXC](https://linuxcontainers.org/), [Docker](https://www.docker.com/)抱歉，這裡不再詳述。

##總結

這段文字有點長，感謝您閱讀至此，相信前文提出的問題皆已被解答。

--8<-- "footer_tc.md"


> 這篇文章是由 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
