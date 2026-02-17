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

#UE Plugin AIChatPlus Dokumentation

##Plugin-Marktplatz

[AIChatPlus](https://www.fab.com/zh-cn/listings/0e49d138-10e1-452e-ba07-9a4bea578ace)

##Öffentliches Lager

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Plugin-Beschreibung

Die neueste Version v2.0.0.

Dieses Plugin unterstützt UE5.2 bis UE5.7.

UE.AIChatPlus ist ein UnrealEngine-Plugin, das die Kommunikation mit verschiedenen GPT AI-Chatdiensten ermöglicht. Derzeit werden folgende Dienste unterstützt: OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama und llama.cpp für lokale Offline-Nutzung. In Zukunft werden weitere Dienstanbieter hinzukommen. Die Implementierung basiert auf asynchronen REST-Anfragen, die leistungsstark und für UE-Entwickler leicht zu integrieren sind, um auf diese AI-Chatdienste zuzugreifen.

Gleichzeitig enthält UE.AIChatPlus auch ein Editor-Tool, mit dem Sie diese AI-Chat-Dienste direkt im Editor nutzen können, um Texte und Bilder zu generieren sowie Bilder zu analysieren.

##Hauptfunktionen

**Neu!** Alle APIs unterstützen nun ToolCall.

**Neu!** OpenAI/Azure unterstützt Speech-to-Text und Text-to-Speech.

**Neu!** Blaupausen unterstützen jetzt Json.

**Neu!** Offline AI llama.cpp auf Version b6792 aktualisiert.

**Neu!** Offline AI llama.cpp mit Unterstützung für GPU Cuda und Metal.

**Neu!** Unterstützt Gemini Sprache-zu-Text.

**API**: Unterstützt OpenAI, Azure OpenAI, Claude, Gemini, Ollama, llama.cpp, DeepSeek

**Offline-Echtzeit-API**: Unterstützt den Offline-Betrieb von AI mit llama.cpp und ermöglicht die Nutzung von GPU Cuda und Metal.

**Text-zu-Text**: Verschiedene APIs unterstützen die Textgenerierung.

**Text zu Bild**: OpenAI Dall-E

**Bild zu Text**: OpenAI Vision, Claude, Gemini, Ollama, llama.cpp

**Bild-zu-Bild**: OpenAI Dall-E

**Spracherkennung**: Gemini

**Blueprint**: Alle APIs und Funktionen unterstützen Blueprint

**Editor Chat-Tool**: Ein funktionsreiches, sorgfältig gestaltetes KI-Chat-Tool für Editoren

**Asynchroner Aufruf**: Alle APIs können asynchron aufgerufen werden

**Praktische Werkzeuge**: Verschiedene Bild- und Audio-Tools

##Unterstützte APIs:

**Offline llama.cpp**: Integration mit der llama.cpp-Bibliothek ermöglicht das offline Ausführen von KI-Modellen! Unterstützt auch multimodale Modelle (experimentell). Kompatibel mit Win64/Mac/Android/iOS. GPU-Unterstützung für CUDA und METAL inklusive.

**OpenAI**: /chat/completions, /completions, /images/generations, /images/edits, /images/variations  

(Note: Since the original text consists mostly of technical terms and paths that are typically not translated (similar to URLs or commands), the German translation remains identical except for the possible addition of German quotation marks or formatting if required by context. In this case, no translation was needed beyond keeping the original terms.)

**Azure OpenAI**: /chat/completions, /images/generations

**Claude**：/nachrichten、/vollständig

**Gemini**: :generateText, :generateContent, :streamGenerateContent  

(Hinweis: Die Begriffe bleiben im Original, da es sich um technische Funktionen/APIs handelt, die meist nicht übersetzt werden.)

**Ollama**: /api/chat, /api/generate, /api/tags

**DeepSeek**: /chat/completions  
(Note: Since "DeepSeek" is a proper name and "/chat/completions" is likely a technical endpoint, they're typically kept as-is in German translations unless part of a full sentence requiring adaptation.)

##Gebrauchsanweisung

[**Anleitung zur Verwendung - Blaupausen**](ue-插件-AIChatPlus-Usage-Blueprint-GetStarted.md)

[**Anleitung zur Verwendung - C++ Teil**](ue-插件-AIChatPlus-Usage-Source-GetStarted.md)

[**Anleitung zur Verwendung - Editor-Teil**](ue-插件-AIChatPlus-Usage-EditorTool-GetStarted.md)

**[Gebrauchsanweisung - Verpackung](ue-插件-AIChatPlus-Usage-Package-GetStarted.md)

##Änderungsprotokoll

[**Änderungsprotokoll**](ue-插件-AIChatPlus-ChangeLogs.md)

##Technischer Support

**Kommentare**: Bei Fragen können Sie gerne einen Kommentar hinterlassen.

**E-Mail**: Sie können mir auch eine E-Mail schreiben (disenonec@gmail.com)

**discord**: Demnächst verfügbar

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt, bitte geben Sie Ihr [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Zeigen Sie auf etwaige Lücken hin. 
