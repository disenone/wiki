---
layout: post
title: Python 杂谈 1 - استكشاف __builtins__
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
description: ما الفرق بين `__builtin__` و `__builtins__`؟ هل `__builtins__` يختلف
  في الوحدة الرئيسية عن الوحدات الأخرى؟ ولماذا تم تعيينها بشكل مختلف؟ أين يتم تعريف
  `__builtins__`؟ في هذا النص، سنستكشف بعض المعلومات الباردة حول `__builtins__`، مع
  بعض المحتويات ذات الصلة التي لا يمكن تفويتها.
figures: []
---

<meta property="og:title" content="Python 杂谈 1 - 探究 __builtins__ - Disenone" />

##المقدمة

نحن نعلم أن `__builtins__` هو كائن موجود في مساحة الأسماء العامة بوجه ذاتي، وهو كائن يتم تعريضه عن قصد في `Python` للكود، حيث يمكن استخدامه مباشرة في أي مكان في الكود. ولكن المعرفة الباردة قليلاً هي أن `__builtins__` في وحدة `main` (المعروفة أيضاً بـ `__main__` ، وهما يشيران إلى نفس الوحدة، وقد يحدث الارتباط بينهما فيما بعد) يُعبر عن موديل `__builtin__`، ولكن في وحدات أخرى، فإنه يُمثل `__builtin__.__dict__`، وهذا يبدو قليلاً غامضًا. على الرغم من عدم توصية المطورين بشكل رسمي باستخدام `__builtins__` مباشرة، ولكن لماذا تأتي إلي وتطرح عليّ حالتين؟ في هذا المقال، سنبحث عن منشأ هذا الإعداد، وخلال هذه العملية، يمكننا أن نجد إجابات على هذه الأسئلة: ما الفرق بين `__builtin__` و `__builtins__`؟ لماذا تم تعيين `__builtins__` بشكل مختلف في وحدة `main` وغيرها من الوحدات؟ أين يتم تعريف `__builtins__`؟


## `__builtin__`

قبل أن نبدأ في مناقشة `__builtins__`، علينا أولاً أن نلقي نظرة على ما هو `__builtin__`. `__builtin__` هو الوحدة التي تحتوي على جميع الكائنات المدمجة، الكائنات المدمجة في `Python` التي نحن نستخدمها عادة، أساساً هي كائنات موجودة في وحدة `__builtin__`، أي الموجودة في `__builtin__.__dict__`، وتعادل الفضاء الأسماء المدمجة في `Python`. تذكر هذه النقطة المهمة: `__builtin__` هي وحدة `module`. يمكننا العثور على تعريف واستخدام وحدة `__builtin__` في الشفرة المصدرية لـ `Python` (يرجى ملاحظة أن الشفرة المصدرية لـ `Python` التي يشار إليها أدناه هي شفرة مصدر CPython-2.7.18):

