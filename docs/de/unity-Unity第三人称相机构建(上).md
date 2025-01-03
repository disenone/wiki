---
layout: post
title: Unity Third-Person Camera Setup (Part 1)
categories:
- unity
catalog: true
tags:
- dev
description: Ich möchte in Unity eine Third-Person-Kamera erstellen, die sich am Verhalten
  der Third-Person-Kamera in "World of Warcraft" orientiert. Lassen Sie uns zunächst
  das Rotationsproblem der Kamera lösen.
figure: null
---

<meta property="og:title" content="Unity第三人称相机构建(上)" />

Ich möchte in Unity eine Third-Person-Kamera erstellen, die sich am Verhalten der Third-Person-Kamera in "World of Warcraft" orientiert. Die genauen Anforderungen sind:

1. Linksklick der Maus: Steuert die Kamera, um den Charakter herum zu drehen, der Charakter dreht sich nicht.
Mit der rechten Maustaste kannst du die Kamera um die Figur herum drehen. Die Blickrichtung der Figur (Unity's tranform.forward) dreht sich entsprechend, während die Oberseite der Figur unverändert bleibt.
Nachdem die linke Maustaste gedrückt wurde, wird der Charakter gedreht. Wenn dann die rechte Maustaste gedrückt wird, richtet sich die Charakterbewegung sofort nach der Drehung mit der linken Maustaste aus. Danach wird die Bewegung durch die Drehung mit der rechten Maustaste angepasst. Zu diesem Zeitpunkt ist es äquivalent zu zwei aufeinanderfolgenden Drehungen mit der rechten Maustaste.
Mausrolle: Steuert die Kamera-Zoom-Funktion.
Die Kamera kann nicht durch irgendeinen starren Körper hindurchgehen.
Die Kamera kehrt allmählich auf ihre ursprüngliche Entfernung zurück, nachdem sie das starre Objekt verlassen hat.
Wenn die Kamera auf ein Objekt stößt, sollte sie sofort reagieren, wenn du das Mausrad benutzt, um die Kamera heranzuzoomen. Danach wird Punkt 6 nicht mehr auftreten.
Die Kamera stößt beim Drehen auf den Boden, hört auf, sich um die Figur zu drehen, und beginnt stattdessen, sich um sich selbst zu drehen, während die seitliche Drehung um die Figur weiterhin erfolgt.



Dieses Anliegen kann zunächst in zwei Teile aufgeteilt werden: Kamerarotation und Kamerarigidität. Zur Vereinfachung wird hier zunächst das Problem der Kamerarotation gelöst, das heißt die ersten 3 Punkte des Anliegens.

Kameraposition anzeigen
----------------
Bevor wir mit der eigentlichen Lösung des Kameraproblems beginnen, müssen wir noch eine Frage klären: die Darstellung der Kameraposition. Dies kann auf verschiedene Arten erfolgen:

Die Weltkoordinaten der Kamera
- Die Kamera im Verhältnis zur Position der Person
- Die Ausrichtung und Entfernung der Kamera im Personen-Koordinatensystem

Da die Kamera in unserem Fall je nach Position der Person verschoben wird, habe ich hier die dritte Methode verwendet, und die Kamera bleibt in der Steuerung immer auf die Person gerichtet, sodass in der Kamera nur die Distanzinformation gespeichert werden muss:

```c#
float curDistance = 5F;
```

Kamera drehen
-------------
Setzen wir unsere Analyse des Kameraverhaltens fort, können wir zwischen Drehungen nach links und Drehungen nach rechts unterscheiden. Lassen Sie uns nun Schritt für Schritt beide Rotationen durchführen. Zuerst machen wir die Kamera zum Subobjekt des Charakters, so dass die grundlegenden Kamerabewegungen automatisch verfolgt werden.

###Bitte beachten Sie: Links drehen ###
Bei der reinen Betrachtung der Linksdrehung ist die Anforderung sehr einfach: Die Kamera dreht sich, die Figur dreht sich nicht. Dies entspricht im Grunde einer Kamera zur Beobachtung des Modells, mit der die Kamera das Zentralobjekt aus beliebigen Winkeln betrachten kann.

In Unity kann man den Status der linken Maustaste mit dem Befehl `Input.GetMouseButton(0)` abrufen. Offensichtlich ist die rechte Maustaste `Input.GetMouseButton(1)`. Um die Bewegung des Mauszeigers zu erhalten (als Verschiebung auf der X-Y-Ebene zwischen Frames), verwende `Input.GetAxis("Mouse X"); Input.GetAxis("Mouse Y")`. Lass uns also zunächst die Bewegung des Mauszeigers nach dem Drücken der linken Maustaste abrufen:

```csharp
if (Input.GetMouseButton(0))
{
    float x = Input.GetAxis("Mouse X");
    float y = Input.GetAxis("Mouse Y");
}
```
 
Der Code ist ziemlich einfach, aber hier kommt der entscheidende Punkt: Wie man die Kamera steuert, um sie zu drehen. Um Rotation zu verstehen, benötigt man etwas Wissen über Quaternionen (es gibt viele Informationen im Internet, hier werde ich sie nicht auflisten). Ein wichtiger Punkt über Quaternionen ist, dass sie Drehungen leicht konstruieren können, insbesondere um einen bestimmten Vektor herum. Nachdem man Quaternionen verstanden hat, ist es nicht schwierig, die Kamera um eine Figur herum zu drehen.

Eine weitere wichtige Sache zu beachten ist, dass der Rotationsvektor von Quaternionen nur ein Vektor ist, der vom Ursprung ausgeht. Wenn Sie einen bestimmten Punkt 'O' im Weltkoordinatensystem als Ursprung verwenden möchten und den Vektor 'V', der von diesem Punkt aus geht, als Rotationsachse verwenden möchten, müssen Sie eine Koordinatensystemtransformation durchführen. Vereinfacht ausgedrückt bedeutet dies, dass der Punkt 'P', der rotiert werden soll, in das Koordinatensystem mit 'O' als Ursprung überführt wird, entsprechend 'V' rotiert wird und dann wieder in das Weltkoordinatensystem transformiert wird. Basierend auf diesen Operationen kann eine Funktion erstellt werden:

```c#
Vector3 MyRotate(Vector3 oldPosition, float angle, Vector3 axis, Vector3 axisPosition)
{
Erstellen Sie einen Quaternion mit der Achse als Rotationsachse. Diese Rotation erfolgt im Koordinatensystem des Charakters.
    Quaternion rotation = Quaternion.AngleAxis(angle, axis);
Hier wird einfach die Koordinatentransformation durchgeführt, um die Weltkoordinaten der Kamera in die Koordinaten des Charakters umzuwandeln.
    Vector3 offset = oldPosition - axisPosition;
Berechnen der Rotation und Rücktransformation in das Weltkoordinatensystem.
    return axisPosition + (rotation * offset);
}
```
`Quaternion` is the type in Unity that represents quaternions. Combined with the previous mouse left-click detection, you can achieve left-click control for rotating the camera left and right.

Die Code zum Steuern der Kamera-Rotation nach links und rechts durch Bewegen der Maus nach links und rechts kann direkt bereitgestellt werden:

```c#
newForward = MyRotate(newForward, x, up, Vector3.zero);
```
Da nur der Vorwärtsvektor hier gedreht wird und keine Koordinatensystemumwandlung erfolgt, ist der vierte Parameter `Vector3.zero`.

Die Steuerung der vertikalen Rotation im Vergleich zur horizontalen Rotation ist etwas schwieriger zu verstehen, da sich die Rotationsachse ständig ändert (hier wird angenommen, dass die Aufrichtung der Figur immer in positive Richtung der Y-Achse ist). Beachten Sie, dass die Kamera ebenfalls ständig rotiert und dass der Blickpunkt immer auf die Figur gerichtet ist. So ist die rechte Seite der Kamera unsere gewünschte Rotationsachse (stellen Sie sich die Kamera rechts als die rechte Seite der Figur vor). Mit dieser Erklärung wird auch der Code für die vertikale Rotation sehr einfach.

```csharp
newForward = MyRotate(newForward, -y, transform.right, Vector3.zero);
```

###Drehung mit der rechten Maustaste ###
Nachdem Sie die linke Drehung gemacht haben, ist die rechte Drehung ganz einfach. Sie müssen nur die Blickrichtung des Charakters beim Drehen nach links und rechts einstellen:

```csharp
player.forward = Vector3.Normalize(new Vector3(oldForward.x, 0, oldForward.z));
```

Drehen nach oben und unten ist der gleiche Code wie für die linke Taste.

###Press left mouse button first, then right mouse button.
Obwohl oben links und rechts separat gedreht werden können, entsteht ein Problem, wenn zuerst links gedreht wird und dann mit der rechten Maustaste gearbeitet wird: Die Vorderseite des Charakters und die Vorderseite der Kamera sind nicht mehr gleich! Dadurch trennen sich die Ausrichtungen der Kamera und des Charakters, was die tatsächliche Bedienung seltsam macht. Daher sollte der Charakter beim Drehen mit der rechten Maustaste zuerst in Richtung der Kamera ausgerichtet werden:

```csharp
player.forward = Vector3.Normalize(new Vector3(oldForward.x, 0, oldForward.z));

```

- - - 

###Die Euler-Winkel-Locks ###
By now, the camera rotation is almost complete, but there is one more issue to pay attention to: Euler angle gimbal lock. I won't go into details of the principle here, interested friends can search it by themselves. In the case of the camera here, when the camera rotates up to align with the character's upper direction, a sudden change in the camera's perspective will occur. This is because when the camera reaches the top of the character's head or feet, the camera's upper direction will experience a sudden change (because the Y value of the camera's upper direction must always be greater than zero), so we need to restrict the range of the camera's up and down rotation to prevent gimbal lock. The operation is simple, just limit the range of the angle between the camera's forward direction and the character's upper direction:

```c#
if ((Vector3.Dot(transform.forward, transform.parent.up) >= -0.95F || y > 0) &&
    (Vector3.Dot(transform.forward, transform.parent.up) <= 0.95F || y < 0))
```

###Vollständiger Code###

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

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt. Bitte bei [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Identify any omissions. 
