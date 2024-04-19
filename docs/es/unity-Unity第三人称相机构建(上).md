---
layout: post
title: Construcción de la cámara en tercera persona de Unity (Parte 1)
categories:
- unity
catalog: true
tags:
- dev
description: Me gustaría crear una cámara en tercera persona en Unity, tomando como
  referencia la cámara en tercera persona de "World of Warcraft". Comencemos por solucionar
  el problema de la rotación de la cámara.
figure: null
---

<meta property="og:title" content="Unity第三人称相机构建(上)" />

Quiero crear una cámara en tercera persona en Unity, cuyo comportamiento esté inspirado en la cámara en tercera persona de "World of Warcraft". Los requisitos específicos son los siguientes:

1. Ratón izquierdo: controla la rotación de la cámara alrededor del personaje, el personaje no gira.
2. Ratón derecho: Controla la rotación de la cámara alrededor del personaje. La dirección hacia la que mira el personaje (transform.forward en Unity) gira en consecuencia, mientras que la dirección hacia arriba del personaje se mantiene constante.
3. Después de girar haciendo clic con el botón izquierdo del ratón, luego girar con el botón derecho, la dirección hacia adelante del personaje se ajustará inmediatamente según la rotación del botón izquierdo, luego se ajustará según la rotación del botón derecho. En este momento, es equivalente a girar dos veces con el botón derecho.
4. **Rueda de desplazamiento**: Controla el acercamiento y alejamiento de la cámara.
5. La cámara no puede atravesar ningún objeto rígido.
6. La cámara vuelve lentamente a la distancia original después de separarse del objeto rígido al que ha chocado.
7. Si la cámara entra en contacto con un objeto, se debe usar la rueda del ratón para acercarla, y la cámara deberá responder inmediatamente. A partir de ese momento, el punto 6 ya no se aplica.
8. La cámara golpeó el suelo mientras giraba, dejando de girar alrededor del personaje de arriba a abajo y cambiando a girar alrededor de sí misma de arriba a abajo. El giro de izquierda a derecha seguirá siendo alrededor del personaje.



Este requisito se puede dividir en dos partes: rotación de la cámara y rigidez de la cámara. Para facilitar las cosas, vamos a resolver primero el problema de la rotación de la cámara, es decir, los primeros 3 puntos del requisito.

**相机位置表示**

La frase "相机位置表示" en español se traduce como "Indicación de la posición de la cámara".
----------------
Antes de abordar formalmente la solución a la operación de la cámara, hay una cuestión que debe resolverse: la representación de la posición de la cámara. Esto se puede hacer de varias formas:

- Coordenadas mundiales de la cámara
- Coordenadas de la cámara con respecto al personaje.
- La dirección y la distancia de la cámara en el sistema de coordenadas de la persona.

Porque en nuestras necesidades, la cámara cambia según la posición de los personajes, aquí utilizo la tercera forma, y en el control la cámara siempre apunta al personaje, por lo que solo necesito guardar la información de la distancia dentro de la cámara.

```c#
float curDistance = 5F;
```

**相机旋转**

La cámara se está girando.
-------------
Para continuar con la subdivisión del comportamiento de rotación de la cámara, podemos dividirlo en rotación con el botón izquierdo y rotación con el botón derecho. A continuación, vamos a completar estos dos tipos de rotación paso a paso. Primero, voy a establecer la cámara como un subobjeto (children) del personaje, de esta manera la cámara seguirá automáticamente los movimientos básicos del personaje.

######Girar con el botón izquierdo del mouse
Solo mirando la rotación del botón izquierdo, el requisito es muy sencillo: **la cámara gira, el personaje no gira**, esto equivale a una cámara de observación de modelos, la cámara puede observar el objeto central desde cualquier ángulo.

