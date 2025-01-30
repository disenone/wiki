---
layout: post
title: Unityの第三人称相機システム構築（上）
categories:
- unity
catalog: true
tags:
- dev
description: 私はUnityでワールドオブウォークラフトのサードパーソンカメラを参考にして、サードパーソンカメラを作成したいと思います。まずはカメラの回転問題を解決しましょう。
figure: null
---

<meta property="og:title" content="Unity第三人称相机构建(上)" />

Unityで第三者視点のカメラを作成したいと思っています。そのカメラの動作は『ワールド・オブ・ウォークラフト』の第三者視点のカメラを参考にしたいです。具体的な要件は：

1. 左クリック：カメラが人物の周りを回転し、人物は回転しません。
マウスの右クリック：キャラクターを中心にカメラを回転させる。キャラクターの前方向（Unityのtransform.forward）も相応に回転し、キャラクターの上方向は変わらない。
マウスの左クリックで回転させた後、右クリックで再度回転させると、キャラクターの前方向が左クリックの回転に即座に合わせられ、更に右クリックの回転に合わせられます。この時、実質的には両方が右クリックで回転させたのと同じです。
4. マウスホイール：カメラのズームを制御する
5. カメラはどんな硬い物体を通過できません。
6. カメラは衝突した剛体から離れた後、徐々に元の距離に戻ります。
7. もしカメラが物体に触れた場合、マウスのホイールを操作してカメラをズームインすると、カメラはすぐに反応する必要があります。その後、6番目のポイントは再発しません。
8. カメラが地面に当たり、人物の周りを上下に回転するのを止めて、自身の周りを回転するように変更されました。左右の回転は依然として人物の周りを回ります。



この要求は、まず2つの部分に分けることができます：カメラの回転、カメラの剛性。簡単のため、ここではまずカメラの回転に焦点を当て、つまり要求の最初の3つの点に対処します。

カメラの位置を示す
----------------
正式なカメラ操作を解決する前に、解決すべき別の問題があります。それはカメラ位置の表現です。これにはさまざまな方法があります：

- カメラのワールド座標
人物に対するカメラの位置
人物座標系におけるカメラの向きと距離

私たちの要件では、カメラはキャラクターの位置に基づいて変化するため、ここでは第三の方法を使用しています。また、カメラは常にキャラクターを照準しているため、カメラ内には距離情報のみを保存すればよいです。

```c#
float curDistance = 5F;
```

カメラ回転
-------------
カメラの回転動作をさらに詳しく分解すると、左クリック回転と右クリック回転に分けることができます。ここでは、これら2つの回転を一歩ずつ行っていきます。まず、カメラをキャラクターの子オブジェクト(children)として設定します。これにより、キャラクターの基本的な移動にカメラが自動的に追従するようになります。

###左クリックで回転###
左クリックで回転するだけで、要求は非常に単純です：**カメラが回転し、キャラクターは回転しない**。これはモデルを見るカメラのようで、カメラは中心のオブジェクトを任意の角度で見ることができます。

Unity内でマウスの左クリック状態を取得するためのコードは、`Input.GetMouseButton(0)`です（補足：後のコード部分は全てC＃を使用しています）。明らかに、右クリックは`Input.GetMouseButton(1)`です。マウスカーソルの移動位置（フレーム間のX-Y上のオフセット）情報を取得するには、`Input.GetAxis("Mouse X"); Input.GetAxis("Mouse Y")`となります。では、まずマウスの左クリック後にカーソルの移動情報を取得してみましょう：

```csharp
if (Input.GetMouseButton(0))
{
    float x = Input.GetAxis("Mouse X");
    float y = Input.GetAxis("Mouse Y");
}
```
 
コードはシンプルですが、重要なのはここです：カメラの回転をどのように制御するか。回転を理解するには、四元数に関する知識が必要です（オンラインで多くの情報がありますが、ここでは挙げません）、四元数の重要な点は、回転を簡単に構築できることです、特に特定のベクトルを中心とした回転。四元数を理解すれば、カメラを人物の周りに回転させることは難しくありません。

