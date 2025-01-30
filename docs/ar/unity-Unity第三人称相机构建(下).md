---
layout: post
title: بناء آلية الشخص الثالث في Unity (الجزء الثاني)
categories:
- unity
catalog: true
tags:
- dev
description: أريد إنشاء كاميرا بزاوية ثالثة في Unity، وسلوك الكاميرا مستوحى من كاميرا
  زاوية ثالثة في "عالم المحترفين". هنا لحل مشكلة الجسم الصلب للكاميرا.
---

<meta property="og:title" content="Unity第三人称相机构建(下)" />

الجزء السابق انتهى عند [دوران الكاميرا](unity-Unity第三人称相机构建(上).md)، لذا فإن المشكلة التي نحتاج إلى حلها الآن هي صلابة الكاميرا، كيف يمكننا القيام بذلك؟

الكاميرا الصلابة
--------------
استعراض المتطلبات المذكورة سابقًا:

4. عجلة الماوس: تتحكم في قرب وبعد الكاميرا
الكاميرا لا يمكنها اختراق أي جسم صلب
عندما تتحرك الكاميرا بعيدًا عن جسم صلب تصادمت به، تعود تدريجياً إلى المسافة الأصلية.
إذا تم تحريك الكاميرا باستخدام عجلة الماوس عند التصادم مع جسم صلب، يجب على الكاميرا الاستجابة فورًا، وبعد ذلك لن يحدث النقطة 6؛ وبعد التصادم مع الأرض، لا يمكن التلاعب بالتكبير.
8. الكاميرا تصطدم بالأرض أثناء الدوران، وتتوقف عن الدوران لأعلى وأسفل حول الشخص، وتتحول للدوران لأعلى وأسفل حول نفسها، بينما يبقى الدوران إلى اليسار واليمين حول الشخص.


هذه النقاط تعني أنه عند اصطدام الكاميرا بجسم صلب، سيتم إجبارها على الاقتراب من الشخص. لذلك نريد عندما تبتعد الكاميرا أن تعود ببطء إلى المسافة الأصلية. ولكن إذا تم الاقتراب تلقائيًا وبعد ذلك تمت إضافة الإقتراب يدويًا باستخدام العجلة، فهذا يعني أن الكاميرا ابتعدت عن الجسم الذي اصطدمت به، وبالتالي المسافة المقربة هذه هي المسافة الفعلية للكاميرا. دعونا نستعرض هذه المتطلبات خطوة بخطوة.

تحكم بالعجلة
----------
تحكم عجلة تمرير الماوس بسيط جدًا، كل ما عليك معرفته هو كيفية الحصول على معلومات العجلة وهو `Input.GetAxis("Mouse ScrollWheel")`، ثم قم بتحديد الحد الأقصى والحد الأدنى للمسافة وسيكون كل شيء على ما يرام:

```c#
public float mouseWheelSensitivity = 2; // control zoom speed
public int mouseWheelZoomMin = 2;       // min distance
public int mouseWheelZoomMax = 10;      // max distance
float curDistance = 5F;
float zoom = Input.GetAxis("Mouse ScrollWheel");
if (zoom != 0F)
{
    float distance = curDistance;
    distance -= zoom * mouseWheelSensitivity;
    distance = Math.Min(mouseWheelZoomMax, Math.Max(mouseWheelZoomMin, distance));
    return distance;
}
```

هنا `playerTransform` تشير إلى الشخصية.

لا يمكن اختراق أي جسم صلب.
--------------------
هذا يتطلب الكشف عن تلامس الكاميرا مع الجسم الصلب، وهناك دالة يمكن أن تحقق هذه الوظيفة:

```c#
static bool Raycast(Ray ray, RaycastHit hitInfo, float distance = Mathf.Infinity, int layerMask = DefaultRaycastLayers);
```

