---
layout: post
title: CllamaServer (llama.cpp server)
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
- CllamaServer
description: CllamaServer (llama.cpp server)
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - CllamaServer (llama.cpp server)" />

#青写真編 - CllamaServer (llama.cpp サーバー)

<!-- 画像が必要：CllamaServerに関連するすべてのブループリントノードの概要を示す、他のドキュメントのxxx_all.pngのようなもの -->
![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_all.png)

##概要

CllamaServerはllama.cppのServerモード実装をベースとしており、ローカルにOpenAI API互換サーバーを起動でき、多様な機能をサポートします：

* **ローカル推論サービス**: 外部のAPIに依存せず、ローカルでAI推論サーバーを起動
* **OpenAI APIとの互換性**: OpenAI互換のAPIフォーマットを使用しているため、移行や統合が容易です
* **マルチセッション対応**: 複数の同時リクエストに対応
* **ツール呼び出し**: 関数呼び出し機能をサポート
* **音声テキスト変換**: Speech-to-Text機能をサポート
* **見える化管理**: エディターに内蔵されたサーバー管理インターフェース

Cllamaとの違い：
* **Cllama**: プロセス内で直接モデルをロードして推論を行い、一度に1つのリクエストしか処理できません
* **CllamaServer**: 独立したHTTPサーバーを起動し、複数の同時リクエストを処理できます。APIはOpenAI形式と互換性があります。

##準備作業

ローカルで実行するためには、事前にオフラインモデルファイルを準備する必要があります。例えば、HuggingFaceからダウンロードしてください：[Qwen1.5-1.8B-Chat-Q8_0.gguf](https://huggingface.co/second-state/Qwen1.5-1.8B-Chat-GGUF/resolve/main/Qwen1.5-1.8B-Chat-Q8_0.gguf)

モデルを特定のフォルダの下に配置します。例えば、ゲームプロジェクトのディレクトリ `Content/LLAMA` の下に置きます。

##CllamaServerの作成

###ブループリントを使用してサーバーを作成する

ブループリント内で右クリックし、ノードを作成 `Create Cllama Server In World`

<!-- 画像が必要です：「Create Cllama Server」を右クリックで検索し、ノードを作成する様子を青写真に表示したスクリーンショットを掲載してください -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_1.png)

###サーバーパラメータの設定

`Cllama Server Param`ノードを作成し、主要なパラメータを設定します。

* **モデル**: モデルファイルのパス（必須）
* **ポート**: サーバーポート（0は自動割り当てを意味します）
* **ホスト**: リスニングアドレス、デフォルトは`127.0.0.1`
* **NGpuLayers**: GPUレイヤー数（-1はGPUをすべて使用することを意味します）

<!-- 画像が必要：FAIChatPlus_CllamaServerParamノードの作成、Modelのパス設定、Port、NGpuLayersなどのパラメータ設定を示すスクリーンショットを表示 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_2.png)

###コールバックイベントのバインド

サーバーのコールバックイベントをバインドする：

* **On Started**: サーバー起動成功時にトリガー
* **停止時**: サーバー停止時にトリガー
* **On Failed**: サーバーの起動に失敗したときにトリガーされます

<!-- 画像が必要：OnStartedListeners、OnStoppedListeners、OnFailedListeners イベントをバインドするブループリントを表示 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_3.png)

###完全な作成の青写真

完全なServer作成の青写真は以下の通りです：

必要な画像：Server 作成の全体像を示すブループリントの完全なビューを表示してください。パラメータ設定、作成ノード、コールバックのバインドを含めます。
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_4.png)

ブループリントを実行した後、Server が正常に起動すると `On Started` イベントがトリガーされます。

<!-- 必要な画像：Server起動成功後の実行結果を表示する、起動成功のログまたは画面出力を表示する -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_create_5.png) -->

##サーバーパラメータの詳細解説

`FAIChatPlus_CllamaServerParam`構造体には以下のパラメータが含まれます：

###よく使われるパラメータ

