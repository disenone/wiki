---
layout: post
title: Unity第三人称相机构建(上)
categories:
- unity
catalog: true
tags:
- dev
description: 私はUnityでサードパーソンカメラを作成したいと思います。カメラの挙動は「ワールドオブウォークラフト」のサードパーソンカメラを参考にしています。まずはカメラの回転問題を解決しましょう。
figure: null
---

<meta property="og:title" content="Unity第三人称相机构建(上)" />

Unityでサードパーソン視点のカメラを作成したいんですが、その挙動は「World of Warcraft」のサードパーソンカメラを参考にしています。具体的な要件は以下の通りです：

マウスの左クリック: 人物の周囲をカメラが回転し、人物は回転しません。
マウスの右クリック：キャラクターの周囲をカメラで制御し、キャラクターの前方向（Unityのtransform.forward）が対応するように回転させ、キャラクターの上方向は変わらないままにします。
マウスの左クリックで回転した後、右クリックで回転すると、キャラクターの向きが左クリックに基づいてすぐに調整され、その後右クリックで回転します。これにより、実質的には2回連続で右クリックで回転した状態になります。
マウスのスクロールホイール：カメラのズームインとアウトを制御します。
カメラはどんな硬い物体も通り抜けることはできない。
6. カメラは剛体の衝突から離れると、ゆっくりと元の位置に戻ります。
カメラがオブジェクトに当たった時にマウスホイールでカメラをズームすると、カメラは直ちに反応する必要があり、その後、6番目のポイントは発生しなくなります。
カメラが地面にぶつかると、キャラクターを中心に上下に回転するのを止め、自分自身を中心に上下に回転するように変更され、左右の回転はまだキャラクターを中心にします。



この要件は、まず2つの部分に分けることができます：カメラの回転とカメラの剛性。簡単のため、ここではまずカメラの回転に焦点を当てます。つまり、要求の最初の3つのポイントに関する問題を解決します。

カメラの位置表示
----------------
カメラの操作を本格的に始める前に、1つ問題があります：カメラの位置表示です。これにはさまざまな方法があります：

カメラのワールド座標
- スタンドカメラは人物に対する座標
- カメラの人物座標系における方向と距離

私たちのニーズに合わせて、カメラはキャラクターの位置に基づいて変化するので、私はここで第3の方法を使用しています。コントロールでは常にカメラがキャラクターを狙っているので、カメラ内には距離情報だけを保存すれば十分です。

```c#
float curDistance = 5F;
```

カメラが回転します
-------------
カメラの回転行動をさらに詳細に分割すると、左回転と右回転に分けられ、ここではこれら2つの回転を段階的に行います。まずはカメラをキャラクターの子オブジェクトに設定しました。これにより、キャラクターの基本的な移動時にもカメラが自動で追跡されるようになります。

###左クリックして回転###
左クリックでのみ回転する場合、要件は非常にシンプルです：**カメラが回転し、キャラクターが回転しない**ことです。これは中心物体を見るための観察モデルのカメラに相当します。カメラは中心の物体を任意の角度で見ることができます。

Unityでマウスの左クリック状態を取得するコードは、`Input.GetMouseButton(0)` です。右クリックは `Input.GetMouseButton(1)` です。マウスカーソルの移動位置（フレーム間のX-Y方向の移動量と考えられます）を取得するには、`Input.GetAxis("Mouse X"); Input.GetAxis("Mouse Y")` を使用します。それでは、マウスの左クリックが押された後にカーソルの移動情報を取得してみましょう。

```csharp
if (Input.GetMouseButton(0))
{
    float x = Input.GetAxis("Mouse X");
    float y = Input.GetAxis("Mouse Y");
}
```
 
コードは単純ですが、重要なのはここです：カメラの回転を制御する方法。回転を理解するためには、四元数に関する基本的な知識が必要です（インターネットには多くの情報がありますが、ここでは挙げません）。四元数の重要な点は、特定のベクトルを中心に回転を簡単に構築できることです。四元数を理解した後、カメラをキャラクターの周りに回転させることは難しくありません。

また、注意しておかなければならない重要な点があります。四元数の回転軸は単なるベクトルで、原点を出発点としています。もし世界座標系内の点`O`を原点とし、その点を出発点とするベクトル`V`を回転軸とする場合、座標系を変換する必要があります。単純に言えば、回転させたい点`P`を、`O`を原点とする座標系に変換し、`V`に応じて回転させ、最後に世界座標系に再変換します。これらの手順に基づいて、以下の機能関数を記述できます：

