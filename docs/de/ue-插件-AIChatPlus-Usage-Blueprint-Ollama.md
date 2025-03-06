---
layout: post
title: Ollama
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
description: Ollama
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Ollama" />

#Blueprint section - Ollama

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_all.png)

##Erhalten Sie Ollama

Sie können die Installationsdatei von der offiziellen Ollama-Website herunterladen und lokal installieren: [ollama.com](https://ollama.com/)

Sie können Ollama über die von anderen bereitgestellte Ollama-API verwenden.

Nutzen Sie Ollama, um Modelle lokal herunterzuladen:

```shell
> ollama run qwen:latest
> ollama run moondream:latest
```

##Textnachrichten.

Erstellen Sie den Knoten "Ollama Options" und legen Sie die Parameter "Model" und "Base Url" fest. Wenn Ollama lokal ausgeführt wird, ist die "Base Url" in der Regel "http://localhost:11434".

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_chat_1.png)

Verbinde den Knoten "Ollama Request" mit dem zugehörigen Knoten "Messages", klicke auf Ausführen, um die auf dem Bildschirm angezeigten Chat-Nachrichten von Ollama zu sehen. Siehe Abbildung.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_ollama_blueprint_chat_2.png)

##Bildgenerierungstext llava

Ollama also supports the llava library, providing the ability of Vision.

Zuerst laden Sie die Multimodal-Modelldatei herunter:

```shell
> ollama run moondream:latest
```

Setzen Sie den Knoten "Optionen" und wählen Sie "Modell" als moondream:latest.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_1.png)

Laden Sie das Bild flower.png und legen Sie die Nachricht fest.

![flower.png](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_3.png)

Verbinde den Knoten "Ollama Request", klicke auf "Ausführen" und du wirst die Chat-Nachrichten sehen, die Ollama zurückgibt. Siehe Abbildung.

![](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_4.png)

![](assets/img/2024-ue-aichatplus/usage/blueprint/ollama_vision_5.png)

--8<-- "footer_de.md"


> (https://github.com/disenone/wiki_blog/issues/new)Bitte weisen Sie auf etwaige Auslassungen hin. 
