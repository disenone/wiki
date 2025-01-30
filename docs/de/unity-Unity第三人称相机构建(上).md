---
layout: post
title: Unity Third-Person Camera Setup (Part 1)
categories:
- unity
catalog: true
tags:
- dev
description: Ich möchte in Unity eine Third-Person-Kamera erstellen, die sich an der
  Third-Person-Kamera von "World of Warcraft" orientiert. Lassen Sie uns zunächst
  das Problem der Kameradrehung lösen.
figure: null
---

<meta property="og:title" content="Unity第三人称相机构建(上)" />

Ich möchte in Unity eine Third-Person-Kamera erstellen, deren Verhalten sich an der Third-Person-Kamera aus „World of Warcraft“ orientiert. Die konkreten Anforderungen sind:

1. Linke Maustaste: Steuert die Kamera, die sich um die Figur dreht, während die Figur selbst nicht rotiert.
2. Rechtsklick: Die Kamera dreht sich um die Person, wobei die Vorderseite der Person (transform.forward in Unity) entsprechend rotiert, während die Oberseite der Person unverändert bleibt.
3. Nachdem die linke Maustaste gedreht wurde, wird bei einer Drehung mit der rechten Maustaste die Vorderansicht des Charakters sofort an die Drehung der linken Maustaste angepasst und anschließend an die Drehung der rechten Maustaste. Zu diesem Zeitpunkt entspricht dies zwei Drehungen mit der rechten Maustaste.
4. Mausrad: Steuert die Kamera-Zoomfunktion
5. Die Kamera kann nicht durch feste Objekte hindurchsehen.
Die Kamera kehrt langsam zu ihrer ursprünglichen Position zurück, nachdem sie den starren Gegenstand berührt hat.
7. Wenn die Kamera auf ein Objekt trifft, sollte die Kamera sofort reagieren, wenn das Mausrad verwendet wird, um die Kamera heranzuzoomen. Danach tritt Punkt 6 nicht mehr ein.
8. Die Kamera berührt den Boden während der Drehung, stoppt das Auf- und Abdrehen um die Person und beginnt stattdessen, sich um sich selbst auf- und abzudrehen, während das Drehen nach links und rechts weiterhin um die Person erfolgt.



Diese Anforderung kann zunächst in zwei Teile unterteilt werden: Kameradrehung und Kamerarigidität. Um es einfach zu halten, betrachten wir hier zunächst das Problem der Kameradrehung, das die ersten drei Punkte der Anforderungen betrifft.

Kameraposition anzeigen
----------------
Bevor die Kamerabedienung offiziell gelöst werden kann, gibt es ein weiteres Problem zu klären: die Darstellung der Kameraposition. Dies kann auf verschiedene Weisen erfolgen:

- Weltkoordinaten der Kamera
Die Kamera in Bezug auf die Position der Person.
- Die Richtung und der Abstand der Kamera im Koordinatensystem der Person

Aufgrund unserer Anforderungen wird die Kamera entsprechend der Position der Person transformiert. Daher verwende ich hier den dritten Ansatz, und die Kamera zielt ständig auf die Person. Daher muss in der Kamera nur die Distanzinformation gespeichert werden:

```c#
float curDistance = 5F;
```

Kamera drehen
-------------
Um das Verhalten der Kamer旋转 weiter zu unterteilen, können wir zwischen Linksklick旋转 und Rechtsklick旋转 unterscheiden. Lassen Sie uns diese beiden旋转 Schritt für Schritt durcharbeiten. Zunächst setze ich die Kamera als untergeordnetes Objekt (children) der Figur, sodass die Kamera einige grundlegende Bewegungen der Figur automatisch verfolgt.

###Bitte entfernen Sie den Text "Links drehen ###"
Allein das Drehen der linken Maustaste ist einfach: **Die Kamera dreht sich, die Figur dreht sich nicht**. Das entspricht einer Kamera, die ein Modell beobachtet, wobei die Kamera das zentrale Objekt aus beliebigem Winkel betrachten kann.

