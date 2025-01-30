---
layout: post
title: Construcción de un sistema de cámara en tercera persona en Unity (Parte 1)
categories:
- unity
catalog: true
tags:
- dev
description: Quiero crear una cámara en tercera persona en Unity, cuyo comportamiento
  se base en la cámara en tercera persona de "World of Warcraft". Primero, abordaremos
  el problema de la rotación de la cámara.
figure: null
---

<meta property="og:title" content="Unity第三人称相机构建(上)" />

Me gustaría crear una cámara en tercera persona en Unity, con un comportamiento similar a la cámara en tercera persona de "World of Warcraft". Las especificaciones son:

1. Clic izquierdo del ratón: controla la cámara que gira alrededor del personaje, sin rotar el personaje.
Haz clic derecho en el mouse: esto te permite rotar la cámara alrededor del personaje, lo que hará que la dirección frontal del personaje (transform.forward en Unity) gire en consecuencia mientras que la dirección hacia arriba del personaje permanece constante.
3. Después de rotar con el botón izquierdo del ratón, si se rota nuevamente con el botón derecho, la dirección frente al personaje se ajustará inmediatamente de acuerdo con la rotación del botón izquierdo y luego según la rotación del botón derecho; en este momento, es equivalente a realizar dos rotaciones con el botón derecho.
4. Rueda del mouse: controla la distancia de la cámara.
5. La cámara no puede atravesar ningún objeto rígido.
6. La cámara regresa lentamente a la distancia original después de alejarse del objeto rígido con el que colisionó.
7. Si la cámara se encuentra con un objeto, al usar la rueda del ratón para acercar la cámara, esta debe reaccionar de inmediato; a partir de ahí, el punto 6 ya no ocurrirá.
8. La cámara toca el suelo mientras rota, deteniéndose en la rotación vertical alrededor de la persona, cambiando a una rotación vertical alrededor de sí misma, mientras que la rotación horizontal sigue siendo alrededor de la persona.



Esta demanda se puede dividir en dos partes: rotación de la cámara y rigidez de la cámara. Para simplificar, aquí abordaremos primero el problema de la rotación de la cámara, es decir, los primeros tres puntos de la demanda.

Indicador de posición de la cámara
----------------
Antes de abordar formalmente la operación de la cámara, hay un tema pendiente: la representación de la posición de la cámara. Esto se puede lograr de varias formas:

- Coordenadas del mundo de la cámara
- Coordenadas de la cámara en relación con la persona
La dirección y la distancia de la cámara en el sistema de coordenadas de la persona.

Debido a que en nuestras necesidades, la cámara cambia según la posición del personaje, aquí he optado por el tercer método, y además, la cámara se mantiene apuntando constantemente al personaje en el control, por lo tanto, solo necesitamos guardar información de la distancia dentro de la cámara:

```c#
float curDistance = 5F;
```

Giro de la cámara
-------------
Siguiendo con el análisis del comportamiento de rotación de la cámara, podemos dividirlo en rotación con el botón izquierdo y rotación con el botón derecho. A continuación, iremos completando estos dos tipos de rotación paso a paso. Primero, estableceré la cámara como un objeto hijo del personaje, de esta manera, algunos de los movimientos básicos del personaje serán automáticamente seguidos por la cámara.

###Girar con el botón izquierdo###
Solo mirando la rotación del botón izquierdo, la necesidad es muy simple: **la cámara rota, la persona no rota**, esto equivale a una cámara que observa el modelo, la cámara puede observar el objeto central desde cualquier ángulo.

