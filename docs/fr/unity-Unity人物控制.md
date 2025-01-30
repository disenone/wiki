---
layout: post
title: Contrôle des personnages Unity
categories:
- unity
catalog: true
tags:
- dev
description: Le contrôle des actions des personnages est une partie très importante
  des jeux. Un jeu avec une bonne jouabilité peut attirer efficacement les joueurs.
  Ici, je vais essayer de créer un contrôle de personnage simple, permettant au personnage
  d'effectuer des mouvements de base, y compris la marche et le saut.
figures:
- assets/img/2014-3-15-unity-3rdperson-control0/run_jump.gif
---

<meta property="og:title" content="Unity人物控制" />

![](assets/img/2014-3-15-unity-3rdperson-control0/run_jump.gif)

Le contrôle des mouvements des personnages est une partie très importante des jeux, des jeux avec une bonne jouabilité peuvent attirer les joueurs efficacement. Ici, j'essaie de mettre en place un contrôle simple des mouvements des personnages, leur permettant d'effectuer des déplacements de base, comme marcher et sauter.

##Demande
Considérons d'abord les besoins spécifiques de notre manipulation des personnages :

Marcher, pouvoir se déplacer à la surface d'un objet rigide, contrôlé en utilisant les directions haut, bas, gauche et droite des touches, sans prendre en compte les processus d'accélération ou de décélération pour le moment.
La vitesse de déplacement peut varier selon la direction, par exemple, reculer devrait être plus lent que avancer.
3. Sauter, contrôlé par la touche jump, le personnage quitte le sol avec une certaine vitesse initiale et retombe lentement au sol.

Alors, l'idée générale est la suivante : utiliser la vitesse pour décrire le mouvement des personnages. Les composantes de la vitesse dans chaque direction peuvent être calculées séparément, et finalement, la vitesse multipliée par le temps donnera le déplacement des personnages.

##Paramètres du composant personnage
Avant d'écrire le script pour manipuler les personnages, il est nécessaire de faire quelques préparatifs en configurant préalablement les composants associés aux personnages :

Pour contrôler les personnages et leur donner une certaine rigidité physique, il est nécessaire d'ajouter un composant "Character Controller" aux personnages.
Pour une meilleure organisation structurelle, séparez d'abord les entrées concernant les personnages, lisez les entrées, traitez-les initialement, puis transmettez les résultats au contrôleur des personnages. Nommez ce script comme `MyThirdPersonInput.cs`.
Le script qui contrôle véritablement le déplacement du personnage est nommé `MyThirdPersonController.cs`.

Le résultat de la configuration est le suivant :
![](assets/img/2014-3-15-unity-3rdperson-control0/setting.png)

##Entrée
L'entrée consiste en haut, bas, gauche, droite et saut, et les directions doivent être normalisées :

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

##Décrivez le mouvement et le saut.
Nous avons besoin de quelques variables pour décrire les actions des personnages, telles que la vitesse de déplacement, la vitesse de saut, etc. Le déplacement est décrit par les variables suivantes:

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

`[System.Serializable]` is used to expose these parameters in the Inspector. The description for the jump is as follows:

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

##Vitesse de décomposition.
Pour faciliter la description des déplacements dans différentes directions, divisons la direction en trois composantes : avant-arrière, gauche-droite, haut-bas, et traitons-les séparément.

Les vitesses avant et arrière sont différentes, vous devez déterminer en fonction du signe des valeurs：

```c#
if (velocity.z > 0)
    velocity.z *= movement.forwardSpeed;
else
    velocity.z *= movement.backwardSpeed;
```

Vitesse cohérente des deux côtés :

```c#
velocity.x = inputMoveDirction.x * movement.sidewardSpeed;
```

Sauter peut poser quelques problèmes, car il est nécessaire de déterminer l'état actuel du personnage :

Si vous êtes déjà en l'air, calculez la vitesse en utilisant la gravité.
- Si c'est sur le sol :
Si vous appuyez sur la touche de saut, la vitesse sera la vitesse de saut initiale.
- - Sinon, la vitesse en direction y est 0.

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

##Mettre à jour la position des personnages.

La vitesse calculée est supposée être la vitesse à partir du début de ce cadre. Par conséquent, la vitesse pour calculer la position dans ce cadre devrait être celle calculée dans le cadre précédent. Ainsi, avant de mettre à jour la vitesse, il faut d'abord calculer la nouvelle position du personnage :

```c#
// move to new position
var collisionFlag = controller.Move(velocity * Time.deltaTime);
isOnGround = (collisionFlag & CollisionFlags.CollidedBelow) != 0;
```

La fonction `controller.Move` renvoie `CollisionFlags` pour indiquer l'état des collisions, permettant ainsi de savoir si le personnage se trouve sur le sol.

Code complet :

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


> Ce post a été traduit avec ChatGPT, veuillez laisser vos [**retours**](https://github.com/disenone/wiki_blog/issues/new)Mentionner tout oubli. 
