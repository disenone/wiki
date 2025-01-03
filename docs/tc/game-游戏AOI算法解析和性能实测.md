---
layout: post
title: 遊戲 AOI 演算法解析和性能實測
categories:
- c++
catalog: true
tags:
- dev
- game
description: 本文討論九宮格和十字鏈兩種演算法，並給出兩種演算法的實測效能分析，讓你用起來心中有數，遇事不慌。
figures: []
date: 2021-11-18
---

<meta property="og:title" content="游戏 AOI 算法解析和性能实测" />

###序言

`AOI`（面積感興趣）在多人線上遊戲中是一項基本功能，玩家需要收到進入視野範圍內的其他玩家或實體（Entity）的訊息。計算哪些實體存在於玩家視野範圍內，以及哪些實體進入或離開視野的演算法，我們一般稱之為 `AOI` 演算法。

本文探討了九宮格和十字鏈兩種 `AOI` 算法，並提供了兩種算法的實測性能分析，讓您能夠心中有數，處事不慌。

文中會提到玩家和實體兩種詞，實體是遊戲中物體的概念，玩家是擁有 AOI 的實體。

文中的程式碼可以在這裡找到：[AoiTesting](https://github.com/disenone/AoiTesting)。

###九宮格

所謂九宮格，是將場景中所有實體的位置按照格子劃分，例如劃分成邊長 200 的正方形，要找出中心玩家 AOI 範圍內的其他實體，就將這個範圍內涉及到的格子內的玩家都逐一比較。

例如，每 100 毫秒場景會進行一次 Tick。在這個 Tick 過程中，我們可以更新玩家的 AOI：

以玩家位置為中心，AOI 半徑計算涉及到的格子集合。
對格子集合中的實體逐一計算與玩家的距離
小於 AOI 半徑的實體集合即為玩家新的 AOI。

九宮格演算法的實作非常簡單，這個演算法可以用幾句話輕鬆描述清楚，詳細的效能分析我們留到後面，現在先來看看十字鏈表演算法。

###十字鏈表

針對 3D 遊戲，我們通常會分別對 X 軸和 Z 軸坐標構建有序的鏈表，每個實體在鏈表上都擁有一個節點，存放著相應的座標軸值，按照值逐漸增加的順序來排列。然而，如果僅存放實體本身的座標點，這兩個鏈表的查詢效率仍然很低。

真正關鍵的是，我們在鏈表上還會給擁有 AOI 的每個玩家增加左右兩個哨兵節點。兩個哨兵的座標值跟玩家本身座標正好相差了 AOI 半徑，舉例來說，玩家 `P` 座標為 `(a, b, c)`，AOI 半徑為 `r`，那麼在 X 軸上會有兩個哨兵 `left_x, right_x`，座標值分別為 `a - r` 和 `a + r`。由於有哨兵的存在，我們透過追蹤哨兵跟其他實體節點的移動來更新 AOI。延續前面的例子，一個實體 `E` 移動導致在 X 軸上的節點從 `left_x` 的右邊向左跨過 `left_x` 來到 `left_x` 的左邊，那麼說明 `E` 確定是離開了 `P` 的 AOI；同理如果向右跨過了 `right_x` 也是離開了 AOI。相反，如果是向右跨過 `left_x`，或者向左跨過 `right_x`，說明有可能會進入到 `P` 的 AOI 中。

可以看到，十字鏈表算法要比九宮格複雜得多，我們需要維護兩條有序的鏈表，並且在每個實體座標更新的時候，同步移動鏈表上的節點，並且在移動跨過其他節點時更新 AOI。

###九宮格的實現

由於牽涉到實測性能，因此我們先稍微深入探討九宮格算法的實現細節：

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

`PlayerAoi` 是用來存放玩家資料的，裡面有一個`sensors`陣列，`sensors` 用來計算一定範圍內的實體，每次`Tick`之後將計算出來的實體放入`aoi_players`。`aoi_players`包含了兩個陣列，用於比較前後兩次`Tick`的結果，找出哪些實體進入和離開玩家。`Tick`的流程大致如下：

```cpp
AoiUpdateInfos SquareAoi::Tick() {
  AoiUpdateInfos update_infos;
  PlayerPtrList remove_list;

  for (auto& elem : player_map_) {
    auto& player = *elem.second;
    // ...
對擁有感應器的玩家進行Aoi計算。
    if (!player.sensors.empty()) {
      auto update_info = _UpdatePlayerAoi(cur_aoi_map_idx_, &player);
      if (!update_info.sensor_update_list.empty()) {
        update_infos.emplace(update_info.nuid, std::move(update_info));
      }
    }
    // ...
  }

  // ...
記錄玩家上次的位置
  for (auto& elem : player_map_) {
    auto& player = *elem.second;
    player.last_pos = player.pos;
  }
  cur_aoi_map_idx_ = 1 - cur_aoi_map_idx_;
  return update_infos;
}
```

`Tick` 做的事情很簡單，遍歷有 `sensors` 的玩家，逐個計算 `sensor` 範圍內的實體，即為 AOI。`last_pos` 是用來參與判斷實體是否有進入或者離開 AOI，`_UpdatePlayerAoi` 的程式碼如下：

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

`old_aoi` 是先前一個 `Tick` 計算出來的 AOI，而 `new_aoi` 則是這一輪 `Tick` 需要計算的 AOI。透過遍歷 AOI 範圍內所有格子的實體，在玩家距離小於 AOI 半徑的情況下進行選取。接著使用 `_CheckLeave` 與 `_CheckEnter` 兩個函數，來計算這一輪 `Tick` 中離開與進入 AOI 的實體。例如，若 `new_aoi` 中的實體 `last_pos` 不在 AOI 範圍內，則代表該實體是這一輪 `Tick` 中進入 AOI 範圍的。詳細的程式碼可參考原始檔案，此處不再贅述。

###十字鏈表的實現

與九宮格相比，十字鏈表的實現較為複雜，先來看基本的數據結構：

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

`Sensor` 和 `PlayerAoi` 與九宮格有部分相似，但多了與鏈表相關的節點結構 `CoordNode`。 `CoordNode` 就是鏈表上的一個節點，記錄了本身節點的類型和數值，類型有三種：玩家節點，`Sensor` 左節點，`Sensor` 右節點。

十字鏈表的大部分工作都是在維持鏈表的有序：

當玩家加入時，需要將玩家節點移動到有序的位置上，並在移動玩家節點的同時，處理進入或離開其他玩家 AOI 事件。
玩家移動到正確的位置後，`Sensor` 左右節點從玩家前後位置出發，移動到正確的位置，並處理跨過其他玩家節點時觸發的進入和離開事件。
當玩家移動時，需更新玩家的座標，同時移動玩家節點和`Sensor`的左右節點，以處理 AOI 進入和離開的情形。

移動節點的程式碼如下，每跨越一個節點，就會呼叫一次 `MoveCross` 函數，`MoveCross` 函數根據移動方向、移動節點和跨越節點的類型來決定是進入還是離開 AOI。

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

鏈表的移動很慢，是 `O(n)` 的複雜度，特別是在玩家新加入場景時，玩家需要從無窮遠的地方，逐步移動到正確的位置上，為此需要大量遍歷的節點，消耗很大。為了優化性能，我們可以在場景中固定位置放置燈塔，這種燈塔處理上跟玩家大致相同，只是比玩家多記錄了一份 `detected_by` 數據，`detected_by` 是用來記錄該哨兵實體處在哪些 `Sensor` 範圍內。玩家首次進入場景時，不再從最遠處開始移動，而是找到一個最近的燈塔，把節點插入到燈塔旁邊，並通過燈塔身上的 `detected_by` 數據，快速進入到跟燈塔一致的其他玩家的 AOI 範圍內，然後開始移動到正確的位置上，當然移動的時候也要處理進入和離開。同理，對於 `Sensor`，也可以通過先繼承燈塔的數據，然後從燈塔的位置上移動到正確位置上。通過這兩種優化能夠提升一倍以上的插入玩家性能。

`Sensor` 身上還有一個名叫 `aoi_player_candidates` 的 `HashMap`（這裡為了性能，使用了[khash](https://github.com/attractivechaos/klib/blob/master/khash.h)移動節點觸發的 AOI 事件，實際上只能檢測到 X-Z 座標軸上邊長為 `2r` 的正方形區域，不是嚴格意義上的圓形區域的 AOI，這個正方形區域內的實體都被記錄在`aoi_player_candidates`上，並在`Tick`中遍歷計算圓形區域內的 AOI 範圍，因此稱為`candidates`。

所有十字鏈表的操作都是為了一直維護正方形區域內的實體 `candidates`，十字鏈表中 `Tick` 做的操作跟九宮格幾乎一致，只是遍歷計算 AOI 的 `candidates` 不相同。九宮格的 `candidates` 是 AOI 圓形區域所覆蓋到的格子的實體，而十字鏈表則是由 `Sensor` 左右節點所界定的邊長為 `2r` 的正方形區域中的實體。定性的來說，十字鏈表的 `candidates` 一般都要比九宮格少，所以在 `Tick` 中的遍歷次數少，性能更優，只是十字鏈表還有大量額外的性能消耗在了維護鏈表上，這兩者整體的性能到底孰優孰劣，我們接下來實測看看。

###性能實測

我這裡分別測量了玩家加入場景（Add Player），計算 AOI 進出事件（Tick），玩家更新坐標位置（Update Pos）三種情況的時間消耗。

玩家初始位置會在地圖範圍內隨機生成，然後將玩家加入場景。`player_num` 是玩家數量，`map_size` 則是地圖 X-Z 坐標軸範圍，玩家的位置將在此範圍內均勻地隨機生成，每位玩家都有一個半徑為`100`的`Sensor`作為 AOI，計算時間使用 `boost::timer::cpu_timer`。`player_num` 分別選擇了 `100、1000、10000` 三種情況，而`map_size` 則選擇了`[-50, 50]、[-100, 100]、[-1000, 1000]、[-10000, 10000]`四種情況。

更新玩家位置將使玩家以`6m/s`的速度保持固定的隨機方向移動。

本次測試環境為：

* CPU: Intel(R) Core(TM) i5-4590 CPU @ 3.30GHz
* 系統：Debian GNU/Linux 10（buster）
gcc 版本: gcc版本8.3.0（Debian 8.3.0-6）
增強版本: boost_1_75_0

####九宮格實測

九宮格的測試結果如下：

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

當玩家數量為 `100` 時，九宮格的三種操作耗時非常小。在極限情況下，地圖大小為 `[-50, 50]`，所有玩家互相都處於 AOI 范圍內，每個 `Tick` 大約需要 `0.4ms`。玩家加入場景和更新坐標都具有線性複雜度 `O(player_num)`，性能表現令人滿意。當玩家數量達到 1 萬時，地圖大小維持 `[-50, 50]`，新增玩家和更新位置由於是線性的，可以在幾毫秒內完成，但每個 `Tick` 的時間就會增長至 `3.8s`，需要大量的 CPU 資源，已經無法使用。當玩家數量達到 1 萬，地圖範圍擴大至 `[-1000, 1000]` 時，每個 `Tick` 大約需要花費 `94ms`。如果能降低 `Tick` 頻率，例如每秒兩次，勉強還處於可接受範圍內。

####十字鏈表實測

十字鏈表的測試結果如下：

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

根據我們的分析，十字鏈表在 `新增玩家` 和 `更新位置` 上耗費的時間較長，特別是在 `新增玩家` 的情況下，跟九宮格相比性能差了好幾百甚至上萬倍（`100, [-50, 50]` 十字鏈表耗時 `2ms`，而九宮格只有 `0.08ms`；`10000, [-50, 50]` 十字鏈表為 `21.6s`，而九宮格只有 `6ms`。`更新位置` 的耗時也會有高達數百倍的差異，`10000, [-100, 100]` 十字鏈表更新玩家位置耗時 `1.5s`，而九宮格僅需 `18ms`。可見，十字鏈表在 `新增玩家` 和 `更新位置` 的耗時範圍要比九宮格更大，受到玩家人數和地圖大小的影響更為明顯，在玩家密集區域，這兩個操作的表現會急劇下降，最終導致無法使用。

對比十字鏈的 `Tick` 操作，整體效能確實比九宮格好，最佳情況下時間約只有九宮格的一半（ `1000, [-1000, 1000]` 下十字鏈耗時 `0.8ms`，九宮格 `1.8ms`），但最差情形下十字鏈卻會退化到接近九宮格性能（`10000, [-10000, 10000]` 下十字鏈耗時 `3.7s`，九宮格 `3.8s`）。這是因為場景較小，玩家彼此都在彼此的 AOI 範圍內，十字鏈 `Tick` 遍歷的 `candidates` 數量實際上已經非常接近九宮格了。

要達到比九宮格性能更優的效果，十字鏈在使用上需要一些更強的假設。例如，在 `player_num = 1000, map_size = [-1000, 1000]` 的情況下，十字鏈的 `Tick` 耗時為 `0.8ms`，九宮格為 `1.8ms`；`Update Pos` 方面，十字鏈為 `0.3ms`，九宮格為 `0.18ms`（注意，對 `Update Pos` 的測試時間為執行了 10 次的總和）。總體來看，在 `Tick + Update Pos` 的時間上，要使十字鏈比九宮格更有效率，則 `Update Pos` 的次數不能超過 `Tick` 的 `8` 倍，換言之，兩個 `Tick` 之間，`Update Pos` 的次數需少於 `8` 次。此外，由於十字鏈的 `Add Player` 操作耗時較多，因此不適用於玩家短時間內頻繁進出場景或在場景內大範圍傳送的情況。此外，如果有大量玩家短時間內進入場景，也易導致性能下降，並造成大量 CPU 資源占用。

對於十字鏈表，在一個前提之下還能做一個優化：幹掉 `Tick`，前提是遊戲能接受正方形的 AOI，並且需要實測正方形 AOI 帶來的其他諸如網絡等消耗是能接受的。其實前提是比較苛刻的，因為在遊戲中 AOI 計費能佔用的 CPU 通常佔比是不大的，但把圓形 AOI 改成方形 AOI 導致 AOI 範圍面積增大，範圍內的玩家數量也增多，均勻分佈下玩家數量可能會增多到原來的 `1.27` 倍。但是，一旦能滿足前提，十字鏈表可以做到不需要 `Tick` 來定期更新 AOI 事件，因為實現上十字鏈表的 `candidates` 就維護了一份方形下 AOI，原來只是為了計算圓形 AOI，而不得不在 `Tick` 中再遍歷計算距離。在這種情況下，十字鏈是有可能能夠達到很好的性能，因為十字鏈表 `Update Pos` 的性能可以跟 `Tick` 相差幾倍到幾十倍。

最後提供兩者的對比直方圖：

![](assets/img/2021-11-18-aoi-tesing/add_player.png)

![](assets/img/2021-11-18-aoi-tesing/tick.png)

![](assets/img/2021-11-18-aoi-tesing/update_pos.png)


###總結

本文介紹了兩種AOI算法（九宮格和十字鏈）的原理和基本實現，並通過實測數據分析了這兩種算法的性能優劣，希望能給讀者帶來一些幫助或啟發。

總的來說，九宮格法實現簡單，性能均衡不容易拉胯，非常適合 AOI 不是性能瓶頸的遊戲來使用，九宮格法的性能波動範圍是在可預期的範圍內，性能下限比較高，也不容易導致瓶頸，但另一方面可優化空間也不大，時間複雜度比較固定。反觀十字鏈法，實現要更複雜，性能下限比九宮格法低，但是如果能夠滿足一些假設和前提，十字鏈可優化空間更高，換句話說是上限是可以更高。這兩種方法各有優劣，遊戲業界內也有不同的引擎分別選擇了兩者之一，各取所需，見仁見智。

本人能力有限，文中內容僅代表本人想法，如有不足不妥之處歡迎留言討論。

--8<-- "footer_tc.md"


> 這篇帖子是由 ChatGPT 翻譯的，如果有任何[**反饋**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遺漏之處。 
