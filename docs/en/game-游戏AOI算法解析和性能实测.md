---
layout: post
title: Analysis and Performance Evaluation of the Game AOI Algorithm
categories:
- c++
catalog: true
tags:
- dev
- game
description: 'This article discusses two algorithms: the nine-grid and the cross-chain
  algorithms, and provides a performance analysis based on practical measurements
  for both algorithms, enabling you to feel confident and composed when faced with
  challenges.'
figures: []
date: 2021-11-18
---

<meta property="og:title" content="游戏 AOI 算法解析和性能实测" />

###Preface

`AOI` (Area Of Interest) is a fundamental feature in multiplayer online games, where players need to receive information about other players or entities that enter their field of vision. The algorithms we generally refer to as `AOI` algorithms calculate which entities exist within a player's visual range and which entities enter or leave that range.

This article discusses two `AOI` algorithms: the nine-grid and the cross-link algorithms, and provides a practical performance analysis of both algorithms, ensuring you have a clear understanding and stay calm in challenging situations.

The text will mention two terms: "players" and "entities." Entities refer to objects in the game, while players are entities with AOI.

The code mentioned in the text can be found here: [AoiTesting](https://github.com/disenone/AoiTesting).

###Nine-square grid

The so-called Nine-Grid is a method of dividing the positions of all entities in a scene into squares, such as dividing them into squares with a side length of 200. To find other entities within the AOI range of the central player, compare all the players within the squares involved in this range.

For example, the scene ticks every 100 milliseconds, and during each tick, we can update the player's AOI like this:

* The collection of grids involved in calculating the AOI radius centered around the player's position.
Calculate the distance between each entity in the grid set and the player one by one.
The collection of entities within a distance less than the AOI radius becomes the player's new AOI.

The nine-grid algorithm is quite simple to implement, and it can be clearly described in just a few sentences. We will leave the detailed performance analysis for later; for now, let's take a look at the cross-linked list algorithm.

###Cross-linked List

For 3D games, we usually construct ordered linked lists for both the X-axis and Z-axis coordinates. Each entity has a node on the list storing its coordinate axis value, arranged in increasing order. However, the efficiency of querying remains low if only the entity's coordinate points are stored in these two lists.

The real key here is that we add two sentinel nodes on the linked list for each player with AOI. The coordinates of the two sentinels are exactly AOI radius away from the player's coordinates. For example, if a player's coordinates are `(a, b, c)` and the AOI radius is `r`, on the X-axis, there will be two sentinels `left_x` and `right_x` with coordinates `a - r` and `a + r` respectively. With the sentinels in place, we track the movement of the sentinels and other entities to update the AOI. Using the previous example, if an entity `E` moves such that on the X-axis it moves from the right of `left_x` to the left of `left_x`, it means that `E` has left the AOI of `P`. Similarly, crossing `right_x` towards the right also means leaving the AOI. Conversely, crossing `left_x` towards the right or crossing `right_x` towards the left indicates a possible entry into the AOI of `P`.

It can be seen that the cross-linked list algorithm is much more complex than the grid method. We need to maintain two ordered linked lists, and during each entity coordinate update, we must synchronize the movement of the nodes on the linked lists and update the AOI when crossing over other nodes.

###Implementation of the Nine-Grid Layout

Because it involves actual performance testing, let's delve a little deeper into the implementation details of the Sudoku algorithm:

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

`PlayerAoi` stores the player data, which includes an array called `sensors`. The `sensors` are used to calculate the entities within a certain range, and after each `Tick`, the calculated entities are placed in `aoi_players`. The `aoi_players` contains two arrays used for comparison with the results from the last `Tick` to determine which players have entered and exited. The general flow of the `Tick` process is as follows:

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
Record the player's last position
  for (auto& elem : player_map_) {
    auto& player = *elem.second;
    player.last_pos = player.pos;
  }
  cur_aoi_map_idx_ = 1 - cur_aoi_map_idx_;
  return update_infos;
}
```

The task of `Tick` is quite simple; it iterates over players with `sensors`, calculating the entities within the range of each `sensor`, which constitutes the AOI. `last_pos` is used to determine whether an entity has entered or exited the AOI. The code for `_UpdatePlayerAoi` is as follows:

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

`old_aoi` is the AOI calculated from the previous `Tick`, while `new_aoi` is the AOI to be calculated for the current `Tick`. `new_aoi` is obtained by iterating through all the entities within the AOI range and selecting those whose distance to the player is less than the AOI radius. Then, using the functions `_CheckLeave` and `_CheckEnter`, the entities entering and leaving the AOI for the current `Tick` are calculated. For example, if an entity's `last_pos` in `new_aoi` is not within the AOI range, it indicates that this entity has entered the AOI range during the current `Tick`. The specific code can be found in the source file, and it won't be elaborated on here.

###Implementation of Cross Linked List

Compared to a grid layout, a cross-linked list is more complex to implement. Let's first look at the basic data structure:

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

`Sensor` and `PlayerAoi` are somewhat similar to the 9-grid, but with the additional linked list related node structure `CoordNode`. `CoordNode` is a node on the linked list, which records the type and value of the node itself. There are three types: player node, left node of `Sensor`, and right node of `Sensor`.

The majority of the work of the cross-linked list is in maintaining the order of the list:

* When a player joins, they need to move the player node to an ordered position, and while moving the player node, handle the events of entering or leaving the AOI of other players.
After the player moves to the correct position, the left and right nodes of the `Sensor` move from the player's front and back positions to the correct position and handle the entering and exiting events triggered when crossing other player nodes.
* When the player moves, update the player's coordinates, and move the player node and the `Sensor` left and right nodes, handling the entry and exit of the AOI.

The code for the moving node is as follows: every time it crosses a node, the `MoveCross` function is called. The `MoveCross` function determines whether to enter or exit the AOI based on the direction of movement and the type of node being crossed.

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

The movement of linked lists is quite slow, with a complexity of `O(n)`, especially when a new player joins the scene. The player must gradually move from an infinite distance to the correct position, which requires a significant number of nodes to traverse and incurs considerable overhead. To optimize performance, we can place fixed-position beacons within the scene. These beacons function similarly to players, but they additionally record a `detected_by` data field, which indicates which `Sensor` ranges the sentinel entity is within. When a player enters the scene for the first time, they no longer start from the farthest point; instead, they locate the nearest beacon, insert the node next to it, and quickly enter the area of interest (AOI) of other players aligned with the beacon using the `detected_by` data on the beacon. They then begin moving to the correct position while also handling entry and exit during the movement. Similarly, for `Sensors`, they can inherit the data from the beacons and then move from the beacon's position to their correct location. These two optimizations can enhance player insertion performance by more than double.

The `Sensor` has a `HashMap` named `aoi_player_candidates` (here, for performance reasons, [khash](https://github.com/attractivechaos/klib/blob/master/khash.h)The AOI event triggered by node movement can actually only detect a square area with a side length of `2r` on the X-Z coordinate axes, rather than a strictly circular AOI. The entities within this square area are all recorded in `aoi_player_candidates`, and during `Tick`, we iterate through and calculate the AOI range within the circular area, hence they are referred to as `candidates`.

All operations in the cross-linked list are aimed at continuously maintaining the entities `candidates` within the square region. The operations performed by the cross-linked list are almost identical to the nine-grid, except for the calculation and traversal of the `candidates` for the AOI. In the nine-grid, the `candidates` consist of the entities covered by the circular AOI, while the cross-linked list defines the entities within a square region of side length `2r` delimited by the left and right nodes of the `Sensor`. Qualitatively speaking, the `candidates` in the cross-linked list are generally fewer than those in the nine-grid, resulting in a lower number of traversals in `Tick` and thus better performance. However, the cross-linked list incurs additional performance overhead in maintaining the list. The overall performance comparison between the two remains to be determined, and we will carry out practical tests to evaluate this aspect.

###Performance testing.

I have separately measured the time consumption for three scenarios: player joining the scene ("Add Player"), calculating AOI in-and-out events ("Tick"), and updating player coordinates ("Update Pos").

The player's starting position is randomly generated within the map range, and then the player is added to the scene. `player_num` represents the number of players, while `map_size` indicates the range of the map on the X-Z coordinate axis. The player's position is uniformly randomly generated within this range. Each player has a `Sensor` with a radius of `100` as the Area of Interest (AOI), and the calculation time is done using `boost::timer::cpu_timer`. Three scenarios for `player_num` - `100, 1000, 10000` were chosen, while four scenarios for `map_size` - `[-50, 50], [-100, 100], [-1000, 1000], [-10000, 10000]` were selected.

Updating the player's position will cause the player to move in a fixed random direction at a speed of `6m/s`.

The current test environment is:

* CPU: Intel(R) Core(TM) i5-4590 CPU @ 3.30GHz
* System: Debian GNU/Linux 10 (buster)
* GCC version: GCC version 8.3.0 (Debian 8.3.0-6)
* boost version: boost_1_75_0

####Nine-grid test

The test results for the 3x3 grid are as follows:

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

The game runs smoothly with 100 players in a tic-tac-toe grid, all operations are quick. In an extreme scenario with a map size of [-50, 50], all players are within the AOI range, and each game tick takes about 0.4ms. Adding players and updating their coordinates are both of linear complexity O(player_num), showing good performance. However, with 10,000 players and the same map size of [-50, 50], things change. Adding players and updating their positions can be done within a few milliseconds due to their linear nature, but each tick now takes around 3.8s, requiring a significant amount of CPU and rendering it unusable. With 10,000 players and a map size of [-1000, 1000], each tick takes around 94ms. If the tick rate could be reduced, for example, to twice per second, it would still fall within an acceptable range.

####Doubly Linked List Test Results

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

As we have analyzed consistently, the cross-linked list takes significantly longer for `Add Player` and `Update Pos`, especially for `Add Player`, which is several hundred to even ten thousand times slower than the grid method (for `100, [-50, 50]`, the cross-linked list takes `2ms`, while the grid only takes `0.08ms`; for `10000, [-50, 50]`, the cross-linked list takes `21.6s`, whereas the grid only takes `6ms`). The time taken for `Update Pos` can also differ by as much as a hundredfold, with the cross-linked list taking `1.5s` to update the player position for `10000, [-100, 100]`, while the grid takes `18ms`. It is evident that the variability in time taken for `Add Player` and `Update Pos` with the cross-linked list is greater than that of the grid method, being more influenced by the number of players and the size of the map. In densely populated areas, the performance of these two operations rapidly declines to the point of becoming unusable.

In contrast to the `Tick` operation of the cross-chain, its overall performance is indeed better than that of the grid system. In the best-case scenario, the time taken is roughly half that of the grid (for `1000, [-1000, 1000]`, the cross-chain takes `0.8ms`, while the grid takes `1.8ms`). However, in the worst-case scenario, the performance of the cross-chain deteriorates to levels close to that of the grid (for `10000, [-10000, 10000]`, the cross-chain takes `3.7s`, while the grid takes `3.8s`). This is because, in smaller scenes, players are within each other's AOI range, resulting in the number of `candidates` traversed by the cross-chain `Tick` becoming quite similar to that of the grid.

To achieve better performance than the Nine-palace Grid, the Cross-chain requires some stronger assumptions. For example, with `player_num = 1000, map_size = [-1000, 1000]`, in the scenario where `Tick` consumes 0.8ms for the Cross-chain and 1.8ms for the Nine-palace Grid, and `Update Pos` takes 0.3ms for the Cross-chain and 0.18ms for the Nine-palace Grid (note that the `Update Pos` time is the sum of 10 executions). In the total time of `Tick + Update Pos`, for the Cross-chain to be faster than the Nine-palace Grid, the number of `Update Pos` cannot exceed 8 times that of `Tick`, or in other words, between two `Tick`s, the number of `Update Pos` needs to be less than 8. Furthermore, due to the significant time consumption of `Add Player` in the Cross-chain, it is not suitable for scenarios where players frequently enter and exit scenes within a short period or undergo large-scale teleportation in the scene. Additionally, a large number of players entering the scene within a short period can easily lead to performance degradation and significant CPU consumption.

For the cross-linked list, there is an optimization that can be performed under one condition: eliminate `Tick`, provided that the game can accept square AOIs, and the actual measured costs associated with square AOIs, such as network usage, are acceptable. This condition is quite stringent because, in games, the CPU usage for AOI billing is usually minimal. However, changing from circular AOIs to square AOIs results in an increased area, which also leads to a higher number of players within that range. If players are evenly distributed, their numbers could increase to about `1.27` times the original. Nevertheless, once the condition is met, the cross-linked list can operate without needing `Tick` for regular AOI event updates, because the `candidates` in the implementation of the cross-linked list already maintain a set of square AOIs, which were initially only used for calculating circular AOIs and necessitated additional distance calculations during `Tick`. In this context, the cross-linked list has the potential to achieve excellent performance, as the performance of `Update Pos` in the cross-linked list can differ from `Tick` by several times to even dozens of times.

Finally, provide a bar chart comparing the two.

![](assets/img/2021-11-18-aoi-tesing/add_player.png)

![](assets/img/2021-11-18-aoi-tesing/tick.png)

![](assets/img/2021-11-18-aoi-tesing/update_pos.png)


###Summary

In this article, we introduce the principles and basic implementations of two AOI algorithms (nine-grid and cross-chain), and analyze the performance advantages and disadvantages of these two algorithms through actual test data, hoping to provide readers with some help or inspiration.

In general, the nine-grid method is simple to implement, with balanced performance that doesn't easily fall short. It is highly suitable for games that do not rely heavily on performance like AOI. The performance fluctuations of the nine-grid method fall within an expected range, with a relatively high performance floor that avoids bottlenecks. On the other hand, the optimization space is limited, and the time complexity is more consistent. On the contrary, the cross-linked method is more complex to implement, with a lower performance floor compared to the nine-grid method. However, if certain assumptions and premises are met, the cross-linked method can offer higher optimization space, meaning the upper limit can be higher. Both methods have their pros and cons, with different game engines in the industry opting for either one based on their specific needs and considerations. It's a matter of preference and individual judgment.

My abilities are limited, and the content of this article only represents my thoughts. Feel free to leave comments for discussion if there are any shortcomings or inappropriate aspects.

--8<-- "footer_en.md"


> This post was translated using ChatGPT, please provide [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions. 
