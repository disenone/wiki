---
layout: post
title: UE erweitern Editor-Menü
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
description: Notieren Sie, wie die UE den Editor-Menü erweitert.
---


<meta property="og:title" content="UE 扩展编辑器菜单" />

#Erweitern Sie das UE-Editor-Menü.

> Protokollieren Sie, wie UE den Editor-Menü erweitert.

## Hook

Hook kann als Ankerpunkt für erweiterte Menüs verstanden werden. Wir können neue Menübefehle vor oder nach einem Hook einstellen. Die meisten integrierten Editor-Menübefehle in UE sind mit einem Hook versehen. Öffne in UE5 die Option `Bearbeiten - Editor-Einstellungen - Allgemein - Andere - UI-Erweiterungspunkte anzeigen`, um alle Hooks für Menüs anzuzeigen:

![](assets/img/2023-ue-extend_menu/show_hook.png)

![](assets/img/2023-ue-extend_menu/show_hook2.png)

##Modulabhängigkeit

Die Module LevelEditor, Slate, SlateCore, EditorStyle, EditorWidgets, UnrealEd und ToolMenus müssen in der .Build.cs-Datei des Projekts hinzugefügt werden.

```c#
PrivateDependencyModuleNames.AddRange(
    new string[]
    {
        "Core",
        "Engine",
        "CoreUObject",
        "LevelEditor",
        "Slate",
        "SlateCore",
        "EditorStyle",
        "EditorWidgets",
        "UnrealEd",
        "ToolMenus",
    }
    );
```

##Fügen Sie eine Menüleiste hinzu.

Bitte senden Sie den Code direkt.

```cpp
auto MenuExtender = MakeShared<FExtender>();

MenuExtender->AddMenuBarExtension(
    "Help", EExtensionHook::After,      // Create After Help
    nullptr,
    FMenuBarExtensionDelegate::CreateLambda([](FMenuBarBuilder& MenuBarBuilder)
    {
        MenuBarBuilder.AddPullDownMenu(
            TEXT("MenuTest"),       // Name
            TEXT("MenuTest"),       // Tips
            FNewMenuDelegate::CreateLambda([](FMenuBuilder& MenuBuilder)
            {
                // create sub menus
            }),
            TEXT("MenuText"));      // New Hook
    })
);
FModuleManager::LoadModuleChecked<FLevelEditorModule>("LevelEditor").GetMenuExtensibilityManager()->AddExtender(MenuExtender);
```

Durch Ausführen des obigen Codes sehen Sie, dass hinter Hilfe eine Menüleiste MenuTest hinzugefügt wurde:

![](assets/img/2023-ue-extend_menu/bar.png)

##Fügen Sie den Befehl hinzu.

Verwenden Sie die Schnittstelle `MenuBuilder.AddMenuEntry`:

```cpp
// Inside MenuTest Lambda
MenuBuilder.AddMenuEntry(
    FText::FromName("MenuTestAction"), FText::FromName("MenuTestAction"),
    FSlateIcon(), FUIAction(FExecuteAction::CreateLambda([]()
    {
        // do action
    })));
```

Legen Sie den obigen Code in CreateLambda, um das Menübefehl zu erstellen:

![](assets/img/2023-ue-extend_menu/action.png)

##Menüabschnitte

Verwenden Sie `MenuBuilder.BeginSection` und `MenuBuilder.EndSection`:

```cpp
MenuBuilder.BeginSection(NAME_None, FText::FromName("MenuTestSection"));
// code to create action
MenuBuilder.EndSection();
```

##Trennzeichen

```cpp
MenuBuilder.AddMenuSeparator();
```

![](assets/img/2023-ue-extend_menu/section&sperator.png)

##Untermenü

The text translates to:

"Untermenü ähnelt einer Menüleiste und muss in der Lambda definiert werden:"

```cpp
MenuBuilder.AddSubMenu(
    FText::FromName("MenuTestSub"),	
    FText::FromName("MenuTestSub"),	
    FNewMenuDelegate::CreateLambda([](FMenuBuilder& MenuBuilder)
    {
        MenuBuilder.AddMenuEntry(
            FText::FromName("MenuTestSubAction"), FText::FromName("MenuTestSubAction"),
            FSlateIcon(), FUIAction(FExecuteAction::CreateLambda([]()
            {
                // do action
            })));
    }));
```

![](assets/img/2023-ue-extend_menu/submenu.png)

#SlateUI controls

Es können weitere UI-Steuerelemente hinzugefügt werden:

