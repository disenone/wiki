---
layout: post
title: Azure
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
description: Azure
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Azure" />

#Blueprint Section - Azure

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/azure_all.png)

Die Verwendung von Azure ähnelt auch sehr der von OpenAI, daher werde ich hier eine kurze Einführung geben.

##Textnachrichten

Erstellen Sie den Knoten "Azure Chat Options" und legen Sie die Parameter "Deployment Name", "Base Url" und "Api Key" fest.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/azure_chat_1.png)

Erstellen Sie einen "Messages" Knoten und verbinden Sie ihn mit "Azure Chat Request", klicken Sie auf Ausführen, um die Chat-Nachrichten von Azure auf dem Bildschirm angezeigt zu bekommen. Siehe Bild.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_chat_2.png)

##Erstellen von Bildern

Erstellen Sie den Knoten "Azure-Bildoptionen" und legen Sie die Parameter "Bereitstellungsname", "Basis-URL" und "API-Schlüssel" fest.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/azure_image_1.png)

Richten Sie die Knoten wie "Azure Image Request" ein, klicken Sie auf Ausführen, um die Chat-Nachrichten von Azure auf dem Bildschirm angezeigt zu bekommen. Siehe Abbildung.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_azure_blueprint_image_1.png)

Gemäß den Einstellungen des obigen Blaupausen wird das Bild unter dem Pfad D:\Dwnloads\butterfly.png gespeichert.

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt, bitte [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Zeigen Sie alle fehlenden Stellen. 
