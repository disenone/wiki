---
layout: post
title: Extension del Editor UE.EditorPlus - Documentación
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
description: UE.EditorPlus es un complemento de editor para UE (Unreal Engine). Este
  documento proporciona información y explicaciones sobre UE.EditorPlus.
---

<meta property="og:title" content="UE 编辑器插件 EditorPlus 说明文档" />

#El complemento UE.EditorPlus del editor UE - Documentación

##**Introducción en video**

![type:video](assets/img/2024-ue-editorplus/market/video.mp4)

##`插件源码`

[UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##Proyecto agregando el complemento del código fuente EU.EditorPlus.

Referencia del documento:

- 中文：[UE 通过插件源码添加插件]

- Spanish: [UE añadir complementos mediante el código fuente del complemento](https://wiki.disenone.site/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)
- English: [UE adds plugins through the plugin source code](https://wiki.disenone.site/en/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)


###### Descripción del complemento

UE.EditorPlus es un complemento del editor de UE que proporciona una forma conveniente de expandir el menú del editor y admite formas avanzadas de expansión, incluyendo algunas herramientas prácticas del editor. Este complemento es compatible con UE5.3+.


##**扩展编辑器菜单** sería **Extender el menú del editor** en español.

![](assets/img/2024-ue-editorplus/menu.png)

![](assets/img/2024-ue-editorplus/toolbar.png)

###**Descripción**

*Soporte para ampliar el menú del editor de varias formas:*

- Método de ruta: `RegisterPathAction("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action")`
- Forma de instanciar: `EP_NEW_MENU(FEditorPlusMenuBar)("Bar")`
- Modo de combinación: `RegisterPath("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action", EP_NEW_MENU(FEditorPlusCommand)("Action")`

###**Markdown:**
路径方式

**Translated:**
Forma de ruta

Puedes registrar un comando de menú del editor de esta manera:

```cpp
FEditorPlusPath::RegisterPathAction(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action",
    FExecuteAction::CreateLambda([]
        {
            // do action
        })
);
```

De esta manera, puedes agregar una barra de menú "Bar" detrás de la opción "Help" en la barra de menú del editor. Dentro de la barra "Bar", puedes añadir un submenú "SubMenu" y dentro de él, agregar un comando "Action".

La formato completo de la ruta sería así: `/<Hook>HookName/<Type1>Name1/<Type2>Name2`, el primer elemento de la ruta debe ser `<Hook>`, los tipos y restricciones soportadas actualmente son:

- `<Hook>`: Indica en qué posición del Hook se debe generar el menú, no se deben incluir `<Hook>` en las rutas posteriores.
- `<MenuBar>`: La barra de menú, la ruta posterior no puede contener `<Hook>, <MenuBar>, <ToolBar>`
- `<ToolBar>`: `<Barra de herramientas>`, la ruta posterior no puede tener `<Hook>, <MenuBar>, <ToolBar>`
- `<Section>`: Sección de menú, no se pueden utilizar las rutas `<Hook>, <MenuBar>, <Section>` a continuación.
- `<Separator>`: Separador de menú, no se puede utilizar después de `<Hook>, <MenuBar>`.
- `<SubMenu>`: Submenú, la ruta posterior no puede contener `<Hook>, <MenuBar>`
- `<Comando>`: Comando de menú, no se permite ingresar ninguna ruta después
- `<Widget>`: Componentes de interfaz de usuario de Slate más personalizables y extensibles. No deben tener ninguna ruta después.

Forma de ruta más sencilla: `/NombreBarra/NombreSubMenu1/NombreSubMenu2/NombreComando`, si no se especifica el tipo, el primer elemento de la ruta es `<MenuBar>`, los del medio son `<SubMenu>` y el último es `<Command>`.

Si no se especifica `<Hook>`, automáticamente se agrega al principio `<Hook>Help`, lo que indica que se agregará después del menú de Ayuda en la barra de menú.

###Formas de instanciar

La forma de ruta es instanciar automáticamente todos los nodos según su tipo y parámetros predeterminados. También podemos controlar la instanciación nosotros mismos y tener un control más preciso sobre el contenido de la expansión.

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

Cuando instancia `MyBar`, puede pasar el nombre del gancho, el nombre localizado y los parámetros de la sugerencia localizada (`"MyBar", LOCTEXT("MyBar", "MyBar"), LOCTEXT("MyBarTips", "MyBarTips")`). El código anterior es equivalente a la forma de ruta `/<Hook>Help/<MenuBar>MyBar/<SubMenu>MySubMenu/<Command>MyAction`.

###**混合方式** se traduce al español como **modo mixto**.

Por supuesto, también se pueden mezclar las dos formas:

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

En esta situación, el complemento instanciará automáticamente los nodos de las rutas intermedias, mientras que el nodo final utilizará la instancia proporcionada por el usuario.

###**更多用例**

Archivo de cabecera:

```cpp
#include <EditorPlusPath.h>
```

La localización del idioma se especifica mediante la ruta, `EP_FNAME_HOOK_AUTO` indica que se utilizará automáticamente el nombre de la ruta como nombre del `Hook`:

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

Obtener nodos y establecer texto localizado a través de la ruta:



```cpp
FEditorPlusPath::GetNodeByPath("/MenuTest")
    ->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))
    ->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
```


Agregar un componente de interfaz de usuario Slate al final de la ruta

```cpp
FEditorPlusPath::RegisterPath(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Widget>Widget",
    EP_NEW_MENU(FEditorPlusWidget)("Widget", LOCTEXT("Widget", "Widget"))
        ->BindWidget(SNew(SHorizontalBox)));
);
```

En el Hook incorporado de la UE, agregue un nuevo nodo.

```cpp
FEditorPlusPath::RegisterPath("<Hook>EpicGamesHelp/<Separator>ExtendSeparator")
```

**多次声明相同的路径，都被识别成同一个路径，因此可以不断扩展相同的路径**

En múltiples ocasiones, declarar la misma ruta se reconoce como una única ruta, por lo tanto, es posible ampliar continuamente la misma ruta.

```cpp
FEditorPlusPath::RegisterPathAction("/MenuTest/SubMenu1/SubMenu1/Path1", Action, EP_FNAME_HOOK_AUTO, LOCTEXT("Path1", "Path1"), LOCTEXT("Path1Tips", "Path1Tips"));
FEditorPlusPath::RegisterPathAction("/MenuTest/SubMenu1/SubMenu1/Path2", Action, EP_FNAME_HOOK_AUTO, LOCTEXT("Path2", "Path2"), LOCTEXT("Path2Tips", "Path2Tips"));
```

**为一个节点继续扩展路径**

Para expandir la ruta de un nodo.

```cpp
auto node = FEditorPlusPath::GetNodeByPath("/MenuTest");
FEditorPlusPath::RegisterChildPath(node, "<SubMenu>Sub/<Separator>Sep");
```

Eliminar una ruta

```cpp
FEditorPlusPath::UnregisterPath("/MenuTest/SubMenu1/SubMenu1/Path1");
```

**扩展工具栏**
```cpp
FEditorPlusPath::RegisterPath("/<Hook>ProjectSettings/<ToolBar>MenuTestToolBar")
->Content({
    EP_NEW_MENU(FEditorPlusCommand)("ToolBarCommand1")
    ->BindAction(...)
});
```

###Por favor, proporcione más contexto o detalles sobre el texto que desea traducir.

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

- `RegisterPath`: Generar menú de rutas
- `RegisterPathAction`: Genera un menú de trayectorias y automáticamente vincula una acción al nodo final `<Command>`.
- `RegisterChildPath`: Genera rutas secundarias para el nodo especificado.
- `RegisterChildPathAction`: Genera automáticamente rutas secundarias para el nodo especificado y enlaza automáticamente la acción.
- `UnregisterPath`: Elimina una ruta. Al utilizar `Leaf` con nodos terminales múltiples del mismo nombre, es posible especificar una coincidencia estricta. Durante el proceso de eliminación, se realizará un retroceso en los nodos intermedios y estos serán eliminados si no tienen ningún hijo.
`GetNodeByPath`: Obtener nodo por ruta


**节点类型**

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

Para obtener más ejemplos e información sobre las interfaces, consulte el código fuente [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus), prueba de caso [MenuTest.cpp](https://github.com/disenone/UE.EditorPlus/blob/ue5.3/Source/EditorPlusTools/Private/MenuTest/MenuTest.cpp)


###**模块化管理**

UE.EditorPlus también proporciona un marco de gestión modular para el menú de extensiones, que admite la carga y descarga automática de los menús de las extensiones al cargar y descargar los complementos.

Haz que la clase del menú herede de `IEditorPlusToolInterface` y sobrescriba las funciones `OnStartup` y `OnShutdown`. `OnStartup` se encarga de crear el menú y `OnShutdown` se encarga de llamar a la función `Destroy` del nodo para limpiar el menú. Si el número de referencias al nodo es 0, se realizará una limpieza automática.

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

La clase de gestión de menús hereda de `IEditorPlusToolManagerInterface` y anula la función `AddTools`, agregando la clase de menú dentro de `AddTools`.

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

Cuando se carga y descarga el complemento, se llaman respectivamente las funciones de la clase de gestión `StartupTools` y `ShutdownTools`.

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

Para completar la adaptación anterior, se cargará y descargará automáticamente el menú de extensiones al cargar y descargar un complemento.


##**Editores de herramientas**

UE.EditorPlus también ofrece algunas herramientas útiles para el editor.

##Crear ventana del editor

Utilizando EditorPlus, puedes crear fácilmente una nueva ventana de editor.

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

`SClassBrowserTab` es un control de interfaz de usuario personalizado.

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

**ClassBrowser** es una herramienta de visualización de clases de UE, que se abre a través del menú EditorPlusTools -> ClassBrowser.

![](assets/img/2024-ue-editorplus/classbrowser_menu.png)

![](assets/img/2024-ue-editorplus/classbrowser.png)

Basado en la reflexión de UE, esto permite ver fácilmente la información de los miembros de varios tipos de UE, incluyendo instrucciones de sugerencias, y admite una búsqueda difusa, así como la posibilidad de abrir la información de la clase padre.

### MenuCollections

**MenuCollections** es una herramienta de búsqueda y recopilación rápida de comandos de menú, que te ayuda a encontrar rápidamente los comandos de menú que necesitas ejecutar, y también te permite guardar los comandos más frecuentes para mejorar tu eficiencia.

![](assets/img/2024-ue-editorplus/menucollection_find.png)

![](assets/img/2024-ue-editorplus/menucollection_star.png)


### SlateResourceBrowser

El `SlateResourceBrowser` es una herramienta que te permite ver rápidamente los recursos de la interfaz de usuario de `Slate UI`. Puede ayudarte a navegar y buscar los recursos del editor que necesitas, lo que facilita la ampliación del editor.

![](assets/img/2024-ue-editorplus/slateresourcebrowser_color.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_icon.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_font.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_widgetstyle.png)

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
