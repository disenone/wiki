---
layout: post
title: UE 設置本地化多語言
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
description: 記錄如何在 UE 中實現本地化多語言
---

<meta property="og:title" content="UE 设置本地化多语言" />

#UE 設置本地化多語言

> 記錄在UE中實現本地化多語言的方法

如果您對UE擴展菜單不熟悉，建議先簡單看一下：[UE擴展編輯器菜單](ue-扩展编辑器菜单.md)，[使用路徑形式擴展選單](ue-使用路径形式扩展菜单.md)

這段文字是基於插件：[UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##功能介紹

UE 內建工具可實現本地化多語言功能，例如我們可以為編輯器選單進行本地化：

中文菜單：

![](assets/img/2023-ue-localization/chinese.png)

英文菜單：

![](assets/img/2023-ue-localization/english.png)

##程式碼宣告

為了實現菜單本地化，我們需要在程式碼中明確聲明需要 UE 處理的字串，使用 UE 定義好的巨集 `LOCTEXT` 和 `NSLOCTEXT`：

- 在文件的整體定義中，首先開始定義一個名為 `LOCTEXT_NAMESPACE` 的巨集，其內容是當前多語言文本所在的命名空間，隨後文件中的文本就可以使用 `LOCTEXT` 來定義，檔案最後取消巨集 `LOCTEXT_NAMESPACE`：

```cpp
// #define LOCTEXT(InKey, InTextLiteral)

#define LOCTEXT_NAMESPACE "EditorPlusTools"
LOCTEXT("Key", "Content");
#undef LOCTEXT_NAMESPACE

```

- 使用 `NSLOCTEXT` 的局部定義方式，在定義文本時加上命名空間參數：

```cpp
// #define NSLOCTEXT(InNamespace, InKey, InTextLiteral)

NSLOCTEXT("EditorPlusTools", "Key", "Content");
```

UE 工具透過搜尋 `LOCTEXT` 和 `NSLOCTEXT` 這些宏的出現來收集所有需要翻譯的文字。

##使用工具翻譯文本

假設我們有如下程式碼定義文字：

```cpp
#define LOCTEXT_NAMESPACE "EditorPlusTools"
// register path node loctext
FEditorPlusPath::GetNodeByPath("/MenuTest")->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
FEditorPlusPath::GetNodeByPath("/MenuTest/<SubMenu>SubMenu1")->SetFriendlyName(LOCTEXT("SubMenu1", "SubMenu1"))->SetFriendlyTips(LOCTEXT("SubMenu1Tips", "SubMenu1Tips"));
FEditorPlusPath::GetNodeByPath("/MenuTest/<SubMenu>SubMenu1/<SubMenu>SubMenu1")->SetFriendlyName(LOCTEXT("SubMenu1", "SubMenu1"))->SetFriendlyTips(LOCTEXT("SubMenu1Tips", "SubMenu1Tips"));
FEditorPlusPath::GetNodeByPath("/<Hook>Help/<MenuBar>MenuTest/<SubMenu>SubMenu1/<Section>Section1")->SetFriendlyName(LOCTEXT("Section1", "Section1"))->SetFriendlyTips(LOCTEXT("Section1Tips", "Section1Tips"));
#undef LOCTEXT_NAMESPACE
```

請將文字翻譯為繁體中文：

首先開啟翻譯工具，進入編輯器的設定`編輯 - 編輯器偏好設置`，勾選`通用 - 實驗性功能 - 工具 - 翻譯選取器`：

![](assets/img/2023-ue-localization/editor_enable_tool.png)


然後開啟翻譯工具 `工具 - 本地化控制板`：

![](assets/img/2023-ue-localization/editor_open_tool.png)

建立一個新目標（在預設的遊戲中也可以，建立一個是為了方便管理和移動這些翻譯文本）

![](assets/img/2023-ue-localization/tool_new_target.png)

設置目標參數，將名稱更改為 `EditorPlusTools`，載入策略為 `編輯器`，從文本中收集，並添加插件目錄，目標依賴性為 `Engine, Editor`，其他配置保持不變：

![](assets/img/2023-ue-localization/tool_target_config.png)

添加语言设置，确保系统同时包含简体中文和英文两种语言选项，在鼠标悬停于语言名称上时，分别显示“zh-Hans”和“en”。同时请选择英文（因为我们的代码中使用英文定义文本，需要收集这些英文文本）。

![](assets/img/2023-ue-localization/tool_target_lang.png)

點擊收集文本：

![](assets/img/2023-ue-localization/tool_target_collect.png)

彈出收集進度方塊，等待收集成功，將顯示綠色勾勾：

![](assets/img/2023-ue-localization/tool_target_collected.png)

關閉收集進度視窗，返回翻譯工具，您可以看到英文一行顯示已收集的數量，我們不需要翻譯英文內容，請點擊中文一行的翻譯按鈕：

![](assets/img/2023-ue-localization/tool_go_trans.png)

打開後我們可以看到未翻譯一欄有內容，在英文文本的右邊一欄輸入翻譯後的內容，翻譯內容都完成之後，保存退出視窗：

![](assets/img/2023-ue-localization/tool_trans.png)

點擊統計字數，結束後能看到中文一欄顯示了翻譯的數量：

![](assets/img/2023-ue-localization/tool_count.png)

最後編譯文字：

![](assets/img/2023-ue-localization/tool_build.png)

翻译的數據會放在 `Content\Localization\EditorPlusTools` 裡面，每種語言一個文件夾，在 zh-Hans 裡面能看到兩個文件，`.archive` 是收集和翻譯的文本，`.locres` 則是編譯之後的數據：

![](assets/img/2023-ue-localization/tool_ret.png)

![](assets/img/2023-ue-localization/tool_ret2.png)

##將已翻譯好的文本放入外掛程式目錄中。

我們將插件生成的翻譯文本放在項目目錄下，我們需要將這些文本移動到插件內，以便與插件一同發布。

將 `Content\Localization\EditorPlusTools` 目錄移動至插件目錄 Content 底下，這裡是 `Plugins\UE.EditorPlus\Content\Localization\EditorPlusTools`。

修改專案的設定檔 `DefaultEditor.ini`，加上新路徑：

```ini
[Internationalization]
+LocalizationPaths=%GAMEDIR%Plugins/UE.EditorPlus/Content/Localization/EditorPlusTools
```

這樣一來，其他專案得到插件後，只需修改 `DefaultEditor.ini` 就能直接使用翻譯文本，而無需重新配置翻譯。

##請注意。

在製作翻譯資料的過程中，遇到了一些問題，以下總結出來需要注意的事項：

- 在程式碼中，定義文本必須使用宏 `LOCTEXT` 和 `NSLOCTEXT`，並確保文本是字串常數，這樣 UE 才能正確收集。
- 翻譯目標名稱不能包含 `.` 符號，`Content\Localiztion\` 目錄中的名稱不能包含 `.`，UE 只會截取 `.` 前面的名稱。會導致 UE 在讀取翻譯文本時，因為名稱錯誤而讀取失敗。
對於編輯器外掛程式，需要判斷如果是命令行模式 `IsRunningCommandlet()` 則不生成選單和 SlateUI，因為命令行模式下沒有 Slate 模塊，會導致收集文本的時候報錯 `Assertion failed: CurrentApplication.IsValid()`。如果你也遇到類似的報錯，可以嘗試加上這個判斷。具體報錯訊息：

    > Assertion failed: CurrentApplication.IsValid() [File:E:\UE\ue5.3_git\Engine\Source\Runtime\Slate\Public\Framework\Application\SlateApplication.h] [Line: 255] 

    ![](assets/img/2023-ue-localization/tool_error.png)

--8<-- "footer_tc.md"


> 此貼文是使用 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
