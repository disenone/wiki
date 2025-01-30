---
layout: post
title: Construction du système de caméra à la troisième personne dans Unity (Partie
  1)
categories:
- unity
catalog: true
tags:
- dev
description: Je veux créer une caméra en troisième personne dans Unity, inspirée du
  comportement de la caméra en troisième personne dans "World of Warcraft". Commençons
  par résoudre le problème de rotation de la caméra.
figure: null
---

<meta property="og:title" content="Unity第三人称相机构建(上)" />

Je souhaite créer une caméra à la troisième personne dans Unity, dont le comportement s'inspire de la caméra à la troisième personne de « World of Warcraft ». Les exigences spécifiques sont :

1. Clic gauche de la souris : contrôler la rotation de la caméra autour du personnage, le personnage ne tourne pas.
Clic droit de la souris : contrôle la rotation de la caméra autour du personnage, rotation correspondant à la direction frontale du personnage (transform.forward dans Unity), la direction vers le haut du personnage reste inchangée.
Après avoir tourné à gauche avec le clic gauche de la souris, tournez à droite à nouveau. L'orientation du personnage devant s'ajuste immédiatement en fonction de la rotation effectuée avec le clic gauche, puis tournez à droite. À ce stade, cela revient à effectuer deux rotations avec le clic droit.
4. Molette de la souris : contrôler la distance de la caméra.
L'appareil photo ne peut pas traverser aucun objet rigide.
6. La caméra revient lentement à sa distance d'origine après avoir quitté l'objet rigide de la collision.
Si la caméra entre en contact avec un objet, utilisez la molette de la souris pour rapprocher la caméra. La caméra doit réagir immédiatement, et ensuite le point 6 ne se produira plus.
La caméra a heurté le sol en tournant, arrêtant de tourner autour de la personne de haut en bas, et commençant à tourner autour d'elle-même de façon verticale. Le mouvement horizontal reste autour de la personne.



Ce besoin peut être divisé en deux parties : rotation de la caméra, rigidité de la caméra. Pour simplifier, commençons par résoudre le problème de la rotation de la caméra, c'est-à-dire les trois premiers points du besoin.

Indication de la position de la caméra
----------------
Avant de résoudre officiellement le fonctionnement de l'appareil photo, il y a encore un problème à régler : la représentation de la position de l'appareil photo. Cela peut se faire de plusieurs manières :

- Coordonnées mondial de la caméra
Les coordonnées de l'appareil photo par rapport à la personne.
La direction et la distance de la caméra dans le système de coordonnées des personnages.

Dans notre cas, la caméra se déplace en fonction de la position des personnages, donc j'utilise la troisième méthode ici. De plus, la caméra reste constamment focalisée sur les personnages dans le contrôle, ce qui signifie qu'il suffit de sauvegarder les informations de distance dans la caméra.

```c#
float curDistance = 5F;
```

Caméra en rotation
-------------
Poursuivons la subdivision des actions de rotation de la caméra, qui peuvent être divisées en rotation à gauche et rotation à droite. Exécutons maintenant ces deux rotations étape par étape. Tout d'abord, je configure la caméra comme un objet enfant du personnage, de sorte que certains mouvements basiques du personnage suivront automatiquement la caméra.

###Tourner à gauche###
En regardant simplement la rotation du bouton gauche, la demande est très simple : **la caméra tourne, le personnage ne tourne pas**, ce qui revient à une caméra d'observation du modèle, la caméra pouvant observer l'objet central sous n'importe quel angle.

Dans Unity, pour obtenir l'état du bouton gauche de la souris, on utilise la déclaration : `Input.GetMouseButton(0)` (note : les sections suivantes concernant le code utilisent C#). Évidemment, le bouton droit est `Input.GetMouseButton(1)`. Pour obtenir les informations sur le mouvement du curseur de la souris (que l'on peut comprendre comme le déplacement du curseur sur l'axe X-Y entre les images), on utilise : `Input.GetAxis("Mouse X"); Input.GetAxis("Mouse Y")`. Commençons par obtenir les informations de déplacement du curseur après avoir cliqué sur le bouton gauche de la souris :

```csharp
if (Input.GetMouseButton(0))
{
    float x = Input.GetAxis("Mouse X");
    float y = Input.GetAxis("Mouse Y");
}
```
 
Le code est assez simple, mais le point crucial est le suivant : comment contrôler la rotation de la caméra. Pour bien comprendre cette rotation, il vous faudra avoir des connaissances sur les quaternions (il y a de nombreuses ressources en ligne à ce sujet, je ne vais pas toutes les énumérer ici). Un point important à retenir sur les quaternions est qu'ils permettent de construire facilement des rotations, notamment autour d'un vecteur donné. Une fois que vous aurez compris les quaternions, il sera facile d'implémenter la rotation de la caméra autour du personnage.

