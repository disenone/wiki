---
layout: post
title: Unity Character Control
categories:
- unity
catalog: true
tags:
- dev
description: The control of character actions is a crucial part of the game, as games
  with strong operability can attract players well. Here I will attempt to create
  a simple character control scheme, where the character can perform basic movements,
  including walking and jumping.
figures:
- assets/img/2014-3-15-unity-3rdperson-control0/run_jump.gif
---

<meta property="og:title" content="Unity人物控制" />

[assets/img/2014-3-15-unity-3rdperson-control0/run_jump.gif]

Character action control is a very important part of the game, and games with strong operability can attract players well. Here I will try to create a simple character control, where the character can perform basic movements, including walking and jumping.

## Requirements
Let's first consider the specific requirements for controlling our characters:

Translate these text into English language:

1. [to_be_replaced[行走，能够在刚体的表面行走，由按键上下左右输入来控制，暂不考虑加速减速过程]]
2. [to_be_replaced[行走的速度在不同方向上可以不同，例如后退应该比前进慢]]
3. [to_be_replaced[跳跃，由jump按键控制，人物以一定初速度从上离开地面，并慢慢回落到地面]]

The basic idea is as follows: Use velocity to describe the movement of a character. The components of velocity in each direction can be calculated separately, and finally, multiplying velocity by time gives the character's displacement.

## Character Component Settings
Before writing scripts to manipulate and control characters, some preparations need to be made to configure the relevant components of the character first:

Translate these text into English language:

1. In order to control the character and give the character some rigid physical behavior, it is necessary to add a `Character Controller Component` to the character.
2. In order to make the structure more clear, separate the input for character actions, read and preprocess the input, and then pass the results to the character controller. Name this part of the script as `MyThirdPersonInput.cs`.
3. The script that actually controls character movement should be named `MyThirdPersonController.cs`.

The result after configuration is as follows:
![](assets/img/2014-3-15-unity-3rdperson-control0/setting.png)

## Input
The input consists of directions for up, down, left, right, and jump. The directions need to be normalized.

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

## Description of Movement and Jumping
We need to use some variables to describe the actions of the character, such as movement speed, jumping speed, etc. The variables used for movement are described below:

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

`[System.Serializable]` is used to make these parameters visible in the Inspector. The description of jumping is as follows:

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
In order to describe the movement in different directions conveniently, the direction is divided into three components: forward/backward, left/right, and up/down, and solved separately.

Different speeds before and after, judging according to the positive and negative values:

```c#
if (velocity.z > 0)
    velocity.z *= movement.forwardSpeed;
else
    velocity.z *= movement.backwardSpeed;
```

Equal Speed on Both Sides:

```c#
velocity.x = inputMoveDirction.x * movement.sidewardSpeed;
```

Jumping is a bit troublesome as it requires determining the current state of the character:

- If already in the air, calculate velocity using gravity.
- If on the ground:
- - If jump key is pressed, velocity is set to the initial jump velocity.
- - Otherwise, the velocity in the y direction is set to 0.

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

Assuming the calculated speed is the speed from the current frame, then the speed used to calculate the position in the current frame should be the speed calculated from the previous frame. Therefore, before updating the speed, calculate the character's new position.

```c#
// move to new position
var collisionFlag = controller.Move(velocity * Time.deltaTime);
isOnGround = (collisionFlag & CollisionFlags.CollidedBelow) != 0;
```

`controller.Move` returns `CollisionFlags` which indicates the collision state, through which we can determine whether the character is standing on the ground.

Full code:


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
