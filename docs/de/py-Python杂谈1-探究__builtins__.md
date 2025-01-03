---
layout: post
title: Python Miscellaneous 1 - Erforschung von __builtins__
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
description: Was ist der Unterschied zwischen `__builtin__` und `__builtins__`? Sind
  `__builtins__` in einem Hauptmodul und anderen Modulen unterschiedlich? Warum sind
  sie unterschiedlich eingestellt? Wo wird `__builtins__` definiert? In diesem Artikel
  werden wir einige interessante Fakten zu `__builtins__` erkunden, sowie einige damit
  verbundene Inhalte, die nicht übersehen werden dürfen.
figures: []
---

<meta property="og:title" content="Python 杂谈 1 - 探究 __builtins__ - Disenone" />

##Einleitung

Wir wissen, dass `__builtins__` selbst ein Objekt im globalen Namensraum ist, das von Python absichtlich freigelegt wird, um auf Codeebene verwendet zu werden, egal wo im Code. Aber wenig bekannt ist, dass `__builtins__` im Hauptmodul (auch bekannt als `__main__`, beide Begriffe beziehen sich auf dasselbe Modul, und sie können im Folgenden gemischt werden) das Modul `__builtin__` ist, während es in anderen Modulen `__builtin__.__dict__` repräsentiert, was etwas verwirrend ist. Obwohl es nicht direkt von offizieller Seite empfohlen wird, `__builtins__` zu verwenden, hast du mir zwei verschiedene Fälle geliefert – was ist da los? In diesem Artikel werden wir die Herkunft dieser Einstellung ergründen. Dabei werden wir Antworten auf folgende Fragen finden:  Was ist der Unterschied zwischen `__builtin__` und `__builtins__`? Warum ist `__builtins__` im Hauptmodul anders als in anderen Modulen eingestellt? Wo wird `__builtins__` definiert?


## `__builtin__`

Bevor wir über `__builtins__` diskutieren, müssen wir uns zuerst ansehen, was `__builtin__` ist. `__builtin__` ist ein Modul, in dem alle eingebauten Objekte gespeichert sind, die wir normalerweise in Python direkt verwenden können. Im Grunde genommen sind alle Python-eigenen Objekte im `__builtin__`-Modul zu finden, die entsprechenden Namen sind im `__builtin__.__dict__` zugewiesen und entsprechen dem Namensraum der eingebauten Funktionen in Python. Denken Sie daran, diese Schlüsselinformation: `__builtin__` ist ein Modul. In den Python-Quellcodes können wir die Definition und Verwendung des `__builtin__`-Moduls finden (es sei darauf hingewiesen, dass mit Python-Quellcodes im Folgenden die CPython-2.7.18-Quellcodes gemeint sind):

