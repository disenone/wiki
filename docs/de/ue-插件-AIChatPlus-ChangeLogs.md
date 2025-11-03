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
description: Versionsprotokoll
---

<meta property="og:title" content="UE 插件 AIChatPlus 版本日志" />

#UE 插件 AIChatPlus 版本日志

UE 插件 AIChatPlus 版本日志.

## v1.8.0 - 2025.11.03

Aktualisiere llama.cpp auf Version b6792.

## v1.7.0 - 2025.07.06

Aktualisiere llama.cpp auf Version b5536.

Unterstützt UE5.6.

Android 发布时会导致崩溃，禁用 llama.cpp。

## v1.6.2 - 2025.03.17

###Neue Funktion

Cllama erhöht den KeepContext-Parameter standardmäßig auf false. Der Kontext wird automatisch nach dem Ende des Chats gelöscht.

Cllama hat einen KeepAlive-Parameter hinzugefügt, der das wiederholte Lesen des Modells reduzieren kann.

## v1.6.1 - 2025.03.07

### Bug Fix

OpenAI Image Chat Blueprint unterstützt das Hochladen von Bildern.

Editor-Tool Cllama mmproj model allows void.

## v1.6.0 - 2025.03.02

###Neue Funktion

llama.cpp has been updated to version b4604.

Cllama unterstützt GPU-Backends: cuda und metal.

Das Chat-Tool Cllama unterstützt die Verwendung von GPU.

Unterstützung beim Lesen von Modelldateien aus einem gepackten Pak.

### Bug Fix

Fixing the issue where Cllama crashes when reloading during reasoning.

Beheben von Fehlern beim Kompilieren von iOS

## v1.5.1 - 2025.01.30

###Neue Funktion

Erlaubt nur Gemini, Audio abzuspielen.

Optimieren Sie die Methode zum Abrufen von PCM-Daten, um die Audiodaten erst beim Erzeugen von B64 zu dekomprimieren.

Bitte fügen Sie zwei Callbacks hinzu: OnMessageFinished und OnImagesFinished.

Optimiere die Gemini-Methode, um automatisch die Methode basierend auf bStream zu erhalten.

Fügen Sie einige Blueprint-Funktionen hinzu, um Wrapper in tatsächliche Typen umzuwandeln und Response-Nachrichten sowie Fehler abzurufen.

### Bug Fix

Behebung des Problems mit mehrfachem Aufruf von "Request Finish".

## v1.5.0 - 2025.01.29

###Neue Funktion

Unterstützung für die Audiowiedergabe an Gemini.

Die Editor-Tool unterstützt das Versenden von Audio und Aufnahmen.

### Bug Fix

Behebung des Fehlers beim Kopieren der Sitzungssitzung.

## v1.4.1 - 2025.01.04

###Problembehebung

Die Chat-Plattform ermöglicht das Versenden von Bildern ohne Text.

Reparieren des Problems beim Hochladen von Bildern über die OpenAI-Schnittstelle fehlgeschlagen.

Fix the issue of missing parameters Quality, Style, ApiVersion in the settings of OpanAI and Azure chat tools.

## v1.4.0 - 2024.12.30

###Neue Funktion

* (Experimental feature) Cllama (llama.cpp) supports multi-modal models and can process images.

Alle Blaupausen-Parameter wurden mit detaillierten Hinweisen versehen.

## v1.3.4 - 2024.12.05

###Neue Funktion

OpenAI unterstützt Vision-API.

###Problembehebung

Fixing the error when OpenAI stream=false.

## v1.3.3 - 2024.11.25

###Neue Funktion

Unterstützt UE-5.5

###Reparatur des Problems

Fixing an issue with some blueprints not working.

## v1.3.2 - 2024.10.10

###Fehlerbehebung

Behebe den Absturz von cllama, wenn das manuelle Stoppen der Anfrage fehlschlägt.

Fix für das Problem bei der Verpackung der heruntergeladenen Version von win im Store, bei dem die Dateien ggml.dll und llama.dll nicht gefunden werden können.

Überprüfen Sie beim Erstellen des Anforderungen, ob sich der Vorgang im GameThread befindet.

## v1.3.1 - 2024.9.30

###Neue Funktion

Fügen Sie einen SystemTemplateViewer hinzu, um Hunderte von Systemeinstellungs-Vorlagen anzuzeigen und zu nutzen.

###Problembehebung

Repariere das Plug-in, das aus dem Store heruntergeladen wurde. Llama.cpp konnte die Bibliothek nicht finden.

Behebung des Problems mit dem zu langen Pfad in LLAMACpp.

Behebung des llama.dll-Fehlers nach dem Verpacken von Windows.

Behebung des Problems mit dem Lesen von Dateipfaden unter iOS/Android.

Repariere den Fehler bei der Einstellung des Namens Cllame.

## v1.3.0 - 2024.9.23

###Signifikante neue Funktion

Integriert llama.cpp für die Unterstützung der lokalen Offline-Ausführung großer Modelle.

## v1.2.0 - 2024.08.20

###Neue Funktion

Unterstützung für OpenAI Image Edit/Image Variation.

Unterstützung der Ollama API, Unterstützung für automatisches Abrufen der Liste der Modelle, die von Ollama unterstützt werden.

## v1.1.0 - 2024.08.07

###Neue Funktion

Unterstützung der Blaupause

## v1.0.0 - 2024.08.05

###Neue Funktion

Grundlegende vollständige Funktionen

Unterstützt OpenAI, Azure, Claude, Gemini.

Mit einem integrierten Chat-Tool mit umfassenden Bearbeitungsfunktionen.

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt. Bitte geben Sie Ihr Feedback unter [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Bitte weisen Sie auf mögliche Auslassungen hin. 
