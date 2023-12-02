---
layout: post
title: Building a third-person camera in Unity (Part 2)
categories:
- unity
catalog: true
tags:
- dev
description: I want to create a third-person camera in Unity, with the camera's behavior
  referencing the third-person camera in "World of Warcraft". Here we will address
  the camera's rigid body issue.
---

<meta property="og:title" content="Unity第三人称相机构建(下)" />

The previous episode was about [camera rotation](unity-Third Person Camera Setup (Part I).md). So now, the problem we need to solve is the rigidity of the camera. How should we do it?

Camera rigidity
--------------
Reviewing the requirements previously mentioned:

4. Mouse scroll wheel: control camera zooming.
5. The camera cannot pass through any rigid objects.
6. After the camera leaves a collision with a rigid object, it slowly returns to its original distance.
7. If the camera encounters a rigid body and the mouse scroll wheel is used to zoom in, the camera needs to react immediately, and point 6 no longer occurs afterwards; scaling operations cannot be performed after colliding with the ground.
8. When the camera in rotation touches the ground, stop rotating around the character up and down, and instead rotate up and down around itself, while left and right rotation still revolves around the character.


The meaning of these points is: When the camera encounters a rigid object, it is forced to get closer to the character. So, we want the camera to slowly return to its original distance when it moves away. However, if after automatically getting closer, you manually zoom in with the scroll wheel, it means that the camera is moving away from the object it collided with, and the zoom distance is the actual distance of the camera. Now let's analyze these requirements step by step.

Scroll control
----------
Scroll wheel control is very simple, you just need to know that obtaining the scroll wheel information is `Input.GetAxis("Mouse ScrollWheel")`, and set the maximum and minimum values for the distance and it's good to go:

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

`playerTransform` here refers to the character.

Cannot pass through any rigid objects.
--------------------
This requires checking the contact between the camera and the object. There is a function that can achieve this functionality:

```c#
static bool Raycast(Ray ray, RaycastHit hitInfo, float distance = Mathf.Infinity, int layerMask = DefaultRaycastLayers);
```

Refer to Unity's [Reference](http://docs.unity3d.com/Documentation/ScriptReference/Physics.Raycast.html) for specific usage. We can implement collision detection as follows:

```c#
RaycastHit hitInfo;
if (Physics.Raycast(playerTransform.position, desiredPosition - playerTransform.position,
    out hitInfo, (playerTransform.position - desiredPosition).magnitude, 1))
{
    curDistance = hitInfo.distance;
}
```

The `targetPosition` is the position of the collision. Set the camera's position to the collision position and you're good to go.

After leaving the rigid body, slowly return to the original distance.
---------------------------------
To accomplish this functionality, firstly, we need to record the desired distance (`desiredDistance`) and the current distance (`curDistance`) that the camera should be at. We will store the result of the scroll wheel operation in the `desiredDistance` variable and then calculate the new distance based on collision.

When we detect that the camera has moved away from the rigid body or has collided with a farther rigid body, we cannot directly assign the position of the collision to the camera. Instead, we need to use a movement speed to approach the new distance. Let's retrieve the new distance first:

```c#
float newDistance = desiredDistance;
RaycastHit hitInfo;
if (Physics.Raycast(playerTransform.position, desiredPosition - playerTransform.position,
    out hitInfo, (playerTransform.position - desiredPosition).magnitude, 1))
{
    newDistance = hitInfo.distance;
}
```

So how can we determine if the camera is moving to a greater distance? We can compare `newDistances` with the current distance:

```c#
// Move closer
if (newDistance < curDistance)
{
    curDistance = newDistance;
}
// Move towards a greater distance
else if(newDistance > curDistance)
{
}
```

So, to determine the movement to a further distance, it becomes very intuitive, just add a velocity to move:

```c#
curDistance = Math.Min(curDistance + Time.deltaTime * autoZoomOutSpeed, newDistance);

```
We have already completed the general behavior of the camera, but there are still some details that need to be handled.

After encountering a rigid body, the roller zooms in and the ground does not scale.
------------------
Here are two requirements:

Translate these text into English language:

1. After encountering a rigid body, you can only pull it closer, not farther apart.
2. After contacting the ground, you cannot scale it.

First, use a variable to store the collision status of the camera:

```c#
bool isHitGround = false;       // Indicates whether it has collided with the ground
bool isHitObject = false;       // Indicates whether it has collided with a rigid body (excluding the ground)
```

Add conditional judgment when determining the zooming of the scroll wheel:

```c#
if (zoom != 0F && (!isHitGround || (isHitObject && zoom > 0F)) )
{
    // calculate distance
}
```

Meet the ground and rotate around oneself up and down.
-----------------
This functionality is a bit complicated to implement. It is necessary because our previous assumption that the camera is always pointed at the character no longer holds true. At this point, we need to split it into two vectors: the camera's orientation (`desireForward`) and the direction from the character to the camera (`cameraToPlayer`). We calculate the values for these two vectors separately. The former determines the camera's orientation, while the latter determines the camera's position. For convenience, we have divided the rotation function from the previous episode into two parts: X rotation (`RotateX`) and Y rotation (`RotateY`). Therefore, when calculating `RotateY` for `cameraToPlayer`, we add a condition:

```c#
if ((!isHitGround) || 
    (isHitGround && transform.forward.y <= cameraToPlayer.y && yAngle > 0))
{
    cameraToPlayer = RotateY(cameraToPlayer, playerTransform.up, 
        transform.right, yAngle);
}
```

This condition has two parts:

- Did not touch the ground.
- Touched the ground but is ready to leave the ground.

Then use `cameraToPlayer` to calculate the position of the camera:

```c#
transform.position = playerTransform.position - cameraToPlayer * curDistance;
```

And calculate the orientation of the camera when necessary (i.e. when it encounters the ground):

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

We have implemented the behavior of this camera.

Complete code:

def hello_world():
    print("Hello, world!")
    
hello_world()

Output:
Hello, world!

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

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
