---
layout: post
title: Construcción de la cámara en tercera persona en Unity (Parte 2)
categories:
- unity
catalog: true
tags:
- dev
description: Quiero crear una cámara en tercera persona en Unity, y su comportamiento
  se basará en la cámara en tercera persona de "World of Warcraft". Aquí se aborda
  el problema del cuerpo rígido de la cámara.
---

<meta property="og:title" content="Unity第三人称相机构建(下)" />

La última entrega terminó de hablar sobre [la rotación de la cámara](unity-Unity第三人称相机构建(上).md), entonces ahora el problema que debemos resolver es la rigidez de la cámara, ¿cómo podemos hacerlo?

La traducción al español de "相机刚性" es "rigidez de la cámara".
--------------
Repasando las necesidades mencionadas anteriormente:

4. Rueda de desplazamiento del mouse: controla la distancia de la cámara.
5. La cámara no puede atravesar ningún objeto rígido.
6. La cámara se aleja lentamente del objeto rígido con el que chocó, volviendo gradualmente a la distancia original.
7. Si la cámara se encuentra con un objeto sólido y se utiliza la rueda del ratón para acercar la cámara, esta debe responder de inmediato y después no ocurrirá el punto 6. No se puede realizar ninguna operación de zoom después de chocar con el suelo.
8. La cámara choca con el suelo mientras gira, deteniendo su giro alrededor del personaje de arriba hacia abajo, cambiando para girar alrededor de sí misma de arriba hacia abajo, mientras que el giro de izquierda a derecha todavía será alrededor del personaje.


Estos puntos significan: cuando la cámara toca un objeto rígido, se verá obligada a acercarse a la distancia del personaje. Entonces, si deseamos que la cámara pueda regresar gradualmente a su distancia original al alejarse, pero si después de acercarse automáticamente, utilizamos la rueda de desplazamiento para acercar manualmente, esto indica que la cámara se aleja del objeto de colisión y esa distancia de acercamiento es la distancia real de la cámara. Ahora analicemos estas necesidades paso a paso.

滚轮控制
----------
El control del scroll del mouse es bastante sencillo, solo necesitas saber que para obtener la información del scroll se utiliza `Input.GetAxis("Mouse ScrollWheel")`, y luego establecer los valores máximos y mínimos de distancia. ¡Y listo!

```c#
public float mouseWheelSensitivity = 2; // control zoom speed
public int mouseWheelZoomMin = 2;       // min distance
public int mouseWheelZoomMax = 10;      // max distance
float curDistance = 5F;
float zoom = Input.GetAxis("Mouse ScrollWheel");
if (zoom != 0F)
{
    float distance = curDistance;
    distance -= zoom * mouseWheelSensitivity;
    distance = Math.Min(mouseWheelZoomMax, Math.Max(mouseWheelZoomMin, distance));
    return distance;
}
```

Aquí `playerTransform` apunta al personaje.

**No puedes atravesar ningún objeto rígido**.
--------------------
Esta función es útil para detectar el contacto entre la cámara y el cuerpo rígido:

```c#
static bool Raycast(Ray ray, RaycastHit hitInfo, float distance = Mathf.Infinity, int layerMask = DefaultRaycastLayers);
```

具体用法参考Unity的[Reference]