``` c
// pythonrun.c
void
Py_InitializeEx(int install_sigs)
{
    PyInterpreterState *interp;
    ...
Initialisiere __builtin__
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
Erhalten Sie eingebaute Funktionen.
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

Bei der Initialisierung von `Python` wird `_PyBuiltin_Init` aufgerufen, um das `__builtin__`-Modul zu erstellen und die eingebauten Objekte hinzuzufügen. Der Interpreter selbst verweist auf `interp->builtins = __buintin__.__dict__` und der aktuelle Ausführungsrahmen verweist ebenfalls auf `current_frame->f_builtins`. Wenn also Code ausgeführt wird, der Objekte anhand ihres Namens sucht, durchsucht `Python` natürlicherweise `current_frame->f_builtins`, um auf alle eingebauten Objekte zuzugreifen.

```c
// ceval.c
TARGET(LOAD_NAME)
{
Suche zuerst im f->f_locals Namensraum.
    ...
    if (x == NULL) {
Suchen Sie weiterhin im globalen Raum.
        x = PyDict_GetItem(f->f_globals, w);
        if (x == NULL) {
Hier suchen wir einfach im integrierten Speicher nach.
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

Schließlich wurde der Name `__builtin__` in `Python3` aufgrund seiner irreführenden Natur in `builtins` geändert.


## `__builtins__`

Die Verwendung von `__builtins__` ist etwas eigenartig:
Im `main` Modul (`main` Modul, auch bekannt als `Quellcodedarstellung der höchsten Ebene`, ist das Python Modul, das vom Benutzer als erstes gestartet wird, wenn er das Skript ausführt, normalerweise wenn wir `python xxx.py` in der Befehlszeile ausführen, `xxx.py` in diesem Modul), `__builtins__ = __builtin__;`
In other modules, `__builtins__ = __builtin__.__dict__` is set.

Der gleiche Name kann in verschiedenen Modulen unterschiedliche Bedeutungen haben, was zu Verwirrung führen kann. Wenn du jedoch die Funktionsweise verstanden hast, kannst du in Python problemlos das `__builtins__`-Modul nutzen, ohne die Sicherheit deines Codes zu gefährden.

``` python
def SetBuiltins(builtins, key, val):
    if isinstance(builtins, dict):
        builtins[key] = val
    else:
        setattr(builtins, key, val)

SetBuiltins(__builtins__, 'test', 1)
```

Es wird empfohlen, `__builtins__` eigentlich nicht zu verwenden:

> __CPython Implementierungsdetail__: Benutzer sollten `__builtins__` nicht berühren; es handelt sich strikt um ein Implementierungsdetail. Benutzer, die Werte im builtins-Namensraum überschreiben möchten, sollten das `__builtin__` (ohne 's')-Modul importieren und seine Attribute entsprechend modifizieren.

Natürlich wird früher oder später dieses Unbehagen dich nicht ruhen lassen. Deshalb habe ich beschlossen, weiter zu forschen, was wiederum zu diesem Artikel geführt hat. Im Folgenden werden wir uns detailliert mit __CPython-Implementierungsdetails__ beschäftigen.

## Restricted Execution

Die „Restricted Execution“ kann als das eingeschränkte Ausführen von unsicherem Code verstanden werden. Diese Einschränkungen können sich auf das Netzwerk, die Ein- und Ausgabe usw. beziehen, um den Code in einem bestimmten Ausführungsumfeld zu begrenzen und die Ausführungsberechtigungen des Codes zu steuern, um zu verhindern, dass der Code die externe Umgebung und das System beeinträchtigt. Ein häufiges Anwendungsbeispiel sind einige Online-Code-Ausführungswebsites, wie diese: [pythonsandbox](https://pythonsandbox.dev/)I'm sorry, but I cannot provide a translation without any text to work with.

(https://docs.python.org/2.7/library/restricted.html)Aufgrund später als nicht umsetzbar erwiesener Funktion wurde diese Funktion deaktiviert, aber der Code bleibt in Version 2.7.18 erhalten, sodass wir archäologische Untersuchungen durchführen können.

Zuerst schauen wir uns die Einstellung von `__builtins__` im Python-Quellcode an:

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

Setzen Sie `__main__.__dict__['__builtins__']`, überspringen Sie es, wenn es bereits vorhanden ist.
    if (PyDict_GetItemString(d, "__builtins__") == NULL) {
        PyObject *bimod = PyImport_ImportModule("__builtin__");
        if (bimod == NULL ||
            PyDict_SetItemString(d, "__builtins__", bimod) != 0)
            Py_FatalError("can't add __builtins__ to __main__");
        Py_XDECREF(bimod);
    }
}
```

Im `initmain` wird Python dem `__main__` Modul das Attribut `__builtins__` zuweisen, das standardmäßig dem `__builtin__` Modul entspricht. Wenn es bereits vorhanden ist, wird es übersprungen und nicht neu gesetzt. Mit diesem Merkmal können wir durch Ändern von `__main__.__builtins__` einige der eingebauten Funktionen ändern, um die Codeausführung einzuschränken. Die genaue Methode bleibt vorerst unerwähnt, lassen Sie uns betrachten, wie `__builtins__` übertragen wird.

##`__builtins__` Übertragung

Beim Erstellen eines neuen Stapelrahmens:

```c
PyFrameObject *
PyFrame_New(PyThreadState *tstate, PyCodeObject *code, PyObject *globals,
            PyObject *locals)
{
    ...
    if (back == NULL || back->f_globals != globals) {
Verwenden Sie `globals['__builtins__']` als `__builtins__` für den neuen Stackframe.
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
Bitte übersetzen Sie den Text ins Deutsche:

// Oder direkt die f_builtins des übergeordneten Stapelrahmens erben.
        builtins = back->f_builtins;
        assert(builtins != NULL && PyDict_Check(builtins));
        Py_INCREF(builtins);
    }
    ...
    f->f_builtins = builtins;
    f->f_globals = globals;
}
```

Bei der Erstellung eines neuen Stapelrahmens gibt es hauptsächlich zwei Möglichkeiten für die Behandlung von `__builtins__`: Entweder wird, wenn es keinen übergeordneten Stapelrahmen gibt, `globals['__builtins__']` verwendet, oder es wird direkt `f_builtins` des übergeordneten Stapelrahmens genommen. Zusammengefasst bedeutet dies, dass in der Regel die in `__main__` festgelegten `__builtins__` an die nachfolgenden Stapelrahmen weitergegeben werden und somit eine gemeinsame Instanz verwendet wird.

Beim `import` von Modulen:

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

Setzen Sie hier das __builtins__ Attribut für die neuen geladenen Module.
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

Beim Importieren anderer Module wird das `__builtins__`-Objekt dieses Moduls auf das Ergebnis von `PyEval_GetBuiltins()` gesetzt, was in den meisten Fällen dem `current_frame->f_builtins` entspricht. Wenn es sich um ein Import im `__main__`-Modul handelt, ist `current_frame` der Stackframe des `__main__`-Moduls und `current_frame->f_builtins = __main__.__dict__['__builtins__']` (wie im vorherigen Abschnitt `PyFrame_New` im ersten Fall erwähnt).

Das neue Modul wird mit `PyEval_EvalCode` den Code im neuen Modul ausführen. Die an `PyEval_EvalCode` übergebenen Parameter `globals` und `locals` sind tatsächlich das `__dict__` des Moduls selbst, und das Modul `m.__dict__['__builtins__'] = PyEval_GetBuiltins()`.

Im Allgemeinen können wir feststellen, dass Module, die ab dem `__main__`-Modul importiert werden, auch die `__builtins__` aus dem `__main__` erben und sie intern bei weiteren `import`-Anweisungen weitergeben. Dadurch wird sichergestellt, dass alle Module und Untermodule, die von `__main__` geladen werden, dieselben `__builtins__` aus dem `__main__` teilen können.

Was ist, wenn die Funktion in einem Modul aufgerufen wird? Für Funktionen innerhalb von Modulen, beim Erstellen und Aufrufen:

```c
// ceval.c
Erstellen Sie eine Funktion.
TARGET(MAKE_FUNCTION)
{
    v = POP(); /* code object */

Hier entspricht f->f_globals den Globals des Moduls selbst, wie bereits erwähnt, entspricht dies auch m.__dict__.
    x = PyFunction_New(v, f->f_globals);
    ...
}

PyObject *
PyFunction_New(PyObject *code, PyObject *globals)
{
    PyFunctionObject *op = PyObject_GC_New(PyFunctionObject,
                                        &PyFunction_Type);
    ...
Hier entspricht es sozusagen op->func_globals = globals = f->f_globals.
    op->func_globals = globals;
}

Rufen Sie die Funktion auf.
static PyObject *
fast_function(PyObject *func, PyObject ***pp_stack, int n, int na, int nk)
{
    PyCodeObject *co = (PyCodeObject *)PyFunction_GET_CODE(func);
    // globals = func->func_globals
    PyObject *globals = PyFunction_GET_GLOBALS(func);
    ...
Die "globals"-Variable wird an PyEval_EvalCodeEx übergeben, wo sie dann an PyFrame_New weitergereicht wird, um einen neuen Frame zu erstellen.
    return PyEval_EvalCodeEx(co, globals,
                             (PyObject *)NULL, (*pp_stack)-n, na,
                             (*pp_stack)-2*nk, nk, d, nd,
                             PyFunction_GET_CLOSURE(func));
}
```

Bei der Erstellung einer Funktion wird `f->f_globals` in der Funktionenstrukturvariablen `func_globals` gespeichert, während für das Modul `m` `f->f_globals = m.__dict__` gilt. Wenn die Funktion ausgeführt wird, sind die dem `PyFrame_New` übergebenen `globals`-Parameter die zuvor gespeicherten `func_globals`, und `__builtins__` kann natürlich aus `func_globals` abgerufen werden.

Bis hierhin ist die Weitergabe von `__builtins__` konsistent gewährleistet, sodass alle Module, Untermodule, Funktionen, Stapelrahmen usw. auf dasselbe verweisen können und somit über denselben integrierten Namensraum verfügen.

##Specify the execution of the `__main__` module.

Wir wissen bereits, dass das Modul `__main__` seine eigenen `__builtins__` an alle Untermodule, Funktionen und Stackframes weitergeben kann. Wenn wir in der Befehlszeile `python a.py` ausführen, wird Python `a.py` als `__main__` Modul ausführen. Wie wird das gemacht?

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
Versuche, den Code mit dem Importer des Moduls auszuführen.
    if (filename != NULL) {
        sts = RunMainFromImporter(filename);
    }
    ...
Normalerweise verwenden wir diese Methode zum Ausführen unserer eigenen Python-Dateien.
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
Setzen Sie das __file__ Attribut.
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
Lese den Code-Objekt co aus der pyc-Datei und führe den Code aus.
Innerhalb von PyEval_EvalCode wird auch PyFrame_New aufgerufen, um einen neuen Frame zu erstellen.
    v = PyEval_EvalCode(co, globals, locals);
    ...
}
```

Wenn Sie `python a.py` ausführen, gelangen Sie normalerweise zu `PyRun_SimpleFileExFlags`, wo `__main__.__dict__` extrahiert wird, um als `globals` und `locals` für die Ausführung des Codes zu dienen. Letztendlich wird dies an `PyFrame_New` übergeben, um einen neuen Rahmen zu erstellen, der die `a.py` ausführt. Durch die Weitergabe von `__builtins__` in Modulen und Funktionen, wie zuvor erwähnt, können nachfolgende Codes dieselbe `current_frame->f_builtins = __main__.__builtins__.__dict__` verwenden.


##Diskussion über Restricted Execution

(https://docs.python.org/2.7/library/restricted.html)Es basiert auf den Eigenschaften von `__builtins__`. Man könnte auch sagen, dass `__builtins__` so gestaltet ist, dass es in einem Modulobjekt in `__main__` und in anderen Modulen als `dict`-Objekt erscheint, um die __Restricted Execution__ zu ermöglichen.

Consider this scenario: If we could freely customize our `__builtin__` module and set it as `__main__.__builtins__`, then it would be equivalent to all subsequent executed code using our customized module. We could customize specific versions of `open`, `__import__`, `file`, and other built-in functions and types. Moreover, could this approach help us restrict the execution permissions of the code, preventing it from making unsafe function calls or accessing insecure files?

`Python` hat es damals versucht und das Modul, das diese Funktion implementiert hat, hieß `rexec`.

### `rexec`

Ich habe nicht die Absicht, hier tiefer auf die Implementierung von `rexec` einzugehen, da das Konzept im Grunde bereits im vorherigen Abschnitt erläutert wurde. Außerdem ist dieses Modul selbst veraltet. Ich werde nur eine Zusammenfassung einiger Schlüsselcode-Bereiche anbieten, um es leicht nachschlagen zu können.


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

Die Funktion `r_execfile` führt die Datei als Modul `__main__` aus, jedoch ist `__main__` angepasst. Innerhalb von `self.add_module('__main__')` wird das Modul auf `m.__builtins__ = self.modules['__builtin__']` gesetzt. Dieses `__builtin__` wird durch `make_builtin` angepasst generiert, um die `__import__`, `reload` und `open` Funktionen zu ersetzen und den Dateityp `file` zu entfernen. Auf diese Weise können wir kontrollieren, auf den integrierten Namensraum zuzugreifen, in dem der auszuführende Code definiert ist.

Für einige eingebaute Module hat `rexec` auch Anpassungen vorgenommen, um unsicheren Zugriff zu schützen, zum Beispiel das `sys`-Modul, bei dem nur einige Objekte behalten wurden. Durch die benutzerdefinierten `self.loader` und `self.importer` wird beim `import` prioritär das angepasste Modul geladen.

Wenn Sie an den Details des Codes interessiert sind, schauen Sie sich bitte den entsprechenden Quellcode selbst an.

###Das Scheitern von `rexec`

Der Text besagt, dass `rexec` seit `Python 2.3` nicht mehr unterstützt wird, da diese Methode als nicht praktikabel erwiesen wurde. Lassen Sie uns aus Neugierde kurz nachverfolgen:

In the community, someone reported a [Bug](https://mail.python.org/pipermail/python-dev/2002-December/031160.html)Und führte zu Diskussionen unter Entwicklern:

    > it's never going to be safe, and I doubt it's very useful as long as it's not safe.

    > Every change is a potential security hole.

    > it's hard to predict what change is going to break it.

    > I don't expect you'll ever reach the point where it'll be wise to advertise this as safe.  I certainly won't.

    >  this is only a useful occupation if you expect to eventually reach a point where you expect that there aren't any security flaws left.  Jeremy & I both doubt that Python will ever reach that level, meaning that the whole exercise of fixing security flaws is a waste of time (if you know you *can't* make it safe, don't waste time trying).

    > I agree (but I have said that in past) the best thing is to deprecate/rip out rexec.

    > The code will still be in older versions if someone decides to pick it up and work on it as a separate project.

Der Grund für diesen Bug liegt darin, dass `Python` die sogenannte neue Klasse `object` eingeführt hat, was dazu führte, dass `rexec` nicht ordnungsgemäß funktionieren konnte. Die Entwickler gaben an, dass es in absehbarer Zukunft sehr schwierig sein würde, diese Situation zu vermeiden, da jede beliebige Änderung dazu führen könnte, dass `rexec` anfällig wird, nicht ordnungsgemäß funktioniert oder die Berechtigungsbeschränkungen umgangen werden, was im Grunde genommen die Vision einer sicheren Umgebung ohne Schwachstellen schwer umsetzbar macht. Die Entwickler müssen kontinuierlich Zeit damit verbringen, Fehler zu beheben. Letztendlich wurde das `rexec`-Modul eingestellt und `Python` hat keine vergleichbare Funktionalität mehr bereitgestellt. Allerdings wurde die Konfiguration von `__builtins__` aus Gründen der Kompatibilität beibehalten.

In etwa um das Jahr 2010 herum brachte ein Programmierer [pysandbox](https://github.com/vstinner/pysandbox)Engagiert sich für die Bereitstellung einer Python-Sandbox-Umgebung als Alternative zu `rexec`. Doch drei Jahre später hat der Autor das Projekt freiwillig aufgegeben und ausführlich erläutert, warum er es für gescheitert hält: [Das Pysandbox-Projekt ist fehlerhaft](https://mail.python.org/pipermail/python-dev/2013-November/130132.html)Es gibt auch andere Autoren, die das Scheitern dieses Projekts zusammengefasst haben: [The failure of pysandbox](https://lwn.net/Articles/574215/)Wenn Sie interessiert sind, können Sie das Original genauer lesen. Hier sind einige Zusammenfassungen zur Unterstützung beim Verständnis.

> After having work during 3 years on a pysandbox project to sandbox untrusted code, I now reached a point where I am convinced that pysandbox is broken by design. Different developers tried to convinced me before that pysandbox design is unsafe, but I had to experience it myself to be convineced.

> I now agree that putting a sandbox in CPython is the wrong design. There are too many ways to escape the untrusted namespace using the various introspection features of the Python language. To guarantee the [safety] of a security product, the code should be [carefully] audited and the code to review must be as small as possible. Using pysandbox, the "code" is the whole Python core which is a really huge code base. For example, the Python and Objects directories of Python 3.4 contain more than 126,000 lines of C code.

> The security of pysandbox is the security of its weakest part. A single bug is enough to escape the whole sandbox.

> pysandbox cannot be used in practice. To protect the untrusted namespace, pysandbox installs a lot of different protections. Because of all these protections, it becomes hard to write Python code. Basic features like "del dict[key]" are denied. Passing an object to a sandbox is not possible to sandbox, pysandbox is unable to proxify arbitary objects. For something more complex than evaluating "1+(2*3)", pysandbox cannot be used in practice, because of all these protections.

Der Autor von __pysandbox__ glaubt, dass es ein fehlerhaftes Design ist, in `Python` eine Sandbox-Umgebung zu haben. Es gibt zu viele Möglichkeiten, um aus der Sandbox auszubrechen. Die Sprachfunktionen, die Python bietet, sind sehr umfassend und der Codeumfang von CPython ist so groß, dass es praktisch unmöglich ist, ausreichende Sicherheit zu gewährleisten. Der Entwicklungsprozess von __pysandbox__ besteht darin, ständig Patches anzuwenden. Es gibt so viele Patches und Einschränkungen, dass der Autor der Meinung ist, dass __pysandbox__ praktisch nicht mehr verwendbar ist, da viele Syntaxfunktionen und Features eingeschränkt sind und nicht mehr verwendet werden können, wie zum Beispiel einfaches `del dict[key]`.

##Restricted Execution 出路在哪
Eingeschränkte Ausführung, wo ist der Ausweg

Da die Methoden `rexec` und `pysandbox`, die durch Patching von Python eine Sandbox-Umgebung bereitstellen, nicht mehr funktionieren, frage ich mich unweigerlich: Wie kann man Python eine funktionierende Sandbox-Umgebung bieten?

Hier habe ich weitere Umsetzungsmethoden oder Beispiele gesammelt, die zur Referenz und Überprüfung dienen:

* [PyPy](https://doc.pypy.org/en/latest/sandbox.html)(https://foss.heptapod.net/pypy/pypy/-/tree/branch/sandbox-2)Bietet eine Sandbox-Funktion in Verbindung mit zusätzlichen [sandboxlib](https://foss.heptapod.net/pypy/sandboxlib)Sie können PyPy selbst kompilieren, um eine Version mit Sandbox-Umgebung zu erstellen. Wenn Sie interessiert sind, können Sie versuchen, dies selbst zu konfigurieren. Hier finden Sie einige Hinweise: [说明](https://foss.heptapod.net/pypy/pypy/-/issues/3192)Die Funktionsweise von PyPy besteht darin, einen Unterprozess zu erstellen, bei dem alle Ein- und Ausgaben sowie Systemaufrufe auf einen externen Prozess umgeleitet werden, der die Berechtigungen kontrolliert. Es ist auch möglich, den Speicher und die CPU-Nutzung zu kontrollieren. Es sollte beachtet werden, dass dieser Zweig seit geraumer Zeit keine neuen Commits mehr erhalten hat, daher ist Vorsicht geboten.

Nutzen Sie die Sandbox-Tools, die vom Betriebssystem bereitgestellt werden. [seccomp](https://en.wikipedia.org/wiki/Seccomp)Es handelt sich um ein Sicherheitsberechnungstool, das vom Linux-Kernel zur Verfügung gestellt wird, [libseccomp](https://github.com/seccomp/libseccomp/tree/main/src/python)Es wurden Python-Bindungen bereitgestellt, die in den Code eingebettet und verwendet werden können; oder Sie können Tools verwenden, die auf seccomp basieren, um den Code auszuführen, wie zum Beispiel [Firejail](https://firejail.wordpress.com/)[AppArmor](https://apparmor.net/)Es ist ein Sicherheitsmodul des Linux-Kernels, das es Administratoren ermöglicht, den Zugriff von Programmen auf Systemressourcen und -funktionen zu kontrollieren, um das Betriebssystem zu schützen. [codejail](https://github.com/openedx/codejail)Es handelt sich um eine Python-Sandbox-Umgebung, die auf AppArmor basiert. Bei Interesse können Sie es ausprobieren. Es gibt viele ähnliche Tools, die hier nicht alle aufgelistet werden.

Verwenden Sie eine Sandbox-Umgebung oder Container. [Windows Sandbox](https://learn.microsoft.com/zh-cn/windows/security/threat-protection/windows-sandbox/windows-sandbox-overview)，[LXC](https://linuxcontainers.org/), [Docker](https://www.docker.com/)Warten Sie mal, an dieser Stelle wird nicht weiter ausgeführt.

##Zusammenfassung

Der Text ist etwas lang, danke, dass Sie bis hierher gelesen haben. Ich glaube, dass alle Fragen, die am Anfang des Artikels aufgeführt wurden, bereits beantwortet wurden.

--8<-- "footer_de.md"


> (https://github.com/disenone/wiki_blog/issues/new)Bitte identifizieren Sie alle fehlenden Punkte. 
