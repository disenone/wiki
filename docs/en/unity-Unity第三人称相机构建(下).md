---
layout: post
title: Building a Third-Person Camera in Unity (Part 2)
categories:
- unity
catalog: true
tags:
- dev
description: I want to create a third-person camera in Unity, and I want the camera's
  behavior to be similar to the third-person camera in World of Warcraft. Let's tackle
  the camera's rigid body issue here.
---

<meta property="og:title" content="Unity第三人称相机构建(下)" />

The previous episode concluded with [camera rotation](unity-Unity第三人称相机构建(上).md), so now the issue we need to address is the rigidity of the camera, how should we proceed?

Camera rigidity
--------------
Looking back at the previously mentioned requirements:

Mouse scroll wheel: Control the camera zoom.
The camera cannot pass through any rigid object
6. The camera slowly returns to its original distance after leaving the rigid object of the collision.
If the camera encounters a rigid body, use the mouse wheel to zoom in on the camera, the camera needs to respond immediately, and point 6 will not occur afterwards; after colliding with the ground, scaling operations cannot be performed.
The camera hit the ground while rotating, stopped spinning around the character vertically, switched to spinning around itself vertically, while still revolving around the character horizontally.


These points mean that when the camera encounters a rigid object, it will be forced to move closer to the subject. We want the camera to gradually return to its original distance when it moves away. However, if after the automatic zooming in, the manual zooming in is done using the wheel, it indicates that the camera has moved away from the colliding object, and this zoomed-in distance represents the camera's actual distance. Now, let's break down these requirements step by step.

Roller control
----------
The mouse wheel control is quite simple; you just need to know that obtaining the scroll wheel information is done using `Input.GetAxis("Mouse ScrollWheel")`, and then set the maximum and minimum values for the distance, and it's all set.

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

Here `playerTransform` points to the character.

Cannot pass through any rigid object.
--------------------
This requires detecting the contact between the camera and the rigid body, and there is a function that can achieve this.

```c#
static bool Raycast(Ray ray, RaycastHit hitInfo, float distance = Mathf.Infinity, int layerMask = DefaultRaycastLayers);
```

Please refer to Unity's [Reference](http://docs.unity3d.com/Documentation/ScriptReference/Physics.Raycast.html)We can achieve collision detection in the following way:

```c#
RaycastHit hitInfo;
if (Physics.Raycast(playerTransform.position, desiredPosition - playerTransform.position,
    out hitInfo, (playerTransform.position - desiredPosition).magnitude, 1))
{
    curDistance = hitInfo.distance;
}
```

`targetPosition` is the position of the collision; just set the camera's position to the collision position.

After leaving the rigid body, slowly return to the original distance.
---------------------------------
To achieve this functionality, we first need to separately record the distance the camera should be at (`desiredDistance`) and the current distance (`curDistance`). We then store the result of the scroll wheel operation in `desiredDistance`, and subsequently calculate the new distance of the object based on collisions.
When the camera is detected to leave the rigid body or collide with a more distant rigid body, the collision position cannot be directly assigned to the camera; instead, a movement speed needs to be used to move towards the new distance. First, we need to obtain the new distance:

```c#
float newDistance = desiredDistance;
RaycastHit hitInfo;
if (Physics.Raycast(playerTransform.position, desiredPosition - playerTransform.position,
    out hitInfo, (playerTransform.position - desiredPosition).magnitude, 1))
{
    newDistance = hitInfo.distance;
}
```

So how can you determine if the camera is moving further away? You can compare `newDistances` with the current distance:

```c#
// Move closer.
if (newDistance < curDistance)
{
    curDistance = newDistance;
}
Move to a greater distance.
else if(newDistance > curDistance)
{
}
```

So when it comes to determining the movement to a farther distance, it becomes quite intuitive; simply add a velocity to move.

```c#
curDistance = Math.Min(curDistance + Time.deltaTime * autoZoomOutSpeed, newDistance);

```
We have completed the general behavior of the camera, but there are still some details that need to be addressed.

When encountering a rigid body, the rear roller approaches without scaling the ground.
------------------
There are two requirements here:

1. After encountering a rigid body, you can only move closer, not farther away.
Cannot shrink after touching the ground.

First, use a variable to save the camera's collision status:

```c#
bool isHitGround = false;       // Indicates whether it has collided with the ground
bool isHitObject = false;       // Indicates whether a rigid body is collided (excluding the ground)
```

Add conditional judgment when determining the scroll wheel zoom:

```c#
if (zoom != 0F && (!isHitGround || (isHitObject && zoom > 0F)) )
{
    // calculate distance
}
```

Rotating up and down around itself upon contact with the ground.
-----------------
(unity-Unity第三人称相机构建(上)Split the rotation function of .md file into X rotation (`RotateX`) and Y rotation (`RotateY`), then when calculating `cameraToPlayer`'s `RotateY`, add the condition:

```c#
if ((!isHitGround) || 
    (isHitGround && transform.forward.y <= cameraToPlayer.y && yAngle > 0))
{
    cameraToPlayer = RotateY(cameraToPlayer, playerTransform.up, 
        transform.right, yAngle);
}
```

This condition consists of two parts:

Not touched the ground.
- Touching the ground, but ready to leave the ground

Then calculate the position of the camera using `cameraToPlayer`:

```c#
transform.position = playerTransform.position - cameraToPlayer * curDistance;
```

And calculate the camera orientation when needed (when it meets the ground):

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

We have achieved all the functions of this camera.

Complete code:

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


> This post was translated using ChatGPT, please provide [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions. 
