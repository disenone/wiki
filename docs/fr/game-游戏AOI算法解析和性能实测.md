---
layout: post
title: Analyse algorithmique et tests de performance du jeu AOI
categories:
- c++
catalog: true
tags:
- dev
- game
description: Ce texte discute de deux algorithmes, le carré magique et la chaîne de
  croix, et fournit une analyse des performances pratiques des deux algorithmes pour
  que vous puissiez les utiliser en toute connaissance de cause et ne pas paniquer
  en cas de problème.
figures: []
date: 2021-11-18
---

<meta property="og:title" content="游戏 AOI 算法解析和性能实测" />

###Prélude

`AOI` (Area Of Interest) is a fundamental feature in multiplayer online games where players need to receive information about other players or entities entering their field of vision. Calculating which entities are within a player's field of view and the algorithms determining which entities enter or leave the field of view are generally referred to as the `AOI` algorithms.

Ce texte discute deux algorithmes AOI, le carré magique et la chaîne en croix, et fournit une analyse de performance expérimentale des deux algorithmes pour que vous puissiez les utiliser en toute confiance et rester calme en cas de problème.

Le texte mentionnera les termes "joueur" et "entité". Une entité est le concept d'un objet dans le jeu, tandis qu'un joueur est une entité possédant une AOI.

