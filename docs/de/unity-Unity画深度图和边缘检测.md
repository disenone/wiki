---
layout: post
title: Unity erstellt Tiefenkarte (Depth Map) und Kantenerkennung (Edge Detection)
categories:
- unity
catalog: true
tags:
- dev
description: Ich habe entdeckt, dass die Funktionen RenderWithShader() und OnRenderImage()
  in Unity verwendet werden können, um viele Effekte zu erzielen. Während ich lerne,
  habe ich beschlossen, diese beiden Funktionen zu nutzen, um die Generierung von
  Tiefenbildern und die Kantenerkennung in der Szene zu implementieren, die als eine
  Art Mini-Karte für das Spiel dienen kann.
figures:
- assets/post_assets/2014-3-27-unity-depth-minimap/topview.png
---

<meta property="og:title" content="Unity画深度图(Depth Map)和边缘检测(Edge Detection)" />

Ich habe erst vor kurzem mit Unity angefangen und bin sehr an Unitys ShaderLab interessiert. Ich finde, es ermöglicht die schnelle Umsetzung verschiedenster Anzeigeeffekte, was sehr spannend ist. Nun, als jemand, der gerade erst anfängt, werde ich mich mal mit Tiefenkarten und Kantenerkennung beschäftigen.

#Kleines Karten-Setup

Weil ich nur einen kleinen Prototyp erstellt habe, beabsichtige ich nicht, im Detail zu erklären, wie man in der Szene eine kleine Karte zeichnet. Im Großen und Ganzen habe ich Folgendes gemacht:

1. Erhalten Sie die Begrenzungsbox der Szene, die bei der Einstellung der Kameraparameter und -position nützlich ist.
Konfigurieren Sie die Mini-Kartenkamera für eine orthogonale Projektion und legen Sie die Nah- und Fernplanen der Kamera entsprechend der Bounding Box fest.
3. Fügen Sie der Kamera ein Personen-Ziel hinzu, das in der Mitte der Karte angezeigt wird.
Bei jeder Aktualisierung der Kamera-Position basierend auf der Position des Ziels und dem maximalen Y-Wert der Szene.

Die spezifische Konfiguration kann im später gegebenen Code nachgeschlagen werden.

#Tiefe Karte abrufen

##depthTextureMode, um die Tiefenkarte zu erhalten

Die Kamera kann selbst einen DepthBuffer oder einen DepthNormalBuffer speichern (zur Kantenerkennung), es muss lediglich eingestellt werden.

```c#
Camera.depthTextureMode = DepthTextureMode.DepthNormals;
```

Then refer to it in the shader.

```c#
sampler2D _CameraDepthNormalsTexture;
```

