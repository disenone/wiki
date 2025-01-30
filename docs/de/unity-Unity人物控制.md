---
layout: post
title: Steuerung von Unity-Charakteren
categories:
- unity
catalog: true
tags:
- dev
description: Die Steuerung der Figurenbewegungen ist ein sehr wichtiger Teil des Spiels.
  Spiele mit hoher Bedienbarkeit können die Spieler gut fesseln. Hier versuche ich,
  eine einfache Figurensteuerung zu erstellen, bei der die Figur grundlegende Bewegungen
  wie Gehen und Springen ausführen kann.
figures:
- assets/img/2014-3-15-unity-3rdperson-control0/run_jump.gif
---

<meta property="og:title" content="Unity人物控制" />

![](assets/img/2014-3-15-unity-3rdperson-control0/run_jump.gif)

Die Steuerung der Charakterbewegungen ist ein sehr wichtiger Teil eines Spiels, denn ein Spiel mit guter Spielbarkeit kann die Spieler gut ansprechen. Hier versuche ich, eine einfache Steuerung für die Charakterbewegungen zu entwickeln, so dass der Charakter grundlegende Bewegungen wie Gehen und Springen ausführen kann.

##需求 translates to "Nachfrage" in German.
Bitte denken Sie zuerst über die konkreten Anforderungen bezüglich der Handhabung unserer Charaktere nach:

Gehen, in der Lage sein, auf der Oberfläche eines starren Körpers zu gehen, gesteuert durch die Eingabe von oben, unten, links und rechts auf den Tasten, ohne Beschleunigung oder Verzögerung zu berücksichtigen.
Die Gehgeschwindigkeit kann je nach Richtung variieren, zum Beispiel sollte das Rückwärtsgehen langsamer sein als das Vorwärtsgehen.
Springen, gesteuert von der Sprungtaste, bei der die Figur mit einer bestimmten Anfangsgeschwindigkeit vom Boden abhebt und langsam wieder auf den Boden zurückkehrt.

Die grundlegende Idee hier ist folgende: Man verwendet die Geschwindigkeit, um die Bewegung einer Figur zu beschreiben. Die Geschwindigkeitskomponenten in jeder Richtung können separat berechnet werden. Am Ende wird die Geschwindigkeit mit der Zeit multipliziert, um die Positionsverschiebung der Figur zu erhalten.

##Einstellungen für Personenkomponenten
Bevor Sie ein Skript für die Charaktersteuerung schreiben, sind einige Vorbereitungen erforderlich, um die relevanten Komponenten des Charakters entsprechend einzurichten:

Um die Kontrolle über Charaktere zu haben und diesen etwas starre physikalische Eigenschaften zu verleihen, muss man dem Charakter ein `Character Controller Component` hinzufügen.
2. Um die Struktur klarer zu gestalten, trennen wir zunächst die Eingaben für die Charaktersteuerung. Nachdem wir die Eingaben gelesen und vorläufig verarbeitet haben, geben wir die Ergebnisse an den Charaktercontroller weiter. Dieses Skript benennen wir `MyThirdPersonInput.cs`;
Das Skript, das die Charakterbewegungen wirklich steuert, wird als `MyThirdPersonController.cs` benannt.

Das Ergebnis nach der Konfiguration ist wie folgt:
![](assets/img/2014-3-15-unity-3rdperson-control0/setting.png)

##Eingabe
Eingaben sind nach oben, unten, links, rechts und Sprünge; die Richtung muss normalisiert werden:

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

##Bewegung und Sprünge beschreiben
Wir benötigen einige Variablen, um die Aktionen von Charakteren zu beschreiben, wie z.B. Bewegungsgeschwindigkeit, Sprungkraft usw. Die Bewegung wird mit den folgenden Variablen beschrieben:

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

`[System.Serializable]` dient dazu, diese Parameter im Inspector sichtbar zu machen. Die Beschreibung des Sprungs lautet wie folgt:

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

##Desintegrationsgeschwindigkeit
Um die Beschreibung der Bewegungen in verschiedenen Richtungen zu erleichtern, werden die Richtungen in drei Komponenten unterteilt: vorwärts/rückwärts, links/rechts und oben/unten, die jeweils separat gelöst werden.

Die Vorwärts- und Rückwärtsgeschwindigkeit ist unterschiedlich, basierend auf dem Vorzeichen der Werte.

```c#
if (velocity.z > 0)
    velocity.z *= movement.forwardSpeed;
else
    velocity.z *= movement.backwardSpeed;
```

Die Geschwindigkeit links und rechts stimmt überein:

```c#
velocity.x = inputMoveDirction.x * movement.sidewardSpeed;
```

Springen ist etwas kompliziert, da der aktuelle Zustand des Charakters berücksichtigt werden muss:

- Wenn Sie sich bereits in der Luft befinden, berechnen Sie die Geschwindigkeit mit der Schwerkraft.
- Wenn es auf dem Boden ist:
- - Wenn die Sprungtaste gedrückt wird, beträgt die Geschwindigkeit die anfängliche Sprunggeschwindigkeit.
- - Andernfalls beträgt die Geschwindigkeit in y-Richtung 0.

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

##Aktualisiere die Position der Person

Die berechnete Geschwindigkeit wird angenommen, dass sie die Geschwindigkeit von diesem Frame an ist, daher sollte die Geschwindigkeit für die Positionsberechnung dieses Frames die aus dem vorherigen Frame berechnete sein. Daher wird vor der Aktualisierung der Geschwindigkeit zunächst die neue Position der Person berechnet:

```c#
// move to new position
var collisionFlag = controller.Move(velocity * Time.deltaTime);
isOnGround = (collisionFlag & CollisionFlags.CollidedBelow) != 0;
```

`controller.Move` gibt `CollisionFlags` zurück, um den Kollisionsstatus anzuzeigen. Anhand dieses Status kann man erkennen, ob die Person auf dem Boden steht.

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


> Dieser Beitrag wurde mit ChatGPT übersetzt, bitte in [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Hinweise auf etwaige Auslassungen. 