もう一つ注意すべき点は、四元数の回転軸は原点を出発点とするベクトルであるということです。もし世界座標系のある点`O`を原点として、その点を出発点とするベクトル`V`を回転軸にする場合は、座標系の変換が必要です。簡単に言うと、回転させる必要がある点`P`を`O`を原点とする座標系に変換し、`V`に従って回転させた後、再度世界座標系に変換します。これらの操作に基づいて、機能関数を作成することができます。

```c#
Vector3 MyRotate(Vector3 oldPosition, float angle, Vector3 axis, Vector3 axisPosition)
{
// 軸を回転軸として四元数を構築する、これは人物座標系での回転です
    Quaternion rotation = Quaternion.AngleAxis(angle, axis);
// ここで行っているのは座標系の変換で、カメラのワールド座標を人物の座標系に変換しています。
    Vector3 offset = oldPosition - axisPosition;
世界座標系に回転して変換する。
    return axisPosition + (rotation * offset);
}
```
`Quaternion`はUnity内で四元数を表す型です。それにマウスの左クリック検出を組み合わせると、カメラの左右回転を左クリックで制御できます。

マウスの左右移動でカメラの左右回転を制御するコードをそのまま提示できます：

```c#
newForward = MyRotate(newForward, x, up, Vector3.zero);
```
こちらは前方ベクトルのみを回転するため、座標系の変換は関係ありませんので、第四引数は`Vector3.zero`となります。

上下の回転を左右の回転よりも理解するのが少し難しいのは、この時点での回転軸が常に変化するためです(ここではキャラクターの上向きが常にY軸の正の方向であると仮定します)。注目すべき点は、カメラも常に回転しており、視点の中心が常にキャラクターを見つめ続けていることです。そのため、カメラの右方向が私たちが回転したい軸であると考えることができます（カメラのrightをキャラクターのrightと考える）。この解釈に基づいて、上下方向の回転のコードも非常に簡単になります：

```csharp
newForward = MyRotate(newForward, -y, transform.right, Vector3.zero);
```

###右クリックで回転###
左クリックで回転したら、右クリックで回転はとても簡単です。人物の向きを設定するだけで、左右に回転します。

```csharp
player.forward = Vector3.Normalize(new Vector3(oldForward.x, 0, oldForward.z));
```

上下旋转のコードは左キーのコードと同じです。

###先に左ボタン、次に右ボタン###
上面の操作では、左クリックで回転し、右クリックで回転を分けることができますが、最初に左クリックで回転してから右クリックで操作しようとすると、問題が発生します：キャラクターの前方向とカメラの前方向が異なる！これにより、カメラとキャラクターの正面方向が分かれてしまい、実際の操作が非常に奇妙になります。したがって、右クリックで回転する際には、キャラクターをカメラの正面方向に合わせる必要があります。

```csharp
player.forward = Vector3.Normalize(new Vector3(oldForward.x, 0, oldForward.z));

```

- - - 

###オイラー角万向ロック###
ここで、カメラの回転はほぼ完了ですが、注意すべき問題が一つあります。それはオイラー角の万向ロックです。原理については詳しくは説明しませんが、興味のある方は自分で調べてみてください。ここでのカメラの状況に関して言えば、カメラが上下に回転して人物の上方向と一致するとき、カメラの視点が突発的に変化します。これは、カメラが人物の頭上や足元に到達した際に、カメラの上方向が変化するためです（カメラの上方向のY値は常にゼロより大きくなければなりません）。したがって、万向ロックを防ぐために、カメラの上下回転範囲を制限する必要があります。操作は非常に簡単で、カメラの前方向と人物の上方向との角度の範囲を制限することです。

```c#
if ((Vector3.Dot(transform.forward, transform.parent.up) >= -0.95F || y > 0) &&
    (Vector3.Dot(transform.forward, transform.parent.up) <= 0.95F || y < 0))
```

###完整代码###

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


> この投稿は ChatGPT を使用して翻訳されました。フィードバックは[**こちら**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。 -> どこか抜けている点を指摘してください。 
