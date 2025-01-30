---
layout: post
title: Python Conversaciones 2 - Actualización en caliente de Python 3.12
tags:
- dev
- game
- python
- reload
- 热更新
description: Registrar cómo implementar actualizaciones en caliente en Python 3.12.
---

<meta property="og:title" content="Python 杂谈 2 - Python3.12 热更新" />

#Python Chat 2 - Actualización en caliente de Python 3.12

> Registro sobre cómo implementar hot reload en Python 3.12

##Actualización en caliente

La actualización en caliente (Hot Reload) se puede entender como una técnica para actualizar un programa sin necesidad de reiniciarlo. Esta técnica tiene una amplia aplicación en la industria de los videojuegos; cuando los desarrolladores corrigen problemas en el juego, a menudo necesitan emplear métodos de actualización silenciosa para no afectar a los jugadores, es decir, la actualización en caliente.


##Actualización en caliente de Python

Python en sí es un lenguaje dinámico, todo es un objeto y tiene la capacidad de realizar actualizaciones en caliente. Podemos dividir de manera aproximada los objetos que necesitan actualización en caliente en Python en dos tipos: datos y funciones.

Los datos, en el contexto de los juegos, se refieren a los valores o ajustes, como el nivel del jugador, los objetos que tiene, etc. Algunos datos no deben actualizarse en caliente, como el nivel actual del jugador o los objetos en su posesión, ya que modificarlos no debería realizarse mediante actualizaciones en caliente. Otros datos, como los valores base de los objetos o habilidades, así como el texto en la interfaz de usuario, son propensos a actualizaciones en caliente.

La función, se puede entender como la lógica del juego, esto es principalmente lo que queremos actualizar, los errores lógicos generalmente necesitan ser solucionados a través de la actualización de la función.

A continuación, veamos específicamente qué métodos se pueden utilizar para realizar una actualización en caliente de Python 3.12.

## Hotfix

La primera forma la llamamos Hotfix, que consiste en hacer que el programa (tanto el cliente como el servidor) ejecute un fragmento específico de código en Python para actualizar los datos y las funciones en caliente. Un fragmento sencillo de código Hotfix podría ser el siguiente:


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

El código anterior muestra de manera simple cómo escribir un Hotfix. Después de modificar los datos / funciones, el programa leerá los nuevos datos / funciones durante los accesos posteriores.

Si eres un poco más detallista, podrías tener una pregunta: ¿qué pasaría si otros códigos hacen referencia a estos datos y funciones que necesitan ser modificados?

```python
# attack.py module

player_fire = player.Player.fire_func

def player_attack_by_gun(player, target):
    player_fire(player, target)
    # ...
```

La respuesta es que el hotfix anterior no tiene efecto en esta situación, la función `fire_func` es como tener una copia adicional en otro módulo, y en el módulo en el que se llama se está utilizando la copia de la función, por lo que las modificaciones en la función original no tienen efecto en la copia.

Por lo tanto, es importante tener en cuenta que en el código en general se debe minimizar las referencias de datos y funciones a nivel de módulo tanto como sea posible, para evitar situaciones en las que la corrección rápida no surta efecto. Si el código ya está escrito de esta manera, la corrección rápida requerirá un esfuerzo adicional:

```python
# hotfix code
# ...

import attack
attack.player_fire = player.Player.fire_func

```

Después de modificar el Hotfix del cuerpo de datos / funciones, se deben realizar cambios adicionales en los lugares donde se hace referencia. Estas modificaciones adicionales son fáciles de omitir, por lo que seguimos recomendando, desde el punto de vista de la normativa de código, evitar en la medida de lo posible la escritura de múltiples referencias.

En resumen, Hotfix puede satisfacer las necesidades básicas de actualizaciones en caliente, aunque presenta los siguientes problemas:

Si los datos/funciones son explícitamente referenciados por otros módulos, se requiere un Hotfix adicional para estas referencias.
Si hay una gran cantidad de datos/funciones que necesitan ser corregidas rápidamente, entonces el código del parche rápido se volverá muy extenso, aumentando la dificultad de mantenimiento y la probabilidad de errores.

## Reload

