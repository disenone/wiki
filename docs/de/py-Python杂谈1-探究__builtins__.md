---
layout: post
title: Python Plauderei 1 - Erforschung von __builtins__
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
description: __builtin__ und __builtins__ Unterschiede? Ist __builtins__ im main-Modul
  anders als in anderen Modulen? Warum wurde es unterschiedlich festgelegt? Wo wird
  __builtins__ definiert? In diesem Artikel werden wir einige interessante Fakten
  über __builtins__ erörtern und auch einige verwandte Themen ansprechen, die Sie
  nicht verpassen sollten.
figures: []
---

<meta property="og:title" content="Python 杂谈 1 - 探究 __builtins__ - Disenone" />

##Einleitung

Wir wissen, dass `__builtins__` selbst ein Objekt ist, das im globalen Namensraum vorhanden ist und absichtlich von Python dem Code zur Verfügung gestellt wird, sodass es an beliebiger Stelle im Code direkt verwendet werden kann. Eine etwas kuriose Tatsache ist, dass `__builtins__` im Hauptmodul (auch bekannt als `__main__`, beide Bezeichnungen beziehen sich auf dasselbe Modul, was später möglicherweise gemischt verwendet wird) das Modul `__builtin__` ist, während es in anderen Modulen `__builtin__.__dict__` bedeutet, was ein wenig verwirrend sein kann. Obwohl die offizielle Empfehlung lautet, `__builtins__` nicht direkt zu nutzen, frage ich mich, warum es zwei verschiedene Situationen gibt. In diesem Artikel werden wir die Herkunft dieser Regelung untersuchen und dabei Antworten auf folgende Fragen finden: Was sind die Unterschiede zwischen `__builtin__` und `__builtins__`? Warum werden `__builtins__` im Hauptmodul und in anderen Modulen unterschiedlich festgelegt? Wo ist `__builtins__` definiert?


## `__builtin__`

Bevor wir `__builtins__` diskutieren, müssen wir zunächst klären, was `__builtin__` ist. `__builtin__` ist das Modul, das alle eingebauten Objekte speichert. Die eingebauten Objekte von `Python`, die wir normalerweise direkt verwenden können, sind im Wesentlichen Objekte aus dem `__builtin__`-Modul, das heißt, sie befinden sich im `__builtin__.__dict__` und entsprechen dem eingebauten Namensraum von `Python`. Merken Sie sich diesen wichtigen Punkt: `__builtin__` ist ein Modul. Wir können die Definition und Nutzung des `__builtin__`-Moduls im `Python`-Quellcode finden (beachten Sie, dass sich der im Folgenden erwähnte `Python`-Quellcode auf CPython-2.7.18 bezieht):

