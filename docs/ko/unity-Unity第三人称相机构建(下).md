---
layout: post
title: Unity 세 번째 인칭 카메라 설정 (하)
categories:
- unity
catalog: true
tags:
- dev
description: 저는 유니티에서 '월드 오브 워크래프트'의 써드 펄슨 카메라를 참고하여 써드 펄슨 카메라를 만들고 싶습니다. 여기서 카메라
  리지드 바디 문제를 해결하려고 합니다.
---

<meta property="og:title" content="Unity第三人称相机构建(下)" />

이전 에피소드에서 [카메라의 회전](unity-Unity第三人称相机构建(上).md)로 지칭되는경우, 우리가 지금 해결해야 할 문제는 카메라의 강성입니다. 어떻게 해야 할까요?

카메라 강성
--------------
이전에 언급한 요구 사항을 다시 살펴보면:

마우스 휠: 카메라 줌 인 아웃
카메라는 어떤 단단한 물체도 통과할 수 없습니다.
카메라는 경직물체와 충돌 후 원래 거리로 천천히 복귀합니다.
카메라가 물체에 충돌하면 이동 중에 마우스 휠을 사용하여 가까이 가는 경우, 카메라는 즉시 반응해야하며 그 후 6번 항목이 더 이상 발생하지 않아야 합니다. 땅에 충돌한 후에는 축소 작업을 수행할 수 없습니다.
8. 카메라가 회전하는 도중에 땅에 부딪혀 인물 주위를 돌며 회전하는 것을 멈추고, 자신 주위를 중심으로 상하로 회전하게 변경되었으며, 좌우 회전은 여전히 인물을 중심으로 합니다.


이 몇 가지 사항은 다음을 의미합니다: 카메라가 단단한 물체와 부딪힐 때, 인물에 가까이 닿게 되고, 따라서 카메라가 떠날 때 다시 원래 거리로 천천히 돌아갈 수 있기를 원합니다. 그러나 자동으로 거리를 가까이 한 후 휠을 사용하여 수동으로 더 가까이 당기면 카메라가 충돌한 물체에서 벗어나기 때문에 해당 가까이 당긴 거리가 카메라의 실제 거리입니다. 이제 이러한 요구 사항을 하나씩 개설해보겠습니다.

스크롤 제어
----------
마우스 휠 제어는 매우 간단합니다. 단순히 `Input.GetAxis("Mouse ScrollWheel")`에서 휠 정보를 얻는 방법을 알면 되며, 최대값과 최소값을 설정하면 됩니다.

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

이곳에서 `playerTransform`은 캐릭터를 가리킵니다.

어떤 단단한 물체도 통과할 수 없습니다.
--------------------
이건 카메라와 강체의 접촉을 감지해야 해, 이 기능을 실행할 수 있는 함수가 있어:

```c#
static bool Raycast(Ray ray, RaycastHit hitInfo, float distance = Mathf.Infinity, int layerMask = DefaultRaycastLayers);
```

