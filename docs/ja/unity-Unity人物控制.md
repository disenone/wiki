---
layout: post
title: Unityのキャラクターコントロール
categories:
- unity
catalog: true
tags:
- dev
description: 人物の動作コントロールはゲームの中で非常に重要な部分であり、操作性の高いゲームはプレイヤーを引きつけることができます。ここでは、簡単な人物操作コントロールを試みてみます。キャラクターは基本的な移動、歩行、ジャンプを行うことができます。
figures:
- assets/img/2014-3-15-unity-3rdperson-control0/run_jump.gif
---

<meta property="og:title" content="Unity人物控制" />

![](assets/img/2014-3-15-unity-3rdperson-control0/run_jump.gif)

人物の動作制御はゲームにとって非常に重要な要素です。操作性の高いゲームはプレイヤーを魅了することができます。ここでは、基本的な移動を含む、簡単なキャラクターの操作制御を試みます。

##需要
人物操作の具体的な要件を考慮してください。

1. Moving, able to move on the surface of a rigid body, controlled by pressing the keys up, down, left, and right, without considering the acceleration and deceleration process for now.
異なる方向によって移動する速度は異なる可能性があります。例えば、後ろに移動する速度は前進する速度よりも遅いはずです。
3. Jumpボタンで操作されるジャンプ。キャラクターは一定の初速度で地面から離れ、ゆっくりと地面に戻ります。

大まかなアイデアは次のとおりです：人物の動きを記述するのに速さを使用し、速さの各方向成分を個別に計算でき、最後に速さに時間をかけることで人物の位置の変位が得られます。

##人物组件设置 --> キャラクターコンポーネントの設定
人物の台本を書く前に、操作や制御を行うための準備作業が必要です。関連する人物のコンポーネントを最初に設定してください：

人物をコントロールし、物理的な挙動を与えるために、人物に`Character Controller Component`を追加する必要があります。
人間に関する操作の入力を分けて作業して、入力を読み取り、初期処理を行った後に結果をキャラクターコントローラーに送り、この部分のスクリプトを`MyThirdPersonInput.cs`と名付けます。
3. The script responsible for controlling character movements is named `MyThirdPersonController.cs`.

配置後の結果はこうです：
![](assets/img/2014-3-15-unity-3rdperson-control0/setting.png)

##入力
入力は上下左右とジャンプです。方向は正規化処理を施す必要があります。

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

##移動やジャンプの記述
人物の行動を説明するために、移動速度、ジャンプ速度などの変数が必要です。移動は以下の変数で記述されます：

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

`[System.Serializable]`っていうのは、これらのパラメータをインスペクターに表示するためのものだね。ジャンプの説明は以下の通りだよ：

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
異なる方向の移動を説明するのに便利にするために、方向を前後、左右、上下の3つの成分に分けて解決します。

前後速度が異なる場合は、数値の正負に基づいて判断します：

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

ジャンプが少し難しいですが、現在のキャラクターの状態を判断する必要があります：

空中にいる場合は、重力を使って速度を計算します。
もし地上にいるのなら:
もしジャンプキーを押すと、速度はジャンプ初速度になります。
- - Otherwise, the velocity in the y-direction is 0.

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

##人物の位置を更新します。

計算された速度は、このフレームからの速度と仮定されるため、このフレームの計算された位置の速度は直前のフレームで計算されたものであるべきです。そのため、速度を更新する前に、まずキャラクターの新しい位置を計算してください：

```c#
// move to new position
var collisionFlag = controller.Move(velocity * Time.deltaTime);
isOnGround = (collisionFlag & CollisionFlags.CollidedBelow) != 0;
```

`controller.Move`は、衝突の状態を示す`CollisionFlags`を返します。この状態を通じて、キャラクターが地面に立っているかどうかがわかります。

完整代码：

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

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されました、[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指の遺漏を見つけてください。 
