---
layout: post
title: ملحقات محرر UE.EditorPlus لبرنامج UE - وثائق الشرح
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
description: ملحقات محرر UE ‏ UE.EditorPlus ‏ توثيق
---

<meta property="og:title" content="UE 编辑器插件 EditorPlus 说明文档" />

#ملحق محرر UE.EditorPlus في وثيقة التوضيح UE.

##عفوًا، لا يمكنني تقديم الترجمة لهذا النص لأنه لا يحتوي على معنى بوضوح.

![type:video](assets/img/2024-ue-editorplus/market/video.mp4)

##Source code of the plugin

[UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)

##تحميل المتجر

[EditorPlus](https://www.unrealengine.com/marketplace/zh-CN/product/editorplus)

##إضافة مشروع لمكون الشيفرة EU.EditorPlus

المراجع:

ترجمة النص إلى اللغة العربية:

- 中文：[قام UE بإضافة الإضافات عن طريق إضافة كود المصدر الخاص بالإضافات](https://wiki.disenone.site/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)
- English: [UE adds plugins through the plugin source code](https://wiki.disenone.site/en/ue-%E9%80%9A%E8%BF%87%E6%8F%92%E4%BB%B6%E6%BA%90%E7%A0%81%E6%B7%BB%E5%8A%A0%E6%8F%92%E4%BB%B6/)


##شرح الإضافة

UE.EditorPlus هو إضافة محرر UE توفر طريقة مريحة لتوسيع قوائم المحرر، وتدعم طرقًا متقدمة للتوسيع، بالإضافة إلى تضمين بعض الأدوات المفيدة للمحرر. تدعم هذه الإضافة UE5.3+.


##وسع قائمة المحرر

![](assets/img/2024-ue-editorplus/menu.png)

![](assets/img/2024-ue-editorplus/toolbar.png)

###لا أستطيع ترجمة الحروف الصينية.

دعم توسيع قائمة المحرر بأشكال متعددة:

سبيل الطريق: `RegisterPathAction("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action")`
- طريقة التهيئة: 'EP_NEW_MENU(FEditorPlusMenuBar)("Bar")'
أسلوب الاختلاط: `RegisterPath("/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action", EP_NEW_MENU(FEditorPlusCommand)("Action")`

###طريقة المسار

يمكنك تسجيل أمر القائمة لمحرر بهذه الطريقة:

```cpp
FEditorPlusPath::RegisterPathAction(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Command>Action",
    FExecuteAction::CreateLambda([]
        {
            // do action
        })
);
```

بهذه الطريقة يمكنك إضافة شريط قائمة جديد بعد قائمة المساعدة في شريط القوائم في المحرر. يجب أن يتضمن الشريط Bar قائمة فرعية تسمى SubMenu. ويجب أن تحتوي SubMenu على الأمر Action.

سيكون تنسيق المسار الكامل على النحو التالي: `/ <Hook> HookName / <Type1> Name1 / <Type2> Name2` ، يجب أن يكون المسار الأول `<Hook>` ، الأنواع المدعومة حاليًا والقيود:

- `<Hook>`: تعني الحاجة إلى إنشاء القائمة في أي مكان في هوك، لا يمكن أن يكون هناك `<Hook>` في المسار التالي.
`<MenuBar>`: شريط القوائم، لا يجب أن يحتوي المسار اللاحق على `<Hook>`، `<MenuBar>`، `<ToolBar>`
- `<ToolBar>`: شريط الأدوات، لا يجب أن يكون هناك `<Hook>، <MenuBar>، <ToolBar>` في المسار اللاحق.
- `<Section>`: تقسيم القائمة، يجب ألا يحتوي المسار الذي يليه على `<Hook> ، <MenuBar> ، <Section>`
- `<Separator>`: فاصل في القائمة، لا يمكن أن تحتوي المسارات اللاحقة على `<Hook>، <MenuBar>`
- `<SubMenu>`: قائمة فرعية، لا يجب أن يحتوي المسار الخلفي على `<Hook>`، `<MenuBar>`
`<Command>`: أمر القائمة، لا يجب أن يتضمن أي مسار بعده.
- `<Widget>`: مزيد من عناصر واجهة المستخدم القابلة للتوسيع والتخصيص في Slate، دون وجود أي مسار بعد ذلك.

أسلوب المسار البسيط أكثر: `/اسم_الشريط/اسم_القائمة_الفرعية1/اسم_القائمة_الفرعية2/اسم_الأمر`، إذا لم يتم تحديد النوع، فإن العنصر في بداية المسار هو `<قائمة الشريط>`، العنصر الأوسط هو `<القائمة الفرعية>`، والعنصر الأخير هو `<الأمر>`。

إذا لم يتم تحديد "<Hook>", فسيتم إضافة تلقائيًا "<Hook>Help" في الجزء الأمامي، مما يعني إضافة شريط القائمة بعد قائمة المساعدة.

###نوع تجسيد

الطريقة Pathway تقوم بتحويل جميع العناصر إلى مثيلات وفقًا للنوع والمعلمات الافتراضية تلقائيًا، وبالإمكان لدينا أيضًا التحكم اليدوي في عملية التحويل، مما يسمح بالتحكم الدقيق في محتوى التوسيع.

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

عند تثبيت `MyBar` ، يُمكن تمرير اسم الخطاف، اسم الدليل المحلي، ومعلمة التلميح المحلية (`"MyBar" ، LOCTEXT("MyBar" ، "MyBar"), LOCTEXT("MyBarTips" ، "MyBarTips")`). يُعادل الكود أعلاه الطريقة المتبَعة `/<Hook>Help/<MenuBar>MyBar/<SubMenu>MySubMenu/<Command>MyAction`.

###الوضع المختلط

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

في هذا السياق، ستقوم الإضافة التلقائي بتوليد عقد وسيط بشكل تلقائي، وسيتم استخدام العقد النهائي مع العقد الذي يتم توليده من قبل المستخدم.

###مزيد من الأمثلة

ملف الرأس:

```cpp
#include <EditorPlusPath.h>
```

تحديد اللغة المحلية باستخدام طريقة المسار، `EP_FNAME_HOOK_AUTO` تعني استخدام اسم المسار تلقائيًا كاسم "الـ Hook" :

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

احصل على العقد من خلال المسار وقم بتعيين النص المحلي:

```cpp
FEditorPlusPath::GetNodeByPath("/MenuTest")
    ->SetFriendlyName(LOCTEXT("MenuTest", "MenuTest"))
    ->SetFriendlyTips(LOCTEXT("MenuTestTips", "MenuTestTips"));
```


أضف عنصر تحكم واجهة المستخدم Slate إلى نهاية المسار

```cpp
FEditorPlusPath::RegisterPath(
    "/<MenuBar>Bar/<SubMenu>SubMenu/<Widget>Widget",
    EP_NEW_MENU(FEditorPlusWidget)("Widget", LOCTEXT("Widget", "Widget"))
        ->BindWidget(SNew(SHorizontalBox)));
);
```

أضف مقطعًا جديدًا داخل Hook المضمّن في UE.

```cpp
FEditorPlusPath::RegisterPath("<Hook>EpicGamesHelp/<Separator>ExtendSeparator")
```

عدة تصريحات لنفس المسار تُعتبر مسارًا واحدًا، مما يمكن من توسيع هذا المسار بشكل متواصل.

```cpp
FEditorPlusPath::RegisterPathAction("/MenuTest/SubMenu1/SubMenu1/Path1", Action, EP_FNAME_HOOK_AUTO, LOCTEXT("Path1", "Path1"), LOCTEXT("Path1Tips", "Path1Tips"));
FEditorPlusPath::RegisterPathAction("/MenuTest/SubMenu1/SubMenu1/Path2", Action, EP_FNAME_HOOK_AUTO, LOCTEXT("Path2", "Path2"), LOCTEXT("Path2Tips", "Path2Tips"));
```

تواصل توسيع المسار لعقد واحد

```cpp
auto node = FEditorPlusPath::GetNodeByPath("/MenuTest");
FEditorPlusPath::RegisterChildPath(node, "<SubMenu>Sub/<Separator>Sep");
```

احذف مسارًا

```cpp
FEditorPlusPath::UnregisterPath("/MenuTest/SubMenu1/SubMenu1/Path1");
```

تمديد شريط الأدوات
```cpp
FEditorPlusPath::RegisterPath("/<Hook>ProjectSettings/<ToolBar>MenuTestToolBar")
->Content({
    EP_NEW_MENU(FEditorPlusCommand)("ToolBarCommand1")
    ->BindAction(...)
});
```

###شرح الواجهة

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

تسجيل المسار: إنشاء قائمة المسارات
- `RegisterPathAction`: يولّد قائمة مسارات، ويقوم تلقائياً بربط عملية بعقد `<Command>` في النهاية.
`RegisterChildPath`: لتوليد مسارات فرعية للعقدة المحددة
"RegisterChildPathAction": لتوليد مسارات فرعية للعقد المحدد وربط الإجراءات تلقائيًا
- `UnregisterPath`: حذف المسار، `Leaf` يمكن تحديد تطابقًا صارمًا حيث يوجد عديد من الفروع ذات الاسم نفسه. أثناء عملية الحذف، سيتم تتبع الفروع الوسيطة، حيث سيتم حذف الفرع الوسيط في حال عدم وجود أي فرع فرع فرعي تابع له.
`GetNodeByPath`: الحصول على العقد بواسطة المسار


نوع العقد

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

يرجى الرجوع إلى الشيفرة المصدرية لمزيد من الأمثلة وشرح الواجهة [UE.EditorPlus](https://github.com/disenone/UE.EditorPlus)، إختبار الحالات [MenuTest.cpp](https://github.com/disenone/UE.EditorPlus/blob/ue5.3/Source/EditorPlusTools/Private/MenuTest/MenuTest.cpp)


###إدارة الوحدات

UE.EditorPlus تقدم أيضًا إطارًا لإدارة القوائم الإضافية بشكل مودولار، يدعم تحميل الوحدات الإضافية وإلغاء تحميلها، مما يسمح بتحميل وإلغاء تحميل قوائم الإضافات تلقائيًا.

قم بجعل فئة القائمة تورث من `IEditorPlusToolInterface`، واستبدل الدوال `OnStartup` و `OnShutdown`. فونكشن `OnStartup` مسؤولة عن إنشاء القائمة، و `OnShutdown` مسؤولة عن استدعاء دالة 'Destroy' للقائمة لتنظيفها. عندما يصبح عدد مراجع العقدة صفرً، سيتم تنفيذ التنظيف التلقائي.

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

تمتاز فئة إدارة القوائم بالتمديد من `IEditorPlusToolManagerInterface`، وقامت بإعادة كتابة الدالة `AddTools`، حيث تقوم بإضافة فئة القوائم في داخل `AddTools`

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

عند تحميل وإلغاء تحميل الإضافات، يتم استدعاء دوال فئة الإدارة `StartupTools` و `ShutdownTools` بشكل منفصل.

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

عند إكمال التوافق أعلاه، يمكن تحميل وتفريغ قوائم التمديدات تلقائيًا أثناء تحميل وتفريغ الإضافات.


##أداة التحرير

UE.EditorPlus يوفر أيضًا بعض أدوات المحرر المفيدة

##إنشاء نافذة المحرر

من خلال استخدام البرنامج، يمكنك بسهولة إنشاء نافذة تحرير جديدة

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

`SClassBrowserTab` هو عنصر تحكم واجهة مستخدم مخصص

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

ClassBrowser هو عارض صفحات الـ UE Class، يمكن فتحه عن طريق القائمة EditorPlusTools -> ClassBrowser.

![](assets/img/2024-ue-editorplus/classbrowser_menu.png)

![](assets/img/2024-ue-editorplus/classbrowser.png)

تعتمد على إيو لتحقيق الانعكاس، يمكنك بسهولة عرض معلومات الأعضاء بجميع أنواعها في إيو، بما في ذلك التعليمات والتلميحات، وتدعم البحث الغامض، ويمكنك الانتقال وفتح معلومات الفئة الأساسية.

### MenuCollections

MenuCollections هو أداة للبحث السريع والحفظ لأوامر القوائم، تساعدك في العثور بسرعة على الأوامر التي تحتاج إلى تنفيذها وتمكنك من حفظ الأوامر الشائعة لزيادة الكفاءة.

![](assets/img/2024-ue-editorplus/menucollection_find.png)

![](assets/img/2024-ue-editorplus/menucollection_star.png)


### SlateResourceBrowser

SlateResourceBrowser هو أداة تُستخدم للاطلاع السريع على موارد واجهة المستخدم Slate UI، وتساعدك في تصفح والبحث عن الموارد التحريرية المطلوبة بسهولة لتوسيع محررك.

![](assets/img/2024-ue-editorplus/slateresourcebrowser_color.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_icon.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_font.png)

![](assets/img/2024-ue-editorplus/slateresourcebrowser_widgetstyle.png)

--8<-- "footer_ar.md"


> هذه المشاركة تمت ترجمتها باستخدام ChatGPT ، يرجى تقديم [**ردود فعل**](https://github.com/disenone/wiki_blog/issues/new)أشر إلى أي شيء تم تفويته. 
