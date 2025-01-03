---
layout: post
title: Unity implementiert volumetrische Lichtstreuung (Volumetric Light Scattering,
  Cloud Gaps Light)
categories:
- unity
catalog: true
tags:
- dev
description: Das volumetrische Lichtstreuung ist ein ziemlich cooles visuelles Effekt,
  bei dem man die Ausbreitung des Lichts in der Luft sieht, die Luftpartikel werden
  vom Licht beleuchtet und ein Teil des Lichts wird wieder verdeckt, was visuell Lichtstrahlen
  erzeugt, die von der Lichtquelle ausgehen.
figures:
- assets/post_assets/2014-3-30-unity-light-scattering/effect.gif
---

<meta property="og:title" content="Unity实现体积光照散射 (Volumetric Light Scattering，云隙光)" />

##Prinzip

Die Prinzipien der volumetrischen Lichtstreuung können im Buch "GPU Gems 3" [Kapitel 13](http://http.developer.nvidia.com/GPUGems3/gpugems3_ch13.html)，Bilder im Buch:

![](assets/img/2014-3-30-unity-light-scattering/goodeffect.png)

Gut aussehend, okay, unser Ziel ist es, dieses Ergebnis zu erzielen.

Das Buch erklärt die Prinzipien, eine wichtige Formel lautet:

\\[ L(s, \theta, \phi) = exposure \times \sum\_{i=0}^n decay^i \times weight \times \frac{L( s\_i, \theta\_i )}{n} \\]

Mein Verständnis ist, dass für jedes Pixel im Bild Licht eintreffen kann. Es wird eine Stichprobe entlang der Verbindungslinie von diesem Pixel zur Lichtquelle (wie es auf das Bild projiziert wird) genommen (entspricht der Formel i), die Stichproben werden gewichtet gemittelt (entspricht der Summe in der Formel) und als neuer Farbwert für das Pixel verwendet. Außerdem ist ein wichtiger Post-Pixel-Shader vorhanden. Wenn jedoch nur dieser Shader zur Verarbeitung der vom Kamera-Rendering erhaltenen Ergebnisse verwendet wird, entstehen deutliche Artefakte mit vielen Streifen:

![](assets/img/2014-3-30-unity-light-scattering/badeffect.png)

Wie wurde der in dem Buch gezeigte Effekt erzielt? Tatsächlich hat das Buch bereits die Antwort gegeben, die mit einer Reihe von Grafiken dargestellt werden kann:

![](assets/img/2014-3-30-unity-light-scattering/steps.png)

Bild a zeigt ein grobes Ergebnis. Bei genauer Betrachtung sind viele Streifen sichtbar, und es wirkt nicht wirklich authentisch verdeckend. Schritte b, c und d sind erforderlich, um ein gutes Ergebnis zu erzielen.

Bildschirmeffekte rendern und Objektverdeckung hinzufügen.

c. Führen Sie den Volumetric Light Scattering-Pixelshader auf b aus, um den verdeckten Effekt zu erhalten.

Fügen Sie die Farben der realen Szene hinzu.

Dann machen wir uns jetzt Schritt für Schritt daran.

##Malerei verdeckende Objekte

Bei der praktischen Umsetzung verwende ich zunächst `RenderWithShader`, um die Objekte, die Überlappungen verursachen, schwarz zu malen, während der Rest weiß bleibt. Da jedem Face Rendering unterzogen werden muss, kann dies bei komplexen Szenen zu einer gewissen Leistungseinbuße führen. In der Szene gibt es undurchsichtige und durchsichtige Objekte. Wir möchten, dass undurchsichtige Objekte eine vollständige Lichtblockierung erfahren, während transparente Objekte nur teilweise blockieren sollen. Dafür müssen wir unterschiedliche Shader für Objekte mit unterschiedlichen Render-Typen schreiben. Render-Typ ist das Tag des SubShader. Wenn Sie sich nicht sicher sind, können Sie hier nachschauen: [link](http://docs.unity3d.com/Documentation/Components/SL-SubshaderTags.html)Nachdem Sie es geschrieben haben, rufen Sie es auf:

```c#
camera.RenderWithShader(objectOcclusionShader, "RenderType");

```
Das zweite Argument von `RenderWithShader` verlangt die Ersetzung des Shaders basierend auf dem Render-Typ. Mit anderen Worten, der Render-Typ des Shaders, der für dasselbe Objekt verwendet wird, muss vor und nach der Ersetzung identisch sein. Auf diese Weise können wir unterschiedliche Shader für Objekte mit unterschiedlichen Render-Typen verwenden.

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

Beachte den Unterschied zwischen den Shadern für undurchsichtige und transparente Objekte: Undurchsichtige Objekte werden direkt in Schwarz gezeichnet; durchsichtige Objekte erfordern Mischung, um den Alpha-Kanal aus der Objekttextur zu erhalten und basierend auf diesem Alpha zu mischen. Der obige Code listet nur Opaque und Transparent auf, zusätzlich gibt es auch TreeOpaque (Shader wie Opaque, aber mit geänderter RenderType) und TreeTransparentCutout (wie Transparent). Da RenderType spezifiziert ist, ist es ratsam, alle möglichen Objekte, die Überlappungen verursachen könnten, so vollständig wie möglich abzudecken. Hierbei handelt es sich nur um die vier oben genannten Typen. Das Ergebnis wäre ungefähr wie folgt:

![](assets/img/2014-3-30-unity-light-scattering/objectocclusion.png)

##Kombinieren Sie die Lichtquellenstrahlung mit der Abschirmung von Objekten.

Das Zeichnen der Strahlung einer Lichtquelle ist nicht schwierig, man sollte jedoch beachten, dass je nach Bildschirmgröße Anpassungen vorgenommen werden müssen, um sicherzustellen, dass die Strahlung der Lichtquelle kreisförmig ist.

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

Dieser Shader erfordert die Eingabe der Bildschirmposition der Lichtquelle (die mit `camera.WorldToViewportPoint` berechnet werden kann und UV-Koordinaten liefert). Danach wird ein Kreis mit abnehmender Helligkeit nach außen gezeichnet, basierend auf einem festgelegten Radius. Dieses Ergebnis wird dann mit dem zuvor erhaltenen Objekt-OKlusionsbild (im `_MainTex` gespeichert) kombiniert. Das Ergebnis sieht ungefähr so aus:

![](assets/img/2014-3-30-unity-light-scattering/light.png)

##Die Behandlung von Lichtstreuung und die Kombination mit realen Farben.

Hier müssen wir den im Buch bereitgestellten Pixel Shader verwenden, meine Version:

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

Im Großen und Ganzen entspricht es dem, was im Buch steht, nur dass meine Parameter von außen an das Programm übergeben werden müssen und mit echten Farbbildern und Lichtstreuungsbildern kombiniert wurden. Das Ergebnis:

![](assets/img/2014-3-30-unity-light-scattering/effect.gif)

##Vollständiger Code

Der Code befindet sich [hier](assets/img/2014-3-30-unity-light-scattering/2014-3-30-unity-light-scattering.zip)Fügen Sie das `cs`-Skript der Kamera hinzu.

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt. Bitte gib dein [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Bitte weisen Sie eventuelle Auslassungen aus. 
