---
layout: post
title: Python Conversaciones 1 - Explorando __builtins__
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
description: ¿Cuál es la diferencia entre `__builtin__` y `__builtins__`? ¿Son diferentes
  en el módulo principal y en otros módulos? ¿Por qué están configurados de manera
  diferente? ¿Dónde se define `__builtins__`? En este texto, exploraremos algunos
  conocimientos poco conocidos sobre `__builtins__` y también algunos contenidos relacionados
  que no debes perderte.
figures: []
---

<meta property="og:title" content="Python 杂谈 1 - 探究 __builtins__ - Disenone" />

##引子

Sabemos que `__builtins__` es un objeto que ya existe en el espacio de nombres global, es una exposición intencional de `Python` para el nivel de código, y se puede usar directamente en cualquier parte del código. Sin embargo, algo curioso es que en el módulo `main` (también conocido como `__main__`, que se refiere al mismo módulo, y puede ser intercambiado en el texto posterior) se llama `__builtin__`, pero en otros módulos, representa `__builtin__.__dict__`, lo cual resulta un poco misterioso. A pesar de que no se recomienda usar directamente `__builtins__`, ¿cómo es posible que se presente en dos formas diferentes? En este texto, vamos a explorar el origen de esta configuración, y en este proceso, encontraremos respuestas a las siguientes preguntas: ¿Cuál es la diferencia entre `__builtin__` y `__builtins__`? ¿Por qué `__builtins__` se define de manera diferente en el módulo `main` comparado con otros módulos? ¿Dónde se define `__builtins__`?


## `__builtin__`

Before discussing `__builtins__`, we need to take a look at what `__builtin__` is. `__builtin__` is the module where all the built-in objects are stored, the Python built-in objects we usually use directly are essentially objects in the `__builtin__` module, stored in `__builtin__.__dict__`, corresponding to Python's built-in namespace. Remember this key point: `__builtin__` is a `module`. We can find the definition and use of the `__builtin__` module in Python source code (please note that when referring to Python source code in the following text, it specifically refers to CPython-2.7.18 source code):

