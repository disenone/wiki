---
layout: post
title: UE verwendet eine Pfadform zur Erweiterung des Menüs.
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
---

<meta property="og:title" content="UE 使用路径形式扩展菜单" />

> Aufzeichnen, wie ein Pfadmenü in UE implementiert wird.

Wenn Sie mit dem UE-Erweiterungsmenü nicht vertraut sind, empfehlen wir, sich zuerst kurz die folgenden Informationen anzusehen: [UE Erweiterungs-Editor-Menü](ue-扩展编辑器菜单.md)

Dieser Text basiert auf dem Plugin: [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##Nodeverwaltung

Verwalten Sie das Menü gemäß der Struktur eines Baumes, wobei das Elternknotenelement Kinder enthalten kann:

```cpp
class EDITORPLUS_API FEditorPlusMenuBase: public TSharedFromThis<FEditorPlusMenuBase>
{
protected:
	// sub menus
	TArray<TSharedRef<FEditorPlusMenuBase>> Children;
}
```

Beim Erstellen des Elternelements gleichzeitig ein Unterelement erstellen:

```cpp
void FEditorPlusMenuBase::Register(FMenuBuilder& MenuBuilder)
{
	for (const auto Menu: Children)
	{
		Menu->Register(MenuBuilder);
	}
}
```

Natürlich wird das konkrete Erstellungsverhalten für jeden Knoten etwas verschieden sein, durch das Überschreiben virtueller Funktionen realisiert:

```cpp
// Menubar
void FEditorPlusMenuBar::Register(FMenuBarBuilder& MenuBarBuilder)
{
	MenuBarBuilder.AddPullDownMenu(
		GetFriendlyName(),
		GetFriendlyTips(),
        // Delegate to call Register
		FEditorPlusMenuManager::GetDelegate<FNewMenuDelegate>(GetUniqueId()),       
		Hook);
}

// Section
void FEditorPlusSection::Register(FMenuBuilder& MenuBuilder)
{
	MenuBuilder.BeginSection(Hook, GetFriendlyName());
	FEditorPlusMenuBase::Register(MenuBuilder);
	MenuBuilder.EndSection();
}

// Separator
void FEditorPlusSeparator::Register(FMenuBuilder& MenuBuilder)
{
	MenuBuilder.AddMenuSeparator(Hook);
	FEditorPlusMenuBase::Register(MenuBuilder);
}

// SubMenu
void FEditorPlusSubMenu::Register(FMenuBuilder& MenuBuilder)
{
	MenuBuilder.AddSubMenu(
		GetFriendlyName(),
		GetFriendlyTips(),
		FNewMenuDelegate::CreateSP(this, &FEditorPlusSubMenu::MakeSubMenu),
		false,
		FSlateIcon(),
		true,
		Hook
	);
}

// Command
void FEditorPlusCommand::Register(FMenuBuilder& MenuBuilder)
{
    MenuBuilder.AddMenuEntry(
        CommandInfo->Label, CommandInfo->Tips, CommandInfo->Icon,
        CommandInfo->ExecuteAction, CommandInfo->Hook, CommandInfo->Type);
}

// ......
```

##Generiere Knoten durch Pfade.

Die Menüstruktur sollte in einer baumartigen Organisation angeordnet werden, und das Pfadformat kann eine solche Baumstruktur des Menüs definieren:

```cpp
"/<Hook>Help/<MenuBar>BarTest/<SubMenu>SubTest/<Command>Action"
```

Der oben genannte Pfad kann verwendet werden, um eine Reihe von Menüs zu erstellen:

- `<Hook>Hilfe`：befindet sich im Menü mit dem Namen Hilfe nach dem Hook
`<MenuBar>BarTest`：Erstellt ein Menü vom Typ MenuBar mit dem Namen BarTest.
- `<SubMenu>SubTest`: Erstelle Knoten, Typ SubMenu, Name SubTest
- `<Command>Action`: Erstelle schließlich einen Befehl.

Die Aufrufmethode der Schnittstelle kann sehr einfach sein:

```cpp
const FString Path = "/<Hook>Help/<MenuBar>BarTest/<SubMenu>SubTest/<Command>Action";
FEditorPlusPath::RegisterPathAction(
	Path, 
    FExecuteAction::CreateLambda([]
    {
        // do action
    })
);
```

##Erzeugung von Knoten durch benutzerdefinierte Formulare

Wir haben immer noch die sperrige Methode beibehalten, um Menüs zu erstellen. Diese sperrige Methode ermöglicht detailliertere Einstellungen und die Organisationsstruktur des Codes ähnelt der Schreibweise der Benutzeroberfläche (UI) von UE SlateUI.

```cpp
EP_NEW_MENU(FEditorPlusMenuBar)("BarTest")
->RegisterPath()
->Content({
    EP_NEW_MENU(FEditorPlusSubMenu)("SubTest")
    ->Content({
        EP_NEW_MENU(FEditorPlusCommand)("Action")
        ->BindAction(FExecuteAction::CreateLambda([]
            {
                // do action
            })),
    })
});
```

##Mischform

Natürlich sind die Pfadformate und die benutzerdefiniert generierten Menüs identisch, sie können untereinander kombiniert werden und bieten große Flexibilität.

```cpp
FEditorPlusPath::RegisterPath(
    "/<MenuBar>BarTest/<SubMenu>SubMenu/<Command>Action1", 
    EP_NEW_MENU(FEditorPlusCommand)("Action1")
    ->BindAction(FExecuteAction::CreateLambda([]
        {
            // do action
        })),
);

FEditorPlusPath::RegisterPath(
    "/<MenuBar>BarTest/<SubMenu>SubMenu/<Command>Action2", 
    EP_NEW_MENU(FEditorPlusCommand)("Action2")
    ->BindAction(FExecuteAction::CreateLambda([]
        {
            // do action
        })),
);
```

Die Menüs, die an verschiedenen Stellen definiert sind, werden in einer einzigen Baumstruktur zusammengeführt, wobei Knoten mit dem gleichen Namen als derselbe betrachtet werden. Mit anderen Worten, der Pfad ist eindeutig, und derselbe Pfad kann einen Menüknoten eindeutig bestimmen.
So können wir auch die Knoten finden und einige Einstellungen und Änderungen vornehmen:

```cpp
// set Name and Tips
FEditorPlusPath::GetNodeByPath("/<MenuBar>BarTest")->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
```


--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt, bitte in [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Bitte weisen Sie auf etwaige Auslassungen hin. 
