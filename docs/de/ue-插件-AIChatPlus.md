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

#UE 插件 AIChatPlus 说明文档 --> UE Plugin AIChatPlus User Manual

##Plugin Store

[AIChatPlus](https://www.fab.com/zh-cn/listings/0e49d138-10e1-452e-ba07-9a4bea578ace)

##Öffentliches Lagerhaus

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Plugin introduction

Die neueste Version v1.6.0.

Dieses Plugin unterstützt UE5.2 - UE5.5.

UE.AIChatPlus ist ein UnrealEngine-Plugin, das die Kommunikation mit verschiedenen GPT-KI-Chat-Services ermöglicht. Derzeit werden Services von OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama und das lokale Offline-Tool llama.cpp unterstützt. In Zukunft werden noch mehr Service-Anbieter unterstützt. Die Implementierung basiert auf asynchronen REST-Anfragen, was eine effiziente Leistung gewährleistet und es UE-Entwicklern ermöglicht, diese KI-Chat-Services einfach zu integrieren.

UE.AIChatPlus enthält auch ein Editor-Tool, mit dem Sie die KI-Chat-Services direkt im Editor verwenden können, um Texte und Bilder zu generieren, Bilder zu analysieren usw.

##Hauptfunktion

**Brandneu!** Das Offline-KI-Programm llama.cpp wurde auf Version b4604 aktualisiert.

**Brandneu!** Die Offline-KI llama.cpp unterstützt GPU Cuda und Metal.

**Brandneu!** Unterstützung für die Gemini-Spracherkennung.

**API**: Unterstützt OpenAI, Azure OpenAI, Claude, Gemini, Ollama, Llama.cpp, DeepSeek

Offline Echtzeit-API: Unterstützt llama.cpp für das Offline-Ausführen von KI und unterstützt GPU Cuda und Metal.

**Text to text**: Various APIs support text generation.

**Text-to-Image**:
OpenAI DALL-E

**Bild-zu-Text**: OpenAI Vision, Claude, Gemini, Ollama, llama.cpp

**Image-to-Image**: OpenAI Dall-E

**Speech-to-Text**: Gemini

**Blueprint**: Alle APIs und Funktionen werden von dem Blueprint unterstützt.

**Editor Chat Tool**: Ein Editor AI-Chat-Tool, das reich an Funktionen ist und sorgfältig entwickelt wurde.

**Asynchrone Aufrufe**: Alle APIs können asynchron aufgerufen werden

**Praktische Werkzeuge**: verschiedene Bild- und Audio-Tools

##Unterstützte API:

**Offline llama.cpp:** Integriert mit der llama.cpp-Bibliothek, ermöglicht das Offline-Ausführen von KI-Modellen! Unterstützt auch multimodale Modelle (experimentell). Kompatibel mit Win64/Mac/Android/IOS. Unterstützt GPU CUDA und METAL.

OpenAI: /chat/completions, /completions, /images/generations, /images/edits, /images/variations

Azure OpenAI: /chat/completions, /images/generations

**Claude**：/Nachrichten、/Fertig

**Gemini**: generateText, generateContent, streamGenerateContent

**Ollama**: /api/chat, /api/generate, /api/tags

**DeepSeek**: /Chat/Vervollständigungen

##Gebrauchsanweisung

(ue-插件-AIChatPlus-Usage-Blueprint-GetStarted.md)

(ue-插件-AIChatPlus-Usage-Source-GetStarted.md)

[**Instructions for Use - Editor Section**](ue-插件-AIChatPlus-Usage-EditorTool-GetStarted.md)

##Ändern Sie das Protokoll.

[**Change log**](ue-插件-AIChatPlus-ChangeLogs.md)

##Technischer Support

**Kommentar**: Bei Fragen können Sie diese gerne im Kommentarbereich unten hinterlassen.

**E-Mail**: Sie können mir auch eine E-Mail an disenonec@gmail.com senden.

**discord**: Wird bald online gehen

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt. Bitte[**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Bitte weisen Sie auf etwaige Auslassungen hin. 
