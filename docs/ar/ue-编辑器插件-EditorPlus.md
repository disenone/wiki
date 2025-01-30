---
layout: post
title: UE محرر الإضافات UE.EditorPlus الوثائق التوضيحية
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
description: ملحق محرر UE.EditorPlus UE! توضيحات توثيقية
---

<meta property="og:title" content="UE 编辑器插件 EditorPlus 说明文档" />

#UE محرر المكونات الإضافية UE.EditorPlus وثيقة الشرح

##فيديو التعريف

![type:video](assets/img/2024-ue-editorplus/market/video.mp4)

##كود مصدر الإضافة

[UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##تنزيل المتجر

[EditorPlus](https://www.unrealengine.com/marketplace/zh-CN/product/editorplus)

##إضافة مصدر المشروع الإضافي EU.EditorPlus

الرجاء تقديم نص باللغة الإنجليزية للترجمة.

الصينية: [أوي يضيف المكونات عبر مصدر البرنامج النصي للمكونات](https://wiki.disenone.site/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)
- English: [UE adds plugins through the plugin source code](https://wiki.disenone.site/en/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)


##وصف الإضافة

UE.EditorPlus هو مكون إضافي لمحرر UE، يقدم طريقة مريحة لتوسيع قائمة المحرر، ويدعم طرقًا متقدمة للتوسيع، بالإضافة إلى احتوائه على بعض أدوات المحرر المفيدة. هذا المكون الإضافي يدعم UE5.3+.


##توسيع قائمة المحرر

![](assets/img/2024-ue-editorplus/menu.png)

![](assets/img/2024-ue-editorplus/toolbar.png)

###说明

دعم توسيع قائمة المحرر بطرق متعددة:

- طريقة المسار: `RegisterPathAction("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action")`
- طريقة التهيئة: `EP_NEW_MENU(FEditorPlusMenuBar)("Bar")`
- النوع المختلط: `RegisterPath("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action",EP_NEW_MENU(FEditorPlusCommand)("Action")`

###أسلوب الطريق

يمكن تسجيل أمر قائمة المحرر بهذه الطريقة:

```cpp
FEditorPlusPath::RegisterPathAction(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action",
    FExecuteAction::CreateLambda([]
        {
            // do action
        })
);
```

بهذه الطريقة يمكن إضافة شريط قائمة Bar بعد قائمة المساعدة Help في محرر القائمة، حيث يتم إضافة قائمة فرعية SubMenu داخل Bar، وداخل SubMenu يتم إضافة أمر Action.

تكون صيغة المسار الكامل على النحو التالي: `/<Hook>HookName/<Type1>Name1/<Type2>Name2`، يجب أن يكون المسار الأول هو `<Hook>`، والأنواع والقيود المدعومة حالياً:

- `<Hook>`: تعني الحاجة إلى إنشاء القائمة في موضع الـ Hook المحدد، والمسموح بالمسارات اللاحقة أن لا تحتوي على `<Hook>`
- `<MenuBar>`: شريط القوائم، لا يمكن وضع `<Hook>` أو `<MenuBar>` أو `<ToolBar>` في المسار الخلفي
- `<ToolBar>`: شريط الأدوات، يجب ألا يكون هناك `<Hook>`، `<MenuBar>`، أو `<ToolBar>` بعده.
- `<Section>`: تقسيم القائمة، لا يمكن وجود `<Hook>، <MenuBar>، <Section>` في الطريق الخلفي.
- `<Separator>`: فاصل القائمة، لا يمكن أن يحتوي المسار التالي على `<Hook>، <MenuBar>`
- `<SubMenu>`: قائمة فرعية، لا يمكن أن تحتوي المسارات التالية على `<Hook>, <MenuBar>`
- `<Command>`: أمر القائمة، ولا يمكن أن يتبعه أي مسار.
- `<Widget>`: مكون واجهة مستخدم Slate الحديث والقابل للتوسيع بشكل مخصص، دون وجود مسارات معينة بعده

مسار شكل أبسط: `/BarName/SubMenuName1/SubMenuName2/CommandName`، إذا لم يتم تحديد النوع، فإن المسار الافتراضي الأول هو `<MenuBar>`، والتي في المنتصف هي `<SubMenu>`، والأخير هو `<Command>`.

إذا لم يتم تحديد `<Hook>` ، فسيتم إضافة `<Hook>Help` تلقائيًا في البداية لتمثيل إضافة شريط القائمة بعد قائمة المساعدة.

###أسلوب التجسيد

طريقة المسار هي تلقائيًا إنشاء جميع العقد حسب النوع والمعلمات الافتراضية، ويمكننا أيضًا التحكم في عملية الإنشاء بأنفسنا، مما يتيح لنا التحكم بشكل أكثر دقة في محتوى التوسيع.

```cpp
EP_NEW_MENU(FEditorPlusMenuBar)("MyBar", "MyBar", LOCTEXT("MyBar", "MyBar"), LOCTEXT("MyBarTips", "MyBarTips"))
->RegisterPath()
->Content({
    EP_NEW_MENU(FEditorPlusSubMenu)("MySubMenu")
    ->Content({
        EP_NEW_MENU(FEditorPlusCommand)("MyAction")
        ->BindAction(FExecuteAction::CreateLambda([]
            {
                // do action
            })),
    })
});
```

عند تثبيت `MyBar` ، يمكن تمرير اسم الخطاف، الاسم المحلي، ومعاملات الإرشاد المحلية (`"MyBar", LOCTEXT("MyBar", "MyBar"), LOCTEXT("MyBarTips", "MyBarTips")`). الرمز أعلاه يعتبر ما يعادل الطريق `/<Hook>Help/<MenuBar>MyBar/<SubMenu>MySubMenu/<Command>MyAction`.

###طريقة المزج

بالطبع يمكن استخدام الطريقتين معًا:

```cpp
FEditorPlusPath::RegisterPath(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action",
    EP_NEW_MENU(FEditorPlusCommand)("Action")
    ->BindAction(FExecuteAction::CreateLambda([]
        {
            // do action
        })),
);
```

في هذه الحالة، ستقوم الوصلة التكميلية بتحويل العقد الوسيطة تلقائيًا، وسيتم استخدام العقد الذي قام المستخدم بتحويله للعقد النهائي.

###مزيد من الأمثلة

رأس الملف:

```cpp
#include <EditorPlusPath.h>
```

تحديد اللغة المحلية عن طريق المسار، `EP_FNAME_HOOK_AUTO` يشير إلى استخدام اسم المسار تلقائيًا كاسم "Hook"،

```cpp
FEditorPlusPath::RegisterPathAction(
        "/Bar/Action",
        FExecuteAction::CreateLambda([]
        {
            // do action
        }),
        EP_FNAME_HOOK_AUTO,
        LOCTEXT("Action", "Action"),
        LOCTEXT("ActionTips", "ActionTips"));
```

من خلال المسار الحصول على العقدة وتعيين النص المحلي:

```cpp
FEditorPlusPath::GetNodeByPath("/MenuTest")
    ->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))
    ->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
```


قم بإضافة عنصر تحكم Slate UI إلى نهاية المسار

```cpp
FEditorPlusPath::RegisterPath(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Widget>Widget",
    EP_NEW_MENU(FEditorPlusWidget)("Widget", LOCTEXT("Widget", "Widget"))
        ->BindWidget(SNew(SHorizontalBox)));
);
```

أضف معلومات جديدة إلى الخطاف الذي توفره الوحدة النمطية في منطقة الشرق الأوسط.

```cpp
FEditorPlusPath::RegisterPath("<Hook>EpicGamesHelp/<Separator>ExtendSeparator")
```

تم التعرف على نفس المسار عند التصريح به عدة مرات كأنه نفس المسار، مما يسمح بالتوسع المستمر لنفس المسار.

```cpp
FEditorPlusPath::RegisterPathAction("/MenuTest/SubMenu1/SubMenu1/Path1", Action, EP_FNAME_HOOK_AUTO, LOCTEXT("Path1", "Path1"), LOCTEXT("Path1Tips", "Path1Tips"));
FEditorPlusPath::RegisterPathAction("/MenuTest/SubMenu1/SubMenu1/Path2", Action, EP_FNAME_HOOK_AUTO, LOCTEXT("Path2", "Path2"), LOCTEXT("Path2Tips", "Path2Tips"));
```

لتمديد المسار لعقدة معينة

```cpp
auto node = FEditorPlusPath::GetNodeByPath("/MenuTest");
FEditorPlusPath::RegisterChildPath(node, "<SubMenu>Sub/<Separator>Sep");
```

مسح مسار

```cpp
FEditorPlusPath::UnregisterPath("/MenuTest/SubMenu1/SubMenu1/Path1");
```

شريط أدوات التوسيع
```cpp
FEditorPlusPath::RegisterPath("/<Hook>ProjectSettings/<ToolBar>MenuTestToolBar")
->Content({
    EP_NEW_MENU(FEditorPlusCommand)("ToolBarCommand1")
    ->BindAction(...)
});
```

###واجهة الشرح

```cpp
class EDITORPLUS_API FEditorPlusPath
{
public:

	static TSharedPtr<FEditorPlusMenuBase> RegisterPath(const FString& Path, const TSharedPtr<FEditorPlusMenuBase>& Menu=nullptr);
	static TSharedPtr<FEditorPlusMenuBase> RegisterPath(const FString& Path, const FText& FriendlyName, const FText& FriendlyTips);
	static TSharedPtr<FEditorPlusMenuBase> RegisterPathAction(
		const FString& Path, const FExecuteAction& ExecuteAction, const FName& Hook=EP_FNAME_HOOK_AUTO,
		const FText& FriendlyName=FText::GetEmpty(), const FText& FriendlyTips=FText::GetEmpty());

	static TSharedPtr<FEditorPlusMenuBase> RegisterChildPath(
		const TSharedRef<FEditorPlusMenuBase>& InParent, const FString& Path, const TSharedPtr<FEditorPlusMenuBase>& Menu=nullptr);
	static TSharedPtr<FEditorPlusMenuBase> RegisterChildPath(
		const TSharedRef<FEditorPlusMenuBase>& InParent, const FString& Path, const FText& FriendlyName, const FText& FriendlyTips);
	static TSharedPtr<FEditorPlusMenuBase> RegisterChildPathAction(
		const TSharedRef<FEditorPlusMenuBase>& InParent, const FString& Path, const FExecuteAction& ExecuteAction,
		const FName& Hook=EP_FNAME_HOOK_AUTO, const FText& FriendlyName=FText::GetEmpty(), const FText& FriendlyTips=FText::GetEmpty());

	static bool UnregisterPath(
		const FString& Path, const TSharedPtr<FEditorPlusMenuBase>& Leaf=nullptr);

	static TSharedPtr<FEditorPlusMenuBase> GetNodeByPath(const FString& Path);
};
```

`RegisterPath`: إنشاء قائمة مسار
- `RegisterPathAction`：إنشاء قائمة المسار، وإجراء عملية الربط تلقائيًا لعقدة `<Command>` النهائية
- `RegisterChildPath`: لمتابعة إنشاء مسارات فرعية للعقدة المحددة
`RegisterChildPathAction`: إنشاء مسارات فرعية للعقد المحدد وربط الإجراء تلقائيا
حذف المسار، `Leaf`، عندما يكون هناك عدة أجزاء نهائية بنفس الاسم، يمكن تحديد الانطباق الصارم. خلال عملية الحذف، سيتم التتبع الى الوراء للوصول الى القوقعود، و سيتم حذفه في حال لم يحتوي على أي عقد فرعية.
- `GetNodeByPath`: الحصول على العقدة بناءً على المسار


نوع العقدة

```cpp
// base class of all node
class EDITORPLUS_API FEditorPlusMenuBase: public TSharedFromThis<FEditorPlusMenuBase> {}

class EDITORPLUS_API FEditorPlusHook: public TEditorPlusMenuBaseRoot {}

class EDITORPLUS_API FEditorPlusMenuBar: public TEditorPlusMenuBaseNode {}

class EDITORPLUS_API FEditorPlusToolBar: public TEditorPlusMenuBaseNode {}

class EDITORPLUS_API FEditorPlusSection: public TEditorPlusMenuBaseNode {}

class EDITORPLUS_API FEditorPlusSeparator: public TEditorPlusMenuBaseNode{}

class EDITORPLUS_API FEditorPlusSubMenu: public TEditorPlusMenuBaseNode {}

class EDITORPLUS_API FEditorPlusCommand: public TEditorPlusMenuBaseLeaf {}

class EDITORPLUS_API FEditorPlusWidget: public TEditorPlusMenuBaseLeaf {}
```

لمزيد من الأمثلة وشرح الواجهات، يرجى الرجوع إلى الشيفرة المصدرية [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)，حالات الاختبار [MenuTest.cpp](https://github.com/disenone/UE.EditorPlus/blob/ue5.3/Source/EditorPlusTools/Private/MenuTest/MenuTest.cpp)


###الإدارة القائمة على الوحدات

UE.EditorPlus يوفر أيضًا إطارًا لإدارة قائمة التوسيع بشكل مُعَدّل، يدعم تحميل وإلغاء تحميل الإضافات تلقائيًا عند تحميل وإلغاء تحميل القائمة الموسعة.

دع الفئة القائمة ترث `IEditorPlusToolInterface`، وتتجاوز دالة `OnStartup` ودالة `OnShutdown`. `OnStartup` مسؤولة عن إنشاء القائمة، و`OnShutdown` مسؤولة عن استدعاء دالة `Destroy` الخاصة بالعقدة لتنظيف القائمة. إذا كانت إشارة العقدة الواحدة 0، فسيتم تنفيذ التنظيف التلقائي.

```cpp
class FMenuTest: public IEditorPlusToolInterface
{
public:
	virtual void OnStartup() override;
	virtual void OnShutdown() override;
}

void FMenuTest::OnStartup()
{
	BuildPathMenu();
	BuildCustomMenu();
	BuildMixMenu();
	BuildExtendMenu();
}

void FMenuTest::OnShutdown()
{
	for(auto Menu: Menus)
	{
		if(Menu.IsValid()) Menu->Destroy();
	}
	Menus.Empty();
}
```

الصف الذي يدير القوائم يرث من واجهة `IEditorPlusToolManagerInterface`، ويعيد تنفيذ الدالة `AddTools`، ويضيف فئة القوائم في داخل `AddTools`.

```cpp
class FEditorPlusToolsImpl: public IEditorPlusToolManagerInterface
{
public:
	virtual void AddTools() override;
}

void FEditorPlusToolsImpl::AddTools()
{
	if (!Tools.Num())
	{
		Tools.Emplace(MakeShared<FMenuTest>());
	}

}
```

عند تحميل وإلغاء تحميل الإضافات، يتم استدعاء دوال التشغيل `StartupTools` و `ShutdownTools` للفئة الإدارية.

```cpp
void FEditorPlusToolsModule::StartupModule()
{
	Impl = FEditorPlusToolsImpl::Get();
	Impl->StartupTools();

}
void FEditorPlusToolsModule::ShutdownModule()
{
	Impl->ShutdownTools();
}
```

بمجرد الانتهاء من التعديل أعلاه، يمكن تحميل وإلغاء تحميل قائمة التمديد تلقائيًا عند تحميل وإلغاء تحميل الإضافات.


##أدوات المحرر

يوفر UE.EditorPlus أيضًا بعض أدوات التحرير المفيدة.

##إنشاء نافذة المحرر

باستخدام EditorPlus، يمكنك بسهولة إنشاء نافذة محرر جديدة.

```cpp
// register spawn tab
Tab = MakeShared<FEditorPlusTab>(LOCTEXT("ClassBrowser", "ClassBrowser"), LOCTEXT("ClassBrowserTip", "Open the ClassBrowser"));
Tab->Register<SClassBrowserTab>();

// register menu action to spawn tab
FEditorPlusPath::RegisterPathAction(
    "/EditorPlusTools/ClassBrowser",
    FExecuteAction::CreateSP(Tab.ToSharedRef(), &FEditorPlusTab::TryInvokeTab),
);
```

`SClassBrowserTab` هو عنصر واجهة مستخدم مخصص

```cpp
class SClassBrowserTab final : public SCompoundWidget
{
	SLATE_BEGIN_ARGS(SClassBrowserTab)
	{}
	SLATE_END_ARGS()
    // ...
}
```

### ClassBrowser

ClassBrowser هو عارض الصفوف UE ، يمكن فتحه من خلال القائمة EditorPlusTools -> ClassBrowser

![](assets/img/2024-ue-editorplus/classbrowser_menu.png)

![](assets/img/2024-ue-editorplus/classbrowser.png)

الاستناد إلى الانعكاسات في UE، يمكن عرض معلومات الأعضاء من أنواع مختلفة في UE بسهولة، بما في ذلك الإرشادات والتلميحات، ويدعم البحث الضبابي، ويمكن التنقل لفتح معلومات الفئة الأساسية.

### MenuCollections

MenuCollections هي أداة سريعة للبحث عن أوامر القائمة وتخزينها، تساعدك على العثور بسرعة على أوامر القائمة التي تحتاج إلى تنفيذها، كما يمكنك تخزين الأوامر الشائعة الاستخدام لزيادة الكفاءة.

![](assets/img/2024-ue-editorplus/menucollection_find.png)

![](assets/img/2024-ue-editorplus/menucollection_star.png)


### SlateResourceBrowser

SlateResourceBrowser هو أداة تستطيع من خلالها الاطلاع بسرعة على موارد واجهة المستخدم Slate UI، والتي يمكن أن تساعدك في تصفح والبحث عن الموارد التحريرية المطلوبة، مما يسهل توسيع المحرر.

![](assets/img/2024-ue-editorplus/slateresourcebrowser_color.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_icon.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_font.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_widgetstyle.png)

--8<-- "footer_ar.md"


> هذا المنشور تم ترجمته باستخدام ChatGPT، يرجى تقديم [**ملاحظات**](https://github.com/disenone/wiki_blog/issues/new)يرجى الإشارة إلى أي نقاط مفقودة. 
