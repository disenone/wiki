---
layout: post
title: Cllama (llama.cpp)
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
- llama.cpp
description: Cllama (llama.cpp)
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Cllama (llama.cpp)" />

#Blueprint chapter - Cllama (llama.cpp)

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_all.png)

##Offline-Modell

Cllama wurde basierend auf llama.cpp entwickelt und unterstützt die Verwendung von KI-Inferenzmodellen offline.

Da die Verbindung getrennt ist, müssen wir zunächst die Modelldateien vorbereiten, zum Beispiel ein Offline-Modell von der HuggingFace-Website herunterladen: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Platzieren Sie das Modell in einem bestimmten Ordner, zum Beispiel im Verzeichnis Content/LLAMA des Spielprojekts.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA > ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Nachdem wir die Offline-Modelldatei haben, können wir mit Cllama AI-Chats durchführen.

##Textnachrichten

Verwenden Sie Cllama für Text-Chats.

In der Blaupause mit der rechten Maustaste einen Knoten namens `Send Cllama Chat Request` erstellen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Erstellen Sie den Options-Knoten und legen Sie `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"` fest.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Erstellen Sie Nachrichten, fügen Sie jeweils eine Systemnachricht und eine Benutzernachricht hinzu.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Erstellen Sie einen Delegierten, um die Ausgabedaten des Modells zu empfangen und auf dem Bildschirm anzuzeigen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Die vollständige Blaupause sieht so aus. Wenn du die Blaupause ausführst, siehst du die Nachrichten, die das Spiel auf dem Bildschirm ausgibt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

##Erzeugung von Text aus Bildern llava

Cllama hat auch experimentelle Unterstützung für die llava-Bibliothek hinzugefügt, die die Fähigkeit von Vision bietet.

Bereiten Sie zunächst die Multimodal Offline-Modelldatei vor, z. B. Moondream ([moondream2-text-model-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-text-model-f16.gguf), [moondream2-mmproj-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-mmproj-f16.gguf)）或者 Qwen2-VL（[Qwen2-VL-7B-Instruct-Q8_0.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/Qwen2-VL-7B-Instruct-Q8_0.gguf), [mmproj-Qwen2-VL-7B-Instruct-f16.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/mmproj-Qwen2-VL-7B-Instruct-f16.gguf)）oder ein anderes von llama.cpp unterstütztes Multimodal-Modell.

Erstellen Sie den Options-Knoten und setzen Sie die Parameter "Model Path" und "MMProject Model Path" auf die entsprechenden Multimodal-Modelldateien.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_1.png)

Erstellen Sie einen Knoten zum Lesen der Bilddatei flower.png und setzen Sie die Nachrichten.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_3.png)

Schließlich wird die erstellte Node die zurückgegebenen Informationen empfangen und auf dem Bildschirm ausgeben. Das vollständige Blueprint sieht dann wie folgt aus:

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_4.png)

Führen Sie die Blaupause aus, um den zurückgegebenen Text anzuzeigen.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_5.png)

##llama.cpp verwendet die GPU.

"Füge dem Parameter 'Num Gpu Layer' in den 'Cllama Chat Request Options' hinzu, um das GPU-Payload in der 'llama.cpp' zu konfigurieren. Dadurch lässt sich die Anzahl der Ebenen festlegen, die auf der GPU berechnet werden sollen. Siehe Abbildung."

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

##Behandlung von Modelldateien in einer .Pak-Datei nach dem Verpacken.

Nachdem das Pak-Paket erstellt wurde, werden alle Ressourcen des Projekts in der .Pak-Datei gespeichert, einschließlich der Offline-Modelldatei gguf.

Aufgrund der Unfähigkeit von llama.cpp, .Pak-Dateien direkt zu lesen, müssen die Offline-Modelldateien aus der .Pak-Datei ins Dateisystem kopiert werden.

AIChatPlus bietet eine Funktion, die automatisch Modelldateien aus der .Pak kopiert und in den Ordner "Saved" platziert.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

Alternativ kannst du die Modelldateien in der .Pak-Datei selbst bearbeiten, das Wichtige ist, die Dateien herauszukopieren, weil llama.cpp die .Pak-Datei nicht korrekt lesen kann.

##Funktionsknoten

Cllama bietet einige Funktionen, um den aktuellen Status in der Umgebung abzurufen.


"Cllama Is Valid"：Verify if Cllama llama.cpp is properly initialized.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"Cllama unterstützt GPU": Überprüfen, ob die Datei llama.cpp in der aktuellen Umgebung das GPU-Backend unterstützt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"Holen Sie sich Support-Backends von Llama": Fetch all backends supported by the current llama.cpp.


![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Cllama Prepare ModelFile In Pak": Kopiert automatisch die Modelldatei(en) aus dem Pak in das Dateisystem.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)


--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt. Bitte gib uns dein [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Bitte weisen Sie auf etwaige Auslassungen hin. 
