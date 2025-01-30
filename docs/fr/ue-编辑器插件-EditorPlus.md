---
layout: post
title: UE éditeur plugin UE.EditorPlus documentation explicative
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
description: Extension de l'éditeur UE  Documentation de l'extension UE.EditorPlus
---

<meta property="og:title" content="UE 编辑器插件 EditorPlus 说明文档" />

#Extension UE.EditorPlus de l'éditeur UE - Documentation explicative

##Présentation vidéo

![type:video](assets/img/2024-ue-editorplus/market/video.mp4)

##Code source du plugin

[UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##Téléchargement de magasin en ligne

[EditorPlus](https://www.unrealengine.com/marketplace/zh-CN/product/editorplus)

##Ajouter le plugin source EU.EditorPlus au projet

Document de référence :

Traduisez ce texte en français :

- 中文：[UE通过插件源码添加插件](https://wiki.disenone.site/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)
- English: [UE adds plugins through the plugin source code](https://wiki.disenone.site/en/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)


##Plugin Description

UE.EditorPlus est un plugin pour l'éditeur UE qui offre un moyen pratique d'étendre le menu de l'éditeur, tout en prenant en charge des méthodes avancées d'extension, et inclut également quelques outils pratiques pour l'éditeur. Ce plugin est compatible avec UE5.3+.


##Étendre le menu de l'éditeur

![](assets/img/2024-ue-editorplus/menu.png)

![](assets/img/2024-ue-editorplus/toolbar.png)

###说明  
Explication

Prise en charge de diverses méthodes pour étendre le menu de l'éditeur :

- Méthode de chemin : `RegisterPathAction("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action")`
- Mode d'instanciation : `EP_NEW_MENU(FEditorPlusMenuBar)("Bar")`
Méthode mixte: `RegisterPath("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action",EP_NEW_MENU(FEditorPlusCommand)("Action")`

###Mode de cheminement

Vous pouvez enregistrer une commande de menu de l'éditeur de cette manière :

```cpp
FEditorPlusPath::RegisterPathAction(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action",
    FExecuteAction::CreateLambda([]
        {
            // do action
        })
);
```

Ainsi, il est possible d'ajouter une barre de menu Bar après le menu Aide dans la barre de menus de l'éditeur, où Bar contiendra un sous-menu SubMenu, et dans SubMenu, il y aura une commande Action.

Le format complet du chemin sera le suivant : `/<Hook>HookName/<Type1>Name1/<Type2>Name2`, le premier chemin doit être `<Hook>`, les types pris en charge actuellement et leurs limitations :

- `<Hook>` : Indicates where the menu should be generated on which Hook, the subsequent path cannot contain `<Hook>`
- `<MenuBar>` : La barre de menu, le chemin ne doit pas contenir `<Hook>`, `<MenuBar>`, `<ToolBar>` à la suite
- `<ToolBar>` : Barre d'outils, le chemin suivant ne peut pas contenir `<Hook>, <MenuBar>, <ToolBar>`
- `<Section>`: La section du menu, le chemin arrière ne peut pas contenir `<Hook>, <MenuBar>, <Section>`
- `<Separator>` : Séparateur de menu, le chemin derrière ne peut pas contenir `<Hook>, <MenuBar>`
- `<SubMenu>`：Sous-menu, les chemins suivants ne peuvent pas avoir `<Hook>, <MenuBar>`
- `<Command>` : Commande de menu, aucun chemin ne doit suivre.
- `<Widget>`: Autres composants UI Slate personnalisables et extensibles, aucun chemin ne doit être ajouté à la suite.

Traduisez ce texte en français :

Forme de chemin plus simple : `/NomDeBarre/NomSousMenu1/NomSousMenu2/NomCommande`, si aucun type n'est spécifié, le premier élément du chemin est `<MenuBar>`, le milieu est `<SubMenu>`, et le dernier est `<Command>`.

Si `<Hook>` n'est pas spécifié, ajoute automatiquement `<Hook>Help` en tête pour indiquer l'ajout de la barre de menu après le menu Aide.

###Méthodes d'instanciation

Le processus d'instanciation consiste à créer automatiquement toutes les nœuds en fonction de leur type et de leurs paramètres par défaut, mais nous avons également la possibilité de gérer nous-mêmes cette instanciation pour un contrôle plus précis de l'extension du contenu.

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

Lors de l'instanciation de `MyBar`, il est possible de passer le nom du Hook, le nom localisé et les paramètres de conseil localisés (`"MyBar", LOCTEXT("MyBar", "MyBar"), LOCTEXT("MyBarTips", "MyBarTips")`). Le code ci-dessus équivaut à la manière par chemin `/<Hook>Help/<MenuBar>MyBar/<SubMenu>MySubMenu/<Command>MyAction`.

###Méthode de mélange

Bien sûr, il est également possible d'utiliser une combinaison des deux méthodes :

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

Dans ce cas, le plugin instanciera automatiquement les nœuds du chemin intermédiaire, tandis que les nœuds de la fin du chemin utiliseront ceux instanciés par l'utilisateur.

###Plus de cas d'utilisation

Fichier d'en-tête :

```cpp
#include <EditorPlusPath.h>
```

Le mode de chemin spécifie la langue de localisation, `EP_FNAME_HOOK_AUTO` indique qu'il faut utiliser automatiquement le nom du chemin comme nom de `Hook` :

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

Obtenir les nœuds via le chemin d'accès et définir le texte localisé :

```cpp
FEditorPlusPath::GetNodeByPath("/MenuTest")
    ->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))
    ->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
```


Ajouter un contrôle Slate UI à l'extrémité du chemin.

```cpp
FEditorPlusPath::RegisterPath(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Widget>Widget",
    EP_NEW_MENU(FEditorPlusWidget)("Widget", LOCTEXT("Widget", "Widget"))
        ->BindWidget(SNew(SHorizontalBox)));
);
```

Ajouter de nouveaux nœuds dans le Hook fourni par l'UE.

```cpp
FEditorPlusPath::RegisterPath("<Hook>EpicGamesHelp/<Separator>ExtendSeparator")
```

Déclarer plusieurs fois le même chemin est reconnu comme le même chemin, ce qui permet d'élargir continuellement le même chemin.

```cpp
FEditorPlusPath::RegisterPathAction("/MenuTest/SubMenu1/SubMenu1/Path1", Action, EP_FNAME_HOOK_AUTO, LOCTEXT("Path1", "Path1"), LOCTEXT("Path1Tips", "Path1Tips"));
FEditorPlusPath::RegisterPathAction("/MenuTest/SubMenu1/SubMenu1/Path2", Action, EP_FNAME_HOOK_AUTO, LOCTEXT("Path2", "Path2"), LOCTEXT("Path2Tips", "Path2Tips"));
```

Étendre le chemin pour un nœud supplémentaire

```cpp
auto node = FEditorPlusPath::GetNodeByPath("/MenuTest");
FEditorPlusPath::RegisterChildPath(node, "<SubMenu>Sub/<Separator>Sep");
```

Supprimer un chemin

```cpp
FEditorPlusPath::UnregisterPath("/MenuTest/SubMenu1/SubMenu1/Path1");
```

Barre d'outils étendue
```cpp
FEditorPlusPath::RegisterPath("/<Hook>ProjectSettings/<ToolBar>MenuTestToolBar")
->Content({
    EP_NEW_MENU(FEditorPlusCommand)("ToolBarCommand1")
    ->BindAction(...)
});
```

###Description de l'interface

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

- `RegisterPath` : menu de chemin de génération
- `RegisterPathAction` : Crée un menu de chemin et associe automatiquement une action à l'élément `<Command>` terminal.
`RegisterChildPath`: Générer des chemins enfants pour un nœud spécifique
- `RegisterChildPathAction` : Continuer à générer des sous-chemins pour le nœud spécifié et lier automatiquement l'action.
- `UnregisterPath`：Supprimer le chemin, `Leaf` peut spécifier une correspondance stricte lorsqu'il y a plusieurs nœuds de terminaison portant le même nom. Pendant le processus de suppression, les nœuds intermédiaires seront parcourus en arrière, et ils seront également supprimés s'ils ne contiennent aucun nœud enfant.
- `GetNodeByPath` : Obtenir le nœud selon le chemin


Type de nœud

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

Pour plus d'exemples et de détails sur l'interface, veuillez consulter le code source [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)，cas de test [MenuTest.cpp](https://github.com/disenone/UE.EditorPlus/blob/ue5.3/Source/EditorPlusTools/Private/MenuTest/MenuTest.cpp)


###Gestion modulaire

UE.EditorPlus offre également un cadre de gestion modulaire pour le menu d'extensions, permettant le chargement et le déchargement automatiques des menus d'extensions lors du chargement et du déchargement des plugins.

Faites hériter la classe de menu de l'interface `IEditorPlusToolInterface`, puis surchargez les fonctions `OnStartup` et `OnShutdown`. `OnStartup` est responsable de la création du menu, tandis que `OnShutdown` est chargée d'appeler la fonction `Destroy` de chaque élément pour nettoyer le menu. Si le nombre de références des éléments tombe à zéro, le nettoyage est effectué automatiquement.

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

La classe de gestion des menus hérite de `IEditorPlusToolManagerInterface` et redéfinit la fonction `AddTools`, dans `AddTools`, elle ajoute les classes de menu.

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

Lors du chargement et du déchargement des plugins, les fonctions `StartupTools` et `ShutdownTools` de la classe de gestion sont respectivement appelées.

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

Pour accomplir ce qui précède, vous pouvez automatiquement charger et décharger le menu des extensions lors du chargement et du déchargement des plugins.


##Outils de l'éditeur

UE.EditorPlus propose également quelques outils d'édition pratiques.

##Créer une fenêtre d'éditeur.

Avec EditorPlus, il est très facile de créer une nouvelle fenêtre d'édition.

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

`SClassBrowserTab` est un composant d'interface utilisateur personnalisé.

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

ClassBrowser is a UE Class viewer, open it through the menu EditorPlusTools -> ClassBrowser.

![](assets/img/2024-ue-editorplus/classbrowser_menu.png)

![](assets/img/2024-ue-editorplus/classbrowser.png)

Basé sur la réflexion de l'UE, cela permet de visualiser facilement les informations sur les membres de différents types d'UE, les indications d'explication, etc. Il prend en charge la recherche floue et permet de naviguer vers les informations de la classe parent en les ouvrant.

### MenuCollections

MenuCollections est un outil de recherche rapide et de collecte de commandes de menu, capable de vous aider à trouver rapidement les commandes de menu que vous devez exécuter, tout en vous permettant de sauvegarder vos commandes courantes pour améliorer votre efficacité.

![](assets/img/2024-ue-editorplus/menucollection_find.png)

![](assets/img/2024-ue-editorplus/menucollection_star.png)


### SlateResourceBrowser

SlateResourceBrowser est un outil qui permet de visualiser rapidement les ressources de l'interface utilisateur Slate, facilitant la navigation et la recherche des ressources d'édition nécessaires pour étendre l'éditeur.

![](assets/img/2024-ue-editorplus/slateresourcebrowser_color.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_icon.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_font.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_widgetstyle.png)

--8<-- "footer_fr.md"


> Ce post a été traduit à l'aide de ChatGPT, veuillez laisser vos [**retours**](https://github.com/disenone/wiki_blog/issues/new)Veuillez signaler tout élément manquant. 
