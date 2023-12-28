---
layout: post
title: UE 设置本地化多语言
tags: [dev, game, UE, UnreanEngine, UE4, UE5]
description: 记录如何在 UE 中实现本地化多语言
---
<meta property="og:title" content="UE 设置本地化多语言" />

# UE 设置本地化多语言

> 记录如何在 UE 中实现本地化多语言

如果不熟悉 UE 扩展菜单，建议先简单看下：[UE 扩展编辑器菜单](ue-扩展编辑器菜单.md)，[ue-使用路径形式扩展菜单](ue-使用路径形式扩展菜单.md)

本文代码基于插件：[UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

## 功能介绍

UE 自带工具可以实现本地化多语言，譬如我们可以为编辑器菜单实现本地化：

中文菜单：

![](assets/img/2023-ue-localization/chinese.png)

英文菜单：

![](assets/img/2023-ue-localization/english.png)

## 代码声明

为了实现菜单本地化，我们需要在代码中明确声明需要 UE 处理的字符串，使用 UE 定义好的宏 `LOCTEXT` 和 `NSLOCTEXT`：

- 文件全局定义方式，先开始定义一个叫做 `LOCTEXT_NAMESPACE` 的宏，内容是当前多语言文本所在的名字空间，之后文件中的文本就可以用 `LOCTEXT` 来定义，文件最后取消宏 `LOCTEXT_NAMESPACE`：

```cpp
// #define LOCTEXT(InKey, InTextLiteral)

#define LOCTEXT_NAMESPACE "EditorPlusTools"
LOCTEXT("Key", "Content");
#undef LOCTEXT_NAMESPACE

```

- 局部定义方式，使用 `NSLOCTEXT`，定义文本的时候带上名字空间参数：

```cpp
// #define NSLOCTEXT(InNamespace, InKey, InTextLiteral)

NSLOCTEXT("EditorPlusTools", "Key", "Content");
```

UE 工具通过查找宏 `LOCTEXT` 和 `NSLOCTEXT` 的出现来收集出所有需要翻译的文本。

## 使用工具翻译文本

假设我们有如下代码定义文本：

```cpp
#define LOCTEXT_NAMESPACE "EditorPlusTools"
// register path node loctext
FEditorPlusPath::GetNodeByPath("/MenuTest")->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
FEditorPlusPath::GetNodeByPath("/MenuTest/<SubMenu>SubMenu1")->SetFriendlyName(LOCTEXT("SubMenu1", "SubMenu1"))->SetFriendlyTips(LOCTEXT("SubMenu1Tips", "SubMenu1Tips"));
FEditorPlusPath::GetNodeByPath("/MenuTest/<SubMenu>SubMenu1/<SubMenu>SubMenu1")->SetFriendlyName(LOCTEXT("SubMenu1", "SubMenu1"))->SetFriendlyTips(LOCTEXT("SubMenu1Tips", "SubMenu1Tips"));
FEditorPlusPath::GetNodeByPath("/<Hook>Help/<MenuBar>MenuTest/<SubMenu>SubMenu1/<Section>Section1")->SetFriendlyName(LOCTEXT("Section1", "Section1"))->SetFriendlyTips(LOCTEXT("Section1Tips", "Section1Tips"));
#undef LOCTEXT_NAMESPACE
```

首先开启翻译工具，打开编辑器设置 `编辑 - 编辑器偏好设置`，勾选 `通用 - 试验性功能 - Tools - 翻译选取器`：

![](assets/img/2023-ue-localization/editor_enable_tool.png)


然后打开翻译工具 `工具 - 本地化控制板`：

![](assets/img/2023-ue-localization/editor_open_tool.png)

新建一个目标（在默认的 Game 下面也行，新建一个是为了方便管理和移动这些翻译文本）

![](assets/img/2023-ue-localization/tool_new_target.png)

配置目标的参数，我这里名字改为 `EditorPlusTools`，加载政策是 `编辑器`，从文本收集，并加上插件目录，目标依赖性是 `Engine, Editor`，其他配置保持不变：

![](assets/img/2023-ue-localization/tool_target_config.png)

添加语系，保证有中文（简体）和英文两个语系，确认鼠标放在语言名字上分别显示 `zh-Hans` 和 `en`，并选中英语（因为我们代码里面是用英文定义的文本，我们这里需要收集这些英语文本）：

![](assets/img/2023-ue-localization/tool_target_lang.png)

点击收集文本：

![](assets/img/2023-ue-localization/tool_target_collect.png)

会弹出收集进度框，等待收集成功，会显示绿色对钩：

![](assets/img/2023-ue-localization/tool_target_collected.png)

关掉收集进度框，回到翻译工具可以看到英文一行有显示收集到的数量，本身英文的我们不需要翻译，点开中文一行的翻译按钮：

![](assets/img/2023-ue-localization/tool_go_trans.png)

打开后我们可以看到未翻译一栏有内容，在英文文本的右边一栏输入翻译后的内容，翻译内容都完成之后，保存退出窗口：

![](assets/img/2023-ue-localization/tool_trans.png)

点击统计字数，结束后能看到中文一栏显示了翻译的数量：

![](assets/img/2023-ue-localization/tool_count.png)

最后编译文本：

![](assets/img/2023-ue-localization/tool_build.png)

翻译的数据会放在 `Content\Localization\EditorPlusTools` 里面，每种语言一个文件夹，在 zh-Hans 里面能看到两个文件，`.archive` 是收集和翻译的文本，`.locres` 则是编译之后的数据：

![](assets/img/2023-ue-localization/tool_ret.png)

![](assets/img/2023-ue-localization/tool_ret2.png)

## 翻译好的文本放入插件目录中

我们上面给插件生成的翻译文本放在了项目目录下面，我们需要把这些文本移动到插件里面，方便随着插件一起发布。

把 `Content\Localization\EditorPlusTools` 目录移动到插件目录 Content 下面，我这里是 `Plugins\UE.EditorPlus\Content\Localization\EditorPlusTools`。

修改项目的配置文件 `DefaultEditor.ini`，加上新路径：

```ini
[Internationalization]
+LocalizationPaths=%GAMEDIR%Plugins/UE.EditorPlus/Content/Localization/EditorPlusTools
```

这样，其他项目拿到插件后，只要修改 `DefaultEditor.ini` 则可以直接使用翻译文本，不需要重新配置翻译。

## 注意事项

在生成翻译数据的过程中，遇到过一些问题，以下总结出来注意的事项：

- 代码里面定义文本必须要用宏 `LOCTEXT` 和 `NSLOCTEXT`，文本需要是字符串常量，这样 UE 才是收集出来。
- 翻译目标名字不能带有符号 `.`，`Content\Localiztion\` 下的目录名字不能带有 `.`，UE 只会截取 `.` 前面的名字。会导致 UE 在读取翻译文本的时候，由于名字错误，读取失败。
- 对于编辑器插件，需要判断如果是命令行模式 `IsRunningCommandlet()` 则不生成菜单和 SlateUI ，因为命令行模式下没有 Slate 模块，会导致收集文本的时候报错 `Assertion failed: CurrentApplication.IsValid()`。如果你也遇到类似的报错，可以尝试加上这个判断。具体报错信息：

    > Assertion failed: CurrentApplication.IsValid() [File:E:\UE\ue5.3_git\Engine\Source\Runtime\Slate\Public\Framework\Application\SlateApplication.h] [Line: 255] 

    ![](assets/img/2023-ue-localization/tool_error.png)

--8<-- "footer.md"