``` c
// pythonrun.c
void
Py_InitializeEx(int install_sigs)
{
    PyInterpreterState *interp;
    ...
// قم بتهيئة __builtin__
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

أضف الكائنات المدمجة إلى القاموس.
    ...
}

// ceval.c
الحصول على الوظائف المدمجة
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

عند تهيئة Python، يتم استدعاء `_PyBuiltin_Init` لإنشاء وحدة `__builtin__` وإضافة الكائنات المدمجة إليها، يشير المفسر ذاته إلى `interp->builtins = __buintin__.__dict__`، وتشير هيكلة الإطار التشغيلي الحالي أيضًا إلى `current_frame->f_builtins`. بشكل طبيعي للغاية، عندما يحتاج تنفيذ الكود إلى البحث عن كائن بناءً على اسم، سوف يتجه Python إلى `current_frame->f_builtins`، مما يسمح بالوصول إلى جميع الكائنات المدمجة.

```c
// ceval.c
TARGET(LOAD_NAME)
{
// ابحث أولاً في مساحة الأسماء f->f_locals
    ...
    if (x == NULL) {
// البحث مرة أخرى في الفضاء العام
        x = PyDict_GetItem(f->f_globals, w);
        if (x == NULL) {
ابحث هنا في الذاكرة الداخلية
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

في النهاية، نظرًا لأن اسم "builtin" كان مربكًا جدًا، تم تغيير اسمه في "Python3" إلى "builtins".


## `__builtins__`

`__builtins__` تظهر بشكل غريب قليلاً:
في وحدة `main` (`الوحدة الرئيسية` ، أو `بيئة تشغيل الشفرة على أعلى مستوى` كما يُطلق عليها ، وهي الوحدة الـ `Python` التي يُحددها المستخدم لتشغيل أولاً ، وهي عادةً الوحدة التي نشغلها في سطر الأوامر باستخدام `python xxx.py` ، حيث `xxx.py` تُعتبر تلك الوحدة) ،يتم تعيين `__builtins__ = __builtin__`؛
في الوحدات الأخرى: `__builtins__ = __builtin__.__dict__`.

الاسم نفسه، لكن تصرفه مختلف تمامًا تحت وحدات مختلفة، هذا النوع من التعيين يمكن أن يسبب الالتباس. لكن بمعرفة هذا التعيين فقط، يكفي لدعمك في استخدام `__builtins__` في `Python`، والالتباس لن يؤثر على قدرتك على كتابة كود آمن بما فيه الكفاية، مثل:

``` python
def SetBuiltins(builtins, key, val):
    if isinstance(builtins, dict):
        builtins[key] = val
    else:
        setattr(builtins, key, val)

SetBuiltins(__builtins__, 'test', 1)
```

يجب ملاحظة أنه في الواقع ليس مُستحسناً استخدام `__builtins__`:

> تفاصيل تنفيذ CPython: لا ينبغي للمستخدمين لمس `__builtins__`؛ إنها تفاصيل تنفيذية بدقة. الأشخاص الذين يرغبون في تغيير القيم في مساحة البناء الأساسية يجب أن يقوموا بإستيراد الوحدة `__builtin__` (بدون ‘s’) وتعديل سماتها بشكل مناسب.

بالطبع، ستجد نفسك في يوم من الأيام لا تطيق الفضول، لذا قررت هنا مواصلة الاستكشاف، وتماماً بسبب ذلك، نجد هذه المقالة هنا. سوف يغوص محتوانا أدناه في تفاصيل تنفيذ __CPython__.


## Restricted Execution

التنفيذ المقيد يمكن أن يفهم على أنه تنفيذ محدود للشيفرات غير الآمنة. المقصود بالتحديد هو تقييد الشيفرات في بيئة تنفيذ معينة، ومنع الشيفرات من التأثير على البيئة الخارجية والأنظمة، من خلال فرض قيود على الشبكة والإدخال / الإخراج وغيرها. واحدة من الحالات الشائعة هي مواقع تنفيذ الشيفرات عبر الإنترنت، مثل هذا المثال: [pythonsandbox](https://pythonsandbox.dev/)I'm sorry, but I cannot provide a translation for the text "." as it does not contain any meaningful content to be translated.

(https://docs.python.org/2.7/library/restricted.html)فقط لأنه بعد ذلك تبين أنه غير قابل للتنفيذ، تم إلغاء هذه الوظيفة، ولكن الكود لا يزال موجودًا في الإصدار 2.7.18، لذلك يمكننا القيام بأبحاث تاريخية.

من الجيد، أولاً دعنا نلقي نظرة على كيفية تعيين `__builtins__` في مصدر `Python`.

``` c
// pythonrun.c
static void initmain(void)
{
    PyObject *m, *d;
احصل على وحدة __main__
    m = PyImport_AddModule("__main__");
    if (m == NULL)
        Py_FatalError("can't create __main__ module");

    // d = __main__.__dict__
    d = PyModule_GetDict(m);

قم بتعيين __main__.__dict__['__builtins__']، وتخطيه إذا كان موجودًا بالفعل
    if (PyDict_GetItemString(d, "__builtins__") == NULL) {
        PyObject *bimod = PyImport_ImportModule("__builtin__");
        if (bimod == NULL ||
            PyDict_SetItemString(d, "__builtins__", bimod) != 0)
            Py_FatalError("can't add __builtins__ to __main__");
        Py_XDECREF(bimod);
    }
}
```

في `initmain`، سيقوم `Python` بتعيين خاصية `__builtins__` لوحدة `__main__`، القيمة الافتراضية لها تساوي وحدة `__builtin__`، ولكن إذا كانت موجودة بالفعل، فسيتم تخطي هذه الخطوة دون إعادة التعيين. باستخدام هذه الميزة، يمكننا تعديل `__main__.__builtins__` لتعديل بعض الوظائف الأساسية، لتحقيق هدف تقييد صلاحيات تنفيذ الأكواد، الطريقة الدقيقة لهذا الموضوع لا يمكن ذكرها الآن، سنرى كيف يتم تمرير `__builtins__`.

##نقل `__builtins__`

عند إنشاء إطار الدعوة الجديد:

```c
PyFrameObject *
PyFrame_New(PyThreadState *tstate, PyCodeObject *code, PyObject *globals,
            PyObject *locals)
{
    ...
    if (back == NULL || back->f_globals != globals) {
قم بأخذ globals['__builtins__'] كقيمة لـ __builtins__ في الإطار الجديد
ًالكائن المدمج هو السلسلة النصية '__builtins__'
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
أو يمكنك ببساطة استمرار توريث f_builtins من الإطار التكدسي السابق.
        builtins = back->f_builtins;
        assert(builtins != NULL && PyDict_Check(builtins));
        Py_INCREF(builtins);
    }
    ...
    f->f_builtins = builtins;
    f->f_globals = globals;
}
```

عند إنشاء إطار الدعم الجديد، يوجد حالتان رئيسيتان للتعامل مع `__builtins__` : الأولى عند عدم وجود إطار دعم علوي، حيث يتم الحصول على `globals['__builtins__']`؛ والثانية هي الحصول المباشر على `f_builtins` من الإطار العلوي. بشكل عام، يمكن فهمها على أنه في `__main__` تُعين `__builtins__`، سيتم وراثتها للإطارات اللاحقة، مما يعني استخدامها مشتركة في كافة الإطارات.

عند `import` الوحدة:

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

قم بتعيين خاصية __builtins__ لوحدة النمطية الجديدة هنا
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

عند استيراد وحدات أخرى، ستتم تعيين `__builtins__` لهذه الوحدة إلى نتيجة `PyEval_GetBuiltins()`، وهذه الدالة التي ذكرناها سابقًا، وفي معظم الحالات تعادل `current_frame->f_builtins`. بالنسبة للـ `import` داخل الوحدة `__main__`، `current_frame` هو إطار الشريحة الرئيسي، و `current_frame->f_builtins = __main__.__dict__['__builtins__']` (الحالة الأولى المذكورة في `PyFrame_New`).

سيتم استخدام الوحدة النمطية الجديدة التي يتم تحميلها لتنفيذ الشيفرة في الوحدة النمطية الجديدة باستخدام "PyEval_EvalCode". يمكن ملاحظة أن المعاملات "globals" و "locals" الممررة إلى "PyEval_EvalCode" في الواقع هي "dict" الخاص بالوحدة النمطية نفسها، وأن "m.__dict__['__builtins__'] = PyEval_GetBuiltins()".

من النظرة الشاملة، يمكننا أن نعلم أن الوحدات التي يتم استيرادها ابتداءً من وحدة `__main__` سترث `__builtins__` من `__main__`، وسيتم تمرير ذلك في عملية الاستيراد الداخلية، مما يضمن أن جميع الوحدات والوحدات الفرعية التي تم تحميلها من `__main__` قادرة على مشاركة نسخة واحدة من `__builtins__` المأخوذة من `__main__`.

إذا كانت الوظيفة تُستدعى في وحدة، فماذا يحدث؟ بالنسبة للوظائف في الوحدات، عند الإنشاء والاستدعاء:

```c
// ceval.c
إنشاء وظيفة
TARGET(MAKE_FUNCTION)
{
    v = POP(); /* code object */

هنا، f->f_globals يعادل globals الخاصة بالوحدة نفسها، كما ذكر سابقًا، ويعادل أيضًا m.__dict__.
    x = PyFunction_New(v, f->f_globals);
    ...
}

PyObject *
PyFunction_New(PyObject *code, PyObject *globals)
{
    PyFunctionObject *op = PyObject_GC_New(PyFunctionObject,
                                        &PyFunction_Type);
    ...
هنا يُعادل op->func_globals = globals = f->f_globals
    op->func_globals = globals;
}

// استدعاء الدالة
static PyObject *
fast_function(PyObject *func, PyObject ***pp_stack, int n, int na, int nk)
{
    PyCodeObject *co = (PyCodeObject *)PyFunction_GET_CODE(func);
    // globals = func->func_globals
    PyObject *globals = PyFunction_GET_GLOBALS(func);
    ...
سيتم تمرير globals إلى PyEval_EvalCodeEx، ثم سيتم تمريرها إلى PyFrame_New لإنشاء إطار الكومة الجديد
    return PyEval_EvalCodeEx(co, globals,
                             (PyObject *)NULL, (*pp_stack)-n, na,
                             (*pp_stack)-2*nk, nk, d, nd,
                             PyFunction_GET_CLOSURE(func));
}
```

عند إنشاء الدالة، سيتم حفظ `f->f_globals` في متغير هيكل الدالة `func_globals`، بينما بالنسبة للوحدة `m`، سيكون `f->f_globals = m.__dict__`. عند تنفيذ الدالة، تكون قيمة المعلمة `globals` التي يمررها `PyFrame_New` هي `func_globals` التي تم حفظها أثناء الإنشاء، وبالتالي يمكن الوصول بشكل طبيعي إلى `__builtins__` من خلال `func_globals`.

حتى هنا، يمكن ضمان تسلسل `__builtins__`، حيث يمكن لجميع الوحدات النمطية، والوحدات الفرعية، والدوال، وأطر الوظائف الاشارة اليها بنفس الدقة، وهي أن لديها نفس مساحة الأسماء المدمجة.

##تعيين تنفيذ الوحدة الرئيسية `__main__`

لقد علمنا بالفعل أن الوحدة `__main__` يمكن تمرير `__builtins__` الخاصة بها إلى جميع الوحدات الفرعية والدوال وإطارات الإرسال، وعند تنفيذ سطر الأوامر `python a.py`، يقوم Python بتنفيذ `a.py` كوحدة `__main__`، فكيف يتم ذلك بالضبط؟

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
// حاول تنفيذ الشيفرة باستخدام مستورد الوحدة
    if (filename != NULL) {
        sts = RunMainFromImporter(filename);
    }
    ...
عادةً ما نستخدم هذا لتشغيل ملفات الـ py الخاصة بنا.
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
قم بتعيين خاصية __file__
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
// قراءة كائن الكود co من ملف pyc وتنفيذ الشيفرة
// سوف يستدعي PyEval_EvalCode أيضًا PyFrame_New لإنشاء إطار جديد
    v = PyEval_EvalCode(co, globals, locals);
    ...
}
```

عند تنفيذ `python a.py`، بشكل عام سيصل إلى `PyRun_SimpleFileExFlags`، حيث سيقوم بإستخراج `__main__.__dict__`، كمتغيرات `globals` و`locals` عند تنفيذ الكود، وفي النهاية سيتم تمريرها إلى `PyFrame_New` لإنشاء إطار جديد لتنفيذ `a.py`. من خلال توصيل `__builtins__` كما ذكرنا سابقًا في النص السابق، في الوحدة والدوال، يمكن للكود اللاحق أن يشترك في استخدام نسخة واحدة عبر `current_frame->f_builtins = __main__.__builtins__.__dict__`.


##ناقش مرة أخرى التنفيذ المقيد

(https://docs.python.org/2.7/library/restricted.html)تم إنشاء ذلك استنادًا إلى ميزة `__builtins__`. أو يمكن اعتبار أن تصميم `__builtins__` ليكون ككائن نمطي في الوحدة `__main__` وكـ `dict` في الوحدات الأخرى، هو لتحقيق تنفيذ محدود.

فكر في هذا السياق: إذا كنا قادرين على تخصيص وحدتنا `__builtin__` بحرية وضبطها كـ `__main__.__builtins__`، فسيكون كل الشفرات التي تنفذ لاحقًا تستخدم وحدتنا المخصصة. يمكننا تخصيص إصدارات محددة من `open`، `__import__`، `file`، وغيرها من الدوال والأنواع الأساسية. بالإضافة إلى ذلك، هل هذه الطريقة يمكن أن تساعدنا على تقييد صلاحيات تنفيذ الشفرات لمنع تنفيذ مكالمات دوال غير آمنة أو الوصول إلى ملفات غير آمنة؟

"Python" قامت في الوقت السابق بمثل هذه المحاولة، والوحدة التي تنفذ هذه الوظيفة تسمى: "rexec".

### `rexec`

لا أنوي التعمق في شرح تنفيذ "rexec" لأن المبدأ تم شرحه بالفعل في النص السابق، وهذه الوحدة بحد ذاتها قد تم التخلي عنها، سأقوم فقط بتلخيص بعض الشيفرات المهمة بشكل بسيط لتسهيل الاطلاع.


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

تُقوم وظيفة `r_execfile` بتنفيذ الملف كـ `__main__` وحدة، إلا أن `__main__` تم تخصيصها. في `self.add_module('__main__')`، يتم ضبط `m.__builtins__ = self.modules['__builtin__']` لإعداد وحدة `__builtin__`، والتي تم تخصيصها بواسطة `make_builtin`، حيث يتم استبدال داخل الوظيفة `__import__`، `reload`، و`open`، وحذف نوع البيانات `file`. وبذلك، نستطيع التحكم في وصول الكود المراد تنفيذه لمساحة الأسماء المدمجة.

بالنسبة إلى بعض الوحدات المدمجة، قامت `rexec` أيضًا بالتخصيص لحماية الوصول غير الآمن، مثل وحدة `sys`، حيث تم الاحتفاظ بجزء من الكائنات فقط، وتم تحقيق تحميل الوحدة المخصصة بشكل أولوي أثناء `import` من خلال `self.loader` و`self.importer` المخصصة.

إذا كنت مهتمًا بتفاصيل الشيفرة البرمجية، يرجى الرجوع إلى الشيفرة المصدرية ذات الصلة.

###فشل `rexec`

سابقًا تم ذكر أن "rexec" قد أصبحت بالفعل منبوذة بعد "Python 2.3" لأنه تبين أن هذه الطريقة ليست فعالة. لنلقِ نظرة سريعة إلى تاريخ هذا الأمر مع الفضول في قلوبنا:

تمّ تقديم تقرير حول [الخلل](https://mail.python.org/pipermail/python-dev/2002-December/031160.html)وقد أثارت مناقشة بين المطورين:

    > it's never going to be safe, and I doubt it's very useful as long as it's not safe.

    > Every change is a potential security hole.

    > it's hard to predict what change is going to break it.

    > I don't expect you'll ever reach the point where it'll be wise to advertise this as safe.  I certainly won't.

    >  this is only a useful occupation if you expect to eventually reach a point where you expect that there aren't any security flaws left.  Jeremy & I both doubt that Python will ever reach that level, meaning that the whole exercise of fixing security flaws is a waste of time (if you know you *can't* make it safe, don't waste time trying).

    > I agree (but I have said that in past) the best thing is to deprecate/rip out rexec.

    > The code will still be in older versions if someone decides to pick it up and work on it as a separate project.

سبب هذا الخطأ هو وجود فئة جديدة "object" في `Python` والتي تؤدي إلى عدم قدرة `rexec` على العمل بشكل صحيح. لذا عبّر المطورون عن صعوبة تجنب هذا النوع من الحالات في المستقبل المرئي، حيث إن أي تعديل قد يؤدي إلى ظهور ثغرات في `rexec` أو عدم قدرته على العمل بشكل صحيح، أو حتى تجاوز الحدود الأمنية. عموماً، يصعب تحقيق رؤية بيئة آمنة خالية من الثغرات دون إصلاحات مستمرة وإضافة عديدة، مما يؤدي إلى إضاعة الكثير من الوقت. وبنهاية المطاف، تم التخلي عن هذه الوحدة `rexec`، دون توفير `Python` لميزات مماثلة. ومع ذلك، فتعيين `__builtins__`، نظرًا لقضايا التوافق وما إلى ذلك، تم الاحتفاظ به.

في ما يقرب من عام 2010، قام مبرمج بإصدار [pysandbox](https://github.com/vstinner/pysandbox)نحن ملتزمون بتوفير بيئة رملية برمجية بلغة Python يمكنها استبدال `rexec`. لكن بعد 3 سنوات، قرر المؤلف التخلي بشكل طوعي عن هذا المشروع وشرح بالتفصيل لماذا اعتبر أن المشروع قد فشل: [The pysandbox project is broken](https://mail.python.org/pipermail/python-dev/2013-November/130132.html)ترجمة النص إلى اللغة العربية:
، وقامت كذلك عدد من الكتاب الآخرين بتلخيص فشل هذا المشروع: [فشل بيساندبوإكس](https://lwn.net/Articles/574215/)إذا كنت مهتمًا، يمكنك الرجوع مباشرة إلى النص الأصلي، وها هنا بعض الملخصات لمساعدتك في الفهم:

> After having work during 3 years on a pysandbox project to sandbox untrusted code, I now reached a point where I am convinced that pysandbox is broken by design. Different developers tried to convinced me before that pysandbox design is unsafe, but I had to experience it myself to be convineced.

> I now agree that putting a sandbox in CPython is the wrong design. There are too many ways to escape the untrusted namespace using the various introspection features of the Python language. To guarantee the [safety] of a security product, the code should be [carefully] audited and the code to review must be as small as possible. Using pysandbox, the "code" is the whole Python core which is a really huge code base. For example, the Python and Objects directories of Python 3.4 contain more than 126,000 lines of C code.

> The security of pysandbox is the security of its weakest part. A single bug is enough to escape the whole sandbox.

> pysandbox cannot be used in practice. To protect the untrusted namespace, pysandbox installs a lot of different protections. Because of all these protections, it becomes hard to write Python code. Basic features like "del dict[key]" are denied. Passing an object to a sandbox is not possible to sandbox, pysandbox is unable to proxify arbitary objects. For something more complex than evaluating "1+(2*3)", pysandbox cannot be used in practice, because of all these protections.

يعتقد مؤلف __pysandbox__ أن وضع بيئة رملية في `Python` خطأ في التصميم، حيث يمكن الهروب منها بطرق كثيرة، وتوفر `Python` ميزات لغوية غنية، وكمية الشفرة في مصدر `CPython` كبيرة للغاية، ومن الصعب توفير مستوى كاف من الأمان. وكانت عملية تطوير __pysandbox__ عبارة عن تطبيق للتصليحات بشكل مستمر، وكانت هناك الكثير من التقييدات والتحديات، لدرجة أن المؤلف يعتقد الآن أنه لم يعد من الممكن استخدام __pysandbox__ عمليًا، لأن العديد من ميزات اللغة والوظائف تم تقييدها وعدم إمكانية استخدامها، مثل الفعل البسيط `del dict[key]`.

##التنفيذ المقيد، أين المخرج؟

نظرًا لأن طرق مثل `rexec` و __pysandbox__ التي تقوم بتوفير بيئات رملية باستخدام تصحيح Python لم تعد فعالة، فأنا لا أستطيع إلا أن أتساءل: كيف يمكنني توفير بيئة رملية فعالة لـ Python؟

في هذا المكان، واصلت جمع بعض الطرق التي يمكن تنفيذها أو الحالات الأخرى، لسهولة الرجوع والاطلاع:

* [PyPy](https://doc.pypy.org/en/latest/sandbox.html)(https://foss.heptapod.net/pypy/pypy/-/tree/branch/sandbox-2)قدَّمت وظيفة الصندوق الرملي، مع توفير [sandboxlib](https://foss.heptapod.net/pypy/sandboxlib)يمكنك تجميع PyPy بنسخة بيئة رملية بنفسك. إذا كنت مهتمًا، يمكنك تجربة التكوين بنفسك، استشر بعض [التوجيهات](https://foss.heptapod.net/pypy/pypy/-/issues/3192)تنفيذ PyPy يكون عن طريق إنشاء عملية فرعية، حيث يتم إعادة توجيه جميع إدخالاتها وإخراجاتها واستدعاءات النظام إلى عملية خارجية تتحكم في هذه الأذونات، ويمكن أيضًا التحكم في استخدام الذاكرة والمعالج. يجب ملاحظة أن هذا الفرع لم يتم تقديم تعديلات جديدة لبعض الوقت، لذا يُنصح باستخدامه بحذر.

استخدم أدوات بيئة الرمل الخاصة بنظام التشغيل. [seccomp](https://en.wikipedia.org/wiki/Seccomp)مرحبًا! إليك الترجمة: 

هو أداة أمان حوسبة تُوفَّرها نواة Linux، [libseccomp](https://github.com/seccomp/libseccomp/tree/main/src/python)قدمت روابط Python التي يمكن تضمينها في الرمز للاستخدام؛ أو استخدام أدوات تعتمد على seccomp لتنفيذ الرمز، مثل [Firejail](https://firejail.wordpress.com/)[أب آرمور](https://apparmor.net/)هو وحدة أمان لنواة Linux تسمح للمسؤولين بالتحكم في الموارد والوظائف التي يمكن للبرامج الوصول إليها، مما يحمي نظام التشغيل. [codejail](https://github.com/openedx/codejail)هو بيئة رملية للـ Python مبنية على AppArmor، يمكنك تجربتها إذا كنت مهتمًا. وهناك العديد من الأدوات المماثلة، لن أذكرها جميعًا هنا.

استخدم بيئة الرمل أو الحاوية الافتراضية. [صندوق الرمل لنظام Windows](https://learn.microsoft.com/zh-cn/windows/security/threat-protection/windows-sandbox/windows-sandbox-overview)، [LXC](https://linuxcontainers.org/), [Docker](https://www.docker.com/)انتظر قليلا، لن أقوم بتوضيح ذلك هنا.

##التلخيص

هذا النص طويل قليلاً، شكراً لقراءتكم حتى هنا، أعتقد أن جميع الأسئلة المذكورة في بداية المقال قد تم الرد عليها.

--8<-- "footer_ar.md"


> هذا المنشور تم ترجمته باستخدام ChatGPT، الرجاء تقديم [**ملاحظات**](https://github.com/disenone/wiki_blog/issues/new)أشير إلى أي نقص أو غياب. 
