---
layout: post
title: Unity implements volumetric light scattering (Volumetric Light Scattering,
  Cloud Gaps Light)
categories:
- unity
catalog: true
tags:
- dev
description: Le scattering de la lumière volumique est un effet visuel plutôt agréable,
  comme si vous pouviez voir la lumière se propager dans l'air, les particules dans
  l'air illuminées par la lumière, tandis qu'une partie de la lumière est obscurcie,
  créant visuellement des rayons qui semblent émaner de la source lumineuse.
figures:
- assets/post_assets/2014-3-30-unity-light-scattering/effect.gif
---

<meta property="og:title" content="Unity实现体积光照散射 (Volumetric Light Scattering，云隙光)" />

##Principe

(http://http.developer.nvidia.com/GPUGems3/gpugems3_ch13.html)，livre avec des images de résultats :

![](assets/img/2014-3-30-unity-light-scattering/goodeffect.png)

C'est joli, n'est-ce pas ? Très bien, notre objectif est d'atteindre cet effet.

Le livre présente les principes, une formule clé est :

\\[ L(s, \theta, \phi) = exposure \times \sum\_{i=0}^n decay^i \times weight \times \frac{L( s\_i, \theta\_i )}{n} \\]

Ma compréhension est que pour chaque pixel sur l'image, la lumière peut potentiellement l'éclairer. Ainsi, il s'agit de prélever un échantillon sur la ligne reliant ce pixel à la source lumineuse (à la position projetée sur l'image) (correspondant à la formule \\(i\\)), d'effectuer une moyenne pondérée des résultats de l'échantillon (correspondant à la formule \\(\sum\\)) et de l'utiliser comme nouvelle valeur de couleur pour ce pixel. De plus, il y a un shader de pixel post-traitement clé, mais si l'on utilise uniquement ce shader pour traiter les résultats du rendu de la caméra, cela produira des traces artificielles évidentes, avec de nombreuses bandes.

![](assets/img/2014-3-30-unity-light-scattering/badeffect.png)

Comment le résultat du livre est-il obtenu ? En réalité, le livre donne déjà la réponse, il peut être expliqué à l'aide d'un ensemble de graphiques :

![](assets/img/2014-3-30-unity-light-scattering/steps.png)

Le texte à traduire en français est le suivant :

图a 就是粗糙的效果，细心地可以看到有许多条纹，并且没有遮挡不够真实，b、c、 d就是为了获得好的效果需要进行的步骤：

b. Appliquer l'effet de rayonnement de la lumière à l'image et ajouter l'occultation des objets.

Appliquer le shader de diffusion de la lumière volumétrique à b pour obtenir l'effet après occultation.

Ajouter les couleurs de scène réelles.

Alors, procédons étape par étape pour réaliser cela.

##Dessiner des objets de遮挡.

