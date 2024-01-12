---
layout: post
title: Python 杂谈 2 - Python3.12 热更新
tags: [dev, game, python, reload, 热更新]
description: 记录如何在 Python3.12 中实现热更新
---
<meta property="og:title" content="Python 杂谈 2 - Python3.12 热更新" />

# Python 杂谈 2 - Python3.12 热更新

> 记录如何在 Python3.12 中实现热更新

## 热更新

热更新（Hot Reload）可以理解在不需要重启程序的情况下对其进行更新的技术。这项技术在游戏行业有广泛的应用，开发者对游戏问题进行修复的时候，为了不对玩家造成影响，往往需要采用一些静默更新的方式，也就是热更新。


## Python 热更新

Python 本身是动态语言，一切皆是对象，是有能力做到热更新的。我们可以粗略把 Python 中的需要热更的对象分成两种：数据 和 函数。

数据，可以理解成游戏中的数值或者设定，譬如玩家的等级，装备等等一些数据，部分数据是不应该热更的（譬如玩家当前等级，玩家身上拥有哪些装备，这些数据的修改不应该通过热更来实现），部分数据是我们想要热更的（譬如装备的基础数值设定，技能的基础数值设定，UI 上的文字等等）。

函数，可以理解成游戏逻辑，这基本都是我们想要热更的，逻辑错误基本都需要通过热更新函数来实现。

下面我们来具体看看有什么方法可以对 Python3.12 执行热更新。

## Hotfix

第一种方法我们叫做 Hotfix，通过让程序（客户端程序 / 服务端程序都可以）执行一段特定的 Python 代码，实现对数据和函数的热更新。一段简单的 Hotfix 代码可能是这样：


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

以上代码简单展示 Hotfix 的写法，数据 / 函数修改之后，程序后续访问的时候就会读到新的数据 / 函数来执行。

如果你比较细致，你可能会有一个疑问：那如果其他代码里面引用住了这些需要修改数据和函数，会发生什么事情？

```python
# attack.py module

player_fire = player.Player.fire_func

def player_attack_by_gun(player, target):
    player_fire(player, target)
    # ...
```

答案是，前面的 Hotfix 对这种情况是不生效的，`fire_func` 这个函数相当于在其他模块多了一份副本，该模块中调用的是函数的副本，我们修改函数本体对副本不生效。

所以需要注意，一般代码中尽量减少模块级别的数据引用和函数引用，避免出现这种 Hotfix 不生效的情况，如果代码已经是这样写的，Hotfix 需要多做一些工作：

```python
# hotfix code
# ...

import attack
attack.player_fire = player.Player.fire_func

```

在对数据 / 函数本体 Hotfix 修改之后，再额外对引用的地方进行修改。这些额外的修改很容易被遗漏，所以我们还是建议，从代码规范上来尽量避免多处引用的写法。

综上，Hotfix 能满足热更的基本需求，同时存在以下问题：

- 如果数据/函数被其他模块明确引用住，需要额外对这些模块的引用 Hotfix
- 如果有大量的数据/函数需要 Hotfix，那么 Hotfix 的代码会变得很庞大，维护难度上升，也更容易出错

## Reload

本章节源码可从这里获得：[python_reloader](https://github.com/disenone/python_reloader)

我们更想要的是自动热更新，不需要额外写 Hotfix，只需要更新代码文件，让程序执行一个 Reload 函数则会自动替换新的函数和新的数据。我们把这个自动热更新的功能叫做 Reload。

Python3.12 提供了 importlib.reload 函数，可以重新加载模块，但是却是全量加载，并且返回新的模块对象，对于其他模块中的引用，并不能自动修改，也就是其他模块如果 import 了 reload 的模块，那么访问的依然是旧的模块对象。这个功能比我们的 Hotfix 好不了多少，更何况是全量 reload 模块，不能由我们控制哪些数据应该保留。我们想要自己实现一个 Reload 功能，满足这些要求：

- 自动替换函数，同时旧函数的引用依然有效，并会执行新函数的内容
- 自动替换数据，同时可控制部分替换
- 保留旧模块的引用，通过旧模块就能访问到新的内容
- 需要 Reload 的模块可控

要完成这些要求，我们需要借助 Python 里面 meta_path 的机制，详细的介绍可以看官方文档 [the-meta-path](https://docs.python.org/zh-cn/3/reference/import.html?highlight=meta_path#the-meta-path)。

sys.meta_path 里面可以定义我们的元路径查找器对象，譬如我们把用于 Reload 的查找器叫做 reload_finder，reload_finder 需要实现一个函数 find_spec 并返回 spec 对象。Python 拿到 spec 对象后，会依次执行 spec.loader.create_module 和 spec.loader.exec_module 完成模块的导入。

如果我们在这个过程中，执行新的模块代码，并把新的模块里面的函数和需要的数据复制到旧模块中，则可以达到 Reload 的目的：

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

如上，`find_spec` 加载最新的模块源码，并在旧模块的 `__dict__` 里面执行新模块的代码，之后我们调用 `ReloadModule` 来处理类 / 函数 / 数据的引用和替换。`MetaLoader` 的目的是适配 meta_path 机制，给 Python 虚拟机返回我们处理过的模块对象。

处理完加载的流程，再来看 `ReloadModule` 的大致实现

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

`ReloadDict` 里面会区分处理不同类型的对象

- 如果是 class，则调用 `ReloadClass`，会返回旧模块的引用，并更新 class 的成员
- 如果是 function / method ，则调用 `ReloadFunction`，会返回旧模块的引用，并更新函数的内部数据
- 如果是数据，并且需要保留，则会回滚 `new_dict[attr_name] = old_attr`
- 其余的都保持新的引用
- 删除新模块不存在的函数

`ReloadClass`，`ReloadFunction` 的具体代码这里不再展开分析，有兴趣可以直接看[源码](https://github.com/disenone/python_reloader)。

整个 Reload 的过程，可以概括为：旧瓶装新酒。为了保持模块/模块的函数/模块的类/模块的数据有效，我们需要保留原来的这些对象的引用（躯壳），转而去更新它们内部的具体数据，譬如对于函数，更新 `__code__`，`__dict__` 等数据，函数执行的时候，就会转而执行新的代码。

## 总结

本文详细介绍了 Python3 的两种热更新方式，每种都有相应的应用场景，希望能对你有帮助。有任何疑问欢迎随时交流。

--8<-- "footer.md"

