---
layout: post
title: تحليل واختبار أداء خوارزمية AOI للألعاب
categories:
- c++
catalog: true
tags:
- dev
- game
description: هذا النص يتناول مناقشة خوارزميتي الشبكة التاسعة وسلسلة الصليب، ويقدم
  تحليلاً لأداء الخوارزميتين على أرض الواقع، لتكون على دراية كاملة عند استخدامهما
  وتتصرف بحكمة في المواقف الصعبة.
figures: []
date: 2021-11-18
---

<meta property="og:title" content="游戏 AOI 算法解析和性能实测" />

###مقدمة

`AOI` (Area Of Interest) في ألعاب الإنترنت الجماعية هو وظيفة أساسية جدًا، حيث يحتاج اللاعبون إلى استقبال معلومات حول لاعبين آخرين أو كيانات داخل نطاق الرؤية. حساب الكيانات الموجودة ضمن نطاق رؤية اللاعب وكياناته التي دخلت أو غادرت هذا النطاق يُعرف عمومًا بخوارزمية `AOI`.

يناقش هذا النص خوارزميات `AOI` الشبكة التاسعة وسلسلة الصليب ، ويقدم تحليل أداء تجريبي لكلا الخوارزميتين ، لتكون على دراية تامة عند استخدامهما ولا تثور في الظروف الصعبة.

سيتم الإشارة في النص إلى كلمتي لاعب وكيان، الكيان هو مفهوم الكائن في اللعبة، واللاعب هو الكائن الذي يمتلك AOI.

