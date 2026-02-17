---
layout: post
title: Json 연산
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
- Json
- Blueprint
description: Json 작업
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Json 操作" />

#청사진편 - Json 조작

<!-- 이미지 필요: Json 관련 모든 블루프린트 노드 개요를 보여주는 이미지. JsonObject, JsonArray, JsonLibrary 분류 아래의 노드들을 포함해야 함 -->
![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_all.png)

##개요

AIChatPlus는 완벽한 JSON 블루프린트 조작 지원을 제공하여 블루프린트에서 JSON 데이터를 처리하는 데 편리합니다. 주로 세 가지 클래스로 구성됩니다:

* **UAIChatPlus_JsonObject**: JSON 객체 작업 클래스로, `{}` 형식의 JSON을 처리합니다.
* **UAIChatPlus_JsonArray**: JSON 배열 조작 클래스로, `[]` 형식의 JSON을 처리하는 데 사용됩니다
* **UAIChatPlus_JsonLibrary**: JSON 유틸리티 함수 라이브러리로, 정적 도구 함수를 제공합니다.

이 클래스들은 다음을 지원합니다:
* JSON 생성, 파싱, 직렬화
* 필드 값 읽기 및 설정하기
* 중첩 경로 쿼리
* JSON과 USTRUCT 상호 변환
* 파일 읽기 및 쓰기
* 체이닝 호출

##JsonObject 기본 연산

###JsonObject 생성하기

`Create Json Object`를 사용하여 빈 JSON 객체 만들기:

<!-- 이미지 필요: 블루프린트 내에서 우클릭하여 "Create Json Object"를 검색하고 노드를 생성하는 스크린샷을 보여주세요 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_create_1.png)

###문자열에서 파싱하기

`Parse Json Object`을 사용하여 JSON 문자열에서 객체 생성하기:

<!-- 이미지 필요: Parse Json Object 노드를 보여주고, '{"name":"test","value":123}' 같은 JSON 문자열을 입력하면 JsonObject, bSuccess, ErrorMessage를 출력함 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_parse_1.png)

###필드 값 설정

JsonObject은 다양한 Set 메서드를 제공하며, 체인 호출을 지원합니다:

| 함수 | 설명 |
|-----|------|
| `문자열 필드 설정` | 문자열 필드 설정 |
| `Set Number Field` | 부동 소수점 숫자 필드 설정 |
| `Set Integer Field` | 정수 필드 설정 |
| `Set Boolean Field` | 부울 필드 설정 |
| `Set Object Field` | 중첩 객체 필드 설정 |
| `배열 필드 설정` | 배열 필드 설정 |
| `NULL 필드 설정` | null 필드 설정 |

<!-- 이미지 필요: 여러 필드를 연쇄적으로 설정하는 블루프린트를 보여주는 예시, 예를 들어 Create Json Object -> Set String Field("name", "player1") -> Set Integer Field("level", 10) -> Set Boolean Field("active", true) -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_set_1.png)

###필드 값 가져오기

JsonObject은 다음과 같은 다양한 Get 메서드를 제공합니다:

| 함수 | 설명 |
|-----|------|
| `Get String Field` | 문자열 필드 가져오기 |
| `Get Number Field` | 부동 소수점 필드 가져오기 |
| `Get Integer Field` | 정수 필드 가져오기 |
| `불리언 필드 가져오기` | 불리언 필드 가져오기 |
| `객체 필드 가져오기` | 중첩된 객체 필드 가져오기 |
| `Get Array Field` | 배열 필드 가져오기 |

<!-- 이미지 필요: JsonObject에서 필드 값을 가져오는 블루프린트 예시, Get String Field 노드를 사용하여 "name" 필드를 가져오는 것을 보여주며, DefaultValue와 bSuccess 매개변수 표시 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_get_1.png)

###필드 검사

| 함수 | 설명 |
|-----|------|
| `필드가 있음` | 필드 존재 여부 확인 |
| `Get Field Type` | 필드 유형 가져오기 |
| `Get Field Names` | 모든 필드 이름 가져오기 |
| `Remove Field` | 필드 제거 |
| `Clear` | 모든 필드 지우기 |

