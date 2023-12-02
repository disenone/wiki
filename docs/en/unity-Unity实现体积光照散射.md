---
layout: post
title: Unity implements volumetric light scattering (also known as Volumetric Light
  Scattering, or cloud gap light)
categories:
- unity
catalog: true
tags:
- dev
description: Volumetric light scattering is a pretty cool visual effect. It's like
  seeing how light spreads in the air, illuminating particles and creating the illusion
  of rays radiating from the light source.
figures:
- assets/post_assets/2014-3-30-unity-light-scattering/effect.gif
---

<meta property="og:title" content="Unity实现体积光照散射 (Volumetric Light Scattering，云隙光)" />

## Principle

The principle of Volumetric Light Scattering can be referred to in Chapter 13 of "GPU Gems 3" (http://http.developer.nvidia.com/GPUGems3/gpugems3_ch13.html). The book contains effective illustrations.

![](assets/img/2014-3-30-unity-light-scattering/goodeffect.png)

[to_be_replace_0]Good-looking, well, then, our goal is to achieve this effect.

The book explains the principle, and one key formula is:

\\[ L(s, \theta, \phi) = exposure \times \sum\_{i=0}^n decay^i \times weight \times \frac{L( s\_i, \theta\_i )}{n} \\]

My understanding is that for each pixel on the image, light can be projected onto it. Therefore, we sample the line connecting the pixel to the light source (corresponding to the formula \\(i\\)), and the sampled result is weighted and averaged (corresponding to the formula \\(\sum\\)), which becomes the new color value for that pixel. Additionally, there is a crucial post-pixel shader, but if we only use that shader to process the rendering results from the camera, it will create noticeable artificial artifacts, such as many stripes.

![](assets/img/2014-3-30-unity-light-scattering/badeffect.png)

So how is the effect in the book achieved? In fact, the answer is already provided in the book and can be illustrated using a set of images:

![](assets/img/2014-3-30-unity-light-scattering/steps.png)

图a represents a rough effect, and if you look carefully, you can see many stripes, and it doesn't cover up the lack of authenticity. Steps b, c, and d are necessary to achieve a good effect.

b. Render the lighting radiance effect onto the image and add object occlusion.

c. Apply the Volumetric Light Scattering pixel shader to b to achieve the effect after occlusion.

d. Add colors from real scenes.

Then let's proceed step by step.

## Painting Obstacles

In actual operation, I first use `RenderWithShader` to render the objects that will be occluded in black, and the rest in white. Because this requires rendering each face, it can lead to a certain performance cost for complex scenes. The objects in the scene can be opaque or transparent. We want opaque objects to produce full occlusion of light, while transparent objects should produce partial occlusion. Therefore, we need to write different shaders for objects with different RenderTypes. RenderType is the Tag for SubShader. If you are not clear about it, you can refer to [here](http://docs.unity3d.com/Documentation/Components/SL-SubshaderTags.html). After writing the shaders, we can call them like this:

```c#
camera.RenderWithShader(objectOcclusionShader, "RenderType");

```
The second parameter of `RenderWithShader` is used to specify the Shader replacement based on the RenderType. In simple terms, when replacing the Shader for the same object, the RenderType of the replacement Shader must be consistent with the original Shader. This allows us to use different Shaders for objects with different RenderTypes.

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

Note the difference between shaders for opaque and transparent objects: opaque objects are directly rendered as black, while transparent objects require blending. We need to extract the alpha channel from the object's texture and use it for blending. The code above only lists Opaque and Transparent shaders, but there are also TreeOpaque (which is the same as Opaque but with a different RenderType) and TreeTransparentCutout (same as Transparent) shaders, among others. Since we have specified the RenderType, in order to be comprehensive, we need to cover as many scenarios as possible where objects can occlude each other. In this case, I have only included the four types mentioned earlier. The results are roughly as follows:

![](assets/img/2014-3-30-unity-light-scattering/objectocclusion.png)

## Combine object occlusion to shade light source radiation.

Painting the radiation of the light source is not difficult, but it is important to make some adjustments based on the size of the screen, so that the radiation of the light source appears circular.

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

This Shader requires the input of the screen position of the light source (which can be calculated using `camera.WorldToViewportPoint`, resulting in UV coordinates). Then, it draws a circle with a specified radius that decays in brightness outwardly. The result is combined with the previously obtained object occlusion image (stored in `_MainTex`), resulting in something like this:

![](assets/img/2014-3-30-unity-light-scattering/light.png)

## Light Scattering processing, combined with real colors.

Here we will need to use the provided Pixel Shader in the book, my version being: [to_be_replace[x]]

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

Generally speaking, it is consistent with what is described in the book, but my parameters need to be passed in the program, and it is combined with real color images and light scattering images. As a result:

![](assets/img/2014-3-30-unity-light-scattering/effect.gif)

## Complete Code

The code is available [here](assets/img/2014-3-30-unity-light-scattering/2014-3-30-unity-light-scattering.zip). Add the `cs` script to the camera.

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
