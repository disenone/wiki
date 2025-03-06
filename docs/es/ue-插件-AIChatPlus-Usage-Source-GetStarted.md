---
layout: post
title: Get Started
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
description: Get Started
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - C++ 篇 - Get Started" />

#C++ Artículo - Empezar

##Presentación del código central

En la actualidad, el complemento se divide en los siguientes módulos:

AIChatPlusCommon: Módulo de tiempo de ejecución responsable de procesar las solicitudes enviadas a través de diversas interfaces de API de IA y analizar el contenido de las respuestas.

AIChatPlusEditor: Módulo del editor, encargado de implementar la herramienta de chat AI del editor.

AIChatPlusCllama: Módulo de tiempo de ejecución (Runtime) responsable de encapsular la interfaz y los parámetros de llama.cpp para lograr la ejecución sin conexión de modelos grandes.

Terceros/LLAMACpp: Módulo de tercero en tiempo de ejecución que integra la biblioteca dinámica y archivos de cabecera de llama.cpp.

El UClass responsable de enviar la solicitud específica es FAIChatPlus_xxxChatRequest, cada servicio API tiene su propio UClass de solicitud independiente. Las respuestas de la solicitud se obtienen a través de UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase, solo es necesario registrar el delegado de devolución de llamada correspondiente.

Antes de enviar la solicitud, es necesario configurar los parámetros de la API y el mensaje a enviar, esto se hace a través de FAIChatPlus_xxxChatRequestBody. El contenido específico de la respuesta también se analiza en FAIChatPlus_xxxChatResponseBody, y al recibir la devolución, se puede obtener el ResponseBody a través de una interfaz específica.

##El código utiliza el modelo fuera de línea Cllama(llama.cpp).

Les paso las instrucciones sobre cómo utilizar el modelo fuera de línea llama.cpp en el código.

Primero, también es necesario descargar el archivo del modelo en Content/LLAMA.

Modificar el código para incluir un comando y enviar un mensaje al modelo sin conexión dentro de dicho comando.

```c++
#include "Common/AIChatPlus_Log.h"
#include "Common_Cllama/AIChatPlus_CllamaChatRequest.h"

void AddTestCommand()
{
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("AIChatPlus.TestChat"),
		TEXT("Test Chat."),
		FConsoleCommandDelegate::CreateLambda([]()
		{
			if (!FModuleManager::GetModulePtr<FAIChatPlusCommon>(TEXT("AIChatPlusCommon"))) return;

			TWeakObjectPtr<UAIChatPlus_ChatHandlerBase> HandlerObject = UAIChatPlus_ChatHandlerBase::New();
			// Cllama

			FAIChatPlus_CllamaChatRequestOptions Options;

			Options.ModelPath.FilePath = FPaths::ProjectContentDir() / "LLAMA" / "qwen1.5-1_8b-chat-q8_0.gguf";
			Options.NumPredict = 400;
			Options.bStream = true;
			// Options.StopSequences.Emplace(TEXT("json"));
			auto RequestPtr = UAIChatPlus_CllamaChatRequest::CreateWithOptionsAndMessages(

				Options,
				{
					{"You are a chat bot", EAIChatPlus_ChatRole::System},
					{"who are you", EAIChatPlus_ChatRole::User}
				});

			HandlerObject->BindChatRequest(RequestPtr);
			const FName ApiName = TEnumTraits<EAIChatPlus_ChatApiProvider>::ToName(RequestPtr->GetApiProvider());

			HandlerObject->OnMessage.AddLambda([ApiName](const FString& Message)
			{
				UE_LOG(AIChatPlus_Internal, Display, TEXT("TestChat[%s] Message: [%s]"), *ApiName.ToString(), *Message);
			});
			HandlerObject->OnStarted.AddLambda([ApiName]()
			{
				UE_LOG(AIChatPlus_Internal, Display, TEXT("TestChat[%s] RequestStarted"), *ApiName.ToString());
			});
			HandlerObject->OnFailed.AddLambda([ApiName](const FAIChatPlus_ResponseErrorBase& InError)
			{
				UE_LOG(AIChatPlus_Internal, Error, TEXT("TestChat[%s] RequestFailed: %s "), *ApiName.ToString(), *InError.GetDescription());
			});
			HandlerObject->OnUpdated.AddLambda([ApiName](const FAIChatPlus_ResponseBodyBase& ResponseBody)
			{
				UE_LOG(AIChatPlus_Internal, Display, TEXT("TestChat[%s] RequestUpdated"), *ApiName.ToString());
			});
			HandlerObject->OnFinished.AddLambda([ApiName](const FAIChatPlus_ResponseBodyBase& ResponseBody)
			{
				UE_LOG(AIChatPlus_Internal, Display, TEXT("TestChat[%s] RequestFinished"), *ApiName.ToString());
			});

			RequestPtr->SendRequest();
		}),
		ECVF_Default
	);
}
```

Una vez que hayas recompilado, puedes usar el comando en la ventana del editor Cmd para ver los resultados de salida del modelo grande en el registro OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

--8<-- "footer_es.md"


> Este mensaje ha sido traducido utilizando ChatGPT, por favor déjenos su [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Señale cualquier omisión. 
