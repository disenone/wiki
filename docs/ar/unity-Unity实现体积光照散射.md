---
layout: post
title: يتم تنفيذ scattering الضوء الحجمي في Unity (تشتت الضوء الحجمي، ضوء الفجوة السحابية)
categories:
- unity
catalog: true
tags:
- dev
description: تشتت الضوء حسب الحجم هو تأثير بصري جيد جدًا، تبدو وكأنك تشاهد انتشار
  الضوء في الهواء، حيث تُضاء الجسيمات الدقيقة في الهواء بالضوء وتُحجب جزءٌ من الأشعة،
  مما يخلق بصريًا خطوط الضوء المنبعثة من مصدر الضوء.
figures:
- assets/post_assets/2014-3-30-unity-light-scattering/effect.gif
---

<meta property="og:title" content="Unity实现体积光照散射 (Volumetric Light Scattering，云隙光)" />

##المبدأ

يمكن الرجوع إلى مبدأ تشتت الضوء الحجمي في "GPU Gems 3" [الفصل 13](http://http.developer.nvidia.com/GPUGems3/gpugems3_ch13.html)،الكتاب يحتوي على صور فعالة:

![](assets/img/2014-3-30-unity-light-scattering/goodeffect.png)

جذاب، حسناً، هدفنا هو تحقيق هذا التأثير.

الكتاب يشرح المبدأ، والمعادلة الرئيسية هي:

\\[ L(s, \theta, \phi) = exposure \times \sum\_{i=0}^n decay^i \times weight \times \frac{L( s\_i, \theta\_i )}{n} \\]

我的理解是，对于图像上的每个像素，光线都有可能照射到，那么对该像素到光源(在投影到图像上的位置)的连线进行采样(对应公式上\\(i\\))，采样出的结果进行加权平均(对应公式上\\(\sum\\))并作为该像素的新的颜色值。另外还有关键的后置像素着色器，但是如果只是用那个着色器来对相机渲染的结果进行处理，会产生明显的人工痕迹，有许多的条纹：

![](assets/img/2014-3-30-unity-light-scattering/badeffect.png)

كيف يتم إنتاج التأثيرات الموجودة في الكتاب؟ في الواقع، قدمت الكتب بالفعل الإجابة، يمكن توضيحها باستخدام مجموعة من الرسوم.

![](assets/img/2014-3-30-unity-light-scattering/steps.png)

الشكل (أ) يمثل التأثير الخشن، ويمكن ملاحظته بدقة وجود العديد من الخطوط، كما أنه لا يوجد ما يحجب الصورة مما يجعلها أقل واقعية. أما (ب) و(ج) و(د) فهي الخطوات اللازمة لتحقيق تأثير جيد.

قم بعرض تأثيرات إشعاع الضوء على الصورة وإضافة تأثير حجب الأجسام.

قم بتنفيذ انتشار الضوء الحجمي Volumetric Light Scattering على b باستخدام مُظلل البكسل، للحصول على تأثير ما يحدث بعد التظليل.

d. إضافة اللون الحقيقي للمشهد

ثم دعونا نقوم بتنفيذه خطوة بخطوة.

##رسم جسم مغطى

في العمليات الفعلية، أستخدم أولاً `RenderWithShader` لرسم الأجسام التي ستتعرض للازدحام باللون الأسود، بينما تكون الأماكن الأخرى باللون الأبيض. وذلك لأن هذا يتطلب رسم كل وجه، وبالتالي بالنسبة للمشاهد المعقدة، سيؤدي ذلك إلى استهلاك معين في الأداء. تحتوي المشهد على أجسام غير شفافة وشفافة، ونريد أن تنتج الأجسام غير الشفافة حجباً كاملاً للضوء، بينما يجب أن تنتج الأجسام الشفافة حجباً جزئياً. لذلك، نحتاج إلى كتابة شيدرز مختلفة لأجسام مختلفة بناءً على RenderType، وهو Tag لـ SubShader، إذا لم تكن واضحاً، يمكنك الاطلاع على [هنا](http://docs.unity3d.com/Documentation/Components/SL-SubshaderTags.html)بعد كتابة النص بشكل جيد، قم بالاستدعاء:

```c#
camera.RenderWithShader(objectOcclusionShader, "RenderType");

```
`RenderWithShader` المعامل الثاني يتطلب استبدال Shader بناءً على RenderType. ببساطة، يجب أن يتطابق RenderType لشادر المستبدل مع الشادر الأصلي لنفس الكائن، وبذلك يمكننا استخدام شادر مختلف لكائنات ذات RenderType مختلفة:

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

يرجى ملاحظة الفرق بين Shaders للكائنات الصلبة والشفافة: يتم رسم الكائنات الصلبة مباشرة باللون الأسود؛ أما الكائنات الشفافة فيلزم تنفيذ الدمج (blending)، حيث يتم الحصول على قناة ألفا (alpha) من نص الكائن واستخدامها في عملية الدمج. الشيفرة أعلاه تستعرض فقط الشفرات للكائنات الصلبة والشفافة، بالإضافة إلى TreeOpaque (الشيفرة مثل الصلبة ولكن يتم تغيير نوع العرض)، و TreeTransparentCutout (نفس الشيفرة للشفافة). نظرًا لتحديد نوع العرض، يجب استكشاف وتوثيق أكبر قدر ممكن من الحالات التي قد تحدث فيها حجب الرؤية في البيئة؛ وهنا، تمثلت هذه الحالات في الأنواع الأربع المذكورة سابقًا. تقريبًا، كانت النتائج كالتالي:

![](assets/img/2014-3-30-unity-light-scattering/objectocclusion.png)

##تواجه هذا التحدّي الذي يجمع فيه جسم مع حجب إشعاع مصدر الضوء

رسم إشعاع مصدر الضوء ليس بالأمر الصعب، ولكن يجب مراعاة القيام ببعض المعالجات بناءً على حجم الشاشة، بحيث يكون شكل إشعاع المصدر دائريًا.

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

هذا الشادر يتطلب إدخال موقع مصدر الضوء على الشاشة (يمكن حسابه باستخدام `camera.WorldToViewportPoint` والذي يعطي إحداثيات الـUV)، ثم يتم رسم دائرة تتلاشى تدريجياً إلى الخارج بالسطوع وفقاً لنصف القطر المحدد، ثم يتم دمج النتيجة مع صورة تظليل الكائن السابقة (التي توضع في `_MainTex`)، النتيجة تكون تقريبياً كالتالي:

![](assets/img/2014-3-30-unity-light-scattering/light.png)

##تشتت الضوء المعالج، مع دمج اللون الحقيقي

سيتم استخدام Pixel Shader المقدم في الكتاب هنا، الإصدار الخاص بي:

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

大体上跟书上的一致，只是我的参数需要在程序中传进来，并且结合了真实的颜色图和Light Scattering图，结果：  
بشكل عام يتماشى مع ما هو في الكتاب، فقط أنه يتعين تمرير معاييري داخل البرنامج، وقد قمت بدمجها مع خريطة الألوان الحقيقية وصورة تشتت الضوء، والنتيجة:

![](assets/img/2014-3-30-unity-light-scattering/effect.gif)

##كود كامل

الشيفرة موجودة [هنا](assets/img/2014-3-30-unity-light-scattering/2014-3-30-unity-light-scattering.zip)إضافة نصي `cs` إلى الكاميرا.

--8<-- "footer_ar.md"


> ترجمت هذه المشاركة باستخدام ChatGPT ، يرجى تقديم [**ردود فعل**](https://github.com/disenone/wiki_blog/issues/new)يرجى الإشارة إلى أي فقرات مفقودة. 