Le code mentionné dans le texte peut être trouvé ici : [AoiTesting](https://github.com/disenone/AoiTesting)I am sorry, but there is nothing to translate in the text you provided. 

###Neuf carrés.

Le "grid" de neuf cases consiste à diviser les positions de toutes les entités dans une scène en cases. Par exemple, si on divise en carrés de 200 de côté, pour trouver les autres entités à l'intérieur de la zone d'intérêt (AOI) du joueur central, il suffit de comparer tous les joueurs présents dans les cases concernées par cette zone.

Par exemple, à chaque intervalle de 100 millisecondes, il y aura un "tick". Pendant ce "tick", nous pouvons mettre à jour la zone d'intérêt du joueur de la manière suivante :

Calcul de l'ensemble des cases en relation avec le rayon AOI centré sur la position du joueur.
Calculer la distance entre chaque entité du groupe de cellules et le joueur.
L'ensemble des entités dont la distance est inférieure au rayon de l'AOI est le nouvel AOI du joueur.

L'algorithme de la grille 9x9 est assez simple à mettre en œuvre, il peut être décrit en quelques phrases, nous laisserons l'analyse de ses performances pour plus tard, commençons d'abord par examiner l'algorithme de la liste croisée.

###Liste chaînée croisée

Pour les jeux en 3D, nous avons l'habitude de construire des listes chaînées ordonnées pour les coordonnées des axes X et Z. Chaque entité a un nœud dans la liste contenant la valeur de l'axe correspondant, classé par ordre croissant. Cependant, si nous stockons uniquement les coordonnées des entités, l'efficacité de recherche de ces deux listes reste très faible.

Ce qui est vraiment crucial, c'est que nous ajoutons à chaque joueur possédant un AOI deux nœuds sentinelles à gauche et à droite de la liste chaînée. Les coordonnées des deux sentinelles diffèrent exactement du rayon AOI par rapport aux coordonnées du joueur lui-même. Par exemple, si les coordonnées du joueur `P` sont `(a, b, c)` et que le rayon AOI est `r`, alors sur l'axe des X, il y aura deux sentinelles, `left_x` et `right_x`, avec des coordonnées respectives `a - r` et `a + r`. 
En présence de sentinelles, nous mettons à jour l'AOI en suivant les déplacements des sentinelles par rapport aux autres entités. Reprenons l'exemple précédent : si une entité `E` se déplace et traverse de la droite vers la gauche au-delà de `left_x` sur l'axe X pour passer à gauche de `left_x`, cela signifie que `E` quitte sûrement l'AOI de `P` ; de même, si elle traverse de la droite à la gauche de `right_x`, c'est aussi qu'elle sort de l'AOI. En revanche, si elle franchit de la droite à la gauche de `left_x`, ou de la gauche à la droite de `right_x`, cela signifie qu'elle pourrait entrer dans l'AOI de `P`.

On peut observer que l'algorithme de la liste en croix est beaucoup plus complexe que la grille en neufs cases. Nous devons maintenir deux listes ordonnées, et lors de chaque mise à jour des coordonnées d'une entité, déplacer synchroniquement les nœuds des listes, et mettre à jour la zone d'intérêt (AOI) lors du déplacement au-dessus d'autres nœuds.

###La mise en œuvre du carré magique.

En raison de la performance liée aux mesures réelles, commençons par gratter un peu la surface des détails de mise en œuvre de l'algorithme de grille de neuf.

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

Le fichier `PlayerAoi` stocke les données des joueurs, incluant un tableau `sensors` qui sert à calculer les entités dans une certaine zone. Après chaque `Tick`, les entités calculées sont placées dans `aoi_players`. Ce dernier contient deux tableaux permettant de comparer les résultats du dernier `Tick` pour déterminer les entrées et sorties de joueurs. Le processus général de `Tick` est le suivant:

```cpp
AoiUpdateInfos SquareAoi::Tick() {
  AoiUpdateInfos update_infos;
  PlayerPtrList remove_list;

  for (auto& elem : player_map_) {
    auto& player = *elem.second;
    // ...
Calcul de l'Aoi pour les joueurs ayant des capteurs.
    if (!player.sensors.empty()) {
      auto update_info = _UpdatePlayerAoi(cur_aoi_map_idx_, &player);
      if (!update_info.sensor_update_list.empty()) {
        update_infos.emplace(update_info.nuid, std::move(update_info));
      }
    }
    // ...
  }

  // ...
Enregistrer la dernière position du joueur.
  for (auto& elem : player_map_) {
    auto& player = *elem.second;
    player.last_pos = player.pos;
  }
  cur_aoi_map_idx_ = 1 - cur_aoi_map_idx_;
  return update_infos;
}
```

La tâche effectuée par `Tick` est assez simple : parcourir les joueurs équipés de `capteurs`, calculer un par un les entités présentes dans la portée du `capteur`, c'est-à-dire la zone d'intérêt active (AOI). `last_pos` est utilisé pour déterminer si une entité est entrée ou sortie de l'AOI. Voici le code de `_UpdatePlayerAoi`: ...

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

`old_aoi` represents the AOI calculated in the previous `Tick`, while `new_aoi` is the AOI to be calculated in the current `Tick`. To determine `new_aoi`, all entities within the AOI range are traversed, selecting those with a distance from the player smaller than the AOI radius. Subsequently, the functions `_CheckLeave` and `_CheckEnter` are used to calculate the entities leaving and entering the AOI in this `Tick`. For instance, if an entity's `last_pos` in `new_aoi` is outside the AOI range, it indicates that the entity has entered the AOI in this `Tick`. Please refer to the source file for specific code implementation, as it won't be elaborated here.

###Implémentation de liste chaînée croisée

Par rapport à la grille en neuf cases, la liste en croix est plus complexe à mettre en place. Regardons d'abord les structures de données de base :

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

Les mots `Sensor` et `PlayerAoi` sont en partie similaires à la grille neuf cases, mais ils incluent une structure de nœud de liste chaînée supplémentaire appelée `CoordNode`. `CoordNode` est un nœud sur la liste chaînée, qui enregistre le type et la valeur du nœud lui-même. Il y a trois types : nœud de joueur, nœud `Sensor` à gauche, nœud `Sensor` à droite.

La majeure partie du travail de la liste chaînée double consiste à maintenir l'ordre de la liste :

Lorsqu'un joueur rejoint, il doit déplacer le nœud du joueur à une position ordonnée, et en déplaçant le nœud du joueur, gérer les événements d'entrée ou de sortie des autres joueurs dans l'Aire d'Intérêt des Joueurs (AOI).
Une fois que le joueur se déplace vers la bonne position, les nœuds `Sensor` de gauche et de droite se déplacent depuis l'avant et l'arrière du joueur jusqu'à la bonne position, et gèrent les événements d'entrée et de sortie déclenchés lorsqu'ils traversent les nœuds d'autres joueurs.
Lorsque le joueur se déplace, mettez à jour ses coordonnées, déplacez le nœud du joueur et les nœuds gauche et droit du `Capteur`, tout en gérant les entrées et sorties de la zone d'intérêt active (AOI).

Le code du nœud mobile est le suivant : chaque fois qu'il franchit un nœud, la fonction `MoveCross` est appelée. Dans `MoveCross`, en fonction de la direction du déplacement, du type de nœud franchi, il est décidé s'il faut entrer ou sortir de l'AOI.

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

Le déplacement des listes chaînées est très lent, avec une complexité de `O(n)`, notamment lorsque de nouveaux joueurs rejoignent la scène. Ils doivent se déplacer progressivement depuis une distance infinie jusqu'à la position correcte, ce qui nécessite une grande quantité de parcours de nœuds et entraîne une consommation élevée. Pour optimiser les performances, nous pouvons placer des phares à des emplacements fixes dans la scène. Ces phares ont un traitement similaire aux joueurs, mais avec une capacité en plus qui enregistre les données `détectées par`, indiquant quels capteurs l'entité sentinelle se trouve dans le champ. Lors de la première entrée d'un joueur dans la scène, il ne commence plus à se déplacer depuis le point le plus éloigné, mais trouve le phare le plus proche, insère le nœud à côté du phare et à travers les données `détectées par` du phare, il entre rapidement dans la plage d'AOI des autres joueurs alignés sur le phare, puis commence à se déplacer vers la position correcte. Bien entendu, pendant le déplacement, il faut également gérer les entrées et sorties. De même, pour les capteurs, il est possible d'optimiser en héritant d'abord des données des phares, puis en se déplaçant de leur position vers la position correcte. Ces deux types d'optimisation peuvent augmenter les performances des insertions de joueurs de plus de deux fois.

Il y a aussi une `HashMap` appelée `aoi_player_candidates` sur le capteur (ici, pour des raisons de performance, [khash](https://github.com/attractivechaos/klib/blob/master/khash.h)Les événements AOI déclenchés par le déplacement des nœuds ne peuvent en fait détecter qu'une zone carrée de côté `2r` sur les axes X-Z, et non une AOI circulaire stricte. Les entités à l'intérieur de cette zone carrée sont enregistrées dans `aoi_player_candidates`, puis parcourues dans `Tick` pour calculer la portée de l'AOI dans la zone circulaire, ce qui les désigne comme des `candidates`.

Toutes les opérations sur les listes croisées sont destinées à maintenir en permanence les entités "candidates" à l'intérieur de la région carrée. Les opérations effectuées par la liste croisée sont presque identiques à celles de la grille de 9 cases, à la différence que le calcul des candidats AOI diffère. Les candidats de la grille de 9 cases sont les entités des cases couvertes par la zone ronde de l'AOI, tandis que la liste croisée est définie par les nœuds gauche et droit du "Capteur" et regroupe les entités de la région carrée de côté 2r. En termes qualitatifs, les candidats des listes croisées sont généralement moins nombreux que ceux de la grille de 9 cases, ce qui entraîne moins de passages dans "Tick", améliorant ainsi les performances. Cependant, les listes croisées consomment également des ressources supplémentaires pour leur maintenance. La performance globale de ces deux approches reste à déterminer, et nous allons le vérifier lors des tests à venir.

###Test de performance

J'ai mesuré séparément le temps pris par les joueurs pour rejoindre la scène (`Ajout de joueur`), pour les événements d'entrée et de sortie de la zone d'intérêt (`Tick`), ainsi que pour la mise à jour des coordonnées des joueurs (`Mise à jour de la position`).

Les joueurs sont placés de façon aléatoire dans la plage de la carte et ajoutés à la scène. `player_num` représente le nombre de joueurs, tandis que `map_size` désigne la plage des coordonnées X-Z de la carte. Les positions des joueurs sont générées de manière aléatoire uniforme dans cette plage, chacun ayant un rayon de `100` pour son capteur d'AOI. Le temps de calcul est effectué à l'aide de `boost::timer::cpu_timer`. Trois scénarios ont été pris pour `player_num`, à savoir `100, 1000, 10000`, tandis que quatre cas ont été étudiés pour `map_size`, à savoir `[-50, 50], [-100, 100], [-1000, 1000], [-10000, 10000]`.

Actualisation de la position du joueur pour le faire se déplacer dans une direction aléatoire à une vitesse de `6m/s`.

Le texte en français est : 

"本次测试环境为："

* CPU: Intel(R) Core(TM) i5-4590 CPU @ 3.30GHz
Système : Debian GNU/Linux 10 (buster)
Version de gcc : gcc version 8.3.0 (Debian 8.3.0-6)
Version boost : boost_1_75_0

####Test de grille en neuf cases

Les résultats du test de la grille de neuf cases sont les suivants :

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

Lorsque le nombre de joueurs dans une grille 3x3 atteint 100, les trois opérations ont un faible temps d'exécution, avec des conditions extrêmes où la taille de la carte est de -50 à 50 et tous les joueurs se trouvent dans la zone d'intérêt (AOI). Un cycle de traitement prend environ 0,4 millisecondes. L'ajout de joueurs et la mise à jour des coordonnées s'effectuent en complexité linéaire O(n) pour des performances satisfaisantes. Cependant, lorsque le nombre de joueurs atteint 10 000, et que la taille de la carte reste la même, l'opération Add Player et Update Pos, malgré leur complexité linéaire, prennent quelques millisecondes, tandis que le Tick prend environ 3,8 secondes, consommant ainsi beaucoup de ressources CPU et rendant le système inutilisable. Avec 10 000 joueurs et une carte de taille -1000 à 1000, le Tick prend environ 94 millisecondes. Réduire la fréquence du Tick à deux fois par seconde maintiendrait le système tout juste dans la plage d'utilisation acceptable.

####Liste croisée vérifiée en pratique

Les résultats des tests de la liste chaînée en croix sont les suivants :

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

Si nous analysons en détail, les listes croisées prennent plus de temps pour les opérations `Ajouter joueur` et `Mettre à jour la position`, en particulier pour `Ajouter joueur`, la performance est inférieure de plusieurs centaines voire milliers de fois par rapport à la grille à neuf cases (`100, [-50, 50]` - listes croisées prennent `2ms`, tandis que la grille à neuf cases n'en prend que `0.08ms`; `10000, [-50, 50]` - listes croisées prennent `21.6s`, la grille à neuf cases uniquement `6ms`). Le temps nécessaire pour `Mettre à jour la position` peut également varier jusqu'à cent fois, pour `10000, [-100, 100]` les listes croisées pour mettre à jour la position d'un joueur prennent `1.5s`, alors que la grille à neuf cases ne prend que `18ms`. On remarque que les listes croisées ont une plage de temps plus large pour les opérations `Ajouter joueur` et `Mettre à jour la position` par rapport à la grille à neuf cases, elles sont plus sensibles au nombre de joueurs et à la taille de la carte. Dans les zones à forte densité de joueurs, les performances de ces deux opérations chuteront rapidement jusqu'à devenir inutilisables.

En ce qui concerne l'opération `Tick` de la grille en croix, les performances globales sont en effet meilleures que celles de la grille en 9 carrés. Dans le meilleur des cas, le temps nécessaire est d'environ la moitié de celui de la grille en 9 carrés (`1000, [-1000, 1000]` - grille en croix : 0,8 ms, grille en 9 carrés : 1,8 ms). Cependant, dans le pire des cas, la performance de la grille en croix peut se dégrader pour être proche de celle de la grille en 9 carrés (`10000, [-10000, 10000]` - grille en croix : 3,7 s, grille en 9 carrés : 3,8 s). En effet, étant donné la petite taille de l'environnement où les joueurs se trouvent dans les AOI les uns des autres, le nombre de "candidates" traversé par le `Tick` de la grille en croix est en réalité très proche de celui de la grille en 9 carrés.

Pour obtenir des performances supérieures à celle de la grille 9x9 en utilisant la grille en croix, il est nécessaire de faire des hypothèses plus fortes, comme par exemple avec `player_num = 1000, map_size = [-1000, 1000]`. Dans ce cas, le temps pris par un `Tick` avec la grille en croix est de `0,8ms` contre `1,8ms` pour la grille 9x9. Pour l'opération `Update Pos`, la grille en croix nécessite `0,3ms` contre `0,18ms` pour la grille 9x9 (il convient de noter que le temps de test de `Update Pos` est la somme des temps de 10 exécutions). Pour réduire le temps total de `Tick + Update Pos` par rapport à la grille 9x9, le nombre d'opérations `Update Pos` ne doit pas dépasser 8 fois le nombre de `Tick`, autrement dit, entre deux `Tick`, le nombre d'opérations `Update Pos` doit être inférieur à 8. De plus, étant donné que l'ajout de joueur sur la grille en croix est très chronophage, elle n'est pas adaptée aux situations où les joueurs entrent et sortent fréquemment du scénario dans un laps de temps court ou se téléportent sur une grande distance dans le scénario. Par ailleurs, l'arrivée massive de joueurs sur une période courte peut également entraîner une baisse des performances et une utilisation intensive du CPU.

En ce qui concerne la liste en croix, il est possible d'optimiser en supprimant le "Tick", à condition que le jeu puisse accepter une zone d'intérêt (AOI) carrée, et que les autres coûts tels que ceux liés au réseau entraînés par l'utilisation d'une AOI carrée soient acceptables. Cette condition est assez stricte, car en général la consommation de CPU liée au calcul de l'AOI dans le jeu n'est pas très élevée. Cependant, le passage d'une AOI circulaire à une AOI carrée entraine une augmentation de la surface de la zone d'intérêt, ce qui peut conduire à une augmentation du nombre de joueurs à l'intérieur, potentiellement jusqu'à 1,27 fois plus. Une fois cette condition remplie, la liste en croix peut être mise à jour sans avoir besoin du "Tick" pour actualiser périodiquement les événements de l'AOI, car la liste en croix maintient déjà une version carrée de l'AOI, qui était antérieurement utilisée uniquement pour calculer l'AOI circulaire, nécessitant ainsi une nouvelle itération de calcul de distance dans le "Tick". Dans ce scénario, la liste en croix peut offrir d'excellentes performances, car les performances de la fonction "Mettre à jour la position" de la liste en croix peuvent être plusieurs fois, voire plusieurs dizaines de fois, plus élevées que celles du "Tick".

Fournir enfin un diagramme en barres comparatif des deux.

![](assets/img/2021-11-18-aoi-tesing/add_player.png)

![](assets/img/2021-11-18-aoi-tesing/tick.png)

![](assets/img/2021-11-18-aoi-tesing/update_pos.png)


###Résumé

Dans ce texte, nous présentons les principes et la mise en œuvre de deux algorithmes AOI (grille de neuf et chaîne en croix), et analysons les performances de ces deux algorithmes à partir de données mesurées, en espérant offrir aux lecteurs une aide ou une inspiration.

Dans l'ensemble, la méthode de la grille en carré est simple à implémenter, avec des performances équilibrées qui ne traînent pas en route, ce qui la rend très adaptée aux jeux qui ne sont pas limités en termes de performances par l'AOI. La plage de fluctuation des performances de la méthode de la grille en carré est dans une fourchette prévisible, avec une performance minimale relativement élevée, ce qui limite également les goulets d'étranglement. D'un autre côté, l'optimisation de l'espace n'est pas très importante, et la complexité temporelle est assez fixe. En revanche, la méthode de la chaîne en croix nécessite une mise en œuvre plus complexe et a une performance minimale inférieure à celle de la méthode de la grille en carré. Cependant, si certaines hypothèses et conditions préalables sont remplies, la méthode de la chaîne en croix peut offrir une meilleure optimisation de l'espace, c'est-à-dire un potentiel d'amélioration plus élevé. Ces deux méthodes ont leurs avantages et leurs inconvénients, et différents moteurs de jeux de l'industrie ont choisi l'une ou l'autre en fonction de leurs besoins respectifs, chacun choisissant ce qui lui convient le mieux, selon son jugement.

Mes compétences sont limitées, le contenu ci-dessus ne représente que mes propres idées. Si des lacunes ou des erreurs sont présentes, n'hésitez pas à laisser un commentaire pour en discuter.

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT, veuillez [**donner votre avis**](https://github.com/disenone/wiki_blog/issues/new)Identifier toute omission éventuelle. 
