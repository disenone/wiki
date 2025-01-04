---
layout: post
title: Unity畫深度圖（Depth Map）和邊緣檢測（Edge Detection）
categories:
- unity
catalog: true
tags:
- dev
description: 發現Unity的RenderWithShader()和OnRenderImage()可以用來實現很多效果，趁著學習的機會，我決定用這兩個函數實現場景深度圖的生成和場景邊緣檢測，可用來作為遊戲的一種小地圖。
figures:
- assets/post_assets/2014-3-27-unity-depth-minimap/topview.png
---

<meta property="og:title" content="Unity画深度图(Depth Map)和边缘检测(Edge Detection)" />

剛接觸Unity沒多久，對Unity的ShaderLab一直很感興趣，感覺它可以快速地實現各種各樣的顯示效果，很有意思。嘛，作為一個門都還沒入的人，我就來搞一搞深度圖和邊緣檢測吧。

#小地圖設置

由於我僅僅完成了一個初步版本，因此我不打算詳細說明如何在場景中繪製小地圖，總括來說，我完成了以下一些工作：

獲取場景的 bounding box，這在設定相機的參數和位置時很有用。
將小地圖相機配置成正交投影，根據bounding box 設定相機的近平面和遠平面。
為該相機新增一個人物目標，目標會顯示在地圖的中心。
每次更新相機位置時，根據目標位置和場景的最大 y 值。

詳細的配置請參考後面提供的程式碼。

#獲取深度圖

##使用 depthTextureMode 可以取得深度圖。

相機可以自行保存深度緩衝區或深度法向量緩衝區（可用於邊緣檢測），只需設置。

```c#
Camera.depthTextureMode = DepthTextureMode.DepthNormals;
```

然後在Shader裡面引用

```c#
sampler2D _CameraDepthNormalsTexture;
```

只需要這樣做，具體的方法可以參考我後面提供的程式碼。有關在Z緩衝區中保存的深度值和真實世界深度的關係，可以參考這兩篇文章：
[Learning to Love your Z-buffer](http://www.sjbaker.org/steve/omniv/love_your_z_buffer.html),[Linearize depth](http://www.humus.name/temp/Linearize%20depth.txt)Unity也提供了一些函數來計算深度: `Linear01Depth`, `LinearEyeDepth` 等。

這不是我這裡討論的重點，我想說的是，本來我的相機設定為正交投影，深度應該是線性的，但我測試出來卻不是線性。然後我用上面連結介紹的方法來計算真實世界的深度，也一直都不正確，以至於一直計算不出真實的線性深度，不知道是Unity的Z_Buffer的問題還是什麼，那位朋友知道的請教教我。當然，如果不需要真實的深度值，單單是比較深度的大小之類的，用上面的方法就足夠了，而且很簡單。但對於我這裡來說，我想要將真實深度映射為顏色值，需要獲得真實的線性的深度值（儘管也是[0, 1]），我只好用另外一種用RenderWithShader 方法了。

##使用 RenderWithShader 來獲取深度圖。

這種方法其實就是使用 Unity Reference 裡面的一個例子：[Rendering with Replaced Shaders](http://docs.unity3d.com/Documentation/Components/SL-ShaderReplacement.html)需要理解的是，`RenderWithShader`會把場景中的相應的Mesh畫一遍。

建立一個 Shader：

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

為您的小地圖相機（若無，則建立之）添加一個腳本，將相機配置為正交投影等，然後在 `Update()` 函式中使用此 Shader 來渲染場景：

```c#
camera.targetTexture = depthTexture;
camera.RenderWithShader(depthShader, "");
```

渲染的結果會儲存在`depthTexture`中，十分簡單吧。

##將深度映射為顏色。
完成這項任務，首要就是要有一張彩色圖，這張圖可以很輕鬆地在 Matlab 中生成，比如我使用的是 Matlab 內置的 jet 圖：

![](assets/img/2014-3-27-unity-depth-minimap/jet.png){ width="200" }

將這張圖片放入專案目錄`Assets\Resources`中，就可以在程式中讀取：

```c#
colorMap = Resources.Load<Texture2D>("colormap");
```

需要注意的是，這張圖片的 `Wrap Mode` 應該是 `Clamp`，防止在兩邊緣的顏色值之間進行插值。

接下來, 您需要使用 `OnRenderImage` 和 `Graphics.Blit` 函式，函式的原型如下：

```c#
void OnRenderImage(RenderTexture src, RenderTexture dst);
static void Blit(Texture source, RenderTexture dest, Material mat, int pass = -1);
```

這個函數的 src 是相機渲染的結果，dst 是處理後傳回給相機的結果，因此這個函數通常用來在相機渲染完成後做圖片的一些效果，例如對深度做顏色映射，還有邊緣檢測。做法就是在`OnRenderImage`中呼叫`Graphics.Blit`，傳入特定的`Material`：

```c#
depthEdgeMaterial.SetTexture("_DepthTex", src);
Graphics.Blit(src, dst, depthEdgeMaterial);
return;
```

需要注意的是，`Graphics.Blit`實際上所做的是：在相機前方繪製一個和螢幕大小相同的平面，將`src`作為此平面的`_MainTex`傳入`Shader`中，然後將結果放入`dst`中，而不是重新繪製實際場景中的Mesh。

對顏色映射其實就是將深度 [0, 1] 視為圖像的 UV，因為我想距離相機近的部分顯示為紅色，所以我對深度取了反：

```glsl
half4 color = tex2D(_ColorMap, float2(saturate(1-depth), 0.5));
```

#邊緣檢測
邊緣檢測需要使用相機自己的 `_CameraDepthNormalsTexture`，主要是用 Normal 的值，深度則使用之前計算出來的。在 `_CameraDepthNormalsTexture` 的每個像素 (x, y, z, w) 中，(x, y) 是法向，(z, w) 是深度，法向是使用了一種方法來存放的，有興趣可以自己搜尋。

程式碼是參考了 Unity 自帶的 Image Effect 裡面的邊緣檢測，需要做的事情就是，比較當前像素的法向深度和鄰近像素的差異，足夠大我們就認為存在邊緣：

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

以下是完整的着色器：

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

類似於這個：

![](assets/img/2014-3-27-unity-depth-minimap/topview.png){ width="200" }

#融合現實世界影像
單單是深度的顏色圖可能有點無趣，那麼我們可以混合真實場景的顏色圖，只需要再建立一個Shader，傳入前面的影像和相機的真實影像，在 `OnRenderImage` 中進行混合：

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
上述程式碼就是完成這個任務所需的，需要理解的是，在呼叫 `RenderWithShader` 時，也會觸發 `OnRenderImage`，換句話說，這個函數會被呼叫兩次，而兩次呼叫所需執行的功能是不同的，因此我在這裡使用一個變數來指示當前的渲染狀態是製作深度圖還是混合。

#完整的程式碼
程式檔案有點多，就放到這裡了 [depth-minimap](assets/img/2014-3-27-unity-depth-minimap/2014-3-27-unity-depth-minimap.zip)。

--8<-- "footer_tc.md"


> 此篇文字是由 ChatGPT 翻譯的，如果有任何[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
