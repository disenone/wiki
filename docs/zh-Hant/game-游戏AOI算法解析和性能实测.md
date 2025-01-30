---
layout: post
title: 遊戲 AOI 演算法解析和性能實測
categories:
- c++
catalog: true
tags:
- dev
- game
description: 本文討論九宮格和十字鏈兩種演算法，並給出兩種演算法的實測性能分析，讓你使用時心中有數，遇事不慌。
figures: []
date: 2021-11-18
---

<meta property="og:title" content="游戏 AOI 算法解析和性能实测" />

###引子

`AOI` (關注區域) 在多人線上遊戲中是一個非常基本的功能，玩家需要接收進入視野範圍內的其他玩家或實體 (Entity) 的資訊。計算玩家視野範圍內存在哪些實體，以及有哪些實體進入或離開視野的算法，我們一般稱之為 `AOI` 算法。

本文討論九宮格和十字鏈兩種 `AOI` 算法，並給出兩種算法的實測性能分析，讓你用起來心中有數，遇事不慌。

文中會提到玩家和實體兩種詞，實體是遊戲中物體的概念，玩家是擁有 AOI 的實體。

文中的程式碼可以在這裡找到：[AoiTesting](https://github.com/disenone/AoiTesting)。

###九宮格

九宮格是指將場景中所有實體的位置劃分為網格，例如將其劃分為邊長為200的正方形。要找出中心玩家AOI範圍內的其他實體，就必須比對這個範圍內涉及到的所有網格內的玩家。

例如場景每 100 毫秒會 Tick 一次，在 Tick 中我們可以這樣更新玩家的 AOI：

以玩家位置為中心，AOI 半徑計算涉及到的格子集合
對格子集合中的實體逐個計算跟玩家的距離
* 距離小於 AOI 半徑的實體集合則是玩家的新 AOI

九宮格演算法做起來很簡單，演算法用幾句話就能描述清楚了，具體的性能分析我們留到後面，先來看看十字鏈表演算法。

###十字鏈表

對於3D遊戲，一般會分別為X軸和Z軸坐標構建有序的鏈表，每個實體在鏈表上都有一個節點，存放的是該坐標軸的值，按照值遞增的順序來排列。但如果僅存放實體本身的坐標點，這兩個鏈表仍然無法提高查詢效率。

真正關鍵的是，我們在鏈表上還會給擁有 AOI 的每個玩家增加左右兩個哨兵節點。兩個哨兵的坐標值跟玩家本身坐標正好相差了 AOI 半徑，例如玩家 `P` 坐標為 `(a, b, c)`，AOI 半徑為 `r`，那麼在 X 軸上會有兩個哨兵 `left_x, right_x`，坐標值分別為 `a - r` 和 `a + r`。由於有哨兵的存在，我們通過跟踪哨兵跟其他實體節點的移動來更新 AOI。繼續前面的例子，一個實體 `E` 移動導致在 X 軸上的節點從 `left_x` 的右邊想左跨過 `left_x` 來到 `left_x` 的左邊，那麼說明 `E` 肯定是離開了 `P` 的 AOI；同理如果向右跨過了 `right_x` 也是離開了 AOI。相反，如果是向右跨過 `left_x`，或者向左跨過 `right_x`，說明有可能會進入到 `P` 的 AOI 中。

可以看到，十字鏈表演算法要比九宮格複雜得多，我們需要維護兩條有序的鏈表，並且在每個實體座標更新的時候，同步移動鏈表上的節點，並且在移動跨過其他節點時更新 AOI。

###九宮格的實現

因為涉及到實測的性能，所以我們先來稍微深入一點九宮格算法的實現細節：

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

`PlayerAoi` 類別用來儲存玩家資料，其中包含一個 `sensors` 陣列，用於計算特定範圍內的實體。每次執行 `Tick` 後，計算出的實體將被放置在 `aoi_players` 中。`aoi_players` 包含兩個陣列，用於比較前後兩次 `Tick` 的結果，以判斷進入或離開玩家的實體。`Tick` 的主要流程如下：

```cpp
AoiUpdateInfos SquareAoi::Tick() {
  AoiUpdateInfos update_infos;
  PlayerPtrList remove_list;

  for (auto& elem : player_map_) {
    auto& player = *elem.second;
    // ...
// 對有 sensors 的玩家計算 Aoi
    if (!player.sensors.empty()) {
      auto update_info = _UpdatePlayerAoi(cur_aoi_map_idx_, &player);
      if (!update_info.sensor_update_list.empty()) {
        update_infos.emplace(update_info.nuid, std::move(update_info));
      }
    }
    // ...
  }

  // ...
// 記錄玩家上次的位置
  for (auto& elem : player_map_) {
    auto& player = *elem.second;
    player.last_pos = player.pos;
  }
  cur_aoi_map_idx_ = 1 - cur_aoi_map_idx_;
  return update_infos;
}
```

`Tick` 做的事情很簡單，遍歷有 `sensors` 的玩家，逐個計算 `sensor` 範圍內的實體，即為 AOI。`last_pos` 是用來參與判斷實體是否有進入或者離開 AOI，`_UpdatePlayerAoi` 的代碼如下：

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

`old_aoi` 是上一个 `Tick` 計算出來的 AOI，`new_aoi` 是本次 `Tick` 需要計算的 AOI。`new_aoi` 透過遍歷 AOI 範圍內的所有格子的實體，選出與玩家距離小於 AOI 半徑以獲得。之後用 `_CheckLeave` 和 `_CheckEnter` 兩個函數，計算本次 `Tick` 離開和進入 AOI 的實體，例如如果 `new_aoi` 中的實體 `last_pos` 不在 AOI 範圍內，說明該實體是在本次 `Tick` 進入了 AOI 範圍。具體的代碼可以查看源文件，這裡不再贅述。

###十字鏈表的實現

與九宮格相比，十字鏈表的實現較為複雜，首先看看基本的數據結構：

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

`Sensor` 和 `PlayerAoi` 跟九宮格有部分相似，不過多了鏈表相關的節點結構 `CoordNode`。`CoordNode` 就是鏈表上的一個節點，記錄了本身節點的類型和數值，類型有三種：玩家節點，`Sensor` 左節點，`Sensor` 右節點。

十字鏈表的大部分工作都是在維持鏈表的有序：

* 玩家加入時需要把玩家節點移動到有序的位置上，並且在移動玩家節點的同時，處理進入或者離開其他玩家 AOI 事件。
當玩家移動到正確位置後，`Sensor` 左右節點會從玩家前後位置出發，移動到正確位置，並處理當穿越其他玩家節點時觸發的進入和離開事件。
當玩家移動時，更新玩家的座標，並移動玩家節點和 `Sensor` 的左右節點，處理 AOI 進入離開。

移動節點的程式碼如下，每穿越一個節點，都會呼叫一次 `MoveCross` 函數，由 `MoveCross` 函數根據移動方向、移動節點和穿越節點的類型來決定是進入還是離開 AOI。

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

鏈表的移動非常緩慢，時間複雜度為 `O(n)`，尤其是當玩家新加入場景時，需要從遠處逐步移動到正確位置，必須遍歷大量節點，消耗龐大。為了優化性能，我們可以在場景中固定位置放置燈塔。這種燈塔處理方式與玩家大致相同，只是多了一份 `detected_by` 資料，用於記錄哨兵實體位於哪些 `Sensor` 範圍內。當玩家首次進入場景時，不再從最遠處開始移動，而是尋找最近的燈塔，將節點插入燈塔旁邊，並透過燈塔的 `detected_by` 資料，迅速進入與燈塔相同的其他玩家 AOI 範圍內，然後開始移動到正確位置上，當然在移動時也必須處理進入和離開。同樣地，對於 `Sensor`，也可以透過繼承燈塔資料，再從燈塔位置移動到正確位置。透過這兩種優化方式，可以提升一倍以上插入玩家的性能。

`Sensor` 身上還有一個名叫 `aoi_player_candidates` 的 `HashMap`（這裡為了性能，使用了[khash](https://github.com/attractivechaos/klib/blob/master/khash.h)）。節點移動觸發的 AOI 事件，其實只能檢測到 X-Z 坐標軸上邊長為 `2r` 的正方形區域，不是我們嚴格意義上的圓形區域的 AOI，這個正方形的區域內的實體都被記錄在 `aoi_player_candidates` 上，並在 `Tick` 中遍歷計算圓形區域內的 AOI 範圍，所以稱為 `candidates`。

所有十字鏈表的操作都是為了一直維護正方形區域內的實體 `candidates`，十字鏈表中 `Tick` 做的操作跟九宮格幾乎一致，只是遍歷計算 AOI 的 `candidates` 不相同。九宮格的 `candidates` 是 AOI 圓形區域所覆蓋到的格子的實體，而十字鏈表則是由 `Sensor` 左右節點所界定的邊長為 `2r` 的正方形區域中的實體。定性的來說，十字鏈表的 `candidates` 一般都要比九宮格少，所以在 `Tick` 中的遍歷次數少，性能更優，只是十字鏈表還有大量額外的性能消耗在了維護鏈表上，這兩者整體的性能到底孰優孰劣，我們接下來實測看看。

###性能實測

我這裡分別測量了玩家加入場景（`Add Player`）、計算 AOI 進出事件（`Tick`）、玩家更新坐標位置（`Update Pos`）這三種情況的時間消耗。

玩家初始位置將在地圖範圍內隨機生成，然後將玩家加入場景。`player_num` 指的是玩家人數，`map_size` 則是地圖 X-Z 座標軸範圍，玩家的位置將在這個範圍內均勻地隨機生成，每個玩家都會有一個半徑為 `100` 的感應器 `Sensor` 用作 AOI，時間計算則使用 `boost::timer::cpu_timer`。分別選擇了 `100, 1000, 10000` 三種不同`player_num`情況，而 `map_size` 則選擇了 `[-50, 50], [-100, 100], [-1000, 1000], [-10000, 10000]` 四種情況。

更新玩家位置會讓玩家固定隨機方向，以 `6m/s` 的速度移動。

這次測試環境為：

* CPU: Intel(R) Core(TM) i5-4590 CPU @ 3.30GHz
系統: Debian GNU/Linux 10 (buster)
* gcc 版本: gcc 版本 8.3.0 (Debian 8.3.0-6)
* boost 版本: boost_1_75_0

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

在有 `100` 名玩家的情况下，当九宫格运作时，三种操作所需的时间都很短。在极端情况下，地图大小为 `[-50, 50]`，所有玩家互相都在AOI范围内，每次Tick运行大约需要 `0.4毫秒`。玩家加入场景和更新坐标都是按照玩家数量的线性复杂度 `O(player_num)` 进行。在有 1 万名玩家，地图大小为 `[-50, 50]` 的情况下，`Add Player` 和 `Update Pos` 都能在几毫秒内完成，但每次 `Tick` 运行则需要 `3.8秒`，需要耗费大量的CPU资源，已经不可用。当有 1 万名玩家，地图大小为 `[-1000, 1000]`时，每次 `Tick` 运行大约需要 `94毫秒`。如果能够降低 `Tick` 的频次，例如降低到每秒两次，那仍勉强属于可用的范围内。

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

如我們分析一致，十字鏈表在 `Add Player` 和 `Update Pos` 上耗時更長，特別是 `Add Player`，相比九宮格性能差了幾百甚至上萬倍（`100, [-50, 50]` 十字鏈耗時 `2ms`，而九宮格只有 `0.08ms`；`10000, [-50, 50]` 十字鏈 `21.6s`，九宮格只有 `6ms`。`Update Pos` 的耗時也最多會有百倍的差距，`10000, [-100, 100]` 十字鏈更新玩家位置耗時 `1.5s`，而九宮格是 `18ms`。可以看出，十字鏈在 `Add Player` 和 `Update Pos` 耗時的上下限範圍比九宮格要大，受人數和地圖大小影響更大，在玩家密集的區域，這兩個操作的性能會急速下降，直至不可用。

觀察十字鏈的 "Tick" 操作，整體表現確實比九宮格好，最佳情況下所需時間大約只有九宮格的一半左右（"1000，[-1000，1000]" 的情況下，十字鏈花費 0.8 毫秒，而九宮格需要 1.8 毫秒），不過在最差情況下，十字鏈的表現會降級到接近九宮格的水平（"10000，[-10000，10000]" 的情況下，十字鏈花費 3.7 秒，九宮格花費 3.8 秒）。這是因為場景較小，玩家彼此間都處於對方的 AOI 範圍內，十字鏈 "Tick" 遍歷的候選數量實際上已經非常接近九宮格了。

十字練使用起來要達到比九宮格性能更優，需要一些更強的假設，例如 `player_num = 1000, map_size = [-1000, 1000]` 情況下，`Tick` 耗時十字練為 `0.8ms` 九宮格 `1.8ms`，`Update Pos` 十字練為 `0.3ms` 九宮格 `0.18ms`（注意測試 `Update Pos` 時間為執行了 10 次的時間總和）。`Tick + Update Pos` 總時間下，十字練如果要比九宮格更少，那 `Update Pos` 的次數不能超過 `Tick` 的 `8` 倍，或者說兩個 `Tick` 之間，`Update Pos` 的次數需要小於 `8` 次。另外因為十字練 `Add Player` 耗時巨大，不適用於玩家短時間頻繁出入場景或者在場景內大範圍傳送的情況，另外如果短時間內有大量玩家進入場景，也很容易導致性能下降，大量佔用 CPU。

對於十字鏈表，在一個前提之下還能做一個優化：幹掉 `Tick`，前提是遊戲能接受正方形的 AOI，並且需要實測正方形 AOI 帶來的其他諸如網路等消耗是能接受的。其實前提是比較苛刻的，因為在遊戲中 AOI 計費能佔用的 CPU 通常占比是不大的，但把圓形 AOI 改成方形 AOI 導致 AOI 範圍面積增大，範圍內的玩家數量也增多，均勻分布下玩家數量可能會增多到原來的 `1.27` 倍。但是，一旦能滿足前提，十字鏈表可以做到不需要 `Tick` 來定期更新 AOI 事件，因為實現上十字鏈表的 `candidates` 就維護了一份方形下的 AOI，原來只是為了計算圓形 AOI，而不得不在 `Tick` 中再遍歷計算距離。在這種情況下，十字鏈是有可能能夠達到很好的性能，因為十字鏈表 `Update Pos` 的性能可以跟 `Tick` 相差幾倍到幾十倍。

最後給出兩者的對比柱狀圖：

![](assets/img/2021-11-18-aoi-tesing/add_player.png)

![](assets/img/2021-11-18-aoi-tesing/tick.png)

![](assets/img/2021-11-18-aoi-tesing/update_pos.png)


###總結

本文介紹了兩種AOI演算法（九宮格和十字鍊）的原理和基本實現，並透過實測數據分析了這兩種演算法的性能優劣，希望能夠為讀者帶來一些幫助或者啟發。

總的來說，九宮格法實現簡單，性能均衡不容易掉鏈，非常適合 AOI 不是性能瓶頸的遊戲來使用，九宮格法的性能波動範圍是在可預期的範圍內，性能下限比較高，也不容易導致瓶頸，但另一方面可優化空間也不大，時間複雜度比較固定。反觀十字鏈法，實現要更複雜，性能下限比九宮格法低，但是如果能夠滿足一些假設和前提，十字鏈可優化空間更高，換句話說是上限是可以更高。這兩種方法各有優劣，遊戲業界內也有不同的引擎分別選擇了兩者之一，各取所需，見仁見智。

本人能力有限，文中內容僅代表本人想法，如有不足不妥之處歡迎留言討論。

--8<-- "footer_tc.md"


> 此帖子是使用 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遺漏之處。 
