---
layout: post
title: 파이썬 이야기 2 - 파이썬 3.12 핫 업데이트
tags:
- dev
- game
- python
- reload
- 热更新
description: 파이썬 3.12에서 핫 업데이트를 구현하는 방법 기록
---

<meta property="og:title" content="Python 杂谈 2 - Python3.12 热更新" />

#Python 얘기 2 - Python 3.12 업데이트하기

> 파이썬 3.12에서 핫 업데이트를 구현하는 방법을 기록하세요.

##실시간 업데이트

핫 리로드(Hot Reload)는 프로그램을 다시 시작하지 않고 업데이트하는 기술을 의미합니다. 이 기술은 게임 산업에서 널리 사용되며, 개발자가 게임 문제를 해결할 때 플레이어에게 영향을 미치지 않도록 정적 업데이트 방식인 핫 업데이트를 사용하기도 합니다.


##Python 업데이트.

파이썬은 원래 동적 언어로 모든 것이 객체이며 업데이트를 적용할 수 있는 능력이 있습니다. 파이썬에서 업데이트가 필요한 객체는 데이터와 함수 두 가지로 대략 분류할 수 있습니다.

데이터는 게임에서 숫자나 설정으로 이해될 수 있습니다. 예를 들어 플레이어의 레벨, 장비 등과 같은 일부 데이터는 핫 업데이트되어서는 안 됩니다. 플레이어의 현재 레벨이나 소유한 장비와 같은 데이터의 변경은 핫 업데이트를 통해 이루어지면 안 됩니다. 일부 데이터는 업데이트가 필요할 수 있습니다. 예를 들어 장비의 기본 숫자 설정, 기술의 기본 숫자 설정, UI의 텍스트 등이 있습니다.

함수는 게임 로직으로 이해할 수 있으며, 대부분은 업데이트를 원하는 부분이라고 볼 수 있습니다. 로직 오류는 주로 업데이트 함수를 통해 해결해야 합니다.

Python 3.12를 업데이트 하는 방법에 대해 구체적으로 살펴보겠습니다.

## Hotfix

첫 번째 방법은 Hotfix라고 부르며, 특정 Python 코드를 실행하여 데이터 및 함수를 업데이트하는 것을 의미합니다. 간단한 Hotfix 코드는 다음과 같을 수 있습니다:


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

상기 코드는 Hotfix 작성 방법을 간단히 보여줍니다. 데이터/함수를 수정한 후 프로그램이 이후 접근할 때 새로운 데이터/함수를 읽고 실행합니다.

만약 신중하게 살펴보면 궁금증이 생길 수도 있어요: 다른 코드에서 이러한 수정이 필요한 데이터와 함수를 참조하고 있다면 무슨 일이 발생할까요?

```python
# attack.py module

player_fire = player.Player.fire_func

def player_attack_by_gun(player, target):
    player_fire(player, target)
    # ...
```

해답은, 이 상황에 대한 이전의 Hotfix가 작동하지 않습니다. `fire_func` 함수는 다른 모듈에 복사본을 추가한 것과 같습니다. 해당 모듈에서 호출하는 것은 함수의 복사본이므로 우리가 함수 원본을 수정해도 복사본에는 영향을 주지 않습니다.

그래서 주의해야 할 점은, 일반적으로 코드에서 모듈 수준의 데이터 및 함수 참조를 최대한 줄이고, Hotfix가 작동되지 않는 경우를 피해야합니다. 코드가 이미 이렇게 작성되어 있다면, Hotfix 작업을 조금 더 해야합니다:

```python
# hotfix code
# ...

import attack
attack.player_fire = player.Player.fire_func

```

데이터/함수 핵심 부분을 수정한 후, 참조된 곳을 추가로 수정하십시오. 이러한 추가 수정은 쉽게 누락될 수 있으므로 여전히 코드 규칙을 준수하여 다중 참조 방식을 피하는 것이 좋습니다.

상기하여, 핫픽스는 핫 업데이트의 기본 요구 사항을 충족시킬 수 있지만 다음과 같은 문제가 존재합니다:

만약 데이터/함수가 다른 모듈에 명시적으로 참조되고 있다면, 해당 모듈들에 대한 참조에 대한 긴급 수정이 필요합니다.
대량의 데이터/함수를 수정해야 되면, 수정 부분이 점점 커져서 유지보수가 어려워지며, 실수하기 쉬워집니다.

## Reload

