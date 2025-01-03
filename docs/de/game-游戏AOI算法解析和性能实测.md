---
layout: post
title: Analyse und Leistungsprüfung des AOI-Algorithmus im Spiel.
categories:
- c++
catalog: true
tags:
- dev
- game
description: Dieser Text diskutiert zwei Algorithmen, das Sudoku-Gitter und die Kreuzkette,
  und bietet eine Leistungsanalyse der beiden Algorithmen, damit Sie sie problemlos
  anwenden können, ohne in Panik zu geraten.
figures: []
date: 2021-11-18
---

<meta property="og:title" content="游戏 AOI 算法解析和性能实测" />

###Einleitung

`AOI` (Area Of Interest) ist eine grundlegende Funktion in Multiplayer-Online-Spielen, bei der Spieler Informationen über andere Spieler oder Entitäten (Entity), die in ihr Sichtfeld gelangen, erhalten müssen. Welche Entitäten sich im Sichtfeld des Spielers befinden, welche Entitäten sich im Sichtfeld bewegen oder verlassen, wird im Allgemeinen als `AOI`-Algorithmus bezeichnet.

Dieser Text diskutiert zwei Arten von `AOI`-Algorithmen, das Nine-Cell-Grid und das Cross-Chain, und liefert eine praktische Leistungsanalyse der beiden Algorithmen, damit Sie sie sicher und gelassen anwenden können.

Im Text wird von Spielern und Entitäten gesprochen. Entitäten sind Konzepte von Objekten im Spiel, während Spieler Entitäten mit einem AOI besitzen.

