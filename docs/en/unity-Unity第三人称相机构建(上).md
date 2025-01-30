---
layout: post
title: Building a third-person camera in Unity (Part 1)
categories:
- unity
catalog: true
tags:
- dev
description: I want to create a third-person camera in Unity, with the camera behavior
  referencing the third-person camera from World of Warcraft. Let's first address
  the camera rotation issue.
figure: null
---

<meta property="og:title" content="Unity第三人称相机构建(上)" />

I want to create a third-person camera in Unity, with behavior inspired by the third-person camera in "World of Warcraft". The specific requirements are:

1. Left mouse button: Controls the camera to rotate around the character while the character remains stationary.
Right-click on the mouse: control the camera to rotate around the character, the character's forward direction (transform.forward in Unity) rotates accordingly, while the character's upward direction remains unchanged.
After rotating with the left mouse button, rotate again with the right mouse button. The character's front direction will immediately adjust according to the rotation of the left button. Then rotate according to the right button. At this point, it is equivalent to rotating twice with the right button.
Mouse scroll wheel: control camera zoom.
The camera cannot pass through any rigid object.
After the camera leaves the rigid object it collided with, it slowly returns to its original distance.
If the camera encounters an object, use the mouse wheel to zoom in, the camera needs to respond immediately, and point 6 will not occur thereafter.
The camera hit the ground while rotating and stopped spinning around the subject vertically. Instead, it started spinning vertically around itself, while still rotating horizontally around the subject.



This requirement can be divided into two parts: camera rotation and camera rigidity. To keep it simple, let's first address the issue of camera rotation, which corresponds to the first three points of the requirement.

Camera position indication.
----------------
Before formally addressing the camera operation, there is one more issue to resolve: indicating the camera position. This could be done in several ways:

- World coordinates of the camera
- The camera's coordinates relative to the subject.
The orientation and distance of the camera in the character coordinate system

Because in our requirements, the camera changes based on the character's position, I am using the third method here, and the camera is always focusing on the character in the control, so only distance information needs to be stored in the camera.

```c#
float curDistance = 5F;
```

Camera rotation
-------------
Continuing to break down the behavior of camera rotation, it can be divided into left mouse button rotation and right mouse button rotation. Now let's complete these two rotations step by step. First, I will set the camera as a child object of the character, so that the camera automatically follows some basic movements of the character.

###Rotate with the left mouse button.
Just looking at the left mouse button rotation, the requirement is very simple: **camera rotation, character not rotating**, this is equivalent to a camera model for observing, the camera can observe the central object at any angle.

To get the status of the left mouse button in Unity, you use the statement: `Input.GetMouseButton(0)` (note: the code mentioned later will be in C#). Clearly, the right button is `Input.GetMouseButton(1)`. The information for obtaining the mouse cursor's movement position (which can be understood as the cursor's offset on the X-Y axis between frames) is: `Input.GetAxis("Mouse X"); Input.GetAxis("Mouse Y")`. So, let's first retrieve the cursor's movement information after pressing the left mouse button:

```csharp
if (Input.GetMouseButton(0))
{
    float x = Input.GetAxis("Mouse X");
    float y = Input.GetAxis("Mouse Y");
}
```
 
The code is simple, now here comes the crucial part: how to control the camera for rotation. To understand rotation, some knowledge about quaternions is needed (there is a lot of information online, I won't list it here). An important aspect of quaternions is their ability to easily construct rotations, especially around a particular vector. Once you grasp quaternions, implementing camera rotation around a character is not difficult.

Another point to note is that the quaternion rotation axis is just a vector originating from the origin. If we want to take a specific point `O` in the world coordinate system as the new origin, and use the vector `V` originating from that point as the rotation axis, we need to perform a coordinate transformation. In simple terms, this means transforming the point `P` that needs to be rotated into a coordinate system where `O` is the origin, performing the rotation based on `V`, and then transforming back to the world coordinate system. Based on these operations, a functional function can be written:

```c#
Vector3 MyRotate(Vector3 oldPosition, float angle, Vector3 axis, Vector3 axisPosition)
{
Construct a quaternion with the axis as the rotation axis, which is the rotation in the character coordinate system.
    Quaternion rotation = Quaternion.AngleAxis(angle, axis);
Here we are doing a coordinate transformation, mapping the world coordinates of the camera to the coordinates in the character's coordinate system.
    Vector3 offset = oldPosition - axisPosition;
Calculate the rotation and transform it back into the world coordinate system.
    return axisPosition + (rotation * offset);
}
```
`Quaternion` is the type that represents quaternions in Unity, and with the previous detection of the left mouse button, you can achieve left mouse button control for rotating the camera left and right.

The code that controls the camera's left and right rotation by moving the mouse left and right can be provided directly:

```c#
newForward = MyRotate(newForward, x, up, Vector3.zero);
```
Because only the forward vector is being rotated here, without involving any coordinate system transformation, the fourth parameter is set to `Vector3.zero`.

Controlling up and down rotation is a bit harder to understand than left and right rotation because the axis of rotation is constantly changing (here we assume the character's up is always in the positive direction of the Y-axis). It's important to note that the camera is also continuously rotating, and the viewpoint is always focused on the character. Thus, the camera's right direction is the axis we want to rotate around (imagine the camera's right as the character's right). With this understanding, the code for up and down rotation becomes quite simple:

```csharp
newForward = MyRotate(newForward, -y, transform.right, Vector3.zero);
```

###Right-click to rotate###
After performing left-click rotation, right-click rotation becomes much simpler. You just need to set the character's facing direction when rotating left or right.

```csharp
player.forward = Vector3.Normalize(new Vector3(oldForward.x, 0, oldForward.z));
```

The code for rotating up and down is the same as the code for the left key.

###Left click first, then right click###
Although the left mouse button can rotate and the right mouse button can rotate separately, once you use the left mouse button to rotate first and then operate with the right mouse button, a problem arises: the character's forward direction and the camera's forward direction become different! At that point, the camera's and the character's forward directions become disconnected, making it quite strange to operate. Therefore, when we rotate with the right mouse button, we need to first adjust the character to align with the camera's forward direction.

```csharp
player.forward = Vector3.Normalize(new Vector3(oldForward.x, 0, oldForward.z));

```

- - - 

###Euler angle gimbal lock.
At this point, the camera's rotation is almost complete, but there’s one more issue to keep in mind: the Euler angle gimbal lock. I won’t go into the details of the principle here, but those interested can search for it themselves. In the context of the camera we’re dealing with, when the camera rotates up and down to align with the character's upward direction, the camera's perspective changes abruptly. This happens because when the camera reaches the top of the character's head or the bottom of their feet, the camera's upward direction experiences a sudden change (since the camera's upward Y value must always be greater than zero). Therefore, we need to restrict the camera's range of up and down rotation to prevent gimbal lock. The operation is quite simple: it involves limiting the angle between the camera's forward direction and the character's upward direction.

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

--8<-- "footer_en.md"


> This post was translated using ChatGPT, please provide your [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions. 
