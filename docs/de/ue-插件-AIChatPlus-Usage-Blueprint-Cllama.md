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

#Blueprint section - Cllama (llama.cpp)

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_all.png)

##Offline-Modell

Cllama wurde basierend auf llama.cpp entwickelt und unterstützt die offline Verwendung von KI-Inferenzmodellen.

Da es offline ist, müssen wir zuerst die Modelldatei vorbereiten, zum Beispiel das Offline-Modell von der HuggingFace-Website herunterladen: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Platzieren Sie das Modell in einem bestimmten Ordner, beispielsweise im Verzeichnis Content/LLAMA des Spielprojekts.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA > ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Nachdem wir die Offline-Modelldatei haben, können wir mit Cllama KI-Chats durchführen.

##Text-Chat

Verwenden Sie Cllama für Text-Chats.

Erstellen Sie in der Blaupause einen Knoten namens "Send Cllama Chat Request" mit der rechten Maustaste.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Erstellen Sie den Options-Knoten und legen Sie `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"` fest.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Erstellen Sie Nachrichten, fügen Sie jeweils eine Systemnachricht und eine Benutzernachricht hinzu.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Erstellen Sie einen Delegaten, der die Ausgabedaten des Modells empfängt und auf dem Bildschirm ausgibt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Das vollständige Blaupausenskript sieht so aus, führe das Skript aus und du wirst sehen, wie die Spielbildschirmanzeige die Nachricht zurückgibt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

##Erzeugen von Text aus Bildern llava

Cllama hat auch experimentelle Unterstützung für die llava-Bibliothek bereitgestellt, um die Fähigkeiten von Vision zu verbessern.

Please prepare the Multimodal offline model file first, such as Moondream ([moondream2-text-model-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-text-model-f16.gguf), [moondream2-mmproj-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-mmproj-f16.gguf)）oder Qwen2-VL（[Qwen2-VL-7B-Instruct-Q8_0.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/Qwen2-VL-7B-Instruct-Q8_0.gguf), [mmproj-Qwen2-VL-7B-Instruct-f16.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/mmproj-Qwen2-VL-7B-Instruct-f16.gguf)Bitte übersetzen Sie diesen Text ins Deutsche:

）oder ein anderes Multimodal-Modell, das von llama.cpp unterstützt wird.

Erstellen Sie einen Options-Knoten und setzen Sie die Parameter "Model Path" und "MMProject Model Path" auf die entsprechenden Multimodal-Modelldateien.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_1.png)

Erstellen Sie einen Knoten zum Lesen der Bilddatei flower.png und zum Setzen von Nachrichten.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_3.png)

Abschließend wird die empfangene Informationen erstellende Knoten erstellt und auf dem Bildschirm ausgegeben. Das vollständige Schaubild sieht folgendermaßen aus:

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_4.png)

Führen Sie die Blueprint aus, um den zurückgegebenen Text anzuzeigen.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_5.png)

##llama.cpp verwendet GPU

"Cllama Chat Request Options" has added the parameter "Num Gpu Layer," which can set the GPU payload of llama.cpp, allowing control over the number of layers that need to be computed on the GPU. See the image.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

## KeepAlive

"Cllama Chat Request Options" haben jetzt die zusätzliche Option "KeepAlive", mit der das geladene Modell im Speicher gehalten werden kann, um es bei Bedarf direkt zu nutzen und die Anzahl der Ladevorgänge zu reduzieren. KeepAlive definiert die Dauer, für die das Modell im Speicher gehalten wird. Eine Einstellung von 0 bedeutet, dass das Modell nicht gespeichert wird und sofort freigegeben wird, während -1 für eine unbegrenzte Speicherung steht. Für jede Anfrage können individuelle KeepAlive-Werte festgelegt werden. Neue Werte überschreiben dabei die alten; zum Beispiel kann man zu Beginn KeepAlive auf -1 setzen, um das Modell im Speicher zu behalten, und am Ende auf 0, um es freizugeben.

##Verarbeitung von Modelldateien in .Pak nach dem Verpacken.

Nachdem das Pak-Paket aktiviert wurde, werden alle Ressourcendateien des Projekts in der .Pak-Datei gespeichert, einschließlich der Offline-Modell gguf-Datei.

Da llama.cpp die direkte Leseunterstützung für .Pak-Dateien nicht unterstützt, müssen die Offline-Modelldateien aus der .Pak-Datei in das Dateisystem kopiert werden.

AIChatPlus bietet eine Funktion, die automatisch Modelldateien aus der .Pak-Datei kopiert und in den Ordner "Saved" platziert:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

Du könntest auch die Modelldateien in der .Pak-Datei selbst bearbeiten, es ist wichtig, die Dateien zu kopieren, da llama.cpp die .Pak-Datei nicht richtig lesen kann.

##Funktionstoken

Cllama bietet einige Funktionsknoten an, um den aktuellen Status in der Umgebung abzurufen.


"Cllama is valid" : Überprüfe Cllama llama.cpp, ob sie ordnungsgemäß initialisiert ist.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"Cllama is Support GPU": Überprüfen Sie, ob llama.cpp in der aktuellen Umgebung das GPU-Backend unterstützt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"Holen Sie sich Support-Backends von Cllama": Holen Sie alle Backends ab, die von der aktuellen llama.cpp unterstützt werden.


![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Cllama Prepare ModelFile In Pak": Automatisch Modelldateien aus Pak in das Dateisystem kopieren.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)


--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt, bitte bei [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Bitte identifizieren Sie jegliche ausgelassene Stellen. 
