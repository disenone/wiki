---
layout: post
title: KCP 原碼剖析
categories:
- c++
catalog: true
tags:
- dev
description: 本文簡單地分析了 KCP 的源碼，並討論了 KCP 上 ARQ 的實現，和一些 KCP 提升流速的策略。
figures: []
---

<meta property="og:title" content="KCP 源码剖析" />

請在閱讀本文之前，如果您沒有聽過KCP，或對KCP一無所知，請花點時間先看看KCP項目的說明文件：[傳送門](https://github.com/skywind3000/kcp)本文的目的是深入瞭解 KCP 的實現細節。

##KCP 是什麼？

KCP 是一個快速可靠的協議，能夠以比 TCP 更低的延遲來傳送資料，資料重傳更快，等待時間更短。

> TCP是為了處理流量（每秒傳輸多少KB的數據）而設計的，主要考慮充分利用帶寬。而KCP是為了處理流速（單個數據包從一端發送到另一端需時多少）而設計的，以10%-20%帶寬浪費的代價換取了比TCP快30%-40%的傳輸速度。TCP信道就像是一條流速緩慢但每秒流量大的運河，而KCP則是水流湍急的小激流。

以上是 KCP 文檔上面寫的，關鍵詞是**帶寬**和**流速**，KCP 會損耗帶寬，帶來的好處是更大更均衡的傳輸速率。更多的說明參考 KCP 自身的文檔。

##KCP Data Structure

KCP 的原始碼位於 `ikcp.h` 和 `ikcp.c` 中，`ikcp.h` 的核心是資料結構的宣告，首先是 `SEGMENT` 資料包，是 KCP 協定處理資料的最小單位：

<details>
<summary> SEGMENT 結構（點擊展開程式碼）</summary>
```cpp
//=====================================================================
一個 SEGMENT 就是一個 SETMENT 数据包
//=====================================================================
struct IKCPSEG
{
鏈表節點，發送和接收隊列都是這裡的鏈表結構。
    struct IQUEUEHEAD node;

// Session ID，同一個 Session ID 相同
    IUINT32 conv;

數據包類型，例如 DATA 或者 ACK
    IUINT32 cmd;

因為 MTU 的限制，大型資料包會被分割成多個小型資料包，這是小型資料包的編號。
    IUINT32 frg

每個數據包都會攜帶發送方的接收窗口大小。
    IUINT32 wnd;

// 如果是ACK包，則發送時間將設置為源數據包的時間戳记。
    IUINT32 ts;

唯一標識資料包的編號
    IUINT32 sn;

代表小於 una 的資料包都接收成功，跟 TCP 含義一致：最老的未確認序列號 SND
    IUINT32 una;

數據長度
    IUINT32 len;

超時重傳時間
    IUINT32 resendts;

// Next time timeout waiting time
    IUINT32 rto;

快速重傳，當接收到此數據包後後續數據包的數量超過特定閾值時，即會啟動快速重傳。
    IUINT32 fastack;

發送次數
    IUINT32 xmit;

// 資料
    char data[1];
};
```
</details>

閱讀完 `SEGMENT` 的註釋後，我們大致可以理解 KCP 的核心也是一種自動重送請求(ARQ)協議，藉由自動超時重送以確保數據的傳輸。接著我們再來看看 KCP 結構 `KCPCB` 的定義：

<details>
<摘要> KCP 結構（點擊展開代碼） </摘要>
```cpp
//---------------------------------------------------------------------
// IKCPCB
//---------------------------------------------------------------------
struct IKCPCB
{
// 會話編號
mtu, mss: 最大傳輸單元，最大資料段大小
// state: 會話狀態，0 有效，-1 斷開
    IUINT32 conv, mtu, mss, state;

// snd_una: 等待確認收據的封包編號
// snd_nxt：下一個等待發送的數據包編號
// rcv_nxt: 下一个等待接收的資料包編號
    IUINT32 snd_una, snd_nxt, rcv_nxt;

// ts_recent, ts_lastack: Not in use
// ssthresh: 拥塞控制慢启动閾值
    IUINT32 ts_recent, ts_lastack, ssthresh;

// rx_rto: rto (retransmission timeout)，超時重傳時間
// rx_rttval, rx_srtt, rx_minrto: 用來計算 RTO 的中間變量
    IINT32 rx_rttval, rx_srtt, rx_rto, rx_minrto;

snd_wnd, rcv_wnd: 最大發送和接收窗口大小
// rmt_wnd: 對端剩餘接收窗口大小
// cwnd: 可傳送窗口大小
// 探針：是否應該發送控制訊息的標誌
    IUINT32 snd_wnd, rcv_wnd, rmt_wnd, cwnd, probe;

// current: 當前時間
// interval: 更新間隔
// ts_flush: 下次需要更新的時間
// xmit: 傳送失敗次數
    IUINT32 current, interval, ts_flush, xmit;

對應鏈表的長度
    IUINT32 nrcv_buf, nsnd_buf;
    IUINT32 nrcv_que, nsnd_que;

// nodelay: 控制超時重傳的 rto 增長速度
// updated: Have you called ikcp_update before?
    IUINT32 nodelay, updated;

// ts_probe, probe_wait: When the receiving window of the other party remains 0 for a long time, actively initiate periodic inquiries.
    IUINT32 ts_probe, probe_wait;

// deal_link: 對端長時間無應答
// incr: 參與計算傳送視窗大小
    IUINT32 dead_link, incr;

// 队列：與用戶層接觸的數據包
// buf: 協議快取的資料包
    struct IQUEUEHEAD snd_queue;
    struct IQUEUEHEAD rcv_queue;
    struct IQUEUEHEAD snd_buf;
    struct IQUEUEHEAD rcv_buf;

需要發送 ack 的資料包資訊
    IUINT32 *acklist;

需要確認收據的封包數量
    IUINT32 ackcount;

// 記錄內存大小
    IUINT32 ackblock;

// 由使用者層傳入的資料
    void *user;

儲存一個 KCP 封包的空間
    char *buffer;

觸發快速重傳的 fastack 次數
    int fastresend;

快速重传最大次数
    int fastlimit;

// nocwnd: 不考慮慢啟動的發送窗口大小
// stream: 流模式
    int nocwnd, stream;

    // debug log
    int logmask;

// 傳送資料介面
    int (*output)(const char *buf, int len, struct IKCPCB *kcp, void *user);

    void (*writelog)(const char *log, struct IKCPCB *kcp, void *user);
};
```
</details>

將 KCP 結構中的每個欄位逐一註釋上去後，可以初步感受到整個 KCP 協議並不那麼複雜。細細分析程式碼後，你我都能讀懂並理解 KCP 協議。 :smile:

##KCP的ARQ實現

KCP本質上是一個ARQ（Auto Repeat-reQuest，自動重傳）協議，最基本的是要保證可靠的傳輸。那麼我們可以先來關注KCP的基本ARQ部分，KCP是怎麼實現可靠傳輸的。

ARQ，也就是自動重複請求，當我們覺得對方端點接收數據包失敗時，就會自動重新發送對應的數據包。它透過確認接收和超時重發兩個機制，實現了可靠的傳輸。在具體的代碼實現中，KCP會為每個數據包（就是上一節提到的SEGMENT）分配唯一的sn標識符。一旦對方端點收到數據包，會回覆一個ACK包（同樣是SEGMENT），ACK包的sn與收到的數據包sn相同，通知接收到該數據包已經成功接收。在SEGMENT中還有一個una字段，表示下一個期待接收的數據包編號，換句話說，即是所有在該編號之前的數據包都已經接收完，相當於一個全部的ACK包，這樣發送端可以更快地更新發送緩衝和發送窗口。

我們可以通過追蹤 KCP 包的發送和接收程式碼，來理解最基本的 ARQ 實現：

###發送

傳送的流程是 `ikcp_send` -> `ikcp_update` -> `ikcp_output`，上層呼叫 `ikcp_send` 把資料傳送給 KCP，KCP 在 `ikcp_update` 中處理資料的傳送。

<details>
<summary> ikcp_send（點擊展開代碼） </summary>
```cpp
//---------------------------------------------------------------------
傳送資料介面，用戶可呼叫 ikcp_send 來讓 kcp 傳送資料
// user/upper level send, returns below zero for error
//---------------------------------------------------------------------
int ikcp_send(ikcpcb *kcp, const char *buffer, int len)
{
    IKCPSEG *seg;
    int count, i;

mss 不能小於1
    assert(kcp->mss > 0);
    if (len < 0) return -1;

    // append to previous segment in streaming mode (if possible)
    if (kcp->stream != 0) {
處理流模式
        // ......
    }

計算分包，如果數據長度 len 大於 mss，需要分成多個包發送，對端接收到之後再拼起來
    if (len <= (int)kcp->mss) count = 1;
    else count = (len + kcp->mss - 1) / kcp->mss;

    if (count >= (int)IKCP_WND_RCV) return -2;

    if (count == 0) count = 1;

// Subcontracting
    for (i = 0; i < count; i++) {
計算封包資料長度，並分配對應的 seg 結構。
        int size = len > (int)kcp->mss ? (int)kcp->mss : len;
        seg = ikcp_segment_new(kcp, size);
        assert(seg);
        if (seg == NULL) {
            return -2;
        }

設置 seg 的數據信息，frg 表示分包編號
        if (buffer && len > 0) {
            memcpy(seg->data, buffer, size);
        }
        seg->len = size;
        seg->frg = (kcp->stream == 0)? (count - i - 1) : 0;

將其添加到 snd_queue 的末尾，然後將 nsnd_qua 加一。
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

`ikcp_send` 是由 KCP 的上層來調用的傳送資料介面，所有讓 KCP 傳送的資料，都應該透過這個介面。`ikcp_send` 做的事情很簡單，主要就是把資料，根據 `kcp->mss`（一個封包最大資料長度）來分成多個封包，並設定分包編號，最後放到傳送鏈表 `snd_queue` 的末尾。流模式就是把多次調用 `ikcp_send` 的資料都看成一個流，會先自動填充未滿的 `SEGMENT` 再分配新的，詳細實現本文不討論，感興趣的，相信看完本文，再對應看看程式碼就能理解。

`ikcp_send` 被呼叫後，資料會被放置在 KCP 的 `snd_queue` 中，之後 KCP 需要適時地將待傳送的資料發送出去，這部分的程式碼都放在 `ikcp_update` 和 `ikcp_flush` 裡面：

<details>
<summary> ikcp_update（點擊展開程式碼） </summary>
```cpp
//---------------------------------------------------------------------
ikcp_update 是一個接口，需要由上層定期呼叫，用來更新 kcp 的狀態，並發送數據。
// update state (call it repeatedly, every 10ms-100ms), or you can ask 
// ikcp_check when to call it again (without ikcp_input/_send calling).
// 'current' - current timestamp in millisec. 
//---------------------------------------------------------------------
void ikcp_update(ikcpcb *kcp, IUINT32 current)
{
    IINT32 slap;

    kcp->current = current;

ikcp_flush 會檢查這個，上層必須呼叫過 ikcp_update 才能呼叫 ikcp_flush，建議只使用 ikcp_update
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
下一次清空的時間
        kcp->ts_flush += kcp->interval;
        if (_itimediff(kcp->current, kcp->ts_flush) >= 0) {
            kcp->ts_flush = kcp->current + kcp->interval;
        }
        ikcp_flush(kcp);
    }
}
```
</details>

`ikcp_update`做的事情很簡單，判斷一下`ts_flush`的時間，符合條件則調用`ikcp_flush`，主要的處理邏輯都在`ikcp_flush`裡面了，因為`ikcp_flush`內容較為複雜，我們目前只關注跟 ARQ 發送相關的部分：

<details>
傳送資料（點擊展開程式碼）
```cpp
//---------------------------------------------------------------------
// ikcp_flush
//---------------------------------------------------------------------
void ikcp_flush(ikcpcb *kcp)
{
    IUINT32 current = kcp->current;

// buffer is the data to be passed to ikcp_output, initialized to 3 times the size of the data packet.
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

seg.wnd表示目前可接收窗口的大小。
    seg.wnd = ikcp_wnd_unused(kcp);
    seg.una = kcp->rcv_nxt;
    seg.len = 0;
    seg.sn = 0;
    seg.ts = 0;

傳送確認訊息
計算傳送窗口
    //...

將數據包從 snd_queue 移動到 snd_buf
移動時需要滿足「發送窗口」大小，如果發送窗口已滿，就停止移動。
放在 snd_buf 的裡面的資料，就是可以直接呼叫 ikcp_output 給對端發送的資料。
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

// seg 唯一序號，其實就是一個遞增的 kcp->snd_nxt
        newseg->sn = kcp->snd_nxt++;

在這裡設定una，通知對端下一個等待接收的封包序號。
        newseg->una = kcp->rcv_nxt;
        newseg->resendts = current;
        newseg->rto = kcp->rx_rto;
        newseg->fastack = 0;
        newseg->xmit = 0;
    }

