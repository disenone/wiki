---
layout: post
title: Building a Third-Person Camera in Unity (Part 1)
categories:
- unity
catalog: true
tags:
- dev
description: I would like to create a third-person camera in Unity, with the camera's
  behavior modeled after the third-person camera in "World of Warcraft". Let's address
  the rotation issue of the camera first.
figure: null
---

<meta property="og:title" content="Unity第三人称相机构建(上)" />

I want to create a third-person camera in Unity, with the camera's behavior modeled after the third-person camera in "World of Warcraft". The specific requirements are:

1. Left mouse button: Control the camera to rotate around the character, but the character itself does not rotate.
2. Right mouse button: Control the camera to rotate around the character. The character's forward direction (Unity's `tranform.forward`) rotates accordingly, but the character's upward direction remains unchanged.
3. After rotating with the left mouse button, if you rotate with the right mouse button, the character's forward direction will immediately adjust based on the left mouse button's rotation. Then, the right mouse button rotation is applied, which is equivalent to two consecutive right mouse button rotations.
4. Mouse scroll wheel: Control the camera's zoom in and out.
5. The camera cannot pass through any rigid objects.
6. After the camera moves away from a colliding rigid object, it gradually returns to its original distance.
7. If the camera encounters an object and you use the mouse scroll wheel to zoom in, the camera needs to respond immediately, and the 6th point no longer occurs thereafter.
8. If the camera hits the ground during rotation, it stops rotating up and down around the character and instead rotates up and down around itself. The left and right rotation still revolves around the character.



This requirement can be divided into two parts: camera rotation and camera rigidity. For simplicity, let's first solve the issue of camera rotation, which refers to the first three points of the requirement.

Camera position indicator
----------------
Before we proceed to the formal resolution of camera operations, there is one more issue that needs to be addressed: the representation of the camera position. This can be done in multiple ways:

- Camera world coordinates
- Camera coordinates relative to the character
- Direction and distance of the camera in the character coordinate system

Because in our needs, the camera is transformed according to the position of the character, so here I use the third method, and the camera in the control always aims at the character, so only distance information needs to be saved in the camera.

```c#
float curDistance = 5F;
```

Camera Rotation
-------------
Continuing to further divide the camera rotation behavior, it can be divided into left button rotation and right button rotation. Now let's complete these two rotations step by step. Firstly, I will set the camera as a child object of the character, so that basic camera movements will automatically follow the character.

### Rotate with Left Mouse Button ###
When it comes to rotating with the left mouse button alone, the requirement is quite simple: **the camera rotates while the character remains stationary**. This is similar to a camera that observes a model, allowing the camera to observe the central object from any angle.

To obtain the state of the left mouse button in Unity, you can use the statement: `Input.GetMouseButton(0)` (Note: all code-related references will be in C#). Similarly, to check the state of the right mouse button, you can use: `Input.GetMouseButton(1)`. To retrieve the movement position of the mouse cursor (which can be understood as the offset of the cursor on the X and Y axes between frames), you can use: `Input.GetAxis("Mouse X"); Input.GetAxis("Mouse Y")`. Now, let's proceed to retrieve the movement information of the cursor after the left mouse button is pressed.

```csharp
if (Input.GetMouseButton(0))
{
    float x = Input.GetAxis("Mouse X");
    float y = Input.GetAxis("Mouse Y");
}
```
The code is simple, and now comes the crucial part: how to control the camera rotation. To understand rotation, some knowledge about quaternions is needed (there are many online resources available, so I won't list them here). One important aspect of quaternions is that they can easily represent rotations, especially rotations around a specific vector. Once you understand quaternions, implementing the camera rotation around a character should not be difficult.

One more thing to note is that the quaternion rotation axis is just a vector with the origin as the starting point. If you want to use a point `O` in the world coordinate system as the origin and a vector `V` starting from that point as the rotation axis, you need to perform a coordinate system transformation. In simple terms, you need to transform the point `P` that needs to be rotated into a coordinate system with `O` as the origin, rotate it based on `V`, and then transform it back to the world coordinate system. Based on these operations, a utility function can be written as follows:

```c#
Vector3 MyRotate(Vector3 oldPosition, float angle, Vector3 axis, Vector3 axisPosition)
{
// Construct a quaternion with `axis` as the rotation axis. This rotation is in the character's coordinate system.
    Quaternion rotation = Quaternion.AngleAxis(angle, axis);
// Here we are performing a coordinate system transformation, converting the camera's world coordinates into coordinates in the character's coordinate system.
    Vector3 offset = oldPosition - axisPosition;
// Calculate rotation and transform back into world coordinate system
    return axisPosition + (rotation * offset);
}
```
`Quaternion` is a type in Unity that represents quaternions. By adding the previously detected mouse left-click, you can complete the left-click control to rotate the camera left and right.

The code to control the camera's left and right rotation by moving the mouse left and right can be directly provided as:

[to_be_replaced[Code]]

```c#
newForward = MyRotate(newForward, x, up, Vector3.zero);
```
Because only the forward vector is being rotated here and there is no coordinate system transformation involved, the fourth parameter is set to `Vector3.zero`.

Controlling the rotation in the up and down direction is a bit more difficult to understand compared to the left and right rotation because the rotation axis keeps changing (assuming here that the character's "up" direction is always the positive Y-axis). It's important to note that the camera is also continuously rotating and keeping the character in the center of the view. In this case, the camera's right direction is the axis we want to rotate around (imagine the camera's right as the character's right). With this understanding, the code for the up and down rotation becomes quite simple:


```csharp
newForward = MyRotate(newForward, -y, transform.right, Vector3.zero);
```

###Right-click Rotation###
After performing a left-click rotation, right-click rotation is quite simple. You just need to set the character's forward direction when rotating left or right.

```csharp
player.forward = Vector3.Normalize(new Vector3(oldForward.x, 0, oldForward.z));
```

The code for vertical rotation is the same as the code for left click.

###First left click, then right click###
Although you can rotate separately with the left click and the right click above, once you rotate with the left click first and then perform the right click operation, a problem will arise: the character's forward direction will be different from the camera's forward direction! This causes the camera and the character's orientation to separate, making the actual operation very strange. So, when we rotate with the right click, we need to adjust the character first to align with the camera's forward direction:

```csharp
player.forward = Vector3.Normalize(new Vector3(oldForward.x, 0, oldForward.z));

```

- - -

###Euler Angle Gimbal Lock###
Up until now, the camera rotation is almost complete, but there is one more thing to be aware of: Euler Angle Gimbal Lock. I won't go into detail about the theory here, but those who are interested can search for it on their own. In the case of the camera here, when the camera rotates up or down to align with the upward direction of the character, the camera's perspective undergoes a sudden change. This is because when the camera reaches the top or bottom of the character, the camera's upward direction experiences a sudden change (since the Y value of the camera's upward direction needs to be greater than zero). Therefore, we need to limit the range of the camera's up and down rotation to prevent gimbal lock from occurring. The operation is very simple, just restrict the angle between the camera's forward direction and the character's upward direction.

```c#
if ((Vector3.Dot(transform.forward, transform.parent.up) >= -0.95F || y > 0) &&
    (Vector3.Dot(transform.forward, transform.parent.up) <= 0.95F || y < 0))
```

### Full Code ###

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

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki_blog/issues/new) if any omissions.
