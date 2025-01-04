---
layout: post
title: Unity第三人称相机构建(上)
categories:
- unity
catalog: true
tags:
- dev
description: 我想在Unity中創建一個第三人稱相機，相機的行為參考《魔獸世界》的第三人稱相機。這裡先來解決相機的旋轉問題。
figure: null
---

<meta property="og:title" content="Unity第三人称相机构建(上)" />

我想在Unity中建立一個第三人稱攝影機，該攝影機的運作方式參考《魔獸世界》中的第三人稱攝影機，具體需求如下：

滑鼠左鍵：控制相機圍繞人物旋轉，人物不會旋轉
滑鼠右鍵：控制相機繞人物旋轉，人物的前方向（Unity 中的 tranform.forward）相應旋轉，人物上方向不變
鼠标左鍵旋轉後，接著右鍵旋轉，角色即時根據左鍵旋轉做調整，再隨右鍵旋轉，此時等同於連續右鍵旋轉兩次。
滑鼠滾輪：控制相機遠近
5. 盈的相機無法穿透任何堅硬的物體.
相機在離開碰撞的剛性物體後，慢慢回到原來的距離上。
7. If the camera touches an object and the camera needs to zoom in using the mouse scroll wheel, it should respond immediately, and the issue mentioned in point 6 should not occur again.
相機在旋轉時撞到地面，停止繞人物上下旋轉，改為繞自身上下旋轉，左右旋轉仍繞著人物。



這個需求可以先分成兩部分：相機旋轉，相機剛性。為了方便起見，這裡先來解決相機旋轉的問題，也就是需求的前3點。

相機位置顯示
----------------
在正式解決相機操作前，還有一個問題需要解決：相機位置的表示。這可以用多種方式：

相機的世界座標
- 相機相對於人物的座標
- 攝影機在人物座標系中的方向和距離

由於相機在我們的需求中是根據人物位置進行變換的，因此我在這裡使用第三種方式，並且在控制中相機一直瞄準人物，所以在相機內只需要保存距離信息：

```c#
float curDistance = 5F;
```

相機旋轉
-------------
繼續細分相機旋轉的行為，可以分成左鍵旋轉和右鍵旋轉，下面我們來一步一步地完成這兩個旋轉。首先我把相機設為人物的子物體，這樣人物的一些基本的移動相機都會自動的跟踪。

###請將這些文字翻譯成繁體中文語言:

Left-click and rotate ###.
單單看左鍵旋轉，需求很簡單：**相機旋轉，人物不旋轉**，這就相當於一個觀察模型的相機，相機可以任意角度觀察中心物體。

在Unity中獲取滑鼠左鍵狀態使用語句：`Input.GetMouseButton(0)`（註：後面涉及到程式碼的地方，都是使用C#），明顯，右鍵就是`Input.GetMouseButton(1)`。獲取滑鼠游標的移動位置（可以理解為幀之間游標在X-Y上的偏移量）資訊是：`Input.GetAxis("Mouse X"); Input.GetAxis("Mouse Y")`。那麼我們可以先來獲取滑鼠左鍵按下後游標的移動資訊：

```csharp
if (Input.GetMouseButton(0))
{
    float x = Input.GetAxis("Mouse X");
    float y = Input.GetAxis("Mouse Y");
}
```
 
代碼很簡單，那下面就是關鍵的地方：如何控制相機來旋轉。要理解旋轉，這裡需要一些關於四元數的知識（網上資料很多，這裡就不列舉了），四元數重要的一點是它可以很簡單地構造旋轉，特別是圍繞某個向量的旋轉，理解四元數後，實現相機圍繞人物的旋轉就不難了。

另外還有一點要注意的是，四元數旋轉軸只是一個向量，以原點為出發點，如果要以世界座標系中的某點`O`為原點，以該點為出發點的向量`V`為旋轉軸，就需要進行座標系的變換，簡單地說，就是把需要旋轉的點`P`變換到，以`O`為原點的座標系中，根據`V`旋轉，再變換回世界座標系。根據這些操作，可以寫出一個功能函數：

```c#
Vector3 MyRotate(Vector3 oldPosition, float angle, Vector3 axis, Vector3 axisPosition)
{
建立一個四元數，以axis為旋轉軸，這是在人物座標系中的旋轉。
    Quaternion rotation = Quaternion.AngleAxis(angle, axis);
這裡進行的是座標系的轉換，將相機的世界座標轉換到人物座標系下的座標。
    Vector3 offset = oldPosition - axisPosition;
計算旋轉並轉換回世界坐標系中
    return axisPosition + (rotation * offset);
}
```
"Quaternion" 是 Unity 中表示四元數的型別，再加上之前滑鼠左鍵的偵測，便可以完成左鍵控制相機左右旋轉。

鼠标左右移動控制相機左右旋轉的程式碼就可以直接給出：

```c#
newForward = MyRotate(newForward, x, up, Vector3.zero);
```
因為這裡只有前向量做旋轉，沒有涉及到座標系的轉換，所以第四個參數為`Vector3.zero`。

控制上下旋轉比左右旋轉難理解一點，因為此時的旋轉軸是會一直變化的（這裡假設人物的up一直是Y軸的正方向）。注意的相機也是一直在旋轉，並且視點中心一直對準人物，那麼相機的右方向(right)就是我們想要圍繞著旋轉的軸了（把相機 right 想像成人物的 right），這樣理解，那麼上下旋轉的程式碼也很簡單了：

```csharp
newForward = MyRotate(newForward, -y, transform.right, Vector3.zero);
```

###右鍵旋轉###
左键旋转已完成，右键旋转将变得容易，只需在左右旋转时設定人物的前方向：

```csharp
player.forward = Vector3.Normalize(new Vector3(oldForward.x, 0, oldForward.z));
```

上下旋轉與左鍵的程式碼相同。

###先左鍵，後右鍵###
儘管可以使用左键和右键分别旋转，但是當先使用左键旋轉後，再對其進行右键操作時，問題就會出現：人物面對的方向和相機的正前方不一致了！這樣相機和人物之間的正確方向就會分離，操作起來就變得很奇怪。所以在使用右鍵旋轉時，必須先將人物調整為與相機的正確方向一致：

```csharp
player.forward = Vector3.Normalize(new Vector3(oldForward.x, 0, oldForward.z));

```

- - - 

###歐拉角萬向鎖###
到這裡，相機的旋轉差不多就完成，不過還有一個問題要注意：歐拉角萬向鎖。原理這裡就不細講，有興趣的朋友可以自行搜索，針對這裡相機的情況，就是當相機上下旋轉到跟人物的上方向重合的時候，相機的視角會發生突變。這是因為相機到達人物的頭頂或者腳底，相機的上方向會發生突變(因為相機的上方向的Y值一直都要大於零)，所以我們需要限制相機的上下旋轉範圍，防止發生萬向鎖。操作很簡單，就是限制相機的前方向與人物的上方向的夾角的範圍：

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


> 這篇文章是透過 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
