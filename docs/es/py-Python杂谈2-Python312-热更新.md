---
layout: post
title: Python Chit-Chat 2 - Actualización en caliente de Python3.12
tags:
- dev
- game
- python
- reload
- 热更新
description: Registrar cómo implementar la actualización en caliente en Python 3.12.
---

<meta property="og:title" content="Python 杂谈 2 - Python3.12 热更新" />

#Python Charla 2 - Actualización en caliente de Python 3.12

> Aquí tienes la traducción del texto al español:

> *Cómo implementar actualizaciones en caliente en Python 3.12*

##**热更新**

La expresión "热更新" se traduce al español como "actualización en tiempo real".

La función de recarga en caliente (Hot Reload) se refiere a la tecnología que permite actualizar un programa sin necesidad de reiniciar. Esta tecnología se usa ampliamente en la industria de los videojuegos, ya que los desarrolladores necesitan solucionar problemas sin interrumpir a los jugadores, por lo que a menudo se emplea la actualización en caliente de forma discreta.


##Python Hot Reload

Python en sí mismo es un lenguaje dinámico, donde todo es un objeto y tiene la capacidad de actualizarse en caliente. Podemos clasificar aproximadamente en dos tipos los objetos en Python que requieren una actualización en caliente: los datos y las funciones.

**数据**，puede entenderse como los valores o configuraciones en un juego, como el nivel del jugador, el equipamiento, etc. Algunos datos no deben ser actualizados en caliente (por ejemplo, el nivel actual del jugador, el equipamiento que tiene el jugador, estos cambios no deben realizarse a través de una actualización en caliente), mientras que otros datos deseamos que se actualicen en caliente (como las configuraciones básicas del equipamiento o las habilidades, el texto en la interfaz de usuario, etc.).

Las funciones se pueden entender como la lógica del juego, que es principalmente lo que queremos actualizar en caliente. Los errores lógicos generalmente se deben solucionar a través de funciones de actualización en caliente.

A continuación, vamos a ver en detalle qué métodos se pueden utilizar para realizar actualizaciones en caliente en Python3.12.

## Hotfix

La primera forma la llamamos Hotfix, mediante la cual se ejecuta un código específico de Python en el programa (tanto en el programa cliente como en el programa del servidor) para realizar una actualización en caliente de los datos y funciones. Un código de Hotfix simple podría ser así:


```python
# hotfix code

# hotfix data
import weapon_data
weapon_data.gun.damage = 100

# hotfix func
import player
def new_fire_func(self, target):
    target.health -= weapon_data.gun.damage
    # ...
player.Player.fire_func = new_fire_func
```

El código anterior muestra de forma sencilla cómo hacer un Hotfix. Después de modificar los datos/funciones, cuando el programa los vuelva a acceder, leerá los nuevos datos/funciones para ejecutarlos.

Si eres detallista, es posible que te surja una pregunta: ¿qué sucede si otros fragmentos de código están haciendo referencia a los datos y funciones que necesitan ser modificados?

```python
# attack.py module

player_fire = player.Player.fire_func

def player_attack_by_gun(player, target):
    player_fire(player, target)
    # ...
```

La respuesta es que el Hotfix anterior no funciona en esta situación. La función `fire_func` es esencialmente una copia adicional en otro módulo. El módulo en cuestión llama a la copia de la función, pero si modificamos el cuerpo de la función, no afectará a la copia.

Para evitar que ocurra la situación en la que las correcciones rápidas no funcionen, es importante tener en cuenta que, en general, se deben minimizar las referencias de datos y funciones a nivel de módulo en el código. Si el código ya se encuentra escrito de esta manera, será necesario realizar un poco más de trabajo para implementar la corrección rápida.

```python
# hotfix code
# ...

import attack
attack.player_fire = player.Player.fire_func

```

