---
layout: post
title: Contrôle des personnages Unity
categories:
- unity
catalog: true
tags:
- dev
description: La maîtrise des mouvements des personnages est une partie essentielle
  des jeux, les jeux avec une bonne jouabilité peuvent attirer efficacement les joueurs.
  Ici, je vais essayer de créer un contrôle basique des mouvements des personnages,
  leur permettant d'effectuer des déplacements fondamentaux, tels que la marche et
  le saut.
figures:
- assets/img/2014-3-15-unity-3rdperson-control0/run_jump.gif
---

<meta property="og:title" content="Unity人物控制" />

![](assets/img/2014-3-15-unity-3rdperson-control0/run_jump.gif)

La gestion des actions des personnages est une partie importante des jeux, et des jeux avec une excellente jouabilité peuvent attirer efficacement les joueurs. Ici, je vais essayer de créer un contrôle simple des actions des personnages, leur permettant d'effectuer des déplacements de base, tels que la marche et le saut.

##Demand
Prenez un moment pour réfléchir aux besoins concrets de manipulation de notre personnage :

Marcher, capable de marcher à la surface d'un objet rigide, contrôlé par les touches haut, bas, gauche, droite, sans tenir compte pour le moment de l'accélération ou de la décélération.
La vitesse de déplacement peut varier dans différentes directions, par exemple, reculer devrait être plus lent que avancer
Effectuer un saut contrôlé par la touche de saut, où le personnage quitte le sol avec une vitesse initiale donnée et retombe progressivement sur le sol.

La ligne directrice générale est la suivante : utiliser la vitesse pour décrire le mouvement des personnages, les composantes de la vitesse dans chaque direction pouvant être calculées séparément, et enfin, multiplier la vitesse par le temps donne le déplacement de la position du personnage.

##Configuration des composants de personnage
Avant d'écrire un script pour contrôler les personnages, il est nécessaire de faire quelques préparatifs en configurant d'abord les composants associés aux personnages :

Afin de contrôler les personnages et leur conférer une certaine rigidité physique, il est nécessaire d'ajouter un composant `Character Controller` au personnage.
Pour une meilleure clarté de la structure, commence par isoler les opérations liées aux personnages, en lisant les entrées, en les traitant initialement, puis en transmettant les résultats au contrôleur des personnages. Nomme ce script de contrôle des personnages `MyThirdPersonInput.cs`.
Le script qui contrôle réellement les déplacements du personnage est nommé `MyThirdPersonController.cs`.

Le résultat après configuration est le suivant :
![](assets/img/2014-3-15-unity-3rdperson-control0/setting.png)

##Entrée
Les entrées consistent en des commandes de déplacement (haut, bas, gauche, droite) et de saut. Il est nécessaire de normaliser ces directions.

```c#
// get movement from input
var direction = new Vector3(Input.GetAxis("Horizontal"), 0, 
	Input.GetAxis("Vertical"));
if (direction != Vector3.zero)
{
    // constrain length to [0, 1]
    var directionLength = direction.magnitude;
    directionLength = Math.Min(1, directionLength);
    direction = direction.normalized * directionLength;
}
person.inputMoveDirction = direction;
person.inputJump = Input.GetButton("Jump");
````

##Décrivez le déplacement et le saut.
Nous avons besoin d'utiliser des variables pour décrire les actions d'un personnage, telles que la vitesse de déplacement, la vitesse de saut, etc. Le déplacement est décrit à l'aide des variables suivantes :

```c#    
[System.Serializable]
public class Movement
{
    public float forwardSpeed = 5F;
    public float backwardSpeed = 5F;
    public float sidewardSpeed = 5F;
}
public Movement movement = new Movement();
```

`[System.Serializable]` is used to expose these parameters in the Inspector. The description of the jump is as follows:

```c#
[System.Serializable]
public class Jumping 
{
    public bool enable = true;      // true if can jump
    public float jumpSpeed = 5F;    // original speed when jump
    public float gravity = 10F;
    public float maxFallSpeed = 20F;
    public bool jumping = false;    // true if now in the air
}
public Jumping jumping = new Jumping();
```

##Le taux de decomposition
Pour faciliter la description des déplacements dans différentes directions, divisez les directions en trois composantes : avant/arrière, gauche/droite, haut/bas, et résolvez-les séparément.

La vitesse avant et arrière est différente, selon le signe de la valeur :

```c#
if (velocity.z > 0)
    velocity.z *= movement.forwardSpeed;
else
    velocity.z *= movement.backwardSpeed;
