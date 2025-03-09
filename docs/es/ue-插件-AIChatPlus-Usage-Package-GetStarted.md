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
description: Embalaje
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - Package 篇 - Get Started" />

#Empaque

##Empaquetado de complementos

Cuando se realiza el empaquetado en Unreal, automáticamente se incluyen todos los archivos de biblioteca dinámica necesarios para el complemento, solo es necesario habilitar el complemento.

Por ejemplo, para Windows, el empaquetado automáticamente colocará los archivos llama.cpp y las DLL relacionadas con CUDA en el directorio empaquetado. Lo mismo se aplica para otras plataformas como Android, Mac e iOS.

Puedes ejecutar el comando "AIChatPlus.PrintCllamaInfo" en la versión de desarrollo del juego empaquetado para ver el estado actual del entorno Cllama, y confirmar si todo está en orden y si se admite la aceleración de GPU.

##Empaquetar el modelo.

Los archivos de modelo para unirse al proyecto están ubicados en el directorio Content/LLAMA. Así que puedes configurar para incluir este directorio al empaquetar.

Abre "Configuración del proyecto", selecciona la pestaña de Empaquetado, o busca directamente "paquete de activos", localiza la configuración "Directorios adicionales no pertenecientes a activos para empaquetar", y añade el directorio Content/LLAMA.

![](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_6.png)

Una vez que se ha añadido el índice, Unreal automáticamente empacará todos los archivos del índice al empaquetarlos.


##Leer el archivo de modelo sin conexión empaquetado.

Unreal generalmente empaqueta todos los archivos del proyecto en un archivo .Pak. En este caso, si se intenta pasar la ruta del archivo en el .Pak al modelo offline de Cllam, la ejecución fallará ya que llama.cpp no puede leer directamente los archivos del modelo empaquetados en el .Pak.

Por lo tanto, es necesario copiar los archivos de modelo del archivo .Pak al sistema de archivos primero. El complemento proporciona una función conveniente que permite copiar directamente los archivos de modelo del archivo .Pak y devolver la ruta del archivo copiado, para que Cllama pueda leerlos fácilmente.

Los nodos de blueprint son llamados "Cllama Prepare ModelFile In Pak": automáticamente copian los archivos de modelo en Pak al sistema de archivos.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

La función del código C++ es:

```
#include <Cllama/AIChatPlusCllama_Util.h>

auto ModelPath = FAIChatPlusCllama_Util::PrepareModelFileInPak(InContentPath);
```

--8<-- "footer_es.md"


> Este mensaje ha sido traducido utilizando ChatGPT, por favor [**proporcione retroalimentación**](https://github.com/disenone/wiki_blog/issues/new)Señalar cualquier omisión. 
