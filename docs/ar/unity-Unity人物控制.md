---
layout: post
title: تحكم شخصيات Unity
categories:
- unity
catalog: true
tags:
- dev
description: تحكم حركات الشخصيات هو جزء مهم جداً في الألعاب، حيث إن الألعاب ذات التحكم
  السلس تستطيع جذب اللاعبين بشكل جيد. هنا سأحاول إنشاء تحكم بسيط لشخصية، حيث يمكن
  للشخصية تنفيذ حركات أساسية مثل المشي والقفز.
figures:
- assets/img/2014-3-15-unity-3rdperson-control0/run_jump.gif
---

<meta property="og:title" content="Unity人物控制" />

![](assets/img/2014-3-15-unity-3rdperson-control0/run_jump.gif)

تحكم حركة الشخصيات هو جزء مهم جدًا في الألعاب، والألعاب التي تتمتع بتجربة تحكم جيدة قادرة على جذب اللاعبين بشكل كبير. في هذا السياق، سأحاول تصميم نظام تحكم بسيط للشخصية يمكنها القيام بالحركات الأساسية، مثل المشي والقفز.

##طلب
دعونا نفكر أولاً في متطلبات تحكم الشخصيات لدينا بشكل محدد:

المشي، القدرة على المشي على سطح الجسم الصلب، بالتحكم من خلال الأزرار للأعلى والأسفل واليسار واليمين، دون النظر في عملية التسارع والتباطؤ في الوقت الحالي.
سرعة المشي يمكن أن تختلف في اتجاهات مختلفة، مثل أن الحركة للخلف يجب أن تكون أبطأ من الحركة للأمام.
3. القفز، يتم التحكم فيه بواسطة زر القفز، حيث يغادر الشخص الأرض بسرعة ابتدائية معينة، ثم ينزل ببطء إلى الأرض.

الفكرة العامة هي استخدام السرعة لوصف حركة الشخصيات، حيث يمكن حساب مكونات السرعة في كل اتجاه بشكل منفصل، وفي النهاية، يتم تحديد تحرك الشخصية من خلال ضرب السرعة في الزمن.

##إعدادات مكون الشخصيات
قبل كتابة脚本操作角色控制，需要进行一些准备工作，先将角色的相关组件配置好：

من أجل التحكم في الشخصيات وضمان وجود بعض التصرفات الفيزيائية الصارمة للشخصيات، يتعين إضافة 'مكوِّن تحكم الشخصية' إلى الشخصية.
2. من أجل أن تكون البنية أكثر وضوحًا، سيكون من الأفضل فصل مدخلات العمليات المتعلقة بالأشخاص. بعد قراءة المدخلات ومعالجتها أوليًا، يتم تمرير النتائج إلى وحدة التحكم في الشخصيات، وسنطلق على هذا الجزء من السكريبت اسم `MyThirdPersonInput.cs`؛
3. السكربت الذي يتحكم فعليًا في حركة الشخصيات يُسمى `MyThirdPersonController.cs`

النتيجة بعد الإعداد هي كما يلي:
![](assets/img/2014-3-15-unity-3rdperson-control0/setting.png)

##إدخال
الإدخال هو الصعود والهبوط واليمين واليسار والقفز، والاتجاه يتطلب معالجة توحيدية:

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

##وصف الحركة والقفز
نحتاج إلى استخدام بعض المتغيرات لوصف حركة الشخصيات، مثل سرعة الحركة، سرعة القفز، وغيرها. يتم وصف الحركة بالمتغيرات التالية:

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

`[System.Serializable]`تستخدم لتعريض هذه المعلمات في مراقب العناصر. وصف القفز كالتالي:

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

##سرعة التحلل
为了方便描述不同方向的移动，把方向分成三个分量：前后、左右、上下，分别求解。

الأمام والخلف سرعات مختلفة، يتم الحكم بناءً على قيمة العدد سواء كانت موجبة أو سالبة:

```c#
if (velocity.z > 0)
    velocity.z *= movement.forwardSpeed;
else
    velocity.z *= movement.backwardSpeed;
```

سرعة متساوية من الجهتين:

```c#
velocity.x = inputMoveDirction.x * movement.sidewardSpeed;
```

القفز يمكن أن يكون معقدًا قليلاً، حيث يتعين تقدير حالة الشخصية الحالية:

إذا كنت محلقًا بالفعل، فاحسب السرعة باستخدام الجاذبية
- إذا كان على الأرض:
- - إذا تم ضغط زر القفز، فإن السرعة ستكون سرعة القفز الابتدائية.
- - وإلا فإن سرعة الحركة في الاتجاه y تساوي 0

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

##تحديث موقع الشخصيات

假定速度计算是从当前帧开始的，那么当前位置的速度应该是根据前一帧得出的。因此，在更新速度之前，首先需要计算角色的新位置：

```c#
// move to new position
var collisionFlag = controller.Move(velocity * Time.deltaTime);
isOnGround = (collisionFlag & CollisionFlags.CollidedBelow) != 0;
```

`controller.Move` ستعيد `CollisionFlags` للإشارة إلى حالة التصادم، ومن خلال هذه الحالة يمكن معرفة ما إذا كان الشخص واقفًا على الأرض.

الكود الكامل:

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

--8<-- "footer_ar.md"


> هذه الرسالة تم ترجمتها باستخدام ChatGPT ، الرجاء تقديم [**ردود فعل**](https://github.com/disenone/wiki_blog/issues/new)أشِر إلى أي نقاط تم إغفالها. 
