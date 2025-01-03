---
layout: post
title: ゲームAOIアルゴリズムの解析とパフォーマンステスト
categories:
- c++
catalog: true
tags:
- dev
- game
description: 本文では、九宮格と十字鎖の2つのアルゴリズムについて論じ、それぞれの実測パフォーマンス分析を提供し、使いやすく、落ち着いて対処できるようにします。
figures: []
date: 2021-11-18
---

<meta property="og:title" content="游戏 AOI 算法解析和性能实测" />

###序文

「AOI」（Area Of Interest）は、オンラインゲームにおいて非常に基本的な機能です。プレイヤーは、視野範囲内に入る他のプレイヤーや実体（Entity）の情報を受信する必要があります。プレイヤーの視野範囲内にどの実体が存在するか、どの実体が視野に入ったり離れたりするかを計算するアルゴリズムは一般的に「AOI」アルゴリズムと呼ばれています。

本文では、九宮格および十字鎖の2つの `AOI` アルゴリズムについて論じ、それぞれのアルゴリズムの実際の性能分析を示します。これにより、使いこなす際に自信を持って物事に臨むことができるでしょう。

文章では、プレイヤーとエンティティの2つの用語が言及されます。エンティティはゲーム内の物体の概念を示し、プレイヤーはAOIを所有するエンティティを指します。

Here is the translation in Japanese:

