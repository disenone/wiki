---
layout: post
title: Unity第三人称相机构建(下)
categories:
- unity
catalog: true
tags:
- dev
description: Unityで第三者視点のカメラを作成したいと思っています。このカメラの動作は《ワールド・オブ・ウォークラフト》の第三者視点のカメラを参考にしています。ここではカメラのリジッドボディの問題について解決します。
---

<meta property="og:title" content="Unity第三人称相机构建(下)" />

(unity-Unity第三人称相机构建(上).md file)、今後の課題はカメラの剛性を解決することですが、どのように対処する必要があるでしょうか？

カメラの剛性
--------------
以前に挙げた要件を振り返ると：

マウスのスクロールホイール：カメラのズームインとズームアウトを制御します。
5. カメラはどんな硬い物体も通過できません。
6. カメラは衝突した剛性物体から離れた後、徐々に元の距離に戻ります。
7. カメラが剛体に衝突した場合、マウスホイールを使ってカメラをズームインすると、カメラはすぐに反応する必要があります。その後、6点目は発生しなくなります。地面に衝突した後は、ズーム操作を行うことはできません。
カメラが地面にぶつかり、人物を中心に上下を回るのを止め、自分自身を中心に回るように切り替え、左右の回転は人物を中心に回るままです。


これらのポイントの意味は、カメラが剛性物体に当たると、人物に近づいてしまうことを強いられることです。したがって、カメラが離れる際に、ゆっくりと元の距離に戻るようにしたいと考えています。しかし、自動的に距離を近づけた後、ホイールを使用して手動で更に近づけると、カメラが物体との衝突から離れたことを示し、この近づけた距離がカメラの実際の距離となります。次に、これらの要件を一つずつ解説していきましょう。

ローラーコントロール
----------
マウスホイールのコントロールは非常に簡単で、ホイール情報を取得するには`Input.GetAxis("Mouse ScrollWheel")`を使用し、距離の最大値と最小値を設定すれば大丈夫です。

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

ここで `playerTransform` はキャラクターを指しています。

どんな硬い物体でも貫通できない
--------------------
これには、カメラと剛体の接触を検出する必要があります。これを実現するための関数が1つあります：

```c#
static bool Raycast(Ray ray, RaycastHit hitInfo, float distance = Mathf.Infinity, int layerMask = DefaultRaycastLayers);
```

具体的な使用方法はUnityの[Reference](http://docs.unity3d.com/Documentation/ScriptReference/Physics.Raycast.html)私たちはこのように衝突の検出を実現できます：

```c#
RaycastHit hitInfo;
if (Physics.Raycast(playerTransform.position, desiredPosition - playerTransform.position,
    out hitInfo, (playerTransform.position - desiredPosition).magnitude, 1))
{
    curDistance = hitInfo.distance;
}
```

`targetPosition`は衝突した位置を指し、カメラの位置を衝突した位置に設定すればいいです。

剛体から離れた後、徐々に元の距離に戻る。
---------------------------------
この機能を完了するには、まずカメラがあるべき距離（`desiredDistance`）と現在の距離（`curDistance`）を記録し、ホイール操作の結果を`desiredDistance`に保存した後、衝突を計算して物体の新しい距離を計算します。
カメラが剛体から離れた場合や、より遠い剛体に衝突した場合、衝突位置を直接カメラに割り当てることはできません。新しい距離に向かって移動するために移動速度を使う必要があります。まず、新しい距離を取得しましょう：

```c#
float newDistance = desiredDistance;
RaycastHit hitInfo;
if (Physics.Raycast(playerTransform.position, desiredPosition - playerTransform.position,
    out hitInfo, (playerTransform.position - desiredPosition).magnitude, 1))
{
    newDistance = hitInfo.distance;
}
```

その場合、カメラがより遠くに移動しているかどうかを判断するにはどうすればよいでしょうか？`newDistances`と現在の距離を比較することができます：

```c#
// より近い距離に移動する
if (newDistance < curDistance)
{
    curDistance = newDistance;
}
// より遠くへ進む
else if(newDistance > curDistance)
{
}
```

そうなると、より遠くへ移動する判断は直感的になりますので、そのまま速度を加えて移動するだけです。

```c#
curDistance = Math.Min(curDistance + Time.deltaTime * autoZoomOutSpeed, newDistance);

```
カメラの大まかな動作は完了しましたが、まだいくつかの詳細を処理する必要があります。

剛体に当たった後、ホイールを引き寄せて、地面は縮尺されません。
------------------
ここには2つの要求があります：

1. 固体に触れた後は、近づくだけで遠ざけることはできない。
2. 地面に触れた後は縮小できません。

最初にカメラの衝突状態を保存するために変数を使用します。

```c#
bool isHitGround = false;       // Indicates whether the ground is hit
bool isHitObject = false;       // Whether the rigid body is hit (excluding the ground)
```

マウスホイールによるズーム操作時に条件分岐を追加してください：

```c#
if (zoom != 0F && (!isHitGround || (isHitObject && zoom > 0F)) )
{
    // calculate distance
}
```

地面にぶつかって自分自身を上下に回転させる
-----------------
この機能を実装するのは少し面倒ですが、これまでカメラが常にキャラクターを向いているという仮定が成り立たなくなりました。そこで、2つのベクトルに分かれます：**カメラの期待する向き (`desireForward`)** と **キャラクターからカメラへの方向 (`cameraToPlayer`)**。それぞれのベクトルの値を計算し、前者がカメラの向きを決定し、後者がカメラの位置を決定します。わかりやすくするため、[前回のエピソード](unity-Unity第三人称相机构建(上).md)の回転関数をX回転（`RotateX`）とY回転（`RotateY`）に分割すると、`cameraToPlayer`の`RotateY`を計算する際に条件を追加します：

```c#
if ((!isHitGround) || 
    (isHitGround && transform.forward.y <= cameraToPlayer.y && yAngle > 0))
{
    cameraToPlayer = RotateY(cameraToPlayer, playerTransform.up, 
        transform.right, yAngle);
}
```

この条件には２つの部分があります：

地面に触れていません
- 地面に接触していますが、地面を離れる準備をしています。

次に、`cameraToPlayer`を使用してカメラの位置を計算します：

```c#
transform.position = playerTransform.position - cameraToPlayer * curDistance;
```

必要なとき、すなわち地面に触れたときにカメラの向きを計算します。

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

このような行動は私たち全員が実現しました。

完整なコード：

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


> この投稿はChatGPTを使用して翻訳されましたが、[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)何か見落としがあれば指摘してください。 
