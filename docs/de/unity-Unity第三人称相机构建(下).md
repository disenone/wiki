---
layout: post
title: Unity Dritte-Person-Kamera-Setup (Teil 2)
categories:
- unity
catalog: true
tags:
- dev
description: Ich möchte in Unity eine Third-Person-Kamera erstellen, deren Verhalten
  sich an der Third-Person-Kamera von „World of Warcraft“ orientiert. Hier wird das
  Problem des Rigidbody der Kamera gelöst.
---

<meta property="og:title" content="Unity第三人称相机构建(下)" />

Die vorherige Episode endete mit [der Drehung der Kamera](unity-Unity第三人称相机构建(上).md), nun, das Problem, das wir jetzt lösen müssen, ist die Steifigkeit der Kamera. Wie gehen wir damit um?

Kamerarigidität
--------------
Rückblick auf die zuvor genannten Anforderungen:

4. Mausrad: Steuert die Nähe und Entfernung der Kamera
5. Die Kamera kann keine festen Objekte durchdringen.
Die Kamera kehrt langsam zu ihrer ursprünglichen Entfernung zurück, nachdem sie das starre Objekt verlassen hat.
Wenn die Kamera auf ein starres Objekt trifft, muss sie sofort auf die Mausradoperation zum Zoomen reagieren. Anschließend tritt Punkt 6 nicht mehr auf; nach dem Aufprall auf dem Boden kann nicht mehr gezoomt werden.
Die Kamera stößt beim Drehen gegen den Boden, hört auf, um die Person herum auf und ab zu drehen, und beginnt stattdessen, sich um sich selbst auf und ab zu drehen, während die seitliche Drehung weiterhin um die Person herum erfolgt.


Diese Punkte bedeuten: Wenn die Kamera auf ein starres Objekt trifft, wird sie gezwungen, sich dem Abstand zu den Personen zu nähern. Wenn wir möchten, dass die Kamera beim Verlassen langsam in ihren ursprünglichen Abstand zurückkehrt, aber nachdem der Abstand automatisch verringert wurde, manuell mit dem Scrollrad näher gebracht wird, bedeutet dies, dass die Kamera das kollidierte Objekt verlässt. Dann ist dieser Verkürzungsabstand der tatsächliche Abstand der Kamera. Jetzt werden wir diese Anforderungen Schritt für Schritt erläutern.

Rollensteuerung.
----------
Das Steuern des Mausrads ist ganz einfach, man muss nur wissen, dass man die Informationen des Rades mit `Input.GetAxis("Mouse ScrollWheel")` abruft und die maximalen und minimalen Abstände festlegt, dann ist alles in Ordnung:

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

Hier verweist `playerTransform` auf die Figur.

Kann keine starren Objekte durchqueren.
--------------------
Dies erfordert die Überprüfung des Kontakts zwischen der Kamera und dem starren Körper, es gibt eine Funktion, die diese Funktion umsetzen kann:

```c#
static bool Raycast(Ray ray, RaycastHit hitInfo, float distance = Mathf.Infinity, int layerMask = DefaultRaycastLayers);
```

