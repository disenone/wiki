---
layout: post
title: Unity réalise la dispersion de la lumière volumétrique (Volumetric Light Scattering,
  crepuscular rays)
categories:
- unity
catalog: true
tags:
- dev
description: La diffusion volumétrique de la lumière est un effet visuel assez sympa,
  on dirait presque que l'on voit la propagation de la lumière dans l'air, les particules
  en suspension dans l'air sont éclairées par la lumière, tandis qu'une partie des
  rayons lumineux est masquée, créant visuellement des rayons émis par la source lumineuse.
figures:
- assets/post_assets/2014-3-30-unity-light-scattering/effect.gif
---

<meta property="og:title" content="Unity实现体积光照散射 (Volumetric Light Scattering，云隙光)" />

##Principe

(http://http.developer.nvidia.com/GPUGems3/gpugems3_ch13.html)，Dans le livre, il y a des illustrations utiles :

![](assets/img/2014-3-30-unity-light-scattering/goodeffect.png)

C'est agréable à voir, d'accord, notre objectif est d'atteindre ce résultat.

Le livre présente les principes, une formule clé est :

\\[ L(s, \theta, \phi) = exposure \times \sum\_{i=0}^n decay^i \times weight \times \frac{L( s\_i, \theta\_i )}{n} \\]

Mon interprétation est que, pour chaque pixel de l'image, la lumière peut être projetée, donc un échantillonnage est effectué le long de la ligne reliant ce pixel à la source lumineuse (correspondant à la variable \\(i\\)), les résultats de l'échantillonnage sont pondérés et moyennés (correspondant à la somme dans l'équation) pour obtenir la nouvelle valeur de couleur du pixel. De plus, il est essentiel d'avoir un shader de post-traitement, cependant si seul ce shader est utilisé pour traiter le rendu de la caméra, cela laissera des artefacts visibles, avec de nombreuses bandes apparaissant.

![](assets/img/2014-3-30-unity-light-scattering/badeffect.png)

Alors, comment est produite l'effet décrit dans le livre ? En réalité, le livre fournit déjà une réponse, qui peut être expliquée à l'aide d'un ensemble d'images :

![](assets/img/2014-3-30-unity-light-scattering/steps.png)

La graphique a est un effet grossier, si on regarde de près, on peut voir de nombreuses rayures et il n'est pas assez réaliste. Les étapes b, c et d sont nécessaires pour obtenir un bon résultat :

Rendu des effets d'éclairage diffus sur l'image et ajout des masques d'objet.

Appliquer le shader de diffusion lumineuse volumétrique à b pour obtenir l'effet de l'occultation.

Ajoutez les couleurs de la scène réelle.

Alors maintenant, passons à la mise en œuvre étape par étape.

##Peindre des objets obstruants

Dans la pratique, j'utilise d'abord `RenderWithShader` pour peindre en noir les objets qui seront occultés et en blanc les autres. Cela nécessite de rendre chaque face individuellement, ce qui peut entraîner une certaine perte de performances pour des scènes complexes. Les objets de la scène peuvent être opaques ou transparents. Nous voulons que les objets opaques bloquent entièrement la lumière, tandis que les objets transparents ne bloquent qu'en partie. Par conséquent, nous devons écrire des shaders différents pour les objets de différents RenderType. Le RenderType est une balise du SubShader, si vous n'êtes pas sûr, vous pouvez consulter [ici](http://docs.unity3d.com/Documentation/Components/SL-SubshaderTags.html)Une fois que c'est bien écrit, appelez :

```c#
camera.RenderWithShader(objectOcclusionShader, "RenderType");

```
Le deuxième paramètre de `RenderWithShader` demande simplement de remplacer le shader en fonction du type de rendu. En d'autres termes, le type de rendu du shader de remplacement doit correspondre à celui du shader d'origine sur le même objet, ce qui nous permet d'utiliser des shaders différents pour des objets de types de rendu différents.

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

Notez la différence entre Shader pour les objets opaques et transparents : les objets opaques sont directement dessinés en noir ; ceux transparents nécessitent un blending, en utilisant le canal alpha de la texture de l'objet pour effectuer ce blending. Le code ci-dessus ne fait que mentionner Opaque et Transparent, mais il y a également TreeOpaque (Shader identique à Opaque, mais en changeant RenderType), TreeTransparentCutout (similaire à Transparent), etc. Étant donné que RenderType est spécifié, afin d'être exhaustif, il est nécessaire d'explorer autant que possible les objets susceptibles d'être occultés dans la scène. Dans mon cas, seules les quatre catégories mentionnées précédemment sont disponibles. Le résultat est globalement le suivant :

![](assets/img/2014-3-30-unity-light-scattering/objectocclusion.png)

##Combiner l'occlusion des objets avec le rayonnement lumineux.

Il n'est pas compliqué de dessiner le rayonnement de la source de lumière, mais il faut veiller à effectuer quelques ajustements en fonction de la taille de l'écran pour que le rayonnement de la source lumineuse soit circulaire :

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

Ce Shader nécessite en entrée la position de la source lumineuse à l'écran (peut être calculée en utilisant `camera.WorldToViewportPoint`, obtenant ainsi les coordonnées UV), puis dessine un cercle de luminosité décroissante vers l'extérieur selon un rayon spécifié. Il combine ensuite ce résultat avec l'image de l'objet précédemment obtenue (stockée dans `_MainTex`), le résultat est approximativement :

![](assets/img/2014-3-30-unity-light-scattering/light.png)

##Traitement de la diffusion de la lumière, associé à des couleurs réelles

Ici, vous devrez utiliser le Pixel Shader fourni dans le livre, voici ma version :

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

En gros, ça correspond à ce qui est dans le livre, sauf que mes paramètres doivent être transmis dans le programme, et j'ai intégré de vraies images de couleurs et des graphiques de diffusion de la lumière. Le résultat :

![](assets/img/2014-3-30-unity-light-scattering/effect.gif)

##Le texte doit être traduit en français.

Le code est [ici](assets/img/2014-3-30-unity-light-scattering/2014-3-30-unity-light-scattering.zip)Ajoutez le script `cs` à la caméra.

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT, veuillez signaler toute [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Indiquez tout ce qui aurait pu être omis. 
