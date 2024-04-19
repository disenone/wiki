---
layout: post
title: Unity genera mapas de profundidad ("Depth Map") y realiza detección de bordes
  ("Edge Detection").
categories:
- unity
catalog: true
tags:
- dev
description: Descubrí que las funciones RenderWithShader() y OnRenderImage() de Unity
  se pueden utilizar para lograr muchos efectos. Aprovechando esta oportunidad de
  aprendizaje, decidí utilizar estas dos funciones para generar un mapa de profundidad
  y realizar detección de bordes en la escena. Esto puede ser utilizado como un tipo
  de mini mapa en el juego.
figures:
- assets/post_assets/2014-3-27-unity-depth-minimap/topview.png
---

<meta property="og:title" content="Unity画深度图(Depth Map)和边缘检测(Edge Detection)" />

Acabo de empezar a usar Unity hace poco tiempo y siempre he estado interesado en ShaderLab de Unity. Siento que me permite implementar rápidamente todo tipo de efectos visuales, es muy interesante. Bueno, como alguien que aún no ha comenzado en serio, voy a probar con el mapa de profundidad y la detección de bordes.

#**小地图设置**

Debido a que solo hice un boceto pequeño, no planeo entrar en detalles sobre cómo dibujar un mapa en la escena. En pocas palabras, hice las siguientes cosas:

1. Obtener el cuadro delimitador de la escena, esto es útil al configurar los parámetros y la posición de la cámara.
2. Configura la cámara de la vista en miniatura para que utilice una proyección ortográfica, y establece el plano cercano y el plano lejano de la cámara según las dimensiones del cuadro delimitador.
3. Para agregar un objetivo de persona a esta cámara, el objetivo se mostrará en el centro del mapa.
4. Cada vez que se actualice la posición de la cámara, se considerará la posición del objetivo y el valor máximo de la escena en el eje 'y'.

La configuración específica se puede consultar en el código proporcionado a continuación.

#Obtener mapa de profundidad

##`depthTextureMode` se utiliza para obtener la textura de profundidad.

La cámara puede guardar por sí misma el DepthBuffer o un DepthNormalBuffer (utilizado para la detección de bordes), solo necesitas configurarlo.

```c#
Camera.depthTextureMode = DepthTextureMode.DepthNormals;
```

Entonces, en el Shader se hace referencia a esto.

```c#
sampler2D _CameraDepthNormalsTexture;
```

