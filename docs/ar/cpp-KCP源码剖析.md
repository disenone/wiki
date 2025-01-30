---
layout: post
title: KCP تحليل شفرة المصدر
categories:
- c++
catalog: true
tags:
- dev
description: تناقش هذه المقالة ببساطة كود مصدر KCP، وتستعرض تنفيذ ARQ على KCP، وبعض
  الاستراتيجيات لتحسين سرعة التدفق في KCP.
figures: []
---

<meta property="og:title" content="KCP 源码剖析" />

قبل قراءة هذا المقال، إذا لم تسمع عن KCP من قبل، أو إذا كنت لا تعرف شيئًا عن KCP، يُرجى قضاء بعض الوقت في الاطلاع على وثائق مشروع KCP: [الرابط](https://github.com/skywind3000/kcp).هدف هذه المقالة هو دراسة تفاصيل تنفيذ KCP لفهم KCP بشكل أعمق.

##ما هو KCP

KCP هو بروتوكول سريع وموثوق، قادر على نقل البيانات بحد أدنى من الكمون مقارنة بـ TCP، حيث يتم إعادة إرسال البيانات بشكل أسرع وتكون فترات الانتظار أقصر.

> TCP تم تصميمه لحركة المرور (كم من البيانات يمكن نقلها في الثانية)، حيث يهتم بالاستفادة الكاملة من النطاق الترددي. بينما تم تصميم KCP لسرعة التدفق (كم من الوقت يحتاج الحزمة الواحدة للوصول من طرف إلى طرف)، مما يتيح زيادة سرعة النقل بنسبة 30%-40% على حساب استهلاك 10%-20% إضافي في النطاق الترددي. تعتبر قناة TCP قناة بنهج بطيء لكن مع تدفق بيانات كبير في الثانية، بينما تعبر KCP عن جدولة مائية صغيرة تتدفق بسرعة.

هذا ما هو مكتوب في وثائق KCP ، الكلمات الرئيسية هي **عرض النطاق الترددي** و **سرعة التدفق** ، سيؤدي KCP إلى فقدان عرض النطاق الترددي، والفائدة الناتجة هي سرعة نقل أكبر وأكثر توازنًا. لمزيد من التوضيح، يُرجى الرجوع إلى وثائق KCP ذاتها.

##هياكل بيانات KCP

كود KCP المصدر موجود في `ikcp.h` و `ikcp.c`، حيث تحتوي `ikcp.h` على إعلانات هياكل البيانات الأساسية، وأولاً يتم تعريف حزمة `SEGMENT`، وهي الحد الأدنى من وحدات البيانات التي يعالجها بروتوكول KCP:

<details>
<summary> تقسيم الهيكل (انقر لعرض الكود) </summary>
```cpp
//=====================================================================
// قطعة (segment) هي ببساطة حزمة بيانات واحدة
//=====================================================================
struct IKCPSEG
{
// عقدة القائمة المرتبطة، كلا من قائمة الإرسال والاستقبال هي هيكل القائمة المرتبطة هنا
    struct IQUEUEHEAD node;

رقم المحادثة، يكون نفس رقم المحادثة لنفس الجلسة
    IUINT32 conv;

// نوع数据包，例如 DATA 或 ACK
    IUINT32 cmd;

// بسبب قيود MTU، فإن حزم البيانات الكبيرة يتم تقسيمها إلى عدة حزم بيانات صغيرة، وهذا هو رقم الحزمة الصغيرة.
    IUINT32 frg

كل حزمة بيانات ستحمل معها حجم نافذة الاستلام الخاصة بالمُرسِل.
    IUINT32 wnd;

// وقت الإرسال، إذا كانت الحزمة ACK، ستُضبط على ts لحزمة المصدر
    IUINT32 ts;

// الرقم الذي يميز حزمة البيانات
    IUINT32 sn;

// تمثل جميع حزم البيانات التي أقل من una تم استلامها بنجاح ، وهذا معناه متطابق مع TCP: أقدم رقم تسلسل لم يتم الاعتراف به SND
    IUINT32 una;

// طول البيانات
    IUINT32 len;

// زمن إعادة الإرسال عند انتهاء المهلة
    IUINT32 resendts;

// مدة الانتظار للوقت المستنفد في المرة القادمة
    IUINT32 rto;

إعادة الإرسال السريع، عدد الحزم البيانات التي تم استلامها بعد هذه الحزمة، إذا تجاوزت قيمة معينة يتم تنشيط إعادة الإرسال السريع.
    IUINT32 fastack;

عدد المرات المرسلة
    IUINT32 xmit;

// البيانات
    char data[1];
};
```
</details>

بعد قراءة تعليق `SEGMENT`، يمكن بشكل عام ملاحظة أن أساس KCP هو أيضا بروتوكول ARQ، حيث يتم ضمان تسليم البيانات من خلال إعادة الإرسال التلقائي بعد فترة من الزمن. الآن دعنا نلقي نظرة على تعريف هيكل KCP `KCPCB`.

<details>
<summary> هيكل KCP (انقر لتوسيع الرمز) </summary>
```cpp
//---------------------------------------------------------------------
// IKCPCB
//---------------------------------------------------------------------
struct IKCPCB
{
// conv: رقم المحادثة
مترجم، مشغل: أقصى وحدة نقل، أقصى حجم لقطعة الرسالة
// state: حالة الجلسة، 0 صالحة، -1 مفصولة
    IUINT32 conv, mtu, mss, state;

// snd_una: انتظار رقم حزمة ACK
// snd_nxt: رقم حزمة البيانات التالية في انتظار الإرسال
// rcv_nxt: الحزمة التالية المنتظر استقبالها من البيانات
    IUINT32 snd_una, snd_nxt, rcv_nxt;

// ts_recent, ts_lastack: غير مستخدم
// ssthresh: عتبة بدء التباطؤ لضبط الازدحام
    IUINT32 ts_recent, ts_lastack, ssthresh;

// rx_rto: rto (توقيت إعادة الإرسال)، وقت إعادة الإرسال عند انتهاء المهلة
// rx_rttval, rx_srtt, rx_minrto: حساب المتغيرات الوسيطة لـ rto
    IINT32 rx_rttval, rx_srtt, rx_rto, rx_minrto;

// snd_wnd، rcv_wnd: حجم أقصى لنافذة الإرسال والاستقبال
// rmt_wnd: remote wnd ، حجم نافذة الاستقبال المتبقي للجهة البعيدة
// cwnd: الحجم القابل للإرسال
// استفسار: هل يجب إرسال علامة لرسالة التحكم؟
    IUINT32 snd_wnd, rcv_wnd, rmt_wnd, cwnd, probe;

// الوقت الحالي: الوقت الحالي
// interval: فترة التحديث
// ts_flush: الوقت القادم الذي يحتاج إلى التحديث
// xmit: عدد مرات فشل الإرسال
    IUINT32 current, interval, ts_flush, xmit;

// طول القائمة المرتبطة
    IUINT32 nrcv_buf, nsnd_buf;
    IUINT32 nrcv_que, nsnd_que;

// nodelay: التحكم في سرعة زيادة rto لإعادة الإرسال عند انتهاء المهلة
// updated: هل تم استدعاء ikcp_update سابقًا
    IUINT32 nodelay, updated;

// ts_probe, probe_wait: عندما تكون نافذة استلام الطرف الآخر 0 لفترة طويلة، يتم بدء الاستفسار بشكل دوري.
    IUINT32 ts_probe, probe_wait;

deal_link: الجانب الآخر غير مستجيب لفترة طويلة
// incr: تزيد: يشارك في حساب حجم نافذة الإرسال
    IUINT32 dead_link, incr;

// queue: حزم البيانات التي تتواصل مع طبقة المستخدم
// buf: حزمة البيانات المخزنة في البروتوكول
    struct IQUEUEHEAD snd_queue;
    struct IQUEUEHEAD rcv_queue;
    struct IQUEUEHEAD snd_buf;
    struct IQUEUEHEAD rcv_buf;

حتماً، سأقوم بترجمة المحتوى إلى اللغة العربية.
    IUINT32 *acklist;

// عدد الحزم المطلوبة التي تحتاج إلى تأكيد الاستلام
    IUINT32 ackcount;

// حجم الذاكرة في القائمة
    IUINT32 ackblock;

// بيانات تم تمريرها من مستوى المستخدم
    void *user;

// مكان لتخزين حزمة kcp
    char *buffer;

// عدد المرات التي تم فيها تفعيل إعادة النقل السريع (fastack)
    int fastresend;

عدد أقصى لإعادة النقل السريع
    int fastlimit;

// nocwnd: لا تأخذ في اعتبارك حجم نافذة الإرسال في بداية التشغيل البطيء
// stream: وضع التدفق
    int nocwnd, stream;

    // debug log
    int logmask;

// واجهة إرسال البيانات
    int (*output)(const char *buf, int len, struct IKCPCB *kcp, void *user);

    void (*writelog)(const char *log, struct IKCPCB *kcp, void *user);
};
```
</details>

قم بتعليق حقول البيانات داخل هيكلية KCP بتسلسل، يمكن أن نشعر بأن نظام بروتوكول KCP ليس معقدًا جدا بشكل أولي. من خلال تحليل الشيفرة بدقة، يمكن لك ولي أيضاً قراءة وفهم بروتوكول KCP :smile:

##تنفيذ ARQ من KCP

يعد KCP أساسًا بروتوكول ARQ (Auto Repeat-reQuest ، الطلب التكراري التلقائي) ، والهدف الأساسي هو ضمان النقل الموثوق به. لذا يمكننا البدء أولًا بالتركيز على جزء ARQ الأساسي لـ KCP ، وكيفية تحقيق النقل الموثوق به.

ARQ كما يوحي الاسم، عندما نعتقد أن الجهة الأخرى قد فشلت في استلام حزمة البيانات، يتم إعادة إرسال الحزمة المقابلة تلقائيًا. يتم ذلك من خلال آليتين هما التأكيد على الاستلام وإعادة الإرسال عند انتهاء المهلة، لتحقيق النقل الموثوق. في الكود الفعلي، يخصص KCP معرفًا فريدًا (`sn`) لكل حزمة بيانات (المعروفة بـ `SEGMENT` في القسم السابق)، وبمجرد استلام الجهة الأخرى لحزمة البيانات، سترد بحزمة ACK (وهي أيضًا `SEGMENT`)، ويكون `sn` لحزمة ACK مطابقًا لـ `sn` للحزمة المستلمة، مما يُعلِم بأن هذه الحزمة قد تم استلامها بنجاح. يحتوي `SEGMENT` أيضًا على حقل `una`، الذي يمثل رقم الحزمة التالية المتوقع استلامها، بمعنى أن جميع الحزم التي تحمل أرقامًا قبل هذا الرقم قد تم استلامها بالكامل، مما يعادل حزمة ACK شاملة، حيث يمكن للجهة المرسلة تحديث مؤقت الإرسال ونافذة الإرسال بشكل أسرع.

يمكننا من خلال تتبع كود إرسال واستقبال حزمة KCP أن نفهم أبسط تطبيق لـ ARQ:

###إرسال

يتكون العملية من `ikcp_send` -> `ikcp_update` -> `ikcp_output`، يقوم الطبقة العليا باستدعاء `ikcp_send` لتسليم البيانات إلى KCP، حيث يتم معالجة إرسال البيانات في `ikcp_update`.

<details>
<summary> ikcp_send(انقر لعرض الكود) </summary>
```cpp
//---------------------------------------------------------------------
واجهة إرسال البيانات، حيث يُستدعى المستخدم ikcp_send لإرسال البيانات عبر kcp
// user/upper level send, returns below zero for error
//---------------------------------------------------------------------
int ikcp_send(ikcpcb *kcp, const char *buffer, int len)
{
    IKCPSEG *seg;
    int count, i;

// mss لا يمكن أن تكون أقل من 1
    assert(kcp->mss > 0);
    if (len < 0) return -1;

    // append to previous segment in streaming mode (if possible)
    if (kcp->stream != 0) {
// معالجة وضع التدفق
        // ......
    }

// حساب الحزمة الفرعية، إذا كانت طول البيانات len أكبر من المss، فيجب تقسيمها إلى عدة حزم للإرسال، ويتعين على الطرف الآخر جمعها بعد الاستلام
    if (len <= (int)kcp->mss) count = 1;
    else count = (len + kcp->mss - 1) / kcp->mss;

    if (count >= (int)IKCP_WND_RCV) return -2;

    if (count == 0) count = 1;

// تقسيم
    for (i = 0; i < count; i++) {
حساب طول بيانات الحزمة، وتخصيص هيكل seg المقابل
        int size = len > (int)kcp->mss ? (int)kcp->mss : len;
        seg = ikcp_segment_new(kcp, size);
        assert(seg);
        if (seg == NULL) {
            return -2;
        }

قم بتعيين معلومات البيانات لـ seg ، حيث يُمثل frg رقم الحزمة المقسمة
        if (buffer && len > 0) {
            memcpy(seg->data, buffer, size);
        }
        seg->len = size;
        seg->frg = (kcp->stream == 0)? (count - i - 1) : 0;

// إضافة إلى نهاية snd_queue، وزيادة nsnd_qua بمقدار واحد
        iqueue_init(&seg->node);
        iqueue_add_tail(&seg->node, &kcp->snd_queue);
        kcp->nsnd_que++;
        if (buffer) {
            buffer += size;
        }
        len -= size;
    }

    return 0;
}
```
</details>

`ikcp_send` هو واجهة إرسال تُستدعى من الطبقة العلوية لبروتوكول KCP، حيث يجب على جميع البيانات التي يتم إرسالها عبر KCP أن تمر عبر هذه الواجهة. يقوم `ikcp_send` بعمل بسيط جدًا، حيث يقسم البيانات إلى حزم متعددة بناءً على `kcp->mss` (أقصى طول بيانات للحزمة) ويعين رقم تسلسلي لكل حزمة، ثم يُضاف في نهاية قائمة الإرسال `snd_queue`. الوضع التدفقي هو أن يُعامل البيانات المُرسلة عبر `ikcp_send` متتالية باعتبارها تدفقًا، حيث يتم ملء الأقسام غير الممتلئة أوتوماتيكيًا أولاً ثم تُخصص أقسام جديدة. لا نتحدث في هذا المقال عن تفاصيل التنفيذ، ولكن من المؤكد أنه بعد قراءة هذا المقال والنظر في الشفرة المصدرية، ستتمكن من فهمه بشكل أفضل.

بعد اكتمال استدعاء `ikcp_send`، يتم وضع البيانات في `snd_queue` الخاصة بـ KCP، لذا يحتاج KCP بعد ذلك إلى إيجاد فرصة لإرسال البيانات التي تنتظر الإرسال، وهذه الكودات موجودة في `ikcp_update` و `ikcp_flush`:

<details>
<summary> ikcp_update（انقر لتوسيع الكود） </summary>
```cpp
//---------------------------------------------------------------------
ikcp_update هو واجهة تُستدعى بانتظام من الطبقة العليا، تُستخدم لتحديث حالة "kcp" وإرسال البيانات.
// update state (call it repeatedly, every 10ms-100ms), or you can ask 
// ikcp_check when to call it again (without ikcp_input/_send calling).
// 'current' - current timestamp in millisec. 
//---------------------------------------------------------------------
void ikcp_update(ikcpcb *kcp, IUINT32 current)
{
    IINT32 slap;

    kcp->current = current;

// ikcp_flush سيتحقق من ذلك، يجب على الطبقة العليا أن تستدعي ikcp_update قبل أن تتمكن من استدعاء ikcp_flush، يُنصح باستخدام ikcp_update فقط
    if (kcp->updated == 0) {
        kcp->updated = 1;
        kcp->ts_flush = kcp->current;
    }

    slap = _itimediff(kcp->current, kcp->ts_flush);

    if (slap >= 10000 || slap < -10000) {
        kcp->ts_flush = kcp->current;
        slap = 0;
    }

    if (slap >= 0) {
وزمن تفريغ المخزون المقبل
        kcp->ts_flush += kcp->interval;
        if (_itimediff(kcp->current, kcp->ts_flush) >= 0) {
            kcp->ts_flush = kcp->current + kcp->interval;
        }
        ikcp_flush(kcp);
    }
}
```
</details>

ترتكز مهمة `ikcp_update` على فحص وقت `ts_flush` وفي حال تحقق الشرط، يتم استدعاء `ikcp_flush`. كافة العمليات الرئيسية تتم في داخل `ikcp_flush`، حيث يركز عملنا حاليًا على الجزء المتعلق بإرسال ARQ.

<details>
<summary> إرسال البيانات (انقر لتوسيع الكود) </summary>
```cpp
//---------------------------------------------------------------------
// ikcp_flush
//---------------------------------------------------------------------
void ikcp_flush(ikcpcb *kcp)
{
    IUINT32 current = kcp->current;

// buffer هو البيانات التي سيتم تمريرها إلى ikcp_output، ويتم تهيئته ليكون ثلاثة أضعاف حجم الحزمة
    char *buffer = kcp->buffer;
    char *ptr = buffer;
    int count, size, i;
    IUINT32 resent, cwnd;
    IUINT32 rtomin;
    struct IQUEUEHEAD *p;
    int change = 0;
    int lost = 0;
    IKCPSEG seg;

    // 'ikcp_update' haven't been called.
    if (kcp->updated == 0) return;

    seg.conv = kcp->conv;
    seg.cmd = IKCP_CMD_ACK;
    seg.frg = 0;

seg.wnd هو متغير يعبر عن حجم النافذة المتاحة حاليًا.
    seg.wnd = ikcp_wnd_unused(kcp);
    seg.una = kcp->rcv_nxt;
    seg.len = 0;
    seg.sn = 0;
    seg.ts = 0;

// إرسال تأكيد (ack)
// حساب نافذة الإرسال
    //...

// نقل حزم البيانات من طابور الإرسال إلى الذاكرة المؤقتة للإرسال
التحرك يتطلب تحقيق حجم نافذة الإرسال، عندما تمتلئ نافذة الإرسال، يتوقف التحرك
البيانات الموجودة في snd_buf هي البيانات التي يمكن إرسالها مباشرة إلى الطرف الآخر عن طريق استدعاء ikcp_output.
    while (_itimediff(kcp->snd_nxt, kcp->snd_una + cwnd) < 0) {
        IKCPSEG *newseg;
        if (iqueue_is_empty(&kcp->snd_queue)) break;

        newseg = iqueue_entry(kcp->snd_queue.next, IKCPSEG, node);

        iqueue_del(&newseg->node);
        iqueue_add_tail(&newseg->node, &kcp->snd_buf);
        kcp->nsnd_que--;
        kcp->nsnd_buf++;

        newseg->conv = kcp->conv;
        newseg->cmd = IKCP_CMD_PUSH;
        newseg->wnd = seg.wnd;
        newseg->ts = current;

// seg رقم تسلسلي فريد، في الواقع هو kcp->snd_nxt المتزايد.
        newseg->sn = kcp->snd_nxt++;

قم بضبط una هنا، وأبلغ الجهة الأخرى برقم التسلسل للحزمة المنتظرة التالية لاستقبالها
        newseg->una = kcp->rcv_nxt;
        newseg->resendts = current;
        newseg->rto = kcp->rx_rto;
        newseg->fastack = 0;
        newseg->xmit = 0;
    }

// حساب علامة الإعادة السريعة، وقت الانتظار في حالة المهلة
    // ...

// إرسال snd_buf
    for (p = kcp->snd_buf.next; p != &kcp->snd_buf; p = p->next) {
        IKCPSEG *segment = iqueue_entry(p, IKCPSEG, node);
        int needsend = 0;
        if (segment->xmit == 0) {
            // الإرسال لأول مرة
// set->xmit تشير إلى عدد الارسالات
// resendts وقت الانتظار لإعادة الإرسال بعد انتهاء المهلة
            needsend = 1;
            segment->xmit++;
            segment->rto = kcp->rx_rto;
            segment->resendts = current + segment->rto + rtomin;
        }
        else if (_itimediff(current, segment->resendts) >= 0) {
            // إعادة الإرسال بعد انتهاء المهلة
            // ...
        }
        else if (segment->fastack >= resent) {
// إعادة النقل السريع
            // ...
        }

        if (needsend) {
            int need;
            segment->ts = current;
            segment->wnd = seg.wnd;
            segment->una = kcp->rcv_nxt;

            size = (int)(ptr - buffer);
            need = IKCP_OVERHEAD + segment->len;

// كلما زادت البيانات في الذاكرة المؤقتة عن mtu، يجب إرسالها أولاً، لتجنب تقسيم الحزم في الطبقة السفلية قدر الإمكان.
            if (size + need > (int)kcp->mtu) {
                ikcp_output(kcp, buffer, size);
                ptr = buffer;
            }

قم بنسخ بيانات التحكم seg إلى الذاكرة buffer ، حيث يتولى الخوارزمية kcp معالجة مشكلة ترتيب البايتات بطريقتها الخاصة.
            ptr = ikcp_encode_seg(ptr, segment);

// إعادة نسخ البيانات
            if (segment->len > 0) {
                memcpy(ptr, segment->data, segment->len);
                ptr += segment->len;
            }


            if (segment->xmit >= kcp->dead_link) {
                kcp->state = (IUINT32)-1;
            }
        }
    }

    // flash remain segments
    size = (int)(ptr - buffer);
    if (size > 0) {
        ikcp_output(kcp, buffer, size);
    }

// حساب ssthresh، تحديث نافذة البدء البطيء
    // ...
}
```
</details>

نحن حاليًا نركز فقط على المنطق المتعلق بإرسال البيانات داخل `ikcp_flush`:

* أولاً، ستقوم KCP بنقل البيانات الموجودة في `snd_queue` إلى `snd_buf` بناءً على حجم نافذة الاستقبال في الطرف الآخر. الصيغة المستخدمة لحساب كمية النقل هي `num = snd_nxt - (snd_una + cwnd)`، مما يعني: أن أكبر رقم حزمة تم إرسالها بنجاح `snd_una` زائد حجم النافذة المنزلقة `cwnd` أكبر من رقم الحزمة التالية المراد إرسالها `snd_nxt`، لذا يمكن متابعة إرسال حزم بيانات جديدة. أثناء نقل `SEG`، يتم ضبط حقول التحكم.

انتقل عبر `snd_buf`، وإذا كان هناك حاجة لإرسال حزمة بيانات، قُم بنسخ البيانات إلى `buffer`، مع معالجة مشكلة ترتيب بتات البيانات لحقول التحكم باستخدام `ikcp_encode_seg`.

* أخيرًا، قم باستدعاء `ikcp_output` لإرسال البيانات الموجودة على `buffer`.

بهذا، أكملت KCP إرسال البيانات.

###接收

عملية接收与发送相反：`ikcp_input` -> `ikcp_update` -> `ikcp_recv`。用户在收到网络上的数据后，需要调用 `ikcp_input` 将其传递给 KCP 进行解析。在调用 `ikcp_update` 时，会向发送端回复 ACK 包，上层通过调用 `ikcp_recv` 来接收 KCP 解析后的数据。

<details>
<summary> استقبال البيانات (اضغط لتوسيع الكود) </summary>
```cpp
//---------------------------------------------------------------------
// input data
//---------------------------------------------------------------------
int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    IUINT32 prev_una = kcp->snd_una;
    IUINT32 maxack = 0, latest_ts = 0;
    int flag = 0;

// فحص الشرعية
    if (data == NULL || (int)size < (int)IKCP_OVERHEAD) return -1;

// البيانات قد تكون عدة حزم KCP، يتم التعامل معها بشكل دوري
    while (1) {
        IUINT32 ts, sn, len, una, conv;
        IUINT16 wnd;
        IUINT8 cmd, frg;
        IKCPSEG *seg;

// غير كافٍ لحزمة KCP واحدة، الخروج
        if (size < (int)IKCP_OVERHEAD) break;

قم أولاً بتحليل الحقول التحكمية.
        data = ikcp_decode32u(data, &conv);
        if (conv != kcp->conv) return -1;

        data = ikcp_decode8u(data, &cmd);
        data = ikcp_decode8u(data, &frg);
        data = ikcp_decode16u(data, &wnd);
        data = ikcp_decode32u(data, &ts);
        data = ikcp_decode32u(data, &sn);
        data = ikcp_decode32u(data, &una);
        data = ikcp_decode32u(data, &len);

        size -= IKCP_OVERHEAD;

        if ((long)size < (long)len || (int)len < 0) return -2;

فحص نوع حزمة البيانات
        if (cmd != IKCP_CMD_PUSH && cmd != IKCP_CMD_ACK &&
            cmd != IKCP_CMD_WASK && cmd != IKCP_CMD_WINS) 
            return -3;

        kcp->rmt_wnd = wnd;

// هنا una هي kcp->rcv_nxt للمرسل، بناءً على هذه البيانات، يمكن التخلص من الحزم التي تم تأكيد استلامها.
        ikcp_parse_una(kcp, una);
// بعد إزالة الحزم التي تم تأكيد استلامها، يتم تحديث snd_una للرقم التسلسلي التالي المراد إرساله
        ikcp_shrink_buf(kcp);

        if (cmd == IKCP_CMD_ACK) {
// حزمة ack
            // ...
        }
        else if (cmd == IKCP_CMD_PUSH) {
// حزمة البيانات
// إذا كان رقم حزمة البيانات المستلمة sn ضمن نافذة الاستقبال، فسيتم معالجته بشكل طبيعي، وإلا سيتم تجاهله مباشرة في انتظار إعادة الإرسال.
            if (_itimediff(sn, kcp->rcv_nxt + kcp->rcv_wnd) < 0) {

// يجب أن يتم إرسال حزمة ack لكل حزمة بيانات تم استلامها، وتسجيلها
                ikcp_ack_push(kcp, sn, ts);

// يتم استدعاء ikcp_parse_data لمعالجة البيانات المستلمة
                if (_itimediff(sn, kcp->rcv_nxt) >= 0) {
                    seg = ikcp_segment_new(kcp, len);
                    seg->conv = conv;
                    seg->cmd = cmd;
                    seg->frg = frg;
                    seg->wnd = wnd;
                    seg->ts = ts;
                    seg->sn = sn;
                    seg->una = una;
                    seg->len = len;

                    if (len > 0) {
                        memcpy(seg->data, data, len);
                    }

                    ikcp_parse_data(kcp, seg);
                }
            }
        }
        else if (cmd == IKCP_CMD_WASK) {
// حزمة نافذة الاستعلام
            // ...
        }
        else if (cmd == IKCP_CMD_WINS) {
// حزمة الرد من نافذة الاستعلام
            // ...
        }
        else {
            return -3;
        }

        data += len;
        size -= len;
    }

// معالجة منطق إعادة الإرسال السريع
    // ...

تحديث نافذة الإرسال
    // ...

    return 0;
}
```
</details>

`ikcp_input` يقوم بمعالجة كل حزمة `SEG` بشكل دوري، حيث يبدأ بفحص صلاحية الحزمة ونوعها، لأن كل حزمة تحمل `una`، والتي تحتوي على رقم تسلسل الحزمة التي ينتظرها الطرف المرسل لاستلامها، ويجب أن تكون الحزم التي تقل عن `una` قد تم قبولها بنجاح من الطرف الآخر، لذا يمكن حذف الحزم التي تحتاج إلى أن تكون أقل من `una` من `snd_buff`، وتحديث `snd_nxt`. يتم التعامل مع هذه الجزء بواسطة `ikcp_parse_una` و `ikcp_shrink_buf`. كل حزمة البيانات المستلمة تحتاج إلى إرسال حزمة ACK، ويتم تسجيلها بواسطة `ikcp_ack_push`، وأخيرًا يتم استدعاء `ikcp_parse_data` لمعالجة البيانات.

<details>
<summary> تحليل البيانات (اضغط لتوسيع الشفرة) </summary>
```cpp
void ikcp_parse_data(ikcpcb *kcp, IKCPSEG *newseg)
{
    struct IQUEUEHEAD *p, *prev;
    IUINT32 sn = newseg->sn;
    int repeat = 0;

// التحقق من الرقم التسلسلي
    if (_itimediff(sn, kcp->rcv_nxt + kcp->rcv_wnd) >= 0 ||
        _itimediff(sn, kcp->rcv_nxt) < 0) {
        ikcp_segment_delete(kcp, newseg);
        return;
    }

// ابحث عن الموقع الذي يجب أن يوضع فيه newseg، لأن seg المستلم قد يكون في ترتيب فوضوي.
    for (p = kcp->rcv_buf.prev; p != &kcp->rcv_buf; p = prev) {
        IKCPSEG *seg = iqueue_entry(p, IKCPSEG, node);
        prev = p->prev;
        if (seg->sn == sn) {
// تكرار الاستلام
            repeat = 1;
            break;
        }
        if (_itimediff(sn, seg->sn) > 0) {
            break;
        }
    }

// ضع newseg في المكان الصحيح داخل rcv_buf
    if (repeat == 0) {
        iqueue_init(&newseg->node);
        iqueue_add(&newseg->node, p);
        kcp->nrcv_buf++;
    }    else {
        ikcp_segment_delete(kcp, newseg);
    }

نقل البيانات من rcv_buf إلى rcv_queue
    while (! iqueue_is_empty(&kcp->rcv_buf)) {
        IKCPSEG *seg = iqueue_entry(kcp->rcv_buf.next, IKCPSEG, node);
// إذا كان رقم تسلسل seg هو الرقم المُنتظر استقباله، انتقل إلى rcv_queue
        if (seg->sn == kcp->rcv_nxt && kcp->nrcv_que < kcp->rcv_wnd) {
            iqueue_del(&seg->node);
            kcp->nrcv_buf--;
            iqueue_add_tail(&seg->node, &kcp->rcv_queue);
            kcp->nrcv_que++;
            kcp->rcv_nxt++;
        }    else {
            break;
        }
    }
}
```
</details>

`ikcp_parse_data` العمل الرئيسي هو وضع `newseg` في الموقع المناسب في `kcp->rcv_buf`، ونقل البيانات من `rcv_buf` إلى `rcv_queue`. موقع `rcv_buf` المناسب يعني أن `rcv_buf` مرتبة حسب ترتيب تسلسلي لـ `sn`، ويجب على `newseg` البحث عن الموقع المناسب بناءً على قيمة `sn` الخاصة به. يجب نقل البيانات الموجودة على `rcv_buf` إلى `rcv_queue` بشرط أن يكون رقم حزمة البيانات في `rcv_buf` يساوي رقم الحزمة الذي ينتظره KCP `kcp->rcv_nxt`، وبعد نقل حزمة بيانات واحدة، يجب تحديث `kcp->rvc_nxt` ثم معالجة الحزمة التالية.

بعد `ikcp_input`، ستقوم الطبقة العليا عند استدعاء `ikcp_update` بإرسال حزمة ACK، بينما استدعاء `ikcp_recv` سيعيد البيانات الفعالة للطبقة العليا. `ikcp_update` و `ikcp_recv` مستقلان عن بعضهما، ولا توجد متطلبات لترتيب الاستدعاء، بل يعتمد ذلك على توقيت استدعاء الطبقة العليا. دعونا نلقي نظرة أولاً على الجزء المتعلق بإرسال ACK داخل `ikcp_update`:

<details>
<summary> رد ACK (انقر لعرض الكود) </summary>
```cpp
تم تحديث ذلك مسبقا، ikcp_update يستدعي في النهاية ikcp_flush.
void ikcp_flush(ikcpcb *kcp, IUINT32 current)
{
    // ...

// رد حزمة ACK
    count = kcp->ackcount;
    for (i = 0; i < count; i++) {
        size = (int)(ptr - buffer);
        if (size + (int)IKCP_OVERHEAD > (int)kcp->mtu) {
            ikcp_output(kcp, buffer, size);
            ptr = buffer;
        }
        ikcp_ack_get(kcp, i, &seg.sn, &seg.ts);
        ptr = ikcp_encode_seg(ptr, &seg);
    }

    kcp->ackcount = 0;

    // ...
}
```
</details>

تم حفظ حزمة ACK مسبقًا بواسطة `ikcp_ack_push`، لذا هنا نحتاج فقط إلى `ikcp_ack_get` للحصول على معلومات كل حزمة ACK وإرسالها للطرف الآخر. يمكن للطبقة العليا استخدام `ikcp_recv` للحصول على البيانات من KCP:

<details>
<summary> ikcp_recv（انقر لتوسيع الكود） </summary>
```cpp
//---------------------------------------------------------------------
// user/upper level recv: returns size, returns below zero for EAGAIN
//---------------------------------------------------------------------
int ikcp_recv(ikcpcb *kcp, char *buffer, int len)
{
    struct IQUEUEHEAD *p;
    int ispeek = (len < 0)? 1 : 0;
    int peeksize;
    int recover = 0;
    IKCPSEG *seg;
    assert(kcp);

// بعض فحوصات الفعالية
    if (iqueue_is_empty(&kcp->rcv_queue))
        return -1;
    if (len < 0) len = -len;

حساب طول البيانات التي يمكن إرجاعها
    peeksize = ikcp_peeksize(kcp);

    if (peeksize < 0)
        return -2;
    if (peeksize > len)
        return -3;

// التحقق من نافذة الاستقبال
    if (kcp->nrcv_que >= kcp->rcv_wnd)
        recover = 1;

تمامًا، هيا لنبدأ:

// استعراض قائمة rcv_queue، ونسخ البيانات إلى buffer
    for (len = 0, p = kcp->rcv_queue.next; p != &kcp->rcv_queue; ) {
        int fragment;
        seg = iqueue_entry(p, IKCPSEG, node);
        p = p->next;

        if (buffer) {
            memcpy(buffer, seg->data, seg->len);
            buffer += seg->len;
        }

        len += seg->len;

// تحديد الحزمة
        fragment = seg->frg;

// إزالة حزمة البيانات
        if (ispeek == 0) {
            iqueue_del(&seg->node);
            ikcp_segment_delete(kcp, seg);
            kcp->nrcv_que--;
        }

// تم نسخ جميع العقود الفرعية، خروج من الحلقة
        if (fragment == 0)
            break;
    }

    assert(len == peeksize);

// تفرغت قائمة الاستقبال (rcv_queue) قليلاً، حاول المتابعة في نقل البيانات من مخزن الاستقبال (rcv_buf) إلى قائمة الاستقبال (rcv_queue)
    while (! iqueue_is_empty(&kcp->rcv_buf)) {
        seg = iqueue_entry(kcp->rcv_buf.next, IKCPSEG, node);
        if (seg->sn == kcp->rcv_nxt && kcp->nrcv_que < kcp->rcv_wnd) {
            iqueue_del(&seg->node);
            kcp->nrcv_buf--;
            iqueue_add_tail(&seg->node, &kcp->rcv_queue);
            kcp->nrcv_que++;
            kcp->rcv_nxt++;
        }    else {
            break;
        }
    }

    return len;
}
```
</details>

`ikcp_recv` تُعيد كل استدعاء حزمة بيانات كاملة واحدة فقط، ويمكن للطبقة العليا الاستمرار في الاستدعاء حتى لا يعود هناك أي بيانات. منطق الدالة بسيط جدًا، حيث يقوم بنسخ البيانات من `rcv_queue` إلى `buffer` الذي تم تمريره من الطبقة العليا، ومن هنا يكون الطرف المتلقى قد أتم معالجة حزمة البيانات المستقبلة.

عندما يُعالج الطرف العائد حزمة البيانات، يُرسل باكت ACK إلى الطرف الإرسال، دعونا نلقي نظرة على كيفية تلقي الطرف الإرسال باكت ACK.

<details>
<summary> معالجة حزمة ACK (انقر للتوسيع على الكود) </summary>
```cpp
int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    // ...
    IUINT32 maxack = 0, latest_ts = 0;
    // ...
    while (1) {
        // ...
// ts هو kcp-> current للطرف الآخر
        data = ikcp_decode32u(data, &ts);
        data = ikcp_decode32u(data, &sn);

        if (cmd == IKCP_CMD_ACK) {
            // تحديث rot
            if (_itimediff(kcp->current, ts) >= 0) {
                ikcp_update_ack(kcp, _itimediff(kcp->current, ts));
            }
// تحديث snd_buf
            ikcp_parse_ack(kcp, sn);
            ikcp_shrink_buf(kcp);

maxack = أكبر رقم تسلسلي (sn) في كل حزم ACK لإدخال هذه المرة
            if (flag == 0) {
                flag = 1;
                maxack = sn;
                latest_ts = ts;
            }    else {
                if (_itimediff(sn, maxack) > 0) {
                #ifndef IKCP_FASTACK_CONSERVE
                    maxack = sn;
                    latest_ts = ts;
                #else
                    if (_itimediff(ts, latest_ts) > 0) {
                        maxack = sn;
                        latest_ts = ts;
                    }
                #endif
                }
            }
        }
        // ...
    }

إذا تم استلام حزمة ACK، قم بتسجيلها لاستخدامها في إعادة الارسال السريع
    if (flag != 0) {
        ikcp_parse_fastack(kcp, maxack, latest_ts);
    }
}
```
</details>

يمكن ملاحظة أنه بمجرد استلام حزمة ACK ، سيتطلب الأمر أيضًا تحديثًا لـ `snd_buf` باستخدام `ikcp_parse_ack` و `ikcp_shrink_buf` ، بالإضافة إلى استدعاء `ikcp_update_ack` لحساب تحديث rto (وقت إعادة الإرسال) . `ikcp_input` يحسب أعلى رقم متسلسل في حزمة ACK الواردة لتسجيله للاستخدام في إعادة الإرسال السريع. وهكذا، بمجرد أن يستلم الجانب الإرسالي حزمة ACK ، يتمتع بإزالة البيانات المرسلة من `snd_buf` ، حيث تصل البيانات بشكل موثوق إلى الجانب المستقبل، وبذلك ينتهي العملية الكاملة لتأكيد الاستلام في نظام الرد الآلي المتكرر.

###إعادة الإرسال بعد فوات الوقت

前面介绍的是 KCP 实现的 ARQ 中的确认接收机制，ARQ 还需要一个超时重传来保证可靠性，下面我们来看看 KCP 是怎么做超时重传的。

دعونا نعود إلى وظيفة `ikcp_flush`:

<details>
<summary> إعادة الإرسال بعد انتهاء الوقت (انقر لتوسيع الشيفرة) </summary>
```cpp
void ikcp_flush(ikcpcb *kcp)
{
    // ...
// إرسال snd_buf
    for (p = kcp->snd_buf.next; p != &kcp->snd_buf; p = p->next) {
        IKCPSEG *segment = iqueue_entry(p, IKCPSEG, node);
        int needsend = 0;
        if (segment->xmit == 0) {
// على المرة الأولى
            needsend = 1;
            segment->xmit++;
            // تعيين segment->rto
قم بحساب وقت إعادة البث الذي يتجاوز وقت الانتهاء الذاتي الخاص بـ segment->resendts عن طريق segment->rto.
            segment->rto = kcp->rx_rto;
            segment->resendts = current + segment->rto + rtomin;
        }
        else if (_itimediff(current, segment->resendts) >= 0) {
// إعادة الإرسال بعد انتهاء المهلة
            needsend = 1;
            segment->xmit++;
            kcp->xmit++;
التحكم بوقت إعادة الإرسال التالي بعد تأخير
            if (kcp->nodelay == 0) {
                segment->rto += kcp->rx_rto;
            }    else {
                segment->rto += kcp->rx_rto / 2;
            }
            segment->resendts = current + segment->rto;
            lost = 1;
        }
        else if (segment->fastack >= resent) {
إعادة النقل السريع
            // ...
        }
        if (needsend) {
إرسال البيانات
            // ...
        }
    // ...
}
```
</details>

بمجرد أن يكون الوقت الحالي `current` أكبر من `segment->resendts` وقت إعادة الإرسال، يعني أنه لم يتم استلام حزمة ACK من الطرف الآخر خلال هذه الفترة، مما يؤدي إلى تنشيط آلية إعادة الإرسال بعد انقضاء المهلة، `needsend = 1`، وإعادة إرسال البيانات.

مع وجود آلية تأكيد الاستلام وآلية إعادة الإرسال في حالة حدوث مهلة، يمكن لـ KCP ضمان نقل البيانات بشكل موثوق. ولكن من أجل الحفاظ على سرعة تدفق البيانات بشكل أكثر استقرارًا، قامت KCP بعدة تحسينات إضافية، دعونا نلقي نظرة على التحسينات التي قامت بها KCP.

##استراتيجية زيادة سرعة تدفق KCP

###إعادة إرسال سريعة

أرسل المرسل حزمتي بيانات برقم تسلسلي `sn` و `sn + 1`، وإذا تلقى فقط حزمة ACK لـ `sn + 1`، فقد يكون ذلك لأن حزمة ACK لـ `sn` لم تصل بعد عبر الشبكة، أو أن حزمة ACK قد فقدت، أو أن حزمة البيانات `sn` قد فقدت. إذا لم يحِن بعد وقت المهلة لإعادة الإرسال، وكانت الشبكة ليست مزدحمة بشكل كبير، فقد يكون فقدان الحزم بسبب بعض الأسباب المؤقتة. في هذه الحالة، يمكن للمرسل أن يختار إرسال حزمة البيانات `sn` بشكل مبكر، مما يساعد المستقبل على استلام البيانات بشكل أسرع وزيادة سرعة التدفق.

KCP في داخله يحقق أيضًا آلية الإعادة السريعة، وذلك أيضًا في `ikcp_flush`:

<details>
<ملخص> إعادة النقل السريع (انقر لعرض الشيفرة) </ملخص>
```cpp
void ikcp_flush(ikcpcb *kcp)
{
    // ...
    resent = (kcp->fastresend > 0)? (IUINT32)kcp->fastresend : 0xffffffff;

// إرسال snd_buf
    for (p = kcp->snd_buf.next; p != &kcp->snd_buf; p = p->next) {
        IKCPSEG *segment = iqueue_entry(p, IKCPSEG, node);
        int needsend = 0;
        if (segment->xmit == 0) {
            // ...
        }
        else if (_itimediff(current, segment->resendts) >= 0) {
            // ...
        }
        else if (segment->fastack >= resent) {
// إعادة الإرسال السريعة
            if ((int)segment->xmit <= kcp->fastlimit ||
                kcp->fastlimit <= 0) {
                needsend = 1;
                segment->xmit++;
                segment->fastack = 0;
                segment->resendts = current + segment->rto;
                change++;
            }
        }
        if (needsend) {
// إرسال البيانات
            // ...
        }
    // ...
}
```
</details>

يجب على المرسل أن يعيد الإرسال بسرعة، هناك شرطان:
* عندما `segment->fastack >= resent` يصبح `resent` معلمة قابلة للتكوين في `kcp->fastresend`، وعند تعيينها كقيمة 0، ستُعطل الإعادة السريعة. يُعين `segment->fastack` في دالة `ikcp_parse_fastack`، وهذه الدالة تُستدعى في `ikcp_input`، حيث يتم زيادة `segment->fastack` لجميع الحزم التي تكون رقم تسلسلها `sn` أقل من `maxack`، الذي يُحسب بناءً على `ikcp_input`، وبالتالي، يُمثل `segment->fastack` عدد حزم وصلت تسلسلها أكبر من `sn`.
* `segment->xmit <= kcp->fastlimit || kcp->fastlimit <= 0`، `setgment->xmit` هو عدد مرات الإرسال، و `kcp->fastlimit` هو الحد الأقصى القابل للتكوين لعدد مرات الإعادة السريعة، ويجب أن يكون عدد مرات الإرسال أقل من الحد الأقصى لعدد مرات الإعادة السريعة.

بمجرد تحقيق شروط إعادة النقل السريعة أعلاه، سيقوم KCP بتنفيذ إعادة النقل السريعة، يجب ملاحظة أن إعادة النقل السريعة لن تعيد تعيين وقت إعادة النقل مكانه، فإن الوقت الأصلي للإعادة سيظل ساري المفعول.

###تقليل زمن إعادة الإرسال في حالة انتهاء المهلة

تعتبر إعادة الإرسال عند انتهاء المهلة آلية جيدة، لكنها تستغرق وقتًا طويلاً. وفقًا لاستراتيجية TCP، يتضاعف وقت إعادة الإرسال بعد كل انتهاء مهلة، مما يؤدي إلى تضخم سريع في وقت الانتظار. خلال فترة الانتظار، قد يكون من المحتمل أن يكون نافذة الاستقبال في الطرف المستقبل قد نفدت، ولا يمكنها استقبال بيانات جديدة، بينما يكون رقم تسلسل الحزمة المعلقة في المقدمة، ولا يمكن للطرف المستقبل إعادة كل البيانات إلى الطبقة العليا حتى يستقبل حزمة إعادة الإرسال. في هذه الحالة، تكون سرعة الشبكة تقريبًا صفرًا. قامت KCP بإضافة إعدادات يمكن أن تخفف من زيادة وقت الانتظار، كما أنها لن تتضاعف. من خلال إعداد `kcp->nodelay` يمكن التحكم في زيادة وقت الانتظار ليكون فقط بمقدار ضعف RTO أو 0.5 ضعف RTO، مما يساعد في تقليل زيادة وقت الانتظار ويساعد الشبكة على استعادة سرعتها بشكل أسرع.

###تحديث نافذة الإرسال

إرسال النافذة تعبر عن عدد حزم البيانات المنقولة في نفس الوقت، كلما كانت النافذة أكبر، زادت كمية البيانات التي يتم نقلها في نفس الوقت وزادت سرعة التدفق، ولكن إذا كانت النافذة كبيرة جدًا، فقد يؤدي ذلك إلى ازدحام الشبكة، وزيادة معدل فقدان الحزم، وزيادة إعادة إرسال البيانات، مما يؤدي إلى انخفاض سرعة التدفق. لذا، يجب تحديث نافذة الإرسال باستمرار وفقًا لحالة الشبكة، لتقترب ببطء من المثالية. كود نافذة الإرسال في KCP:

<details>
<summary> نافذة الإرسال (انقر لتوسيع الشيفرة) </summary>
```cpp
ikcpcb* ikcp_create(IUINT32 conv, void *user)
{
    // ...
// snd_wnd، rcv_wnd حجم缓冲区 للإرسال والاستقبال
    kcp->snd_wnd = IKCP_WND_SND;    // 32
    kcp->rcv_wnd = IKCP_WND_RCV;    // 128
// حجم نافذة الاستقبال البعيدة              // 128
    kcp->rmt_wnd = IKCP_WND_RCV
// 初始化发送窗口 cwnd 为 0
    kcp->cwnd = 0;
// إرسال حجم البايتات في النافذة ، تشارك في حساب cwnd
    kcp->incr = 0
// حد بدء التباطؤ، slow start threshold
    kcp->ssthresh = IKCP_THRESH_INIT;
نعتذر، هذه الجملة لا يمكن ترجمتها إلى اللغة العربية بالشكل المطلوب.
    kcp->nocwnd = 0;
    // ...
}

void ikcp_flush(ikcpcb *kcp)
{
    // ...
عند إرسال البيانات، يتم حساب حجم نافذة الإرسال أولاً، وهو القيمة الصغرى بين حجم الذاكرة المؤقتة للإرسال وحجم نافذة الاستقبال للطرف الآخر.
    cwnd = _imin_(kcp->snd_wnd, kcp->rmt_wnd);
يجب أيضا أن نأخذ في الاعتبار kcp->cwnd، والذي يعتبر نافذة الإرسال المحدّثة بشكل مستمر.
    if (kcp->nocwnd == 0) cwnd = _imin_(kcp->cwnd, cwnd);

// بناءً على حجم cwnd، ينتقل snd_queue إلى snd_buf
    while (_itimediff(kcp->snd_nxt, kcp->snd_una + cwnd) < 0) {
    }
// إرسال البيانات
    resent = (kcp->fastresend > 0)? (IUINT32)kcp->fastresend : 0xffffffff;
// تفعيل إعادة الإرسال بسبب انتهاء المهلة lost = 1
// زيادة تغيير معالجة إعادة الإرسال السريع

// تحديث عتبة بدء التشغيل البطيء ونافذة الإرسال
    if (change) {
// إذا تم تفعيل الإعادة السريعة، يتم تعيين ssthresh إلى نصف عدد الحزم التي يتم نقلها عبر الشبكة.
        IUINT32 inflight = kcp->snd_nxt - kcp->snd_una;
        kcp->ssthresh = inflight / 2;
        if (kcp->ssthresh < IKCP_THRESH_MIN)
            kcp->ssthresh = IKCP_THRESH_MIN;

// يتم إعادة إرسال النافذة عندما تكون أكبر من الحد الأدنى المضبوط، بالإضافة إلى البيانات المتعلقة بالإعادة السريعة.
        kcp->cwnd = kcp->ssthresh + resent;
        kcp->incr = kcp->cwnd * kcp->mss;
    }

    if (lost) {
// إذا كان هناك إعادة إرسال بسبب مهلة، يتم تفعيل الإقلاع البطيء، و تكون عتبة ssthresh نصف حجم نافذة الإرسال.
        kcp->ssthresh = cwnd / 2;
        if (kcp->ssthresh < IKCP_THRESH_MIN)
            kcp->ssthresh = IKCP_THRESH_MIN;
// إعادة إرسال النافذة إلى 1 ، وزيادة التباطؤ من جديد
        kcp->cwnd = 1;
        kcp->incr = kcp->mss;
    }

    if (kcp->cwnd < 1) {
// لأن القيمة الأولية هي 0، ستتم إعادة ضبطها هنا إلى 1
        kcp->cwnd = 1;
        kcp->incr = kcp->mss;
    }
}

int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    IUINT32 prev_una = kcp->snd_una;
معالجة البيانات المستلمة

    while (1) {
        // ...
        data = ikcp_decode16u(data, &wnd)
// rmt_wnd هو حجم نافذة الاستقبال للطرف الآخر
        kcp->rmt_wnd = wnd
        // ...
// معالجة البيانات
    }

آخر تحديث لنافذة الإرسال
// إذا كان kcp->snd_una - prev_una > 0 ، فهذا يعني أنه قد تم استقبال ACK في الإدخال الحالي وأن حافظة الإرسال snd_buf قد تغيرت
    if (_itimediff(kcp->snd_una, prev_una) > 0) {
//再判断对方的接收窗口
        if (kcp->cwnd < kcp->rmt_wnd) {
            IUINT32 mss = kcp->mss;

            if (kcp->cwnd < kcp->ssthresh) {
// أقل من قيمة عتبة بداية التباطؤ، زيادة مضاعفة
                kcp->cwnd++;
                kcp->incr += mss;

            }    else {
// بعد تجاوز عتبة البدء البطيء، يتم تحديث incr من خلال المعادلة، ومن ثم يتم حساب cwnd
                if (kcp->incr < mss) kcp->incr = mss;
                kcp->incr += (mss * mss) / kcp->incr + (mss / 16);
                if ((kcp->cwnd + 1) * mss <= kcp->incr) {
                    kcp->cwnd++;
                }
            }
// يجب مقارنة القيم التي تم تحديثها مع rmt_wnd من جديد
            if (kcp->cwnd > kcp->rmt_wnd) {
                kcp->cwnd = kcp->rmt_wnd;
                kcp->incr = kcp->rmt_wnd * mss;
            }
        }
    }
}
```
</details>

حساب حجم نافذة الإرسال `kcp->cwnd` يتطلب جزءًا أكبر من الكود، لأنه يجب تحديثه أثناء إرسال واستقبال البيانات. يتم تهيئة `kcp->cwnd` إلى 0،
بعد ذلك، سيتم تقييم القيمة عند أول استدعاء لـ `ikcp_flush`. إذا كانت أقل من 1، فسيتم تعديلها إلى 1. بعد ذلك، بناءً على حجم نافذة الإرسال، سيرسل المرسل عددًا مناسبًا من حزم البيانات، في انتظار ACK.
回复包。ACK 包在 `kcp->input` 中进行处理，`kcp->input` 中如果判断有 ACK 包，并有清除发送缓冲中的发送数据包，说明有数据包已经完成送达，`kcp->cwnd++`。实际上很可能是一次 `kcp->input` 只处理到一个 ACK 包，可以理解为，每收到一个 ACK 包都会有 `kcp->cwnd++`，这句自增实现的是翻倍的效果，譬如当前 `kcp->cwnd = 2`，发送两个数据包，收到两个 ACK 包，触发了两次自增，最后就是 `kcp->cwnd = 4` 翻倍。

`cwnd` يمكن أن ينمو بشكل أسي بشكل مستمر حتى يتجاوز عتبة البدء البطيء أو يحدث عملية إعادة الإرسال بسبب انتهاء المهلة أو إعادة الإرسال السريع. بعد حدوث إعادة الإرسال بسبب انتهاء المهلة، سيتم تفعيل البدء البطيء، حيث تكون عتبة البدء البطيء `ssthresh = kcp->cwnd / 2`، نافذة الإرسال `kcp->cwnd = 1`، والعودة إلى البداية لإعادة النمو الأسي. إذا حدثت إعادة الإرسال السريع، فإن KCP يقوم أولاً بتقليل `ssthresh` بشكل مسبق، مما يعني تقليل المساحة المتاحة لنمو `cwnd` الأسي، وبالتالي تقليل سرعة النمو وتقليل حالات الازدحام بشكل مسبق.

زد KCP أيضًا خيارًا جديدًا وهو `nocwnd`، عندما يكون `nocwnd = 1`، فإن إرسال البيانات لن يأخذ في الاعتبار حجم نافذة الإرسال، بل يتم السماح مباشرة بإرسال أكبر عدد ممكن من حزم البيانات، مما يلبي متطلبات وضع السرعة العالية.

##ملخص

تم تحليل بساطة رموز المصدر لـ KCP في هذا النص، وتم مناقشة تنفيذ ARQ على KCP، بالإضافة إلى بعض استراتيجيات KCP التي تعزز من سرعة تدفق البيانات. لا تم ذكر العديد من التفاصيل، لذا يمكن للأشخاص المهتمين الرجوع إلى رموز مصدر KCP ومقارنتها بأنفسهم، ونعتقد أن هناك الكثير من الفوائد التي يمكن الحصول عليها.

--8<-- "footer_ar.md"


> هذا المنشور تم ترجمته باستخدام ChatGPT، يرجى تقديم [**ردود**](https://github.com/disenone/wiki_blog/issues/new)يرجى تحديد أي نقص. 
