---
layout: post
title: Python Rant 2 - Python 3.12 Hot Update
tags:
- dev
- game
- python
- reload
- 热更新
description: How to implement hot reloading in Python 3.12
---

<meta property="og:title" content="Python 杂谈 2 - Python3.12 热更新" />

#Python Rant 2 - Python 3.12 Hot Update

> Record how to achieve hot reloading in Python 3.12

##Hot update

Hot Reload can be understood as a technology that allows updates to be made to a program without the need to restart it. This technology is widely used in the gaming industry. When developers need to fix game issues without impacting players, they often use a method called silent update, which is also known as hot reload.


##`Python Hot Reload`

Python itself is a dynamic language, where everything is an object and it is capable of achieving hot updates. We can roughly classify the objects that need to be hot updated in Python into two categories: data and functions.

Data can be understood as the numerical values or settings in the game, such as player level, equipment, and so on. Some data should not be hot-swapped (such as the player's current level, the equipment the player has, and these data should not be modified through hot-swapping), and some data are what we want to hot-swap (such as the basic numerical settings of equipment, the basic numerical settings of skills, text on the UI, and so on).

Function, can be understood as game logic, this is basically what we want to hotfix, logic errors basically need to be implemented through hotfix functions.

Let's take a closer look at what methods can be used to implement hot reloading for Python 3.12.

## Hotfix

The first method we call Hotfix, which allows the program (both client and server programs) to execute a specific piece of Python code to achieve hot updates for data and functions. A simple Hotfix code might look like this:


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

The above code simply demonstrates the writing of hotfix. After the data/function is modified, the program will read the new data/function for subsequent access.

If you are detail-oriented, you might have a question: What happens if other code references these data and functions that need to be modified?

```python
# attack.py module

player_fire = player.Player.fire_func

def player_attack_by_gun(player, target):
    player_fire(target)
    # ...
```

The answer is, the previous Hotfix does not work for this situation, `fire_func` acts as an extra copy in other modules, and the module calls the copy of the function, so the modifications to the original function do not take effect on the copy.

So it's important to note that in general, in the code, we should minimize the references to module-level data and function references as much as possible to avoid situations where the hotfix does not take effect. If the code is already written this way, the hotfix will require extra work:

```python
# hotfix code
# ...

import attack
attack.player_fire = player.Player.fire_func

```

After the hotfix modification of the data/function itself, make additional modifications to the places where it is referenced. These additional modifications are easy to overlook, so we still recommend avoiding the usage of multiple references as much as possible from the code specification.

In conclusion, the hotfix can meet the basic needs of hot updating, while the following issues exist:

- If the data/functions are explicitly referenced by other modules, additional references to these modules are needed for the hotfix.
If there is a large amount of data/functions that need to be hotfixed, the hotfix code will become very large, making maintenance difficult and more prone to errors.

## Reload

The source code for this chapter can be obtained from here: [python_reloader](https://github.com/disenone/python_reloader)

What we really want is automatic hot updates. We don't want to write additional hotfixes, just update the code files and have the program execute a reload function to automatically replace the new functions and data. We call this automatic hot update feature "Reload".

Python 3.12 provides the `importlib.reload` function, which allows you to reload a module, but it's a full reload and returns a new module object. References from other modules are not automatically updated, so if other modules import the reloaded module, they still access the old module object. This feature isn't much better than our Hotfix, especially since it's a full module reload and we can't control which data should be retained. We want to implement our own Reload feature to meet these requirements:

- Automatically replace the function, while the reference to the old function remains valid, and the content of the new function will be executed.
- Automatically replace data, while controlling partial replacement
- Retain the reference to the old module, so that the new content can be accessed through the old module.
- Modules that need to be reloaded can be controlled.

To meet these requirements, we need to utilize the meta_path mechanism inside Python. For a detailed explanation, please refer to the official documentation [the-meta-path].(https://docs.python.org/zh-cn/3/reference/import.html?highlight=meta_path#the-meta-path).

In `sys.meta_path`, we can define our metapath finder objects. For example, let's call the finder used for reloading `reload_finder`. The `reload_finder` needs to implement a `find_spec` function and return a `spec` object. After obtaining the `spec` object, Python will execute `spec.loader.create_module` and `spec.loader.exec_module` sequentially to complete the module import process.

If we execute new module code during this process and copy the functions and necessary data from the new module to the old module, we can achieve the goal of Reload:

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

As mentioned above, `find_spec` loads the latest source code of the module and executes the code of the new module within the `__dict__` of the old module. Afterwards, we call `ReloadModule` to handle the references and replacements of classes, functions, and data. The purpose of `MetaLoader` is to adapt to the `meta_path` mechanism and return the processed module object to the Python virtual machine.

After handling the loading process, let's take a look at the approximate implementation of `ReloadModule`.

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

The `ReloadDict` will differentiate and handle different types of objects.

- If it is a class, call `ReloadClass`, which will return a reference to the old module and update the members of the class.
If it is a function/method, calling `ReloadFunction` will return the reference to the old module and update the internal data of the function.
- If it is data and needs to be preserved, it will rollback `new_dict[attr_name] = old_attr`.
- Keep the rest as new references.
- Remove functions that do not exist in the new module.

The specific code for `ReloadClass` and `ReloadFunction` will not be analyzed further here. If you are interested, you can directly refer to the [source code].(https://github.com/disenone/python_reloader).

The entire process of reloading can be summarized as "putting new wine in old bottles." In order to keep the modules/functions/classes/data of the modules valid, we need to preserve the references (shells) of these objects and instead update their specific internal data. For example, for functions, we update `__code__`, `__dict__`, and other data. When the function is executed, it will then execute the new code.

##Summary

This article provides a detailed introduction to the two hot update methods of Python3, each with its own applicable scenarios. We hope it can be helpful to you. If you have any questions, please feel free to communicate at any time.

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
