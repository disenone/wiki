---
layout: post
title: توسيع قائمة محرر UE
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
description: سجل كيفية توسيع قائمة المحرّر في UE
---


<meta property="og:title" content="UE 扩展编辑器菜单" />

#تم توسيع قائمة محرر UE.

> سجّل كيفية توسيع قائمة المحرر في UE.

## Hook

يمكن فهم Hook على أنه نقطة ربط لقوائم الامتدادات. يمكننا تعيين أوامر القائمة الجديدة أمام أو خلف Hook. تحتوي معظم أوامر القوائم في محرر UE على Hook. لعرض جميع Hook الخاصة بالقوائم، افتح `تحرير - تفضيلات المحرر - عام - آخرون - عرض نقاط امتداد واجهة المستخدم` في UE5.

![](assets/img/2023-ue-extend_menu/show_hook.png)

![](assets/img/2023-ue-extend_menu/show_hook2.png)

##الاعتماد على الوحدة

يجب أن تقوم بإضافة الوحدات النمطية التالية كتبعيات في ملف .Build.cs للمشروع: LevelEditor, Slate, SlateCore, EditorStyle, EditorWidgets, UnrealEd, ToolMenus.

```c#
PrivateDependencyModuleNames.AddRange(
    new string[]
    {
        "Core",
        "Engine",
        "CoreUObject",
        "LevelEditor",
        "Slate",
        "SlateCore",
        "EditorStyle",
        "EditorWidgets",
        "UnrealEd",
        "ToolMenus",
    }
    );
```

##أضف شريط القوائم

Please provide a sentence or more context for the translation.

```cpp
auto MenuExtender = MakeShared<FExtender>();

MenuExtender->AddMenuBarExtension(
    "Help", EExtensionHook::After,      // Create After Help
    nullptr,
    FMenuBarExtensionDelegate::CreateLambda([](FMenuBarBuilder& MenuBarBuilder)
    {
        MenuBarBuilder.AddPullDownMenu(
            TEXT("MenuTest"),       // Name
            TEXT("MenuTest"),       // Tips
            FNewMenuDelegate::CreateLambda([](FMenuBuilder& MenuBuilder)
            {
                // create sub menus
            }),
            TEXT("MenuText"));      // New Hook
    })
);
FModuleManager::LoadModuleChecked<FLevelEditorModule>("LevelEditor").GetMenuExtensibilityManager()->AddExtender(MenuExtender);
```

تنفيذ الشفرة أعلاه يمكن أن نلاحظ أنه تمت إضافة شريط قوائم MenuTest وراء كلمة "مساعدة".

![](assets/img/2023-ue-extend_menu/bar.png)

##إضافة أمر

استخدام الواجهة `MenuBuilder.AddMenuEntry`:

```cpp
// Inside MenuTest Lambda
MenuBuilder.AddMenuEntry(
    FText::FromName("MenuTestAction"), FText::FromName("MenuTestAction"),
    FSlateIcon(), FUIAction(FExecuteAction::CreateLambda([]()
    {
        // do action
    })));
```

وضع هذا الكود في "CreateLambda" سيُنشئ أمر القائمة.

![](assets/img/2023-ue-extend_menu/action.png)

##تقسيم القائمة

استخدام `MenuBuilder.BeginSection` و `MenuBuilder.EndSection`：

```cpp
MenuBuilder.BeginSection(NAME_None, FText::FromName("MenuTestSection"));
// code to create action
MenuBuilder.EndSection();
```

##فاصلة

```cpp
MenuBuilder.AddMenuSeparator();
```

![](assets/img/2023-ue-extend_menu/section&sperator.png)

##القائمة الفرعية

القائمة الفرعية تشبه شريط القوائم، وتحتاج إلى تعريف داخل اللامبدا:

```cpp
MenuBuilder.AddSubMenu(
    FText::FromName("MenuTestSub"),	
    FText::FromName("MenuTestSub"),	
    FNewMenuDelegate::CreateLambda([](FMenuBuilder& MenuBuilder)
    {
        MenuBuilder.AddMenuEntry(
            FText::FromName("MenuTestSubAction"), FText::FromName("MenuTestSubAction"),
            FSlateIcon(), FUIAction(FExecuteAction::CreateLambda([]()
            {
                // do action
            })));
    }));
```

![](assets/img/2023-ue-extend_menu/submenu.png)

#عنصر التحكم SlateUI

يمكنك أيضاً إضافة عناصر تحكم واجهة المستخدم:

