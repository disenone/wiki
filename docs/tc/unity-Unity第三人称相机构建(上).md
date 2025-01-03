---
layout: post
title: Unity第三人称相机构建(上)
categories:
- unity
catalog: true
tags:
- dev
description: 我想在Unity中創建一個第三人稱相機，相機的行為參考《魔兽世界》的第三人稱相機。這裡先來解決相機的旋轉問題。
figure: null
---

<meta property="og:title" content="Unity第三人称相机构建(上)" />

我想在Unity中建立一個第三人稱相機，相機的行為參考《魔獸世界》的第三人稱相機，具體需求如下：

鼠标左键：控制相機繞人物旋轉，人物不旋轉
2. 右鍵：控制相機繞人物旋轉，人物的前方向(Unity中的tranform.forward)相應旋轉，人物上方向不變
鼠标左鍵旋轉後，再右鍵旋轉，角色前方向馬上根據左鍵的旋轉做調整，再根據右鍵旋轉，此時等價於兩次都是右鍵旋轉。
滑鼠滾輪：控制相機遠近
相機無法穿過任何剛性物體
相機在離開碰撞的剛性物體後，慢慢回到原來的距離上。
如果相機在碰到物體時，使用滑鼠滾輪操作相機拉近，相機需要立即反應，此後第6點不再發生。
相机在旋轉時碰到地面，停止繞人物上下旋轉，改為繞自身上下旋轉，左右旋轉仍然是繞人物。



這個需求可以先分成兩部分：相機旋轉，相機剛性。簡單來說，這裡先來解決相機旋轉的問題，也就是需求的前3點。

相機位置顯示
----------------
在正式解決相機操作前，還有一個問題需要解決：相機位置的表示。這可以用多種方式：

- 相機的世界座標
- 盝機相對於人物的座標
在人物坐标系中，相机的方向和距离

由於相機在我們的需求中根據人物位置進行變換，因此我在這裡使用第三種方法，並且在控制中，相機一直瞄準人物，所以在相機內只需要保存距離信息：

```c#
float curDistance = 5F;
```

相機旋轉
-------------
繼續細分相機旋轉的行為，可以分成左鍵旋轉和右鍵旋轉，下面我們來一步一步地完成這兩個旋轉。首先我把相機設為人物的子物體(children)，這樣人物的一些基本的移動相機都會自動的跟踪。

###左鍵旋轉###
單單看左鍵旋轉，需求很簡單：**相機旋轉，人物不旋轉**，這就相當於一個觀察模型的相機，相機可以任意角度觀察中心物體。

在Unity中獲取滑鼠左鍵狀態的語法為：`Input.GetMouseButton(0)`（註：以下涉及程式碼部分均為使用C#），明顯地，右鍵即為`Input.GetMouseButton(1)`。要獲取滑鼠游標的移動位置（可理解為幀之間游標在X-Y軸上的偏移量）資訊，可以使用：`Input.GetAxis("Mouse X"); Input.GetAxis("Mouse Y")`。現在，讓我們先來獲取滑鼠左鍵按下後游標的移動資訊：

```csharp
if (Input.GetMouseButton(0))
{
    float x = Input.GetAxis("Mouse X");
    float y = Input.GetAxis("Mouse Y");
}
```
 
程式碼很簡單，接下來就是重點：如何控制相機來旋轉。要理解旋轉，這裡需要一些關於四元數的知識（網路上資料很多，這裡就不列舉了），四元數重要的一點是它可以很簡單地構造旋轉，特別是繞某個向量的旋轉，理解四元數後，實現相機繞人物的旋轉就不難了。

另外還有一點要注意的是，四元數旋轉軸只是一個向量，以原點為出發點，如果要以世界座標系中的某點`O`為原點，以該點為出發點的向量`V`為旋轉軸，就需要進行座標系的變換，簡單地說，就是把需要旋轉的點`P`變換到，以`O`為原點的座標系中，根據`V`旋轉，再變換回世界座標系。根據這些操作，可以寫出一個功能函數：

```c#
Vector3 MyRotate(Vector3 oldPosition, float angle, Vector3 axis, Vector3 axisPosition)
{
構造一個四元數，以軸為旋轉軸，這是在人物座標系中的旋轉。
    Quaternion rotation = Quaternion.AngleAxis(angle, axis);
這裡所做的就是坐標系的轉換，將相機的世界坐標轉換到人物坐標系下的坐標。
    Vector3 offset = oldPosition - axisPosition;
// 計算旋轉並變換回世界座標系中
    return axisPosition + (rotation * offset);
}
```
"Quaternion" 是 Unity 中用來表示四元數的資料類型，再加上先前偵測滑鼠左鍵的功能，就能完成控制相機左右旋轉的動作。

滑鼠左右移動控制相機左右旋轉的程式碼就可以直接給出：

```c#
newForward = MyRotate(newForward, x, up, Vector3.zero);
```
因為這裡只有前向量做旋轉，沒有涉及到座標系的轉換，所以第四個參數為 `Vector3.zero`。

控制上下旋轉比左右旋轉難理解一點，因為此時的旋轉軸是會一直變化的（這裡假設人物的up一直是Y軸的正方向）。注意的相機也是一直在旋轉，並且視點中心一直對準人物，那麼相機的右方向（right）就是我們想要繞著旋轉的軸了（把相機right想像成人物的right），這樣理解，那麼上下旋轉的程式碼也很簡單了：

```csharp
newForward = MyRotate(newForward, -y, transform.right, Vector3.zero);
```

###右鍵旋轉###
將左鍵旋轉後，右鍵旋轉就變得簡單了，只需在左右旋轉時設置人物的前方向：

```csharp
player.forward = Vector3.Normalize(new Vector3(oldForward.x, 0, oldForward.z));
```

上下旋轉的程式碼和左鍵的相同。

###請先按左鍵，再按右鍵###
儘管可以使用左鍵和右鍵分別旋轉，但若先用左鍵旋轉，再使用右鍵操作，將出現問題：角色和相機的前方向將不同！這將導致相機和角色的正方向分離，操作起來會很奇怪。因此，在使用右鍵旋轉之前，要先將角色調整為與相機的正方向一致：

```csharp
player.forward = Vector3.Normalize(new Vector3(oldForward.x, 0, oldForward.z));

```

- - - 

###歐拉角萬向鎖###
至此，相機的旋轉差不多就完成，不過還有一個問題要注意：歐拉角萬向鎖。原理這裡就不細講，有興趣的朋友可以自行搜索，針對這裡相機的情況，就是當相機上下旋轉到跟人物的上方向重合的時候，相機的視角會發生突變。這是因為相機到達人物的頭頂或者腳底，相機的上方向會發生突變(因為相機的上方向的Y值一直都要大於零)，所以我們需要限制相機的上下旋轉範圍，防止發生萬向鎖。操作很簡單，就是限制相機的前方向與人物的上方向的夾角的範圍：

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


> 此貼文是使用 ChatGPT 翻譯的，請在 [**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
