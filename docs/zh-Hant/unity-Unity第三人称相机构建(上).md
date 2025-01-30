---
layout: post
title: Unity第三人稱相機構建(上)
categories:
- unity
catalog: true
tags:
- dev
description: 我想在Unity中建立一個第三人稱相機，這個相機的行為參考《魔獸世界》的第三人稱相機。這裡先來解決相機的旋轉問題。
figure: null
---

<meta property="og:title" content="Unity第三人称相机构建(上)" />

我想在Unity中建立一個第三人稱相機，相機的行為參考《魔獸世界》的第三人稱相機，具體的需求是：

滑鼠左鍵：控制相機繞著人物旋轉，人物不旋轉
**2.** 滑鼠右鍵：控制相機圍繞人物旋轉，人物的前方向（Unity 中的 tranform.forward）相應旋轉，人物上方向不變
3. 鼠標左鍵旋轉後，再右鍵旋轉，角色前方向馬上根據左鍵的旋轉做調整，再根據右鍵旋轉，此時等同於兩次都是右鍵旋轉。
4. 滑鼠滾輪：控制相機的遠近
相機無法穿過任何堅硬物體。
相机在离开与之碰撞的刚性物体后，逐渐回到原本的位置。
如果相機碰到物體時，使用滑鼠滾輪操作相機拉近，相機需要立即回應，之後第6點不再發生。
相機在旋轉中碰到地面，停止圍繞人物上下旋轉，改為圍繞自身上下旋轉，左右旋轉依然是圍繞人物。



這個需求可以先分成兩部分：相機旋轉，相機剛性。為了簡單起見，這裡先來解決相機旋轉的問題，也就是需求的前三點。

相機位置表示
----------------
在正式解決相機操作前，還有一個問題需要解決：相機位置的表示。這可以用多種方式：

- 相機的世界坐標
- 相機相對於人物的坐標
- 相機在人物座標系中的方向和距離

在我們的需求中，相機是根據人物位置進行變換的，所以我這裡使用第三種方式，而且在控制中相機一直瞄準人物，所以在相機內只需要保存距離信息：

```c#
float curDistance = 5F;
```

相機旋轉
-------------
繼續細分相機旋轉的行為，可以分成左鍵旋轉和右鍵旋轉，下面我們來一步一步地完成這兩個旋轉。首先我將相機設置為人物的子物體(children)，這樣人物的一些基本移動相機都會自動跟踪。

###左鍵旋轉###
單單看左鍵旋轉，需求很簡單：**相機旋轉，人物不旋轉**，這就相當於一個觀察模型的相機，相機可以任意角度觀察中心物體。

在Unity中獲取鼠標左鍵狀態使用語句：`Input.GetMouseButton(0)`（註：後面涉及到的代碼都是使用C#），顯然，右鍵就是`Input.GetMouseButton(1)`。獲取鼠標光標的移動位置（可以理解為幀之間光標在X-Y上的偏移量）信息是：`Input.GetAxis("Mouse X"); Input.GetAxis("Mouse Y")`。那麼我們可以先來獲取鼠標左鍵按下後光標的移動信息：

```csharp
if (Input.GetMouseButton(0))
{
    float x = Input.GetAxis("Mouse X");
    float y = Input.GetAxis("Mouse Y");
}
```
 
程式碼很簡單，接下來就是重點：如何控制相機來旋轉。要理解旋轉，這裡需要一些關於四元數的知識（網路上有很多資料，這裡就不一一列舉了），四元數重要的一點是它可以很簡單地構造旋轉，特別是環繞某個向量的旋轉，理解四元數後，實現相機環繞人物的旋轉就不難了。

另外還有一點需要注意的是，四元數旋轉軸僅僅是一個向量，以原點為起點。如果要以世界座標系中的某點`O`作為原點，以該點為起點的向量`V`作為旋轉軸，就需要進行座標系的轉換。簡單來說，就是將需要旋轉的點`P`轉換到以`O`為原點的座標系中，根據`V`進行旋轉，再轉換回世界座標系。根據這些操作，可以寫出一個功能函數：

```c#
Vector3 MyRotate(Vector3 oldPosition, float angle, Vector3 axis, Vector3 axisPosition)
{
建構一個四元數，以 axis 為旋轉軸，這是在人物座標系中的旋轉
    Quaternion rotation = Quaternion.AngleAxis(angle, axis);
// 這裡做的就是座標系的變換，把相機的世界坐標變換到人物座標系下的座標
    Vector3 offset = oldPosition - axisPosition;
// 計算旋轉並變換回世界坐標系中
    return axisPosition + (rotation * offset);
}
```
`Quaternion`是Unity中表示四元數的類型，加上之前滑鼠左鍵的偵測，就可以完成左鍵控制相機左右旋轉。

滑鼠左右移動控制攝影機左右旋轉的程式碼就可以直接給出：

```c#
newForward = MyRotate(newForward, x, up, Vector3.zero);
```
因為這裡只有前向量進行旋轉，並未涉及坐標系的轉換，所以第四個參數為`Vector3.zero`。

控制上下旋轉比左右旋轉難理解一點，因為此時的旋轉軸是會一直變化的（這裡假設人物的up一直是Y軸的正方向）。注意的相機也是一直在旋轉，並且視點中心一直對準人物，那麼相機的右方向（right）就是我們想要繞著旋轉的軸了（把相機right想像成人物的right），這樣理解，那麼上下旋轉的程式碼也很簡單了：

```csharp
newForward = MyRotate(newForward, -y, transform.right, Vector3.zero);
```

###右鍵旋轉###
做了左鍵旋轉，右鍵旋轉就很簡單了，只需要在左右旋轉的時候設置人物的前方向：

```csharp
player.forward = Vector3.Normalize(new Vector3(oldForward.x, 0, oldForward.z));
```

上下旋转跟左鍵的程式碼一樣。

###請按下左鍵，再按下右鍵###
雖然上面可以區分左鍵旋轉和右鍵旋轉，但一旦先用左鍵旋轉，再用右鍵操作時，問題就會出現：人物的前方向和相機的前方向就會不同！這樣相機和人物的正方向就會分離，實際操作起來會很奇怪。因此，在用右鍵旋轉時，我們需要先調整人物以使其與相機的正方向一致：

```csharp
player.forward = Vector3.Normalize(new Vector3(oldForward.x, 0, oldForward.z));

```

- - - 

###歐拉角萬向鎖###
至此，相機的旋轉差不多就完成，不過還有一個問題要注意：歐拉角萬向鎖。原理這裡就不細講，有興趣的朋友可以自行搜索，針對這裡相機的情況，就是當相機上下旋轉到跟人物的上方向重合的時候，相機的視角會發生突變。這是因為相機到達人物的頭頂或者腳底，相機的上方向會發生突變（因為相機的上方向的Y值一直都要大於零），所以我們需要限制相機的上下旋轉範圍，防止發生萬向鎖。操作很簡單，就是限制相機的前方向與人物的上方向的夾角的範圍：

```c#
if ((Vector3.Dot(transform.forward, transform.parent.up) >= -0.95F || y > 0) &&
    (Vector3.Dot(transform.forward, transform.parent.up) <= 0.95F || y < 0))
```

###完整代碼###

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

--8<-- "footer_tc.md"


> 這篇文章是由ChatGPT翻譯的，有任何[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
