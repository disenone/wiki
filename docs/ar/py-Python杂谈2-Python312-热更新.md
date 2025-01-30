---
layout: post
title: بايثون دردشة 2 - بايثون 3.12 تحديثات ساخنة
tags:
- dev
- game
- python
- reload
- 热更新
description: سجل كيفية تنفيذ التحديث الساخن في Python3.12
---

<meta property="og:title" content="Python 杂谈 2 - Python3.12 热更新" />

#بايثون الحديث 2 - تحديثات ساخنة في بايثون 3.12.

> 记录如何在 Python3.12 中实现热更新

##التحديث الساخن

إعادة التحميل السريع (Hot Reload) هي التقنية التي تسمح بتحديث البرنامج دون الحاجة إلى إعادة تشغيله. تُستخدم هذه التقنية على نطاق واسع في صناعة الألعاب، حيث يحتاج المطورون إلى إصلاح مشكلات اللعبة دون التأثير على اللاعبين، لذا غالبًا ما يلجأون إلى طرق تحديث صامتة تُعرف باسم إعادة التحميل السريع.


##تحديث بيثون الحيّ.

بايثون هي لغة ديناميكية، كل شيء فيها هو كائن، ولديها القدرة على التحديث الساخن. يمكننا تقريبا تقسيم الكائنات التي تحتاج إلى تحديث ساخن في بايثون إلى نوعين: البيانات والدوال.

يمكن فهم البيانات كقيم أو إعدادات داخل اللعبة، مثل مستوى اللاعب والمعدات وما إلى ذلك من بيانات، بعض البيانات لا ينبغي تحديثها بشكل ساخن (مثل مستوى اللاعب الحالي، المعدات التي يمتلكها اللاعب، ينبغي ألا تتم تعديل هذه البيانات من خلال التحديث الساخن)، والبعض الآخر من البيانات هو ما نريد تحديثه بشكل ساخن (مثل إعدادات القيم الأساسية للمعدات، إعدادات القيم الأساسية للمهارات، النصوص على واجهة المستخدم، وما إلى ذلك).

يمكن فهم الدوال على أنها منطق اللعبة، وهذا ما نرغب عادةً في تحديثه بشكل مستمر، حيث يجب التعامل مع الأخطاء المنطقية بشكل أساسي من خلال دوال التحديث الساخن.

لنلق نظرة أكثر تفصيلًا على الطرق التي يمكن من خلالها تنفيذ التحديثات الساخنة لـPython 3.12.

## Hotfix

الطريقة الأولى نسميها Hotfix، وتتمثل في تنفيذ قطعة معينة من رمز Python من خلال البرنامج (سواءً كان عميلًا أو خادمًا)، لتحقيق تحديث سريع للبيانات والوظائف. يمكن أن يكون رمز Hotfix البسيط على سبيل المثال:


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

تعرض الشيفرة أعلاه كيفية كتابة الإصلاح السريع، حيث يُقرأ المعلومات / الدوال الجديدة عندما يتم الوصول إلى البرنامج بعد تعديل البيانات / الدوال.

إذا كنت دقيقًا بما فيه الكفاية، قد يتبادر إلى ذهنك سؤال: ماذا سيحدث إذا تم الاستشهاد بهذه البيانات والوظائف التي تحتاج إلى تعديلها في كود آخر؟

```python
# attack.py module

player_fire = player.Player.fire_func

def player_attack_by_gun(player, target):
    player_fire(player, target)
    # ...
```

الإجابة هي أن التحديث السريع السابق لا يؤثر على هذه الحالة، حيث يُعتبر الدالة `fire_func` نسخة إضافية في وحدة أخرى، والوحدة تستدعي نسخة من الدالة، وبالتالي فإن تعديل نص الدالة الأصلية لا يؤثر على النسخة.

لذا يجب الانتباه، في الأكواد العامة يُفضل تقليل الإشارات إلى البيانات ووظائف مستوى الوحدة، لتجنب حدوث مثل هذه الحالة التي لا يُظهر فيها Hotfix فعاليته. إذا كان الكود مكتوبًا بهذه الطريقة بالفعل، سيحتاج Hotfix إلى بذل المزيد من الجهود.

```python
# hotfix code
# ...

import attack
attack.player_fire = player.Player.fire_func

```

在对数据 / 函数本体 Hotfix 修改之后，再额外对引用的地方进行修改。这些额外的修改很容易被遗漏，所以我们还是建议，从代码规范上来尽量避免多处引用的写法。

بناءً على ما سبق، يمكن لـ Hotfix تلبية الاحتياجات الأساسية للتحديث الساخن، ومع ذلك، يوجد بعض المشكلات التالية:

- إذا تم الاستشهاد بالبيانات/الدالة من قبل وحدات أخرى بشكل واضح، فسيحتاج ذلك إلى تصحيح إضافي لهذه الوحدات.
- إذا كان هناك كمية كبيرة من البيانات/الدوال تحتاج إلى تصحيح عاجل، فإن كود التصحيح سيصبح ضخمًا، مما يزيد من صعوبة الصيانة، كما أنه يصبح أكثر عرضة للأخطاء.

## Reload

