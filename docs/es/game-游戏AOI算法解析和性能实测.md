---
layout: post
title: '"Análisis y prueba de rendimiento del algoritmo AOI de juegos"'
categories:
- c++
catalog: true
tags:
- dev
- game
description: 'En este texto se discuten dos algoritmos: el sudoku y la cadena cruzada.
  Se proporciona un análisis de rendimiento práctico para ambos algoritmos, para que
  puedas tener una idea clara y actuar con confianza ante cualquier situación.'
figures: []
date: 2021-11-18
---

<meta property="og:title" content="游戏 AOI 算法解析和性能实测" />

###Introducción

`AOI` (Area Of Interest) es una función muy básica en los juegos en línea multijugador, donde los jugadores necesitan recibir información de otros jugadores o entidades (Entity) que se encuentren dentro de su campo de visión. Los algoritmos utilizados para determinar qué entidades existen dentro del campo de visión de un jugador, así como cuáles entran o salen de su campo de visión, generalmente se denominan algoritmos `AOI`.

Este texto discute dos algoritmos `AOI`, el cuadrícula de nueve puntos y la cadena de cruz, y proporciona un análisis de rendimiento empírico de ambos algoritmos para que puedas tener una idea clara y no te pongas nervioso cuando te encuentres con situaciones.

En el texto se mencionarán dos términos: "jugador" y "entidad". "Entidad" se refiere al concepto de un objeto en el juego, mientras que "jugador" se refiere a una entidad que tiene un Área de Interés (AOI).

