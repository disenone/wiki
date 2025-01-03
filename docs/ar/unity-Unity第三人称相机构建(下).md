---
layout: post
title: Unity تخطيط الكاميرا من شخصية الجهة الثالثة (الجزء الثاني)
categories:
- unity
catalog: true
tags:
- dev
description: أرغب في إنشاء كاميرا منظور ثالث في Unity، حيث يكون سلوك الكاميرا مستوحى
  من كاميرا منظور ثالث في "World of Warcraft". سأعمل هنا على حل مشكلة الجسم الصلب
  للكاميرا.
---

<meta property="og:title" content="Unity第三人称相机构建(下)" />

(unity-Unity第三人称相机构建(上).md)، لذا المشكلة التي نحتاج الآن إلى حلها هي صلابة الكاميرا، كيف يمكننا القيام بذلك؟

الكاميرا الصلبة
--------------
مراجعة المتطلبات التي تم ذكرها سابقاً:

عصا التمرير في الفأرة: تحكم في اتجاه الكاميرا من القريب إلى البعيد
الكاميرا لا يمكنها اختراق أي جسم صلب
عندما تنفصل الكاميرا عن الجسم الصلب الذي اصطدمت به، تعود ببطء إلى المسافة الأصلية.
إذا تعرضت الكاميرا لاصطدام مع جسم صلب، فيجب أن تستجيب الكاميرا فورًا عند استخدام عجلة الماوس لتكبيرها، وبعد ذلك لن تحدث النقطة رقم 6؛ لا يمكن تغيير حجم الكاميرا بعد اصطدامها بالأرض.
عندما ارتطمت الكاميرا بالأرض أثناء الدوران، توقفت عن التدوير حول الشخص بشكل عمودي وبدأت بالدوران حول نفسها بشكل عمودي، ولازالت تدور يمينًا ويسارًا حول الشخص.


هذه النقاط تعني: عندما تصطدم الكاميرا بجسم صلب، ستضطر للتقرب من مسافة الشخص، إذن نريد الكاميرا أن تعود ببطء إلى المسافة الأصلية عندما تبتعد؛ ولكن إذا تم سحب المسافة يدوياً بواسطة العجلة بعد التقرب التلقائي، فإن ذلك يعني أن الكاميرا ابتعدت عن الجسم المصطدم، وبالتالي يكون هذا التقرب هو المسافة الفعلية للكاميرا. والآن سنقوم بتحليل هذه الاحتياجات بعناية.

التحكم بالعجلة
----------
التحكم في عجلة التمرير بالماوس بسيط للغاية، فقط تحتاج إلى معرفة كيفية الحصول على معلومات عجلة التمرير بواسطة `Input.GetAxis("Mouse ScrollWheel")` وتحديد القيم القصوى والصغرى للمسافة، ثم تمام:

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

هنا `playerTransform` يشير إلى الشخصية.

يتعذر اختراق أي جسم صلب
--------------------
هذا يتطلب اختبار تواصل الكاميرا مع الجسم الصلب، هناك وظيفة واحدة تستطيع تنفيذ هذه الوظيفة:

```c#
static bool Raycast(Ray ray, RaycastHit hitInfo, float distance = Mathf.Infinity, int layerMask = DefaultRaycastLayers);
```

