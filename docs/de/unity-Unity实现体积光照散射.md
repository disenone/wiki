---
layout: post
title: Unity implementiert volumetrische Lichtstreuung (Volumetric Light Scattering,
  Cloud Gaps Light)
categories:
- unity
catalog: true
tags:
- dev
description: Volumen-Lichtstreuung ist ein ziemlich beeindruckender visueller Effekt.
  Man hat das Gefühl, dass das Licht durch die Luft strömt, wobei die Partikel in
  der Luft vom Licht erleuchtet werden, während ein Teil des Lichts blockiert wird.
  Visuell erzeugt dies die Illusion von Lichtstrahlen, die vom Lichtquelle ausgehen.
figures:
- assets/post_assets/2014-3-30-unity-light-scattering/effect.gif
---

<meta property="og:title" content="Unity实现体积光照散射 (Volumetric Light Scattering，云隙光)" />

##Prinzip

(http://http.developer.nvidia.com/GPUGems3/gpugems3_ch13.html), wirksame Abbildungen im Buch:

![](assets/img/2014-3-30-unity-light-scattering/goodeffect.png)

Sieht gut aus, dann ist es unser Ziel, diesen Effekt zu erzielen.

Im Buch wird das Prinzip vorgestellt, eine Schlüsselgleichung lautet:

\\[ L(s, \theta, \phi) = exposure \times \sum\_{i=0}^n decay^i \times weight \times \frac{L( s\_i, \theta\_i )}{n} \\]

Mein Verständnis ist, dass für jedes Pixel auf dem Bild Licht darauf scheinen kann. Daher wird die Verbindungslinie von diesem Pixel zur Lichtquelle (an der Position, die auf das Bild projiziert wird) abgetastet (entsprechend der Formel \\(i\\)). Die resultierenden Abtastwerte werden gewichtet und gemittelt (entsprechend der Formel \\(\sum\\)), um einen neuen Farbwert für dieses Pixel zu erhalten. Darüber hinaus gibt es einen entscheidenden Nachbearbeitungspixel-Shader, aber wenn man nur diesen Shader verwendet, um die Ergebnisse der Kamera zu verarbeiten, entstehen deutliche künstliche Spuren und viele Streifen:

![](assets/img/2014-3-30-unity-light-scattering/badeffect.png)

Wie werden die Effekte im Buch erreicht? Tatsächlich gibt das Buch bereits die Antwort und kann durch eine Reihe von Bildern veranschaulicht werden:

![](assets/img/2014-3-30-unity-light-scattering/steps.png)

Die Abbildung a zeigt den rauen Effekt, bei dem man genau hinschaut, viele Streifen zu sehen sind, und es wirkt nicht ausreichend realistisch. b, c und d sind die Schritte, die notwendig sind, um einen guten Effekt zu erzielen:

b. Render the light radiance effect onto the image and add object occlusion.

Führen Sie das Volumetric Light Scattering Pixel-Shader auf b aus, um den verdeckten Effekt zu erhalten.

Fügen Sie die Farben der realen Szene hinzu.

Dann lassen Sie uns Schritt für Schritt vorgehen.

##Zeichne verdeckte Objekte.

In practice, I first use `RenderWithShader` to paint obstructed objects in black and the rest in white, as this requires rendering every face, it may bring some performance impact for complex scenes. Objects in the scene can be opaque or transparent. We aim for opaque objects to create full light occlusion and transparent objects to generate partial occlusion. Therefore, we need to write different shaders for objects with different RenderTypes. RenderType is a tag of SubShader, for more information, you can refer to [here](http://docs.unity3d.com/Documentation/Components/SL-SubshaderTags.html)Nachdem Sie den Text geschrieben haben, rufen Sie Folgendes auf:

```c#
camera.RenderWithShader(objectOcclusionShader, "RenderType");

```
Der zweite Parameter von `RenderWithShader` verlangt, dass der Shader basierend auf dem RenderType ersetzt wird. Einfach gesagt, der RenderType des ersetzten Shaders muss mit dem des ursprünglichen Shaders des gleichen Objekts übereinstimmen. So können wir für Objekte mit unterschiedlichen RenderTypes verschiedene Shader verwenden:

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

Achte auf den Unterschied zwischen Shadern für undurchsichtige und transparente Objekte: Undurchsichtige Objekte werden einfach schwarz gemalt; undurchsichtige Objekte erfordern das Ausführen von Blending, um den Alphakanal des Objekttextures zu erhalten und basierend auf diesem Alpha das Blending durchzuführen. Der obige Code erwähnt nur Opaque und Transparent, es gibt auch TreeOpaque (Shader wie Opaque, nur mit geänderter RenderType), TreeTransparentCutout (wie Transparent). Da der RenderType festgelegt ist, muss man versuchen, alle möglichen Objekte zu berücksichtigen, die in der Szene Überlappungen verursachen könnten, ich habe nur die oben genannten vier erwähnt. Das Ergebnis ist ungefähr wie folgt:

![](assets/img/2014-3-30-unity-light-scattering/objectocclusion.png)

##Kombination von Objekt遮挡 und Lichtquelle Strahlung.

Die Strahlung der Lichtquelle zu zeichnen ist nicht schwer, allerdings ist zu beachten, dass einige Anpassungen je nach Größe des Bildschirms vorgenommen werden müssen, damit die Strahlung der Lichtquelle rund ist.

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

Dieser Shader erfordert die Eingabe der Position der Lichtquelle auf dem Bildschirm (kann mit `camera.WorldToViewportPoint` berechnet werden, um die UV-Koordinaten zu erhalten), dann zeichnet er einen Kreis mit abnehmender Helligkeit entsprechend einem bestimmten Radius nach außen. Anschließend wird das Ergebnis mit dem zuvor erhaltenen Objekt-Verdeckungsbild (das in `_MainTex` gespeichert ist) kombiniert. Das Ergebnis sieht ungefähr so aus:

![](assets/img/2014-3-30-unity-light-scattering/light.png)

##Light Scattering-Verarbeitung und Kombination mit echten Farben.

Hier kommt der im Buch bereitgestellte Pixel Shader zum Einsatz, meine Version:

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

Im Großen und Ganzen stimmt es mit dem im Buch Überein, nur müssen meine Parameter im Programm übergeben werden, und es wurden reale Farbkartierungen und Lichtstreuungsdiagramme kombiniert. Das Ergebnis:

![](assets/img/2014-3-30-unity-light-scattering/effect.gif)

##Vollständiger Code

Der Code befindet sich [hier](assets/img/2014-3-30-unity-light-scattering/2014-3-30-unity-light-scattering.zip)Fügen Sie das `cs`-Skript der Kamera hinzu.

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt, bitte im [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)darauf hin, dass es irgendwelche Auslassungen gibt. 