<!-- 이미지 요청: Has Field로 필드 존재 여부를 확인하고, Get Field Type으로 필드 유형을 가져오는 블루프린트를 보여주는 이미지 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_check_1.png)

###문자열로 직렬화

`To Json String`을 사용하여 JsonObject를 문자열로 변환합니다:

<!-- 필요한 이미지: To Json String 노드 표시, JsonObject 입력, bPrettyPrint 매개변수, 출력으로 포맷팅된 JSON 문자열 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_tostring_1.png)

##JsonArray 기본 작업

###JsonArray 생성하기

`Create Json Array`를 사용하여 빈 JSON 배열을 생성합니다:

<!-- 필요 이미지: 청사진에서 Create Json Array 노드를 생성하는 화면 캡처 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_create_1.png)

###요소 추가

JsonArray는 다양한 Add 메소드를 제공하며, 체이닝 호출을 지원합니다:

| 함수 | 설명 |
|-----|------|
| '문자열 추가' | 문자열 요소 추가 |
| `Add Number` | 부동 소수점 요소 추가 |
| `Add Integer` | 정수 요소 추가 |
| `Add Boolean` | 불리언 요소 추가 |
| `Add Object` | 객체 요소 추가 |
| `Add Array` | 배열 요소 추가 |
| `Add Null` | null 요소 추가 |

<!-- 이미지 필요: 여러 요소를 체이닝 방식으로 추가하는 블루프린트를 보여주는 예시. 예를 들어 Create Json Array -> Add String("a") -> Add String("b") -> Add Integer(123) -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_add_1.png)

###요소 가져오기

JsonArray는 인덱스로 요소를 가져오는 방법을 제공합니다:

| 함수 | 설명 |
|-----|------|
| `Get String` | 문자열 요소 가져오기 |
| `숫자 가져오기` | 부동소수점 숫자 요소 가져오기 |
| `Get Integer` | 정수 요소 가져오기 |
| `Get Boolean` | 불리언 요소 가져오기 |
| `Get Object` | 객체 요소 가져오기 |
| `배열 가져오기` | 배열 요소 가져오기 |

<!-- 이미지 필요: Get Object by Index를 사용하여 배열 내 객체 요소를 가져오는 블루프린트 예시 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_get_1.png)

###배열 조작

| 함수 | 설명 |
|-----|------|
| `Length` | 배열의 길이를 가져옵니다 |
| `Is Valid Index` | 인덱스가 유효한지 확인합니다 |
| `Get Element Type` | 요소 유형 가져오기 |
| `Remove At` | 지정된 인덱스의 요소 삭제 |
| `Clear` | 배열 비우기 |

<!-- 이미지 필요: Length를 사용해 배열 길이를 가져오고 For Loop로 배열을 순회하는 블루프린트를 보여주는 예시 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_loop_1.png)

###일괄 변환

JsonArray는 UE 배열과의 일괄 변환을 지원합니다:

| 함수 | 설명 |
|-----|------|
| `From String Array` | 문자열 배열에서 생성 |
| `To String Array` | 문자열 배열로 변환 |
| `From Integer Array` | 정수 배열로부터 생성 |
| `To Integer Array` | 정수 배열로 변환 |

<!-- 이미지 필요: From String Array 및 To String Array 사용 예시 보여주기 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_batch_1.png)

##경로 조회

JsonObject는 `player.inventory.gold`와 같이 점으로 구분된 경로를 사용하여 중첩된 데이터에 접근할 수 있도록 지원합니다.

###경로로 값 가져오기

경로로 문자열 값 가져오기 위해 `Get String By Path` 사용하기:

```json
{
    "player": {
        "name": "Hero",
        "inventory": {
            "gold": 1000
        }
    }
}
```

<!-- 이미지 필요: "player.name"으로 Path가 설정된 Get String By Path 노드를 사용하여 중첩된 값을 가져오는 블루프린트를 보여줌 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_path_get_1.png)

###경로에 따라 값 설정하기