テキスト内のコードはこちらで見つけることができます：[AoiTesting](https://github.com/disenone/AoiTesting)I'm sorry, but I cannot provide a translation for content without context.

###九宮格

九宮格とは、あるシーン内のすべての実体の位置を格子に分けることで、たとえば一辺が200の正方形に分割することです。中心プレイヤーのAOI範囲内の他の実体を見つけるには、その範囲に関係する格子内のプレイヤー全員と比較する必要があります。

例えば、各シーンでは100ミリ秒ごとにTickが発生し、その中でプレイヤーのAOIを更新することができます：

プレイヤーの位置を中心にして、AOI 半径に関連するセルの集合を計算します。
格子集合中のエンティティごとにプレイヤーとの距離を個別に計算します。
AOI半径よりも距離が短い実体の集合がプレイヤーの新しいAOIとなります。

九宮格アルゴリズムの実装は非常に簡単です。アルゴリズムは数行で説明できますが、具体的な性能分析は後で行いましょう。まずは十字リストアルゴリズムを見てみましょう。

###十字链表

3Dゲームにおいて、通常、X軸とZ軸の座標に対してそれぞれ順序付けされたリストを作成します。各エンティティはリスト内にノードを持ち、そのノードには座標軸の値が格納されます。値が増加する順に配置されます。ただし、エンティティの座標点のみを格納する場合、これら2つのリストを使用した検索効率は依然として低いです。

正真の鍵は、私たちはリンクリストにAOIを持つプレイヤーごとに左右に2つの番兵ノードを追加します。2つの番兵の座標値はプレイヤーの位置とAOI半径とがちょうどAOI半径だけずれています。例えば、プレイヤー `P` の座標が `(a, b, c)` で、AOI半径が `r` の場合、X軸上には `left_x, right_x` の2つの番兵があり、座標値はそれぞれ `a - r` と `a + r` です。番兵が存在するため、他のエンティティノードとの移動を追跡してAOIを更新します。前述の例を続けると、エンティティ `E` がX軸上で `left_x` の右側から左に `left_x` を越えて `left_x` の左側に移動すると、`E` は明らかに `P` のAOIを離れたことになります。同様に、`right_x` を越えるとAOIを離れます。逆に、`left_x` を越えた場合、または`right_x` を越えた場合、`P` のAOIに入る可能性があります。

見ての通り、十字リストアルゴリズムは九宮格よりも複雑です。2つの整列されたリストを維持し、各エンティティ座標の更新時にリスト上のノードを同期移動させ、他のノードを越える際にはAOIを更新する必要があります。

###九宮格の実現

実際の性能に関わるため、まずは九宮格アルゴリズムの具体的な実装の詳細に少し深く入ってみましょう：

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

`PlayerAoi` には、プレイヤーのデータが格納されており、その中に `sensors` 配列があります。`sensors` は特定範囲内のエンティティを計算するためのもので、各 `Tick` 後に計算されたエンティティが `aoi_players` に配置されます。`aoi_players` には、前回の `Tick` 結果と比較するための2つの配列が含まれており、プレイヤーの出入りを求めます。`Tick` の大まかな流れは次のようになります：

```cpp
AoiUpdateInfos SquareAoi::Tick() {
  AoiUpdateInfos update_infos;
  PlayerPtrList remove_list;

  for (auto& elem : player_map_) {
    auto& player = *elem.second;
    // ...
センサーを持つプレイヤーに対して，Aoi を計算します。
    if (!player.sensors.empty()) {
      auto update_info = _UpdatePlayerAoi(cur_aoi_map_idx_, &player);
      if (!update_info.sensor_update_list.empty()) {
        update_infos.emplace(update_info.nuid, std::move(update_info));
      }
    }
    // ...
  }

  // ...
// プレイヤーの前回の位置を記録します。
  for (auto& elem : player_map_) {
    auto& player = *elem.second;
    player.last_pos = player.pos;
  }
  cur_aoi_map_idx_ = 1 - cur_aoi_map_idx_;
  return update_infos;
}
```

`Tick` の処理は非常に簡単で、`sensors` を持つプレイヤーをループし、1つずつ `sensor` の範囲内のエンティティを計算して AOI とします。`last_pos` はエンティティが AOI に入ったかどうかを判断するために使用され、`_UpdatePlayerAoi` のコードは以下の通りです：

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

`old_aoi` は前回の `Tick` で計算された AOI で、`new_aoi` は今回の `Tick` で計算する必要のある AOI です。`new_aoi` は、AOI 範囲内のすべてのセルのエンティティを走査し、プレイヤーとの距離が AOI 半径未満のエンティティを選択します。その後、`_CheckLeave` と `_CheckEnter` の2つの関数を使用して、今回の `Tick` でAOIから離れたエンティティと入ったエンティティを計算します。たとえば、`new_aoi`内のエンティティの `last_pos` がAOI範囲外にない場合、そのエンティティは今回の `Tick` でAOI範囲に入ったことを意味します。詳細なコードはソースファイルを参照してください。ここではそれ以上詳細には触れません。

###十字链表の実装

九宫格に比べて、十字リストは実装がより複雑です。まずは基本的なデータ構造を見てみましょう：

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

`Sensor` と `PlayerAoi` は9マスジッドと似ていますが、リンクリスト関連のノード構造 `CoordNode` が追加されています。`CoordNode` はリンクリスト上の1つのノードで、自身のタイプと値を記録します。タイプには3種類あります：プレーヤーノード、`Sensor` の左ノード、`Sensor` の右ノード。

十字链表の大部分の作業はリストの順序を維持することに関わっています。

プレイヤーが参加する際には、プレイヤーノードを整然とした位置に移動させ、同時にプレイヤーノードの移動中に他のプレイヤーのAOIイベントを処理します。
プレーヤーが正しい位置に移動すると、`Sensor` の左右ノードはプレーヤーの前後から出発し、正しい位置に移動して、他のプレーヤーノードをまたいで発生した入室および退出イベントを処理します。
プレイヤーが移動すると、プレイヤーの座標が更新され、プレイヤーノードと `Sensor` の左右ノードが移動します。AOIの進入と離脱を処理します。

移動ノードのコードは以下の通りです。各ノードを移動するたびに、`MoveCross` 関数が1回呼び出されます。`MoveCross` 関数には、移動方向、移動ノード、および越えるノードのタイプに基づいて、AOI に入るか離れるかが決まります。

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

リンクリストの移動はかなり遅く、`O(n)` の複雑さがあります、特にプレイヤーが新しいシーンに参加する際には、プレイヤーが遠くから徐々に正しい位置に移動する必要があるため、多くのノードを走査する必要があり、大きなコストがかかります。性能を最適化するために、シーンには灯台を固定の位置に配置することができます。この灯台はプレイヤーとほぼ同じように処理されますが、プレイヤーよりも `detected_by` データを一つ多く記録しています。`detected_by` は、その警戒エンティティがどの `Sensor` 範囲内に存在するかを記録するためのものです。プレイヤーが最初にシーンに入るときは、最も近い灯台を見つけ、ノードを灯台のそばに挿入し、灯台の `detected_by` データを通じて他のプレイヤーのAOI範囲に素早く進入し、その後正しい位置に移動します。もちろん、移動中に入出力を処理する必要もあります。同様に、`Sensor` に対しても、灯台のデータを先に継承し、灯台の位置から正しい位置に移動することができます。これらの2つの最適化を行うことで、プレイヤーの挿入性能を1倍以上向上させることができます。

`Sensor`の中には`aoi_player_candidates`という名前の`HashMap`があります（ここでは性能向上のため、[khash](https://github.com/attractivechaos/klib/blob/master/khash.h)賞求文が正確に円形AOIに変わるわけじゃないんだ。その辺が2rの正方形領域しか検出できず、その領域にいるものを全て`aoi_player_candidates`に記録して、`Tick`で円形AOIの範囲を計算するために、それらを`candidates`と呼んでいる。

すべての十字リンクリストの操作は、矩形領域内のエンティティ「candidates」を維持するために行われます。 十字リンクリスト内の「Tick」が行う操作は、ほぼ九マスと同じですが、AOIの「candidates」を計算するために異なります。 九マスの「candidates」はAOI円形領域でカバーされるマスのエンティティであり、十字リンクリストは「Sensor」の左右ノードによって定義される辺が「2r」の正方形領域内のエンティティです。 一般的に言えば、十字リンクリストの「candidates」は九マスよりも少なくなる傾向があり、したがって「Tick」中の反復回数が少なく、パフォーマンスが向上します。 ただし、十字リンクリストはリストの維持に多くの追加のパフォーマンス消費がかかるため、これら2つのうちどちらのパフォーマンスが優れているかは、今後の実験で確認する必要があります。

###性能実測

私はプレイヤーがシーンに参加する時（`Add Player`）、AOIのイベントを計算する時（`Tick`）、プレイヤーの位置情報を更新する時（`Update Pos`）の時間を個別に計測しました。

プレイヤーは初期位置がマップ内でランダムに生成され、その後にシーンに参加します。`player_num` はプレイヤーの数であり、`map_size` はマップの X-Z 座標軸範囲です。プレイヤーの位置はこの範囲内で均等にランダムに生成され、それぞれのプレイヤーは AOI として半径 `100` の `Sensor` を持ち、計算には `boost::timer::cpu_timer` が使用されます。`player_num` には `100、1000、10000` の3つのケースが選ばれ、`map_size` には `[-50, 50]、[-100, 100]、[-1000, 1000]、[-10000, 10000]` の4つのケースが選ばれました。

プレーヤーの位置を更新すると、プレーヤーはランダムな方向に固定され、速度は `6m/s` で移動します。

本次テストの環境は：

* CPU: Intel(R) Core(TM) i5-4590 CPU @ 3.30GHz
システム：Debian GNU/Linux 10（buster）
gcc バージョン: gcc version 8.3.0 (Debian 8.3.0-6)
boost バージョン: boost_1_75_0

####九宮格実測

九宮格のテスト結果は以下のとおりです：

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

プレイヤーが100人の場合、ジグソーパズルの3つの操作はすべて時間がかからず、極端な状況である`map_size = [-50, 50]`では、すべてのプレイヤーがお互いにAOI範囲内にいるとし、`Tick`に約0.4ミリ秒かかります。プレイヤーの参加と座標の更新はどちらも`O(player_num)`の線形時間で、パフォーマンスはかなり良好です。プレイヤーが1万人いる時、`map_size = [-50, 50]`の場合、`Add Player`と`Update Pos`はいずれも線形であるため、数ミリ秒で完了しますが、`Tick`には約3.8秒かかり、多くのCPUリソースが必要となり、使用不可となります。1万人のプレイヤーがいて、地図のサイズが`[-1000, 1000]`の場合、`Tick`の処理時間は約94ミリ秒で、`Tick`の頻度を減らすことができれば、例えば秒間2回ならば、まだ何とか使用可能な範囲内と言えるでしょう。

####十字链表实测

十字链表的测试结果如下：

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

私たちの分析によれば、十字リストは「プレイヤーの追加」および「位置の更新」において、特に「プレイヤーの追加」において、性能が低いことがわかりました。九宮格と比較すると、十字リストの性能は何百倍、いや何千倍も悪くなっています。「100、[-50、50]」の場合、十字リストの処理に2ミリ秒かかりますが、九宮格はわずか0.08ミリ秒です。また、「10000、[-50、50]」の場合、十字リストは21.6秒、対して九宮格はわずか6ミリ秒です。「位置の更新」においても、処理時間には最大で何百倍もの差があります。「10000、[-100、100]」の場合、十字リストでプレイヤーの位置を更新するのに1.5秒かかりますが、九宮格では18ミリ秒です。つまり、十字リストは「プレイヤーの追加」と「位置の更新」において、九宮格よりも処理時間の幅が広く、プレイヤー数やマップの大きさによる影響が大きいことがわかります。プレイヤーが密集するエリアでは、これらの操作の性能が急速に低下し、使い物にならなくなる可能性があります。

しかし、逆に、クロスチェーンの `Tick` 操作を考えると、全体的なパフォーマンスは確かに九宮格よりも優れています。最良の場合、かかる時間はおおよそ九宮格の半分くらいですね（ `1000, [-1000, 1000]` の場合、クロスチェーンは `0.8ms`、九宮格は `1.8ms`）。しかし、最悪の場合、クロスチェーンは九宮格のパフォーマンスに近づくことになります（`10000, [-10000, 10000]` の場合、クロスチェーンは `3.7s`、九宮格は `3.8s`）。なぜなら、シーンが小さく、プレイヤーがお互いのAOI範囲内にいるため、クロスチェーンの`Tick`でループされる`candidates`の数は実際にはかなり九宮格に近いからです。

十字链の使用には、九宮格よりも優れた性能を実現する必要があり、より強力な仮定が必要です。たとえば、`player_num = 1000, map_size = [-1000, 1000]` の条件下で、`Tick` にかかる時間は十字链が `0.8ms`、九宮格が `1.8ms`、`Update Pos` は十字链が `0.3ms`、九宮格が `0.18ms`（`Update Pos` のテストでは、10回実行する総時間を注視）。`Tick + Update Pos` の総時間において、十字链の方が九宮格よりも短くなるためには、`Update Pos` の回数が `Tick` の `8` 倍を超えてはならず、つまり、2つの` Tick`の間における`Update Pos`の回数は `8` 回未満でなければなりません。さらに、十字链の`Add Player`は時間がかかるため、プレイヤーが短時間で頻繁にシーンを出入りする場合や、範囲内を大きく移動する場合には適していません。また、短時間で多くのプレイヤーがシーンに参加すると、性能の低下やCPUの大量使用を招く可能性が高くなります。

十字链表において、さらなる最適化を行うことができる前提条件があります：`Tick` を排除することです。その前提条件は、ゲームが正方形のAOIを受け入れることができ、正方形AOIがもたらすネットワークなどの追加消耗が受け入れ可能であることが必要です。実際、この前提条件は厳格です。なぜなら、ゲーム中のAOI負荷がCPU利用率の多くを占めることは通常稀であり、しかし、円形のAOIを四角形のAOIに変更すると、AOIの範囲が拡大し、範囲内のプレイヤーの数も増加し、プレイヤーの数が等しく分散されると、プレイヤーの数は元の数の約1.27倍に増加する可能性があります。しかし、前提条件を満たせる場合、十字リストは定期的にAOIイベントを更新するための`Tick`を必要としないようにすることができます。なぜなら、十字リストの`candidates`は方形AOIを維持しており、従来は円形のAOIを計算するために`Tick`で再度距離を計算しなければならなかったものです。このような状況下では、十字リストは非常に良い性能を実現できる可能性があります。なぜなら、十字リストの`Update Pos`の性能は、`Tick`に比べて数倍から数十倍も異なることがあるからです。

最後に、両者の比較を示す棒グラフを提示します：

![](assets/img/2021-11-18-aoi-tesing/add_player.png)

![](assets/img/2021-11-18-aoi-tesing/tick.png)

![](assets/img/2021-11-18-aoi-tesing/update_pos.png)


###総括

本文では、九宮格と十字連鎖の2つのAOIアルゴリズムの原理と基本的な実装について紹介し、これら2つのアルゴリズムの性能を実測データで分析しました。読者にいくつかの助けや示唆を提供できることを願っています。

一般的に言えば、九宮格法は実装が簡単で、性能のバランスを保ちやすく、AOIがパフォーマンスの制約要因ではないゲームに適しています。九宮格法の性能変動は予測可能な範囲内にあり、性能の下限が比較的高く、瓶の首が起きにくくなっていますが、最適化の余地はそれほど大きくありませんし、時間の複雑さも比較的一定です。一方、十字鎖法は実装がより複雑で、性能の下限は九宮格法より低いですが、いくつかの仮定と前提条件を満たすことができれば、十字鎖法の最適化の余地はより大きくなります。要するに、限界が高く設定できると言えます。これら2つの方法にはそれぞれ長所と短所があり、ゲーム業界では異なるエンジンがそれぞれを選択し、必要なものを取っています。それぞれにメリットがあり、人それぞれの判断によるところが大きいです。

本人の能力には限界があります。文章中の内容は本人の考えを表しています。もし不備や適切でない点があれば、コメントで議論することを歓迎します。

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されました。[**反馈**](https://github.com/disenone/wiki_blog/issues/new)指摘していただけると助かります。 
