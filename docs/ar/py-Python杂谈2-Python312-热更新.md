---
layout: post
title: نقاشات متنوعة حول Python 2 - تحديث ساخن لـ Python 3.12
tags:
- dev
- game
- python
- reload
- 热更新
description: سجل كيفية تنفيذ التحديث الساخن في Python 3.12.
---

<meta property="og:title" content="Python 杂谈 2 - Python3.12 热更新" />

#نقاشات مختلفة حول Python 2 - تحديث Python 3.12 الساخن

> سجل كيفية تحقيق التحديث السريع في Python 3.12.

##تحديث ديناميكي

التحديث الحي (Hot Reload) يمكن فهمه كتقنية تسمح بتحديث البرنامج دون الحاجة لإعادة تشغيله. هذه التقنية تجد تطبيقاً واسعاً في صناعة الألعاب، حيث يحتاج المطورون إلى إصدار تحديثات صامتة عند إصلاح مشاكل اللعبة، وذلك لتجنب التأثير على اللاعبين، وهذا ما يُعرف بالتحديث الحي.


##تحديث Python المباشر

بايثون نفسه هو لغة ديناميكية، حيث أن كل شيء فيه عبارة عن كائن، ولديه القدرة على التحديث الحي. يمكننا تقسيم الكائنات التي تحتاج إلى تحديث حي في بايثون إلى نوعين رئيسيين: البيانات والدوال.

البيانات يُمكن فهمها كقيم في اللعبة أو إعدادات، مثل مستوى اللاعب، والعتاد، وهكذا. بعض البيانات لا ينبغي تحديثها عبر التحديثات الحية (مثل مستوى اللاعب الحالي، والعتاد الذي يحمله اللاعب، ينبغي تحقيق هذه التعديلات بطرق أخرى بدلاً من التحديثات الحية)، بينما بعض البيانات نرغب بتحديثها (مثل إعدادات القيم الأساسية للعتاد، والقيم الأساسية للمهارات، ونصوص واجهة المستخدم وغيرها).

الدوال، يمكن تفهمها على أنها منطق اللعبة، وهي بشكل أساسي ما نرغب في تحديثه، ويجب تصحيح الأخطاء المنطقية من خلال تحديث الدوال.

نأتي الآن للنظر بشكل محدد في الطرق التي يمكن بها تنفيذ التحديث الساخن لـ Python 3.12.

## Hotfix

الطريقة الأولى نسميها Hotfix، وتعمل عن طريق تشغيل قطعة معينة من كود Python (يمكن للعميل أو الخادم تنفيذها) لتحقيق تحديث ساخن للبيانات والوظائف. يمكن أن يكون كود Hotfix بسيطًا مثل هذا:


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

يعرض الشيفرة أعلاه ببساطة كيفية كتابة hotfix، عند تعديل البيانات / الوظائف، سيتم قراءة البيانات / الوظائف الجديدة في الأوقات اللاحقة التي يتم فيها الوصول إلى البرنامج لتنفيذها.

إذا كنت دقيقًا، قد تثور لديك تساؤل واحد: ماذا سيحدث إذا احتوى الشيفرات الأخرى على إشارات تستدعي تلك البيانات والوظائف التي يجب تعديلها؟

```python
# attack.py module

player_fire = player.Player.fire_func

def player_attack_by_gun(player, target):
    player_fire(player, target)
    # ...
```

الإجابة هي أن الإصلاح السريع السابق لا ينطبق على هذه الحالة، الدالة `fire_func` تمثل نسخة إضافية في وحدات أخرى، وهو أن الوحدة التي يتم استدعاء الدالة فيها تستخدم نسخة منها، لذلك تعديل جسم الدالة لا يؤثر على النسخة.

لذا يجب الانتباه، في العموم يجب تقليل استخدام الإشارات إلى البيانات على مستوى الوحدات والإشارات إلى الدوال في الشيفرات قدر الإمكان، لتجنب حدوث حالة عدم فعالية الإصلاح السريع هذه. إذا كانت الشيفرة مكتوبة بهذه الطريقة، فيجب إجراء مزيد من العمل لتنفيذ الإصلاح السريع.

```python
# hotfix code
# ...

import attack
attack.player_fire = player.Player.fire_func

```

بعد تعديل البيانات / الوظيفة في Hotfix ، قم بتعديل الأماكن المشار إليها بشكل إضافي. قد يتم تجاهل هذه التعديلات الإضافية بسهولة، لذا نوصي بالابتعاد عن كتابة العديد من الإشارات من الناحية الجمالية في الشيفرات المصدرية.

باختصار، يمكن لـ Hotfix أن يلبي الاحتياجات الأساسية للتحديث السريع، وفي الوقت نفسه توجد المشاكل التالية:

إذا كانت البيانات / الوظائف مشار إليها صراحة بواسطة وحدات أخرى، فيجب المراجعة الإضافية لمراجعة هذه الوحدات.
إذا كان هناك الكثير من البيانات / الوظائف التي تحتاج إلى إصلاح فوري، فإن كود الإصلاح الفوري سيصبح ضخمًا للغاية، وصعوبة الصيانة ستزيد، وسيكون من الأسهل أيضًا حدوث أخطاء.

## Reload