Konkrete Verwendungsweise siehe Unitys [Referenz](http://docs.unity3d.com/Documentation/ScriptReference/Physics.Raycast.html)Wir können die Kollisionserkennung folgendermaßen umsetzen:

```c#
RaycastHit hitInfo;
if (Physics.Raycast(playerTransform.position, desiredPosition - playerTransform.position,
    out hitInfo, (playerTransform.position - desiredPosition).magnitude, 1))
{
    curDistance = hitInfo.distance;
}
```

`targetPosition` ist die Position des Aufpralls. Setzen Sie die Kamera auf diese Position, um sie korrekt auszurichten.

Nach Verlassen des starren Körpers langsam zur ursprünglichen Entfernung zurückkehren.
---------------------------------
Um diese Funktion zu vervollständigen, müssen zunächst die Distanz, auf die die Kamera eingestellt werden soll (`desiredDistance`), und die aktuelle Distanz (`curDistance`) separat aufgezeichnet werden. Das Ergebnis der Scrollradoperation wird zuerst in `desiredDistance` gespeichert, bevor die neue Distanz des Objekts basierend auf der Kollision berechnet wird;
Wenn die Kamera von einem starren Körper entfernt ist oder mit einem weiter entfernten starren Körper kollidiert, kann die Kollisionsposition nicht direkt der Kamera zugewiesen werden; stattdessen muss eine Bewegungsdynamik verwendet werden, um sich zur neuen Distanz zu bewegen. Zuerst muss die neue Distanz ermittelt werden:

```c#
float newDistance = desiredDistance;
RaycastHit hitInfo;
if (Physics.Raycast(playerTransform.position, desiredPosition - playerTransform.position,
    out hitInfo, (playerTransform.position - desiredPosition).magnitude, 1))
{
    newDistance = hitInfo.distance;
}
```

Wie kann man also feststellen, dass die Kamera sich in eine größere Entfernung bewegt? Man kann `newDistances` mit der aktuellen Entfernung vergleichen:

```c#
// Bewege dich näher heran
if (newDistance < curDistance)
{
    curDistance = newDistance;
}
Bewegen Sie sich in die Ferne.
else if(newDistance > curDistance)
{
}
```

Dann ist die Entscheidung, sich weiter zu bewegen, sehr intuitiv; man fügt einfach eine Geschwindigkeit hinzu, um sich zu bewegen:

```c#
curDistance = Math.Min(curDistance + Time.deltaTime * autoZoomOutSpeed, newDistance);

```
Das allgemeine Verhalten der Kamera haben wir bereits abgeschlossen, es gibt noch einige Details, die wir bearbeiten müssen.

Nach dem Kontakt mit einem starren Körper werden die Rollen näher herangezogen, aber der Boden wird nicht skaliert.
------------------
Hier gibt es zwei Anforderungen:

Nachdem ein Körper auf etwas gestoßen ist, kann er nur näher herangezogen werden, nicht weiter entfernt.
2. Nach dem Kontakt mit dem Boden kann er nicht verkleinert werden.

Zuerst werden Variablen verwendet, um den Kollisionsstatus der Kamera zu speichern:

```c#
bool isHitGround = false;       // Indicates whether the ground is hit
bool isHitObject = false;       // Indicates whether a collision with a rigid body (excluding the ground) occurred.
```

Fügen Sie eine Bedingungsprüfung hinzu, wenn Sie das Scrollrad-Zoom bewerten:

```c#
if (zoom != 0F && (!isHitGround || (isHitObject && zoom > 0F)) )
{
    // calculate distance
}
```

Treffen Sie den Boden und drehen Sie sich um sich selbst nach oben und unten.
-----------------
Diese Funktion ist etwas kompliziert zu implementieren, da unsere vorherige Annahme, dass die Kamera stets auf die Figur ausgerichtet ist, nicht mehr gültig ist. Zu diesem Zeitpunkt teilen wir in zwei Vektoren auf: **die Ausrichtung der Kamera (`desireForward`)** und **die Richtung von der Kamera zur Figur (`cameraToPlayer`)**. Wir berechnen die Werte dieser beiden Vektoren separat; der erste bestimmt die Ausrichtung der Kamera, der zweite bestimmt die Position der Kamera. Zur Vereinfachung nehmen wir [die vorherige Episode](unity-Unity第三人称相机构建(上)Teilen Sie die Rotationsfunktion von `.md` in die X-Rotation (`RotateX`) und Y-Rotation (`RotateY`) auf, und fügen Sie die Bedingung hinzu, wenn Sie `RotateY` von `cameraToPlayer` berechnen:

```c#
if ((!isHitGround) || 
    (isHitGround && transform.forward.y <= cameraToPlayer.y && yAngle > 0))
{
    cameraToPlayer = RotateY(cameraToPlayer, playerTransform.up, 
        transform.right, yAngle);
}
```

Dieses Kriterium hat zwei Teile:

- Berührung mit dem Boden vermieden.
Auf den Boden treffen, aber bereit sein, den Boden zu verlassen.

Dann berechnen Sie die Position der Kamera mit `cameraToPlayer`:

```c#
transform.position = playerTransform.position - cameraToPlayer * curDistance;
```

Und berechnen Sie die Ausrichtung der Kamera bei Bedarf (d. h. wenn sie den Boden berührt):

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

Dieses Verhalten der Kamera haben wir alle umgesetzt.

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


> Dieser Beitrag wurde mit ChatGPT übersetzt, bitte [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Fehler überprüfen. 
