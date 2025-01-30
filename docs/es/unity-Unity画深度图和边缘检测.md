---
layout: post
title: Unity genera mapas de profundidad (Depth Map) y detección de bordes (Edge Detection).
categories:
- unity
catalog: true
tags:
- dev
description: Descubrí que RenderWithShader() y OnRenderImage() de Unity se pueden
  usar para lograr muchos efectos. Aprovechando la oportunidad de aprender, decidí
  utilizar estas dos funciones para implementar la generación del mapa de profundidad
  de la escena y la detección de bordes de la escena, que se puede usar como un pequeño
  mapa del juego.
figures:
- assets/post_assets/2014-3-27-unity-depth-minimap/topview.png
---

<meta property="og:title" content="Unity画深度图(Depth Map)和边缘检测(Edge Detection)" />

Acabo de empezar a usar Unity hace poco tiempo, siempre he estado muy interesado en ShaderLab de Unity, siento que puede ayudar a lograr rápidamente una variedad de efectos visuales, es muy interesante. Bueno, como alguien que recién empieza, voy a explorar un poco con mapas de profundidad y detección de bordes.

#Configuración del mini mapa

Debido a que solo he desarrollado un boceto inicial, no tengo la intención de entrar en detalles sobre cómo crear mapas pequeños en la escena. En términos generales, he realizado las siguientes acciones:

1. Obtener el bounding box de la escena, lo cual es útil al configurar los parámetros y la posición de la cámara.
Configura la cámara del mapa pequeño para que utilice proyección ortográfica, ajustando el plano cercano y el plano lejano de la cámara según la caja delimitadora.
Agregar un objetivo de persona a la cámara, el objetivo se mostrará en el centro del mapa.
Cada vez que se actualiza la posición de la cámara, se tiene en cuenta la posición del objetivo y el valor máximo de y en la escena.

La configuración específica se puede consultar en el código proporcionado más adelante.

#Obtener mapa de profundidad.

##depthTextureMode se utiliza para obtener el mapa de profundidad.

La cámara puede guardar por sí misma un DepthBuffer o un DepthNormalBuffer (que se puede utilizar para la detección de bordes), solo es necesario configurarlo.

```c#
Camera.depthTextureMode = DepthTextureMode.DepthNormals;
```

Luego se hace referencia a esto en el Shader.

```c#
sampler2D _CameraDepthNormalsTexture;
```

