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

#設置本地化多語言。

> 記錄如何在 UE 中實現本地化多語言

如果不熟悉 UE 擴展菜單，建議先簡單看一下：[UE 擴展編輯器菜單](ue-扩展编辑器菜单.md)(ue-使用路径形式扩展菜单.md)

本文代碼基於插件：[UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##功能介紹

UE 自帶工具可以實現本地化多語言，例如我們可以為編輯器菜單實現本地化：

中文菜單：

![](assets/img/2023-ue-localization/chinese.png)

英文菜單：

![](assets/img/2023-ue-localization/english.png)

##代码声明

為了實現菜單本地化，我們需要在程式碼中明確聲明需要 UE 處理的字串，使用 UE 定義好的巨集 `LOCTEXT` 和 `NSLOCTEXT`：

- 文件全局定義方式，首先開始定義一個叫做 `LOCTEXT_NAMESPACE` 的宏，內容是當前多語言文本所在的名字空間，之後文件中的文本就可以用 `LOCTEXT` 來定義，文件最後取消宏 `LOCTEXT_NAMESPACE`：

```cpp
// #define LOCTEXT(InKey, InTextLiteral)

#define LOCTEXT_NAMESPACE "EditorPlusTools"
LOCTEXT("Key", "Content");
#undef LOCTEXT_NAMESPACE

```

- 局部定義方式，使用 `NSLOCTEXT`，定義文本的時候帶上名稱空間參數：

```cpp
// #define NSLOCTEXT(InNamespace, InKey, InTextLiteral)

NSLOCTEXT("EditorPlusTools", "Key", "Content");
```

UE 工具通過搜索 `LOCTEXT` 和 `NSLOCTEXT` 宏的使用來彙集所有需要翻譯的文本。

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

首先開啟翻譯工具，打開編輯器設定 `編輯 - 編輯器偏好設定`，勾選 `通用 - 實驗性功能 - Tools - 翻譯選取器`：

![](assets/img/2023-ue-localization/editor_enable_tool.png)


然後打開翻譯工具 `工具 - 本地化控制板`：

![](assets/img/2023-ue-localization/editor_open_tool.png)

新建一個目標（在默認的 Game 下面也可以，新建一個是為了方便管理和移動這些翻譯文本）

![](assets/img/2023-ue-localization/tool_new_target.png)

設置目標參數，將名稱更改為 `EditorPlusTools`，加載策略為 `編輯器`，從文本收集並加上插件目錄，目標相依性為 `Engine, Editor`，保持其他配置不變：

![](assets/img/2023-ue-localization/tool_target_config.png)

請新增語言選項以確保包含簡體中文和英文兩種語言版本。當滑鼠懸停在語言名稱上時，應分別顯示 `zh-Hans` 和 `en`。請選擇英文（因為我們的程式碼中使用的是英文文本，我們需要收集這些英文文本）。

![](assets/img/2023-ue-localization/tool_target_lang.png)

點選以收集文字：

![](assets/img/2023-ue-localization/tool_target_collect.png)

會彈出收集進度框，等待收集成功，會顯示綠色對勾：

![](assets/img/2023-ue-localization/tool_target_collected.png)

關閉收集進度框，返回翻譯工具，您可以看到已經收集到的英文行數。我們不需要對英文進行翻譯。請點擊中文行的翻譯按鈕：

![](assets/img/2023-ue-localization/tool_go_trans.png)

打開後我們可以看到未翻譯一欄有內容，在英文文本的右邊一欄輸入翻譯後的內容，翻譯內容都完成後，保存退出窗口：

![](assets/img/2023-ue-localization/tool_trans.png)

點擊統計字數，結束後能看到中文一欄顯示了翻譯的數量：

![](assets/img/2023-ue-localization/tool_count.png)

最後編譯文本：

![](assets/img/2023-ue-localization/tool_build.png)

翻譯的資料將存放在 `Content\Localization\EditorPlusTools` 中，每種語言一個資料夾，在 zh-Hans 資料夾中會看到兩個檔案，`.archive` 是收集和翻譯的文字，`.locres` 則是編譯後的資料：

![](assets/img/2023-ue-localization/tool_ret.png)

![](assets/img/2023-ue-localization/tool_ret2.png)

##翻譯好的文本放入插件目錄中

我們將插件生成的翻譯文本放在了項目目錄下面，我們需要將這些文本移動到插件裡面，方便隨著插件一起發布。

把 `Content\Localization\EditorPlusTools` 目錄移動到插件目錄 Content 下面，我這裡是 `Plugins\UE.EditorPlus\Content\Localization\EditorPlusTools`。

修改項目的配置文件 `DefaultEditor.ini`，加上新路徑：

```ini
[Internationalization]
+LocalizationPaths=%GAMEDIR%Plugins/UE.EditorPlus/Content/Localization/EditorPlusTools
```

這樣，其他項目在獲取插件後，只需修改 `DefaultEditor.ini` 即可直接使用翻譯文本，無需重新配置翻譯。

##注意事項

在生成翻譯資料的過程中，遇到過一些問題，以下總結出來注意的事項：

- 在程式碼中，定義文本時必須使用宏 `LOCTEXT` 和 `NSLOCTEXT`，文本必須是字串常數，這樣 Unreal Engine 才能進行收集。
- 翻譯目標名稱不能帶有符號 `.`，`Content\Localiztion\` 下的目錄名稱不能帶有 `.`，UE 只會截取 `.` 前面的名稱。會導致 UE 在讀取翻譯文本的時候，由於名稱錯誤，讀取失敗。
- 對於編輯器插件，需要判斷如果是命令行模式 `IsRunningCommandlet()` 則不生成菜單和 SlateUI，因為命令行模式下沒有 Slate 模塊，會導致收集文本的時候報錯 `Assertion failed: CurrentApplication.IsValid()`。如果你也遇到類似的報錯，可以嘗試加上這個判斷。具體報錯信息：

    > Assertion failed: CurrentApplication.IsValid() [File:E:\UE\ue5.3_git\Engine\Source\Runtime\Slate\Public\Framework\Application\SlateApplication.h] [Line: 255] 

    ![](assets/img/2023-ue-localization/tool_error.png)

--8<-- "footer_tc.md"


> 此帖子是使用 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遺漏之處。 