يمكن الحصول على شفرة المصدر لهذا الفصل من هنا: [python_reloader](https://github.com/disenone/python_reloader)

نحن بحاجة إلى التحديث التلقائي لا يتطلب كتابة إصلاحات إضافية، بل يكفي تحديث ملفات الشيفرة، حيث يتم استدعاء دالة "Reload" ليتم استبدال الدوال والبيانات الجديدة تلقائيًا. نُطلِق على هذه الوظيفة التلقائية للتحديث اسم "Reload".

Python 3.12 قدّم دالة importlib.reload، التي تتيح إعادة تحميل الوحدات، لكنها تحمل خاصية التحميل الكامل، وتعيد كائن وحدة جديد، بينما لا يتم تعديل الإشارات في الوحدات الأخرى بشكل تلقائي، بمعنى أنه إذا قامت وحدات أخرى باستيراد الوحدة التي تم إعادة تحميلها، سيظل الوصول إلى كائن الوحدة القديمة. هذه الميزة ليست أفضل بكثير من Hotfix الخاص بنا، ناهيك عن أنها تقوم بإعادة تحميل الوحدة بالكامل، ولا يمكننا التحكم في البيانات التي ينبغي الاحتفاظ بها. نريد أن نحقق خاصية إعادة التحميل بأنفسنا، لتلبية هذه المتطلبات:

- دالة استبدال تلقائية، في حين أن مراجع الوظيفة القديمة تظل فعالة، وستقوم بتنفيذ محتوى الوظيفة الجديدة.
- استبدال البيانات تلقائيًا، مع إمكانية التحكم في بعض الاستبدالات
احتفظ بالإشارات إلى الوحدة القديمة، بحيث يمكن الوصول إلى المحتوى الجديد من خلال الوحدة القديمة
- يجب أن يكون تحميل الوحدة قابلاً للتحكم.

لإكمال هذه المتطلبات، نحتاج إلى الاعتماد على آلية meta_path داخل Python، يمكنك الاطلاع على التفاصيل في الوثائق الرسمية [the-meta-path](https://docs.python.org/zh-cn/3/reference/import.html?highlight=meta_path#the-meta-path)。

يمكن تحديد كائن الباحث عن المسار الرئيسي الخاص بنا في sys.meta_path، على سبيل المثال، إذا كنا نطلق على الباحث المستخدم لإعادة التحميل بـ reload_finder، يجب أن ينفذ reload_finder وظيفة find_spec ويُرجع كائن spec. بمجرد أن يحصل Python على كائن spec، سينفذ بترتيب spec.loader.create_module و spec.loader.exec_module لإكمال عملية استيراد الوحدة.

إذا قمنا بتنفيذ رموز الوحدة الجديدة خلال هذه العملية ونقوم بنسخ الدوال والبيانات المطلوبة من الوحدة الجديدة إلى الوحدة القديمة، يمكننا تحقيق هدف إعادة التحميل (Reload).

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

كما هو مذكور أعلاه ، يقوم `find_spec` بتحميل شفرة المصدر الأحدث للوحدة وتنفيذ شفرة الوحدة الجديدة داخل `__dict__` للوحدة القديمة ، ثم نُستدعى `ReloadModule` لمعالجة المراجع والاستبدالات للفئات / الدوال / البيانات. تهدف `MetaLoader` إلى تكييف آلية meta_path وتقديم كائنات الوحدات المعالجة من قبلنا إلى الآلة الظاهرية Python.

بمجرد الانتهاء من عملية التحميل، نلقي نظرة عامة على تنفيذ الوحدة `ReloadModule`.

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

`ReloadDict` يميز بين معالجة أنواع مختلفة من الكائنات.

- إذا كان class، فسيتم استدعاء `ReloadClass`، وسيتم إرجاع مرجع الوحدة القديمة وتحديث أعضاء class.
عندما تكون الوظيفة أو الطريقة، استدعاء `ReloadFunction` سيُعيد مرجع الوحدة القديمة وسيُحدث بيانات الدالة الداخلية.
إذا كانت البيانات وكانت بحاجة للحفظ، سيتم التراجع إلى `new_dict[attr_name] = old_attr`
المقتبسات الأخرى تُحتفظ بحالتها الجديدة
قم بحذف الدوال غير الموجودة في الوحدة النمطية الجديدة.

`ReloadClass` و `ReloadFunction` تفاصيل الكود هنا لن يتم توسيعها أو تحليلها، إذا كان لديك اهتمام يمكنك الاطلاع على [المصدر](https://github.com/disenone/python_reloader)I'm sorry, but the text you provided is not readable or translatable. If you have any other content you would like me to translate, please feel free to provide it.

整个 Reload 的过程，可以概括为：旧瓶装新酒。为了保持模块/模块的函数/模块的类/模块的数据有效，我们需要保留原来的这些对象的引用（躯壳），转而去更新它们内部的具体数据，譬如对于函数，更新 `__code__`，`__dict__` 等数据，函数执行的时候，就会转而执行新的代码。  

يمكن تلخيص عملية إعادة التحميل بأكملها على النحو التالي: زجاجة قديمة تحتوي على نبيذ جديد. للحفاظ على فعالية البيانات الموجودة في الوحدات/دوال الوحدات/فئات الوحدات، نحتاج إلى الاحتفاظ بالإشارات الأصلية لتلك الكائنات (الغلاف)، ثم نقوم بتحديث بياناتها الداخلية، مثل تحديث `__code__`، `__dict__` وغيرها من البيانات بالنسبة للدوال، وعندما يتم تنفيذ الدالة، ستقوم بتنفيذ الكود الجديد.

##ملخص

هذا النص يشرح بالتفصيل طريقتين للتحديث الساخن في Python3، ولكل منهما سيناريو تطبيق محدد، نأمل أن يكون ذلك مفيدًا لك. إذا كانت لديك أي أسئلة، فلا تتردد في التواصل في أي وقت.

--8<-- "footer_ar.md"


> هذا المنشور قد تم ترجمته باستخدام ChatGPT، يرجى زيارة [**التعليقات**](https://github.com/disenone/wiki_blog/issues/new)وجه بالكشف عن أي نقص. 
