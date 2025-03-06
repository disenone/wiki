---
layout: post
title: Ollama
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
description: Ollama
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Ollama" />

#البلوبرنت - Ollama

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_all.png)

##الحصول على علماء

يمكنك الحصول على حزمة التثبيت محليًا من خلال موقع Ollama الرسمي: [ollama.com](https://ollama.com/)

يمكن استخدام واجهة برمجة التطبيقات Ollama المقدمة من قبل شخص آخر لاستخدام Ollama.

استخدام Ollama المحلي لتنزيل النماذج:

```shell
> ollama run qwen:latest
> ollama run moondream:latest
```

##الدردشة النصية

أنشئُ نقطة "Ollama Options"، واضبط المعلمات "Model"، "Base Url"، إذا كان Ollama يعمل محلياً، فإن "Base Url" عادةً ما يكون "http://localhost:11434"

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_chat_1.png)

ربط العقد "Ollama Request" بعقد "Messages" ذي الصلة، ثم قم بالنقر على تشغيل، حيث ستتمكن من رؤية الرسائل الدردشة التي يُرجعها Ollama على الشاشة. يُرجى الرجوع إلى الصورة.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

##إنشاء النصوص من الصور

علماء دعموا مكتبة llava ، وقدموا القدرة على Vision.

الرجاء توفير نص محدد للترجمة.

```shell
> ollama run moondream:latest
```

قم بتعيين العقد "Options"، واضبط "Model" على moondream:latest.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_1.png)

قراءة الصورة flower.png وضبط الرسالة

![flower.png](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_3.png)

اتصل بالعقد "Ollama Request"، انقر فوق تشغيل، وسترى رسائل الدردشة التي تمت طباعتها من قبل Ollama على الشاشة. كما هو موضح في الصورة.

![](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_4.png)

![](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_5.png)

--8<-- "footer_ar.md"


> This post was translated using ChatGPT, please provide [**feedback**](https://github.com/disenone/wiki_blog/issues/new)أشر على أي شيء تم تفويته بإصبع الوسطى. 