Dans la pratique, j'utilise d'abord `RenderWithShader` pour peindre les objets susceptibles d'être occultés en noir, tandis que les autres zones restent blanches. Cela nécessite de rendre chaque face, ce qui peut entraîner une certaine consommation de performances dans des scènes complexes. Dans la scène, il y a des objets opaques et transparents. Nous souhaitons que les objets opaques créent une occlusion complète, tandis que les objets transparents devraient engendrer une occlusion partielle. Par conséquent, nous devons rédiger des shaders différents selon les types de rendu (RenderType) des objets. Le RenderType est une balise (Tag) de SubShader, et si ce n'est pas clair, vous pouvez vérifier [ici](http://docs.unity3d.com/Documentation/Components/SL-SubshaderTags.html)Après l'avoir écrit, appelez :

```c#
camera.RenderWithShader(objectOcclusionShader, "RenderType");

```
Le deuxième paramètre de `RenderWithShader` exige de remplacer le Shader en fonction du RenderType. En d'autres termes, le RenderType du Shader à remplacer doit être identique à celui d'avant le remplacement pour le même objet. Ainsi, nous pouvons utiliser des Shaders différents pour des objets de RenderType différents.

```glsl
Shader "Custom/ObjectOcclusion" 
{
	Properties 
	{
		_MainTex ("Base (RGB)", 2D) = "white" {}
	}
	SubShader 
	{
		Tags 
		{
			"Queue" = "Geometry"
			"RenderType" = "Opaque"
		}
		LOD 200
		Pass
		{
			Lighting Off
			ZTest Always Cull Off ZWrite Off
			Fog { Mode off }
			CGPROGRAM
			#pragma vertex vert
			#pragma fragment frag
			#include "UnityCG.cginc"
			
			uniform sampler2D _MainTex;
			
			v2f_img vert(appdata_img i)
			{
				v2f_img o;
				o.pos = mul (UNITY_MATRIX_MVP, i.vertex);
				return o;
			}
			
			half4 frag(v2f_img i): COLOR
			{
				return half4(0, 0, 0, 1);
			}
			ENDCG
		}

	}
		SubShader 
	{
		Tags 
		{
			"Queue" = "Geometry"
			"RenderType" = "Transparent"
		}
		LOD 200
		Pass
		{
			Lighting Off
			ZTest Always Cull Off ZWrite Off
			Fog { Mode off }
			Blend SrcAlpha OneMinusSrcAlpha		// blend for transparent objects
			CGPROGRAM
			#pragma vertex vert
			#pragma fragment frag
			#include "UnityCG.cginc"
			
			uniform sampler2D _MainTex;
			
			v2f_img vert(appdata_img i)
			{
				v2f_img o;
				o.pos = mul (UNITY_MATRIX_MVP, i.vertex);
				o.uv = MultiplyUV( UNITY_MATRIX_TEXTURE0, i.texcoord );
				return o;
			}
			
			half4 frag(v2f_img i): COLOR
			{
				half3 output = (1, 1, 1);
				half4 color = tex2D(_MainTex, i.uv);
				half alpha = color.a;
				return half4(output *(1-alpha), alpha);
			}
			ENDCG
		}

	}
		
	FallBack "Diffuse"
}

```

Notez la différence entre les shaders des objets opaques et transparents : les objets opaques sont directement dessinés en noir ; les objets transparents nécessitent un mélange (blending) pour obtenir le canal alpha de la texture de l'objet et effectuer un mélange en fonction de cet alpha. Le code ci-dessus ne mentionne que les shaders Opaque et Transparent, mais il y a aussi TreeOpaque (même shader qu'Opaque, mais change de RenderType) et TreeTransparentCutout (similaire à Transparent). En spécifiant les RenderTypes, pour une couverture complète, il est nécessaire d'explorer le plus exhaustivement possible les objets susceptibles de se superposer dans la scène. Voici seulement les quatre types mentionnés précédemment. Les résultats approximatifs sont les suivants :

![](assets/img/2014-3-30-unity-light-scattering/objectocclusion.png)

##Combiner l'occlusion des objets et le rayonnement des sources lumineuses.

Il n'est pas difficile de dessiner la radiation d'une source lumineuse. Il est important de prendre en compte la taille de l'écran pour effectuer quelques ajustements, afin que la forme de la radiation de la source lumineuse soit circulaire.

```c#
Shader "Custom/LightRadiate" 
{
	Properties 
	{
		_MainTex ("Base (RGB)", RECT) = "white" {}
		_LightPos ("Light Pos In Screen Space(XY)", Vector) = (0, 0, 0, 1)
		_LightRadius ("Light radiation radius (Pixel)", Float) = 50
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
			
			uniform sampler2D _MainTex;
			float4 _LightPos;
			float _LightRadius;
			
			v2f_img vert(appdata_img i)
			{
				v2f_img o;
				o.pos = mul (UNITY_MATRIX_MVP, i.vertex);
				o.uv = MultiplyUV( UNITY_MATRIX_TEXTURE0, i.texcoord );
				return o;
			}
			
			half4 frag(v2f_img i): COLOR
			{
				half2 deltaTexCoord = (i.uv - _LightPos.xy) * half2(_ScreenParams.x, _ScreenParams.y);
				float dis = dot(deltaTexCoord, deltaTexCoord);
				const float maxDis = _LightRadius * _LightRadius;
				dis = saturate((maxDis-dis) / maxDis * 0.5);
				return half4(dis, dis, dis, 1) * half4(tex2D(_MainTex, i.uv).rgb, 1);				
			}
			
			ENDCG
		}
	} 
	FallBack "Diffuse"
}
```

