---
layout: post
title: 통합 캐릭터 제어
categories:
- unity
catalog: true
tags:
- dev
description: 인물의 움직임 제어는 게임에서 매우 중요한 부분이며 조작성이 우수한 게임은 플레이어를 매혹할 수 있습니다. 여기서 나는 간단한
  인물 조작 제어를 시도해보겠습니다. 인물이 기본적인 이동을 할 수 있도록 만들어보겠습니다. 걷기와 뛰기를 포함합니다.
figures:
- assets/img/2014-3-15-unity-3rdperson-control0/run_jump.gif
---

<meta property="og:title" content="Unity人物控制" />

![](assets/img/2014-3-15-unity-3rdperson-control0/run_jump.gif)

캐릭터의 동작 제어는 게임에서 매우 중요한 부분이며 조작이 용이한 게임은 플레이어를 잘 끌어들일 수 있습니다. 여기서 제가 간단한 캐릭터 조작 제어를 시도해보겠습니다. 캐릭터는 기본 이동, 걷기 및 뛰기를 완성할 수 있습니다.

##요구 사항
먼저 우리 캐릭터 조작의 구체적인 요구사항을 고려해 봅시다:

1. 행동, 강체 표면 위를 이동할 수 있으며, 상하좌우 입력으로 제어되며, 가속 및 감속 과정은 현재 고려하지 않습니다.
발걸음 속도는 서로 다를 수 있어. 예를 들어서 후퇴는 전진보다 더 느려야 해.
3. 점프는 jump 버튼으로 제어되며, 캐릭터는 일정한 초기 속도로 지면을 떠나며 천천히 다시 땅으로 내려온다.

대략적인 아이디어는 다음과 같습니다: 인물의 움직임을 속도로 표현하되, 속도는 각 방향별로 계산할 수 있으며, 최종적인 속도에 시간을 곱하면 인물의 위치 변위가 됩니다.

##인물 구성 요소 설정
특정 인물을 조작하고 제어하기 위해 대본을 작성하기 전에 몇 가지 준비 작업이 필요합니다. 먼저 인물의 관련 구성 요소를 미리 설정해야 합니다:

인물을 제어하고 인물에 약간의 물리적인 강도를 부여하기 위해 인물에 'Character Controller Component'를 추가해야합니다.
인물 작업 관련 부분을 먼저 분리하여 구조를 더 명확하게합니다. 입력을 읽고 초기 처리를 한 다음 결과를 인물 컨트롤러에 전달합니다. 이 부분의 스크립트 이름을 `MyThirdPersonInput.cs`로 지정하십시오.
실제로 캐릭터 이동을 제어하는 스크립트는 `MyThirdPersonController.cs`로 명명되어 있습니다.

구성 후 결과는 다음과 같습니다:
![](assets/img/2014-3-15-unity-3rdperson-control0/setting.png)

##입력
입력은 상하좌우와 점프이며, 방향은 정규화 처리를 해야합니다.

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

##이동 및 점프 설명
우리는 캐릭터의 행동을 설명하기 위해 몇 가지 변수가 필요합니다. 예를 들어 이동 속도, 점프 속도 등을 설명하기 위해 아래와 같은 변수를 사용합니다:

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

`[System.Serializable]` 은 이러한 매개변수를 Inspector에 노출하기 위한 것입니다. 점프의 설명은 다음과 같습니다:

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

##분해 속도
서로 다른 방향의 이동을 설명하기 쉽게 하기 위해 방향을 세 가지 성분으로 나눕니다: 앞뒤, 좌우, 상하에 대해 각각 해결합니다.

전후 속도가 다르므로 숫자의 양수와 음수에 따라 판단하세요:

```c#
if (velocity.z > 0)
    velocity.z *= movement.forwardSpeed;
else
    velocity.z *= movement.backwardSpeed;
```

왼쪽과 오른쪽 속도 일치:

```c#
velocity.x = inputMoveDirction.x * movement.sidewardSpeed;
```

점프가 조금 까다로운데, 현재 캐릭터의 상태를 판단해야 해요:

만약 이미 공중에 있다면 중력을 이용해서 속도를 계산해.
만약 지상에 있다면:
- - 점프 키를 누르면 점프 초기 속도가 됩니다.
그렇지 않으면 y축 방향 속도는 0입니다.

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

##인물 위치를 업데이트합니다.

계산된 속도는 이 프레임부터의 속도로 가정되므로 이 프레임의 위치를 계산하는 속도는 이전 프레임에서 계산된 속도여야 합니다. 따라서 속도를 업데이트하기 전에 먼저 캐릭터의 새로운 위치를 계산합니다.

```c#
// move to new position
var collisionFlag = controller.Move(velocity * Time.deltaTime);
isOnGround = (collisionFlag & CollisionFlags.CollidedBelow) != 0;
```

`controller.Move` 함수는 충돌 상태를 나타내는 `CollisionFlags`를 반환합니다. 이 상태를 통해 캐릭터가 지면 위에 서 있는지 여부를 알 수 있습니다.

전체 코드:

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

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT를 사용하여 번역되었습니다. 피드백은 [**여기**](https://github.com/disenone/wiki_blog/issues/new)어떤 빠진 부분도 가리키다. 
