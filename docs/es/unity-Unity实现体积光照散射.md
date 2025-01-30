---
layout: post
title: Unity implementa la dispersión volumétrica de la luz (Volumetric Light Scattering,
  también conocida como cloud crevice light)
categories:
- unity
catalog: true
tags:
- dev
description: La dispersión de luz volumétrica es un efecto visual bastante interesante,
  como si pudieras ver la propagación de la luz en el aire, las partículas en el aire
  iluminadas por la luz, mientras que parte de la luz es obstruida, creando visualmente
  rayos que parecen irradiar desde la fuente de luz.
figures:
- assets/post_assets/2014-3-30-unity-light-scattering/effect.gif
---

<meta property="og:title" content="Unity实现体积光照散射 (Volumetric Light Scattering，云隙光)" />

##Principio

El principio de Volumetric Light Scattering se puede consultar en "GPU Gems 3" [Capítulo 13](http://http.developer.nvidia.com/GPUGems3/gpugems3_ch13.html)，libro con imágenes efectivas:

![](assets/img/2014-3-30-unity-light-scattering/goodeffect.png)

¡Se ve bien, verdad? Bueno, nuestro objetivo es lograr ese efecto.

El libro explica los principios, una fórmula clave es:

\\[ L(s, \theta, \phi) = exposure \times \sum\_{i=0}^n decay^i \times weight \times \frac{L( s\_i, \theta\_i )}{n} \\]

Mi comprensión es que, para cada píxel en una imagen, la luz puede incidir en él. Por lo tanto, se muestrea la línea que conecta dicho píxel con la fuente de luz (proyectada en la posición de la imagen) (representada en la fórmula como \( i \)), se promedian los resultados muestreados (representado en la fórmula como \( \sum \)) y se utiliza como el nuevo valor de color del píxel. Además, es crucial el sombreador de píxeles posterior, pero si se utiliza solo ese sombreador para procesar los resultados del renderizado de la cámara, se generarán trazas artificiales evidentes, como muchas franjas:

![](assets/img/2014-3-30-unity-light-scattering/badeffect.png)

¿Cómo se logra el efecto mostrado en el libro? En realidad, el libro ya ofrece la respuesta, la cual puede ser explicada a través de un conjunto de gráficos.

![](assets/img/2014-3-30-unity-light-scattering/steps.png)

El texto traducido al español sería:

"A" representa un efecto rugoso, se pueden apreciar muchas líneas cuidadosamente, sin ocultar la falta de realismo. Los pasos a seguir para obtener un buen efecto son "b", "c" y "d".

b. Renderizar el efecto de radiación de luz en la imagen y añadir la oclusión de los objetos.

Aplicar el sombreador de píxeles Volumetric Light Scattering a la entidad b para lograr el efecto de ocultación.

Agregar el color de la escena real.

Entonces ahora procederemos a llevarlo a cabo paso a paso.

##Dibuja un objeto que oculte.

En la práctica, primero utilizo `RenderWithShader` para pintar los objetos que sufrirán oclusión de color negro, mientras que en otras áreas será blanco. Dado que esto requiere renderizar cada polígrafo, para escenas complejas puede haber un cierto desgaste en el rendimiento. Los objetos en la escena son opacos y transparentes; esperamos que los objetos opacos generen una oclusión total de la luz, mientras que los objetos transparentes deben generar una oclusión parcial. Por lo tanto, necesitamos escribir diferentes Shaders para objetos de diferentes RenderType. RenderType es una etiqueta del SubShader; si no lo entiendes, puedes consultar [aquí](http://docs.unity3d.com/Documentation/Components/SL-SubshaderTags.html)Una vez que hayas escrito, llama a:

```c#
camera.RenderWithShader(objectOcclusionShader, "RenderType");

```
El segundo parámetro de `RenderWithShader` requiere reemplazar el Shader según el RenderType. En pocas palabras, el RenderType del Shader que se reemplaza en el mismo objeto debe ser el mismo que el de antes del reemplazo, de esta manera podemos utilizar diferentes Shaders para objetos de diferentes RenderTypes:

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

Nota la diferencia entre los shaders de objetos opacos y transparentes: los objetos opacos se dibujan directamente en negro; para los objetos opacos se necesita ejecutar el blending, obtener el canal alfa de la textura del objeto y realizar el blending basado en este alfa. El código anterior solo enumera Opaque y Transparent, además hay TreeOpaque (shader igual que Opaque, solo cambia el RenderType), TreeTransparentCutout (igual que Transparent), entre otros. Dado que se ha especificado el RenderType, para ser exhaustivos, es necesario incluir en la medida de lo posible todos los objetos en la escena que puedan causar superposición, y aquí solo tengo los cuatro tipos mencionados anteriormente. Los resultados son aproximadamente los siguientes:

![](assets/img/2014-3-30-unity-light-scattering/objectocclusion.png)

##Se utiliza la combinación de objetos para ocultar la radiación de fuentes de luz.

Traduce este texto al idioma español:

Dibujar la radiación de la fuente de luz no es difícil, lo que se debe tener en cuenta es que es necesario realizar ciertos ajustes según el tamaño de la pantalla, para que la radiación de la fuente de luz sea de forma circular:

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

Este Shader necesita la posición de la fuente de luz en la pantalla (se puede calcular usando `camera.WorldToViewportPoint`, obteniendo así las coordenadas uv), y luego dibuja un círculo cuyo brillo disminuye hacia afuera en función de un radio especificado, combinando el resultado con la imagen de oclusión del objeto obtenida anteriormente (almacenada en `_MainTex`), y el resultado es aproximadamente:

![](assets/img/2014-3-30-unity-light-scattering/light.png)

##Procesamiento de Dispersión de Luz, y combinación con colores reales.

Aquí se va a utilizar el Pixel Shader proporcionado en el libro, mi versión:

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

En general, es consistente con lo que dice el libro, solo que mis parámetros necesitan ser pasados en el programa, y se combinan con la imagen de color real y la imagen de dispersión de luz. El resultado:

![](assets/img/2014-3-30-unity-light-scattering/effect.gif)

##Código completo

El código está [aquí](assets/img/2014-3-30-unity-light-scattering/2014-3-30-unity-light-scattering.zip)Agrega el script `cs` a la cámara.

--8<-- "footer_es.md"


> Este mensaje ha sido traducido utilizando ChatGPT, por favor, envíe sus comentarios en [**反馈**](https://github.com/disenone/wiki_blog/issues/new)Señale cualquier omisión. 
