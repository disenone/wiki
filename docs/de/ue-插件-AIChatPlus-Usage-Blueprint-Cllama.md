---
layout: post
title: Cllama (llama.cpp) (veraltet)
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

#Blaupausen-Kapitel - Cllama (llama.cpp) (veraltet)

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_all.png)

##Verworfen

Cllama ist als **veraltet** markiert und wird nicht mehr gewartet.

Die ursprünglichen Funktionen von Cllama wurden von [CllamaServer](ue-插件-AIChatPlus-Usage-Blueprint-CllamaServer.md)zu tragen.

##Offline-Modell

Cllama basiert auf llama.cpp und ermöglicht die offline Nutzung von KI-Inferenzmodellen.

Da es sich um eine Offline-Version handelt, müssen wir zuerst die Modell-Datei vorbereiten, zum Beispiel durch Herunterladen des Offline-Modells von der HuggingFace-Website: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Platziere das Modell in einem bestimmten Ordner, zum Beispiel unter dem Verzeichnis des Spielprojekts unter Content/LLAMA.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA > ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Nachdem wir die Offline-Modelldateien haben, können wir mit Cllama KI-Chats durchführen.

##Text-Chat

Texterstellung mit Cllama

Erstelle einen Knoten mit Rechtsklick im Blueprint `Send Cllama Chat Request`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Erstelle einen Options-Knoten und setze `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Erstellen Sie Messages, fügen Sie jeweils eine System Message und eine User Message hinzu

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Erstelle einen Delegate, der die vom Modell ausgegebenen Informationen empfängt und auf dem Bildschirm ausgibt

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Die vollständige Blaupause sieht so aus. Führe die Blaupause aus, und du siehst den Spielbildschirm, der die vom großen Modell zurückgegebenen Nachrichten ausgibt.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

##Bild zu Text llava

Cllama unterstützt auch experimentell die llava-Bibliothek und bietet damit Vision-Funktionen.

Zuerst bereiten Sie die Multimodal-Offline-Modelldatei vor, zum Beispiel Moondream ([moondream2-text-model-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-text-model-f16.gguf), [moondream2-mmproj-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-mmproj-f16.gguf)) oder Qwen2-VL ([Qwen2-VL-7B-Instruct-Q8_0.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/Qwen2-VL-7B-Instruct-Q8_0.gguf), [mmproj-Qwen2-VL-7B-Instruct-f16.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/mmproj-Qwen2-VL-7B-Instruct-f16.gguf)）oder ein anderes von llama.cpp unterstütztes Multimodales Modell.

Erstellen Sie den Options-Knoten und setzen Sie die Parameter "Model Path" und "MMProject Model Path" jeweils auf die entsprechenden Multimodal-Modelldateien.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_1.png)

Erstellen Sie einen Knoten zum Lesen der Bilddatei flower.png und legen Sie die Messages fest.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_3.png)

Abschließend empfängt der letzte Knoten die zurückgegebenen Informationen und gibt sie auf dem Bildschirm aus. Die vollständige Blaupause sieht dann so aus:

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_4.png)

Führen Sie die Blaupause aus, um den zurückgegebenen Text zu sehen.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_5.png)

##llama.cpp mit GPU-Unterstützung

"Llama Chat-Anfrageoptionen" fügen den Parameter "Num Gpu Layer" hinzu, mit dem die GPU-Nutzlast von llama.cpp eingestellt werden kann, um die Anzahl der auf der GPU zu berechnenden Schichten zu steuern. Siehe Abbildung.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

## KeepAlive

"Cllama Chat Request Options" Fügt den Parameter "KeepAlive" hinzu, welcher ermöglicht, dass die eingelesene Modelldatei im Speicher behalten wird, um sie bei der nächsten Verwendung direkt nutzen zu können und so die Anzahl der Modell-Ladevorgänge zu reduzieren. KeepAlive gibt die Dauer an, für die das Modell im Speicher bleibt. 0 bedeutet keine Beibehaltung – das Modell wird nach der Verwendung sofort freigegeben; -1 bedeutet permanente Beibehaltung. Jede Anfrage mit gesetzten Options kann einen anderen KeepAlive-Wert haben, wobei der neue Wert den alten ersetzt. Beispielsweise können Sie für die ersten Anfragen KeepAlive=-1 setzen, um das Modell im Speicher zu behalten, bis Sie mit der letzten Anfrage KeepAlive=0 setzen, um die Modelldatei freizugeben.

##Verarbeitung von Modell-Dateien in gepackten .Pak-Dateien

Nachdem die Pak-Packung aktiviert wurde, werden alle Ressourcendateien des Projekts in der .Pak-Datei gespeichert, selbstverständlich inklusive der Offline-Modelldatei gguf.

Da llama.cpp keine direkte Unterstützung für das Lesen von .Pak-Dateien bietet, müssen die Offline-Modelldateien aus der .Pak-Datei in das Dateisystem kopiert werden.

AIChatPlus stellt eine Funktionsfunktion bereit, die automatisch Modelldateien aus .Pak-Dateien kopiert und im Saved-Ordner ablegt:

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

Oder Sie können die Modelldateien in der .Pak-Datei selbst verarbeiten. Der Schlüssel liegt darin, die Dateien herauszukopieren, da llama.cpp nicht in der Lage ist, .Pak-Dateien korrekt zu lesen.

##Funktionsknoten

Cllama bietet einige Funktionsknoten zur einfachen Abfrage des aktuellen Umgebungsstatus.


"Cllama Is Valid": Prüft, ob Cllama llama.cpp korrekt initialisiert wurde

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

"Cllama Is Support Gpu": Prüft, ob llama.cpp im aktuellen Umgebung GPU-Backend unterstützt

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"Cllama Get Support Backends": Ermittelt alle aktuell unterstützten Backends von llama.cpp


![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Cllama Prepare ModelFile In Pak": Kopiert automatisch die Modell-Dateien aus dem Pak in das Dateisystem.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)


--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt. Bitte geben Sie Ihr Feedback unter [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Weist auf etwaige Unvollständigkeiten hin. 