Ce Shader nécessite l'entrée de la position de la source de lumière sur l'écran (peut être calculée avec `camera.WorldToViewportPoint`, qui donne les coordonnées UV), puis dessine un cercle avec une luminosité décroissante à l'extérieur en fonction du rayon spécifié. Ensuite, il combine le résultat avec l'image de l'objet obtenu précédemment (stocké dans `_MainTex`), donnant un rendu approximatif de :

![](assets/img/2014-3-30-unity-light-scattering/light.png)

##Traitement de la diffusion de la lumière, en combinaison avec des couleurs réelles.

Ici, nous allons utiliser le Pixel Shader fourni dans le livre. Voici ma version :

```glsl
Shader "Custom/LightScattering" 
{
	Properties 
	{
		_MainTex ("Base (RGB)", 2D) = "white" {}
		_LightRadTex("Light Radiate Tex (RGB)", 2D) = "white" {}
		_LightPos ("Light Pos In Screen Space(XY)", Vector) = (0, 0, 0, 1)
		_Params("Density Weight Decay Exposure", Vector) = (1.0, 1.0, 1.0, 1.0)
	}
	SubShader 
	{
		LOD 200
		Pass
		{
			ZTest Always Cull Off ZWrite Off
			Fog { Mode off }	
			CGPROGRAM
			#pragma vertex vert
			#pragma fragment frag
			#pragma target 3.0
			#include "UnityCG.cginc"
			
			uniform sampler2D _MainTex;
			uniform sampler2D _LightRadTex;
			uniform float4 _LightPos;
			uniform float4 _Params;
			
			v2f_img vert(appdata_img i)
			{
				v2f_img o;
				o.pos = mul (UNITY_MATRIX_MVP, i.vertex);
				o.uv = MultiplyUV( UNITY_MATRIX_TEXTURE0, i.texcoord );
				return o;
			}
			
			half4 frag(v2f_img i): COLOR
			{	
				// Calculate vector from pixel to light source in screen space
				float2 deltaTexCoord = (i.uv - _LightPos.xy);
				
				// Divide by number of samples and scale by control factor, here I use 32 samples
				deltaTexCoord *= 1.0f / 32 * _Params.x;	//density;
				
				// Store color.
				half3 color = tex2D(_MainTex, i.uv).rgb;
				
				// Store initial sample.
				half3 light = tex2D(_LightRadTex, i.uv).rgb;
	
				// Set up illumination decay factor.
				half illuminationDecay = 1.0f;

				for(int j = 0; j < 31; ++j)
				{
					// Step sample location along ray.
					i.uv -= deltaTexCoord;
					
					// Retrieve sample at new location.
					half3 sample = tex2D(_LightRadTex, i.uv).rgb;
					
					// Apply sample attenuation scale/decay factors.
					sample *= illuminationDecay * 0.03125 * _Params.y ;	//weight;
					
					// Accumulate combined light.
					light += sample;
					
					// Update exponential decay factor.
					illuminationDecay *= _Params.z;				//decay;
				}
				
				// Output final color with a further scale control factor.
				return half4(color+(light * _Params.w), 1);	// exposure
			}
			
			ENDCG		
		}

	} 
	FallBack "Diffuse"
}
```

En gros, cela correspond à ce qui est dans le livre, sauf que mes paramètres doivent être passés dans le programme, et en combinant la véritable carte des couleurs et le graphique de diffusion de lumière, le résultat :

![](assets/img/2014-3-30-unity-light-scattering/effect.gif)

##Code complet

Le code se trouve [ici](assets/img/2014-3-30-unity-light-scattering/2014-3-30-unity-light-scattering.zip)Veuillez ajouter le script "cs" à la caméra.

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT, veuillez laisser vos [**commentaires**](https://github.com/disenone/wiki_blog/issues/new)Indiquez tout ce qui manque. 
