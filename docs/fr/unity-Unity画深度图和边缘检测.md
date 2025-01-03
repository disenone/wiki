---
layout: post
title: Unity crée des cartes de profondeur (Depth Map) et détecte les bords (Edge
  Detection).
categories:
- unity
catalog: true
tags:
- dev
description: Découverte que les fonctions RenderWithShader() et OnRenderImage() d'Unity
  peuvent être utilisées pour créer de nombreux effets, j'ai décidé de profiter de
  cette opportunité d'apprentissage pour générer une carte de profondeur de scène
  et détecter les bords de scène en utilisant ces deux fonctions, ce qui pourrait
  servir de mini-carte pour le jeu.
figures:
- assets/post_assets/2014-3-27-unity-depth-minimap/topview.png
---

<meta property="og:title" content="Unity画深度图(Depth Map)和边缘检测(Edge Detection)" />

Je viens de commencer à utiliser Unity, et je suis très intéressé par ShaderLab. Je trouve que cela permet de mettre en place rapidement divers effets visuels, c'est très amusant. Eh bien, en tant que débutant, je vais me plonger dans la création de cartes de profondeur et de détection des bords.

#Configurer la mini-carte.

Étant donné que j'ai simplement réalisé une ébauche, je n'ai pas l'intention d'entrer dans les détails de la création de petites cartes dans la scène. En gros, voici ce que j'ai fait :

Obtenez la boîte englobante de la scène, cela est utile lors de la configuration des paramètres et de la position de la caméra.
Configurer la caméra de la mini-carte en projection orthogonale, en ajustant le plan rapproché et le plan éloigné de la caméra selon la boîte de délimitation.
Ajouter une cible humaine à l'appareil photo ; la cible s'affichera au centre de la carte.
Chaque fois que la position de la caméra est mise à jour, en fonction de la position de la cible et de la valeur y maximale de la scène.

Les paramètres spécifiques peuvent être consultés dans le code fourni ultérieurement.

#Obtenir une carte de profondeur

##Utilisez depthTextureMode pour obtenir la texture de profondeur.

L'appareil photo peut enregistrer automatiquement le DepthBuffer ou un DepthNormalBuffer (utile pour la détection des bords), il suffit de le configurer.

```c#
Camera.depthTextureMode = DepthTextureMode.DepthNormals;
```

Ensuite, faire référence dans le Shader.

```c#
sampler2D _CameraDepthNormalsTexture;
```

