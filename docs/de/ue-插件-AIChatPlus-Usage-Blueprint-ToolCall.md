---
layout: post
title: Tool Call
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
- Tool Call
- Function Calling
description: Tool Call
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Tool Call" />

#Blaupausen Kapitel - Werkzeugaufruf

Eine Werkzeugaufruf (Tool Call), auch bekannt als Funktionsaufruf (Function Calling), bezieht sich darauf, dass ein großes Modell basierend auf dem Dialoginhalt entscheiden kann, ob ein externes Werkzeug oder eine Funktion aufgerufen werden muss, um Informationen zu erhalten oder Aktionen auszuführen. Das Modell gibt den Namen der aufzurufenden Funktion und die Parameter zurück, die dann vom Entwickler ausgeführt werden, bevor das Ergebnis an das Modell zurückgegeben wird, um den Dialog fortzusetzen.

AIChatPlus unterstützt die Tool-Call-Funktion auf folgenden Plattformen:

* OpenAI
* Claude
* Gemini
* Ollama
* CllamaServer (llama.cpp Server)

##Die zentralen Konzepte

###Tool-Definition

Die Definition des Tools umfasst die folgenden Schlüsselfelder:

* **Typ**: Art des Tools, derzeit wird nur `Function` unterstützt
* **Name**: Funktionsname, darf nur aus den Zeichen a-z, A-Z, 0-9, Unterstrichen oder Bindestrichen bestehen, maximale Länge 64
* **Beschreibung**: Funktionsbeschreibung, das Modell nutzt diese, um zu bestimmen, wann die Funktion aufgerufen werden soll
* **Eigenschaften**: Die Funktionsparameterliste, wobei jeder Parameter Attribute wie Name, Beschreibung, Typ, Erforderlich usw. enthält.

###Tool Call Ablauf

Der vollständige Ablauf eines Tool Calls sieht wie folgt aus:

1. **Anfrage senden**: Schicke eine Chat-Anfrage mit Tools-Definitionen an das Modell.
2. **Modellbewertung**: Das Modell entscheidet anhand der Gesprächsinhalte, ob ein Toolaufruf erforderlich ist
3. **Zurückkehrende Tool Calls**: Falls ein Aufruf benötigt wird, gibt das Modell den Namen der aufzurufenden Funktion sowie die Parameter zurück.
4. **Funktionsausführung**: Der Entwickler führt den tatsächlichen Funktionsaufruf basierend auf den zurückgegebenen Informationen durch
5. **Ergebnis zurückgeben**: Das Ergebnis der Funktionenausführung wird als neue Nachricht an das Modell gesendet
6. **Fortsetzen des Dialogs**: Das Modell generiert eine endgültige Antwort basierend auf den Funktionsergebnissen.

##Beispiel für OpenAI Tool Call

Im Folgenden wird OpenAI als Beispiel verwendet, um zu demonstrieren, wie die Tool Call-Funktion genutzt werden kann.

###1. Definition Tool

Erstellen Sie zunächst die Tool-Definition. In diesem Beispiel definieren wir eine Funktion `get_delivery_date`, die das Zustelldatum eines Pakets abruft.

<!-- Bild benötigt: Erstellen des FAIChatPlus_ChatRequestTool-Knotens, Einstellung Type=Function, Name="get_current_weather", Description="Holen Sie sich das aktuelle Wetter an einem bestimmten Ort" -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_1.png)

###2. Definieren der Tool-Parameter

Füge dem Tool Properties (Parameter) hinzu. In diesem Beispiel fügen wir einen Parameter `order_id` vom Typ `string` hinzu und setzen ihn als erforderlich.

<!-- Bild benötigt: Erstellung des FAIChatPlus_ChatRequestToolProperty-Knotens, Einstellung Name="location", Beschreibung="Die Stadt und der Bundesstaat, z.B. San Francisco, CA", Typ="string", Pflichtfeld=true, und Verbindung durch Make Array mit dem Properties-Feld des Tools -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_2.png)

###3. Konfiguration Optionen

Erstelle den Knoten `OpenAI Chat Request Options`, setze den API-Schlüssel und das Modell und verbinde das Tools-Array mit den Optionen.

<!-- Bild benötigt: Erstellung des OpenAI Chat Request Options-Knotens, Einstellung von ApiKey, Model="gpt-4o-mini", Verbindung des oben genannten Tools mit dem Tools-Feld mittels Make Array -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_3.png)

###4. Nachrichten erstellen

Erstellen Sie eine Benutzernachricht, um Fragen zu Paketen zu stellen.

<!-- Benötigt ein Bild: Zeigt die Erstellung eines Messages-Arrays, Hinzufügen einer User Message mit dem Inhalt "Wie ist das Wetter heute in Boston?" -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_4.png)

###5. Anfrage senden und Tool Call verarbeiten

Erstellen Sie den Knoten `Send OpenAI Chat Request In World` und binden Sie das Ereignis `On Message Finished`. Holen Sie im Ereignisrückruf das ToolCalls-Array aus der Payload.

Wenn das Modell entscheidet, ein Tool aufzurufen, ist das ToolCalls-Array nicht leer. Durchlaufen Sie das Array, um Informationen über jeden Tool-Aufruf zu erhalten:

