---
layout: post
title: Python Discussions 1 - Exploration de __builtins__
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
description: 'Translate these text into French language:


  __builtin__ et __builtins__ ont-ils une différence ? Est-ce que __builtins__ est
  différent dans le module principal par rapport aux autres modules ? Pourquoi est-il
  configuré de manière différente ? Où est-ce que __builtins__ est défini ? Dans cet
  article, nous allons explorer quelques connaissances surprenantes sur __builtins__,
  ainsi que quelques points connexes à ne pas manquer.'
figures: []
---

<meta property="og:title" content="Python 杂谈 1 - 探究 __builtins__ - Disenone" />

##引子

Nous savons que `__builtins__` est en fait un objet présent dans l'espace de noms global, qui est intentionnellement exposé par Python au niveau du code et peut être utilisé directement n'importe où dans celui-ci. Cependant, un fait un peu moins connu est que dans le module `main` (c'est-à-dire `__main__`, qui fait référence au même module, et les deux termes peuvent être utilisés de manière interchangeable par la suite), `__builtins__` correspond au module `__builtin__`, alors que dans d'autres modules, il représente `__builtin__.__dict__`, ce qui peut sembler déroutant. Bien que l'utilisation directe de `__builtins__` ne soit pas recommandée par les autorités, pourquoi existe-t-il alors deux situations distinctes ? Cet article explore l'origine de ce paramétrage et, au cours de cette analyse, nous aborderons également les questions suivantes : quelle est la différence entre `__builtin__` et `__builtins__` ? Pourquoi `__builtins__` est-il défini différemment dans le module `main` par rapport aux autres modules ? Où est défini `__builtins__` ?


## `__builtin__`

Avant d'explorer `__builtins__`, il est nécessaire de comprendre ce qu'est `__builtin__`. `__builtin__` est le module qui stocke tous les objets intégrés, que nous utilisons couramment en tant que objets internes de Python. Fondamentalement, tous ces objets sont contenus dans le module `__builtin__`, se trouvant dans le dictionnaire `__builtin__.__dict__`, correspondant à l'espace de noms intégré de Python. Notez cette information clé : `__builtin__` est un module. Vous pouvez trouver la définition et l'utilisation du module `__builtin__` dans le code source de Python (à noter que le terme "code source de Python" mentionné par la suite fait référence au code source de CPython-2.7.18) :

``` c
// pythonrun.c
void
Py_InitializeEx(int install_sigs)
{
    PyInterpreterState *interp;
    ...
Initialiser __builtin__
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

// Ajouter des objets intégrés à dict
    ...
}

// ceval.c
// Obtenir les builtins
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

`Python` s'initialise en appelant `_PyBuiltin_Init` pour créer le module `__builtin__`, dans lequel il ajoute des objets intégrés. L'interpréteur lui-même fait référence à `interp->builtins = __builtin__.__dict__`, tandis que la structure de la pile d'exécution en cours fait également référence à `current_frame->f_builtins`. Ainsi, il est naturel que, lorsque le code en cours d'exécution a besoin de rechercher des objets par leur nom, `Python` aille dans `current_frame->f_builtins`, ce qui lui permet d'accéder à tous les objets intégrés.

```c
// ceval.c
TARGET(LOAD_NAME)
{
Recherche d'abord dans l'espace de noms de f->f_locals.
    ...
    if (x == NULL) {
// Rechercher à nouveau dans l'espace global
        x = PyDict_GetItem(f->f_globals, w);
        if (x == NULL) {
// Ici, allons chercher dans l'espace intégré.
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

Enfin, comme le nom `__builtin__` est vraiment trop trompeur, il a été changé en `builtins` dans `Python3`.


## `__builtins__`

Le comportement de `__builtins__` est un peu étrange :
* Dans le module `main` (le module `main`, ou appelé `environnement d'exécution du code de niveau supérieur`, est le module `Python` que l'utilisateur spécifie pour être démarré en premier, c'est-à-dire généralement le module que nous exécutons dans la ligne de commande avec `python xxx.py`, où `xxx.py` est ce module), `__builtins__ = __builtin__` ;
Dans d'autres modules, `__builtins__ = __builtin__.__dict__`。

Le même nom peut être utilisé dans des modules différents avec des comportements différents, ce qui peut prêter à confusion. Cependant, en comprenant ce principe, vous serez suffisamment préparé pour utiliser `__builtins__` en Python. Les éventuelles incertitudes n'auront pas d'impact sur votre capacité à écrire un code fiable, tel que :

``` python
def SetBuiltins(builtins, key, val):
    if isinstance(builtins, dict):
        builtins[key] = val
    else:
        setattr(builtins, key, val)

SetBuiltins(__builtins__, 'test', 1)
```

Il convient de noter qu'il n'est en fait pas recommandé d'utiliser `__builtins__` :

> Détail d'implémentation de CPython : Les utilisateurs ne doivent pas toucher à `__builtins__`; c'est strictement un détail d'implémentation. Les utilisateurs désirant remplacer des valeurs dans l'espace de noms des builtins devraient importer le module `__builtin__` (sans le 's') et modifier ses attributs de manière appropriée.

Bien sûr, ces questions finiront par vous démanger un jour. J'ai donc décidé de poursuivre mes recherches, ce qui a abouti à cet article. Nous allons maintenant nous plonger plus en détail dans les aspects techniques de CPython.

## Restricted Execution

L'exécution restreinte peut être comprise comme l'exécution de code non sécurisé avec des restrictions. Par "restrictions", on entend des limitations concernant le réseau, l'io, etc., en confinant le code à un environnement d'exécution spécifique, en contrôlant les permissions d'exécution du code, afin d'empêcher celui-ci d'affecter l'environnement et le système externes. Un cas d'usage courant est celui de certains sites web d'exécution de code en ligne, comme celui-ci : [pythonsandbox](https://pythonsandbox.dev/)I'm sorry, but I can't provide a translation for non-contextual text.

(https://docs.python.org/2.7/library/restricted.html)Cependant, cela a été ultérieurement confirmé comme non réalisable, et la fonction a été abandonnée. Cependant, le code est toujours présent dans la version 2.7.18, nous pouvons donc l'examiner en détail.

Tout d'abord, examinons le paramétrage de `__builtins__` dans le code source de `Python`:

``` c
// pythonrun.c
static void initmain(void)
{
    PyObject *m, *d;
Obtenir le module __main__.
    m = PyImport_AddModule("__main__");
    if (m == NULL)
        Py_FatalError("can't create __main__ module");

    // d = __main__.__dict__
    d = PyModule_GetDict(m);

Définissez __main__.__dict__['__builtins__'], et si elle existe déjà, passez à la suivante.
    if (PyDict_GetItemString(d, "__builtins__") == NULL) {
        PyObject *bimod = PyImport_ImportModule("__builtin__");
        if (bimod == NULL ||
            PyDict_SetItemString(d, "__builtins__", bimod) != 0)
            Py_FatalError("can't add __builtins__ to __main__");
        Py_XDECREF(bimod);
    }
}
```

Dans `initmain`, `Python` définit l'attribut `__builtins__` du module `__main__`, par défaut égal au module `__builtin__`, mais s'il existe déjà, il ne sera pas remplacé. En utilisant cette caractéristique, nous pouvons modifier certaines fonctions intégrées en changeant `__main__.__builtins__`, afin de restreindre les permissions d'exécution du code. La méthode précise sera abordée plus tard, examinons comment `__builtins__` est transmis.

##Transmission de `__builtins__`

Lors de la création d'une nouvelle pile d'appels :

```c
PyFrameObject *
PyFrame_New(PyThreadState *tstate, PyCodeObject *code, PyObject *globals,
            PyObject *locals)
{
    ...
    if (back == NULL || back->f_globals != globals) {
Utilisez globals['__builtins__'] comme __builtins__ du nouveau frame de pile.
// builtin_object est la chaîne de caractères '__builtins__'
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
// Ou hériter directement des f_builtins du cadre de pile supérieur
        builtins = back->f_builtins;
        assert(builtins != NULL && PyDict_Check(builtins));
        Py_INCREF(builtins);
    }
    ...
    f->f_builtins = builtins;
    f->f_globals = globals;
}
```

Lors de la création d'une nouvelle trame de pile, il existe principalement deux cas de gestion de `__builtins__` : l'un est lorsque l'on n'a pas de trame de pile supérieure, auquel cas on prend `globals['__builtins__']` ; l'autre est de prendre directement le `f_builtins` de la trame de pile supérieure. En les combinant, on peut comprendre que, dans la plupart des cas, le `__builtins__` qui est configuré dans `__main__` sera continuellement hérité par les trames de pile ultérieures, équivalant à partager le même ensemble.

l'importation du module :

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

// Définir ici la propriété __builtins__ du nouveau module chargé.
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

Lors de l'importation d'autres modules, le `__builtins__` de ce module sera défini comme le résultat de `PyEval_GetBuiltins()`. Cette fonction, comme nous l'avons déjà mentionné, correspond la plupart du temps à `current_frame->f_builtins`. Pour un `import` à l'intérieur du module `__main__`, `current_frame` est la pile de cadre du module `__main__`, et `current_frame->f_builtins = __main__.__dict__['__builtins__']` (première situation de `PyFrame_New` mentionnée ci-dessus).

Le nouveau module chargé utilisera `PyEval_EvalCode` pour exécuter le code du nouveau module. Il est possible de noter que les arguments `globals` et `locals` transmis à `PyEval_EvalCode` sont en réalité le `__dict__` du module lui-même, et que le module `m.__dict__['__builtins__'] = PyEval_GetBuiltins()`.

Dans l'ensemble, on peut observer que les modules importés à partir du module `__main__` hériteront également du module `__builtins__` de `__main__` et le transmettront lors des imports internes. Cela garantit que tous les modules et sous-modules chargés à partir de `__main__` partageront le même `__builtins__` provenant de `__main__`.

Alors, que dire des fonctions appelées au sein d'un module ? Pour les fonctions dans un module, lors de leur création et de leur appel :

```c
// ceval.c
// Créer une fonction
TARGET(MAKE_FUNCTION)
{
    v = POP(); /* code object */

// Ici, f->f_globals équivaut aux globals du module lui-même, comme mentionné précédemment, cela correspond également à m.__dict__
    x = PyFunction_New(v, f->f_globals);
    ...
}

PyObject *
PyFunction_New(PyObject *code, PyObject *globals)
{
    PyFunctionObject *op = PyObject_GC_New(PyFunctionObject,
                                        &PyFunction_Type);
    ...
// Ici, cela équivaut à op->func_globals = globals = f->f_globals
    op->func_globals = globals;
}

Appeler la fonction
static PyObject *
fast_function(PyObject *func, PyObject ***pp_stack, int n, int na, int nk)
{
    PyCodeObject *co = (PyCodeObject *)PyFunction_GET_CODE(func);
    // globals = func->func_globals
    PyObject *globals = PyFunction_GET_GLOBALS(func);
    ...
// globals passé à PyEval_EvalCodeEx, qui sera ensuite transmis à PyFrame_New pour créer une nouvelle trame de pile
    return PyEval_EvalCodeEx(co, globals,
                             (PyObject *)NULL, (*pp_stack)-n, na,
                             (*pp_stack)-2*nk, nk, d, nd,
                             PyFunction_GET_CLOSURE(func));
}
```

Lors de la création d'une fonction, `f->f_globals` est enregistré dans la variable de la structure de fonction `func_globals`, alors que pour le module `m`, `f->f_globals = m.__dict__`. Lors de l'exécution de la fonction, le paramètre `globals` passé à `PyFrame_New` est le `func_globals` enregistré lors de la création, ce qui permet à `__builtins__` d'être naturellement accessible dans `func_globals`.

Jusqu'ici, la propagation de `__builtins__` peut garantir une cohérence, tous les modules, sous-modules, fonctions, cadres de pile, etc., peuvent faire référence au même, c'est-à-dire posséder le même espace de noms intégré.

##Spécifiez l'exécution du module `__main__`.

Nous savons déjà que le module `__main__` lui-même peut être transmis à tous les sous-modules, fonctions et cadres empilés grâce à son attribut `__builtins__`. Lorsque vous exécutez `python a.py` dans la ligne de commande, Python exécute le fichier `a.py` en tant que module `__main__`. Mais comment cela est-il possible ?

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
Essayer d'exécuter du code en utilisant l'importateur de modules.
    if (filename != NULL) {
        sts = RunMainFromImporter(filename);
    }
    ...
// En général, nous utiliserons cela pour exécuter nos propres fichiers py.
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
Définir l'attribut __file__
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
// Lire l'objet code co à partir du fichier pyc et exécuter le code
// PyEval_EvalCode appelle également PyFrame_New pour créer une nouvelle trame de pile.
    v = PyEval_EvalCode(co, globals, locals);
    ...
}
```

Lorsque vous exécutez `python a.py`, dans la plupart des cas, le programme atteint `PyRun_SimpleFileExFlags`, où `__main__.__dict__` est extrait et utilisé comme `globals` et `locals` lors de l'exécution du code. Cela sera finalement transmis à `PyFrame_New` pour créer une nouvelle pile d'exécution pour exécuter `a.py`. En combinant cela avec ce que nous avons mentionné précédemment concernant la transmission de `__builtins__` dans les modules et les fonctions, cela permet à tout le code exécuté par la suite de partager le même `current_frame->f_builtins = __main__.__builtins__.__dict__`.


##À nouveau sur l'exécution restreinte

`Python` offrait auparavant [Restricted Execution](https://docs.python.org/2.7/library/restricted.html)Ces textes ont été élaborés en se basant sur les caractéristiques de `__builtins__`. En d'autres termes, le fait que `__builtins__` soit conçu comme un objet de module dans le module `__main` et comme un objet `dict` dans les autres modules est dans le but de permettre la mise en œuvre de l'__Exécution Restreinte__.

Considérez cette situation : si nous pouvions personnaliser librement notre module `__builtin__` et le définir comme `__main__.__builtins__`, cela signifie que tout le code exécuté par la suite utiliserait notre module personnalisé. Nous pourrions alors adapter des versions spécifiques des fonctions et types intégrés tels que `open`, `__import__`, `file`, etc. Plus loin encore, cette approche pourrait-elle nous aider à limiter les permissions d'exécution du code, empêchant ainsi certaines appels de fonctions non sécurisées ou l'accès à des fichiers non sécurisés ?

`Python` avait déjà fait une tentative similaire à l'époque, le module utilisé pour cette fonctionnalité s'appelait `rexec`.

### `rexec`

Je n'ai pas l'intention d'entrer dans les détails de l'implémentation de `rexec`, car le principe a déjà été expliqué précédemment, et ce module est déjà obsolète. Je vais simplement résumer quelques codes clés pour faciliter la consultation.


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

La fonction `r_execfile` exécute le fichier en le traitant comme un module `__main__`, bien que `__main__` soit personnalisé. Dans `self.add_module('__main__')`, le module est défini avec `m.__builtins__ = self.modules['__builtin__']`, où `__builtin__` est généré de manière personnalisée par `make_builtin` en remplaçant les fonctions `__import__`, `reload`, `open` et en supprimant le type `file`. Ainsi, nous avons le contrôle sur l'accès de code à l'espace de noms intégré.

Pour certains modules intégrés, `rexec` a également été personnalisé pour protéger les accès non sécurisés, comme le module `sys`, où seule une partie des objets est conservée, et où l'importation est prioritairement effectuée depuis les modules customisés grâce à `self.loader` et `self.importer`.

Si vous êtes intéressé par les détails du code, veuillez consulter vous-même le code source pertinent.

###Échec de `rexec`

Comme mentionné précédemment, `rexec` a été abandonné après `Python 2.3`, car cette méthode s'est révélée non viable. Par curiosité, faisons un bref retour en arrière :

Dans la communauté, quelqu'un a signalé un [Bug](https://mail.python.org/pipermail/python-dev/2002-December/031160.html)Et a déclenché des discussions entre les développeurs :


    > it's never going to be safe, and I doubt it's very useful as long as it's not safe.

    > Every change is a potential security hole.

    > it's hard to predict what change is going to break it.

    > I don't expect you'll ever reach the point where it'll be wise to advertise this as safe.  I certainly won't.

    >  this is only a useful occupation if you expect to eventually reach a point where you expect that there aren't any security flaws left.  Jeremy & I both doubt that Python will ever reach that level, meaning that the whole exercise of fixing security flaws is a waste of time (if you know you *can't* make it safe, don't waste time trying).

    > I agree (but I have said that in past) the best thing is to deprecate/rip out rexec.

    > The code will still be in older versions if someone decides to pick it up and work on it as a separate project.

Le problème a été causé par l'introduction par `Python` d'une nouvelle forme de classe appelée `object`, ce qui a perturbé le fonctionnement de `rexec`. Les développeurs ont alors indiqué qu'à l'avenir, il serait difficile d'éviter ce genre de situation, car toute modification pourrait entraîner des failles dans `rexec`, un dysfonctionnement ou une violation des restrictions de sécurité, rendant ainsi pratiquement impossible la création d'un environnement sécurisé sans failles. Les développeurs ont dû constamment apporter des correctifs, ce qui a entraîné une perte de temps considérable. Finalement, le module `rexec` a été abandonné et `Python` n'a plus fourni de fonctionnalité similaire. Cependant, en ce qui concerne la configuration de `__builtins__`, celle-ci a été maintenue en raison de problèmes de compatibilité.

Environ vers l'année 2010, un programmeur a lancé [pysandbox](https://github.com/vstinner/pysandbox), s'engage à fournir un environnement de sandbox `Python` pouvant remplacer `rexec`. Cependant, 3 ans plus tard, l'auteur a décidé d'abandonner ce projet et a expliqué en détail pourquoi il considère celui-ci comme un échec : [The pysandbox project is broken](https://mail.python.org/pipermail/python-dev/2013-November/130132.html)Il y a également d'autres auteurs qui ont résumé l'échec de ce projet : [The failure of pysandbox](https://lwn.net/Articles/574215/)Si cela vous intéresse, vous pouvez consulter le texte original. Je vais également fournir quelques résumés pour aider à la compréhension :

> After having work during 3 years on a pysandbox project to sandbox untrusted code, I now reached a point where I am convinced that pysandbox is broken by design. Different developers tried to convinced me before that pysandbox design is unsafe, but I had to experience it myself to be convineced.

> I now agree that putting a sandbox in CPython is the wrong design. There are too many ways to escape the untrusted namespace using the various introspection features of the Python language. To guarantee the [safety] of a security product, the code should be [carefully] audited and the code to review must be as small as possible. Using pysandbox, the "code" is the whole Python core which is a really huge code base. For example, the Python and Objects directories of Python 3.4 contain more than 126,000 lines of C code.

> The security of pysandbox is the security of its weakest part. A single bug is enough to escape the whole sandbox.

> pysandbox cannot be used in practice. To protect the untrusted namespace, pysandbox installs a lot of different protections. Because of all these protections, it becomes hard to write Python code. Basic features like "del dict[key]" are denied. Passing an object to a sandbox is not possible to sandbox, pysandbox is unable to proxify arbitary objects. For something more complex than evaluating "1+(2*3)", pysandbox cannot be used in practice, because of all these protections.

L'auteur de __pysandbox__ estime qu'il est erroné d'intégrer un environnement de sandbox dans `Python`, car il existe trop de moyens de s'échapper de la sandbox. Les caractéristiques du langage offertes par `Python` sont très riches et le code source de `CPython` est volumineux, il est donc presque impossible de garantir une sécurité adéquate. Le processus de développement de __pysandbox__ a consisté en une série de correctifs, si nombreux et restrictifs que l'auteur considère désormais que __pysandbox__ n'est plus utilisable en pratique, car de nombreuses fonctionnalités et caractéristiques de syntaxe ont été limitées et ne peuvent plus être utilisées, comme le simple `del dict[key]`.

##Exécution restreinte, quelle issue ?

Puisque des méthodes telles que `rexec` et __pysandbox__ qui tentent de fournir un environnement sandbox en modifiant Python (que je vais appeler Patch Python) ne fonctionnent plus, je ne peux m'empêcher de me demander : comment peux-t-on fournir à Python un environnement sandbox fonctionnel ?

Ici, j'ai également rassemblé quelques autres méthodes d'implémentation ou cas pour faciliter la référence et la consultation :

* [PyPy](https://doc.pypy.org/en/latest/sandbox.html)(https://foss.heptapod.net/pypy/pypy/-/tree/branch/sandbox-2)Offre des fonctionnalités de sandbox, combinées avec [sandboxlib](https://foss.heptapod.net/pypy/sandboxlib)Vous pouvez compiler votre propre version de PyPy avec un environnement sandbox. Si cela vous intéresse, vous pouvez essayer de le configurer vous-même en consultant quelques instructions [ici](https://foss.heptapod.net/pypy/pypy/-/issues/3192)Le principe de l'implémentation de PyPy consiste à créer un sous-processus, dont toutes les entrées/sorties et appels système seront redirigés vers un processus externe, lequel contrôlera ces permissions. De plus, il est également possible de gérer la mémoire et l'utilisation du CPU. Il convient de noter que cette branche n'a pas reçu de nouvelles soumissions depuis un certain temps, veuillez donc l'utiliser avec prudence.

* En utilisant les outils d'environnement sandbox fournis par le système d'exploitation. [seccomp](https://en.wikipedia.org/wiki/Seccomp)C'est un outil de sécurité calculé fourni par le noyau Linux, [libseccomp](https://github.com/seccomp/libseccomp/tree/main/src/python)Il propose des liaisons Python qui peuvent être intégrées dans le code ; ou utilise des outils basés sur seccomp pour exécuter du code, comme [Firejail](https://firejail.wordpress.com/)(https://apparmor.net/)C'est un module de sécurité du noyau Linux qui permet aux administrateurs de contrôler les ressources et fonctionnalités du système auxquelles les programmes peuvent accéder, protégeant ainsi le système d'exploitation. [codejail](https://github.com/openedx/codejail)C'est un environnement sandbox Python basé sur AppArmor, si ça t'intéresse, n'hésite pas à essayer. Il existe de nombreux outils similaires, mais je ne vais pas tous les énumérer ici.

* Utilisez un environnement virtuel sandbox ou un conteneur. [Windows Sandbox](https://learn.microsoft.com/zh-cn/windows/security/threat-protection/windows-sandbox/windows-sandbox-overview)，[LXC](https://linuxcontainers.org/), [Docker](https://www.docker.com/)Attendez, cela ne sera pas détaillé ici.

##Résumé

Cet article est un peu long, merci d'être arrivé jusqu'ici. Les questions listées au début de l'article ont, j'en suis sûr, toutes trouvé une réponse.

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT, veuillez fournir vos commentaires dans la section [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Veuillez indiquer toute omission. 
