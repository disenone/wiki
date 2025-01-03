---
layout: post
title: استخدام المسار لتوسيع القائمة UE
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
---

<meta property="og:title" content="UE 使用路径形式扩展菜单" />

> سجل كيفية توسيع قائمة المسارات في UE.

إذا كنت غير ملم بقائمة تمديد UE، فأنصح بالنظر إليها بشكل مبسّط أولاً: [قائمة محرر تمديد UE](ue-扩展编辑器菜单.md)

هذا النص مبني على الإضافة: [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##إدارة العقدة

قم بإدارة القائمة بناءً على هيكل الشجرة، حيث يمكن أن تضم العقد الأب الأطفال:

```cpp
class EDITORPLUS_API FEditorPlusMenuBase: public TSharedFromThis<FEditorPlusMenuBase>
{
protected:
	// sub menus
	TArray<TSharedRef<FEditorPlusMenuBase>> Children;
}
```

في إنشاء العقد الأب، إنشاء العقد الفرعي في نفس الوقت:

```cpp
void FEditorPlusMenuBase::Register(FMenuBuilder& MenuBuilder)
{
	for (const auto Menu: Children)
	{
		Menu->Register(MenuBuilder);
	}
}
```

بالطبع، ستكون سلوكيات إنشاء كل عقدة محددة مختلفة قليلاً، استخدام الدوال الافتراضية المشتركة لتحقيق ذلك:

```cpp
// Menubar
void FEditorPlusMenuBar::Register(FMenuBarBuilder& MenuBarBuilder)
{
	MenuBarBuilder.AddPullDownMenu(
		GetFriendlyName(),
		GetFriendlyTips(),
        // Delegate to call Register
		FEditorPlusMenuManager::GetDelegate<FNewMenuDelegate>(GetUniqueId()),       
		Hook);
}

// Section
void FEditorPlusSection::Register(FMenuBuilder& MenuBuilder)
{
	MenuBuilder.BeginSection(Hook, GetFriendlyName());
	FEditorPlusMenuBase::Register(MenuBuilder);
	MenuBuilder.EndSection();
}

// Separator
void FEditorPlusSeparator::Register(FMenuBuilder& MenuBuilder)
{
	MenuBuilder.AddMenuSeparator(Hook);
	FEditorPlusMenuBase::Register(MenuBuilder);
}

// SubMenu
void FEditorPlusSubMenu::Register(FMenuBuilder& MenuBuilder)
{
	MenuBuilder.AddSubMenu(
		GetFriendlyName(),
		GetFriendlyTips(),
		FNewMenuDelegate::CreateSP(this, &FEditorPlusSubMenu::MakeSubMenu),
		false,
		FSlateIcon(),
		true,
		Hook
	);
}

// Command
void FEditorPlusCommand::Register(FMenuBuilder& MenuBuilder)
{
    MenuBuilder.AddMenuEntry(
        CommandInfo->Label, CommandInfo->Tips, CommandInfo->Icon,
        CommandInfo->ExecuteAction, CommandInfo->Hook, CommandInfo->Type);
}

// ......
```

##إنشاء عقدة عن طريق المسار

قم بتنظيم القوائم بتنسيق شجري، حيث يمكن تحديد هيكل شجري لقائمة واحدة عبر تنسيق المسار.

```cpp
"/<Hook>Help/<MenuBar>BarTest/<SubMenu>SubTest/<Command>Action"
```

يمكن تعريف سلسلة من القوائم من خلال المسار أعلاه:

- `<‏خطاف>المساعدة`：الموقع بعد القائمة التي اسمها Hook والذي يليه اسم Help
- `<MenuBar>BarTest` : إنشاء قائمة من نوع MenuBar بالاسم BarTest
- `<SubMenu>SubTest`: إنشاء العقدة الفرعية، من نوع SubMenu، بالاسم SubTest
- `<Command>Action`：أنشئ أمرًا في النهاية

يمكن أن تكون طريقة استدعاء الواجهة بسيطة جدًا:

```cpp
const FString Path = "/<Hook>Help/<MenuBar>BarTest/<SubMenu>SubTest/<Command>Action";
FEditorPlusPath::RegisterPathAction(
	Path, 
    FExecuteAction::CreateLambda([]
    {
        // do action
    })
);
```

##إنشاء عقد بتنسيق مخصص

لقد استمررنا في الاحتفاظ بالطريقة الثقيلة لإنشاء القوائم، حيث يمكن للطريقة الثقيلة أن تسمح بإعدادات أكثر تفصيلاً، ويشبه تنظيم الرمز في SlateUI الخاص بـ UE إلى حد ما:

```cpp
EP_NEW_MENU(FEditorPlusMenuBar)("BarTest")
->RegisterPath()
->Content({
    EP_NEW_MENU(FEditorPlusSubMenu)("SubTest")
    ->Content({
        EP_NEW_MENU(FEditorPlusCommand)("Action")
        ->BindAction(FExecuteAction::CreateLambda([]
            {
                // do action
            })),
    })
});
```

##الرجاء تحديد اللغة التي ترغب في ترجمتها.

بالطبع، شكل مسار الصفحة وقوائم الإنشاء المخصصة يتشابهان، يمكن دمجهما معًا بمرونة كبيرة:

```cpp
FEditorPlusPath::RegisterPath(
    "/<MenuBar>BarTest/<SubMenu>SubMenu/<Command>Action1", 
    EP_NEW_MENU(FEditorPlusCommand)("Action1")
    ->BindAction(FExecuteAction::CreateLambda([]
        {
            // do action
        })),
);

FEditorPlusPath::RegisterPath(
    "/<MenuBar>BarTest/<SubMenu>SubMenu/<Command>Action2", 
    EP_NEW_MENU(FEditorPlusCommand)("Action2")
    ->BindAction(FExecuteAction::CreateLambda([]
        {
            // do action
        })),
);
```

سيتم دمج القوائم المعرفة في أماكن متعددة في هيكل شجري واحد، حيث يُعتبر العقد ذو الاسم المماثل كعقد واحد. بمعنى آخر، المسار فريد، ويمكن لنفس المسار تحديد عقد واحد من القائمة بصورة فريدة.
بناءً عليه، يمكننا أيضًا تحديد العقد، وإعادة تهيئة وتعديل بعض الإعدادات.

```cpp
// set Name and Tips
FEditorPlusPath::GetNodeByPath("/<MenuBar>BarTest")->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
```


--8<-- "footer_ar.md"


> تمت ترجمة هذه المشاركة باستخدام ChatGPT ، يرجى تقديم [**تقييم**](https://github.com/disenone/wiki_blog/issues/new)أشر على أي شيء مفقود. 