يمكنك الرجوع إلى [Reference](http://docs.unity3d.com/Documentation/ScriptReference/Physics.Raycast.html)يمكننا تحقيق كشف التصادم بهذه الطريقة:

```c#
RaycastHit hitInfo;
if (Physics.Raycast(playerTransform.position, desiredPosition - playerTransform.position,
    out hitInfo, (playerTransform.position - desiredPosition).magnitude, 1))
{
    curDistance = hitInfo.distance;
}
```

`targetPosition` هو موقع التصادم، يمكنك ضبط موضع الكاميرا على موقع التصادم.

离开刚体后，慢慢回到原来的距离上  
بعد الابتعاد عن الجسم الصلب، عد ببطء إلى المسافة الأصلية.
---------------------------------
لإكمال هذه الوظيفة، يجب أولاً تسجيل المسافة التي ينبغي أن يكون فيها الكاميرا (`desiredDistance`) والمسافة الحالية (`curDistance`) بشكل منفصل، ثم حفظ نتيجة عملية العجلة باستخدام `desiredDistance`، وبعد ذلك حساب المسافة الجديدة للجسم بناءً على الاصطدام؛
عندما يتم اكتشاف أن الكاميرا انفصلت عن الجسم الثابت، أو تصادمت مع جسم آخر بعيد، لا يمكن تعيين موقع التصادم مباشرة للكاميرا، بل يجب استخدام سرعة الحركة للتحرك نحو المسافة الجديدة. نبدأ بالحصول على المسافة الجديدة:

```c#
float newDistance = desiredDistance;
RaycastHit hitInfo;
if (Physics.Raycast(playerTransform.position, desiredPosition - playerTransform.position,
    out hitInfo, (playerTransform.position - desiredPosition).magnitude, 1))
{
    newDistance = hitInfo.distance;
}
```

إذن كيف يمكننا判断 أن الكاميرا تتحرك إلى مسافة أبعد؟ يمكننا استخدام `newDistances` ومقارنتها بالمسافة الحالية:

```c#
// الانتقال إلى مسافة أقرب
if (newDistance < curDistance)
{
    curDistance = newDistance;
}
نقل إلى مسافات أبعد
else if(newDistance > curDistance)
{
}
```

لذا، عندما نحكم على الانتقال لمسافة أبعد، يصبح الأمر واضحًا جدًا، فقط نضيف سرعة للتنقل:

```c#
curDistance = Math.Min(curDistance + Time.deltaTime * autoZoomOutSpeed, newDistance);

```
لقد أنهينا السلوك العام للكاميرا، لا يزال هناك بعض التفاصيل التي تحتاج إلى معالجة.

عندما يلامس الجسم الصلب، تقترب العجلة ولا يحدث أي تغيير في مستوى الأرض.
------------------
هناك شروطان:

1. عند الاصطدام بالجسم الصلب، يمكن الاقتراب فقط، ولا يمكن الابتعاد.
2. عند ملامسة الأرض لا يمكن تغيير الحجم

يُرجى ترجمة هذه النص إلى اللغة العربية:
"أولاً، استخدم المتغيرات لحفظ حالة اصطدام الكاميرا:"

```c#
bool isHitGround = false;       // تشير إلى ما إذا كانت هناك اصطدام مع الأرض
bool isHitObject = false;       // يشير إلى ما إذا كان هناك تصادم مع الجسم الصلب (باستثناء الأرض)
```

أضف شرطًا عند تحديد تكبير عجلة التمرير:

```c#
if (zoom != 0F && (!isHitGround || (isHitObject && zoom > 0F)) )
{
    // calculate distance
}
```

碰到地面绕自身上下旋转
-----------------
هذا الفعل يتطلب بعض التعقيدات، لأنه في هذه اللحظة، لم يعد افتراضنا بأن الكاميرا موجهة نحو الشخص صحيحاً. هنا، نقسم الأمر إلى متجهين: **اتجاه الكاميرا نفسها (`desireForward`)** و**الاتجاه من الشخص إلى الكاميرا (`cameraToPlayer`)**، حيث يتم حساب قيم هذين المتجهين بشكل منفصل. الأول يحدد اتجاه الكاميرا، بينما الثاني يحدد موقع الكاميرا. لتسهيل الأمر، دعنا نعود إلى [الحلقة السابقة](unity-Unity第三人称相机构建(上)تم تقسيم وظيفة الدوران في (.md) إلى دوران X (`RotateX`) ودوران Y (`RotateY`). لذا، عند حساب `RotateY` لـ `cameraToPlayer`، قم بإضافة الشرط:

```c#
if ((!isHitGround) || 
    (isHitGround && transform.forward.y <= cameraToPlayer.y && yAngle > 0))
{
    cameraToPlayer = RotateY(cameraToPlayer, playerTransform.up, 
        transform.right, yAngle);
}
```

هذا الشرط ينقسم إلى جزئين:

- لم تلامس الأرض
- اصطدم بالأرض، لكنه مستعد لمغادرة الأرض

ثم استخدم `cameraToPlayer` لحساب موضع الكاميرا:

```c#
transform.position = playerTransform.position - cameraToPlayer * curDistance;
```

وعند الحاجة (أي عند ملامسة الأرض)، يتم حساب اتجاه الكاميرا:

```c#
if (!isHitGround)
{
    transform.LookAt(playerTransform);
}
else
{
    desireForward = RotateX(desireForward, playerTransform.up, xAngle);
    desireForward = RotateY(desireForward, playerTransform.up, transform.right, yAngle);
    transform.forward = desireForward;
}
```

لقد حققنا جميعًا هذا السلوك للكاميرا.

الكود الكامل:

```c#
using UnityEngine;
using System;
using System.Collections;

// use a forward vector and distance to describe the camera position
public class MyThirdPersonCamera : MonoBehaviour {

    private Transform playerTransform;      // reference to player

    public float mouseWheelSensitivity = 3; // control zoom speed
    public int mouseWheelZoomMin = 2;       // min distance
    public int mouseWheelZoomMax = 10;      // max distance

    public float rotateSpeed = 5F;          // speed of rotate around player    
    public float autoZoomOutSpeed = 10F;    // speed of auto zoom out, camera will auto zoom out 
                                            // to pre distance when stop colliding object
    float curDistance = 5F;                 // distance to player
    float desiredDistance = 5F;             // distance should be      
    bool isHitGround = false;               // hit ground flag
    bool isHitObject = false;               // hit object(except ground) flag
    
    // Use this for initialization
    void Awake ()
    {
        playerTransform = transform.parent;
    }

    void Start () 
    {
        transform.position = playerTransform.position - playerTransform.forward 
            * curDistance;
        transform.LookAt(playerTransform);
        
    }
    
    // Update is called once per frame
    void Update () 
    {
        Vector3 cameraToPlayer = 
            (playerTransform.position - transform.position).normalized;

        Vector3 desireForward = transform.forward;

        // get new distance of zoom
        desiredDistance = ZoomIt(curDistance, desiredDistance);

        float xAngle, yAngle;
        bool isRightDown;

        // get mouse LB, RB status
        GetMouseButtonStatus(out xAngle, out yAngle, out isRightDown);

        // rotate camera by x-axis movement
        cameraToPlayer = RotateX(cameraToPlayer, playerTransform.up, xAngle);

        // if RB on, change player orientation
        if (isRightDown)
        {
            playerTransform.forward = Vector3.Normalize(new Vector3(cameraToPlayer.
                x, 0, cameraToPlayer.z));
        }

        // rotate camera by y-axis, if camera is not on ground or camera is going to leave ground
        if ((!isHitGround) 
        || (isHitGround && transform.forward.y <= cameraToPlayer.y && yAngle > 0))
        {
            cameraToPlayer = RotateY(cameraToPlayer, playerTransform.up, transform.
                right, yAngle);
        }

        // detect collision of camera to rigid body, get the distance camera should be
        float newDistance = DealWithCollision(playerTransform.position, 
            -cameraToPlayer, desiredDistance,ref isHitGround, ref isHitObject);

        // check the distance
        if (newDistance <= curDistance)
        {
            curDistance = newDistance;
        }
        else
        {
            // now moving to farther position, use a speed to move it
            curDistance = Math.Min(curDistance + Time.deltaTime * autoZoomOutSpeed, 
                newDistance);
        }

        // now calculate the position
        transform.position = playerTransform.position - cameraToPlayer * curDistance;

        // calculate the camera forward, if on ground, camera will rotate on self.Space
        if (!isHitGround)
        {
            transform.LookAt(playerTransform);
        }
        else
        {
            desireForward = RotateX(desireForward, playerTransform.up, xAngle);
            desireForward = RotateY(desireForward, playerTransform.up, transform.
                right, yAngle);
            transform.forward = desireForward;
        }
    }

    // zoom in and zoom out
    float ZoomIt(float curDistance, float desiredDistance)
    {
        float zoom = Input.GetAxis("Mouse ScrollWheel");

        //  zoom when hit rigid body and zoom in, or not on ground
        if (zoom != 0F && (!isHitGround || (isHitObject && zoom > 0F)) )
        {
            float distance = curDistance;

            distance -= zoom * mouseWheelSensitivity;
            distance = Math.Min(mouseWheelZoomMax, Math.Max(mouseWheelZoomMin, distance));

            return distance;
        }
        return desiredDistance;
    }

    // rotate oldPosition around a axis starting at axisPosition
    Vector3 RotateAroundAxis(Vector3 point, float angle, Vector3 axis, Vector3 axisPosition)
    {
        Quaternion rotation = Quaternion.AngleAxis(angle, axis);
        Vector3 offset = point - axisPosition;
        return axisPosition + (rotation * offset);
    }

    void GetMouseButtonStatus(out float x, out float y, out bool isRightDown)
    {
        x = y = 0F;
        isRightDown = false;
        if (Input.GetMouseButton(0) ^ Input.GetMouseButton(1))
        {
            x = Input.GetAxis("Mouse X") * rotateSpeed;
            y = -Input.GetAxis("Mouse Y") * rotateSpeed;
            if (Input.GetMouseButton(1))
            {
                isRightDown = true;
            }
        }
    }

    // rotate vectorP2C(player to camera) around up while mouse x is on, return true if do rotate
    Vector3 RotateX(Vector3 vectorP2C, Vector3 up, float angle)
    {
        Vector3 newVector = vectorP2C;
        if (angle != 0F)
        {
            newVector = RotateAroundAxis(newVector, angle, up, Vector3.zero);
        }
        return newVector;
    }

    // rotate vectorP2C(player to camera) around right while mouse y is on, return true is do rotate
    Vector3 RotateY(Vector3 vectorP2C, Vector3 up, Vector3 right, float angle)
    {
        Vector3 newVector = vectorP2C;
        if (angle != 0F)
        {
            if ((Vector3.Dot(vectorP2C, up) >= -0.99F || angle < 0)
                && (Vector3.Dot(vectorP2C, up) <= 0.99F || angle > 0))
            {
                newVector = RotateAroundAxis(newVector, angle, right, Vector3.zero);
            }
        }
        return newVector;
    }

    // return distance if no collision, else return distance to rigid body
    float DealWithCollision(Vector3 origin, Vector3 direction, float distance, 
        ref bool ishitGround, ref bool ishitObject)
    {
        // collision detection
        RaycastHit hitInfo;
        float newDistance = distance;
        if (Physics.Raycast(playerTransform.position, direction, out hitInfo, desiredDistance, 1))
        {
            if (hitInfo.collider is TerrainCollider)
            {
                ishitGround = true;
                ishitObject = false;
            }
            else
            {
                ishitObject = true;
                ishitGround = false;
            }
            newDistance = hitInfo.distance;
        }
        else
        {
            ishitGround = ishitObject = false;
        }

        return newDistance;
    }
}
```

--8<-- "footer_ar.md"


> هذا المنشور تمت ترجمته باستخدام ChatGPT، يرجى تقديم [**تعليقات**](https://github.com/disenone/wiki_blog/issues/new)الرجاء تحديد أي اهتمامات أو نقاط يمكن أن تكون قد تم تجاهلها. 
