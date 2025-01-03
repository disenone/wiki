---
layout: post
title: Python の雑談 1 - \_\_builtins\_\_ の探求
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
description: '`__builtin__` と `__builtins__` には何か違いがありますか？`__builtins__` は main モジュールと他のモジュールでは異なりますか？なぜ異なって設定されているのですか？`__builtins__`
  はどこで定義されていますか？この記事では、`__builtins__` に関するマイナーな情報や、関連する内容を探ってみます。見逃せませんよ。'
figures: []
---

<meta property="og:title" content="Python 杂谈 1 - 探究 __builtins__ - Disenone" />

##序文

私たちは、`__builtins__` がグローバルな名前空間に最初から存在するオブジェクトであり、`Python` がコードレベルで利用可能にするために意図的に公開していることを知っています。しかし、少し興味深いのは、`__builtins__` が `main` モジュール（つまり `__main__` を指しますが、同じモジュールを指すことになります。後述の文中では混在する可能性があります）の中では `__builtin__` モジュールを表し、他のモジュールでは `__builtin__.__dict__` を表すということです。実際に `__builtins__` を直接使用することは推奨されていませんが、どうして2つの状況があるのかを理解したいですね。この記事では、この設定の由来について考察し、`__builtin__` と `__builtins__` の違い、`main` モジュールと他のモジュールで `__builtins__` が異なる理由、そして `__builtins__` がどこで定義されているのかについて探求します。


## `__builtin__`

`__builtins__` を探る前に、まず `__builtin__` が何かを見てみる必要があります。`__builtin__` はすべての組み込みオブジェクトが格納されているモジュールであり、通常、私たちが直接使用する`Python`の組み込みオブジェクトは、本質的に`__builtin__`モジュール内のオブジェクトであり、つまり`__builtin__.__dict__`に配置されており、これは`Python`の組み込み名前空間に対応しています。この重要なポイントを覚えておいてください：`__builtin__`は`module`モジュールです。`Python`ソースコードから`__builtin__`モジュールの定義と使用を見つけることができます（注意：ここで言及される`Python`ソースコードはすべてCPython-2.7.18ソースコードを指します）。

