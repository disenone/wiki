---
layout: post
title: Documentación de instrucciones
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
description: Documentación de instrucciones
---

<meta property="og:title" content="UE 插件 AIChatPlus 说明文档" />

#Documentación del Complemento UE AIChatPlus

##Tienda de Plugins

[AIChatPlus](https://www.fab.com/zh-cn/listings/0e49d138-10e1-452e-ba07-9a4bea578ace)

##Depósito público

[UE.AIChatPlus.Public](https://github.com/disenone/UE.AIChatPlus.Public)

##Descripción del complemento

última versión v2.0.0.

Este complemento es compatible con UE5.2 a UE5.7.

UE.AIChatPlus es un complemento para UnrealEngine que permite la comunicación con diversos servicios de chat basados en IA GPT. Actualmente, admite servicios como OpenAI (ChatGPT, DALL-E), Azure OpenAI (ChatGPT, DALL-E), Claude, Google Gemini, Ollama y llama.cpp para uso local sin conexión. En el futuro, se añadirán más proveedores de servicios. Su implementación se basa en solicitudes REST asíncronas, asegurando un alto rendimiento y facilitando a los desarrolladores de UE la integración de estos servicios de chat con IA.

Además, UE.AIChatPlus incluye una herramienta de editor que permite utilizar directamente estos servicios de chat con IA dentro del editor, generando textos e imágenes, analizando imágenes, entre otras funciones.

##Funciones principales

**¡Nuevo!** Todas las API admiten ToolCall.

**¡Nuevo!** OpenAI/Azure admite speech-to-text y text-to-speech.

**¡Nuevo!** Los planos ahora admiten Json.

**¡Nuevo!** La IA fuera de línea llama.cpp se actualiza a la versión b6792.

**¡Nuevo!** AI fuera de línea llama.cpp con soporte para GPU Cuda y Metal.

**¡Nuevo!** Compatibilidad con Gemini de voz a texto.

**API**: Compatible con OpenAI, Azure OpenAI, Claude, Gemini, Ollama, llama.cpp, DeepSeek

**API en tiempo real sin conexión**: Admite el funcionamiento sin conexión de AI mediante llama.cpp, con soporte para GPU Cuda y Metal.

**Texto a texto**: Varias API admiten la generación de texto.

**Texto a imagen**: OpenAI Dall-E

**Convertir imagen a texto**: OpenAI Vision, Claude, Gemini, Ollama, llama.cpp

**Imagen a imagen**: OpenAI Dall-E

**Transcripción de voz a texto**: Gemini

**Plan Maestro**: Todas las API y funciones admiten planos.

**Editor de chat**: Una herramienta de chat con IA para editores, rica en funciones y elaborada cuidadosamente.

**Llamada asíncrona**: Todas las API pueden ser llamadas asíncronamente.

**Herramientas prácticas**: Variedad de herramientas de imagen y audio.

##API compatibles：

**Llama.cpp sin conexión**: ¡Integrado con la biblioteca llama.cpp, permite ejecutar modelos de IA fuera de línea! También incluye soporte para modelos multimodales (experimental). Compatible con Win64/Mac/Android/IOS. Soporta GPU CUDA y METAL.

**OpenAI**: /chat/completions, /completions, /images/generations, /images/edits, /images/variations

**Azure OpenAI**: /chat/completions, /images/generations

**Claude**: /mensajes, /completar

**Géminis**: generateText, generateContent, streamGenerateContent

**Ollama**: /api/chat, /api/generate, /api/tags

**DeepSeek**: /chat/completions

##Instrucciones de uso

[**Instrucciones de uso - Planos**](ue-插件-AIChatPlus-Usage-Blueprint-GetStarted.md)

[**Instrucciones de uso - Capítulo de C++**](ue-插件-AIChatPlus-Usage-Source-GetStarted.md)

[**Instrucciones de uso - Editor**](ue-插件-AIChatPlus-Usage-EditorTool-GetStarted.md)

[**Instrucciones de uso - Embalaje**](ue-插件-AIChatPlus-Usage-Package-GetStarted.md)

##Registro de cambios

[**Registro de Cambios**](ue-插件-AIChatPlus-ChangeLogs.md)

##Soporte técnico

**Comentarios**: Si tienes alguna pregunta, no dudes en dejarla en la sección de comentarios a continuación.

**Correo electrónico**: También puedes enviarme un correo electrónico a ( disenonec@gmail.com )

**discord**: Próximamente disponible

--8<-- "footer_es.md"


> Esta publicación está traducida con ChatGPT, por favor proporciona tu [**retroalimentación**](https://github.com/disenone/wiki_blog/issues/new)Indicar cualquier omisión en el texto. 
