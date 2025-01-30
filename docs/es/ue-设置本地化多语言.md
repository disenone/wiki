---
layout: post
title: UE establece la localización multilingüe.
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
description: Registre cómo lograr la localización de varios idiomas en UE.
---

<meta property="og:title" content="UE 设置本地化多语言" />

#UE establece la localización multilingüe.

> Documentar cómo implementar la localización multilingüe en UE.

Si no estás familiarizado con el menú de extensiones de UE, se recomienda que primero eches un vistazo a: [Menú del editor de extensiones de UE](ue-扩展编辑器菜单.md)，[ue-uso de la ruta para extender el menú](ue-使用路径形式扩展菜单.md)

Este texto está basado en el complemento: [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##Presentación de funciones

Las herramientas integradas en la UE permiten la localización en varios idiomas, por ejemplo, podemos localizar los menús del editor:

Menú en chino:

![](assets/img/2023-ue-localization/chinese.png)

Menú en inglés:

![](assets/img/2023-ue-localization/english.png)

##Declaración de código

Para lograr la localización del menú, necesitamos declarar explícitamente en el código las cadenas que requieren ser procesadas por UE, utilizando los macros definidos por UE `LOCTEXT` y `NSLOCTEXT`:

En la definición global de archivos, se comienza definiendo un macro llamado `LOCTEXT_NAMESPACE`, que contiene el nombre del espacio de nombres actual donde se encuentran los textos multilingües. Luego, los textos en el archivo pueden definirse usando `LOCTEXT`, y al final del archivo se elimina el macro `LOCTEXT_NAMESPACE`.

```cpp
// #define LOCTEXT(InKey, InTextLiteral)

#define LOCTEXT_NAMESPACE "EditorPlusTools"
LOCTEXT("Key", "Content");
#undef LOCTEXT_NAMESPACE

```

- Forma de definición parcial, utilizando `NSLOCTEXT`, al definir el texto, incluye el parámetro de espacio de nombres:

```cpp
// #define NSLOCTEXT(InNamespace, InKey, InTextLiteral)

NSLOCTEXT("EditorPlusTools", "Key", "Content");
```

La herramienta UE recopila todo el texto que requiere traducción al buscar la presencia de las macros `LOCTEXT` y `NSLOCTEXT`.

##Usar herramientas para traducir el texto.

Suppose we have the following code defining text:

```cpp
#define LOCTEXT_NAMESPACE "EditorPlusTools"
// register path node loctext
FEditorPlusPath::GetNodeByPath("/MenuTest")->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
FEditorPlusPath::GetNodeByPath("/MenuTest/<SubMenu>SubMenu1")->SetFriendlyName(LOCTEXT("SubMenu1", "SubMenu1"))->SetFriendlyTips(LOCTEXT("SubMenu1Tips", "SubMenu1Tips"));
FEditorPlusPath::GetNodeByPath("/MenuTest/<SubMenu>SubMenu1/<SubMenu>SubMenu1")->SetFriendlyName(LOCTEXT("SubMenu1", "SubMenu1"))->SetFriendlyTips(LOCTEXT("SubMenu1Tips", "SubMenu1Tips"));
FEditorPlusPath::GetNodeByPath("/<Hook>Help/<MenuBar>MenuTest/<SubMenu>SubMenu1/<Section>Section1")->SetFriendlyName(LOCTEXT("Section1", "Section1"))->SetFriendlyTips(LOCTEXT("Section1Tips", "Section1Tips"));
#undef LOCTEXT_NAMESPACE
```

Primero, abre la herramienta de traducción y ve a la configuración del editor en `Editar - Preferencias del editor`, luego marca la opción `General - Funciones experimentales - Herramientas - Selector de traducción`.

![](assets/img/2023-ue-localization/editor_enable_tool.png)


Abre la herramienta de traducción `Herramientas - Panel de control de localización`:

![](assets/img/2023-ue-localization/editor_open_tool.png)

Crear un nuevo objetivo (también es válido en el Game por defecto, crear uno nuevo para facilitar la gestión y el movimiento de estos textos traducidos).

![](assets/img/2023-ue-localization/tool_new_target.png)

Configurar los parámetros del objetivo, aquí lo nombré como `EditorPlusTools`, la política de carga es `Editor`, recoge desde texto y añade el directorio de plugins, la dependencia del objetivo es `Engine, Editor`, el resto de la configuración se mantiene sin cambios:

![](assets/img/2023-ue-localization/tool_target_config.png)

Agrega los idiomas, asegurando que haya dos idiomas: chino (simplificado) y inglés. Confirma que al pasar el mouse sobre el nombre del idioma se muestren `zh-Hans` y `en` respectivamente, y selecciona inglés (porque en nuestro código definimos los textos en inglés, necesitamos recopilar estos textos en inglés aquí).

![](assets/img/2023-ue-localization/tool_target_lang.png)

Haga clic para recopilar el texto:

![](assets/img/2023-ue-localization/tool_target_collect.png)

Se mostrará un cuadro de progreso de recolección, esperando que la recolección sea exitosa, y se mostrará una marca de verificación verde:

![](assets/img/2023-ue-localization/tool_target_collected.png)

Desactive la ventana de recopilación de progreso, regrese a la herramienta de traducción donde verá que se muestra la cantidad recopilada en una línea en inglés. No necesitamos traducir el texto en inglés en sí. Haga clic en el botón de traducción en la línea en chino.

![](assets/img/2023-ue-localization/tool_go_trans.png)

Al abrirlo, podemos ver que hay contenido en la columna de "Sin traducir". En la columna derecha del texto en inglés, debemos ingresar el contenido traducido. Una vez que hayamos terminado de traducir todo el contenido, guardamos y cerramos la ventana.

![](assets/img/2023-ue-localization/tool_trans.png)

Haz clic en el conteo de palabras; al finalizar, podrás ver la cantidad de traducciones mostradas en la columna en chino:

![](assets/img/2023-ue-localization/tool_count.png)

Última versión del texto:

![](assets/img/2023-ue-localization/tool_build.png)

Los datos traducidos se almacenarán en `Content\Localization\EditorPlusTools`, con una carpeta para cada idioma. Dentro de zh-Hans, se pueden ver dos archivos: `.archive` es el texto recopilado y traducido, y `.locres` es el dato después de la compilación.

![](assets/img/2023-ue-localization/tool_ret.png)

![](assets/img/2023-ue-localization/tool_ret2.png)

##Coloca el texto traducido en el directorio del plugin.

Coloque los textos de traducción generados para el complemento en el directorio del proyecto, y luego muévalos al interior del complemento para facilitar su publicación junto con el mismo.

Mueve el directorio `Content\Localization\EditorPlusTools` a la carpeta de plugins Content, aquí es `Plugins\UE.EditorPlus\Content\Localization\EditorPlusTools`.

Edit the configuration file of the project `DefaultEditor.ini`, adding the new path:

```ini
[Internationalization]
+LocalizationPaths=%GAMEDIR%Plugins/UE.EditorPlus/Content/Localization/EditorPlusTools
```

De esta manera, otros proyectos que obtengan el plugin, simplemente modificando el `DefaultEditor.ini`, podrán utilizar el texto traducido sin necesidad de reconfigurar la traducción.

##Por favor, traduzca este texto al español:

 Nota por favor

Durante la creación de datos de traducción, se han encontrado algunos problemas, a continuación se resumen los aspectos a tener en cuenta:

- En el código, el texto debe definirse usando los macros `LOCTEXT` y `NSLOCTEXT`. El texto tiene que ser una constante de cadena, de esta manera UE podrá recopilarlo.
- El nombre del objetivo de la traducción no puede contener el símbolo `.`. Los nombres de las carpetas en `Content\Localization\` no pueden llevar `.`. UE solo tomará en cuenta el nombre antes del `.`. Esto puede provocar que UE no pueda leer el texto traducido debido a un error en el nombre, resultando en una lectura fallida.
- Para los plugins del editor, es necesario determinar si está en modo de línea de comandos `IsRunningCommandlet()`, en cuyo caso no se generarán los menús ni el SlateUI, ya que en modo de línea de comandos no hay módulos de Slate, lo que provocará un error al recopilar texto: `Assertion failed: CurrentApplication.IsValid()`. Si también encuentras un error similar, puedes intentar agregar esta verificación. Información específica del error:

    > Assertion failed: CurrentApplication.IsValid() [File:E:\UE\ue5.3_git\Engine\Source\Runtime\Slate\Public\Framework\Application\SlateApplication.h] [Line: 255] 

    ![](assets/img/2023-ue-localization/tool_error.png)

--8<-- "footer_es.md"


> Este post fue traducido usando ChatGPT, por favor en [**retroalimentación**](https://github.com/disenone/wiki_blog/issues/new)Indique cualquier omisión. 
