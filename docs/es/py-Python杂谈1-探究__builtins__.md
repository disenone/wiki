---
layout: post
title: Python 杂谈 1 - Explorando __builtins__
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
description: ¿Cuál es la diferencia entre __builtin__ y __builtins__? ¿__builtins__
  es diferente en el módulo principal y en los demás módulos? ¿Por qué se establece
  como diferente? ¿Dónde se define __builtins__? En este artículo, exploraremos algunos
  detalles interesantes sobre __builtins__ y también algunas ideas relacionadas que
  no deben pasarse por alto.
figures: []
---

<meta property="og:title" content="Python 杂谈 1 - 探究 __builtins__ - Disenone" />

##> **Introducción

Sabemos que `__builtins__` es un objeto que ya existe en el espacio de nombres global, y se expone intencionalmente por Python para su uso en el código en cualquier parte. Sin embargo, una curiosidad interesante es que en el módulo `main` (también conocido como `__main__`, se refieren al mismo módulo, que se puede utilizar indistintamente) se refiere al módulo `__builtin__`, pero en otros módulos se refiere a `__builtin__.__dict__`, lo cual resulta un tanto confuso. Aunque no se recomienda su uso directo, ¿por qué hay dos situaciones diferentes? En este artículo vamos a explorar el origen de esta configuración y, en el proceso, encontraremos respuestas a estas preguntas: ¿Cuál es la diferencia entre `__builtin__` y `__builtins__`? ¿Por qué `__builtins__` es diferente en el módulo `main` y en otros módulos? ¿Dónde se define `__builtins__`?


## `__builtin__`

Antes de hablar sobre `__builtins__`, primero debemos ver qué es `__builtin__`. `__builtin__` es un módulo que contiene todos los objetos incorporados. Todos los objetos incorporados en Python que usamos comúnmente son, en esencia, objetos en el módulo `__builtin__`, almacenados en `__builtin__.__dict__`, correspondiendo al espacio de nombres incorporado de Python. Recuerda este punto clave: `__builtin__` es un módulo. Podemos encontrar la definición y el uso del módulo `__builtin__` en el código fuente de Python (ten en cuenta que se hace referencia al código fuente de CPython-2.7.18 en el siguiente texto):

