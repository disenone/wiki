---
layout: post
title: Python Chat 2 - Python 3.12 Hot Update
tags:
- dev
- game
- python
- reload
- 热更新
description: How to implement hot reloading in Python 3.12.
---

<meta property="og:title" content="Python 杂谈 2 - Python3.12 热更新" />

#Python Misc 2 - Python 3.12 Hot Reload

> Record how to achieve hot reloading in Python 3.12

##Hot update

Hot Reload allows updates to be made to a program without the need to restart it. This technology is widely used in the gaming industry. When developers need to fix issues in a game without impacting the players, they often use a technique called hot reload.


##`Python Hot Update`

Python itself is a dynamic language, where everything is an object, capable of achieving hot updates. We can roughly divide the objects that need to be updated in Python into two categories: data and functions.

Data can be understood as the numerical values or settings in the game, such as the player's level, equipment, and so on. Some data should not be hot-updated (such as the player's current level, the equipment the player has, these data modifications should not be done through hot-updates), some data are the ones we want to hot-update (such as the basic numerical settings of equipment, the basic numerical settings of skills, the text on the UI, and so on).

Function, can be understood as game logic, this is basically what we want to hotfix, logic errors basically need to be implemented through hot update functions.

Let's take a closer look at what methods can be used to implement hot updates for Python 3.12.

## Hotfix

The first method we call Hotfix, which allows the program (both client program and server program) to execute a specific Python code segment to achieve hot updates for data and functions. A simple Hotfix code could look like this:


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

The above code simply demonstrates the writing method of Hotfix. After the data/function is modified, the program will read the new data/function for execution during subsequent accesses.

If you are meticulous, you may have a question: What happens if other code references these data and functions that need to be modified?

```python
# attack.py module

player_fire = player.Player.fire_func

def player_attack_by_gun(player, target):
    player_fire(player, target)
    # ...
```

The answer is, the previous Hotfix does not take effect in this situation, the `fire_func` function is like an extra copy in other modules, and the module calls the copy of the function, so the modifications made to the original function do not take effect on the copy.

So need to be careful, generally in the code try to reduce the references to module-level data and function references as much as possible, to avoid the situation where the hotfix does not take effect. If the code is already written this way, the hotfix needs to do more work:

```python
# hotfix code
# ...

import attack
attack.player_fire = player.Player.fire_func

```

After modifying the data/function core hotfix, make additional modifications to the places where it is referenced. These additional modifications are easily overlooked, so we still recommend avoiding the use of multiple references as much as possible from the code specification.

In conclusion, Hotfix can meet the basic needs of hot updates, while also presenting the following issues:

**Translate these text into English language:**

- If the data/function is explicitly referenced by other modules, additional references to these modules are required. Hotfix
If there's a large amount of data/functions that need to be hotfixed, the hotfix code will become very lengthy, maintenance will become more difficult, and it will also be more prone to errors.

## Reload

The source code for this chapter can be obtained from here: [python_reloader](https://github.com/disenone/python_reloader)

What we really want is automatic hot reloading, without the need to write additional hotfixes. We just need to update the code files, and when the program executes a reload function, it will automatically replace the new functions and data. We call this automatic hot reloading function "Reload."

Python 3.12 provides the importlib.reload function, which can reload modules, but it is a full reload and returns a new module object. For references in other modules, it does not automatically update. In other words, if other modules import the reloaded module, they will still access the old module object. This feature is not much better than our Hotfix, especially considering that it fully reloads the module and does not allow us to control which data should be retained. We want to implement our own reload function to meet these requirements:

- Automatic replacement function, while the reference to the old function remains valid and will execute the content of the new function
- Automatically replace data while controlling partial replacement
- Retain references to the old module, so that the new content can be accessed through the old module.
- Modules that need to be reloaded are controllable.

To accomplish these requirements, we need to make use of the meta_path mechanism inside Python. For a detailed explanation, you can refer to the official documentation [the-meta-path(https://docs.python.org/zh-cn/3/reference/import.html?highlight=meta_path#the-meta-path).

In `sys.meta_path` we can define our meta-path finder objects. For example, if we name the finder used for reloading as `reload_finder`, `reload_finder` needs to implement a function `find_spec` and return a `spec` object. Upon receiving the `spec` object, Python will sequentially execute `spec.loader.create_module` and `spec.loader.exec_module` to complete the module import.

If, during this process, we execute new module code and copy the functions and required data from the new module into the old module, we can achieve the goal of reloading.

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

As mentioned, `find_spec` loads the latest module source code and executes the new module's code within the `__dict__` of the old module. Then we call `ReloadModule` to handle the references and replacements of classes, functions, and data. The purpose of `MetaLoader` is to adapt to the meta_path mechanism and to return the processed module objects to the Python virtual machine.

After handling the loading process, let's take a look at the general implementation of `ReloadModule`.

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

If it's a class, calling `ReloadClass` will return a reference to the old module and update the class members.
If it is a function/method, calling `ReloadFunction` will return a reference to the old module and update the internal data of the function.
If it's data and needs to be preserved, it will roll back `new_dict[attr_name] = old_attr`
- The rest should keep the new reference.
- Remove functions that do not exist in the new module

The specific code for `ReloadClass` and `ReloadFunction` will not be further analyzed here. If you are interested, you can directly check the [source code(https://github.com/disenone/python_reloader)。

The whole Reload process can be summarized as "old wine in a new bottle". To keep the module/module function/module class/module data valid, we need to retain references to these original objects (shells) and update their specific data internally, for example, for functions, update `__code__`, `__dict__`, etc. When the function is executed, it will then execute the new code instead.

##Summary

This article provides a detailed introduction to two hot update methods of Python3, each with its corresponding application scenarios, hoping to be helpful to you. If you have any questions, please feel free to communicate at any time.

--8<-- "footer_en.md"



> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
