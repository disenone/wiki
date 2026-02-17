---
layout: post
title: JSON操作
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
description: Json 操作
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - 蓝图篇 - Json 操作" />

#青写真編 - Json操作

<!-- 画像が必要：Jsonに関連するすべてのブループリントノードの概要を示す。JsonObject、JsonArray、JsonLibraryのカテゴリに分類されたノードを含む -->
![blueprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_all.png)

##概要

AIChatPlusは完全なJSONブループリント操作サポートを提供し、ブループリントでのJSONデータ処理を容易にします。主に三つのクラスを含んでいます：

* **UAIChatPlus_JsonObject**: JSON オブジェクト操作クラス。`{}` 形式の JSON を処理するために使用されます。
* **UAIChatPlus_JsonArray**: JSON 配列操作クラス。`[]` 形式のJSONを処理するために使用されます。
* **UAIChatPlus_JsonLibrary**: JSONユーティリティ関数ライブラリ、静的なツール関数を提供します

これらのクラスは、以下の機能をサポートしています：
* JSONの作成、解析、シリアル化
* フィールド値の読み取りと設定
* ネストされたパスクエリ
* JSON と USTRUCT の相互変換
* ファイルの読み書き
* メソッドチェーン

##JsonObject 基本操作

###JsonObjectを作成する

空の JSON オブジェクトを作成するには `Create Json Object` を使用します：

<!-- 必要な画像：「Create Json Object」を右クリックで検索し、ノードを作成する手順を示すスクリーンショットをブループリント内に表示する -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_create_1.png)

###文字列から解析

JSON文字列からオブジェクトを作成するには、 `Parse Json Object`を使用してください。

<!-- 画像が必要：Parse Json Object ノードを示し、入力としてJSON文字列（例：'{"name":"test","value":123}'）を、出力としてJsonObject、bSuccess、ErrorMessageを表示させる -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_parse_1.png)

###フィールド値の設定

JsonObjectはさまざまなSetメソッドを提供し、メソッドチェーンをサポートしています：

| 関数 | 説明 |
|-----|------|
| `Set String Field` | 文字列フィールドを設定 |
`Set Number Field` | 数値フィールドの設定
| `Set Integer Field` | 整数フィールドを設定 |
| `Set Boolean Field` | ブールフィールドを設定 |
| `Set Object Field` | ネストされたオブジェクトフィールドを設定 |
| `Set Array Field` | 配列フィールドを設定 |
| `Set Null Field` | NULLフィールドを設定 |

<!-- 必要な画像：複数のフィールドをチェーン設定するブループリントを表示。例：Create Json Object -> Set String Field("name", "player1") -> Set Integer Field("level", 10) -> Set Boolean Field("active", true) -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_set_1.png)

###フィールド値の取得

JsonObject では、さまざまな Get メソッドが提供されています：

| 関数 | 説明 |
|-----|------|
| `Get String Field` | 文字列フィールドを取得する |
| `Get Number Field` | 浮動小数点数フィールドを取得 |
| `Get Integer Field` | 整数フィールドを取得する |
| `Get Boolean Field` | ブール型フィールドを取得 |
| `Get Object Field` | 入れ子オブジェクトのフィールドを取得 |
| `Get Array Field` | 配列フィールドの取得 |

<!-- 画像が必要：JsonObjectからフィールド値を取得するブループリントを示すイメージ。"name"フィールドを取得するためにGet String Fieldを使用し、DefaultValueとbSuccessパラメータを表示する -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_get_1.png)

###フィールドチェック

| 関数 | 説明 |
|-----|------|
| `Has Field` | フィールドが存在するかどうかをチェック |
| `フィールドタイプを取得` | フィールドタイプを取得 |
| `Get Field Names` | すべてのフィールド名を取得 |
| `Remove Field` | フィールドを削除 |
| `クリア` | 全てのフィールドを消去 |

<!-- 画像が必要：Has Fieldでフィールドの存在を確認し、Get Field Typeでフィールドのタイプを取得するブループリントを表示 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_check_1.png)

###文字列にシリアライズする

`JsonObject` を文字列に変換するには `To Json String` を使用します：

<!-- 必要画像：To Json String ノードを表示し、入力として JsonObject を受け取り、bPrettyPrint パラメータを設定した結果、整形された JSON 文字列が出力される様子を提示 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_tostring_1.png)

##JsonArray 基本操作

###JsonArrayの作成

`Create Json Array`を使用して空のJSON配列を作成します：

<!-- 画像が必要：青写真内でCreate Json Arrayノードを作成する画面のスクリーンショットを表示 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_create_1.png)

###要素を追加

JsonArrayでは、複数のAddメソッドを提供しており、メソッドチェーンのサポートが可能です：

| 関数 | 説明 |
|-----|------|
| `Add String` | 文字列要素を追加 |
| `Add Number` | 浮動小数点数要素を追加 |
| `Add Integer` | 整数要素を追加 |
| `Add Boolean` | ブール要素を追加 |
| `Add Object` | オブジェクトを追加 |
| `Add Array` | 配列要素を追加 |
| `Add Null` | null要素を追加 |