```cpp
MenuBuilder.AddWidget(
    SNew(SHorizontalBox)
        + SHorizontalBox::Slot()
        .AutoWidth()
        [
            SNew(SEditableTextBox)
            .MinDesiredWidth(50)
            .Text(FText::FromName("MenuTestWidget"))
        ]
        
        + SHorizontalBox::Slot()
        .AutoWidth()
        .Padding(5, 0, 0, 0)
        [
        SNew(SButton)
        .Text(FText::FromName("ExtendWidget"))
        .OnClicked(FOnClicked::CreateLambda([]()
        {
            // do action
            return FReply::Handled();
        }))
        ],
    FText::GetEmpty()
);
```

![](assets/img/2023-ue-extend_menu/widget.png)

سليت يو آي المتعلقة هنا لن نقوم بتوضيحها بالتفصيل، يمكنك البحث عن مقال آخر إذا كنت مهتمًا.

#Hook تزيين القائمة

أضف أمرًا مثل تلك الموجودة في `الأدوات - البرمجة`.

```cpp
MenuExtender->AddMenuExtension(
    "Programming", EExtensionHook::After,
    nullptr,
    FMenuExtensionDelegate::CreateLambda([](FMenuBuilder& MenuBuilder)
    {
        MenuBuilder.AddMenuEntry(
        FText::FromName("MenuTestAction"), FText::FromName("MenuTestAction"),
        FSlateIcon(), FUIAction(FExecuteAction::CreateLambda([]()
        {
            // do action
        })));
    })
);
```

![](assets/img/2023-ue-extend_menu/other_hook.png)

يمكنك أيضًا إضافة أنواع قوائم طعام أخرى.

#الرجاء تقديم نص آخر للترجمة.

```cpp
void BuildTestMenu()
{
	auto MenuExtender = MakeShared<FExtender>();

	MenuExtender->AddMenuBarExtension(
		"Help", EExtensionHook::After,
		nullptr,
		FMenuBarExtensionDelegate::CreateLambda([](FMenuBarBuilder& MenuBarBuilder)
		{
			MenuBarBuilder.AddPullDownMenu(
				FText::FromName("MenuTest"),
				FText::FromName("MenuTest"),
				FNewMenuDelegate::CreateLambda([](FMenuBuilder& MenuBuilder)
				{
					MenuBuilder.BeginSection(NAME_None, FText::FromName("MenuTestSection"));
					MenuBuilder.AddMenuSeparator();
					MenuBuilder.AddMenuEntry(
						FText::FromName("MenuTestAction"), FText::FromName("MenuTestAction"),
						FSlateIcon(), FUIAction(FExecuteAction::CreateLambda([]()
						{
                            // do action
						})));

					MenuBuilder.AddSubMenu(
						FText::FromName("MenuTestSubb"),
						FText::FromName("MenuTestSubb"),
						FNewMenuDelegate::CreateLambda([](FMenuBuilder& MenuBuilder)
						{
							MenuBuilder.AddMenuEntry(
								FText::FromName("MenuTestSubAction"), FText::FromName("MenuTestSubAction"),
								FSlateIcon(), FUIAction(FExecuteAction::CreateLambda([]()
								{
                                    // do action
								})));
						}));
					MenuBuilder.EndSection();

					MenuBuilder.AddWidget(
					SNew(SHorizontalBox)
						 + SHorizontalBox::Slot()
						 .AutoWidth()
						 [
							 SNew(SEditableTextBox)
							 .MinDesiredWidth(50)
							 .Text(FText::FromName("MenuTestWidget"))
						 ]
						 + SHorizontalBox::Slot()
						 .AutoWidth()
						 .Padding(5, 0, 0, 0)
						 [
							SNew(SButton)
							.Text(FText::FromName("ExtendWidget"))
							.OnClicked(FOnClicked::CreateLambda([]()
							{
								// do action
								return FReply::Handled();
							}))
						 ],
					 FText::GetEmpty()
					);
				}),
				"MenuTest");
		})
	);

	MenuExtender->AddMenuExtension(
		"Programming", EExtensionHook::After,
		nullptr,
		FMenuExtensionDelegate::CreateLambda([](FMenuBuilder& MenuBuilder)
		{
			MenuBuilder.AddMenuEntry(
			FText::FromName("MenuTestAction"), FText::FromName("MenuTestAction"),
			FSlateIcon(), FUIAction(FExecuteAction::CreateLambda([]()
			{
                // do action
			})));
		})
	);

	FModuleManager::LoadModuleChecked<FLevelEditorModule>("LevelEditor").GetMenuExtensibilityManager()->AddExtender(MenuExtender);
}
```

![](assets/img/2023-ue-extend_menu/overall.png)

--8<-- "footer_ar.md"



> تم ترجمة هذه المشاركة باستخدام ChatGPT، يرجى تقديم [**ردود الفعل**](https://github.com/disenone/wiki_blog/issues/new)يرجى إشارة إلى أي نقص. 
