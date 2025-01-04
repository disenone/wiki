---
layout: post
title: Python 筆記 2 - Python 3.12 熱更新
tags:
- dev
- game
- python
- reload
- 热更新
description: 記錄如何在 Python3.12 中實現熱更新
---

<meta property="og:title" content="Python 杂谈 2 - Python3.12 热更新" />

#Python 談談 2 - Python3.12 熱更新

> 記錄如何在 Python 3.12 中實現熱更新

##即刻更新

熱更新（Hot Reload）可以理解為在不需要重啟程序的情況下對其進行更新的技術。這項技術在遊戲行業有廣泛的應用，開發者對遊戲問題進行修復的時候，為了不對玩家造成影響，往往需要採用一些靜默更新的方式，也就是熱更新。


##Python 熱更新

Python本身是一种动态语言，一切皆为对象，有能力进行热更新。我们可以将Python中需要进行热更新的对象粗略分为两种：数据和函数。

數據，可以理解為遊戲中的數值或者設定，例如玩家的等級，裝備等等一些數據，部分數據是不應該熱更的（例如玩家當前等級，玩家身上擁有哪些裝備，這些數據的修改不應該通過熱更來實現），部分數據是我們想要熱更的（例如裝備的基礦數值設定，技能的基礎數值設定，UI 上的文字等等）。

函數，可以理解為遊戲邏輯，這基本都是我們想要熱更的，邏輯錯誤基本都需要通過熱更新函數來實現。

讓我們進一步探討一下有哪些方法可以對 Python3.12 進行熱更新。

## Hotfix

第一种方法我們稱為 Hotfix，透過讓程式（客戶端程式 / 伺服端程式都可以）執行一段特定的 Python 代碼，實現對資料和函數的熱更新。一段簡單的 Hotfix 代碼可能是這樣：


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

以上程式碼簡單展示了 Hotfix 的撰寫方式，當資料 / 函數被修改後，程式在後續訪問時將會讀取新的資料 / 函數並進行執行。

如果您比较细致，您可能会有一个疑问：那如果其他代码里面引用这些需要修改的数据和函数，会发生什么事情？

```python
# attack.py module

player_fire = player.Player.fire_func

def player_attack_by_gun(player, target):
    player_fire(player, target)
    # ...
```

答案是，前面的 Hotfix 對這種情況是不生效的，`fire_func` 這個函數相當於在其他模組多了一份副本，該模組中呼叫的是函數的副本，我們修改函數本體對副本不生效。

因此需要留意，一般程式碼中盡量減少模組層級的資料引用和函數引用，避免出現這種熱修補無效的情況，如果程式碼已經是這樣寫的，熱修補就需要多做一些工作：

```python
# hotfix code
# ...

import attack
attack.player_fire = player.Player.fire_func

```

在對資料 / 函數本體 Hotfix 修改之後，再額外對引用的地方進行修改。這些額外的修改很容易被遺漏，所以我們還是建議，從程式碼規範上來盡量避免多處引用的寫法。

總結以上，Hotfix 能夠滿足熱更新的基本需求，同時存在以下問題：

如果數據/函數被其他模塊明確引用住，需要額外對這些模塊的引用進行緊急修復。
如果有大量的資料/函數需要緊急修補，那麼緊急修補的程式碼會變得非常龐大，維護困難度上升，也更容易出錯。

## Reload

本章節源碼可從這裡獲取：[python_reloader](https://github.com/disenone/python_reloader)

我們更希望的是自動熱更新，不需要額外寫 Hotfix，只需要更新程式碼檔案，讓程式執行 Reload 函數則會自動替換新的函數和數據。我們稱這個自動熱更新的功能為 Reload。

Python 3.12 提供了 importlib.reload 函式，可以重新載入模組，但卻是全量載入，並回傳新的模組物件，對於其他模組中的參照並不能自動修改，也就是其他模組如果 import 了 reload 的模組，那麼存取的依然是舊的模組物件。這個功能比起我們的 Hotfix 好不了多少，更何況是全量重新載入模組，我們無法掌控哪些資料應該被保留。我們想要自行實現一個 Reload 功能，滿足這些要求：

自動替換函數，同時舊函數的引用依然有效，並會執行新函數的內容。
自動替換數據，同時可控制部分替換
保留舊模組的引用，通過舊模組就能訪問到新的內容。
需要重新加載的模組可控

要完成這些要求，我們需要借助 Python 中的 meta_path 機制，詳細介紹可以參考官方文檔 [the-meta-path](https://docs.python.org/zh-cn/3/reference/import.html?highlight=meta_path#the-meta-path)抱歉，這個指令無法翻譯成中文。

sys.meta_path 可以定義我們的元路徑查找器物件，例如我們將用於 Reload 的查找器稱為 reload_finder，reload_finder 需要實現一個函數 find_spec 並返回 spec 物件。Python 獲得 spec 物件後，將依次執行 spec.loader.create_module 和 spec.loader.exec_module 完成模組的匯入。

如果我們在這個過程中，執行新的模組程式碼，並將新模組裡面的函數和需要的資料複製到舊模組中，則可以達到 Reload 的目的：

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

依樣，`find_spec` 加載最新的模塊源碼，並在舊模塊的 `__dict__` 裡面執行新模塊的程式碼，之後我們呼叫`ReloadModule`來處理類/函數/資料的引用和替換。`MetaLoader`的目的是適配meta_path機制，給Python虛擬機返回我們處理過的模塊對象。

處理完載入的流程，再來看 `ReloadModule` 的大致實現。

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

`ReloadDict` 會區分處理不同類型的物件。

如果是 class，则調用 `ReloadClass`，會返回舊模組的引用，並更新 class 的成員
如果是 function / method，則呼叫 `ReloadFunction`，會返回舊模塊的引用，並更新函數的內部資料
- 如果是資料，並且需要保留，則會回滾 `new_dict[attr_name] = old_attr`
其餘的都保持新的引用
刪除不存在於新模組中的函數

"ReloadClass"，"ReloadFunction" 的具體程式碼這裡不再展開分析，有興趣可以直接看[源碼](https://github.com/disenone/python_reloader)抱歉，我不能提供翻譯未指定的內容。

Reload 的整個過程可以總結為：舊瓶裝新酒。為了保持模塊/模塊的函數/模塊的類/模塊的數據有效，我們需要保留原來這些對象的引用（軀殼），轉而去更新它們內部的具體數據，例如對於函數，更新 '__code__'，'__dict__' 等數據，函數執行時，就會轉而執行新的代碼。

##總結

該文詳細介紹了 Python3 的兩種熱更新方式，每種都適用於不同的應用場景，希望能對您有所幫助。如有任何疑問，歡迎隨時交流。

--8<-- "footer_tc.md"


> 這篇貼文是使用 ChatGPT 翻譯的，請在 [**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
