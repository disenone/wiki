---
layout: post
title: UE sets up localized multilingual options.
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
description: Record how to achieve localization and multilingual support in Unreal
  Engine.
---

<meta property="og:title" content="UE 设置本地化多语言" />

#UE sets up localized multilingual support.

> How to implement localization and multiple languages in UE记录

If you are not familiar with UE extension menu, it is recommended to take a quick look at: [UE extension editor menu](ue-扩展编辑器菜单.md),[ue- Use path form to extend the menu](ue-使用路径形式扩展菜单.md)

The code in this article is based on the plugin: [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##Function Introduction

The built-in tools of UE can achieve localized multilingual support; for example, we can localize the editor menu.

Chinese Menu:

![](assets/img/2023-ue-localization/chinese.png)

English menu:

![](assets/img/2023-ue-localization/english.png)

##Code declaration

To achieve menu localization, we need to explicitly declare the strings that require UE handling in the code, using the macros `LOCTEXT` and `NSLOCTEXT` defined by UE.

- The global definition method for documents starts by defining a macro called `LOCTEXT_NAMESPACE`, which contains the namespace of the current multilingual text. After that, text in the document can be defined using `LOCTEXT`, and finally, the macro `LOCTEXT_NAMESPACE` is canceled at the end of the file.

```cpp
// #define LOCTEXT(InKey, InTextLiteral)

#define LOCTEXT_NAMESPACE "EditorPlusTools"
LOCTEXT("Key", "Content");
#undef LOCTEXT_NAMESPACE

```

Define text locally using `NSLOCTEXT`, remember to include the namespace parameter when defining the text:

```cpp
// #define NSLOCTEXT(InNamespace, InKey, InTextLiteral)

NSLOCTEXT("EditorPlusTools", "Key", "Content");
```

The UE tool collects all the text that needs to be translated by searching for the occurrences of the macros `LOCTEXT` and `NSLOCTEXT`.

##Translate text using tools.

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

First, open the translation tool and go to the editor settings by clicking `Edit - Editor Preferences`. Then, check `General - Experimental Features - Tools - Translation Selector`:

![](assets/img/2023-ue-localization/editor_enable_tool.png)


Then open the translation tool `Tools - Localization Control Panel`:

![](assets/img/2023-ue-localization/editor_open_tool.png)

Create a new target (it can be under the default Game as well; creating a new one is for easier management and movement of these translation texts).

![](assets/img/2023-ue-localization/tool_new_target.png)

Configure the parameters for the target, I will rename it to `EditorPlusTools`, the loading policy is `Editor`, it collects from text, adds the plugin directory, and the target dependencies are `Engine, Editor`, with other configurations remaining unchanged:

![](assets/img/2023-ue-localization/tool_target_config.png)

Add language options to ensure both Simplified Chinese and English are available. Confirm that when hovering over the language names, `zh-Hans` and `en` are displayed respectively, and select English (as the text in our code is defined in English, we need to collect these English texts here).

![](assets/img/2023-ue-localization/tool_target_lang.png)

Click to collect text:

![](assets/img/2023-ue-localization/tool_target_collect.png)

A dialog box will pop up to show the progress of the collection. Please wait until the collection is successful. A green checkmark will be displayed once the collection is complete.

![](assets/img/2023-ue-localization/tool_target_collected.png)

Turn off the progress collection box, and return to the translation tool where you can see the collected quantity displayed on the English line. The English text itself does not need translation. Click the translation button on the Chinese line.

![](assets/img/2023-ue-localization/tool_go_trans.png)

After opening, we can see that there is content in the untranslated column. Enter the translated content in the column to the right of the English text. Once all translations are completed, save and close the window.

![](assets/img/2023-ue-localization/tool_trans.png)

Click to count the number of characters, and after it finishes, you can see the Chinese column showing the translated quantity:

![](assets/img/2023-ue-localization/tool_count.png)

Final compilation text:

![](assets/img/2023-ue-localization/tool_build.png)

The translated data will be placed in `Content\Localization\EditorPlusTools`, with a separate folder for each language. In the zh-Hans folder, you will find two files: `.archive` contains the collected and translated text, while `.locres` is the compiled data.

![](assets/img/2023-ue-localization/tool_ret.png)

![](assets/img/2023-ue-localization/tool_ret2.png)

##Place the translated text into the plugin directory.

We have placed the translated text generated for the plugin in the project directory, and we need to move this text into the plugin for easier release along with the plugin.

Move the `Content\Localization\EditorPlusTools` directory to the plugin directory under Content, which in my case is `Plugins\UE.EditorPlus\Content\Localization\EditorPlusTools`.

Edit the configuration file of the project `DefaultEditor.ini` and add the new path:

```ini
[Internationalization]
+LocalizationPaths=%GAMEDIR%Plugins/UE.EditorPlus/Content/Localization/EditorPlusTools
```

In this way, once other projects receive the plugin, they can simply modify `DefaultEditor.ini` to use the translated text directly, without the need to reconfigure the translation.

##Precautions

During the process of generating translation data, several issues were encountered. Below is a summary of the important points to be aware of:

Text inside the code must be defined using the macros `LOCTEXT` and `NSLOCTEXT`, and the text needs to be a string constant for Unreal Engine to collect it.
The translated text is:

- The translated target name cannot contain the symbols `.`, and the directory names under `Content\Localization\` cannot contain `.`. UE will only extract the name before `.`. This may cause UE to fail to read the translated text due to incorrect names.
For editor plugins, it is necessary to check if it is running in command-line mode by using `IsRunningCommandlet()`, in which case menus and SlateUI should not be generated since the Slate module is not available in command-line mode. This can cause an error when collecting text, such as `Assertion failed: CurrentApplication.IsValid()`. If you encounter a similar error, you can try adding this check. Specific error message:

    > Assertion failed: CurrentApplication.IsValid() [File:E:\UE\ue5.3_git\Engine\Source\Runtime\Slate\Public\Framework\Application\SlateApplication.h] [Line: 255] 

    ![](assets/img/2023-ue-localization/tool_error.png)

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please provide feedback in [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions. 
