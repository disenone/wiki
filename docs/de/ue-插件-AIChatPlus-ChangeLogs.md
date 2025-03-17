---
layout: post
title: Versionsprotokoll
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
description: Versionsprotokoll.
---

<meta property="og:title" content="UE 插件 AIChatPlus 版本日志" />

#UE Plugin AIChatPlus Version Log

## v1.6.2 - 2025.03.17

###Neue Funktion

Cllama erhöht den KeepContext-Parameter standardmäßig auf false. Der Kontext wird nach Beendigung des Chats automatisch gelöscht.

Cllama erhöht den KeepAlive-Parameter, um das wiederholte Lesen des Modells zu reduzieren.

## v1.6.1 - 2025.03.07

### Bug Fix

OpenAI Image Chat blueprint supports input images.

Editor-Tool Cllama mmproj 模型允许空

## v1.6.0 - 2025.03.02

###Neue Funktion

Upgrade der Datei llama.cpp auf Version b4604.

Cllama supports GPU backends: cuda and metal.

Das Chat-Tool Cllama unterstützt die Verwendung von GPU.

Unterstützung zum Lesen von Modelldateien aus einem gepackten Pak.

### Bug Fix

Fixing the issue where Cllama crashes when reloading during deduction.

Beheben Sie die Fehlermeldung beim Kompilieren von iOS.

## v1.5.1 - 2025.01.30

###Neue Funktion

Nur Gemini kann Audio abspielen.

Optimiere die Methode zum Abrufen von PCM-Daten, um die Audiodaten erst beim Generieren von B64 zu dekomprimieren.

Bitte hinzufügen von zwei Callbacks OnMessageFinished und OnImagesFinished.

Optimiere die Gemini-Methode, um automatisch die Methode basierend auf dem bStream zu erhalten.

Fügen Sie einige Blueprint-Funktionen hinzu, um das Wrapper in den tatsächlichen Typ umzuwandeln und die Response-Nachricht und Fehler abzurufen.

### Bug Fix

Behebung des Problems mit wiederholten Aufrufen von "Request Finish".

## v1.5.0 - 2025.01.29

###Neue Funktion

Unterstützung für die Audioausgabe an Gemini.

Die Editor-Tools unterstützen das Senden von Audio und Aufnahmen.

### Bug Fix

Beheben Sie den Fehler beim Kopieren der Sitzung.

## v1.4.1 - 2025.01.04

###Fehlerbehebung

Die Chat-Plattform ermöglicht das Versenden von Bildern ohne Text.

Reparatur des Problems beim Senden von Bildern über die OpenAI-Schnittstelle gescheitert.

Repair of missing parameters Quality, Style, ApiVersion in OpanAI and Azure chat tool settings.

## v1.4.0 - 2024.12.30

###Neue Funktion

* （Experimental feature）Cllama (llama.cpp) supports multimodal models and can handle images.

Alle Blueprint-Typenparameter wurden mit ausführlichen Hinweisen versehen.

## v1.3.4 - 2024.12.05

###Neue Funktion

OpenAI unterstützt die Vision-API.

###Problembehebung

Fix the error when OpenAI stream=false

## v1.3.3 - 2024.11.25

###Neue Funktion

Unterstützt UE-5.5

###Fehlerbehebung

Fixing some blueprints not working issue.

## v1.3.2 - 2024.10.10

###Problembehebung

Beheben Sie das Problem, bei dem cllama abstürzt, wenn der manuelle Stop-Befehl ausgeführt wird.

Behebung des Problems mit fehlenden ggml.dll und llama.dll Dateien in der heruntergeladenen Win-Version des Shops.

Beim Erstellen einer Anfrage wird überprüft, ob sich der Vorgang im GameThread befindet.

## v1.3.1 - 2024.9.30

###Neue Funktion

Fügen Sie einen SystemTemplateViewer hinzu, mit dem Sie Hunderte von Systemsatzvorlagen anzeigen und verwenden können.

###Problembehebung

Fix plugin downloaded from Marketplace, llama.cpp cannot find link library.

Reparatur des Problems mit zu langen Pfaden in LLAMACpp.

Behebe den Fehler mit der Verknüpfung der Llama.dll nach dem Windows-Paketieren.

Beheben Sie das Problem mit dem Lesen von Dateipfaden in iOS/Android.

Fixing the Cllame setting name error.

## v1.3.0 - 2024.9.23

###Wichtige neue Funktion.

Integrierte llama.cpp zur Unterstützung der lokalen Offline-Ausführung großer Modelle.

## v1.2.0 - 2024.08.20

###Neue Funktion

Unterstützung für OpenAI Image Edit/Image Variation.

Unterstützt die Ollama API, um automatisch eine Liste der von Ollama unterstützten Modelle abzurufen.

## v1.1.0 - 2024.08.07

###Neue Funktion

Unterstützung der Blaupause

## v1.0.0 - 2024.08.05

###Neue Funktion

Grundlegende vollständige Funktion.

Unnterstützung für OpenAI, Azure, Claude, Gemini.

Mit integriertem umfangreichen Editor für Chat-Funktionen.

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt, bitte geben Sie Ihr Feedback im [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Bitte identifizieren Sie jegliche Übersehen. 