```

Vitesse égale des deux côtés :

```c#
velocity.x = inputMoveDirction.x * movement.sidewardSpeed;
```

Sauter peut être un peu problématique, car il faut évaluer l'état actuel du personnage :

Si vous êtes déjà en l'air, calculez la vitesse en fonction de la gravité.
Si sur la terre :
Si le bouton de saut est enfoncé, la vitesse est la vitesse de saut initiale.
Sinon, la vitesse dans la direction y est de 0.

```c#
if (!isOnGround)
{
    yVelocity = Math.Max(yVelocity - jumping.gravity * Time.deltaTime, 
    	-jumping.maxFallSpeed);
}
else
{
    if (jumping.enable && inputJump)
    {
        yVelocity = jumping.jumpSpeed;
    }
    else
        yVelocity = 0F;
}
```

##Actualisation de la position des personnages

Calculer la vitesse calculée est supposée être la vitesse à partir de cette trame, donc la vitesse du calcul de position de cette trame devrait être celle calculée dans la trame précédente. Ainsi, avant de mettre à jour la vitesse, calculez d'abord la nouvelle position du personnage :

```c#
// move to new position
var collisionFlag = controller.Move(velocity * Time.deltaTime);
isOnGround = (collisionFlag & CollisionFlags.CollidedBelow) != 0;
```

La méthode `controller.Move` renvoie `CollisionFlags` pour indiquer l'état des collisions, permettant ainsi de déterminer si le personnage se trouve sur le sol.

Code complet:

MyThirdPersonInput.cs:

```c#
using UnityEngine;
using System;
using System.Collections;
[RequireComponent(typeof(MyThirdPersonController))]

public class MyThirdPersonInput : MonoBehaviour {

    private MyThirdPersonController person;

    void Awake()
    {
        person = GetComponent<MyThirdPersonController>();
    }
	
	// Update is called once per frame
	void Update () 
    {
        // get movement from input
        var direction = new Vector3(Input.GetAxis("Horizontal"), 0, 
        	Input.GetAxis("Vertical"));

        if (direction != Vector3.zero)
        {
            // constrain length to [0, 1]
            var directionLength = direction.magnitude;

            directionLength = Math.Min(1, directionLength);

            direction = direction.normalized * directionLength;

        }

        person.inputMoveDirction = direction;
        person.inputJump = Input.GetButton("Jump");
        
    }
}

```

MyThirdPersonController.cs:

```c#
using UnityEngine;
using System;
using System.Collections;

public class MyThirdPersonController : MonoBehaviour {

    // The current global direction we want the character to move in.
    [System.NonSerialized]
    public Vector3 inputMoveDirction = Vector3.zero;

    // Is the jump button held down? We use this interface instead of checking
    // for the jump button directly so this script can also be used by AIs.
    [System.NonSerialized]
    public bool inputJump = false;

    [System.Serializable]
    public class Movement
    {
        public float forwardSpeed = 5F;
        public float backwardSpeed = 5F;
        public float sidewardSpeed = 5F;
    }
    public Movement movement = new Movement();
    
    [System.Serializable]
    public class Jumping 
    {
        public bool enable = true;      // true if can jump
        public float jumpSpeed = 5F;    // original speed when jump
        public float gravity = 10F;     
        public float maxFallSpeed = 20F;
        public bool jumping = false;    // true if now in the air
    }
    public Jumping jumping = new Jumping();

    private CharacterController controller;
    private Vector3 velocity = Vector3.zero;
    private bool isOnGround = true;
	// Use this for initialization
	void Start () 
    {
        controller = GetComponent<CharacterController>();
	}
	
	// Update is called once per frame
    void FixedUpdate() 
    {
        // move to new position
        var collisionFlag = controller.Move(velocity * Time.deltaTime);
        isOnGround = (collisionFlag & CollisionFlags.CollidedBelow) != 0;

        // update velocity
        float yVelocity = velocity.y;
        velocity = Vector3.zero;

        // x-z plane velocity
        if (inputMoveDirction != Vector3.zero)
        {
            velocity.z = inputMoveDirction.z;
            if (velocity.z > 0)
                velocity.z *= movement.forwardSpeed;
            else
                velocity.z *= movement.backwardSpeed;

            velocity.x = inputMoveDirction.x * movement.sidewardSpeed;
        }

        // y velocity
        if (!isOnGround)
        {
            yVelocity = Math.Max(yVelocity - jumping.gravity * Time.deltaTime, 
            	-jumping.maxFallSpeed);
        }
        else
        {
            if (jumping.enable && inputJump)
            {
                yVelocity = jumping.jumpSpeed;
            }
            else
                yVelocity = 0F;
        }

        velocity = transform.rotation * velocity;
        velocity.y = yVelocity;
	}
}
```

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT. Veuillez partager vos [**retours**](https://github.com/disenone/wiki_blog/issues/new)Signalez toute omission. 
