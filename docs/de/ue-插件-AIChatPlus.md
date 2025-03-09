---
layout: post
title: Dokumentation
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
description: Dokumentation
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#UE 插件 AIChatPlus User Guide

##Plugin Store

[AIChatPlus](https://www.fab.com/zh-cn/listings/0e49d138-10e1-452e-ba07-9a4bea578ace)

##Gemeinschaftslager

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Plugin overview

Die neueste Version v1.6.0.

Dieses Plugin unterstützt UE5.2 - UE5.5.

UE.AIChatPlus ist ein UnrealEngine-Plugin, das die Kommunikation mit verschiedenen GPT AI-Chat-Services ermöglicht. Derzeit werden Dienste von OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama und llama.cpp (lokal offline) unterstützt. In Zukunft werden noch mehr Serviceanbieter unterstützt. Die Implementierung basiert auf asynchronen REST-Anfragen, was eine effiziente Leistung gewährleistet und es Entwicklern in der UnrealEngine ermöglicht, diese AI-Chat-Services zu integrieren.

UE.AIChatPlus enthält auch ein Editor-Tool, mit dem Sie direkt in der Editor-Oberfläche auf diese KI-Chat-Services zugreifen, Texte und Bilder erstellen sowie Bilder analysieren können.

##Hauptfunktion

**Brandneu!** Das Offline-KI-Programm Llama.cpp wurde auf Version b4604 aktualisiert.

**Brandneu!** Die Offline-KI llama.cpp unterstützt GPU Cuda und Metal.

Brandneu! Unterstützung für die Sprach-zu-Text-Funktion von Gemini.

**API**: Unterstützt OpenAI, Azure OpenAI, Claude, Gemini, Ollama, llama.cpp, DeepSeek

**Offline Real-time API**: Unterstützt das Ausführen der KI von llama.cpp offline und unterstützt GPU Cuda und Metal.

**Text-to-Text**: Textgenerierung wird von verschiedenen APIs unterstützt.

**Text-to-Image**: OpenAI Dall-E

**Bild-zu-Text**: OpenAI Vision, Claude, Gemini, Ollama, llama.cpp

**Image to Image**: OpenAI Dall-E

**Sprache-zu-Text**: Gemini

**Blueprint**: Alle APIs und Funktionen unterstützen die Blueprints.

**Editor-Chat-Tool**: Ein reichhaltiges und sorgfältig gestaltetes Editor-KI-Chat-Tool.

**Asynchrone Aufrufe**: Alle APIs können asynchron aufgerufen werden.

**Praktische Werkzeuge**: verschiedene Bild- und Audiowerkzeuge

##Unterstützte APIs:

"离线 llama.cpp": Integriert mit der llama.cpp-Bibliothek, ermöglicht das Offline-Ausführen von KI-Modellen! Unterstützt auch Multi-Modal-Modelle (experimentell). Kompatibel mit Win64/Mac/Android/IOS. Unterstützt GPU CUDA und METAL.

**OpenAI**: /chat/completions, /completions, /images/generations, /images/edits, /images/variations.

**Azure OpenAI**：/chat/completions、/images/generations

**Claude**: /Nachrichten, /vollständig

**Zwillinge**: generateText, generateContent, streamGenerateContent

**Ollama**: /api/chat, /api/generate, /api/tags

**DeepSeek**: /Chat/Vervollständigungen

##Gebrauchsanweisung

[**Instructions for Use - Blueprint Section**](ue-插件-AIChatPlus-Usage-Blueprint-GetStarted.md)

(ue-插件-AIChatPlus-Usage-Source-GetStarted.md)

(ue-插件-AIChatPlus-Usage-EditorTool-GetStarted.md)

(ue-插件-AIChatPlus-Usage-Package-GetStarted.md)

##Ändern Sie das Protokoll

(ue-插件-AIChatPlus-ChangeLogs.md)

##Technischer Support

**Kommentar**: Bei Fragen können Sie gerne unten einen Kommentar hinterlassen.

**E-Mail**: Sie können mir auch eine E-Mail senden (disenonec@gmail.com)

**Discord**: Coming soon.

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt. Bitte gib dein [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Weisen Sie auf etwaige Auslassungen hin. 