| パラメータ | タイプ | デフォルト値 | 説明 |
|-----|------|-------|------|
| モデル | F文字列 | - | モデルファイルのパス（必須） |
| Port | int32 | 0 | リスニングポート、0は自動割り当てを意味します |
| ホスト | FString | 127.0.0.1 | リスニングアドレス |
| NGpuLayers | int32 | -1 | GPUレイヤー数、-1はすべてを意味します |
| bUseJinja | bool | false | Jinjaテンプレートを使用 |
| MMProj | FString | - | マルチモーダル投影ファイルのパス |
以下是将给定文本翻译成日语后的结果：

| 温度 | float | 0.8 | サンプリング温度 | 

注意：保持了表格格式和英文术语"float"，仅对中文部分进行了本地化处理。"采样温度"译为"サンプリング温度"（采样の温度/サンプリング時の温度的简略说法），符合技术文档常用表述。

###推論パラメータ

| パラメータ | タイプ | デフォルト値 | 説明 |
|-----|------|-------|------|
| CtxSize | int32 | 4096 | コンテキストサイズ |
| NPredict | int32 | -1 | 予測するトークン数、-1は無制限を意味 |
| スレッド数 | int32 | -1 | CPUのスレッド数。-1は自動を意味します |
| BatchSize | int32 | 2048 | バッチサイズ |

###サンプリングパラメータ

| パラメータ | タイプ | デフォルト値 | 説明 |
|-----|------|-------|------|
| TopK | int32 | 40 | Top-Kサンプリング |
| TopP | float | 0.9 | Top-Pサンプリング |
| MinP | float | 0.1 | Min-Pサンプリング |
| RepeatPenalty | float | 1.0 | 反復ペナルティ |

###サーバー設定

| パラメータ | タイプ | デフォルト値 | 説明 |
|-----|------|-------|------|
| ApiKey | FString | - | APIキー（オプション） |
| タイムアウト | int32 | 600 | タイムアウト時間（秒） |
| Parallel | int32 | 1 | 並列シーケンス数 |
| bNoWebUI | bool | false | Web UIを無効にする |
| bVerbose | bool | false | 詳細ログ |

##CllamaServerを使用してチャットする

###チャットリクエストを作成

サーバーの起動に成功した後、`Send CllamaServer Chat Request` ノードを使用してチャットリクエストを送信できます。

<!-- 必要な画像：ブループリント内で右クリックし「CllamaServer Chat Request」を検索してノードを作成する画面のスクリーンショット -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_1.png)

###チャットオプションの配置

`CllamaServer Chat Request Options` ノードを作成し、BaseUrl にサーバーのアドレスを設定します。

`Get Server Info By ID`ノードを使用してサーバーの情報を取得できます。

<!-- 画像が必要：FAIChatPlus_CllamaServerChatRequestOptionsノードの作成を展示し、Get Http Addressを使用してサーバーアドレスを取得し、BaseUrlに設定するブループリントを示す -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_2.png)

###メッセージを作成

Messages配列を作成し、System MessageとUser Messageを追加します。

<!-- 画像が必要：Messages配列の作成を示す（System Message（アシスタントの役割を設定）とUser Message（ユーザーの質問）を含むブループリントを表示） -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_3.png)

###コールバックをバインドして応答を処理

モデルからの応答を受信するには、`On Message` または `On Message Finished` イベントをバインドしてください。

<!-- 画像が必要：OnMessageListenersイベントをバインドし、コールバックでメッセージを画面に表示するブループリントを示す -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_4.png)

###完全なチャット設計図

チャットの完全な青写真は以下の通りです：

<!-- 画像が必要：サーバーの作成、起動待機、チャットリクエストの送信、レスポンス処理の完全なフローを含む、チャットの全体像を示すブループリントを表示してください -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_5.png)

###実行結果

青写真を実行すると、モデルが返すメッセージが画面に表示されます。

<!-- 画像が必要：チャットの実行結果を表示し、画面上にモデルが返した返答内容を表示する -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_chat_6.png) -->

##サーバー管理

###サーバー情報を取得する

`Get Server Info` ノードを使用してサーバーの詳細情報を取得します。

<!-- 必要な画像：Get Server Infoノードを使用してFAIChatPlus_CllamaServerInfoを取得するブループリントと、各フィールドをBreakで表示する図を提示する -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_info_1.png)

