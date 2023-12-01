---
layout: post
title: Building Third-Person Camera in Unity (Part 1)
categories:
- unity
catalog: true
tags:
- dev
description: I want to create a third-person camera in Unity, with the camera's behavior
  based on the third-person camera in "World of Warcraft". Let's start by addressing
  the camera rotation issue.
figure: null
---


I want to create a third-person camera in Unity, with the camera behavior based on the third-person camera in "World of Warcraft". The specific requirements are as follows:

1. **Left mouse button:** Control the camera to rotate around the character without rotating the character.
2. **Right mouse button:** Control the camera to rotate around the character. The character's forward direction (Unity's transform.forward) rotates accordingly, while the character's upward direction remains unchanged.
3. After rotating with the left mouse button, rotating with the right mouse button will immediately adjust the character's forward direction based on the left mouse button's rotation. Then, continuing to rotate with the right mouse button is equivalent to rotating with the right mouse button twice.
4. **Mouse scroll wheel:** Control the zoom level of the camera.
5. The camera cannot pass through any rigid objects.
6. After the camera moves away from a colliding rigid object, it gradually returns to its original distance.
7. If the camera encounters an object and the mouse scroll wheel is used to zoom in, the camera needs to respond immediately, and the 6th point no longer applies.
8. If the camera collides with the ground while rotating, it stops rotating up and down around the character and instead rotates up and down around itself. The left and right rotation still revolves around the character.



This requirement can be divided into two parts: camera rotation and camera rigidity. For simplicity, let's first solve the problem of camera rotation, which corresponds to the first 3 points of the requirement.

Camera Position Indicator
----------------
Before we address the formal camera operations, there is one more issue that needs to be resolved: the representation of the camera position. This can be done in multiple ways:

- > Original: <https://disenone.github.io/wiki>
- > This post is protected by [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by/4.0/deed.en) agreement, should be reproduced with attribution.
- [to_be_replace[3]]

- World coordinates of the camera
- Coordinates of the camera relative to the character
- Direction and distance of the camera in the character coordinate system

Because in our requirements, the camera is transformed based on the character's position, so here I am using the third method, and in the controls, the camera is always aimed at the character, so only distance information needs to be saved inside the camera.

```c#
float curDistance = 5F;
```

Camera rotation
-------------
Continuing the subdivision of camera rotation behavior, it can be divided into left-click rotation and right-click rotation. Let's proceed step by step to complete these two rotations. First, I set the camera as a child object of the character, so that the camera will automatically track some basic movements of the character.

###Rotate with Left Mouse Button###
Simply put, the requirement for left mouse button rotation is quite simple: **the camera rotates while the character remains stationary**. This is similar to having a camera for observing a model, where the camera can freely rotate around the central object.

To obtain the status of the left mouse button in Unity, use the statement: `Input.GetMouseButton(0)` (Note: all the code sections mentioned below will be in C#). Similarly, the right mouse button can be detected using `Input.GetMouseButton(1)`. To get the mouse cursor's movement position (which can be understood as the offset of the cursor on the X-Y axis between frames), use: `Input.GetAxis("Mouse X"); Input.GetAxis("Mouse Y")`. So, let's first obtain the movement information of the cursor after the left mouse button is pressed:

```csharp
if (Input.GetMouseButton(0))
{
    float x = Input.GetAxis("Mouse X");
    float y = Input.GetAxis("Mouse Y");
}
```
The code is very simple, and the crucial part is below: how to control the camera rotation. To understand rotation, some knowledge about quaternions is needed (there is a lot of information available online, so I won't list it here). One important aspect of quaternions is their ability to easily construct rotations, especially rotations around a certain vector. Once quaternion understanding is achieved, implementing camera rotation around a character is not difficult.

And another point to note is that the rotation axis of quaternions is just a vector, starting from the origin. If you want to take a point `O` in the world coordinate system as the origin and a vector `V` starting from that point as the rotation axis, you need to transform the coordinate system. Simply put, you need to transform the point `P` that needs to be rotated to a coordinate system with the origin at `O`, perform the rotation according to `V`, and then transform it back to the world coordinate system. Based on these operations, a functional function can be written:

```c#
Vector3 MyRotate(Vector3 oldPosition, float angle, Vector3 axis, Vector3 axisPosition)
{
```python
// Construct a quaternion, with `axis` as the rotation axis, which is in the character's coordinate system.
```

    Quaternion rotation = Quaternion.AngleAxis(angle, axis);
// Here we are performing a coordinate transformation, converting the camera's world coordinates to coordinates under the character's coordinate system.
    Vector3 offset = oldPosition - axisPosition;
    // Calculate the rotation and transform it back to the world coordinate system.
    return axisPosition + (rotation * offset);
}
```
`Quaternion` is the type used in Unity to represent quaternions. By adding the previous left mouse button detection, you can complete the left mouse button control to rotate the camera left and right.

The code to control the camera's left and right rotation by moving the mouse left and right can be directly provided as follows:

```c#
newForward = MyRotate(newForward, x, up, Vector3.zero);
```
Because only the forward vector is being rotated here without involving coordinate system transformation, the fourth parameter is `Vector3.zero`.

Controlling the vertical rotation is slightly more difficult to grasp than the horizontal rotation because the rotation axis is constantly changing (assuming here that the character's "up" direction is always the positive Y-axis). It is important to note that the camera is also constantly rotating, with its focal point always aligned with the character. Therefore, the camera's right direction (right) is the axis we want to rotate around (think of the camera's right as the character's right). With this understanding, the code for vertical rotation is also quite simple:

```csharp
newForward = MyRotate(newForward, -y, transform.right, Vector3.zero);
```

###Right-click to rotate###

After performing a left-click rotation, right-click rotation becomes very simple. You just need to set the character's forward direction when rotating left or right.

```csharp
player.forward = Vector3.Normalize(new Vector3(oldForward.x, 0, oldForward.z));
```

The code for rotating up and down is the same as the code for the left mouse button.

###Left click first, then right click###
Although it is possible to rotate with the left mouse button and the right mouse button separately, a problem arises when the left mouse button is used to rotate first and then the right mouse button is used: the character's forward direction becomes different from the camera's forward direction! As a result, the camera and the character's orientation are separated, which feels odd in actual operation. Therefore, when we rotate with the right mouse button, we need to adjust the character to align with the camera's forward direction first:

```csharp
player.forward = Vector3.Normalize(new Vector3(oldForward.x, 0, oldForward.z));

```

- - - 

###Euler Angle Gimbal Lock###
By now, the rotation of the camera is almost complete, but there is one more issue to pay attention to: Euler Angle Gimbal Lock. The principle won't be explained here, those who are interested can search for it on their own. In the case of the camera here, when the camera rotates up and aligns with the upward direction of the character, the camera's perspective will undergo a sudden change. This is because when the camera reaches the top or bottom of the character, the upward direction of the camera will undergo a sudden change (because the Y value of the upward direction of the camera always needs to be greater than zero). Therefore, we need to limit the range of the camera's up and down rotation to prevent gimbal lock. The operation is quite simple, which is to limit the range of the angle between the forward direction of the camera and the upward direction of the character:

```c#
if ((Vector3.Dot(transform.forward, transform.parent.up) >= -0.95F || y > 0) &&
    (Vector3.Dot(transform.forward, transform.parent.up) <= 0.95F || y < 0))
```

###Complete code###

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

> Original: <https://disenone.github.io/wiki>  
> This post is protected by [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by/4.0/deed.en) agreement, should be reproduced with attribution.


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
