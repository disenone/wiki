---
layout: post
title: Unity Third Person Camera Setup Part 2
categories:
- unity
catalog: true
tags:
- dev
description: Je veux créer une caméra à la troisième personne dans Unity, basée sur
  le comportement de la caméra à la troisième personne de "World of Warcraft". Voyons
  comment résoudre le problème du corps de la caméra.
---

<meta property="og:title" content="Unity第三人称相机构建(下)" />

La dernière diffusion a traité de [la rotation de l'appareil photo](unity-Unity第三人称相机构建(上)Translate these text into French language: 

.md), donc le problème que nous devons résoudre maintenant est la rigidité de l'appareil photo, comment devrions-nous procéder ?

Rigidité de l'appareil photo
--------------
Revue des exigences précédemment mentionnées :

Molette de la souris : contrôle du zoom de la caméra
L'appareil photo ne peut pas passer à travers aucun objet rigide.
Lorsque l'appareil photo quitte un objet rigide après avoir été frappé, il revient lentement à sa distance d'origine.
Si la caméra rencontre un objet rigide, utilisez la molette de la souris pour rapprocher la caméra. La réaction de la caméra doit être instantanée, et le point 6 ne se produira plus par la suite. Après avoir heurté le sol, il n'est plus possible d'effectuer de zoom.
La caméra a heurté le sol en pivotant, cessant de tourner autour du personnage de haut en bas pour tourner autour d'elle-même de haut en bas, tout en continuant de tourner autour du personnage de gauche à droite.


Ces points signifient que lorsque l'appareil photo rencontre un objet rigide, il est contraint de se rapprocher de la personne, alors nous voulons que l'appareil photo puisse revenir lentement à sa distance d'origine lorsqu'il s'éloigne; mais si après avoir automatiquement rapproché la distance, nous rapprochons manuellement à nouveau avec la molette, cela signifie que l'appareil photo quitte l'objet en collision, alors cette distance rapprochée est la distance réelle de l'appareil photo. Explorons maintenant progressivement ces besoins.

Contrôle de la molette
----------
La manipulation de la molette de la souris est très simple, il vous suffit de connaître la commande pour obtenir les informations de la molette : `Input.GetAxis("Mouse ScrollWheel")`, puis de définir les valeurs maximale et minimale de la distance, et c'est tout !

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

Ici, `playerTransform` fait référence au personnage.

Impossible de traverser un objet rigide.
--------------------
Cela nécessite de détecter le contact entre la caméra et le corps rigide, il existe une fonction qui peut réaliser cette fonctionnalité :

```c#
static bool Raycast(Ray ray, RaycastHit hitInfo, float distance = Mathf.Infinity, int layerMask = DefaultRaycastLayers);
```

(http://docs.unity3d.com/Documentation/ScriptReference/Physics.Raycast.html)Nous pouvons détecter les collisions de la manière suivante :

```c#
RaycastHit hitInfo;
if (Physics.Raycast(playerTransform.position, desiredPosition - playerTransform.position,
    out hitInfo, (playerTransform.position - desiredPosition).magnitude, 1))
{
    curDistance = hitInfo.distance;
}
```

`targetPosition` is the position of the collision, setting the camera's position to the collision position will do the trick.

Après avoir quitté le corps rigide, revenir progressivement à la distance initiale.
---------------------------------
Pour accomplir cette fonction, il est d'abord nécessaire d'enregistrer séparément la distance à laquelle la caméra devrait être positionnée (`desiredDistance`) et la distance actuelle (`curDistance`). Enregistrez d'abord le résultat de l'opération de la molette dans `desiredDistance`, puis calculez la nouvelle distance de l'objet en fonction de la collision.
Lorsqu'il est détecté que la caméra s'éloigne du corps rigide ou entre en collision avec un autre corps plus lointain, il n'est pas possible de simplement attribuer la position de la collision à la caméra. Il est nécessaire de déplacer la caméra vers la nouvelle distance en utilisant une vitesse de déplacement. Tout d'abord, obtenons la nouvelle distance :

```c#
float newDistance = desiredDistance;
RaycastHit hitInfo;
if (Physics.Raycast(playerTransform.position, desiredPosition - playerTransform.position,
    out hitInfo, (playerTransform.position - desiredPosition).magnitude, 1))
{
    newDistance = hitInfo.distance;
}
```

Alors, comment peut-on identifier si l'appareil photo se déplace vers une distance plus lointaine ? On peut comparer les `newDistances` avec la distance actuelle :

```c#
Déplacez-vous vers une distance plus proche.
if (newDistance < curDistance)
{
    curDistance = newDistance;
}
Déplacer vers une distance plus lointaine
else if(newDistance > curDistance)
{
}
```

Alors, une fois qu'il est déterminé que l'on se déplace vers une distance plus éloignée, il est assez évident, il suffit d'ajouter une vitesse pour se déplacer :

```c#
curDistance = Math.Min(curDistance + Time.deltaTime * autoZoomOutSpeed, newDistance);

```
Nous avons déjà finalisé le fonctionnement général de l'appareil photo, il reste quelques détails à régler.

Lorsque vous heurtez un objet rigide, rapprochez les roues sans modifier l'échelle du sol.
------------------
Il y a deux exigences ici :

Après avoir rencontré un objet rigide, il est possible de se rapprocher mais pas de s'éloigner.
Lorsqu'il touche le sol, il ne peut pas se rétracter.

Tout d'abord, utilisez une variable pour enregistrer l'état de collision de la caméra :

```c#
bool isHitGround = false; // Indicates whether it has hit the ground
bool isHitObject = false;       // Indicates whether a collision with a rigid body (excluding the ground)
```

Ajoutez une condition de vérification lors de l'analyse pour le zoom de la molette.

```c#
if (zoom != 0F && (!isHitGround || (isHitObject && zoom > 0F)) )
{
    // calculate distance
}
```

Rencontrer le sol en tournant autour de soi-même de haut en bas.
-----------------
(unity-Unity第三人称相机构建(上)Translate these text into French language: 

Les fonctions de rotation de (.md) ont été décomposées en rotation selon X (`RotateX`) et en rotation selon Y (`RotateY`). Ainsi, lorsque vous calculez la rotation selon Y de `cameraToPlayer`, ajoutez la condition :

```c#
if ((!isHitGround) || 
    (isHitGround && transform.forward.y <= cameraToPlayer.y && yAngle > 0))
{
    cameraToPlayer = RotateY(cameraToPlayer, playerTransform.up, 
        transform.right, yAngle);
}
```

Ce critère se compose de deux parties :

N'a pas touché le sol.
Rencontrer le sol mais prêt à le quitter

Ensuite, utilisez `cameraToPlayer` pour calculer la position de la caméra :

```c#
transform.position = playerTransform.position - cameraToPlayer * curDistance;
```

Et calcule l'orientation de la caméra lorsque cela est nécessaire (c'est-à-dire lorsqu'elle rencontre le sol) :

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

Nous avons tous pris des mesures pour mettre en œuvre ce comportement de l'appareil photo.

Code complet :

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

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT, veuillez signaler [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Indiquez toute omission. 
