---
layout: post
title: Unity におけるボリューメトリック・ライト・スキャッタリング（Volumetric Light Scattering、雲隙光）の実装
categories:
- unity
catalog: true
tags:
- dev
description: 体積光散乱はなかなか素敵な視覚効果だね、まるで光が空中で伝播するのを見ているようだ。空中の微粒子が光で照らされ、一部の光は遮られる中、視覚的には光源から放射される光線が生じる。
figures:
- assets/post_assets/2014-3-30-unity-light-scattering/effect.gif
---

<meta property="og:title" content="Unity实现体积光照散射 (Volumetric Light Scattering，云隙光)" />

##原理

(http://http.developer.nvidia.com/GPUGems3/gpugems3_ch13.html)書に有効な図表が載っている場合：

![](assets/img/2014-3-30-unity-light-scattering/goodeffect.png)

見た目いいね、了解した、私たちの目標はこの効果を実現することだ。

書には原理が説明され、重要な一つの式が次のようになっています：

\\[ L(s, \theta, \phi) = exposure \times \sum\_{i=0}^n decay^i \times weight \times \frac{L( s\_i, \theta\_i )}{n} \\]

私の理解では、画像の各ピクセルには光が当たる可能性があります。したがって、そのピクセルから光源に向かう直線（画像に投影される位置で）をサンプリング（対応する数式では\\(i\\)）し、サンプリング結果を重み付け平均化（数式では\\(\sum\\)）し、それを新しい色値として使用します。さらに、重要なのはポストピクセルシェーダーですが、カメラのレンダリング結果を処理するためにそのシェーダーだけを使用すると、人工的な痕跡が明らかに現れ、ストライプが多数発生します。

![](assets/img/2014-3-30-unity-light-scattering/badeffect.png)

その場合、書籍の効果はどのように作られるのか？実際には、書籍は既に答えを提供しており、一連の図を用いて説明できます：

![](assets/img/2014-3-30-unity-light-scattering/steps.png)

図aは粗い効果です。注意深く見ると多くの筋が見え、十分にリアルでない遮蔽がないことがわかります。b、c、dが良い効果を得るために必要な手順です。

画像に照明の放射効果をレンダリングし、オブジェクトの遮蔽を追加します。

bを持っているVolumetric Light Scatteringピクセルシェーダーをcに適用して、隠蔽された効果を得ます。

d. 真実のシーンの色を追加

それでは、次は一歩ずつ実現していきましょう。

##物体を覆う絵や障害物

実際の操作では、まず`RenderWithShader`を使用して、遮蔽が発生するオブジェクトを黒く描画し、他の部分を白くします。各面をレンダリングする必要があるため、複雑なシーンではパフォーマンスに影響を与える可能性があります。シーンには不透明と透明なオブジェクトがあり、不透明なオブジェクトは完全な光の遮蔽を生成することを望み、透明なオブジェクトは部分的な遮蔽を生成する必要があります。そのため、異なるRenderTypeのオブジェクトには異なるShaderを書く必要があります。RenderTypeはSubShaderのタグです。詳細は[こちら](http://docs.unity3d.com/Documentation/Components/SL-SubshaderTags.html)，文章を書いた後には、次のように呼び出します：

```c#
camera.RenderWithShader(objectOcclusionShader, "RenderType");

```
`RenderWithShader`関数の第二引数は、RenderTypeに基づいてShaderを置換するように求められます。要するに、同じオブジェクトの置換されるShaderのRenderTypeは置換前と一致している必要があります。これにより、異なるRenderTypeのオブジェクトに異なるShaderを使用することができます。

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

不透明と透明の物体のシェーダーの違いに注意してください：不透明の物体は直接黒で描画されます。不透明の物体はブレンディングを実行し、物体のテクスチャ上のアルファチャンネルを取得し、そのアルファに基づいてブレンディングを行う必要があります。上記のコードは単に不透明と透明を挙げたものであり、Opaqueとは異なってTreeOpaque（Opaqueと同じShaderだけどRenderTypeが変えられたもの）、TreeTransparentCutout（Transparentと同じ）などもあります。RenderTypeを指定したため、できるだけシーン内で隠蔽が起こる物体を広く網羅する必要がありますが、ここには前述の4種類しかないです。結果はおおよそ以下のようになります：

![](assets/img/2014-3-30-unity-light-scattering/objectocclusion.png)

##物体が光源の放射を遮ることを考慮に入れる

光源の放射を描くことは難しくありません。注意が必要なのは、画面のサイズに合わせて適切な処理を行い、光源の放射が円形であるようにします。

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

このシェーダーは、画面上のライトの位置を入力する必要があります（`camera.WorldToViewportPoint`を使用して計算でき、UV座標が得られます）。その後、指定された半径で外側に輝度が減衰する円を描画し、その結果を前述のオブジェクトの遮蔽画像（`_MainTex`に配置）と組み合わせます。結果はおおよそ次の通りです：

![](assets/img/2014-3-30-unity-light-scattering/light.png)

##光散乱処理を行い、実際の色と組み合わせます。

ここでは、書籍で提供されているピクセルシェーダーを使用する必要があります。私のバージョン：

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

基本的に、本に書かれている内容と一致していますが、私のパラメータはプログラム内で渡す必要があり、実際のカラーマップと光の散乱図を組み合わせました。結果は以下の通りです：

![](assets/img/2014-3-30-unity-light-scattering/effect.gif)

##完整なコード

「コードは[ここ](assets/img/2014-3-30-unity-light-scattering/2014-3-30-unity-light-scattering.zip)，`cs`スクリプトをカメラに追加します。

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されました。[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指で油断なく抜け漏れを見つけ出す。 
