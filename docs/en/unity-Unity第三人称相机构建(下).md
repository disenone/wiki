---
layout: post
title: Building a Third-Person Camera in Unity (Part 2)
categories:
- unity
catalog: true
tags:
- dev
description: I want to create a third-person camera in Unity, with the camera behavior
  inspired by the third-person camera in "World of Warcraft". Here we will solve the
  issue with the camera's rigid body.
---


We have finished discussing the [rotation of the camera](unity-Building-a-Third-Person-Camera-in-Unity-Part-1.md) in the previous episode. Now, the problem we need to solve is the rigidity of the camera. How should we do it?

Camera Rigidity
--------------
Reviewing the requirements mentioned earlier:

4. Mouse Wheel: Control the camera zoom.
5. The camera cannot pass through any rigid objects.
6. After the camera moves away from a colliding rigid object, it slowly returns to its original distance.
7. If the camera encounters a rigid body and the mouse wheel is used to zoom in, the camera needs to respond immediately and point 6 will no longer occur; after colliding with the ground, scaling operations are not allowed.
8. When the camera rotates and touches the ground, it stops rotating up and down around the character and instead rotates up and down around itself, while left and right rotation still revolves around the character.


The meaning of these points is: When the camera encounters a rigid object, it is forced to get closer to the character. So, we want the camera to slowly return to its original distance when it moves away. However, if the camera is manually zoomed in using the scroll wheel after automatically zooming in, it means that the camera is moving away from the object it collided with. In this case, the zoomed-in distance is the actual distance of the camera. Now, let's analyze these requirements step by step.

Scroll control
----------
Controlling the mouse scroll wheel is very simple. You just need to know that to obtain the scroll wheel information, you use `Input.GetAxis("Mouse ScrollWheel")`, and then set the maximum and minimum values for the distance. That's it.

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

Here, `playerTransform` points to the character.

Cannot penetrate through any rigid object.
--------------------
This requires detecting the contact between the camera and the rigid body. There is a function that can achieve this functionality:

`[to_be_replaced[function_name]]`

```c#
static bool Raycast(Ray ray, RaycastHit hitInfo, float distance = Mathf.Infinity, int layerMask = DefaultRaycastLayers);
```

Refer to Unity's [Reference](http://docs.unity3d.com/Documentation/ScriptReference/Physics.Raycast.html) for specific usage. We can implement collision detection like this:

```c#
RaycastHit hitInfo;
if (Physics.Raycast(playerTransform.position, desiredPosition - playerTransform.position,
    out hitInfo, (playerTransform.position - desiredPosition).magnitude, 1))
{
    curDistance = hitInfo.distance;
}
```

`targetPosition` is the position of the collision. Set the camera's position to the collision position and you're good to go.

After leaving the rigid body, slowly return to the original distance.
---------------------------------
To complete this functionality, it is necessary to first record the desired distance (`desiredDistance`) and the current distance (`curDistance`) that the camera should be positioned at. The result of the scroll wheel operation should be stored in `desiredDistance` first, and then the new distance of the object should be calculated based on collision. 

When it is detected that the camera has moved away from the rigid body or collided with a further rigid body, it is not directly assigned the position of the collision to the camera. Instead, a movement speed is used to move towards the new distance. Let's first obtain the new distance:

```c#
float newDistance = desiredDistance;
RaycastHit hitInfo;
if (Physics.Raycast(playerTransform.position, desiredPosition - playerTransform.position,
    out hitInfo, (playerTransform.position - desiredPosition).magnitude, 1))
{
    newDistance = hitInfo.distance;
}
```

So how can we determine if the camera is moving further away? We can compare `newDistances` with the current distance.

```c#
// Move closer
if (newDistance < curDistance)
{
    curDistance = newDistance;
}
// Move to a greater distance
else if(newDistance > curDistance)
{
}
```

Then, judging by moving to a farther distance, it becomes very intuitive. Just add speed to move.

```c#
curDistance = Math.Min(curDistance + Time.deltaTime * autoZoomOutSpeed, newDistance);

```
We have completed the general behavior of the camera, there are still some details that need to be addressed.

After encountering a rigid body, the scroll wheel zooms in without scaling the ground.
------------------
[to_be_replace[这里有两个要求：]]

1. After encountering a rigid body, you can only get closer, not further away.
2. After encountering the ground, scaling is not allowed.

First, use a variable to keep track of the collision status of the camera:

```c#
bool isHitGround = false;       // Indicates whether it hits the ground
bool isHitObject = false;       // Indicates whether it hits a rigid body (excluding the ground)
```

Add condition judgment when judging scroll zoom:

```c#
if (zoom != 0F && (!isHitGround || (isHitObject && zoom > 0F)) )
{
    // calculate distance
}
```

Land on the ground and rotate around yourself up and down.
-----------------
This functionality is a bit tricky to implement because our previous assumption that the camera is always focused on the character no longer holds true. Now we need to separate it into two vectors: the desired orientation of the camera (desireForward) and the direction from the player to the camera (cameraToPlayer). We calculate the values of these two vectors separately, with the former determining the camera's orientation and the latter determining its position. To simplify things, we split the rotation function mentioned in the previous episode (unity-Unity第三人称相机构建(上).md) into two parts: X rotation (RotateX) and Y rotation (RotateY). When calculating the RotateY for cameraToPlayer, we include the following condition:

```c#
if ((!isHitGround) || 
    (isHitGround && transform.forward.y <= cameraToPlayer.y && yAngle > 0))
{
    cameraToPlayer = RotateY(cameraToPlayer, playerTransform.up, 
        transform.right, yAngle);
}
```

This condition has two parts:

- Did not touch the ground
- Touched the ground, but preparing to leave the ground

Then calculate the position of the camera using `cameraToPlayer`:

```c#
transform.position = playerTransform.position - cameraToPlayer * curDistance;
```

And calculate the orientation of the camera when needed (when it hits the ground):

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

> Original: <https://disenone.github.io/wiki>  
> This post is protected by [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by/4.0/deed.en) agreement, should be reproduced with attribution.


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
