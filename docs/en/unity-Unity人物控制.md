---
layout: post
title: Unity Character Control
categories:
- unity
catalog: true
tags:
- dev
description: The control of character actions is a crucial part of games, as games
  with good operability can attract players well. Here I will try to create a simple
  character control system, where characters can perform basic movements, including
  walking and jumping.
figures:
- assets/img/2014-3-15-unity-3rdperson-control0/run_jump.gif
---

<meta property="og:title" content="Unity人物控制" />

![](assets/img/2014-3-15-unity-3rdperson-control0/run_jump.gif)

Character movement control is a crucial aspect of games, and games with strong interactivity can effectively attract players. Here, I will attempt to create a simple character control system that allows for basic movement, including walking and jumping.

##Demand
First, let's consider the specific requirements for manipulating our characters:

Move around, able to walk on the surface of the rigid body, controlled by pressing keys for up, down, left, and right movements, without considering acceleration and deceleration for now.
The speed of movement can vary in different directions, for example, moving backward should be slower than moving forward.
3. Jumping is controlled by the jump key, where the character leaves the ground with a certain initial speed and slowly falls back to the ground.

So, the general idea is to use speed to describe the movement of characters, the speed components in each direction can be calculated separately, and finally, multiplying the speed by time gives the character's position offset.

##Setting of character components
Before writing a script to control characters, some preparations are needed. First, configure the relevant components of the characters.

In order to control characters and give them some rigid physical behavior, you need to add a "Character Controller Component" to the characters.
In order to make the structure clearer, separate the input related to the characters first, read the input, process it initially, and then pass the results to the character controller. Name this part of the script as 'MyThirdPersonInput.cs'.
3. The script that truly controls character movement is named `MyThirdPersonController.cs`.

The result after configuration is as follows:
![](assets/img/2014-3-15-unity-3rdperson-control0/setting.png)

##Input
The input consists of moving in all directions and jumping, the directions need to undergo a normalization process:

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

##Describing movement and jumping
We need to use some variables to describe the character's actions, such as movement speed, jumping speed, etc. The movement is described using the variables below:

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

##Decomposition rate
To facilitate describing movement in different directions, divide the directions into three components: front/back, left/right, up/down, and solve them separately.

The front and rear speeds are different, judged by the sign of the values:

```c#
if (velocity.z > 0)
    velocity.z *= movement.forwardSpeed;
else
    velocity.z *= movement.backwardSpeed;
```

Consistent speed on both sides:

```c#
velocity.x = inputMoveDirction.x * movement.sidewardSpeed;
```

Jumping is a bit tricky as you need to determine the current state of the character:

If already in the air, calculate speed using gravity.
- If on the ground:
- If the jump key is pressed, the speed is the initial jumping speed.
- Otherwise, the velocity in the y direction will be 0.

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

##Update character location.

The calculated speed is assumed to be the speed from the current frame, so the speed for calculating the position in this frame should be the speed calculated from the previous frame. Therefore, before updating the speed, first calculate the new position of the character:

```c#
// move to new position
var collisionFlag = controller.Move(velocity * Time.deltaTime);
isOnGround = (collisionFlag & CollisionFlags.CollidedBelow) != 0;
```

The `controller.Move` method will return a `CollisionFlags` to indicate the collision status, allowing us to determine if the character is standing on the ground.

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

--8<-- "footer_en.md"


> This post has been translated using ChatGPT, please provide [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Please point out any omissions. 
