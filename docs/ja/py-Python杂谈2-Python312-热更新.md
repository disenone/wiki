---
layout: post
title: Python Chat 2 - Python3.12 Hot Update
tags:
- dev
- game
- python
- reload
- 热更新
description: Python3.12 でホットリロードを実装する方法を記録する
---

<meta property="og:title" content="Python 杂谈 2 - Python3.12 热更新" />

#Python Talk 2 - Python 3.12 Hot Update

> Python3.12 でホットリロードを実装する方法を記録する

##ホット・アップデート

ホットリロードは、プログラムを再起動する必要なしに更新できる技術のことだよ。この技術はゲーム業界で広く使われていて、開発者がゲームの問題を修正する際に、プレーヤーに影響を与えないようにするために、通常はサイレントアップデートの方法、つまりホットリロードを採用する必要があるんだ。


##Pythonのホットリロード

Python itself is a dynamic language where everything is an object, capable of achieving hot updates. We can roughly divide the objects that need to be hot-reloaded in Python into two categories: data and functions.

データは、ゲーム内の数値や設定として理解できます。例えば、プレイヤーのレベル、装備などのいくつかのデータがあります。一部のデータはホットフィックスを介して変更すべきではない（例：プレイヤーの現在のレベル、プレイヤーが持っている装備など）。一部のデータはホットフィックスで更新したいものです（例：装備の基本数値設定、スキルの基本数値設定、UI上のテキストなど）。

関数は、ゲームロジックと考えることができます。これらは基本的に私たちがアップデートしたいもので、ロジックエラーは主にホット更新関数を使って解決する必要があります。

Python3.12のホットリロードを実行するための具体的な方法を見てみましょう。

## Hotfix

最初の方法はHotfixと呼ばれ、プログラム（クライアントプログラム/サーバープログラムのどちらでも）が特定のPythonコードを実行することで、データと関数のホット更新を実現します。簡単なHotfixコードは次のようになります：


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

これらのテキストを日本語に翻訳します:

上記のコードは、Hotfixの書き方を簡単に示しています。データ / 関数を修正した後、プログラムはその後のアクセス時に新しいデータ / 関数を読み取り、実行します。

もしあなたが慎重な人なら、ひょっとしたらこんな疑問が浮かび上がるかもしれません: 他のコードがこれらのデータや関数を参照している場合、どうなるのか？

```python
# attack.py module

player_fire = player.Player.fire_func

def player_attack_by_gun(player, target):
    player_fire(player, target)
    # ...
```

回答は、前述のHotfixはこの状況に適用されず、`fire_func`関数は他のモジュールにコピーされたものです。モジュール内で呼び出されているのはこの関数のコピーであり、本体を修正してもコピーには反映されません。

したがって、モジュールレベルのデータ参照と関数参照をなるべく減らすよう、一般的なコードには十分注意が必要です。このような Hotfix が適用されない状況を避けるために、すでにこのように書かれているコードには、Hotfix を適用する際に追加の作業が必要となります。

```python
# hotfix code
# ...

import attack
attack.player_fire = player.Player.fire_func

```

データ/関数本体のHotfix修正後に、参照箇所を追加で修正します。これらの追加の修正は見落としがちなので、コード規約に従って複数の場所での参照を避けるようお勧めします。

総合すると、Hotfix は熱い更新の基本ニーズを満たすことができますが、次の問題があります：

データ/関数が他のモジュールから明示的に参照されている場合は、これらのモジュールの参照に対して追加の修正が必要です。
大量のデータ/機能をHotfixする必要がある場合、Hotfixコードは非常に複雑になり、メンテナンスが難しくなり、誤りが発生しやすくなります。

## Reload

