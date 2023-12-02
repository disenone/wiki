---
layout: post
title: Unity Character Control
categories:
- unity
catalog: true
tags:
- dev
description: The control of character actions is a crucial part of the game, and games
  with strong operability can attract players well. Here, I will try to create a simple
  character control that allows the character to perform basic movements, including
  walking and jumping.
figures:
- assets/img/2014-3-15-unity-3rdperson-control0/run_jump.gif
---

<meta property="og:title" content="Unity人物控制" />

![](assets/img/2014-3-15-unity-3rdperson-control0/run_jump.gif)

Character action control is a crucial part of the game, as games with strong operation capabilities can effectively attract players. Here, I will attempt to create a simple character control system where the character can perform basic movements, including walking and jumping.

## Requirement
First, let's consider the specific requirements for character operations:

1. Walking, able to walk on the surface of the rigid body, controlled by arrow keys for up, down, left, and right input, without considering the acceleration and deceleration process for now.
2. The walking speed can be different in different directions, for example, moving backward should be slower than moving forward.
3. Jumping, controlled by the jump key, the character leaves the ground with a certain initial velocity and gradually falls back to the ground.

The general idea is as follows: Use velocity to describe the movement of a character. The components of velocity in each direction can be calculated separately, and finally, multiplying velocity by time gives the character's position offset.

## Character Component Settings
Before writing scripts to control and manipulate characters, some preparation work needs to be done to configure the relevant components of the character.

1. In order to control the characters and give them some rigid physical behavior, it is necessary to add a `Character Controller Component` to the characters.
2. For a clearer structure, separate the input for character operations first, read and preprocess the input, and then pass the results to the character controller. Name this part of the script as `MyThirdPersonInput.cs`.
3. The script that actually controls the character's movement should be named `MyThirdPersonController.cs`.

The result after configuration is as follows:

![](assets/img/2014-3-15-unity-3rdperson-control0/setting.png)

## Input
The input consists of up, down, left, right, and jump commands. The direction needs to be normalized:

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
We need to use some variables to describe the character's actions, such as movement speed, jumping speed, etc. Movement is described using the following variable:

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

`[System.Serializable]` is used to expose these parameters in the Inspector. The description of jumping is as follows:

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
In order to facilitate the description of movement in different directions, the direction is divided into three components: front and back, left and right, and up and down, respectively, to be resolved.

The speed difference before and after varies. It can be determined based on the sign of the numerical value:

```c#
if (velocity.z > 0)
    velocity.z *= movement.forwardSpeed;
else
    velocity.z *= movement.backwardSpeed;
```

Same Speed on Both Sides:

```c#
velocity.x = inputMoveDirction.x * movement.sidewardSpeed;
```

Jumping is a bit troublesome as it requires determining the current status of the character:

- If already in the air, calculate the speed with gravity.
- If on the ground:
- - If the jump key is pressed, the speed is the initial jump speed.
- - Otherwise, the speed in the y direction is 0.

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

## Update Character Location

The calculated velocity is assumed to be the velocity from the current frame. So, the velocity used to calculate the position in the current frame should be the one calculated in the previous frame. Therefore, before updating the velocity, calculate the character's new position first.

```c#
// move to new position
var collisionFlag = controller.Move(velocity * Time.deltaTime);
isOnGround = (collisionFlag & CollisionFlags.CollidedBelow) != 0;
```

`controller.Move` will return `CollisionFlags` to indicate the collision state, through which we can determine whether the character is standing on the ground or not.

Complete code:

(to_be_replaced1)

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

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
