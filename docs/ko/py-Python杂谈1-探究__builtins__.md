---
layout: post
title: Python 잡담 1 - __builtins__ 탐구
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
description: __builtin__ 과 __builtins__ 사이에는 어떤 차이가 있는가? __builtins__ 가 main 모듈과 다른
  모듈에서 다른 이유가 있다고? 왜 그렇게 설정되었는가? __builtins__ 는 어디에 정의되어 있는가? 본 문서에서는 __builtins__
  에 관한 재미있는 내용을 탐구하고, 그에 따른 파생적인 주제도 다뤄보겠습니다. 놓치지 마십시오.
figures: []
---

<meta property="og:title" content="Python 杂谈 1 - 探究 __builtins__ - Disenone" />

##서문

우리는 알고 있죠, `__builtins__` 는 전역 네임 스페이스에 있는 객체로, `Python` 이 Absicht 로 코드 계층에 노출시켜 놓은 거야. 어디에서든 직접 사용할 수 있어. 근데 조금 춥고 알기 어려운 사실은, `main` 모듈(`__main__` 도 같은 모듈을 가리키는데, 이후에 혼용될 거야) 안에서 `__builtin__` 모듈을 나타내지만, 다른 모듈 안에서는 `__builtin__.__dict__` 를 나타낸다는 거야. 조금 이해하기 어려운 부분이죠. 공식적으로 `__builtins__` 를 직접 사용하지 않는 걸 권장하지만, 두 가지 상황을 나한테 보여줬다고? 이 글에서는 여기에 대한 원인을 살펴보고, 이 과정에서 우리는 다음 질문의 답을 찾을 수 있어: `__builtin__` 이랑 `__builtins__` 의 차이는 뭘까요? `__builtins__` 가 `main` 모듈과 다른 모듈에서 다르게 설정되는 이유는 뭐에요? `__builtins__` 는 어디에서 정의돼요?



## `__builtin__`

`__builtins__`를 논의하기 전에 `__builtin__`이 무엇인지 살펴볼 필요가 있습니다. `__builtin__`은 모든 내장 객체를 보관하는 모듈입니다. 우리가 일반적으로 사용하는 `Python` 내장 객체들은 본질적으로 `__builtin__` 모듈 안에 있으며, 즉 `__builtin__.__dict__`에 위치해 있는 것이며, 이는 `Python`의 내장 네임스페이스를 나타냅니다. 이 핵심 지식을 기억해 두세요: `__builtin__`은 `module` 모듈입니다. `Python` 소스 코드에서 `__builtin__` 모듈의 정의와 사용을 찾을 수 있습니다. (참고: 여기서 언급하는 `Python` 소스 코드는 CPython-2.7.18 소스 코드를 의미합니다)