يرجى الرجوع إلى [المرجع](http://docs.unity3d.com/Documentation/ScriptReference/Physics.Raycast.html)نستطيع تحقيق كشف التصادم بهذه الطريقة:

```c#
RaycastHit hitInfo;
if (Physics.Raycast(playerTransform.position, desiredPosition - playerTransform.position,
    out hitInfo, (playerTransform.position - desiredPosition).magnitude, 1))
{
    curDistance = hitInfo.distance;
}
```

`targetPosition` هو موقع الاصطدام، يمكنك ضبط موقع الكاميرا إلى موقع الاصطدام.

عندما يتحرك الكائن الصلب بعيداً ثم يتجه ببطء للمسافة الأصلية
---------------------------------
لإكمال هذه الوظيفة، يجب أولاً تسجيل المسافة المطلوبة للكاميرا (`desiredDistance`) والمسافة الحالية (`curDistance`) على حدة، ثم تُخزن نتيجة تشغيل عجلة التمرير باستخدام `desiredDistance`، ومن ثم يتم حساب المسافة الجديدة للجسم وفقًا لعمليات الاصطدام؛
عند اكتشاف أن الكاميرا انفصلت عن الهيكل الصلب أو اصطدمت بهيكل صلب أبعد، لا يمكن تعيين موقع الاصطدام مباشرة للكاميرا، بل يجب استخدام سرعة الحركة للانتقال إلى المسافة الجديدة. أولاً، لنحصل على المسافة الجديدة:

```c#
float newDistance = desiredDistance;
RaycastHit hitInfo;
if (Physics.Raycast(playerTransform.position, desiredPosition - playerTransform.position,
    out hitInfo, (playerTransform.position - desiredPosition).magnitude, 1))
{
    newDistance = hitInfo.distance;
}
```

كيف يمكن تحديد أن الكاميرا تتحرك بعيدًا؟ يمكن استخدام "newDistances" لمقارنتها بالمسافة الحالية.

```c#
تحرك إلى مسافة أقرب
if (newDistance < curDistance)
{
    curDistance = newDistance;
}
تحرك لمسافات أبعد
else if(newDistance > curDistance)
{
}
```

بعد تقدير المسافة الأبعد، يصبح الأمر واضحًا للغاية، ما عليك سوى إضافة سرعة للتحرك:

```c#
curDistance = Math.Min(curDistance + Time.deltaTime * autoZoomOutSpeed, newDistance);

```
لقد أكملنا تقريبًا سلوك الكاميرا، ولكن هناك بعض التفاصيل التي يتعين علينا التعامل معها.

بمجرد ملامسة الكائن الصلب، يتم سحب العجلات القريبة دون تغيير في مقياس الأرضية.
------------------
هناك متطلباتان:

بعد الاصطدام بالجسم الصلب، يمكن سحبه نحوك فقط، دون إبعاده.
بمجرد الاصطدام بالأرض لا يمكن التقليص

أولا، استخدم متغير لحفظ حالة تصادم الكاميرا:

```c#
تم ترجمة النص إلى اللغة العربية:

متغير منطقي يسمى isHitGround وقيمته الافتراضية هي "خطأ"، وهو يُشير إلى ما إذا كان هناك اصطدام بالأرض.
تم الترجمة:

تم الوصول_للاعب = خطأ؛       // يشير إلى ما إذا كان الجسم قد تعرض للإصابة (باستثناء الأرض)
```

عند تقدير التكبير باستخدام عجلة التمرير، ضع شرطاً للتقييم:

```c#
if (zoom != 0F && (!isHitGround || (isHitObject && zoom > 0F)) )
{
    // calculate distance
}
```

تصادف الأرض وتدور حول نفسها من الأعلى إلى الأسفل
-----------------
هذا الوظيفة تنفيذها قليلاً معقد، حيث نحتاج إلى تقديم فرضياتنا السابقة حيث لم يكن من الممكن أن تكون الكاميرا دائمًا موجهة نحو الشخص. في هذه الحالة تنقسم الأمور إلى اتجاهين: "اتجاه الكاميرا نفسها (`desireForward`)" و "اتجاه الشخص إلى الكاميرا (`cameraToPlayer`)", علينا حساب قيم كلا الاتجاهين بشكل منفصل، حيث الأول يحدد اتجاه الكاميرا، والثاني يحدد موقع الكاميرا. لتسهيل الأمور، يتم تقديم [الحلقة السابقة](unity-Unity第三人称相机构建(上)عند تجزئة وظيفة الدوران في (.md) إلى دوران X (`RotateX`) ودوران Y (`RotateY`)، يجب إضافة الشرط التالي عند حساب `RotateY` لـ `cameraToPlayer`:

```c#
if ((!isHitGround) || 
    (isHitGround && transform.forward.y <= cameraToPlayer.y && yAngle > 0))
{
    cameraToPlayer = RotateY(cameraToPlayer, playerTransform.up, 
        transform.right, yAngle);
}
```

هذا الشرط يتألف من جزئين:

لم يلامس الأرض
عندما تلامس الأرض، ولكن مستعد للمغادرة الأرض

ثم استخدم 'cameraToPlayer' لحساب موقع الكاميرا:

```c#
transform.position = playerTransform.position - cameraToPlayer * curDistance;
```

وعند الحاجة (أي عند الاصطدام بالأرض)، قم بحساب اتجاه الكاميرا:

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

الرمز الكامل:

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


> تم ترجمة هذه المشاركة باستخدام ChatGPT ، يرجى تقديم [**ردود الفعل**](https://github.com/disenone/wiki_blog/issues/new)يرجى إشارة إلى أي نقص. 
