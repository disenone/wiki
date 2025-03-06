---
layout: post
title: Documento de instrucciones
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
description: Documento de explicación
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#Documento de instrucciones del complemento AIChatPlus de UE.

##Tienda de complementos

[AIChatPlus](https://www.fab.com/zh-cn/listings/0e49d138-10e1-452e-ba07-9a4bea578ace)

##Almacén público

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Introducción del complemento

La última versión v1.6.0.

Este complemento es compatible con UE5.2 - UE5.5.

UE.AIChatPlus es un complemento de UnrealEngine que permite la comunicación con diversos servicios de chat de inteligencia artificial GPT. Actualmente es compatible con servicios como OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, y llama.cpp en modo offline local. En el futuro se agregarán más proveedores de servicios. Su implementación se basa en solicitudes REST asíncronas, lo que garantiza un alto rendimiento y facilita la integración de estos servicios de chat AI para los desarrolladores de Unreal Engine.

UE.AIChatPlus también incluye una herramienta de edición que permite utilizar los servicios de chat AI directamente en la interfaz, generando texto e imágenes, y realizando análisis de imágenes, entre otras funciones.

##Función principal.

**¡Nuevo!** ¡AI sin conexión llama.cpp actualizado a la versión b4604!

**¡Nuevo!** ¡AI fuera de línea llama.cpp soporta GPU Cuda y Metal!

**¡Novedad!** ¡Compatible con la función de traducción de voz a texto de Gemini!

**API**: compatible con OpenAI, Azure OpenAI, Claude, Gemini, Ollama, llama.cpp, DeepSeek

**API en tiempo real sin conexión**: Compatible con la ejecución sin conexión de AI en llama.cpp, compatible con GPU Cuda y Metal.

**Texto a texto**: Varias API admiten la generación de texto.

**Texto a imagen**: OpenAI Dall-E

**Texto de la imagen**: OpenAI Vision, Claude, Gemini, Ollama, llama.cpp

**Imagen a imagen**: OpenAI DALL-E

**Transcripción de voz a texto**: Géminis

**Blueprint**: Todos los API y funciones son compatibles con el blueprint.

**Herramienta de chat con inteligencia artificial para editores**: una herramienta de chat cuidadosamente elaborada y llena de funciones para editores.

**Llamada asíncrona**: Todas las API pueden ser llamadas de forma asíncrona.

**Herramientas Prácticas**: Diversas herramientas para imágenes y audio.

##API compatible:

**llama.cpp fuera de línea**: Integrado con la biblioteca llama.cpp, permite ejecutar modelos de inteligencia artificial fuera de línea. ¡También es compatible con modelos multimodales (experimental)! Compatible con Win64/Mac/Android/IOS, y admite GPU CUDA y METAL.

**OpenAI**: /completados de chat, /completados, /generaciones de imágenes, /ediciones de imágenes, /variaciones de imágenes

Azure OpenAI: /chat/completions, /images/generations

**Claude**：/mensajes,/completar

**Géminis**：:generarTexto, :generarContenido, :generarContenidoDelFlujo

**Ollama**: /api/chat, /api/generate, /api/tags.

**DeepSeek**: /chat/completions

##Instrucciones de uso

(ue-插件-AIChatPlus-Usage-Blueprint-GetStarted.md)

[**Instrucciones de uso - C++**](ue-插件-AIChatPlus-Usage-Source-GetStarted.md)

(ue-插件-AIChatPlus-Usage-EditorTool-GetStarted.md)

##Modificar bitácora

(ue-插件-AIChatPlus-ChangeLogs.md)

##Soporte técnico

**Comentario**: Si tienes alguna pregunta, no dudes en dejar un mensaje en la sección de comentarios a continuación.

**Correo electrónico**: También puedes enviarme un correo electrónico a esta dirección ( disenonec@gmail.com )

**discord**: Próximamente disponible

--8<-- "footer_es.md"


> Este mensaje ha sido traducido usando ChatGPT. Por favor deja tus comentarios en [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Señale cualquier omisión. 
