---
layout: post
title: UE utiliza el formulario de ruta para expandir el menú.
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
---

<meta property="og:title" content="UE 使用路径形式扩展菜单" />

> Registrar cómo implementar menús de expansión de forma de ruta en UE.

Si no estás familiarizado con el menú de extensiones de UE, te recomendamos que mires brevemente: [Menú del Editor de Extensiones de UE](ue-扩展编辑器菜单.md)

El código del artículo se basa en el complemento: [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##Gestión de nodos

Organiza el menú siguiendo la estructura de un árbol, donde los nodos padres pueden contener nodos hijos:

```cpp
class EDITORPLUS_API FEditorPlusMenuBase: public TSharedFromThis<FEditorPlusMenuBase>
{
protected:
	// sub menus
	TArray<TSharedRef<FEditorPlusMenuBase>> Children;
}
```

Crear nodos secundarios al mismo tiempo que se crea el nodo principal:

```cpp
void FEditorPlusMenuBase::Register(FMenuBuilder& MenuBuilder)
{
	for (const auto Menu: Children)
	{
		Menu->Register(MenuBuilder);
	}
}
```

Por supuesto, el comportamiento específico de creación de cada nodo puede variar un poco. Se sobrescribe la función virtual para implementarlo:

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

##Generar nodos a través de una ruta.

Organiza el menú en una estructura de árbol; el formato de ruta puede definir la estructura de árbol de un menú:

```cpp
"/<Hook>Help/<MenuBar>BarTest/<SubMenu>SubTest/<Command>Action"
```

El camino anterior permite definir una serie de creaciones de menús:

- `<Hook>Ayuda`：ubicado en el menú llamado Help de Hook
- `<MenuBar>BarTest`: Crea un menú de tipo MenuBar, llamado BarTest.
- `<SubMenu>SubTest`: Crear un nodo hijo, tipo SubMenu, nombre SubTest
- `<Command>Action`：Crea un comando al final.

La forma de llamar a la interfaz puede ser muy sencilla:

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

##Generación de nodos con formato personalizado.

Seguimos utilizando un enfoque antiguo para crear menús, este enfoque permite una configuración más detallada y la estructura del código se asemeja un poco a la forma en que se escribe en SlateUI de UE:

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

##Forma mixta

Por supuesto, las formas de menú prediseñadas y las personalizadas son iguales en esencia, y se pueden combinar libremente, lo que ofrece una gran flexibilidad:

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

Varios menús definidos en diferentes lugares se combinarán en una misma estructura jerárquica, y los nodos con el mismo nombre se considerarán el mismo nodo. En otras palabras, la ruta es única, y una misma ruta puede determinar de manera única un nodo del menú.
Así que también podemos encontrar los nodos y realizar algunos ajustes y modificaciones.

```cpp
// set Name and Tips
FEditorPlusPath::GetNodeByPath("/<MenuBar>BarTest")->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
```


--8<-- "footer_es.md"


> Este post ha sido traducido utilizando ChatGPT. Por favor, proporcione su [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Señale cualquier omisión. 
