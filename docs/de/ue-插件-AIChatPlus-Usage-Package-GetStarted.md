---
layout: post
title: Verpacken
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
description: Verpacken
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - Package 篇 - Get Started" />

#Verpacken.

##Plugin verpacken

Bei der Verpackung von Unreal werden automatisch alle erforderlichen dynamischen Bibliotheksdateien des Plugins mitverpackt, sodass das Plugin nur noch aktiviert werden muss.

Für Windows zum Beispiel werden bei der Verpackung automatisch die Dateien llama.cpp und die CUDA-bezogenen DLL-Dateien in das Verzeichnis nach dem Verpacken kopiert. Das gilt auch für andere Plattformen wie Android/Mac/iOS.

In der verpackten Entwicklerversion des Spiels können Sie den Befehl "AIChatPlus.PrintCllamaInfo" ausführen, um den aktuellen Zustand der Cllama-Umgebung zu überprüfen und zu bestätigen, ob der Zustand normal ist und ob die GPU-Backend-Unterstützung gegeben ist.

##Modellverpackung  


Die Modelldateien für das Projekt befinden sich im Verzeichnis "Content/LLAMA". Sie können dieses Verzeichnis beim Packen des Projekts einschließen:

Öffnen Sie die "Projekteinstellungen", wählen Sie die Registerkarte "Verpackung" oder suchen Sie direkt nach "Asset-Paket", um die Einstellung "Zusätzliche Nicht-Asset-Verzeichnisse zum Verpacken" zu finden. Fügen Sie das Verzeichnis "Content/LLAMA" hinzu.

![](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_6.png)

Nachdem du das Inhaltsverzeichnis hinzugefügt hast, packt Unreal beim Erstellen automatisch alle Dateien aus dem Verzeichnis mit ein.


##Laden Sie die verpackte Offline-Modelldatei.

Normalerweise packt Uneal alle Projektdateien in eine .Pak-Datei. Wenn Sie den Dateipfad der Dateien im .Pak an das Offline-Modell Cllam weitergeben, schlägt dies fehl, da llama.cpp die verpackte Modelldatei im .Pak nicht direkt lesen kann.

Daher ist es erforderlich, die Modelldateien aus der .Pak-Datei zuerst ins Dateisystem zu kopieren. Das Plugin bietet eine praktische Funktion, um die Modelldateien direkt aus der .Pak-Datei zu kopieren und den Pfad der kopierten Datei zurückzugeben, damit Cllama einfach darauf zugreifen kann.

Die Blueprint-Node lautet "Cllama Prepare ModelFile in Pak": Kopiert automatisch Modelldateien aus dem Pak in das Dateisystem.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

Der C++ Code lautet:

```
#include <Cllama/AIChatPlusCllama_Util.h>

auto ModelPath = FAIChatPlusCllama_Util::PrepareModelFileInPak(InContentPath);
```

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt, bitte gib dein [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Der Text lautet auf Deutsch: "Auf alle Übersehenen hinweisen." 