Der Code im Text ist hier zu finden: [AoiTesting](https://github.com/disenone/AoiTesting)I'm sorry, but there is nothing to translate in "".

###Sudoku

Die sogenannte Nine-Square-Grid teilt die Positionen aller Entitäten in einer Szene in Gitter auf, beispielsweise in Quadrate mit einer Kantenlänge von 200. Um andere Entitäten im AOI-Bereich des Zentralspielers zu finden, vergleicht man einfach alle Spieler in den Gittern, die sich innerhalb dieses Bereichs befinden.

For example, the scene will tick once every 100 milliseconds. During the tick, we can update the player's AOI like this:

Berechnung der Zellenmenge, die von dem AOI-Radius um die Spielerposition herum betroffen ist.
Berechne die Entfernung jedes Elements des Raster-Sets zum Spieler.
Die Entitätensammlung innerhalb eines Radius kleiner als AOI bildet das neue AOI des Spielers.

Die Umsetzung des Sudoku-Algorithmus ist recht einfach. Der Algorithmus lässt sich in wenigen Sätzen klar beschreiben. Eine detaillierte Leistungsanalyse wird später behandelt. Lassen Sie uns zuerst den Algorithmus für verkettete Listen betrachten.

###Crosslinked list

Für 3D-Spiele erstellen wir normalerweise geordnete Listen für die X- und Z-Achsen, wobei jeder Entität in der Liste ein Knoten zugeordnet ist, der den Achsenwert enthält, und die Liste nach aufsteigenden Werten sortiert ist. Allerdings bleibt die Effizienz der Abfrage für diese beiden Listen niedrig, wenn nur die Koordinatenpunkte der Entitäten gespeichert werden.

Das eigentliche Schlüsselelement hier ist, dass wir jedem Spieler, der einen AOI besitzt, in der verketteten Liste zwei Wächterknoten hinzufügen werden. Die Koordinaten der beiden Wächterknoten unterscheiden sich jeweils um den AOI-Radius von den Koordinaten des Spielers selbst. Angenommen ein Spieler `P` hat die Koordinaten `(a, b, c)` und der AOI-Radius beträgt `r`, dann gibt es auf der X-Achse zwei Wächter, `left_x` und `right_x`, mit den Koordinaten `a - r` und `a + r`. Dank der Wächter können wir durch die Verfolgung der Bewegungen der Wächter und anderer Entitätsknoten das AOI aktualisieren. In Bezug auf das frühere Beispiel: Wenn eine Entität `E` sich bewegt und einen Knoten auf der X-Achse von rechts nach links über `left_x` überschreitet, bewegt sie sich von der rechten Seite von `left_x` auf die linke, was bedeutet, dass `E` definitiv den AOI von `P` verlassen hat. Entsprechend verlässt sie den AOI, wenn sie `right_x` von rechts nach links überschreitet. Auf der anderen Seite, wenn `left_x` von rechts nach links überschritten wird, oder `right_x` von links nach rechts, könnte dies bedeuten, dass die Entität in den AOI von `P` eintritt.

Es ist ersichtlich, dass der Algorithmus für kreuzförmige Verknüpfungen viel komplexer ist als bei einem 3x3-Raster. Wir müssen zwei geordnete Listen pflegen und beim Aktualisieren jeder physischen Position die Knoten der Listen synchron verschieben. Beim Überqueren anderer Knoten müssen wir außerdem das sichtbare Gebiet (AOI) aktualisieren.

###Die Umsetzung des 9-Feld-Rasters.

Aufgrund der beteiligten Leistungsprüfung werden wir nun etwas tiefer in die Implementierungsdetails des 9-Punkte-Gitteralgorithmus eintauchen:

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

`PlayerAoi` stores player data, including an array called `sensors` used to calculate entities within a certain range. After each `Tick`, the calculated entities are planned to be placed in `aoi_players`. `aoi_players` contains two arrays, used to compare the results of the last `Tick` in order to determine players entering and leaving. The approximate workflow of a `Tick` is as follows:

```cpp
AoiUpdateInfos SquareAoi::Tick() {
  AoiUpdateInfos update_infos;
  PlayerPtrList remove_list;

  for (auto& elem : player_map_) {
    auto& player = *elem.second;
    // ...
// Berechnen Sie Aoi für Spieler mit Sensoren.
    if (!player.sensors.empty()) {
      auto update_info = _UpdatePlayerAoi(cur_aoi_map_idx_, &player);
      if (!update_info.sensor_update_list.empty()) {
        update_infos.emplace(update_info.nuid, std::move(update_info));
      }
    }
    // ...
  }

  // ...
// Aufzeichnen der vorherigen Position des Spielers
  for (auto& elem : player_map_) {
    auto& player = *elem.second;
    player.last_pos = player.pos;
  }
  cur_aoi_map_idx_ = 1 - cur_aoi_map_idx_;
  return update_infos;
}
```

Das von `Tick` ausgeführte Verhalten ist recht simpel. Es durchläuft die Spieler mit Sensoren, berechnet für jedes Sensorelement die im Bereich liegenden Entitäten - also den *Area of Interest* (AOI). `last_pos` wird verwendet, um zu prüfen, ob eine Entität den AOI betreten hat oder verlassen hat. Der Code für `_UpdatePlayerAoi` ist wie folgt:

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

`old_aoi` is the AOI calculated from the previous `Tick`, and `new_aoi` is the AOI to be calculated for this `Tick`. `new_aoi` selects entities within the AOI radius by iterating through all cells in the AOI range that are closer to the player. Subsequently, using the `_CheckLeave` and `_CheckEnter` functions, the entities leaving and entering the AOI for this `Tick` are calculated. For instance, if the entity `last_pos` in `new_aoi` is not within the AOI range, it indicates that the entity entered the AOI during this `Tick`. Please refer to the source file for specific code details as they will not be further elaborated here.

###Die Implementierung einer verketteten Liste.

Im Vergleich zum 9x9-Gitter ist die Implementierung einer Kreuzverkettung komplexer. Schauen wir uns zuerst die grundlegende Datenstruktur an:

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

`Sensor` und `PlayerAoi` sind teilweise ähnlich dem Rastersystem, aber zusätzlich mit der knotenbezogenen Struktur `CoordNode`. `CoordNode` ist ein Knoten in der Liste, der den Typ und den Wert des Knotens aufzeichnet. Die Typen sind: Spielerknoten, `Sensor`-linker Knoten, `Sensor`-rechter Knoten.

Die meiste Arbeit bei einer Kreuzliste besteht darin, die Liste geordnet zu halten:

Wenn ein Spieler beitritt, muss der Spieler-Knoten an eine geordnete Position verschoben werden. Gleichzeitig müssen beim Verschieben des Spieler-Knotens die Ereignisse für das Betreten oder Verlassen des AOI anderer Spieler verarbeitet werden.
Sobald sich der Spieler an die richtige Position bewegt hat, starten die `Sensor`-Knoten links und rechts von der Spielerposition und bewegen sich an den korrekten Ort, um die Eintritts- und Austrittsereignisse auszulösen, wenn sie über andere Spielerknoten hinweggehen.
Wenn der Spieler sich bewegt, werden die Koordinaten des Spielers aktualisiert, und der Knoten des Spielers sowie die linken und rechten Knoten des `Sensor` werden verschoben, um den Eintritt und Austritt aus dem AOI zu handhaben.

Der Code für die beweglichen Knoten lautet wie folgt: Jedes Mal, wenn ein Knoten überschritten wird, wird die Funktion `MoveCross` aufgerufen. Anhand der Bewegungsrichtung, des bewegten Knotens und des überschrittenen Knotens entscheidet die Funktion `MoveCross`, ob der Knoten den AOI betritt oder verlässt.

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

Das Verschieben der verketteten Liste ist sehr langsam und hat eine Komplexität von `O(n)`, besonders wenn neue Spieler der Szene hinzugefügt werden. Die Spieler müssen von sehr weit entfernten Orten allmählich an die richtige Position bewegt werden, was eine große Anzahl von durchzulaufenden Knoten erfordert und einen erheblichen Aufwand verursacht. Um die Leistung zu optimieren, können wir Leuchttürme an festen Positionen in der Szene platzieren. Diese Leuchttürme funktionieren ähnlich wie die Spieler, zeichnen jedoch zusätzlich Daten von `detected_by` auf, um festzuhalten, in welchen Sensoren sich die Wachposten befinden. Wenn ein Spieler die Szene zum ersten Mal betritt, muss er nicht mehr von den entferntesten Orten aus beginnen zu bewegen, sondern sucht nach dem nächstgelegenen Leuchtturm, fügt den Knoten neben dem Leuchtturm ein und betritt schnell den AOI-Bereich anderer Spieler, die von diesem Leuchtturm erfasst werden. Anschließend beginnt er sich an die richtige Position zu bewegen, wobei auch das Betreten und Verlassen berücksichtigt werden muss. Gleiches gilt für Sensoren, die auch durch Vererbung der Daten des Leuchtturms an die richtige Stelle bewegt werden können. Durch diese beiden Optimierungen kann die Leistung bei der Einfügung von Spielern um mehr als das Doppelte verbessert werden.

Es gibt auch eine `HashMap` namens `aoi_player_candidates` im `Sensor` (hier wurde [khash](https://github.com/attractivechaos/klib/blob/master/khash.h)Bei einem AOI-Ereignis, das durch das Bewegen von Knoten ausgelöst wird, kann tatsächlich nur ein quadratischer Bereich mit einer Kantenlänge von `2r` entlang der X-Z-Koordinatenachse erfasst werden, der nicht genau unserem kreisförmigen AOI entspricht. Die Entitäten innerhalb dieses quadratischen Bereichs sind in `aoi_player_candidates` aufgezeichnet und werden während des `Tick` durchsucht, um den AOI-Bereich innerhalb des kreisförmigen Bereichs zu berechnen, weshalb sie als `Kandidaten` bezeichnet werden.

Alle Operationen des Kreuzlisten sind darauf ausgerichtet, die Entitäten in dem quadratischen Bereich `candidates` ständig zu verwalten. Die Operationen, die von der `Tick` -Funktion in der Kreuzliste durchgeführt werden, ähneln denen des 3x3-Gitters fast, nur dass die zu berechnenden `candidates` des AOI unterschiedlich sind. Die `candidates` des 3x3-Gitters sind die Entitäten, die vom kreisförmigen AOI-Bereich abgedeckt werden, während die Kreuzliste die Entitäten im quadratischen Bereich mit einer Kantenlänge von `2r` definiert wird von den linken und rechten Knoten des `Sensors`. Qualitativ gesehen sind in der Regel weniger `candidates` in der Kreuzliste als im 3x3-Gitter vorhanden, sodass die Anzahl der Iterationen in `Tick` geringer ist und die Leistung besser ist. Allerdings hat die Kreuzliste immer noch erhebliche zusätzliche Leistungseinbußen durch die Verwaltung der Liste, daher müssen wir die Gesamtperformance der beiden noch genauer messen, um herauszufinden, welche besser ist.

###Leistungstest

Ich habe hier jeweils die Zeitdauer für den Spielerbeitritt zur Szene ("Add Player"), das Berechnen von AOI-Ein- und Austrittsereignissen ("Tick") und das Aktualisieren der Spielerposition ("Update Pos") gemessen.

Der Ausgangspunkt des Spielers wird zufällig innerhalb des Kartenumfangs generiert, und dann wird der Spieler der Szene hinzugefügt. `player_num` steht für die Anzahl der Spieler, `map_size` bezeichnet den Bereich der X-Z-Koordinatenachse der Karte, wobei die Spielerpositionen in diesem Bereich gleichmäßig zufällig generiert werden. Jeder Spieler hat einen `Sensor` mit einem Radius von `100` als AOI, und die Berechnungszeit erfolgt mit dem `boost::timer::cpu_timer`. Es wurden drei verschiedene Fälle für `player_num` ausgewählt: `100, 1000, 10000`, und vier verschiedene Fälle für `map_size`: `[-50, 50], [-100, 100], [-1000, 1000], [-10000, 10000]`.

Aktualisieren der Spielerposition führt dazu, dass der Spieler sich mit einer konstant zufälligen Richtung mit einer Geschwindigkeit von `6m/s` bewegt.

Die Testumgebung in diesem Fall ist:

* CPU: Intel(R) Core(TM) i5-4590 CPU @ 3.30GHz
Betriebssystem: Debian GNU/Linux 10 (Buster)
* gcc Version: gcc Version 8.3.0 (Debian 8.3.0-6)
boost 版本: boost_1_75_0

####Neunfeldertest

Die Testergebnisse des Gitters sind wie folgt:

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

Bei 100 Spielern im Gitter sind die drei Operationen sehr schnell, selbst unter extremen Bedingungen mit einer Kartengröße von [-50, 50], wo alle Spieler sich im AOI-Bereich befinden und ein Tick etwa 0,4 ms benötigt. Das Hinzufügen von Spielern und das Aktualisieren von Koordinaten haben beide eine lineare Komplexität von O(Spielerzahl) und die Leistung ist gut. Wenn die Spielerzahl jedoch 10.000 erreicht und die Karte auf [-50, 50] verbleibt, beanspruchen sowohl das Hinzufügen von Spielern als auch das Aktualisieren von Positionen nur wenige Millisekunden, aber der Tick benötigt etwa 3,8 s, was viel CPU-Leistung erfordert und daher als nicht verwendbar gilt. Bei 10.000 Spielern und einer Karten größe von [-1000, 1000] beträgt der Zeitaufwand für den Tick ungefähr 94 ms. Wenn die Tick-Frequenz verringert werden kann, z. B. auf zweimal pro Sekunde, liegt dies immer noch knapp innerhalb des akzeptablen Bereichs.

####Kreuzverkettete Liste getestet

Die Testergebnisse der Cross Linked List sind wie folgt:

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

Wenn wir es durchgehen, dauern die Operationen "Spieler hinzufügen" und "Position aktualisieren" im Gitter mit Kreuzverweisen länger, besonders "Spieler hinzufügen". Im Vergleich zur performance von Sudoku-Gittern ist die Leistung um Hunderte oder sogar Tausende von Malen schlechter. Bei "100, [-50, 50]" dauert das Kreuzgitter 2ms, während das Sudoku-Gitter nur 0,08ms benötigt; bei "10000, [-50, 50]" dauert das Kreuzgitter 21,6s, das Sudoku-Gitter benötigt nur 6ms. Die Leistung der Operation "Position aktualisieren" kann ebenfalls um das Hundertfache variieren; bei "10000, [-100, 100]" dauert die Aktualisierung der Spielerposition im Kreuzgitter 1,5s, im Sudoku-Gitter hingegen nur 18ms. Es ist offensichtlich, dass die obere und untere Grenze der Leistung des Kreuzgitters bei "Spieler hinzufügen" und "Position aktualisieren" größer ist als die des Sudoku-Gitters. Es wird stärker vom Spielern und Kartenmaßstab beeinflusst. In Bereichen mit hoher Spielerdichte sinkt die Performance dieser beiden Operationen dramatisch und wird letztendlich unbrauchbar.

Bei der Betrachtung der "Tick" -Operation des Cross-Grids ist die Gesamtleistung tatsächlich besser als bei den Nine-Grits. Im besten Fall beträgt die Dauer ungefähr nur die Hälfte der Nine-Grits (bei "1000, [-1000, 1000]" dauert das Cross-Grid 0,8 ms, während das Nine-Grit 1,8 ms dauert), aber im schlimmsten Fall wird das Cross-Grid auf eine Leistung reduziert, die der des Nine-Grits nahe kommt ("10000, [-10000, 10000]" dauert das Cross-Grid 3,7 s, Nine-Grit 3,8 s). Dies liegt daran, dass aufgrund der geringen Szene die Spieler sich alle im AOI-Bereich des anderen befinden. Die Anzahl der "Kandidaten", die das Cross-Grid "Tick" durchläuft, ist tatsächlich schon sehr nahe an der des Nine-Grits.

Das Kreuzketten-System muss besser funktionieren als das 9x9-Gittersystem und erfordert daher einige stärkere Annahmen, wie z.B. `player_num = 1000, map_size = [-1000, 1000]`. Unter diesen Bedingungen beträgt die Zeit für einen `Tick` im Kreuzketten-System 0,8 ms und im 9x9-Gittersystem 1,8 ms, und die Zeit für `Update Pos` beträgt im Kreuzketten-System 0,3 ms und im 9x9-Gittersystem 0,18 ms (beachten Sie, dass die Testzeit für `Update Pos` die Summe der Zeiten für 10 Ausführungen ist). Bei der Gesamtzeit von `Tick + Update Pos` darf die Anzahl der `Update Pos`-Aufrufe im Kreuzketten-System nicht mehr als das 8-fache der Anzahl der `Tick`-Aufrufe betragen, oder anders gesagt, zwischen zwei `Ticks` dürfen die `Update Pos`-Aufrufe nicht mehr als 8-mal erfolgen. Darüber hinaus ist aufgrund des großen Zeitaufwands für das Hinzufügen von Spielern im Kreuzketten-System dieses nicht geeignet, wenn Spieler häufig kurz hintereinander in Szenen eintreten oder sich innerhalb der Szene weit bewegen. Außerdem kann eine große Anzahl von Spielern, die innerhalb kurzer Zeit in eine Szene gelangen, leicht zu Leistungseinbußen und einer hohen CPU-Auslastung führen.

In Bezug auf die Cross-Liste gibt es unter einer Bedingung eine Optimierungsmöglichkeit: das Entfernen des `Tick`. Voraussetzung ist, dass das Spiel ein Quadrat-basiertes AOI akzeptieren kann und die zusätzliche Belastung, die ein Quadrat-AOI verursacht (beispielsweise Netzwerk), akzeptabel ist. Tatsächlich ist die Voraussetzung ziemlich streng, da die CPU-Belastung für die AOI-Berechnung im Spiel normalerweise gering ist. Die Umstellung von einem kreisförmigen AOI auf ein quadratisches AOI führt jedoch zu einer größeren Fläche des AOI und zu einer größeren Anzahl von Spielern im Bereich. Unter der Annahme einer gleichmäßigen Verteilung kann die Spieleranzahl möglicherweise um das 1,27-fache gegenüber dem vorherigen Wert zunehmen. Sobald jedoch die Voraussetzung erfüllt ist, kann die Cross-Liste ohne die Notwendigkeit eines `Tick` zur regelmäßigen Aktualisierung von AOI-Ereignissen verwendet werden. Denn in der Implementierung pflegt die Cross-Liste bereits eine Liste von Spielern im Quadrat-AOI anstelle des ursprünglichen Zwecks der Berechnung eines kreisförmigen AOI, der zuvor im `Tick` durch Schleifen durchgeführt werden musste. In solchen Fällen ist es möglich, dass die Cross-Liste eine gute Leistung erbringen kann, da die Leistung die des `Tick` um ein Vielfaches bis hin zu mehreren Zehnerpotenzen übersteigen kann.

Schließlich wird ein Vergleichsdiagramm beider dargestellt:

![](assets/img/2021-11-18-aoi-tesing/add_player.png)

![](assets/img/2021-11-18-aoi-tesing/tick.png)

![](assets/img/2021-11-18-aoi-tesing/update_pos.png)


###Zusammenfassung

In this article, we introduce the principles and basic implementations of two AOI algorithms (nine-grid and cross-link), and analyze the performance advantages and disadvantages of these two algorithms through empirical data. We hope to provide readers with some assistance or inspiration.

Im Großen und Ganzen ist die 9x9-Gittermethode einfach umzusetzen, bietet eine ausgewogene Leistung und eignet sich gut für Spiele, bei denen AOI nicht die Leistungsgrenze darstellt. Der Leistungsbereich der 9x9-Gittermethode liegt innerhalb der erwarteten Reichweite, die untere Leistungsgrenze ist relativ hoch und führt nicht leicht zu Engpässen. Andererseits lässt sich der Raum auch nicht besonders optimieren und die Zeitkomplexität ist ziemlich stabil. Im Gegensatz dazu ist die Implementierung der Kreuzkettenmethode komplexer, die untere Leistungsgrenze ist niedriger als die der 9x9-Gittermethode. Wenn jedoch bestimmte Annahmen und Voraussetzungen erfüllt werden können, bietet die Kreuzkettenmethode eine höhere Raumoptimierung, was bedeutet, dass das obere Leistungsniveau höher sein kann. Beide Methoden haben ihre Vor- und Nachteile, und in der Spielebranche haben verschiedene Engines jeweils eine der beiden Methoden ausgewählt, je nach Bedarf und Einschätzung.

Meine Fähigkeiten sind begrenzt, der Inhalt des Textes repräsentiert nur meine Gedanken. Wenn etwas unzureichend oder unangemessen ist, freue ich mich über Kommentare und Diskussionen.

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt. Bitte [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Bitte geben Sie jede übersehene Stelle an. 
