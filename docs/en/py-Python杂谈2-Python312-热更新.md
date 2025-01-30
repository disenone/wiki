---
layout: post
title: Python Chat 2 - Python 3.12 Hot Update
tags:
- dev
- game
- python
- reload
- 热更新
description: Record how to implement hot updates in Python 3.12.
---

<meta property="og:title" content="Python 杂谈 2 - Python3.12 热更新" />

#Python Chat 2 - Python 3.12 Hot Update

> How to implement hot reloading in Python 3.12

##Hot update

Hot Reload is a technology that allows updates to be made to a program without the need for a restart. This technique is widely used in the gaming industry. When developers need to fix issues in games without affecting players, they often resort to silent updates, also known as Hot Reload.


##Python hot update

Python itself is a dynamic language where everything is an object, capable of hot updating. We can roughly categorize the objects that need hot updates in Python into two types: data and functions.

Data can be understood as the numerical values or settings within a game, such as the player's level, equipment, and so on. Some data should not be hot-updated (for example, the player's current level and which equipment the player possesses; modifications to this data should not be implemented through hot updates), while there is other data that we want to hot-update (for instance, the base numerical settings for equipment, the base numerical settings for skills, text on the UI, etc.).

Functions can be understood as game logic, which is basically what we want to hotfix. Logic errors generally need to be addressed through hot update functions.

Now let's take a closer look at the specific methods available for implementing hot updates in Python 3.12.

## Hotfix

The first method we call Hotfix, which allows the program (either client-side or server-side) to execute a specific piece of Python code to achieve hot updates for data and functions. A simple Hotfix code might look like this:


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

The above code simply demonstrates how to write a hotfix. After modifying the data/functions, the program will read the new data/functions for execution when accessed later.

If you are being meticulous, you might have a question: What will happen if other parts of the code reference the data and functions that need to be modified?

```python
# attack.py module

player_fire = player.Player.fire_func

def player_attack_by_gun(player, target):
    player_fire(player, target)
    # ...
```

The answer is that the previous Hotfix does not apply to this situation. The `fire_func` function is essentially an additional copy in another module; the copy is what is called in that module, and modifications to the original function do not affect the copy.

Therefore, it is important to be cautious and minimize module-level data and function references in the code to avoid situations where Hotfix does not take effect. If the code is already written this way, additional work is needed for the Hotfix to work properly:

```python
# hotfix code
# ...

import attack
attack.player_fire = player.Player.fire_func

```

After making the Hotfix modifications to the data / function body, additional changes should be made in the places where it is referenced. These extra modifications can easily be overlooked, so we recommend, from a coding standards perspective, to avoid writing multiple references as much as possible.

Taking everything into consideration, Hotfix can meet the basic requirements of real-time updates, but it also faces the following issues:

- If the data/function is explicitly referenced by other modules, an additional Hotfix for the references of these modules is required.
If there is a large amount of data/functions that need to be hotfixed, the code for the hotfix will become very large, increasing maintenance difficulty and making it more prone to errors.

## Reload

The source code for this chapter can be obtained from here: [python_reloader](https://github.com/disenone/python_reloader)

What we really want is automatic hot reloading, without the need to write additional hotfixes. Simply updating the code files and having the program execute a Reload function will automatically replace the new functions and data. We call this automatic hot reloading feature Reload.

Python 3.12 introduces the importlib.reload function, which allows for the reloading of modules. However, it performs a full reload and returns a new module object. References in other modules are not automatically updated; this means that if other modules have imported the reloaded module, they will still access the old module object. This functionality is not significantly better than our Hotfix, especially considering the full module reload, which we cannot control in terms of which data should be retained. We want to implement our own Reload feature that meets these requirements:

Automatically replace the function while preserving the validity of the old function's references, and executing the content of the new function.
Automatically replace data, while also being able to control partial replacements.
Retain references to the old module, so that the new content can be accessed through the old module.
Modules that require reloading can be controlled.

To fulfill these requirements, we need to leverage the meta_path mechanism in Python. A detailed introduction can be found in the official documentation [the-meta-path](https://docs.python.org/zh-cn/3/reference/import.html?highlight=meta_path#the-meta-path).

You can define our meta-path finder object in sys.meta_path, for example, if we name the finder used for reloading as reload_finder, reload_finder needs to implement a function find_spec and return a spec object. After Python obtains the spec object, it will sequentially execute spec.loader.create_module and spec.loader.exec_module to complete the module importation.

If we execute the new module code during this process and copy the functions and necessary data from the new module into the old module, we can achieve the purpose of Reload.

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

As mentioned above, `find_spec` loads the latest source code of the module and executes the new module's code within the `__dict__` of the old module. After that, we call `ReloadModule` to handle the references and replacements of classes/functions/data. The purpose of `MetaLoader` is to adapt to the meta_path mechanism, returning the processed module objects to the Python virtual machine.

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

The 'ReloadDict' will differentiate and process objects of different types inside.

- If it is a class, then calling `ReloadClass` will return a reference to the old module and update the class's members.
If it is a function/method, calling `ReloadFunction` will return a reference to the old module and update the internal data of the function.
If it's data and needs to be preserved, it will roll back to `new_dict[attr_name] = old_attr`.
Keep the rest of the citations fresh.
Remove functions that do not exist in the new module.

The specific code for `ReloadClass` and `ReloadFunction` will not be further analyzed here, if you are interested, you can directly refer to the [source code](https://github.com/disenone/python_reloader).

The entire Reload process can be summarized as: new wine in an old bottle. To maintain the validity of the module's functions/classes/data, we need to keep references to the original objects (shells) and instead update the specific data inside them. For example, for functions, we update the `__code__`, `__dict__`, and other data, so that when the function is executed, it will run the new code.

##Summary

This article provides a detailed introduction to two hot update methods in Python 3, each suitable for specific scenarios. I hope it can be helpful to you. Feel free to ask if you have any questions or need further clarification.

--8<-- "footer_en.md"


> This post has been translated using ChatGPT. Please provide feedback in [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Please point out any omissions. 
