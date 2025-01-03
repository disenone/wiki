---
layout: post
title: KCP كود المصدر التحليل
categories:
- c++
catalog: true
tags:
- dev
description: هذا المقال يحلل ببساطة شيفرة KCP ويناقش تنفيذ نقارة التكرار التلقائي
  على KCP، بالإضافة إلى بعض استراتيجيات تعزيز سرعة تدفق KCP.
figures: []
---

<meta property="og:title" content="KCP 源码剖析" />

قبل قراءة هذا المقال، إذا لم تسمع عن KCP من قبل، أو إذا كنت لا تعرف شيئًا عن KCP، يرجى قضاء بعض الوقت في الاطلاع على وثائق شرح مشروع KCP: [رابط](https://github.com/skywind3000/kcp)الهدف من هذا النص هو فهم تفاصيل تنفيذ KCP بشكل متعمق.

##ما هو KCP

KCP هو بروتوكول سريع وموثوق، يمكنه نقل البيانات بتأخير أقل بالمقارنة مع TCP، كما أن إعادة نقل البيانات أسرع والوقت المستغرق في الانتظار أقصر.

> TCP مصمم لحركة المرور (كم من البيانات بالكيلوبايت يمكن نقلها في الثانية)، حيث يهتم باستخدام النطاق الترددي بشكل كامل. بينما KCP مصمم لسرعة تدفق البيانات (كم من الوقت يحتاج الحزمة الواحدة للانتقال من طرف إلى طرف)، مقابل تضييع ما يصل إلى 10%-20% من النطاق الترددي للحصول على سرعة نقل تصل إلى 30%-40% أسرع من TCP. قناة TCP هي قناة برقم تدفق بطيء جدًا ولكن بشحنة بيانات ضخمة في الثانية، بينما KCP هو تيار سريع للمياه.

هذا ما ورد في وثائق KCP، الكلمات الرئيسية هي **عرض النطاق الترددي** و**سرعة التدفق**، يمكن أن يؤدي KCP إلى فقدان عرض النطاق الترددي، مما يتيح فوائد كبيرة من ناحية معدلات النقل الأكبر والأكثر توازنًا. لمزيد من التفاصيل، يُرجى الرجوع إلى وثائق KCP ذاته.

##KCP هيكل البيانات

مصدر رمز KCP موجود في `ikcp.h` و `ikcp.c`، حيث يحتوي `ikcp.h` على تعريفات البنية الأساسية، أولها هو حزمة البيانات `SEGMENT`، وهي الوحدة الأصغر لمعالجة بيانات بروتوكول KCP:

<details>
<ملخص> تركيب القطعة (انقر لعرض الكود) </ملخص>
```cpp
//=====================================================================
// التقسيم هو مجموعة بيانات واحدة
//=====================================================================
struct IKCPSEG
{
// تعتبر العقدة في القائمة المرتبطة، حيث كل من قائمة الإرسال والاستقبال هما هياكل القوائم هنا
    struct IQUEUEHEAD node;

// رقم المحادثة، نفس رقم المحادثة متطابق
    IUINT32 conv;

// نوع حزمة البيانات، مثل DATA أو ACK
    IUINT32 cmd;

بسبب الحد الأقصى لوحدة النقل (MTU)، قد يتم تقسيم حزم البيانات الكبيرة إلى عدة حزم بيانات صغيرة، وهذا هو رقم حزمة البيانات الصغيرة.
    IUINT32 frg

كل حزمة بيانات ستحتوي على حجم نافذة الاستقبال للمرسل.
    IUINT32 wnd;

// وقت الإرسال، إذا كان الحزمة هي حزمة ACK، سيتم ضبطها على الوقت الزمني الخاص بحزمة البيانات الأصلية
    IUINT32 ts;

// رقم يعرف حزمة البيانات بشكل فريد
    IUINT32 sn;

تمثل جميع حزم البيانات التي تكون أقل من una تلقت بنجاح، وهذا يتماشى مع معنى TCP: أقدم رقم تسلسل غير معترف به SND
    IUINT32 una;

طول البيانات
    IUINT32 len;

// وقت إعادة الإرسال في حالة تجاوز الوقت
    IUINT32 resendts;

// وقت الانتظار الزائد في المرة القادمة
    IUINT32 rto;

سريع إعادة البث، يتم تفعيله عندما يتلقى عدد معين من الحزم البيانات بعد استلام هذه الحزمة.
    IUINT32 fastack;

عدد المرات المرسلة
    IUINT32 xmit;

// البيانات
    char data[1];
};
```
</details>

بعد قراءة تعليقات `SEGMENT`، يمكن بشكل عام أن نرى أن جوهر KCP هو بروتوكول ARQ أيضًا، حيث يضمن وصول البيانات من خلال إعادة الإرسال التلقائي بالتوقيت المناسب. لنلق نظرة على تعريف هيكل KCP `KCPCB` بعد ذلك:

<details>
<ملخص> هيكل KCP (انقر لعرض الكود) </ملخص>
```cpp
//---------------------------------------------------------------------
// IKCPCB
//---------------------------------------------------------------------
struct IKCPCB
{
// conv: رقم المحادثة
// mtu, mss: أقصى وحدة نقل، أقصى حجم لقطع البيانات
state: حالة الجلسة ، 0 فعال ، -1 فصل
    IUINT32 conv, mtu, mss, state;

// snd_una: انتظار رقم حزمة ACK
// snd_nxt: رقم الحزمة القادمة المنتظرة للإرسال
// rcv_nxt: الرقم التسلسلي للبيانات التالية المنتظر استقبالها
    IUINT32 snd_una, snd_nxt, rcv_nxt;

// ts_recent، ts_lastack: غير مستخدمة
// ssthresh: عتبة بدء التباطؤ لتحكم الازدحام
    IUINT32 ts_recent, ts_lastack, ssthresh;

// rx_rto: rto (retransmission timeout)，وقت انتهاء العرض (إعادة الإرسال)، وقت إعادة البث
// rx_rttval، rx_srtt، rx_minrto: حساب المتغيرات الوسيطة لـ rto
    IINT32 rx_rttval, rx_srtt, rx_rto, rx_minrto;

// حجم النافذة الخاصة بالإرسال والاستقبال: أقصى حجم للنافذة المستخدمة لعمليات الإرسال والاستقبال
// rmt_wnd: نافذة بعيدة ، حجم نافذة الاستقبال المتبقي للطرف الآخر
// cwnd: حجم نافذة الإرسال القابلة
// الاستعلام: هل تريد إرسال علامة رسالة التحكم؟
    IUINT32 snd_wnd, rcv_wnd, rmt_wnd, cwnd, probe;

// الحالي: الوقت الحالي
// interval: تحديث الفاصل
// ts_flush: الوقت الذي يجب أن يتم فيه التحديث في المرة القادمة
// xmit: عدد مرات فشل الإرسال
    IUINT32 current, interval, ts_flush, xmit;

طول القائمة المرتبطة
    IUINT32 nrcv_buf, nsnd_buf;
    IUINT32 nrcv_que, nsnd_que;

// nodelay: تحكم في سرعة زيادة rto لإعادة الإرسال المتأخر
هل تم استدعاء ikcp_update؟
    IUINT32 nodelay, updated;

// عملية ts_probe، probe_wait: عندما تصبح نوافذ استقبال الجهة المقابلة صفر لفترة طويلة، يتم إطلاق الاستفسارات بانتظام بشكل نشط
    IUINT32 ts_probe, probe_wait;

// deal_link: الجانب الآخر غير مستجيب لفترة طويلة
// incr: Calculate the transmission window size.
    IUINT32 dead_link, incr;

// قائمة الانتظار: حزمة البيانات التي تتفاعل مع طبقة المستخدم
// buf: حزم البيانات المخزنة مؤقتًا
    struct IQUEUEHEAD snd_queue;
    struct IQUEUEHEAD rcv_queue;
    struct IQUEUEHEAD snd_buf;
    struct IQUEUEHEAD rcv_buf;

بيانات الحزمة التي تحتاج إلى إرسال تأكيد ACK
    IUINT32 *acklist;

// تحتاج إلى عدد الحزم ack
    IUINT32 ackcount;

// حجم الذاكرة الداخلية
    IUINT32 ackblock;

// البيانات التي تم تمريرها من طبقة المستخدم
    void *user;

// مساحة تخزين حزمة kcp
    char *buffer;

عدد مرات تنفيذ fastack لتشغيل إعادة الإرسال السريع
    int fastresend;

// عدد مرات إعادة النقل السريع القصوى
    int fastlimit;

//nocwnd: لا يُنظر إلى حجم نافذة الإرسال في التشغيل البطيء
// تيار: وضع التدفق
    int nocwnd, stream;

    // debug log
    int logmask;

// واجهة إرسال البيانات
    int (*output)(const char *buf, int len, struct IKCPCB *kcp, void *user);

    void (*writelog)(const char *log, struct IKCPCB *kcp, void *user);
};
```
</details>

قم بتعليق حقول هيكل KCP بشكل متسلسل، يمكننا أن نشعر بأن بروتوكول KCP ليس معقدًا جدًا. عند تحليل الشفرة بدقة، يمكن لكل منا فهم وفهم بروتوكول KCP :smile:

##تنفيذ ARQ لدى KCP

KCP هو بروتوكول ARQ (Auto Repeat-reQuest، طلب الإعادة التلقائي) في الجوهر، الهدف الأساسي هو ضمان نقل المعلومات بشكل موثوق. لذا، يمكننا أن نركز أولاً على الجزء الأساسي ARQ من KCP وكيف يضمن نقل المعلومات بشكل موثوق.

ARQ، هو اختصار تعني Automatic Repeat reQuest، عندما نعتقد أن الطرف الآخر فشل في استقبال حزمة بيانات، يتم إعادة إرسال الحزمة المقابلة تلقائيًا، يتم تحقيق النقل الآمن من خلال آليتي التأكيد على الاستلام وإعادة الإرسال بعد الانتهاء من المدة الزمنية المحددة. من الناحية العملية لتنفيذ الشيفرة، يخصص KCP معرفًا فريدًا "sn" لكل حزمة بيانات (التي تمت ذكرها في الجزء السابق باسم "SEGMENT")، وبمجرد أن يستلم الطرف الآخر الحزمة بيانات، سيقوم بإرسال حزمة استلام ACK (وهي نفس النوع "SEGMENT")، والـ "sn" لحزمة ACK يتطابق مع "sn" للحزمة البيانات التي تمت استلامها، ويُعلم بأن الحزمة تم استلامها بنجاح. على الـ "SEGMENT" يوجد حقل آخر يسمى "una" يُمثل رقم الحزمة القادمة المتوقع استلامها، بمعنى آخر، أي أن جميع الحزم التي سبقت هذا الرقم قد تم استلامها بالفعل، ويعتبر ذلك بمثابة حزمة ACK شاملة، مما يتيح للطرف المُرسل تحديث الذاكرة المؤقتة للإرسال والنافذة للإرسال بشكل أسرع.

يمكننا فهم تنفيذ ARQ الأساسي عن طريق تتبع رموز إرسال واستقبال حزم الـ KCP.

###إرسال

عملية الإرسال تتضمن `ikcp_send` -> `ikcp_update` -> `ikcp_output`، حيث يُستدعى `ikcp_send` من الطبقة العلوية ليمرر البيانات إلى KCP، ويتم معالجة إرسال البيانات في KCP خلال `ikcp_update`.

<details>
<ملخص> ikcp_send（انقر لعرض الشيفرة）</ملخص>
```cpp
//---------------------------------------------------------------------
// واجهة إرسال البيانات، حيث يُستدعى العميل ikcp_send لإرسال بيانات kcp
// user/upper level send, returns below zero for error
//---------------------------------------------------------------------
int ikcp_send(ikcpcb *kcp, const char *buffer, int len)
{
    IKCPSEG *seg;
    int count, i;

// يجب أن لا تكون قيمة mss أقل من 1
    assert(kcp->mss > 0);
    if (len < 0) return -1;

    // append to previous segment in streaming mode (if possible)
    if (kcp->stream != 0) {
نمط تدفق المعالجة
        // ......
    }

قم بتقسيم البيانات إلى حزم إذا كان طول البيانات len أكبر من mss، ويجب إرسالها في حزم متعددة لتجميعها من قبل الطرف الآخر.
    if (len <= (int)kcp->mss) count = 1;
    else count = (len + kcp->mss - 1) / kcp->mss;

    if (count >= (int)IKCP_WND_RCV) return -2;

    if (count == 0) count = 1;

// تقسيم الحزم
    for (i = 0; i < count; i++) {
حساب طول بيانات الحزمة وتخصيص هيكل seg المقابل
        int size = len > (int)kcp->mss ? (int)kcp->mss : len;
        seg = ikcp_segment_new(kcp, size);
        assert(seg);
        if (seg == NULL) {
            return -2;
        }

قم بتعيين معلومات بيانات seg، حيث تعبر frg عن رقم الحزمة.
        if (buffer && len > 0) {
            memcpy(seg->data, buffer, size);
        }
        seg->len = size;
        seg->frg = (kcp->stream == 0)? (count - i - 1) : 0;

// إضافة إلى نهاية snd_queue، ثم زيادة nsnd_qua بمقدار واحد
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

`ikcp_send` هي واجهة إرسال البيانات التي يجب استدعاؤها من طبقة KCP العليا ، حيث يجب على جميع البيانات التي يتعين إرسالها عبر KCP تمريرها من خلال هذه الواجهة. الأمر الذي تقوم به `ikcp_send` بسيط جدًا ، حيث يقوم أساسًا بتقسيم البيانات إلى عدة حزم وتعيين رقم تسلسلي لكل حزمة ووضعها في نهاية قائمة الإرسال `snd_queue` استنادًا إلى `kcp->mss` (طول البيانات القصوى للحزمة). يتيح الوضع التسلسلي تحويل البيانات التي تم إرسالها بواسطة `ikcp_send` مرارًا وتكرارًا إلى تدفق واحد ، حيث يتم ملء `SEGMENT`غير المكتمل تلقائيًا أولاً ثم تخصيص جديد ، لا تدرس هذه المقالة التفاصيل التنفيذية بشكل مفصل ، إذا كنت مهتمًا ، فأعتقد أن بعد قراءة هذه المقالة ، من الممكن فهم الشفرة بعد رؤيتها.

بمجرد استكمال استدعاء `ikcp_send` ، يتم وضع البيانات في `snd_queue` في KCP. فيما بعد ، يجب على KCP أن يجد فرصة لإرسال البيانات المعلقة، وتوضع هذه الشفرة البرمجية في `ikcp_update` و `ikcp_flush`.

<details>
ikcp_update（انقر لعرض الكود）
```cpp
//---------------------------------------------------------------------
ikcp_update is an interface that should be periodically called by the upper layer to update the state of kcp and send data.
// update state (call it repeatedly, every 10ms-100ms), or you can ask 
// ikcp_check when to call it again (without ikcp_input/_send calling).
// 'current' - current timestamp in millisec. 
//---------------------------------------------------------------------
void ikcp_update(ikcpcb *kcp, IUINT32 current)
{
    IINT32 slap;

    kcp->current = current;

ikcp_flush سوف يتحقق من ذلك، يجب على الطبقة العليا استدعاء ikcp_update قبل استدعاء ikcp_flush، نوصي باستخدام ikcp_update فقط.
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
// الوقت التالي للتفريغ
        kcp->ts_flush += kcp->interval;
        if (_itimediff(kcp->current, kcp->ts_flush) >= 0) {
            kcp->ts_flush = kcp->current + kcp->interval;
        }
        ikcp_flush(kcp);
    }
}
```
</details>

تقوم وظيفة `ikcp_update` بفعل بسيط جدًا، تقوم بتقييم الوقت الخاص بـ `ts_flush`، وإذا تم اجتياز الشرط، سيتم استدعاء `ikcp_flush`. ويتم التعامل الرئيسي في داخل `ikcp_flush`، لأن محتوى `ikcp_flush` أكثر تعقيدًا قليلاً، حاليًا نحن مهتمون فقط بالجزء المتعلق بإرسال الطلبات التكرارية التلقائية ARQ.

<details>
<ملخص> إرسال البيانات (انقر لعرض الشفرة) </ملخص>
```cpp
//---------------------------------------------------------------------
// ikcp_flush
//---------------------------------------------------------------------
void ikcp_flush(ikcpcb *kcp)
{
    IUINT32 current = kcp->current;

// buffer يجب أن تمرر البيانات إلى ikcp_output ، يتم تهيئتها بحجم حزم البيانات ثلاث مرات.
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

// seg.wnd هو تعبير يمثل حجم النافذة الحالية المتاحة للاستقبال
    seg.wnd = ikcp_wnd_unused(kcp);
    seg.una = kcp->rcv_nxt;
    seg.len = 0;
    seg.sn = 0;
    seg.ts = 0;

// إرسال تأكيد
حساب نافذة الإرسال
    //...

نقل حزمة البيانات من قائمة الإرسال إلى الذاكرة النصية للإرسال
التحرك يتطلب تلبية حجم النافذة المرسلة، عندما تمتلئ النافذة المرسلة، يتوقف التحرك.
البيانات الموجودة داخل snd_buf هي البيانات التي يمكن إرسالها مباشرة إلى الطرف الآخر عن طريق استدعاء ikcp_output.
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

// "seg" is a unique serial number, actually it is an increasing kcp->snd_nxt
        newseg->sn = kcp->snd_nxt++;

تم تعيين una هنا لإشعار جهة الاستقبال برقم تسلسل الحزمة التالية التي يجب استقبالها.
        newseg->una = kcp->rcv_nxt;
        newseg->resendts = current;
        newseg->rto = kcp->rx_rto;
        newseg->fastack = 0;
        newseg->xmit = 0;
    }

