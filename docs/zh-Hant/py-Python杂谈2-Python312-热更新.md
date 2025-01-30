---
layout: post
title: Python 閒談 2 - Python 3.12 熱更新
tags:
- dev
- game
- python
- reload
- 热更新
description: 記錄如何在 Python3.12 中實現熱更新。
---

<meta property="og:title" content="Python 杂谈 2 - Python3.12 热更新" />

#Python 談話 2 - Python3.12 熱更新

> 記錄如何在 Python3.12 中實現熱更新

##熱更新

熱更新（Hot Reload）可以理解為在不需要重啟程序的情況下對其進行更新的技術。這項技術在遊戲行業有廣泛的應用，開發者對遊戲問題進行修復的時候，為了不對玩家造成影響，往往需要採用一些靜默更新的方式，也就是熱更新。


##Python 熱更新

Python 本身是動態語言，一切皆是對象，是有能力做到熱更新的。我們可以粗略把 Python 中的需要熱更的對象分成兩種：數據 和 函數。

數據，可以理解成遊戲中的數值或者設定，例如玩家的等級、裝備等等一些數據，部分數據是不應該熱更的（例如玩家當前等級、玩家身上擁有哪些裝備，這些數據的修改不應該通過熱更來實現），部分數據是我們想要熱更的（例如裝備的基礎數值設定、技能的基礎數值設定、UI上的文字等等）。

函數，可以理解為遊戲邏輯，這基本上都是我們想要熱更的，邏輯錯誤基本上都需要通過熱更新函數來實現。

讓我們深入探討一下，有哪些方法可以對 Python3.12 進行熱更新。

## Hotfix

我們將這段文字翻譯為繁體中文：

第一種方法我們稱為 Hotfix，通過讓程式（客戶端程式 / 服務端程式都可以）執行一段特定的 Python 代碼，實現對數據和函數的熱更新。一段簡單的 Hotfix 代碼可能是這樣：


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

以上程式碼簡單展示了 Hotfix 的撰寫方式，當資料 / 函數被修改後，程式在後續存取時會讀取到新的資料 / 函數來執行。

如果你比較細緻，你可能會有一個疑問：那如果其他代碼裡面引用了這些需要修改的數據和函數，會發生什麼事情？

```python
# attack.py module

player_fire = player.Player.fire_func

def player_attack_by_gun(player, target):
    player_fire(player, target)
    # ...
```

答案是，前面的 Hotfix 對這種情況是不生效的，`fire_func` 這個函數相當於在其他模塊多了一份副本，該模塊中調用的是函數的副本，我們修改函數本體對副本不生效。

所以需要注意，一般代碼中儘量減少模塊級別的數據引用和函數引用，避免出現這種 Hotfix 不生效的情況，如果代碼已經是這樣寫的，Hotfix 需要多做一些工作：

```python
# hotfix code
# ...

import attack
attack.player_fire = player.Player.fire_func

```

在對數據 / 函數本體 Hotfix 修改之後，再額外對引用的地方進行修改。這些額外的修改很容易被遺漏，所以我們還是建議，從代碼規範上來儘量避免多處引用的寫法。

綜上所述，Hotfix 能滿足熱更的基本需求，同時存在以下問題：

如果資料/函數被其他模組明確引用，需要額外對這些模組的引用進行緊急修補。
如果有大量的資料/函數需要立即修正，那麼這些修正的程式碼會變得非常龐大，讓維護變得更難，也更容易出錯。

## Reload

本章的源碼可從這裡獲得：[python_reloader](https://github.com/disenone/python_reloader)

我們更希望的是自動熱更新，不需要額外編寫 Hotfix，只需更新程式碼文件，讓程序執行一個 Reload 函數即可自動替換新的函數和新的數據。我們將這個自動熱更新的功能稱為 Reload。

Python3.12 提供了 importlib.reload 函數，可以重新加載模組，但是卻是全量加載，並且返回新的模組物件，對於其他模組中的引用，並不能自動修改，也就是其他模組如果 import 了 reload 的模組，那麼訪問的依然是舊的模組物件。這個功能比我們的 Hotfix 好不了多少，更何況是全量 reload 模組，不能由我們控制哪些資料應該保留。我們想要自己實現一個 Reload 功能，滿足這些要求：

- 自動替換函數，同時舊函數的引用依然有效，並會執行新函數的內容
自動替換數據，同時可控制部分替換
保留舊模組的引用，透過舊模組就能存取到新的內容。
需要 Reload 的模組可控

要完成這些要求，我們需要借助 Python 內部 meta_path 的機制，詳細的介紹可以參考官方文檔 [the-meta-path](https://docs.python.org/zh-cn/3/reference/import.html?highlight=meta_path#the-meta-path)這些文字翻譯成繁體中文語言：

sys.meta_path 中可以定義我們的元路徑查找器物件，例如我們將用於 Reload 的查找器稱為 reload_finder，reload_finder 需要實現一個函數 find_spec 並返回 spec 物件。Python 收到 spec 物件後，將依次執行 spec.loader.create_module 和 spec.loader.exec_module 完成模組的匯入。

如果我們在這個過程中，執行新的模組代碼，並將新的模組裡面的函數和需要的數據複製到舊模組中，則可以達到 Reload 的目的：

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

如上，`find_spec` 會加載最新的模塊源碼，並在舊模塊的 `__dict__` 裡面執行新模塊的代碼，之後我們調用 `ReloadModule` 來處理類 / 函數 / 數據的引用和替換。`MetaLoader` 的目的是適配 meta_path 機制，給 Python 虛擬機返回我們處理過的模塊對象。

處理完載入的流程後，再來看 `ReloadModule` 的大致實現。

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

`ReloadDict` 裡面會區分處理不同類型的對象。

如果是 class，則調用 `ReloadClass`，會返回舊模塊的引用，並更新 class 的成員
- 如果是 function / method，則調用 `ReloadFunction`，會返回舊模塊的引用，並更新函數的內部數據
- 如果是數據，並且需要保留，則會回滾 `new_dict[attr_name] = old_attr`
其餘的都保持新的引用
刪除不存在於新模組中的函數

`ReloadClass`，`ReloadFunction` 的具體程式碼這裡不再展開分析，有興趣可以直接看[源碼](https://github.com/disenone/python_reloader)抱歉，我無法翻譯沒有內容的文字。您可以提供更多需要翻譯的文字嗎?

整個 Reload 的過程，可以概括為：舊瓶裝新酒。為了保持模組/模組的函數/模組的類/模組的數據有效，我們需要保留原來這些對象的引用（躯壳），轉而去更新它們內部的具體數據，例如對於函數，更新 `__code__`，`__dict__` 等數據，函數執行的時候，就會轉而執行新的代碼。

##總結

本文詳細介紹了 Python3 的兩種熱更新方式，每種都有相應的應用場景，希望能對你有幫助。有任何疑問歡迎隨時交流。

--8<-- "footer_tc.md"


> 此帖子是使用 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
