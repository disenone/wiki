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

#C++ 강좌 - 시작하기

##핵심 코드 소개

현재 플러그인은 다음 모듈로 분할됩니다:

* **AIChatPlusCommon**: 런타임 모듈(Runtime)은 다양한 AI API 인터페이스 요청을 처리하고 응답 내용을 해석하는 역할을 합니다.

* **AIChatPlusEditor**: 편집기 모듈(Editor)은 AI 채팅 도구를 편집하는 데 책임이 있습니다.

AIChatPlusCllama: 런타임 모듈(Runtime)은 llama.cpp의 인터페이스와 매개변수를 캡슐화하여 대규모 모델의 오프라인 실행을 구현합니다.

* **Thirdparty/LLAMACpp**: 런타임(이)시에 llama.cpp의 다이나믹 라이브러리와 헤더 파일이 통합된 제3자 모듈입니다.

특정 요청을 보낼 책임이 있는 UClass는 FAIChatPlus_xxxChatRequest입니다. 각 API 서비스마다 별도의 요청 UClass가 있습니다. 응답은 UAIChatPlus_ChatHandlerBase / UAIChatPlus_ImageHandlerBase 두 가지 UClass를 통해 받을 수 있으며, 해당하는 콜백 델리게이트를 등록하기만 하면 됩니다.

API 매개변수 및 전송 메시지를 설정한 후에 요청을 보내야 합니다. 이 부분은 FAIChatPlus_xxxChatRequestBody를 통해 설정됩니다. 또한 응답된 내용은 FAIChatPlus_xxxChatResponseBody로 구문 분석되며, 콜백을 받았을 때 특정 인터페이스를 통해 ResponseBody를 가져올 수 있습니다.

##"코드는 오프라인 모델 Cllama(llama.cpp)을 사용합니다."

코드에서 오프라인 모델 llama.cpp을 사용하는 방법에 대한 설명입니다.

먼저, Content/LLAMA 폴더에 모델 파일을 다운로드해야 합니다.

코드를 수정해서 명령어를 추가하고 해당 명령어를 통해 오프라인 모델에 메시지를 전송합니다.

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

재 컴파일 후, 편집기 Cmd에서 명령을 사용하여 OutputLog에서 대규모 모델의 출력 결과를 볼 수 있습니다.

![guide code](assets/img/2024-ue-aichatplus/guide_code_1.png)

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT를 사용하여 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)모든 누락 사항을 지적하십시오. 