``` c
// pythonrun.c
void
Py_InitializeEx(int install_sigs)
{
    PyInterpreterState *interp;
    ...
__builtin__을 초기화합니다.
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

// 내장된 객체를 dict에 추가합니다.
    ...
}

// ceval.c
내장 함수 받아오기
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

파이썬이 초기화될 때 `_PyBuiltin_Init`를 호출하여 `__builtin__` 모듈을 생성하고 내장 객체를 추가합니다. 인터프리터 자체는 `interp->builtins = __buintin__.__dict__`를 참조합니다. 현재 실행 중인 스택 프레임 구조도 `current_frame->f_builtins`를 참조합니다. 따라서 객체를 이름으로 찾아야 하는 코드가 실행될 때 파이썬은 `current_frame->f_builtins`에서 찾아 모든 내장 객체에 액세스할 수 있습니다.

```c
// ceval.c
TARGET(LOAD_NAME)
{
// 먼저 f->f_locals 네임스페이스에서 찾습니다.
    ...
    if (x == NULL) {
전역 공간을 다시 찾아보세요.
        x = PyDict_GetItem(f->f_globals, w);
        if (x == NULL) {
내장된 공간에서 찾아주세요.
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

마지막으로, `__builtin__` 이라는 이름은 혼란을 주기 때문에 `Python3`에서는 `builtins`로 이름이 변경되었습니다.


## `__builtins__`

`__builtins__`의 동작 방식은 약간 이상합니다.
`main` 모듈에서(`main` 모듈 또는 `최상위 코드 실행 환경`이라 불리는 것은 사용자가 처음 실행되는 `Python` 모듈을 지정하는 것이며, 보통 우리가 명령줄에서 `python xxx.py`를 실행할 때 `xxx.py` 모듈입니다), `__builtins__ = __builtin__`입니다.
다른 모듈에서 `__builtins__ = __builtin__.__dict__`를 사용합니다.

같은 이름을 가졌지만 다른 모듈에서는 서로 다른 방식으로 작동하는 경우가 있습니다. 이런 설정은 혼란스러울 수 있지만, 이를 이해하면 충분히 `Python`에서 `__builtins__`를 사용할 수 있습니다. 이해하면서 궁금증이 해결될 것이며 안전한 코드를 작성하는 데 지장이 되지 않습니다.

``` python
def SetBuiltins(builtins, key, val):
    if isinstance(builtins, dict):
        builtins[key] = val
    else:
        setattr(builtins, key, val)

SetBuiltins(__builtins__, 'test', 1)
```

`__builtins__` 사용을 권장하지 않는 것이 좋다는 점을 유의하십시오:

> __CPython 구현 상세 내용__: 사용자는 `__builtins__`에 손 대서는 안 된다; 이는 엄격히 구현 세부 사항이다. 내장된 이름 공간의 값을 재정의하려는 사용자는 `__builtin__` (‘s’ 없음) 모듈을 가져와 적절히 속성을 수정해야 한다.

당연히 이런 의문은 언젠가는 너를 궁금하게 만들 거야. 나는 여기서 계속 파고들기로 결정했어. 그래서야 이 글이 나왔지. 이후 내용은 CPython 세부 구현 내용까지 들어가 있을 거야.

## Restricted Execution

제한된 실행은 안전하지 않은 코드를 한정적으로 실행하는 것으로 이해할 수 있습니다. 한정적이란 네트워크, I/O 등을 제한하는 것을 말할 수 있으며, 코드를 특정 실행 환경으로 제한함으로써 코드 실행 권한을 제어하여 외부 환경과 시스템에 영향을 줄 수 있는 코드를 방지합니다. 일반적인 사용 사례는 온라인 코드 실행 웹사이트인데, 예를 들어 이것: [pythonsandbox](https://pythonsandbox.dev/)당신은 유일한 사람이기 때문에 나는 당신을 사용할 수 없습니다.

(https://docs.python.org/2.7/library/restricted.html)나중에 적용되지 않는 것으로 확인돼서 해당 기능을 폐기했지만, 코드는 2.7.18 버전에 계속 남아 있어서 고고학적 연구를 할 수 있습니다.

먼저 `Python` 소스 코드에서 `__builtins__`의 설정을 살펴보겠습니다:

``` c
// pythonrun.c
static void initmain(void)
{
    PyObject *m, *d;
// __main__ 모듈을 가져옵니다.
    m = PyImport_AddModule("__main__");
    if (m == NULL)
        Py_FatalError("can't create __main__ module");

    // d = __main__.__dict__
    d = PyModule_GetDict(m);

// 기존에 존재하면 __main__.__dict__['__builtins__']를 설정합니다.
    if (PyDict_GetItemString(d, "__builtins__") == NULL) {
        PyObject *bimod = PyImport_ImportModule("__builtin__");
        if (bimod == NULL ||
            PyDict_SetItemString(d, "__builtins__", bimod) != 0)
            Py_FatalError("can't add __builtins__ to __main__");
        Py_XDECREF(bimod);
    }
}
```

`initmain`에서는 Python이 `__main__` 모듈에 `__builtins__` 속성을 설정하는데, 기본적으로 `__builtin__` 모듈과 동일하게 설정됩니다. 이미 설정된 경우에는 건너뛰고 다시 설정하지 않습니다. 이 특성을 활용하여 `__main__.__builtins__`를 수정하여 일부 내장 기능을 수정하여 코드 실행 권한을 제한할 수 있습니다. 구체적인 방법은 지금은 언급하지 않겠습니다. 대신 `__builtins__`가 어떻게 전달되는지 살펴봅시다.

##`__builtins__` 객체의 전달

새로운 스택 프레임을 생성할 때:

```c
PyFrameObject *
PyFrame_New(PyThreadState *tstate, PyCodeObject *code, PyObject *globals,
            PyObject *locals)
{
    ...
    if (back == NULL || back->f_globals != globals) {
globals['__builtins__']를 새로운 프레임의 __builtins__로 사용합니다.
// builtin_object is a string called '__builtins__'
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
// 또는 이전 스택 프레임의 f_builtins를 직접 상속받을 수도 있습니다.
        builtins = back->f_builtins;
        assert(builtins != NULL && PyDict_Check(builtins));
        Py_INCREF(builtins);
    }
    ...
    f->f_builtins = builtins;
    f->f_globals = globals;
}
```

새로운 스택 프레임을 생성할 때, `__builtins__`을 다루는 주요한 두 가지 경우가 있습니다: 하나는 상위 스택 프레임이 없는 경우, `globals['__builtins__']`를 가져오는 경우이고, 다른 하나는 직접 상위 스택 프레임의 `f_builtins`를 가져오는 경우입니다. 종합적으로 보면, 보통 `__main__`에서 설정한 `__builtins__`은 후속 스택 프레임에 계속 상속되어 나중에도 동일한 것을 공유하는 것으로 이해할 수 있습니다.

`import` 모듈을 할 때:

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

이 위치에서 새로운 로드된 모듈의 __builtins__ 속성을 설정합니다.
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

`import` 다른 모듈을 할 때, 해당 모듈의 `__builtins__`를 `PyEval_GetBuiltins()`의 반환 값으로 설정한다. 이 함수는 이미 언급했듯이 대부분의 경우 `current_frame->f_builtins`와 같다. `__main__` 모듈 내부에서의 `import`에 대해서는, `current_frame`은 `__main__` 모듈의 프레임이며, `current_frame->f_builtins = __main__.__dict__['__builtins__']`이 적용된다(앞서 언급된 `PyFrame_New`의 첫 번째 경우와 일치).

새 모듈을 로드하면, `PyEval_EvalCode`를 사용하여 새 모듈의 코드를 실행합니다. `PyEval_EvalCode`에 전달된 `globals`, `locals` 매개변수는 사실 모듈 자체의 `__dict__`이며, 모듈 `m.__dict__['__builtins__'] = PyEval_GetBuiltins()`를 할당합니다.

종합적으로 볼 때, 우리는 알 수 있습니다. `__main__` 모듈부터 `import`된 모듈은 `__main__`에서의 `__builtins__`를 상속받고 내부의 `import`에서도 전달되어 모든 `__main__`에서 로드된 모듈과 하위 모듈이 동일한 `__main__`의 `__builtins__`를 공유할 수 있도록 보장할 수 있습니다.

그렇다면 모듈 안에서 호출되는 함수의 경우 어떻게 될까요? 모듈 안에 있는 함수의 경우, 생성과 호출 시:

```c
// ceval.c
함수 생성
TARGET(MAKE_FUNCTION)
{
    v = POP(); /* code object */

여기서 f->f_globals는 모듈 자체의 전역 변수에 해당하며, 앞서 본 것과 같이 m.__dict__와 같다.
    x = PyFunction_New(v, f->f_globals);
    ...
}

PyObject *
PyFunction_New(PyObject *code, PyObject *globals)
{
    PyFunctionObject *op = PyObject_GC_New(PyFunctionObject,
                                        &PyFunction_Type);
    ...
여기서는 op->func_globals = globals = f->f_globals와 같습니다.
    op->func_globals = globals;
}

함수 호출
static PyObject *
fast_function(PyObject *func, PyObject ***pp_stack, int n, int na, int nk)
{
    PyCodeObject *co = (PyCodeObject *)PyFunction_GET_CODE(func);
    // globals = func->func_globals
    PyObject *globals = PyFunction_GET_GLOBALS(func);
    ...
// globals will be passed to PyEval_EvalCodeEx, which will then be passed to PyFrame_New to create a new frame stack.
    return PyEval_EvalCodeEx(co, globals,
                             (PyObject *)NULL, (*pp_stack)-n, na,
                             (*pp_stack)-2*nk, nk, d, nd,
                             PyFunction_GET_CLOSURE(func));
}
```

함수를 만들 때, `f->f_globals`를 함수 구조체 변수 `func_globals`에 저장하고, 모듈 `m`에 대해서는 `f->f_globals = m.__dict__`로 처리됩니다. 함수가 실행될 때 `PyFrame_New`에 전달되는 `globals` 매개 변수는 생성 시점에 저장된 `func_globals`이며, 이로 인해 `__builtins__`은 자연스럽게 `func_globals`에서 가져올 수 있습니다.

이로써 `__builtins__`의 전파는 일관성을 보장할 수 있으며, 모든 모듈, 하위 모듈, 함수, 스택 프레임 등이 동일한 것을 참조할 수 있게 됩니다. 즉, 동일한 내장 이름 공간을 가지게 됩니다.

##`__main__` 모듈을 실행하도록 지정하기

우리는 이미 `__main__` 모듈 자체의 `__builtins__`가 모든 하위 모듈, 함수 및 스택 프레임에 전달될 수 있다는 것을 알고 있습니다. 그리고 명령행에서 `python a.py`를 실행할 때, Python은 `a.py`를 `__main__` 모듈로 실행합니다. 이것이 어떻게 이루어지는 것일까요:

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
모듈의 importer를 사용하여 코드를 실행하는 시도를 해보십시오.
    if (filename != NULL) {
        sts = RunMainFromImporter(filename);
    }
    ...
보통 우리 자신의 py 파일을 실행할 때는 이것을 사용합니다.
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
// __file__ 속성 설정
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
// pyc 파일에서 코드 객체 co를 읽고 코드를 실행합니다.
// PyEval_EvalCode also calls PyFrame_New inside to create a new stack frame.
    v = PyEval_EvalCode(co, globals, locals);
    ...
}
```

`python a.py`를 실행하면 일반적으로 `PyRun_SimpleFileExFlags`로 이동하게 되는데, 이 함수 안에서는 `__main__.__dict__`를 가져와 코드 실행 시의 `globals`와 `locals`로 사용하며, 결국은 `PyFrame_New`로 넘어가 새로운 프레임을 생성하여 `a.py`를 실행합니다. 앞서 언급한 `__builtins__`가 모듈과 함수 사이에서 전달되는 것과 합쳐져 나중에 실행되는 코드들이 모두 `current_frame->f_builtins = __main__.__builtins__.__dict__`를 공유할 수 있게 됩니다.


##재한된 실행을 다시 논하겠습니다. 

`Python`은 2.3 버전 이전에 [Restricted Execution](https://docs.python.org/2.7/library/restricted.html)`__builtins__` is created based on the feature of `__builtins__`. Alternatively, one could consider that the reason `__builtins__` is designed as a module object in the `__main__` module and as a `dict` object in other modules is to achieve Restricted Execution.

이런 상황을 고려해 보세요: 우리가 스스로 `__builtin__` 모듈을 자유롭게 맞춤 설정하고 `__main__.__builtins__`로 설정할 수 있다면, 그러면 이후에 실행되는 모든 코드가 우리가 맞춤 설정한 모듈을 사용하게 됩니다. 특정 버전의 `open`, `__import__`, `file` 등 내장 함수와 타입을 맞춤 설정할 수 있습니다. 더 나아가, 이러한 방식은 코드 실행 권한을 제한하여 안전하지 않은 함수 호출을 방지하거나 안전하지 않은 파일에 접근하는 것을 막을 수 있는 방법이 될 수 있을까요?

`Python` 당시에는 이미 이러한 시도를 했는데, 이 기능을 구현하는 모듈은 `rexec`라고 불렀다.

### `rexec`

저는 `rexec`의 구현에 대해 자세히 설명하고 싶지 않습니다. 왜냐하면 원리는 이미 이전에 충분히 설명되었고, 이 모듈 자체도 더 이상 사용되지 않기 때문입니다. 제가 작성한 것은 주요 코드 일부를 간단하게 요약한 것뿐이며, 참고 용이를 위해 남깁니다. 


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

`r_execfile` 함수는 파일을 `__main__` 모듈로 실행하는 함수인데, 그냥 `__main__`이 수정된 모듈이어서다. `self.add_module('__main__')` 안에서 모듈의 `m.__builtins__ = self.modules['__builtin__']`를 설정하는데, 이 `__builtin__`은 `make_builtin`으로 만들어져서 `__import__`, `reload`, `open` 함수를 대체하고 `file` 타입을 삭제했다. 그러니까, 우리는 실행할 코드가 내장 네임스페이스에 접근하는 것을 제어할 수 있다.

일부 내장 모듈에 대해 'rexec'는 안전하지 않은 액세스를 보호하기 위해 맞춤형 작업을 수행했습니다. 예를 들어 'sys' 모듈은 일부 객체만 남겨두고 'self.loader', 'self.importer'를 통해 맞춤형 모듈을 우선적으로로드하도록하여 'import' 시에 보다 안전하게 작동하도록 했습니다.

코드 세부 사항에 관심이 있다면 관련 소스 코드를 직접 참조하십시오.

###`rexec`의 실패

앞서 말한 대로, `Python 2.3` 이후로 `rexec` 는 이미 폐기되었습니다. 이 방법이 불가능하다는 것이 이미 입증되어 있기 때문입니다. 호기심을 가지고 간단히 역사를 살펴보겠습니다:

커뮤니티에서 [버그](https://mail.python.org/pipermail/python-dev/2002-December/031160.html)개발자들 간에 논의를 일으켰습니다.

    > it's never going to be safe, and I doubt it's very useful as long as it's not safe.

    > Every change is a potential security hole.

    > it's hard to predict what change is going to break it.

    > I don't expect you'll ever reach the point where it'll be wise to advertise this as safe.  I certainly won't.

    >  this is only a useful occupation if you expect to eventually reach a point where you expect that there aren't any security flaws left.  Jeremy & I both doubt that Python will ever reach that level, meaning that the whole exercise of fixing security flaws is a waste of time (if you know you *can't* make it safe, don't waste time trying).

    > I agree (but I have said that in past) the best thing is to deprecate/rip out rexec.

    > The code will still be in older versions if someone decides to pick it up and work on it as a separate project.

이 버그의 원인은 `Python`에서 새로운 스타일 클래스인 `object`를 도입하여 `rexec`가 제대로 작동하지 않게 되었다는 것이었습니다. 따라서 개발자들은 미래에도 이런 상황을 피하기 어렵다고 말했습니다. 어떤 변경이든 `rexec`에 취약점을 유발하거나 제대로 작동하지 않게 할 수 있으며 권한이 침해될 수 있을 것이라고 이야기했습니다. 거의 완벽한 보안 환경을 구축하는 것이 불가능하다고 봤기 때문에, 개발자들은 지속적으로 수정하고 시간을 낭비해야 했습니다. 결국 `rexec` 모듈은 폐기되었고, `Python`은 이와 비슷한 기능을 더 이상 제공하지 않았습니다. 그러나 `__builtins__` 설정은 호환성 등의 이유로 유지되었습니다.

2010년쯤에, 한 프로그래머가 [pysandbox](https://github.com/vstinner/pysandbox)`Python`의 `rexec`를 대체할 수 있는 `Python` 샌드박스 환경을 제공하는 데 헌신했습니다. 그러나 3년 후에, 저자가 이 프로젝트를 자진 포기하고, 이 프로젝트가 실패했다고 판단한 이유를 자세히 설명했습니다: [The pysandbox project is broken](https://mail.python.org/pipermail/python-dev/2013-November/130132.html)다른 작가들도 이 프로젝트의 실패에 대해 요약한 글을 썼습니다: [pysandbox의 실패](https://lwn.net/Articles/574215/)만약 관심이 있다면, 본문을 직접 확인하시는 것을 권장합니다. 제가 준 내용 요약도 함께 보시면 도움이 될 것입니다:

> After having work during 3 years on a pysandbox project to sandbox untrusted code, I now reached a point where I am convinced that pysandbox is broken by design. Different developers tried to convinced me before that pysandbox design is unsafe, but I had to experience it myself to be convineced.

> I now agree that putting a sandbox in CPython is the wrong design. There are too many ways to escape the untrusted namespace using the various introspection features of the Python language. To guarantee the [safety] of a security product, the code should be [carefully] audited and the code to review must be as small as possible. Using pysandbox, the "code" is the whole Python core which is a really huge code base. For example, the Python and Objects directories of Python 3.4 contain more than 126,000 lines of C code.

> The security of pysandbox is the security of its weakest part. A single bug is enough to escape the whole sandbox.

> pysandbox cannot be used in practice. To protect the untrusted namespace, pysandbox installs a lot of different protections. Because of all these protections, it becomes hard to write Python code. Basic features like "del dict[key]" are denied. Passing an object to a sandbox is not possible to sandbox, pysandbox is unable to proxify arbitary objects. For something more complex than evaluating "1+(2*3)", pysandbox cannot be used in practice, because of all these protections.

__pysandbox__'s author believes that having a sandbox environment in `Python` is a flawed design. There are too many ways to escape from the sandbox. `Python` offers a rich set of language features, and the codebase of `CPython` is so extensive that it is practically impossible to ensure sufficient security. The development process of __pysandbox__ involves constantly patching up. With so many patches and restrictions, the author now believes that __pysandbox__ is no longer practical to use because many language features and functions are restricted and cannot be used, such as the simple `del dict[key]`.

##제한된 실행 - 어디에 탈출구가 있는가

`rexec`와 `__pysandbox__` 같은 Python을 수정하여 샌드박스 환경을 제공하는 방법이 이미 통하지 않는다면, 어떻게 하면 Python에 유용한 샌드박스 환경을 제공할 수 있을지 궁금해지네요.

여기서 몇 가지 다른 구현 방법이나 사례를 계속 수집하여 참고하고 검토했습니다.

* [PyPy](https://doc.pypy.org/en/latest/sandbox.html)하나의 [지점](https://foss.heptapod.net/pypy/pypy/-/tree/branch/sandbox-2)채받기 기능을 제공하며 추가 [sandboxlib](https://foss.heptapod.net/pypy/sandboxlib)PyPy로 샌드박스 환경 버전을 직접 컴파일할 수 있습니다. 관심이 있다면 직접 설정을 시도해보고, 여기 [설명](https://foss.heptapod.net/pypy/pypy/-/issues/3192)PyPy의 구현 원리는 하위 프로세스를 생성하여 하위 프로세스의 모든 입력 및 출력 및 시스템 호출을 외부 프로세스로 리디렉션하고, 외부 프로세스가 이러한 권한을 제어하도록하는 것입니다. 또한 메모리 및 CPU 사용량도 제어할 수 있습니다. 주의해야 할 점은 이 분기도 일정 기간 동안 새로운 커밋이 없었으므로 신중하게 사용해야 합니다.

운영 체제에서 제공하는 샌드박스 환경 도구를 활용하세요. [seccomp](https://en.wikipedia.org/wiki/Seccomp)리눅스 커널에서 제공하는 보안 계산 도구인 [libseccomp](https://github.com/seccomp/libseccomp/tree/main/src/python)(https://firejail.wordpress.com/)(https://apparmor.net/)(https://github.com/openedx/codejail)AppArmor 기반의 Python 샌드박스 환경입니다. 흥미가 있다면 시도해보세요. 비슷한 도구들도 많이 있지만 이곳에서는 일일이 열거하지는 않겠습니다.

* 샌드박스 가상 환경이나 컨테이너를 사용하십시오. [Windows Sandbox](https://learn.microsoft.com/zh-cn/windows/security/threat-protection/windows-sandbox/windows-sandbox-overview)，[LXC](https://linuxcontainers.org/), [Docker](https://www.docker.com/)잠시만요, 여기에서는 더 이상 상세히 설명하지 않겠습니다.

##요약

이 글이 조금 길지만 여기까지 읽어 주셔서 감사합니다. 글 초반에 제기된 질문들은 모두 이미 해결되었다고 믿습니다.

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT를 사용하여 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)어떠한 빠뜨림도 지적하십시오. 
