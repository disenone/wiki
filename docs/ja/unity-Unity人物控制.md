---
layout: post
title: Unityキャラクターコントロール
categories:
- unity
catalog: true
tags:
- dev
description: 人物の動作制御はゲームにおいて非常に重要な部分であり、操作性の高いゲームはプレイヤーを魅了することができます。ここでは、基本的な移動、歩行、ジャンプを含むシンプルなキャラクター操作制御を試みます。
figures:
- assets/img/2014-3-15-unity-3rdperson-control0/run_jump.gif
---

<meta property="og:title" content="Unity人物控制" />

![](assets/img/2014-3-15-unity-3rdperson-control0/run_jump.gif)

キャラクターの動作コントロールはゲームにおいて非常に重要な部分です。操作性の高いゲームはプレイヤーを魅了することができます。ここでは、基本的なキャラクター操作コントロールをシンプルに試みてみます。キャラクターは基本的な移動、すなわち歩行やジャンプを行うことができます。

##需要
もし、個別の必要性を考慮したい場合は、まず私たちの文字の操作を考えてみてください：

1. 行走は、剛体の表面を歩くことができ、ボタンの上下左右入力で制御されます。加速や減速の過程はまだ考慮していません。
異なる方向における移動速度は異なることがあります。例えば、後退は前進よりも遅いはずです。
3. ジャンプはジャンプボタンで制御され、キャラクターは一定の初速度で地面から離れ、ゆっくりと地面に戻ってきます。

大まかなアイディアは次のとおりです：人物の動きを速度で表します。速度の各方向成分は個別に計算でき、最終的に速度に時間をかけると人物の位置が移動します。

##人物コンポーネント設定
キャラクターの操作スクリプトを書く前に、いくつかの準備作業が必要です。まず、キャラクターの関連コンポーネントを設定しておきましょう。

人物を制御し、物理的な動作を構築するために、人物に`Character Controller Component`を追加する必要があります。
2. より明確な構造にするために、まずキャラクターに関する操作入力を分けて、入力を読み込み初期処理を行った後、その結果をキャラクターコントローラーに渡します。この部分のスクリプトは`MyThirdPersonInput.cs`と名付けます。
人物移動を制御するスクリプトを`MyThirdPersonController.cs`という名前にしています。

配置後の結果はこうなります：
![](assets/img/2014-3-15-unity-3rdperson-control0/setting.png)

##入力
入力は上下左右とジャンプです。方向は正規化される必要があります：

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

##移動とジャンプの説明
人物の行動を説明するために、移動速度、ジャンプ速度などの値を使う必要があります。移動速度を次のように表します：

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

`[System.Serializable]`はこれらのパラメータをInspectorに露出させるためのものです。ジャンプの説明は以下の通りです：

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
留一下這個想法有點具體化：移動時，為了更清楚地講解不同方向，我們把方向分成三個部分：前後、左右、上下，然後一一解決。

前後の速度が異なるため、数値の正負によって判断します：

```c#
if (velocity.z > 0)
    velocity.z *= movement.forwardSpeed;
else
    velocity.z *= movement.backwardSpeed;
```

左右の速度が一致。

```c#
velocity.x = inputMoveDirction.x * movement.sidewardSpeed;
```

ジャンプに少し手間がかかりますが、現在のキャラクターの状態を判断する必要があります。

- もし空中にいる場合は、重力を使って速度を計算します。
- 地面にいる場合：
- - ジャンプボタンを押すと、速度はジャンプの初速度です。
- - If not, the y-direction velocity is 0.

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

計算された速度は、このフレームからの速度と仮定されるため、このフレームの計算位置の速度は、直前のフレームで計算された速度となるため、速度を更新する前に、まずキャラクターの新しい位置を計算します。

```c#
// move to new position
var collisionFlag = controller.Move(velocity * Time.deltaTime);
isOnGround = (collisionFlag & CollisionFlags.CollidedBelow) != 0;
```

`controller.Move`は`CollisionFlags`を返し、衝突の状態を示します。この状態を通じて、キャラクターが地面に立っているかどうかを知ることができます。

完整なコード：

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


> この投稿はChatGPTを使って翻訳されましたので、[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指で何かの欠落を指摘してください。 
