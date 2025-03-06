---
layout: post
title: Gemini
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
description: Gemini
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Gemini" />

#Blueprint Chapter - Gemini

![](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_all.png)

###Textnachrichten

Erstellen Sie den Knoten "Gemini-Chat-Optionen" und geben Sie die Parameter "Modell" und "API-Schlüssel" ein.

![](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_chat_1.png)

Erstellen Sie den "Gemini Chat Request" Knoten und verbinden Sie ihn mit den "Options" und "Messages" Knoten. Klicken Sie auf Ausführen, um die auf dem Bildschirm angezeigten Chat-Nachrichten von Gemini zu sehen.

![](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_1.png)

![](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_chat_2.png)

###Generierung von Text aus Bildern

Erstellen Sie ebenfalls einen Knoten namens "Gemini Chat Options" und legen Sie die Parameter "Model" und "Api Key" fest.

Lade das Bild flower.png aus der Datei und setze es in "Messages".

![flower.png](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_vision_1.png)

Erstellen Sie einen "Gemini Chat Request" Knoten, klicken Sie auf Ausführen, um die Chat-Nachrichten anzeigen zu können, die von Gemini zurückgegeben werden, wie im Bild:

![](assets/img/2024-ue-aichatplus/usage/blueprint/gemini_vision_2.png)

###Audio in Text umwandeln.

Gemini unterstützt die Umwandlung von Audio in Text.

Erstellen Sie das folgende Schema, konfigurieren Sie das Laden von Audio, richten Sie die Gemini-Optionen ein, klicken Sie auf Ausführen. Auf dem Bildschirm sehen Sie dann die gedruckten Chat-Informationen, die nach der Audiobearbeitung durch Gemini zurückgegeben wurden.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_gemini_blueprint_sound_2.png)

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt. Bitte [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Weisen Sie auf etwaige Auslassungen hin. 
