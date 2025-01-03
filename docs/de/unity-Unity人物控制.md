---
layout: post
title: Steuerung von Unity-Charakteren
categories:
- unity
catalog: true
tags:
- dev
description: Die Steuerung der Charakterbewegungen ist ein wichtiger Teil des Spiels,
  eine gute Spielbarkeit kann die Spieler gut anziehen. Hier werde ich versuchen,
  eine einfache Steuerung für die Charaktere zu erstellen, damit sie grundlegende
  Bewegungen wie Gehen und Springen ausführen können.
figures:
- assets/img/2014-3-15-unity-3rdperson-control0/run_jump.gif
---

<meta property="og:title" content="Unity人物控制" />

![](assets/img/2014-3-15-unity-3rdperson-control0/run_jump.gif)

Die Steuerung der Charakterbewegungen ist ein wichtiger Teil eines Spiels, denn Spiele mit guter Spielbarkeit können die Spieler gut anziehen. Hier werde ich versuchen, eine einfache Steuerung der Charakterbewegungen zu erstellen, damit der Charakter grundlegende Bewegungen ausführen kann, einschließlich Gehen und Springen.

##Nachfrage
Beginnen wir damit, über die konkreten Anforderungen für das Handling unserer Figuren nachzudenken:

Gehen, um auf der Oberfläche eines starren Körpers zu gehen, gesteuert durch die Eingabe von Tasten für Auf, Ab, Links und Rechts, vorübergehend ohne Beschleunigung oder Verzögerung zu berücksichtigen.
Die Gehgeschwindigkeit kann je nach Richtung unterschiedlich sein, zum Beispiel sollte rückwärts langsamer sein als vorwärts.
Springen, gesteuert durch die Taste "Springen", lässt die Figur mit einer bestimmten Anfangsgeschwindigkeit vom Boden abheben und langsam wieder auf den Boden zurückfallen.

Die grundlegende Idee ist also: Man benutzt die Geschwindigkeit, um die Bewegung einer Person zu beschreiben. Die Geschwindigkeit in jeder Richtung kann separat berechnet werden, und am Ende ergibt die Geschwindigkeit multipliziert mit der Zeit die Verschiebung der Position der Person.

##Die Einstellungen für das Charakter-Element.
Bevor Sie das Skript zur Steuerung der Charaktere schreiben, müssen Sie einige Vorbereitungen treffen und die entsprechenden Komponenten des Charakters zuerst konfigurieren:

Um einen Charakter zu steuern und ihm einige steife physikalische Eigenschaften zu geben, muss dem Charakter ein `Character Controller Component` hinzugefügt werden.
Um die Struktur etwas klarer zu gestalten, trennen wir zuerst die Eingaben bezüglich der Charaktere ab, lesen sie ein und verarbeiten sie vorläufig, bevor wir die Ergebnisse an den Charakter-Controller übergeben. Nennen wir dieses Skript `MyThirdPersonInput.cs`.
Der Code, der die Bewegung des Charakters steuert, wird als `MyThirdPersonController.cs` bezeichnet.

Die resultierende Konfiguration ist wie folgt:
![](assets/img/2014-3-15-unity-3rdperson-control0/setting.png)

##Eingabe
Die Eingabe besteht aus den Richtungen oben, unten, links, rechts und Springen. Die Richtungen müssen normalisiert werden.

```c#
// get movement from input
var direction = new Vector3(Input.GetAxis("Horizontal"), 0, 
	Input.GetAxis("Vertical"));
if (direction != Vector3.zero)
{
    // constrain length to [0, 1]
    var directionLength = direction.magnitude;
    directionLength = Math.Min(1, directionLength);
    direction = direction.normalized * directionLength;
}
person.inputMoveDirction = direction;
person.inputJump = Input.GetButton("Jump");
````

##Beschreibung von Bewegung und Springen
Wir müssen einige Variablen verwenden, um die Bewegungen der Figuren zu beschreiben, wie zum Beispiel Geschwindigkeit beim Laufen, Springen usw. Die Bewegung wird mit den folgenden Variablen beschrieben:

```c#    
[System.Serializable]
public class Movement
{
    public float forwardSpeed = 5F;
    public float backwardSpeed = 5F;
    public float sidewardSpeed = 5F;
}
public Movement movement = new Movement();
```

`[System.Serializable]` is used to expose these parameters in the Inspector. The description of the jump is as follows:

```c#
[System.Serializable]
public class Jumping 
{
    public bool enable = true;      // true if can jump
    public float jumpSpeed = 5F;    // original speed when jump
    public float gravity = 10F;
    public float maxFallSpeed = 20F;
    public bool jumping = false;    // true if now in the air
}
public Jumping jumping = new Jumping();
```

##Zersetzungsgeschwindigkeit
Um verschiedene Bewegungsrichtungen besser beschreiben zu können, werden die Richtungen in drei Komponenten unterteilt: Vorwärts und rückwärts, links und rechts, oben und unten, die jeweils separat berechnet werden.

Die Geschwindigkeit vorwärts und rückwärts ist unterschiedlich. Entscheidend ist das Vorzeichen des Werts:

```c#
if (velocity.z > 0)
    velocity.z *= movement.forwardSpeed;
