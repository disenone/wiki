---
layout: post
title: Unity realiza la dispersión de luz volumétrica (Volumetric Light Scattering,
  luz de brechas en las nubes)
categories:
- unity
catalog: true
tags:
- dev
description: La dispersión de la luz volumétrica es un efecto visual muy impresionante,
  te hace sentir como si estuvieras viendo la propagación de la luz en el aire, las
  partículas en el aire iluminadas por la luz y parte de la luz bloqueada, lo que
  crea visualmente los rayos de luz radiantes desde la fuente de luz.
figures:
- assets/post_assets/2014-3-30-unity-light-scattering/effect.gif
---

<meta property="og:title" content="Unity实现体积光照散射 (Volumetric Light Scattering，云隙光)" />

### **原理**

El término **原理** en el contexto proporcionado se traduce al español como **principio**.

El principio de Dispersión de Luz Volumétrica se puede consultar en "GPU Gems 3" [Capítulo 13](http://http.developer.nvidia.com/GPUGems3/gpugems3_ch13.html)，Imagen con resultados efectivos en el libro:

![](assets/img/2014-3-30-unity-light-scattering/goodeffect.png)

Bueno, de acuerdo, nuestro objetivo es lograr este resultado.

En el libro se explican los principios, siendo una fórmula clave la siguiente:

\\[ L(s, \theta, \phi) = exposure \times \sum\_{i=0}^n decay^i \times weight \times \frac{L( s\_i, \theta\_i )}{n} \\]

Mi comprensión es que, para cada píxel en la imagen, la luz puede incidir sobre él. Por lo tanto, se realiza un muestreo de la línea que conecta dicho píxel con la fuente de luz (en la posición proyectada en la imagen), lo cual se representa mediante la variable "i" en la fórmula correspondiente. Los resultados de este muestreo se promedian ponderadamente (representado por la suma en la fórmula) y se utilizan como el nuevo valor de color para ese píxel. Además, es importante mencionar el elemento clave del sombreador de píxeles posterior. Sin embargo, si solo se utiliza dicho sombreador para procesar los resultados de la renderización de la cámara, se pueden generar marcas artificiales evidentes, como muchas bandas.

![](assets/img/2014-3-30-unity-light-scattering/badeffect.png)

Entonces, ¿cómo se logra el efecto descrito en el libro? En realidad, el libro ya proporciona la respuesta, que puede ser ilustrada con un conjunto de imágenes:

![](assets/img/2014-3-30-unity-light-scattering/steps.png)

La imagen a es simplemente el resultado áspero. Si te fijas cuidadosamente, podrás ver muchas rayas y no hay suficiente realismo. Los pasos a seguir para obtener buenos resultados son b, c y d:

b. Renderizar el efecto de iluminación en la imagen y agregar la occlusión de los objetos.

c. Aplicar un sombreador de pixel de dispersión volumétrica a b para obtener el efecto de ocultación.

d. Agregar el color de la escena real

Entonces, a continuación vamos a llevar a cabo paso a paso.

##@media(spanish) {
 画遮挡物体
}

Traduce este texto al español: 

 Dibujar un objeto de obstrucción.

En la implementación real, primero uso `RenderWithShader` para pintar los objetos que se ocultarán de color negro, mientras que el resto del área se quedará blanco. Dado que esto requiere renderizar cada polígono individualmente, puede afectar el rendimiento en escenas complejas. En la escena hay objetos opacos y transparentes, y queremos que los objetos opacos bloqueen completamente la luz, mientras que los objetos transparentes solo bloqueen parcialmente. Por lo tanto, necesitamos escribir shaders distintos para objetos con diferentes valores de RenderType. RenderType es una etiqueta de SubShader. Si no está seguro, puede consultar [aquí](http://docs.unity3d.com/Documentation/Components/SL-SubshaderTags.html)，después de escribirlo, llamar a:

```c#
camera.RenderWithShader(objectOcclusionShader, "RenderType");

```
El segundo parámetro de `RenderWithShader` solicita la sustitución del Shader basado en el RenderType. En pocas palabras, el RenderType del Shader sustituto debe ser idéntico al del Shader original del mismo objeto. De esa manera, podemos utilizar diferentes Shaders para objetos con diferentes RenderTypes.

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

注意 la diferencia entre los Shaders de objetos opacos y transparentes: los objetos opacos se dibujan directamente en negro; los objetos transparentes requieren realizar blending para obtener el canal alfa de la textura del objeto y realizar blending basado en ese alfa. El código anterior solo menciona Opaque y Transparent, pero también hay TreeOpaque (el Shader es igual que Opaque, solo cambia el RenderType) y TreeTransparentCutout (igual a Transparent). Dado que se ha especificado el RenderType, para ser exhaustivos, es necesario abarcar todos los objetos que puedan ocultar la escena tanto como sea posible, pero aquí solo menciono estas cuatro mencionadas anteriormente. El resultado es aproximadamente el siguiente:

![](assets/img/2014-3-30-unity-light-scattering/objectocclusion.png)

##**结合物体遮挡画光源辐射**

Combina la obstrucción de objetos con la representación de la radiación de fuentes de luz.

La proyección de la fuente de luz no es difícil, lo que hay que tener en cuenta es que se debe realizar un procesamiento acorde al tamaño de la pantalla para que la proyección de la fuente de luz sea en forma de círculo.

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

Este Shader requiere la posición de la fuente de luz en la pantalla (puede calcularse utilizando `camera.WorldToViewportPoint`, obteniendo las coordenadas UV). Luego, se dibuja un círculo con un brillo que disminuye hacia afuera de acuerdo con el radio especificado. Este resultado se combina con la imagen de obstrucción del objeto obtenida anteriormente (almacenada en `_MainTex`). El resultado aproximado es el siguiente:

![](assets/img/2014-3-30-unity-light-scattering/light.png)

##**Light Scattering** es un proceso de procesamiento que se utiliza en combinación con colores reales.

Aquí se utilizará el Pixel Shader proporcionado en el libro, mi versión es:

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

大体上跟书上的一致，只是我的参数需要在程序中传进来，并且结合了真实的颜色图和Light Scattering图，结果：

![](assets/img/2014-3-30-unity-light-scattering/effect.gif)

##完整代码

Código completo

El código está [aquí](assets/img/2014-3-30-unity-light-scattering/2014-3-30-unity-light-scattering.zip), añade el script `cs` a la cámara.

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
