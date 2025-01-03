---
layout: post
title: Unity erstellt Tiefenkarten (Depth Maps) und führt Kantenerkennung (Edge Detection)
  durch.
categories:
- unity
catalog: true
tags:
- dev
description: Entdeckt, dass Unity's RenderWithShader() und OnRenderImage() für viele
  Effekte eingesetzt werden können, habe ich beschlossen, während dem Lernen diese
  beiden Funktionen zu nutzen, um Tiefenkarten der Szene zu erstellen und Kanten zu
  erkennen. Diese können dann als eine Art Mini-Karte im Spiel verwendet werden.
figures:
- assets/post_assets/2014-3-27-unity-depth-minimap/topview.png
---

<meta property="og:title" content="Unity画深度图(Depth Map)和边缘检测(Edge Detection)" />

Gerade erst vor kurzem mit Unity in Berührung gekommen, war immer schon interessiert an Unity's ShaderLab. Es scheint, dass es schnell verschiedene Anzeigeeffekte umsetzen kann, sehr faszinierend. Nun ja, als jemand, der noch am Anfang steht, werde ich mich mal mit Tiefenkarten und Kantenerkennung beschäftigen.

#Kleine Kartenoptionen

Da ich nur einen Entwurf gemacht habe, habe ich nicht vor, im Detail zu erklären, wie man kleine Karten in Szenen einzeichnet. Kurz gesagt, habe ich folgendes gemacht:

Erhalten Sie die Begrenzungsrahmen der Szene, dies ist nützlich beim Festlegen der Kameraparameter und -position.
Konfigurieren Sie die Minikartenkamera so, dass sie eine orthografische Projektion verwendet, und legen Sie die Nähe- und Fernplane der Kamera gemäß der Begrenzungsrahmen fest.
Fügen Sie dem Kamera ein Personenziel hinzu; das Ziel wird in der Mitte der Karte angezeigt.
Jedes Mal, wenn die Kamera neu positioniert wird, basierend auf der Position des Ziels und dem maximalen y-Wert der Szene.

Die genauen Einstellungen können im untenstehenden Code überprüft werden.

#Erhalten Sie ein Tiefenbild.

##depthTextureMode wird verwendet, um Tiefenkarten abzurufen.

Die Kamera kann entweder einen Tiefenpuffer oder einen Tiefen-Normalen-Puffer speichern (zum Beispiel für die Kantenerkennung), es muss nur eingestellt werden.

```c#
Camera.depthTextureMode = DepthTextureMode.DepthNormals;
```

Then reference it in the shader.

```c#
sampler2D _CameraDepthNormalsTexture;
```

