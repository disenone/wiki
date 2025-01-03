---
layout: post
title: تنفيذ Unity لتشتت الضوء الحجمي (Volumetric Light Scattering، الضوء المتناثر
  في السحب)
categories:
- unity
catalog: true
tags:
- dev
description: توزيع الضوء الحجمي هو تأثير بصري جيد جدًا، حيث تبدو وكأنك ترى انتشار
  الضوء في الهواء، حيث يُضاء الجسيمات الدقيقة في الهواء بالضوء، ويتم حجب جزء من الأشعة،
  مما يولد بصريًا أشعة تشع من مصدر الضوء.
figures:
- assets/post_assets/2014-3-30-unity-light-scattering/effect.gif
---

<meta property="og:title" content="Unity实现体积光照散射 (Volumetric Light Scattering，云隙光)" />

##المبدأ

(http://http.developer.nvidia.com/GPUGems3/gpugems3_ch13.html)لا يوجد نص محدد للترجمة.

![](assets/img/2014-3-30-unity-light-scattering/goodeffect.png)

حسنًا، إذن، هدفنا هو تحقيق هذا التأثير.

الكتاب يشرح المبدأ، وإحدى الصيغ الرئيسية هي:

\\[ L(s, \theta, \phi) = exposure \times \sum\_{i=0}^n decay^i \times weight \times \frac{L( s\_i, \theta\_i )}{n} \\]

فهمي هو، لكل بكسل في الصورة، هناك احتمال أن تصله الضوء، فنقوم بأخذ عينات للخط بين هذا البكسل ومصدر الضوء (المحاكاة في موضع الصورة) (معادلة \\(i\\))، ثم نقوم بتقديم التعويض المرجح للنتائج المتخذة من العينات (معادلة \\(\sum\\)) ونعتبر ذلك قيمة لون جديدة لهذا البكسل. بالإضافة إلى ذلك، هناك تقنية أساسية أخرى تسمى مشعاع البكسل الذي يأتي بعد مرحلة معالجة البكسل، ولكن إذا استخدمنا هذا المشعاع فقط لمعالجة نتائج تقنية الكاميرا، سنحصل على آثار اصطناعية واضحة مثل الخطوط والشرائط العديدة.

![](assets/img/2014-3-30-unity-light-scattering/badeffect.png)

كيف تم إنشاء التأثيرات الموجودة في الكتاب؟ في الحقيقة، قد قدم الكتاب الإجابة بالفعل، يمكن توضيحها باستخدام مجموعة من الرسوم.

![](assets/img/2014-3-30-unity-light-scattering/steps.png)

هذا هو الترجمة باللغة العربية:

هو النتيجة الخام، يُمكن رؤية العديد من الخطوط بعناية وليس هناك تمويه كافٍ، وأ، ب، ج هي الخطوات اللازم اتخاذها للحصول على نتيجة جيدة.

قم بتقديم تأثيرات إشعاع الضوء على الصورة وإضافة تظليل الأجسام.

قم بتطبيق Volumetric Light Scattering على b باستخدام معالج الظلال بالبكسل للحصول على تأثير محجوب.

إضافة ألوان المشهد الحقيقي.

ذلك الآن لنقم بتنفيذه خطوة بخطوة.

##رسم عوائق الجسم

في التشغيل الفعلي، أقوم أولاً باستخدام 'RenderWithShader' لرسم الكائنات التي ستتعرض للاختفاء باللون الأسود، والأماكن الأخرى باللون الأبيض، لأن هذا يتطلب عملية تقديم لكل وجه، وبالتالي، في الحالات العقيدة، سيؤدي ذلك إلى بعض استهلاك الأداء. الكائنات في الساحة تكون شفافة وغير شفافة، ونحن نرغب في أن تتسبب الكائنات غير الشفافة في حجب الضوء تماما، بينما يجب على الكائنات الشفافة أن تحجب الضوء جزئيا، لذلك نحتاج إلى كتابة Shaders مختلفة لكائنات RenderType المختلفة، حيث RenderType هو علامة SubShader، إذا كنت لست متأكدًا، يمكنك الاطلاع على [هنا](http://docs.unity3d.com/Documentation/Components/SL-SubshaderTags.html)بعد كتابة النص، قم بالاستدعاء:

```c#
camera.RenderWithShader(objectOcclusionShader, "RenderType");

```
المعلمة الثانية لدالة `RenderWithShader` هي استبدال الـShader بناءً على نوع الـRenderType. ببساطة، يجب أن يكون نوع الـRenderType للـShader الجديد المستبدل نفسه كنوع الـRenderType للـShader السابق، وبهذه الطريقة يمكننا استخدام Shaders مختلفة لأجسام بـ RenderTypes مختلفة.

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

يجب مراعاة الفروقات بين المواد الغير شفافة والشفافة في الـ Shader: تُرسم المواد الغير شفافة مباشرة باللون الأسود؛ بينما تتطلب المواد الغير شفافة تنفيذ عملية الدمج (blending)، حيث يتم الحصول على قناة الألفا (alpha) على النسيج الخاص بالجسم واستنادًا لهذه القيمة يتم الدمج. الشفرة أعلاه تعرض فقط المواد الغير شفافة والشفافة، بالإضافة إلى TreeOpaque (الشفرة مماثلة للغير شفافة ولكن يتم تغيير نوع العرض)، و TreeTransparentCutout (مماثلة للشفافة). بسبب تحديد نوع العرض، يجب في أقصى قدر ممكن استكمال مجموعة الكائنات في السيناريو التي قد تحدث حجبًا، وهنا تأتي الأربعة التي تم الإشارة إليها. تكوين النتائج تقريبًا كالتالي:

![](assets/img/2014-3-30-unity-light-scattering/objectocclusion.png)

##توازن بين تعتيم الجسم وإشعاع مصدر الضوء

ترجمة النص إلى اللغة العربية:

رسم إشعاع مصدر الضوء ليس بالأمر الصعب، المهم هو الانتباه إلى أنه يجب أن يتم التعامل مع حجم الشاشة بحيث يكون شكل إشعاع مصدر الضوء دائريًا.

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

هذا الشيدر يتطلب إدخال موقع مصدر الضوء على الشاشة (يمكن حسابه باستخدام `camera.WorldToViewportPoint` ، حيث يتم الحصول على إحداثيات UV)، ثم يتم رسم دائرة تتلاشى تدريجياً إلى الخارج بسطوع مُحدد بناءً على النصف القطر المُحدد، ونختم النتيجة مع صورة الكتمان للجسم التي تم الحصول عليها سابقاً (التي توضع في `_MainTex`)، وسيكون الناتج تقريبياً مثل:

![](assets/img/2014-3-30-unity-light-scattering/light.png)

##معالجة تشتيت الضوء وتوحيد الألوان الحقيقية.

سيتم استخدام Pixel Shader المقدم في الكتاب هنا. إصداري هو:

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

تقريبًا متطابق مع ما هو مذكور في الكتاب، إلا أنّ البارامترات الخاصة بي تحتاج إلى تمريرها داخل البرنامج، مع الجمع بين صورة الألوان الحقيقية ورسم تبدد الضوء، والنتيجة:

![](assets/img/2014-3-30-unity-light-scattering/effect.gif)

##الرمز الكامل

الرمز موجود [هنا](assets/img/2014-3-30-unity-light-scattering/2014-3-30-unity-light-scattering.zip)إضافة النص `cs` إلى الكاميرا.

--8<-- "footer_ar.md"


> هذه المشاركة تمت ترجمتها باستخدام ChatGPT، يرجى تقديم [**تعليق**](https://github.com/disenone/wiki_blog/issues/new)حدد أي اهتمامات مفقودة. 
