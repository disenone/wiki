---
layout: post
title: UE تقوم بإضافة المكونات الإضافية من مصدر البرنامج المساعد
date: 2023-12-01
categories:
- c++
- ue
catalog: true
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
description: سجل ببساطة كيفية إضافة مكون إضافي لـ UE عندما يكون لديك مصدر المكون الإضافي
figures: []
---

<meta property="og:title" content="UE 通过插件源码添加插件" />

#تم إضافة ملحق UE من خلال إضافة مصدر البرنامج النصي للملحق.

#إضافة مكون إضافي

> 简单记录一下如何在拥有插件源码的情况下添加插件.

باستخدام الإضافة [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)على سبيل المثال

وضع الشفرة المصدرية في دليل Plugins.
يرجى ترجمة النصوص التالية إلى اللغة العربية:

- يمكن تجاهل هذه الخطوة: قم بتعديل ملف .uproject للمشروع، وأضف تحت حقل الـ Plugins النص التالي:
    ```json
        "Plugins": [
        {
            "Name": "EditorPlus",
            "Enabled": true,
            "TargetAllowList": [
                "Editor"
            ]
        }
    ```
- انقر بزر الماوس الأيمن على ملف uproject، واختر "توليد ملفات مشروع Visual Studio"، لتحديث ملف مشروع sln.
- افتح ملف sln، وقم بتجميع المشروع

#تعيين اللغات المتعددة

قم بتعديل ملف إعدادات المشروع `DefaultEditor.ini`، وأضف المسار الجديد:

```ini
[Internationalization]
+LocalizationPaths=%GAMEDIR%Plugins/UE.EditorPlus/Content/Localization/EditorPlusTools
```


--8<-- "footer_ar.md"


> هذا المنشور تم ترجمته باستخدام ChatGPT، يرجى في [**التعليقات**](https://github.com/disenone/wiki_blog/issues/new)يرجى الإشارة إلى أي اهتمامات مفقودة. 
