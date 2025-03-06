---
layout: post
title: Unity에서 부피 광 성산 (Volumetric Light Scattering, 클라우드 간격 광)을 구현합니다.
categories:
- unity
catalog: true
tags:
- dev
description: 체적 광산산은 꽤 괜찮은 시각 효과야. 마치 공기 속에서 빛이 번지는 것을 보는 것 같아. 공기 중의 미립자들이 빛을 비추고
  있는데, 일부 빛은 가려져서 시각적으로는 광원에서 방사되는 빛이 생겨나.
figures:
- assets/post_assets/2014-3-30-unity-light-scattering/effect.gif
---

<meta property="og:title" content="Unity实现体积光照散射 (Volumetric Light Scattering，云隙光)" />

##원리

부피 빛 산란의 원리는 "GPU Gems 3" [13장](http://http.developer.nvidia.com/GPUGems3/gpugems3_ch13.html)「책에 있는 효과적인 그림:

![](assets/img/2014-3-30-unity-light-scattering/goodeffect.png)

이 제출한 텍스트를 한국어로 번역하겠습니다.

책에는 이론이 소개되었고, 중요한 한 가지 공식은 다음과 같다:

\\[ L(s, \theta, \phi) = exposure \times \sum\_{i=0}^n decay^i \times weight \times \frac{L( s\_i, \theta\_i )}{n} \\]

내 이해에 따르면, 이미지의 각 픽셀에 대해 빛이 비추어질 수 있다는 것인데, 이 픽셀에서 빛원(이미지에 투사된 위치)까지의 선을 샘플링하여(수식에서 \\(i\\)에 해당), 샘플링된 결과를 가중 평균하여(수식에서 \\(\sum\\)에 해당) 해당 픽셀의 새로운 색상 값으로 사용합니다. 또한 핵심 후-픽셀 셰이더도 있지만, 그 셰이더만 사용하여 카메라 렌더링 결과를 처리하면 인위적인 흔적이 생기며 많은 줄무늬가 발생합니다.

![](assets/img/2014-3-30-unity-light-scattering/badeffect.png)

책에서 설명한 효과는 어떻게 만드는 거죠? 사실 책에서 이미 답을 제시했는데, 하나의 그림 집합으로 설명할 수 있어요:

![](assets/img/2014-3-30-unity-light-scattering/steps.png)

그림 a는 거친 효과를 의미하며, 주의 깊게 보면 많은 줄무늬가 있으며 가려지는 것이 없어야 실감이 난다. b, c, d는 좋은 효과를 얻기 위해 수행해야 하는 단계입니다:

이 텍스트를 한국어로 번역하십시오:

b. 조명의 방사 효과를 이미지에 렌더링하고 물체의 가림을 추가합니다.

b를 통해 부피 빛 산란 픽셀 셰이더를 실행하여 가려진 효과를 얻습니다.

실제 장면의 색상을 추가하세요.

그럼 이제 우리는 한 걸음 한 걸음 실현해 보겠습니다.

##물체 가리는 그림

실제 작업 중에는 'RenderWithShader'를 사용하여 가려지는 물체를 검정색으로, 다른 곳은 흰색으로 그리는데, 이는 각 면을 렌더링해야 하기 때문에 복잡한 장면에서는 일정한 성능 손실을 가져올 수 있습니다. 장면에는 불투명하고 투명한 물체가 있으며, 불투명한 오브젝트는 완전한 광선 가림을 만들어야 하고, 투명한 물체는 부분적인 가림을 만들어야 합니다. 따라서 다른 RenderType에 대한 물체에 대해 다른 Shader를 작성해야 하며, RenderType은 SubShader의 Tag입니다. 모르겠다면 [여기](http://docs.unity3d.com/Documentation/Components/SL-SubshaderTags.html)이 텍스트를 한국어로 번역해드리겠습니다:，작성한 후에 호출합니다:

```c#
camera.RenderWithShader(objectOcclusionShader, "RenderType");

```
`RenderWithShader` 함수의 두 번째 매개변수는 RenderType에 따라 Shader를 교체하는 것을 요청합니다. 다시 말해서, 동일한 객체의 Shader 교체는 이전 Shader와 RenderType이 일치해야 합니다. 이렇게 하면 다른 RenderType의 객체에 다른 Shader를 사용할 수 있습니다:

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

일종의 광역으로 불투명 및 투명 물체의 쉐이더 간 차이에 유의하십시오: 불투명 물체는 단순히 검정색으로 그려집니다. 불투명 물체는 블렌딩을 수행해야 하며, 물체 텍스처의 알파 채널을 얻은 후 이 알파를 기반으로 블렌딩을 수행해야 합니다. 위 코드는 불투명 및 투명만 나열했지만, 또 다른 TreeOpaque (쉐이더가 불투명과 동일하지만 RenderType이 변경된 것), TreeTransparentCutout (Transparent와 동일) 등도 있습니다. RenderType이 지정되었으므로 가능한 한 장면에서 가려지는 물체를 완전히 탐색해야 합니다. 여기에는 앞서 언급한 네 가지만 있습니다. 대략적인 결과는 다음과 같습니다:

![](assets/img/2014-3-30-unity-light-scattering/objectocclusion.png)

##물체가 빛원을 가리는 현상입니다.

광원의 방사를 그리는 것은 어렵지 않지만 화면 크기에 따라 처리를 해야 하며 광원의 방사 형태가 원형이 되도록 주의해야 합니다:

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

이 Shader는 스크린 상의 광원 위치를 입력해야 합니다(`camera.WorldToViewportPoint`를 사용하여 UV 좌표를 얻을 수 있음). 그 후 지정된 반지름에 따라 외부로 흐려지는 밝기의 원을 그려주어야 하며 이 결과물은 이전에 얻은 물체 가리는 이미지(`_MainTex`에 저장)와 결합되어 대략적으로는 다음과 같아야 합니다:

![](assets/img/2014-3-30-unity-light-scattering/light.png)

##빛 산란 처리 및 실제 색상을 결합합니다.

여기서는 책에 제공된 픽셀 쉐이더를 사용해야 합니다. 제 버전은:

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

대체로 책에 나와 있는 것과 일치하지만, 제 매개변수는 프로그램에서 전달되어야 하며, 실제 색상 이미지와 광산포도 그림을 결합하여 다음과 같은 결과가 도출되었습니다:

![](assets/img/2014-3-30-unity-light-scattering/effect.gif)

##완전한 코드

해당 코드는 [여기](assets/img/2014-3-30-unity-light-scattering/2014-3-30-unity-light-scattering.zip)카메라에 'cs' 스크립트를 추가하십시오.

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT를 사용하여 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)어떤 빠뜨림도 지적해 주세요. 
