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

#Blueprint Section - Function Nodes

Das Plugin bietet zusätzliche praktische Blueprint-Funktionsknoten an.

##Cllama related

"Cllama Is Valid": Überprüfen ob Cllama llama.cpp ordnungsgemäß initialisiert wurde.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"Cllama unterstützt GPU"：Überprüfen, ob llama.cpp in der aktuellen Umgebung die GPU-Backend unterstützt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"Cllama Get Support Backends": Holen Sie sich alle Backends, die von llama.cpp unterstützt werden.


![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

„Cllama bereitet die Modelldatei in Pak vor“: Automatisches Kopieren der Modelldateien aus dem Pak in das Dateisystem.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

###Bildbezogen

"Convert UTexture2D to Base64": "Umwandeln von UTexture2D in Base64"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_5.png)

"UTexture2D in eine .png-Datei speichern"

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_6.png)

"Laden Sie die .png-Datei in UTexture2D."

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_7.png)

"Duplicate UTexture2D": Dupliziere UTexture2D

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_8.png)

###Audio-Related

"Laden Sie die .wav-Datei in USoundWave."

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_9.png)

"Konvertiere .WAV-Daten in USoundWave": 把 WAV-Binärdaten in USoundWave umwandeln.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_10.png)

"Save USoundWave to .wav file": USoundWave als .wav-Datei speichern.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_11.png)

"Holen Sie sich die USoundWave-Roh-PCM-Daten": Konvertieren Sie USoundWave in Binäraudiodaten.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_12.png)

"Konvertiere USoundWave in Base64": Konvertiere USoundWave in Base64-Daten

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_13.png)

"Duplicating USoundWave": Duplizieren von USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_14.png)

"Konvertiere Audio-Capture-Daten in USoundWave": Convert Audio Capture Data to USoundWave

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_15.png)

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt. Bitte im [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Zeigen Sie etwaige Auslassungen. 
