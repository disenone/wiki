---
layout: post
title: Unity crée une carte de profondeur (Depth Map) et une détection de contours
  (Edge Detection)
categories:
- unity
catalog: true
tags:
- dev
description: J'ai découvert que RenderWithShader() et OnRenderImage() dans Unity peuvent
  être utilisés pour réaliser de nombreux effets. Profitant de cette occasion d'apprentissage,
  j'ai décidé d'utiliser ces deux fonctions pour générer une carte de profondeur de
  scène et effectuer une détection de contours dans la scène, ce qui peut être utilisé
  comme un petit tableau de bord pour le jeu.
figures:
- assets/post_assets/2014-3-27-unity-depth-minimap/topview.png
---

<meta property="og:title" content="Unity画深度图(Depth Map)和边缘检测(Edge Detection)" />

Je viens de commencer à utiliser Unity depuis peu, et je suis très intéressé par le ShaderLab de Unity. Je trouve que cela permet de réaliser rapidement divers effets visuels, ce qui est très intéressant. Bon, étant encore novice, je vais commencer par travailler sur les cartes de profondeur et la détection des bords.

#Paramètres de la mini-carte

Parce que je n'ai fait qu'un petit prototype, je ne prévois pas de parler en détail de la manière de dessiner une mini-carte dans la scène. En gros, j'ai fait les choses suivantes :

1. Obtenez la boîte englobante de la scène, cela est utile lors de la configuration des paramètres et de la position de la caméra.
2. Configurez la caméra de la mini-carte en projection orthographique, en définissant le plan proche et le plan lointain de la caméra selon la bounding box.
Ajouter un sujet humain à cet appareil photo, le sujet apparaîtra au centre de la carte.
Chaque fois que la position de la caméra est mise à jour en fonction de la position de la cible et de la valeur maximale de l'axe des ordonnées de la scène

Les détails de la configuration peuvent être consultés dans le code fourni plus loin.

#Obtenir une carte de profondeur

##depthTextureMode pour obtenir une carte de profondeur

L'appareil photo peut enregistrer lui-même un DepthBuffer ou un DepthNormalBuffer (qui peut être utilisé pour la détection des contours), il suffit de le configurer.

```c#
Camera.depthTextureMode = DepthTextureMode.DepthNormals;
```

Ensuite, référez-vous à cela dans le Shader.

```c#
sampler2D _CameraDepthNormalsTexture;
```

C'est suffisant, vous pouvez vous référer au code que je donnerai plus bas pour les méthodes spécifiques. En ce qui concerne la relation entre les valeurs de profondeur enregistrées dans le Z-Buffer et les profondeurs du monde réel, vous pouvez consulter ces deux articles :
[Learning to Love your Z-buffer](http://www.sjbaker.org/steve/omniv/love_your_z_buffer.html),[Linearize depth](http://www.humus.name/temp/Linearize%20depth.txt)De plus, Unity propose également quelques fonctions pour calculer la profondeur : `Linear01Depth`, `LinearEyeDepth`, etc.

Ce n'est pas le point que je souhaite aborder ici. Ce que je veux dire, c'est que mon appareil photo devait être configuré en projection orthogonale, donc la profondeur devrait être linéaire. Cependant, les tests que j'ai réalisés indiquent le contraire. J'ai alors essayé de calculer la profondeur du monde réel en suivant la méthode présentée dans le lien ci-dessus, mais cela s'avère être incorrect. Je n'arrive pas à obtenir une profondeur linéaire précise, je ne sais pas si cela est dû au Z_Buffer de Unity ou à autre chose. Si quelqu'un a la réponse, je serais reconnaissant d'en être informé. Bien sûr, si la profondeur réelle n'est pas nécessaire et qu'il suffit de comparer les profondeurs, la méthode mentionnée précédemment est adéquate et simple. Cependant, dans mon cas, j'aimerais convertir la profondeur réelle en valeur de couleur, ce qui demande une profondeur linéaire précise (bien qu'elle soit également comprise entre 0 et 1). J'ai donc dû me résoudre à utiliser une autre méthode avec RenderWithShader.

##RenderWithShader pour obtenir la carte de profondeur.