```cpp
MenuBuilder.AddWidget(
    SNew(SHorizontalBox)
        + SHorizontalBox::Slot()
        .AutoWidth()
        [
            SNew(SEditableTextBox)
            .MinDesiredWidth(50)
            .Text(FText::FromName("MenuTestWidget"))
        ]
        
        + SHorizontalBox::Slot()
        .AutoWidth()
        .Padding(5, 0, 0, 0)
        [
        SNew(SButton)
        .Text(FText::FromName("ExtendWidget"))
        .OnClicked(FOnClicked::CreateLambda([]()
        {
            // do action
            return FReply::Handled();
        }))
        ],
    FText::GetEmpty()
);
```

![](assets/img/2023-ue-extend_menu/widget.png)

Der Inhalt im Zusammenhang mit Slate UI wird hier nicht ausführlich behandelt. Bei Interesse können Sie in anderen Artikeln weiterlesen.

#Hook - Menü hinzufügen

Fügen Sie beispielsweise in "Werkzeug - Programmierung" einen Befehl hinzu:

```cpp
MenuExtender->AddMenuExtension(
    "Programming", EExtensionHook::After,
    nullptr,
    FMenuExtensionDelegate::CreateLambda([](FMenuBuilder& MenuBuilder)
    {
        MenuBuilder.AddMenuEntry(
        FText::FromName("MenuTestAction"), FText::FromName("MenuTestAction"),
        FSlateIcon(), FUIAction(FExecuteAction::CreateLambda([]()
        {
            // do action
        })));
    })
);
```

![](assets/img/2023-ue-extend_menu/other_hook.png)

Sie können auch andere Arten von Menüs hinzufügen.

#Vollständiger Code

```cpp
void BuildTestMenu()
{
	auto MenuExtender = MakeShared<FExtender>();

	MenuExtender->AddMenuBarExtension(
		"Help", EExtensionHook::After,
		nullptr,
		FMenuBarExtensionDelegate::CreateLambda([](FMenuBarBuilder& MenuBarBuilder)
		{
			MenuBarBuilder.AddPullDownMenu(
				FText::FromName("MenuTest"),
				FText::FromName("MenuTest"),
				FNewMenuDelegate::CreateLambda([](FMenuBuilder& MenuBuilder)
				{
					MenuBuilder.BeginSection(NAME_None, FText::FromName("MenuTestSection"));
					MenuBuilder.AddMenuSeparator();
					MenuBuilder.AddMenuEntry(
						FText::FromName("MenuTestAction"), FText::FromName("MenuTestAction"),
						FSlateIcon(), FUIAction(FExecuteAction::CreateLambda([]()
						{
                            // do action
						})));

					MenuBuilder.AddSubMenu(
						FText::FromName("MenuTestSubb"),
						FText::FromName("MenuTestSubb"),
						FNewMenuDelegate::CreateLambda([](FMenuBuilder& MenuBuilder)
						{
							MenuBuilder.AddMenuEntry(
								FText::FromName("MenuTestSubAction"), FText::FromName("MenuTestSubAction"),
								FSlateIcon(), FUIAction(FExecuteAction::CreateLambda([]()
								{
                                    // do action
								})));
						}));
					MenuBuilder.EndSection();

					MenuBuilder.AddWidget(
					SNew(SHorizontalBox)
						 + SHorizontalBox::Slot()
						 .AutoWidth()
						 [
							 SNew(SEditableTextBox)
							 .MinDesiredWidth(50)
							 .Text(FText::FromName("MenuTestWidget"))
						 ]
						 + SHorizontalBox::Slot()
						 .AutoWidth()
						 .Padding(5, 0, 0, 0)
						 [
							SNew(SButton)
							.Text(FText::FromName("ExtendWidget"))
							.OnClicked(FOnClicked::CreateLambda([]()
							{
								// do action
								return FReply::Handled();
							}))
						 ],
					 FText::GetEmpty()
					);
				}),
				"MenuTest");
		})
	);

	MenuExtender->AddMenuExtension(
		"Programming", EExtensionHook::After,
		nullptr,
		FMenuExtensionDelegate::CreateLambda([](FMenuBuilder& MenuBuilder)
		{
			MenuBuilder.AddMenuEntry(
			FText::FromName("MenuTestAction"), FText::FromName("MenuTestAction"),
			FSlateIcon(), FUIAction(FExecuteAction::CreateLambda([]()
			{
                // do action
			})));
		})
	);

	FModuleManager::LoadModuleChecked<FLevelEditorModule>("LevelEditor").GetMenuExtensibilityManager()->AddExtender(MenuExtender);
}
```

![](assets/img/2023-ue-extend_menu/overall.png)

--8<-- "footer_de.md"



> (https://github.com/disenone/wiki_blog/issues/new)Geben Sie alle übersehenen Punkte an. 
