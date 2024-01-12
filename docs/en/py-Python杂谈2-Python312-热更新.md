---
layout: post
title: Python Miscellany 2 - Python 3.12 Hot Update
tags:
- dev
- game
- python
- reload
- 热更新
description: How to achieve hot reloading in Python 3.12 recorded
---

<meta property="og:title" content="Python 杂谈 2 - Python3.12 热更新" />

#Python Chat 2 - Python 3.12 now available for updates

> Record how to achieve hot reloading in Python 3.12

##Hot Update

Hot Reload is a technology that allows updates to be made to a program without the need for restarting it. This technology is widely used in the gaming industry. When developers need to fix issues in games, they often use some silent update methods, that's what Hot Reload is.


##Python hot reload

Python itself is a dynamic language, where everything is an object and has the ability to achieve hot updates. We can roughly divide the objects that need to be hot updated in Python into two categories: data and functions.

Data can be understood as the numerical values or settings in a game, such as the player's level, equipment, and so on. Some data should not be hot-updated (such as the player's current level and the player's inventory of equipment; these data should not be modified through hot updates), while some data is what we want to hot-update (such as the basic numerical settings of equipment, the basic numerical settings of skills, and the text on the UI, etc.).

Function, can be understood as game logic, this is basically what we want to hotfix, logic errors basically need to be implemented through hotfix functions.

Below we'll take a closer look at what methods can be used to perform hot updates on Python 3.12.

## Hotfix

The first method we call Hotfix, by letting the program (client program / server program both can) execute a specific Python code to achieve hot updates for data and functions. A simple Hotfix code might look like this:


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

The above code simply demonstrates how to write a Hotfix. After the data/function is modified, the program will read the new data/function for execution when accessed later.

If you are meticulous, you may have a question: What will happen if other code refers to these data and functions that need to be modified?

```python
# attack.py module

player_fire = player.Player.fire_func

def player_attack_by_gun(player, target):
    player_fire(target)
    # ...
```

The answer is that the previous Hotfix does not work for this situation. The function `fire_func` is like an additional copy in other modules. The module calls the copy of the function, and our modifications to the original function do not affect the copy.

So it's important to note that in general code, try to minimize module-level data references and function references as much as possible to avoid situations where the Hotfix doesn't take effect. If the code is already written this way, the Hotfix will require some additional work:

```python
# hotfix code
# ...

import attack
attack.player_fire = player.Player.fire_func

```

After modifying the data/function core with a hotfix, make additional modifications to the places where it is referenced. These additional modifications are easy to overlook, so we still recommend avoiding the use of multiple references as much as possible from a code standard perspective.

In conclusion, Hotfix can meet the basic needs of hot updates, while also having the following issues:

If the data/function is explicitly referenced by other modules, additional references to these modules are required for the hotfix.
If there are a large amount of data/functions that need to be hotfixed, the hotfix code will become very large, making maintenance more difficult and prone to errors.

## Reload

The source code for this chapter can be obtained from here: [python_reloader](https://github.com/disenone/python_reloader)

What we really want is automatic hot updates, without the need to write additional hotfixes. We just need to update the code files and have the program execute a "Reload" function, which will automatically replace the new functions and data. We call this automatic hot update feature "Reload".

Python 3.12 provides the `importlib.reload` function, which allows modules to be reloaded. However, this function performs a full reload and returns a new module object. It does not automatically modify references in other modules. This means that if other modules import the reloaded module, they will still access the old module object. This functionality is not much better than our Hotfix solution, especially since it performs a full reload and we cannot control which data should be preserved. We want to implement our own Reload feature that meets the following requirements:

- Auto-replace function, while the reference to the old function remains valid and will execute the content of the new function.
- Automatically replace data, while allowing partial control over the replacement.
- Keep the reference to the old module, and you will be able to access the new content through the old module.
- Modules that require reloading are controllable.

To fulfill these requirements, we need to rely on the `meta_path` mechanism in Python. For detailed information, please refer to the [official documentation on meta_path].(https://docs.python.org/zh-cn/3/reference/import.html?highlight=meta_path#the-meta-path).

Inside `sys.meta_path`, we can define our meta path finder objects. For example, if we name the finder used for reload as `reload_finder`, `reload_finder` needs to implement a function called `find_spec` and return a `spec` object. After obtaining the `spec` object, Python will execute `spec.loader.create_module` and `spec.loader.exec_module` to complete the module import.

If we execute new module code during this process and copy the functions and data needed from the new module into the old module, we can achieve the goal of Reload.

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

As mentioned above, `find_spec` loads the latest source code of the module and executes the code of the new module within the `__dict__` of the old module. After that, we call `ReloadModule` to handle references and replacements of classes/functions/data. The purpose of `MetaLoader` is to adapt to the `meta_path` mechanism and return the modified module object to the Python virtual machine.

After completing the loading process, let's take a look at the approximate implementation of `ReloadModule`.

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

Inside `ReloadDict`, different types of objects will be distinguished and processed.

If it is a `class`, then calling `ReloadClass` will return a reference to the old module and update the members of the class.
If it is a function/method, invoking `ReloadFunction` will return a reference to the old module and update the internal data of the function.
- If it's data and needs to be preserved, it will roll back `new_dict[attr_name] = old_attr`
- Keep the rest of the citations as new.
- Delete functions that do not exist in the new module.

The specific code for `ReloadClass` and `ReloadFunction` will not be further analyzed here. If interested, you can directly refer to the [source code].(https://github.com/disenone/python_reloader).

The whole process of Reload can be summarized as "putting new wine in old bottles". In order to keep the module/module functions/module classes/module data valid, we need to preserve the references (shells) of these original objects and update their specific data internally. For example, when it comes to functions, we update `__code__`, `__dict__`, and other data. When the function is executed, it will then execute the new code.

##Summary

This article provides a detailed introduction to the two methods of hot updating in Python3, each with its specific application scenarios. We hope it can be helpful to you. Please feel free to reach out if you have any questions.

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
