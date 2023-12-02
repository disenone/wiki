---
layout: post
title: Game AOI Algorithm Analysis and Performance Testing
categories:
- c++
catalog: true
tags:
- dev
- game
description: 'This text discusses two algorithms: the nine-grid and the cross-link.
  It also provides practical performance analysis for both algorithms, so that you
  can have a clear understanding and remain calm when dealing with them.'
figures: []
date: 2021-11-18
---

<meta property="og:title" content="游戏 AOI 算法解析和性能实测" />

### Introduction

`AOI` (Area Of Interest) is a fundamental feature in multiplayer online games, where players need to receive information about other players or entities entering their field of view. The algorithms that calculate which entities are present within a player's field of view and which entities enter or exit the field of view are generally referred to as `AOI` algorithms.

This article discusses two types of `AOI` algorithms: Grid of Nine and Cross-chain. It also provides performance analysis of these two algorithms to give you a clear understanding and help you remain calm when facing challenges.

The text will mention two terms: "玩家" and "实体". "实体" refers to the concept of objects in the game, while "玩家" refers to entities that have the AOI.

The code mentioned in the text can be found here: [AoiTesting](https://github.com/disenone/AoiTesting).

### Nine-grid/matrix

The so-called "Nine Palace" is a division of the positions of all entities in a scene into grids, for example, dividing them into squares with a side length of 200. To find other entities within the AOI (Area of Interest) of the central player, compare all the players within the grids involved in this range.

For example, in a scene, there is a tick every 100 milliseconds. In the tick function, we can update the player's AOI like this:

* Calculate the set of grids involved in the AOI radius, with the player's position as the center.
* Calculate the distance between each entity in the grid set and the player.
* The set of entities whose distance is less than the AOI radius is the player's new AOI.

The Sudoku algorithm is quite simple to implement. It can be described in a few sentences. We will discuss the performance analysis later. Let's take a look at the Cross-linked List algorithm first.

### Cross-linked list

For 3D games, we usually create ordered linked lists for the X and Z coordinates separately. Each entity has a node on the linked list, storing the corresponding coordinate axis value. The values are stored in ascending order. However, if we only store the coordinates of the entities themselves, the efficiency of querying using these two linked lists is still low.

The real key is that we will add left and right sentinel nodes to each player who has AOI on the linked list. The coordinates of the two sentinels are exactly equal to the player's coordinates plus or minus the AOI radius. For example, if the player `P` has coordinates `(a, b, c)` and the AOI radius is `r`, then there will be two sentinels `left_x` and `right_x` on the X-axis, with coordinates `a - r` and `a + r`, respectively. With the presence of the sentinels, we update AOI by tracking the movement of the sentinels and other entity nodes. Continuing with the previous example, if an entity `E` moves and crosses from the right side of `left_x` to the left side of `left_x` on the X-axis, it means that `E` has definitely left the AOI of `P`; similarly, if it crosses from the left side of `right_x` to the right side of `right_x`, it has also left the AOI. Conversely, if it crosses from the right side of `left_x` or the left side of `right_x`, it means that it may enter the AOI of `P`.

It can be seen that the Cross-link List algorithm is much more complex than the Nine-grid algorithm. We need to maintain two sorted lists and synchronize the movement of nodes on the lists whenever an entity coordinate is updated, and update the AOI when crossing over other nodes.

### Implementation of the Nine-grid System

Because it involves performance measurements, let's delve a little deeper into the implementation details of the Sudoku algorithm.

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

`PlayerAoi` stores player data, including an array called `sensors` which is used to calculate entities within a certain range. After each `Tick`, the calculated entities are then placed in the `aoi_players` array. `aoi_players` is a container that holds two arrays, used to compare the previous `Tick` results and determine players entering or leaving. The general flow of `Tick` is as follows:

```cpp
AoiUpdateInfos SquareAoi::Tick() {
  AoiUpdateInfos update_infos;
  PlayerPtrList remove_list;

  for (auto& elem : player_map_) {
    auto& player = *elem.second;
    // ...
// Calculate Aoi for players with sensors
    if (!player.sensors.empty()) {
      auto update_info = _UpdatePlayerAoi(cur_aoi_map_idx_, &player);
      if (!update_info.sensor_update_list.empty()) {
        update_infos.emplace(update_info.nuid, std::move(update_info));
      }
    }
    // ...
  }

  // ...
// Record the player's last position
  for (auto& elem : player_map_) {
    auto& player = *elem.second;
    player.last_pos = player.pos;
  }
  cur_aoi_map_idx_ = 1 - cur_aoi_map_idx_;
  return update_infos;
}
```

The task performed by `Tick` is very simple. It iterates through players with `sensors` and calculates the entities within the range of the `sensor`, which is referred to as AOI (Area of Interest). `last_pos` is used to determine whether an entity has entered or left the AOI. The code for `_UpdatePlayerAoi` is as follows:

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

The `old_aoi` is the AOI calculated from the previous `Tick`, and the `new_aoi` is the AOI to be calculated for this `Tick`. The `new_aoi` is obtained by traversing all the entities in the grid within the AOI range and selecting those that are within a distance less than the AOI radius from the player. Then, the `_CheckLeave` and `_CheckEnter` functions are used to calculate the entities that leave and enter the AOI in this `Tick`. For example, if an entity's `last_pos` in `new_aoi` is not within the AOI range, it means that the entity has entered the AOI in this `Tick`. The specific code can be found in the source file, and will not be further elaborated here.

### Implementation of Cross-linked List

Compared to the nine-grid, the implementation of the cross-linked list is more complex. Let's first take a look at the basic data structure:

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

`Sensor` and `PlayerAoi` have some similarities with the 9-grid, but with the addition of a linked list-related node structure called `CoordNode`. `CoordNode` represents a node on the linked list, and it records the type and value of the node itself. There are three types: player node, left node of `Sensor`, and right node of `Sensor`.

Most of the work in a cross-linked list is to maintain the order of the list.

* When a player joins, they need to move their player node to the correct position, and at the same time, handle the AOI events of other players entering or leaving.
* After the player moves to the correct position, the left and right nodes of the `Sensor` move from the front and back positions of the player to the correct position, and handle the events triggered when crossing other player nodes, such as entering and leaving.
* When the player moves, update their coordinates and move the player node and the left and right nodes of the `Sensor`, handling AOI enter and leave events.

The code for moving a node is as follows. Each time a node is traversed, the `MoveCross` function is called. Based on the direction of movement, the node being moved, and the type of node being crossed, the `MoveCross` function determines whether to enter or leave the AOI.

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

Moving the linked list is slow, with a complexity of `O(n)`, especially when a new player joins the scene. The player needs to move gradually from a faraway location to the correct position, which requires traversing a large number of nodes and consumes a significant amount of resources. To optimize performance, we can place lighthouses in fixed positions in the scene. These lighthouses function similarly to players, but they additionally maintain a separate set of `detected_by` data, which records the sensors within range of the sentinel entity. When a player first enters the scene, they no longer start moving from the farthest point. Instead, they find the nearest lighthouse, insert their node next to it, and quickly enter the AOI (Area of Interest) range of other players who match the lighthouse's `detected_by` data. Then, they begin moving to the correct position. Of course, during the movement, entering and leaving also need to be handled. Similarly, for sensors, we can first inherit the lighthouse's data and then move to the correct position from the lighthouse's location. By implementing these two optimizations, player insertion performance can be improved by more than double.

`Sensor` has another `HashMap` called `aoi_player_candidates` (here, for performance reasons, [khash](https://github.com/attractivechaos/klib/blob/master/khash.h) is used). The AOI events triggered by node movement can only detect a square area with side length `2r` on the X-Z coordinate axis, which is not strictly a circular AOI. The entities within this square area are recorded in `aoi_player_candidates` and the circular AOI range is calculated by iterating through them in the `Tick` function, hence the name `candidates`.

All operations of the cross-linked list are to continuously maintain the entities `candidates` within the square area. The operations performed by the `Tick` in the cross-linked list are almost identical to those of the 9-grid, except that the calculation of the AOI `candidates` in the traversal is different. The `candidates` in the 9-grid are the entities covered by the circular AOI area in the grid, while the cross-linked list is the entities in the square area defined by the left and right nodes of the `Sensor` with a side length of `2r`. Qualitatively speaking, the `candidates` in the cross-linked list are generally fewer than those in the 9-grid, so the number of traversals in the `Tick` is smaller, resulting in better performance. However, the cross-linked list also has a lot of additional performance overhead on maintaining the list. The overall performance of these two approaches remains to be tested.

### Performance Testing

I have separately tested the time consumption of the player joining the scene (`Add Player`), calculating AOI enter and exit events (`Tick`), and updating player coordinates (`Update Pos`).

The player's initial position is randomly generated within the map range, and then the player is added to the scene. `player_num` represents the number of players, and `map_size` denotes the range of X-Z coordinates on the map. The player's position is uniformly generated within this range. Each player has a `Sensor` with a radius of 100, which is used for AOI (Area of Interest). The boost::timer::cpu_timer is used for time calculation. The `player_num` field includes three scenarios: 100, 1000, and 10000, while the `map_size` field includes four scenarios: [-50, 50], [-100, 100], [-1000, 1000], and [-10000, 10000].

Updating player position will make the player move in a fixed random direction at a speed of `6m/s`.

The current test environment is:

* CPU: Intel(R) Core(TM) i5-4590 CPU @ 3.30GHz
* System: Debian GNU/Linux 10 (buster)
* gcc version: gcc version 8.3.0 (Debian 8.3.0-6)
* boost version: boost_1_75_0

#### Nine-grid Actual Test

The test results for the grid of nine squares are as follows:

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

In the game grid, when there are `100` players, the time required for the three operations is very short. In the extreme case where `map_size = [-50, 50]`, all players are within the AOI range, and the time required for each `Tick` is approximately `0.4ms`. The performance is good, and both the player joining the scene and updating the coordinates have a linear complexity of `O(player_num)`.

However, when the number of players reaches ten thousand (`player_num = 10000`) with a map size of `[-50, 50]`, both the `Add Player` and `Update Pos` operations can be completed within a few milliseconds due to their linear complexity. But the `Tick` operation takes up to `3.8s`, requiring a significant amount of CPU resources and rendering it unusable. In the case of ten thousand players and a map size of `[-1000, 1000]`, the `Tick` operation consumes approximately `94ms`. If the `Tick` frequency is reduced, for example, to twice per second, it can still be considered usable, albeit with some difficulty.

#### Cross-linked List Measurement

The test results of the cross-linked list are as follows:

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

As we analyze, the cross-linked list takes more time in `Add Player` and `Update Pos`, especially in `Add Player`, which is several hundred or even tens of thousands times slower than the grid performance (`100, [-50, 50]` cross-linked list takes `2ms`, while the grid only takes `0.08ms`; `10000, [-50, 50]` cross-linked list takes `21.6s`, while the grid only takes `6ms`). There can also be a difference of up to a hundredfold in the execution time of `Update Pos`, where `10000, [-100, 100]` cross-linked list takes `1.5s`, while the grid takes only `18ms`. It can be observed that the cross-linked list has a wider range of execution time for `Add Player` and `Update Pos` compared to the grid, and is more affected by the number of players and the size of the map. In densely populated areas, the performance of these two operations will rapidly decline until they become unusable.

Looking at the `Tick` operation of the Cross-chain, the overall performance is indeed better than that of the Nine-grid. In the best case, the time consumed is approximately only half of the Nine-grid's time (`0.8ms` for Cross-chain with `1000, [-1000, 1000]`, and `1.8ms` for Nine-grid), but in the worst case, the performance of the Cross-chain will degrade to be close to that of the Nine-grid (`3.7s` for Cross-chain with `10000, [-10000, 10000]`, and `3.8s` for Nine-grid). This is because, due to the small scene, players are all within each other's AOI range, and the number of `candidates` traversed by the Cross-chain `Tick` is actually very close to that of the Nine-grid.

The Cross-Chain needs to achieve better performance than the Nine-Grid when used. This requires some stronger assumptions, such as `player_num = 1000, map_size = [-1000, 1000]`. In this case, the Cross-Chain takes 0.8ms for `Tick`, while the Nine-Grid takes 1.8ms; for `Update Pos`, the Cross-Chain takes 0.3ms and the Nine-Grid takes 0.18ms (note that the test time for `Update Pos` is the sum of the time for 10 executions). In order for the Cross-Chain to be faster than the Nine-Grid in terms of the total time of `Tick + Update Pos`, the number of `Update Pos` operations cannot exceed 8 times the number of `Tick` operations, or in other words, the number of `Update Pos` operations between two `Tick` operations needs to be less than 8 times. 

Furthermore, due to the significant time consumption of `Add Player` in the Cross-Chain, it is not suitable for scenarios where players frequently enter and exit scenes within a short period of time or when there is large-scale teleportation within the scene. Additionally, if a large number of players enter the scene within a short period of time, it can easily lead to performance degradation and consume a significant amount of CPU resources.

For the cross-linked list, there is an optimization that can be done under one condition: get rid of `Tick`. The condition is that the game can accept a square-shaped AOI, and the additional costs such as network consumption brought by the square-shaped AOI are acceptable when measured. Actually, the condition is quite strict, because in the game, the CPU usage of AOI calculation is usually not significant. However, changing the circular AOI to a square AOI increases the area of the AOI range, and the number of players within the range may increase, possibly up to 1.27 times the original amount under a uniform distribution. However, once the condition is met, the cross-linked list can eliminate the need for `Tick` to periodically update AOI events, because the `candidates` of the cross-linked list already maintains a square-shaped AOI, which was originally used only for calculating the circular AOI distance in `Tick`. In this case, the cross-linked list has the potential to achieve excellent performance, as the performance of the cross-linked list's `Update Pos` can be several times to tens of times better than `Tick`.

Finally, here is a comparative bar graph of the two:

![](assets/img/2021-11-18-aoi-tesing/add_player.png)

![](assets/img/2021-11-18-aoi-tesing/tick.png)

![](assets/img/2021-11-18-aoi-tesing/update_pos.png)


### Summary

In this article, we introduce the principles and basic implementations of two AOI algorithms (grid-based and cross-linked), and analyze the performance pros and cons of these two algorithms through empirical data. We hope that this will provide some assistance or inspiration to the readers.

In general, the Nine-grid method is easy to implement and has balanced performance. It is very suitable for games that are not performance-intensive, such as AOI. The performance fluctuation range of the Nine-grid method is within the expected range, with a relatively high performance lower limit, making it less likely to become a bottleneck. However, on the other hand, the optimization space is not large, and the time complexity is relatively fixed. 
On the contrary, the Cross-chain method has a more complex implementation and a lower performance lower limit compared to the Nine-grid method. However, if certain assumptions and prerequisites can be met, the Cross-chain method can offer higher optimization space, in other words, the upper limit can be higher. 
These two methods have their own advantages and disadvantages. Different game engines in the gaming industry have chosen one of them. It's a matter of personal preference and needs.

I have limited ability, and the content of this text only represents my own thoughts. If there are any deficiencies or inappropriate aspects, please feel free to leave a comment for discussion.

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
