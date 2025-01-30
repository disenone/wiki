---
layout: post
title: Unity におけるボリューメトリック ライト スキャッタリング（Volumetric Light Scattering、クラウド シャドウ）の実装
categories:
- unity
catalog: true
tags:
- dev
description: 体積光散乱はかなり素敵な視覚効果です。まるで空中で光線が広がっているのが見えるようで、空中の微粒子が光で照らされ、一部の光が遮られると、視覚的に光源から放射された光線が生じます。
figures:
- assets/post_assets/2014-3-30-unity-light-scattering/effect.gif
---

<meta property="og:title" content="Unity实现体积光照散射 (Volumetric Light Scattering，云隙光)" />

##原理

(http://http.developer.nvidia.com/GPUGems3/gpugems3_ch13.html)書籍には有効な図があります：

![](assets/img/2014-3-30-unity-light-scattering/goodeffect.png)

見た目が良いでしょう、それなら、私たちの目標はこのような効果を実現することです。

書籍では原理について説明されており、重要な公式の一つは次の通りです：

\\[ L(s, \theta, \phi) = exposure \times \sum\_{i=0}^n decay^i \times weight \times \frac{L( s\_i, \theta\_i )}{n} \\]

私の理解では、画像上の各ピクセルに対して、光が当たる可能性があります。そのため、そのピクセルから光源（画像上の位置への投影）への直線をサンプリング（式上の\\(i\\)に対応）し、サンプリングされた結果を重み付け平均（式上の\\(\sum\\)に対応）して、そのピクセルの新しい色値とします。また、重要な後処理ピクセルシェーダーもありますが、そのシェーダーだけでカメラがレンダリングした結果を処理すると、明らかな人工的な痕跡が生じ、多くのストライプが現れます。

![](assets/img/2014-3-30-unity-light-scattering/badeffect.png)

その効果は本でどのように作られていますか？実際、本には答えが既に示されており、一連の図を使用して説明できます：

![](assets/img/2014-3-30-unity-light-scattering/steps.png)

图aは荒っぽい効果ですね、じっくり見るとたくさんのしわがあります、そして隠れていないので本物っぽいですね、b、c、dは良い効果を得るために必要なステップです。

b. ライトの放射効果を画像にレンダリングし、物体の遮蔽を追加する

bにVolumetric Light Scatteringのピクセルシェーダを適用して、遮蔽された効果を得る

d. 実際のシーンの色を追加する

では、次に私たちは一歩ずつ実現していきましょう。

##物体を隠す。

実際の操作では、まず`RenderWithShader`を使用して、隠れる物体を黒色に描画し、他の場所を白色にしています。各面をレンダリングする必要があるため、複雑なシーンでは一定のパフォーマンスコストがかかります。シーン内の物体には不透明と透明があり、不透明な物体は完全な光線遮蔽を生成し、透明な物体は部分的な遮蔽を生成することを望んでいます。したがって、異なるRenderTypeの物体に対して異なるShaderを書く必要があります。RenderTypeはSubShaderのタグです。分からない場合は[こちら](http://docs.unity3d.com/Documentation/Components/SL-SubshaderTags.html)，書き終えたら呼び出します：

```c#
camera.RenderWithShader(objectOcclusionShader, "RenderType");

```
`RenderWithShader`の第二引数は、RenderTypeに基づいてShaderを置き換えることを要求します。簡単に言うと、同じオブジェクトの置き換え後のShaderのRenderTypeは、置き換え前と一致する必要があります。これにより、異なるRenderTypeのオブジェクトに異なるShaderを使用することができます。

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

不透明と透明オブジェクトのシェーダーの違いに注意してください：不透明なオブジェクトは直接黒色で描画されます。不透明な物体にはblendingが必要で、オブジェクトのテクスチャのアルファチャンネルを取得し、そのアルファに基づいてblendingを行います。上記のコードはOpaqueとTransparentを示していますが、TreeOpaque（RenderTypeを変更するだけでOpaqueと同じ）やTreeTransparentCutout（Transparentと同じ）などもあります。RenderTypeが指定されているため、全体を考慮するためには、シーンでオクルージョンが発生する可能性のあるオブジェクトをできるだけ網羅する必要があります。ここでは、前述の4種類のみを扱います。結果はおおよそ以下のようになります：

![](assets/img/2014-3-30-unity-light-scattering/objectocclusion.png)

##物体が光源の放射線を遮る場合、それを塗ることを意味します。

画光源的辐射并不困难，需要注意的是根据屏幕的尺寸进行一些调整，确保光源的辐射呈圆形状。

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

このシェーダーは、画面上の光源の位置（`camera.WorldToViewportPoint`を使用して計算できるUV座標）を入力する必要があります。そして指定された半径で外側に向かって輝度が減衰する円を描画し、その結果を先に得られたオブジェクトの遮蔽イメージ（`_MainTex`に配置）と組み合わせます。結果はおおよそ以下のようになります：

![](assets/img/2014-3-30-unity-light-scattering/light.png)

##光散乱処理と実際の色の組み合わせ

ここでは、本に提供されているPixel Shaderを使用します。私のバージョン：

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

大体的に書籍と一致していますが、私のパラメータはプログラム内で渡す必要があります。また、実際のカラー画像と光散乱画像を組み合わせた結果：

![](assets/img/2014-3-30-unity-light-scattering/effect.gif)

##完整なコード

[ここ](assets/img/2014-3-30-unity-light-scattering/2014-3-30-unity-light-scattering.zip)カメラに`cs`スクリプトを追加します。

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されました。[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)どの箇所でも見落としを指摘してください。 