Please refer to the [Reference](http://docs.unity3d.com/Documentation/ScriptReference/Physics.Raycast.html)，podemos lograr la detección de colisiones de la siguiente manera:

```c#
RaycastHit hitInfo;
if (Physics.Raycast(playerTransform.position, desiredPosition - playerTransform.position,
    out hitInfo, (playerTransform.position - desiredPosition).magnitude, 1))
{
    curDistance = hitInfo.distance;
}
```

`targetPosition` es la posición de la colisión, simplemente debes ajustar la posición de la cámara a la posición de la colisión.

Después de separarse del cuerpo rígido, regrese lentamente a la distancia original.
---------------------------------
Para lograr esta funcionalidad, primero necesitamos registrar la distancia a la que la cámara debería estar (`desiredDistance`) y la distancia actual (`curDistance`). Guardaremos el resultado de la operación de la rueda en la variable `desiredDistance` y luego calcularemos la nueva distancia del objeto en base a las colisiones.
Cuando se detecta que la cámara se aleja del objeto o colisiona con otro objeto más lejano, no se puede asignar directamente la posición de la colisión a la cámara, se necesita utilizar una velocidad de movimiento para desplazarse hacia la nueva distancia. Primero, obtengamos la nueva distancia:

```c#
float newDistance = desiredDistance;
RaycastHit hitInfo;
if (Physics.Raycast(playerTransform.position, desiredPosition - playerTransform.position,
    out hitInfo, (playerTransform.position - desiredPosition).magnitude, 1))
{
    newDistance = hitInfo.distance;
}
```

Entonces, ¿cómo se puede determinar si la cámara se está moviendo hacia una distancia mayor? Puede compararse con `newDistances` y la distancia actual:

```c#
// Moverse hacia distancias más cortas
if (newDistance < curDistance)
{
    curDistance = newDistance;
}
// Moverse hacia distancias más lejanas
else if(newDistance > curDistance)
{
}
```

En ese caso, una vez que se ha determinado que se requiere moverse a una distancia mayor, la solución es bastante sencilla: simplemente se aumenta la velocidad para moverse.

```c#
curDistance = Math.Min(curDistance + Time.deltaTime * autoZoomOutSpeed, newDistance);

```
**相机的大致行为我们已经完成了，还有一些细节需要处理。**

La funcionalidad general de la cámara ya la hemos completado, pero aún queda por resolver algunos detalles.

Después de chocar con un objeto sólido, la rueda se acercará y el suelo no se escalará.
------------------
Aquí hay dos requisitos:

1. Después de chocar con un objeto sólido, solo puedes acercarte, no alejarte.
2. Después de que toque el suelo no puede hacer zoom.

Primero, se utiliza una variable para guardar el estado de colisión de la cámara:

```c#
bool isHitGround = false;       // Indica si ha tocado el suelo
bool isHitObject = false;       // Indicates whether it collided with a rigid body (excluding the ground)
```

En el momento de evaluar el escalado de la rueda de desplazamiento, agregue una condición de evaluación:

```c#
if (zoom != 0F && (!isHitGround || (isHitObject && zoom > 0F)) )
{
    // calculate distance
}
```

Al entrar en contacto con el suelo, girar alrededor de uno mismo en un movimiento ascendente y descendente.
-----------------
Este proceso puede resultar un poco complicado de implementar, ya que nuestra suposición anterior de que la cámara siempre está apuntando al personaje ya no es válida en este caso. Ahora tenemos que dividirlo en dos vectores: **la orientación de la cámara en sí (`desireForward`)** y **la dirección desde el personaje hacia la cámara (`cameraToPlayer`)**. Debemos calcular los valores de estos dos vectores por separado, donde el primero determinará la orientación de la cámara y el segundo determinará su posición. Para mayor comodidad, vamos a referirnos al [episodio anterior](unity-Unity第三人称相机构建(上)Si se divide la función de rotación de .md) en rotación X (`RotateX`) y rotación Y (`RotateY`), entonces al calcular `cameraToPlayer` para `RotateY`, se agrega una condición:

```c#
if ((!isHitGround) || 
    (isHitGround && transform.forward.y <= cameraToPlayer.y && yAngle > 0))
{
    cameraToPlayer = RotateY(cameraToPlayer, playerTransform.up, 
        transform.right, yAngle);
}
```

Este requisito tiene dos partes:

- No ha tocado el suelo.
- Mala noticia, me encontré con el suelo pero estoy listo para levantarme del suelo.

Luego, usa `cameraToPlayer` para calcular la posición de la cámara:

```c#
transform.position = playerTransform.position - cameraToPlayer * curDistance;
```

Y cuando sea necesario (es decir, cuando se encuentre en el suelo), calcular la dirección de la cámara:

```c#
if (!isHitGround)
{
    transform.LookAt(playerTransform);
}
else
{
    desireForward = RotateX(desireForward, playerTransform.up, xAngle);
    desireForward = RotateY(desireForward, playerTransform.up, transform.right, yAngle);
    transform.forward = desireForward;
}
```

Así es como logramos implementar el comportamiento de la cámara.

def greet(name):
    """ This function takes a name as input and prints a greeting message """
    if name.lower() == 'alice':
        print('Hello, Alice!')
    elif name.lower() == 'bob':
        print('Hello, Bob!')
    else:
        print('Hello, stranger!')

# Test the function
greet('Alice')
greet('Bob')
greet('Charlie')

Traducción:
def saludar(nombre):
    """ Esta función recibe un nombre como entrada y muestra un mensaje de saludo """
    if nombre.lower() == 'alice':
        print('¡Hola, Alice!')
    elif nombre.lower() == 'bob':
        print('¡Hola, Bob!')
    else:
        print('¡Hola, desconocido!')

# Probar la función
saludar('Alice')
saludar('Bob')
saludar('Charlie')

```c#
using UnityEngine;
using System;
using System.Collections;

// use a forward vector and distance to describe the camera position
public class MyThirdPersonCamera : MonoBehaviour {

    private Transform playerTransform;      // reference to player

    public float mouseWheelSensitivity = 3; // control zoom speed
    public int mouseWheelZoomMin = 2;       // min distance
    public int mouseWheelZoomMax = 10;      // max distance

    public float rotateSpeed = 5F;          // speed of rotate around player    
    public float autoZoomOutSpeed = 10F;    // speed of auto zoom out, camera will auto zoom out 
                                            // to pre distance when stop colliding object
    float curDistance = 5F;                 // distance to player
    float desiredDistance = 5F;             // distance should be      
    bool isHitGround = false;               // hit ground flag
    bool isHitObject = false;               // hit object(except ground) flag
    
    // Use this for initialization
    void Awake ()
    {
        playerTransform = transform.parent;
    }

    void Start () 
    {
        transform.position = playerTransform.position - playerTransform.forward 
            * curDistance;
        transform.LookAt(playerTransform);
        
    }
    
    // Update is called once per frame
    void Update () 
    {
        Vector3 cameraToPlayer = 
            (playerTransform.position - transform.position).normalized;

        Vector3 desireForward = transform.forward;

        // get new distance of zoom
        desiredDistance = ZoomIt(curDistance, desiredDistance);

        float xAngle, yAngle;
        bool isRightDown;

        // get mouse LB, RB status
        GetMouseButtonStatus(out xAngle, out yAngle, out isRightDown);

        // rotate camera by x-axis movement
        cameraToPlayer = RotateX(cameraToPlayer, playerTransform.up, xAngle);

        // if RB on, change player orientation
        if (isRightDown)
        {
            playerTransform.forward = Vector3.Normalize(new Vector3(cameraToPlayer.
                x, 0, cameraToPlayer.z));
        }

        // rotate camera by y-axis, if camera is not on ground or camera is going to leave ground
        if ((!isHitGround) 
        || (isHitGround && transform.forward.y <= cameraToPlayer.y && yAngle > 0))
        {
            cameraToPlayer = RotateY(cameraToPlayer, playerTransform.up, transform.
                right, yAngle);
        }

        // detect collision of camera to rigid body, get the distance camera should be
        float newDistance = DealWithCollision(playerTransform.position, 
            -cameraToPlayer, desiredDistance,ref isHitGround, ref isHitObject);

        // check the distance
        if (newDistance <= curDistance)
        {
            curDistance = newDistance;
        }
        else
        {
            // now moving to farther position, use a speed to move it
            curDistance = Math.Min(curDistance + Time.deltaTime * autoZoomOutSpeed, 
                newDistance);
        }

        // now calculate the position
        transform.position = playerTransform.position - cameraToPlayer * curDistance;

        // calculate the camera forward, if on ground, camera will rotate on self.Space
        if (!isHitGround)
        {
            transform.LookAt(playerTransform);
        }
        else
        {
            desireForward = RotateX(desireForward, playerTransform.up, xAngle);
            desireForward = RotateY(desireForward, playerTransform.up, transform.
                right, yAngle);
            transform.forward = desireForward;
        }
    }

    // zoom in and zoom out
    float ZoomIt(float curDistance, float desiredDistance)
    {
        float zoom = Input.GetAxis("Mouse ScrollWheel");

        //  zoom when hit rigid body and zoom in, or not on ground
        if (zoom != 0F && (!isHitGround || (isHitObject && zoom > 0F)) )
        {
            float distance = curDistance;

            distance -= zoom * mouseWheelSensitivity;
            distance = Math.Min(mouseWheelZoomMax, Math.Max(mouseWheelZoomMin, distance));

            return distance;
        }
        return desiredDistance;
    }

    // rotate oldPosition around a axis starting at axisPosition
    Vector3 RotateAroundAxis(Vector3 point, float angle, Vector3 axis, Vector3 axisPosition)
    {
        Quaternion rotation = Quaternion.AngleAxis(angle, axis);
        Vector3 offset = point - axisPosition;
        return axisPosition + (rotation * offset);
    }

    void GetMouseButtonStatus(out float x, out float y, out bool isRightDown)
    {
        x = y = 0F;
        isRightDown = false;
        if (Input.GetMouseButton(0) ^ Input.GetMouseButton(1))
        {
            x = Input.GetAxis("Mouse X") * rotateSpeed;
            y = -Input.GetAxis("Mouse Y") * rotateSpeed;
            if (Input.GetMouseButton(1))
            {
                isRightDown = true;
            }
        }
    }

    // rotate vectorP2C(player to camera) around up while mouse x is on, return true if do rotate
    Vector3 RotateX(Vector3 vectorP2C, Vector3 up, float angle)
    {
        Vector3 newVector = vectorP2C;
        if (angle != 0F)
        {
            newVector = RotateAroundAxis(newVector, angle, up, Vector3.zero);
        }
        return newVector;
    }

    // rotate vectorP2C(player to camera) around right while mouse y is on, return true is do rotate
    Vector3 RotateY(Vector3 vectorP2C, Vector3 up, Vector3 right, float angle)
    {
        Vector3 newVector = vectorP2C;
        if (angle != 0F)
        {
            if ((Vector3.Dot(vectorP2C, up) >= -0.99F || angle < 0)
                && (Vector3.Dot(vectorP2C, up) <= 0.99F || angle > 0))
            {
                newVector = RotateAroundAxis(newVector, angle, right, Vector3.zero);
            }
        }
        return newVector;
    }

    // return distance if no collision, else return distance to rigid body
    float DealWithCollision(Vector3 origin, Vector3 direction, float distance, 
        ref bool ishitGround, ref bool ishitObject)
    {
        // collision detection
        RaycastHit hitInfo;
        float newDistance = distance;
        if (Physics.Raycast(playerTransform.position, direction, out hitInfo, desiredDistance, 1))
        {
            if (hitInfo.collider is TerrainCollider)
            {
                ishitGround = true;
                ishitObject = false;
            }
            else
            {
                ishitObject = true;
                ishitGround = false;
            }
            newDistance = hitInfo.distance;
        }
        else
        {
            ishitGround = ishitObject = false;
        }

        return newDistance;
    }
}
```

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
