---
layout: post
title: Tool Call
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
- Tool Call
- Function Calling
description: Tool Call
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Tool Call" />

#青写真篇 - ツールコール

Tool Call（ツールコール）はFunction Calling（関数コール）とも呼ばれ、大規模言語モデルが会話内容に基づいて外部ツールや関数の呼び出しが必要かどうかを判断し、情報取得や操作実行を行う仕組みです。モデルは呼び出すべき関数名とパラメータを返し、開発者が実際に関数を呼び出した後、その結果をモデルに返して会話を続行します。

AIChatPlus は以下のプラットフォームの Tool Call 機能をサポートしています：

* OpenAI
* Claude
* Gemini
* Ollama
* CllamaServer（llama.cpp サーバー）

##中核概念

###ツール定義

ツールの定義には以下の主要なフィールドが含まれます：

* **タイプ**: ツールの種類。現時点では `Function` のみをサポートしています。
* **名前**: 関数名。a-z、A-Z、0-9、アンダースコアまたはハイフンで構成され、最大長は64文字です。
* **説明**: 関数の説明で、モデルはこの説明に基づいて関数をいつ呼び出すかを判断します
* **プロパティ**: 関数のパラメータリストで、各パラメータにはName、Description、Type、Requiredなどの属性が含まれます

###ツールコールのプロセス

Tool Callの完全なフローは以下の通りです：

1. **リクエストを送信する**: ツール定義を含むチャットリクエストをモデルに送信する
2. **モデル判断**: モデルは対話内容に基づいてツールを呼び出す必要があるかどうかを判断します
3. **Tool Callsの返却**: 呼び出しが必要な場合、モデルは呼び出す関数名と引数を返します。
4. **関数の実行**: 開発者は返された情報に基づいて実際の関数呼び出しを実行します
5. **結果を返す**: 関数の実行結果を新しいメッセージとしてモデルに送信する
6. **会話を続ける**: モデルが関数の結果に基づいて最終的な返答を生成する

##OpenAIツールコールの例

以下にOpenAIを例として、Tool Call機能の使用方法をデモンストレーションします。

###1. Tool を定義する

最初にツール定義を作成します。この例では、宅配便の配達日を取得する関数 `get_delivery_date` を定義します。

<!-- 画像が必要：FAIChatPlus_ChatRequestToolノードを作成し、Type=Function、Name="get_current_weather"、Description="指定された場所の現在の天気を取得する"と設定する画面を表示 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_1.png)

###2. Toolパラメータの定義

ToolにProperties（プロパティ）を追加します。この例では、`order_id`というパラメータを追加し、タイプを`string`に設定し、必須項目とします。

<!-- 画像が必要：FAIChatPlus_ChatRequestToolPropertyノードの作成を表示し、Name="location"、Description="都市と州、例：サンフランシスコ、CA"、Type="string"、Required=trueに設定し、Make Arrayを介してToolのPropertiesフィールドに接続する -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_2.png)

###3. 配置オプション

`OpenAI Chat Request Options`ノードを作成し、APIキーとモデルを設定して、ツール配列をオプションに接続します。

<!-- 必要な画像：OpenAI Chat Request Options ノードの作成を表示し、ApiKeyを設定、Model="gpt-4o-mini"とし、Make Arrayを使用して上記のToolをToolsフィールドに接続する -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_3.png)

###4. メッセージを作成

ユーザーメッセージを作成し、宅配便の小包に関する質問をする。

<!-- 画像が必要：メッセージ配列の作成と、ユーザーメッセージ「What's the weather like in Boston today?」を追加し、Contentを設定している様子を表示する -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_4.png)

###5. リクエストを送信し、Tool Callを処理する

`Send OpenAI Chat Request In World` ノードを作成し、`On Message Finished` イベントをバインドします。イベントコールバック内で、PayloadからToolCalls配列を取得します。

モデルがツールの呼び出しを決定した場合、ToolCalls配列は空ではありません。配列を順に処理して各Tool Callの情報を取得します：

* **ID**: Tool Callの一意な識別子
* **FunctionName**: 呼び出す関数名
* **FunctionArguments**: 関数の引数（JSON文字列形式）