El código mencionado en el texto se puede encontrar aquí: [AoiTesting](https://github.com/disenone/AoiTesting).

###九宫格

El llamado "cuadrícula 9x9" es la división de las posiciones de todas las entidades en un escenario en casillas, por ejemplo, dividiéndolas en cuadrados de 200 unidades de lado. Para encontrar otras entidades dentro del rango de AOI del jugador central, se compara con todos los jugadores dentro de las casillas involucradas en este rango.

Por ejemplo, en cada momento, la escena hará un "Tick" cada 100 milisegundos. En el Tick, podemos actualizar el AOI del jugador de la siguiente manera:

* Con el jugador como centro, se calcula la colección de casillas involucradas con un radio de AOI.
* Calcular la distancia entre cada entidad en el conjunto de celdas y el jugador.
* La colección de entidades cuya distancia es menor al radio de AOI se convierte en el nuevo AOI del jugador.

El algoritmo de la cuadrícula de 9 casillas es bastante simple de implementar, ya que se puede describir en pocas frases. Dejaremos el análisis de rendimiento específico para más adelante, primero echemos un vistazo al algoritmo de lista enlazada de cruz.

###**十字链表**

Una **lista de enlaces cruzados** es una estructura de datos utilizada comúnmente en programación. También se conoce como una **lista de enlaces dobles** o una **lista enlazada cruzada**. En esta estructura, cada nodo contiene referencias a los nodos siguientes en dos direcciones: hacia adelante y hacia atrás. Esto permite un acceso eficiente a los elementos anteriores y siguientes en la lista. La implementación de una lista de enlaces cruzados puede ser muy útil en una amplia variedad de aplicaciones, como edición de texto, manipulación de imágenes o trabajo con bases de datos. Esta estructura de datos es especialmente útil cuando se necesita realizar operaciones de inserción o eliminación en una lista de forma eficiente.

Para los juegos en 3D, normalmente creamos listas enlazadas ordenadas para las coordenadas del eje X y del eje Z. Cada entidad tiene un nodo en la lista que almacena el valor de la coordenada correspondiente. Los valores se almacenan en orden creciente. Sin embargo, si solo almacenamos los puntos de coordenadas de las entidades, la eficiencia de búsqueda de estas dos listas sigue siendo baja.

Lo realmente importante es que en la lista enlazada también agregamos dos nodos centinela, uno a la izquierda y otro a la derecha, para cada jugador que tenga un AOI. Las coordenadas de estos dos nodos centinela difieren exactamente en el radio del AOI en comparación con las coordenadas del jugador. Por ejemplo, si las coordenadas del jugador `P` son `(a, b, c)` y el radio del AOI es `r`, entonces en el eje X habrá dos nodos centinela, `left_x` y `right_x`, con coordenadas `a - r` y `a + r` respectivamente. Con la presencia de estos nodos centinela, actualizamos el AOI mediante el seguimiento del movimiento de los nodos centinela y los demás nodos de entidades.

Continuando con el ejemplo anterior, si una entidad `E` se mueve y cruza desde la derecha de `left_x` hacia la izquierda de `left_x`, entonces significa que `E` definitivamente ha salido del AOI de `P`. De manera similar, si cruza a la derecha de `right_x`, también ha salido del AOI. Por el contrario, si cruza a la derecha de `left_x` o a la izquierda de `right_x`, significa que es posible que entre en el AOI de `P`.

Se puede observar que el algoritmo de lista cruzada es mucho más complejo que el algoritmo de cuadrícula de nueve celdas. Necesitamos mantener dos listas ordenadas y, al actualizar las coordenadas de las entidades, mover los nodos en las listas de forma sincronizada y actualizar el AOI cuando pasamos por encima de otros nodos.

###Implementación de la rejilla de nueve celdas

Debido a que implica un rendimiento medido, vamos a profundizar un poco en los detalles de implementación del algoritmo de matriz 9x9:

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

`PlayerAoi` almacena los datos del jugador, que incluye una matriz llamada `sensores`, utilizada para calcular entidades dentro de un rango específico. Después de cada `Tick`, las entidades calculadas se colocan en la variable `aoi_players`. `aoi_players` es un arreglo que almacena dos matrices y se utiliza para comparar los resultados del último `Tick`, determinando las entidades que ingresan y salen del jugador. El proceso aproximado del `Tick` es el siguiente:

```cpp
AoiUpdateInfos SquareAoi::Tick() {
  AoiUpdateInfos update_infos;
  PlayerPtrList remove_list;

  for (auto& elem : player_map_) {
    auto& player = *elem.second;
    // ...
// Calculando el Aoi para los jugadores con sensores
    if (!player.sensors.empty()) {
      auto update_info = _UpdatePlayerAoi(cur_aoi_map_idx_, &player);
      if (!update_info.sensor_update_list.empty()) {
        update_infos.emplace(update_info.nuid, std::move(update_info));
      }
    }
    // ...
  }

  // ...
// Registrar la última posición del jugador
  for (auto& elem : player_map_) {
    auto& player = *elem.second;
    player.last_pos = player.pos;
  }
  cur_aoi_map_idx_ = 1 - cur_aoi_map_idx_;
  return update_infos;
}
```

`Tick` hace algo muy sencillo, recorre a los jugadores con `sensores` y calcula individualmente las entidades dentro del rango del `sensor`, que es el AOI. `last_pos` se utiliza para determinar si una entidad ha entrado o salido del AOI. El código de `\_UpdatePlayerAoi` es el siguiente:

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

`old_aoi` es el AOI calculado en el último `Tick`, `new_aoi` es el AOI que se va a calcular en esta ocasión. `new_aoi` se obtiene recorriendo todas las entidades en las celdas dentro del rango del AOI, seleccionando aquellas que están a una distancia menor al radio del AOI desde el jugador. Luego, se utilizan las funciones `_CheckLeave` y `_CheckEnter` para determinar las entidades que salen o entran en el AOI en este `Tick`. Por ejemplo, si la posición `last_pos` de una entidad en `new_aoi` no está dentro del rango del AOI, significa que esa entidad entró en el rango en este `Tick`. El código específico se puede encontrar en el archivo fuente, por lo que no entraré en más detalles aquí.



###**La implementación de una lista enlazada circular**

En comparación con la lista de cuadrícula, la implementación de la lista de enlaces cruzados es más compleja. Primero, veamos la estructura de datos básica:

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

`Sensor` y `PlayerAoi` son similares al `Grid de nueve cuadros`, pero tienen una estructura de nodo de lista vinculada adicional llamada `CoordNode`. `CoordNode` es un nodo en la lista vinculada que registra el tipo y el valor del propio nodo. Hay tres tipos: nodo del jugador, nodo izquierdo de `Sensor` y nodo derecho de `Sensor`.

La mayor parte del trabajo de una lista enlazada cruzada consiste en mantenerla ordenada:

*Cuando un jugador se une, debe mover el nodo del jugador a una posición ordenada y, al mismo tiempo, manejar los eventos de entrada o salida de otros jugadores en el sistema AOI.*
Una vez que el jugador se mueve a la posición correcta, los nodos de "Sensor" izquierdo y derecho se mueven desde la posición del jugador hacia adelante y hacia atrás, se posicionan correctamente y manejan los eventos de entrada y salida que se activan al cruzar otros nodos de jugadores.
* Cuando el jugador se mueve, se actualizan las coordenadas del jugador y se mueven los nodos del jugador y los nodos izquierdo y derecho del `Sensor`, para manejar la entrada y salida en el AOI.

El código para mover el nodo móvil es el siguiente: cada vez que se pasa por un nodo, se llama a la función `MoveCross`. La función `MoveCross` decide si se ingresa o se sale del Área de Interés (AOI) en función de la dirección del movimiento, el nodo que se está moviendo y el tipo de nodo que se cruza.

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

La movilidad de las listas enlazadas es lenta, con una complejidad de `O(n)`, especialmente cuando se agrega un nuevo jugador al escenario. Los jugadores tienen que moverse desde una distancia infinita hasta llegar a la posición correcta, lo que implica recorrer una gran cantidad de nodos y consume muchos recursos. Para optimizar el rendimiento, podemos colocar faros en posiciones fijas dentro del escenario. Estos faros se comportan de manera similar a los jugadores, pero además llevan un registro adicional llamado `detected_by`, que guarda información sobre los sensores que detectan a la entidad centinela. Al momento de ingresar al escenario, en lugar de comenzar desde la posición más lejana, el jugador encuentra el faro más cercano, inserta el nodo junto a él y, utilizando los datos de `detected_by` del faro, ingresa rápidamente al rango de AOI (área de interés) de otros jugadores que coinciden con el faro. Luego, comienza a moverse hacia la posición correcta, teniendo en cuenta también las entradas y salidas. Del mismo modo, los sensores pueden heredar los datos de los faros y moverse desde la posición del faro hasta la posición correcta. Estas dos optimizaciones permiten mejorar el rendimiento de inserción de jugadores en más del doble.

El `Sensor` todavía tiene un `HashMap` llamado `aoi_player_candidates` en su cuerpo (aquí, para mejorar el rendimiento, se utiliza [khash](https://github.com/attractivechaos/klib/blob/master/khash.h)）。El evento AOI desencadenado por el movimiento de los nodos solo puede detectar un área cuadrada con longitud de lado de `2r` en los ejes X-Z, no es el AOI circular en el sentido estricto. Las entidades dentro de esta área cuadrada se registran en `aoi_player_candidates` y se calcula el rango del AOI en el área circular durante el `Tick`, por lo que se llaman "candidatos".

Todas las operaciones de la lista de crucigramas se realizan para mantener constantemente las entidades "candidatas" dentro de un área cuadrada. Las operaciones realizadas por el "Tick" en la lista de crucigramas son casi idénticas a las del patrón de casillas de un sudoku, solo que el cálculo de las entidades "candidatas" que se recorren para calcular el "AOI" es diferente. Las entidades "candidatas" en el patrón de casillas de un sudoku son aquellas que están cubiertas por el área circular del "AOI", mientras que en la lista de crucigramas son las que se encuentran dentro de un área cuadrada de longitud de lado "2r" definida por los nodos izquierdo y derecho del "Sensor". Cualitativamente hablando, las entidades "candidatas" en la lista de crucigramas suelen ser menos que las del patrón de casillas de un sudoku, por lo que el número de iteraciones dentro de "Tick" es menor, lo que se traduce en un rendimiento óptimo. Sin embargo, la lista de crucigramas todavía tiene una cantidad significativa de consumo adicional de rendimiento debido al mantenimiento de la lista. Así que ahora probemos y comparemos el rendimiento general de estos dos enfoques.

###性能实测

Aquí he medido el tiempo de ejecución de tres casos diferentes en mi juego: la entrada de un jugador a una escena (`Añadir Jugador`), el cálculo de eventos de entrada y salida en el área de interés (`Tick`), y la actualización de la posición del jugador (`Actualizar Pos`).

El punto de partida del jugador se genera aleatoriamente dentro del rango del mapa y luego se incorpora al escenario. `player_num` es la cantidad de jugadores y `map_size` es el rango de ejes X-Z del mapa. La posición de cada jugador se genera aleatoriamente de manera uniforme dentro de este rango. Cada jugador tiene un "Sensor" con un radio de `100` que se utiliza como Área de Interés (AOI) y se utiliza el temporizador de CPU `boost::timer::cpu_timer` para calcular el tiempo. Se seleccionaron tres casos diferentes para `player_num`: `100, 1000, 10000`, y cuatro casos diferentes para `map_size`: `[-50, 50], [-100, 100], [-1000, 1000], [-10000, 10000]`.

Actualizar la ubicación del jugador hará que el jugador se mueva en dirección aleatoria fija a una velocidad de `6m/s`.

La configuración del entorno de prueba en esta ocasión es la siguiente:

* CPU: Intel(R) Core(TM) i5-4590 CPU @ 3.30GHz
* Sistema: Debian GNU/Linux 10 (buster)
* Versión de gcc: gcc versión 8.3.0 (Debian 8.3.0-6)
* Versión de Boost: boost_1_75_0

####九宫格实测

Los resultados de la prueba del cuadrado mágico son los siguientes:

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

En el caso de un tablero de juego de nueve cuadrículas con `100` jugadores, las tres operaciones tienen un tiempo de ejecución muy corto. En el caso extremo de `map_size = [-50, 50]`, todos los jugadores están dentro del rango de AOI y el tiempo de ejecución de `Tick` es de aproximadamente `0.4ms`. Tanto la operación de agregar jugadores a la escena como la de actualizar las coordenadas tienen una complejidad lineal `O(player_num)`, y su rendimiento es bueno. Sin embargo, cuando el número de jugadores aumenta a 10,000 (`player_num = 10000`) y se mantiene el mismo tamaño de mapa (`map_size = [-50, 50]`), agregar jugadores y actualizar posiciones toman solo unos milisegundos debido a su complejidad lineal, pero el tiempo de ejecución de `Tick` aumenta a `3.8s`, lo que requiere una gran cantidad de CPU y ya no es utilizable. Si tenemos 10,000 jugadores y un tamaño de mapa de `[-1000, 1000]`, el tiempo de ejecución de `Tick` es de aproximadamente `94ms`. Si pudiéramos reducir la frecuencia de `Tick`, por ejemplo a dos veces por segundo, aún estaría dentro de un rango utilizable, aunque con dificultad.

####**十字链表实测**  

Traducción al español:  

**Pruebas prácticas de lista enlazada cruzada**

El resultado de la prueba de la lista enlazada cruzada es el siguiente:

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

Como hemos analizado, la lista de crucigrama es más lenta en las operaciones `Add Player` y `Update Pos`, especialmente en `Add Player`, donde su rendimiento es incluso cientos o incluso miles de veces peor que el de la cuadrícula de nueve celdas (`100, [-50, 50]` la lista de crucigrama lleva `2ms`, mientras que la cuadrícula de nueve celdas solo toma `0.08ms`; `10000, [-50, 50]` la lista de crucigrama lleva `21.6s`, mientras que la cuadrícula de nueve celdas solo toma `6ms`). El tiempo de ejecución de `Update Pos` también puede diferir hasta en cientos de veces, donde `10000, [-100, 100]` la actualización de la posición del jugador en la lista de crucigrama lleva `1.5s`, mientras que en la cuadrícula de nueve celdas solo toma `18ms`. Se puede observar que la lista de crucigrama tiene un rango de límites superior e inferior más amplio en términos de tiempo de ejecución en `Add Player` y `Update Pos`, y es más afectada por el número de jugadores y el tamaño del mapa. En áreas con una alta densidad de jugadores, el rendimiento de estas dos operaciones disminuirá rápidamente hasta volverse inutilizables.

Por otro lado, en cuanto a la operación "Tick" de la cadena de crucigramas, en general, su rendimiento es realmente mejor que el del cuadrado mágico. En el mejor de los casos, solo toma aproximadamente la mitad del tiempo que el cuadrado mágico. (Cadena de crucigramas: 0.8 ms, Cuadrado mágico: 1.8 ms) Sin embargo, en el peor de los casos, la cadena de crucigramas puede degradarse y tener un rendimiento similar al del cuadrado mágico. (Cadena de crucigramas: 3.7 s, Cuadrado mágico: 3.8 s) Esto se debe a que, debido a que la escena es pequeña, los jugadores están dentro del rango de AOI de los demás, por lo que la cantidad de "candidatos" que atraviesa la cadena de crucigramas en cada iteración del "Tick" es muy similar a la del cuadrado mágico.

十字链使用起来要达到比九宫格性能更优，需要一些更强的假设，譬如 `player_num = 1000, map_size = [-1000, 1000]` 情况下，`Tick` 耗时十字链为 `0.8ms` 九宫格 `1.8ms`，`Update Pos` 十字链为 `0.3ms` 九宫格 `0.18ms`（注意测试 `Update Pos` 时间为执行了 10 次的时间总和）。`Tick + Update Pos` 总时间下，十字链如果要比九宫格更少，那 `Update Pos` 的次数不能超过 `Tick` 的 `8` 倍，或者说两个 `Tick` 之间，`Update Pos` 的次数需要小于 `8` 次。另外因为十字链 `Add Player` 耗时巨大，不适用于玩家短时间频繁出入场景或者在场景内大范围传送的情况，另外如果短时间内有大量玩家进入场景，也很容易导致性能下降，大量占用 CPU。

Para la lista enlazada cruzada, se puede realizar una optimización bajo la premisa de eliminar `Tick`, siempre y cuando el juego pueda aceptar un AOI cuadrado y se pueda tolerar el consumo adicional en otras áreas como la red, siempre y cuando se haya probado experimentalmente. En realidad, esta premisa es bastante estricta, ya que en los juegos, el porcentaje de CPU que puede ocupar el cálculo del AOI no suele ser muy alto. Sin embargo, cambiar el AOI circular a un AOI cuadrado provoca un aumento en el área del AOI, lo que a su vez puede aumentar la cantidad de jugadores dentro del rango, lo que podría resultar en un incremento aproximado de 1.27 veces la cantidad original.

Sin embargo, una vez que se cumple esta premisa, la lista enlazada cruzada puede lograr actualizaciones periódicas de los eventos del AOI sin necesidad de `Tick`, ya que la implementación de la lista enlazada cruzada mantiene una versión del AOI en forma de un área cuadrada. Anteriormente, esto solo se hacía para calcular el AOI circular y se veía obligado a realizar cálculos de distancia dentro de `Tick`. En esta situación, la lista enlazada cruzada puede proporcionar un rendimiento óptimo, ya que la eficiencia de la función "Update Pos" puede ser varias veces o incluso decenas de veces mejor en comparación con `Tick`.

Finalmente, se presenta un gráfico de barras que muestra la comparación entre ambas.

![](assets/img/2021-11-18-aoi-tesing/add_player.png)

![](assets/img/2021-11-18-aoi-tesing/tick.png)

![](assets/img/2021-11-18-aoi-tesing/update_pos.png)


###**总结**

En este documento, presentamos los principios y la implementación básica de dos algoritmos de AOI (Área de Interés Automática): la cuadrícula de nueve celdas y la cadena en forma de cruz. Además, analizamos el rendimiento y las ventajas y desventajas de estos dos algoritmos utilizando datos de pruebas reales. Esperamos que esto pueda brindar ayuda e inspiración a los lectores.

En resumen, el método de la rejilla de nueve cuadros es fácil de implementar y equilibra bien el rendimiento, por lo que es muy adecuado para juegos que no dependen tanto del rendimiento como AOI. La variación de rendimiento del método de la rejilla de nueve cuadros se mantiene dentro de un rango previsible, con un límite inferior de rendimiento relativamente alto y no es fácil que se convierta en un cuello de botella. Sin embargo, en cuanto a la optimización del espacio, tiene un margen bastante limitado y su complejidad es similar en términos de tiempo de ejecución.

Por otro lado, el método de la cadena de cruz es más complicado de implementar y tiene un límite inferior de rendimiento más bajo que el método de la rejilla de nueve cuadros. Sin embargo, si se cumplen ciertas suposiciones y premisas, el método de la cadena de cruz tiene un potencial de optimización de espacio más alto, es decir, su límite superior puede ser más alto. Ambos métodos tienen sus ventajas y desventajas, y en la industria de los videojuegos existen diferentes motores que eligen uno de estos métodos según sus necesidades y opiniones individuales.

**本人能力有限，文中内容仅代表本人想法，如有不足不妥之处欢迎留言讨论。**

Mis habilidades son limitadas, el contenido de este texto representa únicamente mi opinión. Si encuentran algún error o algo inadecuado, les agradezco que dejen un mensaje para discutirlo.

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
