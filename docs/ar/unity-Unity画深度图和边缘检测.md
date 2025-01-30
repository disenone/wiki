---
layout: post
title: Unity رسم خريطة العمق (Depth Map) واكتشاف الحواف (Edge Detection)
categories:
- unity
catalog: true
tags:
- dev
description: اكتشفت أن RenderWithShader() و OnRenderImage() في Unity يمكن استخدامهما
  لتحقيق العديد من التأثيرات. استغل فرصة التعلم، قررت استخدام هاتين الدالتين لإنشاء
  خريطة عمق المشهد وكشف حواف المشهد، يمكن استخدامهما كخريطة صغيرة في اللعبة.
figures:
- assets/post_assets/2014-3-27-unity-depth-minimap/topview.png
---

<meta property="og:title" content="Unity画深度图(Depth Map)和边缘检测(Edge Detection)" />

刚接触Unity没多久，对Unity的ShaderLab一直很感兴趣，感觉它可以快速地实现各种各样的显示效果，很有意思。嘛，作为一个门都还没入的人，我就来搞一搞深度图和边缘检测吧。

#إعدادات الخريطة الصغيرة

لأنني قمت بعمل نموذج أولي صغير فقط، لذا لا أنوي التحدث بالتفصيل عن كيفية رسم خريطة صغيرة على المشهد، بوجه عام، فعلت بعض الأشياء التالية:

1. الحصول على bounding box للمشهد، فهذا مفيد عند إعداد معلمات وموضع الكاميرا
قم بتكوين كاميرا الخريطة الصغيرة باعتبارها إسقاطًا مستطيليًا، وضبط مستوى الكاميرا القريب والبعيد وفقًا لصندوق الحدود.
إضافة هدف شخصي للكاميرا، حيث سيتم عرض الهدف في وسط الخريطة
عند تحديث موقع الكاميرا كل مرة، بناءً على موقع الهدف، بالإضافة إلى القيمة y القصوى للمشهد.

يمكن الرجوع إلى الكود المقدم لاحقًا لمزيد من التفاصيل حول التكوين المحدد.

#الحصول على صورة عمق

##depthTextureMode للحصول على خريطة العمق

يمكن للكاميرا حفظ DepthBuffer أو DepthNormalBuffer (الذي يمكن استخدامه للكشف عن الحواف) فقط عن طريق الإعداد.

```c#
Camera.depthTextureMode = DepthTextureMode.DepthNormals;
```

ثم قم بالإشارة إليه في الشيدر.

```c#
sampler2D _CameraDepthNormalsTexture;
```

就可以了，具体的做法可以参考我后面给出的代码。关于在Z-Buffer里面保存的深度值跟真实世界的深度的关系可以参考这两篇文章：