else
    velocity.z *= movement.backwardSpeed;
```

Gleiche Geschwindigkeit auf beiden Seiten:

```c#
velocity.x = inputMoveDirction.x * movement.sidewardSpeed;
```

Springen ist etwas komplizierter, weil der aktuelle Zustand der Figur berücksichtigt werden muss:

Wenn du bereits in der Luft bist, berechne die Geschwindigkeit basierend auf der Schwerkraft.
Wenn es auf dem Boden ist:
Wenn die Sprungtaste gedrückt wird, ist die Geschwindigkeit gleich der Anfangsgeschwindigkeit des Sprungs.
Sonst ist die Geschwindigkeit in y-Richtung null.

```c#
if (!isOnGround)
{
    yVelocity = Math.Max(yVelocity - jumping.gravity * Time.deltaTime, 
    	-jumping.maxFallSpeed);
}
else
{
    if (jumping.enable && inputJump)
    {
        yVelocity = jumping.jumpSpeed;
    }
    else
        yVelocity = 0F;
}
```

##Aktualisierung der Charakterposition.

Berechnete Geschwindigkeiten werden als die Geschwindigkeiten ab dem aktuellen Frame angenommen. Die Geschwindigkeit, mit der die Position dieses Frames berechnet wird, sollte die sein, die im vorherigen Frame berechnet wurde. Daher wird die neue Position der Figur vor der Aktualisierung der Geschwindigkeit berechnet:

```c#
// move to new position
var collisionFlag = controller.Move(velocity * Time.deltaTime);
isOnGround = (collisionFlag & CollisionFlags.CollidedBelow) != 0;
```

Die `controller.Move` Methode gibt die `CollisionFlags` zurück, um den Kollisionsstatus anzuzeigen. Anhand dieses Status kann festgestellt werden, ob die Figur auf dem Boden steht.

Vollständiger Code:

MyThirdPersonInput.cs:

```c#
using UnityEngine;
using System;
using System.Collections;
[RequireComponent(typeof(MyThirdPersonController))]

public class MyThirdPersonInput : MonoBehaviour {

    private MyThirdPersonController person;

    void Awake()
    {
        person = GetComponent<MyThirdPersonController>();
    }
	
	// Update is called once per frame
	void Update () 
    {
        // get movement from input
        var direction = new Vector3(Input.GetAxis("Horizontal"), 0, 
        	Input.GetAxis("Vertical"));

        if (direction != Vector3.zero)
        {
            // constrain length to [0, 1]
            var directionLength = direction.magnitude;

            directionLength = Math.Min(1, directionLength);

            direction = direction.normalized * directionLength;

        }

        person.inputMoveDirction = direction;
        person.inputJump = Input.GetButton("Jump");
        
    }
}

```

MyThirdPersonController.cs:

```c#
using UnityEngine;
using System;
using System.Collections;

public class MyThirdPersonController : MonoBehaviour {

    // The current global direction we want the character to move in.
    [System.NonSerialized]
    public Vector3 inputMoveDirction = Vector3.zero;

    // Is the jump button held down? We use this interface instead of checking
    // for the jump button directly so this script can also be used by AIs.
    [System.NonSerialized]
    public bool inputJump = false;

    [System.Serializable]
    public class Movement
    {
        public float forwardSpeed = 5F;
        public float backwardSpeed = 5F;
        public float sidewardSpeed = 5F;
    }
    public Movement movement = new Movement();
    
    [System.Serializable]
    public class Jumping 
    {
        public bool enable = true;      // true if can jump
        public float jumpSpeed = 5F;    // original speed when jump
        public float gravity = 10F;     
        public float maxFallSpeed = 20F;
        public bool jumping = false;    // true if now in the air
    }
    public Jumping jumping = new Jumping();

    private CharacterController controller;
    private Vector3 velocity = Vector3.zero;
    private bool isOnGround = true;
	// Use this for initialization
	void Start () 
    {
        controller = GetComponent<CharacterController>();
	}
	
	// Update is called once per frame
    void FixedUpdate() 
    {
        // move to new position
        var collisionFlag = controller.Move(velocity * Time.deltaTime);
        isOnGround = (collisionFlag & CollisionFlags.CollidedBelow) != 0;

        // update velocity
        float yVelocity = velocity.y;
        velocity = Vector3.zero;

        // x-z plane velocity
        if (inputMoveDirction != Vector3.zero)
        {
            velocity.z = inputMoveDirction.z;
            if (velocity.z > 0)
                velocity.z *= movement.forwardSpeed;
            else
                velocity.z *= movement.backwardSpeed;

            velocity.x = inputMoveDirction.x * movement.sidewardSpeed;
        }

        // y velocity
        if (!isOnGround)
        {
            yVelocity = Math.Max(yVelocity - jumping.gravity * Time.deltaTime, 
            	-jumping.maxFallSpeed);
        }
        else
        {
            if (jumping.enable && inputJump)
            {
                yVelocity = jumping.jumpSpeed;
            }
            else
                yVelocity = 0F;
        }

        velocity = transform.rotation * velocity;
        velocity.y = yVelocity;
	}
}
```

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt. Bitte geben Sie Ihr [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Bitte weisen Sie auf eventuelle Auslassungen hin. 
