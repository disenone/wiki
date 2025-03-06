---
layout: post
title: 게임 AOI 알고리즘 분석 및 성능 테스트
categories:
- c++
catalog: true
tags:
- dev
- game
description: 본문에서는 스도쿠 및 십자링크 두 가지 알고리즘을 논의하고, 두 알고리즘의 성능을 실제로 분석하여 사용 시에 자신감을 갖도록
  도와줍니다.
figures: []
date: 2021-11-18
---

<meta property="og:title" content="游戏 AOI 算法解析和性能实测" />

###전문 번역 엔진으로 의해 제공된 콘텐츠는 전문적이며 세련되며 숙련되어 있습니다.

`AOI` (Area Of Interest)는 온라인 게임에서 매우 기본적인 기능으로, 플레이어는 시야 범위 내에 있는 다른 플레이어나 엔티티(Entity)의 정보를 수신해야 합니다. 플레이어 시야 범위 내에 어떤 엔티티가 있는지 계산하고, 어떤 엔티티가 시야에 들어오거나 나가는지를 판단하는 알고리즘을 우리는 일반적으로 `AOI` 알고리즘이라고 부릅니다.

본문에서는 九宫格和十字链两种 `AOI` 알고리즘에 대해 논의하고, 두 가지 알고리즘의 현장 성능 분석을 제시하여 사용자가 마주한 일에 당황하지 않고 느슨하지 않도록 합니다.

본문에는 플레이어와 엔티티 두 용어가 언급됩니다. 엔티티는 게임 안의 물체 개념을 가리키며, 플레이어는 AOI를 소유한 엔티티를 지칭합니다.