يمكن العثور على الرمز في النص هنا: [AoiTesting](https://github.com/disenone/AoiTesting)I'm sorry, but there is no text to translate.

###الشبكة التاسعة

ما يُعرف بشبكة الـ ٩ مربعات هو تقسيم مواقع جميع الكيانات في الساحة إلى مربعات. على سبيل المثال، تقسيمها إلى مربع ذو طول حافة 200. إذا أردت العثور على الكيانات الأخرى داخل نطاق AOI للاعب الرئيسي في الوسط، يتعين مقارنة جميع لاعبي المربعات الذين يتأثرون ضمن هذا النطاق.

على سبيل المثال، سيتم Tick للمشهد كل 100 ميلي ثانية، وخلال Tick يمكننا تحديث AOI للاعب بالطريقة التالية:

باستخدام موقع اللاعب كمحور، يتم حساب مجموعة الخلايا المعنية في نصف قطر AOI.
قم بحساب المسافة بين الكيانات في مجموعة الخلايا واللاعب تباعًا.
الكيانات التي يكون مركزها أقرب من نصف قطر AOI هي الجدول الجديد للاعب.

ترجمة النص إلى اللغة العربية:

تأتي خوارزمية شبكة الجوف بسهولة، حيث يمكن وصف الخوارزمية ببضع جمل لتوضيحها، سنترك تحليل الأداء التفصيلي لاحقًا ولكن دعونا نلقي نظرة أولاً على خوارزمية قائمة التوصيل المتقاطعة.

###ترجمة: الباقة المشعبة

بالنسبة لألعاب 3D، عادة ما نقوم بإنشاء قوائم مرتبة لإحداثيات المحور X والمحور Z على حدة، حيث يحتوي كل كيان على عقدة في القائمة تحتوي على قيمة المحور. يتم تخزين الكيانات وفق ترتيب تصاعدي حسب القيمة. ومع ذلك، فإن كفاءة البحث في هاتين القائمتين لتخزين نقاط الكيان نفسه ما زالت منخفضة.

النقطة الحقيقية هي توسيع قائمة الوصل بإضافة عقد جاسوسين إلى كل لاعب يمتلك تجاويف الاهتمام. تكون إحدى العقدين على يساره والآخر على يمينه بحيث يكون اختلاف قيم الإحداثيات بمقدار نصف نصف نصف قطر تجاويف الاهتمام، على سبيل المثال إذا كانت إحداثيات اللاعب P (a، b، c) ونصف قطر AOI هو r، فسيكون هناك عقدي جاسوسين على المحور X، بقيم a - r و a + r. بسبب وجود الجاسوسين، نُحدث تجاويف الاهتمام عن طريق مراقبة حركة الجواسيس مع عقد الكيانات الأخرى. ومستمرين في المثال السابق، حركة الكيان E التي تسببها الجواسيس على المحور X من الجهة اليمنى لـ left_x لتعبر left_x إلى اليسار، فهذا يعني بالتأكيد أن E تغادر تجاويف اهتمام P؛ بالمثل، إذا تجاوز right_x إلى اليمين، فإنه يغادر أيضًا تجاويف الاهتمام. وعلى الجانب الآخر، إذا تجاوز left_x إلى اليمين، أو تجاوز right_x إلى اليسار، فإنه من الممكن أن يدخل إلى تجاويف الاهتمام P.

يمكن رؤية أن خوارزمية القائمة المتشابكة أكثر تعقيدًا بكثير مقارنة بالشبكة المربعة التقليدية. نحتاج إلى الحفاظ على قائمتين مرتبتين وتحديث العقدة عند كل تحديث لإحداثيات الكيان، مع التحرك المتزامن لعقد القائمة وتحديث منطقة الاهتمام عند تجاوز العقدة الأخرى.

###تحقيق الشبكة التاسعة

بسبب تورط أداء الاختبار، سنقوم أولاً بالتعمق قليلاً في تفاصيل تنفيذ خوارزمية الشبكة البيضوية.

```cpp
struct Sensor {
  // ...
  Nuid sensor_id;
  float radius;
  float radius_square;
  PlayerPtrList aoi_players[2];
};

struct PlayerAoi {
  // ...    
  Nuid nuid;
  SquareId square_id;
  int square_index;
  Pos pos;
  Pos last_pos;
  Uint32 flags;
  std::vector<Sensor> sensors;
};
```

`PlayerAoi` هو الكائن الذي يحتوي على بيانات اللاعب، بما في ذلك مصفوفة `sensors` التي تُستخدم لحساب الكيانات ضمن نطاق معين، حيث يُقرر ذلك بعد كل `Tick` وتُخزن الكيانات المُحسوبة في `aoi_players`. `aoi_players` هو كائن يحتوي على مصفوفتين، وهو يُستخدم لمقارنة نتائج الـ `Tick` السابقة لتحديد الدخول والخروج من نطاق اللاعب. تتبّع تنفيذ `Tick` تقريبًا كالتالي:

```cpp
AoiUpdateInfos SquareAoi::Tick() {
  AoiUpdateInfos update_infos;
  PlayerPtrList remove_list;

  for (auto& elem : player_map_) {
    auto& player = *elem.second;
    // ...
// حساب Aoi للاعبين الذين لديهم مستشعرات
    if (!player.sensors.empty()) {
      auto update_info = _UpdatePlayerAoi(cur_aoi_map_idx_, &player);
      if (!update_info.sensor_update_list.empty()) {
        update_infos.emplace(update_info.nuid, std::move(update_info));
      }
    }
    // ...
  }

  // ...
سجل موقع اللاعب في المرة السابقة
  for (auto& elem : player_map_) {
    auto& player = *elem.second;
    player.last_pos = player.pos;
  }
  cur_aoi_map_idx_ = 1 - cur_aoi_map_idx_;
  return update_infos;
}
```

العمل الذي يقوم به "Tick" بسيط للغاية، حيث يقوم بتحليل اللاعبين الذين لديهم "sensors"، ويقوم بحساب الكيانات داخل نطاق "sensor" تلو الآخر، وهذا ما يسمى AOI. "last_pos" تستخدم لتحديد ما إذا كانت الكيانات دخلت أو غادرت AOI، وإليكم رمز "_UpdatePlayerAoi" كالتالي:

```cpp
AoiUpdateInfo SquareAoi::_UpdatePlayerAoi(Uint32 cur_aoi_map_idx, PlayerAoi* pptr) {
  AoiUpdateInfo aoi_update_info;
  aoi_update_info.nuid = pptr->nuid;
  Uint32 new_aoi_map_idx = 1 - cur_aoi_map_idx;

  for (auto& sensor : pptr->sensors) {
    auto& old_aoi = sensor.aoi_players[cur_aoi_map_idx];
    auto& new_aoi = sensor.aoi_players[new_aoi_map_idx];
    (this->*calc_aoi_players_func_)(*pptr, sensor, &new_aoi);

    SensorUpdateInfo update_info;

    auto& enters = update_info.enters;
    auto& leaves = update_info.leaves;
    float radius_square = sensor.radius_square;

    _CheckLeave(pptr, radius_square, old_aoi, &leaves);
    _CheckEnter(pptr, radius_square, new_aoi, &enters);

    if (enters.empty() && leaves.empty()) {
      continue;
    }

    update_info.sensor_id = sensor.sensor_id;
    aoi_update_info.sensor_update_list.push_back(std::move(update_info));
  }

  return aoi_update_info;
}
```

`old_aoi` هو AOI الذي تم حسابه في الـ `Tick` السابق، بينما `new_aoi` هو AOI الذي يجب حسابه في هذا الـ `Tick`. يتم اختيار الكيانات داخل نطاق AOI بالتجول عبر جميع الخلايا واختيار تلك التي تكون على مسافة أقل من نصف نصف قطر AOI من اللاعب. بعد ذلك، يتم استخدام الدوال `_CheckLeave` و `_CheckEnter` لحساب الكيانات التي تغادر أو تدخل AOI في هذا الـ `Tick`. على سبيل المثال، إذا كان موقع `last_pos` للكيان في `new_aoi` ليس ضمن نطاق AOI، فهذا يعني أن هذا الكيان قد دخل إلى نطاق AOI في هذا الـ `Tick`. يمكن الاطلاع على الشيفرة المصدرية للتفاصيل الدقيقة، ولا داعي لإعادة الإطالة هنا.

###تنفيذ قائمة الارتباط المتشعب

بالمقارنة مع لوحة التاسعة، تعتبر قائمة العشرة أكثر تعقيدًا في التنفيذ. دعنا نلقي نظرة على الهيكل الأساسي للبيانات:

```cpp
struct CoordNode {
  // ...
  Uint8 type;
  float value;
  CoordNode *prev = nullptr;
  CoordNode *next = nullptr;
  PlayerAoi *pplayer;
  Sensor *psensor;

};

KHASH_MAP_INIT_INT64(SensorHashMap, PlayerAoi*);

struct Sensor {
  // ...
  Nuid sensor_id;
  float radius;
  float radius_square;
  PlayerAoi *pplayer;
  CoordNode left_x;
  CoordNode right_x;
  CoordNode left_z;
  CoordNode right_z;
  PlayerPtrList aoi_players[2];

  std::shared_ptr<khash_t(SensorHashMap)> aoi_player_candidates;
};

struct PlayerAoi {
  // ...
  Nuid nuid;
  Pos pos;
  Pos last_pos;
  Uint32 flags;
  CoordNode node_x;
  CoordNode node_z;
  std::vector<Sensor> sensors;
  std::shared_ptr<boost::unordered_map<Nuid, std::vector<Nuid>>> detected_by;
};
```

`المستشعر` و`PlayerAoi` مشابهين لشبكة التسعة بس يحتوون على هيكل للعقد `CoordNode` المتعلق بقائمة الروابط. ال`CoordNode` هو عقد على القائمة، يسجل نوع العقد نفسه وقيمته، حيث تكون هناك ثلاثة أنواع: عقد اللاعب، عقد المستشعر الأيسر، عقد المستشعر الأيمن.

معظم أعمال قائمة الارتباط الصليبي تتمثل في الحفاظ على ترتيب القائمة:

عندما ينضم اللاعب، يجب نقله إلى موضع منظم وفي الوقت نفسه، يتعامل مع أحداث دخول أو مغادرة لاعبين آخرين في منطقة الاهتمام المحيطة به.
بمجرد أن ينتقل اللاعب إلى الموقع الصحيح، تنطلق العقد الأيمن والأيسر لجهاز `Sensor` من مواقع اللاعب الأمامية والخلفية، وتنتقل إلى الموقع الصحيح، وتتعامل مع الأحداث التي تم تشغيلها عند تجاوز عقد اللاعب الآخر.
عندما يتحرك اللاعب، يتم تحديث إحداثيات اللاعب، ونقل محور اللاعب باليسار واليمين ومعالجة دخول وخروج AOI.

يتضمن رمز العقد المتحرك التالي، عبر كل عقدة، سيتم استدعاء وظيفة `MoveCross` مرة واحدة، حيث ستقوم وظيفة `MoveCross` بتحديد ما إذا كان يتعين الدخول أو الخروج من AOI بناءً على اتجاه الحركة، وعقد النقل، ونوع العقد المتجاوز.

```cpp
void ListUpdateNode(CoordNode **list, CoordNode *pnode) {
  float value = pnode->value;

  if (pnode->next && pnode->next->value < value) {
    // move right
    auto cur_node = pnode->next;
    while (1) {
      MoveCross(MOVE_DIRECTION_RIGHT, pnode, cur_node);
      if (!cur_node->next || cur_node->next->value >= value) break;
      cur_node = cur_node->next;
    }

    ListRemove(list, pnode);
    ListInsertAfter(list, cur_node, pnode);

  } else if (pnode->prev && pnode->prev->value > value) {
    // move left
    auto cur_node = pnode->prev;
    while (1) {
      MoveCross(MOVE_DIRECTION_LEFT, pnode, cur_node);
      if (!cur_node->prev || cur_node->prev->value <= value) break;
      cur_node = cur_node->prev;
    }

    ListRemove(list, pnode);
    ListInsertBefore(list, cur_node, pnode);
  }
}
```

تتحرك قوائم الروابط ببطء شديد، حيث تكون تعقيدية O(n)، خاصة عندما ينضم لاعب جديد إلى المشهد، يجب على اللاعب أن يتحرك تدريجيًا من مكان بعيد للغاية إلى الموضع الصحيح، وبالتالي يتطلب هذا الأمر عملية تصفح كبيرة واستهلاك كبير. من أجل تحسين الأداء، يمكننا وضع أبراج إنارة في مواقع ثابتة في الساحة، هذه الأبراج تعالج بشكل عامل اللاعبين، مع إضافة تسجيل إضافي لـ detected_by، حيث يُستخدم detected_by لتسجيل المنطاق التي يتواجد فيها كيان الحارس. عندما يدخل اللاعب لأول مرة إلى المشهد، لن يبدأ في التحرك من المكان الأبعد، بل سيبحث عن برج إنارة أقرب، ويركب العقد بجوار البرج، ثم من خلال بيانات detected_by على البرج، يتمكن من الدخول بسرعة إلى نطاق AOI المتطابق مع لاعبين آخرين بشكل سريع، وبدء التحرك إلى الموضع الصحيح. بالطبع، يجب أيضًا التعامل مع الدخول والخروج أثناء التحرك. بنفس الطريقة، يمكن أيضًا القيام بذلك مع المستشعرات، حيث يمكن التحرك من موقع البرج إلى الموضع الصحيح عن طريق الوراثة أولاً من بيانات البرج. يمكن رفع أداء إدراج اللاعبين بمقدار مرتين أو أكثر من خلال هاتين الأمثلتين للتحسين.

هنالك `HashMap` آخر تحت اسم "aoi_player_candidates" على جهاز `Sensor` (هنا تم استخدام [khash](https://github.com/attractivechaos/klib/blob/master/khash.h)حدث AOI الذي تم تحريك النقطة بسببه، يمكنه في الواقع اكتشاف منطقة مربعة على محور X-Z بطول حافتيها يبلغ `2r`، وليس AOI بالمعنى الصارم من منطقة دائرية. الكائنات داخل هذه المنطقة المربعة تُسجل في `aoi_player_candidates`، ويتم حساب مدى AOI داخل منطقة دائرية عند تجاوز `Tick`، ولذلك تسمى `candidates`.

جميع عمليات قائمة الصلبان تتم من أجل الحفاظ على كيانات "candidates" داخل منطقة مربعة مستمرة. العمليات التي تُنفذ بواسطة قائمة الصلبان تقريبًا مماثلة لتلك التي تتم في التسع مربعات، باستثناء عدم تطابق "candidates" AOI التي تُحسب عندما يكون AOI المستدير للتسعة مربعات. يُعتبر "candidates" في التسع مربعات الكيانات التي تُغطيها منطقة دائرية AOI، بينما يُحدد قائمة الصلبان الكيانات داخل منطقة مربعة طول ضلعها ٢ر. بشكل عام، يكون هناك عادة أقل "candidates" في قائمة الصلبان مقارنة بالتسع مربعات، مما يؤدي إلى عدد أقل من عمليات التمرير في "Tick"، مما يجعل الأداء أفضل. ومع ذلك، تقوم قائمة الصلبان بتكبد نفقات أداء إضافية كبيرة في صيانة القائمة، لذا فإنه من المهم معرفة أيهما أفضل من حيث الأداء بشكل عام. الخطوة القادمة ستكون اختبار الأداء لنرى.

###أداء الاختبار العملي

لقد قمت هنا بقياس فترات زمنية منفصلة لثلاث حالات: انضمام لاعب إلى المشهد (`Add Player`)، حساب حدث دخول وخروج AOI (`Tick`)، تحديث موقع اللاعب (`Update Pos`).

موقع اللاعب الابتدائي يتم إنشاؤه عشوائيًا داخل نطاق الخريطة ثم يتم إضافة اللاعب إلى السيناريو. `player_num` هو عدد اللاعبين، بينما `map_size` هو نطاق محوري X-Z للخريطة، يتم إنشاء مواقع اللاعبين بشكل عشوائي متساوٍ داخل هذا النطاق، وكل لاعب لديه "حساسية" ذات نصف قطر `100` كـ `Sensor` لحساب الزمن باستخدام `boost::timer::cpu_timer`. تم اختيار حالات `player_num` بشكل فردي على التوالي `100, 1000, 10000`، بينما تم اختيار حالات `map_size` على التوالي `[-50, 50], [-100, 100], [-1000, 1000], [-10000, 10000]`.

تحديث موقع اللاعب سيجعل اللاعب يتحرك في اتجاه عشوائي ثابت بسرعة `6م/ث`.

هذا الترجمة باللغة العربية: "موقع التجربة هذا هو:"

* CPU: Intel(R) Core(TM) i5-4590 CPU @ 3.30GHz
النظام: Debian GNU/Linux 10 (buster)
الإصدار من GCC: gcc الإصدار 8.3.0 (ديبيان 8.3.0-6)
إصدار boost: boost_1_75_0

####تحقيق شبكة الـ ٩ مربعات

نتائج اختبار الشبكة التاسعة كما يلي:

```python
===Begin Milestore: player_num = 100, map_size = (-50.000000, 50.000000)
Add Player (1 times) 0.000081s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
Tick (1 times) 0.000452s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
Update Pos (10 times) 0.000230s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
===End Milestore

===Begin Milestore: player_num = 100, map_size = (-100.000000, 100.000000)
Add Player (1 times) 0.000070s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
Tick (1 times) 0.000338s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
Update Pos (10 times) 0.000185s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
===End Milestore

===Begin Milestore: player_num = 100, map_size = (-1000.000000, 1000.000000)
Add Player (1 times) 0.000084s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
Tick (1 times) 0.000103s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
Update Pos (10 times) 0.000187s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
===End Milestore

===Begin Milestore: player_num = 100, map_size = (-10000.000000, 10000.000000)
Add Player (1 times) 0.000084s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
Tick (1 times) 0.000080s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
Update Pos (10 times) 0.000185s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
===End Milestore

===Begin Milestore: player_num = 1000, map_size = (-50.000000, 50.000000)
Add Player (1 times) 0.000673s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
Tick (1 times) 0.035298s wall, 0.030000s user + 0.000000s system = 0.030000s CPU (85.0%)
Update Pos (10 times) 0.001841s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
===End Milestore

===Begin Milestore: player_num = 1000, map_size = (-100.000000, 100.000000)
Add Player (1 times) 0.000664s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
Tick (1 times) 0.025806s wall, 0.030000s user + 0.000000s system = 0.030000s CPU (116.3%)
Update Pos (10 times) 0.001842s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
===End Milestore

===Begin Milestore: player_num = 1000, map_size = (-1000.000000, 1000.000000)
Add Player (1 times) 0.000721s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
Tick (1 times) 0.001793s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
Update Pos (10 times) 0.001849s wall, 0.010000s user + 0.000000s system = 0.010000s CPU (540.8%)
===End Milestore

===Begin Milestore: player_num = 1000, map_size = (-10000.000000, 10000.000000)
Add Player (1 times) 0.000885s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
Tick (1 times) 0.000804s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
Update Pos (10 times) 0.001855s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
===End Milestore

===Begin Milestore: player_num = 10000, map_size = (-50.000000, 50.000000)
Add Player (1 times) 0.006454s wall, 0.010000s user + 0.000000s system = 0.010000s CPU (154.9%)
Tick (1 times) 3.822028s wall, 3.800000s user + 0.020000s system = 3.820000s CPU (99.9%)
Update Pos (10 times) 0.018402s wall, 0.020000s user + 0.000000s system = 0.020000s CPU (108.7%)
===End Milestore

===Begin Milestore: player_num = 10000, map_size = (-100.000000, 100.000000)
Add Player (1 times) 0.006439s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
Tick (1 times) 2.805551s wall, 2.760000s user + 0.040000s system = 2.800000s CPU (99.8%)
Update Pos (10 times) 0.018489s wall, 0.010000s user + 0.000000s system = 0.010000s CPU (54.1%)
===End Milestore

===Begin Milestore: player_num = 10000, map_size = (-1000.000000, 1000.000000)
Add Player (1 times) 0.006698s wall, 0.010000s user + 0.000000s system = 0.010000s CPU (149.3%)
Tick (1 times) 0.093759s wall, 0.100000s user + 0.000000s system = 0.100000s CPU (106.7%)
Update Pos (10 times) 0.018350s wall, 0.010000s user + 0.000000s system = 0.010000s CPU (54.5%)
===End Milestore

===Begin Milestore: player_num = 10000, map_size = (-10000.000000, 10000.000000)
Add Player (1 times) 0.009046s wall, 0.010000s user + 0.000000s system = 0.010000s CPU (110.6%)
Tick (1 times) 0.012091s wall, 0.010000s user + 0.000000s system = 0.010000s CPU (82.7%)
Update Pos (10 times) 0.019033s wall, 0.020000s user + 0.000000s system = 0.020000s CPU (105.1%)
===End Milestore
```

عندما يكون عدد اللاعبين في الجدول التاسع 100، فإن العمليات الثلاثة تستغرق وقتًا قليلاً جدًا، في الحالة الحدية `map_size = [-50, 50]`، جميع اللاعبين يكونون في نطاق AOI بعضهم ببعض، يستغرق `Tick` حوالي `0.4ms`. إن انضمام اللاعبين إلى المشهد وتحديث الإحداثيات يكونان بتعقيد خطي O(player_num)، والأداء جيد للغاية. عندما يصل عدد اللاعبين إلى 10,000 و `map_size = [-50, 50]`، تكون إضافة اللاعب وتحديث الوضع بسبب طبيعتهما الخطية، يمكن إكمالها في ثوانٍ، ولكن يصل وقت `Tick` إلى 3.8 ثوانٍ، يجب استخدام الكثير من وحدة المعالجة المركزية، وهو غير قابل للاستخدام. عندما يصل عدد اللاعبين إلى 10,000 وحجم الخريطة `[-1000, 1000]`، يكون وقت `Tick` حوالي 94 مللي ثانية، إذا كان بإمكاننا خفض تردد `Tick`، مثلاً مرتين في الثانية، سيكون ذلك في الحدود المقبولة.

####تم اختبار قائمة التشعب العشرية

نتائج اختبار قائمة الوصل المتقاطع كما يلي:

```python
===Begin Milestore: player_num = 100, map_size = (-50.000000, 50.000000)
Add Player (1 times) 0.002057s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
Tick (1 times) 0.000330s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
Update Pos (10 times) 0.000232s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
===End Milestore

===Begin Milestore: player_num = 100, map_size = (-100.000000, 100.000000)
Add Player (1 times) 0.001201s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
Tick (1 times) 0.000222s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
Update Pos (10 times) 0.000272s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
===End Milestore

===Begin Milestore: player_num = 100, map_size = (-1000.000000, 1000.000000)
Add Player (1 times) 0.000288s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
Tick (1 times) 0.000048s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
Update Pos (10 times) 0.000200s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
===End Milestore

===Begin Milestore: player_num = 100, map_size = (-10000.000000, 10000.000000)
Add Player (1 times) 0.000194s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
Tick (1 times) 0.000041s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
Update Pos (10 times) 0.000192s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
===End Milestore

===Begin Milestore: player_num = 1000, map_size = (-50.000000, 50.000000)
Add Player (1 times) 0.130766s wall, 0.130000s user + 0.000000s system = 0.130000s CPU (99.4%)
Tick (1 times) 0.028091s wall, 0.020000s user + 0.000000s system = 0.020000s CPU (71.2%)
Update Pos (10 times) 0.005369s wall, 0.010000s user + 0.000000s system = 0.010000s CPU (186.2%)
===End Milestore

===Begin Milestore: player_num = 1000, map_size = (-100.000000, 100.000000)
Add Player (1 times) 0.103015s wall, 0.100000s user + 0.000000s system = 0.100000s CPU (97.1%)
Tick (1 times) 0.019545s wall, 0.020000s user + 0.000000s system = 0.020000s CPU (102.3%)
Update Pos (10 times) 0.009208s wall, 0.010000s user + 0.000000s system = 0.010000s CPU (108.6%)
===End Milestore

===Begin Milestore: player_num = 1000, map_size = (-1000.000000, 1000.000000)
Add Player (1 times) 0.010150s wall, 0.010000s user + 0.000000s system = 0.010000s CPU (98.5%)
Tick (1 times) 0.000845s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
Update Pos (10 times) 0.003023s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
===End Milestore

===Begin Milestore: player_num = 1000, map_size = (-10000.000000, 10000.000000)
Add Player (1 times) 0.004950s wall, 0.010000s user + 0.000000s system = 0.010000s CPU (202.0%)
Tick (1 times) 0.000427s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
Update Pos (10 times) 0.002234s wall, 0.000000s user + 0.000000s system = 0.000000s CPU (n/a%)
===End Milestore

===Begin Milestore: player_num = 10000, map_size = (-50.000000, 50.000000)
Add Player (1 times) 21.606402s wall, 21.040000s user + 0.570000s system = 21.610000s CPU (100.0%)
Tick (1 times) 3.696885s wall, 3.680000s user + 0.030000s system = 3.710000s CPU (100.4%)
Update Pos (10 times) 0.434396s wall, 0.430000s user + 0.000000s system = 0.430000s CPU (99.0%)
===End Milestore

===Begin Milestore: player_num = 10000, map_size = (-100.000000, 100.000000)
Add Player (1 times) 18.499235s wall, 18.470000s user + 0.020000s system = 18.490000s CPU (100.0%)
Tick (1 times) 2.292608s wall, 2.290000s user + 0.000000s system = 2.290000s CPU (99.9%)
Update Pos (10 times) 1.522617s wall, 1.530000s user + 0.000000s system = 1.530000s CPU (100.5%)
===End Milestore

===Begin Milestore: player_num = 10000, map_size = (-1000.000000, 1000.000000)
Add Player (1 times) 1.642519s wall, 1.640000s user + 0.000000s system = 1.640000s CPU (99.8%)
Tick (1 times) 0.042767s wall, 0.050000s user + 0.000000s system = 0.050000s CPU (116.9%)
Update Pos (10 times) 0.202949s wall, 0.200000s user + 0.000000s system = 0.200000s CPU (98.5%)
===End Milestore

===Begin Milestore: player_num = 10000, map_size = (-10000.000000, 10000.000000)
Add Player (1 times) 0.571257s wall, 0.570000s user + 0.000000s system = 0.570000s CPU (99.8%)
Tick (1 times) 0.006325s wall, 0.010000s user + 0.000000s system = 0.010000s CPU (158.1%)
Update Pos (10 times) 0.042568s wall, 0.040000s user + 0.000000s system = 0.040000s CPU (94.0%)
===End Milestore
```

كما تم تحليله من قبل، يتطلب قائمة الصلبان وقتًا أطول في `إضافة لاعب` و `تحديث الموقع`، وخاصة `إضافة لاعب`، حيث يكون أداءها أسوأ بمئات إلى آلاف المرات مقارنة بشبكة الخلية المربعة. على سبيل المثال، لـ `100، [-50، 50]` يحتاج قائمة الصلبان إلى `2 مللي ثانية`، بينما شبكة الخلية النسعية تحتاج فقط إلى `0.08 مللي ثانية`؛ لـ `10000، [-50، 50]`، تحتاج قائمة الصلبان إلى `21.6 ثانية`، بينما شبكة الخلية النسعية تحتاج فقط إلى `6 مللي ثانية`. ويمكن أن يكون هناك فارق يصل إلى مئات مرات في وقت `تحديث الموقع`، حيث تحتاج قائمة الصلبان إلى `1.5 ثانية` لتحديث موقع اللاعبين لـ `10000، [-100، 100]`، بينما تحتاج شبكة الخلية النسعية إلى `18 مللي ثانية`. ويمكن مشاهدة أن قائمة الصلبان تمتلك نطاقات أوسع للحد الأدنى و الأقصى من وقت العمل مقارنة بشبكة الخلية النسعية، وهي تتأثر بشكل أكبر بعدد اللاعبين وحجم الخريطة، حيث يمكن أن تنخفض أداءات هذين العملين بسرعة في المناطق ذات تكدس لاعبين، حتى تصبح غير قابلة للاستخدام.

عند النظر إلى عملية "Tick" الخاصة بشبكة الصليب، يمكن القول إن الأداء العام بالفعل أفضل من الشبكة التسعية، حيث يكون الوقت المستغرق في أفضل الحالات فقط حوالي نصف وقت الشبكة التسعية (0.8 مللي ثانية للصليب مقابل 1.8 مللي ثانية للشبكة التسعية)، ولكن في أسوأ الحالات، يمكن أن تنخفض أداء شبكة الصليب إلى مستوى يقترب من أداء الشبكة التسعية (3.7 ثانية للصليب مقارنة بـ 3.8 ثانية للشبكة التسعية). يرجع هذا إلى أنه نظرًا لصغر نطاق الساحة وتواجد اللاعبين داخل نطاق AOI لبعضهم البعض، فإن عدد المرشحين الذين يتم تجاوزهم أثناء عملية "Tick" في شبكة الصليب يقترب بالفعل كثيرًا من عددهم في الشبكة التسعية.

عند استخدام سلسلة الصليب، يجب أن تكون الأداء أفضل من الشبكة التاسعة, وهذا يتطلب بعض الافتراضات الأقوى مثل `player_num = 1000, map_size = [-1000, 1000]`، على سبيل المثال، يستغرق Tick في سلسلة الصليب 0.8 مللي ثانية بينما في الشبكة التاسعة 1.8 مللي ثانية، وبالنسبة لـ `Update Pos`، يستغرق Tick في سلسلة الصليب 0.3 مللي ثانية بينما في الشبكة التاسعة 0.18 مللي ثانية (يرجى ملاحظة أن وقت اختبار `Update Pos` هو مجموع الوقت لتنفيذ هذا الإجراء 10 مرات). في المجمل، إذا كانت الصليبة أقل من الشبكة التاسعة في الإجمالي بين Tick و Update Pos، فإن عدد مرات `Update Pos` لا يجب أن يتجاوز 8 مرات Tick، أي أن عدد مرات `Update Pos` بين عمليتين Tick يجب أن يكون أقل من 8 مرات. بالإضافة إلى ذلك، نظرًا لأن عملية "Add Player" في سلسلة الصليب تأخذ وقتًا كبيرًا، فإنها ليست مناسبة لحالات دخول وخروج اللاعبين بشكل متكرر في وقت قصير أو لنقل لاعبين على نطاق واسع داخل المشهد. إضافة إلى ذلك، إذا دخل كمية كبيرة من اللاعبين إلى المشهد خلال وقت قصير، يمكن أن يؤدي ذلك بسهولة إلى تدهور الأداء واستهلاك كبير لوحدة المعالجة المركزية.

بالنسبة للقائمة الصليبية، يمكن إجراء تحسين تحت شرط واحد: التخلص من "Tick"، شريطة أن يكون اللعبة قادرة على قبول AOI على شكل مربع وأن تكون النفقات الأخرى الناتجة عن التبديل إلى AOI على شكل مربع مقبولة من حيث الشبكة بعد الاختبار الفعلي لها. الشرط في الواقع صارم نوعًا ما؛ لأن تكلفة حساب AOI في اللعبة عادة لا تمثل حصة كبيرة من الوحدة المركزية المركزية، ولكن تحويل AOI الدائري إلى AOI مربع يؤدي إلى زيادة مساحة نطاق AOI، مما يزيد من عدد اللاعبين ضمن نطاق معين بشكل أكبر، وقد يزيد عدد اللاعبين بشكل متساوٍ إلى حوالي "1.27" مرة من العدد الأصلي. ومع ذلك، بمجرد تحقيق الشرط، يمكن للقائمة الصليبية عمل بدون الحاجة إلى "Tick" لتحديث أحداث AOI بانتظام، لأن قائمة العمليات في القائمة الصليبية تحتفظ بنسخة من AOI على شكل مربع، حيث كان يسبق أن كانت تستخدم لحساب AOI الدائري ولكن كان يتعين عليها متابعة حسابات المسافة في كل "Tick". في هذه الحالة، يمكن للقائمة الصليبية أن تحقق أداءً جيدًا إذا تم تنفيذ "تحديث الموقع" بشكل جيد، حيث يمكن أن يكون الأداء لعملية تحديث القائمة الصليبية بمقدار عدة مرات إلى عدة عشرات مقارنة بـ "Tick".

عرض عمودي لمقارنة العنصرين النهائية:

![](assets/img/2021-11-18-aoi-tesing/add_player.png)

![](assets/img/2021-11-18-aoi-tesing/tick.png)

![](assets/img/2021-11-18-aoi-tesing/update_pos.png)


###ملخص

وقدّمنا في هذا النص شرحاً لاثنتين من خوارزميات فحص الجودة البصري (AOI)، وهما 'شبكة التاسع' و 'سلسلة العشرة'، موضحين مبادئهما وتنفيذهما الأساسي، وتحليلنا لأداء كل منهما بناءً على البيانات التجريبية، ونأمل أن يقدم ذلك بعض المساعدة أو الإلهام للقراء.

بشكل عام، طريقة الشبكة التاسعة سهلة التنفيذ ومتوازنة من حيث الأداء ولا تعاني من مشاكل الأداء الضعيفة. تناسب بشكل كبير الألعاب التي لا تعتمد على أداء الجهاز البصري الآلي. نطاق تقلب الأداء لطريقة الشبكة التاسعة يبقى ضمن الحدود المتوقعة، والحد الأدنى للأداء مرتفع نسبيًا ولا يسبب مشاكل أداء، ومن جانب آخر، ليس هناك الكثير من الفرص لتحسين المساحة، وتعقيد الوقت ثابت نسبيًا. بالمقابل، تتطلب طريقة السلسلة الصليبية تنفيذًا أكثر تعقيدًا ويكون الحد الأدنى للأداء أقل من طريقة الشبكة التاسعة، ولكن إذا تمكنت من تلبية بعض الافتراضات والفروض، يمكن لطريقة السلسلة الصليبية تحقيق تحسين أعلى للمساحة، بمعنى آخر، يمكن أن يكون الحد الأعلى أكبر. هاتان الطريقتان لهما مزايا وعيوبها، وهناك اختلاف في صناعة الألعاب حيث اختارت بعض المحركات إحدى الطريقتين، حسب الاحتياجات والرؤى.

أنا ذو قدرات محدودة، وما ورد في النص يعبر فقط عن آرائي الشخصية، إذا كان هناك أي نقص أو خطأ، فلا تتردد في ترك تعليق لمناقشته.

--8<-- "footer_ar.md"


> هذه المشاركة تمت ترجمتها باستخدام ChatGPT، يرجى تقديم [**تعليقات**](https://github.com/disenone/wiki_blog/issues/new)Seems like the text is in Chinese. Let me translate it for you in Arabic:

أشير إلى أي اهتمام يمكن أن يكون قد تم تفويته. 
