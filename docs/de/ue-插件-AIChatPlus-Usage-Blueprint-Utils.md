---
layout: post
title: Funktionsknoten
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
description: Funktionsknoten
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - 功能节点" />

#Blauer Druck - Funktionsknoten

Das Plugin bietet zusätzliche nützliche Blueprint-Funktionsknoten.

##Cllama related

"Cllama ist gültig"：Checken, ob Cllama llama.cpp ordnungsgemäß initialisiert wurde.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"Cllama unterstützt GPU" bedeutet, dass überprüft werden soll, ob die Datei llama.cpp die GPU-Unterstützung in der aktuellen Umgebung bietet.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"Holen Sie sich die unterstützten Backends von llama.cpp": Get all backends supported by llama.cpp.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Cllama Prepare ModelFile In Pak": Automatisch kopiert die Modelldatei(en) aus dem Pak in das Dateisystem

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

##Bildbezogen

"Konvertieren von UTexture2D in Base64": Konvertiere das Bild von UTexture2D in das PNG Base64-Format.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_5.png)

"Speichern Sie UTexture2D als .png-Datei": Speichern Sie UTexture2D als .png-Datei

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_6.png)

"Laden Sie die .png-Datei in den UTexture2D"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_7.png)

"Duplicate UTexture2D": Kopiere UTexture2D

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_8.png)

##Audio-related

"Laden Sie die .wav-Datei in USoundWave."

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_9.png)

Konvertiere `.wav`-Daten in `USoundWave`: 把 wav 二进制数据转成 USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_10.png)

"USoundWave als .wav-Datei speichern"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_11.png)

"Holen Sie sich die USoundWave-Roh-PCM-Daten": Convert USoundWave in binäre Audiodaten.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_12.png)

"USoundWave" in Base64 umwandeln: 把 USoundWave 转成 Base64 数据

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_13.png)

"Duplicate USoundWave": Kopiere USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_14.png)

"Konvertiere Audioaufnahmedaten in USoundWave": 把 Audio Capture 录音数据转成 USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_15.png)

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt. Bitte geben Sie Ihr Feedback unter [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Bitte identifizieren Sie mögliche Auslassungen. 
