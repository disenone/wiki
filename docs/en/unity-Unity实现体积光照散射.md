---
layout: post
title: Unity implements Volumetric Light Scattering (also known as cloud gap light).
categories:
- unity
catalog: true
tags:
- dev
description: Volume light scattering is a pretty neat visual effect where you can
  see the propagation of light in the air. The particles in the air are illuminated
  by the light while some of the light rays are blocked, resulting in visual rays
  radiating from the light source.
figures:
- assets/post_assets/2014-3-30-unity-light-scattering/effect.gif
---



## Principle

The principle of Volumetric Light Scattering can be referenced in Chapter 13 of "GPU Gems 3" ([link](http://http.developer.nvidia.com/GPUGems3/gpugems3_ch13.html)). The book contains informative illustrations.

![](assets/img/2014-3-30-unity-light-scattering/goodeffect.png)

Looks good, well then, our goal is to achieve this effect.

The book explains the principle, and one crucial formula is:

\\[ L(s, \theta, \phi) = exposure \times \sum\_{i=0}^n decay^i \times weight \times \frac{L( s\_i, \theta\_i )}{n} \\]

My understanding is that for each pixel in the image, light can be projected onto it. Then, samples are taken along the line connecting the pixel to the light source (corresponding to the formula \\(i\\)). The sampled results are weighted and averaged (corresponding to the formula \\(\sum\\)), and this average is used as the new color value for that pixel. There is also a crucial post-pixel shader, but if only that shader is used to process the camera's rendering result, it will result in obvious artificial artifacts, such as many stripes.

![](assets/img/2014-3-30-unity-light-scattering/badeffect.png)

So how is the effect in the book achieved? Actually, the book has already provided the answer, it can be explained using a set of pictures:

![](assets/img/2014-3-30-unity-light-scattering/steps.png)

图a (Figure a) is the rough effect, if you look carefully, you can see many stripes, and there is no sufficient coverage, not realistic enough. Steps b, c, d are necessary to achieve a good result.

b. Render the radiance effect of the lighting onto the image, and add occlusion of objects.

c. Apply Volumetric Light Scattering pixel shader to b to achieve the desired effect after occlusion.

d. Add the color of real scenes.

So now let's go step by step and implement it.

## Paint obscuring objects

In actual practice, I first use `RenderWithShader` to render objects that will be occluded in black, while other areas will be rendered in white. This operation requires rendering each face individually, which may result in some performance overhead for complex scenes. There are both opaque and transparent objects in the scene. We want opaque objects to fully occlude light, while transparent objects should only partially occlude it. To achieve this, we need to write different shaders for objects with different RenderTypes. RenderType is the tag of the SubShader. If you are not familiar with it, you can refer to [here](http://docs.unity3d.com/Documentation/Components/SL-SubshaderTags.html). After writing the shaders, we call:

```c#
camera.RenderWithShader(objectOcclusionShader, "RenderType");

```
The second parameter of `RenderWithShader` is used to specify the replacement Shader based on the RenderType. In simple terms, the replacement Shader for the same object should have the same RenderType as the original Shader, allowing us to use different Shaders for objects with different RenderTypes.

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

Note the differences between shaders for opaque and transparent objects: opaque objects are directly drawn as black; transparent objects require blending, taking the alpha channel from the object's texture and blending based on this alpha. The above code only lists Opaque and Transparent, but there are also other shaders like TreeOpaque (same as Opaque, just changes RenderType) and TreeTransparentCutout (same as Transparent). Since RenderType is specified, in order to be comprehensive, it is necessary to exhaustively consider objects that may cause occlusion in the scene. Here, I only have the four types mentioned earlier. The results are roughly as follows:

![](assets/img/2014-3-30-unity-light-scattering/objectocclusion.png)

## Combining object occlusion and rendering of light sources

Drawing the radiation of the light source is not difficult. What needs to be noted is that some adjustments need to be made according to the size of the screen to ensure that the radiation of the light source appears circular.

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

This Shader requires the input of the position of the light source on the screen (which can be calculated using `camera.WorldToViewportPoint`, resulting in the uv coordinates). Then, it draws a circle with a specified radius that gradually attenuates the brightness outward. The result is then combined with the previously obtained object occlusion image (stored in `_MainTex`). The overall result is approximately:

![](assets/img/2014-3-30-unity-light-scattering/light.png)

## Light Scattering processing, combined with true colors

I will need to use the Pixel Shader provided in the book, version [to_be_replace[x]]:


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

More or less consistent with what is written in the book, except that my parameters need to be passed into the program, combined with real color images and Light Scattering images, the results are:

![](assets/img/2014-3-30-unity-light-scattering/effect.gif)

## Complete Code

The code is [here](assets/img/2014-3-30-unity-light-scattering/2014-3-30-unity-light-scattering.zip), add the `cs` script to the camera.

> Original: <https://disenone.github.io/wiki>  
> This post is protected by [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by/4.0/deed.en) agreement, should be reproduced with attribution.


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
