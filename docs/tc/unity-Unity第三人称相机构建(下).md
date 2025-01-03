---
layout: post
title: Unity第三人称相機構建(下)
categories:
- unity
catalog: true
tags:
- dev
description: 我想在Unity中創建一個第三人稱相機，相機的行為參考《魔獸世界》的第三人稱相機。這裡來解決相機的剛體問題。
---

<meta property="og:title" content="Unity第三人称相机构建(下)" />

上一集講完了 [相機的旋轉](unity-Unity第三人称相机构建(上)若您正使用 Markdown（.md）格式，那我們現在需處理的是相機的剛性問題，該如何處理呢？

相機剛性
--------------
請回顧之前提出的需求：

4. 滑鼠滾輪：控制相機遠近
相機不能穿過任何剛性物體
當相機離開碰撞的剛性物體後，會慢慢返回原本的距離。
當相機與物體碰撞時，若使用滑鼠滾輪拉近相機，需即時響應，之後不再發生第6點；碰觸地面後無法縮放。
相機在旋轉時碰到地面，停止圍繞人物上下旋轉，改為圍繞自身上下旋轉，左右旋轉依然是圍繞人物。


這幾點的意思是：相機在碰到剛性物體時，會被迫拉近跟人物的距離，那麼我們想要相機在離開的時候，可以慢慢地回到原來的距離；但是如果在自動拉近距離後，用滾輪再手動拉近，說明相機離開碰撞的物體，那麼這個拉近的距離就是相機的實際距離。下面我們來一點一點的解這些需求。

滾輪控制
----------
滑鼠滾輪控制很簡單，只需要知道獲取滾輪資訊的方法是`Input.GetAxis("Mouse ScrollWheel")`，然後設定最大和最小距離值就可以了：

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

這裡的 `playerTransform` 指向人物。

無法穿透任何堅硬物體
--------------------
這需要檢測相機跟剛體的接觸，有一個函數可以實現這個功能：

```c#
static bool Raycast(Ray ray, RaycastHit hitInfo, float distance = Mathf.Infinity, int layerMask = DefaultRaycastLayers);
```

請參考Unity的[參考資料](http://docs.unity3d.com/Documentation/ScriptReference/Physics.Raycast.html)我們可以透過以下方式來實現碰撞的檢測：

```c#
RaycastHit hitInfo;
if (Physics.Raycast(playerTransform.position, desiredPosition - playerTransform.position,
    out hitInfo, (playerTransform.position - desiredPosition).magnitude, 1))
{
    curDistance = hitInfo.distance;
}
```

`targetPosition`是指碰撞的位置，將相機的位置設定為碰撞的位置即可。

離開剛體後，慢慢回到原來的距離上。
---------------------------------
為了完成這個功能，首先要分別記錄下相機應該處於的距離(`desiredDistance`)和目前距離(`curDistance`)，將滾輪操作的結果用`desiredDistance`先存起來，再根據碰撞計算物體的新距離；
當檢測到相機離開剛體，或者碰撞到更遠的剛體時，不能直接將碰撞位置的數值賦予給相機，須要透過一個移動速度值來逐漸移動至新的距離。首先取得新的距離：

```c#
float newDistance = desiredDistance;
RaycastHit hitInfo;
if (Physics.Raycast(playerTransform.position, desiredPosition - playerTransform.position,
    out hitInfo, (playerTransform.position - desiredPosition).magnitude, 1))
{
    newDistance = hitInfo.distance;
}
```

那麼怎麼判斷相機正在向更遠的距離移動呢？可以用`newDistances`和當前的距離進行比較：

```c#
向更近的距離移動
if (newDistance < curDistance)
{
    curDistance = newDistance;
}
向更遠的距離移動
else if(newDistance > curDistance)
{
}
```

在向更遠的距離移動後，判斷就變得很直觀了，只需要增加速度來移動：

```c#
curDistance = Math.Min(curDistance + Time.deltaTime * autoZoomOutSpeed, newDistance);

```
我們已經完成了相機的大致功能，接下來還有一些細節需要處理。

遇到剛體時，滾輪會被拉近，而地板不會縮放。
------------------
這裡有兩個要求：

碰到剛體後只能拉近，不能拉遠
2. 觸地後無法縮放

首先使用變數來保存相機的碰撞狀態：

```c#
bool isHitGround = false;       // 表示是否碰撞地面
bool isHitObject = false;       // 代表是否撞击物体（不包括地面）
```

在判斷滾輪縮放的時候加上條件判斷：

```c#
if (zoom != 0F && (!isHitGround || (isHitObject && zoom > 0F)) )
{
    // calculate distance
}
```

遇到地面時繞著自己旋轉上下。
-----------------
該功能的實現有些複雜，因為現在我們之前對相機一直對準人物的假設不成立了，現在要分成兩個向量：**相機自身的朝向(`desireForward`)**和**人物到相機的方向(`cameraToPlayer`)**，分別計算這兩個向量的值，前者決定相機的朝向，後者決定相機的位置。為了方便起見，下一集就將…[Truncated](unity-Unity第三人称相机构建(上)將.md)的旋轉函數拆成X旋轉(`RotateX`)和Y旋轉(`RotateY`)，那麼在計算`cameraToPlayer`的`RotateY`時加上條件：

```c#
if ((!isHitGround) || 
    (isHitGround && transform.forward.y <= cameraToPlayer.y && yAngle > 0))
{
    cameraToPlayer = RotateY(cameraToPlayer, playerTransform.up, 
        transform.right, yAngle);
}
```

此條件分為兩個部分：

- Not touching the ground
觸地，然而正準備離開。

接著使用 `cameraToPlayer` 計算相機的位置：

```c#
transform.position = playerTransform.position - cameraToPlayer * curDistance;
```

並且在有需要的時候(也就是碰到地面)計算相機的朝向：

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

我們已實現這款相機的功能。

完整代碼：

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

--8<-- "footer_tc.md"


> 此貼文是由 ChatGPT 翻譯，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