```c#
Vector3 MyRotate(Vector3 oldPosition, float angle, Vector3 axis, Vector3 axisPosition)
{
// 人物の座標系で、軸を回転軸として四元数を構築します。
    Quaternion rotation = Quaternion.AngleAxis(angle, axis);
以下是文本的日语翻译：

ここでやっているのは座標系の変換だ。カメラのワールド座標をキャラクターの座標系に変換する。
    Vector3 offset = oldPosition - axisPosition;
回すのを計算して、それを世界座標系に変換します。
    return axisPosition + (rotation * offset);
}
```
「Quaternion」は四元数を表すUnityのデータ型です。マウスの左クリックの検出と組み合わせると、左クリックでカメラが左右に回転する制御が完了します。

マウスを左右に移動させると、カメラも左右に回転するコードは以下の通りです：

```c#
newForward = MyRotate(newForward, x, up, Vector3.zero);
```
ここでは前方ベクトルのみが回転するため、座標系の変換は行われませんので、第四引数は`Vector3.zero`となります。

上下の回転を左右の回転より難しいのは、この時点での回転軸が常に変化するためです（ここでは、キャラクターの上向きが常にY軸の正方向であると仮定しています）。注目すべきは、カメラも常に回転し、視点の中心が常にキャラクターに合わせていることです。したがって、カメラの右方向（右）は私たちが周りを回転させたい軸です（カメラの右をキャラクターの右と考えてください）。このように理解すると、上下の回転のコードも非常に簡単になります：

```csharp
newForward = MyRotate(newForward, -y, transform.right, Vector3.zero);
```

###右键旋转###
左クリックで左に回転させたら、右クリックで右に回転させるのも簡単です。キャラクターの正面方向を左右に回転するだけでいいですね。

```csharp
player.forward = Vector3.Normalize(new Vector3(oldForward.x, 0, oldForward.z));
```

上下旋転と左キーのコードは同じです。

###左クリックし、次に右クリックしてください。###
上記のテキストを日本語に翻訳します：

上面は左クリックで回転し、右クリックで回転できますが、最初に左クリックしてから右クリックで操作し始めると問題が発生します：キャラクターとカメラの前方向が異なります！そのため、カメラとキャラクターの正面方向が分かれてしまい、実際の操作が非常に奇妙になります。したがって、右クリックで回転する際には、まずキャラクターをカメラの正面方向に合わせる必要があります：

```csharp
player.forward = Vector3.Normalize(new Vector3(oldForward.x, 0, oldForward.z));

```

- - - 

###オイラーアングル万能ロック###
ここまで、カメラの回転はだいたい完了ですが、注意すべき問題がもう1つあります：オイラー角のジンバルロックです。この原理については詳しく説明しませんが、興味のある方は自分で検索してください。この場合、カメラが上下に回転して人物の上方向と一致すると、カメラの視点が急変します。これは、カメラが人物の頭の上や足元に到達すると、カメラの上方向が急変するため（カメラの上方向のY値は常に0より大きくなければならないため）、カメラの上下回転範囲を制限し、ジンバルロックを防止する必要があるからです。操作は簡単で、カメラの前方向と人物の上方向との間の角度を制限するだけです。

```c#
if ((Vector3.Dot(transform.forward, transform.parent.up) >= -0.95F || y > 0) &&
    (Vector3.Dot(transform.forward, transform.parent.up) <= 0.95F || y < 0))
```

###完整なコード###

```csharp
// rotate oldPosition around a axis starting at axisPosition
Vector3 MyRotate(Vector3 oldPosition, float angle, Vector3 axis, Vector3 axisPosition)
{
    Quaternion rotation = Quaternion.AngleAxis(angle, axis);
    Vector3 offset = oldPosition - axisPosition;
    return axisPosition + (rotation * offset);
}

// rotate oldForward, player forward may change when use mouse RB
Vector3 RotateIt(Vector3 oldForward, Vector3 up, Vector3 right, Transform player)
{
    Vector3 newForward = -oldForward;
    // mouse LB RB rotate camera and character
    if (Input.GetMouseButton(0) ^ Input.GetMouseButton(1))
    {
        float x = Input.GetAxis("Mouse X") * rotateSpeed;
        float y = Input.GetAxis("Mouse Y") * rotateSpeed;

        if (x != 0F)
        {
            newForward = MyRotate(newForward, x, up, Vector3.zero);

            // mouse RB, character rotate together
            if (Input.GetMouseButton(1))
            {
                player.forward = Vector3.Normalize(new Vector3(oldForward.x, 0, 
                    oldForward.z));
            }
        }

        if (y != 0F)
        {

            if ((Vector3.Dot(transform.forward, up) >= -0.95F || y > 0)
                && (Vector3.Dot(transform.forward, up) <= 0.95F || y < 0))
            {
                newForward = MyRotate(newForward, -y, transform.right, Vector3.zero);

            }
        }
    }

    return -newForward;
}
```

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されたものです。[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。 -> どこか抜け落ちているところがあれば指摘してください。 