``` c
// pythonrun.c
void
Py_InitializeEx(int install_sigs)
{
    PyInterpreterState *interp;
    ...
// Inicializando __builtin__
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

// Darle a `dict` objetos integrados
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

`Python` inicializa llamando a `_PyBuiltin_Init` para crear el módulo `__builtin__` y añadir objetos integrados en él. El intérprete se referirá a `interp->builtins = __buintin__.__dict__` para mantener una referencia a estos objetos integrados. Además, la estructura del marco de ejecución actual también mantendrá una referencia a `current_frame->f_builtins`. Por lo tanto, cuando el código requiere buscar un objeto por su nombre, `Python` buscará dentro de `current_frame->f_builtins`, permitiendo así acceder a todos los objetos integrados:

```c
// ceval.c
TARGET(LOAD_NAME)
{
// Primero busca en el espacio de nombres de f->f_locals
    ...
    if (x == NULL) {
// Buscar en el espacio global una vez más
        x = PyDict_GetItem(f->f_globals, w);
        if (x == NULL) {
// Aquí es donde buscamos en el espacio integrado
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

Finalmente, debido a que el nombre `__builtin__` es realmente confuso, se ha cambiado a `builtins` en Python 3.


## `__builtins__`

`__builtins__` es un poco extraño en su comportamiento:
En el módulo `main` (el módulo `main`, o también conocido como el entorno en el que se ejecuta el código de nivel superior), que es el módulo de Python especificado por el usuario que se ejecuta primero, cuando ejecutamos `python xxx.py` en la línea de comandos, `xxx.py` se convierte en este módulo), `__builtins__ = __builtin__`.
En otros módulos, `__builtins__ = __builtin__.__dict__`.

El mismo nombre, pero se comporta de manera diferente en diferentes módulos, esta configuración puede resultar confusa. Sin embargo, una vez que entiendas esta configuración, será suficiente para ayudarte a utilizar `__builtins__` en Python. La confusión no afectará tu capacidad para escribir un código lo suficientemente seguro, como por ejemplo:

``` python
def SetBuiltins(builtins, key, val):
    if isinstance(builtins, dict):
        builtins[key] = val
    else:
        setattr(builtins, key, val)

SetBuiltins(__builtins__, 'test', 1)
```

Necesitas tener en cuenta que en realidad no se recomienda utilizar `__builtins__`:

> __Detalles de implementación de CPython__: Los usuarios no deben modificar `__builtins__`; es estrictamente un detalle de implementación. Los usuarios que deseen reemplazar valores en el espacio de nombres de los módulos integrados deben importar el módulo `__builtin__` (sin 's') y modificar sus atributos de manera apropiada.

Por supuesto, estas dudas tarde o temprano te generarán una intriga irresistible, así que he decidido seguir investigando y por ello surge este artículo. A continuación, profundizaremos en los detalles de implementación de __CPython__.

## Restricted Execution

La "Restricted Execution" se puede entender como la ejecución restringida de código inseguro. La idea es limitar el acceso a la red, IO, y otros recursos, manteniendo así el código contenido dentro de un entorno controlado. El objetivo es evitar que el código tenga impacto en el entorno externo y en el sistema. Un caso común de uso son las páginas web que ejecutan código en línea, como esta: [pythonsandbox](https://pythonsandbox.dev/).

(https://docs.python.org/2.7/library/restricted.html)，sólo porque más tarde se confirmó que era inviable, tuvimos que eliminar esa funcionalidad, pero el código aún se mantiene en la versión 2.7.18, así que podemos hacer una especie de arqueología.

首先, echemos un vistazo a la configuración de `__builtins__` en el código fuente de `Python`:


``` c
// pythonrun.c
static void initmain(void)
{
    PyObject *m, *d;
// Obtener el módulo __main__
    m = PyImport_AddModule("__main__");
    if (m == NULL)
        Py_FatalError("can't create __main__ module");

    // d = __main__.__dict__
    d = PyModule_GetDict(m);

// Define __main__.__dict__['__builtins__'], if it already exists, skip it

// Establecer __main__.__dict__['__builtins__'], si ya existe, omitirlo
    if (PyDict_GetItemString(d, "__builtins__") == NULL) {
        PyObject *bimod = PyImport_ImportModule("__builtin__");
        if (bimod == NULL ||
            PyDict_SetItemString(d, "__builtins__", bimod) != 0)
            Py_FatalError("can't add __builtins__ to __main__");
        Py_XDECREF(bimod);
    }
}
```

En `initmain`, Python establece el atributo `__builtins__` al módulo `__main__`, que por defecto es igual al módulo `__builtin__`, pero si ya existe, no se volverá a establecer. Aprovechando esta característica, podemos modificar algunas funcionalidades integradas al modificar `__main__.__builtins__`, con el fin de limitar los permisos de ejecución de código. Por ahora, no entraremos en detalles sobre los métodos específicos, pero veremos cómo se transmite `__builtins__`.

##`__builtins__` 的传递

Al crear un nuevo marco de pila:

```c
PyFrameObject *
PyFrame_New(PyThreadState *tstate, PyCodeObject *code, PyObject *globals,
            PyObject *locals)
{
    ...
    if (back == NULL || back->f_globals != globals) {
        // Usar globals['__builtins__'] como __builtins__ para el nuevo marco de pila
// `builtin_object` es simplemente una cadena de texto '__builtins__'
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
        // O heredar directamente los f_builtins del marco de pila superior
        builtins = back->f_builtins;
        assert(builtins != NULL && PyDict_Check(builtins));
        Py_INCREF(builtins);
    }
    ...
    f->f_builtins = builtins;
    f->f_globals = globals;
}
```

Al crear un nuevo marco de pila, hay dos casos principales para manejar `__builtins__`: uno es cuando no hay un marco de pila superior, en ese caso se toma `globals['__builtins__']`; el otro caso es cuando se toma directamente `f_builtins` del marco de pila superior. En conjunto, se puede entender que, en general, `__builtins__` establecido en `__main__` se hereda a los marcos de pila siguientes, es como compartir la misma referencia.

Al importar el módulo:

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

// En este punto establece la propiedad __builtins__ del nuevo módulo cargado
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

Al importar otros módulos, el módulo importado establece su `__builtins__` como el resultado de `PyEval_GetBuiltins()`, función que hemos mencionado anteriormente, que en la mayoría de los casos es equivalente a `current_frame->f_builtins`. En el caso de las importaciones dentro del módulo `__main__`, `current_frame` se refiere al frame de pila del módulo `__main__` y `current_frame->f_builtins = __main__.__dict__['__builtins__']` (como se mencionó anteriormente en el primer caso de `PyFrame_New`).

En el caso de nuevos módulos cargados, se utilizará `PyEval_EvalCode` para ejecutar el código del nuevo módulo. Podemos observar que los argumentos `globals` y `locals` pasados a `PyEval_EvalCode` son en realidad el `__dict__` del propio módulo. Además, se establece `m.__dict__['__builtins__'] = PyEval_GetBuiltins()`.

En general, podemos afirmar que los módulos importados que comienzan con `__main__` también heredarán los `__builtins__` de `__main__` y se transmitirán internamente en las importaciones. Esto garantiza que todos los módulos y submódulos cargados desde `__main__` compartirán los mismos `__builtins__` provenientes de `__main__`.

Entonces, ¿qué sucede si estamos llamando a una función dentro de un módulo? En el caso de las funciones dentro de un módulo, al momento de su creación y llamada:

```c
// ceval.c
// Crear función
TARGET(MAKE_FUNCTION)
{
    v = POP(); /* code object */

    // Aquí, f->f_globals es equivalente a los globals del propio módulo, como se puede deducir del texto anterior, también es equivalente a m.__dict__.
    x = PyFunction_New(v, f->f_globals);
    ...
}

PyObject *
PyFunction_New(PyObject *code, PyObject *globals)
{
    PyFunctionObject *op = PyObject_GC_New(PyFunctionObject,
                                        &PyFunction_Type);
    ...
    // Aquí, esto sería equivalente a op->func_globals = globals = f->f_globals
    op->func_globals = globals;
}

// Llamar a una función
static PyObject *
fast_function(PyObject *func, PyObject ***pp_stack, int n, int na, int nk)
{
    PyCodeObject *co = (PyCodeObject *)PyFunction_GET_CODE(func);
    // globals = func->func_globals
    PyObject *globals = PyFunction_GET_GLOBALS(func);
    ...
// `globals` se pasa a `PyEval_EvalCodeEx`, y luego se pasa a `PyFrame_New` para crear un nuevo marco de pila.
    return PyEval_EvalCodeEx(co, globals,
                             (PyObject *)NULL, (*pp_stack)-n, na,
                             (*pp_stack)-2*nk, nk, d, nd,
                             PyFunction_GET_CLOSURE(func));
}
```

Al crear una función, se guarda `f->f_globals` en la variable de estructura de función `func_globals`. En el caso del módulo `m`, `f->f_globals = m.__dict__`. Cuando se ejecuta la función, el parámetro `globals` que se pasa a `PyFrame_New` es el `func_globals` almacenado anteriormente durante la creación, por lo que `__builtins__` se puede obtener naturalmente en `func_globals`.

Hasta este punto, se puede garantizar la consistencia de la propagación de `__builtins__`, todos los módulos, submódulos, funciones, marcos de pila, etc., pueden hacer referencia a lo mismo, es decir, tener el mismo espacio de nombres incorporado.

##指定 `__main__` 模块执行

Ya sabemos que el módulo `__main__` tiene acceso a `__builtins__` y puede ser pasado a todos los submódulos, funciones y marcos de pila. Cuando ejecutamos `python a.py` en la línea de comandos, Python ejecuta el archivo `a.py` como el módulo `__main__`. ¿Cómo es posible lograr esto?

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
// Intenta ejecutar el código utilizando el importador del módulo
    if (filename != NULL) {
        sts = RunMainFromImporter(filename);
    }
    ...
    // 一般我们自己的 py 文件，会使用这个来执行

    // Por lo general, usamos esto para ejecutar nuestros propios archivos py
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
// Establecer el atributo __file__
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
// Se lee el objeto de código "co" del archivo pyc y se ejecuta el código
    // Dentro de PyEval_EvalCode también se llama a PyFrame_New para crear un nuevo marco de pila.
    v = PyEval_EvalCode(co, globals, locals);
    ...
}
```

Cuando se ejecuta `python a.py`, generalmente se llega a `PyRun_SimpleFileExFlags`, dentro de `PyRun_SimpleFileExFlags` se extrae `__main__.__dict__` como `globals` y `locals` del código a ejecutar, y finalmente se pasa a `PyFrame_New` para crear un nuevo marco de pila y ejecutar `a.py`. Combinando lo mencionado anteriormente sobre la transferencia de `__builtins__` en módulos y funciones, podemos hacer que el código que se ejecuta posteriormente comparta el mismo conjunto de `current_frame->f_builtins = __main__.__builtins__.__dict__`.


##**再论 Restricted Execution**

La idea de **Restricted Execution** se basa en el concepto de limitar la ejecución de ciertos procesos o actividades. Esta estrategia consiste en establecer restricciones a fin de proteger la integridad y seguridad de un sistema. 

La implementación de **Restricted Execution** puede contribuir a prevenir posibles riesgos y vulnerabilidades que puedan comprometer la privacidad y confidencialidad de los datos. Al restringir la ejecución, se minimizan las posibilidades de que programas maliciosos o código no autorizado se ejecuten en un entorno protegido.

Existen distintas medidas que se pueden aplicar para lograr la ejecución restringida, tales como el uso de mecanismos de autorización y autenticación, la definición de políticas de acceso y el establecimiento de controles de seguridad. Estas acciones brindan una capa adicional de protección y permiten mantener la integridad del sistema.

En resumen, el uso de **Restricted Execution** es crucial para garantizar la seguridad y confiabilidad de un sistema, al limitar la ejecución de procesos no autorizados. Es importante implementar estas medidas de manera efectiva para proteger la información sensible y salvaguardar la integridad de los sistemas informáticos.

`Python` en versiones anteriores a la 2.3, solía ofrecer [Ejecución Restringida](https://docs.python.org/2.7/library/restricted.html)，se ha construido sobre la característica de `__builtins__`. O se podría decir que `__builtins__` se diseñó como un objeto de módulo en el módulo `__main__`, pero como un objeto `dict` en otros módulos, con el fin de lograr la __Ejecución Restringida__.

Consider the following situation: if we could customize our own `__builtin__` module and set it as `__main__.__builtins__`, then all the subsequent executed code would use our customized module. We could customize specific versions of built-in functions and types such as `open`, `__import__`, `file`, and so on. Moreover, could this approach help us limit the permissions of executing code, preventing it from making unsafe function calls or accessing unsafe files?

`Python` hizo ese intento en ese momento para implementar esta funcionalidad con el módulo llamado `rexec`.

### `rexec`

No tengo la intención de profundizar en la explicación de la implementación de `rexec`, ya que el principio ya se explicó claramente en el texto anterior, y además este módulo está obsoleto. Aquí simplemente presentaré un resumen de algunos fragmentos de código clave para facilitar la referencia.


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

La función `r_execfile` ejecuta el archivo como si fuera el módulo `__main__`, aunque personalizado. Dentro de `self.add_module('__main__')`, se establece `m.__builtins__ = self.modules['__builtin__']`, donde `__builtin__` es personalizado por `make_builtin` y reemplaza las funciones `__import__`, `reload` y `open`, y también elimina el tipo de dato `file`. De esta manera, tenemos control sobre el acceso del código ejecutado al espacio de nombres incorporado.

Para algunos módulos incorporados, `rexec` también ha sido personalizado para proteger los accesos inseguros, como el módulo `sys`, que solo conserva parte de los objetos y, a través de `self.loader` y `self.importer` personalizados, logra cargar primero los módulos personalizados durante la importación.

Si estás interesado en los detalles del código, por favor consulta el código fuente relevante por ti mismo.

###La falla de `rexec`

En el texto anterior se menciona que a partir de `Python 2.3`, el módulo `rexec` quedó en desuso debido a que este enfoque ha demostrado ser inviable. Con curiosidad, vamos a rastrear un poco su origen:

* En la comunidad alguien reportó un [Bug](https://mail.python.org/pipermail/python-dev/2002-December/031160.html)，并引发了开发者之间的讨论：

    > it's never going to be safe, and I doubt it's very useful as long as it's not safe.

    > Every change is a potential security hole.

    > it's hard to predict what change is going to break it.

    > I don't expect you'll ever reach the point where it'll be wise to advertise this as safe.  I certainly won't.

    >  this is only a useful occupation if you expect to eventually reach a point where you expect that there aren't any security flaws left.  Jeremy & I both doubt that Python will ever reach that level, meaning that the whole exercise of fixing security flaws is a waste of time (if you know you *can't* make it safe, don't waste time trying).

    > I agree (but I have said that in past) the best thing is to deprecate/rip out rexec.

    > The code will still be in older versions if someone decides to pick it up and work on it as a separate project.

El origen de este error es que `Python` introdujo la clase de nuevo estilo `object`, lo cual causó que `rexec` no funcionara correctamente. Como resultado, los desarrolladores expresaron que en un futuro previsible sería difícil evitar esta situación, cualquier modificación podría provocar vulnerabilidades en `rexec`, hacer que no funcione correctamente o superar las restricciones de permisos. Básicamente, resultaba casi imposible proporcionar un entorno seguro sin vulnerabilidades, por lo que los desarrolladores tuvieron que dedicar mucho tiempo a arreglar y parchar continuamente. Finalmente, se abandonó el módulo `rexec` y `Python` no proporcionó una funcionalidad similar. Sin embargo, debido a problemas de compatibilidad y otros, la configuración de `__builtins__` se mantuvo.

Después, aproximadamente en el año 2010, un programador lanzó [pysandbox](https://github.com/vstinner/pysandbox)，dedicado a proporcionar un entorno de sandbox en `Python` que pueda reemplazar a `rexec`. Sin embargo, después de 3 años, el autor decidió abandonar este proyecto y explicó en detalle por qué consideraba que había fracasado: [El proyecto pysandbox está roto](https://mail.python.org/pipermail/python-dev/2013-November/130132.html)，también ha habido otros autores que han resumido el fracaso de este proyecto: [El fracaso de pysandbox](https://lwn.net/Articles/574215/)Si estás interesado, puedes leer el texto original para obtener más información. Aquí te proporciono un resumen para ayudarte a entender:

> After having work during 3 years on a pysandbox project to sandbox untrusted code, I now reached a point where I am convinced that pysandbox is broken by design. Different developers tried to convinced me before that pysandbox design is unsafe, but I had to experience it myself to be convineced.

> I now agree that putting a sandbox in CPython is the wrong design. There are too many ways to escape the untrusted namespace using the various introspection features of the Python language. To guarantee the [safety] of a security product, the code should be [carefully] audited and the code to review must be as small as possible. Using pysandbox, the "code" is the whole Python core which is a really huge code base. For example, the Python and Objects directories of Python 3.4 contain more than 126,000 lines of C code.

> The security of pysandbox is the security of its weakest part. A single bug is enough to escape the whole sandbox.

> pysandbox cannot be used in practice. To protect the untrusted namespace, pysandbox installs a lot of different protections. Because of all these protections, it becomes hard to write Python code. Basic features like "del dict[key]" are denied. Passing an object to a sandbox is not possible to sandbox, pysandbox is unable to proxify arbitary objects. For something more complex than evaluating "1+(2*3)", pysandbox cannot be used in practice, because of all these protections.

El autor de __pysandbox__ considera que es un diseño erróneo tener un entorno de sandbox en `Python`, ya que hay demasiadas formas de escapar de dicho sandbox. Las características del lenguaje que ofrece `Python` son muy diversas y el código fuente de `CPython` es muy extenso, por lo que es prácticamente imposible garantizar la seguridad adecuada. El proceso de desarrollo de __pysandbox__ consistió en aplicar parches de forma continua, pero se han aplicado tantos parches y restricciones que el autor considera que __pysandbox__ ya no puede utilizarse en la práctica, ya que muchas características y funcionalidades han sido restringidas y no se pueden utilizar, como por ejemplo la operación sencilla `del dict[key]`.

##Ejecución restringida ¿Dónde está la salida?

Dado que los métodos como `rexec` y __pysandbox__, que proporcionaban un entorno de sandbox mediante el parcheo de Python, ya no funcionan, me pregunto: ¿cómo podemos proporcionar un entorno de sandbox funcional para Python?

Aquí continué recopilando algunos otros métodos de implementación o casos de estudio para facilitar su consulta y referencia:

* [PyPy](https://doc.pypy.org/en/latest/sandbox.html)Hay una [rama](https://foss.heptapod.net/pypy/pypy/-/tree/branch/sandbox-2)Se ha proporcionado la funcionalidad de la caja de arena, en combinación con [sandboxlib](https://foss.heptapod.net/pypy/sandboxlib)，puedes compilar tú mismo una versión de PyPy con entorno sandbox. Si estás interesado, puedes intentar configurarlo por tu cuenta, consulta algunas [instrucciones](https://foss.heptapod.net/pypy/pypy/-/issues/3192)La implementación de PyPy se basa en la creación de un subproceso en el que todas las entradas, salidas y llamadas al sistema se redirigen a un proceso externo, que controla estos permisos. También es posible controlar el uso de memoria y CPU. Es importante tener en cuenta que esta rama ha estado un tiempo sin nuevas confirmaciones, así que utilízala con precaución.

* Utilizar la herramienta del entorno del sistema operativo conocida como "sandbox" [seccomp](https://en.wikipedia.org/wiki/Seccomp)Es una herramienta de seguridad computacional proporcionada por el núcleo de Linux, [libsecomp](https://github.com/seccomp/libseccomp/tree/main/src/python)Se ha proporcionado una interfaz de Python que se puede incrustar en el código para su uso, o puede utilizar herramientas basadas en seccomp para ejecutar código, como [Firejail](https://firejail.wordpress.com/)[AppArmor](https://apparmor.net/)Es un módulo de seguridad del kernel de Linux que permite al administrador controlar los recursos y funciones a los que un programa puede acceder, protegiendo el sistema operativo. [codejail](https://github.com/openedx/codejail)Es un entorno de sandbox de Python implementado basado en AppArmor. Si estás interesado, puedes probarlo. Hay muchas herramientas similares, pero no se enumeran todas aquí.

* Utiliza un entorno de sandbox o contenedor. [Windows Sandbox](https://learn.microsoft.com/zh-cn/windows/security/threat-protection/windows-sandbox/windows-sandbox-overview)，[LXC](https://linuxcontainers.org/), [Docker](https://www.docker.com/)Espere un momento, aquí no se detalla más.

##**总结** 

El término "总结" en chino se traduce al español como "resumen".

Este texto es un poco largo, gracias por llegar hasta aquí, todas las preguntas mencionadas al comienzo del artículo estoy seguro de que ya han sido respondidas.

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
