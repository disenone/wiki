---
layout: post
title: Unity人物控制
categories:
- unity
catalog: true
tags:
- dev
description: 人物的動作控制是在遊戲中非常重要的一部分，操作性強的遊戲能夠很好地吸引玩家。在這裡，我嘗試做一個簡單的人物操作控制，人物能夠完成基本的移動，包括行走和跳躍。
figures:
- assets/img/2014-3-15-unity-3rdperson-control0/run_jump.gif
---

<meta property="og:title" content="Unity人物控制" />

![](assets/img/2014-3-15-unity-3rdperson-control0/run_jump.gif)

人物的動作控制是遊戲中非常重要的一部分，具有良好操作性的遊戲能夠有效吸引玩家。這裡我嘗試做一個簡單的人物操作控制，讓角色能夠完成基本的移動，包括行走和跳躍。

##需求
請先思考一下，我們對角色操作的具體需求：

行走，能在剛體的表面行走，由按鍵上下左右輸入來控制，暫不考慮加速減速過程。
行走的速度在不同方向上可以不同，例如後退應該比前進慢。
跳躍，由跳按鈕控制，人物以一定初始速度從上離開地面，並慢慢回落到地面。

大致的想法就是：使用速度來描述角色的移動，可以分別計算速度在每個方向上的分量，最後將速度乘以時間就能獲得角色的位置偏移。

##人物組件設置
在為角色撰寫腳本以進行操作控制之前，需要進行一些準備工作，先配置好角色相關的組件：

為了控制人物並使其在物理層面展現一些剛性特性，需要為人物添加一個「Character Controller Component」。
為了讓結構更清晰，先將有關人物操作的輸入分離出來，讀取輸入並進行初步處理後傳遞給人物控制器，將這部分的腳本命名為`MyThirdPersonInput.cs`；
將該腳本命名為`MyThirdPersonController.cs`，這是用來真正控制角色移動的。

配置完成後的結果是這樣：
![](assets/img/2014-3-15-unity-3rdperson-control0/setting.png)

##輸入
輸入就是上下左右和跳躍，方向需要做一個歸一化的處理：

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

##描述移动和跳跃
我哋需要一啲變量嚟描述人物嘅動作，例如移動速度，跳躍速度等等，移動係用以下變量描述：

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

`[System.Serializable]`是為了讓這些參數顯示在檢視器上。跳躍的描述如下：

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

##分解速度
為了更方便描述不同方向的移動，將方向分成三個分量：前後、左右、上下，分別求解。

前後速度不同，根據數值的正負判斷：

```c#
if (velocity.z > 0)
    velocity.z *= movement.forwardSpeed;
else
    velocity.z *= movement.backwardSpeed;
```

左右速度一致：

```c#
velocity.x = inputMoveDirction.x * movement.sidewardSpeed;
```

跳躍有點困難，需要判斷當前角色的狀態：

- 如果已經在空中，用重力計算速度
- 如果在地上：
- - 如果按下跳躍鍵，速度為跳躍初始速度
否則 y 方向速度為0。

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

##更新人物位置

將計算出的速度假設為從本幀開始的速度，那麼本幀計算位置的速度應該是前一幀計算出的，因此在更新速度前，先計算角色的新位置：

```c#
// move to new position
var collisionFlag = controller.Move(velocity * Time.deltaTime);
isOnGround = (collisionFlag & CollisionFlags.CollidedBelow) != 0;
```

`controller.Move` 會返回 `CollisionFlags` 來表示碰撞的狀態，通過這個狀態就可以知道人物是不是站在地面上。

完整代碼：

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

--8<-- "footer_tc.md"


> 此帖子是使用 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
