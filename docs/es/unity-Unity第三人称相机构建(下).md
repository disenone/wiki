---
layout: post
title: Construir cámara en tercera persona Unity (parte 3)
categories:
- unity
catalog: true
tags:
- dev
description: Quiero crear una cámara en tercera persona en Unity, tomando como referencia
  la cámara en tercera persona de "World of Warcraft". Aquí se abordará el problema
  del cuerpo rígido de la cámara.
---

<meta property="og:title" content="Unity第三人称相机构建(下)" />

La última entrega terminó con [la rotación de la cámara](unity-Unity第三人称相机构建(上).md)，entonces ahora el problema que tenemos que resolver es la rigidez de la cámara, ¿cómo lo hacemos?

Rigidez de la cámara
--------------
Revisando los requisitos mencionados anteriormente:

4. Rueda del ratón: controla el acercamiento y alejamiento de la cámara.
5. La cámara no puede atravesar ningún objeto rígido.
La cámara se aleja lentamente del objeto rígido con el que chocó, volviendo a su distancia original.
7. Si la cámara se encuentra con un objeto sólido, al usar la rueda del ratón para acercar la cámara, esta debe reaccionar de inmediato; después de eso, el punto 6 ya no aplica; no se puede realizar la operación de zoom después de colisionar con el suelo.
La cámara golpea el suelo mientras gira, deteniendo el giro alrededor del personaje, y comienza a girar alrededor de sí misma verticalmente, manteniendo el giro horizontal alrededor del personaje.


Estos puntos significan que cuando la cámara se acerca a un objeto rígido, se ve obligada a acercarse al sujeto. Por lo tanto, queremos que la cámara regrese lentamente a su distancia original al alejarse. Sin embargo, si después de acercarse automáticamente, se vuelve a acercar manualmente con la rueda, significa que la cámara se está alejando del objeto con el que colisionó, por lo que esa distancia de acercamiento es la distancia real de la cámara. Ahora vamos a abordar poco a poco estas necesidades.

Control del rodillo
----------
El control de la rueda de desplazamiento del mouse es bastante sencillo, solo necesitas saber que para obtener la información de la rueda de desplazamiento se usa `Input.GetAxis("Mouse ScrollWheel")`, y luego simplemente establecer los valores máximo y mínimo de la distancia. ¡Listo!

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

Aquí, `playerTransform` apunta al personaje.

No se puede atravesar ningún objeto rígido.
--------------------
Se requiere detectar el contacto entre la cámara y el cuerpo rígido, hay una función que puede llevar a cabo esta función:

```c#
static bool Raycast(Ray ray, RaycastHit hitInfo, float distance = Mathf.Infinity, int layerMask = DefaultRaycastLayers);
```

Consulta la [Referencia](http://docs.unity3d.com/Documentation/ScriptReference/Physics.Raycast.html)Podemos implementar la detección de colisiones de esta manera:

```c#
RaycastHit hitInfo;
if (Physics.Raycast(playerTransform.position, desiredPosition - playerTransform.position,
    out hitInfo, (playerTransform.position - desiredPosition).magnitude, 1))
{
    curDistance = hitInfo.distance;
}
```

`targetPosition` es la posición del choque, simplemente coloca la posición de la cámara en la posición del choque.

离开刚体后，慢慢回到原来的距离上。 

Translation: 

Después de alejarse del cuerpo rígido, regresa lentamente a la distancia original.
---------------------------------
Para llevar a cabo esta función, primero se deben registrar por separado la distancia a la que la cámara debería estar (`desiredDistance`) y la distancia actual (`curDistance`). Luego, se guarda el resultado de la operación de la rueda en `desiredDistance` y se calcula la nueva distancia del objeto según la colisión.
Al detectar que la cámara se aleja de un objeto rígido o choca con otro objeto rígido más distante, no se puede asignar directamente la posición de la colisión a la cámara; se necesita utilizar una velocidad de movimiento para trasladarse a una nueva distancia. Primero, se debe obtener la nueva distancia:

```c#
float newDistance = desiredDistance;
RaycastHit hitInfo;
if (Physics.Raycast(playerTransform.position, desiredPosition - playerTransform.position,
    out hitInfo, (playerTransform.position - desiredPosition).magnitude, 1))
{
    newDistance = hitInfo.distance;
}
```

Entonces, ¿cómo se puede determinar si la cámara se está moviendo hacia una distancia mayor? Puedes comparar `newDistances` con la distancia actual:

```c#
// Moverse a una distancia más cercana
if (newDistance < curDistance)
{
    curDistance = newDistance;
}
// Moverse a distancias más lejanas
else if(newDistance > curDistance)
{
}
```

Entonces, al determinar que se mueve a una distancia mayor, es bastante intuitivo, simplemente se le añade una velocidad para moverse:

```c#
curDistance = Math.Min(curDistance + Time.deltaTime * autoZoomOutSpeed, newDistance);

```
Hemos completado la funcionalidad básica de la cámara, ahora queda por resolver algunos detalles.

Al encontrarse con un cuerpo rígido, la rueda trasera se acerca, el suelo no se escala.
------------------
Aquí hay dos requisitos:

Al chocar con un cuerpo rígido, solo se puede acercar, no alejar.
Después de tocar el suelo, no se puede hacer zoom.

Primero, utiliza variables para guardar el estado de colisión de la cámara:

```c#
bool isHitGround = false;       // Indicates whether it has hit the ground
bool isHitObject = false;       // Indica si hay colisión con un cuerpo rígido (excluyendo el suelo)
```

Al juzgar el zoom con la rueda, agrega una condición de evaluación:

```c#
if (zoom != 0F && (!isHitGround || (isHitObject && zoom > 0F)) )
{
    // calculate distance
}
```

Encontrarse con el suelo y girar alrededor de sí mismo de arriba a abajo.
-----------------
Esta función resulta un poco complicada de implementar, ya que en este momento nuestra suposición de que la cámara siempre apunta hacia el personaje ya no se mantiene. En este caso, se dividen en dos vectores: **la dirección propia de la cámara (`desireForward`)** y **la dirección del personaje hacia la cámara (`cameraToPlayer`)**, calculando respectivamente el valor de estos dos vectores. El primero determina la orientación de la cámara, mientras que el segundo determina la posición de la cámara. Para facilitar, tomemos [el episodio anterior](unity-Unity第三人称相机构建(上)Dividir la función de rotación de .md en rotación X (`RotateX`) y rotación Y (`RotateY`), y luego al calcular el `RotateY` de `cameraToPlayer`, agregar la siguiente condición:

```c#
if ((!isHitGround) || 
    (isHitGround && transform.forward.y <= cameraToPlayer.y && yAngle > 0))
{
    cameraToPlayer = RotateY(cameraToPlayer, playerTransform.up, 
        transform.right, yAngle);
}
```

Esta condición tiene dos partes:

- No ha tocado el suelo.
- Tocando el suelo, pero listo para despegar.

Luego, se utiliza `cameraToPlayer` para calcular la posición de la cámara:

```c#
transform.position = playerTransform.position - cameraToPlayer * curDistance;
```

Y además, calcula la orientación de la cámara cuando sea necesario (es decir, al tocar el suelo):

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

De esta manera, hemos conseguido el comportamiento de la cámara.

Código completo:

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

--8<-- "footer_es.md"


> Este post fue traducido utilizando ChatGPT, por favor en [**retroalimentación**](https://github.com/disenone/wiki_blog/issues/new)Señale cualquier omisión. 