``` c
// pythonrun.c
void
Py_InitializeEx(int install_sigs)
{
    PyInterpreterState *interp;
    ...
// Initialisierung __builtin__
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

Fügen Sie dem Dictionary eingebaute Objekte hinzu.
    ...
}

// ceval.c
Holen der integrierten Funktionen.
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

`Python` ruft beim Initialisieren `_PyBuiltin_Init` auf, um das `__builtin__`-Modul zu erstellen und darin die eingebauten Objekte hinzuzufügen. Der Interpreter selbst verweist auf `interp->builtins = __builtin__.__dict__`, während die derzeit ausgeführte Stapelrahmenstruktur ebenfalls eine Referenz auf `current_frame->f_builtins` hat. So ist es nur natürlich, dass `Python`, wenn der Code ein Objekt anhand des Namens sucht, in `current_frame->f_builtins` nachschaut und somit alle eingebauten Objekte abrufen kann:

```c
// ceval.c
TARGET(LOAD_NAME)
{
// Zuerst im Namensraum von f->f_locals suchen
    ...
    if (x == NULL) {
// Suche den globalen Raum erneut
        x = PyDict_GetItem(f->f_globals, w);
        if (x == NULL) {
Bitte suchen Sie den integrierten Speicherplatz hier.
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

Schließlich wurde der Name `__builtin__` aufgrund seiner Verwirrung durch `Python3` in `builtins` geändert.


## `__builtins__`

`__builtins__` behave a bit strangely:
* Im `main`-Modul (das `main`-Modul, auch als `Umgebung des höchsten Code-Laufniveaus` bezeichnet, ist das `Python`-Modul, das der Benutzer angibt, um zuerst zu starten. Das ist normalerweise das Modul, das wir beim Ausführen von `python xxx.py` im Terminal verwenden, also `xxx.py`), `__builtins__ = __builtin__`；
In anderen Modulen ist `__builtins__ = __builtin__.__dict__` gesetzt.

Der gleiche Name, aber unterschiedliches Verhalten in verschiedenen Modulen kann leicht Verwirrung stiften. Doch sobald Sie dieses Konzept verstehen, sind Sie gut gerüstet, um `__builtins__` in `Python` zu verwenden. Ihre Verwirrung wird sich nicht darauf auswirken, dass Sie sicheren Code schreiben können, wie zum Beispiel:

``` python
def SetBuiltins(builtins, key, val):
    if isinstance(builtins, dict):
        builtins[key] = val
    else:
        setattr(builtins, key, val)

SetBuiltins(__builtins__, 'test', 1)
```

Es ist wichtig zu beachten, dass die Verwendung von `__builtins__` eigentlich nicht empfohlen wird:

> __CPython-Implementierungsdetail__: Benutzer sollten `__builtins__` nicht anfassen; es ist strikt ein Implementierungsdetail. Benutzer, die Werte im Builtins-Namespace überschreiben möchten, sollten das `__builtin__` (ohne ‘s’) Modul importieren und dessen Attribute entsprechend ändern.

Natürlich wird dich solche Zweifel eines Tages unruhig machen, und ich habe mich entschlossen, weiter zu forschen. Deshalb gibt es diesen Artikel. Im Folgenden werden wir in die __CPython-Implementierungsdetails__ eintauchen.

## Restricted Execution

Restricted Execution kann als die eingeschränkte Ausführung unsicherer Code verstanden werden. Mit "eingerichtet" ist gemeint, dass Einschränkungen bezüglich Netzwerk, IO usw. bestehen, um den Code in einer bestimmten Ausführungsumgebung zu isolieren, die Ausführungsberechtigungen des Codes zu steuern und zu verhindern, dass der Code die externe Umgebung und Systeme beeinflusst. Ein häufiges Anwendungsbeispiel sind Online-Code-Ausführungswebsites, wie etwa diese: [pythonsandbox](https://pythonsandbox.dev/)。

Wie du vermutet hast, hängt die Einstellung von `Python` zu `__builtins__` mit der eingeschränkten Ausführung zusammen. `Python` bot vor der Version 2.3 eine ähnliche Funktionalität [Restricted Execution](https://docs.python.org/2.7/library/restricted.html)Nur weil es später als nicht machbar bestätigt wurde, wurde diese Funktion gestrichen. Der Code ist jedoch noch in der Version 2.7.18 vorhanden, also können wir hier etwas ausgraben.

Zuerst sehen wir uns die Einstellung von `__builtins__` im Quellcode von `Python` an:

``` c
// pythonrun.c
static void initmain(void)
{
    PyObject *m, *d;
// Holen Sie sich das __main__ Modul
    m = PyImport_AddModule("__main__");
    if (m == NULL)
        Py_FatalError("can't create __main__ module");

    // d = __main__.__dict__
    d = PyModule_GetDict(m);

// Setze __main__.__dict__['__builtins__'], wenn vorhanden, überspringen
    if (PyDict_GetItemString(d, "__builtins__") == NULL) {
        PyObject *bimod = PyImport_ImportModule("__builtin__");
        if (bimod == NULL ||
            PyDict_SetItemString(d, "__builtins__", bimod) != 0)
            Py_FatalError("can't add __builtins__ to __main__");
        Py_XDECREF(bimod);
    }
}
```

Im `initmain` setzt `Python` das Attribut `__builtins__` des `__main__` Moduls, standardmäßig gleich dem Modul `__builtin__`, überspringt jedoch die Neusetzen, wenn es bereits vorhanden ist. Nutzen wir dieses Merkmal, können wir durch die Modifikation von `__main__.__builtins__` einige grundlegende Funktionen ändern, um die Ausführungsrechte des Codes einzuschränken. Die genauen Methoden lassen wir vorerst beiseite, schauen wir uns an, wie `__builtins__` übergeben wird.

##`__builtins__` Übertragung

Beim Erstellen eines neuen Stack-Frames:

```c
PyFrameObject *
PyFrame_New(PyThreadState *tstate, PyCodeObject *code, PyObject *globals,
            PyObject *locals)
{
    ...
    if (back == NULL || back->f_globals != globals) {
// Verwende globals['__builtins__'] als __builtins__ für das neue Stack-Frame
// Die builtin_object ist der String '__builtins__'
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
Oder direkt die f_builtins des übergeordneten Stack-Frames erben.
        builtins = back->f_builtins;
        assert(builtins != NULL && PyDict_Check(builtins));
        Py_INCREF(builtins);
    }
    ...
    f->f_builtins = builtins;
    f->f_globals = globals;
}
```

Bei der Erstellung eines neuen Stapelrahmens gibt es hauptsächlich zwei Möglichkeiten, wie mit `__builtins__` umgegangen wird: In einem Fall, wenn es keinen übergeordneten Stapelrahmen gibt, wird `globals['__builtins__']` genommen. Andernfalls wird einfach `f_builtins` des übergeordneten Stapelrahmens übernommen. Zusammenfassend kann man sagen, dass normalerweise das in `__main__` festgelegte `__builtins__` an die nachfolgenden Stapelrahmen weitergegeben wird und somit gemeinsam genutzt wird.

Beim Importieren eines `import`-Moduls:

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

// Hier das __builtins__ Attribut des neu geladenen Moduls festlegen
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

Beim Importieren anderer Module wird `__builtins__` des Moduls auf das Ergebnis von `PyEval_GetBuiltins()` gesetzt. Diese Funktion haben wir bereits erwähnt; in den meisten Fällen entspricht sie `current_frame->f_builtins`. Für den Import innerhalb des `__main__` Moduls ist `current_frame` das Stack-Frame des `__main__` Moduls, wobei `current_frame->f_builtins = __main__.__dict__['__builtins__']` (im ersten Fall von `PyFrame_New` oben).

Das neue Modul, das geladen wird, wird `PyEval_EvalCode` verwenden, um den Code im neuen Modul auszuführen. Es ist zu erkennen, dass die Argumente `globals` und `locals`, die an `PyEval_EvalCode` übergeben werden, tatsächlich das `__dict__` des Moduls selbst sind, und das Modul `m.__dict__['__builtins__'] = PyEval_GetBuiltins()` zugewiesen wird.

Im Allgemeinen lässt sich sagen, dass Module, die ab dem `__main__`-Modul importiert werden, auch die `__builtins__` des `__main__`-Moduls erben und sie intern bei weiteren `import`-Anweisungen weitergeben. Auf diese Weise lässt sich sicherstellen, dass alle Module und Untermodule, die von `__main__` geladen werden, denselben `__builtins__` aus `__main__` nutzen können.

Was ist, wenn die Funktion in einem Modul aufgerufen wird? Für Funktionen in Modulen gelten beim Erstellen und Aufrufen folgende Regeln:

```c
// ceval.c
Erstellen Sie die Funktion.
TARGET(MAKE_FUNCTION)
{
    v = POP(); /* code object */

// Hier entspricht f->f_globals den globals des Moduls selbst, was aus dem vorherigen Text ersichtlich ist, und entspricht auch m.__dict__
    x = PyFunction_New(v, f->f_globals);
    ...
}

PyObject *
PyFunction_New(PyObject *code, PyObject *globals)
{
    PyFunctionObject *op = PyObject_GC_New(PyFunctionObject,
                                        &PyFunction_Type);
    ...
// Hier entspricht op->func_globals = globals = f->f_globals
    op->func_globals = globals;
}

// Funktion aufrufen
static PyObject *
fast_function(PyObject *func, PyObject ***pp_stack, int n, int na, int nk)
{
    PyCodeObject *co = (PyCodeObject *)PyFunction_GET_CODE(func);
    // globals = func->func_globals
    PyObject *globals = PyFunction_GET_GLOBALS(func);
    ...
// Die globalen Variablen werden an PyEval_EvalCodeEx übergeben, was dann an PyFrame_New weitergereicht wird, um einen neuen Frame zu erstellen.
    return PyEval_EvalCodeEx(co, globals,
                             (PyObject *)NULL, (*pp_stack)-n, na,
                             (*pp_stack)-2*nk, nk, d, nd,
                             PyFunction_GET_CLOSURE(func));
}
```

Beim Erstellen einer Funktion wird `f->f_globals` in der Strukturvariable `func_globals` der Funktion gespeichert. Für das Modul `m` gilt `f->f_globals = m.__dict__`. Wenn die Funktion ausgeführt wird, ist das `globals`-Argument, das an `PyFrame_New` übergeben wird, das zu Erstellungszeit gespeicherte `func_globals`, und `__builtins__` kann natürlich in `func_globals` abgerufen werden.

Bis hierher ist die Weitergabe von `__builtins__` konsistent gewährleistet, alle Module, Untermodule, Funktionen, Stack Frames usw. können auf dasselbe verweisen und somit über denselben eingebauten Namensraum verfügen.

##Führen Sie das `__main__` Modul aus.

Wir wissen bereits, dass das `__builtins__` Modul von `__main__` an alle Untermodule, Funktionen und Rahmen übergeben werden kann. Wenn Sie `python a.py` in der Befehlszeile ausführen, wird Python `a.py` als `__main__` Modul ausführen. Aber wie wird das gemacht?

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
// Versuchen, den Importer des Moduls zu verwenden, um den Code auszuführen
    if (filename != NULL) {
        sts = RunMainFromImporter(filename);
    }
    ...
Normalerweise verwenden wir dieses, um unsere eigenen Python-Dateien auszuführen.
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
// Setze das __file__ Attribut
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
// Lesen Sie das Codeobjekt co aus der pyc-Datei und führen Sie den Code aus.
// In PyEval_EvalCode wird ebenfalls PyFrame_New aufgerufen, um ein neues Stack-Frame zu erstellen.
    v = PyEval_EvalCode(co, globals, locals);
    ...
}
```

Beim Ausführen von `python a.py` gelangt man normalerweise zu `PyRun_SimpleFileExFlags`, das in `PyRun_SimpleFileExFlags` `__main__.__dict__` abruft, welches als `globals` und `locals` während der Codeausführung dient. Letztendlich wird es auch an `PyFrame_New` übergeben, um einen neuen Stack-Frame für die Ausführung von `a.py` zu erstellen. In Verbindung mit dem zuvor erwähnten `__builtins__`, das in Modulen und Funktionen weitergegeben wird, ermöglicht dies, dass der nachfolgende Code die gleiche `current_frame->f_builtins = __main__.__builtins__.__dict__` verwendet.


##Erneute Diskussion über die eingeschränkte Ausführung

`Python` hat vor Version 2.3 eine [Restricted Execution](https://docs.python.org/2.7/library/restricted.html)Es ist also auf den Eigenschaften von `__builtins__` basiert. Man könnte auch sagen, dass `__builtins__` so entworfen wurde, dass es im `__main__`-Modul ein Modulobjekt und in anderen Modulen ein `dict`-Objekt ist, um die __Restricted Execution__ zu ermöglichen.

Denk mal darüber nach: Wenn wir unseren `__builtin__`-Modul frei anpassen könnten und es als `__main__.__builtins__` setzen würden, würde das bedeuten, dass alle nachfolgenden Code-Ausführungen unser angepasstes Modul verwenden würden. Wir könnten spezielle Versionen von `open`, `__import__`, `file` und anderen integrierten Funktionen und Typen anpassen. Darüber hinaus könnte diese Herangehensweise uns helfen, die Berechtigungen für die Codeausführung einzuschränken, um uns vor unsicheren Funktionsaufrufen oder dem Zugriff auf unsichere Dateien zu schützen.

`Python` hatte zu diesem Zeitpunkt bereits einen Versuch unternommen, um diese Funktionalität umzusetzen, und das entsprechende Modul wurde als `rexec` bezeichnet.

### `rexec`

Ich habe nicht die Absicht, die Implementierung von `rexec` zu tiefgehend zu erläutern, da die Grundlagen bereits im vorherigen Text klar dargelegt wurden und dieses Modul ohnehin veraltet ist. Ich werde lediglich einige Schlüsselausschnitte des Codes zusammenfassen, um die Nachschlagefreundlichkeit zu erleichtern.


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

Die Funktion `r_execfile` behandelt eine Datei als `__main__`-Modul, wobei `__main__` angepasst wurde. In `self.add_module('__main__')` wird das Modul so eingerichtet, dass `m.__builtins__ = self.modules['__builtin__']` gesetzt wird. Dieses `__builtin__` wird von `make_builtin` angepasst generiert, wobei `__import__`, `reload` und `open` Funktionen ersetzt und der `file`-Typ entfernt wurde. Auf diese Weise können wir den Zugriff des auszuführenden Codes auf den integrierten Namensraum steuern.

Für einige integrierte Module hat `rexec` ebenfalls Anpassungen vorgenommen, um unsicheren Zugriff zu schützen. Zum Beispiel wurde im `sys`-Modul nur ein Teil der Objekte beibehalten, und durch die angepassten `self.loader` und `self.importer` wird sichergestellt, dass beim `import` vorrangig die angepassten Module geladen werden.

Wenn Sie sich für die Details des Codes interessieren, konsultieren Sie bitte den entsprechenden Quellcode selbst.

###Das Versagen von `rexec`.

In dem obigen Text wurde erwähnt, dass `rexec` nach `Python 2.3` bereits eingestellt wurde, da sich diese Methode als unpraktikabel erwiesen hat. Neugierig geworden, wollen wir einen kurzen Überblick über die Geschichte werfen:

In der Community wurde ein [Fehler](https://mail.python.org/pipermail/python-dev/2002-December/031160.html)Und löste eine Diskussion unter den Entwicklern aus:

    > it's never going to be safe, and I doubt it's very useful as long as it's not safe.

    > Every change is a potential security hole.

    > it's hard to predict what change is going to break it.

    > I don't expect you'll ever reach the point where it'll be wise to advertise this as safe.  I certainly won't.

    >  this is only a useful occupation if you expect to eventually reach a point where you expect that there aren't any security flaws left.  Jeremy & I both doubt that Python will ever reach that level, meaning that the whole exercise of fixing security flaws is a waste of time (if you know you *can't* make it safe, don't waste time trying).

    > I agree (but I have said that in past) the best thing is to deprecate/rip out rexec.

    > The code will still be in older versions if someone decides to pick it up and work on it as a separate project.

Der Fehler entstand durch die Einführung der neuen Klasse `object` in `Python`, was dazu führte, dass `rexec` nicht ordnungsgemäß funktionierte. Die Entwickler gaben an, dass es in naher Zukunft schwierig sein würde, solche Situationen zu vermeiden, da jede Änderung dazu führen könnte, dass `rexec` anfällig wird, nicht ordnungsgemäß funktioniert oder die Berechtigungsbeschränkungen umgangen werden können. Die Vision, eine sichere Umgebung ohne Sicherheitslücken bereitzustellen, war daher praktisch nicht realisierbar, da Entwickler kontinuierlich Zeit damit verbringen müssten, Probleme zu beheben. Letztendlich wurde das Modul `rexec` eingestellt, und `Python` bot keine ähnliche Funktionalität mehr an. Jedoch wurde die Einstellung betreffend `__builtins__` aus Kompatibilitätsgründen beibehalten.

In etwa im Jahr 2010 brachte ein Softwareentwickler [pysandbox](https://github.com/vstinner/pysandbox), verpflichtet, eine `Python` Sandbox-Umgebung anzubieten, die `rexec` ersetzen kann. Drei Jahre später gab der Autor jedoch das Projekt freiwillig auf und erklärte ausführlich, warum er der Meinung war, dass das Projekt gescheitert ist: [The pysandbox project is broken](https://mail.python.org/pipermail/python-dev/2013-November/130132.html)Es gibt auch andere Autoren, die über das Scheitern dieses Projekts geschrieben haben: [The failure of pysandbox](https://lwn.net/Articles/574215/)Wenn Sie interessiert sind, können Sie den Originaltext spezifisch durchblättern. Ich gebe hier auch einige Zusammenfassungen zur Unterstützung des Verständnisses:

> After having work during 3 years on a pysandbox project to sandbox untrusted code, I now reached a point where I am convinced that pysandbox is broken by design. Different developers tried to convinced me before that pysandbox design is unsafe, but I had to experience it myself to be convineced.

> I now agree that putting a sandbox in CPython is the wrong design. There are too many ways to escape the untrusted namespace using the various introspection features of the Python language. To guarantee the [safety] of a security product, the code should be [carefully] audited and the code to review must be as small as possible. Using pysandbox, the "code" is the whole Python core which is a really huge code base. For example, the Python and Objects directories of Python 3.4 contain more than 126,000 lines of C code.

> The security of pysandbox is the security of its weakest part. A single bug is enough to escape the whole sandbox.

> pysandbox cannot be used in practice. To protect the untrusted namespace, pysandbox installs a lot of different protections. Because of all these protections, it becomes hard to write Python code. Basic features like "del dict[key]" are denied. Passing an object to a sandbox is not possible to sandbox, pysandbox is unable to proxify arbitary objects. For something more complex than evaluating "1+(2*3)", pysandbox cannot be used in practice, because of all these protections.

Der Autor von __pysandbox__ ist der Meinung, dass es ein fehlerhaftes Design ist, in `Python` eine Sandbox-Umgebung zu haben. Es gibt zu viele Möglichkeiten, aus der Sandbox auszubrechen, die Sprachfunktionen, die Python bietet, sind sehr vielfältig. Der Umfang des CPython-Quellcodes ist so groß, dass es im Grunde unmöglich ist, ausreichende Sicherheit zu gewährleisten. Der Entwicklungsprozess von __pysandbox__ besteht im ständigen Patchen, aber es gibt so viele Patches und Einschränkungen, dass der Autor findet, dass __pysandbox__ praktisch nicht mehr verwendbar ist. Viele syntaktische Eigenschaften und Funktionen sind eingeschränkt, z.B. das einfache `del dict[key]`.

##Eingeschränkte Ausführung: Wo ist der Ausweg?

Da "rexec" und "pysandbox", Methoden, die über das Patchen von Python eine Sandbox-Umgebung bereitstellen (ich nenne diese Methode vorläufig "Patch Python"), nicht mehr funktionieren, frage ich mich unwillkürlich: Wie kann man Python eine funktionierende Sandbox-Umgebung zur Verfügung stellen?

Hier habe ich weitere Umsetzungsmethoden oder Fallbeispiele gesammelt, die zur Referenz und Nachschlage dienen:

* [PyPy](https://doc.pypy.org/en/latest/sandbox.html)Es gibt einen [Zweig](https://foss.heptapod.net/pypy/pypy/-/tree/branch/sandbox-2)Bietet die Funktion eines Sandkastens in Verbindung mit der zusätzlichen [sandboxlib](https://foss.heptapod.net/pypy/sandboxlib)Man kann eine Version von PyPy mit einer Sandbox-Umgebung selbst kompilieren. Wenn Sie interessiert sind, können Sie versuchen, es selbst zu konfigurieren, indem Sie sich auf einige [Erklärungen](https://foss.heptapod.net/pypy/pypy/-/issues/3192)PyPy implementiert die Funktionsweise, indem es einen Unterprozess erstellt, in dem alle Ein- und Ausgaben sowie Systemaufrufe des Unterprozesses auf einen externen Prozess umgeleitet werden, der die Berechtigungen kontrolliert. Es ist auch möglich, den Speicher und die CPU-Nutzung zu kontrollieren. Beachten Sie bitte, dass dieser Zweig seit einiger Zeit keine neuen Einreichungen mehr erhalten hat. Benutzen Sie ihn daher vorsichtig.

* Nutzung der von dem Betriebssystem bereitgestellten Sandbox-Umgebungstools. [seccomp](https://en.wikipedia.org/wiki/Seccomp)Es handelt sich um ein Sicherheitswerkzeug, das vom Linux-Kernel bereitgestellt wird, [libseccomp](https://github.com/seccomp/libseccomp/tree/main/src/python)Es werden Python-Bindungen bereitgestellt, die in den Code eingebettet und verwendet werden können. Alternativ kann auch ein Tool verwendet werden, das auf seccomp basiert, um den Code auszuführen, zum Beispiel [Firejail](https://firejail.wordpress.com/)。[AppArmor](https://apparmor.net/)Es handelt sich um ein Sicherheitsmodul des Linux-Kernels, das es Administratoren ermöglicht, den Zugriff von Programmen auf Systemressourcen und -funktionen zu kontrollieren, um das Betriebssystem zu schützen. [codejail](https://github.com/openedx/codejail)Es handelt sich um eine auf AppArmor basierende Python-Sandbox-Umgebung, die Sie gerne ausprobieren können. Es gibt viele ähnliche Tools, die ich hier nicht einzeln auflisten werde.

Verwenden Sie Sandbox-Virtualisierungsumgebungen oder Container. [Windows Sandbox](https://learn.microsoft.com/zh-cn/windows/security/threat-protection/windows-sandbox/windows-sandbox-overview)，[LXC](https://linuxcontainers.org/), [Docker](https://www.docker.com/)Warten Sie, ich werde hier nicht weiter ins Detail gehen.

##Zusammenfassung

Dieser Text ist etwas lang, danke, dass Sie bis hierher gelesen haben. Ich glaube, dass alle Fragen, die am Anfang des Artikels aufgeführt wurden, nun beantwortet wurden.

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt. Bitte im [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Auf etwaige Auslassungen hinweisen. 
