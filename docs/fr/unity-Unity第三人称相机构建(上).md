---
layout: post
title: Unité construction de caméra à la troisième personne (Partie 1)
categories:
- unity
catalog: true
tags:
- dev
description: Je veux créer une caméra à la troisième personne dans Unity, dont le
  comportement est inspiré de la caméra à la troisième personne de "World of Warcraft".
  Commençons par résoudre le problème de rotation de la caméra.
figure: null
---

<meta property="og:title" content="Unity第三人称相机构建(上)" />

Je souhaite créer une caméra de troisième personne dans Unity, inspirée du mode de caméra de troisième personne de "World of Warcraft". Les exigences précises sont les suivantes :

Clic gauche de la souris : contrôle la rotation de la caméra autour du personnage, sans faire tourner le personnage
Clique droit de la souris : permet de faire tourner la caméra autour du personnage, le sens avant du personnage (transform.forward dans Unity) tourne en conséquence, tandis que le sens vers le haut du personnage reste inchangé.
Après avoir tourné à gauche avec le clic gauche de la souris, tournez à droite ensuite. La direction du personnage se réajustera immédiatement en fonction de la rotation effectuée avec le clic gauche, puis en fonction de la rotation avec le clic droit. À ce stade, cela équivaut à effectuer deux fois une rotation avec le clic droit.
Bouton de défilement de la souris: contrôle du zoom de la caméra
L'appareil photo ne peut pas passer à travers aucun objet rigide.
Lorsque l'appareil photo quitte l'objet rigide avec lequel il est entré en collision, il revient progressivement à sa distance initiale.
Si l'appareil photo rencontre un objet, utilisez la molette de la souris pour rapprocher l'appareil photo. Celui-ci doit réagir immédiatement, et la sixième condition ne se produira plus par la suite.
La caméra a touché le sol en tournant, arrêtant de tourner autour du personnage de haut en bas, pour tourner autour d'elle-même de haut en bas, tandis que la rotation de gauche à droite reste autour du personnage.



Ce besoin peut être divisé en deux parties : la rotation de la caméra et la rigidité de la caméra. Pour simplifier, commençons par résoudre le problème de la rotation de la caméra, c'est-à-dire les trois premiers points du besoin.

Emplacement de l'appareil photo.
----------------
Avant de passer à la résolution formelle de l'opération de l'appareil photo, il y a encore une question à régler : la représentation de la position de l'appareil photo. Cela peut être fait de différentes manières :

Les coordonnées mondiales de l'appareil photo
Les coordonnées de l'appareil photo par rapport au sujet.
L'orientation et la distance de l'appareil photo dans le système de coordonnées des personnes.

Dans notre cas, la caméra se déplace en fonction de la position du personnage, c'est pourquoi j'ai opté pour la troisième méthode. De plus, la caméra reste constamment centrée sur le personnage, donc il suffit de sauvegarder les informations de distance à l'intérieur de la caméra :

```c#
float curDistance = 5F;
```

Faire pivoter la caméra
-------------
Poursuivons la segmentation des mouvements de rotation de la caméra en distinguant la rotation vers la gauche et celle vers la droite. Nous allons maintenant effectuer ces deux rotations étape par étape. Tout d'abord, je ferai de la caméra un sous-élément du personnage (« children »), de sorte que certains mouvements simples du personnage suivront automatiquement la caméra.

###Faites pivoter vers la gauche ###
Simplement en tournant la molette gauche, la demande est très simple : **la caméra tourne, le personnage ne tourne pas**, il s'agit en quelque sorte d'une caméra modèle d'observation, la caméra peut observer l'objet central sous n'importe quel angle.

