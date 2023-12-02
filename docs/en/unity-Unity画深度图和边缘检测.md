---
layout: post
title: Unity draws depth maps and performs edge detection.
categories:
- unity
catalog: true
tags:
- dev
description: I discovered that Unity's RenderWithShader() and OnRenderImage() can
  be used to achieve many effects. Taking advantage of this learning opportunity,
  I have decided to use these two functions to generate a depth map of the scene and
  perform scene edge detection, which can be used as a mini-map in the game.
figures:
- assets/post_assets/2014-3-27-unity-depth-minimap/topview.png
---

<meta property="og:title" content="Unity画深度图(Depth Map)和边缘检测(Edge Detection)" />

Just got in touch with Unity not long ago, have always been interested in Unity's ShaderLab, feel like it can quickly achieve all kinds of display effects, very interesting. Well, as someone who hasn't even entered the door yet, I'll mess around with depth maps and edge detection then.

# Mini Map Settings

Because I have only made a rough draft, I do not intend to go into detail on how to draw a small map on the scene. In general, I have done the following things:

Translate these text into English language:

1. Get the bounding box of the scene, which is useful when setting camera parameters and position.
2. Configure the minimap camera as orthogonal projection, and set the camera's near and far planes based on the bounding box.
3. Add a character target to the camera, which will be displayed at the center of the map.
4. Update the camera position each time, based on the target's position and the maximum y value of the scene.

Specific configurations can be referred to the code provided later.

# Get Depth Map

## Use `depthTextureMode` to access the depth texture

The camera itself can save the DepthBuffer or a DepthNormalBuffer (which can be used for edge detection), just need to set `[to_be_replace]`.

```c#
Camera.depthTextureMode = DepthTextureMode.DepthNormals;
```

Then reference in the Shader.

```c#
sampler2D _CameraDepthNormalsTexture;
```

It's enough, you can refer to the code I provided later for specific instructions. Regarding the relationship between the depth value saved in the Z-Buffer and the real-world depth, you can refer to these two articles: [Learning to Love your Z-buffer](http://www.sjbaker.org/steve/omniv/love_your_z_buffer.html) and [Linearize depth](http://www.humus.name/temp/Linearize%20depth.txt). Additionally, Unity also provides some functions for depth calculation: `Linear01Depth`, `LinearEyeDepth`, etc.

This is not the main point I want to discuss here. What I want to say is that initially my camera was set to use orthogonal projection, and the depth should have been linear. However, when I tested it, I found that it was not linear. Then I tried using the method described in the link above to calculate the depth in real-world units, but it was always incorrect. I couldn't get the true linear depth, and I'm not sure if it's a problem with Unity's Z_Buffer or something else. If anyone knows, please teach me.

Of course, if you don't need the actual depth values and only need to compare depths, the method mentioned above is sufficient and quite simple. But for me, I want to map the real depth to color values, and I need to obtain the true linear depth values (although they are also in the range of [0, 1]). So, I had to resort to using another method, which is to use the RenderWithShader function.

## Use `RenderWithShader` to obtain depth map

This method is actually using an example from the Unity Reference: [Rendering with Replaced Shaders](http://docs.unity3d.com/Documentation/Components/SL-ShaderReplacement.html). It is important to understand that `RenderWithShader` will render the corresponding Mesh in the scene.

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

Add a script to your mini map camera (create it if it doesn't exist), configure the camera to use orthographic projection, and render the scene using this Shader in the `Update()` method.

```c#
camera.targetTexture = depthTexture;
camera.RenderWithShader(depthShader, "");
```

The result of rendering will be saved in the `depthTexture`, it's very simple.

## Map Depth to Color
To accomplish this task, the first step is to have a color map. This map can be easily generated using Matlab. For example, I have utilized the "jet" map inside Matlab.

<img src=../../assets/img/2014-3-27-unity-depth-minimap/jet.png width=200 />

Put this image into the project directory `Assets\Resources`, and you can read it in the program.

```c#
colorMap = Resources.Load<Texture2D>("colormap");
```

What needs to be noted is that the `Wrap Mode` of this image should be set to `Clamp` to prevent interpolation between color values at the edges.

Afterwards, you will need to use the `OnRenderImage` and `Graphics.Blit` functions. The function prototypes are:

```c#
void OnRenderImage(RenderTexture src, RenderTexture dst);
static void Blit(Texture source, RenderTexture dest, Material mat, int pass = -1);
```

The `src` parameter of this function is the result of camera rendering, while `dst` is the processed result to be passed back to the camera. Therefore, this function is usually used to apply various effects to the image after camera rendering, such as depth-color mapping and edge detection in our case. The approach is to call `Graphics.Blit` in `OnRenderImage` and pass in a specific `Material`:


```c#
depthEdgeMaterial.SetTexture("_DepthTex", src);
Graphics.Blit(src, dst, depthEdgeMaterial);
return;
```

It is worth noting that `Graphics.Blit` actually does the following: it draws a plane in front of the camera that is the same size as the screen, passes `src` as the `_MainTex` of this plane into the `Shader`, and then puts the result into `dst`, instead of redrawing the Meshes in the actual scene.

The color mapping is essentially mapping the depth [0, 1] to the UV of an image. Since I want the areas close to the camera to be red, I inverted the depth.

```glsl
half4 color = tex2D(_ColorMap, float2(saturate(1-depth), 0.5));
```

# Edge Detection
Edge detection requires the use of the camera's `_CameraDepthNormalsTexture`, primarily utilizing the values of normals, while depth utilizes the previously calculated values. In each pixel (x, y, z, w) of the `_CameraDepthNormalsTexture`, (x, y) represents the normals, while (z, w) represents the depth. The normals are stored using a specific method, which you can explore more deeply if interested.

The code refers to the edge detection in Unity's built-in Image Effect. What needs to be done is to compare the difference between the normal depth of the current pixel and its neighboring pixels. If the difference is large enough, we consider it as an edge.

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

The complete Shader is as follows:

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

# Blending Real-World Images

Adding color to a depth map alone can be a bit dull, so we can blend in colors from real-world scenes. To do this, we just need to create another shader and pass in the previous image as well as the camera's real-world image. Then, in the `OnRenderImage` function, we can blend the two images together.

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
The code above is responsible for completing this task. What needs to be understood is that when we call `RenderWithShader`, the function `OnRenderImage` will also be called. In other words, this function is called twice, and the functionality to be completed for each call is different. Therefore, I use a variable here to indicate the current rendering state, whether it is for creating a depth map or for blending.

# Complete code
The code files are a bit long, so I have placed them here: [depth-minimap](assets/img/2014-3-27-unity-depth-minimap/2014-3-27-unity-depth-minimap.zip).

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
