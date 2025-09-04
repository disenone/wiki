---
layout: post
title: 包む
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
description: パッケージング
---

<meta property="og:title" content="UE 插件 AIChatPlus 使用说明 - Package 篇 - Get Started" />

#梱包

##プラグインのパッケージング

Unreal Engine は、パッケージング時に、プラグインに必要なダイナミック ライブラリ ファイルを自動的にパッケージングしてくれるため、プラグインを有効にするだけで使用できます。

Windowsに関しては、パッケージング時にはlama.cppやCUDA関連のdllファイルが自動的にパッケージングされたディレクトリに配置されます。Android/Mac/iOSなど他のプラットフォームでも同様です。

開発版ゲームのパッケージング後に "AIChatPlus.PrintCllamaInfo" コマンドを実行して、現在の Cllama 環境の状態を確認し、ステータスが正常かどうか、GPU バックエンドがサポートされているかどうかを確認してください。

##モデルパッケージング

仮にプロジェクトに組み込むモデルファイルがディレクトリ Content/LLAMA に置かれているとしたら、パッケージングする際にこのディレクトリを含めるように設定できます：

"Project Setting"を開き、Packagingタブを選択するか、「asset package」と検索してください。「Additional Non-Asset Directories to Package」の設定を見つけ、ディレクトリ Content/LLAMA を追加してください。

![](assets/img/2024-ue-aichatplus/usage/package/getstarted_1.png)

目次を追加すると、Unreal はパッケージングの際に自動的に目次内のすべてのファイルをパッケージングします。

##パッケージ化されたオフラインモデルファイルを読み込む

一般Uneal会将项目文件打包至.Pak文件中，若将.Pak内的文件路径传递给Cllam离线模型，会导致执行失败，因为llama.cpp无法直接读取.Pak文件中打包后的模型文件。

したがって、まずは .Pak ファイル内のモデルファイルをファイルシステムにコピーする必要があります。プラグインには、.Pak のモデルファイルを直接コピーしてコピー後のファイルパスを返す便利な関数が用意されており、Cllama が簡単に読み取れるようにしています。

ブループリントノード "Cllama Prepare ModelFile In Pak" は、Pak内のモデルファイルを自動的にファイルシステムにコピーします。

![guide bludprint](assets/img/2024-ue-aichatplus/guide_util_4.png)

C ++ コードの関数は：

```
#include <Cllama/AIChatPlusCllama_Util.h>

auto ModelPath = FAIChatPlusCllama_Util::PrepareModelFileInPak(InContentPath);
```

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されましたので、[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。 - どこか見落としのある点を指摘してください。 
