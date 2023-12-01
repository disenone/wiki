---
layout: post
title: Game AOI Algorithm Analysis and Performance Testing
categories:
- c++
catalog: true
tags:
- dev
- game
description: 'This article discusses two algorithms: the 9-box grid and the cross-link.
  It also provides a practical performance analysis of both algorithms, so that you
  can have a clear understanding and remain calm when faced with any situation.'
figures: []
date: 2021-11-18
---


### Prologue

`AOI` (Area Of Interest) is a fundamental feature in multiplayer online games, where players need to receive information about other players or entities (Entity) that enter their field of view. The algorithms used to determine which entities are present in a player's field of view, as well as which entities enter or leave the field of view, are commonly referred to as `AOI` algorithms.

This article discusses two types of `AOI` algorithms - Grid AOI and Cross-link AOI. It also provides empirical performance analysis for both algorithms to give you a clear understanding and avoid panic when facing problems.

In the text, two terms will be mentioned: "player" and "entity". "Entity" refers to the concept of objects in the game, while "player" is an entity that possesses AOI.

The code mentioned in the text can be found here: [AoiTesting](https://github.com/disenone/AoiTesting).

### Nine-grid

The so-called Nine-square Grid is a way of dividing the positions of all entities in a scene into grids, for example, dividing them into squares with a side length of 200. In order to find out the other entities within the AOI range of the central player, we need to compare all the players in the grids involved in this range.

For example, the scene will tick once every 100 milliseconds, and in the tick function, we can update the player's AOI in the following way:

- Calculate the set of grid cells involved based on the player's position as the center using the AOI radius.
- Calculate the distance between each entity in the grid cell set and the player.
- The set of entities with a distance less than the AOI radius is the player's new AOI.

The Nine-Grid Algorithm is easy to implement. It can be described in a few sentences. We will discuss the performance analysis later. Let's take a look at the Cross-Linked List Algorithm first.

### Cross-linked list

For 3D games, we usually create ordered linked lists for the X and Z axes coordinates respectively. Each entity has a node on the list, storing its coordinate value. The values are stored in ascending order. However, if we only store the coordinates of the entities themselves, the efficiency of querying with these two linked lists is still very low.

The real key is that we will add left and right sentinel nodes to each player with AOI on the linked list. The coordinates of the two sentinels are exactly the AOI radius away from the player's own coordinates. For example, if the player `P` has coordinates `(a, b, c)` and the AOI radius is `r`, then there will be two sentinels `left_x` and `right_x` on the X-axis, with coordinates `a - r` and `a + r` respectively. With the existence of sentinels, we update AOI by tracking the movement of the sentinels and other entity nodes. Continuing with the previous example, if an entity `E` moves and crosses from the right side of `left_x` to the left side of `left_x` on the X-axis, it means that `E` has definitely left the AOI of `P`. Similarly, if it crosses to the right of `right_x`, it has also left AOI. On the contrary, if it crosses to the right of `left_x`, or to the left of `right_x`, it means that it may enter the AOI of `P`.

可以看到，十字链表算法要比九宫格复杂得多，我们需要维护两条有序的链表，并且在每个实体坐标更新的时候，同步移动链表上的节点，并且在移动跨过其他节点时更新 AOI。

As we can see, the Cross-linked List algorithm is much more complex than the Nine-palace Grid. We need to maintain two sorted lists and synchronize moving the nodes on the lists whenever the entity coordinates are updated. Additionally, we need to update AOI when crossing over other nodes while moving.

### Implementation of 9-grid layout

Because it involves the actual performance measurement, let's first delve a little deeper into the implementation details of the Nine-Cell Algorithm:

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

`PlayerAoi` stores player data. Within it, there is an array called `sensors`, which is used to calculate entities within a certain range. After each `Tick`, the calculated entities are added to the `aoi_players`. `aoi_players` stores two arrays, which are used to compare the results from the previous `Tick` and determine which players have entered or left. The general flow of a `Tick` is as follows:

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

`Tick` does a simple task, it iterates through players with `sensors`, calculates entities within the range of each `sensor`, and defines it as AOI (Area of Interest). `last_pos` is used to determine whether an entity has entered or left the AOI. The code for `_UpdatePlayerAoi` is as follows:

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

`old_aoi` is the AOI calculated from the previous `Tick`, and `new_aoi` is the AOI to be calculated in the current `Tick`. `new_aoi` is obtained by traversing all the entities within the AOI range and selecting those whose distance from the player is less than the AOI radius. After that, the functions `_CheckLeave` and `_CheckEnter` are used to calculate the entities that leave and enter the AOI in the current `Tick`. For example, if the entity's `last_pos` in `new_aoi` is not within the AOI range, it means that the entity has entered the AOI range in the current `Tick`. For specific code, please refer to the source file, which will not be reiterated here.

### Implementation of Cross Linked List

Compared to the 9-grid, the implementation of the cross-linked list is more complex. First, let's look at the basic data structure:

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

`Sensor` and `PlayerAoi` are partially similar to the Nine Grid, but they have an additional linked list related node structure called `CoordNode`. `CoordNode` represents a node on the linked list, which records the type and value of the node itself. There are three types: player node, left node of `Sensor`, and right node of `Sensor`.

Most of the work of a cross-linked list is to maintain the order of the list.

* When a player joins, they need to move their player node to the correct position in order, and at the same time, handle the entering or leaving of other player AOI events.
* After the player moves to the correct position, the `Sensor` left and right nodes start from the player's front and back positions, move to the correct position, and handle the entering and leaving events triggered when crossing other player nodes.
* When a player moves, update their coordinates, move the player node and the `Sensor` left and right nodes, and handle AOI entering and leaving.

The code for moving nodes is as follows. Every time a node is crossed, the `MoveCross` function is called to determine whether to enter or leave the AOI based on the direction of movement, the node being moved, and the type of the crossed node.

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

Moving the linked list is very slow, with a complexity of `O(n)`, especially when a new player joins the scene. The player needs to move from a faraway place to the correct position step by step, which requires traversing a large number of nodes and consumes a lot of resources. In order to optimize performance, we can place lighthouses in fixed positions in the scene. These lighthouses handle things in a similar way to the players, except they also keep a record of "detected_by" data, which indicates which "Sensors" the sentinel entity is within range of. When a player enters the scene for the first time, they no longer start moving from the farthest point. Instead, they find the nearest lighthouse, insert themselves next to it, and quickly enter the AOI (Area of Interest) range of other players that is consistent with the lighthouse, by making use of the "detected_by" data on the lighthouse. Then they start moving to the correct position. Of course, entering and leaving must also be handled during the movement. Similarly, for the "Sensor", we can inherit data from the lighthouse and then move to the correct position from the lighthouse's location. These two optimizations can significantly improve the performance of inserting players by more than double.

`Sensor` also has a `HashMap` called `aoi_player_candidates` (here, for performance reasons, we use [khash](https://github.com/attractivechaos/klib/blob/master/khash.h)). The AOI event triggered by node movement, in fact, can only detect a square region with a side length of `2r` on the X-Z coordinate axis, which is not strictly a circular AOI region. All entities within this square region are recorded in `aoi_player_candidates` and the AOI range within the circular region is calculated during the `Tick` by traversing the `candidates`, so it is called `candidates`.

All operations of the cross-linked list are designed to continuously maintain the entities `candidates` within a square region. The operations performed by the `Tick` in the cross-linked list are almost identical to the calculations in the 9-grid, except that the `candidates` traversed and calculated for AOI are different. The `candidates` in the 9-grid are entities covered by the circular AOI region, while the cross-linked list consists of entities within a square region defined by the left and right nodes of the `Sensor`, with a side length of `2r`. In qualitative terms, the `candidates` in the cross-linked list are generally fewer than those in the 9-grid, resulting in fewer iterations in the `Tick` and improved performance. However, the cross-linked list also incurs additional performance overhead in maintaining the list. The overall performance of these two approaches remains to be evaluated in our upcoming tests.

### Performance Testing

I have separately measured the time consumption for three scenarios: player joining the scene (`Add Player`), AOI event calculation (`Tick`), and player position update (`Update Pos`).

The initial position of the player is randomly generated within the range of the map, and then the player is added to the scene. `player_num` represents the number of players, while `map_size` represents the range of the X-Z coordinate axis of the map. The positions of the players are randomly generated uniformly within this range. Each player has a `Sensor` with a radius of `100` as AOI. The computation time is measured using `boost::timer::cpu_timer`. Three cases were considered for `player_num`: `100, 1000, 10000`, and four cases were considered for `map_size`: `[-50, 50], [-100, 100], [-1000, 1000], [-10000, 10000]`.

Updating player position will cause the player to move in a fixed random direction at a speed of `6m/s`.

The testing environment for this session is:

* CPU: Intel(R) Core(TM) i5-4590 CPU @ 3.30GHz
- System: Debian GNU/Linux 10 (buster)
- GCC version: gcc version 8.3.0 (Debian 8.3.0-6)
- Boost version: boost_1_75_0

#### Nine-square grid test

The test results of the Tic-tac-toe grid are as follows:

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

When there are `100` players in the grid, the three operations have very small time consumption. In the extreme case where `map_size = [-50, 50]` and all players are within the AOI range, the `Tick` operation takes approximately `0.4ms`. The performance of joining the scene and updating coordinates, which both have a linear complexity of `O(player_num)`, is good. When the number of players reaches 10,000 (`player_num = 10000`) with a map size of `[-50, 50]`, the `Add Player` and `Update Pos` operations can be completed in a few milliseconds due to their linear nature. However, the `Tick` operation takes about `3.8s` and consumes a large amount of CPU, rendering it unusable. In the case of 10,000 players and a map size of `[-1000, 1000]`, the `Tick` time consumption is approximately `94ms`. If the `Tick` frequency can be reduced, for example, twice per second, it can still be considered usable, although barely within acceptable limits.

#### Cross-linked list test

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

If we analyze it, the cross-linked list takes longer on `Add Player` and `Update Pos`, especially on `Add Player`. Compared to the grid, its performance is hundreds or even thousands of times worse (`100, [-50, 50]` takes `2ms` for the cross-linked list, while the grid only takes `0.08ms`; `10000, [-50, 50]` takes `21.6s` for the cross-linked list, and the grid only takes `6ms`). The time difference on `Update Pos` can also be up to hundreds of times, `10000, [-100, 100]` takes `1.5s` for the cross-linked list to update player positions, while the grid only takes `18ms`. It can be seen that the cross-linked list has a wider range of time consumption limits for `Add Player` and `Update Pos` compared to the grid. It is more affected by the number of players and the size of the map. In densely populated player areas, the performance of these two operations will rapidly decline until they become unusable.

The overall performance of the "Tick" operation in the Cross-Chain is indeed better than the Nine-Grid. In the best case scenario, it takes about half the time of the Nine-Grid (0.8ms for the Cross-Chain with parameters `1000, [-1000, 1000]`, compared to 1.8ms for the Nine-Grid). However, in the worst case scenario, the performance of the Cross-Chain is similar to that of the Nine-Grid (3.7s for the Cross-Chain with parameters `10000, [-10000, 10000]`, compared to 3.8s for the Nine-Grid). This is because the scene is small and players are all within each other's AOI range, so the number of candidates traversed in the Cross-Chain "Tick" operation is actually very close to that of the Nine-Grid.

The cross-chain requires stronger assumptions than the nine-grid to achieve better performance. For example, when `player_num = 1000` and `map_size = [-1000, 1000]`, the cross-chain takes `0.8ms` for `Tick` and `1.8ms` for the nine-grid. For `Update Pos`, the cross-chain takes `0.3ms` and the nine-grid takes `0.18ms` (note that the `Update Pos` time is the sum of 10 executions). In terms of the total time of `Tick + Update Pos`, in order for the cross-chain to be faster than the nine-grid, the number of `Update Pos` iterations should not exceed `8` times that of `Tick`, or in other words, the number of `Update Pos` iterations between two `Tick` should be less than `8` times. 

Additionally, due to the significant time-consuming operation of adding a player to the cross-chain, it is not suitable for scenarios where players frequently enter and exit the scene or perform large-scale teleportation within the scene. Moreover, if a large number of players enter the scene within a short period of time, it can easily lead to performance degradation and a high CPU usage.

As for the cross-linked list, there is an optimization that can be done under one premise: eliminate `Tick`. The premise is that the game can accept a square-shaped AOI and other consumptions such as network caused by the square-shaped AOI are acceptable when measured. Actually, the premise is quite harsh because in games, the CPU usage of AOI calculation is usually relatively low. However, changing the circular AOI to a square-shaped AOI results in an increase in the area of the AOI range and the number of players within the range. Under a uniform distribution, the number of players may increase by up to 1.27 times the original amount. However, once the premise is satisfied, the cross-linked list can achieve AOI updates without the need for a `Tick`, since the `candidates` maintained by the cross-linked list implementation already represents the AOI within the square, which was originally calculated in `Tick` by iterating and calculating distances. In this case, the cross-linked list has the potential to achieve excellent performance, as the performance of the `Update Pos` operation in the cross-linked list can be several times to tens of times faster than a `Tick`.

Finally, a bar chart comparing the two is provided:

![to_be_replace1](to_be_replace1)

![](assets/img/2021-11-18-aoi-tesing/add_player.png)

![](assets/img/2021-11-18-aoi-tesing/tick.png)

![](assets/img/2021-11-18-aoi-tesing/update_pos.png)


### Summary

In this article, we introduce the principles and basic implementation of two AOI algorithms (grid-based and cross-chain), and analyze the performance of these two algorithms based on actual test data, hoping to provide readers with some assistance or inspiration.

Generally speaking, the Nine-grid method is easy to implement and has balanced performance. It is very suitable for games that do not have performance bottlenecks. The performance fluctuation range of the Nine-grid method is within the expected range, and its performance lower limit is relatively high, so it is not easily bottlenecked. However, on the other hand, there is not much room for optimization, and the time complexity is relatively fixed. On the contrary, the Cross-chain method is more complex to implement, and its performance lower limit is lower than that of the Nine-grid method. But if it can meet certain assumptions and prerequisites, the Cross-chain method can have a higher optimization space, or in other words, a higher upper limit. These two methods have their own advantages and disadvantages, and different game engines in the industry have chosen one of them, based on their own needs and perspectives.

My abilities are limited, and the content of this text only represents my own thoughts. If there are any deficiencies or inappropriate aspects, please feel free to leave a comment for discussion.

> Original: <https://disenone.github.io/wiki>  
> This post is protected by [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by/4.0/deed.en) agreement, should be reproduced with attribution.


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