Justo eso, puedes consultar el código que proporcioné más adelante para obtener instrucciones detalladas. Para obtener más información sobre la relación entre los valores de profundidad guardados en el búfer Z y la profundidad real del mundo, puedes consultar estos dos artículos:
[Learning to Love your Z-buffer](http://www.sjbaker.org/steve/omniv/love_your_z_buffer.html),[Linearize depth](http://www.humus.name/temp/Linearize%20depth.txt)Además, Unity también ofrece algunas funciones para calcular la profundidad: `Linear01Depth`, `LinearEyeDepth`, etc.

Este no es el punto que quiero discutir aquí. Lo que quería decir es que mi cámara originalmente estaba configurada para proyección ortogonal, así que la profundidad debería ser lineal, pero al probarla, no resulta ser lineal. Luego, utilicé el método indicado en el enlace anterior para calcular la profundidad en el mundo real, pero siempre ha estado incorrecto, hasta el punto en que no puedo obtener una profundidad lineal real. No sé si es un problema del Z_Buffer de Unity o qué; si algún amigo sabe, le agradecería que me enseñara. Por supuesto, si no se necesitan valores de profundidad reales, sino solo comparar tamaños de profundidad, el método anterior es suficiente y muy sencillo. Sin embargo, para mi caso, quiero mapear la profundidad real a valores de color, así que necesito obtener el valor de profundidad lineal real (aunque también esté en el rango [0, 1]), por lo que tendré que usar otro método con RenderWithShader.

##RenderWithShader para obtener el mapa de profundidad.

Este método en realidad es un ejemplo en la referencia de Unity: [Rendering with Replaced Shaders](http://docs.unity3d.com/Documentation/Components/SL-ShaderReplacement.html). Es importante entender que `RenderWithShader` renderizará el Mesh correspondiente en la escena.

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

Agrega un script a tu cámara de mini mapa (crea una si no la tienes) para configurar la cámara en proyección ortográfica, y utiliza este shader para renderizar la escena dentro de `Update()`:

```c#
camera.targetTexture = depthTexture;
camera.RenderWithShader(depthShader, "");
```

El resultado de la renderización se guardará en `depthTexture`, muy sencillo, ¿verdad?

##Transforma la profundidad en colores.
Para completar este trabajo, primero se necesita una imagen en color, esta imagen se puede generar fácilmente con Matlab, por ejemplo, yo utilicé la imagen 'jet' dentro de Matlab:

![](assets/img/2014-3-27-unity-depth-minimap/jet.png){ width="200" }

Coloca esta imagen en el directorio del proyecto `Assets\Resources`, y podrás leerla en el programa:

```c#
colorMap = Resources.Load<Texture2D>("colormap");
```

Es importante tener en cuenta que el modo de envoltura (`Wrap Mode`) de esta imagen debería ser `Clamp`, para evitar la interpolación entre los valores de color en los bordes.

Después se necesita utilizar la función `OnRenderImage` y `Graphics.Blit`, cuyo prototipo es:

```c#
void OnRenderImage(RenderTexture src, RenderTexture dst);
static void Blit(Texture source, RenderTexture dest, Material mat, int pass = -1);
```

La fuente (src) de esta función es el resultado de la renderización de la cámara, y el destino (dst) es el resultado que se devuelve a la cámara tras el procesamiento. Por lo tanto, esta función se utiliza generalmente para aplicar efectos a las imágenes una vez que la cámara ha completado la renderización, como el mapeo de colores para la profundidad y la detección de bordes que tenemos aquí. La manera de hacerlo es llamar a `Graphics.Blit` en `OnRenderImage`, pasando un `Material` específico:

```c#
depthEdgeMaterial.SetTexture("_DepthTex", src);
Graphics.Blit(src, dst, depthEdgeMaterial);
return;
```

Lo que hay que tener en cuenta es que `Graphics.Blit` en realidad hace lo siguiente: dibuja un plano del mismo tamaño que la pantalla delante de la cámara, establece `src` como `_MainTex` de este plano en el `Shader`, luego coloca el resultado en `dst`, en lugar de renderizar de nuevo toda la malla de la escena real.

La asignación de colores en realidad consiste en considerar la profundidad [0, 1] como las coordenadas u y v de una imagen, ya que deseo que lo cercano a la cámara aparezca en rojo, por lo tanto, he invertido la profundidad:

```glsl
half4 color = tex2D(_ColorMap, float2(saturate(1-depth), 0.5));
```

#Detección de bordes
La detección de bordes requiere el uso de la propia `_CameraDepthNormalsTexture` de la cámara, principalmente utilizando los valores de Normales, mientras que la profundidad se calcula con los datos previamente obtenidos. En cada píxel (x, y, z, w) de `_CameraDepthNormalsTexture`, (x, y) representa la normal y (z, w) es la profundidad. Las normales se almacenan utilizando un método específico, que puedes investigar si te interesa.

El código se basa en la detección de bordes del efecto de imagen incorporado en Unity. Lo que hay que hacer es comparar la profundidad normal del píxel actual con la diferencia de los píxeles cercanos. Si es lo suficientemente grande, consideramos que hay un borde.

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

El Shader completo es el siguiente:

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

El resultado es similar a esto: 

![](assets/img/2014-3-27-unity-depth-minimap/topview.png){ width="200" }

#Mezcla de imágenes del mundo real
Sola la profundidad de la imagen de color puede ser un poco aburrida, así que podemos mezclarla con el mapa de color de la escena real. Solo necesitamos crear un Shader adicional, pasando la imagen anterior y la imagen real de la cámara, y mezclando en `OnRenderImage`:

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
El código anterior realiza esta tarea. Lo que se necesita entender es que, al llamar a `RenderWithShader`, también se llamará a `OnRenderImage`, es decir, esta función se llama dos veces y las funcionalidades que deben cumplirse en cada llamada son diferentes. Por eso aquí utilizo una variable para indicar el estado actual de la renderización: si se está haciendo un mapa de profundidad o mezcla.

#Código completo
El archivo de código es un poco extenso, así que lo dejo aquí [depth-minimap](assets/img/2014-3-27-unity-depth-minimap/2014-3-27-unity-depth-minimap.zip)Lo siento, pero no puedo traducir ese texto ya que no contiene ninguna información. ¿Hay algo más en lo que pueda ayudarte?

--8<-- "footer_es.md"


> Este post fue traducido utilizando ChatGPT, por favor en [**Comentarios**](https://github.com/disenone/wiki_blog/issues/new)Señale cualquier omisión. 
