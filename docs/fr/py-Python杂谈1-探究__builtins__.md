---
layout: post
title: Python Chatter 1 - Exploring __builtins__
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
  différent dans le module principal par rapport aux autres modules ? Pourquoi ont-ils
  été mis en place de manière différente ? Où __builtins__ est-il défini ? Dans cet
  article, nous allons explorer quelques connaissances obscures sur __builtins__,
  ainsi que des sujets connexes qu''il ne faut pas manquer.'
figures: []
---

<meta property="og:title" content="Python 杂谈 1 - 探究 __builtins__ - Disenone" />

##Prélude

Nous savons que `__builtins__` est en soi un objet présent dans l'espace de noms global, exposé intentionnellement par `Python` pour être utilisé directement n'importe où dans le code. Cependant, un fait peu connu est que dans le module `main` (également connu sous le nom de `__main__`, se référant au même module, parfois utilisés de manière interchangeable), il fait référence au module `__builtin__`, alors que dans les autres modules, il représente `__builtin__.__dict__`, ce qui peut sembler assez mystérieux. Bien que l'utilisation directe de `__builtins__` ne soit pas recommandée officiellement, pourquoi y a-t-il ces deux situations différentes ? Dans cet article, nous allons examiner l'origine de cette configuration et chercher les réponses à ces questions : quelle est la différence entre `__builtin__` et `__builtins__` ? Pourquoi `__builtins__` est-il différemment défini dans le module `main` par rapport aux autres modules ? Où est-ce que `__builtins__` est-il défini ?


## `__builtin__`

Avant d'explorer `__builtins__`, nous devons d'abord examiner ce qu'est `__builtin__`. `__builtin__` est le module qui contient tous les objets intégrés, les objets intégrés de Python que nous utilisons couramment sont essentiellement des objets du module `__builtin__`, stockés dans `__builtin__.__dict__`, correspondant à l'espace de noms intégré de Python. Souvenez-vous de ce point clé : `__buintin__` est un module. Vous pouvez trouver la définition et l'utilisation du module `__builtin__` dans le code source Python (remarquez que lorsque nous faisons référence au code source Python, nous parlons du code source de CPython-2.7.18) :

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

Ajoutez des objets intégrés au dictionnaire.
    ...
}

// ceval.c
Obtenir des fonctions intégrées.
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

Lors de l'initialisation de `Python`, la fonction `_PyBuiltin_Init` est appelée pour créer le module `__builtin__`, y ajoutant des objets intégrés. L'interprète lui-même fait référence à `interp->builtins = __builtin__.__dict__`, et la structure de trame d'exécution en cours fait également référence à `current_frame->f_builtins`. Ainsi, de manière naturelle, lors de l'exécution du code nécessitant de rechercher un objet par son nom, `Python` va chercher dans `current_frame->f_builtins`, permettant ainsi d'accéder à tous les objets intégrés.

```c
// ceval.c
TARGET(LOAD_NAME)
{
Recherchez d'abord dans l'espace de noms f->f_locals.
    ...
    if (x == NULL) {
// Recherchez à nouveau dans l'espace global
        x = PyDict_GetItem(f->f_globals, w);
        if (x == NULL) {
Recherchez simplement dans l'espace intégré.
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

Enfin, en raison de la confusion causée par le nom `__builtin__`, il a été renommé en `builtins` dans Python 3.


## `__builtins__`

`__builtins__` in the performance is a bit strange:
Dans le module `main`, `__builtins__ = __builtin__` ;
Dans d'autres modules, `__builtins__ = __builtin__.__dict__`.

Le même nom, mais des comportements différents selon les modules, peut facilement prêter à confusion. Cependant, une fois que vous comprenez ce paramètre, vous pouvez en toute confiance utiliser `__builtins__` en Python sans que la confusion n'affecte votre capacité à écrire un code suffisamment sécurisé, par exemple :

``` python
def SetBuiltins(builtins, key, val):
    if isinstance(builtins, dict):
        builtins[key] = val
    else:
        setattr(builtins, key, val)