Das wäre ausreichend, die genaue Vorgehensweise kann anhand des Codes, den ich später bereitstelle, nachvollzogen werden. Informationen zur Beziehung zwischen den im Z-Buffer gespeicherten Tiefenwerten und den Tiefen im realen Leben können in diesen beiden Artikeln gefunden werden:
[Learning to Love your Z-buffer](http://www.sjbaker.org/steve/omniv/love_your_z_buffer.html),[Linearize depth](http://www.humus.name/temp/Linearize%20depth.txt)Unity bietet auch einige Funktionen zur Berechnung von Tiefen wie `Linear01Depth`, `LinearEyeDepth` usw. an.

Das ist nicht der Hauptpunkt meiner Diskussion hier. Was ich sagen möchte ist, dass meine Kamera eigentlich auf orthografische Projektion eingestellt war und die Tiefe linear sein sollte, aber es stellte sich heraus, dass sie es nicht war. Ich habe dann versucht, mithilfe der Methode aus dem oben genannten Link die echte Welttiefe zu berechnen, aber es war immer falsch. Ich konnte einfach nicht die echte lineare Tiefe berechnen. Ich weiß nicht, ob es am Z-Puffer von Unity liegt oder an etwas anderem. Wenn jemand das weiß, bitte hilf mir. Natürlich, wenn du nur die relative Tiefe vergleichen möchtest oder Ähnliches, reicht die oben genannte Methode aus und ist sehr einfach. Aber für mich hier, möchte ich die echte Tiefe in Farbwerte umwandeln. Dafür benötige ich echte lineare Tiefenwerte (obwohl sie auch zwischen 0 und 1 liegen). Deshalb musste ich auf eine andere Methode mit RenderWithShader umsteigen.

##RenderWithShader, um die Tiefenkarte zu erhalten.

Diese Methode basiert tatsächlich auf einem Beispiel aus der Unity-Referenz: [Rendering with Replaced Shaders](http://docs.unity3d.com/Documentation/Components/SL-ShaderReplacement.html)Es ist wichtig zu verstehen, dass `RenderWithShader` die entsprechenden Meshes in der Szene einmal zeichnet.

Einen Shader erstellen:

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

Füge deiner Mini-Kartenkamera (erstelle eine, falls du keine hast) ein Skript hinzu, um die Kamera auf orthographische Projektion umzustellen, und verwende diesen Shader im `Update()`, um die Szene zu rendern:

```c#
camera.targetTexture = depthTexture;
camera.RenderWithShader(depthShader, "");
```

Das Ergebnis der Renderung wird in `depthTexture` gespeichert, ganz einfach, oder?

##Übersetzen Sie diesen Text ins Deutsche:

"Mapping der Tiefe in Farbe umwandeln"
Um diese Arbeit zu erledigen, benötigen Sie zunächst ein Farbbild, das ganz einfach mit Matlab erstellt werden kann. Zum Beispiel könnten Sie das Jet-Bild in Matlab verwenden.

![](assets/img/2014-3-27-unity-depth-minimap/jet.png){ width="200" }

Legen Sie dieses Bild in das Verzeichnis "Assets\Resources" des Projekts, dann kann es im Programm gelesen werden:

```c#
colorMap = Resources.Load<Texture2D>("colormap");
```

Es ist zu beachten, dass der `Wrap Mode` dieses Bildes auf `Clamp` eingestellt sein sollte, um eine Interpolation zwischen den Farbwerten an den beiden Rändern zu verhindern.

Danach müssen die Funktionen `OnRenderImage` und `Graphics.Blit` verwendet werden, deren Prototyp wie folgt aussieht:

```c#
void OnRenderImage(RenderTexture src, RenderTexture dst);
static void Blit(Texture source, RenderTexture dest, Material mat, int pass = -1);
```

Diese Funktion hat als src das Ergebnis des Kamera-Renderings, dst ist das Ergebnis, das nach der Verarbeitung an die Kamera zurückgegeben wird. Daher wird diese Funktion normalerweise verwendet, um nach Abschluss des Kamera-Renderings einige Effekte auf das Bild anzuwenden, wie zum Beispiel die Farbmapping von Tiefen und die Kantenerkennung. Die Vorgehensweise besteht darin, in `OnRenderImage` `Graphics.Blit` aufzurufen und ein bestimmtes `Material` zu übergeben:

```c#
depthEdgeMaterial.SetTexture("_DepthTex", src);
Graphics.Blit(src, dst, depthEdgeMaterial);
return;
```

Es ist zu beachten, dass `Graphics.Blit` tatsächlich Folgendes macht: Es zeichnet eine Ebene vor der Kamera, die die gleiche Größe wie der Bildschirm hat, überträgt `src` als `_MainTex` in den `Shader` dieser Ebene und platziert das Ergebnis in `dst`, anstatt das Mesh der tatsächlichen Szene erneut zu zeichnen.

Die Farbzuordnung betrachtet die Tiefe [0, 1] als die UV-Koordinaten des Bildes, da ich möchte, dass Bereiche, die nahe an der Kamera sind, rot dargestellt werden, habe ich die Tiefe umgedreht.

```glsl
half4 color = tex2D(_ColorMap, float2(saturate(1-depth), 0.5));
```

#Kantenfindung
Die Kantenerkennung verwendet die `_CameraDepthNormalsTexture` der Kamera selbst, hauptsächlich für die Normalenwerte, während die Tiefe mit zuvor berechneten Werten verwendet wird. In jedem Pixel (x, y, z, w) von `_CameraDepthNormalsTexture` stellen (x, y) die Normalen dar, während (z, w) die Tiefe repräsentieren. Die Normalen werden auf eine spezielle Art und Weise gespeichert, die bei Interesse eigenständig recherchiert werden kann.

Der Code basiert auf der Kantenerkennung der integrierten Bild-Effekte von Unity. Die Aufgabe besteht darin, die Unterschiede zwischen der Normalen Tiefe des aktuellen Pixels und den benachbarten Pixeln zu vergleichen. Wenn der Unterschied groß genug ist, betrachten wir dies als eine Kante.

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

Die vollständigen Shader sind wie folgt:

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

Das Ergebnis ähnelt diesem:

![](assets/img/2014-3-27-unity-depth-minimap/topview.png){ width="200" }

#Mischen Sie echte Weltbilder.
Allein die tiefen Farbbilder könnten etwas langweilig sein, also können wir die Farbgebung eines realen Szenenbildes mischen. Dazu müssen wir einen zusätzlichen Shader erstellen, der das vorherige Bild und das echte Bild der Kamera übergibt und in `OnRenderImage` die Mischung vornimmt:

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
Der obenstehende Code erfüllt diese Aufgabe. Es ist wichtig zu verstehen, dass beim Aufrufen von `RenderWithShader` auch `OnRenderImage` aufgerufen wird, was bedeutet, dass diese Funktion zweimal aufgerufen wird und die beiden Aufrufe unterschiedliche Funktionen erfüllen müssen. Daher verwende ich hier eine Variable, um den aktuellen Renderstatus anzuzeigen, ob ein Tiefenbild oder eine Mischung durchgeführt wird.

#Vollständiger Code
Die Code-Dateien sind etwas zu viele, also habe ich sie hier abgelegt [depth-minimap](assets/img/2014-3-27-unity-depth-minimap/2014-3-27-unity-depth-minimap.zip)Unfortunately, I cannot translate the text as it does not contain any meaningful content. If you have any other text you need help with, feel free to ask!

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt; bitte geben Sie Ihr [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Bitte identifizieren Sie etwaige Lücken. 
