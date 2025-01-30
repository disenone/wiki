---
layout: post
title: Python 杂谈 1 - 探究 __builtins__
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
description: __builtin__ 跟 __builtins__ 有什麼區別？__builtins__ 在 main 模組跟其他模組是不同的？為什麼會設定成不同？__builtins__
  是在哪裡定義的？本文我們來探討一下關於 __builtins__ 的冷知識，並且還有一些引申的內容，不容錯過。
figures: []
---

<meta property="og:title" content="Python 杂谈 1 - 探究 __builtins__ - Disenone" />

##引子

我們知道，`__builtins__` 本身是在全局命名空間中就有的一個物件，是 `Python` 故意暴露出來給程式碼層用的，在程式的任意地方都可以直接使用。但有趣的是，`__builtins__` 在 `main` 模組（也就是 `__main__`，指的都是同一個模組，後文可能會混用）裡面是 `__builtin__` 這個模組，但在其他模組裡面，它表示的是 `__builtin__.__dict__`，這就有點讓人摸不著頭緒。雖然官方不推薦直接使用 `__builtins__`，但你給我搞兩種情況是怎麼回事？本文我們就來盤一盤這個設定的由來，在這過程中，我們還可以找到這些問題的答案：`__builtin__` 跟 `__builtins__` 有什麼區別？`__builtins__` 在 `main` 模組跟其他模組為什麼會設定成不同？`__builtins__` 是在哪裡定義的？


## `__builtin__`

在探討 `__builtins__` 之前，我們需要先看看 `__builtin__` 是什麼。`__builtin__` 是存放所有內建對象的模塊，我們平常可以直接使用的 `Python` 內建對象，本質上都是 `__builtin__` 模塊裡的對象，即放在 `__builtin__.__dict__` 裡，對應著的是 `Python` 的內建名字空間。記住這個關鍵知識點：`__builtin__` 是一個模塊 `module`。我們可以在 `Python` 原碼中找到 `__builtin__` 模塊的定義和使用（注意，下文提到的 `Python` 原碼，都是指 CPython-2.7.18 原碼）：