<!-- 画像が必要：完全なリクエスト送信のブループリントを表示し、Send OpenAI Chat Request In Worldノードを作成し、OptionsとMessagesを接続し、On Message Finishedイベントをバインドし、イベントコールバック内でBreakノードを使用してPayloadからToolCallsを取得 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_5.png)

<!-- 画像が必要：ToolCalls配列を走査するブループリントを表示し、For Each Loopを使用して各要素を反復処理し、Breakノードを使用してId、FunctionName、FunctionArgumentsフィールドを取得し、それらをプリントアウトします -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_6.png) -->

###6. 関数を実行して結果を返す

FunctionName に基づいて対応する関数ロジックを実行し（この例では宅配便の到着時間をシミュレート）、その結果を ToolCallResult 型のメッセージとしてモデルに返します。

新しいメッセージを作成するには、以下を設定する必要があります：

* **役割**: `ツール` に設定
* **内容**: 関数実行の結果
* **ToolCallResults**: `FAIChatPlus_ChatRequestToolCallResult` を追加し、Id（前回のTool Call Idを使用）、FunctionName、およびFunctionResultを設定します

<!-- 画像が必要です：Toolロールのメッセージ作成のブループリントを示し、新しいMessageを作成、Role=Tool、Contentをシミュレートされた天気データ（例：'{"temperature": "22", "unit": "celsius", "description": "Sunny"}'）に設定し、ToolCallResultsに対応する結果情報を追加した様子を示す画像 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_7.png)

###7. 会話を続ける

ツールコールの結果を含むメッセージを履歴メッセージに追加し、再度リクエストを送信します。モデルは関数が返した結果に基づいて、最終的な自然言語での返答を生成します。

<!-- 画像が必要：2回目のリクエストの完全なブループリントを表示し、元のユーザーメッセージ、モデルが返したアシスタントメッセージ（ToolCallsを含む）、およびツールの結果メッセージを新しいメッセージ配列に組み合わせ、再度「Send OpenAI Chat Request In World」を呼び出す -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_8.png)

### 9. 完全な青写真

<!-- 完全なTool Callの設計図はこのような見た目になります： -->

<!-- 画像が必要：Tool定義、最初のリクエスト、Tool Call処理、2回目のリクエストを含む、完全なTool Callプロセスの全体図を表示する -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_9.png) -->

### 10. 実行結果

<!-- ブループリントを実行すると、モデルが天気情報を含む自然言語の返答を返すのが確認できます。-->

<!-- 画像が必要です：実行結果のスクリーンショットを示し、画面上にはモデルの最終的な返答が表示され、「ボストンの現在の天気は晴れで、気温は22℃です。」のような内容が含まれているものとします。 -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_openai_10.png) -->

##上級者向けの使い方

###複数のツール

複数のツールを同時に定義することができ、モデルは必要に応じてどの関数を呼び出すか選択します。

<!-- 画像が必要：複数のToolsを定義するブループリントを示す。例えば、get_current_weatherとget_stock_priceの2つのToolを同時に定義し、Make Arrayを使用してToolsの配列に組み合わせる例 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_multi_tools.png)

###複雑なパラメータ型

ツールのパラメータは複数の型をサポートしており、`ExtraJsonString` や `ExtraJsonObject` フィールドを通じてより複雑なパラメータ定義（例えば列挙型など）を追加できます：

```json
{"enum": ["Beijing", "HongKong"]}
```

<!-- 画像が必要：ExtraJsonStringを使用して列挙型パラメータを設定したブループリントを示す、PropertyノードのExtraJsonStringフィールドに '{"enum": ["celsius", "fahrenheit"]}' と記入されている様子 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/toolcall_extra_json.png)

###他のプラットフォーム

Claude、Gemini、Ollama、そしてCllamaServerにおけるTool Callの使用方法はOpenAIと似ており、対応するRequestとOptionsノードを置き換えるだけで済みます。各プラットフォームのコアデータ構造（`FAIChatPlus_ChatRequestTool`、`FAIChatPlus_ChatResponseToolCall`など）は共通です。

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されたものです。ご意見・ご感想は[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指出した抜け漏れを記す。 
