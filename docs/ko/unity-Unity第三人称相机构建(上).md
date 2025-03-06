---
layout: post
title: Unity 세 번째 인칭 카메라 구축(상)
categories:
- unity
catalog: true
tags:
- dev
description: 제가 유니티에서 월드 오브 워크래프트의 써드 펄슨 카메라를 기반으로 한 세 번째 인칭 카메라를 만들고 싶습니다. 우선 카메라의
  회전 문제를 해결하겠습니다.
figure: null
---

<meta property="og:title" content="Unity第三人称相机构建(上)" />

Unity에서 서드 퍼슨 카메라를 만들고 싶어요. 카메라 동작은 '월드 오브 워크래프트'의 서드 퍼슨 카메라를 참고하려고 해요. 구체적인 요구 사항은 다음과 같아요:

마우스 왼쪽 버튼: 캐릭터 주변 카메라 회전을 제어하며 캐릭터는 회전하지 않습니다.
마우스 오른쪽 버튼: 캐릭터 주위에서 카메라를 제어하여 회전시키고, 캐릭터의 전방(Unity의 tranform.forward)도 회전시키면서 캐릭터의 상방 방향은 그대로 유지합니다.
3. 마우스 왼쪽 버튼을 회전한 후 오른쪽 버튼으로 다시 회전하면 캐릭터의 전방 방향이 왼쪽 버튼의 회전에 따라 즉시 조정되어 오른쪽 버튼 회전에 따라 조정됩니다. 이 시점에서는 두 번 연속 오른쪽 버튼 회전과 동등합니다.
마우스 휠: 카메라 줌 제어
카메라는 어떤 강체 물체를 통과할 수 없습니다.
카메라는 강체 물체와 충돌한 후 천천히 원래의 거리로 돌아간다.
카메라가 물체에 부딪힐 때, 마우스 휠을 사용하여 카메라를 가까이하면 카메라가 즉각적으로 반응해야 합니다. 그 후 6번째 항목은 더 이상 발생하지 않습니다.
카메라가 지면에 부딪혀 회전을 멈추고, 인물 주위를 위아래로 도는 대신 자체 주위를 도게 되며, 좌우로는 여전히 인물을 중심으로 돕니다.



이 요구 사항은 먼저 두 부분으로 나눌 수 있습니다: 카메라 회전 및 카메라 강성. 간단히 말해서 여기서는 우선 카메라 회전 문제를 해결하고, 즉 요구 사항의 처음 3가지를 다루겠습니다.

카메라 위치 표시
----------------
카메라 작동을 공식적으로 처리하기 전에 해결해야 할 문제가 하나 더 있습니다: 카메라 위치의 표시입니다. 이는 여러 가지 방법으로 표시할 수 있습니다:

카메라의 월드 좌표
카메라가 대상에 대한 좌표
- 사진기의 방향과 거리가 인물 좌표계에서 어떻게 되는지

우리의 요구에 따라 카메라는 캐릭터의 위치에 따라 변화하므로 여기서는 세 번째 방법을 사용했고, 컨트롤에서 카메라는 항상 캐릭터를 노리고 있으므로 카메라 내부에는 거리 정보만 저장하면 됩니다.

```c#
float curDistance = 5F;
```

카메라 회전
-------------
필히 지속적으로 카메라 회전 동작을 미세하게 세분화할 수 있으며, 왼쪽 키 회전과 오른쪽 키 회전으로 나눌 수 있습니다. 이제 이 두 가지 회전을 한 단계씩 완성해 보겠습니다. 우선 카메라를 캐릭터의 하위 항목으로 설정하면 캐릭터의 일부 기본 이동은 자동으로 추적됩니다.

###'왼쪽 클릭하여 회전###'
왼쪽 클릭하여 카메라를 회전하는 것만 생각하면, 요구사항은 매우 간단합니다: **카메라만 회전하고 캐릭터는 회전하지 않아야** 합니다. 이는 관찰 모델의 카메라와 같은 것으로, 카메라는 중심 객체를 어떤 각도에서도 관찰할 수 있습니다.

Unity에서 마우스 왼쪽 클릭 상태를 얻는 명령은 `Input.GetMouseButton(0)`입니다. 오른쪽 클릭은 당연히 `Input.GetMouseButton(1)`입니다. 마우스 커서의 이동 위치를 얻는 방법(프레임 간 X-Y 이동량으로 이해 가능)은 `Input.GetAxis("Mouse X")`, `Input.GetAxis("Mouse Y")`입니다. 따라서 먼저 마우스 왼쪽 클릭 후 커서 이동 정보를 얻어봅시다:

```csharp
if (Input.GetMouseButton(0))
{
    float x = Input.GetAxis("Mouse X");
    float y = Input.GetAxis("Mouse Y");
}
```
 
코드는 굉장히 간단한데요. 이제 중요한 부분이 나옵니다: 카메라를 어떻게 회전시킬 것인가. 회전을 이해하기 위해서는 사원수에 대한 몇가지 지식이 필요합니다(인터넷에 많은 자료가 있지만 여기서는 나열하지 않겠습니다). 사원수에서 중요한 점은 회전을 간단하게 구현할 수 있다는 것이죠, 특히 어떤 벡터 주위의 회전을 만들어내는 것. 사원수를 이해하면, 카메라가 캐릭터를 중심으로 회전하는 것을 구현하는 것은 어렵지 않습니다.

