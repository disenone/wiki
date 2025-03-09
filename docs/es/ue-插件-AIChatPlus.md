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
description: Documento de instrucciones
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#Documentación de instrucciones de AIChatPlus, complemento de UE.

##Tienda de complementos

[AIChatPlus](https://www.fab.com/zh-cn/listings/0e49d138-10e1-452e-ba07-9a4bea578ace)

##Almacén público

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Introducción del complemento.

La versión más reciente v1.6.0.

Este complemento es compatible con UE5.2 a UE5.5.

UE.AIChatPlus es un complemento para UnrealEngine que permite la comunicación con varios servicios de chat de inteligencia artificial GPT. Actualmente, los servicios compatibles incluyen OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama, y llama.cpp en modo offline local. En el futuro, se agregarán más proveedores de servicios. Su implementación se basa en solicitudes REST asíncronas, lo que garantiza un rendimiento eficiente y facilita la integración de estos servicios de chat de inteligencia artificial para los desarrolladores de UnrealEngine.

UE.AIChatPlus también incluye una herramienta de edición que permite utilizar directamente los servicios de chatbot de inteligencia artificial en el editor, para producir texto e imágenes, analizar imágenes, entre otras funciones.

##Función principal

**¡Nuevo!** AI offline llama.cpp actualizado a la versión b4604.

**¡Nuevo!** La función de IA offline llama.cpp es compatible con GPU Cuda y Metal.

**¡Novedad!** Admite la conversión de voz a texto en Gemini.

**API**: Compatible con OpenAI, Azure OpenAI, Claude, Gemini, Ollama, llama.cpp, DeepSeek.

**API en tiempo real fuera de línea**: compatible con la ejecución del AI llama.cpp fuera de línea, con soporte para GPU Cuda y Metal.

**Texto a texto**: Diversas APIs admiten la generación de texto.

**Texto a imagen**: OpenAI Dall-E

**Texto a imagen**: OpenAI Vision, Claude, Gemini, Ollama, llama.cpp

**Imagen a imagen**: OpenAI Dall-E

**Transcripción de voz a texto**: Géminis

**Blueprint**: All API and features support blueprints.

**Herramienta de chat de IA del editor**: una herramienta de chat de IA de editor cuidadosamente diseñada y repleta de funciones.

**Llamada asincrónica**: Todas las API pueden ser invocadas de forma asincrónica.

**Herramientas prácticas**: diversas herramientas de imagen y audio.

##API soportadas:

**Offline llama.cpp**: Integrated with the llama.cpp library, it enables offline execution of AI models! It also supports multimodal models (experimental). Compatible with Win64/Mac/Android/IOS. Supports GPU CUDA and METAL.

OpenAI: /chat/completions, /completions, /images/generations, /images/edits, /images/variations

Azure OpenAI: /chat/completions, /images/generations

**Claude**: /mensajes、/completar

**: Gemini **: generarTexto, generarContenido, streamGenerarContenido.

**Ollama**: /api/chat, /api/generate, /api/tags

**DeepSeek**: /chat/completions

##Instrucciones de uso

[**Instrucciones de uso - Sección de planos**](ue-插件-AIChatPlus-Usage-Blueprint-GetStarted.md)

(ue-插件-AIChatPlus-Usage-Source-GetStarted.md)

[**Instrucciones de uso - Editor**](ue-插件-AIChatPlus-Usage-EditorTool-GetStarted.md)

(ue-插件-AIChatPlus-Usage-Package-GetStarted.md)

##Modificar el registro

[**Change log**](ue-插件-AIChatPlus-ChangeLogs.md)

##Soporte técnico

**Comentario**: Si tienes alguna pregunta, no dudes en dejar un mensaje en la sección de comentarios a continuación.

**Correo electrónico**: También puedes enviarme un correo electrónico a través de mi dirección de correo (disenonec@gmail.com)

**discord**: Próximamente disponible.

--8<-- "footer_es.md"


> Este mensaje fue traducido utilizando ChatGPT, por favor [**proporciona retroalimentación**](https://github.com/disenone/wiki_blog/issues/new)Señalar cualquier omisión. 