경로를 따라 값을 설정하려면 `Set String By Path`를 사용하세요:

<!-- 필요 이미지: Set String By Path 노드를 사용하여 중첩 경로 값을 설정하는 블루프린트를 보여주는 이미지로, FAIChatPlus_JsonPathOptions 파라미터(bCaseSensitive, bCreateMissing)가 표시되어야 함 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_path_set_1.png)

###조회 결과

경로 조회는 `FAIChatPlus_JsonQueryResult` 구조체를 반환하며, 여기에는 다음이 포함됩니다:

* **bSuccess**: 쿼리 성공 여부
* **ValueType**: 반환값의 유형
* **ErrorMessage**: 오류 메시지(실패한 경우)

<!-- 이미지 필요: Break FAIChatPlus_JsonQueryResult 노드를 보여주고, bSuccess, ValueType, ErrorMessage 필드를 표시해야 함 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_path_result_1.png)

##JSON과 USTRUCT 변환

AIChatPlus는 JSON과 USTRUCT 간 변환을 지원하여 블루프린트 구조체와 손쉽게 연동할 수 있도록 합니다.

###JSON 문자열을 USTRUCT로 변환

`Json String To Struct`를 사용하여 JSON 문자열을 USTRUCT로 직접 변환하기

<!-- 이미지 필요: Json String To Struct 노드 표시, JSON 문자열 입력, 출력 파라미터가 사용자 정의 USTRUCT 변수(예: FAIChatPlus_OpenAIChatRequestOptions)에 연결된 상태 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_struct_1.png)

###USTRUCT를 JSON 문자열로 변환

`Struct To Json String`를 사용하여 USTRUCT를 JSON 문자열로 변환합니다:

<!-- 이미지 필요: Struct To Json String 노드 표시, USTRUCT 변수 입력, bPrettyPrint 매개변수, JSON 문자열 출력 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_struct_2.png)

###JsonObject을 USTRUCT로 변환

JsonObject의 `To Struct` 메소드 사용하기:

<!-- 이미지 필요: JsonObject의 To Struct 노드 사용법을 보여주는 그림 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_struct_3.png)

###USTRUCT를 JsonObject로 변환

`From Struct` 정적 메서드를 사용하여 USTRUCT에서 JsonObject 생성하기:

<!-- 필요 이미지: From Struct 노드 표시, 입력은 USTRUCT, 출력은 JsonObject -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_struct_4.png)

##JsonLibrary 유틸리티 함수

`UAIChatPlus_JsonLibrary`는 일련의 정적 도구 함수들을 제공합니다.

###빠른 생성

| 함수 | 설명 |
|-----|------|
| `문자열 필드로 Json 객체 만들기` | 빠르게 단일 필드를 가진 JsonObject 생성하기 |
| `Make Json Object From String Map` | 맵으로부터 JsonObject 생성하기 |

<!-- 필요 이미지: Make Json Object From String Map 사용 예시, 입력은 TMap<FString, FString>, 출력은 JsonObject를 보여주는 블루프린트 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_make_1.png)

#### 검증

| 함수 | 설명 |
|-----|------|
| `Validate Json String` | JSON 문자열 유효성 검사 |
| `Is Json Object` | JSON 객체인지 확인 |
| `Is Json Array` | JSON 배열인지 확인합니다 |

<!-- 이미지 필요: Validate Json String을 사용하여 JSON 문자열을 검증하는 블루프린트를 보여주는 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_validate_1.png)

###포맷

| 함수 | 설명 |
|-----|------|
| `Prettify Json` | JSON 예쁘게 만들기 (들여쓰기 및 줄바꿈 추가) |
| `Minify Json` | JSON 압축(공백 제거) |

<!-- 이미지 필요: Prettify Json을 사용하여 JSON 문자열을 포맷팅하는 모습을 보여주며, 입력된 압축된 JSON과 출력된 포맷팅된 JSON을 표시 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_format_1.png)

###파일 작업

| 함수 | 설명 |
|-----|------|
| `Load Json Object From File` | 파일에서 JsonObject 로드하기 |
| `Save Json Object To File` | JsonObject를 파일에 저장 |
| `Load Json Array From File` | 파일에서 JsonArray 로드하기 |
| `Save Json Array To File` | JsonArray를 파일에 저장 |