El código fuente de este capítulo se puede obtener aquí: [python_reloader](https://github.com/disenone/python_reloader)

Lo que realmente queremos es una actualización automática en caliente, sin necesidad de escribir un Hotfix adicional; simplemente actualizar los archivos de código y hacer que el programa ejecute una función Reload, lo que reemplazará automáticamente las nuevas funciones y nuevos datos. A esta función de actualización automática en caliente la llamamos Reload.

Python 3.12 introduces the importlib.reload function, which allows you to reload modules. However, it performs a full reload and returns a new module object. References in other modules do not get automatically updated. In other words, if a module that has been reloaded is imported in another module, the old module object will still be accessed. This feature is not much better than our Hotfix, especially considering it reloads the entire module without allowing us to control which data should be preserved. We aim to implement our own Reload function to meet these requirements:

- Función de reemplazo automático, mientras que las referencias a la función antigua siguen siendo válidas y ejecutarán el contenido de la nueva función.
- Reemplazo automático de datos, con la posibilidad de controlar parte del reemplazo.
- Conservar la referencia al módulo antiguo, a través del módulo antiguo se podrá acceder al nuevo contenido.
Se requiere que los módulos que necesitan ser recargados sean controlables.

Para cumplir con estos requisitos, necesitamos aprovechar el mecanismo de meta_path dentro de Python. Para más detalles, consulte la documentación oficial [the-meta-path](https://docs.python.org/zh-cn/3/reference/import.html?highlight=meta_path#the-meta-path)Lo siento, pero no puedo traducir texto que no contiene palabras o contenido. ¿Puedo ayudarte con algo más?

Dentro de sys.meta_path se pueden definir nuestros objetos buscadores de rutas, como por ejemplo si llamamos a nuestro buscador utilizado para recargar "reload_finder", este debe implementar una función llamada find_spec y devolver un objeto spec. Una vez Python obtiene el objeto spec, ejecutará secuencialmente spec.loader.create_module y spec.loader.exec_module para completar la importación del módulo.

Si durante este proceso ejecutamos el código de un nuevo módulo y copiamos las funciones y datos necesarios del nuevo módulo al antiguo, podremos lograr el objetivo de Recargar.

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

Como se mencionó anteriormente, `find_spec` carga el código fuente más reciente del módulo y ejecuta el código del nuevo módulo dentro del `__dict__` del módulo antiguo. Luego, llamamos a `ReloadModule` para manejar la referencia y sustitución de clases / funciones / datos. El propósito de `MetaLoader` es adaptarse al mecanismo de `meta_path`, devolviendo al intérprete de Python los objetos de módulo que hemos manipulado.

Una vez completado el proceso de carga, veamos la implementación general de `ReloadModule`.

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

`ReloadDict` distingue el tratamiento de diferentes tipos de objetos.

Si es una clase, llama a `ReloadClass`, que devolverá la referencia al módulo anterior y actualizará los miembros de la clase.
- Si es una función / método, se llamará a `ReloadFunction`, que devolverá la referencia del módulo antiguo y actualizará los datos internos de la función.
Si se trata de datos y es necesario conservarlos, se revertirá `new_dict[attr_name] = old_attr.`
Mantén el resto de las citas nuevas.
Eliminar las funciones que no existen en el nuevo módulo.

No se profundizará más en el código específico de `ReloadClass` y `ReloadFunction`, los interesados pueden consultar directamente [el código fuente](https://github.com/disenone/python_reloader)。

El proceso completo de Reload se puede resumir en: un nuevo vino en una botella vieja. Para mantener la validez de las funciones/clases/datos del módulo, necesitamos conservar las referencias a esos objetos originales (las estructuras), y actualizar los datos concretos en su interior. Por ejemplo, para las funciones, se actualizan datos como `__code__`, `__dict__`, etc., y cuando la función se ejecute, comenzará a ejecutar el nuevo código.

##Resumen

Este texto presenta en detalle dos métodos de actualización en caliente de Python 3, cada uno con sus propias situaciones de aplicación. Espero que te resulte útil. No dudes en comunicarte si tienes alguna pregunta.

--8<-- "footer_es.md"


> Esta publicación fue traducida utilizando ChatGPT, por favor en [**comentarios**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。 
