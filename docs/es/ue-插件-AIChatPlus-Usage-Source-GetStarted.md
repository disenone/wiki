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

#C++ Article - Empezar

##Introducción al código principal.

En la actualidad, el complemento se divide en los siguientes módulos:

* **AIChatPlusCommon**: Módulo de tiempo de ejecución (Runtime), responsable de manejar las solicitudes enviadas a través de diversas interfaces de API de inteligencia artificial y analizar el contenido de las respuestas.

* **AIChatPlusEditor**: Módulo del editor, encargado de implementar la herramienta de chat de IA del editor.

* **AIChatPlusCllama**: Módulo de tiempo de ejecución, encargado de encapsular la interfaz y los parámetros de llama.cpp para lograr la ejecución offline de modelos complejos.

**Thirdparty/LLAMACpp**: Módulo de terceros en tiempo de ejecución, que integra la biblioteca dinámica y los archivos de cabecera de llama.cpp.

El UClass específico responsable de enviar la solicitud es FAIChatPlus_xxxChatRequest. Cada servicio API tiene su propio UClass de solicitud independiente. Las respuestas a las solicitudes se obtienen a través de dos UClass diferentes, UAIChatPlus_ChatHandlerBase y UAIChatPlus_ImageHandlerBase, solo es necesario registrar los delegados de devolución de llamada correspondientes.

Antes de enviar una solicitud, es necesario configurar los parámetros de la API y el mensaje a enviar. Esto se hace a través de FAIChatPlus_xxxChatRequestBody. La respuesta específica también se analiza en FAIChatPlus_xxxChatResponseBody, que se puede obtener a través de una interfaz específica al recibir una devolución de llamada.

##El código utiliza el modelo fuera de línea Cllama(llama.cpp)

La siguiente explicación detalla cómo utilizar el modelo fuera de línea llama.cpp en el código.

Primero, también necesitas descargar el archivo del modelo en la carpeta Content/LLAMA.

Editar el código para agregar un comando y enviar un mensaje al modelo sin conexión dentro de dicho comando.

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

Después de compilar de nuevo, con el comando en el editor Cmd, podrás ver los resultados de la salida del gran modelo en el registro OutputLog.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

--8<-- "footer_es.md"


> Este mensaje fue traducido utilizando ChatGPT, por favor en[**反馈**](https://github.com/disenone/wiki_blog/issues/new)Señale cualquier omisión. 
