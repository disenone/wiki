---
layout: post
title: قم بتوليف صورة العمق(depth map) وكشف الحواف (edge detection)
categories:
- unity
catalog: true
tags:
- dev
description: اكتشفت أن RenderWithShader() و OnRenderImage() في Unity يمكن استخدامهما
  لتحقيق العديد من التأثيرات. خلال فرصة التعلم، قررت استخدام هاتين الدالتين لإنشاء
  خريطة عمق المشهد وكشف حواف المشهد، يمكن استخدامهما كخريطة صغيرة في اللعبة.
figures:
- assets/post_assets/2014-3-27-unity-depth-minimap/topview.png
---

<meta property="og:title" content="Unity画深度图(Depth Map)和边缘检测(Edge Detection)" />

لقد بدأت مؤخرًا في استكشاف Unity، وكنت دائمًا مهتمًا بـ ShaderLab في Unity. أشعر بأنه يمكن أن يساعدني في تحقيق مجموعة متنوعة من تأثيرات العرض بسرعة، وهذا مثير للاهتمام. على أي حال، كمبتدئ في هذا المجال، سأبدأ باستكشاف الرسوميات العميقة وكشف الحواف.

#ضبط الخريطة الصغيرة

بسبب أنني قمت فقط بعمل نسخة ابتدائية، لذلك لا أنوي أن أشرح بالتفصيل كيفية رسم خريطة صغيرة في المشهد، بشكل عام قمت باتباع الخطوات التالية:

الحصول على صندوق الحد الأقصى للمشهد، هذا مفيد عند ضبط معلمات الكاميرا وموضعها
قم بتكوين كاميرا الخريطة الصغيرة بتصوير عرضي وفقًا لمربع الحدود، وحدد مستوى الكاميرا القريب والبعيد.
إضافة هدف شخص على الكاميرا، وسيظهر الهدف في وسط الخريطة.
كل مرة يتم تحديث موقع الكاميرا وفق موقع الهدف وقيمة y القصوى للمشهد.

يمكن الرجوع إلى الشيفرة الواردة بعد ذلك للحصول على التفاصيل الدقيقة للتكوين.

#احصل على الصورة العميقة

##استخدام depthTextureMode للحصول على العمق من الصورة.

الكاميرا يمكنها حفظ DepthBuffer أو DepthNormalBuffer (يمكن استخدامها للكشف عن الحواف)، فقط قم بضبط الإعدادات

```c#
Camera.depthTextureMode = DepthTextureMode.DepthNormals;
```

ثم قم بالإشارة إليه في الـShader.

```c#
sampler2D _CameraDepthNormalsTexture;
```

