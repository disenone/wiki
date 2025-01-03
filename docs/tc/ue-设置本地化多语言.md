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
description: 紀錄如何在 UE 中實現本地化多語言
---

<meta property="og:title" content="UE 设置本地化多语言" />

#設定本地化多語言

> 記錄如何在UE中實現本地化多語言。

如果對於UE擴展菜單不太熟悉的話，建議先簡單看一下：[UE擴展編輯器菜單](ue-扩展编辑器菜单.md)(ue-使用路径形式扩展菜单.md)

這段文字是基於插件：[UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##功能介紹

UE自帶工具可以實現本地化多語言，譬如我們可以為編輯器菜單實現本地化：

中文菜單：

![](assets/img/2023-ue-localization/chinese.png)

英文菜單：

![](assets/img/2023-ue-localization/english.png)

##程式碼聲明

為了實現菜單本地化，我們需要在程式碼中明確聲明需要 UE 處理的字串，使用 UE 定義好的宏 `LOCTEXT` 和 `NSLOCTEXT`：

- 詞典全域定義方式，首先定義一個名為`LOCTEXT_NAMESPACE`的巨集，其內容為目前多語言文本所在的命名空間，隨後文件中的文本即可使用`LOCTEXT`進行定義，檔案最後取消巨集`LOCTEXT_NAMESPACE`：

```cpp
// #define LOCTEXT(InKey, InTextLiteral)

#define LOCTEXT_NAMESPACE "EditorPlusTools"
LOCTEXT("Key", "Content");
#undef LOCTEXT_NAMESPACE

```

- 使用局部定義方法，可以運用 `NSLOCTEXT`，在定義文本時請加上命名空間參數：

```cpp
// #define NSLOCTEXT(InNamespace, InKey, InTextLiteral)

NSLOCTEXT("EditorPlusTools", "Key", "Content");
```

UE工具透過搜尋 `LOCTEXT` 和 `NSLOCTEXT` 宏的出現，來收集所有需要翻譯的文字。

##使用工具將文本翻譯為繁體中文。

假設我們有以下程式碼定義文本：

```cpp
#define LOCTEXT_NAMESPACE "EditorPlusTools"
// register path node loctext
FEditorPlusPath::GetNodeByPath("/MenuTest")->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
FEditorPlusPath::GetNodeByPath("/MenuTest/<SubMenu>SubMenu1")->SetFriendlyName(LOCTEXT("SubMenu1", "SubMenu1"))->SetFriendlyTips(LOCTEXT("SubMenu1Tips", "SubMenu1Tips"));
FEditorPlusPath::GetNodeByPath("/MenuTest/<SubMenu>SubMenu1/<SubMenu>SubMenu1")->SetFriendlyName(LOCTEXT("SubMenu1", "SubMenu1"))->SetFriendlyTips(LOCTEXT("SubMenu1Tips", "SubMenu1Tips"));
FEditorPlusPath::GetNodeByPath("/<Hook>Help/<MenuBar>MenuTest/<SubMenu>SubMenu1/<Section>Section1")->SetFriendlyName(LOCTEXT("Section1", "Section1"))->SetFriendlyTips(LOCTEXT("Section1Tips", "Section1Tips"));
#undef LOCTEXT_NAMESPACE
```

請先啟用翻譯工具，打開編輯器設定 `編輯 - 編輯器偏好設定`，勾選 `通用 - 實驗性功能 - Tools - 翻譯選擇器`：

![](assets/img/2023-ue-localization/editor_enable_tool.png)


接著開啟翻譯工具 `工具 - 本地化控制板`：

![](assets/img/2023-ue-localization/editor_open_tool.png)

新建一個目標（在預設的 Game 下面也行，新建一個是為了方便管理和移動這些翻譯文本）

![](assets/img/2023-ue-localization/tool_new_target.png)

將設定目標的參數調整，將其名稱修改為 `EditorPlusTools`，載入政策為`編輯器`，採用文本收集並包括插件目錄，目標相依性為`引擎, 編輯器`，其餘配置保持不變：

![](assets/img/2023-ue-localization/tool_target_config.png)

添加語系，確保有中文（簡體）和英文兩種語系，確認滑鼠放在語言名字上分別顯示 `zh-Hans` 和 `en`，並選中英語（因為我們程式裡是用英文定義的文本，我們這裡需要收集這些英語文本）：

![](assets/img/2023-ue-localization/tool_target_lang.png)

點選以收集文字：

![](assets/img/2023-ue-localization/tool_target_collect.png)

將會彈出收集進度視窗，等待收集成功後，將會顯示綠色勾勾：

![](assets/img/2023-ue-localization/tool_target_collected.png)

關閉收集進度框，回到翻譯工具可看到英文一行有顯示收集到的數量，本身英文的我們不需要翻譯，點開中文一行的翻譯按鈕：

![](assets/img/2023-ue-localization/tool_go_trans.png)

打開後我們可以看到未翻譯一欄有內容，在英文文本的右邊一欄輸入翻譯後的內容，翻譯內容都完成之後，保存退出窗口：

![](assets/img/2023-ue-localization/tool_trans.png)

點擊統計字數，結束後能看到中文一欄顯示了翻譯的數量：

![](assets/img/2023-ue-localization/tool_count.png)

最後編譯文本：

![](assets/img/2023-ue-localization/tool_build.png)

翻譯的資料會放在`Content\Localization\EditorPlusTools`裡面，每種語言一個資料夾， 在zh-Hans裡面能看到兩個檔案，`.archive`是收集和翻譯的文字，`.locres`則是編譯之後的資料:

![](assets/img/2023-ue-localization/tool_ret.png)

![](assets/img/2023-ue-localization/tool_ret2.png)

##將翻譯好的文本放入外掛程式目錄中。

我哋哋喺項目目錄底下插件生成果啲翻譯文本，我哋需要將呢啲文本移動返插件入面，方便隨住插件一齊發佈。

將 `Content\Localization\EditorPlusTools` 目錄移動到插件目錄 Content 底下，這裡是 `Plugins\UE.EditorPlus\Content\Localization\EditorPlusTools`。

修改項目的配置文件 `DefaultEditor.ini`，加上新路徑：

```ini
[Internationalization]
+LocalizationPaths=%GAMEDIR%Plugins/UE.EditorPlus/Content/Localization/EditorPlusTools
```

這樣一來，其他專案只要拿到插件之後，就能直接修改 `DefaultEditor.ini` 來使用翻譯文本，而不需重新配置翻譯。

##注意事項

在產生翻譯資料的過程中，遇到過一些問題，以下總結出來注意的事項：

在程式碼中，必須使用宏 `LOCTEXT` 和 `NSLOCTEXT` 來定義文本，這些文本必須是字串常量，這樣 Unreal Engine 才能將其收集起來。
- 翻譯目標名稱不能包含 `.` 符號，`Content\Localiztion\` 資料夾名稱中不能包含 `.`，UE 將僅抓取 `.` 前的名稱。這可能導致 UE 在讀取翻譯文本時因名稱錯誤而無法讀取成功。
對於編輯器插件，需要判斷如果是命令行模式 `IsRunningCommandlet()` 則不生成選單和 SlateUI，因為命令行模式下沒有 Slate 模塊，會導致收集文本的時候報錯 `Assertion failed: CurrentApplication.IsValid()`。如果你也遇到類似的報錯，可以嘗試加上這個判斷。具體報錯訊息：

    > Assertion failed: CurrentApplication.IsValid() [File:E:\UE\ue5.3_git\Engine\Source\Runtime\Slate\Public\Framework\Application\SlateApplication.h] [Line: 255] 

    ![](assets/img/2023-ue-localization/tool_error.png)

--8<-- "footer_tc.md"


> 此篇文章是由 ChatGPT 翻譯的，[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出所有被忽略的地方。 