또 한 가지 주의해야 할 점은 사원수 회전 축은 그냥 벡터일 뿐이에요. 원점을 기준으로 하니까요. 만약 세계 좌표계의 어떤 점 'O'를 원점으로 삼고, 그 점을 기준으로 하는 벡터 'V'를 회전 축으로 삼으려면 좌표계를 변환해야 해요. 간단히 말해서, 회전할 점 'P'를 'O'를 원점으로 하는 좌표계로 변환한 다음 'V'를 기준으로 회전한 뒤 다시 세계 좌표계로 돌려놓는 거죠. 이러한 작업에 기반해 다음과 같은 기능 함수를 작성할 수 있어요:

```c#
Vector3 MyRotate(Vector3 oldPosition, float angle, Vector3 axis, Vector3 axisPosition)
{
축을 회전 축으로 하는 사원수를 구성하십시오. 이것은 캐릭터 좌표계에서의 회전입니다.
    Quaternion rotation = Quaternion.AngleAxis(angle, axis);
여기서 하는 일은 좌표계 변환입니다. 카메라의 월드 좌표를 캐릭터 좌표계로 변환하는 작업이죠.
    Vector3 offset = oldPosition - axisPosition;
// 회전 계산 후 월드 좌표계로 변환
    return axisPosition + (rotation * offset);
}
```
`Quaternion`은 Unity에서 사원수를 나타내는 유형입니다. 이전에 마우스 왼쪽 버튼을 감지하는 기능을 결합하면 카메라를 좌우로 회전하는 왼쪽 버튼 제어를 완료할 수 있습니다.

마우스 왼쪽 및 오른쪽 이동으로 카메라를 좌우로 회전시키는 코드를 직접 제공할 수 있습니다:

```c#
newForward = MyRotate(newForward, x, up, Vector3.zero);
```
여기에서는 전방 벡터만 회전하기 때문에 좌표계 변환이 필요하지 않으므로 네 번째 매개변수는 `Vector3.zero`입니다.

위아래 회전을 좌우 회전보다 이해하기 어려운 이유는 현재 회전 축이 계속 변하기 때문이다(여기서 캐릭터의 상단이 항상 Y축의 양의 방향이라고 가정한다). 카메라도 계속 회전하며 시야 중심은 항상 캐릭터를 향해 있다. 따라서 카메라의 오른쪽 방향은 우리가 회전하고 싶어하는 축이 된다(카메라의 오른쪽을 캐릭터의 오른쪽으로 생각하면 이해하기 쉽다). 이것을 이해하면 위아래 회전 코드도 매우 간단해진다:

```csharp
newForward = MyRotate(newForward, -y, transform.right, Vector3.zero);
```

###우클릭하여 회전###
마우스 왼쪽으로 회전하고 오른쪽으로 회전하면 간단해집니다. 캐릭터의 전방을 설정해주면 됩니다.

```csharp
player.forward = Vector3.Normalize(new Vector3(oldForward.x, 0, oldForward.z));
```

위아래 회전은 왼쪽 키와 동일한 코드입니다.

###맨 처음 왼쪽 버튼을 클릭한 후에 오른쪽 버튼을 클릭하세요.
위의 내용을 한국어로 번역하시겠어요:

위에서는 좌클릭으로 회전하고 우클릭으로도 회전할 수 있지만, 좌클릭으로 회전한 후 우클릭으로 조작하면 문제가 발생합니다: 캐릭터의 전방과 카메라의 전방이 다르게 됩니다! 그러면 카메라와 캐릭터의 정면이 분리되어, 실제 조작이 매우 이상해집니다. 따라서 우클릭으로 회전할 때 캐릭터를 먼저 조정하여 카메라의 정면과 일치시켜야 합니다:

```csharp
player.forward = Vector3.Normalize(new Vector3(oldForward.x, 0, oldForward.z));

```

- - - 

###오일러 각도 올바인 뮤턴트릭스###
여기까지, 카메라 회전 거의 완료한 것 같아. 다만 주의할 점이 하나 있어: 오일러 각 공략. 이론은 여기서 자세히 설명 안 할 테니까 관심 있는 사람은 그냥 검색해. 이 카메라 상황에서 주의할 점은, 카메라가 위아래로 회전해 인물의 윗 방향과 일치하는 경우, 카메라 시점이 갑자기 변할 거야. 이는 카메라가 인물의 머리 위나 발 아래로 도착하면, 카메라의 윗 방향이 갑자기 변하기 때문인데 (카메라의 윗 방향인 Y값은 항상 0보다 커야 해), 그래서 카메라의 상하 회전 범위를 제한해서 각 현상이 발생하지 않도록 해야 해. 조작은 매우 간단해, 카메라의 전방향과 인물의 윗 방향 사이의 각도를 제한하는 거야:

```c#
if ((Vector3.Dot(transform.forward, transform.parent.up) >= -0.95F || y > 0) &&
    (Vector3.Dot(transform.forward, transform.parent.up) <= 0.95F || y < 0))
```

###완전한 코드###

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

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT를 사용하여 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)어떤 누락 사항을 지적하십시오. 
