---
layout: post
title: '### Version History'
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

#UE插件AIChatPlus版本日志

## v1.6.0 - 2025.03.02

###Neue Funktion

llama.cpp updated to version b4604

Cllama supports GPU backends: cuda and metal.

Das Chat-Tool Cllama unterstützt die Verwendung von GPU.

Unterstützung des Lesens von Modelldateien aus einem Paket (`.pak`).

### Bug Fix

Behebung des Problems beim Absturz von Cllama beim Neuladen während des Rätselns.

Beheben von Kompilierfehlern in iOS.

## v1.5.1 - 2025.01.30

###Neue Funktion.

Bitte übersetzen Sie den Text ins Deutsche:

* Nur Gemini darf Audio abspielen.

Optimierung der Methode zur Erstellung von PCMData, um die Audiodaten erst beim Generieren von B64 zu dekomprimieren.

Bitte hinzufügen Sie zwei Callbacks: OnMessageFinished und OnImagesFinished.

Optimiere die Gemini-Methode, um automatisch die Methode basierend auf bStream zu erhalten.

Fügen Sie einige Blaupausenfunktionen hinzu, um Wrapper in tatsächliche Typen umzuwandeln und Antwortnachrichten und Fehler abzurufen.

### Bug Fix

Beheben Sie das Problem mehrerer Aufrufe von Request Finish.

## v1.5.0 - 2025.01.29

###Neue Funktion

Unterstützung für das Senden von Audiodateien an Gemini.

Die Editor-Tools unterstützen das Versenden von Audio und Aufnahmen.

### Bug Fix

Behebung des Fehlers beim Kopieren der Sitzung.

## v1.4.1 - 2025.01.04

###Problembehebung

Die Chat-Anwendung ermöglicht das Versenden nur von Bildern ohne Nachrichten.

Reparatur des Problems mit dem Senden von Bildern über die OpenAI-Schnittstelle fehlgeschlagen.

Reparatur des fehlenden Parameters Quality, Style, ApiVersion in den Einstellungen von OpenAI und Azure-Chat-Tools =

## v1.4.0 - 2024.12.30

###Neue Funktion

* (Experimental Feature) Cllama (llama.cpp) supports multi-modal models and can process images.

Alle Blaupausen-Typenparameter wurden mit ausführlichen Hinweisen versehen.

## v1.3.4 - 2024.12.05

###Neue Funktion

OpenAI unterstützt Vision-API.

###Problembehebung

Fixing the error when OpenAI stream=false.

## v1.3.3 - 2024.11.25

###Neue Funktion

Unterstützt UE-5.5.

###Fehlerbehebung

Behebung des Problems, dass einige Blaupausen nicht funktionieren.

## v1.3.2 - 2024.10.10

###Fehlerbehebung

Behebung des Absturzes von cllama beim manuellen Stoppen der Anfrage.

Fix das Problem mit dem Fehlen der Dateien ggml.dll und llama.dll beim Packen der Win-Version des Shop-Downloads.

Beim Erstellen der Anfrage wird überprüft, ob sich dies im GameThread befindet.

## v1.3.1 - 2024.9.30

###Neue Funktion

Fügen Sie einen SystemTemplateViewer hinzu, um Hunderte von Systemeinstellungs-Vorlagen anzuzeigen und zu verwenden.

###Problembehebung

Beheben Sie das Problem mit dem Plugin, das aus dem App Store heruntergeladen wurde. Die Datei llama.cpp kann nicht auf die Bibliothek verweisen.

Behebung des Problems mit zu langen Pfaden in LLAMACpp.

Beheben Sie den Link-Fehler von llama.dll nach dem Windows-Paket.

Behebung des Problems beim Lesen von Dateipfaden in iOS/Android.

Repariere den Fehler beim Setzen des Namens in Cllame.

## v1.3.0 - 2024.9.23

###Wichtige neue Funktion

Integriert llama.cpp, unterstützt die lokale Offline-Ausführung von großen Modellen.

## v1.2.0 - 2024.08.20

###Neue Funktion

Unterstützung für OpenAI Image Edit/Image Variation.

Unterstützt die Ollama API und die automatische Erfassung der vom Ollama unterstützten Modellliste.

## v1.1.0 - 2024.08.07

###Neue Funktion

Unterstützung der Blaupause

## v1.0.0 - 2024.08.05

###Neue Funktion

Grundlegende vollständige Funktionen.

Unterstützung für OpenAI, Azure, Claude, Gemini.

Mit integriertem verbessertem Editor-Chat-Tool.

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt. Bitte teilen Sie uns [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Bitte weisen Sie auf eventuelle Auslassungen hin. 
