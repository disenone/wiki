---
layout: post
title: Unity تحكم الشخصيات
categories:
- unity
catalog: true
tags:
- dev
description: توجه تحرك الشخصيات هو جزء مهم جدًا من الألعاب، فالألعاب ذات القابلية
  العالية للتحكم تستطيع جذب اللاعبين بشكل جيد. سأحاول هنا إنشاء نموذج بسيط لتحكم الشخصيات،
  حيث يستطيع الشخصيات إتمام الحركات الأساسية مثل المشي والقفز.
figures:
- assets/img/2014-3-15-unity-3rdperson-control0/run_jump.gif
---

<meta property="og:title" content="Unity人物控制" />

![](assets/img/2014-3-15-unity-3rdperson-control0/run_jump.gif)

سيطرة حركة الشخصية تعتبر جزءًا أساسيًا في الألعاب، فالألعاب ذات القابلية العالية في التحكم قادرة على جذب اللاعبين بشكل جيد. هنا أحاول تصميم نظام تحكم بسيط للشخصية، يمكن للشخصية أن تقوم بالحركات الأساسية مثل المشي والقفز.

##الطلب
قبل البدء، لننظر إلى احتياجات عملية تشغيل شخصياتنا:

المشي، القدرة على المشي على سطح الجسم الصلب، بالسيطرة عن طريق أزرار الاتجاه للأعلى، الأسفل، اليمين، واليسار، دون النظر إلى عمليات التسارع والتباطؤ.
سرعة الحركة يمكن أن تختلف في اتجاهات مختلفة، على سبيل المثال، يجب أن تكون الرجوع أبطأ من السير قدمًا
القفز، يتم التحكم فيها بواسطة زر القفز، حيث يغادر الشخص الأرض من الأعلى بسرعة محددة ويعود ببطء إلى الأرض.

الفكرة العامة هي استخدام السرعة لوصف حركة الشخصيات، حيث يمكن حساب مكونات السرعة في كل اتجاه بشكل مستقل، وفي النهاية يتم حساب انزياح موقع الشخصية بضرب السرعة في الزمن.

##إعدادات مكون الشخصية
قبل البدء في كتابة النصوص لإدارة الشخصيات، تحتاج إلى بعض الإعدادات الأولية، قم بتهيئة مكونات الشخصيات المتعلقة أولاً:

من أجل السيطرة على الشخصية ومنحها بعض السمات الفيزيائية الصلبة، يجب إضافة مكون تحكم الشخصية Character Controller Component للشخصية.
لتحقيق هيكلية أكثر وضوحًا، يجب تقسيم عمليات الشخصيات من الإدخال أولاً، ثم قراءة الإدخالات ومعالجتها أولياً لتمرير النتائج إلى متحكم الشخصيات، يتعين تسمية جزء النصوص هذا بـ "MyThirdPersonInput.cs".
تمت تسمية النص البرمجي الذي يتحكم فعليًا في حركة الشخصية بـ `MyThirdPersonController.cs`

نتائج التكوين كما يلي:
![](assets/img/2014-3-15-unity-3rdperson-control0/setting.png)

##ادخال
الإدخال هو الصعود والهبوط واليسار واليمين والقفز، يجب معالجة الاتجاه بطريقة موحدة:

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
نحتاج إلى استخدام بعض المتغيرات لوصف حركة الشخصيات، مثل سرعة الحركة وسرعة القفز وما إلى ذلك، حيث يتم وصف الحركة باستخدام المتغيرات التالية:

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

##سرعة تحلل
لتسهيل وصف الحركة في اتجاهات مختلفة، يمكن تقسيم الاتجاه إلى ثلاث مكونات: الأمام والخلف، اليمين واليسار، الأعلى والأسفل، ثم حل كلٍ على حدة.

السرعة تختلف من الأمام إلى الوراء، يتم تقييمها استنادًا إلى إيجابية أو سلبية القيمة:

```c#
if (velocity.z > 0)
    velocity.z *= movement.forwardSpeed;
else
    velocity.z *= movement.backwardSpeed;
```

المحتوى الذي يجب ترجمته هو: 
"左右速度一致："

```c#
velocity.x = inputMoveDirction.x * movement.sidewardSpeed;
```

القفز أكثر تعقيدًا قليلا، حيث يجب تقدير حالة الشخصية الحالية:

إذا كنت بالفعل في الهواء، حسب الجاذبية لحساب السرعة
إذا كنت على الأرض:
إذا قمت بالضغط على مفتاح القفز، ستكون السرعة هي سرعة القفز الابتدائية
إلا إذا كانت السرعة في الاتجاه y تساوي صفر

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

حساب السرعة المحسوبة يُفترض أن تكون السرعة من بدء هذا الإطار، وبالتالي يجب أن تكون سرعة حساب موقع هذا الإطار سرعة حُسِبَت من الإطار السابق، لذا قبل تحديث السرعة، يجب حساب موقع الشخصية الجديد:

```c#
// move to new position
var collisionFlag = controller.Move(velocity * Time.deltaTime);
isOnGround = (collisionFlag & CollisionFlags.CollidedBelow) != 0;
```

controller.Move ستعيد CollisionFlags لتعكس حالة الاصطدام، ويمكنك من خلال هذه الحالة معرفة ما إذا كان الشخص يقف على الأرض أم لا.

الرمز الكامل:

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


> هذا المنشور تمت ترجمته باستخدام ChatGPT، يرجى تقديم [**ردود فعل**](https://github.com/disenone/wiki_blog/issues/new)أشير إلى أي تغيير قد يكون غائبًا. 