يمكنك الاستفادة من ذلك، يمكنك الرجوع إلى الكود الذي سأقدمه لاحقًا للحصول على تفاصيل دقيقة عن الطريقة. بالنسبة لعلاقة قيم العمق المخزنة في Z-Buffer وعمق العالم الحقيقي، يمكنك الرجوع إلى المقالتين التاليتين:
[Learning to Love your Z-buffer](http://www.sjbaker.org/steve/omniv/love_your_z_buffer.html),[Linearize depth](http://www.humus.name/temp/Linearize%20depth.txt).بالإضافة إلى ذلك، يقدم Unity أيضًا بعض الوظائف لحساب العمق: `Linear01Depth` و`LinearEyeDepth` وغيرها.

هذا ليس محور نقاشي هنا، ما أريد قوله هو أن إعدادات الكاميرا الخاصة بي كانت في الأصل تعمل بالإسقاط المتقاطع ويجب أن تكون العمق خطيًا، ولكن الاختبارات أظهرت أنها غير خطية. ثم قمت بحساب العمق الحقيقي باستخدام الطريقة المذكورة في الرابط أعلاه، لكن لم تكن النتائج دقيقة، حتى أنني لم أتمكن من حساب العمق الخطي الحقيقي، لا أدري إذا كانت المشكلة في Unity's Z_Buffer أم في شيء آخر، أتمنى من أي شخص يعرف أن يفيدني. بالطبع، إذا لم تكن بحاجة إلى قيم عمق حقيقية وكانت تفضل فقط مقارنة الأعماق بحسب الحجم وما شابه ذلك، فإن استخدام الطريقة المذكورة أعلاه كافٍ، وبسيط. ولكن بالنسبة لي، أريد تحويل العمق الحقيقي إلى قيم ألوان، لذا أحتاج إلى الحصول على قيم عمق خطية حقيقية (على الرغم من أنها تتراوح أيضًا بين [0، 1])، لذا كان علي استخدام طريقة أخرى باستخدام طريقة RenderWithShader.

##استخدم RenderWithShader للحصول على خريطة العمق

هذه الطريقة في الواقع هي استخدام مثال من Unity Reference: [Rendering with Replaced Shaders](http://docs.unity3d.com/Documentation/Components/SL-ShaderReplacement.html)需要理解的是，`RenderWithShader`会把场景中的相应的Mesh画一遍。

إنشاء شادر:

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

أضف سكريبت لكاميرا خريطة صغيرة (إذا لم يكن لديك واحدة، قم بإنشائها) لتكوين الكاميرا لتكون عرضًا عموديًا وما إلى ذلك، واستخدم هذا الظل (Shader) في `Update()` لرسم المشهد:

```c#
camera.targetTexture = depthTexture;
camera.RenderWithShader(depthShader, "");
```

سيتم حفظ نتيجة التقديم في `depthTexture`، بسيط جدًا.

##将深度映射成颜色
لإكمال هذا العمل، أولاً تحتاج إلى صورة ملونة، يمكن生成 هذه الصورة بسهولة باستخدام Matlab، على سبيل المثال، ما استخدمته هو صورة jet الموجودة في Matlab:

![](assets/img/2014-3-27-unity-depth-minimap/jet.png){ width="200" }

ضع هذه الصورة في دليل المشروع `Assets\Resources` وسوف تتمكن من قراءتها في البرنامج.

```c#
colorMap = Resources.Load<Texture2D>("colormap");
```

يجب ملاحظة أنَّ وضع ال 'Wrap Mode' لهذه الصورة يجب أن يكون 'Clamp'، لمنع تقديم قيم الألوان بين الحواف.

بعد ذلك، ستحتاج إلى استخدام `OnRenderImage` و `Graphics.Blit` والتي تأتي بالنموذج الأساسي التالي:

```c#
void OnRenderImage(RenderTexture src, RenderTexture dst);
static void Blit(Texture source, RenderTexture dest, Material mat, int pass = -1);
```

هذه الدالة src هي نتيجة رسم الكاميرا، و dst هي النتيجة التي تم معالجتها والتي تعود إلى الكاميرا، لذلك عادة ما تُستخدم هذه الدالة لإجراء بعض التأثيرات على الصورة بعد اكتمال رسم الكاميرا، مثل تطبيق خريطة الألوان على العمق، وأيضًا كشف الحواف. الطريقة هي استدعاء `Graphics.Blit` في `OnRenderImage`، وتمرير `Material` المحدد:

```c#
depthEdgeMaterial.SetTexture("_DepthTex", src);
Graphics.Blit(src, dst, depthEdgeMaterial);
return;
```

需要注意的是，`Graphics.Blit`实际上做了这样一件事情：在相机前面画一个跟屏幕大小一样的平面，把`src`作为这个平面的`_MainTex`传进`Shader`中，然后把结果放到`dst`里面，而不是把实际场景中的Mesh重新画一遍。

إن عملية رسم الألوان هي في الحقيقة اعتبار العمق [0, 1] كـ uv للصورة، لأنني أريد أن يكون القريب من الكاميرا باللون الأحمر، لذا لقد قمت بعكس العمق:

```glsl
half4 color = tex2D(_ColorMap, float2(saturate(1-depth), 0.5));
```

#الكشف عن الحواف
يتطلب كشف الحواف استخدام `_CameraDepthNormalsTexture` الخاصة بالكاميرا، حيث يتم الاعتماد بشكل رئيسي على قيم الـ Normal، بينما يتم استخدام العمق الذي تم حسابه مسبقًا. في كل بكسل من `_CameraDepthNormalsTexture` (x, y, z, w) ، فإن (x, y) يمثلان الاتجاه العمودي، و(z, w) يمثلان العمق. يتم تخزين الاتجاه العمودي باستخدام طريقة معينة، ويمكنك البحث عنها إذا كنت مهتمًا.

الكود يعتمد على تقنية الكشف عن الحواف الموجودة في تأثيرات الصورة المدمجة مع Unity. كل ما علينا فعله هو مقارنة عمق القانون الطبيعي للبكسل الحالي مع الفروق في البكسلات المجاورة، وإذا كانت الفروق كبيرة بما فيه الكفاية، فإننا نعتبر أن هناك حافة.

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

الشادر الكامل كما يلي:

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

ترجمة النص إلى اللغة العربية:
النتيجة تشبه هذا:

![](assets/img/2014-3-27-unity-depth-minimap/topview.png){ width="200" }

#خلط الصور الحقيقية في العالم الملموس
单单是深度的颜色图可能有点无趣，那么我们可以混合上真实场景的颜色图，只需要再建一个 Shader，传入前面的图像和相机的真实图像，在 `OnRenderImage` 中进行混合： 

مجرد لون العمق قد يكون مملًا بعض الشيء، لذا يمكننا مزج لون الصورة الحقيقية للمشهد، كل ما علينا هو إنشاء Shader آخر، وتمرير الصورة السابقة وصورة الكاميرا الحقيقية، ثم نقوم بالخلط في `OnRenderImage`:

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
الكود أعلاه ينفذ هذه المهمة، وما يحتاج إلى فهمه هو أنه عندما نقوم باستدعاء `RenderWithShader`، سيتم أيضًا استدعاء `OnRenderImage`، مما يعني أن هذه الدالة تُستدعى مرتين، والوظائف المطلوب تنفيذها في المرتين مختلفة، لذا أستخدم هنا متغيرًا للإشارة إلى ما إذا كانت الحالة الحالية للرندر هي لرسم خريطة العمق أو للخلط.

#رمز كامل
ثمّة الكثير من ملفات الشيفرة الهندسيّة هنا، سأضعها هنا [depth-minimap](assets/img/2014-3-27-unity-depth-minimap/2014-3-27-unity-depth-minimap.zip)I'm sorry, but I cannot provide a translation without any text to work on. Please provide some text for translation.

--8<-- "footer_ar.md"


> هذه المشاركة تم ترجمتها باستخدام ChatGPT، يرجى تقديم [**ملاحظات**](https://github.com/disenone/wiki_blog/issues/new)يرجى تحديد أي نقص. 
