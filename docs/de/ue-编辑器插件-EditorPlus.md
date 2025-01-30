---
layout: post
title: UE.EditorPlus Documentation
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
description: UE 编辑器插件 UE.EditorPlus 说明文档  ⟶  UE EditorPlus Plugin Erklärungsdokument
---

<meta property="og:title" content="UE 编辑器插件 EditorPlus 说明文档" />

#UE 编辑器插件 UE.EditorPlus 说明文档 

würde ins Deutsche übersetzt:

 UE EditorPlus-Editor-Plugin-Dokumentation.

##Vorstellungsvideo

![type:video](assets/img/2024-ue-editorplus/market/video.mp4)

##Die Übersetzung lautet: "Plugin-Quellcode".

[UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##Marktplatz herunterladen

[EditorPlus](https://www.unrealengine.com/marketplace/zh-CN/product/editorplus)

##Please translate the following text into German language:

Projekt hinzugefügtes Quellcode-Plugin EU.EditorPlus

Referenzdokument:

-  Deutsch: [Durch das Hinzufügen von Plug-In-Quellcode fügt UE Plug-Ins hinzu](https://wiki.disenone.site/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)
- English: [UE adds plugins through the plugin source code](https://wiki.disenone.site/en/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)


##Plug-in description

UE.EditorPlus ist ein Plugin für den UE-Editor, das eine bequeme Möglichkeit bietet, das Editor-Menü zu erweitern, und unterstützt fortgeschrittene Erweiterungen, während es einige nützliche Editorenwerkzeuge enthält. Dieses Plugin unterstützt UE5.3+.


##Erweitere den Editor-Menü.

![](assets/img/2024-ue-editorplus/menu.png)

![](assets/img/2024-ue-editorplus/toolbar.png)

###Erklärung

Unterstützung für verschiedene Möglichkeiten zur Erweiterung des Editors-Menüs:

Pfadmethode: `RegisterPathAction("/<MenuBar>Leiste/<SubMenu>Untermenü/<Command>Aktion")`
- Instanziierungsart: `EP_NEW_MENU(FEditorPlusMenuBar)("Bar")`
Mischmethode: `RegisterPath("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action",EP_NEW_MENU(FEditorPlusCommand)("Action")`

###Pfadmodus

Sie können einen Editor-Menübefehl auf folgende Weise registrieren:

```cpp
FEditorPlusPath::RegisterPathAction(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action",
    FExecuteAction::CreateLambda([]
        {
            // do action
        })
);
```

Auf diese Weise können Sie im Editor-Menü Hilfe eine Menüleiste "Bar" hinzufügen, in der dann ein Untermenü "SubMenu" mit einer Aktion "Action" erstellt wird.

Die vollständige Pfadformatierung würde wie folgt aussehen: `/<Hook>HookName/<Type1>Name1/<Type2>Name2`, wobei der erste Pfad `<Hook>` sein muss. Die derzeit unterstützten Typen und Einschränkungen sind:

- `<Hook>`: Gibt an, an welcher Stelle des Hooks das Menü generiert werden soll; der nachfolgende Pfad darf kein `<Hook>` enthalten.
- `<MenuBar>`: Menüleiste, der Pfad hinten darf nicht `<Hook>, <MenuBar>, <ToolBar>` enthalten.
- `<ToolBar>`: Symbolleiste, darf nicht `<Hook>, <MenuBar>, <ToolBar>` hinter dem Pfad stehen.
- `<Section>`: Menüabschnitt, der nachfolgende Pfad darf keine `<Hook>, <MenuBar>, <Section>` enthalten.
- `<Separator>`: Menü-Trennzeichen, der nachfolgende Pfad darf kein `<Hook>, <MenuBar>` enthalten.
- `<SubMenu>`: Untermenü, der nachfolgende Pfad darf kein `<Hook>, <MenuBar>` enthalten.
- `<Command>`: Menübefehl, es dürfen keine Pfade folgen.
- `<Widget>`: Mehr anpassbare Slate UI-Komponenten für Erweiterungen, ohne nachfolgende Pfade.

Eine einfachere Pfadform: `/BarName/SubMenuName1/SubMenuName2/CommandName`. Wenn kein Typ angegeben ist, ist das erste Element des Pfades `<MenuBar>`, das mittlere `<SubMenu>` und das letzte `<Command>`.

Falls `<Hook>` nicht angegeben ist, wird automatisch `<Hook>Help` vorangestellt, um anzugeben, dass die Menüleiste nach dem Hilfe-Menü hinzugefügt werden soll.

###Instanziierungsart

Der Pfadmodus instanziiert automatisch alle Knoten basierend auf ihrem Typ und den Standardparametern. Wir können jedoch auch selbst die Instanziierung steuern, um die Inhalte der Erweiterungen detaillierter zu kontrollieren.

```cpp
EP_NEW_MENU(FEditorPlusMenuBar)("MyBar", "MyBar", LOCTEXT("MyBar", "MyBar"), LOCTEXT("MyBarTips", "MyBarTips"))
->RegisterPath()
->Content({
    EP_NEW_MENU(FEditorPlusSubMenu)("MySubMenu")
    ->Content({
        EP_NEW_MENU(FEditorPlusCommand)("MyAction")
        ->BindAction(FExecuteAction::CreateLambda([]
            {
                // do action
            })),
    })
});
```

Beim Instanziieren von `MyBar` kann der Hook-Name, der lokalisierte Name und die lokalisierte Hinweisparameter übergeben werden (`"MyBar", LOCTEXT("MyBar", "MyBar"), LOCTEXT("MyBarTips", "MyBarTips")`). Der obige Code entspricht dem Pfadansatz `/<Hook>Help/<MenuBar>MyBar/<SubMenu>MySubMenu/<Command>MyAction`.

###Gemischte Methode

Natürlich können auch beide Methoden kombiniert werden:

```cpp
FEditorPlusPath::RegisterPath(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action",
    EP_NEW_MENU(FEditorPlusCommand)("Action")
    ->BindAction(FExecuteAction::CreateLambda([]
        {
            // do action
        })),
);
```

In this case, the plugin will automatically instantiate the nodes of the intermediate paths, while the final path will use nodes instantiated by the user themselves.

###Mehr Beispiele

Headerdatei:

```cpp
#include <EditorPlusPath.h>
```

Der Pfad gibt an, welche Sprache für die Lokalisierung verwendet wird. 'EP_FNAME_HOOK_AUTO' bedeutet, dass der Namen des Betreffs automatisch aus dem Pfadnamen entnommen wird.

```cpp
FEditorPlusPath::RegisterPathAction(
        "/Bar/Action",
        FExecuteAction::CreateLambda([]
        {
            // do action
        }),
        EP_FNAME_HOOK_AUTO,
        LOCTEXT("Action", "Action"),
        LOCTEXT("ActionTips", "ActionTips"));
```

Durch den Pfad Knoten abrufen und lokalisierte Texte festlegen:

```cpp
FEditorPlusPath::GetNodeByPath("/MenuTest")
    ->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))
    ->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
```


Fügen Sie am Ende des Pfades ein Slate UI-Steuerlement hinzu.

```cpp
FEditorPlusPath::RegisterPath(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Widget>Widget",
    EP_NEW_MENU(FEditorPlusWidget)("Widget", LOCTEXT("Widget", "Widget"))
        ->BindWidget(SNew(SHorizontalBox)));
);
```

Neue Knoten im mit UE mitgelieferten Hook hinzufügen.

```cpp
FEditorPlusPath::RegisterPath("<Hook>EpicGamesHelp/<Separator>ExtendSeparator")
```

Mehrfach erklärte denselben Pfad werden als derselbe Pfad erkannt, sodass der gleiche Pfad kontinuierlich erweitert werden kann.

```cpp
FEditorPlusPath::RegisterPathAction("/MenuTest/SubMenu1/SubMenu1/Path1", Action, EP_FNAME_HOOK_AUTO, LOCTEXT("Path1", "Path1"), LOCTEXT("Path1Tips", "Path1Tips"));
FEditorPlusPath::RegisterPathAction("/MenuTest/SubMenu1/SubMenu1/Path2", Action, EP_FNAME_HOOK_AUTO, LOCTEXT("Path2", "Path2"), LOCTEXT("Path2Tips", "Path2Tips"));
```

Für einen Knoten den Pfad weiter ausbauen.

```cpp
auto node = FEditorPlusPath::GetNodeByPath("/MenuTest");
FEditorPlusPath::RegisterChildPath(node, "<SubMenu>Sub/<Separator>Sep");
```

Einen Pfad löschen.

```cpp
FEditorPlusPath::UnregisterPath("/MenuTest/SubMenu1/SubMenu1/Path1");
```

Erweiterungswerkzeugleiste
```cpp
FEditorPlusPath::RegisterPath("/<Hook>ProjectSettings/<ToolBar>MenuTestToolBar")
->Content({
    EP_NEW_MENU(FEditorPlusCommand)("ToolBarCommand1")
    ->BindAction(...)
});
```

###Schnittstellenbeschreibung

```cpp
class EDITORPLUS_API FEditorPlusPath
{
public:

	static TSharedPtr<FEditorPlusMenuBase> RegisterPath(const FString& Path, const TSharedPtr<FEditorPlusMenuBase>& Menu=nullptr);
	static TSharedPtr<FEditorPlusMenuBase> RegisterPath(const FString& Path, const FText& FriendlyName, const FText& FriendlyTips);
	static TSharedPtr<FEditorPlusMenuBase> RegisterPathAction(
		const FString& Path, const FExecuteAction& ExecuteAction, const FName& Hook=EP_FNAME_HOOK_AUTO,
		const FText& FriendlyName=FText::GetEmpty(), const FText& FriendlyTips=FText::GetEmpty());

	static TSharedPtr<FEditorPlusMenuBase> RegisterChildPath(
		const TSharedRef<FEditorPlusMenuBase>& InParent, const FString& Path, const TSharedPtr<FEditorPlusMenuBase>& Menu=nullptr);
	static TSharedPtr<FEditorPlusMenuBase> RegisterChildPath(
		const TSharedRef<FEditorPlusMenuBase>& InParent, const FString& Path, const FText& FriendlyName, const FText& FriendlyTips);
	static TSharedPtr<FEditorPlusMenuBase> RegisterChildPathAction(
		const TSharedRef<FEditorPlusMenuBase>& InParent, const FString& Path, const FExecuteAction& ExecuteAction,
		const FName& Hook=EP_FNAME_HOOK_AUTO, const FText& FriendlyName=FText::GetEmpty(), const FText& FriendlyTips=FText::GetEmpty());

	static bool UnregisterPath(
		const FString& Path, const TSharedPtr<FEditorPlusMenuBase>& Leaf=nullptr);

	static TSharedPtr<FEditorPlusMenuBase> GetNodeByPath(const FString& Path);
};
```

- `RegisterPath`: Menüpfad erstellen
- `RegisterPathAction`: Erzeugt ein Pfadmenü und bindet automatisch eine Aktion an das Endknoten `<Command>` Knoten.
`RegisterChildPath`：Generieren Sie fortlaufende Unterpfade für den angegebenen Knoten.
- `RegisterChildPathAction`: Fortsetzung der Generierung von Unterpfaden für den angegebenen Knoten und automatische Bindung der Aktion
- `UnregisterPath`: Löschen des Pfads. `Leaf` kann in Fällen verwendet werden, in denen mehrere Endknoten denselben Namen haben, um eine genaue Übereinstimmung festzulegen. Während des Löschvorgangs wird auf mittlere Knoten zurückverfolgt, und sobald ein mittlerer Knoten keine Unterstützung hat, wird er ebenfalls gelöscht.
- `GetNodeByPath`: Holen Sie den Knoten anhand des Pfads.


Knotentyp

```cpp
// base class of all node
class EDITORPLUS_API FEditorPlusMenuBase: public TSharedFromThis<FEditorPlusMenuBase> {}

class EDITORPLUS_API FEditorPlusHook: public TEditorPlusMenuBaseRoot {}

class EDITORPLUS_API FEditorPlusMenuBar: public TEditorPlusMenuBaseNode {}

class EDITORPLUS_API FEditorPlusToolBar: public TEditorPlusMenuBaseNode {}

class EDITORPLUS_API FEditorPlusSection: public TEditorPlusMenuBaseNode {}

class EDITORPLUS_API FEditorPlusSeparator: public TEditorPlusMenuBaseNode{}

class EDITORPLUS_API FEditorPlusSubMenu: public TEditorPlusMenuBaseNode {}

class EDITORPLUS_API FEditorPlusCommand: public TEditorPlusMenuBaseLeaf {}

class EDITORPLUS_API FEditorPlusWidget: public TEditorPlusMenuBaseLeaf {}
```

Mehr Beispiele und Schnittstellenerklärungen finden Sie im Quellcode [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)，Testfall [MenuTest.cpp](https://github.com/disenone/UE.EditorPlus/blob/ue5.3/Source/EditorPlusTools/Private/MenuTest/MenuTest.cpp)


###Modularmanagement

UE.EditorPlus bietet auch ein modulares Framework zur Verwaltung von Erweiterungsmenüs, das das automatische Laden und Entladen von Menüs während des Plug-in-Lade- und -Entladevorgangs unterstützt.

Lassen Sie die Menu-Klasse von 'IEditorPlusToolInterface' erben und die Funktionen 'OnStartup' und 'OnShutdown' überschreiben. 'OnStartup' ist für die Erstellung des Menüs verantwortlich, 'OnShutdown' ruft die 'Destroy'-Funktion des Knotens auf, um das Menü zu bereinigen. Wenn die Referenzanzahl des einzelnen Knotens 0 erreicht, erfolgt automatische Bereinigung.

```cpp
class FMenuTest: public IEditorPlusToolInterface
{
public:
	virtual void OnStartup() override;
	virtual void OnShutdown() override;
}

void FMenuTest::OnStartup()
{
	BuildPathMenu();
	BuildCustomMenu();
	BuildMixMenu();
	BuildExtendMenu();
}

void FMenuTest::OnShutdown()
{
	for(auto Menu: Menus)
	{
		if(Menu.IsValid()) Menu->Destroy();
	}
	Menus.Empty();
}
```

Die Menu-Management-Klasse erbt von `IEditorPlusToolManagerInterface` und überschreibt die Funktion `AddTools`, um die Menüklasse hinzuzufügen.

```cpp
class FEditorPlusToolsImpl: public IEditorPlusToolManagerInterface
{
public:
	virtual void AddTools() override;
}

void FEditorPlusToolsImpl::AddTools()
{
	if (!Tools.Num())
	{
		Tools.Emplace(MakeShared<FMenuTest>());
	}

}
```

Beim Laden und Entladen des Plugins werden die Funktionen `StartupTools` und `ShutdownTools` der Verwaltungsklasse aufgerufen.

```cpp
void FEditorPlusToolsModule::StartupModule()
{
	Impl = FEditorPlusToolsImpl::Get();
	Impl->StartupTools();

}
void FEditorPlusToolsModule::ShutdownModule()
{
	Impl->ShutdownTools();
}
```

Mit der obigen Anpassung können das Laden und Entladen von Plugins automatisch erfolgen, was das automatische Laden und Entladen des erweiterten Menüs ermöglicht.


##Editor-Tools

UE.EditorPlus bietet auch einige nützliche Editor-Tools.

##Erstellen eines Editor-Fensters

Mit EditorPlus können Sie ganz einfach ein neues Editorfenster erstellen.

```cpp
// register spawn tab
Tab = MakeShared<FEditorPlusTab>(LOCTEXT("ClassBrowser", "ClassBrowser"), LOCTEXT("ClassBrowserTip", "Open the ClassBrowser"));
Tab->Register<SClassBrowserTab>();

// register menu action to spawn tab
FEditorPlusPath::RegisterPathAction(
    "/EditorPlusTools/ClassBrowser",
    FExecuteAction::CreateSP(Tab.ToSharedRef(), &FEditorPlusTab::TryInvokeTab),
);
```

`SClassBrowserTab` is a custom UI control.

```cpp
class SClassBrowserTab final : public SCompoundWidget
{
	SLATE_BEGIN_ARGS(SClassBrowserTab)
	{}
	SLATE_END_ARGS()
    // ...
}
```

### ClassBrowser

ClassBrowser ist ein UE Klassenbetrachter, der über das Menü EditorPlusTools -> ClassBrowser geöffnet werden kann.

![](assets/img/2024-ue-editorplus/classbrowser_menu.png)

![](assets/img/2024-ue-editorplus/classbrowser.png)

Basierend auf der UE-Reflexion implementiert, können verschiedene Arten von Mitgliederinformationen, Erklärungen und Hinweise von UE leicht eingesehen werden. Es unterstützt die Fuzzy-Suche und ermöglicht das Öffnen von Informationen der übergeordneten Klasse.

### MenuCollections

MenuCollections ist ein Tool zum schnellen Suchen und Speichern von Menübefehlen, das Ihnen hilft, schnell die Menübefehle zu finden, die Sie ausführen müssen, und Ihnen ermöglicht, häufig verwendete Befehle zu speichern, um die Effizienz zu steigern.

![](assets/img/2024-ue-editorplus/menucollection_find.png)

![](assets/img/2024-ue-editorplus/menucollection_star.png)


### SlateResourceBrowser

SlateResourceBrowser ist ein Tool, mit dem Sie schnell auf Slate UI-Ressourcen zugreifen können. Es hilft Ihnen dabei, die benötigten Editor-Ressourcen zu durchsuchen und zu finden, um den Editor leicht zu erweitern.

![](assets/img/2024-ue-editorplus/slateresourcebrowser_color.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_icon.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_font.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_widgetstyle.png)

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt. Bitte [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Benutze deinen Mittelfinger, um irgendwelche vergessenen Stellen zu markieren. 
