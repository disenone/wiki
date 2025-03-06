---
layout: post
title: Get Started
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
description: Get Started
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Get Started" />

#Blueprint Section - Loslegen

![blueprint](assets/img/2024-ue-aichatplus/blueprint.png)

## Get Started

Im Folgenden wird am Beispiel von OpenAI die grundlegende Verwendungsmethode des Blaupausen vorgestellt.

###Textnachrichten

Verwenden Sie OpenAI für Textchats.

Erstellen Sie einen Knoten mit der rechten Maustaste in der Blaupause namens `Send OpenAI Chat Request In World`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Erstellen Sie den Options-Knoten und setzen Sie `Stream=True, API-Schlüssel="Ihr API-Schlüssel von OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Erstellen Sie Nachrichten, fügen Sie jeweils eine Systemnachricht und eine Benutzernachricht hinzu.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Erstellen Sie einen Delegaten, der die Ausgabeinformationen des Modells empfängt und auf dem Bildschirm ausgibt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Eine vollständige Blaupause sieht so aus: Wenn du die Blaupause ausführst, siehst du die Nachricht, die auf dem Bildschirm des Spiels gedruckt wird.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

###Dieser Text lautet auf Deutsch:

Dieser Text wird in ein Bild umgewandelt.

Verwenden Sie OpenAI, um Bilder zu erstellen.

Erstellen Sie in der Blaupause einen Knoten "Send OpenAI Image Request" mit der rechten Maustaste und legen Sie "In Prompt = 'ein schöner Schmetterling'" fest.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Erstellen Sie einen Options-Knoten und setzen Sie `Api Key="Ihr API-Schlüssel von OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Binden Sie das On Images-Ereignis und speichern Sie das Bild auf der lokalen Festplatte.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

Die vollständige Blaupause sieht so aus. Führen Sie die Blaupause aus, um zu sehen, dass das Bild an dem festgelegten Ort gespeichert wird.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

###Bild in Text umwandeln

Verwenden Sie OpenAI Vision zur Analyse von Bildern.

Erstellen Sie mit der rechten Maustaste einen Knoten namens "Send OpenAI Image Request" in der Blaupause.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_1.png)

Erstellen Sie den Options-Knoten und legen Sie `Api Key="Ihr API-Schlüssel von OpenAI"` fest. Setzen Sie das Modell auf `gpt-4o-mini`.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_2.png)

Erstellen von Nachrichten.
Erstelle zuerst einen Knoten mit dem Namen "Datei als Textur 2D importieren", um ein Bild aus dem Dateisystem zu laden.
Verwandle das Bild mit dem Knoten "Erstelle AIChatPlus-Textur aus Texture2D" in ein Objekt, das vom Plugin verwendet werden kann.
Verknüpfen Sie das Bild über den Knoten "Make Array" mit dem Feld "Images" des Knotens "AIChatPlus_ChatRequestMessage".
Setzen Sie den Inhalt des Feldes "Content" auf "Beschreiben Sie dieses Bild".

Wie im Bild:

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_3.png)

Das vollständige Muster sieht folgendermaßen aus, führen Sie das Muster aus, und Sie können die Ergebnisse auf dem Bildschirm sehen.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_4.png)

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt, bitte [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Zeigen Sie jede ausgelassene Stelle an. 
