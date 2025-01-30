---
layout: post
title: Python の雑談 1 - __builtins__ の探求
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
description: '`__builtin__` 跟 `__builtins__` 有什么区别？`__builtins__` 在 main 模块跟其他模块是不同的？为什么会设定成不同？`__builtins__`
  是在哪里定义的？本文我们来探讨一下关于 `__builtins__` 的冷知识，并且还有一些引申的内容，不容错过。'
figures: []
---

<meta property="og:title" content="Python 杂谈 1 - 探究 __builtins__ - Disenone" />

##引子

私たちは知っていますが、`__builtins__` はグローバル名前空間に存在するオブジェクトであり、`Python` が意図的にコード層に露出させているもので、コードのどこにでも直接使用できます。しかし、少し冷たい知識として、`__builtins__` は `main` モジュール（つまり `__main__`、これらは同じモジュールを指し、後の文脈で混用されるかもしれません）では `__builtin__` モジュールですが、他のモジュールでは `__builtin__.__dict__` を表します。これには少し驚くべきことがあります。公式では `__builtins__` の直接使用は推奨されていませんが、私に2つの状況を提示するのはどういうことなのでしょうか？この記事では、この設定の由来を掘り下げ、この過程で以下の疑問に対する答えも見つけていきましょう：`__builtin__` と `__builtins__` の違いは何ですか？`__builtins__` が `main` モジュールと他のモジュールで異なる設定になっている理由は何ですか？`__builtins__` はどこで定義されているのですか？


## `__builtin__`

`__builtins__` を探る前に、まず `__builtin__` が何かを見てみましょう。`__builtin__` は全ての組み込みオブジェクトが格納されているモジュールであり、私たちが普段直接使用する `Python` の組み込みオブジェクトは、本質的に `__builtin__` モジュール内のオブジェクトであり、すなわち `__builtin__.__dict__` に格納されています。これは `Python` の組み込み名前空間に対応しています。この重要な知識を覚えておいてください：`__builtin__` はモジュールです。私たちは `Python` のソースコードの中で `__builtin__` モジュールの定義と使用を見つけることができます（注意：以下で言及する `Python` ソースコードは、CPython-2.7.18 ソースコードを指します）。

