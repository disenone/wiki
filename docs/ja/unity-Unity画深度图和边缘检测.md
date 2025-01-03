---
layout: post
title: Unity が深度マップ(Depth Map)とエッジ検出(Edge Detection)を行います。
categories:
- unity
catalog: true
tags:
- dev
description: UnityのRenderWithShader()およびOnRenderImage()を使用してさまざまな効果を実現できることがわかりました。学習の機会を活かして、これらの関数を使用してシーンの深度マップの生成とシーンのエッジ検出を実装することに決めました。これはゲームの一種のミニマップとして使用できます。
figures:
- assets/post_assets/2014-3-27-unity-depth-minimap/topview.png
---

<meta property="og:title" content="Unity画深度图(Depth Map)和边缘检测(Edge Detection)" />

Unityに触れたばかりで、ShaderLabに興味を持ってます。いろいろな表示効果を素早く実現できる感じがして、面白いですね。まあ、まだ初心者なので、深度マップとエッジ検出を試してみますかね。

#地図設定

私はまだプロトタイプしか作成していませんので、シーンに小さなマップを描く方法について詳細に説明するつもりはありません。おおまかに言うと、以下のことを行いました：

シーンのバウンディングボックスを取得して、カメラのパラメータや位置を設定する際に役立ちます。
小さな地図カメラを正射投影に設定し、境界ボックスに基づいてカメラの近および遠平面を設定します。
このテキストを日本語に翻訳してください：「地図の中心に人物のターゲットを追加する」
カメラの位置を更新するたびに、ターゲットの位置とシーンの最大 y 値に基づいてください。

具体な配置については、後述のコードを参照してください。

#深度マップを取得する

##depthTextureMode を使用してデプステクスチャを取得します。

カメラは、DepthBufferまたはDepthNormalBuffer（エッジ検出に使用できる）を保存できます。ただし、設定が必要です。

```c#
Camera.depthTextureMode = DepthTextureMode.DepthNormals;
```

シェーダー内でこれを参照します。

```c#
sampler2D _CameraDepthNormalsTexture;
```

