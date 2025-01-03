---
layout: post
title: Unity Third-Person Camera Setup (Continued)
categories:
- unity
catalog: true
tags:
- dev
description: Ich möchte in Unity eine Third-Person-Kamera erstellen, die sich an der
  Third-Person-Kamera von "World of Warcraft" orientiert. Hier geht es darum, das
  Problem des Kamerarigidkörpers zu lösen.
---

<meta property="og:title" content="Unity第三人称相机构建(下)" />

Die vorherige Folge handelte von [der Drehung der Kamera](unity-Unity第三人称相机构建(上).md)，jetzt müssen wir das Problem der Kamerastabilität lösen, wie gehen wir vor?

Kameragehäusefestigkeit
--------------
Überprüfen wir die zuvor genannten Anforderungen:

Mausrolle: Steuerung der Kamerazoom.
Die Kamera kann nicht durch jedes starre Objekt hindurchsehen.
Die Kamera kehrt langsam zu ihrer ursprünglichen Entfernung zurück, nachdem sie das starre Objekt verlassen hat.
Wenn die Kamera auf ein starres Objekt trifft, sollte die Kamera sofort reagieren, wenn man das Mausrad benutzt, um heranzuzoomen. Danach sollte Punkt 6 nicht mehr auftreten. Nachdem die Kamera auf den Boden gestoßen ist, kann nicht mehr gezoomt werden.
Die Kamera hat den Boden berührt, als sie sich drehte, und hat aufgehört, um die Person herum zu rotieren. Stattdessen rotiert sie jetzt um sich selbst, während die seitliche Rotation immer noch um die Person erfolgt.


Diese Punkte bedeuten: Wenn die Kamera auf ein starres Objekt trifft, wird sie gezwungen, sich dem Motiv zu nähern. Wenn wir wollen, dass die Kamera sich beim Entfernen allmählich wieder in die ursprüngliche Position zurückbewegt, aber wenn sie sich nach dem automatischen Näherkommen manuell mit dem Mausrad weiter annähert, bedeutet das, dass die Kamera das kollidierte Objekt verlässt und der Abstand, um den sie näher kommt, ist dann der tatsächliche Abstand der Kamera. Jetzt werden wir Schritt für Schritt diese Anforderungen klären.

Scrollsteuerung
----------
Die Steuerung des Mausrads ist ganz einfach. Du musst nur wissen, dass du die Mausradinformationen mit `Input.GetAxis("Mouse ScrollWheel")` abrufen kannst. Lege einfach die maximalen und minimalen Werte für die Entfernung fest, und schon bist du startklar:

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

Hier zeigt `playerTransform` auf den Charakter.

Kann nicht durch jedes starre Objekt hindurchgehen.
--------------------
Dies erfordert die Überprüfung des Kontakts zwischen der Kamera und dem starren Körper. Es gibt eine Funktion, die diese Funktionalität ermöglichen kann:

```c#
static bool Raycast(Ray ray, RaycastHit hitInfo, float distance = Mathf.Infinity, int layerMask = DefaultRaycastLayers);
```

