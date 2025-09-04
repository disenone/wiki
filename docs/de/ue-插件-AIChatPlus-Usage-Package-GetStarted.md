---
layout: post
title: Packen
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
description: Einpacken
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - Package 篇 - Get Started" />

#Verpacken

##Pluginverpackung

Beim Verpacken von Unreal werden automatisch die erforderlichen DLL-Dateien für die Plugins gepackt. Du musst nur das Plugin aktivieren.

Beispielsweise für Windows werden beim Packen automatisch die Dateien llama.cpp und die entsprechenden CUDA-DLL-Dateien in das Verzeichnis nach dem Packen kopiert. Für andere Plattformen wie Android, Mac und IOS gilt dasselbe.

In der gepackten Entwicklerversion des Spiels können Sie den Befehl "AIChatPlus.PrintCllamaInfo" ausführen, um den aktuellen Cllama-Umgebungszustand zu überprüfen und zu bestätigen, ob alles normal ist und ob die GPU-Backend-Unterstützung aktiviert ist.

##Modellverpackung

Angenommen, die Modelldateien für das Projekt sind im Verzeichnis Content/LLAMA gespeichert, dann kann man beim Packen des Projekts dieses Verzeichnis einbeziehen:

Öffnen Sie die "Projekteinstellungen", wählen Sie den Reiter "Verpackung" aus, oder suchen Sie direkt nach "asset package". Suchen Sie nach der Einstellung "Zusätzliche Nicht-Asset-Verzeichnisse zum Verpacken" und fügen Sie das Verzeichnis "Content/LLAMA" hinzu.

![](assets/img/2024-ue-aichatplus/usage/package/getstarted_1.png)

Nachdem ein Inhaltsverzeichnis hinzugefügt wurde, packt Unreal automatisch alle Dateien im Verzeichnis während des Verpackungsvorgangs.

##Lesen Sie die verpackte Offline-Modelldatei.

Unreal packt normalerweise Projektdateien in eine .Pak-Datei. Wenn du dann den Dateipfad der Datei aus dem .Pak an das Offline-Modell Cllam übergibst, wird es fehlschlagen, da llama.cpp die verpackte Modelldatei in .Pak nicht direkt lesen kann.

Deshalb ist es erforderlich, zuerst die Modelldateien aus der .Pak-Datei ins Dateisystem zu kopieren. Das Plugin bietet eine praktische Funktion, um die Modelldateien direkt aus der .Pak-Datei zu kopieren und den Pfad der kopierten Dateien zurückzugeben, damit Cllama sie leicht lesen kann.

Die Blueprint-Node lautet "Cllama Prepare ModelFile In Pak": Sie kopiert automatisch Modelldateien aus dem Pak in das Dateisystem.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

Die Funktion des C++-Codes lautet:

```
#include <Cllama/AIChatPlusCllama_Util.h>

auto ModelPath = FAIChatPlusCllama_Util::PrepareModelFileInPak(InContentPath);
```

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt. Bitte gib dein [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Zeigen Sie alle übersehenen Stellen an. 