본문의 코드는 이곳에서 찾을 수 있습니다: [AoiTesting](https://github.com/disenone/AoiTesting)In Korean, it is translated as:

"。"

###구름격

九宮格란 모든 개체의 위치를 그리드로 분할하는 것을 말합니다. 예를 들어, 한 변이 200인 정사각형으로 나눕니다. 중심 플레이어 AOI 범위 내의 다른 개체를 찾으려면 해당 범위에 영향을 받는 격자 내의 플레이어를 모두 비교합니다.

예를 들어, 매 100 밀리초마다 한 번씩 Tick이 발생하는 상황에서 Tick 중에 플레이어의 AOI를 업데이트할 수 있습니다:

플레이어 위치를 중심으로 하여, 관심 영역 반경에 관련된 타일 집합을 계산합니다.
격자 집합 안의 개체를 하나하나씩 플레이어와의 거리를 계산합니다.
AOI 반경보다 작은 거리에 있는 개체들은 플레이어의 새로운 AOI가 됩니다.

9x9 Sudoku solving algorithm is quite simple to implement. The algorithm can be described concisely in a few sentences, while a detailed performance analysis will be discussed later. First, let's take a look at the cross-linked list algorithm.

###십자형 연결 리스트

3D 게임의 경우, 보통 X축과 Z축 좌표에 대해 각각 정렬된 링크드 리스트를 만듭니다. 각각의 엔티티는 해당 좌표 축 값이 담긴 노드를 갖고 있으며, 값이 증가하는 순서대로 저장됩니다. 그러나 단순히 엔티티의 좌표점을 저장하는 경우, 이 두 링크드 리스트로 질의하는 효율은 여전히 매우 낮습니다.

진정한 핵심은, 우리는 링크드 리스트에 각 플레이어에게 AOI를 갖게 할 때 좌우에 각각 두 개의 센티넬 노드를 추가할 것입니다. 두 개의 센티넬의 좌표 값은 플레이어 자체의 좌표와 AOI 반경만큼 정확히 다릅니다. 예를 들어 플레이어 `P`의 좌표가 `(a, b, c)`이고, AOI 반경이 `r`이면, X 축에 `left_x, right_x` 두 개의 센티넬이 있을 것입니다. 좌표 값은 각각 `a - r`과 `a + r`일 겁니다. 센티넬이 있기 때문에, 우리는 센티넬과 다른 엔티티 노드의 이동을 추적하여 AOI를 업데이트합니다. 이전 예시를 계속하면, 엔티티 `E`의 이동으로 인해 X 축에서 `left_x`의 오른쪽에서 왼쪽으로 `left_x`를 지나 `left_x`의 왼쪽에 도착한다면, `E`이 `P`의 AOI를 벗어났음을 의미합니다. 마찬가지로 오른쪽으로 `right_x`를 넘어간다면 AOI를 벗어났음을 의미합니다. 반대로, `left_x`를 넘어 오른쪽으로 이동하거나, `right_x`를 넘어 왼쪽으로 이동한다면, `P`의 AOI에 들어갈 수 있다는 것을 의미합니다.

우리는 십자 모양의 링크드 리스트 알고리즘이 구구절절한 그리드보다 훨씬 복잡하다는 것을 알 수 있습니다. 우리는 두 개의 정렬된 리스트를 유지해야 하며 각 엔티티 좌표 업데이트할 때마다 리스트 노드를 동기화하여 다른 노드를 건널 때 AOI를 업데이트해야 합니다.

###구십자판의 실행

실제 성능에 관련이 있기 때문에 먼저 구름 상자 알고리즘의 구현 세부 사항을 조금 더 자세히 알아보겠습니다:

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

`PlayerAoi`은 플레이어 데이터를 저장하는 곳이야. 그 안에 `sensors` 배열이 있어. `sensors`는 일정 범위 내의 엔티티를 계산하는 데 사용되고, 각 `Tick` 후에 계산된 엔티티가 `aoi_players`에 배치돼. `aoi_players`에는 지난 `Tick` 결과를 비교하여 플레이어의 접속 및 이탈을 추적하는 두 개의 배열이 들어 있지. `Tick`의 전반적인 흐름은 이렇지:

```cpp
AoiUpdateInfos SquareAoi::Tick() {
  AoiUpdateInfos update_infos;
  PlayerPtrList remove_list;

  for (auto& elem : player_map_) {
    auto& player = *elem.second;
    // ...
센서가 있는 플레이어에 대한 Aoi를 계산합니다.
    if (!player.sensors.empty()) {
      auto update_info = _UpdatePlayerAoi(cur_aoi_map_idx_, &player);
      if (!update_info.sensor_update_list.empty()) {
        update_infos.emplace(update_info.nuid, std::move(update_info));
      }
    }
    // ...
  }

  // ...
플레이어의 이전 위치를 기록합니다.
  for (auto& elem : player_map_) {
    auto& player = *elem.second;
    player.last_pos = player.pos;
  }
  cur_aoi_map_idx_ = 1 - cur_aoi_map_idx_;
  return update_infos;
}
```

`Tick` 하는 일은 매우 간단하다. `sensors`가 있는 플레이어를 순회하며, 각각의 `sensor` 범위 내에서 엔티티를 계산하여 AOI로 정의한다. `last_pos`는 엔티티가 AOI에 진입하거나 빠져나갔는지 판단하는 데 사용된다. `_UpdatePlayerAoi`의 코드는 아래와 같다:

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

`old_aoi`는 이전 `Tick`에서 계산된 AOI이고, `new_aoi`는 현재 `Tick`에서 계산해야 하는 AOI입니다. `new_aoi`는 AOI 범위 내의 모든 셀의 엔티티를 탐색하여 플레이어와의 거리가 AOI 반경보다 작은 것을 선택합니다. 그런 다음 `_CheckLeave`와 `_CheckEnter` 두 함수를 사용하여 현재 `Tick`에서 AOI를 떠나거나 들어온 엔티티를 계산합니다. 예를 들어, `new_aoi`의 엔티티 `last_pos`가 AOI 범위 내에 없는 경우, 해당 엔티티가 이번 `Tick`에 AOI 범위 내에 들어온 것입니다. 자세한 코드는 소스 파일을 참조하시기 바랍니다. 여기서는 더 이상 자세히 설명하지 않겠습니다.

###십자 연결 리스트 구현

구 글자 그리드에 비해서 십자가 연결 리스트는 구현이 더 복잡합니다. 먼저 기본 데이터 구조를 살펴봅시다.

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

`Sensor` 와 `PlayerAoi`는 육목과 약간 유사하지만, `CoordNode`와 관련된 노드 구조가 더 추가되었습니다. `CoordNode`는 링크드 리스트의 한 노드로, 해당 노드의 유형과 값이 기록되어 있습니다. 유형은 세 가지가 있습니다: 플레이어 노드, `Sensor` 왼쪽 노드, `Sensor` 오른쪽 노드.

십자 연결 리스트의 대부분 작업은 리스트를 순서대로 유지하는 데 사용됩니다:

플레이어가 참가할 때, 플레이어 노드를 정돈된 위치로 이동하고 동시에 플레이어 노드를 이동하는 동안 다른 플레이어의 AOI 이벤트에 대한 처리를 해야 합니다.
플레이어가 올바른 위치로 이동한 후, `Sensor`의 왼쪽 및 오른쪽 노드가 플레이어의 앞뒤 위치에서 출발하여 올바른 위치로 이동하고, 다른 플레이어 노드를 통과할 때 발생하는 진입 및 이탈 이벤트를 처리합니다.
플레이어가 이동할 때, 플레이어의 좌표를 업데이트하고, 플레이어 노드와 'Sensor' 노드를 좌우로 이동하여 AOI(관심 영역)에 대한 진입과 이탈을 처리합니다.

이동 노드의 코드는 아래와 같습니다. 각 노드를 걸을 때마다 'MoveCross' 함수가 한 번 호출됩니다. 'MoveCross' 함수는 이동 방향, 이동 노드, 그리고 건너 뛴 노드의 유형에 따라 AOI에 진입할지 떠날지를 결정합니다.

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

연결리스트의 이동은 굉장히 느리며, `O(n)` 복잡도를 가지고 있습니다. 특히 플레이어가 새로운 씬에 합류할 때, 플레이어는 먼 곳에서부터 올바른 위치로 점진적으로 이동해야 하며, 이를 위해 많은 노드를 순회해야 하여 많은 자원을 소모합니다. 성능을 최적화하기 위해, 씬에는 랜턴을 고정된 위치에 배치할 수 있습니다. 이 랜턴은 플레이어와 거의 유사하게 처리됩니다. 단지 플레이어보다는 하나 더 많은 `detected_by` 데이터를 기록한다는 차이가 있습니다. 플레이어가 씬에 처음 들어올 때, 가장 먼 곳에서 이동하는 대신, 가장 가까운 랜턴을 찾아 해당 노드를 랜턴 옆에 삽입하고, 랜턴의 `detected_by` 데이터를 통해 빠르게 랜턴과 동일한 다른 플레이어의 AOI 범위로 이동한 후, 올바른 위치로 이동합니다. 물론 이동 중에는 진입과 이탈도 처리해야 합니다. 마찬가지로 `Sensor`에 대해서도 랜턴의 데이터를 상속한 후, 랜턴의 위치에서 올바른 위치로 이동할 수 있습니다. 이 두 가지 최적화를 통해 플레이어 삽입 성능을 1배 이상 향상시킬 수 있습니다.

`Sensor`에는 `aoi_player_candidates`라는 이름의 `HashMap`이 또 있어. 여기서 성능을 위해 [khash](https://github.com/attractivechaos/klib/blob/master/khash.h)이동 노드를 트리거하는 AOI 이벤트는 사실 X-Z 좌표축 상의 한 변이 `2r`인 정사각형 영역만을 감지할 수 있으며 엄밀히 말해 원형 AOI가 아닙니다. 이 정사각형 영역 내 엔티티는 'aoi_player_candidates'에 기록되며 'Tick'에서 원형 AOI 범위를 계산하기 위해 반경을 계산하여 'candidates'로 지칭됩니다.

모든 십자형 연결리스트의 동작은 계속해서 정사각형 영역 내의 실체 `candidates`를 유지하기 위한 것이다. 십자형 연결리스트에서 `Tick`이 하는 동작은 아홉 칸 모두와 거의 동일한데, AOI의 `candidates`를 계산하는 것만 다르다. 아홉 칸의 `candidates`는 AOI 원형 영역에 덮인 칸의 실체를 나타내지만, 십자형 연결리스트는 `Sensor` 좌우 노드로 정의된 변 길이가 `2r`인 정사각형 영역 내의 실체를 나타낸다. 일반적으로 말해서, 십자형 연결리스트의 `candidates`는 일반적으로 아홉 칸보다 적어서, `Tick` 중의 반복 횟수가 적어져 더 나은 성능을 보인다. 단, 십자형 연결리스트는 여전히 많은 추가적인 성능 소비가 연결리스트 유지에 소모되는데, 두 방법의 전체적인 성능은 무엇이 우세하고 불리한지에 대해서는 실제 테스트를 통해 알아봐야 할 것이다. 

###성능 실측

저는 여기서 플레이어가 씬에 추가되는 시간(`Add Player`), AOI 진입 및 이탈 이벤트를 계산하는 시간(`Tick`), 그리고 플레이어 위치를 업데이트하는 데 걸리는 시간(`Update Pos`)을 각각 측정했습니다.

플레이어 초기 위치가 맵 내에서 무작위로 생성되고, 그 후 플레이어를 장면에 추가합니다. `player_num`은 플레이어 수이고, `map_size`는 지도 X-Z 좌표 범위입니다. 플레이어의 위치는이 범위 내에서 균일하게 무작위로 생성되며, 각 플레이어는 AOI로 사용되는 반지름이 `100`인 `Sensor`를 가지고 있습니다. 계산 시간은 `boost::timer::cpu_timer`를 사용합니다. `player_num`에는 각각 `100, 1000, 10000` 세 가지 상황이 선택되었으며, `map_size`에는 `[-50, 50], [-100, 100], [-1000, 1000], [-10000, 10000]` 네 가지 상황이 선택되었습니다.

플레이어 위치를 업데이트하면 플레이어가 6m/s의 속도로 고정된 무작위 방향으로 이동합니다.

이 텍스트를 한국어로 번역하십시오:

本次测试环境为：

* CPU: Intel(R) Core(TM) i5-4590 CPU @ 3.30GHz
시스템: Debian GNU/Linux 10 (buster)
* gcc 버전: gcc 버전 8.3.0 (Debian 8.3.0-6)
boost 버전: boost_1_75_0

####아홉 칸 실측

구궁격 테스트 결과는 다음과 같습니다:

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

플레이어 수가 `100` 명일 때, 3가지 조작은 모두 시간이 매우 적게 소요된다. 극단적인 경우 `map_size = [-50, 50]`, 모든 플레이어가 상호적으로 AOI 영역 내에 있고, `Tick` 수행 시 약 `0.4ms` 소요된다. 플레이어가 장면에 참여하고 좌표를 업데이트 하는 것은 모두 선형 복잡도 `O(player_num)`를 갖고 있으며, 성능은 전반적으로 우수하다. 플레이어 수가 `10000` 명, `map_size = [-50, 50]`일 때, 플레이어 수가 1만 명에 도달할 때, `Add Player`와 `Update Pos`는 모두 선형이므로 몇 밀리초 안에 완료될 수 있다. 그러나 `Tick` 시간은 `3.8초`로 증가하며 대량의 CPU를 소모하게 된다. 1만 명의 인구와 지도 크기가 `[-1000, 1000]`인 경우, `Tick` 시간 소요는 약 `94ms`이며, `Tick` 주기를 줄일 수 있다면, 예를 들어 초당 2회, 아주 가까운 범주 내에서 사용 가능하다고 할 수 있다.

####십자 연결 목록 테스트됨

십자 연결 리스트의 테스트 결과는 다음과 같습니다:

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

우리의 분석에 따르면 十字链表이 `Add Player` 및 `Update Pos`에서 더 많은 시간이 소요된다는 것을 알 수 있습니다. 특히 `Add Player`의 경우, Nine-Grid에 비해 수백 심지어 수천 배까지 성능이 떨어진다. (`100, [-50, 50]`에서 十字链은 `2ms`가 소요되고, Nine-Grid는 단지 `0.08ms`가 소요된다. `10000, [-50, 50]`에서 十字链은 `21.6s`가 소요되고, Nine-Grid는 단지 `6ms`가 소요된다. `Update Pos`의 경우에도 백 배 이상의 차이가 발생할 수 있으며, `10000, [-100, 100]`에서 十字链은 플레이어 위치 업데이트에 `1.5s`가 소요되고, Nine-Grid는 `18ms`가 소요된다. 十字链은 Nine-Grid에 비해 `Add Player` 및 `Update Pos`에서 소요되는 시간의 범위가 더 크며, 인원수 및 지도 크기에 민감하다는 것을 알 수 있습니다. 플레이어가 밀집된 지역에서는 이 두 작업의 성능이 급속히 하락하여 사용 불가능한 상태가 될 수 있습니다.

`Tick` operation of the Cross Chain, on the other hand, does indeed exhibit better overall performance than the Nine-Cell Grid. In optimal conditions, the Cross Chain takes roughly only half the time compared to the Nine-Cell Grid (`0.8ms` for Cross Chain versus `1.8ms` for Nine-Cell Grid under `1000, [-1000, 1000]`). However, in the worst-case scenario, the Cross Chain's performance regresses to be nearly on par with the Nine-Cell Grid (`3.7s` for Cross Chain versus `3.8s` for Nine-Cell Grid under `10000, [-10000, 10000]`). This is due to the fact that in a small-scale setting where players are all within each other's AOI range, the number of `candidates` traversed by the Cross Chain `Tick` operation is actually quite close to that of the Nine-Cell Grid.

십자링크 사용은 9x9 그리드보다 우수한 성능을 보이려면 추가적인 강력한 가정이 필요합니다. 예를 들어 `player_num = 1000, map_size = [-1000, 1000]`와 같은 상황에서, 십자링크의 `Tick` 소요 시간은 `0.8ms`이고 9x9 그리드는 `1.8ms`입니다. `Update Pos`의 경우 십자링크는 `0.3ms`이고 9x9 그리드는 `0.18ms`입니다(주의: `Update Pos` 시간은 10회 실행한 총 시간). `Tick + Update Pos` 총 시간에서, 십자링크가 9x9 그리드보다 적게 걸리려면 `Update Pos` 횟수가 `Tick`의 8배를 넘지 않아야 하며, 또는 두 번의 `Tick` 사이에 `Update Pos` 횟수는 8회보다 작아야 합니다. 또한 십자링크의 `Add Player`가 큰 시간을 소모하므로, 플레이어가 짧은 시간에 빈번하게 씬에 들어오거나 씬 내에서 대규모 이동하는 경우에는 적합하지 않습니다. 또한 짧은 시간 내에 많은 플레이어가 씬에 들어오면 성능 저하와 CPU 과부하가 발생할 수 있습니다.

십자 연결 리스트의 경우, 조건이 충분하다면 최적화를 할 수 있습니다: `Tick`를 없애는 거죠. 이때의 전제 조건은 게임이 정사각형 AOI를 수용할 수 있어야 하며, 정사각형 AOI로 인한 네트워크 등 추가 소모를 테스트해야 합니다. 사실 이 전제는 꽤 엄격합니다. 왜냐하면 게임에서 AOI 계산이 CPU 소비 비중이 크지 않을 때가 많으며, 원형 AOI를 정사각형 AOI로 변경하면 AOI 범위가 커지고 플레이어 수도 증가하게 되어 플레이어 수가 원래의 `1.27` 배 증가할 수 있습니다. 그러나, 한번 전제를 충족할 수 있다면, 십자 연결 리스트는 `Tick` 없이도 정기적으로 AOI 이벤트를 업데이트할 수 있습니다. 왜냐하면 십자 연결 리스트의 `candidates`는 이미 정사각형 AOI를 유지하고 있기 때문입니다. 기존에는 원형 AOI를 계산하기 위해 `Tick`에서 다시 거리를 계산해야 했던 것인데요. 이런 상황에서 십자 연결 리스트는 좋은 성능을 보여줄 수 있습니다. 왜냐하면 십자 연결 리스트 `Update Pos`의 성능은 `Tick`와 비교했을 때 몇 배에서 수십 배 정도나 차이가 날 수 있기 때문입니다.

마지막으로 두 가지의 비교 막대 그래프를 제시합니다:

![](assets/img/2021-11-18-aoi-tesing/add_player.png)

![](assets/img/2021-11-18-aoi-tesing/tick.png)

![](assets/img/2021-11-18-aoi-tesing/update_pos.png)


###요약

본문에서는 9×9 격자 및 십자 체인 두 가지 AOI 알고리즘의 원리와 기본 구현을 소개하고, 이 두 알고리즘의 성능을 실제 데이터로 분석하여 비교했습니다. 독자들에게 도움이나 영감을 줄 수 있기를 희망합니다.

총적으로 말하자면, 9스퀘어 메소드는 구현이 간단하고 성능이 균형을 이루는 것이 어렵지 않아요. AOI에서 성능 병목이 되지 않는 게임에 적합하며, 9스퀘어 메소드의 성능 변동 범위는 예상 가능한 범위 내에 있어요. 성능 하한이 상대적으로 높아 병목 현상을 일으키기 어렵지만, 최적화 공간이 크지 않은 편이에요. 시간 복잡도는 상대적으로 고정되어 있어요. 반면에, 크로스 체인 메소드는 구현이 더 복잡하고, 성능 하한이 9스퀘어 메소드보다 낮아요. 하지만 가정과 전제 몇 가지를 충족한다면, 크로스 체인은 최적화 공간이 더 크고, 즉 한 마디로 상한이 높을 수 있어요. 이 두 가지 방법은 각각 장단점이 있고, 게임 업계에서도 다양한 엔진이 두 가지 중 하나를 선택하여 필요에 맞게 사용하고 있어요. 각자 적합한 방법을 선택하는 것이 중요하며, 본인이 판단할 수 있는 문제에 따라 선택하면 돼요.

제 실력은 제한되어 있습니다. 이 문서의 내용은 전적으로 제 의견을 대표합니다. 부족하거나 적절하지 않은 부분이 있다면 언제든지 의견을 남기고 토론해 주십시오.

--8<-- "footer_ko.md"


> 본 게시물은 ChatGPT를 사용하여 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)모든 누락된 부분을 찾아내세요. 