<!-- 画像が必要：チェーンメソッドで複数の要素を追加するブループリントを表示。例：Create Json Array -> Add String("a") -> Add String("b") -> Add Integer(123) -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_add_1.png)

###要素の取得

JsonArray はインデックスによる要素の取得方法を提供します：

| 関数 | 説明 |
|-----|------|
| `Get String` | 文字列要素を取得する |
| `Get Number` | 浮動小数点要素を取得 |
| `Get Integer` | 整数要素を取得 |
| `ブール値を取得` | ブール要素を取得 |
| `Get Object` | オブジェクト要素を取得 |
| `Get Array` | 配列要素を取得する |

<!-- 必要な画像：Get Object を使用してインデックスで配列内のオブジェクト要素を取得するブループリントを示す -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_get_1.png)

###配列操作

| 関数 | 説明 |
|-----|------|
| `Length` | 配列の長さを取得 |
| `Is Valid Index` | インデックスが有効かどうかを確認 |
| `Get Element Type` | 要素タイプを取得 |
| `Remove At` | 指定したインデックスの要素を削除 |
| `Clear` | 配列をクリア |

<!-- 必要な画像：Lengthを使用して配列の長さを取得し、For Loopと組み合わせて配列を走査するブループリントを示す -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_loop_1.png)

###一括変換

JsonArrayはUEの配列とのバッチ変換をサポートしています：

| 関数 | 説明 |
|-----|------|
| `From String Array` | 文字列配列から作成 |
| `To String Array` | 文字列配列に変換 |
| `From Integer Array` | 整数配列から作成 |
| `To Integer Array` | 整数配列に変換 |

<!-- 画像が必要：文字列配列から変換および文字列配列へ変換の使用例を示す -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_array_batch_1.png)

##経路検索

JsonObjectは、`player.inventory.gold`のようにドットで区切られたパスを使ってネストされたデータにアクセスすることをサポートしています。

###パスに従って値を取得

`Get String By Path`を使用して、パスで文字列値を取得します：

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

<!-- 必要な画像：Get String By Pathノードを使用し、Pathを「player.name」に設定して、ネストされた値を取得するブループリントを表示 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_path_get_1.png)

###パスに従って値を設定

パスごとに値を設定するために `Set String By Path` を使用：

<!-- 画像が必要：Set String By Path ノードを使用してネストされたパス値を設定するブループリントを表示し、FAIChatPlus_JsonPathOptions パラメーター（bCaseSensitive、bCreateMissing）を表示する -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_path_set_1.png)

###検索結果

パス検索は `FAIChatPlus_JsonQueryResult` 構造体を返し、以下の内容を含みます：

**bSuccess**: クエリが成功したかどうか
* **ValueType**: 戻り値の型
* **ErrorMessage**: エラーメッセージ（失敗時）

<!-- 必要な画像：Break FAIChatPlus_JsonQueryResult ノードを表示し、bSuccess、ValueType、ErrorMessage フィールドを示す -->

注：上記の翻訳では、HTMLコメントとコード内のノード名は原文のまま保持していますが、実際にはそれらも必要に応じて翻訳される場合があります。ただし、この場合は技術的なコンテキストが強く、特にノード名やフィールド名はそのまま使われることが多いため、翻訳せずに残しました。より自然な日本語表現にする場合は、以下のように調整することも可能です：

<!-- 必要な画像：FAIChatPlus_JsonQueryResultを解析するBreakノードで、bSuccess、ValueType、ErrorMessage各フィールドが表示されている様子 -->

どちらの翻訳が適切かは、実際の使用文脈（技術ドキュメントなのかUI表示なのか）によって異なります。
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_path_result_1.png)

##JSON と USTRUCT の変換

AIChatPlusはJSONとUSTRUCT間の変換をサポートしており、ブループリント構造体との連携に便利です。

###JSON文字列からUSTRUCTへ変換

`Json String To Struct`を使ってJSON文字列を直接USTRUCTに変換する：

<!-- 必要な画像：Json String To Struct ノードを示し、JSON文字列を入力として受け取り、出力パラメータをカスタムUSTRUCT変数（例：FAIChatPlus_OpenAIChatRequestOptions）に接続している様子 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_struct_1.png)

###USTRUCT から JSON 文字列へ変換

USTRUCTをJSON文字列に変換するには`Struct To Json String`を使用します：

<!-- 画像が必要：Struct To Json Stringノードを表示し、USTRUCT変数を入力し、bPrettyPrintパラメータを設定し、JSON文字列を出力 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_struct_2.png)

###JsonObject を USTRUCT に変換

JsonObject の `To Struct` メソッドを使用：

<!-- 必要画像：JsonObject の To Struct ノードの使用方法を示す -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_struct_3.png)

###USTRUCT から JsonObject へ変換

`From Struct` 静的メソッドを使用して USTRUCT から JsonObject を作成します：

<!-- 画像が必要：From Structノードを示し、入力がUSTRUCT、出力がJsonObjectであることを示す -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_struct_4.png)

##JsonLibrary ユーティリティ関数