Un autre point à noter est que l'axe de rotation des quaternions n'est qu'un vecteur, partant de l'origine. Si l'on souhaite prendre un point `O` du système de coordonnées mondial comme origine et le vecteur `V` partant de ce point comme axe de rotation, il est nécessaire de transformer le système de coordonnées. En d'autres termes, il s'agit de transformer le point `P` à faire pivoter dans le système de coordonnées avec l'origine `O`, de le faire pivoter selon `V`, puis de le retransformer dans le système de coordonnées mondial. En se basant sur ces opérations, il est possible d'écrire une fonctionnalité :

```c#
Vector3 MyRotate(Vector3 oldPosition, float angle, Vector3 axis, Vector3 axisPosition)
{
Crée un quaternion avec l'axe comme axe de rotation, c'est une rotation dans le repère de l'entité.
    Quaternion rotation = Quaternion.AngleAxis(angle, axis);
Il s'agit ici de réaliser une transformation de coordonnées, en convertissant les coordonnées mondiales de la caméra en coordonnées dans le référentiel du personnage.
    Vector3 offset = oldPosition - axisPosition;
// Calculer la rotation et transformer dans le système de coordonnées mondiales
    return axisPosition + (rotation * offset);
}
```
"Quaternion" is the type used in Unity to represent quaternions. Combined with the previous left mouse button detection, you can now achieve camera rotation to the left or right with the left mouse button.

Le code qui contrôle la rotation de la caméra à gauche et à droite en déplaçant la souris de gauche à droite peut être donné directement :

```c#
newForward = MyRotate(newForward, x, up, Vector3.zero);
```
Comme seule la première vector fait pivoter ici, sans implication de changement de système de coordonnées, le quatrième paramètre est défini comme `Vector3.zero`.

Contrôler la rotation verticale par rapport à la rotation horizontale peut être un peu difficile à comprendre, car l'axe de rotation change constamment (en supposant que le haut du personnage soit toujours l'axe Y positif). Il est important de noter que la caméra elle-même effectue également une rotation tout en maintenant le personnage au centre de la vue. Ainsi, la direction droite de la caméra (right) devient l'axe de rotation souhaité (similaire à la droite du personnage). Avec cette compréhension, le code pour la rotation verticale devient également simple :

```csharp
newForward = MyRotate(newForward, -y, transform.right, Vector3.zero);
```

###Clic droit pour faire pivoter###
Effectuer une rotation vers la gauche est déjà fait, donc faire une rotation vers la droite est assez simple, il suffit de définir l'orientation du personnage lors des rotations à gauche et à droite :

```csharp
player.forward = Vector3.Normalize(new Vector3(oldForward.x, 0, oldForward.z));
```

Faites tourner vers le haut ou vers le bas comme le code de la touche gauche.

###Appuyez d'abord sur la touche gauche, puis sur la touche droite###
Bien que vous puissiez effectuer des rotations à gauche ou à droite séparément, une difficulté survient lorsque vous effectuez d'abord une rotation à gauche puis que vous passez à une opération à droite : la direction avant du personnage ne correspond plus à celle de la caméra ! Cela entraîne une séparation entre la direction avant de la caméra et celle du personnage, ce qui rend l'interaction très étrange. Ainsi, lors de la rotation à droite, il est nécessaire d'ajuster d'abord la direction du personnage pour qu'elle corresponde à celle de la caméra.

```csharp
player.forward = Vector3.Normalize(new Vector3(oldForward.x, 0, oldForward.z));

```

- - - 

###Les angles d'Euler lock locked###
Jusqu'ici, la rotation de la caméra est presque terminée, mais il y a encore un problème à prendre en compte : le verrouillage des angles d'Euler. Je ne vais pas approfondir le principe ici, ceux qui sont intéressés peuvent faire des recherches par eux-mêmes. Pour la situation de la caméra ici, lorsque la caméra tourne vers le haut pour se superposer à la direction verticale du personnage, l'angle de vue de la caméra subit un changement soudain. Cela se produit lorsque la caméra atteint le sommet ou le bas du personnage, provoquant un changement soudain dans la direction verticale de la caméra (car la valeur Y de la direction verticale de la caméra doit toujours être supérieure à zéro). C'est pour cela que nous devons limiter la plage de rotation de la caméra vers le haut et vers le bas afin d'éviter le verrouillage des angles d'Euler. La manipulation est très simple, il s'agit de limiter l'angle entre la direction vers l'avant de la caméra et la direction verticale du personnage :

```c#
if ((Vector3.Dot(transform.forward, transform.parent.up) >= -0.95F || y > 0) &&
    (Vector3.Dot(transform.forward, transform.parent.up) <= 0.95F || y < 0))
```

###Code complet###

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

--8<-- "footer_fr.md"


> Ce post a été traduit à l'aide de ChatGPT, veuillez laisser vos [**retours**](https://github.com/disenone/wiki_blog/issues/new)Veuillez signaler toute omission. 
