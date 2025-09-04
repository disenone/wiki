---
layout: post
title: Empaque
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
- AI Chat
- Chatbot
- Image Generation
- OpenAI
- Azure
- Claude
- Gemini
- Ollama
description: Empaquetar
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - Package 篇 - Get Started" />

#Empaquetar

##Empaquetado de complementos

Cuando se empaqueta Unreal, automáticamente se incluyen los archivos de biblioteca dinámica necesarios para los complementos, simplemente activa el complemento.

Por ejemplo, para Windows, al empaquetar automáticamente se incluirán los archivos llama.cpp y las dll relacionadas con CUDA en el directorio empaquetado. Lo mismo ocurre para otras plataformas como Android, Mac e iOS.

Puedes ejecutar el comando "AIChatPlus.PrintCllamaInfo" en el juego de la versión de desarrollo empaquetado para verificar el estado del entorno Cllama actual, para confirmar si el estado es normal y si es compatible con el backend de GPU.

##Empaquetar el modelo

Si los archivos del modelo se encuentran en la carpeta Content/LLAMA dentro del proyecto, se puede configurar para que esta carpeta se incluya en el paquete durante el empaquetado.

Abre "Configuración del Proyecto", selecciona la pestaña "Empaquetado", o busca directamente "paquete de activos", y localiza la configuración "Directorios Adicionales No de Activos a Empaquetar". Añade el directorio Content/LLAMA.

![](assets/img/2024-ue-aichatplus/usage/package/getstarted_1.png)

Una vez añadido el directorio, Unreal automáticamente empaquetará todos los archivos del directorio al momento de empaquetar.

##Leer el archivo del modelo fuera de línea empaquetado.

Generalmente, Uneal empaqueta todos los archivos del proyecto en un archivo .Pak. En este caso, si se pasa la ruta del archivo .Pak al modelo fuera de línea Cllam, la ejecución fallará porque llama.cpp no puede leer directamente el archivo del modelo empaquetado en el archivo .Pak.

Por lo tanto, es necesario copiar los archivos de modelo del archivo .Pak al sistema de archivos primero. El complemento proporciona una función conveniente que permite copiar directamente los archivos de modelo del archivo .Pak y devuelve la ruta de archivo copiada, para que Cllama pueda leerlos fácilmente.

Los nodos de blueprint son "Cllama Prepare ModelFile In Pak": copia automáticamente los archivos de modelo en el sistema de archivos desde el Pak.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

La función del código en C++ es:

```
#include <Cllama/AIChatPlusCllama_Util.h>

auto ModelPath = FAIChatPlusCllama_Util::PrepareModelFileInPak(InContentPath);
```

--8<-- "footer_es.md"


> Este mensaje ha sido traducido usando ChatGPT, por favor, [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Señala cualquier omisión. 
