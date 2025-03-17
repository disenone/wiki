---
layout: post
title: Cllama (llama.cpp)
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
- llama.cpp
description: Cllama (llama.cpp)
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Cllama (llama.cpp)" />

#Documento de diseño - Cllama (llama.cpp)

![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_all.png)

##Modelo sin conexión

Cllama está implementado basado en llama.cpp y admite el uso offline de modelos de inferencia de IA.

Debido a que estamos sin conexión, necesitamos preparar primero el archivo del modelo, como por ejemplo, descargar el modelo sin conexión desde el sitio web de HuggingFace: [Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

Coloca el modelo en una carpeta específica, por ejemplo, en el directorio Content/LLAMA del proyecto de juego.

```shell
E:/UE/projects/FP_Test1/Content/LLAMA > ls
qwen1.5-1_8b-chat-q8_0.gguf*
```

Una vez que tengamos el archivo del modelo sin conexión, podremos utilizar Cllama para llevar a cabo un chat de IA.

##Conversación de texto

Usa Cllama para chatear por texto.

En el diagrama, haz clic derecho para crear un nodo llamado `Enviar solicitud de chat de Cllama`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_1.png)

Cree un nodo Options y establezca `Stream=true, ModelPath="E:\UE\projects\FP_Test1\Content\LLAMA\qwen1.5-1_8b-chat-q8_0.gguf"`

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_3.png)

Crear Messages, agregar un mensaje de Sistema y un mensaje de Usuario.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_4.png)

Crear un Delegado que acepte la información de salida del modelo y la imprima en la pantalla.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_5.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_6.png)

Un plano completo se vería así, ejecuta el plano para ver el mensaje que devuelve la pantalla del juego imprimiendo el modelo en gran escala.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_7.png)

![guide bludprint](assets/img/2024-ue-aichatplus/guide_blueprint_8.png)

##Generación de texto a partir de imágenes.

Cllama ha proporcionado soporte experimental para la biblioteca llava, ofreciendo capacidades de Vision.

Primero, prepara el archivo del modelo offline multimodal, como por ejemplo Moondream ([moondream2-text-model-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-text-model-f16.gguf), [moondream2-mmproj-f16.gguf](https://huggingface.co/vikhyatk/moondream2/blob/main/moondream2-mmproj-f16.gguf)）o Qwen2-VL（[Qwen2-VL-7B-Instruct-Q8_0.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/Qwen2-VL-7B-Instruct-Q8_0.gguf), [mmproj-Qwen2-VL-7B-Instruct-f16.gguf](https://huggingface.co/bartowski/Qwen2-VL-7B-Instruct-GGUF/resolve/main/mmproj-Qwen2-VL-7B-Instruct-f16.gguf)O cualquier otro modelo multimodal compatible con llama.cpp.

Cree un nodo de opciones y configure los parámetros "Ruta del Modelo" y "Ruta del Modelo del Proyecto de MM" con los archivos de modelo Multimodal correspondientes.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_1.png)

Crear un nodo para leer el archivo de imagen flower.png y configurar mensajes.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_2.png)

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_3.png)

Crear un nodo al final que reciba la información devuelta y la imprima en la pantalla. El aspecto completo del diagrama es el siguiente:

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_4.png)

Ejecutar el diagrama de flujo para ver el texto devuelto.

![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllama_vision_5.png)

##El archivo llama.cpp utiliza la GPU.

"Opciones de solicitud de chat de Cllama". Se ha añadido el parámetro "Num Gpu Layer" para ajustar la carga de GPU en llama.cpp, lo que permite controlar el número de capas que deben calcularse en la GPU. Ver imagen.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_1.png)

## KeepAlive

Añadir el parámetro "KeepAlive" a las "Opciones de solicitud de chat" puede mantener el archivo del modelo en la memoria después de la lectura, lo cual facilita su uso directo la próxima vez y reduce la cantidad de veces que se debe leer el modelo. KeepAlive indica cuánto tiempo se debe mantener el modelo en la memoria: 0 significa que no se guarda y se libera de inmediato después de usarlo; -1 significa que se mantiene de forma permanente. Cada vez que se realiza una solicitud, las Opciones pueden configurar un valor diferente de KeepAlive. El nuevo valor reemplazará al anterior; por ejemplo, las primeras solicitudes pueden establecer KeepAlive=-1 para mantener el modelo en memoria hasta que la última solicitud establezca KeepAlive=0 y libere el archivo del modelo.

##Manejar los archivos de modelos dentro del archivo .Pak después de empacar.

Una vez que se inicia el proceso de empaquetado de archivos con Pak, todos los recursos del proyecto se almacenarán en el archivo .Pak, incluyendo los archivos de modelo offline gguf.

Debido a que llama.cpp no puede leer directamente archivos .Pak, es necesario copiar los archivos de modelos offline del archivo .Pak al sistema de archivos.

AIChatPlus ha proporcionado una función que automáticamente copia y procesa los archivos de modelos en .Pak, colocándolos en la carpeta Guardado.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_cllama_gpu_3.png)

O también puedes manejar los archivos de modelos en .Pak tú mismo, lo importante es copiar los archivos, ya que llama.cpp no puede leer correctamente los archivos .Pak.

##Nodo de función

Cllama proporciona algunos nodos de función para facilitar la obtención del estado actual en el entorno.


"La validez de Cllama": Comprueba si Cllama llama.cpp está inicializado correctamente.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_1.png)

Determinar si llama.cpp es compatible con el backend de GPU en el entorno actual.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_2.png)

"Obtener Soporte Backends de Llama": Obtener todos los backends compatibles con llama.cpp actuales.


![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_3.png)

"Preparar modelo de archivo en Pak": Automaticamente copia los archivos de modelo en Pak al sistema de archivos.

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)


--8<-- "footer_es.md"


> Este mensaje ha sido traducido utilizando ChatGPT, por favor, en[**反馈**](https://github.com/disenone/wiki_blog/issues/new)Señalar cualquier omisión. 