SetBuiltins(__builtins__, 'test', 1)
```

Il est important de noter qu'il n'est pas recommandé d'utiliser `__builtins__` :

> Détail d'implémentation de CPython : Les utilisateurs ne devraient pas toucher à `__builtins__` ; c'est strictement un détail d'implémentation. Les utilisateurs souhaitant remplacer des valeurs dans l'espace de noms builtins devraient importer le module `__builtin__` (sans 's') et modifier ses attributs de manière appropriée.

Bien sûr, ces interrogations finiront par vous démanger un jour ou l'autre. J'ai donc décidé de poursuivre mes recherches, c'est ainsi que cet article a vu le jour. Le contenu suivant plongera plus en profondeur dans les __détails de l'implémentation CPython__.

## Restricted Execution

L'exécution restreinte peut être comprise comme l'exécution limitée de code non sécurisé. Cette limitation peut consister à restreindre l'accès au réseau, aux E/S, etc., en maintenant le code dans un environnement d'exécution spécifique afin de contrôler les autorisations d'exécution et d'éviter que le code n'affecte l'environnement et le système externes. Un cas d'utilisation courant est celui des sites web permettant d'exécuter du code en ligne, comme celui-ci : [pythonsandbox](https://pythonsandbox.dev/)I'm sorry, but I can't provide a translation without any text. If you could please provide me with some text to translate, I'd be happy to help you. 

(https://docs.python.org/2.7/library/restricted.html)Cependant, cette fonctionnalité a été abandonnée plus tard car elle a été jugée inapplicable, mais le code est toujours présent dans la version 2.7.18, donc nous pouvons le redécouvrir.

Tout d'abord, examinons le paramètre `__builtins__` défini dans le code source de `Python`.

``` c
// pythonrun.c
static void initmain(void)
{
    PyObject *m, *d;
Obtenir le module __main__
    m = PyImport_AddModule("__main__");
    if (m == NULL)
        Py_FatalError("can't create __main__ module");

    // d = __main__.__dict__
    d = PyModule_GetDict(m);

Définir __main__.__dict__['__builtins__'], en sautant cette étape si elle est déjà effectuée.
    if (PyDict_GetItemString(d, "__builtins__") == NULL) {
        PyObject *bimod = PyImport_ImportModule("__builtin__");
        if (bimod == NULL ||
            PyDict_SetItemString(d, "__builtins__", bimod) != 0)
            Py_FatalError("can't add __builtins__ to __main__");
        Py_XDECREF(bimod);
    }
}
```

Dans `initmain`, Python va assigner à l'attribut `__builtins__` du module `__main__` la valeur par défaut équivalente au module `__builtin__`, mais si une valeur est déjà présente, elle ne sera pas modifiée. En exploitant cette particularité, il est possible de restreindre l'exécution du code en modifiant `__main__.__builtins__` pour altérer certaines fonctionnalités intégrées. Les détails de cette méthode ne seront pas abordés pour le moment, intéressons-nous plutôt à la transmission de `__builtins__`.

##La diffusion de `__builtins__`

Lors de la création d'un nouveau cadre de pile:


```c
PyFrameObject *
PyFrame_New(PyThreadState *tstate, PyCodeObject *code, PyObject *globals,
            PyObject *locals)
{
    ...
    if (back == NULL || back->f_globals != globals) {
Remplacer globals['__builtins__'] par __builtins__ dans le nouveau frame.
Le `builtin_object` est la chaîne de caractères '__builtins__'.
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
// Ou hériter directement des fonctions intégrées de la couche de pile supérieure
        builtins = back->f_builtins;
        assert(builtins != NULL && PyDict_Check(builtins));
        Py_INCREF(builtins);
    }
    ...
    f->f_builtins = builtins;
    f->f_globals = globals;
}
```

Lors de la création d'un nouveau cadre de pile, le traitement de `__builtins__` comprend principalement deux cas : l'un est lorsque qu'il n'y a pas de cadre de pile supérieur, puis on prend `globals['__builtins__']` ; l'autre cas est de prendre directement `f_builtins` du cadre de pile supérieur. Dans l'ensemble, on peut comprendre que généralement, dans le module `__main__`, le `__builtins__` défini restera hérité par les cadres de pile suivants, fonctionnant comme une ressource partagée commune.

Lors de l'importation du module :

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

Définissez ici la propriété __builtins__ du nouveau module chargé.
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

Lors de l'importation d'autres modules, le module en question aura son objet `__builtins__` réglé sur le résultat de `PyEval_GetBuiltins()`, une fonction que nous avons déjà mentionnée, qui dans la plupart des cas est équivalente à `current_frame->f_builtins`. Pour les imports dans le module `__main__`, `current_frame` fait référence au cadre de pile du module `__main__`, et `current_frame->f_builtins = __main__.__dict__['__builtins__']` (voir le premier cas de `PyFrame_New` mentionné précédemment).

Le nouveau module chargé utilisera `PyEval_EvalCode` pour exécuter le code du nouveau module. On peut voir que les arguments `globals` et `locals` passés à `PyEval_EvalCode` sont en fait le `__dict__` du module lui-même, et que le module `m.__dict__['__builtins__'] = PyEval_GetBuiltins()`.

Dans l'ensemble, nous pouvons conclure que les modules importés à partir du module `__main__` hériteront également des `__builtins__` du `__main__` et que cette héritage sera transmis aux imports internes. Ainsi, il est assuré que tous les modules et sous-modules chargés depuis `__main__` pourront partager les mêmes `__builtins__` provenant de `__main__`.

Alors, que se passe-t-il lorsque la fonction est appelée dans un module ? En ce qui concerne les fonctions présentes dans un module, lors de leur création et de leur appel :

```c
// ceval.c
Créer la fonction
TARGET(MAKE_FUNCTION)
{
    v = POP(); /* code object */

Ici, f->f_globals correspond aux globals du module lui-même, comme mentionné précédemment, c'est également équivalent à m.__dict__.
    x = PyFunction_New(v, f->f_globals);
    ...
}

