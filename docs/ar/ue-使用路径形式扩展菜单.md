---
layout: post
title: UE استخدام مسار شكل توسيع القائمة
tags:
- dev
- game
- UE
- UnreanEngine
- UE4
- UE5
---

<meta property="og:title" content="UE 使用路径形式扩展菜单" />

> تسجيل كيفية تنفيذ قائمة توسيع نوع المسار في UE

إذا كنت غير معتاد على قائمة التمديدات في UE، يُنصح بمراجعة ما يلي بإيجاز: [قائمة محرر التمديدات في UE](ue-扩展编辑器菜单.md)

هذا النص يعتمد على البرنامج المساعد: [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##إدارة العقد

قم بإدارة القائمة وتنظيمها وفقًا لهيكل الشجرة، حيث يمكن للعقد الأب أن يحتوي على فروع فرعية:

```cpp
class EDITORPLUS_API FEditorPlusMenuBase: public TSharedFromThis<FEditorPlusMenuBase>
{
protected:
	// sub menus
	TArray<TSharedRef<FEditorPlusMenuBase>> Children;
}
```

在创建父节点的同时创建子节点：  
عند إنشاء العقدة الأم، يتم إنشاء العقدة الفرعية في نفس الوقت:

```cpp
void FEditorPlusMenuBase::Register(FMenuBuilder& MenuBuilder)
{
	for (const auto Menu: Children)
	{
		Menu->Register(MenuBuilder);
	}
}
```

بالطبع، سلوك إنشاء كل عقدة سيكون مختلفًا بعض الشيء، يتم تنفيذ ذلك عن طريق كتابة دالة افتراضية.

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

##إنشاء العقد عبر المسار

قم بتنظيم القوائم حسب هيكل شجري، بحيث يمكن تعريف شكل مسار القوائم على شكل هيكل شجري لقائمة معينة:

```cpp
"/<Hook>Help/<MenuBar>BarTest/<SubMenu>SubTest/<Command>Action"
```

يمكن بسهولة تعريف سلسلة من القوائم من خلال المسارات المذكورة أعلاه:

- `<Hook>Help` : تقع بعد القائمة التي يطلق عليها اسم Help.
- `<MenuBar>BarTest`：إنشاء قائمة من النوع MenuBar، باسم BarTest
- `<SubMenu>SubTest`：إنشاء عقدة فرعية، نوع SubMenu، اسم SubTest
- `<Command>Action`：أنشئ آخر أمر

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

##توليد عقد بالشكل المخصص

لازلنا نحتفظ بالطريقة الثقيلة لإنشاء القوائم، حيث تتيح هذه الطريقة إعدادات أكثر تفصيلاً، وتنظيم الكود مشابه إلى حد ما لأسلوب SlateUI في UE:

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

##الرجاء تقديم كلمات جديدة للترجمة.

بالطبع، شكل المسار نفسه والقوائم المُولَّدة بشكل مخصص، كلاهما متشابهان، ويمكن استخدامهما بشكل متبادل، مما يوفر مرونة كبيرة.

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

سيتم دمج القوائم التي تم تعريفها في أماكن متعددة في هيكل شجري واحد، وسيُعتبر العقد ذو الاسم المتطابق نفسه. بمعنى آخر، المسار فريد، ويمكن لنفس المسار تحديد عقد قائمة واحد.
ثم يمكننا أن نحدد العقد، ونقوم بعمل بعض الإعدادات والتعديلات من جديد:

```cpp
// set Name and Tips
FEditorPlusPath::GetNodeByPath("/<MenuBar>BarTest")->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
```


--8<-- "footer_ar.md"


> تمت ترجمة هذه المشاركة باستخدام ChatGPT، يرجى تقديم [**تعليقاتك**](https://github.com/disenone/wiki_blog/issues/new)يرجى الإشارة إلى أي نقاط تم التغاضي عنها. 