Bitte beachten Sie die spezifische Verwendung im [Referenz](http://docs.unity3d.com/Documentation/ScriptReference/Physics.Raycast.html)Wir können die Kollisionserkennung auf folgende Weise durchführen:

```c#
RaycastHit hitInfo;
if (Physics.Raycast(playerTransform.position, desiredPosition - playerTransform.position,
    out hitInfo, (playerTransform.position - desiredPosition).magnitude, 1))
{
    curDistance = hitInfo.distance;
}
```

`targetPosition` is just the position of the collision. Set the camera's position to the collision position and you're good to go.

Nach dem Verlassen des starren Körpers kehre langsam zur ursprünglichen Entfernung zurück.
---------------------------------
Um diese Funktion abzuschließen, müssen zunächst die jeweiligen Abstände festgehalten werden, den die Kamera haben sollte (`desiredDistance`) und den aktuellen Abstand (`curDistance`). Das Ergebnis der Scrollrad-Bedienung wird zuerst in `desiredDistance` gespeichert und dann wird basierend auf der Kollision die neue Distanz des Objekts berechnet.
Beim Erkennen, dass die Kamera den starren Körper verlässt oder mit einem entfernteren starren Körper kollidiert, sollte die Kollisionsposition nicht direkt der Kamera zugewiesen werden. Stattdessen sollte eine Bewegungsgeschwindigkeit verwendet werden, um sich an die neue Entfernung anzupassen. Zuerst sollte die neue Entfernung abgerufen werden:

```c#
float newDistance = desiredDistance;
RaycastHit hitInfo;
if (Physics.Raycast(playerTransform.position, desiredPosition - playerTransform.position,
    out hitInfo, (playerTransform.position - desiredPosition).magnitude, 1))
{
    newDistance = hitInfo.distance;
}
```

Wie kann man feststellen, dass die Kamera sich in eine größere Entfernung bewegt? Man kann `newDistances` mit der aktuellen Entfernung vergleichen:


```c#
Bewegen Sie sich näher heran.
if (newDistance < curDistance)
{
    curDistance = newDistance;
}
Bewegen Sie sich weiter weg.
else if(newDistance > curDistance)
{
}
```

So einfach ist es zu entscheiden, wenn man sich in weiter Entfernung bewegen muss - einfach die Geschwindigkeit erhöhen:

```c#
curDistance = Math.Min(curDistance + Time.deltaTime * autoZoomOutSpeed, newDistance);

```
Wir haben nun die grundlegende Funktionalität der Kamera implementiert, es sind jedoch noch einige Details zu klären.

Nach dem Kontakt mit starren Körpern die Rollen annähern, ohne die Bodenskalierung zu ändern.
------------------
Hier sind zwei Anforderungen:

Nach dem Aufprall auf einen starren Körper kann man sich nur annähern, aber nicht entfernen.
Nach dem Aufprall auf dem Boden nicht skalieren.

Zuerst speichern wir den Kollisionsstatus der Kamera in einer Variablen:

```c#
bool isHitGround = false;       // Indicates whether it has hit the ground
bool isHitObject = false;       // Indicates whether a collision with a rigid body (excluding the ground)
```

Fügen Sie eine Bedingungsüberprüfung hinzu, um das Scrollrad-Zoomen zu überprüfen:

```c#
if (zoom != 0F && (!isHitGround || (isHitObject && zoom > 0F)) )
{
    // calculate distance
}
```

Begegnung mit dem Boden und sich um die eigene Achse drehen.
-----------------
(unity-Unity第三人称相机构建(上)Teilen Sie die Rotationsfunktion von `.md` in die X-Rotation (`RotateX`) und Y-Rotation (`RotateY`) auf, und fügen Sie in der Berechnung von `cameraToPlayer` für `RotateY` die Bedingung hinzu:

```c#
if ((!isHitGround) || 
    (isHitGround && transform.forward.y <= cameraToPlayer.y && yAngle > 0))
{
    cameraToPlayer = RotateY(cameraToPlayer, playerTransform.up, 
        transform.right, yAngle);
}
```

Dieses Kriterium besteht aus zwei Teilen:

Hat den Boden nicht berührt.
Auf den Boden treffen, aber bereit sein, den Boden zu verlassen.

Dann wird die Position der Kamera mit `cameraToPlayer` berechnet:

```c#
transform.position = playerTransform.position - cameraToPlayer * curDistance;
```

Und berechnen Sie die Ausrichtung der Kamera, wenn erforderlich (d.h. wenn sie den Boden berührt):

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

Wir haben das Verhalten der Kamera auf diese Weise alle umgesetzt.

Vollständiger Code:

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

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt. Bitte teilen Sie uns [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Bitte weisen Sie auf jegliche Auslassungen hin. 