(http://docs.unity3d.com/Documentation/ScriptReference/Physics.Raycast.html)우리는 충돌 감지를 이렇게 구현할 수 있습니다:

```c#
RaycastHit hitInfo;
if (Physics.Raycast(playerTransform.position, desiredPosition - playerTransform.position,
    out hitInfo, (playerTransform.position - desiredPosition).magnitude, 1))
{
    curDistance = hitInfo.distance;
}
```

`targetPosition`은 충돌 위치를 나타내며, 카메라 위치를 충돌 위치로 설정하면 됩니다.

강체를 떠난 후, 천천히 원래의 거리로 돌아가세요.
---------------------------------
해당 기능을 완료하려면, 먼저 카메라가 있어야 하는 거리(`desiredDistance`)와 현재 거리(`curDistance`)를 각각 기록해야 하며, 스크롤 휠 조작 결과를 `desiredDistance`에 먼저 저장한 다음 충돌 계산에 따라 객체의 새로운 거리를 계산해야합니다.
카메라가 움직이거나 더 먼 곳의 물체와 충돌할 때, 충돌 위치를 바로 카메라에 할당할 수 없습니다. 새 거리로 이동하는 데 속도를 사용해야 합니다. 먼저 새로운 거리를 얻어보세요:

```c#
float newDistance = desiredDistance;
RaycastHit hitInfo;
if (Physics.Raycast(playerTransform.position, desiredPosition - playerTransform.position,
    out hitInfo, (playerTransform.position - desiredPosition).magnitude, 1))
{
    newDistance = hitInfo.distance;
}
```

그렇다면 카메라가 더 멀리 이동하고 있는지 어떻게 판단할까요? `newDistances`와 현재 거리를 비교하여 확인할 수 있습니다:

```c#
더 가까운 거리로 이동하세요.
if (newDistance < curDistance)
{
    curDistance = newDistance;
}
더 멀리 이동하세요.
else if(newDistance > curDistance)
{
}
```

그럼 더 멀리 이동하는 것을 인식하면, 속도를 더해 이동합니다.

```c#
curDistance = Math.Min(curDistance + Time.deltaTime * autoZoomOutSpeed, newDistance);

```
카메라의 대략적인 동작은 이미 완료되었고, 몇 가지 세부 사항이 처리되어야 합니다.

닿으면 강체에 바퀴가 가까워지며 바닥이 축소되지 않습니다.
------------------
이 문구를 한국어로 번역하겠습니다:

여기에 두 가지 요구 사항이 있습니다:

정체에 닿으면 가까이 당겨질 수만 있고 멀어지지는 못한다.
지면에 닿으면 축소할 수 없습니다.

먼저 카메라의 충돌 상태를 저장할 변수를 사용합니다:

```c#
bool isHitGround = false;       // 지면과 충돌했는지 여부를 나타냄
isHitObject라는 변수는 거짓으로 설정되어 있습니다. // 表시是否碰撞刚体(除去地面)
```

휠 확대/축소를 결정할 때 조건 판별 추가:

```c#
if (zoom != 0F && (!isHitGround || (isHitObject && zoom > 0F)) )
{
    // calculate distance
}
```

땅에 닿아서 몸 주변을 위아래로 회전합니다.
-----------------
이 기능을 구현하는 것은 조금 귀찮은데, 그 이유는 이제 우리가 이전에 가정했던 거인물을 항상 향하고 있다는 가정이 성립되지 않았기 때문이다. 이것을 두 개의 벡터로 분리하면 됩니다: **카메라 자체의 방향(`desireForward`)**과 **카메라에서 플레이어로 향하는 방향(`cameraToPlayer`)**. 이 두 벡터의 값을 각각 계산하여, 전자는 카메라의 방향을 결정하고, 후자는 카메라의 위치를 결정합니다. 편의를 위해 [이전 회차](unity-Unity第三人称相机构建(上).md)의 회전 함수를 X회전('RotateX')과 Y회전('RotateY')로 분리하면, 'cameraToPlayer'의 'RotateY'를 계산할 때 조건을 추가하십시오:

```c#
if ((!isHitGround) || 
    (isHitGround && transform.forward.y <= cameraToPlayer.y && yAngle > 0))
{
    cameraToPlayer = RotateY(cameraToPlayer, playerTransform.up, 
        transform.right, yAngle);
}
```

이 조건에는 두 부분이 있습니다:

지면에 닿지 않았습니다.
땅에 닿았지만 땅을 떠날 준비 중입니다.

그런 다음 `cameraToPlayer`를 사용하여 카메라의 위치를 계산합니다:

```c#
transform.position = playerTransform.position - cameraToPlayer * curDistance;
```

그리고 필요한 경우(즉, 땅에 닿을 때) 카메라 방향을 계산하십시오.

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

이렇게 카메라의 동작을 우리는 모두 실현했다.

전체 코드:

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

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT를 사용하여 번역되었습니다. 피드백은 [**여기**](https://github.com/disenone/wiki_blog/issues/new)어떤 빠짐 없이 지적하십시오. 
