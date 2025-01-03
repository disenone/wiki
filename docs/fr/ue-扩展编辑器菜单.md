---
layout: post
title: Élargir le menu de l'éditeur UE
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
description: Enregistrer comment étendre le menu de l'éditeur UE
---


<meta property="og:title" content="UE 扩展编辑器菜单" />

#Extension du menu de l'éditeur UE

> Enregistrer comment étendre le menu de l'éditeur UE

## Hook

Le terme "Hook" peut être interprété comme l'ancre d'un menu d'extension. Nous avons la possibilité de positionner de nouveaux éléments de menu avant ou après le Hook. La plupart des commandes de menu de l'éditeur intégré d'UE possèdent un Hook. Pour afficher tous les Hooks des menus, vous pouvez accéder à "Édition - Préférences de l'éditeur - Général - Autres - Afficher les points d'extension de l'interface utilisateur" sous UE5.

![](assets/img/2023-ue-extend_menu/show_hook.png)

![](assets/img/2023-ue-extend_menu/show_hook2.png)

##Dépendance de module

Il est nécessaire d'ajouter les modules dépendants LevelEditor, Slate, SlateCore, EditorStyle, EditorWidgets, UnrealEd, ToolMenus dans le fichier .Build.cs du projet.

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

##Ajouter une barre de menu.

Veuillez fournir le code directement.

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

Exécuter le code ci-dessus permet de constater qu'un menu déroulant MenuTest a été ajouté après l'aide.

![](assets/img/2023-ue-extend_menu/bar.png)

##Ajouter la commande

Utilisez l'interface `MenuBuilder.AddMenuEntry` :

```cpp
// Inside MenuTest Lambda
MenuBuilder.AddMenuEntry(
    FText::FromName("MenuTestAction"), FText::FromName("MenuTestAction"),
    FSlateIcon(), FUIAction(FExecuteAction::CreateLambda([]()
    {
        // do action
    })));
```

Placez le code ci-dessus dans CreateLambda pour générer la commande du menu :

![](assets/img/2023-ue-extend_menu/action.png)

##Diviser le menu en sections.

Utilisez `MenuBuilder.BeginSection` et `MenuBuilder.EndSection` :

```cpp
MenuBuilder.BeginSection(NAME_None, FText::FromName("MenuTestSection"));
// code to create action
MenuBuilder.EndSection();
```

##Séparateur

```cpp
MenuBuilder.AddMenuSeparator();
```

![](assets/img/2023-ue-extend_menu/section&sperator.png)

##Sous-menu

Les sous-menus sont semblables à la barre de menus et doivent être définis à l'intérieur de la fonction Lambda :

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

#Composant SlateUI

Il est possible d'ajouter des composants d'interface utilisateur :

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

Le contenu lié à l'interface utilisateur de Slate n'est pas explicitement expliqué ici, si vous êtes intéressé, vous pouvez trouver d'autres articles à ce sujet.

#Ajouter un menu Hook

Ajouter une commande dans "Outils - Programmation", par exemple :

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

On peut aussi ajouter d'autres types de menus de la même manière.

#Code complet

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

--8<-- "footer_fr.md"



> Ce message a été traduit en utilisant ChatGPT. Veuillez fournir vos commentaires dans la section [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Identifier tout manquant. 