Simplemente eso, puedes consultar el código que he proporcionado más adelante para obtener instrucciones detalladas. Para entender la relación entre los valores de profundidad guardados en el Z-Buffer y la profundidad real del mundo, consulta los siguientes dos artículos:
[Learning to Love your Z-buffer](http://www.sjbaker.org/steve/omniv/love_your_z_buffer.html),[Linearize depth](http://www.humus.name/temp/Linearize%20depth.txt)Además, Unity también proporciona algunas funciones para calcular la profundidad: `Linear01Depth`, `LinearEyeDepth`, etc.

No es el punto que estoy discutiendo aquí. Lo que quiero decir es que, originalmente, mi cámara estaba configurada en proyección ortográfica y se suponía que la profundidad sería lineal. Sin embargo, al hacer las pruebas, descubrí que no era lineal. Intenté utilizar el método mencionado en el enlace anterior para calcular la profundidad del mundo real, pero siempre obtuve resultados incorrectos. No sé si se trata de un problema con el Z_Buffer de Unity o algo más. Si alguien sabe, por favor, enséñenme. Por supuesto, si no necesitas el valor de profundidad real y solo quieres comparar tamaños de profundidad u otros aspectos similares, el método mencionado anteriormente es suficiente y bastante sencillo. Pero en mi caso, necesito mapear la verdadera profundidad en valores de color y obtener una profundidad lineal real (aunque también esté en el rango de [0, 1]). Por lo tanto, me vi obligado a utilizar otro método, utilizando `RenderWithShader`.

##Utiliza RenderWithShader para obtener el mapa de profundidad.

Esta técnica en realidad utiliza un ejemplo del Unity Reference: [Rendering with Replaced Shaders](http://docs.unity3d.com/Documentation/Components/SL-ShaderReplacement.html)Es importante entender que `RenderWithShader` dibuja la malla correspondiente de la escena.

Crear un Shader:

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

Para agregar un script a tu cámara de mini mapa (si no lo tienes, créalo), configura la cámara para utilizar una proyección ortográfica, y utiliza este Shader para renderizar la escena en el método `Update()`.

```c#
camera.targetTexture = depthTexture;
camera.RenderWithShader(depthShader, "");
```

El resultado del renderizado se almacenará en `depthTexture`, muy sencillo.

##Transformar la profundidad en colores
Para completar este trabajo, primero se necesita una imagen en color. Esta imagen se puede generar fácilmente con Matlab, por ejemplo, utilizando el gráfico "jet" disponible en Matlab.

![](assets/img/2014-3-27-unity-depth-minimap/jet.png){ width="200" }

Coloca esta imagen en el directorio del proyecto `Assets\Resources`, y podrás acceder a ella en el programa:

```c#
colorMap = Resources.Load<Texture2D>("colormap");
```

El **modo de envoltura** de esta imagen debe ser `Clamp`, para evitar la interpolación entre los valores de color en los bordes.

Después de eso, necesitarás usar las funciones `OnRenderImage` y `Graphics.Blit`. El prototipo de la función es:

```c#
void OnRenderImage(RenderTexture src, RenderTexture dst);
static void Blit(Texture source, RenderTexture dest, Material mat, int pass = -1);
```

Esta función toma el resultado del renderizado de la cámara como entrada (src) y devuelve el resultado procesado de nuevo a la cámara (dst). Por lo tanto, normalmente se utiliza para aplicar algunos efectos a una imagen después de que se haya completado el renderizado de la cámara. Por ejemplo, en este caso, estamos aplicando una asignación de colores a la profundidad, así como una detección de bordes. El procedimiento implica llamar a `Graphics.Blit` en el método `OnRenderImage` y pasar un `Material` específico.

```c#
depthEdgeMaterial.SetTexture("_DepthTex", src);
Graphics.Blit(src, dst, depthEdgeMaterial);
return;
```

Necesita tener en cuenta que `Graphics.Blit` en realidad realiza la siguiente acción: dibuja un plano del mismo tamaño que la pantalla delante de la cámara, utiliza `src` como el valor `_MainTex` de este plano y lo pasa a través del `Shader`, luego coloca el resultado en `dst`, en lugar de volver a dibujar la malla de la escena real.

La asignación de colores es básicamente tomar la profundidad [0, 1] y considerarla como las coordenadas UV de una imagen. Como quiero que lo que está más cerca de la cámara sea de color rojo, invierto la profundidad.

```glsl
half4 color = tex2D(_ColorMap, float2(saturate(1-depth), 0.5));
```

#**边缘检测**
La detección de bordes requiere el uso de `_CameraDepthNormalsTexture` de la propia cámara, principalmente para obtener los valores de las normales, mientras que la profundidad se obtiene a partir de un cálculo previo. En cada píxel (x, y, z, w) de `_CameraDepthNormalsTexture`, (x, y) representa las normales y (z, w) representa la profundidad. Las normales se almacenan utilizando un método específico, si tienes interés, puedes realizar tu propia investigación al respecto.

El código se basa en la detección de bordes de los efectos de imagen incorporados en Unity. Lo que se debe hacer es comparar la diferencia de profundidad normal del píxel actual con los píxeles vecinos. Si es lo suficientemente grande, consideramos que hay un borde.

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

El código completo del Shader es el siguiente:

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

El resultado es similar a este:

![](assets/img/2014-3-27-unity-depth-minimap/topview.png){ width="200" }

#**混合真实世界图像**

En el campo de la realidad aumentada, el término "混合真实世界图像" se refiere a la integración de imágenes virtuales con el entorno real. Esta técnica permite superponer elementos generados por ordenador en tiempo real sobre una imagen en directo capturada por una cámara. Con esta tecnología, es posible crear experiencias interactivas y enriquecidas que combinan el mundo físico con elementos digitales.
Simplemente tener una imagen de color en 2D puede ser un poco aburrido, por lo que podemos mezclarla con una imagen realista de una escena. Solo necesitamos crear un Shader adicional, pasar la imagen anterior y la imagen real de la cámara, y mezclarlas en `OnRenderImage`.

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
El código anterior es el encargado de realizar esta tarea, lo que se debe entender es que, al llamar a `RenderWithShader`, también se llama a `OnRenderImage`, es decir, esta función se llama dos veces, pero se requiere realizar funcionalidades diferentes en cada llamada. Por eso, aquí utilizo una variable para indicar si el estado actual de renderizado es para hacer un mapa de profundidad o una mezcla.

#**Código completo**
El archivo de código es un poco largo, así que lo he colocado aquí [depth-minimap](assets/img/2014-3-27-unity-depth-minimap/2014-3-27-unity-depth-minimap.zip)Lo siento, pero necesito algo más de contexto para poder traducir el texto adecuadamente. ¿Puede brindarme más información sobre lo que desea traducir?

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