يمكنك فعل ذلك، يمكنك الرجوع إلى الشيفرة التالية التي سأقدمها بعد ذلك. بالنسبة للعلاقة بين قيم العمق المحفوظة في الذاكرة المؤقتة Z-buffer والعمق الحقيقي للعالم يمكنك الرجوع إلى هذين المقالتين:
[Learning to Love your Z-buffer](http://www.sjbaker.org/steve/omniv/love_your_z_buffer.html),[Linearize depth](http://www.humus.name/temp/Linearize%20depth.txt)بالإضافة إلى ذلك، تقدم Unity أيضًا بعض الدوال لحساب العمق، مثل `Linear01Depth`، `LinearEyeDepth` وغيرها.

هذا ليس محور مناقشتي هنا، أريد أن أقول، الكاميرا الخاصة بي كانت مضبوطة بتصوير متساوي الاطراف، وعمقه يجب أن يكون خطيًّا، ولكن النتائج أظهرت عكس ذلك. ثم جربت الطريقة المقدمة بالرابط أعلاه لحساب عمق العالم الحقيقي، ولكن لم يكن دقيقًا أبدًا، حتى لم أتمكن من حساب العمق الحقيقي بشكل خطي، لا أدري هل هو مشكلة في ذاكرة الـ Z لبرنامج Unity أم شيء آخر، إذا كان أحد يعرف الحل، فليعلمني من فضلك. بالطبع، إذا لم يكن هناك حاجة لقيمة العمق الحقيقية، وكانت المقارنة فقط بين أعماق مختلفة وما شابه ذلك، فإن الطريقة المشار إليها أعلاه كافية، وبسيطة أيضًا. ولكن بالنسبة لي، أود تحويل العمق الحقيقي إلى قيمة لونية، وهذا يتطلب الحصول على قيمة عمق حقيقية خطية (رغم أنها تتراوح من 0 إلى 1)، لذا اضطررت لاستخدام طريقة أخرى باستخدام الـ RenderWithShader.

##استخدم RenderWithShader للحصول على صورة العمق

هذه الطريقة في الواقع تعتمد على مثال موجود داخل الـ Unity Reference: [Rendering with Replaced Shaders](http://docs.unity3d.com/Documentation/Components/SL-ShaderReplacement.html) يتطلب الفهم أن `RenderWithShader` سيقوم برسم Mesh المقابل في الساحة.

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

أضف نصًا إلى الكاميرا الصغيرة الخاصة بك (إن لم تكن موجودة، فأنشئها) ، وقم بتكوين الكاميرا بإعدادات العرض المتساوي واستخدام هذا ال Shader لتقديم المشهد في `Update()` .

```c#
camera.targetTexture = depthTexture;
camera.RenderWithShader(depthShader, "");
```

ستتم حفظ نتيجة التظليل في `depthTexture`، سهل جدًا.

##تحويل العمق إلى ألوان
لإكمال هذا العمل، يجب أولاً الحصول على صورة ملونة، يمكن إنشاء هذه الصورة بسهولة باستخدام Matlab، على سبيل المثال، أنا استخدم jet داخل Matlab:

![](assets/img/2014-3-27-unity-depth-minimap/jet.png){ width="200" }

ضع هذه الصورة في دليل المشروع `Assets\Resources` ، حتى تتمكن من قراءتها في البرنامج:

```c#
colorMap = Resources.Load<Texture2D>("colormap");
```

يجب ملاحظة أن وضع اللف "Wrap Mode" لهذه الصورة يجب أن يكون "Clamp" لتجنب التعويض بين قيم الألوان على الحواف.

بعد ذلك، ستحتاج إلى استخدام الدوال `OnRenderImage` و `Graphics.Blit`، حيث يكون نموذج الدالة كالتالي:

```c#
void OnRenderImage(RenderTexture src, RenderTexture dst);
static void Blit(Texture source, RenderTexture dest, Material mat, int pass = -1);
```

وظيفة هذا هي أن يكون src ناتج العرض البصري الذي يجلبه الكاميرا، أما dst فهو الناتج المعالج الذي يعود إلى الكاميرا، لذلك تُستخدم هذه الوظيفة عادة لإضافة بعض التأثيرات على الصور بعد أن ينتهي العرض البصري للكاميرا، مثل تطبيق تصوير الألوان على العمق، وكذلك كشف الحواف. الطريقة هي استدعاء `Graphics.Blit` في `OnRenderImage` وتمرير `Material` المحدد:

```c#
depthEdgeMaterial.SetTexture("_DepthTex", src);
Graphics.Blit(src, dst, depthEdgeMaterial);
return;
```

يجب ملاحظة أن `Graphics.Blit` يقوم في الواقع بعمل ما يلي: يقوم برسم مستوى بحجم الشاشة أمام الكاميرا، يضع `src` كـ `_MainTex` لهذا المستوى ويمرره إلى `Shader` ، ثم يضع النتيجة في `dst`، بدلاً من إعادة رسم Mesh الفعلية في الساحة.

فعلياً، تعني عملية تعيين الألوان مطابقة العمق [0، 1] بأنها إحداثيات صورة uv، حيث قمت بتغيير العمق عكسياً لجعل الأشياء الأقرب للكاميرا باللون الأحمر.

```glsl
half4 color = tex2D(_ColorMap, float2(saturate(1-depth), 0.5));
```

#الكشف عن الحواف
يتطلب كشف الحواف استخدام `_CameraDepthNormalsTexture` الخاص بالكاميرا ، حيث يتم استخدام قيمة Normal بشكل أساسي ، ويتم استخدام العمق الذي تم حسابه مسبقًا. في كل بكسل (x ، y ، z ، w) في `_CameraDepthNormalsTexture` ، (x ، y) هما الطرق السطحية ، (z ، w) هما العمق. الطرق السطحية تم تخزينها باستخدام طريقة معينة ، لمن يكون لديه الاهتمام يمكنه البحث بنفسه.

تم استعمال الشيفرة المصدرية لتأثير الصور المدمج في Unity للكشف عن الحواف. ما علينا فعله هو مقارنة عمق السطوح الطبيعية للبيكسل الحالي مع الاختلاف بين البيكسل المجاور، إذا كان الاختلاف كبيرًا بما فيه الكفاية فإننا نعتبر أن هناك حافة.

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

الشيدر الكامل كما يلي:

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

تمامًا كما في هذا:

![](assets/img/2014-3-27-unity-depth-minimap/topview.png){ width="200" }

#مزج صور العالم الحقيقي
قد تكون صور الألوان العميقة وحدها قليلاً مملة، لذا يمكننا دمج صور الألوان الحقيقية للمشاهد، ما عليك سوى إنشاء Shader جديد، وتمرير الصورة السابقة وصورة الكاميرا الحقيقية في الدالة `OnRenderImage` للقيام بالمزج بينهما:

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
الشيفرة أعلاه هي التي تنفذ هذا العمل. يجب فهم أنه عند استدعاء `RenderWithShader`، سيتم أيضًا استدعاء `OnRenderImage`، أي أن هذه الدالة ستستدعى مرتين، ولكل استدعاء مهمة مختلفة. لذلك استخدمت متغيرًا هنا للإشارة إلى ما إذا كانت حالة العرض الحالية تقوم بعمل خريطة عمق أم اختلاط.

#الشفرة الكاملة
الملفات في الكود كتير شوي، فحطيتهن هون [depth-minimap](assets/img/2014-3-27-unity-depth-minimap/2014-3-27-unity-depth-minimap.zip)I apologize, but I cannot provide a translation for this text as it does not contain any meaningful content.

--8<-- "footer_ar.md"


> هذه المشاركة تم ترجمتها باستخدام ChatGPT، يرجى تقديم [**ردود**](https://github.com/disenone/wiki_blog/issues/new)يرجى تحديد أي شيء تم إغفاله. 