PyObject *
PyFunction_New(PyObject *code, PyObject *globals)
{
    PyFunctionObject *op = PyObject_GC_New(PyFunctionObject,
                                        &PyFunction_Type);
    ...
Ici, cela équivaut à op->func_globals = globals = f->f_globals
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
Les variables globales sont transmises à PyEval_EvalCodeEx, puis transmises à PyFrame_New pour créer un nouveau frame de pile.
    return PyEval_EvalCodeEx(co, globals,
                             (PyObject *)NULL, (*pp_stack)-n, na,
                             (*pp_stack)-2*nk, nk, d, nd,
                             PyFunction_GET_CLOSURE(func));
}
```

Lors de la création d'une fonction, l'attribut `f->f_globals` est stocké dans la variable de structure de fonction `func_globals`, tandis que pour le module `m`, `f->f_globals = m.__dict__`. Lors de l'exécution de la fonction, le paramètre `globals` passé à `PyFrame_New` est l'attribut `func_globals` sauvegardé lors de la création, ce qui signifie que `__builtins__` peut naturellement être obtenu dans `func_globals`.

Jusqu'ici, la transmission de `__builtins__` peut garantir la cohérence, tous les modules, sous-modules, fonctions, cadres empilés, etc., peuvent faire référence au même, ayant ainsi le même espace de noms intégré.

##Spécifie l'exécution du module `__main__`.

Nous savons déjà que le module `__main__` lui-même peut être transmis à tous les sous-modules, fonctions et cadres de pile via `__builtins__`, alors que lorsque vous exécutez `python a.py` en ligne de commande, Python exécute `a.py` en tant que module `__main__`. Comment cela est-il possible :

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
Essayez d'utiliser l'importateur de module pour exécuter le code.
    if (filename != NULL) {
        sts = RunMainFromImporter(filename);
    }
    ...
Généralement, nous utilisons ceci pour exécuter nos propres fichiers py.
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
Lire l'objet de code co du fichier pyc et exécuter le code.
Le code PyEval_EvalCode fait également appel à PyFrame_New pour créer un nouveau frame.
    v = PyEval_EvalCode(co, globals, locals);
    ...
}
```

Lorsque vous exécutez `python a.py`, en général, le code va passer à `PyRun_SimpleFileExFlags`. À l'intérieur de `PyRun_SimpleFileExFlags`, il va extraire `__main__.__dict__`, qui servira de `globals` et `locals` lors de l'exécution du code, et sera ensuite transmis à `PyFrame_New` pour créer un nouveau frame afin d'exécuter `a.py`. En combinant ce que nous avons mentionné précédemment sur la transmission de `__builtins__` dans les modules et fonctions, cela permet à tout le code exécuté ultérieurement de partager le même `current_frame->f_builtins = __main__.__builtins__.__dict__`.


##Revue de l'exécution restreinte

