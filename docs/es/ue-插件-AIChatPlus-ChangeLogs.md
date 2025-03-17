---
layout: post
title: Registro de versiones
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
description: Registro de versiones
---

<meta property="og:title" content="UE 插件 AIChatPlus 版本日志" />

#Registro de versiones del complemento de UE AIChatPlus.

## v1.6.2 - 2025.03.17

###Nueva función

Aumenta el parámetro KeepContext de Cllama a su valor predeterminado false. El Context se destruye automáticamente al finalizar el Chat.

Agrega el parámetro KeepAlive a `Cllama`, puede ayudar a reducir la lectura repetida del modelo.

## v1.6.1 - 2025.03.07

### Bug Fix

OpenAI Image Chat supports inputting images.

Herramienta de edición de mmproj que permite el modelo vacío.

## v1.6.0 - 2025.03.02

###Nueva función.

Actualización de llama.cpp a la versión b4604.

* Cllama supports GPU backends: cuda and metal.

La herramienta de chat Cllama admite el uso de GPU.

Soportar la lectura de archivos de modelo empaquetados en Pak.

### Bug Fix

Corregir el problema de Cllama que provoca un fallo al recargar durante la inferencia.

Reparar error de compilación en iOS.

## v1.5.1 - 2025.01.30

###Nuevas características.

Solo se permite la transmisión de audio para Gemini.

Optimizar el método para obtener PCMData, descomprimir los datos de audio al generar B64.

Solicitar añadir dos callbacks OnMessageFinished y OnImagesFinished.

Optimiza el Método Gemini, obteniendo automáticamente el Método según bStream.

Agregar algunas funciones de blueprint para facilitar la conversión de Wrapper a tipos reales, y para obtener el mensaje de respuesta y los errores.

### Bug Fix

Corregido el problema de múltiples llamadas a Request Finish.

## v1.5.0 - 2025.01.29

###Nueva función.

Apoyar el envío de archivos de audio a Gemini.

Las herramientas del editor admiten el envío de audio y grabaciones.

### Bug Fix

Corregir el error de copia de sesión fallido.

## v1.4.1 - 2025.01.04

###Reparación de problemas

Apoyo para enviar solo fotos sin mensajes en la herramienta de chat.

Reparar fallo al enviar imágenes a través de la interfaz de OpenAI.

Corregir la omisión de los parámetros Quality, Style y ApiVersion en la configuración de las herramientas de chat OpanAI y Azure.

## v1.4.0 - 2024.12.30

###Nueva función

* (Función experimental) Cllama (llama.cpp) admite modelos multimodales y puede procesar imágenes.

Todos los parámetros de tipo blueprint ahora tienen instrucciones detalladas agregadas.

## v1.3.4 - 2024.12.05

###Nueva funcionalidad

OpenAI admite la API de visión.

###Reparación de problemas

Corregir el error al establecer OpenAI stream=false.

## v1.3.3 - 2024.11.25

###Nueva función

Compatible con UE-5.5.

###Reparación de problemas

Corregir el problema de ciertos planos que no funcionan.

## v1.3.2 - 2024.10.10

###Reparación de problemas.

Reparar el fallo de cllama al detener manualmente la solicitud.

Corregir el problema en la versión de descarga de Win del centro comercial donde no se encuentra el archivo ggml.dll o llama.dll.

Crear solicitud y verificar en el hilo del juego si CreateRequest está activo.

## v1.3.1 - 2024.9.30

###Nueva característica

Agregar un SystemTemplateViewer que permita ver y utilizar cientos de plantillas de configuración del sistema.

###Reparación de problemas

Reparar el plugin descargado de la tienda, no se encuentra la biblioteca de vínculos llama.cpp.

Corregir el problema de la ruta demasiado larga en LLAMACpp

Reparar el error del archivo de enlace llama.dll después de empaquetar Windows.

Corregir problema de lectura de ruta de archivos en iOS/Android.

Reparar el error en la configuración del nombre de Cllame.

## v1.3.0 - 2024.9.23

###Important new feature

Integración de llama.cpp para admitir la ejecución local sin conexión de grandes modelos.

## v1.2.0 - 2024.08.20

###Nueva función

Apoyo a OpenAI Image Edit/Image Variation.

Admite la API de Ollama, admite la obtención automática de la lista de modelos admitidos por Ollama.

## v1.1.0 - 2024.08.07

###Nueva función.

Apoyar el plan estratégico.

## v1.0.0 - 2024.08.05

###Nueva función

Funcionalidad básica completa

Apoyo a OpenAI, Azure, Claude y Gemini.

Herramienta de chat con editor incorporado y funciones completas.

--8<-- "footer_es.md"


> Este mensaje ha sido traducido utilizando ChatGPT, por favor en [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Señalar cualquier omisión. 
