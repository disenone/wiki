---
layout: post
title: Python Discussion 2 - Python3.12 Hot Update
tags:
- dev
- game
- python
- reload
- 热更新
description: Python3.12におけるホットリロードの実装方法の記録
---

<meta property="og:title" content="Python 杂谈 2 - Python3.12 热更新" />

#Python Talk 2 - Python 3.12 Hot Reload

> Python3.12 におけるホットアップデートの実装方法を記録する

##ホットリロード

ホットリロード（Hot Reload）は、プログラムを再起動することなく更新できる技術と理解できます。この技術はゲーム業界で広く利用されており、開発者がゲームの問題を修正する際に、プレイヤーに影響を与えないように、静かな更新方法、つまりホットリロードを採用することがよくあります。


##Pythonのホットリロード

Pythonは動的な言語であり、すべてがオブジェクトであり、ホットリロードが可能です。私たちは、Pythonにおいてホットリロードが必要なオブジェクトを大まかに二つに分けることができます：データと関数です。

データは、ゲーム内の数値や設定として考えることができます。たとえば、プレイヤーのレベル、装備などのいくつかのデータがあります。一部のデータはホットフィックスで更新すべきではない（たとえば、プレイヤーの現在のレベルや所持している装備などの変更はホットフィックスによって行うべきではありません）。一部のデータは更新したいと考えています（たとえば、装備の基本数値設定、スキルの基本数値設定、UI上のテキストなど）。

関数はゲームのロジックとして理解できます。これが基本的に私たちがホットアップデートしたいものです。ロジックのエラーは基本的にホットアップデート関数を通じて実現する必要があります。

Python3.12をホットアップデートする方法について具体的に見ていきましょう。

## Hotfix

最初の方法はHotfixと呼ばれ、プログラム（クライアントプログラム/サーバープログラムのどちらでも）が特定のPythonコードを実行することで、データと関数の熱い更新を実現します。簡単なHotfixコードは次のようになります：


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

以上のコードは、Hotfix の書き方を簡単に示しています。データ / 関数の変更後、プログラムがその後アクセスする際には新しいデータ / 関数を読み込んで実行します。

もしあなたが細かいことを気にするタイプであれば、次のような疑問が浮かぶかもしれません：他のコードがこれらの修正が必要なデータや関数を参照している場合、何が起こるのでしょうか？

```python
# attack.py module

player_fire = player.Player.fire_func

def player_attack_by_gun(player, target):
    player_fire(player, target)
    # ...
```

解答は、前のHotfixではこの状況に対して効果がありません。`fire_func` 関数は他のモジュールにコピーされたものです。モジュール内で呼び出されるのは関数のコピーであり、本体を変更してもコピーには影響しません。

したがって、一般的なコードでは、モジュールレベルのデータ参照や関数参照をできるだけ減らす必要があります。このようなHotfixが機能しない状況を避けるためです。もしコードがすでにこのように書かれている場合、Hotfixはより多くの作業を必要とします。

```python
# hotfix code
# ...

import attack
attack.player_fire = player.Player.fire_func

```

データ/関数本体のHotfixを修正した後、引用された部分に対しても追加の修正を行います。これらの追加修正は見落とされやすいため、コード規範の観点から、できる限り複数の引用を避けることをお勧めします。

以上を踏まえると、ホットフィックスはアップデートの基本的なニーズを満たすことができますが、以下の問題が存在しています：

他がそれらのモジュールに明示的に参照されるデータ/関数が存在する場合、これらのモジュールへの参照を追加で修正する必要があります。Hotfix
- 大量のデータや関数にホットフィックスが必要な場合、ホットフィックスのコードが非常に大きくなり、メンテナンスが難しくなり、ミスが起こりやすくなります。

## Reload