Cette méthode est en fait un exemple tiré de Unity Reference : [Rendu avec des shaders remplacés](http://docs.unity3d.com/Documentation/Components/SL-ShaderReplacement.html)Il est important de comprendre que `RenderWithShader` dessinera le Mesh correspondant dans la scène.

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

Ajoutez un script à votre petite caméra de carte (créez-en une si vous n'en avez pas) pour configurer la caméra en projection orthographique, et utilisez ce Shader pour rendre la scène dans `Update()` :

```c#
camera.targetTexture = depthTexture;
camera.RenderWithShader(depthShader, "");
```

Le résultat du rendu sera stocké dans `depthTexture`, c'est simple, n'est-ce pas ?

##Mapper la profondeur en couleur
Pour mener à bien cette tâche, il convient tout d'abord de disposer d'une image en couleur, une image que l'on peut facilement générer avec Matlab. Par exemple, j'ai utilisé le schéma de couleurs "jet" présent dans Matlab.

![](assets/img/2014-3-27-unity-depth-minimap/jet.png){ width="200" }

Placez cette image dans le répertoire du projet `Assets\Resources`, vous pourrez la lire dans le programme :

```c#
colorMap = Resources.Load<Texture2D>("colormap");
```

Il convient de noter que le mode d'enveloppement de cette image devrait être "Clamp" afin d'éviter une interpolation entre les valeurs de couleur aux deux extrémités.

Après cela, vous devrez utiliser les fonctions `OnRenderImage` et `Graphics.Blit`, dont le prototype est le suivant :

```c#
void OnRenderImage(RenderTexture src, RenderTexture dst);
static void Blit(Texture source, RenderTexture dest, Material mat, int pass = -1);
```

La source de cette fonction est le rendu de la caméra, le résultat est le résultat traité renvoyé à la caméra. Par conséquent, cette fonction est généralement utilisée pour ajouter des effets à l'image après le rendu de la caméra, tels que la cartographie des couleurs en profondeur et la détection des bords. La méthode consiste à appeler Graphics.Blit dans `OnRenderImage`, en lui fournissant un `Material` spécifique :

```c#
depthEdgeMaterial.SetTexture("_DepthTex", src);
Graphics.Blit(src, dst, depthEdgeMaterial);
return;
```

Il est important de noter que `Graphics.Blit` fait en réalité cela : il dessine un plan de la même taille que l'écran devant la caméra, en passant `src` comme `_MainTex` de ce plan dans le `Shader`, puis en plaçant le résultat dans `dst`, au lieu de redessiner à nouveau les Mesh de la scène réelle.

La cartographie des couleurs consiste en fait à considérer la profondeur [0, 1] comme les uv de l'image. Comme je souhaite que les éléments proches de la caméra apparaissent en rouge, j'ai inversé la profondeur :

```glsl
half4 color = tex2D(_ColorMap, float2(saturate(1-depth), 0.5));
```

#Détection de contours
La détection de bord nécessite l'utilisation de la texture `_CameraDepthNormalsTexture` de la caméra elle-même, principalement pour les valeurs de normales, la profondeur quant à elle est calculée préalablement. Chaque pixel (x, y, z, w) de la texture `_CameraDepthNormalsTexture` contient les informations suivantes : (x, y) représentent les normales, (z, w) la profondeur. Les normales sont stockées selon une méthode spécifique, pour plus de détails, vous pouvez faire vos propres recherches.

Le code s'inspire de l'effet d'image intégré à Unity pour la détection des contours. Ce que nous devons faire, c'est comparer la profondeur normale du pixel actuel avec celle des pixels voisins. Si la différence est suffisamment grande, nous considérons qu'il y a un bord.

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

#Mélanger des images du monde réel
Tout simplement, une carte de couleur en profondeur peut être un peu ennuyeuse, alors nous pouvons mélanger une carte de couleur de scène réelle. Il suffit de créer un Shader supplémentaire, d'entrer l'image précédente et l'image réelle de la caméra, et de procéder au mélange dans `OnRenderImage`.

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
Le code ci-dessus est celui qui accomplit cette tâche. Il est important de comprendre que lorsque nous appelons `RenderWithShader`, `OnRenderImage` est également appelé. En d'autres termes, cette fonction est appelée deux fois, mais chaque appel doit accomplir une tâche différente. C'est pourquoi j'utilise une variable pour indiquer si l'état de rendu actuel est pour la profondeur ou le mélange.

#Le code complet
Il y a un peu trop de fichiers de code, donc je les mets ici [depth-minimap](assets/img/2014-3-27-unity-depth-minimap/2014-3-27-unity-depth-minimap.zip)Translate these text into French language:

。

--8<-- "footer_fr.md"


> Ce message a été traduit avec ChatGPT, veuillez laisser vos [**retours**](https://github.com/disenone/wiki_blog/issues/new)Veuillez indiquer toute omission. 