In Unity wird der Status der linken Maustaste mit folgendem Code abgerufen: `Input.GetMouseButton(0)` (Hinweis: Alle Codebeispiele sind in C#). Offensichtlich wird der Status der rechten Maustaste mit `Input.GetMouseButton(1)` abgefragt. Um die Bewegung des Mauszeigers (den Versatz des Cursors auf der X-Y-Ebene zwischen Frames) zu erhalten, können Sie `Input.GetAxis("Mouse X"); Input.GetAxis("Mouse Y")` verwenden. Nun können wir zuerst die Bewegungsinformationen des Cursors erhalten, nachdem die linke Maustaste gedrückt wurde:

```csharp
if (Input.GetMouseButton(0))
{
    float x = Input.GetAxis("Mouse X");
    float y = Input.GetAxis("Mouse Y");
}
```
 
Der Code ist einfach, der entscheidende Punkt liegt jedoch darunter: Wie man die Kamera steuert, um zu rotieren. Um Rotation zu verstehen, benötigt man hier einige Kenntnisse über Quaternionen (es gibt viele Online-Ressourcen dazu, daher liste ich sie hier nicht auf). Ein wichtiger Punkt von Quaternionen ist, dass sie Rotation sehr einfach konstruieren können, insbesondere Drehungen um einen bestimmten Vektor. Nachdem man Quaternionen verstanden hat, wird es nicht schwierig sein, die Kamera um eine Figur zu rotieren.

Ein weiterer Punkt, den man beachten sollte, ist, dass die Rotationsachse des Quaternion nur ein Vektor ist, der vom Ursprung ausgeht. Wenn man einen bestimmten Punkt `O` im Weltkoordinatensystem als Ursprung nehmen und den Vektor `V`, der von diesem Punkt ausgeht, als Rotationsachse verwenden möchte, ist eine Koordinatentransformation erforderlich. Vereinfacht gesagt, muss der Punkt `P`, der rotiert werden soll, in das Koordinatensystem transformiert werden, das `O` als Ursprung hat. Anschließend wird um `V` rotiert, bevor wieder in das Weltkoordinatensystem zurücktransformiert wird. Basierend auf diesen Operationen kann eine Funktion geschrieben werden:

```c#
Vector3 MyRotate(Vector3 oldPosition, float angle, Vector3 axis, Vector3 axisPosition)
{
Erstellen Sie ein Quaternion mit der Achse als Rotationsachse. Dies erfolgt in Bezug auf das Koordinatensystem der Figur.
    Quaternion rotation = Quaternion.AngleAxis(angle, axis);
// Hier wird die Koordinatentransformation durchgeführt, um die Weltkoordinaten der Kamera in die Koordinaten des Personenkoordinatensystems zu verwandeln.
    Vector3 offset = oldPosition - axisPosition;
Berechne die Rotation und transformiere sie zurück in das Weltkoordinatensystem.
    return axisPosition + (rotation * offset);
}
```
`Quaternion` ist der Typ zur Darstellung von Quaternionen in Unity. In Kombination mit der vorherigen Erkennung der linken Maustaste kann somit eine Steuerung der Kameradrehung nach links und rechts erfolgen.

Die Codes, die die linke und rechte Bewegung der Maus steuern und die Kamera links und rechts drehen lassen, können direkt bereitgestellt werden:

```c#
newForward = MyRotate(newForward, x, up, Vector3.zero);
```
Da hier nur der Vorwärtsvektor gedreht wird, ohne eine Umwandlung des Koordinatensystems, ist der vierte Parameter `Vector3.zero`.

Die Kontrolle über die vertikale Drehung im Vergleich zur horizontalen Drehung ist etwas schwieriger zu verstehen, da sich die Drehachse ständig verändert (hier wird angenommen, dass die Aufwärtsbewegung des Charakters immer in die positive Richtung der Y-Achse zeigt). Beachten Sie, dass die Kamera sich ebenfalls ständig dreht und dabei stets auf den Mittelpunkt des Charakters gerichtet bleibt. Somit entspricht die rechte Seite der Kamera (right) der Achse, um die wir rotieren möchten (stell dir die rechte Seite der Kamera als die rechte Seite des Charakters vor). Mit diesem Verständnis wird auch der Code für die vertikale Drehung sehr einfach:

```csharp
newForward = MyRotate(newForward, -y, transform.right, Vector3.zero);
```

###Rechtsklick drehen###
Nachdem Sie die linke Maustaste zum Drehen verwendet haben, ist das Drehen mit der rechten Maustaste sehr einfach. Sie müssen nur beim Drehen nach links und rechts die Blickrichtung der Figur einstellen:

```csharp
player.forward = Vector3.Normalize(new Vector3(oldForward.x, 0, oldForward.z));
```

Die Codes für das Auf- und Abdrehen sind identisch mit dem für die linke Maustaste.

###Zuerst die linke Maustaste, dann die rechte Maustaste###
Obwohl Sie oben mit der linken Maustaste und der rechten Maustaste drehen können, entsteht ein Problem, wenn Sie zuerst mit der linken Maustaste drehen und dann mit der rechten Maustaste handeln: Die Ausrichtung der Figur und die Ausrichtung der Kamera unterscheiden sich! Dadurch werden die Ausrichtungen von Kamera und Figur voneinander getrennt, was die tatsächliche Handhabung seltsam macht. Daher müssen wir die Figur beim Drehen mit der rechten Maustaste zuerst so anpassen, dass sie mit der Ausrichtung der Kamera übereinstimmt:

```csharp
player.forward = Vector3.Normalize(new Vector3(oldForward.x, 0, oldForward.z));

```

- - - 

###欧拉角万向锁###
Bis hierhin ist die Drehung der Kamera nahezu abgeschlossen, jedoch gibt es ein Problem, das beachtet werden muss: der Euler-Winkel-Gimbal-Lock. Die Theorie hierzu möchte ich nicht im Detail erläutern; interessierte Leser können selbst nachforschen. Im Kontext der Kamera bedeutet dies, dass der Kamerawinkel einen plötzlichen Wechsel erfährt, wenn die Kamera beim Hoch- oder Runterdrehen mit der Oberseite des Körpers übereinstimmt. Dies geschieht, weil die Kamera entweder den Kopf oder die Füße der Person erreicht, wodurch sich die obere Richtung der Kamera ändert (da der Y-Wert der oberen Richtung der Kamera immer über null liegen muss). Daher müssen wir den vertikalen Drehbereich der Kamera einschränken, um einen Gimbal-Lock zu vermeiden. Die Handhabung ist ganz einfach: Wir beschränken den Winkel zwischen der Vorwärtsrichtung der Kamera und der oberen Richtung der Person.

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


> Dieser Beitrag wurde mit ChatGPT übersetzt, bitte unter [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Es wird auf etwaige Auslassungen hingewiesen. 
