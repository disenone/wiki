---
layout: post
title: UE lokale Mehrsprachigkeit einstellen
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
description: Aufzeichnung zur Implementierung von lokalisierter Mehrsprachigkeit in
  der UE
---

<meta property="og:title" content="UE 设置本地化多语言" />

#UE Localization Multilingual Settings

> Dokumentation zur Umsetzung von lokalisierter Mehrsprachigkeit in der UE

Wenn Sie mit dem UE-Erweiterungsmenü nicht vertraut sind, empfehle ich Ihnen, zuerst einen kurzen Blick darauf zu werfen: [UE-Erweiterungseditor-Menü](ue-扩展编辑器菜单.md)，[ue- Verwendung des Pfadformats zur Erweiterung des Menüs](ue-使用路径形式扩展菜单.md)

Der folgende Code basiert auf dem Plugin: [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##Funktionsbeschreibung

UE bringt integrierte Werkzeuge mit, die die Lokalisierung mehrerer Sprachen ermöglichen, zum Beispiel können wir die Menüführung des Editors lokalisieren:

Chinesisches Menü:

![](assets/img/2023-ue-localization/chinese.png)

Englisches Menü:

![](assets/img/2023-ue-localization/english.png)

##Code-Deklaration

Um die Menülokalisierung zu realisieren, müssen wir im Code die Strings, die von UE verarbeitet werden sollen, eindeutig deklarieren, indem wir die von UE definierten Makros `LOCTEXT` und `NSLOCTEXT` verwenden:

- Die globale Definition der Datei erfolgt, indem zunächst ein Makro namens `LOCTEXT_NAMESPACE` definiert wird, dessen Inhalt der aktuelle Namensraum des mehrsprachigen Textes ist. Danach können die Texte in der Datei mit `LOCTEXT` definiert werden. Am Ende der Datei wird das Makro `LOCTEXT_NAMESPACE` aufgehoben:

```cpp
// #define LOCTEXT(InKey, InTextLiteral)

#define LOCTEXT_NAMESPACE "EditorPlusTools"
LOCTEXT("Key", "Content");
#undef LOCTEXT_NAMESPACE

```

Lokale Definitionsmethode, verwenden Sie `NSLOCTEXT`, wenn Sie Text definieren, fügen Sie den Namensraumparameter hinzu:

```cpp
// #define NSLOCTEXT(InNamespace, InKey, InTextLiteral)

NSLOCTEXT("EditorPlusTools", "Key", "Content");
```

UE Tool sammelt alle Texte, die übersetzt werden müssen, indem es nach dem Auftreten der Makros `LOCTEXT` und `NSLOCTEXT` sucht.

##Verwenden Sie ein Werkzeug, um den Text zu übersetzen.

Angenommen, wir haben den folgenden Code zur Definition von Text:

```cpp
#define LOCTEXT_NAMESPACE "EditorPlusTools"
// register path node loctext
FEditorPlusPath::GetNodeByPath("/MenuTest")->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
FEditorPlusPath::GetNodeByPath("/MenuTest/<SubMenu>SubMenu1")->SetFriendlyName(LOCTEXT("SubMenu1", "SubMenu1"))->SetFriendlyTips(LOCTEXT("SubMenu1Tips", "SubMenu1Tips"));
FEditorPlusPath::GetNodeByPath("/MenuTest/<SubMenu>SubMenu1/<SubMenu>SubMenu1")->SetFriendlyName(LOCTEXT("SubMenu1", "SubMenu1"))->SetFriendlyTips(LOCTEXT("SubMenu1Tips", "SubMenu1Tips"));
FEditorPlusPath::GetNodeByPath("/<Hook>Help/<MenuBar>MenuTest/<SubMenu>SubMenu1/<Section>Section1")->SetFriendlyName(LOCTEXT("Section1", "Section1"))->SetFriendlyTips(LOCTEXT("Section1Tips", "Section1Tips"));
#undef LOCTEXT_NAMESPACE
```

Zuerst das Übersetzungstool öffnen, die Editor-Einstellungen aufrufen `Bearbeiten - Editor-Einstellungen`, und `Allgemein - Experimentelle Funktionen - Werkzeuge - Übersetzungsselector` auswählen:

![](assets/img/2023-ue-localization/editor_enable_tool.png)


Dann öffnen Sie das Übersetzungstool `Werkzeuge - Lokalisierungssteuerung`:

![](assets/img/2023-ue-localization/editor_open_tool.png)

Ein neues Ziel erstellen (es ist auch in der Standardeinstellung "Game" möglich, das Erstellen eines neuen Ziels dient der einfacheren Verwaltung und dem Verschieben dieser Übersetzungstexte)

![](assets/img/2023-ue-localization/tool_new_target.png)

Die Parameter für das Konfigurationsziel werden hier in `EditorPlusTools` umbenannt, die Ladepolitik ist `Editor`, die Daten stammen aus Textsammlungen und werden mit dem Plug-In-Verzeichnis ergänzt. Die Zielabhängigkeiten sind `Engine, Editor`, alle anderen Konfigurationen bleiben unverändert:

![](assets/img/2023-ue-localization/tool_target_config.png)

Add language support to ensure there are two language options available: Simplified Chinese and English. Make sure that when the mouse hovers over the language name, it displays 'zh-Hans' and 'en' respectively. Select English as the default language (since the text in our code is in English, we need to collect this English text here).

![](assets/img/2023-ue-localization/tool_target_lang.png)

Klicken Sie hier, um den Text zu sammeln:

![](assets/img/2023-ue-localization/tool_target_collect.png)

Es wird ein Sammel-Fortschrittsfenster angezeigt, warte auf erfolgreiche Sammlung, dann wird ein grüner Haken angezeigt:

![](assets/img/2023-ue-localization/tool_target_collected.png)

Schalten Sie das Fortschrittsfenster aus, um zum Übersetzungstool zurückzukehren. Dort können Sie in der englischen Zeile die gesammelte Anzahl sehen. Den englischen Text müssen wir nicht übersetzen; klicken Sie einfach auf die Schaltfläche zur Übersetzung in der chinesischen Zeile:

![](assets/img/2023-ue-localization/tool_go_trans.png)

Nachdem wir es geöffnet haben, können wir sehen, dass es im Bereich "Nicht übersetzt" Inhalte gibt. Geben Sie die übersetzten Inhalte in die rechte Spalte neben dem englischen Text ein. Nachdem alle Übersetzungen abgeschlossen sind, speichern Sie und schließen das Fenster.

![](assets/img/2023-ue-localization/tool_trans.png)

Klicken Sie auf "Wortanzahl", nach Abschluss sehen Sie die Anzahl der übersetzten Zeichen in der chinesischen Spalte.

![](assets/img/2023-ue-localization/tool_count.png)

Letzte kompilierte Texte:

![](assets/img/2023-ue-localization/tool_build.png)

Die übersetzten Daten werden im Verzeichnis `Content\Localization\EditorPlusTools` abgelegt, wobei für jede Sprache ein eigener Ordner erstellt wird. Im Ordner zh-Hans sind zwei Dateien zu finden: `.archive` enthält den gesammelten und übersetzten Text, während `.locres` die nach der Kompilierung erhaltenen Daten bezieht.

![](assets/img/2023-ue-localization/tool_ret.png)

![](assets/img/2023-ue-localization/tool_ret2.png)

##Die übersetzten Texte in das Plugin-Verzeichnis einfügen.

Wir haben die von unserem Plugin generierten Übersetzungstexte im Projektverzeichnis abgelegt. Wir müssen diese Texte in das Plugin verschieben, damit sie gemeinsam mit dem Plugin veröffentlicht werden können.

Bewege das Verzeichnis `Content\Localization\EditorPlusTools` in das Plugin-Verzeichnis Content, bei mir ist es `Plugins\UE.EditorPlus\Content\Localization\EditorPlusTools`.

Ändern Sie die Konfigurationsdatei `DefaultEditor.ini` und fügen Sie den neuen Pfad hinzu:

```ini
[Internationalization]
+LocalizationPaths=%GAMEDIR%Plugins/UE.EditorPlus/Content/Localization/EditorPlusTools
```

So können andere Projekte, nachdem sie das Plugin erhalten haben, die Übersetzungstexte direkt verwenden, indem sie einfach die `DefaultEditor.ini` ändern, ohne die Übersetzung neu konfigurieren zu müssen.

##Bitte beachten Sie die folgenden Hinweise.

Im Prozess der Erstellung von Übersetzungsdaten sind einige Probleme aufgetreten. Die folgenden Punkte sind zusammengefasst, auf die man achten sollte:

- Im Code müssen Texte mit den Makros `LOCTEXT` und `NSLOCTEXT` definiert werden. Der Text muss eine Zeichenkonstante sein, damit UE ihn sammeln kann.
- Der Name des Übersetzungsziels darf keine Symbole wie `.` enthalten, und die Verzeichnisnamen unter `Content\Localization\` dürfen ebenfalls kein `.` haben. UE wird nur den Namen vor dem `.` erfassen. Dies kann dazu führen, dass UE beim Lesen des Übersetzungstextes aufgrund eines falschen Namens nicht erfolgreich ist.
- Für das Editor-Plugin muss überprüft werden, ob der `IsRunningCommandlet()`-Modus aktiv ist; dann sollten weder das Menü noch die SlateUI generiert werden, da im Kommandozeilenmodus kein Slate-Modul vorhanden ist, was zu einem Fehler bei der Textsammlung führt: `Assertion failed: CurrentApplication.IsValid()`. Wenn du auf einen ähnlichen Fehler stößt, kannst du versuchen, diese Überprüfung hinzuzufügen. Genauer Fehlertext:

    > Assertion failed: CurrentApplication.IsValid() [File:E:\UE\ue5.3_git\Engine\Source\Runtime\Slate\Public\Framework\Application\SlateApplication.h] [Line: 255] 

    ![](assets/img/2023-ue-localization/tool_error.png)

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt, bitte im [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Zeigen Sie jegliches Übersehen des Mittelfingers auf. 
