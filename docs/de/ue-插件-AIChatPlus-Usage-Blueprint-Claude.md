---
layout: post
title: Claude
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
description: Claude
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Claude" />

#Blueprint Chapter - Claude

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/claude_all.png)

##Textnachrichten

Erstellen Sie den Knoten "Optionen" und legen Sie die Parameter "Modell", "API-Key" und "Anthropic Version" fest.

![](assets/img/2024-ue-aichatplus/usage/blueprint/claude_chat_1.png)

Verbinden Sie den Knoten "Claude Request" mit dem entsprechenden "Messages"-Knoten, klicken Sie auf Ausführen, um die auf dem Bildschirm angezeigten Chat-Nachrichten von Claude zu sehen. Siehe Abbildung.

![](assets/img/2024-ue-aichatplus/usage/blueprint/claude_chat_2.png)

##Bild in Text umwandeln

Claude unterstützt auch die Vision-Funktion.

In der Blaupause mit der rechten Maustaste einen Knoten mit dem Namen `Send Claude Chat Request` erstellen.

![](assets/img/2024-ue-aichatplus/guide_claude_blueprint_1.png)

Erstellen Sie den Options-Knoten und legen Sie `Stream=true, Api Key="Ihr API-Schlüssel von Clude", Max Output Tokens=1024` fest.

![](assets/img/2024-ue-aichatplus/guide_claude_blueprint_2.png)

Erstellen Sie Nachrichten, indem Sie aus einer Datei Texture2D erstellen und aus Texture2D AIChatPlusTexture erstellen, und fügen Sie dann AIChatPlusTexture der Nachricht hinzu.

![](assets/img/2024-ue-aichatplus/guide_claude_blueprint_3.png)

Event and print the information on the game screen.

Die vollständige Blaupause sieht so aus. Wenn Sie die Blaupause ausführen, sehen Sie die Nachricht, die auf dem Bildschirm erscheint, wenn das große Modell gedruckt wird.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_claude_blueprint_5.png)


--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt. Bitte gib uns dein [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Bitte weisen Sie auf alle fehlenden Stellen hin. 
