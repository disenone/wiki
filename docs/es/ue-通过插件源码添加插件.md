---
layout: post
title: UE permite agregar complementos mediante el código fuente del complemento.
date: 2023-12-01
categories:
- c++
- ue
catalog: true
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
description: Voy a hacer un breve registro sobre cómo agregar un complemento a UE
  cuando se tiene el código fuente del complemento.
figures: []
---

<meta property="og:title" content="UE 通过插件源码添加插件" />

#UE (Unreal Engine) permite agregar complementos mediante el código fuente del complemento.

#**Agregar complemento**

> Registra brevemente cómo agregar un complemento cuando dispones del código fuente del mismo.

以插件 [UE.EditorPlus]

Utilizando el complemento [UE.EditorPlus], se puede mejorar la funcionalidad de tu editor de Unreal Engine. Este complemento proporciona características adicionales y herramientas que te permiten optimizar y personalizar tu flujo de trabajo de desarrollo de juegos. Con [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)Para ilustrar

- Coloca el código fuente en el directorio de Plugins.
- （Esta etapa es opcional）Modifica el archivo .uproject del proyecto, agrega lo siguiente en el campo Plugins:
    ```json
        "Plugins": [
        {
            "Name": "EditorPlus",
            "Enabled": true,
            "TargetAllowList": [
                "Editor"
            ]
        }
    ```
- Haz clic derecho en el archivo uproject, selecciona "Generate Visual Studio Project Files" y actualiza el archivo del proyecto sln.
- Abrir el archivo sln y compilar el proyecto.

#**Configuración de múltiples idiomas**

Modificar el archivo de configuración del proyecto `DefaultEditor.ini`, añadir la nueva ruta:

```ini
[Internationalization]
+LocalizationPaths=%GAMEDIR%Plugins/UE.EditorPlus/Content/Localization/EditorPlusTools
```


--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