本章のソースコードはここから入手できます：[python_reloader](https://github.com/disenone/python_reloader)

私たちがもっと望んでいるのは、自動ホット更新であり、追加でHotfixを書く必要はなく、コードファイルを更新するだけで、プログラムがReload関数を実行すれば自動的に新しい関数と新しいデータに置き換わるということです。この自動ホット更新の機能をReloadと呼んでいます。

Python3.12 で導入された importlib.reload 関数はモジュールを再読み込みする機能を提供していますが、全体的な再読み込みとして新しいモジュールオブジェクトを返すため、他のモジュールでの参照は自動的に変更されません。つまり、他のモジュールが reload されたモジュールを import した場合でも、アクセスするのは古いモジュールオブジェクトのままです。この機能は私たちの Hotfix とそれほど変わらないし、しかも全体的なモジュール再読み込みであり、どのデータを保持すべきかを制御できません。したがって、これらの要求を満たすために独自の Reload 機能を実装したいと考えています：

自動関数置換機能は、古い関数への参照を保持し、新しい関数の内容を実行します。
データを自動的に置換し、一部の置換を制御できます。
古いモジュールの参照を保持し、古いモジュールを介して新しいコンテンツにアクセスできるようにします。
- 需要 Reload のモジュールは制御可能です

これらの要件を満たすためには、Python の meta_path メカニズムを利用する必要があります。詳しい説明は公式ドキュメント [the-meta-path](https://docs.python.org/zh-cn/3/reference/import.html?highlight=meta_path#the-meta-path)I'm sorry, but there is nothing to translate in the text you provided.

sys.meta_path内で、私たちのメタパスファインダーオブジェクトを定義できます。例えば、リロードに使用するファインダーをreload_finderと呼ぶことができます。このreload_finderは、find_spec関数を実装してspecオブジェクトを返す必要があります。Pythonはspecオブジェクトを取得すると、順番にspec.loader.create_moduleおよびspec.loader.exec_moduleを実行してモジュールのインポートを完了します。

もし新しいモジュールのコードを実行し、新しいモジュール内の関数と必要なデータを古いモジュールにコピーすることで、Reload の目的を達成できます。

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

上記の通り、`find_spec` は最新のモジュールのソースコードをロードし、古いモジュールの `__dict__` 内で新しいモジュールのコードを実行します。その後、クラス/関数/データの参照と置換を処理するために `ReloadModule` を呼び出します。`MetaLoader` の目的は、meta_path メカニズムに適合し、Python仮想マシンに私たちが処理したモジュールオブジェクトを返すことです。

ロードされたプロセスを処理した後、`ReloadModule` のおおよその実装を見てみましょう。

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

`ReloadDict` の中では、異なるタイプのオブジェクトを区別して処理します。

- もしクラスであれば、`ReloadClass`を呼び出します。これにより、古いモジュールの参照が返され、クラスのメンバーが更新されます。
- 関数/メソッドの場合、`ReloadFunction`を呼び出すと、古いモジュールの参照が返され、関数の内部データが更新されます。
- もしデータであり、かつ保持する必要がある場合は、`new_dict[attr_name] = old_attr` にロールバックされます。
- 他のすべては新しい引用を保持してください。
- 存在しない関数を新しいモジュールから削除する

`ReloadClass`と`ReloadFunction`の具体的なコードはここでは詳細に分析しませんが、興味があれば直接[ソースコード](https://github.com/disenone/python_reloader)。

Reload 全体の過程は、古いボトルに新しい酒を詰めると言える。モジュール/モジュールの関数/モジュールのクラス/モジュールのデータを有効に保つためには、これらのオブジェクトの参照（外部構造）を保持し、それらの内部データを更新する必要があります。たとえば、関数の場合、`__code__`、`__dict__`などのデータを更新し、関数が実行されると、新しいコードが実行されるようになります。

##まとめ

本稿では、Python3の2つのホットリロード方法について詳しく説明します。それぞれに対応する適用シーンがあり、あなたにとって役立つことを願っています。何か疑問があれば、いつでもお気軽にご相談ください。

--8<-- "footer_ja.md"


> この投稿はChatGPTで翻訳されました。フィードバックは[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。 
