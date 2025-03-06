---
layout: post
title: OpenAI
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
description: OpenAI
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - OpenAI" />

#Sección Blueprint - OpenAI

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_all.png)

En [Empezar](ue-插件-AIChatPlus-Usage-Blueprint-GetStarted.md)Se ha presentado anteriormente el uso básico de OpenAI en secciones anteriores, ahora ofrecemos una descripción más detallada de su uso aquí.

##Charla de texto

Utilizar OpenAI para chatear por texto

En la vista de diseño, haz clic derecho para crear un nodo llamado `Enviar solicitud de chat de OpenAI en el mundo`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_1.png)

Crea un nodo de Opciones y establece `Stream=true, Api Key="tu clave de API de OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_2.png)

Crear mensajes, agregar un mensaje del sistema y un mensaje del usuario.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Establecer un Delegado que reciba la información de salida del modelo y la imprima en pantalla.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

El aspecto de un blueprint completo es este: ejecuta el blueprint y verás en la pantalla del juego el mensaje que devuelve la impresión del gran modelo.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_3.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_blueprint_4.png)

##Este texto generará una imagen.

Utilizando OpenAI para crear imágenes.

En el diagrama, haz clic derecho para crear un nodo llamado `Send OpenAI Image Request` y establece `In Prompt="una hermosa mariposa"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_1.png)

Crea un nodo de Options y establece `Api Key="tu clave de API de OpenAI"`.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_2.png)

Vincula el evento "On Images" y guarda las imágenes en el disco duro local.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_3.png)

El esquema completo se ve así, ejecuta el esquema y verás que la imagen se guarda en la ubicación especificada.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_4.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_openai_image_blueprint_5.png)

##Generación de texto a partir de imágenes.

Utilizar OpenAI Vision para analizar imágenes.

En el blueprint, haz clic derecho y crea un nodo llamado 'Enviar solicitud de imagen a OpenAI'.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_1.png)

Crear un nodo de Options y establecer `Api Key="tu clave de API de OpenAI"`, configurar el modelo como `gpt-4o-mini`.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_2.png)

Crear Mensajes.
Crear primero un nodo "Importar archivo como textura 2D" para cargar una imagen desde el sistema de archivos.
Utilizando el nodo "Crear textura AIChatPlus a partir de Texture2D" para convertir la imagen en un objeto utilizable por el complemento.
Conecta las imágenes al campo "Images" del nodo "AIChatPlus_ChatRequestMessage" usando el nodo "Make Array".
Establecer el contenido del campo "Content" como "describir esta imagen".

Según la imagen:

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_3.png)

La representación completa del diseño se ve así, al ejecutar el diseño, podrás ver los resultados mostrados en la pantalla.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/getstarted_vision_4.png)

##Editar imagen

OpenAI supports modifying regions labeled in images.

Primero, prepare dos imágenes.

Una imagen que necesita ser modificada src.png

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_1.png)

Una de las imágenes es mask.png, en la que se señalan las áreas que necesitan ser modificadas. Puedes modificar la imagen original estableciendo la opacidad de las áreas modificadas en 0, es decir, cambiando el valor del canal alfa a 0.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_2.png)

Leer cada una de esas dos fotos por separado y combinarlas en un array.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_3.png)

Por favor, crea un nodo "OpenAI Image Options", establece ChatType = Edit y cambia "End Point Url" a v1/images/edits.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_4.png)

Crea una "Solicitud de Imagen OpenAI", establece el "Desencadenante" como "cambiar en dos mariposas", conecta el nodo "Opciones" con la matriz de imágenes y guarda las imágenes generadas en el sistema de archivos.

El plano completo se ve así:

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_5.png)

Ejecutar el diagrama, guardando la imagen generada en la ubicación especificada.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_6.png)

##Variantes de imagen

OpenAI es capaz de generar variantes similares a partir de una imagen de entrada. (Variación)

Primero, prepara una imagen llamada src.png y luego impórtala en el blueprint.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_1.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_1.png)

Crear un nodo "OpenAI Image Options", establecer ChatType = Variación y modificar "End Point Url" = v1/images/variations.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_2.png)

Crear la solicitud de imagen de OpenAI, dejando el campo "Prompt" vacío, conectar el nodo de "Opciones" con la imagen, y guardar la imagen generada en el sistema de archivos.

El texto traducido al español es: "El plano completo se ve así:"

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_3.png)

Ejecutar el diagrama, guardar la imagen generada en la ubicación especificada.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_variation_4.png)

--8<-- "footer_es.md"


> Este mensaje ha sido traducido utilizando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Indica cualquier omisión. 
