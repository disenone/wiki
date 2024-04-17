---
layout: post
title: UE sets up localization for multiple languages.
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
description: How to implement localization and multi-language support in UE.
---

<meta property="og:title" content="UE 设置本地化多语言" />

#Localizing Multilingual User Experience

> Record how to achieve localization and multilingual support in UE.

If you're not familiar with the UE extension menu, it's recommended to take a quick look at: [UE extension editor menu](ue-扩展编辑器菜单.md), [ue-Use path to expand the menu](ue-使用路径形式扩展菜单.md)

This text is based on the plugin: [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##Feature Introduction

The UE comes with tools for implementing localization for multiple languages, for example, we can localize the editor menu:

English Menu:

![](assets/img/2023-ue-localization/chinese.png)

English menu:


![](assets/img/2023-ue-localization/english.png)

##Code declaration

In order to achieve menu localization, we need to explicitly declare the strings that require UE processing in the code, using the macros `LOCTEXT` and `NSLOCTEXT` defined by UE.

- To define the entire file globally, start by defining a macro called `LOCTEXT_NAMESPACE`, which contains the namespace of the current multilingual text. Then, use `LOCTEXT` to define the text in the file. Finally, remove the `LOCTEXT_NAMESPACE` macro at the end of the file.

```cpp
// #define LOCTEXT(InKey, InTextLiteral)

#define LOCTEXT_NAMESPACE "EditorPlusTools"
LOCTEXT("Key", "Content");
#undef LOCTEXT_NAMESPACE

```

Local definition method, use `NSLOCTEXT`, when defining text, add namespace parameter:

```cpp
// #define NSLOCTEXT(InNamespace, InKey, InTextLiteral)

NSLOCTEXT("EditorPlusTools", "Key", "Content");
```

The UE tool collects all the text that needs to be translated by searching for the presence of the macros `LOCTEXT` and `NSLOCTEXT`.

##Use a tool to translate the text

Assuming we have the following code defining the text:

```cpp
#define LOCTEXT_NAMESPACE "EditorPlusTools"
// register path node loctext
FEditorPlusPath::GetNodeByPath("/MenuTest")->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
FEditorPlusPath::GetNodeByPath("/MenuTest/<SubMenu>SubMenu1")->SetFriendlyName(LOCTEXT("SubMenu1", "SubMenu1"))->SetFriendlyTips(LOCTEXT("SubMenu1Tips", "SubMenu1Tips"));
FEditorPlusPath::GetNodeByPath("/MenuTest/<SubMenu>SubMenu1/<SubMenu>SubMenu1")->SetFriendlyName(LOCTEXT("SubMenu1", "SubMenu1"))->SetFriendlyTips(LOCTEXT("SubMenu1Tips", "SubMenu1Tips"));
FEditorPlusPath::GetNodeByPath("/<Hook>Help/<MenuBar>MenuTest/<SubMenu>SubMenu1/<Section>Section1")->SetFriendlyName(LOCTEXT("Section1", "Section1"))->SetFriendlyTips(LOCTEXT("Section1Tips", "Section1Tips"));
#undef LOCTEXT_NAMESPACE
```

First, open the translation tool and go to the editor settings `Edit - Editor Preferences`, then check `General - Experimental Features - Tools - Translation Selector`.

![](assets/img/2023-ue-localization/editor_enable_tool.png)


Then open the translation tool `Tools - Localization Control Panel`:

![](assets/img/2023-ue-localization/editor_open_tool.png)

Create a new target (It's okay to create under the default Game, creating a new one for the convenience of managing and moving these translated texts)

![](assets/img/2023-ue-localization/tool_new_target.png)

Set the parameters for the target, change the name to `EditorPlusTools` here, load the policy as `Editor`, collect from text, and add the plugin directory. The target dependencies are `Engine, Editor`, keep the other configurations unchanged:

![](assets/img/2023-ue-localization/tool_target_config.png)

Add language support to ensure that there are two language options: Chinese (Simplified) and English. Verify that when the mouse is placed over the language name, "zh-Hans" and "en" are displayed respectively. Select English, as the text in our code is defined in English, and we need to gather this English text here.

![](assets/img/2023-ue-localization/tool_target_lang.png)

Click to collect text:

![](assets/img/2023-ue-localization/tool_target_collect.png)

A progress dialog will pop up, wait for the collection to be successful, and a green check mark will be displayed:

![](assets/img/2023-ue-localization/tool_target_collected.png)

Turn off the collection progress dialog and go back to the translation tool. You can see the number of collected items displayed in one line of English that we don't need to translate. Click the translation button for the Chinese line.

![](assets/img/2023-ue-localization/tool_go_trans.png)

Open the window and you will see that the "Untranslated" column has content. On the right side of the English text, input the translated content. Once all the content has been translated, save and exit the window.

![](assets/img/2023-ue-localization/tool_trans.png)

Click to calculate the number of words, and after finishing, you will be able to see the Chinese column displaying the translated quantity:

![](assets/img/2023-ue-localization/tool_count.png)

Final compiled text:

![](assets/img/2023-ue-localization/tool_build.png)

The translated data will be placed in `Content\Localization\EditorPlusTools`, with one folder for each language. Inside the zh-Hans folder, you can see two files. `.archive` is the collected and translated text, while `.locres` is the compiled data.

![](assets/img/2023-ue-localization/tool_ret.png)

![](assets/img/2023-ue-localization/tool_ret2.png)

##Put the translated text into the plugin directory

We've placed the translation text generated for the plugin in the project directory above. We need to move these texts into the plugin to facilitate publishing them along with the plugin.

Move the `Content\Localization\EditorPlusTools` directory to the plugin directory under Content, I have it here as `Plugins\UE.EditorPlus\Content\Localization\EditorPlusTools`.

Modify the configuration file of the project `DefaultEditor.ini` and add the new path:

```ini
[Internationalization]
+LocalizationPaths=%GAMEDIR%Plugins/UE.EditorPlus/Content/Localization/EditorPlusTools
```

In this way, after receiving the plugin, other projects can simply modify `DefaultEditor.ini` to directly use the translated text without the need to reconfigure the translation.

##Precautions

In the process of generating translation data, we have encountered some issues. The following are the key points to be aware of:

In the code, text must be defined using the `LOCTEXT` and `NSLOCTEXT` macros, and the text needs to be a string constant for Unreal Engine to collect it.
Translate these text into English language:

The target name of the translation cannot contain the symbols `.`, and the directory name under `Content\Localization\` cannot contain `.`. UE will only take the name before the `.`. This may cause UE to fail to read the translation text due to incorrect names.
For editor plugins, it is necessary to check if it is in command line mode using `IsRunningCommandlet()`. If it is, then menus and SlateUI should not be generated because there is no Slate module in command line mode, which can lead to an error when collecting text: `Assertion failed: CurrentApplication.IsValid()`. If you encounter a similar error, you can try adding this check. Specific error information:

    > Assertion failed: CurrentApplication.IsValid() [File:E:\UE\ue5.3_git\Engine\Source\Runtime\Slate\Public\Framework\Application\SlateApplication.h] [Line: 255]

    ![](assets/img/2023-ue-localization/tool_error.png)

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki_blog/issues/new) if any omissions.