``` c
// pythonrun.c
void
Py_InitializeEx(int install_sigs)
{
    PyInterpreterState *interp;
    ...
// 初始化 __builtin__
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

將這些文字翻譯成繁體中文:

    // 在 dict 中加入內建對象
    ...
}

// ceval.c
// 獲取內建函數
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

`Python` 初始化的時候會調用 `_PyBuiltin_Init` 來創建 `__builtin__` 模塊，並在裡面添加上內建的對象，解釋器本身會引用住 `interp->builtins = __builtin__.__dict__`，當前執行的堆疊幀結構同時也會引用一份 `current_frame->f_builtins`。那麼很自然地，當執行代碼需要根據名字尋找對象的時候，`Python` 會去 `current_frame->f_builtins` 裡面來找，自然就能拿到所有的內建對象：

```c
// ceval.c
TARGET(LOAD_NAME)
{
// 先在 f->f_locals 名字空間裡面找
    ...
    if (x == NULL) {
// 再尋找全域空間
        x = PyDict_GetItem(f->f_globals, w);
        if (x == NULL) {
// 去內建空間找
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

`__builtins__` 的表現有點奇怪：
在 `main` 模塊中（`main` 模塊，或者稱為`最高層級代碼運行所在環境`，是用戶指定最先啟動運行的 `Python` 模塊，也就是通常我們在命令行執行 `python xxx.py` 時，`xxx.py` 這個模塊），`__builtins__ = __builtin__`；
* 在其他模組中 `__builtins__ = __builtin__.__dict__`。

相同的名字，但在不同的模塊下表現卻是不相同的，這樣的設定很容易讓人疑惑。不過只要知道這個設定，就足夠支持你在 `Python` 中使用 `__builtins__`，疑惑並不會影響你寫出足夠安全的代碼，諸如：

``` python
def SetBuiltins(builtins, key, val):
    if isinstance(builtins, dict):
        builtins[key] = val
    else:
        setattr(builtins, key, val)

SetBuiltins(__builtins__, 'test', 1)
```

請注意，實際上不建議使用 `__builtins__`：

> __CPython 實作細節__: 用戶不應該觸碰 `__builtins__`；這純粹是實作細節。希望覆蓋內建命名空間中值的用戶應該匯入 `__builtin__`（沒有 's'）模組，並適當地修改其屬性。

當然，這樣的疑惑，總有一天會讓你心癢難耐，我這裡就決定繼續探究下去，也因為這樣，才有了這篇文章。我們下面的內容會深入到 __CPython implementation detail__ 中去。

## Restricted Execution

受限制的執行可理解為有限制地執行不安全的程式碼，所謂限制可以是限制網路、io 等等，將程式碼限制在特定執行環境中，控制程式碼的執行權限，防止程式碼影響外部環境和系統。常見的應用案例就是一些線上程式碼執行網站，比如這個：[pythonsandbox](https://pythonsandbox.dev/)。

跟你猜想的一樣，`Python` 對 `__builtins__` 的設定是跟 Restricted Execution 有關。`Python` 在 2.3 版本之前，曾經提供過類似的功能 [Restricted Execution](https://docs.python.org/2.7/library/restricted.html)由於事後證實可行性不高，這項功能最終被放棄了，但在 2.7.18 版本中仍有保留代碼，我們可以進行考古。

首先來看 `Python` 源碼裡面對 `__builtins__` 的設定：

``` c
// pythonrun.c
static void initmain(void)
{
    PyObject *m, *d;
// 取得 __main__ 模組
    m = PyImport_AddModule("__main__");
    if (m == NULL)
        Py_FatalError("can't create __main__ module");

    // d = __main__.__dict__
    d = PyModule_GetDict(m);

// 設置 __main__.__dict__['__builtins__']，如果已存在，則跳過
    if (PyDict_GetItemString(d, "__builtins__") == NULL) {
        PyObject *bimod = PyImport_ImportModule("__builtin__");
        if (bimod == NULL ||
            PyDict_SetItemString(d, "__builtins__", bimod) != 0)
            Py_FatalError("can't add __builtins__ to __main__");
        Py_XDECREF(bimod);
    }
}
```

在 `initmain` 中，`Python` 會給 `__main__` 模組設置 `__builtins__` 屬性，默認等於 `__builtin__` 模組，但如果已存在，則跳過不會重新設置。利用這個特點，我們就可以通過修改 `__main__.__builtins__` 來修改內建的一些功能，以達到限制代碼執行權限的目的，具體的方法先按下不表，我們看看 `__builtins__` 是怎麼被傳遞的。

##`__builtins__` 的傳遞

在建立新的堆疊框架時：

```c
PyFrameObject *
PyFrame_New(PyThreadState *tstate, PyCodeObject *code, PyObject *globals,
            PyObject *locals)
{
    ...
    if (back == NULL || back->f_globals != globals) {
// 取 globals['__builtins__'] 作為新堆疊框架的 __builtins__
// 內建物件是字串 '__builtins__'
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
或者直接繼承上一層棧框架的 f_builtins
        builtins = back->f_builtins;
        assert(builtins != NULL && PyDict_Check(builtins));
        Py_INCREF(builtins);
    }
    ...
    f->f_builtins = builtins;
    f->f_globals = globals;
}
```

創建新的堆棧幀時，對於 `__builtins__` 的處理主要有兩種情況：一種是在沒有上層堆棧幀的情況下，取 `globals['__builtins__']`；另一種是直接取上層堆棧幀的 `f_builtins`。聯合起來看，可以理解為，一般情況下，在 `__main__` 中設置好的 `__builtins__`，會一直繼承給後面的堆棧幀，相當於共用同一份。

導入`import`模組時：

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

// 在這裡設置新加載模塊的 __builtins__ 屬性
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

在 `import` 其他模組的時候，會把該模組的 `__builtins__` 設置為 `PyEval_GetBuiltins()` 的返回結果，這個函數我們已經提到過，大部分情況下相當於 `current_frame->f_builtins`。對於 `__main__` 模組內的 `import`，`current_frame` 就是 `__main__` 模組的堆疊框架，`current_frame->f_builtins = __main__.__dict__['__builtins__']`（上文 `PyFrame_New` 的第一種情況）。

載入新模組時，將使用 `PyEval_EvalCode` 執行新模組中的程式碼。可見傳給 `PyEval_EvalCode` 的參數 `globals` 和 `locals` 實際上都是模組本身的 `__dict__`，並且模組 `m.__dict__['__builtins__'] = PyEval_GetBuiltins()`。

綜合來看，我們可以知道，從`__main__`模組開始`import`的模組，也會繼承`__main__`中的`__builtins__`，並會在內部的`import`中傳遞下去，這樣就可以確保，所有從`__main__`載入的模組和子模組，都能共用同一份來自`__main__`的`__builtins__`。

那麼如果是在模組中調用的函數呢？對於模組中的函數，創建和調用時：

```c
// ceval.c
建立函數
TARGET(MAKE_FUNCTION)
{
    v = POP(); /* code object */

在這裡，f->f_globals 指的是模組本身的全域變數，根據前文可知，也等同於 m.__dict__。
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

// 調用函數
static PyObject *
fast_function(PyObject *func, PyObject ***pp_stack, int n, int na, int nk)
{
    PyCodeObject *co = (PyCodeObject *)PyFunction_GET_CODE(func);
    // globals = func->func_globals
    PyObject *globals = PyFunction_GET_GLOBALS(func);
    ...
將這些文字翻譯成正體中文：

    // globals 會傳遞給 PyEval_EvalCodeEx，然後傳遞到 PyFrame_New 以建立新的堆疊框架
    return PyEval_EvalCodeEx(co, globals,
                             (PyObject *)NULL, (*pp_stack)-n, na,
                             (*pp_stack)-2*nk, nk, d, nd,
                             PyFunction_GET_CLOSURE(func));
}
```

創建函數時，會把 `f->f_globals` 存到函數結構體變量 `func_globals` 裡面，而對於模組 `m`，`f->f_globals = m.__dict__`。函數執行的時候，傳給 `PyFrame_New` 的 `globals` 參數，就是創建時保存起來的 `func_globals`，`__builtins__` 自然就可以在 `func_globals` 中獲取。

至此，`__builtins__` 的傳遞能夠保證一致性，所有模組、子模組、函數、堆疊幀等都能引用同一個，也就是擁有相同的內建名稱空間。

##指定 `__main__` 模塊執行

我們已經知道 `__main__` 模組本身的 `__builtins__` 可以傳遞給所有子模組、函數和堆疊框架，而在命令行執行 `python a.py` 時，Python 會將 `a.py` 視為 `__main__` 模組來執行，那這是如何做到的呢：

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
// 設置 __file__ 屬性
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
從 pyc 檔案讀取程式碼對象 co，並執行程式碼
// PyEval_EvalCode 裡面也同樣會呼叫 PyFrame_New 創建新堆疊框架
    v = PyEval_EvalCode(co, globals, locals);
    ...
}
```

當執行 `python a.py` 時，一般情況下會走到 `PyRun_SimpleFileExFlags`，`PyRun_SimpleFileExFlags` 裡面會取出 `__main__.__dict__`，作為程式碼執行時的 `globals` 和 `locals`，最終也會傳到 `PyFrame_New` 中創建新的堆棧幀來執行 `a.py`。結合我們上文提到的 `__builtins__` 在模塊和函數中傳遞，就可以讓後續執行的程式碼都能共用同一份 `current_frame->f_builtins = __main__.__builtins__.__dict__`。


##再談限制執行

`Python` 在 2.3 版本之前，曾經提供過的 [Restricted Execution](https://docs.python.org/2.7/library/restricted.html)這段文字是基於 `__builtins__` 特性製作的。或者可以視為，`__builtins__` 之所以在 `__main__` 模組中被設計為一個模組物件，在其他模組中則為一個 `dict` 物件，是為了實現__Restricted Execution__。

考慮這種情況：如果我們可以自由定制我們的`__builtin__`模塊，並設置為`__main__.__builtins__`，那就相當於後續所有執行的程式碼，都會使用我們定制的模塊， 我們可以定制特定版本的`open`、`__import__`、`file`等內建函數和類型，更進一步，這種方式是不是可以幫助我們限制執行程式碼的權限，防止程式碼做一些不安全的函數調用，或者訪問一些不安全的文件？

`Python` 當時就做過這種嘗試，實現這個功能的模塊就叫做: `rexec`。

### `rexec`

我無意太深入講解 `rexec` 的實現，因為原理其實上文已經講清楚了，並且這個模塊本身就已經廢棄，我這些僅簡單做一些關鍵代碼的摘要，方便查閱。


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

`r_execfile` 函數會把文件當作 `__main__` 模塊來執行，只是 `__main__` 是定制過的。`self.add_module('__main__')` 裡面，會設置模塊的 `m.__builtins__ = self.modules['__builtin__']`，這個 `__builtin__` 是由 `make_builtin` 來定制生成的，在裡面替換了 `__import__`、`reload`、`open` 函數，並刪除了 `file` 類型。這樣，我們就能控制要執行的代碼對內建命名空間的訪問了。

對於一些內建模組，`rexec` 也做了定制，保護不安全的訪問，例如 `sys` 模組，只保留了一部分的對象，並且通過定制的 `self.loader`、`self.importer`，來實現 `import` 的時候，優先加載定制的模組。

如果對程式碼細節感興趣，請自行查閱相關原始碼。

###`rexec` 的失敗

上文提到，`Python 2.3` 之後，`rexec` 就已經廢棄了，因為這種方式已經被證實為不可行。帶著好奇心，我們來簡單溯源一下：

* 在社區有人報告了 [Bug](https://mail.python.org/pipermail/python-dev/2002-December/031160.html)，並引發了開發者之間的討論：

    > it's never going to be safe, and I doubt it's very useful as long as it's not safe.

    > Every change is a potential security hole.

    > it's hard to predict what change is going to break it.

    > I don't expect you'll ever reach the point where it'll be wise to advertise this as safe.  I certainly won't.

    >  this is only a useful occupation if you expect to eventually reach a point where you expect that there aren't any security flaws left.  Jeremy & I both doubt that Python will ever reach that level, meaning that the whole exercise of fixing security flaws is a waste of time (if you know you *can't* make it safe, don't waste time trying).

    > I agree (but I have said that in past) the best thing is to deprecate/rip out rexec.

    > The code will still be in older versions if someone decides to pick it up and work on it as a separate project.

* 該 Bug 的起因是 `Python` 引入了新式類別（new-style class） `object`，導致 `rexec` 不能正常工作。於是開發者表示，在可預見的未來，這種情況都很難避免，任意的修改都有可能導致 `rexec` 出現漏洞，不能正常工作，或者被突破權限的限制，基本上無法實現沒有漏洞地提供一個安全環境的願景，開發者需要不斷地修修補補，浪費大量的時間。最終，`rexec` 這個模組就被廢棄掉了，`Python` 也沒有再提供類似的功能。但關於 `__builtins__` 的設定，由於相容性等問題，則繼續保留下來了。

後來在大約 2010 年的時候，有位程式設計師推出了 [pysandbox](https://github.com/vstinner/pysandbox)，致力於提供可以替代 `rexec` 的 `Python` 沙盒環境。但是 3 年後，作者主動放棄了這個項目，並詳細說明了為什麼作者認為這個項目是失敗的：[The pysandbox project is broken](https://mail.python.org/pipermail/python-dev/2013-November/130132.html)相同一倇，亦有其他作者寫文摘要了這計劃失敗的原因：[The failure of pysandbox](https://lwn.net/Articles/574215/)。如果感兴趣的话，可以具体去翻翻原文，我这里也给一些摘要来帮助了解：

> After having work during 3 years on a pysandbox project to sandbox untrusted code, I now reached a point where I am convinced that pysandbox is broken by design. Different developers tried to convinced me before that pysandbox design is unsafe, but I had to experience it myself to be convineced.

> I now agree that putting a sandbox in CPython is the wrong design. There are too many ways to escape the untrusted namespace using the various introspection features of the Python language. To guarantee the [safety] of a security product, the code should be [carefully] audited and the code to review must be as small as possible. Using pysandbox, the "code" is the whole Python core which is a really huge code base. For example, the Python and Objects directories of Python 3.4 contain more than 126,000 lines of C code.

> The security of pysandbox is the security of its weakest part. A single bug is enough to escape the whole sandbox.

> pysandbox cannot be used in practice. To protect the untrusted namespace, pysandbox installs a lot of different protections. Because of all these protections, it becomes hard to write Python code. Basic features like "del dict[key]" are denied. Passing an object to a sandbox is not possible to sandbox, pysandbox is unable to proxify arbitary objects. For something more complex than evaluating "1+(2*3)", pysandbox cannot be used in practice, because of all these protections.

__pysandbox__ 的作者認為，在 `Python` 裡面放一個沙盒環境是錯誤的設計，有太多的方式可以從沙盒中逃逸出去，`Python` 提供的語言特性很豐富，`CPython` 源碼的代碼量很大，基本不可能保證有足夠的安全性。而 __pysandbox__ 的開發過程就是在不斷地打補丁，補丁太多，限制太多，以至於作者認為 __pysandbox__ 已經沒法實際使用，因為很多的語法特性和功能都被限制不能使用了，例如簡單的 `del dict[key]`。

##受限執行 出路在哪

既然 `rexec` 和 __pysandbox__ 這類透過修改 Python 以提供沙盒環境的方法（這裡姑且稱之為修改 Python），已經不再可行，那麼我不禁好奇：要如何才能為 Python 提供一個可用的沙盒環境？

我在這裡繼續收集了一些其他的實現方法或案例，方便參考和查閱：

* [PyPy](https://doc.pypy.org/en/latest/sandbox.html)有一個[分支](https://foss.heptapod.net/pypy/pypy/-/tree/branch/sandbox-2)提供了沙盒的功能，结合额外的 [sandboxlib](https://foss.heptapod.net/pypy/sandboxlib)您可以自行編譯帶沙盒環境版本的 PyPy。如果您感興趣，可以嘗試自行配置，參考這裡的一些[說明](https://foss.heptapod.net/pypy/pypy/-/issues/3192)PyPy 實現的原理是創建一個子進程，子進程的所有輸入輸出和系統調用，都會重定向到外部進程，由外部進程控制這些權限，另外也可以控制內存和 CPU 的使用量。需要注意的是，這個分支也有段時間沒有新的提交了，請謹慎使用。

利用操作系统提供的沙盒環境工具。[seccomp](https://en.wikipedia.org/wiki/Seccomp)是 Linux 內核提供的計算安全工具，[libsecoomp](https://github.com/seccomp/libseccomp/tree/main/src/python)提供了 Python 綁定，可以內嵌到程式碼中使用；或者使用基於 seccomp 實現的工具來執行程式碼，譬如 [Firejail](https://firejail.wordpress.com/)。[應用程式防火牆](https://apparmor.net/)`codejail` 是一個 Linux 內核安全模組，允許管理員控制程式能訪問的系統資源和功能，保護作業系統。[codejail](https://github.com/openedx/codejail)是基於 AppArmor 實現的 Python 沙盒環境，有興趣可以嘗試。還有很多類似的工具，這裡不一一列舉。

使用沙盒虛擬環境或容器。[Windows 沙盒](https://learn.microsoft.com/zh-cn/windows/security/threat-protection/windows-sandbox/windows-sandbox-overview)，[LXC](https://linuxcontainers.org/), [Docker](https://www.docker.com/)等等，這裡不再詳述。

##總結

本文篇幅有點長，感謝看到這裡，文章一開始所列出的疑問，相信都已經解答完畢。

--8<-- "footer_tc.md"


> 此帖子是使用 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遺漏之處。 
