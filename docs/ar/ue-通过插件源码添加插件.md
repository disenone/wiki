---
layout: post
title: يرجى إضافة البرنامج التابع لـ UE عن طريق إضافة مصدر البرنامج إلى المكون الإضافي
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
description: سجّل ببساطة كيفية إضافة ملحقات لـ UE عندما تكون لديك مصدر الإضافة.
figures: []
---

<meta property="og:title" content="UE 通过插件源码添加插件" />

#عن طريق إضافة شفرة المصدر للإضافات، يُمكن لـ UE إضافة الإضافات.

#أضف إضافة

> سجّل بإيجاز كيفية إضافة إضافة عندما تكون لديك مصدر الإضافة.

من خلال الإضافة [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)لأخذ مثال

ضع الشيفرة المصدرية في دليل "الإضافات"
يمكنك ترك هذه الخطوة دون تنفيذها: قم بتعديل ملف .uproject للمشروع وأضف السطر التالي تحت حقل Plugins:
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
انقر بزر الماوس الأيمن على ملف uproject، ثم قم بتنفيذ "Generate Visual Studio Project Files" لتحديث ملفات مشروع sln.
افتح ملف sln، وقم بتجميع المشروع.

#قم بضبط اللغات المتعددة

عدل ملف تكوين المشروع `DefaultEditor.ini`، وأضف المسار الجديد:

```ini
[Internationalization]
+LocalizationPaths=%GAMEDIR%Plugins/UE.EditorPlus/Content/Localization/EditorPlusTools
```


--8<-- "footer_ar.md"


> هذه المشاركة تمت ترجمتها باستخدام ChatGPT، يرجى تقديم [**عودة**](https://github.com/disenone/wiki_blog/issues/new)أشير إلى أي نقص. 