``` c
// pythonrun.c
void
Py_InitializeEx(int install_sigs)
{
    PyInterpreterState *interp;
    ...
__builtin__を初期化します
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

dictに組み込みオブジェクトを追加する
    ...
}

// ceval.c
組み込み関数の取得
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

Pythonの初期化時には、`_PyBuiltin_Init`が呼び出され、`__builtin__`モジュールが作成され、その中に組み込みオブジェクトが追加されます。インタプリタ自体は、`interp->builtins = __builtin__.__dict__`を参照し、現在実行中のスタックフレーム構造も`current_frame->f_builtins`を参照します。したがって、コードを実行する際に名前に基づいてオブジェクトを検索する必要があるとき、Pythonは`current_frame->f_builtins`を検索し、すべての組み込みオブジェクトを取得できます。

```c
// ceval.c
TARGET(LOAD_NAME)
{
// Search for the name in the f->f_locals namespace.
    ...
    if (x == NULL) {
// 他の領域を探してください
        x = PyDict_GetItem(f->f_globals, w);
        if (x == NULL) {
このテキストを日本語に翻訳してください:

// ここで組み込みスペースを探してください
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

最後、`__builtin__` という名前は本当に混乱を招くので、`Python3` では既に `builtins` に改名されています。


## `__builtins__`

`__builtins__` というものはちょっと変わった振る舞いをするんだよ：
`main` モジュール内（`main` モジュール、または `最高層レベルコード実行環境` とも呼ばれるものは、ユーザが最初に起動する `Python` モジュールを指定するものであり、通常、コマンドラインで `python xxx.py` を実行する際に `xxx.py` というモジュールが実行されます）、`__builtins__ = __builtin__`；
他のモジュールで `__builtins__ = __builtin__.__dict__` が使われています。

同じ名前を持つことがありますが、異なるモジュールで使われる場合は異なる振る舞いをすることがあります。これは混乱を招く可能性がありますが、この設定を知っていれば、Python で __builtins__ を使用することがサポートされ、十分安全なコードを書くことができます。

``` python
def SetBuiltins(builtins, key, val):
    if isinstance(builtins, dict):
        builtins[key] = val
    else:
        setattr(builtins, key, val)

SetBuiltins(__builtins__, 'test', 1)
```

`__builtins__` を使用することはお勧めしません。

> CPythonの実装の詳細：ユーザーは`__builtins__`に触れてはいけません。これは厳密に実装の詳細です。組み込み名前空間の値を上書きしたいユーザーは、`__builtin__`モジュールをインポートして適切に属性を変更すべきです。

もちろんですが、そのような疑念はいつかあなたを不安にさせることになるでしょう。だからこそ、私は続けて探求することを決意し、その結果、この記事が生まれました。以下の内容は、__CPython implementation detail__ に詳細に踏み込む予定です。

## Restricted Execution

Restricted Execution は、安全でないコードを制限付きで実行することを意味します。 ここでの制限とは、ネットワークや入出力などを制限することができ、コードを特定の実行環境に制限し、コードの実行権限を制御し、コードが外部環境やシステムに影響を与えるのを防ぎます。 一般的な使用例は、オンラインコード実行サイトのようなものです。 例えば、[pythonsandbox](https://pythonsandbox.dev/)すみません、入力内容が空白です。もう一度送信してください。

あなたの推測通り、`Python` の `__builtins__` に関する設定は Restricted Execution と関連があります。`Python` は2.3バージョン以前に、同様の機能[Restricted Execution](https://docs.python.org/2.7/library/restricted.html)後に行き詰まったことが判明したため、その機能を削除せざるを得なくなりました。しかし、コードはまだ 2.7.18 バージョンに残っているので、古代学的研究を行うことができます。

まず、`Python`のソースコードで`__builtins__`がどのように設定されているかを見てみましょう。

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

「__main__.__dict__['__builtins__']」を設定します。既に存在する場合はスキップします。
    if (PyDict_GetItemString(d, "__builtins__") == NULL) {
        PyObject *bimod = PyImport_ImportModule("__builtin__");
        if (bimod == NULL ||
            PyDict_SetItemString(d, "__builtins__", bimod) != 0)
            Py_FatalError("can't add __builtins__ to __main__");
        Py_XDECREF(bimod);
    }
}
```

`initmain` function では、`Python` は `__main__` モジュールに `__builtins__` 属性を設定します。デフォルトではこの属性は `__builtin__` モジュールと等しい値になりますが、既に設定されている場合は再設定はされません。この特性を利用して、`__main__.__builtins__` を変更することで内蔵関数を制限してコードの実行権限を制御することが可能です。具体的な方法についてはここでは触れませんが、`__builtins__` がどのように伝播されるかを見てみましょう。

##`__builtins__` の伝達

新しいスタックフレームを作成する際に：

```c
PyFrameObject *
PyFrame_New(PyThreadState *tstate, PyCodeObject *code, PyObject *globals,
            PyObject *locals)
{
    ...
    if (back == NULL || back->f_globals != globals) {
// 取 globals['__builtins__'] 作为新スタックフレームの __builtins__
`// builtin_object` は文字列 '__builtins__' を表しています。
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
// または直接前のスタックフレームの f_builtins を継承する
        builtins = back->f_builtins;
        assert(builtins != NULL && PyDict_Check(builtins));
        Py_INCREF(builtins);
    }
    ...
    f->f_builtins = builtins;
    f->f_globals = globals;
}
```

新しいスタックフレームを作成する際、`__builtins__` の処理には主に2つのケースがあります：1つは上位のスタックフレームがない場合、`globals['__builtins__']`を取得すること；もう1つは直接上位スタックフレームの`f_builtins`を取得することです。総じて考えると、通常、`__main__` で設定された `__builtins__` は、後続のスタックフレームに引き継がれ、実質的に同じものを共有していると理解できます。

`import` 模块时：

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

こちらで新しいロードされるモジュールの __builtins__ 属性を設定してください。
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

`import` の場合、他のモジュールをインポートすると、そのモジュールの `__builtins__` が `PyEval_GetBuiltins()` の戻り値に設定されます。この関数は既に言及しましたが、ほとんどの場合、`current_frame->f_builtins` に相当します。`__main__` モジュール内の `import` については、`current_frame` は `__main__` モジュールのフレームであり、`current_frame->f_builtins = __main__.__dict__['__builtins__']` になります（前述の `PyFrame_New` の最初のケース）。

新しいモジュールをロードすると、`PyEval_EvalCode`が新しいモジュールのコードを実行します。`globals`や`locals`などの引数は実際にはモジュール自身の`__dict__`であり、かつモジュール`m.__dict__['__builtins__'] = PyEval_GetBuiltins()`が設定されます。

総合的に見ると、`__main__` モジュールから import されるモジュールも、`__main__` の `__builtins__` を継承し、内部の import に伝えられるため、`__main__` からロードされるすべてのモジュールとサブモジュールが、同じ `__main__` の `__builtins__` を共有できるようになります。

モジュール内で呼び出される関数の場合はどうでしょうか？モジュール内の関数の場合、作成および呼び出し時には：

```c
// ceval.c
関数を作成します
TARGET(MAKE_FUNCTION)
{
    v = POP(); /* code object */

ここでの f->f_globals は、モジュール自体のグローバル変数を指します。先ほどの文脈からもわかる通り、これは m.__dict__ と同じです。
    x = PyFunction_New(v, f->f_globals);
    ...
}

PyObject *
PyFunction_New(PyObject *code, PyObject *globals)
{
    PyFunctionObject *op = PyObject_GC_New(PyFunctionObject,
                                        &PyFunction_Type);
    ...
ここでの意味は op->func_globals = globals = f->f_globals と同等である。
    op->func_globals = globals;
}

// 関数を呼び出す
static PyObject *
fast_function(PyObject *func, PyObject ***pp_stack, int n, int na, int nk)
{
    PyCodeObject *co = (PyCodeObject *)PyFunction_GET_CODE(func);
    // globals = func->func_globals
    PyObject *globals = PyFunction_GET_GLOBALS(func);
    ...
// globals 传给 PyEval_EvalCodeEx，里面就会传给 PyFrame_New 来创建新的栈帧

// globals パラメーターは PyEval_EvalCodeEx に渡され、その中で PyFrame_New に渡されて新しいフレームが作成されます。
    return PyEval_EvalCodeEx(co, globals,
                             (PyObject *)NULL, (*pp_stack)-n, na,
                             (*pp_stack)-2*nk, nk, d, nd,
                             PyFunction_GET_CLOSURE(func));
}
```

関数を作成する際には、`f->f_globals` が関数の構造体変数である`func_globals`に保存され、モジュール`m`に対しては、`f->f_globals = m.__dict__`となります。関数を実行する際に、`PyFrame_New`に渡す`globals`パラメータは、作成時に保存された`func_globals`です。`__builtins__`は自ずと`func_globals`から取得できます。

これまで、`__builtins__` の伝達は一貫性を確保することができるため、すべてのモジュール、サブモジュール、関数、およびスタックフレームは同じものを参照でき、つまり同じ組み込み名前空間を持っています。

##指定された `__main__` モジュールを実行します。

私たちはすでに `__main__` モジュール自体の `__builtins__` がすべてのサブモジュール、関数、およびスタックフレームに渡されることを知っていますが、コマンドラインで `python a.py` を実行すると、Python は `a.py` を `__main__` モジュールとして実行します。これがどのように実現されているのかというと、どのようにでしょうか。

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
モジュールのインポーターを使用してコードを実行しようとしています。
    if (filename != NULL) {
        sts = RunMainFromImporter(filename);
    }
    ...
一般、私たち自身の Python ファイルでは、これを使用して実行します。
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
// __file__属性を設定します
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
// 从 pyc 文件读取代码对象 co ，并执行代码
// PyEval_EvalCode 里面也同样会调用 PyFrame_New 创建新栈帧
    v = PyEval_EvalCode(co, globals, locals);
    ...
}
```

実行すると、通常、 `python a.py` は `PyRun_SimpleFileExFlags` に進みます。`PyRun_SimpleFileExFlags` では `__main__.__dict__` が取得され、それがコードの実行時の `globals` と `locals` として使用され、最終的に `PyFrame_New` に渡されて `a.py` を実行する新しいフレームが作成されます。モジュールと関数で渡される `__builtins__` を考慮に入れると、その後のコードの実行で `current_frame->f_builtins = __main__.__builtins__.__dict__` が共有されることが確認できます。


##制限付き実行に関する再考

`Python` 2.3 バージョン以前では、[Restricted Execution](https://docs.python.org/2.7/library/restricted.html)，`__builtins__` の特性を利用して作成されました。または、`__builtins__` が`__main__`モジュールではモジュールオブジェクトとして設計されており、他のモジュールでは`dict`オブジェクトとして設計されているのは、__Restricted Execution__ を実現するためです。

このシチュエーションを考えてみましょう：もし `__builtin__` モジュールを自由にカスタマイズして `__main__.__builtins__` に設定できるなら、その結果、今後のすべてのコード実行が、私たちがカスタマイズしたモジュールを使用するようになります。特定のバージョンの `open`、`__import__`、`file` などの組み込み関数や型をカスタマイズできるだけでなく、この方法はコードの実行権限を制限し、不安全な関数呼び出しを防いだり、危険なファイルへのアクセスを制限するのに役立つかもしれませんね？

"Python" は以前、この種の試みを行い、この機能を実現するモジュールは `rexec` と呼ばれます。

### `rexec`

私は"rexec"の実装について深く説明するつもりはありません。なぜなら、その原理はすでに前文で説明したことであり、このモジュール自体がすでに廃止されているからです。私はこれらの内容を簡潔にまとめて、重要なコードを引用しております。参照用に。


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

`r_execfile` 関数はファイルを `__main__` モジュールとして実行しますが、カスタマイズされた `__main__` です。`self.add_module('__main__')` の中で、モジュールの `m.__builtins__ = self.modules['__builtin__']` が設定されます。この `__builtin__` は `make_builtin` によってカスタマイズ生成され、そこで `__import__`、`reload`、`open` 関数が置き換えられ、`file` クラスが削除されています。これにより、実行するコードが組み込み名前空間にアクセスすることを制御できます。

いくつかの組み込みモジュールについて、 `rexec` はカスタマイズされ、安全でないアクセスを保護します。 例えば、 `sys` モジュールは一部のオブジェクトのみを保持し、カスタマイズされた `self.loader`、`self.importer` を通じて `import` 時にカスタムモジュールを優先的にロードします。

コードの詳細に興味がある場合は、関連するソースコードを自分で参照してください。

###`rexec` の失敗

前述の通り、`Python 2.3`以降、`rexec`は廃止されており、この手法が実行不可能であることが証明されています。興味を持ったので、簡単にその由来をたどってみましょう：

コミュニティで [Bug](https://mail.python.org/pipermail/python-dev/2002-December/031160.html)開発者の間でディスカッションを引き起こしました：

    > it's never going to be safe, and I doubt it's very useful as long as it's not safe.

    > Every change is a potential security hole.

    > it's hard to predict what change is going to break it.

    > I don't expect you'll ever reach the point where it'll be wise to advertise this as safe.  I certainly won't.

    >  this is only a useful occupation if you expect to eventually reach a point where you expect that there aren't any security flaws left.  Jeremy & I both doubt that Python will ever reach that level, meaning that the whole exercise of fixing security flaws is a waste of time (if you know you *can't* make it safe, don't waste time trying).

    > I agree (but I have said that in past) the best thing is to deprecate/rip out rexec.

    > The code will still be in older versions if someone decides to pick it up and work on it as a separate project.

このバグの原因は、`Python` が新しいスタイルのクラス `object` を導入したことにより、`rexec` が正常に機能しなくなったことです。開発者は将来的にはこのような状況を避けるのが難しいと述べており、任意の変更が`rexec`に脆弱性を引き起こし、正常に機能しないか、権限制限を破られる可能性があることを示しています。完全に脆弱性のない安全な環境を提供するという理想を実現することは基本上不可能であり、開発者は継続的に修正を行う必要があり、多くの時間が無駄になることを指摘しています。結果的に、このモジュールである`rexec`は廃止され、`Python`も同様の機能を提供しなくなりました。ただし、`__builtins__`に関する設定は、互換性の問題などから残されることになりました。

2010 年ごろ、1人のプログラマーが [pysandbox](https://github.com/vstinner/pysandbox)提供できるPythonの`rexec`を代替できる環境構築に尽力してました。しかし、3年後、作者自らがこのプロジェクトを放棄し、なぜそのプロジェクトが失敗だと考えるのか詳細に説明しています：[The pysandbox project is broken](https://mail.python.org/pipermail/python-dev/2013-November/130132.html)同じく，他の作家がこのプロジェクトの失敗をまとめた記事もあります：[The failure of pysandbox](https://lwn.net/Articles/574215/)もし興味があれば、実際に原文を読んでみてください。こちらにはいくつかの要約も添えていますので、理解の助けになるかもしれません：

> After having work during 3 years on a pysandbox project to sandbox untrusted code, I now reached a point where I am convinced that pysandbox is broken by design. Different developers tried to convinced me before that pysandbox design is unsafe, but I had to experience it myself to be convineced.

> I now agree that putting a sandbox in CPython is the wrong design. There are too many ways to escape the untrusted namespace using the various introspection features of the Python language. To guarantee the [safety] of a security product, the code should be [carefully] audited and the code to review must be as small as possible. Using pysandbox, the "code" is the whole Python core which is a really huge code base. For example, the Python and Objects directories of Python 3.4 contain more than 126,000 lines of C code.

> The security of pysandbox is the security of its weakest part. A single bug is enough to escape the whole sandbox.

> pysandbox cannot be used in practice. To protect the untrusted namespace, pysandbox installs a lot of different protections. Because of all these protections, it becomes hard to write Python code. Basic features like "del dict[key]" are denied. Passing an object to a sandbox is not possible to sandbox, pysandbox is unable to proxify arbitary objects. For something more complex than evaluating "1+(2*3)", pysandbox cannot be used in practice, because of all these protections.

__pysandbox__ の作者は、Python の中でサンドボックス環境を作ることはデザイン上の誤りだと考えています。サンドボックスから抜け出す方法が多すぎるからです。Python は豊富な言語機能を提供しており、CPython のソースコードは非常に大規模であり、十分なセキュリティを保証することはほとんど不可能です。そして、__pysandbox__ の開発過程は、修正を繰り返していく中で進んでおり、修正が多すぎ、制限が多すぎるため、作者自身も__pysandbox__ が実際に使用できないと考えています。なぜなら、多くの文法的な機能が制限されて使用できなくなっており、例えば単純な `del dict[key]` も使用できません。

##制限付きの実行。出口はどこにあるのか。

`rexec` および `pysandbox` など、Python をパッチしてサンドボックス環境を提供する方法はもはや有効ではないようですね。では、Python に適用可能なサンドボックス環境を与えるには、どのようにすればよいのでしょうか？

私はここでいくつかの追加実現方法や事例を収集しましたので、参考や参照に便利です：

* [PyPy](https://doc.pypy.org/en/latest/sandbox.html)1つの[分岐](https://foss.heptapod.net/pypy/pypy/-/tree/branch/sandbox-2)サンドボックス機能を追加して、[sandboxlib](https://foss.heptapod.net/pypy/sandboxlib)PyPyのサンドボックス環境版を独自にコンパイルすることができます。興味があれば、自分で設定してみてください。こちらの[説明](https://foss.heptapod.net/pypy/pypy/-/issues/3192)PyPy の仕組みは、子プロセスを作成し、そのすべての入出力とシステムコールを外部プロセスにリダイレクトし、外部プロセスがこれらの権限を制御するというものです。また、メモリと CPU の使用量も制御できます。ただし、このブランチにはしばらく新しいコミットがないので、使用には注意が必要です。

(https://en.wikipedia.org/wiki/Seccomp)Linux カーネルが提供するセキュリティツール、[libseccomp](https://github.com/seccomp/libseccomp/tree/main/src/python)Pythonのバインディングが提供され、コードに埋め込んで使用することができます。または、seccompに基づいたツールを使用してコードを実行することもできます。例えば、[Firejail](https://firejail.wordpress.com/)(https://apparmor.net/)(https://github.com/openedx/codejail)AppArmor に基づく Python サンドボックス環境であり、興味があれば試してみてください。同様のツールは他にも多数ありますが、ここでは一つずつ挙げることはしません。

サンドボックス仮想環境またはコンテナを使用してください。[Windowsサンドボックス](https://learn.microsoft.com/zh-cn/windows/security/threat-protection/windows-sandbox/windows-sandbox-overview)，[LXC](https://linuxcontainers.org/), [Docker](https://www.docker.com/)すみませんが、そのテキストは中国語です。私は日本語に翻訳します。

##要求翻译为日语。

本文の長さは少々ありますが、ここまで読んでいただき、最初に挙げられた疑問はすべて解決されたと信じています。

--8<-- "footer_ja.md"


> この投稿はChatGPTによって翻訳されましたので、ご意見や[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。 
どこか見落としている箇所があれば教えてください。 