Después de modificar el núcleo de los datos / funciones a través de la corrección de errores, realizar cambios adicionales en los lugares donde se hace referencia a ellos. Estos cambios adicionales suelen pasarse por alto fácilmente, por lo que todavía recomendamos tratar de evitar en la medida de lo posible el uso de múltiples referencias en el código según las normas de estilo.

En resumen, Hotfix puede satisfacer las necesidades básicas de las actualizaciones en tiempo real, pero también presenta los siguientes problemas:

- Si los datos/funciones son explícitamente referenciados por otros módulos, se requiere un Hotfix para estas referencias a los módulos adicionales.
- Si hay una gran cantidad de datos/funciones que necesitan ser corregidos rápidamente, entonces el código para corregir rápidamente se volverá muy extenso, lo que dificultará su mantenimiento y aumentará las posibilidades de cometer errores.

## Reload

El código fuente de este capítulo se puede obtener aquí: [python_reloader](https://github.com/disenone/python_reloader)

Lo que realmente queremos es una actualización automática en caliente, sin necesidad de escribir un Hotfix adicional, solo necesitamos actualizar los archivos de código, de modo que al ejecutar una función "Reload" se reemplacen automáticamente las nuevas funciones y datos. A esta funcionalidad de actualización automática en caliente la llamamos "Reload".

Python 3.12 proporciona la función `importlib.reload`, que permite recargar un módulo, pero lo hace de forma completa y devuelve un nuevo objeto de módulo. Sin embargo, no modifica automáticamente las referencias a este módulo en otros módulos. Esto significa que si otros módulos importan el módulo recargado, seguirán accediendo al antiguo objeto de módulo. Esta funcionalidad no es muy superior a nuestra solución de Hotfix, ya que además recarga completamente el módulo sin dar opción a controlar qué datos se deben conservar. Queremos implementar nuestro propio mecanismo de recarga que cumpla con los siguientes requisitos:

- `自动替换函数`  se refiere a una función que se reemplaza automáticamente, mientras que las referencias a la función anterior siguen siendo válidas y ejecutarán el contenido de la nueva función.
- Reemplazo automático de datos, con control parcial de la substitución.
- Se reserva la referencia del módulo antiguo para acceder al nuevo contenido a través de él.
- Los módulos que necesitan volver a cargarse son controlables.

Para cumplir con estos requisitos, necesitamos utilizar el mecanismo `meta_path` en Python. Puedes encontrar una explicación detallada en la documentación oficial [the-meta-path](https://docs.python.org/zh-cn/3/reference/import.html?highlight=meta_path#the-meta-path).

En `sys.meta_path` podemos definir nuestros objetos de buscador de ruta de metadatos. Por ejemplo, podemos llamar a nuestro buscador para recargar `reload_finder`, el cual necesita implementar una función llamada `find_spec` y devolver un objeto `spec`. Una vez que Python tenga el objeto `spec`, ejecutará `spec.loader.create_module` y `spec.loader.exec_module` en secuencia para completar la importación del módulo.

Si durante este proceso, ejecutamos el código del nuevo módulo y copiamos las funciones y los datos necesarios dentro del módulo antiguo, podremos lograr el objetivo de recargar (Reload).

```python linenums="1"
class MetaFinder:
    def __init__(self, reloader):
        self._reloader = reloader

    def find_spec(self, fullname, path, target=None):
        # find source file
        finder = importlib.machinery.PathFinder()
        spec = finder.find_spec(fullname, path)
        if not spec:
            return

        old_module = self._reloader.GetOldModule(fullname)
        if old_module:
            # run new code in old module dict
            code = spec.loader.get_code(fullname)
            exec(code, old_module.__dict__)
            module = old_module
        else:
            # if old module not exists, just create a new one
            module = import_util.module_from_spec(spec)
            spec.loader.exec_module(module)

        try:
            self._reloader.ReloadModule(module)
        except:
            sys.excepthook(*sys.exc_info())

        return import_util.spec_from_loader(fullname, MetaLoader(module))


class MetaLoader:
    def __init__(self, module):
        self._module = module

    def create_module(self, spec):
        return self._module

    def exec_module(self, module):
        # restore __spec__
        module.__spec__ = module.__dict__.pop('__backup_spec__')
        module.__loader__ = module.__dict__.pop('__backup_loader__')
```

Como se mencionó anteriormente, `find_spec` carga el código fuente más reciente del módulo y ejecuta el código del nuevo módulo dentro del `__dict__` del módulo anterior. Luego, utilizamos `ReloadModule` para manejar las referencias y reemplazar clases, funciones y datos. El propósito de `MetaLoader` es adaptarse al mecanismo `meta_path` y devolver al intérprete de Python los objetos de módulo que hemos procesado.

Después de que se complete el proceso de carga, echemos un vistazo a la implementación aproximada de `ReloadModule`.

```python linenums="1"
# ...
def ReloadModule(self, module):
    old_module_info = self._old_module_infos.get(module.__name__)
    if not old_module_info:
        return

    self.ReloadDict(module, old_module_info, module.__dict__)

def ReloadDict(self, module, old_dict, new_dict, _reload_all_data=False, _del_func=False):
    dels = []

    for attr_name, old_attr in old_dict.items():

        if attr_name in self.IGNORE_ATTRS:
            continue

        if attr_name not in new_dict:
            if _del_func and (inspect.isfunction(old_attr) or inspect.ismethod(old_attr)):
                dels.append(attr_name)
            continue

        new_attr = new_dict[attr_name]

        if inspect.isclass(old_attr):
            new_dict[attr_name] = self.ReloadClass(module, old_attr, new_attr)

        elif inspect.isfunction(old_attr):
            new_dict[attr_name] = self.ReloadFunction(module, old_attr, new_attr)

        elif inspect.ismethod(old_attr) or isinstance(old_attr, classmethod) or isinstance(old_attr, staticmethod):
            self.ReloadFunction(module, old_attr.__func__, new_attr.__func__)
            new_dict[attr_name] = old_attr

        elif inspect.isbuiltin(old_attr) \
                or inspect.ismodule(old_attr) \
                or inspect.ismethoddescriptor(old_attr) \
                or isinstance(old_attr, property):
            # keep new
            pass

        elif not _reload_all_data and not self.NeedUpdateData(module, new_dict, attr_name):
            # keep old data
            new_dict[attr_name] = old_attr

    if dels:
        for name in dels:
            old_dict.pop(name)
# ...

```

En la función `ReloadDict`, se diferenciará y se procesará de manera distinta los diferentes tipos de objetos.

- Si es una clase, se llama a `ReloadClass`, que devuelve una referencia al módulo antiguo y actualiza los miembros de la clase.
- Si es una función / método, llame a `ReloadFunction`, que devolverá la referencia al antiguo módulo y actualizará los datos internos de la función.
- Si se trata de datos y se necesita conservar, se revertirá `new_dict[attr_name] = old_attr`
- Mantenga el resto de las citas como nuevas.
- Eliminar las funciones que no se encuentran en el nuevo módulo.

El código concreto para `ReloadClass` y `ReloadFunction` no se analizará en detalle aquí. Si estás interesado, puedes consultar directamente el [código fuente](https://github.com/disenone/python_reloader).

整个重新加载的过程，可以概括为：给旧东西注入新的魂魄。为了保持模块/模块的函数/模块的类/模块的数据有效，我们需要保存原来这些对象的引用（外壳），然后更新它们内部的具体数据，例如对于函数，更新 `__code__`，`__dict__` 等数据，函数执行时，将执行新的代码。

##**Resumen**

Este documento describe en detalle dos formas de actualización en caliente disponibles en Python3, cada una con sus respectivos casos de uso. Esperamos que te sea útil. Si tienes alguna pregunta, no dudes en comunicarte en cualquier momento.

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
