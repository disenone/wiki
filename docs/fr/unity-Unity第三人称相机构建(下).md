---
layout: post
title: Construction d'un système de caméra à la troisième personne dans Unity (partie
  2)
categories:
- unity
catalog: true
tags:
- dev
description: Je veux créer une caméra troisième personne dans Unity, dont le comportement
  fait référence à la caméra troisième personne de World of Warcraft. Ici, nous allons
  résoudre le problème du rigide de la caméra.
---

<meta property="og:title" content="Unity第三人称相机构建(下)" />

Le dernier épisode a traité [la rotation de l'appareil photo](unity-Unity第三人称相机构建(上)Les fichiers .md), donc le problème que nous devons résoudre maintenant est la rigidité de l'appareil photo, comment procéder ?

Rigidité de l'appareil photo
--------------
Revenons sur les besoins évoqués précédemment :

Molette de la souris : contrôle du zoom de la caméra
5. La caméra ne peut pas traverser n'importe quel objet rigide.
6. L'appareil photo revient lentement à sa distance d'origine après avoir quitté l'objet rigide qui a subi la collision.
7. Si la caméra entre en contact avec un corps rigide, l'utilisation de la molette de la souris pour zoomer doit entraîner une réaction immédiate de la caméra, après quoi le point 6 ne se produira plus ; il est impossible d'effectuer une opération de zoom après avoir heurté le sol.
La caméra a heurté le sol en tournant, cessant de tourner autour du personnage de haut en bas, pour tourner autour d'elle-même de haut en bas. La rotation de gauche à droite reste autour du personnage.


Ces quelques points signifient que : lorsque la caméra rencontre un objet rigide, elle est contrainte de se rapprocher du personnage. Nous souhaitons ensuite que la caméra, en s'éloignant, puisse revenir lentement à sa distance d'origine. Cependant, si après un rapprochement automatique, nous utilisons la molette pour rapprocher manuellement, cela indique que la caméra s'éloigne de l'objet en collision. Dans ce cas, la distance rapprochée représente la distance réelle de la caméra. Examinons ces besoins point par point.

Contrôle à molette
----------
Contrôler la molette de la souris est assez simple, il suffit simplement de savoir que pour obtenir les informations de la molette, vous pouvez utiliser `Input.GetAxis("Mouse ScrollWheel")`, puis définir les valeurs maximale et minimale de la distance, et c'est bon :

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

Il est impossible de traverser un objet rigide.
--------------------
Cela nécessite de détecter le contact entre la caméra et le corps rigide, il existe une fonction pour réaliser cette fonctionnalité :

```c#
static bool Raycast(Ray ray, RaycastHit hitInfo, float distance = Mathf.Infinity, int layerMask = DefaultRaycastLayers);
```

Se référer à la [Référence](http://docs.unity3d.com/Documentation/ScriptReference/Physics.Raycast.html)Nous pouvons réaliser la détection de collision de cette manière :

```c#
RaycastHit hitInfo;
if (Physics.Raycast(playerTransform.position, desiredPosition - playerTransform.position,
    out hitInfo, (playerTransform.position - desiredPosition).magnitude, 1))
{
    curDistance = hitInfo.distance;
}
```

`targetPosition` is the position of the collision, you just need to set the camera's position to the collision position.

Après avoir quitté le corps rigide, revenez lentement à la distance d'origine.
---------------------------------
Pour réaliser cette fonctionnalité, il faut d'abord enregistrer la distance à laquelle l'appareil photo doit se trouver (`desiredDistance`) et la distance actuelle (`curDistance`). Ensuite, on stocke d'abord le résultat de l'opération de la molette dans `desiredDistance`, puis on calcule la nouvelle distance de l'objet en fonction des collisions.
Lorsque la caméra quitte le corps rigide ou entre en collision avec un autre corps plus éloigné, il n'est pas possible de simplement attribuer la position de la collision à la caméra. Il est nécessaire d'utiliser une vitesse de déplacement pour se déplacer vers la nouvelle distance. Commençons par obtenir cette nouvelle distance :

```c#
float newDistance = desiredDistance;
RaycastHit hitInfo;
if (Physics.Raycast(playerTransform.position, desiredPosition - playerTransform.position,
    out hitInfo, (playerTransform.position - desiredPosition).magnitude, 1))
{
    newDistance = hitInfo.distance;
}
```

Alors, comment peut-on déterminer si l'appareil photo se déplace vers une distance plus éloignée ? Vous pouvez comparer les `newDistances` avec la distance actuelle :

```c#
// Se déplacer vers une distance plus proche
if (newDistance < curDistance)
{
    curDistance = newDistance;
}
Déplacez-vous vers une distance plus lointaine
else if(newDistance > curDistance)
{
}
```

Alors, une fois que vous avez déterminé que vous devez vous déplacer à une plus grande distance, il est assez intuitif de simplement ajouter une vitesse pour se déplacer:

```c#
curDistance = Math.Min(curDistance + Time.deltaTime * autoZoomOutSpeed, newDistance);

```
Nous avons déjà finalisé le fonctionnement général de l'appareil photo, il reste quelques détails à régler.

Lorsqu'on rencontre un rouleau rigide, le rouleau se rapproche, le sol ne se réduit pas.
------------------
Il y a deux exigences ici :

1. On ne peut que se rapprocher après avoir rencontré un corps rigide, pas s'en éloigner.
Après avoir touché le sol, il est impossible de redimensionner.

Tout d'abord, utilisez des variables pour sauvegarder l'état de collision de la caméra :

```c#
bool isHitGround = false;       // Indique si une collision avec le sol a eu lieu
bool isHitObject = false;       // Indique si un corps rigide est en collision (autre que le sol)
```

Ajoutez une condition pour identifier le zoom avec la roulette de défilement:

```c#
if (zoom != 0F && (!isHitGround || (isHitObject && zoom > 0F)) )
{
    // calculate distance
}
```

Rencontre le sol et tourne autour de soi-même de haut en bas.
-----------------
Cette fonction est un peu complexe à mettre en place, car notre hypothèse selon laquelle la caméra était toujours pointée vers le personnage ne tient plus. Il faut alors diviser en deux vecteurs : **l'orientation de la caméra elle-même (`desireForward`)** et **la direction du joueur vers la caméra (`cameraToPlayer`)**, puis calculer les valeurs de ces deux vecteurs. Le premier détermine l'orientation de la caméra, tandis que le second détermine sa position. Pour simplifier, référez-vous au [épisode précédent](unity-Unity第三人称相机构建(上)La fonction de rotation de (.md) est décomposée en rotation autour de X (`RotateX`) et rotation autour de Y (`RotateY`). Ainsi, lors du calcul de `cameraToPlayer` pour `RotateY`, ajoutez une condition :

```c#
if ((!isHitGround) || 
    (isHitGround && transform.forward.y <= cameraToPlayer.y && yAngle > 0))
{
    cameraToPlayer = RotateY(cameraToPlayer, playerTransform.up, 
        transform.right, yAngle);
}
```

Cette condition se compose de deux parties :

- N'a pas touché le sol
Rencontrer le sol, mais se préparer à le quitter.

Ensuite, utilisez `cameraToPlayer` pour calculer la position de la caméra :

```c#
transform.position = playerTransform.position - cameraToPlayer * curDistance;
```

Et calculez l'orientation de la caméra lorsque nécessaire (c'est-à-dire lorsqu'elle touche le sol) :

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

Nous avons tous réalisé ce type de comportement de l'appareil photo.

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


> Ce message a été traduit en utilisant ChatGPT, veuillez donner votre [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Identifiez toute omission éventuelle. 