* **Id**: Die eindeutige Kennung des Tool Calls
* **Funktionsname**: Der aufzurufende Funktionsname
* **FunctionArguments**: Funktionsargumente (im JSON-String-Format)

<!-- Bild benötigt: Zeigt das vollständige Send Request-Blueprint, erstelle einen Send OpenAI Chat Request In World-Knoten, verbinde Options und Messages, binde das On Message Finished-Ereignis, verwende im Ereignisrückruf einen Break-Knoten, um ToolCalls aus der Payload zu extrahieren -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_5.png)

<!-- Benötigt Bild: Zeigt ein Blueprint zum Durchlaufen des ToolCalls-Arrays, verwendet For Each Loop zur Iteration, nutzt Break-Knoten für jedes Element, um die Felder Id, FunctionName und FunctionArguments abzurufen und gibt sie aus -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_6.png) -->

###6. Funktion ausführen und Ergebnis zurückgeben

Führe die entsprechende Funktionslogik basierend auf dem FunctionName aus (in diesem Beispiel wird simuliert, die Lieferzeit eines Pakets abzurufen) und gib das Ergebnis dann als Nachricht vom Typ ToolCallResult an das Modell zurück.

Erstellen einer neuen Nachricht, folgende Einstellungen sind erforderlich:

* **Rolle**: Auf `Werkzeug` gesetzt
* **Inhalt**: Das Ergebnis der Funktionsausführung
* **ToolCallResults**: Fügen Sie ein `FAIChatPlus_ChatRequestToolCallResult` hinzu, legen Sie die Id (mit der zuvor verwendeten Tool Call Id), FunctionName und FunctionResult fest

<!-- Benötigt ein Bild: Zeigt das Blueprint für die Erstellung einer Tool-Rollen-Nachricht, Erstellung einer neuen Message, Role=Tool, Content eingestellt auf simulierte Wetterdaten wie '{"temperature": "22", "unit": "celsius", "description": "Sunny"}', und fügt entsprechende Ergebnisinformationen in ToolCallResults hinzu -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_7.png)

###7. Konversation fortsetzen

Füge die Nachricht mit dem ToolCallResult-Ergebnis zum Nachrichtenverlauf hinzu und sende die Anfrage erneut. Das Modell generiert basierend auf den zurückgegebenen Funktionen eine abschließende Antwort in natürlicher Sprache.

<!-- Benötigt Bild: Zeigt das vollständige zweite Anforderungs-Blueprint, das die ursprüngliche User Message, die vom Modell zurückgegebene Assistant Message (einschließlich ToolCalls) und die Tool-Ergebnis-Message zu einem neuen Messages-Array kombiniert und erneut Send OpenAI Chat Request In World aufruft. -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_8.png)

<!-- ### 9. Vollständiger Bauplan -->

<!-- Die vollständige Blaupause eines Tool Calls sieht folgendermaßen aus: -->

<!-- Bild benötigt: Ablaufdiagramm des vollständigen Tool Call-Prozesses, einschließlich Tool-Definition, erste Anfrage, Tool Call-Verarbeitung und zweite Anfrage im vollständigen Prozess. -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_9.png) -->

### 10. Ergebnisse

<!-- Führen Sie das Blueprint aus, um eine natürlichsprachige Antwort mit Wetterinformationen zu sehen, die das Modell zurückgibt. -->

<!-- Bild benötigt: Screenshot der Ausführungsergebnisse anzeigen, auf dem der endgültige Antworttext des Modells zu sehen ist, ähnlich wie "Das aktuelle Wetter in Boston ist sonnig bei einer Temperatur von 22°C." -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_10.png) -->

##Fortgeschrittene Verwendung

###Mehrere Tools

Es können mehrere Tools gleichzeitig definiert werden, und das Modell wählt nach Bedarf aus, welche Funktionen aufgerufen werden sollen.

<!-- Bild benötigt: Ein Blueprint, der mehrere Tools definiert, beispielsweise die gleichzeitige Definition der beiden Tools get_current_weather und get_stock_price, die durch Make Array zu einem Tools-Array kombiniert werden -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_multi_tools.png)

###Komplexe Parametertypen

Tool-Parameter unterstützen verschiedene Typen. Über die Felder `ExtraJsonString` oder `ExtraJsonObject` können komplexere Parameterdefinitionen hinzugefügt werden, wie beispielsweise Aufzählungstypen:

```json
{"enum": ["Beijing", "HongKong"]}
```

<!-- Bild erforderlich: Eine Blueprint zeigen, die den ExtraJsonString verwendet, um Enumerationsparameter festzulegen, wobei im ExtraJsonString-Feld des Property-Knotens '{"enum": ["celsius", "fahrenheit"]}' eingetragen ist -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_extra_json.png)

###Andere Plattformen

Die Verwendung von Tool Call für Claude, Gemini, Ollama und CllamaServer ähnelt der von OpenAI. Sie müssen lediglich die entsprechenden Request- und Options-Knoten ersetzen. Die zentralen Datenstrukturen jeder Plattform (`FAIChatPlus_ChatRequestTool`, `FAIChatPlus_ChatResponseToolCall` usw.) sind universell.

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt. Bitte geben Sie Ihr Feedback unter [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Weisen Sie auf etwaige Auslassungen hin. 
