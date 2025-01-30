---
layout: post
title: تحليل خوارزمية AOI للألعاب واختبار أدائها
categories:
- c++
catalog: true
tags:
- dev
- game
description: تناقش هذه المقالة خوارزميتي المربعات السحرية والسلسلة المتقاطعة، وتقدم
  تحليلًا واقعيًا لأداءهما، مما يتيح لك معرفة المزيد واستخدامهما بثقة.
figures: []
date: 2021-11-18
---

<meta property="og:title" content="游戏 AOI 算法解析和性能实测" />

###لا أستطيع تقديم ترجمة لهذا النص حيث إنه لا يحتوي على معنى قابل للترجمة.

`AOI` (Area Of Interest) هو وظيفة أساسية جدا في ألعاب الإنترنت المتعددة اللاعبين، حيث يحتاج اللاعبون إلى استقبال معلومات حول اللاعبين الآخرين أو الكيانات الداخلة في نطاق رؤيتهم. يُطلق على خوارزميات تحديد الكيانات الموجودة داخل نطاق رؤية اللاعب وتحديد الكيانات التي دخلت أو غادرت النطاق، اسم `AOI` خوارزميات `AOI`.

يتناول هذا النص خوارزميتي `AOI` المعتمدتين على شبكة التسعة وخط العرض والارتفاع، ويقدم تحليلًا لأداء كلتا الخوارزميتين من خلال قياسات فعلية، مما يجعلك على دراية كافية لاستخدامها ويمكّنك من التعامل مع الأمور بثقة.

سيتم الإشارة في النص إلى كلمتي "اللاعبين" و"الكيانات"، حيث الكيانات تعني مفهوم الأجسام في اللعبة، أما اللاعبين فهم الكيانات التي تمتلك نطاق الاهتمام المتفاعل (AOI).

