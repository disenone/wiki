---
layout: post
title: Unity에서 깊이 맵(Depth Map)과 가장자리 감지(Edge Detection)를 구현합니다.
categories:
- unity
catalog: true
tags:
- dev
description: Unity의 RenderWithShader()와 OnRenderImage() 함수를 활용하면 다양한 효과를 구현할 수 있다.
  학습 기회를 활용하여 이 두 함수를 이용해 장면 깊이 맵 및 장면 가장자리 감지를 구현하기로 결정했다. 이는 게임에서 사용될 수 있는 한 종류의
  작은 지도로 활용할 수 있다.
figures:
- assets/post_assets/2014-3-27-unity-depth-minimap/topview.png
---

<meta property="og:title" content="Unity画深度图(Depth Map)和边缘检测(Edge Detection)" />

Unity에 대해 최근에 접해 본 지 얼마 안 된 터라 ShaderLab에 항상 흥미를 느끼고 있습니다. 다양한 효과를 빠르게 구현할 수 있다는 느낌이 들어, 매우 흥미롭다고 생각해요. 그러니 입문자인 내가 깊이 맵과 가장자리 검출을 시도해 보겠습니다.

#작은 지도 설정

내가 그저 작은 초안을 만들었을 뿐이기 때문에 장면에 작은 지도를 그리는 방법을 자세히 설명할 계획은 없어. 대략적으로 내가 다음과 같은 몇 가지를 했어:

씬의 바운딩 박스를 얻어요. 카메라 매개변수와 위치를 설정할 때 유용해요.
작은 지도 카메라를 직교 투영으로 설정하여 바운딩 박스에 따라 카메라의 Near 및 Far 평면을 설정합니다.
이 카메라에 인물 대상을 추가하여 대상이 지도 중앙에 표시되도록 합니다.
카메라 위치를 갱신할 때마다 대상 위치와 장면의 최대 y 값에 따라 설정합니다.

구체적인 구성은 뒤에 제공된 코드를 참고하십시오.

#깊이 그림 획득

##深度텍스처 모드를 사용하여 깊이 이미지를 획득합니다.

카메라는 DepthBuffer 또는 DepthNormalBuffer(가장자리 감지에 사용)를 직접 저장할 수 있습니다. 설정만 하면 됩니다.

```c#
Camera.depthTextureMode = DepthTextureMode.DepthNormals;
```

차후에 Shader 안에서 호출

```c#
sampler2D _CameraDepthNormalsTexture;
```

당신은 한국어로 번역요청을 하셨군요. 여기 번역본이에요:

그대로 해 주시고, 구체적인 방법은 저가 제시한 코드를 참고하세요. Z-버퍼에 저장된 깊이 값과 실제 세계의 깊이와의 관계에 대해서는 이 두 문서를 참조해 주세요:
[Learning to Love your Z-buffer](http://www.sjbaker.org/steve/omniv/love_your_z_buffer.html),[Linearize depth](http://www.humus.name/temp/Linearize%20depth.txt)또한 Unity는 깊이를 계산하기 위한 몇 가지 함수도 제공합니다: `Linear01Depth`, `LinearEyeDepth` 등.

이 부분은 내가 토론하고 싶은 중점이 아니야. 내가 말하고 싶은 건, 내 카메라가 원래 정사영 투영으로 설정되어 있어서 깊이가 선형이어야 하는데, 하지만 내가 테스트해보니까 선형이 아니더라고. 그래서 위 링크에서 소개한 방법을 사용해서 실제 세계의 깊이를 계산해 보았지만, 계속해서 올바르지 않았어. 계속해서 실제 선형 깊이를 계산할 수 없어서, Unity의 Z_Buffer 문제인지 무엇인지 모르겠어. 이것에 대해 알고 있는 친구가 있으면 가르쳐 주십시오. 물론, 실제 깊이 값이 필요하지 않다면, 단지 깊이의 상대적 크기를 비교하는 것과 같은 경우, 위의 방법만으로도 충분하며 매우 간단해. 그러나 내 경우에는 실제 깊이를 색상 값으로 매핑하고 싶어서, 실제 선형 깊이 값을 얻어야 해([0, 1] 범위 내라도). 그래서 다른 RenderWithShader 방법을 사용하게 되었어.

##RenderWithShader를 사용하여 깊이 맵을 가져옵니다.

이 방법은 실제로 Unity 참조에 있는 한 예제를 사용하는 것입니다: [Rendering with Replaced Shaders](http://docs.unity3d.com/Documentation/Components/SL-ShaderReplacement.html)`. 이해해야 할 점은 'RenderWithShader'가 씬 내에서 해당 Mesh를 그려준다는 것입니다.`

샤더를 만드세요:

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

당신의 작은 미니맵 카메라에 (없다면 만들어주세요) 스크립트를 추가하여 카메라를 등각 투영 등으로 설정하고 `Update()`에서 이 셰이더를 사용하여 씬을 렌더링합니다:

```c#
camera.targetTexture = depthTexture;
camera.RenderWithShader(depthShader, "");
```

`depthTexture`에 렌더링 결과가 저장됩니다. 간단하죠?

##깊이를 색상으로 매핑합니다.
이 작업을 완료하려면 먼저 컬러 맵이 필요합니다. 이 그래프는 Matlab을 사용해서 쉽게 생성할 수 있는데, 예를 들면 전 Jet 그래프를 사용했습니다.

![](assets/img/2014-3-27-unity-depth-minimap/jet.png){ width="200" }

이 그림을 프로젝트 폴더 'Assets\Resources'에 넣으면 프로그램에서 읽을 수 있습니다.

```c#
colorMap = Resources.Load<Texture2D>("colormap");
```

주의해야 할 점은 이 그림의 `Wrap Mode`가 `Clamp`여야 하며, 양쪽 가장자리 색상 값 사이에서 보간이 발생하지 않도록해야 한다.

이후에는 `OnRenderImage` 및 `Graphics.Blit` 함수를 사용해야 합니다. 함수의 원형은 다음과 같습니다:

```c#
void OnRenderImage(RenderTexture src, RenderTexture dst);
static void Blit(Texture source, RenderTexture dest, Material mat, int pass = -1);
```

이 함수의 src는 카메라 렌더링 결과물이고, dst는 처리된 후 다시 카메라로 전달되는 결과물입니다. 따라서 이 함수는 보통 카메라 렌더링이 완료된 후 이미지에 몇 가지 효과를 적용하기 위해 사용됩니다. 예를 들어, 여기서는 깊이에 대한 색상 매핑 및 가장자리 감지 등이 있습니다. `OnRenderImage`에서 `Graphics.Blit`을 호출하고 특정 `Material`을 전달하는 방식입니다.

```c#
depthEdgeMaterial.SetTexture("_DepthTex", src);
Graphics.Blit(src, dst, depthEdgeMaterial);
return;
```

주의해야 할 점은 `Graphics.Blit`이 사실 이렇게 동작한다는 것입니다: 카메라 앞에 화면과 같은 크기의 평면을 그리고, `src`를 이 평면의 `_MainTex`로 쉐이더에 전달하고, 결과를 `dst`에 넣는다는 것입니다. 실제 장면의 메쉬를 다시 그리는 것이 아니라는 것이죠.

색상 매핑에 대해서 실제로는 깊이 [0, 1]를 이미지의 UV로 간주하는 것이며, 카메라와의 거리가 가까운 부분을 빨간색으로 만들기 위해 깊이를 반전시켰습니다:

```glsl
half4 color = tex2D(_ColorMap, float2(saturate(1-depth), 0.5));
```

#가장자리 감지
모서리 감지에는 카메라의 `_CameraDepthNormalsTexture`가 필요합니다. 이것은 주로 Normal 값에 사용되며, 깊이는 이전에 계산한 값이 사용됩니다. `_CameraDepthNormalsTexture`의 각 픽셀 (x, y, z, w)에서 (x, y)는 법선을 나타내고, (z, w)는 깊이를 나타냅니다. 법선은 특정 방법으로 저장되었으며, 관심이 있다면 직접 검색해보세요.

코드는 Unity의 내장 이미지 효과 중 가장자리 감지를 참고합니다. 해야 할 일은 현재 픽셀의 법선 깊이와 인접 픽셀의 차이를 비교하는 것입니다. 충분히 크다면 가장자리가 있다고 간주합니다:

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

다음은 완전한 Shader입니다:

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

이 내용을 한국어로 번역해주세요:


![](assets/img/2014-3-27-unity-depth-minimap/topview.png){ width="200" }

#혼합 현실 세계 이미지
깊이 색상 그림 하나만으로는 다소 지루할 수 있습니다. 실제 장면의 색상 그림을 섞어 볼까요? 이를 위해 새로운 셰이더를 작성하여 앞서 언급한 그림과 카메라의 실제 그림을 혼합하는 방법이 있습니다. 그때 `OnRenderImage`에서 혼합 작업을 수행하면 됩니다.

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
위의 코드는이 작업을 수행하는 데 사용됩니다. 이해해야 할 점은 'RenderWithShader'를 호출할 때 'OnRenderImage'도 호출된다는 것입니다. 즉, 이 함수가 두 번 호출된다는 것이고, 두 번의 호출에서 수행해야 할 기능은 다릅니다. 그래서 여기서는 현재 렌더링 상태가 깊이 맵을 만들어야 하는지 블렌딩을 해야 하는지를 나타내는 변수를 사용했습니다.

#완전한 코드
소스 코드 파일이 좀 많아서 여기에 놔두겠습니다 [depth-minimap](assets/img/2014-3-27-unity-depth-minimap/2014-3-27-unity-depth-minimap.zip)"。" --> "。"

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT를 사용하여 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)모든 누락된 부분을 찾아내세요. 