Vous pouvez le faire, vous pouvez vous référer au code que j'ai fourni plus tard. Pour en savoir plus sur la relation entre les valeurs de profondeur stockées dans le tampon Z et la profondeur réelle du monde, vous pouvez consulter ces deux articles :
[Learning to Love your Z-buffer](http://www.sjbaker.org/steve/omniv/love_your_z_buffer.html),[Linearize depth](http://www.humus.name/temp/Linearize%20depth.txt)De plus, Unity propose également plusieurs fonctions pour calculer la profondeur : `Linear01Depth`, `LinearEyeDepth`, etc.

Ce n'est pas le point dont je traite ici, ce que je veux dire, c'est que mon appareil photo était initialement configuré en projection orthogonale, la profondeur devrait être linéaire, mais mes tests ont montré le contraire. J'ai essayé de calculer la profondeur du monde réel en utilisant la méthode liée ci-dessus, mais les résultats étaient toujours incorrects. Je n'arrivais pas à obtenir une profondeur linéaire précise, je ne sais pas si c'est un problème de tampon Z d'Unity ou autre chose. Si quelqu'un a des connaissances à ce sujet, je serais reconnaissant de les partager. Bien sûr, si vous n'avez pas besoin d'une profondeur réelle, juste une comparaison de la profondeur, la méthode mentionnée ci-dessus est suffisante et simple. Mais pour moi, je veux mapper la véritable profondeur en valeurs de couleur, donc j'ai dû utiliser une autre méthode avec RenderWithShader.

##Utilisez RenderWithShader pour obtenir la carte de profondeur.

Ce procédé consiste en réalité à utiliser un exemple dans la référence Unity : [Rendering with Replaced Shaders](http://docs.unity3d.com/Documentation/Components/SL-ShaderReplacement.html)Il est important de noter que `RenderWithShader` va dessiner le Mesh correspondant dans la scène.

Créer un Shader :

```glsl
Shader "Custom/DepthByReplaceShader" 
{
SubShader 
{
    Tags { "RenderType"="Opaque" }
    Pass {
        Fog { Mode Off }
		CGPROGRAM
		#pragma vertex vert
		#pragma fragment frag
		#include "UnityCG.cginc"

		struct v2f {
		    float4 pos : SV_POSITION;
		    float2 depth : TEXCOORD0;
		};

		v2f vert (appdata_base v) {
		    v2f o;
		    o.pos = mul (UNITY_MATRIX_MVP, v.vertex);
		    UNITY_TRANSFER_DEPTH(o.depth);
		    return o;
		}

		float4 frag(v2f i) : COLOR {
		    //UNITY_OUTPUT_DEPTH(i.depth);
		    float d = i.depth.x/i.depth.y;
		    return float4(d, d, d, 1);
		}
		ENDCG
	}
}
}
```

Ajoutez un script à votre petite caméra (créez-en une si elle n'existe pas) pour configurer la caméra en projection orthographique, puis utilisez ce shader pour rendre la scène dans `Update()`.

```c#
camera.targetTexture = depthTexture;
camera.RenderWithShader(depthShader, "");
```

Les résultats du rendu seront stockés dans `depthTexture`, c'est simple, n'est-ce pas?

##Convertir la profondeur en couleur.
Pour réaliser cette tâche, vous aurez d'abord besoin d'une image en couleur, facilement générée avec Matlab. Par exemple, j'ai utilisé le graphique jet dans Matlab.

![](assets/img/2014-3-27-unity-depth-minimap/jet.png){ width="200" }

Placez cette image dans le répertoire du projet `Assets\Resources`, vous pourrez ainsi la lire dans le programme :

```c#
colorMap = Resources.Load<Texture2D>("colormap");
```

Il convient de noter que le mode d'enroulement de cette image devrait être "Clamp" pour éviter l'interpolation des valeurs de couleur entre les bords.

Après cela, il sera nécessaire d'utiliser les fonctions `OnRenderImage` et `Graphics.Blit`, dont le prototype est le suivant :

```c#
void OnRenderImage(RenderTexture src, RenderTexture dst);
static void Blit(Texture source, RenderTexture dest, Material mat, int pass = -1);
```

Le paramètre src de cette fonction correspond au résultat du rendu de la caméra, tandis que dst représente le résultat traité renvoyé à la caméra. Par conséquent, cette fonction est généralement utilisée pour appliquer certains effets à l'image une fois que le rendu de la caméra est terminé, tels que la cartographie des couleurs en fonction de la profondeur et la détection des bords. La méthode consiste à appeler Graphics.Blit dans OnRenderImage, en fournissant un Material spécifique en argument :

```c#
depthEdgeMaterial.SetTexture("_DepthTex", src);
Graphics.Blit(src, dst, depthEdgeMaterial);
return;
```

Il est à noter que `Graphics.Blit` fait en fait ce qui suit : il dessine un plan de la même taille que l'écran devant la caméra, passe `src` en tant que `_MainTex` de ce plan dans le `Shader`, puis place le résultat dans` dst`, au lieu de redessiner les Mesh réels de la scène.

La cartographie des couleurs consiste en réalité à considérer la profondeur [0, 1] comme les coordonnées uv de l'image, car je veux que ce qui est proche de la caméra soit rouge, c'est pourquoi j'ai inversé la profondeur :

```glsl
half4 color = tex2D(_ColorMap, float2(saturate(1-depth), 0.5));
```

#Détection des bords
La détection de bord nécessite l'utilisation de la texture `_CameraDepthNormalsTexture` de la caméra, principalement pour les valeurs des normales, tandis que la profondeur utilise les calculs précédents. Chaque pixel (x, y, z, w) de la texture `_CameraDepthNormalsTexture` contient les données des normales dans (x, y) et de la profondeur dans (z, w). Les normales sont encodées selon une méthode spécifique, pour plus d'informations, vous pouvez faire vos propres recherches.

Le code est inspiré de la détection des bords dans les effets d'image intégrés à Unity. La tâche consiste à comparer la profondeur normale actuelle du pixel avec la différence des pixels voisins. Si la différence est suffisamment grande, nous considérons qu'un bord est présent :

```c#
inline half CheckSame (half2 centerNormal, half2 sampleNormal, float centerDepth, float sampleDepth)
{
	// difference in normals
	// do not bother decoding normals - there's no need here
	half2 diff = abs(centerNormal - sampleNormal);
	half isSameNormal = (diff.x + diff.y) < 0.5;
	
	// difference in depth
	float zdiff = abs(centerDepth-sampleDepth);
	// scale the required threshold by the distance
	half isSameDepth = (zdiff < 0.09 * centerDepth) || (centerDepth < 0.1);
	
	// return:
	// 1 - if normals and depth are similar enough
	// 0 - otherwise
	return isSameNormal * isSameDepth;
}
```

Les shaders complets sont les suivants :

```glsl
Shader "Custom/DepthColorEdge" {

Properties 
{
	_DepthTex ("Depth Tex", 2D) = "white" {}
	_ColorMap ("Color Map", 2D) = "white" {}
}
	SubShader 
	{
		Tags { "RenderType"="Opaque" }
		LOD 200
		Pass
		{
			ZTest Always Cull Off ZWrite Off
			Fog { Mode off }
			CGPROGRAM
			#pragma vertex vert
			#pragma fragment frag
			#include "UnityCG.cginc"
			sampler2D _CameraDepthNormalsTexture;
			sampler2D _DepthTex;
			uniform float4 _DepthTex_TexelSize;
			sampler2D _ColorMap;
			float _ZNear;
			float _ZFar;
			
			struct v2f 
			{
			    float4 pos : SV_POSITION;
			    float2 uv[3] : TEXCOORD0;
			};

			v2f vert (appdata_base v)
			{
			    v2f o;
			    o.pos = mul (UNITY_MATRIX_MVP, v.vertex);
			    o.uv[0] = MultiplyUV( UNITY_MATRIX_TEXTURE0, v.texcoord );
			    o.uv[1] = o.uv[0] + float2(-_DepthTex_TexelSize.x, -_DepthTex_TexelSize.y);
			    o.uv[2] = o.uv[0] + float2(+_DepthTex_TexelSize.x, -_DepthTex_TexelSize.y);
			    return o;
			}


			inline half CheckSame (half2 centerNormal, half2 sampleNormal, float centerDepth, float sampleDepth)
			{
				// difference in normals
				// do not bother decoding normals - there's no need here
				half2 diff = abs(centerNormal - sampleNormal);
				half isSameNormal = (diff.x + diff.y) < 0.5;
				
				// difference in depth
				float zdiff = abs(centerDepth-sampleDepth);
				// scale the required threshold by the distance
				half isSameDepth = (zdiff < 0.09 * centerDepth) || (centerDepth < 0.1);
				
				// return:
				// 1 - if normals and depth are similar enough
				// 0 - otherwise
				return isSameNormal * isSameDepth;
			}

			half4 frag(v2f i) : COLOR 
			{
				// get color based on depth
			    float depth = tex2D (_DepthTex, i.uv[0]).r;
			    half4 color = tex2D(_ColorMap, float2(saturate(1-depth), 0.5));
			    
			    // detect normal diff
			    half2 centerNormal = tex2D(_CameraDepthNormalsTexture, i.uv[0]).xy;
			    half2 sampleNormal1 = tex2D (_CameraDepthNormalsTexture, i.uv[1]).xy;
				half2 sampleNormal2 = tex2D (_CameraDepthNormalsTexture, i.uv[2]).xy;
				float sampleDepth1 = tex2D (_DepthTex, i.uv[1]).r;
				float sampleDepth2 = tex2D (_DepthTex, i.uv[2]).r;
				color *= CheckSame(centerNormal, sampleNormal1, depth, sampleDepth1);
				color *= CheckSame(centerNormal, sampleNormal2, depth, sampleDepth2);

			    return color;
			}
			ENDCG
		}

	}
	FallBack "Diffuse"
}
```

Le résultat est similaire à ceci :

![](assets/img/2014-3-27-unity-depth-minimap/topview.png){ width="200" }

#Mélange d'images du monde réel
Seulement afficher des images en niveaux de gris peut sembler un peu monotone. Pour apporter de la vie, nous pourrions mélanger les images en couleurs et les images de la scène réelle. Il suffit de créer un shader supplémentaire, d'intégrer les images précédentes et l'image réelle de la caméra, puis de les combiner dans `OnRenderImage`.

```glsl
Shader "Custom/ColorMixDepth" {
	Properties {
		_MainTex ("Base (RGBA)", 2D) = "white" {}
		_DepthTex ("Depth (RGBA)", 2D) = "white" {}
	}
	SubShader {
		Tags { "RenderType"="Opaque" }
		LOD 200
		
		CGPROGRAM
		#pragma surface surf Lambert

		sampler2D _MainTex;
		sampler2D _DepthTex;

		struct Input {
			float2 uv_MainTex;
			float2 uv_DepthTex;
		};

		void surf (Input IN, inout SurfaceOutput o) {
			half4 c = tex2D (_MainTex, IN.uv_MainTex);
			half4 d = tex2D (_DepthTex, IN.uv_DepthTex);
			//d = d.x == 1? 0 : d;
			o.Albedo = c.rgb*0.1 + d.rgb*0.9;
			o.Alpha = 1;
		}
		ENDCG
	} 
	FallBack "Diffuse"
}
```

```c#
void OnRenderImage(RenderTexture src, RenderTexture dst)
{
    // if now rendering depth map
    if (isRenderDepth)
    {
        depthEdgeMaterial.SetTexture("_DepthTex", src);
        if(isUseColorMap)
            Graphics.Blit(src, dst, depthEdgeMaterial);
        else
            Graphics.Blit(src, dst);
        return;
    }
    // else rendering real color scene, mix the real color with depth map
    else
    {
        mixMaterial.SetTexture("_MainTex", src);
        mixMaterial.SetTexture("_DepthTex", depthTexture);
        Graphics.Blit(src, dst, mixMaterial);
        ReleaseTexture();
    }
}
```
Le code ci-dessus accomplit cette tâche. Il est important de comprendre que lors de l'appel de `RenderWithShader`, la fonction `OnRenderImage` est également appelée. En d'autres termes, cette fonction est appelée deux fois, mais les tâches à accomplir lors de ces deux appels sont différentes. Ainsi, j'utilise une variable pour indiquer si l'état de rendu actuel concerne la création d'une carte de profondeur ou de mélange.

#Code complet
Les fichiers de code sont un peu nombreux, je les ai donc placés ici [profondeur-minimap](assets/img/2014-3-27-unity-depth-minimap/2014-3-27-unity-depth-minimap.zip)I am sorry, but there is no text to translate.

--8<-- "footer_fr.md"


> Ce message a été traduit à l'aide de ChatGPT. Veuillez [**transmettre vos commentaires**](https://github.com/disenone/wiki_blog/issues/new)Indiquez tout oubli. 