يمكن الحصول على شفرة المصدر لهذا الفصل من هنا: [python_reloader](https://github.com/disenone/python_reloader)

نحن بحاجة بشدة إلى نظام تحديث تلقائي، حتى لا يكون هناك حاجة لكتابة تصحيحات فورية (Hotfix) إضافية، كل ما علينا فعله هو تحديث ملفات الكود، وبعد تنفيذ دالة إعادة التحميل (Reload) سيتم استبدال الوظائف والبيانات الجديدة تلقائيًا. نطلق على هذه الميزة التحديث الساخن التلقائي ونسميه Reload.

Python3.12 تقدم وظيفة importlib.reload ، التي يمكن استخدامها لإعادة تحميل الوحدة، لكنها تحميل كامل، وتُعيد كائن الوحدة الجديدة، ولا يتم تعديل الإشارات في الوحدات الأخرى تلقائيًا، وبمعنى آخر، إذا قامت وحدة أخرى بالاستيراد للوحدة المُعادة تحميلها، فإنها ستظل تصل إلى الكائن القديم. هذه الوظيفة ليست أفضل كثيرًا من Hotfix الخاص بنا، وخاصة بتحميل كامل الوحدات، ولا يمكننا التحكم في أي بيانات يجب الاحتفاظ بها. نرغب في تنفيذ وظيفة إعادة تحميل خاصة بنا، تلبي هذه المتطلبات:

استبدال الوظيفة تلقائيا، مع الاحتفاظ بصلة الوظيفة القديمة سارية، وتنفيذ محتوى الوظيفة الجديدة
استبدال البيانات تلقائيًا، مع القدرة على التحكم في الاستبدال الجزئي
الرجاء الاحتفاظ بالإشارات إلى الوحدات القديمة حيث يمكن الوصول إلى المحتوى الجديد من خلال الوحدات القديمة.
- الوحدات التي تحتاج إعادة تحميل يمكن التحكم فيها

لإكمال هذه المتطلبات، نحتاج إلى الاعتماد على آلية meta_path الموجودة في Python، يمكنك الاطلاع على التفاصيل في الوثائق الرسمية [the-meta-path](https://docs.python.org/zh-cn/3/reference/import.html?highlight=meta_path#the-meta-path)I'm sorry, but it seems like there is no text to translate.

يمكن تعريف الكائن البحثي لمساراتنا في sys.meta_path، على سبيل المثال، يمكننا تسمية الباحث المستخدم لإعادة التحميل reload_finder، ويجب على reload_finder تنفيذ وظيفة find_spec وإرجاع كائن spec. بمجرد أن يحصل Python على كائن spec، سيقوم بتنفيذ spec.loader.create_module و spec.loader.exec_module بالتتابع لإتمام عملية استيراد الوحدة.

إذا قمنا بتنفيذ رموز وحدة جديدة خلال هذه العملية وقمنا بنسخ الدوال والبيانات المطلوبة من داخل الوحدة الجديدة إلى الوحدة القديمة، فيمكننا تحقيق الهدف المتمثل في إعادة التحميل.

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

كما ذُكر أعلاه، يقوم `find_spec` بتحميل شفرة مصدر الوحدة الأحدث وتنفيذها في `__dict__` الخاص بالوحدة القديمة، ثم نقوم باستدعاء `ReloadModule` لمعالجة المراجع والاستبدالات الخاصة بالأصناف، والدوال، والبيانات. يهدف `MetaLoader` إلى تكييف آلية meta_path، لتعود الآلة الظاهرية بالبايثون بكائنات الوحدات التي تم التعامل معها.

بمجرد الانتهاء من عملية التحميل، دعنا نلقي نظرة على تنفيذ `ReloadModule` تقريباً.

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

ستقوم `ReloadDict` بتمييز ومعالجة أنواع مختلفة من الكائنات في داخله

إذا كانت الصنف (class) ، سيتم استدعاء `ReloadClass` ، وسيُرجع إشارة الوحدة القديمة ، وسيُحدث أعضاء الصنف
إذا كانت الوظيفة / الطريقة، فسيتم استدعاء "ReloadFunction"، وسيُرجع مرجع الوحدة القديمة، وسيُحدث بيانات الدالة الداخلية
إذا كانت البيانات وتحتاج إلى الاحتفاظ بها ، فستُرجع `new_dict[attr_name] = old_attr`
الرجاء تقديم النص الذي ترغب في ترجمته.
قم بحذف الدوال التي لا توجد في الوحدة الجديدة.

لا يتم تحليل رمز `ReloadClass` و `ReloadFunction` هنا بالتفصيل. يمكنك الاطلاع مباشرة على [الشيفرة المصدرية](https://github.com/disenone/python_reloader)I'm sorry, but I cannot provide a translation for single punctuation marks or characters. If you have a longer text or specific content you need translated, feel free to provide it.

يمكن تلخيص عملية Reload بشكل عام بأنها "وضع الماء في الكؤوس القديمة". من أجل الحفاظ على سلامة الوحدات / وظائف الوحدات / صفوف الوحدات / البيانات الخاصة بالوحدات، يجب علينا الاحتفاظ بالمراجع الأصلية لهذه الكائنات (الهياكل) وبدلاً من ذلك تحديث البيانات الدقيقة الداخلية لها، على سبيل المثال بالنسبة للوظائف، من خلال تحديث `__code__`، `__dict__` وما إلى ذلك من البيانات، عند تنفيذ الوظيفة، سيتم تنفيذ الشيفرة الجديدة بدلاً منها.

##تلخيص

وقد وضح هذا المقال بالتفصيل طريقتي تحديث لغة Python3، كل منهما له استخداماته الخاصة، نأمل أن يكون الأمر مفيدًا لك. إذا كان لديك أي استفسار، فلا تتردد في التواصل في أي وقت.

--8<-- "footer_ar.md"


> هذه المشاركة تمت ترجمتها باستخدام ChatGPT، يرجى تقديم [**تعليقات**](https://github.com/disenone/wiki_blog/issues/new)إشارة إلى أي نقص. 
