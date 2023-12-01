---
layout: post
title: Unity character control
categories:
- unity
catalog: true
tags:
- dev
description: Character movement control is a crucial part of the game, and games with
  responsive controls can effectively attract players. Here, I will attempt to create
  a simple character movement control where the character can perform basic actions
  such as walking and jumping.
figures:
- assets/img/2014-3-15-unity-3rdperson-control0/run_jump.gif
---


The control of character actions is a very important part of the game, and games with strong operability can attract players very well. Here I will try to create a simple character control system where the character can perform basic movements, including walking and jumping.

## Requirement

Let's first consider the specific requirements for character operation:

1. Walking, being able to walk on the surface of a rigid body, controlled by inputting the up, down, left, and right keys, without considering the process of acceleration and deceleration for now.

2. The walking speed can be different in different directions, for example, moving backwards should be slower than moving forward.

3. Jumping, controlled by the jump key, the character leaves the ground with a certain initial velocity and gradually falls back to the ground.

So the general idea is: using velocity to describe the movement of characters, the components of velocity in each direction can be calculated separately, and the position offset of the characters is determined by multiplying velocity by time.

## Character Component Setup
Before writing scripts to manipulate and control characters, some preparation work is needed. The relevant components of the character should be configured first:

1. To control the character and give it some rigid physical behavior, it is necessary to add a `Character Controller Component` to the character.
2. In order to have a clearer structure, the operations related to the character should be separated. After reading and processing the inputs, the results are then passed to the character controller. This part of the script should be named `MyThirdPersonInput.cs`.
3. The script that actually controls the character's movement should be named `MyThirdPersonController.cs`.

The result after configuration is as follows:
![](assets/img/2014-3-15-unity-3rdperson-control0/setting.png)

## Input
Input consists of up, down, left, right, and jump. The directions need to be normalized.

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

## Describing Movement and Jumping
We need to use some variables to describe the character's actions, such as movement speed, jumping speed, etc. Movement is described using the following variables:

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

## Decomposition Speed

In order to describe the movement in different directions easily, the direction is divided into three components: front and back, left and right, up and down, and solved separately.

The speed is different before and after, based on the positive or negative value:

```c#
if (velocity.z > 0)
    velocity.z *= movement.forwardSpeed;
else
    velocity.z *= movement.backwardSpeed;
```

Left and right speed consistent:

```c#
velocity.x = inputMoveDirction.x * movement.sidewardSpeed;
```

Jumping is a bit troublesome, as you need to determine the current status of the character.

- If already in the air, calculate speed using gravity
- If on the ground:
- - If the jump key is pressed, the speed is the initial jump velocity
- - Otherwise, the speed in the y direction is 0

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

## Update character location

The calculated speed is assumed to be the speed from the current frame, so the velocity at which the position of the current frame is calculated should be the one calculated from the previous frame. Therefore, before updating the speed, calculate the character's new position.

```c#
// move to new position
var collisionFlag = controller.Move(velocity * Time.deltaTime);
isOnGround = (collisionFlag & CollisionFlags.CollidedBelow) != 0;
```

The `controller.Move` will return `CollisionFlags` to indicate the collision status, through which we can know if the character is standing on the ground.

Complete code:

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

> Original: <https://disenone.github.io/wiki>  
> This post is protected by [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by/4.0/deed.en) agreement, should be reproduced with attribution.


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
