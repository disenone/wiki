---
layout: post
title: سجل الإصدارات
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
- Editor
- Editor Plus
- Editor Plugin
- AI Chat
- Chatbot
- Image Generation
- OpenAI
- Azure
- Claude
- Gemini
- Ollama
description: سجل الإصدارات
---

<meta property="og:title" content="UE 插件 AIChatPlus 版本日志" />

#سجل تحديثات إضافة AIChatPlusUE

## v1.6.0 - 2025.03.02

###الميزة الجديدة

يرجى الترقية إلى الإصدار B4604 من ملف Llama.cpp.

Cllama supports GPU backends: cuda and metal.

أداة الدردشة Cllama تدعم استخدام وحدة GPU

دعم قراءة ملفات نموذج من حزمة Pak

### Bug Fix

إصلاح مشكلة تعطّل Cllama عند إعادة التحميل أثناء التفكير.

إصلاح رسالة خطأ تجميع iOS

## v1.5.1 - 2025.01.30

###الميزة الجديدة

إذا تبي ثانية مساعدة، ناطرك.

تحسين طريقة الحصول على بيانات PCMData، وفك ضغط بيانات الصوت عند توليد B64

* الطلب: زيادة اثنين من الاستدعاءات OnMessageFinished و OnImagesFinished

تحسين طريقة Gemini، والحصول تلقائيًا على الطريقة بناءً على bStream

أضف بعض الدوال المعمارية لتسهيل تحويل المحيط إلى أنواع فعلية، والحصول على رسالة الاستجابة والخطأ.

### Bug Fix

إصلاح مشكلة استدعاء  Request Finish مرارًا وتكرارًا

## v1.5.0 - 2025.01.29

###الميزة الجديدة

دعم تشغيل الصوت لـ Gemini

تغيير من النص إلى اللغة العربية:

"تدعم أدوات المحرر إرسال الصوتيات وتسجيل الصوت."

### Bug Fix

إصلاح خلل فشل نسخ الجلسة

## v1.4.1 - 2025.01.04

###إصلاح المشكلة

يدعم أدوات المحادثة إرسال الصور فقط دون إرسال رسائل.

قدّم الصورة الفاشلة لمشكلة إرسال الصور في واجهة OpenAI.

إصلاح تغييرات في إعدادات أدوات الدردشة OpanAI وAzure التي تغيبت عنها معلمات الجودة والنمط وإصدار الواجهة Quality، Style، ApiVersion.

## v1.4.0 - 2024.12.30

###الميزة الجديدة

（وظيفة تجريبية） تدعم النموذج متعدد الأوضاع Cllama (llama.cpp) ، يمكنها معالجة الصور.

تمت إضافة توجيهات تفصيلية لجميع معلمات نوع العنصر الأزرق

## v1.3.4 - 2024.12.05

###الميزة الجديدة

OpenAI تدعم واجهة برمجة التطبيقات البصرية.

###إصلاح المشكلة

إصلاح الخطأ في OpenAI stream=false

## v1.3.3 - 2024.11.25

###ميزة جديدة

دعم UE-5.5

###إصلاح المشكلات

إصلاح مشكلة عدم تفعيل بعض النماذج الزرقاء.

## v1.3.2 - 2024.10.10

###إصلاح المشكلة

إصلاح الانهيار الذي يحدث عند إيقاف طلب الوقف اليدوي cllama

إصلاح مشكلة عدم العثور على ملفات ggml.dll وllama.dll عند تحميل نسخة win المعبأة من المتجر.

عند إنشاء الطلب، تحقق إذا كان في خيط اللعبة GameThread.

## v1.3.1 - 2024.9.30

###وظيفة جديدة

إضافة SystemTemplateViewer جديد، يمكنك من خلاله عرض واستخدام مئات القوالب النظامية.

###إصلاح المشكلة

قم بإصلاح الإضافات التي تم تنزيلها من المتجر، حيث يُعجز llama.cpp عن العثور على مكتبة الربط.

قم بإصلاح مشكلة طول مسار LLAMACpp.

إصلاح خطأ ربط ملف llama.dll بعد تعبئة windows

إصلاح مشكلة قراءة مسار الملفات في نظام التشغيل iOS/Android

إصلاح خطأ في تسمية إعدادات Cllame

## v1.3.0 - 2024.9.23

###مهم جداً

دمج llama.cpp ، ودعم تنفيذ نماذج كبيرة محليًا دون اتصال بالإنترنت.

## v1.2.0 - 2024.08.20

###الميزة الجديدة

دعم تحرير الصور OpenAI/Image Variation.

دعم واجهة برمجة التطبيقات Ollama، ودعم الحصول التلقائي على قائمة النماذج المدعومة بواسطة Ollama.

## v1.1.0 - 2024.08.07

###الميزة الجديدة

دعم الخطة الزرقاء

## v1.0.0 - 2024.08.05

###الميزة الجديدة

الوظائف الأساسية الكاملة

دعما لـ OpenAI، Azure، Claude، Gemini

أداة تحرير محادثات مع محرر مدمج يتميز بوظائف متكاملة

--8<-- "footer_ar.md"


> هذه المشاركة تم ترجمتها باستخدام ChatGPT، يرجى تقديم [**ردود فعل**](https://github.com/disenone/wiki_blog/issues/new)يرجى تحديد أي نقص. 
