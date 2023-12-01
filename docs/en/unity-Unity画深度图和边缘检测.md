---
layout: post
title: Unity can create depth maps and perform edge detection.
categories:
- unity
catalog: true
tags:
- dev
description: I discovered that Unity's RenderWithShader() and OnRenderImage() can
  be used to achieve many effects. Taking advantage of this learning opportunity,
  I have decided to use these two functions to generate a depth map of the scene and
  perform edge detection, which can be used as a mini-map in the game.
figures:
- assets/post_assets/2014-3-27-unity-depth-minimap/topview.png
---


Just recently started working with Unity, and have been very interested in ShaderLab. I feel like it allows for quickly achieving various visual effects, which is quite intriguing. Well, as someone who is still new to this field, I'll give a try to working with depth maps and edge detection.

# Mini Map Settings

Because I have only created a rough prototype, I do not intend to explain in detail how to draw a small map on the scene. In general, I have done the following things:

1. Get the bounding box of the scene, which is useful for setting the parameters and position of the camera.
2. Configure the mini-map camera with an orthogonal projection, based on the bounding box, set the near and far planes of the camera.
3. Add a character target to this camera, the target will be displayed at the center of the map.
4. Update the position of the camera each time, based on the position of the target and the maximum y value of the scene.

The specific configuration can be referred to the code provided later.

# Get Depth Map

## Use `depthTextureMode` to obtain the depth map.

The camera can save the DepthBuffer or a DepthNormalBuffer itself (which can be used for edge detection), just need to set [to_be_replace]

```c#
Camera.depthTextureMode = DepthTextureMode.DepthNormals;
```

Then reference it in the shader.

```c#
sampler2D _CameraDepthNormalsTexture;
```

That's it, you can refer to the code I provided later for the specific procedure. For the relationship between the depth value saved in the Z-Buffer and the real-world depth, you can refer to these two articles: [Learning to Love your Z-buffer](http://www.sjbaker.org/steve/omniv/love_your_z_buffer.html), [Linearize depth](http://www.humus.name/temp/Linearize%20depth.txt). In addition, Unity also provides some functions for calculating depth, such as `Linear01Depth`, `LinearEyeDepth`, etc.

This is not the focus of our discussion here. What I want to say is that my camera was originally set to use orthographic projection and the depth should be linear. However, when I tested it, it turned out to be non-linear. Then I tried using the method mentioned in the above link to calculate the real world depth, but it has always been incorrect. I couldn't calculate the true linear depth, and I don't know if it's a problem with Unity's Z_Buffer or something else. If any of you know, please teach me. Of course, if you don't need the real depth value and only need to compare depth, the method mentioned above is sufficient and very simple. However, for my case, I want to map the real depth to color values and I need to obtain the true linear depth value (even though it's still in the range [0,1]), so I had to use another method called RenderWithShader.

## Use RenderWithShader to get depth maps

This method is actually using an example from Unity Reference: [Rendering with Replaced Shaders](http://docs.unity3d.com/Documentation/Components/SL-ShaderReplacement.html). What needs to be understood is that `RenderWithShader` will draw the corresponding Mesh in the scene.

Create a Shader:

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

Add a script to your minimap camera (if it doesn't exist) to configure the camera as orthographic projection etc., and use this Shader to render the scene in `Update()` function.

```c#
camera.targetTexture = depthTexture;
camera.RenderWithShader(depthShader, "");
```

The rendering result will be saved inside `depthTexture`, it's quite simple, right?

## Mapping depth to color

To accomplish this task, you first need a color map. This map can be easily generated using Matlab. For example, I used the jet colormap in Matlab for this purpose.

<img src=../../assets/img/2014-3-27-unity-depth-minimap/jet.png width=200 />

Put this image in the project directory `Assets\Resources`, so it can be read in the program:

```c#
colorMap = Resources.Load<Texture2D>("colormap");
```

It should be noted that the `Wrap Mode` of this image should be set to `Clamp` to prevent interpolation between color values at the edges.

Afterwards, you will need to use `OnRenderImage` and `Graphics.Blit` functions, the function prototypes are:

```c#
void OnRenderImage(RenderTexture src, RenderTexture dst);
static void Blit(Texture source, RenderTexture dest, Material mat, int pass = -1);
```

The `src` of this function is the result of camera rendering, while the `dst` is the result that will be passed back to the camera after processing. Therefore, this function is usually used to apply some effects to the image after camera rendering, such as depth color mapping and edge detection. The approach is to call `Graphics.Blit` in the `OnRenderImage` function and pass in a specific `Material`.

```c#
depthEdgeMaterial.SetTexture("_DepthTex", src);
Graphics.Blit(src, dst, depthEdgeMaterial);
return;
```

It is important to note that `Graphics.Blit` actually does the following: it draws a plane in front of the camera that is the same size as the screen, passes `src` as the `_MainTex` of this plane into the `Shader`, and then puts the result into `dst`, instead of redrawing the actual Mesh in the scene.

Mapping colors is actually treating the depth [0, 1] as the uv of an image. Because I want the areas closer to the camera to be red, I inverted the depth.

```glsl
half4 color = tex2D(_ColorMap, float2(saturate(1-depth), 0.5));
```

# Edge Detection
Edge detection requires the use of the camera's `_CameraDepthNormalsTexture`, mainly for the values of the normals. The depth value is still obtained from the previous calculation. In each pixel (x, y, z, w) of the `_CameraDepthNormalsTexture`, (x, y) represents the normals, while (z, w) represents the depth. The normals are stored using a specific method, which you can search for if interested.

The code is referenced from the built-in Image Effect of Unity for edge detection. The task is to compare the difference between the current pixel's normal depth and nearby pixels. If the difference is significant enough, we consider an edge to be present.

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

The complete shader is as follows:

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

The result is similar to this:

<img src=../../assets/img/2014-3-27-unity-depth-minimap/topview.png width=200 />

# Mixed Real World Images
Just having a color map of depth alone may be a bit dull, so we can mix in the color map from a real scene. We just need to create another shader, pass in the previous image and the real image from the camera, and blend them in the `OnRenderImage` function.

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
The code above is responsible for completing this task. What needs to be understood is that when we call `RenderWithShader`, `OnRenderImage` will also be called. In other words, this function is called twice, but each call has a different functionality to perform. Therefore, I use a variable to indicate whether the current rendering state is for depth mapping or blending.

# Complete Code
The code files are a bit extensive, so I'm just going to place them here [depth-minimap](assets/img/2014-3-27-unity-depth-minimap/2014-3-27-unity-depth-minimap.zip).

> Original: <https://disenone.github.io/wiki>  
> This post is protected by [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by/4.0/deed.en) agreement, should be reproduced with attribution.


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