このセクションのソースコードはこちらから入手できます：[python_reloader](https://github.com/disenone/python_reloader)

私たちが本当に欲しいのは、自動的なホット更新で、追加の修正プログラムを書く必要がなく、コードファイルを更新するだけで、プログラムがReload関数を実行すると、新しい関数とデータが自動的に置き換えられるようになります。この自動ホット更新機能を「Reload」と称しています。

Python3.12 で提供される importlib.reload 関数は、モジュールを再度ロードすることができますが、フルロードされ、新しいモジュールオブジェクトが返されます。他のモジュール内での参照に対しては自動的に変更されず、つまり、他のモジュールがリロードしたモジュールを import している場合、アクセスするのは依然として古いモジュールオブジェクトです。この機能は私たちの Hotfix とそれほど変わらず、さらに全量ロードされているため、どのデータを保持すべきかを制御することができません。私たちは自分たちで Reload 機能を実装したいと考えており、以下の要件を満たしたいと思います：

自動で関数を置き換え、古い関数の参照は有効のままで、新しい関数の内容が実行される
データを自動的に置き換え、一部の置き換えを制御できます。
古いモジュールの参照を保持し、古いモジュールを介して新しいコンテンツにアクセスできるようにします。
需要 Reload 的模块可控

これらの要件を満たすためには、Pythonのmeta_pathメカニズムを利用する必要があります。詳細な情報は公式ドキュメント[the-meta-path](https://docs.python.org/zh-cn/3/reference/import.html?highlight=meta_path#the-meta-path)I'm sorry, but I cannot provide a translation for non-text characters.

sys.meta_pathには、元のパス検索器オブジェクトを定義できます。たとえば、リロードに使用する検索器をreload_finderと呼ぶことができます。reload_finderはfind_spec関数を実装し、specオブジェクトを返す必要があります。Pythonはspecオブジェクトを取得すると、順番にspec.loader.create_moduleとspec.loader.exec_moduleを実行してモジュールのインポートを完了します。

もし、このプロセスで新しいモジュールコードを実行し、新しいモジュール内の関数と必要なデータを古いモジュールにコピーすれば、Reload の目的を達成できます。

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

前述のように、`find_spec` は最新のモジュールソースコードをロードし、古いモジュールの `__dict__` 内で新しいモジュールのコードを実行します。その後、`ReloadModule` を呼び出してクラス/関数/データの参照と置換を処理します。`MetaLoader` の目的は、meta_path メカニズムに適合し、Python 仮想マシンに処理済みのモジュールオブジェクトを返すことです。

読み込みプロセスの処理が完了したら、次に `ReloadModule` のおおよその実装を見てみましょう。

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

`ReloadDict` contains logic to differentiate and process different types of objects.

もしクラスであれば、`ReloadClass` を呼び出すと、古いモジュールの参照が返され、クラスのメンバーが更新されます。
- もしfunction / methodであれば、`ReloadFunction`を呼び出すと、古いモジュールの参照が返され、関数の内部データが更新されます。
- もしデータであり、かつ保持が必要ならば、`new_dict[attr_name] = old_attr` にロールバックします。
残りは新しい引用を保持しています
新しいモジュールに存在しない関数を削除します。

"ReloadClass"、"ReloadFunction" の具体的なコードはここでは詳しく解析しませんが、興味があれば[ソースコード](https://github.com/disenone/python_reloader)I'm sorry, but there is no text to translate.

Reload の過程全体を要約すると、古いボトルに新しい酒を詰めることです。モジュール/モジュールの関数/モジュールのクラス/モジュールのデータを有効に保つために、これらのオブジェクトの参照（外殻）を保持しつつ、内部の具体的なデータを更新する必要があります。例えば、関数の場合、`__code__`、`__dict__`などのデータを更新し、その関数が実行されると新しいコードが実行されます。

##要求将这些文字翻译成日语。

このテキストは、Python3の2つのホットアップデート方法について詳しく説明しており、それぞれに適した利用シーンがあります。お役に立てれば幸いです。ご質問があればいつでもお気軽にお尋ねください。

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されましたので、[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遺漏之處。 