<!-- 이미지 필요: Save Json Object To File 및 Load Json Object From File 사용 예시 표시 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_file_1.png)

###비교

| 함수 | 설명 |
|-----|------|
| `Equals Json Object` | 두 JsonObject가 같은지 비교합니다 |
| `Equals Json Array` | 두 JsonArray가 동일한지 비교합니다 |

<!-- 이미지 필요: Equals Json Object를 사용하여 두 JsonObject를 비교하는 블루프린트를 보여주는 이미지 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_compare_1.png)

###고급 경로 조회

| 함수 | 설명 |
|-----|------|
| `Query String By Path` | 경로로 문자열 조회하기 (배열 인덱스 지원, 예: `items[0].name`) |
| `Query Object By Path` | 경로별 객체 조회 |
| `경로별 배열 조회` | 배열을 경로별로 조회 |

<!-- 이미지 필요: 배열 인덱스가 포함된 경로(예: "data.items[0].name")를 Query String By Path로 조회하는 것을 보여주는 이미지 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_query_1.png)

###일괄 처리

| 함수 | 설명 |
|-----|------|
| `맵에서 문자열 필드 설정` | 문자열 필드 일괄 설정 |
| `Get String Fields To Map` | 문자열 필드를 매핑하기 위해 가져오기 |

<!-- 이미지 필요: Set String Fields From Map를 사용하여 필드를 일괄 설정하는 블루프린트 예시 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_batch_1.png)

##기타 작업

###JSON 객체 합치기

두 개의 JsonObject를 `Merge` 메서드로 병합하기:

<!-- 이미지 필요: Merge 노드를 보여주고, 두 JsonObject를 병합하며 bOverwrite 매개변수를 표시 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_merge_1.png)

###JsonObject 복사

`Duplicate` 메서드를 사용하여 JsonObject 깊은 복사하기:

<!-- 필요한 이미지: Duplicate 노드가 JsonObject를 복제하는 블루프린트를 보여주는 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_dup_1.png)

##실제 응용 예시

###API 응답 분석

AI 채팅 응답에서 Tool Call의 매개변수 추출:

<!-- 이미지 필요: 완전한 파싱 예시 블루프린트를 보여주는 이미지: FunctionArguments 문자열을 JsonObject로 Parse한 다음, Get String Field를 사용하여 매개변수 값을 가져오는 과정 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_example_1.png)

###요청 매개변수 구성

JsonObject를 사용하여 복잡한 요청 파라미터 구성하기:

<!-- 이미지 필요: 중첩된 JSON 구조를 구축하는 청사진을 보여주며, 여러 필드를 설정하는 JsonObject를 생성하고, 중첩된 JsonObject와 JsonArray를 포함하는 예시 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_example_2.png)

###설정 파일 읽기 및 쓰기

JSON 파일에서 설정을 불러와 수정한 후 저장하기:

<!-- 그림 필요: 완전한 구성 읽기 및 쓰기 과정 표시: 파일에서 Json 객체 로드 -> 필드 수정 -> 파일에 Json 객체 저장 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_example_3.png)

##유형 열거

`EAIChatPlus_JsonValueType` 열거형은 JSON 값의 타입을 정의합니다:

| 열거형 값 | 설명 |
|-------|------|
| `없음` | 알 수 없는 유형 |
| `Null` | 널 값 |
| `String` | 문자열 |
| `Number` | 숫자 |
| `Boolean` | 불리안 |
| `Boolean` | 불리언 |
| `Array` | 배열 |
| `Object` | 객체 |

<!-- 이미지 필요: JsonValueType에 따라 Switch 노드를 사용해 다양한 처리를 하는 블루프린트를 보여주는 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_type_1.png)

--8<-- "footer_ko.md"


> 이 게시물은 ChatGPT로 번역되었습니다. [**피드백**](https://github.com/disenone/wiki_blog/issues/new)누락된 부분을 지적합니다. 