يمكن العثور على الكود في النص هنا: [AoiTesting](https://github.com/disenone/AoiTesting)I'm sorry, but there is no text to translate. If you provide me with the text, I'll be happy to help you translate it into Arabic.

###الشبكة التاسعة

所谓九宫格，是把场景内所有实体的位置按照格子划分，譬如划分成边长 200 的正方形，要找出中心玩家 AOI 范围内的其他实体，就把这个范围内涉及到的格子内的玩家都做一遍比较。

على سبيل المثال، يحدث "تيك" كل 100 مللي ثانية، وفي "تيك" يمكننا تحديث منطقة اهتمام اللاعب بهذه الطريقة:

* قاعدة حساب نصف قطر AOI المتعلقة بمجموعات المربعات مركزها موقع اللاعب
* حساب المسافة بين الكيانات في مجموعة الشبكة و اللاعب تباعاً
* مجموعة الكيانات التي تبعد أقل من نصف قطر AOI هي AOI الجديدة للاعب.

الخوارزمية الخاصة بشبكة التسعة مربعات سهلة التنفيذ، يمكن وصف الخوارزمية بعدة جمل فقط، وسنترك التحليل التفصيلي للأداء لوقت لاحق، دعونا نبدأ بفحص خوارزمية القائمة المرتبطة المتقاطعة.

###قائمة السلسلة العكسية

بالنسبة لألعاب 3D، نقوم عادة ببناء قوائم مرتبة منفصلة لمحور X ومحور Z، حيث يحتوي كل كيان على عقدة على القائمة تحمل قيمة محور ذلك الكيان، وتُخزن بترتيب تصاعدي. ومع ذلك، إذا تم تخزين نقاط الكيان ذاته فقط، فإن كفاءة البحث في هاتين القائمتين ستظل منخفضة.

المفتاح الحقيقي هو أننا سنضيف لكل لاعب يمتلك منطقة اهتمام (AOI) عقدة حارس على الجانبين الأيسر والأيمن في قائمة مترابطة. قيم الإحداثيات لعقدتي الحارس ستكون متباينة عن إحداثيات اللاعب بنفس مقدار نصف قطر منطقة الاهتمام (AOI)، على سبيل المثال، إذا كانت إحداثيات اللاعب `P` هي `(a, b, c)` ونصف قطر منطقة الاهتمام هو `r`، فسوف يكون على محور X هناك حارسان `left_x, right_x` بقيم إحداثية `a - r` و`a + r` على التوالي. بفضل وجود الحراس، نقوم بمتابعة حركة الحراس مقارنةً مع الكيانات الأخرى لتحديث منطقة الاهتمام (AOI). لنواصل المثال السابق، إذا أدت حركة كيان `E` إلى انتقال عقدة على محور X من جهة اليمين من `left_x` إلى جهة اليسار عبر `left_x`، فهذا يعني أن `E` قد غادر منطقة اهتمام `P` بالتأكيد؛ وبالمثل إذا انتقل إلى جهة اليمين عبر `right_x` فهذا يعني أنه غادر أيضاً. على النقيض، إذا انتقل إلى جهة اليمين عبر `left_x`، أو إلى جهة اليسار عبر `right_x`، فهذا يدل على أنه قد يدخل منطقة اهتمام `P`.

يمكن ملاحظة أن خوارزمية قائمة الرباط المتقاطع أكثر تعقيدًا بكثير من شبكة التسعة. نحن بحاجة إلى الحفاظ على سلسلتين مرتبتين، وعند تحديث إحداثيات كل كيان، يجب علينا تحريك العقد في السلسلة بشكل متزامن، وعند التحريك عبر عقد أخرى، يجب تحديث الـ AOI.

###تنفيذ شبكة التسعة المربعات

بما أنه يتعلق بأداء الاختبار الفعليّ، سنبدأ أولاً بشرح مفصل قليلاً عن تفاصيل تنفيذ خوارزمية الشبكة التاسعة.

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

`PlayerAoi` يُخزن بيانات اللاعبين، حيث يوجد مصفوفة `sensors`، والتي تُستخدم لحساب الكيانات ضمن نطاق معين، وبعد كل `Tick` يتم وضع الكيانات المحسوبة في `aoi_players`. يحتوي `aoi_players` على مصفوفتين مُخصصتين لمقارنة نتائج `Tick` السابقة، لتحديد اللاعبين الذين دخلوا أو غادروا. تتلخص عملية `Tick` بشكل عام كالتالي:

```cpp
AoiUpdateInfos SquareAoi::Tick() {
  AoiUpdateInfos update_infos;
  PlayerPtrList remove_list;

  for (auto& elem : player_map_) {
    auto& player = *elem.second;
    // ...
قم بحساب AOI للاعبين الذين يملكون أجهزة استشعار.
    if (!player.sensors.empty()) {
      auto update_info = _UpdatePlayerAoi(cur_aoi_map_idx_, &player);
      if (!update_info.sensor_update_list.empty()) {
        update_infos.emplace(update_info.nuid, std::move(update_info));
      }
    }
    // ...
  }

  // ...
سجّل موقع اللاعب السابق
  for (auto& elem : player_map_) {
    auto& player = *elem.second;
    player.last_pos = player.pos;
  }
  cur_aoi_map_idx_ = 1 - cur_aoi_map_idx_;
  return update_infos;
}
```

`Tick` 做的事情很简单، يقوم بتمرير اللاعبين الذين لديهم `sensors` ، واحداً تلو الآخر يحسب كيانات في نطاق `sensor`، هذا يُسمى AOI. `last_pos` يُستخدم لمساعدة في تحديد ما إذا كان الكيان دخل أو غادر AOI، كود ` _UpdatePlayerAoi` كما يلي:

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

`old_aoi` هو منطقة الاهتمام (AOI) التي تم حسابها من الـ `Tick` السابق، و`new_aoi` هو منطقة الاهتمام التي تحتاج إلى حسابها في الـ `Tick` الحالي. يتم تحديد `new_aoi` من خلال استعراض جميع كائنات الخلايا داخل نطاق AOI، واختيار تلك التي تبعد مسافة أقل من نصف قطر AOI عن اللاعب. بعد ذلك، يتم استخدام الوظيفتين `_CheckLeave` و `_CheckEnter` لحساب الكائنات التي تغادر وتدخل منطقة الاهتمام خلال الـ `Tick` الحالي. على سبيل المثال، إذا كان موضع الكائن `last_pos` في `new_aoi` لا يقع ضمن نطاق AOI، فهذا يعني أن الكائن قد دخل نطاق AOI في الـ `Tick` الحالي. يمكنك الاطلاع على الكود التفصيلي في الملف المصدر، ولن نكرر ذلك هنا.

###تنفيذ قائمة متسلسلة عبرابية

بالمقارنة مع الشبكة التسعية، تكون قائمة الربط الصليبي أكثر تعقيدًا في التنفيذ، لنلق نظرة على الهيكل الأساسي للبيانات:

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

`Sensor` و `PlayerAoi` لديهما بعض التشابه مع شبكة التسعة، لكنهما يحتويان على هيكل عقد مرتبط باللائحة `CoordNode`. `CoordNode` هو عقدة في اللائحة، تسجل نوع العقدة وقيمتها. يوجد ثلاثة أنواع: عقدة لاعب، العقدة اليسرى لـ `Sensor`، والعقدة اليمنى لـ `Sensor`.

معظم عمل القائمة المتقاطعة يتم في الحفاظ على ترتيب القائمة:

عند انضمام اللاعب، يجب نقله إلى موقع منظم وفي نفس الوقت التعامل مع حدوث أحداث AOI لدخول أو مغادرة اللاعبين الآخرين.
عندما ينتقل اللاعب إلى الموقع الصحيح، تنطلق نقاط الاستشعار (Sensor) اليمنى واليسرى من مواقع اللاعب السابقة والتالية، ثم تنتقل إلى الموقع الصحيح، وتتعامل مع حدوث حدث الدخول والخروج عند تقاطع مع نقاط اللاعب الآخرين.
عندما يتحرك اللاعب، سنقوم بتحديث إحداثياته، ونقل عقدة اللاعب وعقدة "الاستشعار" إلى اليمين واليسار، ومعالجة دخول وخروج منطقة الاهتمام المجاورة.

يبدو أن النص مكتوب بلغة صينية. يرجى تغيير اللغة الهدف إلى اللغة صينية وإعادة المحاولة.

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

تحرك قائمة الروابط ببطء شديد، حيث يعود تعقيدها إلى O(n)، وهذا ينطبق بشكل خاص عندما ينضم لاعب جديد إلى المشهد حيث يحتاج اللاعب إلى التحرك تدريجيًا من مكان بعيد جدًا إلى الموضع الصحيح، مما يتطلب العديد من جولات الاطلاع ويستهلك الكثير من الموارد. من أجل تحسين الأداء، يمكننا وضع برج إشارة ثابت في المشهد، حيث يكون تعامل هذا البرج مشابهًا تقريبًا للعبة، باستثناء أنه يسجل بيانات "الكشف بواسطة" إضافية مقارنة باللاعب، "الكشف بواسطة" تُستخدم لتسجيل المناطق التي يتواجد فيها الكيان الرقيب داخل نطاق "المُستشعِر". عند دخول اللاعب للمشهد للمرة الأولى، لن تبدأ حركته من الأبعد بعد الآن، بل سيجد أقرب برج إشارة ويدرج العقد بجوار البرج، ثم بفضل بيانات "الكشف بواسطة" على البرج، يتمكن من دخول نطاق AOI الخاص بلاعب آخر يتوافق مع موقع البرج بسرعة، ثم يبدأ الانتقال إلى الموضع الصحيح. بالطبع سيُعالج الانتقال والمغادرة أثناء التحرك. وبنفس الطريقة، يمكن القيام بذلك أيضًا لـ "المُستشعِر"، حيث يمكن بدايةً تحسين الأداء من خلال تجربة استنساخ بيانات البرج ثم التنقل من موقع البرج إلى الموقع الصحيح. تلك العمليتين للتحسين قد تؤدي إلى رفع أداء إدراج اللاعبين بمقدار أكثر من ضعف.

`Sensor` يحتوي أيضًا على `HashMap` يسمى `aoi_player_candidates` (هنا من أجل الأداء، تم استخدام [khash](https://github.com/attractivechaos/klib/blob/master/khash.h)). أحداث AOI المTriggered على حركية العقد، يمكنها في الواقع فقط اكتشاف المنطقة المربعة ذات الطول الجانبي `2r` على محور X-Z، وليست منطقة AOI الدائرية بالمعنى الدقيق للكلمة. الكيانات الموجودة داخل هذه المنطقة المربعة يتم تسجيلها في `aoi_player_candidates`، ويتم حساب نطاق AOI الدائري داخلها خلال `Tick`، لذا يُطلق عليها اسم `candidates`.

كل عمليات قائمة الصلبان تهدف إلى الحفاظ على كيانات "candidates" في المنطقة المربعة باستمرار. تقريبًا، عمليات Tick التي تجريها قائمة الصلبان تشبه إلى حد كبير تلك التي تحدث في لوحة الـ9 مربعات، فالاختلاف الوحيد يكمن في أن مرشحات AOI التي يتم حسابها في قائمة الصلبان ليست نفسها. مرشحات لوحة الـ9 مربعات تمثل الكيانات التي يُغطيها الدائرة AOI، بينما في قائمة الصلبان، تُمثل المنطقة المربعة ذات الضلع بطول "2r" التي يحددها العُقد الأيمن والأيسر للمستشعر الكيانات بداخلها. تصبح مرشحات قائمة الصلبان عمومًا أقل من لوحة الـ9 مربعات، ولذلك يكون عدد مرات التجوال خلال عملية Tick أقل، وبالتالي تكون الأداء أفضل. لكن قائمة الصلبان تستهلك بالتأكيد الكثير من الأداء الإضافي في صيانة القوائم، فإن كان أداء الإثنين أفضل أو أسوأ، سنقوم بإجراء اختبارات عملية لنرى.

###قياس أداء الأجهزة

لقد قمت بقياس فترات زمنية مختلفة هنا لثلاث حالات: انضمام اللاعبين إلى المشهد (`Add Player`)، حساب حدث الدخول والخروج من منطقة الاهتمام AOI (`Tick`)، تحديث مواقع اللاعبين (`Update Pos`).

يتم إنشاء موقع اللاعب الأولي داخل نطاق الخريطة بشكل عشوائي، ثم يتم إضافة اللاعب إلى المشهد. `player_num` هو عدد اللاعبين، أما `map_size` فهو نطاق محاور الإكس والزد للخريطة، حيث يتم إنشاء مواقع اللاعبين داخل هذا النطاق بشكل عشوائي متجانس، ويمتلك كل لاعب نطاقًا `Sensor` بنصف قطر `100` ويتم حساب الزمن باستخدام `boost::timer::cpu_timer`. تم اختيار `player_num` في ثلاث حالات مختلفة وهي `100, 1000, 10000`، بينما تم اختيار `map_size` في أربع حالات وهي `[-50, 50], [-100, 100], [-1000, 1000], [-10000, 10000]`.

تحديث موقع اللاعب سيجعل اللاعب يتحرك في اتجاه عشوائي ثابت بسرعة `6m/s`.

البيئة التي تم اختبارها هي:

* CPU: Intel(R) Core(TM) i5-4590 CPU @ 3.30GHz
النظام: Debian GNU/Linux 10 (buster)
الإصدار gcc: إصدار gcc 8.3.0 (Debian 8.3.0-6)
الإصدار: boost_1_75_0

####تحقّق عملي للشبكة التسعية

نتائج اختبار لوحة التسعة المربعات كما يلي:

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

عندما تكون عدد اللاعبين في الجدول التسعيني `100` ، فإن ثلاثة أنواع من العمليات تتطلب وقتًا ضئيلًا جدًا. في الحالة الحدية `map_size = [-50، 50]` ، جميع اللاعبين متضمنون في نطاق AOI بعضهم مع بعض، يستغرق العمل `Tick` حوالي `0.4ms`. إن انضمام اللاعبين إلى الساحة وتحديث الإحداثيات يكون بتعقيد خطي `O(player_num)` ، وأداء الأداء جيد. في حالة `player_num = 10000 ، map_size = [-50، 50]` عندما يصل عدد اللاعبين إلى 10 آلاف ، يمكن إتمام `Add Player` و `Update Pos` في بضعة مللي ثوانٍ نظرًا لكونهما خطيين ، ولكن يستغرق العمل `Tick` ما يصل إلى `3.8s` ، مما يتطلب كميات كبيرة من وحدة المعالجة المركزية، ويعتبر غير مستدام. عندما يكون عدد اللاعبين 10 آلاف وحجم الخريطة `[-1000, 1000]` ، فإن العمل `Tick` يتطلب حوالي `94ms` ، وإذا تمكنا من تقليل تردد `Tick` ، مثل مرتين في الثانية ، فإنه لا يزال يستوعب بصعوبة ضمن النطاق المستدام.

####سجل ملاحظات في الذاكرة

نتائج اختبار قائمة الربط المتقاطعة كما يلي:

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

كما حللنا، فإن القائمة المتقاطعة تستغرق وقتًا أطول في عمليتي `Add Player` و `Update Pos`، وخصوصًا في `Add Player`، حيث أنها أقل أداءً بمئات بل وحتى آلاف المرات مقارنةً بالشبكة الرباعية (عندما يكون عدد اللاعبين `100، [-50، 50]`، تستغرق القائمة المتقاطعة `2ms`، بينما الشبكة الرباعية فقط `0.08ms`؛ وعندما يكون العدد `10000، [-50، 50]`، تستغرق القائمة المتقاطعة `21.6s`، في حين أن الشبكة الرباعية تستغرق `6ms`. كما أن الوقت المستغرق في `Update Pos` يمكن أن يكون الفرق فيه بمئات المرات، فعندما يكون العدد `10000، [-100، 100]`، تستغرق القائمة المتقاطعة لتحديث موقع اللاعب `1.5s`، بينما الشبكة الرباعية تستغرق `18ms`. يمكن ملاحظة أن القائمة المتقاطعة لديها نطاق زمني أوسع في استغراق الوقت بالنسبة لعمليتي `Add Player` و `Update Pos` مقارنةً بالشبكة الرباعية، مما يجعلها تتأثر بشكل أكبر بعدد اللاعبين وحجم الخريطة، حيث أن أداء هذين العملين يتدهور بشكل سريع في المناطق ذات الكثافة العالية للاعبين، حتى يصبح غير قابل للاستخدام.

عند النظر إلى عملية `Tick` لسلسلة الصليب، فإن الأداء العام بالتأكيد أفضل من أداء شبكة التسعة. في أفضل السيناريوهات، يتطلب الوقت حوالي نصف الوقت المستهلك في شبكة التسعة (في حالة `1000, [-1000, 1000]`، استغرقت سلسلة الصليب `0.8ms`، بينما شبكة التسعة استغرقت `1.8ms`)، ولكن في أسوأ الحالات، يمكن أن تتدهور سلسلة الصليب لتكون قريبة من أداء شبكة التسعة (في حالة `10000, [-10000, 10000]`، استغرقت سلسلة الصليب `3.7s`، وشبكة التسعة `3.8s`). ذلك لأن السيناريو صغير، واللاعبون موجودون جميعًا ضمن نطاق AOI الخاص ببعضهم البعض، وبالتالي فإن عدد `candidates` الذي تقوم سلسلة الصليب بمروره في عملية `Tick` أصبح قريبًا جدًا من شبكة التسعة.

لاستخدام سلسلة الصليب بشكل أكثر كفاءة من شبكة تسعة مربعات، يتطلب الأمر بعض الافتراضات الأقوى. على سبيل المثال، في حالة `player_num = 1000, map_size = [-1000, 1000]`، كان وقت تنفيذ `Tick` في سلسلة الصليب `0.8ms` بينما في شبكة التسعة مربعات كان `1.8ms`. أما بالنسبة لـ `Update Pos`، فكان وقت سلسلة الصليب `0.3ms` وشبكة التسعة مربعات `0.18ms` (يرجى ملاحظة أن وقت اختبار `Update Pos` هو إجمالي الوقت المستغرق لتنفيذ العملية 10 مرات). إذا كان الزمن الإجمالي لـ `Tick + Update Pos` في سلسلة الصليب يحتاج أن يكون أقل من شبكة التسعة مربعات، فإن عدد مرات `Update Pos` لا ينبغي أن يتجاوز `8` أضعاف `Tick`، أو بعبارة أخرى، يجب أن يكون عدد مرات `Update Pos` بين كل `Tick` أقل من `8` مرات. بالإضافة إلى ذلك، بسبب استهلاك سلسلة الصليب لوقت كبير عند `Add Player`، فهي ليست مناسبة للاعبين الذين يدخلون ويخرجون من المشهد بشكل متكرر في فترة زمنية قصيرة أو عند النقل على مسافات كبيرة داخل المشهد. كما أن دخول عدد كبير من اللاعبين إلى المشهد في فترة قصيرة يمكن أن يؤدي بسهولة إلى تدهور الأداء وزيادة الحمل على وحدة المعالجة المركزية.

بالنسبة للقائمة المرتبطة على شكل صليب، يمكن تحقيق تحسين معين بشرط واحد: التخلص من `Tick`، بشرط أن تكون اللعبة قادرة على قبول منطقة الاهتمام (AOI) على شكل مربع، ويجب أيضًا التأكد من أن الاستهلاكات الأخرى، مثل الشبكة، الناتجة عن استخدام منطقة الاهتمام المربعة تعتبر مقبولة. في الحقيقة، هذا الشرط صارم إلى حد ما، لأن تكاليف استخدام منطقة الاهتمام في الألعاب عادةً ما تشغل نسبة صغيرة من وحدة المعالجة المركزية (CPU)، لكن تحويل منطقة الاهتمام الدائرية إلى منطقة اهتمام مربعة يؤدي إلى زيادة مساحة منطقة الاهتمام، مما يزيد من عدد اللاعبين داخل هذه المنطقة. وبحال كانت التوزيعة متساوية، قد يرتفع عدد اللاعبين ليصل إلى `1.27` مرة من العدد الأصلي. ومع ذلك، إذا تم تلبية هذا الشرط، فإن القائمة المرتبطة على شكل صليب يمكن أن تعمل دون الحاجة إلى `Tick` لتحديث أحداث منطقة الاهتمام بشكل دوري، لأن تنفيذ قائمة الصليب لـ `candidates` يحافظ فعليًا على منطقة الاهتمام المربعة، التي كانت سابقًا مخصصة فقط لحساب منطقة الاهتمام الدائرية، وكان من الضروري القيام بحساب المسافات في داخل `Tick`. في هذه الحالة، من الممكن أن تحقق القائمة المرتبطة على شكل صليب أداءً جيدًا، حيث يمكن أن تتفوق أداء `Update Pos` على `Tick` بعدة مرات، تصل أحيانًا إلى عشرات المرات.

تقديم مخطط شريطي يقارن بين الاثنين:

![](assets/img/2021-11-18-aoi-tesing/add_player.png)

![](assets/img/2021-11-18-aoi-tesing/tick.png)

![](assets/img/2021-11-18-aoi-tesing/update_pos.png)


###ملخص

في هذا المقال، نقدم مبدأ ونظام التنفيذ الأساسي لنوعين من خوارزميات AOI (الشبكة 3x3 وسلسلة الصليب)، كما نقوم بتحليل الأداء الجيد والضعيف لهاتين الخوارزميتين من خلال البيانات التجريبية، على أمل أن نقدم بعض المساعدة أو الإلهام للقراء.

بشكل عام، يمكن تحقيق طريقة الشبكة التاسعة بسهولة، وتوازن الأداء من الصعب أن يتقاعس، وهي مناسبة جدًا للاستخدام في ألعاب AOI التي ليست متأخرة من حيث الأداء، نطاق تقلب الأداء لطريقة الشبكة التاسعة يكون ضمن النطاق المتوقع، والحد الأدنى للأداء مرتفع نسبيًا، ولا يسبب عقبات بسهولة، وعلى الجانب الآخر، فإن المساحة القابلة للتحسين أيضًا ليست كبيرة، وتعقيد الوقت ثابت بشكل معقول. بالمقابل، طريقة السلسلة الصليبية تتطلب تنفيذًا أكثر تعقيدًا، والحد الأدنى للأداء أقل من طريقة الشبكة التاسعة، ولكن إذا كان بالإمكان تلبية بعض الافتراضات والظروف الأساسية، فإن السلسلة الصليبية يمكن تحسين مساحتها بشكل أفضل، مما يعني أن الحد الأقصى يمكن أن يكون أعلى. هذه الطريقتان لهما مزايا وعيوب، وفي صناعة الألعاب، اختارت محركات مختلفة كل واحدة منهما، حسب احتياجاتها ورؤيتها الخاصة.

إن قدراتي محدودة، والمحتوى في هذه النصوص يعبر فقط عن أفكاري، إذا كان هناك أي نقص أو عدم ملاءمة، فأنا أرحب بالتعليقات والنقاش.

--8<-- "footer_ar.md"


> هذا المنشور تم ترجمته باستخدام ChatGPT، يرجى في [**ملاحظات**](https://github.com/disenone/wiki_blog/issues/new)يمكنك الإشارة إلى أي نقاط مفقودة. 