計算快速重傳標誌，超時等待時間
    // ...

傳送 snd_buf
    for (p = kcp->snd_buf.next; p != &kcp->snd_buf; p = p->next) {
        IKCPSEG *segment = iqueue_entry(p, IKCPSEG, node);
        int needsend = 0;
        if (segment->xmit == 0) {
// 首次發送
// set->xmit 表示傳輸次數
// 超時重傳的等待時間
            needsend = 1;
            segment->xmit++;
            segment->rto = kcp->rx_rto;
            segment->resendts = current + segment->rto + rtomin;
        }
        else if (_itimediff(current, segment->resendts) >= 0) {
超時重傳
            // ...
        }
        else if (segment->fastack >= resent) {
快速重傳
            // ...
        }

        if (needsend) {
            int need;
            segment->ts = current;
            segment->wnd = seg.wnd;
            segment->una = kcp->rcv_nxt;

            size = (int)(ptr - buffer);
            need = IKCP_OVERHEAD + segment->len;

每當緩衝區中的數據超過 MTU，就儘快發送出去，盡量避免在底層再分包。
            if (size + need > (int)kcp->mtu) {
                ikcp_output(kcp, buffer, size);
                ptr = buffer;
            }

將seg控制資料複製到緩衝區(buffer)上，由kcp自行處理大小端問題。
            ptr = ikcp_encode_seg(ptr, segment);

// 複製資料
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

計算 ssthresh，更新慢啟動窗口
    // ...
}
```
</details>

我們目前僅關注 `ikcp_flush` 裡面有關發送數據的邏輯：

* 首先，KCP 將根據對端的接收窗口大小，將 `snd_queue` 上的數據移動到 `snd_buf` 上，計算移動數量的公式是 `num = snd_nxt - (snd_una + cwnd)`，也就是說：已成功發送的最大封包序號 `snd_una` 加上滑動窗口大小 `cwnd` 大於下個待發送的封包序號 `snd_nxt`，則可以繼續發送新的數據包。在移動 `SEG` 的同時，設置控制欄位。

遍歷 `snd_buf`，若需發送資料包，則將資料複製到 `buffer` 上，同時使用 `ikcp_encode_seg` 處理控制字段資料的大小端問題。

最後呼叫 `ikcp_output` 將 `buffer` 上的資料發送出去

至此，KCP 已完成數據的傳送。

###接收

接收的過程是跟發送相反的：`ikcp_input` -> `ikcp_update` -> `ikcp_recv`，用戶接收到網絡上的數據之後，需要調用 `ikcp_input` 傳給 KCP 解析，調用 `ikcp_update` 的時候會給發送端回覆 ACK 包，上層通過調用 `ikcp_recv` 來接收 KCP 解析之後的數據。

<details>
<summary> 接收資料（點擊展開代碼） </summary>
```cpp
//---------------------------------------------------------------------
// input data
//---------------------------------------------------------------------
int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    IUINT32 prev_una = kcp->snd_una;
    IUINT32 maxack = 0, latest_ts = 0;
    int flag = 0;

合法性檢查
    if (data == NULL || (int)size < (int)IKCP_OVERHEAD) return -1;

// data may consist of multiple KCP packets, handle them in a loop.
    while (1) {
        IUINT32 ts, sn, len, una, conv;
        IUINT16 wnd;
        IUINT8 cmd, frg;
        IKCPSEG *seg;

// 未達到一個 KCP 封包的標準，退出
        if (size < (int)IKCP_OVERHEAD) break;

將控制欄位先解析出來。
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

// 資料包類型檢查
        if (cmd != IKCP_CMD_PUSH && cmd != IKCP_CMD_ACK &&
            cmd != IKCP_CMD_WASK && cmd != IKCP_CMD_WINS) 
            return -3;

        kcp->rmt_wnd = wnd;

這裡的 "una" 是發送方的 kcp->rcv_nxt，根據這個數據，可以去掉已確認接收的數據包。
        ikcp_parse_una(kcp, una);
去除已確認接收的封包後，更新 snd_una 下一個要傳送的序號。
        ikcp_shrink_buf(kcp);

        if (cmd == IKCP_CMD_ACK) {
// 确认包
            // ...
        }
        else if (cmd == IKCP_CMD_PUSH) {
數據包
如果接收到的資料包序號 sn 落在接收視窗內，就按照正常程序處理；如果不在，則直接丟棄，等待重送。
            if (_itimediff(sn, kcp->rcv_nxt + kcp->rcv_wnd) < 0) {

收到的每个数据包都需要回复一个ack包，并将其记录下来。
                ikcp_ack_push(kcp, sn, ts);

接收的資料會進行 ikcp_parse_data 處理。
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
查詢視窗包
            // ...
        }
        else if (cmd == IKCP_CMD_WINS) {
// 查詢視窗的回應包
            // ...
        }
        else {
            return -3;
        }

        data += len;
        size -= len;
    }

處理快速重傳邏輯
    // ...

更新傳送視窗
    // ...

    return 0;
}
```
</details>

`ikcp_input` 會逐一處理每個 `SEG` 封包，優先檢查封包的合法性和類型。因為每個封包都會攜帶 `una`，其中存放著發送端等待接收的封包序號，需要小於 `una` 的對端都已成功接收，因此可以清除 `snd_buff` 中需要小於 `una` 的部分，同時更新 `snd_nxt`。這部分工作由 `ikcp_parse_una` 和 `ikcp_shrink_buf` 負責處理。 每接收到一個封包，都需要回覆 ACK 封包，由 `ikcp_ack_push` 記錄下來，最後呼叫 `ikcp_parse_data` 處理數據。

<details>
解析資料（點擊展開程式碼）
```cpp
void ikcp_parse_data(ikcpcb *kcp, IKCPSEG *newseg)
{
    struct IQUEUEHEAD *p, *prev;
    IUINT32 sn = newseg->sn;
    int repeat = 0;

// Serial number check
    if (_itimediff(sn, kcp->rcv_nxt + kcp->rcv_wnd) >= 0 ||
        _itimediff(sn, kcp->rcv_nxt) < 0) {
        ikcp_segment_delete(kcp, newseg);
        return;
    }

找出應該放置 newseg 的位置，因為接收到的 seg 可能是亂序的。
    for (p = kcp->rcv_buf.prev; p != &kcp->rcv_buf; p = prev) {
        IKCPSEG *seg = iqueue_entry(p, IKCPSEG, node);
        prev = p->prev;
        if (seg->sn == sn) {
重複收到
            repeat = 1;
            break;
        }
        if (_itimediff(sn, seg->sn) > 0) {
            break;
        }
    }

將 newseg 放置於 rcv_buf 的正確位置。
    if (repeat == 0) {
        iqueue_init(&newseg->node);
        iqueue_add(&newseg->node, p);
        kcp->nrcv_buf++;
    }    else {
        ikcp_segment_delete(kcp, newseg);
    }

將資料從 rcv_buf 移動到 rcv_queue
    while (! iqueue_is_empty(&kcp->rcv_buf)) {
        IKCPSEG *seg = iqueue_entry(kcp->rcv_buf.next, IKCPSEG, node);
如果 seg 序號是等待接收的序號，移動到 rcv_queue
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

`ikcp_parse_data` 的主要任務是將 `newseg` 放置到 `kcp->rcv_buf` 適當的位置上，並將數據從 `rcv_buf` 移動到 `rcv_queue`。`rcv_buf` 適當的位置是指，根據 `sn` 遞增的順序排列，`newseg` 需要根據自己的 `sn` 大小查找合適的位置。數據需要從 `rcv_buf` 移動到 `rcv_queue` 的條件是，`rcv_buf` 上的數據包序號等於 KCP 正在等待接收的包序號 `kcp->rcv_nxt` 。移動一個數據包後，需要更新 `kcp->rcv_nxt`，然後處理下一個數據包。

在调用`ikcp_input`后，上层会通过调用 `ikcp_update` 发送ACK包，并通过调用 `ikcp_recv` 返回有效数据。`ikcp_update`和`ikcp_recv`相互独立，无需特定的调用顺序，依赖于上层调用的时机。让我们首先来看看`ikcp_update`中关于ACK包发送的部分：

<details>
<summary>回覆 ACK（點擊展開程式碼）</summary>
```cpp
前面提到過，ikcp_update 最終是呼叫 ikcp_flush。
void ikcp_flush(ikcpcb *kcp, IUINT32 current)
{
    // ...

// Respond to ACK packet
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

ACK 包的內容已經先前由 `ikcp_ack_push` 保存好了，因此這裡只需要使用 `ikcp_ack_get` 來獲取每個 ACK 包的資訊並傳送給對方。上層可以使用 `ikcp_recv` 從 KCP 取得資料：

<details>
<summary> ikcp_recv（點擊展開程式碼）</summary>
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

// 一些有效性檢查
    if (iqueue_is_empty(&kcp->rcv_queue))
        return -1;
    if (len < 0) len = -len;

計算可以回傳的資料長度
    peeksize = ikcp_peeksize(kcp);

    if (peeksize < 0)
        return -2;
    if (peeksize > len)
        return -3;

判斷接收視窗
    if (kcp->nrcv_que >= kcp->rcv_wnd)
        recover = 1;

// 遍歷 rcv_queue，將資料複製到 buffer 上
    for (len = 0, p = kcp->rcv_queue.next; p != &kcp->rcv_queue; ) {
        int fragment;
        seg = iqueue_entry(p, IKCPSEG, node);
        p = p->next;

        if (buffer) {
            memcpy(buffer, seg->data, seg->len);
            buffer += seg->len;
        }

        len += seg->len;

// 判斷分包
        fragment = seg->frg;

刪除資料包
        if (ispeek == 0) {
            iqueue_del(&seg->node);
            ikcp_segment_delete(kcp, seg);
            kcp->nrcv_que--;
        }

所有子程序已經複製完成，退出循環。
        if (fragment == 0)
            break;
    }

    assert(len == peeksize);

rcv_queue 又空了一些，嘗試繼續從 rcv_buf 移動到 rcv_queue
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

`ikcp_recv` 一次調用只會返回一個完整的數據包，上層可以循環調用直到沒有數據返回為止，函數的邏輯比較簡單，就是從 `rcv_queue` 中複製數據到上層傳進來的 `buffer` 裡面，至此接收方對於接收到的數據包已經處理完畢。

當接收方處理資料包時，向發送方發送了確認包（ACK），接下來我們再來看看發送方對確認包的處理：

<details>
<summary>處理 ACK 封包（點擊展開程式碼）</summary>
```cpp
int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    // ...
    IUINT32 maxack = 0, latest_ts = 0;
    // ...
    while (1) {
        // ...
// ts represents the current of the remote kcp -> current
        data = ikcp_decode32u(data, &ts);
        data = ikcp_decode32u(data, &sn);

        if (cmd == IKCP_CMD_ACK) {
更新 rot
            if (_itimediff(kcp->current, ts) >= 0) {
                ikcp_update_ack(kcp, _itimediff(kcp->current, ts));
            }
更新 snd_buf
            ikcp_parse_ack(kcp, sn);
            ikcp_shrink_buf(kcp);

maxack = 這次輸入的所有確認ACK封包中最大的序列號sn
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

如果收到 ACK 封包，請記錄下來以供進行快速重傳。
    if (flag != 0) {
        ikcp_parse_fastack(kcp, maxack, latest_ts);
    }
}
```
</details>

在接收到確認包後，同樣需要使用 `ikcp_parse_ack` 和 `ikcp_shrink_buf` 來更新 `snd_buf`。此外，還需要調用 `ikcp_update_ack` 來計算更新 rto（重發超時時間）。`ikcp_input` 用於計算收到的確認包中的最大序號，以便記錄用於快速重傳。因此，一旦發送方收到確認包，就會從 `snd_buf` 中移除發送的數據，該數據包已可靠地傳達給接收方，一個完整的自動重試請求（ARQ）確認過程就此結束。

###超時重傳

前面提到的是 KCP 實現的 ARQ 中的確認接收機制，ARQ 還需要一個超時重傳來保證可靠性，下面讓我們來看看 KCP 是如何處理超時重傳的。

讓我們回到 `ikcp_flush` 函數：

<details>
<summary>超時重傳（點擊展開程式碼）</summary>
```cpp
void ikcp_flush(ikcpcb *kcp)
{
    // ...
發送 snd_buf
    for (p = kcp->snd_buf.next; p != &kcp->snd_buf; p = p->next) {
        IKCPSEG *segment = iqueue_entry(p, IKCPSEG, node);
        int needsend = 0;
        if (segment->xmit == 0) {
// First time sending
            needsend = 1;
            segment->xmit++;
設置 segment->rto
通過 segment->rto 計算 segment->resendts 超時重傳時間
            segment->rto = kcp->rx_rto;
            segment->resendts = current + segment->rto + rtomin;
        }
        else if (_itimediff(current, segment->resendts) >= 0) {
// 超時重傳
            needsend = 1;
            segment->xmit++;
            kcp->xmit++;
// 當前的程式碼段用於控制下一次超時重傳的時間計算。
            if (kcp->nodelay == 0) {
                segment->rto += kcp->rx_rto;
            }    else {
                segment->rto += kcp->rx_rto / 2;
            }
            segment->resendts = current + segment->rto;
            lost = 1;
        }
        else if (segment->fastack >= resent) {
快速重傳
            // ...
        }
        if (needsend) {
傳送資料
            // ...
        }
    // ...
}
```
</details>

一旦當前時間 `current` 大於 `segment->resendts` 超時重傳時間，說明在這段時間內，都沒有收到接收方的 ACK 包，觸發超時重傳機制，`needsend = 1`，重新發送數據。

透過確認接收和超時重傳機制，KCP 現在能夠確保基本的可靠資料傳輸。不過，為了維持更穩定的資料流速，KCP 還進行了更多的優化。讓我們一起看看 KCP 做了哪些優化。

##KCP 提升流速的策略

###快速重傳

發送方發送了序號為 `sn` 和 `sn + 1` 兩個資料包，如果只收到了 `sn + 1` 的 ACK 包，那可能是因為 `sn` 的 ACK 包在網路中還沒到達，又或者 ACK 包丟了，又或者 `sn` 資料包丟了，如果此時還沒到超時重傳的時間，網路也還不太擁擠，只是因為某種原因而突發丟包，那麼發送方主動提前發送 `sn` 資料包，可以幫助接收方更快地接收資料，提高流速。

KCP 內也相應實現了快速重傳機制，也在 `ikcp_flush` 裡面：

<details>
<summary>快速重傳（點擊展開程式碼）</summary>
```cpp
void ikcp_flush(ikcpcb *kcp)
{
    // ...
    resent = (kcp->fastresend > 0)? (IUINT32)kcp->fastresend : 0xffffffff;

// 傳送 snd_buf
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
快速重傳
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
// 傳送資料
            // ...
        }
    // ...
}
```
</details>

進行快速重傳時，需要滿足兩個條件：
* `segment->fastack >= resent`，resent 是可配置的參數 `kcp->fastresend`，配置為 0 會關閉快速重傳。`segment->fastack` 是在函數 `ikcp_parse_fastack` 裡面設置的，這個函數是在 `ikcp_input` 裡面調用，會根據 `ikcp_input` 算出的 `maxack` 來給所有 `sn` 小於 `maxack` 的 `segment->fastack` 加一，所以 `segment->fastack` 就是表示收到比 `sn` 大的包的次數。
`segment->xmit <= kcp->fastlimit || kcp->fastlimit <= 0`，`setgment->xmit` 是發送次數，`kcp->fastlimit` 是可配置的最大快速重傳次數，發送次數需要小於最大快速重傳次數。

一旦滿足快速重傳的以上條件，KCP 就會執行快速重傳，要注意快速重傳並不會重置超時重傳時間，原來的超時時間依然會生效。

###縮短超時重傳時間

超時重傳是一個很好的機制，但就是太花時間了，按照TCP的策略，每次超時重傳時間翻倍，等待時間膨脹得很快，在等待時間內，很可能由於接收端的接收窗口已耗盡，無法接收新數據，而等待重傳的包序號是在最前面，接收方要接收到重傳的包才能把所有數據返回給上層，這種情況，整個網路的流速幾乎為0。KCP增加了配置可以減緩等待的時間增長，而且也不會是翻倍，通過配置 `kcp->nodelay` 控制每次等待時間只會增長1倍的RTO或者0.5倍的RTO，有效減緩等待時間的增長，幫助網路盡快恢復流速。

###更新傳送視窗

傳送視窗代表同時傳輸的資料包數量，視窗越大，同時傳輸的資料越多，流速越快。不過，若視窗過大，可能導致網路擁塞，造成封包丟失率升高、資料重傳頻繁，從而降低流速。因此，發送視窗須視網路狀況而不斷更新，逐漸趨近最佳。KCP 對發送視窗的相關程式碼：

<details>
<summary>傳送視窗（點擊展開程式碼）</summary>
```cpp
ikcpcb* ikcp_create(IUINT32 conv, void *user)
{
    // ...
snd_wnd，rcv_wnd 是指發送和接收的緩衝區大小。
    kcp->snd_wnd = IKCP_WND_SND;    // 32
    kcp->rcv_wnd = IKCP_WND_RCV;    // 128
// 對端接收窗口大小              // 128
    kcp->rmt_wnd = IKCP_WND_RCV
將此文本翻譯成傳統中文語言：

    // 傳送窗口 cwnd 初始化為 0
    kcp->cwnd = 0;
傳送視窗的位元組大小，用於計算 cwnd。
    kcp->incr = 0
慢啟動閾值，slow start threshold
    kcp->ssthresh = IKCP_THRESH_INIT;
nocwnd 是一個可配置的參數，1 代表不考慮 cwnd。
    kcp->nocwnd = 0;
    // ...
}

void ikcp_flush(ikcpcb *kcp)
{
    // ...
在發送數據時，首先計算發送窗口大小，即發送緩衝區大小和對方接收窗口大小的較小值。
    cwnd = _imin_(kcp->snd_wnd, kcp->rmt_wnd);
// 預設還需要考慮 kcp->cwnd，即為不斷更新的發送視窗
    if (kcp->nocwnd == 0) cwnd = _imin_(kcp->cwnd, cwnd);

根據 cwnd 大小，snd_queue 移動到 snd_buf
    while (_itimediff(kcp->snd_nxt, kcp->snd_una + cwnd) < 0) {
    }
// 傳送資料
    resent = (kcp->fastresend > 0)? (IUINT32)kcp->fastresend : 0xffffffff;
觸發超時重傳，lost = 1
// 觸發快速重傳 變更++

更新慢啟動閾值和發送窗口
    if (change) {
如果出現快速重传觸發，ssthresh 會被設置為當前網路上正在傳輸的封包數量的一半。
        IUINT32 inflight = kcp->snd_nxt - kcp->snd_una;
        kcp->ssthresh = inflight / 2;
        if (kcp->ssthresh < IKCP_THRESH_MIN)
            kcp->ssthresh = IKCP_THRESH_MIN;

將此文本翻譯成繁體中文：

// 發送窗口設置為閾值再加上與快速重傳相關的重傳。
        kcp->cwnd = kcp->ssthresh + resent;
        kcp->incr = kcp->cwnd * kcp->mss;
    }

    if (lost) {
若遇到重傳超時情況，將啟動慢啟動，ssthresh閾值設為發送窗口的一半。
        kcp->ssthresh = cwnd / 2;
        if (kcp->ssthresh < IKCP_THRESH_MIN)
            kcp->ssthresh = IKCP_THRESH_MIN;
將發送窗口重置為1，重新啟動慢啟動增長。
        kcp->cwnd = 1;
        kcp->incr = kcp->mss;
    }

    if (kcp->cwnd < 1) {
由於初始化為 0，到達這裡將被設置為 1。
        kcp->cwnd = 1;
        kcp->incr = kcp->mss;
    }
}

int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    IUINT32 prev_una = kcp->snd_una;
處理接收的數據

    while (1) {
        // ...
        data = ikcp_decode16u(data, &wnd)
rmt_wnd為對方的接收窗口大小。
        kcp->rmt_wnd = wnd
        // ...
處理數據
    }

最後更新發送視窗
kcp->snd_una - prev_una > 0，表示本次 input 有接收到 ACK 并且发送缓冲 snd_buf 有变化
    if (_itimediff(kcp->snd_una, prev_una) > 0) {
再判断对方的接收窗口
        if (kcp->cwnd < kcp->rmt_wnd) {
            IUINT32 mss = kcp->mss;

            if (kcp->cwnd < kcp->ssthresh) {
小於慢啟動閾值，雙倍增長
                kcp->cwnd++;
                kcp->incr += mss;

            }    else {
在超過慢啟動閾值之後，藉由公式更新 incr，進而計算 cwnd。
                if (kcp->incr < mss) kcp->incr = mss;
                kcp->incr += (mss * mss) / kcp->incr + (mss / 16);
                if ((kcp->cwnd + 1) * mss <= kcp->incr) {
                    kcp->cwnd++;
                }
            }
// 再對更新後的值進行 rmt_wnd 進行進一步比較
            if (kcp->cwnd > kcp->rmt_wnd) {
                kcp->cwnd = kcp->rmt_wnd;
                kcp->incr = kcp->rmt_wnd * mss;
            }
        }
    }
}
```
</details>

計算發送窗口 `kcp->cwnd` 的大小所涉及的程式碼片段會稍微多一點，因為在發送和接收資料時，都需要進行更新。`kcp->cwnd` 初始化為 0。
在第一次呼叫 `ikcp_flush` 時，將小於 1 的值更改為 1。然後發送端根據發送窗口大小發送相應數量的數據包，等待 ACK。
回覆封包。ACK 封包在 `kcp->input` 中進行處理，若 `kcp->input` 中檢測到 ACK 封包並清除發送緩衝區中的發送資料封包，代表有資料封包已經成功送達，`kcp->cwnd++`。事實上很可能一次 `kcp->input` 只處理一個 ACK 封包，可以理解為，每接收一個 ACK 封包就會執行一次 `kcp->cwnd++`，這個自增實現了倍增的效果，例如當前 `kcp->cwnd = 2`，發送兩個資料封包，收到兩個ACK 封包，觸發兩次自增，最終得到 `kcp->cwnd = 4` 倍增。

`cwnd` 可以持續指數成長，直到超過慢啟動閾值，或發生擁塞逾時重傳、快速重傳情況。發生逾時重傳後，將觸發慢啟動，慢啟動閾值 `ssthresh = kcp->cwnd / 2`，發送窗口 `kcp->cwnd = 1`，重新回到最初指數成長。若發生快速重傳，KCP 將提前調降 `ssthresh`，即降低了 `cwnd` 指數增長的空間，減緩增長速度，提前緩解擁塞狀況。

KCP 還增加了一個配置 `nocwnd`，當 `nocwnd = 1`，發送數據時不再考慮發送窗口大小，直接將最多可發送的數量的數據包發送出去，滿足高速模式下的要求。

##總結

本文簡單地分析了 KCP 的源碼，並討論了 KCP 上 ARQ 的實現，和一些 KCP 提升流速的策略。還有很多細節沒有提到，感興趣的可以自己翻 KCP 的源碼對照著看，相信也能有不少的收穫。

--8<-- "footer_tc.md"


> 此帖文是由 ChatGPT 翻譯，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
