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
description: __builtin__ ما الفرق بين __builtins__؟ هل __builtins__ في وحدة main مختلف
  عن الوحدات الأخرى؟ لماذا يتم تحديدها بشكل مختلف؟ أين تم تعريف __builtins__؟ في هذه
  المقالة، سنتناول بعض المعلومات الشيقة حول __builtins__، بالإضافة إلى بعض المحتويات
  الإضافية التي لا ينبغي تفويتها.
figures: []
---

<meta property="og:title" content="Python 杂谈 1 - 探究 __builtins__ - Disenone" />

##مقدمة

نحن نعلم أن `__builtins__` هو كائن موجود في مساحة الأسماء العالمية، وهو معروض عمدًا من قبل `Python` للطبقات البرمجية، ويمكن استخدامه مباشرة في أي مكان في الكود. لكن هناك معلومة غريبة بعض الشيء، وهي أن `__builtins__` في الوحدة `main` (أي `__main__`، ويشير كلاهما إلى نفس الوحدة، وقد يتم استخدامهما بالتبادل لاحقًا) هو عبارة عن الوحدة `__builtin__`، ولكن في الوحدات الأخرى، فإنه يمثل `__builtin__.__dict__`، وهذا قد يسبب القليل من الارتباك. على الرغم من أن الجهة الرسمية لا توصي باستخدام `__builtins__` مباشرة، فما هي تلك الحالتين؟ في هذه المقالة، سنقوم بتتبع أصل هذا الإعداد، وفي هذه العملية، يمكننا إيجاد إجابات لهذه الأسئلة: ما الفرق بين `__builtin__` و `__builtins__`؟ لماذا يتم تعيين `__builtins__` في الوحدة `main` بشكل مختلف عن الوحدات الأخرى؟ وأين تم تعريف `__builtins__`؟


## `__builtin__`

قبل مناقشة `__builtins__`، نحتاج أولاً إلى فهم ماهية `__builtin__`. `__builtin__` هو الوحدة التي تحتوي على جميع الكائنات المدمجة؛ فالكائنات المدمجة في `Python` التي يمكننا استخدامها مباشرة هي في الأساس كائنات موجودة في وحدة `__builtin__`، أي تلك الموجودة في `__builtin__.__dict__`، التي تت correspond بشكل مباشر مع مساحة الأسماء المدمجة في `Python`. تذكر هذه النقطة المهمة: `__builtin__` هو وحدة (`module`). يمكننا العثور على تعريف واستخدام وحدة `__builtin__` في كود مصدر `Python` (لاحظ أن كود `Python` المشار إليه أدناه هو CPython-2.7.18):