이 장의 소스 코드는 여기서 받을 수 있습니다: [python_reloader](https://github.com/disenone/python_reloader)

우리가 가장 원하는 것은 자동 업데이트인데, Hotfix를 따로 작성할 필요 없이 코드 파일을 업데이트하고 프로그램에서 Reload 함수를 실행하면 자동으로 새 함수와 새 데이터로 교체됩니다. 우리는 이 자동 업데이트 기능을 "Reload"라고 부릅니다.

파이썬 3.12에서는 importlib.reload 함수를 제공하는데, 이 함수를 사용하면 모듈을 다시로드할 수 있지만 전체적으로 다시 로드하게 되며 새로운 모듈 객체를 반환합니다. 다른 모듈에서의 참조는 자동으로 업데이트되지 않습니다. 즉, 다른 모듈이 다시로드된 모듈을 import하면 여전히 기존 모듈 개체에 액세스하게 됩니다. 이 기능은 우리의 Hotfix와 별로 다를 게 없습니다. 특히 모듈을 전체적으로 다시로드하게 되면 어떤 데이터를 유지해야 하는지 우리가 제어할 수 없습니다. 우리는 이러한 요구 사항을 충족하는 Reload 기능을 직접 구현하고자 합니다:

- 자동으로 함수를 대체하여, 기존 함수를 여전히 유효하게 유지하면서 새 함수의 내용을 실행합니다.
자동으로 데이터를 교체하며 동시에 일부 교체를 제어할 수 있습니다.
기존 모듈의 참조를 유지하여 기존 모듈을 통해 새로운 내용에 접근할 수 있습니다.
Reload 가능한 모듈이 필요합니다.

이러한 요구 사항을 완수하려면 Python의 meta_path 메커니즘을 활용해야 합니다. 자세한 내용은 공식 문서 [the-meta-path](https://docs.python.org/zh-cn/3/reference/import.html?highlight=meta_path#the-meta-path)Sorry, I can't provide a translation for the text ".", as it does not contain any meaningful content.

sys.meta_path 내에서는 우리의 메타 경로 검색기 객체를 정의할 수 있습니다. 예를 들어, 다시로드에 사용되는 검색기를 reload_finder라고합니다. reload_finder는 find_spec 함수를 구현하고 spec 객체를 반환해야합니다. Python은 spec 객체를받은 후에 spec.loader.create_module 및 spec.loader.exec_module을 순서대로 실행하여 모듈을 가져옵니다.

만약 새 모듈 코드를 실행하고 새 모듈 내의 함수와 필요한 데이터를 이전 모듈로 복사한다면, 다시로드하는 목적을 달성할 수 있습니다.

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

위와 같이, `find_spec`는 최신 모듈 소스 코드를로드하고 이전 모듈의 `__dict__`에서 새 모듈 코드를 실행합니다. 그런 다음 `ReloadModule`을 호출하여 클래스/함수/데이터의 참조 및 대체를 처리합니다. `MetaLoader`의 목적은 meta_path 메커니즘을 적응시키고 Python 가상 머신에 처리 된 모듈 객체를 반환하는 것입니다.

로드된 프로세스를 처리한 후, `ReloadModule`의 대략적인 구현을 살펴보겠습니다.

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

`ReloadDict` 내부에서는 다른 유형의 객체를 구분하여 처리합니다.

만약 class인 경우, `ReloadClass`를 호출하면 이전 모듈의 참조를 반환하고 class의 멤버를 업데이트할 거야.
- 만약 함수 / 메소드인 경우, 'ReloadFunction'을 호출하면 이전 모듈의 참조를 반환하고 함수 내부 데이터를 업데이트합니다.
- 데이터인 경우 유지해야하면 롤백됩니다 `new_dict[attr_name] = old_attr`
나머지는 모두 새 인용을 유지하십시오.
존재하지 않는 새 모듈의 함수를 제거하십시오.

`ReloadClass`와 `ReloadFunction`의 구체적인 코드는 여기에서 더 이상 분석하지 않겠습니다. 관심이 있다면 직접 [소스 코드](https://github.com/disenone/python_reloader)"。" -> "。"

전체 Reload 과정은 기존 정보를 새로운 컨텍스트에 맞게 재구성하는 것으로 요약될 수 있습니다. 모듈 또는 모듈의 함수, 클래스, 데이터를 유효하게 유지하기 위해서, 우리는 기존 객체의 참조를 유지해야 합니다. 이후 내부의 구체적 데이터를 갱신하여 새로운 코드를 실행할 수 있습니다.

##요약

본문에서는 Python3의 두 가지 업데이트 방법을 자세히 설명하고, 각각이 적합한 응용 시나리오를 소개했습니다. 도움이 되었으면 좋겠습니다. 궁금한 점이 있으면 언제든지 질문해 주세요.

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT를 사용하여 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)어떤 빠진 부분도 지적해 주세요. 