`UAIChatPlus_JsonLibrary`は、一連の静的ユーティリティ関数を提供しています。

###迅速に作成

| 関数 | 説明 |
|-----|------|
| `Make Json Object With String Field` | 単一フィールドを持つJsonObjectを迅速に作成します |
| `文字列マップからJsonオブジェクトを作成` | MapからJsonObjectを作成 |

<!-- 必要な画像：Make Json Object From String Map の使用を示す、入力は TMap<FString, FString>、出力は JsonObject のブループリント -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_make_1.png)

###検証する

| 関数 | 説明 |
|-----|------|
| `Validate Json String` | JSON 文字列が有効かどうかを検証する |
| `Is Json Object` | JSON オブジェクトかどうかをチェックします |
| `Is Json Array` | JSON配列かどうかを確認します |

<!-- 必要画像：Validate Json String を使用して JSON 文字列を検証するブループリントを示す -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_validate_1.png)

###フォーマット

| 関数 | 説明 |
|-----|------|
以下是将给定文本翻译成日语的结果：

| `Prettify Json` | JSONを整形（インデントと改行を追加） |
| `Minify Json` | JSONを圧縮（空白を除去） |

必要画像：Prettify Jsonを使用してJSON文字列をフォーマットする様子を示し、入力された圧縮JSONと出力されたフォーマット済みJSONを表示する
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_format_1.png)

###ファイル操作

| 関数 | 説明 |
|-----|------|
| `Load Json Object From File` | ファイルからJsonObjectをロード |
`Save Json Object To File` | JsonObjectをファイルに保存
| `Load Json Array From File` | ファイルから JsonArray を読み込む |
| `JSON配列をファイルに保存` | JSON配列をファイルに保存 |

<!-- 必要な画像：Save Json Object To File と Load Json Object From File の使用例を示す -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_file_1.png)

###比較

| 関数 | 説明 |
|-----|------|
| `Equals Json Object` | 2つのJsonObjectが等しいかどうかを比較します |
| `Equals Json Array` | 2つのJsonArrayが等しいかどうかを比較します |

<!-- 画像が必要：Equals Json Objectを使用して2つのJsonObjectを比較するブループリントを示す -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_compare_1.png)

###高度なパス検索

| 関数 | 説明 |
|-----|------|
| `Query String By Path` | パスによる文字列のクエリ（配列インデックスをサポート、例: `items[0].name`） |
| `Query Object By Path` | パスによるオブジェクトのクエリ |
| `Query Array By Path` | パスで配列を検索 |

<!-- 必要な画像：Query String By Path を使用して配列インデックス付きのパス（例： "data.items[0].name"）を検索する様子を示す -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_query_1.png)

###一括操作

| 関数 | 説明 |
|-----|------|
| `Set String Fields From Map` | 文字列フィールドを一括設定 |
| `Get String Fields To Map` | 文字列フィールドを一括取得 |

<!-- 画像が必要です：Set String Fields From Mapを使用したブループリントでフィールドを一括設定する様子を表示 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_lib_batch_1.png)

##その他の操作

###JsonObject をマージ

2つの JsonObject を `Merge` メソッドで結合します：

<!-- 画像が必要：Mergeノードを表示し、2つのJsonObjectを統合し、bOverwriteパラメータを表示する -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_merge_1.png)

###JsonObjectのコピー

`Duplicate`メソッドを使用してJsonObjectをディープコピー：

<!-- 必要な画像：DuplicateノードがJsonObjectを複製するブループリントを表示 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_dup_1.png)

##実用例

###APIレスポンスの解析

AI チャット応答から Tool Call のパラメータを抽出する

<!-- 必要画像：完全な解析例のブループリントを示す：FunctionArguments 文字列を JsonObject に Parse してから、Get String Field を使用してパラメータ値を取得する -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_example_1.png)

###リクエストパラメータの構築

複雑なリクエストパラメータを構築するには、JsonObjectを使用します。

<!-- 画像が必要：ネストされたJSON構造の設計図を表示し、複数のフィールドを設定したJsonObjectの作成、ネストされたJsonObjectとJsonArrayを含む -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_example_2.png)

###設定ファイルの読み書き

JSONファイルから設定を読み込み、変更後に保存：

<!-- 画像が必要：完全な設定読み書きフローを表示する：ファイルからJsonオブジェクトをロード -> フィールドを変更 -> Jsonオブジェクトをファイルに保存 -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_example_3.png)

##タイプ列挙

`EAIChatPlus_JsonValueType` 列挙型はJSON値の型を定義します：

| 列挙値 | 説明 |
|-------|------|
| `None` | 不明なタイプ |
| `Null` | null 値 |
| `String` | 文字列 |
| `Number` | 数字 |
| `Boolean` | ブーリアン |
| `Array` | 配列 |
| `Object` | オブジェクト |

<!-- 必要な画像：JsonValueType に応じて異なる処理を行う Switch ノードの使用を示すブループリント -->
![guide bludprint](assets/img/2024-ue-aichatplus/usage/blueprint/json_type_1.png)

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されました。ご意見・ご要望は[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)以下の箇所で見落としがあるかどうか指摘してください。 