これで結構です、具体的な手法は私が後で提供するコードを参考にしてください。Z-Bufferに保存されている深度値と実世界の深度の関係については、以下の2つの記事を参考にしてください：
[Learning to Love your Z-buffer](http://www.sjbaker.org/steve/omniv/love_your_z_buffer.html),[Linearize depth](http://www.humus.name/temp/Linearize%20depth.txt)Unity also provides some functions for calculating depth such as `Linear01Depth`, `LinearEyeDepth`, and so on.

ここで議論されているのは私の重点ではありませんが、言いたいことは、元々私のカメラは直交投影に設定されており、深度は線形であるはずですが、テストしてみると線形ではないことがわかりました。そして、上記リンクで紹介された方法を使って実世界の深度を計算しようとしましたが、これまで正確な結果が得られず、実際の線形深度を計算できませんでした。UnityのZ_Bufferの問題なのかどうか、知っている方がいれば教えていただきたいと思います。もちろん、実際の深度値が必要ない場合や、単に深度の比較などが必要な場合は、上記の方法で十分であり、かつ簡単です。しかし、私の場合、実際の深度を色値にマップしたいため、実際の線形深度値を取得する必要があります（[0, 1]の範囲内でも）。したがって、RenderWithShaderメソッドを使用するほかに方法はないようです。

##RenderWithShaderを使って深度マップを取得します。

この方法は実際にはUnityのリファレンス内にある例を使っています：[Rendering with Replaced Shaders](http://docs.unity3d.com/Documentation/Components/SL-ShaderReplacement.html)理解に値することは、`RenderWithShader`はシーン中の対応するメッシュを描画することです。

シェーダーを作成する：

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

あなたのミニマップカメラ（ない場合は作成）にスクリプトを追加し、カメラを平行投影などに設定し、`Update()`内でこのシェーダーを使用してシーンをレンダリングします：

```c#
camera.targetTexture = depthTexture;
camera.RenderWithShader(depthShader, "");
```

「溢れる結果は`depthTexture`に保存されます。簡単でしょう。」

##深度を色にマッピングします。
この仕事を完成するには、まず色付きの図が必要です。この図はMatlabで簡単に生成できます。例えば、私が使用しているのはMatlab内の「jet」図です。

![](assets/img/2014-3-27-unity-depth-minimap/jet.png){ width="200" }

この画像を`Assets\Resources`フォルダに配置すれば、プログラム内で読み込むことができます。

```c#
colorMap = Resources.Load<Texture2D>("colormap");
```

この画像の `Wrap Mode` は `Clamp` にする必要があります。両側の色の間で補間が行われないようにするためです。

その後は、`OnRenderImage` と `Graphics.Blit` 関数を使用する必要があります。 関数のプロトタイプは次の通りです：

```c#
void OnRenderImage(RenderTexture src, RenderTexture dst);
static void Blit(Texture source, RenderTexture dest, Material mat, int pass = -1);
```

この関数の src はカメラのレンダリング結果で、dst は処理後にカメラに戻す結果です。したがって、通常、この関数はカメラのレンダリングが完了した後に画像効果を加えるために使用されます。例えば、深度に対するカラーマッピングやエッジ検出などです。具体的な手順は、`OnRenderImage` 内で `Graphics.Blit` を呼び出し、特定の `Material` を渡すことです。

```c#
depthEdgeMaterial.SetTexture("_DepthTex", src);
Graphics.Blit(src, dst, depthEdgeMaterial);
return;
```

重要な点は、`Graphics.Blit`が実際に行っていることです。つまり、カメラの前に画面と同じサイズの平面を描き、`src`をこの平面の`_MainTex`に渡し、結果を`dst`に配置することです。実際のシーン中のメッシュを再描画するのではないことにご注意ください。

色のマッピングに関しては、基本的に深度 [0, 1] を画像のuvと見なしています。カメラに近いほど赤色にしたいので、深度を反転させています。

```glsl
half4 color = tex2D(_ColorMap, float2(saturate(1-depth), 0.5));
```

#エッジ検出
エッジ検出には、カメラの `_CameraDepthNormalsTexture` が必要で、主に法線値を使用しており、深度は以前に計算したものを使用しています。 `_CameraDepthNormalsTexture` の各ピクセル (x, y, z, w) では、(x, y) が法線を表し、(z, w) が深度を表します。法線は特定の方法で格納されており、興味があれば自分で検索してみてください。

このコードは、Unityに組み込まれているImage Effectのエッジ検出を参考にしています。現在のピクセルの法線深度と周囲のピクセルとの差を比較し、その差が十分大きい場合にエッジが存在するとみなします。

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

このテキストを日本語に翻訳してください：

![](assets/img/2014-3-27-unity-depth-minimap/topview.png){ width="200" }

#融合された現実世界画像
深い色のグラフだけだとちょっとつまらないかもしれませんね。そんな時は実際のシーンのカラーグラフと混ぜてみるのはどうでしょう。新しいシェーダを作成して、前述のグラフとカメラの実際の画像を渡し、`OnRenderImage` 内で混ぜ合わせます。

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
上記のコードはこのタスクを完了するために使われています。覚えておくべき点は、`RenderWithShader` を呼び出す際に、`OnRenderImage` も呼び出されることです。つまり、この関数が2回呼び出されることになりますが、両方の呼び出しで行われる処理は異なります。そのため、現在のレンダリング状態が深度マップを作成しているのか、ブレンド処理を行っているのかを示すために、変数を使用しています。

#完整なコード
コードファイルが少し多いので、ここに入れておきます[depth-minimap](assets/img/2014-3-27-unity-depth-minimap/2014-3-27-unity-depth-minimap.zip)I'm sorry, but the text provided is already in Japanese. Can I assist you with anything else?

--8<-- "footer_ja.md"


> この投稿はChatGPTによって翻訳されましたので、[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)Please point out any omissions. 