Das ist in Ordnung, Sie können sich an dem Code orientieren, den ich Ihnen später geben werde. Für weitere Informationen über den Zusammenhang zwischen den im Z-Buffer gespeicherten Tiefenwerten und den Tiefenwerten der realen Welt können Sie sich auf die folgenden beiden Artikel beziehen:
[Learning to Love your Z-buffer](http://www.sjbaker.org/steve/omniv/love_your_z_buffer.html),[Linearize depth](http://www.humus.name/temp/Linearize%20depth.txt)Unity bietet auch einige Funktionen zur Berechnung von Tiefen wie `Linear01Depth` und `LinearEyeDepth`.

Dies ist nicht der Fokus meiner Diskussion hier, was ich sagen möchte, ist dass meine Kamera ursprünglich auf orthographische Projektion eingestellt war und die Tiefe linear sein sollte, aber ich fand heraus, dass sie nicht linear ist. Dann habe ich versucht, die tatsächliche Welttiefe mit der Methode aus dem obigen Link zu berechnen, aber es war immer falsch, sodass ich die echte lineare Tiefe nie berechnen konnte. Ich weiß nicht, ob es am Z-Buffer von Unity liegt oder an etwas anderem. Kann mir jemand, der sich damit auskennt, bitte weiterhelfen? Natürlich, wenn echte Tiefenwerte nicht benötigt werden, sondern nur Vergleiche der Tiefen, reicht die oben genannte Methode aus und ist sehr einfach. Aber in meinem Fall möchte ich die echte Tiefe in Farbwerte umwandeln, daher benötige ich echte lineare Tiefenwerte (obwohl sie auch im Bereich von [0, 1] liegen). Deshalb musste ich auf eine andere Methode mit RenderWithShader zurückgreifen.

##Verwenden Sie RenderWithShader, um das Tiefenbild zu erhalten.

Diese Methode basiert tatsächlich auf einem Beispiel im Unity-Referenzhandbuch: [Rendering with Replaced Shaders](http://docs.unity3d.com/Documentation/Components/SL-ShaderReplacement.html)Es muss verstanden werden, dass `RenderWithShader` das entsprechende Mesh in der Szene zeichnet.

Erstellen Sie einen Shader:

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

Fügen Sie Ihrem Mini-Kartenkamera (falls nicht vorhanden, erstellen Sie sie) ein Skript hinzu, um die Kamera auf eine orthografische Projektion und dergleichen einzustellen, und verwenden Sie diesen Shader im `Update()` für das Rendern der Szene:

```c#
camera.targetTexture = depthTexture;
camera.RenderWithShader(depthShader, "");
```

Die gerenderten Ergebnisse werden einfach im `depthTexture` gespeichert. Einfach, oder?

##Konvertieren Sie die Tiefe in Farbe.
Um diese Arbeit zu erledigen, wird zunächst ein Farbdiagramm benötigt. Dieses Diagramm kann ganz einfach mit Matlab erstellt werden, zum Beispiel verwende ich das Jet-Diagramm in Matlab.

![](assets/img/2014-3-27-unity-depth-minimap/jet.png){ width="200" }

Legen Sie dieses Bild in das Projektverzeichnis `Assets\Resources`, so dass Sie es im Code lesen können:

```c#
colorMap = Resources.Load<Texture2D>("colormap");
```

Bitte beachten Sie, dass der `Wrap Mode` dieses Bildes auf `Clamp` eingestellt sein sollte, um eine Interpolation zwischen den Farbwerten am Rand zu verhindern.

Danach muss man die Funktionen `OnRenderImage` und `Graphics.Blit` nutzen, deren Prototyp wie folgt aussieht:

```c#
void OnRenderImage(RenderTexture src, RenderTexture dst);
static void Blit(Texture source, RenderTexture dest, Material mat, int pass = -1);
```

Die src dieses Funktion ist das Rendering-Ergebnis der Kamera, während dst das nach der Bearbeitung an die Kamera zurückgegebene Ergebnis ist. Daher wird diese Funktion normalerweise verwendet, um nach Abschluss des Kamera-Renderings einige Effekte auf das Bild anzuwenden, wie z.B. die Farbzuweisung an die Tiefe und die Kantenerkennung, die wir hier machen. Der Ansatz besteht darin, in `OnRenderImage` `Graphics.Blit` aufzurufen und ein spezifisches `Material` zu übergeben:

```c#
depthEdgeMaterial.SetTexture("_DepthTex", src);
Graphics.Blit(src, dst, depthEdgeMaterial);
return;
```

Die `Graphics.Blit`-Funktion führt im Grunde genommen Folgendes aus: Sie zeichnet eine Ebene vor der Kamera, die die gleiche Größe wie der Bildschirm hat. Dann wird `src` als `_MainTex` in diesen Shader übergeben und das Ergebnis wird in `dst` platziert, anstatt das Mesh der tatsächlichen Szene erneut zu zeichnen.

Die Farbzuordnung ist im Grunde genommen, wenn man die Tiefe [0, 1] als die uv-Koordinaten des Bildes betrachtet. Da ich möchte, dass Objekte, die näher an der Kamera liegen, rot angezeigt werden, habe ich die Tiefe umgekehrt:

```glsl
half4 color = tex2D(_ColorMap, float2(saturate(1-depth), 0.5));
```

#Kantenerkennung
Die Kanten-Erkennung benötigt die `_CameraDepthNormalsTexture` der Kamera, hauptsächlich für die Normalenwerte, während die Tiefe weiterhin aus vorherigen Berechnungen stammt. In jedem Pixel (x, y, z, w) der `_CameraDepthNormalsTexture` sind (x, y) die Normalen und (z, w) die Tiefe. Die Normalen werden auf eine spezielle Weise gespeichert, Interessierte können dies selbst recherchieren.

Der Code wurde basierend auf der Kantenentdeckung in den von Unity bereitgestellten Bild-Effekten erstellt. Die Aufgabe besteht darin, den Unterschied zwischen der Normalentiefe des aktuellen Pixels und benachbarter Pixel zu vergleichen. Wenn dieser Unterschied groß genug ist, nehmen wir an, dass eine Kante vorhanden ist.

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

#Mischen von echten Weltbildern
Nur eine Tiefenkarte zu haben, ist vielleicht ein bisschen langweilig, also könnten wir die Tiefenkarte mit Farben aus der realen Szene mischen. Es ist nur notwendig, einen zusätzlichen Shader zu erstellen, der das vorherige Bild und das echte Kamerabild einbezieht und die Mischung in `OnRenderImage` durchführt:

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
Der obenstehende Code erledigt diese Aufgabe. Was wichtig ist zu verstehen, ist dass beim Aufruf von `RenderWithShader` auch `OnRenderImage` aufgerufen wird. Das bedeutet, dass diese Funktion zweimal aufgerufen wird, aber jedes Mal verschiedene Aufgaben zu erledigen hat. Darum benutze ich hier eine Variable, um anzuzeigen, ob der aktuelle Rendering-Status Tiefe oder Mischung ist.

#Vollständiger Code
Die Code-Dateien sind ziemlich zahlreich, daher habe ich sie hier abgelegt [depth-minimap](assets/img/2014-3-27-unity-depth-minimap/2014-3-27-unity-depth-minimap.zip)I'm sorry, but I cannot provide a translation for the character "。" as it does not contain any content to be translated.

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt. Bitte [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Zeigen Sie alles, was fehlt. 
