---
layout: post
title: 包みます
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
description: 包装
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - Package 篇 - Get Started" />

#包装

##プラグインをパッケージ化

Unrealのパッケージング時には、プラグインに必要なダイナミックライブラリファイルが自動的にパッケージされるため、プラグインを有効にするだけで済みます。

Windowsでは、例えば、llama.cppやCUDA関連のdllファイルが、自動的にパッケージングされたディレクトリに配置されます。Android / Mac / IOSなど、他のプラットフォームでも同様です。

Development版のゲームがパッケージ化された後、「AIChatPlus.PrintCllamaInfo」というコマンドを実行して、現在のCllama環境の状態を確認し、状態が正常かどうか、GPUバックエンドをサポートしているかを確認してください。

##モデルを梱包

プロジェクトに参加しているモデルファイルは、Content/LLAMAディレクトリに配置されています。したがって、このディレクトリをパッケージ化する設定が可能です：

「Project Setting」を開いて、Packagingタブを選択するか、「asset package」を検索して、「Additional Non-Asset Directories to Package」という設定を見つけて、ディレクトリ「Content/LLAMA」を追加すればOKです。

![](assets/img/2024-ue-aichatplus/usage/blueprint/openai_image_edit_6.png)

目次を追加すると、Unreal はパッケージング時に自動的にそのディレクトリ内のすべてのファイルをパッケージ化します。


##パッケージ化されたオフラインモデルファイルを読み込む

一般の場合、Unealはプロジェクトファイルを.Pakファイルにパッケージングします。この時、.Pak内のファイルパスをCllamオフラインモデルに渡すと、実行に失敗します。なぜなら、llama.cppは直接.Pak内のパッケージ化されたモデルファイルを読むことができないからです。

したがって、最初に .Pak ファイル内のモデルファイルをファイルシステムにコピーする必要があります。プラグインには、.Pak のモデルファイルを直接コピーし、コピー後のファイルパスを返す便利な関数が提供されています。これにより、Cllama が簡単に読み取れるようになります。

ブループリントノードは "Cllama Prepare ModelFile In Pak" です："Pak"内のモデルファイルを自動的にファイルシステムにコピーします。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

C++のコード関数は：

```
#include <Cllama/AIChatPlusCllama_Util.h>

auto ModelPath = FAIChatPlusCllama_Util::PrepareModelFileInPak(InContentPath);
```

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されました。[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。 