En Unity, para obtener el estado del botón izquierdo del mouse se utiliza la instrucción: `Input.GetMouseButton(0)` (Nota: en las secciones que involucren código, se está utilizando C#). De manera similar, el botón derecho es `Input.GetMouseButton(1)`. La información sobre la posición del cursor del mouse (que se puede entender como el desplazamiento en X-Y del cursor entre fotogramas) es: `Input.GetAxis("Mouse X"); Input.GetAxis("Mouse Y")`. Así que primero podemos obtener la información del movimiento del cursor después de presionar el botón izquierdo del mouse:

```csharp
if (Input.GetMouseButton(0))
{
    float x = Input.GetAxis("Mouse X");
    float y = Input.GetAxis("Mouse Y");
}
```
 
La parte clave aquí es cómo controlar la rotación de la cámara. Para entender este concepto, es necesario tener conocimientos sobre cuaterniones (hay mucha información en línea al respecto que no detallaré aquí). Uno de los aspectos más importantes de los cuaterniones es su capacidad para construir rotaciones de manera sencilla, especialmente en torno a un vector dado. Una vez se comprenden los cuaterniones, no resulta difícil implementar la rotación de la cámara alrededor de un personaje.

Además, hay un punto más a tener en cuenta: el eje de rotación del cuaternión es solo un vector que parte del origen. Si queremos utilizar un punto `O` del sistema de coordenadas del mundo como origen, y tomar el vector `V` que parte de ese punto como eje de rotación, será necesario realizar una transformación del sistema de coordenadas. En términos simples, esto implica trasladar el punto `P` que necesita rotar al sistema de coordenadas con `O` como origen, rotarlo según `V` y luego transformarlo de nuevo al sistema de coordenadas del mundo. Con base en estas operaciones, se puede escribir una función funcional:

```c#
Vector3 MyRotate(Vector3 oldPosition, float angle, Vector3 axis, Vector3 axisPosition)
{
Crear un cuaternión con el eje como eje de rotación. Esto se refiere a la rotación en el sistema de coordenadas del personaje.
    Quaternion rotation = Quaternion.AngleAxis(angle, axis);
// Aquí lo que se hace es la transformación del sistema de coordenadas, convirtiendo las coordenadas del mundo de la cámara a las coordenadas del sistema del personaje.
    Vector3 offset = oldPosition - axisPosition;
Calcular la rotación y transformar de vuelta al sistema de coordenadas del mundo.
    return axisPosition + (rotation * offset);
}
```
`Quaternion` es el tipo en Unity que representa cuaterniones. Combinado con la detección previa del clic izquierdo del ratón, se puede lograr el control de la rotación izquierda y derecha de la cámara mediante el clic izquierdo.

El código para controlar la rotación izquierda y derecha de la cámara al mover el ratón hacia la izquierda y hacia la derecha se puede proporcionar directamente:

```c#
newForward = MyRotate(newForward, x, up, Vector3.zero);
```
Porque aquí solo se realiza la rotación del vector de dirección, sin involucrar la transformación de coordenadas, por lo que el cuarto parámetro es `Vector3.zero`.

Controlar la rotación vertical es un poco más difícil de entender que la horizontal, ya que en este caso el eje de rotación está en constante cambio (aquí suponemos que la dirección hacia arriba del personaje siempre es el eje Y positivo). Ten en cuenta que la cámara también está girando constantemente y que el centro de la vista siempre sigue al personaje, por lo que la dirección derecha (right) de la cámara es el eje alrededor del cual queremos rotar (piensa en el right de la cámara como el right del personaje). Con esta comprensión, el código para la rotación vertical también es muy sencillo:

```csharp
newForward = MyRotate(newForward, -y, transform.right, Vector3.zero);
```

###Por favor, gira hacia la derecha.
Hice una rotación con el botón izquierdo, y la rotación con el botón derecho es muy sencilla; solo necesito establecer la dirección del personaje al rotar hacia la izquierda o hacia la derecha.

```csharp
player.forward = Vector3.Normalize(new Vector3(oldForward.x, 0, oldForward.z));
```

La codificación para la rotación arriba y abajo es la misma que para la tecla izquierda.

###Haga clic con el botón izquierdo primero, luego con el botón derecho###
Aunque se puede rotar con el botón izquierdo y con el botón derecho por separado, surge un problema cuando primero se rota con el botón izquierdo y luego se usa el derecho: ¡la dirección del personaje y la dirección de la cámara son diferentes! Así, la dirección del personaje y la de la cámara quedan separadas, lo que resulta extraño al operar. Por lo tanto, cuando usamos el botón derecho para rotar, debemos primero ajustar al personaje para que esté alineado con la dirección de la cámara.

```csharp
player.forward = Vector3.Normalize(new Vector3(oldForward.x, 0, oldForward.z));

```

- - - 

###Bloqueo de gimbal de ángulos de Euler###
Hasta aquí, la rotación de la cámara casi está completa, pero hay un problema a tener en cuenta: el bloqueo de los ángulos de Euler. No voy a entrar en detalles sobre el principio aquí, aquellos interesados pueden buscar por sí mismos. Para la situación de la cámara aquí, cuando la cámara rota hacia arriba hasta coincidir con la dirección hacia arriba de un personaje, el ángulo de visión de la cámara cambiará bruscamente. Esto se debe a que al llegar la cámara a la parte superior o inferior de la cabeza del personaje, el ángulo hacia arriba de la cámara cambiará (ya que el valor Y del ángulo hacia arriba de la cámara siempre debe ser mayor que cero), por lo que necesitamos restringir el rango de rotación hacia arriba y abajo de la cámara para evitar el bloqueo de los ángulos de Euler. La operación es muy sencilla, simplemente limitar el rango del ángulo entre la dirección frontal de la cámara y la dirección hacia arriba del personaje.

```c#
if ((Vector3.Dot(transform.forward, transform.parent.up) >= -0.95F || y > 0) &&
    (Vector3.Dot(transform.forward, transform.parent.up) <= 0.95F || y < 0))
```

###Código completo###

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

--8<-- "footer_es.md"


> Este mensaje fue traducido usando ChatGPT, por favor [**反馈**](https://github.com/disenone/wiki_blog/issues/new)Indica cualquier omisión. 