``` c
// pythonrun.c
void
Py_InitializeEx(int install_sigs)
{
    PyInterpreterState *interp;
    ...
// تهيئة __builtin__
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
احصل على الوظائف الأساسية
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

عندما يتم تهيئة `Python`، يتم استدعاء `_PyBuiltin_Init` لإنشاء وحدة `__builtin__` وإضافة الكائنات الداخلية إليها. يشير المفسر بنفسه إلى `interp->builtins = __buintin__.__dict__`، بينما يشير الإطار التنفيذي الحالي أيضًا إلى `current_frame->f_builtins`. وبطبيعة الحال، عندما يحتاج تنفيذ الشيفرة إلى البحث عن كائن بناءً على الاسم، يقوم `Python` بالبحث في `current_frame->f_builtins`، مما يمكنه من الوصول إلى جميع الكائنات الداخلية.

```c
// ceval.c
TARGET(LOAD_NAME)
{
// ابحث أولاً في مساحة الأسماء f->f_locals
    ...
    if (x == NULL) {
// يُرجى البحث مرة أخرى في الفضاء العام
        x = PyDict_GetItem(f->f_globals, w);
        if (x == NULL) {
الرجاء تزويدي بنص آخر للترجمة، لا يمكن ترجمة الرموز والأحرف التي لا يتم فهمها.
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

في النهاية ، بسبب كون اسم `__builtin__` مضللاً للغاية ، تم إعادة تسميته في `Python3` إلى `builtins`.


## `__builtins__`

`__builtins__` سلوكه غريب بعض الشيء:
* في وحدة `main` (وحدة `main`، أو ما يسمى `بيئة تشغيل الشيفرة الأعلى`، هي الوحدة التي يحددها المستخدم لتبدأ التشغيل أولاً في `Python`، أي عندما نقوم عادةً بتنفيذ الأمر `python xxx.py` من سطر الأوامر، فإن الوحدة `xxx.py` هي التي يتم تشغيلها)، `__builtins__ = __builtin__`؛
* في وحدات أخرى `__builtins__ = __builtin__.__dict__`.

أسماء متماثلة، لكن تتصرف بشكل مختلف تحت وحدات مختلفة، هذا النوع من التعيينات يمكنه أن يثير الشكوك. ولكن بمعرفة هذا التعيين، سيكون ذلك كافيًا لدعمك في استخدام `__builtins__` في `Python`، فالشكوك لن تؤثر على قدرتك على كتابة كود آمن بما فيه الكفاية، مثل:

``` python
def SetBuiltins(builtins, key, val):
    if isinstance(builtins, dict):
        builtins[key] = val
    else:
        setattr(builtins, key, val)

SetBuiltins(__builtins__, 'test', 1)
```

يجب أخذ العلم بأنه في الواقع غير مُستحسَن استخدام `__builtins__`:

> تفاصيل تنفيذ CPython: لا ينبغي للمستخدمين لمس `__builtins__`؛ إنه تفصيل تنفيذي بدقة. الراغبون في تجاوز القيم في مساحة الأسماء المدمجة يجب أن يقوموا باستيراد الوحدة `__builtin__` (بدون 's') وتعديل سماتها بشكل مناسب.

بالطبع، هذه الشكوك ستجعلك في يوم من الأيام تشعر بالفضول، ولذلك قررت هنا أن أواصل البحث، ولهذا السبب كتبنا هذه المقالة. سنتناول في المحتوى التالي تفاصيل __تنفيذ CPython__ بشكل أعمق.

## Restricted Execution

التنفيذ المحدود يمكن تفسيره على أنه تنفيذ محدود للكود غير الآمن، وعند الحديث عن التحديد، يمكن أن يكون هذا التحديد متعلقًا بالشبكة أو الإدخال/الإخراج وغيرها، يتم تقييد الكود في بيئة تنفيذ معينة، وضبط صلاحيات تنفيذ الكود، لمنع تأثير الكود على البيئة الخارجية والنظام. واحد من الأمثلة الشائعة هو بعض مواقع تنفيذ الكود عبر الإنترنت، مثل هذا الموقع: [pythonsandbox](https://pythonsandbox.dev/)。

كما تخيلت، إعداد `Python` لـ `__builtins__` يتعلق بالتنفيذ المقيد. قبل الإصدار 2.3، قدمت `Python` ميزات مشابهة [التنفيذ المقيد](https://docs.python.org/2.7/library/restricted.html)فقط لأنه ثبت لاحقًا أنه غير قابل للتنفيذ، اضطررنا لإلغاء هذه الميزة، لكن الشيفرة لا تزال موجودة في الإصدار 2.7.18، لذلك يمكننا القيام بالتنقيب.

دعنا نلقي نظرة أولا على الضبط في مصدر `Python` بالنسبة لـ `__builtins__`:

``` c
// pythonrun.c
static void initmain(void)
{
    PyObject *m, *d;
الحصول على وحدة __main__
    m = PyImport_AddModule("__main__");
    if (m == NULL)
        Py_FatalError("can't create __main__ module");

    // d = __main__.__dict__
    d = PyModule_GetDict(m);

قم بتعيين __main__.__dict__['__builtins__']، وإذا تم بالفعل ذلك، فتخطى
    if (PyDict_GetItemString(d, "__builtins__") == NULL) {
        PyObject *bimod = PyImport_ImportModule("__builtin__");
        if (bimod == NULL ||
            PyDict_SetItemString(d, "__builtins__", bimod) != 0)
            Py_FatalError("can't add __builtins__ to __main__");
        Py_XDECREF(bimod);
    }
}
```

في `initmain`، سيُعين `Python` خاصية `__builtins__` لوحدة `__main__`، حيث تكون القيمة الافتراضية تساوي وحدة `__builtin__`، ولكن إذا كانت موجودة بالفعل، فسيتم تجاوز الإعداد مرة أخرى. باستخدام هذه الميزة، يمكننا تعديل `__main__.__builtins__` لتعديل بعض الوظائف الأساسية، بهدف تقييد صلاحيات تنفيذ الكود، كيفية التنفيذ بالتحديد لا يمكن الكشف عنه الآن، دعونا نلقي نظرة على كيفية تمرير `__builtins__`.

##`__builtins__` 传递

在创建新的栈帧的时候：  
عند إنشاء إطار مكدس جديد:

```c
PyFrameObject *
PyFrame_New(PyThreadState *tstate, PyCodeObject *code, PyObject *globals,
            PyObject *locals)
{
    ...
    if (back == NULL || back->f_globals != globals) {
// احصل على globals['__builtins__'] كـ __builtins__ لإطار المكدس الجديد
// builtin_object هو السلسلة '__builtins__'
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
// أو مباشرة وراثة f_builtins من إطار المكدس السابق
        builtins = back->f_builtins;
        assert(builtins != NULL && PyDict_Check(builtins));
        Py_INCREF(builtins);
    }
    ...
    f->f_builtins = builtins;
    f->f_globals = globals;
}
```

عند إنشاء إطار الدعم الجديد، هناك حالتان رئيسيتان لمعالجة `__builtins__`: إما عدم وجود إطار دعم علوي، في هذه الحالة سيتم استخدام `globals['__builtins__']`؛ أو التقاط إطار دعم `f_builtins` مباشرة من الإطار العلوي. بهذه الطريقة، يمكن فهمها كما أنه عموماً، سيتم توريث `__builtins__` المعدة في `__main__` إلى الإطارات اللاحقة، كما لو كانت تشترك في الاستخدام نفسه.

عند استيراد الوحدة:

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

قم بتعيين خاصية __builtins__ للوحدة الجديدة المحملة هنا
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

عند استيراد وحدات أخرى، يتم ضبط `__builtins__` لهذه الوحدة كنتيجة لدالة `PyEval_GetBuiltins()`، هذه الدالة التي ذكرناها من قبل، في معظم الحالات تكون ما يعادل `current_frame->f_builtins`. بالنسبة للاستيراد في وحدة `__main__`، `current_frame` هو إطار الدعم الخاص بوحدة `__main__`، وتكون `current_frame->f_builtins = __main__.__dict__['__builtins__']` (كما هو مذكور في الحالة الأولى لـ `PyFrame_New`).

يتم استخدام `PyEval_EvalCode` لتنفيذ الشيفرة في الوحدة الجديدة التي تم تحميلها، ويمكن ملاحظة أن المعاملات المعطاة لـ `PyEval_EvalCode`، `globals` و `locals`، هي في الحقيقة `__dict__` الخاصة بالوحدة نفسها، بالإضافة إلى أن الوحدة `m.__dict__['__builtins__'] = PyEval_GetBuiltins()` .

من خلال النظر الشامل، يمكننا أن نستنتج أنه عند استيراد الوحدات (modules) من وحدة `__main__`، فإن هذه الوحدات ستُرث `__builtins__` الموجودة في `__main__`، وستُمرر ذلك في الاستيراد الداخلي، مما يضمن أن جميع الوحدات الفرعية (submodules) المحمّلة من `__main__` ستتمكن من مشاركة نفس مجموعة `__builtins__` القادمة من `__main__`.

إذن ماذا عن الدوال التي يتم استدعاؤها داخل الوحدة؟ بالنسبة للدوال في الوحدة، عند الإنشاء والاستدعاء:

```c
// ceval.c
// إنشاء دالة
TARGET(MAKE_FUNCTION)
{
    v = POP(); /* code object */

// هنا f->f_globals ، تعادل globals الخاصة بالوحدة نفسها ، كما يتضح من النص أعلاه ، تعادل أيضًا m.__dict__
    x = PyFunction_New(v, f->f_globals);
    ...
}

PyObject *
PyFunction_New(PyObject *code, PyObject *globals)
{
    PyFunctionObject *op = PyObject_GC_New(PyFunctionObject,
                                        &PyFunction_Type);
    ...
هنا يعادل op->func_globals = globals = f->f_globals
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
// globals تُمرر إلى PyEval_EvalCodeEx، حيث تُمرر إلى PyFrame_New لإنشاء إطار مكدس جديد
    return PyEval_EvalCodeEx(co, globals,
                             (PyObject *)NULL, (*pp_stack)-n, na,
                             (*pp_stack)-2*nk, nk, d, nd,
                             PyFunction_GET_CLOSURE(func));
}
```

عند إنشاء الدالة، يتم تخزين `f->f_globals` في متغير هيكل الدالة `func_globals`، أما بالنسبة للوحدة `m`، فإن `f->f_globals = m.__dict__`. عند تنفيذ الدالة، فإن المعامل `globals` المرسل إلى `PyFrame_New` هو `func_globals` الذي تم الاحتفاظ به عند الإنشاء، وبهذا يمكن بالطبع الحصول على `__builtins__` من `func_globals`.

至此，`__builtins__` 的传递是能保证一致性的，所有模块、子模块 、函数，栈帧等都能引用到同一个，也就是拥有相同的内建名字空间。

##تعني تحديد تنفيذ وحدة `__main__`

لقد تم تحديد أننا (نحن) نعلم الآن إن الوحدة `__main__` من الوظائف الأساسية يمكن أن تنقل إلى جميع الوحدات الفرعية والدوال وإطارات البرنامج، وعند تشغيل Python من خلال السطر الأمر `python a.py`، يقوم Python بتنفيذ الملف `a.py` كوحدة `__main__`، فكيف يتحقق هذا؟

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
// حاول استخدام المستورد الخاص بالوحدة لتنفيذ الكود
    if (filename != NULL) {
        sts = RunMainFromImporter(filename);
    }
    ...
// عادةً ما نستخدم هذا لتنفيذ ملفات py الخاصة بنا
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
// تعيين خاصية __file__
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
// قراءة كائن الشيفرة co من ملف pyc ، وتنفيذ الشيفرة
// ستقوم PyEval_EvalCode بالاتصال أيضًا بـ PyFrame_New لإنشاء إطار مكدس جديد
    v = PyEval_EvalCode(co, globals, locals);
    ...
}
```

عند تنفيذ `python a.py`، في الظروف العادية، سيصل التنفيذ إلى `PyRun_SimpleFileExFlags`، حيث سيتم استخراج `__main__.__dict__` منها كـ `globals` و `locals` خلال تشغيل الكود، و سيُمرر في النهاية إلى `PyFrame_New` لإنشاء إطار مكدس جديد لتنفيذ `a.py`. بالجمع بين ما ذكرناه سابقاً عن انتقال `__builtins__` في الوحدات والدوال، يمكن أن تسمح هذه الطريقة للكود الذي سيتم تطبيقه لاحقاً بمشاركة نفس النسخة من `current_frame->f_builtins = __main__.__builtins__.__dict__`.


##إعادة النظر في التنفيذ المقيد

"Python" كان يوفر [Restricted Execution](https://docs.python.org/2.7/library/restricted.html)هو مبني على خاصية `__builtins__`. أو يمكن اعتباره أن تم تصميم `__builtins__` ليكون ككائن موديول في نموذج `__main__`، بينما في النماذج الأخرى ككائن من نوع `dict`، من أجل تحقيق التنفيذ المحدود.

考虑这种情况：如果我们可以自由定制自己的 `__builtin__` 模块，并设置成 `__main__.__builtins__`，那就相当于后续所有执行的代码，都会使用我们定制的模块，我们可以定制特定版本的 `open`、`__import__`、`file` 等内建函数和类型，更进一步，这种方式是不是可以帮助我们限制执行代码的权限，防止代码做一些不安全的函数调用，或者访问一些不安全的文件？

في ذلك الوقت، تم القيام بمثل هذه المحاولة في `Python`، وكان اسم الوحدة التي تحقق هذه الوظيفة هو: `rexec`.

### `rexec`

لا أنوي التعمق كثيرًا في شرح تنفيذ `rexec`، لأن المبادئ فعلياً تم شرحها بالفعل في النص السابق، بالإضافة إلى أن هذه الوحدة بحد ذاتها قد أصبحت منسوخة، سأقوم فقط بتلخيص بعض الشفرات الرئيسية لتسهيل الاطلاع عليها.


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

تقوم وظيفة r_execfile بتنفيذ الملف كوحدة main على أنها مخصصة. في داخل self.add_module('__main__')، سيتم تعيين m.__builtins__ للوحدة النمطية self.modules['__builtin__']، حيث تم إنشاء '__builtin__' بواسطة make_builtin بحيث يقوم بتحديث وظائف __import__ و reload و open، وحذف نوع البيانات file. بفضل هذا، يمكننا التحكم في الوصول إلى فضاء الأسماء المدمجة من خلال رمز التنفيذ.

بالنسبة لبعض الوحدات المضمّنة، قام "rexec" بتخصيص حماية الوصول غير الآمن، مثل وحدة `sys`، حيث يتم الاحتفاظ فقط بجزء من الكائنات، ويتم تنفيذ تحميل الوحدة المخصّصة بالأسبقية أثناء عملية الـ `import` من خلال `self.loader` و `self.importer` المخصصتين.

إذا كنت مهتمًا بتفاصيل الشيفرة، يُرجى الرجوع إلى الشيفرات المصدرية ذات الصلة.

###فشل `rexec`

سبق الإشارة في النص أعلاه إلى أن `rexec` قد تم تهجيره بعد `Python 2.3`، لأنه تم تأكيد عدم جدواه. من أجل إشباع فضولنا، دعونا نعود ببساطة إلى جذور الأمر:

* في المجتمع، تم الإبلاغ عن [خطأ](https://mail.python.org/pipermail/python-dev/2002-December/031160.html)وشجَّب نقاشاً بين المطورين:

    > it's never going to be safe, and I doubt it's very useful as long as it's not safe.

    > Every change is a potential security hole.

    > it's hard to predict what change is going to break it.

    > I don't expect you'll ever reach the point where it'll be wise to advertise this as safe.  I certainly won't.

    >  this is only a useful occupation if you expect to eventually reach a point where you expect that there aren't any security flaws left.  Jeremy & I both doubt that Python will ever reach that level, meaning that the whole exercise of fixing security flaws is a waste of time (if you know you *can't* make it safe, don't waste time trying).

    > I agree (but I have said that in past) the best thing is to deprecate/rip out rexec.

    > The code will still be in older versions if someone decides to pick it up and work on it as a separate project.

* سبب هذه المشكلة هو أن `Python` قدمت فئة جديدة (new-style class) وهي `object`، مما أدى إلى عدم عمل `rexec` بشكل صحيح. لذلك، أفاد المطورون أنه في المستقبل القريب، سيكون من الصعب تجنب هذه الحالة، لأن أي تعديل قد يؤدي إلى ثغرات في `rexec`، مما يجعله غير قادر على العمل بشكل صحيح، أو يخترق قيود الأذونات. بشكل أساسي، من المستحيل تحقيق رؤية بيئة آمنة دون ثغرات، مما يستدعي من المطورين العمل بشكل مستمر على الإصلاحات، مما يضيع الكثير من الوقت. في النهاية، تم إهمال وحدة `rexec`، ولم توفر `Python` أي وظائف مشابهة بعد ذلك. لكن بخصوص إعداد `__builtins__`، فقد تم الاحتفاظ به بسبب مشاكل التوافق وغيرها.

خلال حوالي عام 2010 تقريبًا، قام مطور برامج بإطلاق [pysandbox](https://github.com/vstinner/pysandbox)، وتهدف إلى توفير بيئة `Python` صح Sandbox بديلة لـ `rexec`. ومع ذلك، بعد ثلاث سنوات، تخلّى المؤلف عن هذا المشروع طواعية، موضحًا بالتفصيل لماذا يعتبر أن هذا المشروع كان فاشلاً: [مشروع pysandbox معطل](https://mail.python.org/pipermail/python-dev/2013-November/130132.html)وقد قام أيضاً مؤلفون آخرون بتلخيص فشل هذا المشروع: [فشل pysandbox](https://lwn.net/Articles/574215/)إذا كنت مهتمًا، يمكنك الرجوع إلى النص الأصلي، وسأقدم هنا بعض الملخصات للمساعدة في الفهم:

> After having work during 3 years on a pysandbox project to sandbox untrusted code, I now reached a point where I am convinced that pysandbox is broken by design. Different developers tried to convinced me before that pysandbox design is unsafe, but I had to experience it myself to be convineced.

> I now agree that putting a sandbox in CPython is the wrong design. There are too many ways to escape the untrusted namespace using the various introspection features of the Python language. To guarantee the [safety] of a security product, the code should be [carefully] audited and the code to review must be as small as possible. Using pysandbox, the "code" is the whole Python core which is a really huge code base. For example, the Python and Objects directories of Python 3.4 contain more than 126,000 lines of C code.

> The security of pysandbox is the security of its weakest part. A single bug is enough to escape the whole sandbox.

> pysandbox cannot be used in practice. To protect the untrusted namespace, pysandbox installs a lot of different protections. Because of all these protections, it becomes hard to write Python code. Basic features like "del dict[key]" are denied. Passing an object to a sandbox is not possible to sandbox, pysandbox is unable to proxify arbitary objects. For something more complex than evaluating "1+(2*3)", pysandbox cannot be used in practice, because of all these protections.

يعتقد مؤلف __pysandbox__ أن وضع بيئة عازلة داخل `Python` هو تصميم خاطئ، حيث توجد طرق عديدة للهروب من هذه البيئة. تقدم `Python` ميزات لغوية غنية، وحجم الشيفرة المصدرية لـ `CPython` كبير جداً، مما يجعل من المستحيل تقريباً ضمان مستوى كافٍ من الأمان. كانت عملية تطوير __pysandbox__ عبارة عن تصحيح مستمر، حيث كانت هناك العديد من التصحيحات والقيود، لدرجة أن المؤلف يرى أن __pysandbox__ لم يعد قابلاً للاستخدام العملي، لأن العديد من ميزات اللغة والوظائف قد تم تقييد استخدامها، مثل `del dict[key]` البسيطة.

##التنفيذ المحدود - أين المخرج

بما أن الطرق التي تعتمد على تعديل Python مثل `rexec` و__pysandbox__ لتوفير بيئة رملية لم تعد فعالة، فإنني لا أستطيع إلا أن أتساءل: كيف يمكننا توفير بيئة رملية صالحة للاستخدام لـ Python؟

هنا، واصلت جمع بعض الطرق التنفيذية الأخرى أو الحالات العملية للرجوع إليها والاطلاع عليها:

* [PyPy](https://doc.pypy.org/en/latest/sandbox.html)有一个[分支]  
يوجد [فرع](https://foss.heptapod.net/pypy/pypy/-/tree/branch/sandbox-2)提供了沙盒的功能，结合额外的 [sandboxlib]  
قدم ميزة الصندوق الرملي، بالاشتراك مع [sandboxlib](https://foss.heptapod.net/pypy/sandboxlib)يمكنك تجميع إصدار PyPy الذي يأتي مع بيئة Sandbox بنفسك. إذا كنت مهتمًا، يمكنك محاولة تكوينه بنفسك، وراجع بعض [التوجيهات](https://foss.heptapod.net/pypy/pypy/-/issues/3192)تقنية PyPy تقوم على إنشاء عملية فرعية، حيث يتم إعادة توجيه جميع المدخلات والمخرجات واستدعاءات النظام الخاصة بالعملية الفرعية إلى عملية خارجية، والتي تتحكم في هذه الصلاحيات. بالإضافة إلى ذلك، يمكن التحكم في استخدام الذاكرة وCPU. تجدر الإشارة إلى أن هذا الفرع لم يشهد أي تحديثات جديدة منذ بعض الوقت، لذا يرجى استخدامه بحذر.

استخدام أدوات بيئة الرمال الناتجة عن نظام التشغيل. [seccomp](https://en.wikipedia.org/wiki/Seccomp)هو أداة تضامن آمنة مقدمة من نواة Linux، [libsecoomp](https://github.com/seccomp/libseccomp/tree/main/src/python)يوفر ربط Python، يمكن تضمينه في الشيفرة لاستخدامه؛ أو استخدام أدوات تعتمد على تنفيذ seccomp لتنفيذ الشيفرة، مثل [Firejail](https://firejail.wordpress.com/)ترجمة النص إلى اللغة العربية:

[AppArmor](https://apparmor.net/)هو وحدة أمان نواة Linux، تتيح للمسؤول التحكم في الموارد والوظائف النظامية التي يمكن للبرامج الوصول إليها، مما يحمي نظام التشغيل. [codejail](https://github.com/openedx/codejail)يستند إلى بيئة Python sandbox التي تم تنفيذها باستخدام AppArmor، إذا كنت مهتمًا يمكنك التجربة. هناك العديد من الأدوات المماثلة، ولن أذكرها جميعًا هنا.

* استخدام بيئة افتراضية أو حاويات (Sandbox). [Windows Sandbox](https://learn.microsoft.com/zh-cn/windows/security/threat-protection/windows-sandbox/windows-sandbox-overview)،[LXC](https://linuxcontainers.org/), [Docker](https://www.docker.com/)انتظر، لن أذكر المزيد من التفاصيل هنا.

##ملخص

هذا النص طويل قليلاً، شكرًا لك على الوصول إلى هنا، نعتقد أن جميع الأسئلة المدرجة في بداية المقال قد تم الرد عليها بالفعل.

--8<-- "footer_ar.md"


> يتمتع هذا المنشور بترجمة باستخدام ChatGPT، يرجى تقديم [**تغذية راجعة**](https://github.com/disenone/wiki_blog/issues/new)يرجى الإشارة إلى أي نقاط مفقودة. 
