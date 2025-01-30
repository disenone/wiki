---
layout: post
title: Controles de personaje en Unity
categories:
- unity
catalog: true
tags:
- dev
description: El control de las acciones de los personajes es una parte muy importante
  en los videojuegos; los juegos con una buena jugabilidad pueden atraer a los jugadores
  de manera efectiva. Aquí intentaré crear un control sencillo para la manipulación
  de personajes, que permita realizar movimientos básicos, como caminar y saltar.
figures:
- assets/img/2014-3-15-unity-3rdperson-control0/run_jump.gif
---

<meta property="og:title" content="Unity人物控制" />

![](assets/img/2014-3-15-unity-3rdperson-control0/run_jump.gif)

El control de los movimientos de los personajes es una parte crucial en los videojuegos, ya que una jugabilidad fluida puede atraer a los jugadores. Aquí intentaré crear un sistema simple de control de personajes, permitiendo que se muevan básicamente, incluyendo caminar y saltar.

##Demanda
Primero, consideremos las necesidades específicas de nuestra manipulación de personajes:

Caminar, capaz de caminar en la superficie de un cuerpo rígido, controlado por las teclas de dirección arriba, abajo, izquierda y derecha, sin considerar por ahora el proceso de aceleración y desaceleración.
2. La velocidad de caminar puede ser diferente en distintas direcciones, por ejemplo, retroceder debería ser más lento que avanzar.
3. Saltar, controlado por la tecla jump, el personaje abandona el suelo con una cierta velocidad inicial y vuelve lentamente al suelo.

那么大致的思路就是：用速度来描述人物的运动，速度每个方向上的分量可以分别计算，最后速度乘以时间就是人物的位置偏移了。 

Así que la idea general es la siguiente: usar la velocidad para describir el movimiento de los personajes, se pueden calcular por separado los componentes de la velocidad en cada dirección, y al final la velocidad multiplicada por el tiempo nos da el desplazamiento de la posición del personaje.

##Configuración del componente de personajes
Antes de comenzar a escribir el guion para controlar a los personajes, es necesario hacer algunos preparativos y configurar los componentes relacionados con el personaje.

Para controlar un personaje y lograr que tenga cierto comportamiento físico rígido, es necesario agregar un componente de control de personaje.
Para que la estructura sea más clara, primero separa las operaciones relacionadas con los personajes en una entrada, lee la entrada y procesa los resultados preliminares para luego enviarlos al controlador de personajes. Nombra este script como `MyThirdPersonInput.cs`.
3. El script que controla realmente el movimiento del personaje se llama `MyThirdPersonController.cs`

El resultado después de la configuración es el siguiente:
![](assets/img/2014-3-15-unity-3rdperson-control0/setting.png)

##Entrada
La entrada consiste en arriba, abajo, izquierda, derecha y saltar, las direcciones deben normalizarse:

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

##Descripción del movimiento y el salto
Necesitamos utilizar ciertas variables para describir las acciones de un personaje, como la velocidad de desplazamiento, la velocidad de salto, etc. El desplazamiento se describe con las siguientes variables:

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

La etiqueta `[System.Serializable]` se utiliza para exponer estos parámetros en el Inspector. La descripción del salto es la siguiente:

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

##Velocidad de descomposición
Para facilitar la descripción de los movimientos en diferentes direcciones, se dividen en tres componentes: adelante-atrás, izquierda-derecha y arriba-abajo, y se resuelven por separado.

La velocidad de adelante y atrás es diferente, se juzga según el signo del valor.

```c#
if (velocity.z > 0)
    velocity.z *= movement.forwardSpeed;
else
    velocity.z *= movement.backwardSpeed;
```

Velocidades izquierda y derecha iguales:

```c#
velocity.x = inputMoveDirction.x * movement.sidewardSpeed;
```

Saltar puede ser un poco complicado, ya que hay que determinar el estado actual del personaje:

- Si ya estás en el aire, calcula la velocidad usando la gravedad.
Si estás en el suelo:
- - Si se presiona la tecla de salto, la velocidad es la velocidad inicial de salto.
- - De lo contrario, la velocidad en la dirección y sería 0.

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

##Actualizar la posición del personaje

La velocidad calculada se asume como la velocidad a partir del comienzo del cuadro actual, por lo que la velocidad para calcular la posición en este cuadro debería ser la que se calculó en el cuadro anterior. Por lo tanto, antes de actualizar la velocidad, primero se debe calcular la nueva posición del personaje:

```c#
// move to new position
var collisionFlag = controller.Move(velocity * Time.deltaTime);
isOnGround = (collisionFlag & CollisionFlags.CollidedBelow) != 0;
```

`controller.Move` devolverá `CollisionFlags` para indicar el estado de la colisión, y a través de este estado se puede saber si el personaje está de pie sobre el suelo.

Código completo:

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

--8<-- "footer_es.md"


> Este poste fue traducido utilizando ChatGPT, por favor en [**comentarios**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。  
Señalar cualquier omisión. 
