---
layout: post
title: Unityの第三人称カメラの構築（下）
categories:
- unity
catalog: true
tags:
- dev
description: 私はUnityで「World of Warcraft」のサードパーソンカメラを参考にしたサードパーソンカメラを作成したいと考えています。ここで、カメラのリジッドボディの問題を解決します。
---

<meta property="og:title" content="Unity第三人称相机构建(下)" />

前回のエピソードでは、[カメラの回転](unity-Unity第三人称相机构建(上).md)，今回解決しなければならない課題はカメラの剛性です。どうすればいいのでしょうか？

相机刚性
--------------
過去に提起された要件を振り返る：

マウスのスクロールホイール：カメラのズームイン・アウトを制御します。
カメラはどんな剛体も通過できません。
物体と衝突すると、カメラは元の位置にゆっくり戻る
カメラが剛体に触れると、マウスホイールを使用してカメラを近づける場合、カメラはすぐに反応する必要があります。その後、6番目の点は発生しません。地面に衝突した後は、ズーム操作を行うことができません。
カメラが地面にぶつかり、人物の周りを回るのを止めて、自身の周りを回るように変更されました。左右の回転は依然として人物を中心に行われます。


これらのテキストを日本語に翻訳します：

これらの点の意味は、カメラが剛体に触れると、カメラが人物に近づくように強制されるということです。そのため、カメラが離れると、ゆっくりと元の距離に戻るようにしたいのです。ただし、自動的に近づいた後にホイールで手動で引き寄せると、カメラが衝突した物体から離れたことを意味し、その引き寄せた距離がカメラの実際の距離になります。次に、これらの要求を1つずつ解説していきましょう。

ホイールコントロール
----------
マウスのスクロールホイールのコントロールは非常に簡単です。ただし、`Input.GetAxis("Mouse ScrollWheel")`を使用してスクロール情報を取得し、最大値と最小値の距離を設定するだけです。

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

ここで`playerTransform`はキャラクターを指しています。

どんな固体でも貫けないよ。
--------------------
これにはカメラと剛体の衝突を検出する必要があります。この機能を実現するための関数が1つあります：

```c#
static bool Raycast(Ray ray, RaycastHit hitInfo, float distance = Mathf.Infinity, int layerMask = DefaultRaycastLayers);
```

具体な使用方法はUnityの[Reference](http://docs.unity3d.com/Documentation/ScriptReference/Physics.Raycast.html)我々はこのように衝突検出を実現できます：

```c#
RaycastHit hitInfo;
if (Physics.Raycast(playerTransform.position, desiredPosition - playerTransform.position,
    out hitInfo, (playerTransform.position - desiredPosition).magnitude, 1))
{
    curDistance = hitInfo.distance;
}
```

`targetPosition` is the position of the collision, so set the camera's position to the collision position.

剛体を離れた後、ゆっくり元の距離に戻る
---------------------------------
この機能を完成させるには、まず、カメラが設定するべき距離（`desiredDistance`）と現在の距離（`curDistance`）をそれぞれ記録して、ホイールの操作結果を`desiredDistance`に一時保存し、その後衝突を計算して物体の新しい距離を求めます。
カメラが剛体から離れたり、より遠い剛体に衝突した場合、衝突位置を直接カメラに割り当てることはできません。新しい距離に移動するために移動速度を使用する必要があります。まず新しい距離を取得します：

```c#
float newDistance = desiredDistance;
RaycastHit hitInfo;
if (Physics.Raycast(playerTransform.position, desiredPosition - playerTransform.position,
    out hitInfo, (playerTransform.position - desiredPosition).magnitude, 1))
{
    newDistance = hitInfo.distance;
}
```

その場合、カメラがより遠くに移動しているかどうかを判断するにはどうすればいいでしょうか？`newDistances`と現在の距離を比較することができます：

```c#
より近い距離に移動します
if (newDistance < curDistance)
{
    curDistance = newDistance;
}
より遠くへ移動します
else if(newDistance > curDistance)
{
}
```

それでは、より遠くに移動すると判断された場合、それは非常に直感的です。単に速度を上げて移動します：

```c#
curDistance = Math.Min(curDistance + Time.deltaTime * autoZoomOutSpeed, newDistance);

```
カメラの基本動作はほぼ完成しましたが、いくつかの細かい部分を修正する必要があります。

剛体に当たったら、ホイールを引き寄せて、地面のスケーリングはしないでください。
------------------
Here are two requirements:

剛体にぶつかったら、引き寄せることしかできず、遠ざけることはできません。
地面に触れたら縮小できません。

最初に、カメラの衝突状態を保存するための変数を使用します。

```c#
isHitGround変数はfalseです。  // 地面に当たったかどうかを表します
isHitObjectという変数は、falseです。 // 地面以外の剛体と衝突したかどうかを示す。
```

スクロールホイールでのズーム判定時に条件判定を追加してください：

```c#
if (zoom != 0F && (!isHitGround || (isHitObject && zoom > 0F)) )
{
    // calculate distance
}
```

地面に触れて自分自身を上下に回転させる
-----------------
この機能を実装するのは少々手間がかかります。なぜなら、この時点では以前に仮定していたカメラが常に人物を向いているという前提が成立しなくなっています。そのため、2つのベクトルに分割する必要があります：**カメラ自体の向き(`desireForward`)** と **プレイヤーからカメラへの方向(`cameraToPlayer`)** 、それぞれのベクトルの値を計算し、前者がカメラの向きを決定し、後者がカメラの位置を決定します。便宜上、[前のエピソード](unity-Unity第三人称相机构建(上).md)の回転関数をX軸回転(`RotateX`)とY軸回転(`RotateY`)に分けると、`cameraToPlayer`の`RotateY`を計算する際に条件を追加します：

```c#
if ((!isHitGround) || 
    (isHitGround && transform.forward.y <= cameraToPlayer.y && yAngle > 0))
{
    cameraToPlayer = RotateY(cameraToPlayer, playerTransform.up, 
        transform.right, yAngle);
}
```

この条件には2つの部分があります：

地面に触れていない
地面に触れましたが、地面を離れる準備をしています。

`cameraToPlayer`を使用して、カメラの位置を計算します：

```c#
transform.position = playerTransform.position - cameraToPlayer * curDistance;
```

そして必要なとき（つまり地面に触れると）カメラの方向を計算します：

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

これによって、私たちはカメラの動作をすべて実現しました。

コード全体：

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

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されました。[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。 