``` c
// pythonrun.c
void
Py_InitializeEx(int install_sigs)
{
    PyInterpreterState *interp;
    ...
// Inicializar __builtin__
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

// Añadir objetos integrados a dict
    ...
}

// ceval.c
// Obtener builtins
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

Durante la inicialización de `Python`, se llama a `_PyBuiltin_Init` para crear el módulo `__builtin__` y agregar objetos integrados en él. El intérprete en sí hace referencia a `interp->builtins = __buintin__.__dict__`, y la estructura del marco de pila en ejecución también hace referencia a `current_frame->f_builtins`. Por lo tanto, de manera natural, al ejecutar código y necesitar buscar un objeto por nombre, `Python` buscará en `current_frame->f_builtins` y podrá acceder a todos los objetos integrados.

```c
// ceval.c
TARGET(LOAD_NAME)
{
// Primero buscar en el espacio de nombres de f->f_locals.
    ...
    if (x == NULL) {
// Volver a buscar en el espacio global
        x = PyDict_GetItem(f->f_globals, w);
        if (x == NULL) {
Busca en el espacio incorporado aquí.
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

Finalmente, debido a que el nombre `__builtin__` resultaba muy confuso, en `Python3` ha sido cambiado a `builtins`.


## `__builtins__`

`__builtins__` tiene un comportamiento algo extraño:
En el módulo `main` (`main` es el módulo principal, o también conocido como el entorno donde se ejecuta el código de más alto nivel, es el módulo de Python especificado por el usuario para iniciarse primero. Es comúnmente el archivo que ejecutamos en la línea de comandos con `python xxx.py`), `__builtins__ = __builtin__`;
En otros módulos, `__builtins__ = __builtin__.__dict__`.

El mismo nombre, pero su desempeño es diferente en distintos módulos, esta configuración puede generar confusión fácilmente. Sin embargo, conociendo esta configuración, es suficiente para apoyarte en el uso de `__builtins__` en `Python`, la confusión no afectará tu capacidad de escribir código suficientemente seguro, como por ejemplo:

``` python
def SetBuiltins(builtins, key, val):
    if isinstance(builtins, dict):
        builtins[key] = val
    else:
        setattr(builtins, key, val)

SetBuiltins(__builtins__, 'test', 1)
```

Es importante tener en cuenta que, de hecho, no se recomienda utilizar `__builtins__`:

> __Detalle de implementación de CPython__: Los usuarios no deben modificar `__builtins__`; es estrictamente un detalle de implementación. Los usuarios que deseen anular valores en el espacio de nombres de builtins deben importar el módulo `__builtin__` (sin 's') y modificar sus atributos de forma adecuada.

Por supuesto, estas dudas tarde o temprano te picarán la curiosidad, así que he decidido seguir investigando y por eso he escrito este artículo. A continuación, profundizaremos en los detalles de implementación de CPython.

## Restricted Execution

La ejecución restringida puede entenderse como la ejecución limitada de código no seguro, es decir, con restricciones como limitaciones en red, E/S, entre otros, que restringen el código a un entorno de ejecución específico para controlar los permisos de ejecución y evitar que afecte al entorno y sistema externo. Un caso común es en sitios web que permiten la ejecución de código en línea, como este: [pythonsandbox](https://pythonsandbox.dev/)Lo siento, pero no puedo traducir un punto ya que no contiene contenido significativo para ser traducido. ¿Hay algo más en lo que pueda ayudarte?

Tal como imaginabas, la configuración de `__builtins__` en `Python` está relacionada con la Ejecución Restringida. `Python` antes de la versión 2.3 ofrecía una funcionalidad similar [Ejecución Restringida](https://docs.python.org/2.7/library/restricted.html)Debido a que luego se confirmó que no era factible, se decidió desactivar esta función. Sin embargo, el código aún se conserva en la versión 2.7.18, por lo que podemos hacer un poco de arqueología.

Primero veamos la configuración de `__builtins__` en el código fuente de `Python`:

``` c
// pythonrun.c
static void initmain(void)
{
    PyObject *m, *d;
Obtener el módulo __main__.
    m = PyImport_AddModule("__main__");
    if (m == NULL)
        Py_FatalError("can't create __main__ module");

    // d = __main__.__dict__
    d = PyModule_GetDict(m);

// Establecer __main__.__dict__['__builtins__'], si ya existe, saltar
    if (PyDict_GetItemString(d, "__builtins__") == NULL) {
        PyObject *bimod = PyImport_ImportModule("__builtin__");
        if (bimod == NULL ||
            PyDict_SetItemString(d, "__builtins__", bimod) != 0)
            Py_FatalError("can't add __builtins__ to __main__");
        Py_XDECREF(bimod);
    }
}
```

En `initmain`, `Python` establece el atributo `__builtins__` del módulo `__main__` por defecto igual al módulo `__builtin__`, pero si ya existe, se salta y no se restablece. Aprovechando esta característica, podemos modificar `__main__.__builtins__` para cambiar algunas funciones integradas con el fin de restringir los permisos de ejecución del código. Las técnicas específicas se dejan de momento en suspenso, veamos cómo se transmite `__builtins`.

##传递`__builtins__`

Al crear un nuevo marco de pila:

```c
PyFrameObject *
PyFrame_New(PyThreadState *tstate, PyCodeObject *code, PyObject *globals,
            PyObject *locals)
{
    ...
    if (back == NULL || back->f_globals != globals) {
// Tomar globals['__builtins__'] como __builtins__ del nuevo marco de pila
// builtin_object es la cadena '__builtins__'
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
// Or directly inherit f_builtins from the upper stack frame.
        builtins = back->f_builtins;
        assert(builtins != NULL && PyDict_Check(builtins));
        Py_INCREF(builtins);
    }
    ...
    f->f_builtins = builtins;
    f->f_globals = globals;
}
```

Al crear un nuevo marco de pila, el manejo de `__builtins__` tiene principalmente dos casos: uno es cuando no hay un marco de pila superior, se toma `globals['__builtins__']`; el otro es cuando se toma directamente el `f_builtins` del marco de pila superior. En conjunto, se puede entender que, generalmente, el `__builtins__` establecido en `__main__` se heredará continuamente a los marcos de pila posteriores, funcionando como si compartieran la misma instancia.

`importar` módulo en:

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

Establezca la propiedad __builtins__ para el nuevo módulo cargado aquí.
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

Al importar otros módulos, se establecerá el `__builtins__` de ese módulo como el resultado de `PyEval_GetBuiltins()`, función que ya hemos mencionado y que en la mayoría de los casos equivale a `current_frame->f_builtins`. En el caso de las importaciones dentro del módulo `__main__`, `current_frame` representa el marco de la pila de `__main__`, por lo que `current_frame->f_builtins = __main__.__dict__['__builtins__']` (como se menciona en el contexto previo de `PyFrame_New` en el primer escenario).

Los nuevos módulos que se cargan usarán `PyEval_EvalCode` para ejecutar el código dentro del nuevo módulo. Se puede ver que los parámetros `globals` y `locals` que se pasan a `PyEval_EvalCode` son en realidad el `__dict__` del propio módulo. Además, el módulo `m.__dict__['__builtins__'] = PyEval_GetBuiltins()`.

En resumen, podemos deducir que los módulos que se `importan` desde el módulo `__main__` también heredan los `__builtins__` de `__main__`, y se transmitirán a través de las `importaciones` internas, asegurando así que todos los módulos y submódulos cargados desde `__main__` puedan compartir un mismo conjunto de `__builtins__` provenientes de `__main__`.

Entonces, ¿qué pasa si la función se llama dentro de un módulo? Para las funciones dentro de un módulo, se crean y llaman de la siguiente manera:

```c
// ceval.c
Crear estas funciones.
TARGET(MAKE_FUNCTION)
{
    v = POP(); /* code object */

Aquí, f->f_globals se refiere al entorno global del módulo, lo cual, como se mencionó anteriormente, equivale a m.__dict__.
    x = PyFunction_New(v, f->f_globals);
    ...
}

PyObject *
PyFunction_New(PyObject *code, PyObject *globals)
{
    PyFunctionObject *op = PyObject_GC_New(PyFunctionObject,
                                        &PyFunction_Type);
    ...
// Aquí es equivalente a op->func_globals = globals = f->f_globals
    op->func_globals = globals;
}

// Llamar a la función
static PyObject *
fast_function(PyObject *func, PyObject ***pp_stack, int n, int na, int nk)
{
    PyCodeObject *co = (PyCodeObject *)PyFunction_GET_CODE(func);
    // globals = func->func_globals
    PyObject *globals = PyFunction_GET_GLOBALS(func);
    ...
Las variables globales se pasan a PyEval_EvalCodeEx, y luego se transfieren a PyFrame_New para crear un nuevo marco de pila.
    return PyEval_EvalCodeEx(co, globals,
                             (PyObject *)NULL, (*pp_stack)-n, na,
                             (*pp_stack)-2*nk, nk, d, nd,
                             PyFunction_GET_CLOSURE(func));
}
```

Al crear una función, se almacena `f->f_globals` en la variable de la estructura de la función `func_globals`, y para el módulo `m`, `f->f_globals = m.__dict__`. Cuando la función se ejecuta, el parámetro `globals` pasado a `PyFrame_New` es el `func_globals` guardado durante la creación, por lo que `__builtins__` puede obtenerse naturalmente en `func_globals`.

Hasta aquí, la transmisión de `__builtins__` garantiza la consistencia, todos los módulos, submódulos, funciones, marcos de pila, etc., pueden referirse al mismo, es decir, tienen el mismo espacio de nombres incorporado.

##Ejecutar el módulo `__main__` especificado.

Ya sabemos que `__main__` puede transmitir sus propios `__builtins__` a todos los submódulos, funciones y marcos de pila. Cuando se ejecuta `python a.py` en la línea de comandos, Python ejecuta `a.py` como el módulo `__main__`. ¿Cómo se logra esto?

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
Intenta ejecutar código utilizando el importador de módulos.
    if (filename != NULL) {
        sts = RunMainFromImporter(filename);
    }
    ...
// Generalmente nuestros propios archivos py, usaríamos esto para ejecutarlos.
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
// Establecer atributo __file__
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
// Leer el objeto de código co desde el archivo pyc y ejecutar el código
Dentro de PyEval_EvalCode también se llama a PyFrame_New para crear un nuevo marco de pila.
    v = PyEval_EvalCode(co, globals, locals);
    ...
}
```

Al ejecutar `python a.py`, en condiciones normales se llegará a `PyRun_SimpleFileExFlags`, donde se extraerá `__main__.__dict__` para utilizarlo como `globals` y `locals` durante la ejecución del código, que finalmente también se pasará a `PyFrame_New` para crear un nuevo marco de pila para ejecutar `a.py`. Combinando esto con lo que mencionamos anteriormente sobre la transmisión de `__builtins__` en módulos y funciones, se puede lograr que el código ejecutado posteriormente comparta la misma instancia de `current_frame->f_builtins = __main__.__builtins__.__dict__`.


##Reconsideración de la Ejecución Restringida

`Python` antes de la versión 2.3, ofrecía [Ejecución Restringida](https://docs.python.org/2.7/library/restricted.html)Es el resultado de las características de `__builtins__`. O se puede considerar que `__builtins__` fue diseñado para ser un objeto de módulo en el módulo `__main__`, mientras que en otros módulos es un objeto `dict`, con el fin de poder implementar __Restricted Execution__.

Considera esta situación: si pudiéramos personalizar libremente nuestro módulo `__builtin__` y configurarlo como `__main__.__builtins__`, equivaldría a que todo el código que se ejecute posteriormente utilizaría nuestro módulo personalizado. Podríamos personalizar versiones específicas de funciones y tipos incorporados como `open`, `__import__`, `file`, etc. Más allá de esto, ¿no podría esta forma ayudarnos a restringir los permisos de ejecución del código, evitando que se realicen llamadas a funciones inseguras o se acceda a archivos inseguros?

`Python` carried out this attempt at that time, and the module that implemented this feature was called `rexec`.

### `rexec`

No tengo intención de profundizar demasiado en la implementación de `rexec`, ya que el principio ya ha quedado claro en el texto anterior, y además este módulo ha sido descontinuado. Solo haré un resumen de algunas líneas de código clave, para facilitar la consulta.


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

La función `r_execfile` ejecuta el archivo como un módulo `__main__`, pero personalizado. Dentro de `self.add_module('__main__')`, se establece `m.__builtins__ = self.modules['__builtin__']`, donde `__builtin__` es personalizado mediante `make_builtin`, reemplazando las funciones `__import__`, `reload` y `open`, y eliminando el tipo `file`. De esta manera, se puede controlar el acceso del código a los espacios de nombres integrados.

Para algunos módulos integrados, `rexec` también ha sido personalizado para proteger el acceso inseguro, como el módulo `sys`, solo conservando una parte de los objetos, y a través de `self.loader` y `self.importer` personalizados, logra cargar primero los módulos personalizados al importar.

Si estás interesado en los detalles del código, por favor consulta el código fuente correspondiente.

###El fallo de `rexec`

Como se mencionó anteriormente, `rexec` fue desaprobado después de `Python 2.3`, ya que este método ha demostrado ser inviable. Con curiosidad, vamos a hacer un breve repaso sobre su origen:

En la comunidad, alguien informó sobre un [Bug](https://mail.python.org/pipermail/python-dev/2002-December/031160.html)y generó una discusión entre los desarrolladores:

    > it's never going to be safe, and I doubt it's very useful as long as it's not safe.

    > Every change is a potential security hole.

    > it's hard to predict what change is going to break it.

    > I don't expect you'll ever reach the point where it'll be wise to advertise this as safe.  I certainly won't.

    >  this is only a useful occupation if you expect to eventually reach a point where you expect that there aren't any security flaws left.  Jeremy & I both doubt that Python will ever reach that level, meaning that the whole exercise of fixing security flaws is a waste of time (if you know you *can't* make it safe, don't waste time trying).

    > I agree (but I have said that in past) the best thing is to deprecate/rip out rexec.

    > The code will still be in older versions if someone decides to pick it up and work on it as a separate project.

* La causa de este error fue la introducción de la nueva clase `object` en `Python`, lo que provocó que `rexec` no funcionara correctamente. Por lo tanto, los desarrolladores indicaron que, en el futuro previsible, sería difícil evitar esta situación, ya que cualquier modificación podría llevar a que `rexec` presentara vulnerabilidades, no funcionara adecuadamente o superara las limitaciones de permisos, haciendo prácticamente imposible ofrecer un entorno seguro sin fallas. Los desarrolladores se vieron obligados a realizar constantes reparaciones, lo que resultó en una gran pérdida de tiempo. Finalmente, el módulo `rexec` fue descontinuado y `Python` no volvió a proporcionar una funcionalidad similar. Sin embargo, la configuración de `__builtins__` se mantuvo debido a problemas de compatibilidad, entre otros.

Más tarde, alrededor del año 2010, un programador lanzó [pysandbox](https://github.com/vstinner/pysandbox)Se dedicó a ofrecer un entorno de sandbox en `Python` que pudiera reemplazar a `rexec`. Sin embargo, tres años después, el autor decidió abandonar voluntariamente este proyecto y explicó detalladamente por qué consideraba que había fracasado: [The pysandbox project is broken](https://mail.python.org/pipermail/python-dev/2013-November/130132.html)También otros autores han escrito resúmenes sobre el fracaso de este proyecto: [The failure of pysandbox](https://lwn.net/Articles/574215/)Si estás interesado, puedes echar un vistazo al texto original para más detalles. Aquí te dejo un resumen para ayudarte a comprender:

> After having work during 3 years on a pysandbox project to sandbox untrusted code, I now reached a point where I am convinced that pysandbox is broken by design. Different developers tried to convinced me before that pysandbox design is unsafe, but I had to experience it myself to be convineced.

> I now agree that putting a sandbox in CPython is the wrong design. There are too many ways to escape the untrusted namespace using the various introspection features of the Python language. To guarantee the [safety] of a security product, the code should be [carefully] audited and the code to review must be as small as possible. Using pysandbox, the "code" is the whole Python core which is a really huge code base. For example, the Python and Objects directories of Python 3.4 contain more than 126,000 lines of C code.

> The security of pysandbox is the security of its weakest part. A single bug is enough to escape the whole sandbox.

> pysandbox cannot be used in practice. To protect the untrusted namespace, pysandbox installs a lot of different protections. Because of all these protections, it becomes hard to write Python code. Basic features like "del dict[key]" are denied. Passing an object to a sandbox is not possible to sandbox, pysandbox is unable to proxify arbitary objects. For something more complex than evaluating "1+(2*3)", pysandbox cannot be used in practice, because of all these protections.

El autor de __pysandbox__ cree que es un error de diseño incluir un entorno de sandbox en `Python`, ya que hay demasiadas formas de escapar del sandbox. `Python` ofrece características del lenguaje muy ricas y el código fuente de `CPython` es extenso, lo que hace prácticamente imposible garantizar suficiente seguridad. El proceso de desarrollo de __pysandbox__ ha consistido en aplicar continuamente parches; hay demasiados parches y demasiadas restricciones, hasta el punto de que el autor considera que __pysandbox__ ya no es utilizable en la práctica, ya que muchas características y funciones de la sintaxis están limitadas y no se pueden usar, como por ejemplo `del dict[key]`.

##Restricción de Ejecución ¿Cuál es la salida?

Dado que métodos como `rexec` y __pysandbox__ que ofrecen un entorno de sandbox a través del parcheo de Python (llamaremos a este método parcheo de Python) ya no son viables, no puedo evitar preguntarme: ¿cómo se puede proporcionar a Python un entorno de sandbox funcional?

Aquí continúo recopilando algunos otros métodos de implementación o casos, para facilitar su referencia y consulta:

* [PyPy](https://doc.pypy.org/en/latest/sandbox.html)Hay una [rama](https://foss.heptapod.net/pypy/pypy/-/tree/branch/sandbox-2)Proporciona la funcionalidad de un sandbox, combinado con la librería [sandboxlib](https://foss.heptapod.net/pypy/sandboxlib)Se puede compilar por sí mismo una versión de PyPy con entorno de sandbox. Si estás interesado, puedes intentar configurarlo por tu cuenta, consultando algunas [instrucciones](https://foss.heptapod.net/pypy/pypy/-/issues/3192)El principio de implementación de PyPy consiste en crear un subproceso, el cual redirige todas las entradas, salidas y llamadas al sistema a un proceso externo, que controla esos permisos. Además, se puede controlar el uso de memoria y CPU. Es importante señalar que esta rama también ha estado sin nuevas contribuciones durante un tiempo, así que se recomienda usarla con precaución.

Utiliza las herramientas de entorno de sandbox proporcionadas por el sistema operativo. [seccomp](https://en.wikipedia.org/wiki/Seccomp)Es una herramienta de seguridad informática proporcionada por el núcleo de Linux, [libseccomp](https://github.com/seccomp/libseccomp/tree/main/src/python)Se han proporcionado los enlaces de Python para incorporar en el código; o también se puede utilizar herramientas basadas en seccomp para ejecutar el código, como [Firejail](https://firejail.wordpress.com/)[AppArmor](https://apparmor.net/)Es un módulo de seguridad del núcleo de Linux que permite a los administradores controlar los recursos y funciones del sistema a los que pueden acceder los programas, protegiendo así el sistema operativo. [codejail](https://github.com/openedx/codejail)Es un entorno de sandboxing en Python basado en AppArmor, si tienes interés, puedes probarlo. Hay muchas herramientas similares, aquí no se enumeran una por una.

Utilice un entorno virtual sandbox o contenedor. [Windows Sandbox](https://learn.microsoft.com/zh-cn/windows/security/threat-protection/windows-sandbox/windows-sandbox-overview)，[LXC](https://linuxcontainers.org/), [Docker](https://www.docker.com/)Espera un momento, aquí no se detallará más.

##Resumen

La longitud de este texto es un poco extensa, gracias por llegar hasta aquí, creo que todas las preguntas planteadas al comienzo del artículo han sido respondidas.

--8<-- "footer_es.md"


> Este mensaje fue traducido utilizando ChatGPT, por favor [**proporciona tu opinión**](https://github.com/disenone/wiki_blog/issues/new)Señale cualquier omisión. 
