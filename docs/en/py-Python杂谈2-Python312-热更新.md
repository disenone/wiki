---
layout: post
title: Python Miscellaneous 2 - Python 3.12 Hot Update
tags:
- dev
- game
- python
- reload
- 热更新
description: How to implement hot reload in Python 3.12.
---

<meta property="og:title" content="Python 杂谈 2 - Python3.12 热更新" />

#Python Miscellaneous 2 - Python 3.12 Hot Update

> Record how to achieve hot update in Python 3.12

##Hot update

Hot Reload is a technology that allows updates to be made to a program without the need for a restart. This technology is widely used in the gaming industry. When developers need to fix issues in games without impacting players, they often use a form of silent update, which is known as Hot Reload.


##Python Hot Update

Python itself is a dynamic language where everything is an object and has the ability to achieve hot updates. We can roughly divide the objects that need hot updates in Python into two categories: data and functions.

Data can be understood as the values or settings in the game, such as the player's level, equipment, and so on. Some data should not be hot-updated (such as the player's current level, the player's owned equipment; these data should not be modified through hot updates), while some data is what we want to hot-update (such as the basic numerical settings of equipment, the basic numerical settings of skills, text on the UI, etc.).

Function, can be understood as game logic, this is basically what we want to hotfix, logic errors basically need to be implemented through hot update functions.

Let's take a closer look at what methods can be used to perform hot reloading on Python 3.12.

## Hotfix

The first method we call Hotfix, through letting the program (both client and server programs) execute a specific Python code, achieves hot updates for data and functions. A simple Hotfix code may look like this:


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

The above code demonstrates the basic usage of Hotfix. After the data / function is modified, the program will subsequently read and execute the new data / function when accessed.

If you are meticulous, you may have a question: What would happen if other code references these data and functions that need to be modified?

```python
# attack.py module

player_fire = player.Player.fire_func

def player_attack_by_gun(player, target):
    player_fire(player, target)
    # ...
```

The answer is that the previous Hotfix does not work in this case. The `fire_func` function is like an extra copy in other modules. The module calls the copy of the function, so modifications to the original function do not affect the copy.

So it's important to note that in general, we should try to minimize module-level data references and function references in the code, to avoid situations where the hotfixes don't take effect. If the code is already written this way, extra work will be needed for the hotfix.

```python
# hotfix code
# ...

import attack
attack.player_fire = player.Player.fire_func

```

After modifying the data/function core Hotfix, make additional modifications to the referenced locations. These additional modifications are easy to overlook, so we still recommend avoiding the use of multiple references as much as possible from the code specification.

In conclusion, hotfix can meet the basic needs of live updates, but it also has the following issues:

If the data/function is explicitly referenced by other modules, additional references to these modules need to be hotfixed.
If there is a large amount of data/functions that need to be hotfixed, the hotfix code will become very large, making maintenance more difficult and prone to errors.

## Reload

This chapter's source code can be obtained from here: [python_reloader](https://github.com/disenone/python_reloader)

What we really want is automatic hot updates, without the need for writing extra hotfixes. We just need to update the code files and then have the program execute a reload function to automatically replace the new functions and data. We call this automatic hot update feature "Reload".

Python 3.12 provides the `importlib.reload` function, which can reload modules, but it is a full reload and returns a new module object. For references to the reloaded module in other modules, they are not automatically updated, meaning that if other modules import the reloaded module, they still access the old module object. This feature is not much better than our Hotfix, especially because it fully reloads the module and we can't control which data should be retained. We want to implement our own Reload feature that meets these requirements:

- Automatic replacement function, while the reference to the old function remains valid and will execute the content of the new function
- Automatically replace data while controlling partial replacements
- Keep the reference to the old module, and through the old module, you can access the new content.
- Modules requiring reload are controllable

To meet these requirements, we need to make use of the mechanism inside Python called meta_path. For a detailed explanation, you can refer to the official documentation [the-meta-path].(https://docs.python.org/zh-cn/3/reference/import.html?highlight=meta_path#the-meta-path)。

Inside `sys.meta_path`, we can define our meta path finder objects, for example, we can name the finder used for reloading as `reload_finder`. `reload_finder` needs to implement a function called `find_spec` and return a `spec` object. After Python obtains the `spec` object, it will execute `spec.loader.create_module` and `spec.loader.exec_module` in sequence to complete the module import.

If we execute new module code during this process and copy the functions and required data from the new module to the old module, we can achieve the purpose of reloading.

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

As mentioned above, `find_spec` loads the latest source code of a module and executes the new module's code within the `__dict__` of the old module. After that, we call `ReloadModule` to handle the references and replacements of classes / functions / data. The purpose of `MetaLoader` is to adapt to the meta_path mechanism and return the processed module objects to the Python virtual machine.

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

The `ReloadDict` will differentiate and handle different types of objects inside.

If it is a class, calling `ReloadClass` will return a reference to the old module and update the members of the class.
If it's a function/method, invoking `ReloadFunction` will return the reference of the old module and update the internal data of the function.
If it's data and needs to be preserved, it will roll back `new_dict[attr_name] = old_attr`.
- The rest should remain in the new citation.
- Remove functions that do not exist in the new module

The specific code for `ReloadClass` and `ReloadFunction` will not be further analyzed here. If you are interested, you can directly refer to the [source code].(https://github.com/disenone/python_reloader)。

The entire Reload process can be summarized as putting new wine in old bottles. In order to keep the module/module functions/module classes/module data valid, we need to retain the references to these original objects (shells) and then update their specific data internally. For example, for functions, we update `__code__`, `__dict__`, and other data. When the function is executed, it will in turn execute the new code.

##Summary

This article provides a detailed introduction to the two hot update methods of Python3, each with its own corresponding use cases, hoping to be helpful to you. Feel free to reach out if you have any questions.

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
