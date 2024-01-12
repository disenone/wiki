---
layout: post
title: Python Miscellaneous 2 - Python 3.12 Hot Reload
tags:
- dev
- game
- python
- reload
- 热更新
description: Recording how to achieve hot reloading in Python 3.12
---

<meta property="og:title" content="Python 杂谈 2 - Python3.12 热更新" />

#Python Miscellaneous 2 - Python 3.12 Hot Update

> Record how to implement hot reloading in Python 3.12

##Hot update

Hot Reload is a technology that allows updates to be made to a program without the need for a restart. This technology is widely used in the gaming industry. When developers need to fix issues with games, they often use silent updates, or hot reloads, to avoid impacting players.


##Python hot reload

Python itself is a dynamic language, where everything is an object and has the ability to achieve hot updates. We can roughly categorize the objects in Python that need hot updates into two types: data and functions.

Data can be understood as the numerical values or settings in the game, such as the player's level, equipment, and so on. Some data should not be updated in real-time. For example, the player's current level, the equipment the player has, should not be modified through real-time updates. Some data is what we want to update in real-time, such as the basic numerical settings of equipment, the basic numerical settings of skills, and the text on the UI, and so on.

Function, can be understood as game logic, which is basically what we want to hotfix, logic errors basically need to be implemented through hot update functions.

Let's take a closer look at what methods can be used to perform hot reloading on Python 3.12.

## Hotfix

The first method we call Hotfix, it allows the program (both client and server programs) to execute a specific piece of Python code, achieving hot updates to data and functions. A simple Hotfix code might look like this:


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

The above code simply demonstrates the usage of Hotfix. After the data/function is modified, the program will read the new data/function for subsequent access and execution.

If you are meticulous, you may have a question: What will happen if other code refers to these data and functions that need to be modified?

```python
# attack.py module

player_fire = player.Player.fire_func

def player_attack_by_gun(player, target):
    player_fire(player, target)
    # ...
```

The answer is that the previous Hotfix does not work for this situation. The function `fire_func` is like an extra copy in another module. The module calls the copy of the function, so the modifications to the original function do not affect the copy.

So it's important to note that in general, we should try to minimize module-level data references and function references in the code to avoid situations where Hotfixes don't take effect. If the code is already written this way, extra work will be needed for the Hotfix to work properly:

```python
# hotfix code
# ...

import attack
attack.player_fire = player.Player.fire_func

```

After modifying the data/function core with a hotfix, make additional modifications to the places where it is referenced. These additional modifications are easily overlooked, so we still recommend avoiding the practice of multiple references as much as possible from the code specification perspective.

In conclusion, Hotfix can meet the basic needs of hot updates, but it also has the following problems:

- If the data/function is explicitly referenced by other modules, additional references to these modules are required. Hotfix
If there is a large amount of data/functions that need to be hotfixed, then the code of the hotfix will become very large, maintenance will become more difficult, and it will also be more prone to errors.

## Reload

You can obtain the source code for this section from here: [python_reloader](https://github.com/disenone/python_reloader)

What we really want is automatic hot updates, without the need to write additional hotfixes. Just update the code files, execute a reload function, and the program will automatically replace the new functions and data. We call this automatic hot update feature "Reload."

Python 3.12 provides the `importlib.reload` function, which can reload modules, but it is a full reload and returns a new module object, so it doesn't automatically update references in other modules. This means that if other modules import the reloaded module, they will still access the old module object. This functionality isn't much better than our Hotfix, especially since it's a full reload of the module and we can't control which data should be retained. We want to implement our own Reload feature that meets these requirements:

- Automatically replace the function, while the reference to the old function remains valid and will execute the content of the new function
- Automatically replace data while controlling partial replacement
- Keep the reference to the old module, so that the new content can be accessed through the old module.
- Modules that need reloading are controllable

To meet these requirements, we need to leverage the meta_path mechanism within Python. For detailed information, please refer to the official documentation [the-meta-path](https://docs.python.org/zh-cn/3/reference/import.html?highlight=meta_path#the-meta-path)。

In `sys.meta_path`, we can define our meta path finder objects, for example, we name the finder used for reloading as `reload_finder`. The `reload_finder` needs to implement a function `find_spec` and return the `spec` object. Once Python gets the `spec` object, it will sequentially execute `spec.loader.create_module` and `spec.loader.exec_module` to complete the module import.

If we execute new module code during this process and copy the functions and required data from the new module into the old module, we can achieve the purpose of reloading.

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

As mentioned above, `find_spec` loads the latest module source code and executes the new module's code inside the `__dict__` of the old module. Afterwards, we call `ReloadModule` to handle the references and replacements of classes, functions, and data. The purpose of `MetaLoader` is to adapt to the meta_path mechanism and return the processed module objects to the Python virtual machine.

After completing the loading process, let's take a look at the general implementation of `ReloadModule`.

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

The `ReloadDict` inside will differentiate and handle different types of objects.

If it's a class, calling `ReloadClass` will return the reference to the old module and update the class members.
If it is a function/method, calling `ReloadFunction` will return a reference to the old module and update the internal function data.
If it's data and needs to be preserved, it will roll back `new_dict[attr_name] = old_attr`
- The rest should remain with the new citation.
- Remove functions that do not exist in the new module

The specific code for `ReloadClass` and `ReloadFunction` will not be further analyzed here. If you are interested, you can directly refer to the [source code](https://github.com/disenone/python_reloader)。

The entire process of Reload can be summarized as "putting new wine in old bottles." In order to maintain the effectiveness of modules, module functions, module classes, and module data, we need to retain references to these original objects (shells) and then update their specific data internally. For example, for functions, we update `__code__`, `__dict__`, and other data. When the function is executed, it will then execute the new code.

##Summary

This article provides a detailed introduction to two hot update methods of Python3, each with its corresponding use cases, hoping to be helpful to you. Feel free to reach out if you have any questions.

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