// حساب علامة إعادة النقل السريع، ووقت الانتظار الزائد
    // ...

// إرسال snd_buf
    for (p = kcp->snd_buf.next; p != &kcp->snd_buf; p = p->next) {
        IKCPSEG *segment = iqueue_entry(p, IKCPSEG, node);
        int needsend = 0;
        if (segment->xmit == 0) {
// الإرسال الأول
set->xmit تعني عدد مرات الإرسال
// وقت الانتظار لإعادة إرسال resendts بعد انتهاء المهلة
            needsend = 1;
            segment->xmit++;
            segment->rto = kcp->rx_rto;
            segment->resendts = current + segment->rto + rtomin;
        }
        else if (_itimediff(current, segment->resendts) >= 0) {
إعادة الإرسال بسبب تجاوز الوقت
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

عندما تتجاوز بيانات الحافظة mtu ، قم بإرسالها أولاً لتجنب تجزئة الطبقة السفلية.
            if (size + need > (int)kcp->mtu) {
                ikcp_output(kcp, buffer, size);
                ptr = buffer;
            }

نسخ بيانات تحكم seg إلى buffer ،  kcp سيتولى التعامل مع مشكلة نهاية البايت لوحده.
            ptr = ikcp_encode_seg(ptr, segment);

// يتم نسخ البيانات مرة أخرى.
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

// حساب قيمة ssthresh وتحديث نافذة البدء البطيء
    // ...
}
```
</details>

نحن حالياً مركزون على المنطق المتعلق بإرسال البيانات داخل `ikcp_flush`:

أولاً، ستقوم KCP بنقل البيانات من `snd_queue` إلى `snd_buf` استنادًا إلى حجم نافذة الاستقبال للطرف الآخر. يُحسب عدد النقل بالمعادلة التالية: `num = snd_nxt - (snd_una + cwnd)`، أي: إذا كانت أقصى رقم تسلسل للحزمة المرسلة بنجاح `snd_una` بزيادة حجم نافذة الانزلاق `cwnd` أكبر من رقم تسلسل الحزمة التالية المقرر إرسالها `snd_nxt`، يمكن مواصلة إرسال بيانات جديدة. خلال نقل `SEG`، سيتم ضبط حقول التحكم.

قم بتمرير `snd_buf`، وفي حال الحاجة إلى إرسال حزمة بيانات، قم بنسخ البيانات إلى الـ `buffer`، مع معالجة مشكلة تناوب البيانات في الحقل التحكم باستخدام `ikcp_encode_seg`.

قم بتنفيذ `ikcp_output` في النهاية لإرسال البيانات على `buffer`

حتى الآن ، أكمل KCP إرسال البيانات.

###استقبال

عملية الاستقبال معاكسة لعملية الإرسال: `ikcp_input` -> `ikcp_update` -> `ikcp_recv`، بعد استلام المستخدم للبيانات عبر الشبكة، يتعين عليه استدعاء `ikcp_input` لتحليلها بواسطة KCP، وأثناء استدعاء `ikcp_update` سيتم إرسال باك ACK إلى الجهة المرسلة، ويمكن للطبقة العليا استقبال البيانات المحللة بعد ذلك عن طريق استدعاء `ikcp_recv`.

<details>
<الملخص> استقبال البيانات (انقر لعرض الشيفرة) </الملخص>
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

// البيانات قد تكون مجموعة من طرود KCP، يتم التعامل معها بشكل دوري
    while (1) {
        IUINT32 ts, sn, len, una, conv;
        IUINT16 wnd;
        IUINT8 cmd, frg;
        IKCPSEG *seg;

لا يكفي وجود حزمة KCP واحدة، تم الخروج
        if (size < (int)IKCP_OVERHEAD) break;

// دعونا نبدأ بتحليل الحقول التحكمية
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

التحقق من نوع الحزمة البيانية
        if (cmd != IKCP_CMD_PUSH && cmd != IKCP_CMD_ACK &&
            cmd != IKCP_CMD_WASK && cmd != IKCP_CMD_WINS) 
            return -3;

        kcp->rmt_wnd = wnd;

هنا، 'una' تمثل 'kcp->rcv_nxt' للجهة المرسلة. باستناد إلى هذه البيانات، يمكن إزالة الحزم التي تم تأكيد استلامها بالفعل.
        ikcp_parse_una(kcp, una);
بعد إزالة الحزم التي تم تأكيد استلامها ، قم بتحديث snd_una بالرقم التسلسلي الذي سيتم إرساله التالي.
        ikcp_shrink_buf(kcp);

        if (cmd == IKCP_CMD_ACK) {
ٍصادق، حزمة //
            // ...
        }
        else if (cmd == IKCP_CMD_PUSH) {
// حُزمة بيانات
إذا كان رقم تسلسل حزمة البيانات المستلمة يقع ضمن نافذة الاستقبال، يتم التعامل معها بشكل طبيعي، في حالة عدم وجوده ضمنها، يتم تجاهلها مباشرة وفي انتظار إعادة الإرسال.
            if (_itimediff(sn, kcp->rcv_nxt + kcp->rcv_wnd) < 0) {

كل حزمة بيانات تستلم يجب أن تُرسَل حزمة تأكيد (ack) معها وتُسجَّل
                ikcp_ack_push(kcp, sn, ts);

// يتم معالجة البيانات المستلمة باستخدام ikcp_parse_data
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
// التحقق من نافذة الحزم
            // ...
        }
        else if (cmd == IKCP_CMD_WINS) {
// رد نافذة الاستعلام
            // ...
        }
        else {
            return -3;
        }

        data += len;
        size -= len;
    }

معالجة منطقية إعادة الإرسال السريع
    // ...

تحديث نافذة الإرسال
    // ...

    return 0;
}
```
</details>

`ikcp_input` یعالج كل حزمة `SEG` بشكل دوري، يتحقق أولاً من صحة البيانات ونوع الحزمة، لأن كل حزمة بيانات تحمل `una`، التي تحتوي على رقم تسلسلي للحزمة التي ينبغي على المرسل انتظار استلامها، عليه أن تكون الحزم التي يحتاج الطرف الآخر استلامها قبل `una` قد تم استقبالها بنجاح، لذا يمكن حذف الحزم التي تحتاج إلى أن تكون قبل `una` من `snd_buff` وتحديث `snd_nxt`، وتتم هذه العملية بواسطة `ikcp_parse_una` و `ikcp_shrink_buf`. كل حزمة بيانات تصل يجب الرد عليها بحزمة ACK، وتُسجّل بواسطة `ikcp_ack_push`، وأخيرًا يتم استدعاء `ikcp_parse_data` لمعالجة البيانات.

<details>
<summary> تحليل البيانات (انقر لعرض الشيفرة) </summary>
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

العثور على الموقع الصحيح لـ newseg، لأن seg الوارد قد يكون غير مرتب بالتسلسل الصحيح.
    for (p = kcp->rcv_buf.prev; p != &kcp->rcv_buf; p = prev) {
        IKCPSEG *seg = iqueue_entry(p, IKCPSEG, node);
        prev = p->prev;
        if (seg->sn == sn) {
من فضلك، قد يكون التصريح غير واضح، يُرجى تقديم سياق إضافي.
            repeat = 1;
            break;
        }
        if (_itimediff(sn, seg->sn) > 0) {
            break;
        }
    }

وضع newseg في مكانه الصحيح داخل rcv_buf
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
إذا كان رقم seg هو رقم الانتظار للتلقي، قم بنقله إلى قائمة الاستقبال.
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

وظيفة `ikcp_parse_data` الرئيسية هي وضع `newseg` في موضع مناسب في `kcp->rcv_buf` ونقل البيانات من `rcv_buf` إلى `rcv_queue`. الموضع المناسب في `rcv_buf` يعني أن `rcv_buf` مرتب بترتيب تصاعدي حسب `sn` ويحتاج `newseg` إلى البحث عن موضع مناسب بناءً على حجم `sn` الخاص به. يجب نقل البيانات الموجودة على `rcv_buf` إلى `rcv_queue` شريطة أن يكون رقم حزمة البيانات على `rcv_buf` مساويًا لرقم حزمة البيانات التي ينتظر KCP تلقيها `kcp->rcv_nxt`، بعد نقل حزمة بيانات، يجب تحديث `kcp->rcv_nxt` ومن ثم معالجة الحزمة البيانات التالية.

بعد `ikcp_input`، عند استدعاء الطبقة العلوية لـ `ikcp_update` سيتم إرسال حزمة ACK، وعند استدعاء `ikcp_recv` ستُعاد البيانات الصحيحة للطبقة العلوية. `ikcp_update` و`ikcp_recv` مستقلّتان تماما، لا توجد متطلبات لترتيب الاستدعاء، بل تعتمد على توقيت الاستدعاء من الطبقة العلوية. دعنا ننظر أولاً إلى الجزء المتعلق بإرسال ACK داخل `ikcp_update`:

<details>
<ملخص> الرد على ACK (انقر لعرض الكود) </ملخص>
```cpp
تم ذكره سابقًا أن ikcp_update يقوم في النهاية باستدعاء ikcp_flush.
void ikcp_flush(ikcpcb *kcp, IUINT32 current)
{
    // ...

// الرد على حزمة ACK
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

تم حفظ حزم ACK مسبقًا بواسطة `ikcp_ack_push` ، لذا هنا يكفي استخدام `ikcp_ack_get` للحصول على معلومات كل حزمة ACK وإرسالها إلى الطرف الآخر. يمكن للطبقة العلوية استخدام `ikcp_recv` للحصول على البيانات من KCP:

<details>
ikcp_recv（انقر لعرض الكود）
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

// بعض الفحوصات الصحيحة
    if (iqueue_is_empty(&kcp->rcv_queue))
        return -1;
    if (len < 0) len = -len;

حساب طول البيانات التي يمكن إرجاعها
    peeksize = ikcp_peeksize(kcp);

    if (peeksize < 0)
        return -2;
    if (peeksize > len)
        return -3;

// تحقق من نافذة الاستلام
    if (kcp->nrcv_que >= kcp->rcv_wnd)
        recover = 1;

تجول في قائمة rcv_queue وانسخ البيانات إلى الbuffer.
    for (len = 0, p = kcp->rcv_queue.next; p != &kcp->rcv_queue; ) {
        int fragment;
        seg = iqueue_entry(p, IKCPSEG, node);
        p = p->next;

        if (buffer) {
            memcpy(buffer, seg->data, seg->len);
            buffer += seg->len;
        }

        len += seg->len;

// التحقق من التقسيم
        fragment = seg->frg;

قم بإزالة الحزمة البيانية
        if (ispeek == 0) {
            iqueue_del(&seg->node);
            ikcp_segment_delete(kcp, seg);
            kcp->nrcv_que--;
        }

تم نسخ جميع الحزم الفرعية، انسحب من الحلقة
        if (fragment == 0)
            break;
    }

    assert(len == peeksize);

// تم تفريغ rcv_queue قليلاً مرة أخرى، يتم محاولة الاستمرار في نقل البيانات من rcv_buf إلى rcv_queue
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

`ikcp_recv` ستُعيد مرة واحدة فقط حزمة بيانات كاملة ، يمكن للطبقة العلوية استدعاء دالة حلقياً حتى لا توجد بيانات تعود ، المنطقية للدالة بسيطة نوعًا ما ، حيث تقوم بنسخ البيانات من `rcv_queue` إلى `buffer` الذي تم تمريره من قبل الطبقة العلوية ، وبهذا تكون الجهة العايدة قد أنهت معالجة البيانات التي تلقتها.

عندما يقوم جهة الاستقبال بمعالجة حزمة البيانات، يُرسل إلى الجهة المرسلة حزمة تأكيد (ACK)، لنلق نظرة أخرى على كيفية استقبال الجهة المرسلة حزمة الـACK.

<details>
<ملخص> معالجة حزمة ACK (انقر لعرض الرمز) </ملخص>
```cpp
int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    // ...
    IUINT32 maxack = 0, latest_ts = 0;
    // ...
    while (1) {
        // ...
// ts يشير إلى kcp-> current النقطة النهائية
        data = ikcp_decode32u(data, &ts);
        data = ikcp_decode32u(data, &sn);

        if (cmd == IKCP_CMD_ACK) {
تحديث rot
            if (_itimediff(kcp->current, ts) >= 0) {
                ikcp_update_ack(kcp, _itimediff(kcp->current, ts));
            }
تحديث snd_buf
            ikcp_parse_ack(kcp, sn);
            ikcp_shrink_buf(kcp);

maxack = أكبر رقم متسلسل في جميع حزم ACK لهذا المدخل
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

إذا تم استلام حزمة ACK، سجلها لاستخدامها في إعادة الإرسال السريع.
    if (flag != 0) {
        ikcp_parse_fastack(kcp, maxack, latest_ts);
    }
}
```
</details>

يمكن رؤية أنه بعد استلام حزمة ACK ، ستحتاج أيضًا إلى استخدام `ikcp_parse_ack` و `ikcp_shrink_buf` لتحديث `snd_buf` ، بالإضافة إلى استدعاء `ikcp_update_ack` لحساب تحديث rto (وقت تكرار الإرسال، مهلة إعادة الإرسال). `ikcp_input` يحسب أكبر رقم تسلسل في حزمة ACK المستلمة ، لتسجيله للاستخدام في الإرسال السريع للبيانات. وبهذه الطريقة ، عندما يستلم الطرف الإرسالي حزمة ACK ، يتمتع بإزالة البيانات المُرسلة من `snd_buf` ، حيث تصل البيانات بشكل موثوق إلى الطرف العامل ، وتنتهي عملية التأكيد الكاملة للاستقبال الآلي (ARQ).

###إعادة الإرسال بعد تجاوز المهلة

سيكون النص المترجم باللغة العربية كالتالي:

تم التعريف في السابق بآلية تأكيد الاستلام في ARQ التي تم تحقيقها بواسطة KCP، تتطلب ARQ أيضًا إعادة الإرسال بعد فترة محددة لضمان الموثوقية، والآن سنلقي نظرة على كيفية تنفيذ إعادة الإرسال بواسطة KCP.

دعونا نعود إلى دالة `ikcp_flush`.

<details>
الملخص: إعادة الإرسال في حالة انتهاء المهلة (انقر لعرض الشيفرة)
```cpp
void ikcp_flush(ikcpcb *kcp)
{
    // ...
// إرسال snd_buf
    for (p = kcp->snd_buf.next; p != &kcp->snd_buf; p = p->next) {
        IKCPSEG *segment = iqueue_entry(p, IKCPSEG, node);
        int needsend = 0;
        if (segment->xmit == 0) {
// الإرسال الأول
            needsend = 1;
            segment->xmit++;
قم بتعيين segment->rto
// استنادًا إلى segment->rto ، يتم حساب وقت إعادة إرسال segment->resendts
            segment->rto = kcp->rx_rto;
            segment->resendts = current + segment->rto + rtomin;
        }
        else if (_itimediff(current, segment->resendts) >= 0) {
// إعادة الإرسال بعد فترة من الانقطاع
            needsend = 1;
            segment->xmit++;
            kcp->xmit++;
تحكم في حساب وقت إعادة النقل المؤجل للمرة القادمة.
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

بمجرد أن يكون الوقت الحالي أكبر من وقت الإعادة `segment->resendts`، يشير ذلك إلى أنه لم يتم استلام حزم ACK من الطرف الآخر خلال هذه الفترة الزمنية. في هذه الحالة، يتم تنشيط آلية إعادة الإرسال نتيجة لتجاوز الوقت المحدد، حيث تُعيد البيانات ويتم تعيين `needsend = 1`.

بعد توفير آلية التأكيد على الاستلام وإعادة الإرسال في حالة الانتهاء من الوقت، يمكن لبروتوكول KCP ضمان نقل البيانات الموثوق به بدعم قواعد البيانات الأساسية. ومن أجل الحفاظ على تدفق البيانات بشكل أسرع، قام KCP أيضًا بالعديد من التحسينات. دعنا نلقي نظرة على الطرق التي قام فيها KCP بتحسين الأداء.

##إستراتيجية زيادة سرعة التدفق لـ KCP

###إعادة النقل السريع

يتلقى المرسل حزمتي بيانات بأرقام متسلسلة `sn` و`sn + 1`. إذا تم استلام حزمة ACK الخاصة بـ `sn + 1` فقط، فقد يكون ذلك بسبب عدم وصول حزمة ACK لـ `sn` إلى الشبكة بعد أو بسبب فقدان حزمة ACK، أو بسبب فقدان حزمة `sn`. في حال عدم انقضاء فترة إعادة البث بسبب عدم الوصول إلى الحد الأقصى للمهلة، وبسبب عدم اكتظاظ الشبكة بشكل كبير أيضًا، وإنما بسبب ظروف مفاجئة تؤدي إلى الفقد، فيمكن للمرسل أن يقوم بإرسال حزمة البيانات `sn` مبكرًا بشكل نشط. هذا يمكن أن يساعد في تسريع استلام البيانات من قبل الطرف الآخر وزيادة سرعة التدفق.

تم تنفيذ آلية إعادة الإرسال السريع داخل KCP، وهو ما يظهر أيضًا في `ikcp_flush`.

<details>
<summary>إعادة النقل السريعة (انقر لعرض الكود)</summary>
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
إعادة النقل السريع
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

يجب أن يتم إعادة النقل السريع في حالتين:
* `segment->fastack >= resent`، resent هو معلم قابل للتكوين في `kcp->fastresend`، وتعيينه على القيمة 0 سيعطل الإعادة السريعة. تُعيَّن قيمة `segment->fastack` في دالة `ikcp_parse_fastack`، وهذه الدالة تُستدعى في `ikcp_input`، حيث يتم زيادتها بواحد لكافة الـ `segment->fastack` التي تقلقيم `sn` من `maxack` المحسوب في `ikcp_input`، وبالتالي، `segment->fastack` تمثل عدد المرات التي تم فيها استقبال باقات تحمل قيمة `sn` أكبر.
الشرط segment->xmit <= kcp->fastlimit || kcp->fastlimit <= 0 ، حيث أن setgment->xmit هو عدد مرات الإرسال، و kcp->fastlimit هو عدد مرات إعادة الإرسال السريع الأقصى الذي يمكن تكوينه، وعدد مرات الإرسال يجب أن يكون أقل من أقصى عدد مرات لإعادة الإرسال السريع

بمجرد توافر شروط إعادة النقل السريع، سيبدأ KCP في تنفيذ إعادة النقل السريع. يجب ملاحظة أن إعادة النقل السريع لن تعيد ضبط زمن إعادة النقل الزائد، سيظل الوقت الأصلي لإعادة النقل الزائد ساري المفعول.

###تقليل وقت إعادة الإرسال في حالة تجاوز الوقت القصوى

الإعادة بالتجاوز في حالة تجاوز الوقت هي آلية رائعة، ولكن تأخذ وقتًا طويلاً، وفقًا لاستراتيجية TCP، يتضاعف وقت الإعادة بالتجاوز في كل مرة، مما يؤدي إلى توسع سريع في وقت الانتظار. قد يحدث في غضون فترة الانتظار أن يكون نافذة الاستقبال بالجهة المستقبلة قد استنفذت، مما يجعلها غير قادرة على استقبال البيانات الجديدة، بينما تكون حزمة الإعادة بالتجاوز في أقصى الأمام، ويجب على الجهة المستقبلة تلقي الحزمة المعادة قبل استعادة جميع البيانات للطبقة العليا، وفي مثل هذه الحالة، يكاد تدفق الشبكة بأكمله يكون صفرًا تقريبًا. يقوم KCP بزيادة تكوينات يمكنها تباطؤ نمو وقت الانتظار، ولن يتم المضاعفة، من خلال تكوين 'kcp->nodelay' لمراقبة زيادة متعددة للمرة الواحدة فقط من RTO أو 0.5RTO، مما يقلل بشكل فعال من زيادة وقت الانتظار، ويساعد الشبكة على استعادة السرعة بسرعة.

###تحديث نافذة الإرسال

يشير نافذة الإرسال إلى عدد حزم البيانات التي تتم نقلها في نفس الوقت، كلما زادت النافذة، زاد عدد البيانات التي يتم نقلها في نفس الوقت وسرعة التدفق، ولكن عندما تكون النافذة كبيرة جدًا، قد تؤدي إلى اكتظاظ الشبكة، وزيادة معدل فقدان الحزم، وزيادة إعادة نقل البيانات، وانخفاض سرعة التدفق. لذلك، من الضروري تحديث نافذة الإرسال بناءً على الوضع الشبكي بشكل مستمر، والتقريب التدريجي إلى الأمثل. الشيفرة حول نافذة الإرسال في KCP:

<details>
<ملخص> إرسال النافذة (انقر لعرض الشيفرة) </ملخص>
```cpp
ikcpcb* ikcp_create(IUINT32 conv, void *user)
{
    // ...
حجم نافذة الإرسال والاستقبال لحجم البيانات المخزنة
    kcp->snd_wnd = IKCP_WND_SND;    // 32
    kcp->rcv_wnd = IKCP_WND_RCV;    // 128
// حجم نافذة الاستقبال على الجانب المستقبل           // 128
    kcp->rmt_wnd = IKCP_WND_RCV
// تهيئة نافذة الإرسال cwnd إلى القيمة 0
    kcp->cwnd = 0;
// إرسال حجم بايت النافذة ، يستخدم في حساب cwnd
    kcp->incr = 0
// عتبة بدء بطيء، حدّ التباطؤ في البداية
    kcp->ssthresh = IKCP_THRESH_INIT;
// nocwnd هو معلمة قابل للتكوين ، 1 لا ينظر إلى cwnd
    kcp->nocwnd = 0;
    // ...
}

void ikcp_flush(ikcpcb *kcp)
{
    // ...
عند إرسال البيانات، يتم حساب حجم نافذة الإرسال أولاً، وهو أصغر قيمة بين حجم النافذة الخاصة بالذاكرة المؤقتة للإرسال وحجم نافذة الاستقبال للشخص الآخر.
    cwnd = _imin_(kcp->snd_wnd, kcp->rmt_wnd);
يجب النظر في القيمة الافتراضية kcp->cwnd، وهي النافذة القابلة للإرسال المحدثة بشكل مستمر.
    if (kcp->nocwnd == 0) cwnd = _imin_(kcp->cwnd, cwnd);

تحريك snd_queue إلى snd_buf وفقًا لحجم cwnd.
    while (_itimediff(kcp->snd_nxt, kcp->snd_una + cwnd) < 0) {
    }
قم بترجمة هذه النص إلى اللغة العربية:

// 发送数据
    resent = (kcp->fastresend > 0)? (IUINT32)kcp->fastresend : 0xffffffff;
// يُعيد تشغيل النقل في حالة فقدان الاتصال lost = 1
// تغيير تنشيط إعادة الارسال السريع ++

// تحديث عتبة البدء البطيء ونافذة الإرسال
    if (change) {
إذا كان هناك إعادة نقل سريعة، فإن قيمة ssthresh يتم تعيينها إلى نصف عدد الحزم التي تُنقل حاليًا عبر الشبكة
        IUINT32 inflight = kcp->snd_nxt - kcp->snd_una;
        kcp->ssthresh = inflight / 2;
        if (kcp->ssthresh < IKCP_THRESH_MIN)
            kcp->ssthresh = IKCP_THRESH_MIN;

// ترسل نافذة تتكون من القيمة الحدية بالإضافة إلى إعادة الإرسال المتعلقة بالإعادة السريعة.
        kcp->cwnd = kcp->ssthresh + resent;
        kcp->incr = kcp->cwnd * kcp->mss;
    }

    if (lost) {
إذا تم إعادة الإرسال بعد فترة زمنية معينة، سيتم تنشيط البدء البطيء، وقيمة ssthresh تكون نصف حجم النافذة المرسلة
        kcp->ssthresh = cwnd / 2;
        if (kcp->ssthresh < IKCP_THRESH_MIN)
            kcp->ssthresh = IKCP_THRESH_MIN;
// إرسال نافذة مرة أخرى إلى 1، وزيادة التشغيل البطيء مرة أخرى
        kcp->cwnd = 1;
        kcp->incr = kcp->mss;
    }

    if (kcp->cwnd < 1) {
بسبب أنه تم تهيئتها إلى القيمة 0، ستُعاد تعيينها هنا إلى 1.
        kcp->cwnd = 1;
        kcp->incr = kcp->mss;
    }
}

int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    IUINT32 prev_una = kcp->snd_una;
// معالجة البيانات المستلمة

    while (1) {
        // ...
        data = ikcp_decode16u(data, &wnd)
// rmt_wnd هو حجم نافذة الاستقبال للطرف الآخر
        kcp->rmt_wnd = wnd
        // ...
ترجمة النص إلى اللغة العربية:

// تناول البيانات
    }

// تحديث نافذة الإرسال الأخيرة
إذا كان "kcp->snd_una - prev_una > 0"، فهذا يعني أنه تم استلام ACK خلال هذا الإدخال وأن حجم الذاكرة المؤقتة للإرسال snd_buf قد تغير.
    if (_itimediff(kcp->snd_una, prev_una) > 0) {
// تقييم نافذة الاستقبال الخاصة بالطرف الآخر
        if (kcp->cwnd < kcp->rmt_wnd) {
            IUINT32 mss = kcp->mss;

            if (kcp->cwnd < kcp->ssthresh) {
// أقل من عتبة التباطؤ، زيادة مضاعفة
                kcp->cwnd++;
                kcp->incr += mss;

            }    else {
بعد تجاوز قيمة عتبة بدء التشغيل البطيء، من خلال تحديث الزيادة بالصيغة، ثم حساب حجم النافذة المتحكمة.
                if (kcp->incr < mss) kcp->incr = mss;
                kcp->incr += (mss * mss) / kcp->incr + (mss / 16);
                if ((kcp->cwnd + 1) * mss <= kcp->incr) {
                    kcp->cwnd++;
                }
            }
يجب مقارنة القيمة المحدثة مرة أخرى مع rmt_wnd.
            if (kcp->cwnd > kcp->rmt_wnd) {
                kcp->cwnd = kcp->rmt_wnd;
                kcp->incr = kcp->rmt_wnd * mss;
            }
        }
    }
}
```
</details>

سيكون هناك قدر أكبر من قطع الشيفرة التي تتعلق بحساب حجم نافذة الإرسال `kcp->cwnd`، لأنه يتطلب تحديثًا عند إرسال البيانات واستقبالها. يتم تهيئة `kcp->cwnd` بقيمة صفر،
سيتم بعد ذلك، عند استدعاء `ikcp_flush` لأول مرة، فحصها إذا كانت أقل من 1 ، ستُعدل إلى 1. بعد ذلك، سيرسل المرسل عددًا من حزم البيانات المقابل لحجم نافذة الإرسال، ثم ينتظر تأكيد الاستقبال.
الرد ACK يتم معالجته في الحزمة `kcp->input`. إذا تم الكشف عن حزمة ACK في `kcp->input` وتم مسح بيانات الحزمة المرسلة في الذاكرة المؤقتة للإرسال، فهذا يعني أن الحزمة قد وصلت بنجاح. سيتم زيادة قيمة `kcp->cwnd++`. في الواقع، من المحتمل جدًا أن يتم معالجة حزمة ACK واحدة فقط في كل عملية `kcp->input`. يمكن تفسير الزيادة `kcp->cwnd++` بأنها زيادة بنسبة مئوية، على سبيل المثال، إذا كان `kcp->cwnd = 2`، وتم إرسال حزمتين، واستقبال حزمتين ACK، ستحدث زيادة مرتين، مما يؤدي إلى `kcp->cwnd = 4`، وهكذا.

`cwnd` can grow exponentially until it exceeds the slow start threshold, or in case of congestion timeout retransmission, or fast retransmission. After a timeout retransmission, slow start is triggered, and the slow start threshold `ssthresh = kcp->cwnd / 2`, the sending window `kcp->cwnd = 1`, returns to the initial exponential growth. In the event of fast retransmission, KCP first reduces `ssthresh` in advance, reducing the space for exponential growth in `cwnd`, slowing down the growth rate, and preemptively alleviating congestion.

KCP قد أضاف إعدادًا جديدًا يسمى `nocwnd`، حيث عندما يكون `nocwnd = 1`، يتم إرسال البيانات دون النظر إلى حجم النافذة، بل يتم إرسال عدد البيانات الأقصى الممكن مباشرة، لتلبية متطلبات الوضع السريع.

##تلخيص

تم تحليل كود المصدر لـ KCP بشكل بسيط في هذا المقال، وتم مناقشة تنفيذ ARQ على KCP، بالإضافة إلى بعض استراتيجيات تعزيز سرعة تدفق KCP. لم يتم ذكر العديد من التفاصيل، يمكن للمهتمين الاطلاع على كود مصدر KCP بأنفسهم والتحقق منه، وأعتقد أنهم سيستفيدون كثيرًا من ذلك.

--8<-- "footer_ar.md"


> تم ترجمة هذه المشاركة باستخدام ChatGPT، يرجى تقديم [**ردود فعل**](https://github.com/disenone/wiki_blog/issues/new)وسمح المكان الذي تم التغاضي عنه. 