サーバー情報には以下の情報が含まれます：
* **ServerID**: サーバー一意ID
* **ホスト**: リスニングアドレス
* **ポート**: リッスンポート
* **アドレス**: 完全なアドレス（host:port）
* **HttpAddress**: HTTPアドレス（http://host:port）
* **bIsRunning**: 実行中かどうか
* **パラメータ**: サーバーパラメータ

###サーバー停止

`Stop Server By ID` ノードを使用して現在の Server を停止します。

<!-- 画像が必要：Stop Cllama Server ノードを呼び出すブループリントを表示する -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_stop_1.png)

###静的マネジメント関数

AIChatPlus はすべてのサーバーを管理するための一連の静的関数を提供しています。

| 関数 | 説明 |
|-----|------|
| `Is Server Valid (Static)` | Serverが有効かどうかを確認 |
| `サーバーは動作中ですか（静的）` | サーバーが実行中かどうかを確認します |
| `ID でサーバーを停止` | ID を指定してサーバーを停止 |
| `Stop All Servers` | すべてのサーバーを停止 |
| `ID でサーバー情報を取得` | ID によるサーバー情報の取得 |
| `全てのサーバーIDを取得` | すべてのサーバーIDを取得 |
| `Get Server By ID` | ID による Server インスタンスの取得 |

<!-- 必要画像：Get All Server IDsやStop All Serversなどの静的マネジメント関数を使用したブループリント例を表示 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_static_1.png)

##マルチモーダルサポート

CllamaServerはマルチモーダルモデル（Moondream、Qwen2-VLなど）をサポートしています。

###マルチモーダルパラメータの配置

Server パラメータで `MMProj`（マルチモーダル投影ファイルパス）を設定します：

<!-- 画像が必要です：Server ParamでModelとMMProjの2つのパスの設定を表示するブループリント -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_vision_1.png)

###画像メッセージを送信

Messagesに画像を追加：

<!-- 必要な画像：画像ファイルを読み込み、画像を含む Message を作成し、CllamaServer にリクエストを送信する手順を示す図 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_vision_2.png)

### 実行結果

<!-- 画像が必要：画像認識の実行結果を表示する画面で、モデルが画像の内容を説明している様子を表示 -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_vision_3.png) -->

## Tool Calling

CllamaServerはTool Calling（関数呼び出し）機能をサポートしており、使用法はOpenAIと同様です。

詳細な使用方法については [Tool Call](ue-插件-AIChatPlus-Usage-Blueprint-ToolCall.md)ドキュメント。

CllamaServerを使用してTool Callを行う場合、以下のことが必要です：
1. Server パラメータで `bUseJinja = true` を設定する
2. Chat OptionsのToolsフィールドでツールを定義する

<!-- 画像が必要です：CllamaServer Tool Callの完全なブループリントを表示し、bUseJinja=trueの設定とTools定義を含めてください -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_tool_1.png)

##エディター Server 管理

AIChatPlusはエディタツール内で視覚的なCllamaServer管理インターフェースを提供しており、複数のServerを簡単に作成、監視、管理できます。

エディターツールを開きます：`Tools -> AIChatPlus -> AIChat` を選択し、Cllama Server Manager タブを開きます。

<!-- 必要な画像：エディタ内のCllamaServer管理インターフェースのスクリーンショットで、Serverリスト、作成ボタン、ステータス情報などを表示したもの -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_editor_1.png)

エディターでは以下のことが可能です：
新しいサーバーを作成
* 実行中のServerの状態を確認
* 指定されたサーバーを停止する
* サーバーの構成パラメータ
* Serverの配置は自動的に保存されます

<!-- 必要画像：エディター内で新しいServerを作成する画面のスクリーンショット、パラメーター設定パネルを表示 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_editor_2.png)

##他のAPIとの関係

CllamaServer は OpenAI API 形式と互換性があるため、OpenAI の Chat Request ノードを使用して CllamaServer と通信することもできます。`BaseUrl` を CllamaServer のアドレスに設定するだけでOKです。

<!-- 画像が必要：OpenAI Chat Requestノードを使用していますが、BaseUrlがCllamaServerのアドレスに設定されているブループリントの例を示す -->
<!-- ![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/cllamaserver_openai_1.png) -->

--8<-- "footer_ja.md"


> この投稿はChatGPTによって翻訳されています。ご意見やご感想は[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指出すべき欠落点を指摘してください。 
