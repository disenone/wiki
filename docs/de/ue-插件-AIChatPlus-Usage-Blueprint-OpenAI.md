---
layout: post
title: OpenAI
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
description: OpenAI
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - OpenAI" />

#Blueprints - OpenAI

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_all.png)

Bei [Loslegen](ue-插件-AIChatPlus-Usage-Blueprint-GetStarted.md)Das Kapitel hat bereits die grundlegende Verwendung von OpenAI erläutert; hier werden wir nun detailliertere Anwendungen vorstellen.

##Textchat

Nutzen von OpenAI für Text-Chats

Im Blaupausendesign mit der rechten Maustaste einen Knoten namens `Send OpenAI Chat Request In World` erstellen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Erstellen Sie den Options-Knoten und legen Sie `Stream=true, Api Key="Ihren API-Schlüssel von OpenAI"` fest.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Erstellen Sie Nachrichten, fügen Sie jeweils eine Systemnachricht und eine Benutzer-Nachricht hinzu.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Erstellen Sie einen Delegaten, der die Ausgabeinformationen des Modells empfängt und auf dem Bildschirm druckt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Das vollständige Blaupausendesign sieht so aus, wenn die Blaupause ausgeführt wird, wird auf dem Bildschirm die Nachricht mit dem gedruckten Modell angezeigt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

##Dieser Text lautet: "Dieser Text wird als Bild generiert."

Verwenden von OpenAI zur Erstellung von Bildern.

Erstellen Sie in der Blaupause einen Knoten mit der rechten Maustaste mit dem Namen "Send OpenAI Image Request" und setzen Sie "In Prompt = 'einen schönen Schmetterling'" ein.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Erstellen Sie einen Options-Knoten und setzen Sie `Api Key="Ihr API-Schlüssel von OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Binden Sie das "On Images" Ereignis und speichern Sie das Bild auf der lokalen Festplatte.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

Die vollständige Blaupause sieht so aus, führen Sie die Blaupause aus und Sie sehen das Bild, das an dem festgelegten Ort gespeichert ist.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

##Erzeugung von Text aus Bildern

Verwenden Sie OpenAI Vision zur Analyse von Bildern.

Erstellen Sie einen Knoten mit der rechten Maustaste im Blueprint namens "Send OpenAI Image Request".

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_1.png)

Erstellen Sie den Options-Knoten und setzen Sie `Api Key="your api key from OpenAI"` und das Modell auf `gpt-4o-mini`.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_2.png)

Erstellen von Nachrichten.
Bitte erstellen Sie zunächst das Element "Datei als Textur 2D importieren" und laden Sie ein Bild aus dem Dateisystem.
Verwenden Sie den Knoten "Erstelle AIChatPlus-Textur aus Texture2D", um das Bild in ein für das Plugin verwendbares Objekt umzuwandeln.
Verbinde das Bild mit dem Node "AIChatPlus_ChatRequestMessage" über den "Make Array" Node mit dem Feld "Images".
Setzen Sie den Inhalt des Feldes "Content" auf "Beschreiben Sie dieses Bild".

Wie abgebildet:

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_3.png)

Eine vollständige Blaupause sieht so aus, führe sie aus und du wirst das Ergebnis auf dem Bildschirm sehen.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_4.png)

##Ändern Sie das Bild.

OpenAI unterstützt die Bearbeitung von markierten Bereichen in Bildern.

Bereite zunächst zwei Bilder vor.

Ein Bild, das bearbeitet werden muss: src.png

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_1.png)

Ein Bild mask.png, auf dem die Bereiche markiert sind, die geändert werden müssen, und durch Ändern des Ausgangsbildes kann die Transparenz der geänderten Bereiche auf 0 gesetzt werden, indem der Alphakanalwert auf 0 geändert wird.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_2.png)

Lesen Sie die beiden Fotos separat ein und kombinieren Sie sie zu einem Array.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_3.png)

Erstellen Sie den Knoten "OpenAI Image Options", setzen Sie ChatType = Edit und ändern Sie "Endpunkt-URL" = v1/images/edits.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_4.png)

Erstellen Sie eine "OpenAI Image Request", setzen Sie den "Prompt" auf "Verwandeln Sie sich in zwei Schmetterlinge", verbinden Sie den "Options" Knoten mit dem Bilderarray und speichern Sie das generierte Bild im Dateisystem.

The complete blueprint looks like this:

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_5.png)

Führen Sie das Blueprint aus, und speichern Sie das generierte Bild an der angegebenen Stelle.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_6.png)

##Bildvariante

OpenAI unterstützt die Erzeugung ähnlicher Varianten (Variationen) basierend auf einem eingegebenen Bild.

Zuerst bereite ein Bild mit dem Namen src.png vor und lade es in den Blueprint hoch.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_1.png)

Erstellen Sie den Knoten "OpenAI Bildoptionen", legen Sie ChatType auf Variation fest und ändern Sie "Endpunkt-URL" auf v1/images/variations.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_2.png)

Erstellen Sie "OpenAI Image Request", lassen Sie "Prompt" leer, verbinden Sie den "Options" Knoten mit dem Bild und speichern Sie das generierte Bild im Dateisystem.

Das vollständige Konzept sieht folgendermaßen aus:

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_3.png)

Führen Sie den Blueprint aus, und das generierte Bild wird an dem angegebenen Speicherort gespeichert.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_4.png)

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt. Bitte [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Benennen Sie bitte alle ausgebliebenen Stellen. 