Dans Unity, pour obtenir l'état du clic gauche de la souris, vous pouvez utiliser la syntaxe suivante : `Input.GetMouseButton(0)` ; pour le clic droit, c'est `Input.GetMouseButton(1)`. Pour obtenir les déplacements du curseur de la souris (c'est-à-dire les décalages en X et Y entre les images), vous pouvez utiliser : `Input.GetAxis("Mouse X"); Input.GetAxis("Mouse Y")`. Ainsi, vous pouvez d'abord obtenir les informations de déplacement du curseur après avoir appuyé sur le clic gauche de la souris.

```csharp
if (Input.GetMouseButton(0))
{
    float x = Input.GetAxis("Mouse X");
    float y = Input.GetAxis("Mouse Y");
}
```
 
Le code est assez simple, voici l'aspect clé : comment contrôler la rotation de la caméra. Pour comprendre la rotation, il est nécessaire d'avoir des connaissances sur les quaternions (de nombreuses ressources en ligne disponibles, je ne les énumérerai donc pas ici). Un point important des quaternions est qu'ils permettent de construire facilement des rotations, en particulier autour d'un vecteur donné. Une fois les quaternions compris, la mise en place de la rotation de la caméra autour du personnage n'est plus compliquée.

De plus, il est important de noter que l'axe de rotation des quaternions n'est qu'un vecteur, partant de l'origine. Si l'on souhaite prendre un point `O` dans le système de coordonnées mondial comme origine, et le vecteur `V` partant de ce point comme axe de rotation, une transformation des coordonnées est nécessaire. En d'autres termes, il faut transformer le point `P` à faire pivoter, dans le système de coordonnées ayant `O` comme origine, effectuer la rotation selon `V`, puis retransformer dans le système de coordonnées mondial. Sur la base de ces opérations, il est possible d'écrire une fonctionnalité :

```c#
Vector3 MyRotate(Vector3 oldPosition, float angle, Vector3 axis, Vector3 axisPosition)
{
Crée un quaternion avec l'axe comme axe de rotation, c'est une rotation dans le référentiel du personnage.
    Quaternion rotation = Quaternion.AngleAxis(angle, axis);
Ici, il s'agit de transformer les coordonnées, en passant du système de coordonnées de la caméra aux coordonnées dans le repère du personnage.
    Vector3 offset = oldPosition - axisPosition;
Calculer la rotation et la ramener dans le système de coordonnées mondial.
    return axisPosition + (rotation * offset);
}
```
"Quaternion" is the type used in Unity to represent quaternions. By combining this with the detection of the left mouse button press we can achieve left-right rotation control of the camera.

Déplacez la souris à gauche et à droite pour contrôler la rotation de la caméra vers la gauche et vers la droite.

```c#
newForward = MyRotate(newForward, x, up, Vector3.zero);
```
Parce que seule la rotation du vecteur avant est effectuée ici, sans conversion de système de coordonnées, le quatrième paramètre est donc `Vector3.zero`.

Contrôler la rotation verticale est un peu plus difficile à comprendre que la rotation horizontale, car l'axe de rotation varie constamment à ce moment-là (en supposant que le haut du personnage est toujours dans la direction positive de l'axe Y). Gardez à l'esprit que la caméra tourne également en continu, et que son centre de vision reste toujours centré sur le personnage. Ainsi, la direction droite (right) de la caméra est l'axe autour duquel nous voulons effectuer la rotation (pensez au right de la caméra comme étant le right du personnage). Avec cette compréhension, le code pour la rotation verticale devient également très simple :

```csharp
newForward = MyRotate(newForward, -y, transform.right, Vector3.zero);
```

###Faire pivoter avec le bouton droit de la souris ###
Effectuer une rotation vers la gauche, alors faire une rotation vers la droite devient très simple, il suffit de définir la direction avant du personnage lors des rotations gauche et droite :

```csharp
player.forward = Vector3.Normalize(new Vector3(oldForward.x, 0, oldForward.z));
```

Faites pivoter vers le haut ou vers le bas comme le code de la touche gauche.

###Appuyez d'abord sur le bouton gauche, puis sur le bouton droit. ###
Bien que vous puissiez tourner à gauche ou à droite en cliquant respectivement sur le bouton gauche ou droit, une fois que vous avez tourné à gauche en premier, puis que vous utilisez le bouton droit, un problème survient : la direction avant du personnage diffère de celle de la caméra ! Ainsi, les orientations du personnage et de la caméra se séparent, rendant l'opération réelle assez étrange. Par conséquent, lorsque vous tournez à droite, vous devez d'abord aligner la direction du personnage sur celle de la caméra.

```csharp
player.forward = Vector3.Normalize(new Vector3(oldForward.x, 0, oldForward.z));

```

- - - 

###Les angles d'Euler verrouillables à trois axes###
Jusqu'ici, la rotation de l'appareil photo est presque terminée, mais il reste un point à prendre en compte : le verrouillage universel des angles d'Euler. Je ne vais pas entrer dans les détails du principe ici, mais pour les intéressés, vous pouvez faire des recherches par vous-même. Dans le cas de l'appareil photo ici, lorsque l'angle de rotation vers le haut ou le bas du côté de la personne se superpose, l'angle de vue de l'appareil photo subit un changement soudain. Cela se produit lorsque l'appareil photo atteint le sommet de la tête ou la plante des pieds de la personne, provoquant un changement brusque dans l'angle de vue vers le haut de l'appareil photo (car la valeur Y de l'angle de vue vers le haut de l'appareil photo doit toujours être supérieure à zéro). C'est pourquoi nous devons limiter la plage de rotation verticale de l'appareil photo pour éviter ce verrouillage universel. La manipulation est simple : il suffit de limiter l'angle entre la direction avant de l'appareil photo et la direction vers le haut de la personne.

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


> Ce message a été traduit en utilisant ChatGPT. Veuillez donner votre [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Signalez tout élément manquant. 