Python a déjà fourni une fonctionnalité appelée [Exécution Restreinte](https://docs.python.org/2.7/library/restricted.html)Ces textes ont été élaborés en se basant sur les fonctionnalités de `__builtins__`. On peut considérer que la raison pour laquelle `__builtins__` a été conçu comme un objet de module dans le module `__main` et comme un objet `dict` dans les autres modules, est pour permettre la réalisation de l'__Exécution Restreinte__.

Considérez ce scénario : si nous pouvions personnaliser librement notre module `__builtin__` et le définir en tant que `__main__.__builtins__`, alors cela équivaudrait à tous les codes exécutés ultérieurement utilisant notre module personnalisé. Nous pourrions personnaliser des fonctions intégrées et des types spécifiques tels que `open`, `__import__`, `file`, etc. De plus, cette approche pourrait-elle nous aider à restreindre les autorisations d'exécution du code, à empêcher les appels de fonctions non sécurisés ou l'accès à des fichiers non sécurisés ?

Le langage de programmation `Python` a déjà tenté cette approche, avec un module appelé `rexec` qui permettait d'implémenter cette fonctionnalité.

### `rexec`

Je n'ai pas l'intention d'expliquer en profondeur l'implémentation de `rexec`, car le principe a déjà été clairement expliqué précédemment, et ce module est d'ailleurs obsolète. Je me contenterai donc de résumer simplement quelques parties clés du code pour faciliter la consultation.


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

La fonction `r_execfile` exécutera le fichier en le considérant comme un module `__main__`, bien que `__main__` soit personnalisé. À l'intérieur de `self.add_module('__main__')`, le module est configuré avec `m.__builtins__ = self.modules['__builtin__']`, où ce `__builtin__` est généré de manière personnalisée par `make_builtin`. Il remplace les fonctions `__import__`, `reload`, `open`, et supprime le type `file`. Ainsi, nous pouvons contrôler l'accès de notre code à l'espace de noms intégré.

Pour certains modules intégrés, `rexec` a également été personnalisé pour protéger les accès non sécurisés, comme le module `sys`, où seuls certains objets sont conservés, et où l'importation est prioritairement effectuée sur des modules personnalisés grâce à `self.loader` et `self.importer`.


Si vous êtes intéressé par les détails du code, veuillez consulter le code source correspondant.

###L'échec de `rexec`

Dans le passage précédent, il a été mentionné que `rexec` a été abandonné après `Python 2.3`, car cette méthode a été prouvée comme non viable. Curieux, revenons brièvement sur l'origine de ce changement:

Dans la communauté, quelqu'un a signalé un [Bug](https://mail.python.org/pipermail/python-dev/2002-December/031160.html)Et a déclenché des discussions entre les développeurs :

    > it's never going to be safe, and I doubt it's very useful as long as it's not safe.

    > Every change is a potential security hole.

    > it's hard to predict what change is going to break it.

    > I don't expect you'll ever reach the point where it'll be wise to advertise this as safe.  I certainly won't.

    >  this is only a useful occupation if you expect to eventually reach a point where you expect that there aren't any security flaws left.  Jeremy & I both doubt that Python will ever reach that level, meaning that the whole exercise of fixing security flaws is a waste of time (if you know you *can't* make it safe, don't waste time trying).

    > I agree (but I have said that in past) the best thing is to deprecate/rip out rexec.

    > The code will still be in older versions if someone decides to pick it up and work on it as a separate project.

Le bug est dû à l'introduction par `Python` des nouvelles classes de style (`new-style class`) avec l'objet `object`, ce qui a rendu le fonctionnement de `rexec` impossible. Les développeurs ont donc indiqué qu'à l'avenir, il serait difficile d'éviter ce type de situation : toute modification pourrait potentiellement introduire des failles dans `rexec`, l'empêcher de fonctionner correctement ou contourner ses restrictions de sécurité. Il était pratiquement impossible de réaliser le rêve de fournir un environnement sécurisé sans faille sans cesse rectifié, entraînant une perte de temps considérable. Finalement, le module `rexec` a été abandonné et `Python` n'a plus proposé de fonctionnalités similaires. Cependant, en raison de problèmes de compatibilité, la configuration de `__builtins__` a été conservée.

Dans les environs de 2010, un programmeur a créé [pysandbox](https://github.com/vstinner/pysandbox)Il s'engage à fournir un environnement sandbox Python alternatif à `rexec`. Cependant, trois ans plus tard, l'auteur a décidé de volontairement abandonner ce projet et a expliqué en détail pourquoi il considérait que ce projet était un échec : [Le projet pysandbox est cassé](https://mail.python.org/pipermail/python-dev/2013-November/130132.html)D'autres auteurs ont également rédigé des articles résumant l'échec de ce projet : [The failure of pysandbox](https://lwn.net/Articles/574215/)Si cela vous intéresse, vous pouvez consulter le texte original pour plus de détails. Voici quelques résumés pour vous aider à comprendre :

> After having work during 3 years on a pysandbox project to sandbox untrusted code, I now reached a point where I am convinced that pysandbox is broken by design. Different developers tried to convinced me before that pysandbox design is unsafe, but I had to experience it myself to be convineced.

> I now agree that putting a sandbox in CPython is the wrong design. There are too many ways to escape the untrusted namespace using the various introspection features of the Python language. To guarantee the [safety] of a security product, the code should be [carefully] audited and the code to review must be as small as possible. Using pysandbox, the "code" is the whole Python core which is a really huge code base. For example, the Python and Objects directories of Python 3.4 contain more than 126,000 lines of C code.

> The security of pysandbox is the security of its weakest part. A single bug is enough to escape the whole sandbox.

> pysandbox cannot be used in practice. To protect the untrusted namespace, pysandbox installs a lot of different protections. Because of all these protections, it becomes hard to write Python code. Basic features like "del dict[key]" are denied. Passing an object to a sandbox is not possible to sandbox, pysandbox is unable to proxify arbitary objects. For something more complex than evaluating "1+(2*3)", pysandbox cannot be used in practice, because of all these protections.

L'auteur de __pysandbox__ estime qu'instaurer un environnement de type bac à sable dans `Python` est une conception erronée, car il existe de nombreuses manières de s'en échapper. Les fonctionnalités du langage offertes par `Python` sont riches, le volume de code source de CPython est très important, et il est pratiquement impossible de garantir une sécurité suffisante. Le processus de développement de __pysandbox__ consiste à apporter constamment des correctifs. Cependant, le nombre de correctifs et les restrictions imposées sont tels que l'auteur estime que __pysandbox__ est désormais inutilisable en pratique, car de nombreuses fonctionnalités et caractéristiques du langage sont désormais limitées, comme par exemple la simple instruction `del dict[key]`.

##Exécution restreinte Où est la sortie

Puisque les méthodes telles que `rexec` et __pysandbox__ qui utilisaient le "patch Python" pour fournir un environnement de bac à sable ne fonctionnent plus, je me demande : comment pouvons-nous maintenant offrir à Python un environnement de bac à sable fonctionnel ?

Ici, j'ai rassemblé quelques autres méthodes de mise en œuvre ou des exemples pour référence et consultation :

* [PyPy](https://doc.pypy.org/en/latest/sandbox.html)(https://foss.heptapod.net/pypy/pypy/-/tree/branch/sandbox-2)Fournit une fonction de bac à sable, combinée avec [sandboxlib](https://foss.heptapod.net/pypy/sandboxlib)Vous pouvez compiler vous-même une version de PyPy avec un environnement sandbox. Si vous êtes intéressé, vous pouvez essayer de configurer vous-même en consultant ces [instructions](https://foss.heptapod.net/pypy/pypy/-/issues/3192)PyPy implements the creation of a subprocess, where all input and output, as well as system calls, are redirected to an external process that controls these permissions. Additionally, memory and CPU usage can be controlled. It is important to note that this branch has not received new commits for some time, so use it with caution.

Utilisez les outils de l'environnement sandbox fournis par le système d'exploitation. [seccomp](https://en.wikipedia.org/wiki/Seccomp)C'est un outil de sécurité informatique fourni par le noyau Linux, [libseccomp](https://github.com/seccomp/libseccomp/tree/main/src/python)Le texte traduit en français est le suivant :
"Python dispose de liaisons embarquées intégrables dans le code, ou vous pouvez utiliser des outils basés sur seccomp pour exécuter du code, par exemple [Firejail](https://firejail.wordpress.com/). [AppArmor](https://apparmor.net/)C'est un module de sécurité du noyau Linux qui permet aux administrateurs de contrôler les ressources système et les fonctionnalités auxquelles les programmes peuvent accéder, protégeant ainsi le système d'exploitation. [codejail](https://github.com/openedx/codejail)C'est un environnement sandbox Python basé sur AppArmor, si cela vous intéresse, vous pouvez essayer. Il existe de nombreux outils similaires, mais je ne vais pas tous les énumérer ici.

Utilisez un environnement virtuel sandbox ou un conteneur. [Windows Sandbox](https://learn.microsoft.com/zh-cn/windows/security/threat-protection/windows-sandbox/windows-sandbox-overview)，[LXC](https://linuxcontainers.org/), [Docker](https://www.docker.com/)Attend un instant, je ne vais pas développer davantage ici.

##Résumé

Ce texte est un peu long, merci d'être arrivé jusqu'ici. Je crois que toutes les questions posées au début du texte ont maintenant été répondues.

--8<-- "footer_fr.md"


> Ce message a été traduit en français par ChatGPT. Veuillez [**反馈**](https://github.com/disenone/wiki_blog/issues/new)Veuillez signaler toute omission. 
