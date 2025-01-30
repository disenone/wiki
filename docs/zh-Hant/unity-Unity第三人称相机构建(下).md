---
layout: post
title: Unity第三人稱相機構建(下)
categories:
- unity
catalog: true
tags:
- dev
description: 我想在Unity中創建一個第三人稱相機，相機的行為參考《魔獸世界》的第三人稱相機。這裡來解決相機的剛體問題。
---

<meta property="og:title" content="Unity第三人称相机构建(下)" />

上一集講完了[相機的旋轉](unity-Unity第三人称相机构建(上).md)，那麼現在我們要解決的問題是相機的剛性，要怎麼做呢？

相機剛性
--------------
回顧之前提到的需求：

滑鼠滾輪：控制攝影機的遠近
相機無法穿過任何堅硬物體。
相机在与刚性物体发生碰撞后，会逐渐回到原来的位置上。
7. 如果相機在碰到剛體時，使用滑鼠滾輪操作相機拉近，相機需要馬上反應，此後第6點不再發生；碰撞地面後不能進行縮放操作。
相機在旋轉中碰到地面，停止圍繞人物上下旋轉，改為圍繞自身上下旋轉，左右旋轉依然是圍繞人物。


這幾點的意思是：相機在遇到剛性物體時，會被迫拉近與人物的距離，那麼我們希望相機在離開的時候，可以慢慢地回到原來的距離；但是如果在自動拉近距離後，再用滾輪手動拉近，這說明相機已經遠離碰撞的物體，那麼這個拉近的距離就是相機的實際距離。下面我們來一點一點地解釋這些需求。

滾輪控制
----------
滑鼠滾輪的控制非常簡單，只需要知道如何獲取滾輪資訊`Input.GetAxis("Mouse ScrollWheel")`，然後設定最大和最小的距離值就可以了：

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

這裡的 `playerTransform` 指向角色。

不能穿過任何剛性物體
--------------------
需要測試相機與剛體的接觸，有一個函數可以實現這個功能：

```c#
static bool Raycast(Ray ray, RaycastHit hitInfo, float distance = Mathf.Infinity, int layerMask = DefaultRaycastLayers);
```

具體用法參考Unity的[Reference](http://docs.unity3d.com/Documentation/ScriptReference/Physics.Raycast.html)，我們可以這樣實現碰撞的檢測：

```c#
RaycastHit hitInfo;
if (Physics.Raycast(playerTransform.position, desiredPosition - playerTransform.position,
    out hitInfo, (playerTransform.position - desiredPosition).magnitude, 1))
{
    curDistance = hitInfo.distance;
}
```

`targetPosition`就是碰撞的位置，把相机的位置設到碰撞的位置就可以。

離開剛體後，慢慢回到原來的距離上
---------------------------------
完成這項功能的首要步驟是分別記錄相機應該處於的距離(`desiredDistance`)以及當前距離(`curDistance`)，將滾輪操作的結果暫存為`desiredDistance`，然後根據碰撞計算物體的新距離。
在檢測到相機離開剛體，或者碰撞到更遠的剛體時，不能直接將碰撞的位置賦值給相機，需要用一個移動速度來向新的距離移動。先來獲取新的距離：

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
// 向更近的距離移動
if (newDistance < curDistance)
{
    curDistance = newDistance;
}
// 向更遠的距離移動
else if(newDistance > curDistance)
{
}
```

當你評估移動到更遠的距離後，解決方案就變得更直觀了，只需增加速度進行移動：

```c#
curDistance = Math.Min(curDistance + Time.deltaTime * autoZoomOutSpeed, newDistance);

```
我們已經大致完成了相機的功能，還有一些細節需要處理。

碰到剛體後滾輪拉近，地面不縮放
------------------
這裡有兩個要求：

碰到剛體後只能拉近，不能拉遠
碰到地面後不能縮放

首先用變數來保存相機的碰撞狀態：

```c#
bool isHitGround = false;       // 表示是否碰撞地面
isHitObject 這個布林值變數表示是否碰撞到物體（不包括地面）。
```

在判斷滾輪縮放的時候加上條件判斷：

```c#
if (zoom != 0F && (!isHitGround || (isHitObject && zoom > 0F)) )
{
    // calculate distance
}
```

碰到地面時围绕自身上下旋转
-----------------
這個功能實現起來有點麻煩，因為這時我們之前假設相機一直對準人物的情況不成立。這時分成兩個向量：**相機自身的朝向(`desireForward`)**和**人物到相機的方向(`cameraToPlayer`)**，分別計算這兩個向量的值，前者決定相機的朝向，後者決定相機的位置。為了方便，把[上一集](unity-Unity第三人称相机构建(上)將.md)的旋轉函數分解為X旋轉(`RotateX`)和Y旋轉(`RotateY`)，所以在計算`cameraToPlayer`的`RotateY`時加上條件：

```c#
if ((!isHitGround) || 
    (isHitGround && transform.forward.y <= cameraToPlayer.y && yAngle > 0))
{
    cameraToPlayer = RotateY(cameraToPlayer, playerTransform.up, 
        transform.right, yAngle);
}
```

這個條件有兩部分：

未觸及地面
- 碰到地面，但準備離開地面

然後用`cameraToPlayer`計算相機的位置：

```c#
transform.position = playerTransform.position - cameraToPlayer * curDistance;
```

並且在有需要的時候（也就是碰到地面）計算相機的朝向：

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

我們已經實現了這相機的功能。

完整程式碼：

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


> 此帖子是使用 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)請指出任何遺漏之處。 