En Unity, para obtener el estado del clic izquierdo del ratón, podemos usar la expresión `Input.GetMouseButton(0)` (nota: en las secciones de código que siguen, se usa el lenguaje C#). De manera similar, el clic derecho se representa con `Input.GetMouseButton(1)`. Para obtener la información de desplazamiento del cursor del ratón (es decir, el desplazamiento en los ejes X e Y entre frames), se utilizan las siguientes expresiones: `Input.GetAxis("Mouse X")` y `Input.GetAxis("Mouse Y")`. Ahora, podemos obtener la información de desplazamiento del cursor cuando se mantiene pulsado el clic izquierdo del ratón:

```csharp
if (Input.GetMouseButton(0))
{
    float x = Input.GetAxis("Mouse X");
    float y = Input.GetAxis("Mouse Y");
}
```
 
El código es muy simple, pero aquí está la parte clave: cómo controlar la rotación de la cámara. Para comprender la rotación, se necesita algún conocimiento sobre cuaterniones (hay mucha información en línea, no la enumeraré aquí). Un punto importante sobre los cuaterniones es que pueden construir rotaciones de manera muy sencilla, especialmente alrededor de un vector dado. Una vez que se comprenden los cuaterniones, no es difícil implementar la rotación de la cámara alrededor de un personaje.

Otra cosa a tener en cuenta es que el eje de rotación de los cuaterniones es simplemente un vector con origen en el punto (0,0,0). Si se desea tomar como origen el punto `O` en el sistema de coordenadas del mundo, y utilizar el vector `V` con origen en dicho punto como eje de rotación, es necesario realizar una transformación de coordenadas. En pocas palabras, se debe llevar el punto `P` que se desea rotar al sistema de coordenadas con origen en `O`, rotarlo según el vector `V` y luego volver a transformarlo al sistema de coordenadas del mundo. A partir de estas operaciones, se puede escribir una función con esta funcionalidad: 

```c#
Vector3 MyRotate(Vector3 oldPosition, float angle, Vector3 axis, Vector3 axisPosition)
{
// Construye un cuaternión que rota alrededor del eje "axis" en el sistema de coordenadas del personaje.
    Quaternion rotation = Quaternion.AngleAxis(angle, axis);

    Vector3 offset = oldPosition - axisPosition;
// Calcular la rotación y transformar de vuelta al sistema de coordenadas global
    return axisPosition + (rotation * offset);
}
```
`Quaternion` es el tipo de dato en Unity que representa los cuaterniones. Al combinarlo con la detección del clic izquierdo del mouse que hemos hecho anteriormente, podemos lograr el control de rotación izquierda y derecha de la cámara.

El código para controlar el movimiento de la cámara hacia la izquierda y hacia la derecha con el movimiento del ratón se puede proporcionar directamente:

```c#
newForward = MyRotate(newForward, x, up, Vector3.zero);
```
Debido a que aquí solo hay una rotación en el vector frontal y no hay una conversión de sistema de coordenadas, el cuarto parámetro es `Vector3.zero`.

Controlar la rotación vertical o la rotación horizontal puede resultar un poco más difícil de entender en comparación con la rotación izquierda o derecha, ya que en este caso el eje de rotación está en constante cambio (supongamos que la dirección "up" del personaje siempre es el eje Y positivo). También hay que tener en cuenta que la cámara está en constante rotación y siempre apunta hacia el centro del personaje, por lo que la dirección derecha (right) de la cámara sería el eje de rotación que deseamos usar (pensándolo como la dirección derecha del personaje). Con esta comprensión, el código para la rotación vertical o la rotación horizontal también resulta sencillo.

```csharp
newForward = MyRotate(newForward, -y, transform.right, Vector3.zero);
```

###Haz clic derecho y gira ###
Habiendo realizado la rotación con el botón izquierdo, la rotación con el botón derecho se vuelve muy sencilla, simplemente se necesita establecer la dirección frontal del personaje al rotar hacia la izquierda o hacia la derecha:

```csharp
player.forward = Vector3.Normalize(new Vector3(oldForward.x, 0, oldForward.z));
```

El código de rotación hacia arriba y hacia abajo es el mismo que el del botón izquierdo.

###Primero haz clic izquierdo, luego haz clic derecho.
Aunque se puede rotar utilizando el clic izquierdo o el clic derecho por separado, hay un problema cuando se utiliza primero el clic izquierdo y luego se utiliza el control con el clic derecho: ¡La dirección frontal del personaje y la dirección frontal de la cámara se vuelven diferentes! Esto hace que la cámara y la dirección frontal del personaje se separen, lo cual es bastante extraño al operar. Por lo tanto, al girar con el clic derecho, debemos ajustar previamente al personaje para que esté alineado con la dirección frontal de la cámara.

```csharp
player.forward = Vector3.Normalize(new Vector3(oldForward.x, 0, oldForward.z));

```

- - - 

###欧拉角万向锁
Hasta aquí, la rotación de la cámara está casi completa, aunque todavía hay un problema a tener en cuenta: el bloqueo de Euler. No voy a entrar en detalles sobre el principio aquí, aquellos interesados pueden buscar por sí mismos. En lo que respecta a la situación de la cámara aquí, cuando la cámara rota hacia arriba y se superpone con la dirección hacia arriba del personaje, el ángulo de visión de la cámara sufre un cambio brusco. Esto se debe a que cuando la cámara llega a la parte superior o inferior de la cabeza del personaje, la dirección hacia arriba de la cámara experimenta un cambio brusco (porque el valor Y de la dirección hacia arriba de la cámara siempre debe ser mayor que cero), por lo que necesitamos limitar el rango de rotación hacia arriba y hacia abajo de la cámara para evitar el bloqueo de Euler. La operación es muy sencilla, simplemente debemos limitar el ángulo entre la dirección frontal de la cámara y la dirección hacia arriba del personaje dentro de un cierto rango:

```c#
if ((Vector3.Dot(transform.forward, transform.parent.up) >= -0.95F || y > 0) &&
    (Vector3.Dot(transform.forward, transform.parent.up) <= 0.95F || y < 0))
```

###完整代码###

Traducir estos textos al idioma español:

完整代码###

```csharp
// rotate oldPosition around a axis starting at axisPosition
Vector3 MyRotate(Vector3 oldPosition, float angle, Vector3 axis, Vector3 axisPosition)
{
    Quaternion rotation = Quaternion.AngleAxis(angle, axis);
    Vector3 offset = oldPosition - axisPosition;
    return axisPosition + (rotation * offset);
}

// rotate oldForward, player forward may change when use mouse RB
Vector3 RotateIt(Vector3 oldForward, Vector3 up, Vector3 right, Transform player)
{
    Vector3 newForward = -oldForward;
    // mouse LB RB rotate camera and character
    if (Input.GetMouseButton(0) ^ Input.GetMouseButton(1))
    {
        float x = Input.GetAxis("Mouse X") * rotateSpeed;
        float y = Input.GetAxis("Mouse Y") * rotateSpeed;

        if (x != 0F)
        {
            newForward = MyRotate(newForward, x, up, Vector3.zero);

            // mouse RB, character rotate together
            if (Input.GetMouseButton(1))
            {
                player.forward = Vector3.Normalize(new Vector3(oldForward.x, 0, 
                    oldForward.z));
            }
        }

        if (y != 0F)
        {

            if ((Vector3.Dot(transform.forward, up) >= -0.95F || y > 0)
                && (Vector3.Dot(transform.forward, up) <= 0.95F || y < 0))
            {
                newForward = MyRotate(newForward, -y, transform.right, Vector3.zero);

            }
        }
    }

    return -newForward;
}
```

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