``` c
// pythonrun.c
void
Py_InitializeEx(int install_sigs)
{
    PyInterpreterState *interp;
    ...
// __builtin__を初期化します
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

// dict にビルトインオブジェクトを追加する
    ...
}

// ceval.c
// ビルトインを取得する
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

`Python`の初期化では、`_PyBuiltin_Init`が呼び出され、`__builtin__`モジュールが作成され、ビルトインオブジェクトが追加されます。 インタプリタ自体は、`interp->builtins = __buintin__.__dict__`を参照しますし、現在のフレーム構造も`current_frame->f_builtins`を参照します。したがって、コードを実行する際にオブジェクトを名前で検索する必要がある場合、`Python`は`current_frame->f_builtins`を検索し、すべてのビルトインオブジェクトにアクセスできます。

```c
// ceval.c
TARGET(LOAD_NAME)
{
// まず f->f_locals 名前空間の中を探す
    ...
    if (x == NULL) {
// 全体のスペースを再度検索してください
        x = PyDict_GetItem(f->f_globals, w);
        if (x == NULL) {
// ここで内蔵スペースを探します
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

最後に、`__builtin__`という名前は本当に混乱を招くので、`Python3`では`builtins`という名前に変更されています。


## `__builtins__`

`__builtins__`の挙動はちょっと奇妙です：
* `main` モジュール内では（`main` モジュール、または `最高層コード実行環境` とも呼ばれ、ユーザーが最初に起動する `Python` モジュールです。通常、コマンドラインで `python xxx.py` を実行する際の `xxx.py` というモジュールです）、`__builtins__ = __builtin__`；
* 他のモジュールでは `__builtins__ = __builtin__.__dict__` です。

同じ名前ですが、異なるモジュールでの挙動は異なります。このような設定は混乱を招くことがあります。しかし、この設定を理解していれば、`Python` の `__builtins__` を使用するためのサポートは十分です。混乱は、安全なコードを書く際には影響を与えません。例えば：

``` python
def SetBuiltins(builtins, key, val):
    if isinstance(builtins, dict):
        builtins[key] = val
    else:
        setattr(builtins, key, val)

SetBuiltins(__builtins__, 'test', 1)
```

注意が必要ですが、実際には `__builtins__` の使用は推奨されていません：

> __CPythonの実装詳細__: ユーザーは `__builtins__` に触れるべきではありません。それは厳密に実装の詳細です。ビルトインネームスペースの値をオーバーライドしたい場合は、`__builtin__`（‘s’なし）モジュールをインポートし、その属性を適切に変更する必要があります。

当然、このような疑問は、いつかあなたをじれったくさせるでしょう。私はこちらで探求を続けることに決めました。そのため、この文章が生まれました。以下の内容では、__CPython implementation detail__ に深く入っていきます。

## Restricted Execution

制限付き実行とは、安全でないコードを制限された形で実行することを指します。制限とは、ネットワークやIOなどの制限を含み、コードを特定の実行環境に制約し、コードの実行権限を管理することで、外部の環境やシステムに影響を与えないようにすることです。一般的な使用例として、いくつかのオンラインコード実行サイトがあります。例えば、こちらのサイト：[pythonsandbox](https://pythonsandbox.dev/)Sure, the text "。" in Japanese language is "。".

あなたの推測通り、`Python` プログラムにおける `__builtins__` の設定は制限付き実行と関連しています。`Python` は2.3版以前において、同様の機能 [Restricted Execution](https://docs.python.org/2.7/library/restricted.html)後に実行不可能と判明したため、この機能は無効になりましたが、コードはまだ2.7.18バージョンに残っているので、過去の状態を確認できます。

まずは`Python`のソースコードで`__builtins__`が設定されている部分を見てみましょう：

``` c
// pythonrun.c
static void initmain(void)
{
    PyObject *m, *d;
// __main__ モジュールを取得する
    m = PyImport_AddModule("__main__");
    if (m == NULL)
        Py_FatalError("can't create __main__ module");

    // d = __main__.__dict__
    d = PyModule_GetDict(m);

// __main__.__dict__['__builtins__']を設定します。既に存在する場合はスキップします。
    if (PyDict_GetItemString(d, "__builtins__") == NULL) {
        PyObject *bimod = PyImport_ImportModule("__builtin__");
        if (bimod == NULL ||
            PyDict_SetItemString(d, "__builtins__", bimod) != 0)
            Py_FatalError("can't add __builtins__ to __main__");
        Py_XDECREF(bimod);
    }
}
```

`initmain` 中、`Python` では `__main__` モジュールに `__builtins__` 属性が設定され、デフォルトでは `__builtin__` モジュールと同じになります。しかし、既にある場合は再設定されずにスキップされます。この特性を利用して、`__main__.__builtins__` を変更して、いくつかの組み込み機能を変更して、コードの実行権限を制限することができます。具体的な方法については触れませんが、`__builtins__` がどのように渡されるかを見てみましょう。

##`__builtins__` の渡し方

新しいスタックフレームを作成する際には：

```c
PyFrameObject *
PyFrame_New(PyThreadState *tstate, PyCodeObject *code, PyObject *globals,
            PyObject *locals)
{
    ...
    if (back == NULL || back->f_globals != globals) {
// 新しいスタックフレームの __builtins__ として globals['__builtins__'] を取る
// builtin_object は文字列 '__builtins__' です
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
// または、直接前のスタックフレームの f_builtins を継承します。
        builtins = back->f_builtins;
        assert(builtins != NULL && PyDict_Check(builtins));
        Py_INCREF(builtins);
    }
    ...
    f->f_builtins = builtins;
    f->f_globals = globals;
}
```

新しいスタックフレームを作成する際、`__builtins__`の処理には主に2つのケースがあります。一つは、上位のスタックフレームが存在しない場合に`globals['__builtins__']`を取得することです。もう一つは、上位のスタックフレームの`f_builtins`を直接取得することです。これらを合わせて見ると、一般的には`__main__`で設定された`__builtins__`がその後のスタックフレームに継承され、同じものを共有していると理解できます。

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

// ここで新しく読み込まれたモジュールの __builtins__ 属性を設定します
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

他のモジュールを `import` すると、そのモジュールの `__builtins__` が `PyEval_GetBuiltins()` の戻り値に設定されます。この関数についてはすでに述べましたが、大部分の状況では `current_frame->f_builtins` に相当します。`__main__` モジュール内の `import` に関しては、`current_frame` は `__main__` モジュールのスタックフレームであり、`current_frame->f_builtins = __main__.__dict__['__builtins__']`（前述の `PyFrame_New` の第一のケース）となります。

読み込まれた新しいモジュールは、`PyEval_EvalCode` を使用して新しいモジュール内のコードを実行します。このとき、`PyEval_EvalCode` に渡される引数 `globals` と `locals` は実際にはモジュール自身の `__dict__` であり、さらにモジュール `m.__dict__['__builtins__'] = PyEval_GetBuiltins()` となっています。

総合的に見ると、`__main__` モジュールから `import` されたモジュールは、`__main__` 内の `__builtins__` を継承し、内部の `import` で引き継がれることがわかります。これにより、すべての `__main__` から読み込まれたモジュールとサブモジュールが、`__main__` からの同じ `__builtins__` を共有できることが保証されます。

モジュール内で呼び出される関数の場合はどうでしょうか？モジュール内の関数について、作成および呼び出し時には：

```c
// ceval.c
// 関数を作成する
TARGET(MAKE_FUNCTION)
{
    v = POP(); /* code object */

// ここでの f->f_globals は、モジュール自身の globals に相当し、上記からもわかるように、m.__dict__ にも相当します。
    x = PyFunction_New(v, f->f_globals);
    ...
}

PyObject *
PyFunction_New(PyObject *code, PyObject *globals)
{
    PyFunctionObject *op = PyObject_GC_New(PyFunctionObject,
                                        &PyFunction_Type);
    ...
ここは op->func_globals = globals = f->f_globals となります。
    op->func_globals = globals;
}

関数を呼び出す
static PyObject *
fast_function(PyObject *func, PyObject ***pp_stack, int n, int na, int nk)
{
    PyCodeObject *co = (PyCodeObject *)PyFunction_GET_CODE(func);
    // globals = func->func_globals
    PyObject *globals = PyFunction_GET_GLOBALS(func);
    ...
// globals is passed to PyEval_EvalCodeEx, which in turn will be passed to PyFrame_New to create a new frame.
    return PyEval_EvalCodeEx(co, globals,
                             (PyObject *)NULL, (*pp_stack)-n, na,
                             (*pp_stack)-2*nk, nk, d, nd,
                             PyFunction_GET_CLOSURE(func));
}
```

関数を作成する際、`f->f_globals` が関数構造体変数 `func_globals` に保存されます。そして、モジュール `m` に対しては、`f->f_globals = m.__dict__` となります。関数が実行されるとき、`PyFrame_New` に渡される `globals` 引数は、作成時に保存された `func_globals` であり、`__builtins__` は自然に `func_globals` の中から取得できます。

これまで`__builtins__`の伝達は一貫性を確保できるため、すべてのモジュール、サブモジュール、関数、スタックフレームなどが同じものを参照でき、つまり同じ組み込み名前空間を持っています。

##`__main__` モジュールを指定して実行

私たちはすでに `__main__` モジュール自身の `__builtins__` がすべてのサブモジュール、関数およびスタックフレームに渡されることを知っています。そして、コマンドラインで `python a.py` を実行すると、Python は `a.py` を `__main__` モジュールとして実行しますが、これはどのように実現されているのでしょうか：

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
// モジュールのインポーターを使ってコードを実行してみる
    if (filename != NULL) {
        sts = RunMainFromImporter(filename);
    }
    ...
// 一般的に自分の py ファイルは、これを使って実行します
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
// __file__属性の設定
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
// pycファイルからコードオブジェクトcoを読み込み、コードを実行する
// PyEval_EvalCode の中でも同様に PyFrame_New を呼び出して新しいスタックフレームを作成します
    v = PyEval_EvalCode(co, globals, locals);
    ...
}
```

`python a.py` を実行すると、一般的には `PyRun_SimpleFileExFlags` に到達し、そこで `__main__.__dict__` を取り出して、コード実行時の `globals` と `locals` として使用します。最終的にはこれが `PyFrame_New` に渡され、新しいスタックフレームが作成されて `a.py` を実行します。前述の通り、モジュールや関数内で `__builtins__` を渡すことにより、以降のコード実行で同じ `current_frame->f_builtins = __main__.__builtins__.__dict__` を共有できるようになります。


##再論制限された実行

`Python` の 2.3 バージョン以前に提供されていた [Restricted Execution](https://docs.python.org/2.7/library/restricted.html)これは `__builtins__` の特性に基づいて作られています。あるいは、`__builtins__` が `__main__` モジュール内ではモジュールオブジェクトであり、他のモジュール内では `dict` オブジェクトとして設計されているのは、__Restricted Execution__ を実現するためであると考えることができます。

考えてみてください：もし自分たちの`__builtin__`モジュールを自由にカスタマイズして、それを`__main__.__builtins__`に設定できるとしたら、その後に実行されるすべてのコードは、カスタマイズしたモジュールを使用することになります。特定のバージョンの`open`、`__import__`、`file`などの組み込み関数や型をカスタマイズできる可能性があります。さらに、この方法はコードの実行権限を制限し、危険な関数呼び出しを防いだり、危険なファイルにアクセスさせないために役立つかもしれませんね。

`Python` 当時にこのような試みを行い、この機能を実現するモジュールは `rexec` と呼ばれました。

### `rexec`

私は「rexec」の実装について詳しく説明するつもりはありません。なぜなら、その原理はすでに前文で説明されており、さらにこのモジュール自体が廃止されているからです。私はいくつかのキーコードの要約を簡単に行い、参照しやすくします。


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

「r_execfile」関数はファイルを「__main__」モジュールとして実行しますが、ただし「__main__」はカスタマイズされています。「self.add_module('__main__')」内では、モジュールの` m.__builtins__ = self.modules['__builtin__']`が設定されますが、この`__builtin__`は`make_builtin`によって生成され、そこで`__import__`、`reload`、`open`関数が置換され、`file`型が削除されています。これにより、実行されるコードが組み込み名前空間にアクセスする方法を制御できます。

一部の組み込みモジュールに対して、`rexec` はカスタマイズを行い、安全でないアクセスを保護しています。例えば、`sys` モジュールにおいては、一部のオブジェクトのみが保持されており、カスタマイズされた `self.loader` や `self.importer` を介して、`import` の際に優先的にカスタマイズされたモジュールが読み込まれるようになっています。

コードの詳細に興味がある場合は、関連するソースコードをご自身で参照してください。

###`rexec` の失敗

上文では、`Python 2.3` 以降、`rexec` は廃止されたことが言及されています。なぜなら、この方法が実行可能ではないことが証明されたからです。好奇心を抱きながら、簡単にその起源を辿ってみましょう：

(https://mail.python.org/pipermail/python-dev/2002-December/031160.html)開発者間での議論を引き起こしました：

    > it's never going to be safe, and I doubt it's very useful as long as it's not safe.

    > Every change is a potential security hole.

    > it's hard to predict what change is going to break it.

    > I don't expect you'll ever reach the point where it'll be wise to advertise this as safe.  I certainly won't.

    >  this is only a useful occupation if you expect to eventually reach a point where you expect that there aren't any security flaws left.  Jeremy & I both doubt that Python will ever reach that level, meaning that the whole exercise of fixing security flaws is a waste of time (if you know you *can't* make it safe, don't waste time trying).

    > I agree (but I have said that in past) the best thing is to deprecate/rip out rexec.

    > The code will still be in older versions if someone decides to pick it up and work on it as a separate project.

このバグの原因は、`Python` が新しいスタイルのクラス (`new-style class`) `object` を導入したためで、これにより `rexec` が正常に機能しなくなりました。開発者は、今後予見可能な期間において、この状況を避けることは非常に難しいと述べており、任意の修正が `rexec` に脆弱性を引き起こし、正常に動作しなかったり、権限の制限を突破されたりする可能性があります。基本的に、脆弱性なしで安全な環境を提供するというビジョンを実現することはほとんど不可能であり、開発者は不断に修正作業を続ける必要があり、大量の時間を無駄にしてしまいます。最終的に、`rexec` というモジュールは廃止され、`Python` も類似の機能を提供しなくなりました。しかし、`__builtins__` の設定については、互換性などの問題から引き続き保持されることになりました。

2010年頃、あるプログラマーが[pysandbox](https://github.com/vstinner/pysandbox)`rexec` の代替となる `Python` サンドボックス環境の提供を目指しました。しかし 3 年後、作者はこのプロジェクトを自主的に放棄し、なぜ作者がこのプロジェクトを失敗だと考えているのかを詳述しました：[The pysandbox project is broken](https://mail.python.org/pipermail/python-dev/2013-November/130132.html)、他の著者もこのプロジェクトの失敗をまとめた文章を書いています：[The failure of pysandbox](https://lwn.net/Articles/574215/)もし興味があるなら、具体的に原文を読んでみてください。ここには要約もありますので、理解の助けになるかもしれません：

> After having work during 3 years on a pysandbox project to sandbox untrusted code, I now reached a point where I am convinced that pysandbox is broken by design. Different developers tried to convinced me before that pysandbox design is unsafe, but I had to experience it myself to be convineced.

> I now agree that putting a sandbox in CPython is the wrong design. There are too many ways to escape the untrusted namespace using the various introspection features of the Python language. To guarantee the [safety] of a security product, the code should be [carefully] audited and the code to review must be as small as possible. Using pysandbox, the "code" is the whole Python core which is a really huge code base. For example, the Python and Objects directories of Python 3.4 contain more than 126,000 lines of C code.

> The security of pysandbox is the security of its weakest part. A single bug is enough to escape the whole sandbox.

> pysandbox cannot be used in practice. To protect the untrusted namespace, pysandbox installs a lot of different protections. Because of all these protections, it becomes hard to write Python code. Basic features like "del dict[key]" are denied. Passing an object to a sandbox is not possible to sandbox, pysandbox is unable to proxify arbitary objects. For something more complex than evaluating "1+(2*3)", pysandbox cannot be used in practice, because of all these protections.

「pysandbox」の作者は、Pythonの中にサンドボックス環境を置くのは間違った設計だと考えています。サンドボックスから脱出する方法があまりにも多く、Pythonの提供する言語機能は非常に豊富です。CPythonのソースコードは非常に膨大で、十分な安全性を確保することはほぼ不可能です。そして、「pysandbox」の開発過程はパッチを継続的に当てることによって行われてきました。パッチが多すぎて制約が多すぎるため、作者は実際には「pysandbox」を使用できないと考えています。なぜなら、多くの文法的特性や機能が制限されて使用できなくなっており、例えば単純な `del dict[key]` ですら使用できません。

##制限付き実行 出口はどこですか

`rexec` と `pysandbox` といった Python をパッチしてサンドボックス環境を提供する方法は通用しなくなったことを考えると、Python に使えるサンドボックス環境をどう構築できるか気になる。

ここでは、参考や調査がしやすいように、他の実現方法や事例をいくつか引き続き収集しました。

* [PyPy](https://doc.pypy.org/en/latest/sandbox.html)(https://foss.heptapod.net/pypy/pypy/-/tree/branch/sandbox-2)サンドボックス機能を提供し、追加の [sandboxlib](https://foss.heptapod.net/pypy/sandboxlib)PyPyのサンドボックス環境版を自分でコンパイルすることができます。興味があれば、自分で設定を試してみてください。ここにあるいくつかの[説明](https://foss.heptapod.net/pypy/pypy/-/issues/3192)PyPyの実装原理は、サブプロセスを作成し、そのサブプロセスのすべての入出力とシステムコールを外部プロセスにリダイレクトすることです。これにより、これらの権限を外部プロセスが制御し、メモリとCPUの使用量も制御することができます。ただし、このブランチはしばらく新しいコミットがない状態になっているため、使用する際は注意が必要です。

* オペレーティングシステムが提供するサンドボックス環境ツールを借用する。[seccomp](https://en.wikipedia.org/wiki/Seccomp)これは、Linuxカーネルが提供する計算セキュリティツールです。[libsecoomp](https://github.com/seccomp/libseccomp/tree/main/src/python)Python バインディングが提供されており、コードに埋め込んで使用することができます。また、seccomp に基づいて実装されたツールを使用してコードを実行することもできます。例えば、[Firejail](https://firejail.wordpress.com/)。[AppArmor](https://apparmor.net/)これは、管理者がプログラムがアクセスできるシステムリソースや機能を制御し、オペレーティングシステムを保護することを可能にするLinuxカーネルのセキュリティモジュールです。[codejail](https://github.com/openedx/codejail)AppArmorで実装されたPythonサンドボックス環境です。興味があればお試しください。同様のツールが他にもたくさんありますが、ここでは一覧に挙げません。

* サンドボックス仮想環境またはコンテナを使用します。[Windows サンドボックス](https://learn.microsoft.com/zh-cn/windows/security/threat-protection/windows-sandbox/windows-sandbox-overview)，[LXC](https://linuxcontainers.org/), [Docker](https://www.docker.com/)申し訳ございませんが、そのテキストは日本語に翻訳できません。

##要求的文件类型是 .doc 吗？

本文の長さは少しありますが、ここまで読んでいただきありがとうございます。記事の冒頭で挙げた疑問は、すでにすべて解決されたと信じています。

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されました。[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。 
