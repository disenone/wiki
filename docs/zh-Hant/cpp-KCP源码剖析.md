---
layout: post
title: KCP 源碼剖析
categories:
- c++
catalog: true
tags:
- dev
description: 本文簡單地分析了 KCP 的源碼，並討論了 KCP 上 ARQ 的實現，和一些 KCP 提升流速的策略。
figures: []
---

<meta property="og:title" content="KCP 源码剖析" />

在閱讀本文之前，如果對 KCP 完全不熟悉，請花點時間先查閱 KCP 項目的說明文件：[傳送門](https://github.com/skywind3000/kcp)這篇文章的目的是深入瞭解 KCP 的實現細節。

##KCP 是什么？

KCP 是一個快速可靠的協議，能以比 TCP 更低的延遲來傳送資料，資料重傳更快，等待時間更短。

> TCP是為了處理流量而設計的（每秒內可以傳輸多少KB的數據），著眼於充分利用帶寬。而KCP則是針對流速設計的（單個數據包從一端發送到另一端需要多少時間），以10%-20%的帶寬浪費換取了比TCP快30%-40%的傳輸速度。TCP信道就像是一條流速緩慢，但每秒流量龐大的大河，而KCP則像是急流湍急的小溪川。

以上是 KCP 文件中所述，關鍵字詞為**帶寬**和**流速**，KCP 將消耗帶寬，帶來的好處是更大更均衡的傳輸速率。詳情請參考 KCP 自身的文件。

##KCP 資料結構

KCP 源碼位於 `ikcp.h` 和 `ikcp.c` 兩個檔案中，`ikcp.h` 的核心部分是資料結構的宣告部分，首先是 `SEGMENT` 資料包，它是 KCP 協議處理資料的最小單位：

<details>
<summary> SEGMENT 結構（點擊展開程式碼） </summary>
```cpp
//=====================================================================
一個 SEGMENT 就是一個 SETMENT。
//=====================================================================
struct IKCPSEG
{
鏈表節點，發送和接收隊列都是這裡的鏈表的結構。
    struct IQUEUEHEAD node;

會話編號，同一個會話編號相同
    IUINT32 conv;

敬请为我转换成传统中文：

    // 資料包類型，例如 DATA 或 ACK
    IUINT32 cmd;

因MTU的限制，大數據包會被拆分成多個小數據包，這是小數據包的編號。
    IUINT32 frg

每個數據包，都會附帶上發送方的接收窗口大小。
    IUINT32 wnd;

// 如果這是一個確認收據包，則發送時間將設置為源數據包的時間戳記
    IUINT32 ts;

唯一標識資料包的編號
    IUINT32 sn;

所有小於una的數據包都已成功接收，這與TCP中的概念一致：最老的未確認序列號SND。
    IUINT32 una;

數據長度
    IUINT32 len;

超時重傳時間
    IUINT32 resendts;

下次超时等待時間
    IUINT32 rto;

快速重传，收到本数据包之后的数据包的数量，大于一定数量就触发快速重传
    IUINT32 fastack;

發送次數
    IUINT32 xmit;

// 資料
    char data[1];
};
```
</details>

閱讀完 `SEGMENT` 的註釋，大致上可以看出 KCP 的核心也是一種 ARQ 協定，透過自動超時重傳來確保資料的傳送。接著再來看看 KCP 結構 `KCPCB` 的定義：

<details>
<summary> KCP 結構（點擊展開程式碼） </summary>
```cpp
//---------------------------------------------------------------------
// IKCPCB
//---------------------------------------------------------------------
struct IKCPCB
{
// 会話編號
mtu, mss：最大傳輸單元，最大報文段大小
// state: 會話狀態，0 有效，-1 斷開
    IUINT32 conv, mtu, mss, state;

// snd_una: 等待 ACK 的包編號
// snd_nxt: 下一個等待發送的資料包編號
// rcv_nxt: 下一個等待接收的資料包編號
    IUINT32 snd_una, snd_nxt, rcv_nxt;

// ts_recent, ts_lastack: Not used
// ssthresh: 拥塞控制慢啟動閾值
    IUINT32 ts_recent, ts_lastack, ssthresh;

// rx_rto: rto (retransmission timeout)，重發超時時間
// rx_rttval, rx_srtt, rx_minrto: 計算 RTO 的中間變數
    IINT32 rx_rttval, rx_srtt, rx_rto, rx_minrto;

// snd_wnd, rcv_wnd: 最大發送和接收視窗大小
// rmt_wnd: 遠端窗口，對方剩餘可接收窗口大小
// cwnd: 可傳送窗口大小
// 探測：是否需要發送控制訊息的標誌
    IUINT32 snd_wnd, rcv_wnd, rmt_wnd, cwnd, probe;

// current: 當前時間
// interval: 更新間隔
ts_flush: 下次需要更新的時間
// xmit: 發送失敗次數
    IUINT32 current, interval, ts_flush, xmit;

對應鏈表的長度
    IUINT32 nrcv_buf, nsnd_buf;
    IUINT32 nrcv_que, nsnd_que;

// nodelay: 控制超時重傳的 rto 增長速度
// updated: Have you called ikcp_update before?
    IUINT32 nodelay, updated;

// ts_probe, probe_wait: When the receiving window of the remote end remains 0 for a long time, actively initiate inquiries at regular intervals.
    IUINT32 ts_probe, probe_wait;

// deal_link: 對端長時間無應答
// incr: 參與計算傳送視窗大小
    IUINT32 dead_link, incr;

// queue: 與使用者層接觸的數據包
// buf: 用來暫存協議資料的數據包
    struct IQUEUEHEAD snd_queue;
    struct IQUEUEHEAD rcv_queue;
    struct IQUEUEHEAD snd_buf;
    struct IQUEUEHEAD rcv_buf;

需要發送 ack 的資料包資訊
    IUINT32 *acklist;

需要確認的封包數量
    IUINT32 ackcount;

// 記錄清單中的記憶體大小
    IUINT32 ackblock;

// 由使用者介面傳入的資料
    void *user;

// 儲存一個 kcp 封包的空間
    char *buffer;

觸發快速重傳的 fastack 次數
    int fastresend;

快速重傳最大次數
    int fastlimit;

// nocwnd: 不考慮慢啟動的傳送窗口大小
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

逐一將 KCP 結構內的字段加上註釋，你會初步感覺到 KCP 的協議並不是太複雜。透徹分析代碼後，大家都能讀懂並理解 KCP 協議。😊

##KCP 的 ARQ 實現

KCP 本質上是一種 ARQ（自動重複請求）協議，最基本的是要確保可靠的傳輸。那麼我們可以先來關注 KCP 的基本 ARQ 部分，KCP 是怎麼實現可靠傳輸的。

ARQ 顧名思義，當我們認為對端接收資料包失敗時，自動重新發送對應的資料包，它是透過確認接收和超時重傳兩個機制，來實現可靠傳輸。具體的程式實現上，KCP 給每個資料包（就是上一節提到的 `SEGMENT`）分配唯一的 `sn` 標識符，一旦對端接收到資料包，會回覆一個 ACK 包（同樣是 `SEGMENT`），ACK 包的 `sn` 跟接收到的資料包 `sn` 相同，通知接收到此資料包已經接收成功。`SEGMENT` 上還有一個 `una` 欄位，表示下一個期待接收的資料包的編號，換句話說，即是所有在該編號之前的資料包都已經接收完，相當於一個全量的 ACK 包，發送端可以更快的更新發送緩衝和發送窗口。

我們可以透過追蹤 KCP 封包的發送和接收代碼，來了解最基本的 ARQ 實現：

###發送

將文字翻譯成繁體中文：

傳送過程為 `ikcp_send` -> `ikcp_update` -> `ikcp_output`，上層調用`ikcp_send`將資料傳送給KCP，KCP在`ikcp_update`中處理資料的傳送。

<details>
<summary> ikcp_send（點擊展開程式碼） </summary>
```cpp
//---------------------------------------------------------------------
// 用戶可以調用ikcp_send來呼叫kcp發送數據接口
// user/upper level send, returns below zero for error
//---------------------------------------------------------------------
int ikcp_send(ikcpcb *kcp, const char *buffer, int len)
{
    IKCPSEG *seg;
    int count, i;

// mss 不能小於1
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
計算封包的資料長度，並分配相應的 seg 結構。
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

將其添加到 snd_queue 末尾，並將 nsnd_qua 加一。
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

`ikcp_send` 是由 KCP 的上層來調用的傳送數據介面，所有讓 KCP 傳送的數據，都應該通過這個介面。`ikcp_send` 做的事情很簡單，主要就是把數據，根據 `kcp->mss`（一個包最大數據長度）來分成多個包，並設置分包編號，最後放到傳送鏈表 `snd_queue` 的末尾。流模式就是把多次調用 `ikcp_send` 的數據都看成一個流，會先自動填充未滿的 `SEGMENT` 再分配新的，詳細實現本文不討論，感興趣的，相信看完本文，再對應看看程式碼就能理解。

在`ikcp_send`調用完成後，數據將被放置在KCP的`snd_queue`中，接著KCP需要找到合適的時機將待發送的數據發送出去。這部分程式碼都位於`ikcp_update`和`ikcp_flush`函數中：

<details>
<summary> ikcp_update（點擊展開程式碼） </summary>
```cpp
//---------------------------------------------------------------------
ikcp_update是一個供上層定期調用的接口，用於更新kcp的狀態，發送數據。
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
// 下次排出的時間
        kcp->ts_flush += kcp->interval;
        if (_itimediff(kcp->current, kcp->ts_flush) >= 0) {
            kcp->ts_flush = kcp->current + kcp->interval;
        }
        ikcp_flush(kcp);
    }
}
```
</details>

`ikcp_update` 做的事情很簡單，判斷一下 `ts_flush` 的時間，符合條件則調用 `ikcp_flush`，主要的處理邏輯都在 `ikcp_flush` 裏面了，因為 `ikcp_flush` 內容複雜一點，我們目前只關注跟 ARQ 發送相關的部分：

<details>
<summary>傳送資料（點擊展開代碼）</summary>
```cpp
//---------------------------------------------------------------------
// ikcp_flush
//---------------------------------------------------------------------
void ikcp_flush(ikcpcb *kcp)
{
    IUINT32 current = kcp->current;

// buffer 是要傳給 ikcp_output 的資料，初始化為 3 倍數據包大小
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

seg.wnd 表示當前可接收窗口大小。
    seg.wnd = ikcp_wnd_unused(kcp);
    seg.una = kcp->rcv_nxt;
    seg.len = 0;
    seg.sn = 0;
    seg.ts = 0;

發送 ack
// 計算傳送窗口
    //...

將資料包從 snd_queue 移動到 snd_buf
移動時必須符合發送視窗的大小，當發送視窗已滿時，即停止移動。
放在 snd_buf 的里面的資料，就是可以直接呼叫 ikcp_output 給對端發送的資料。
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

在這裡設置unna，通知對端下一個等待接收的數據包序號。
        newseg->una = kcp->rcv_nxt;
        newseg->resendts = current;
        newseg->rto = kcp->rx_rto;
        newseg->fastack = 0;
        newseg->xmit = 0;
    }

計算快速重傳標誌，超時等待時間
    // ...

// 傳送 snd_buf
    for (p = kcp->snd_buf.next; p != &kcp->snd_buf; p = p->next) {
        IKCPSEG *segment = iqueue_entry(p, IKCPSEG, node);
        int needsend = 0;
        if (segment->xmit == 0) {
初次發送
// set->xmit 表示發送次數
// 重新傳送超時重傳等待時間
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
快速重传
            // ...
        }

        if (needsend) {
            int need;
            segment->ts = current;
            segment->wnd = seg.wnd;
            segment->una = kcp->rcv_nxt;

            size = (int)(ptr - buffer);
            need = IKCP_OVERHEAD + segment->len;

每當緩衝區中的資料超過 MTU 時，就應該儘快發送出去，以盡量避免底層再次分包。
            if (size + need > (int)kcp->mtu) {
                ikcp_output(kcp, buffer, size);
                ptr = buffer;
            }

將 seg 控制數據複製到 buffer 上，kcp 會自行處理大小端問題。
            ptr = ikcp_encode_seg(ptr, segment);

再複製數據
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

我們目前只專注於 `ikcp_flush` 裡面有關發送數據的邏輯：

首先，KCP 會根據對端的接收窗口大小，將 `snd_queue` 上的資料移動到 `snd_buf` 上，計算移動數量的公式為 `num = snd_nxt - (snd_una + cwnd)`，換句話說：已經成功發送的最大封包序號 `snd_una` 加上滑動窗口大小 `cwnd` 大於下一個待發送的封包序號 `snd_nxt`，則可以繼續發送新的資料封包。在移動 `SEG` 的同時，設置控制欄位。

遍歷 `snd_buf`，如果需要傳送資料包，則將資料複製到 `buffer` 上，複製的同時使用 `ikcp_encode_seg` 處理控制欄位資料的大小端問題。

最後呼叫 `ikcp_output` 將 `buffer` 上的資料發送出去

到這裡，KCP 完成數據的發送。

###接收

接收的過程是與發送相反的：`ikcp_input` -> `ikcp_update` -> `ikcp_recv`，用戶接收到網絡上的數據之後，需要調用 `ikcp_input` 傳給 KCP 解析，調用 `ikcp_update` 的時候會給發送端回覆 ACK 包，上層通過調用 `ikcp_recv` 來接收 KCP 解析之後的數據。

<details>
接收資料（點擊展開程式碼）
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

// data could be multiple KCP packets, handle in a loop
    while (1) {
        IUINT32 ts, sn, len, una, conv;
        IUINT16 wnd;
        IUINT8 cmd, frg;
        IKCPSEG *seg;

/KCP 封包不足，結束
        if (size < (int)IKCP_OVERHEAD) break;

首先將控制欄位解析出來。
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

// 檢查資料包類型
        if (cmd != IKCP_CMD_PUSH && cmd != IKCP_CMD_ACK &&
            cmd != IKCP_CMD_WASK && cmd != IKCP_CMD_WINS) 
            return -3;

        kcp->rmt_wnd = wnd;

在這裡，`una` 代表了發送者的 `kcp->rcv_nxt`，據此資料，可以移除已確認接收的資料包。
        ikcp_parse_una(kcp, una);
將已確認接收的封包刪除後，更新 snd_una 下一個要發送的序號。
        ikcp_shrink_buf(kcp);

        if (cmd == IKCP_CMD_ACK) {
// 确认包
            // ...
        }
        else if (cmd == IKCP_CMD_PUSH) {
數據包
如果接收到的數據包序號 sn 在接收窗口內，則正常處理，否則直接丟棄，等待重傳。
            if (_itimediff(sn, kcp->rcv_nxt + kcp->rcv_wnd) < 0) {

接收到的每個數據包，都要回一個 ack 包，記錄下來
                ikcp_ack_push(kcp, sn, ts);

// 使用 ikcp_parse_data 函數處理接收到的數據
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
// 查詢視窗的回覆封包
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

更新發送視窗
    // ...

    return 0;
}
```
</details>

`ikcp_input` 迴圈處理每一個 `SEG` 包，首先檢查數據包的合法性和類型，因為每個數據包都會攜帶 `una`，存放的是發送端等待接收的包序號，需要小於 `una` 的包對端都已經接受成功，所以可以把 `snd_buff` 中需要小於 `una` 的都刪掉，並更新 `snd_nxt`，這一部分由 `ikcp_parse_una` 和 `ikcp_shrink_buf` 來處理。接收到的每個數據包，都需要回覆 ACK 包，由 `ikcp_ack_push` 記錄下來，最後調用 `ikcp_parse_data` 處理數據。

<details>
解析數據（點擊展開代碼）
```cpp
void ikcp_parse_data(ikcpcb *kcp, IKCPSEG *newseg)
{
    struct IQUEUEHEAD *p, *prev;
    IUINT32 sn = newseg->sn;
    int repeat = 0;

// Serial Number Verification
    if (_itimediff(sn, kcp->rcv_nxt + kcp->rcv_wnd) >= 0 ||
        _itimediff(sn, kcp->rcv_nxt) < 0) {
        ikcp_segment_delete(kcp, newseg);
        return;
    }

請找到 newseg 應該放置的位置，因為接收到的 seg 可能是亂序的。
    for (p = kcp->rcv_buf.prev; p != &kcp->rcv_buf; p = prev) {
        IKCPSEG *seg = iqueue_entry(p, IKCPSEG, node);
        prev = p->prev;
        if (seg->sn == sn) {
// 重複收到
            repeat = 1;
            break;
        }
        if (_itimediff(sn, seg->sn) > 0) {
            break;
        }
    }

將 newseg 放置在 rcv_buf 的正確位置。
    if (repeat == 0) {
        iqueue_init(&newseg->node);
        iqueue_add(&newseg->node, p);
        kcp->nrcv_buf++;
    }    else {
        ikcp_segment_delete(kcp, newseg);
    }

將數據從 rcv_buf 移動到 rcv_queue
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

`ikcp_parse_data` 的主要工作是將 `newseg` 放置在 `kcp->rcv_buf` 的適當位置，並將數據從 `rcv_buf` 移動到 `rcv_queue`。這裡的適當位置指的是，`rcv_buf` 是按照 `sn` 遞增順序排列的，`newseg` 需要根據自己的 `sn` 大小來尋找適當位置。將 `rcv_buf` 上的數據移動到 `rcv_queue` 的條件是，`rcv_buf` 上的數據包序號等於 KCP 等待接收的包序號 `kcp->rcv_nxt`，移動一個數據包後，需要更新 `kcp->rcv_nxt`，再處理下一個數據包。

在调用 `ikcp_input` 后，当上层调用 `ikcp_update` 时，将发送 ACK 数据包；而调用 `ikcp_recv` 时，则会向上层传递有效数据。`ikcp_update` 和 `ikcp_recv` 是相互独立的，没有特定的调用顺序要求，而取决于上层调用的时机。让我们首先来看一下`ikcp_update` 中与 ACK 数据包发送相关的部分：

<details>
<summary> 回覆 ACK（點擊展開程式碼） </summary>
```cpp
我們之前提過，ikcp_update 最終會呼叫 ikcp_flush。
void ikcp_flush(ikcpcb *kcp, IUINT32 current)
{
    // ...

回覆 ACK 封包
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

ACK 包的之前已經由 `ikcp_ack_push` 保存起來了，所以這裡只需要 `ikcp_ack_get` 獲取每個 ACK 包的資訊，發送給對方。上層可以使用 `ikcp_recv` 從 KCP 獲取數據：

<details>
<summary>ikcp_recv（點擊展開程式碼）</summary>
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

一些有效性檢查
    if (iqueue_is_empty(&kcp->rcv_queue))
        return -1;
    if (len < 0) len = -len;

計算能返回的數據長度
    peeksize = ikcp_peeksize(kcp);

    if (peeksize < 0)
        return -2;
    if (peeksize > len)
        return -3;

確認接收視窗大小
    if (kcp->nrcv_que >= kcp->rcv_wnd)
        recover = 1;

遍歷 rcv_queue，將資料複製到 buffer 上
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

移除資料包
        if (ispeek == 0) {
            iqueue_del(&seg->node);
            ikcp_segment_delete(kcp, seg);
            kcp->nrcv_que--;
        }

所有的子程序都已經複製完成，結束迴圈。
        if (fragment == 0)
            break;
    }

    assert(len == peeksize);

// rcv_queue 又空了一些，嘗試繼續從 rcv_buf 移動到 rcv_queue
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

當接收方處理數據包時，如果發送方收到了ACK包，接下來我們來看看發送方處理ACK包的情況：

<details>
<summary> 處理 ACK 封包（點擊展開程式碼） </summary>
```cpp
int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    // ...
    IUINT32 maxack = 0, latest_ts = 0;
    // ...
    while (1) {
        // ...
// ts is the kcp->current of the peer
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

maxack = 所有ACK封包中的最大sn
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

如果收到 ACK 封包，請記錄下來以便進行快速重傳。
    if (flag != 0) {
        ikcp_parse_fastack(kcp, maxack, latest_ts);
    }
}
```
</details>

收到 ACK 包後，需要埋首於 `ikcp_parse_ack` 和 `ikcp_shrink_buf` 來更新 `snd_buf`，同時還要呼叫 `ikcp_update_ack` 來計算更新 rto（重新傳輸超時時間）。`ikcp_input` 則計算收到的 ACK 包中的最大序號，用以記錄快速重傳。這樣一來，當發送端接收到 ACK 包時，會從 `snd_buf` 中刪除發送的資料，確保資料包可靠地送達接收端，完成一倵完整ARQ確認接收流程。

###超時重傳

前面介紹的是 KCP 實現的 ARQ 中的 確認接收機制，ARQ 還需要一個超時重傳來保證可靠性，下面我們來看看 KCP 是怎麼做超時重傳的。

讓我們回到 `ikcp_flush` 函式：

<details>
超時重傳（點擊展開代碼）
```cpp
void ikcp_flush(ikcpcb *kcp)
{
    // ...
傳送 snd_buf
    for (p = kcp->snd_buf.next; p != &kcp->snd_buf; p = p->next) {
        IKCPSEG *segment = iqueue_entry(p, IKCPSEG, node);
        int needsend = 0;
        if (segment->xmit == 0) {
// 首次發送
            needsend = 1;
            segment->xmit++;
設置 segment->rto
透過 segment->rto 計算 segment->resendts 的逾時重傳時間。
            segment->rto = kcp->rx_rto;
            segment->resendts = current + segment->rto + rtomin;
        }
        else if (_itimediff(current, segment->resendts) >= 0) {
// Timeout retransmission
            needsend = 1;
            segment->xmit++;
            kcp->xmit++;
// nodelay 控制下一次超时重传时间的计算
            if (kcp->nodelay == 0) {
                segment->rto += kcp->rx_rto;
            }    else {
                segment->rto += kcp->rx_rto / 2;
            }
            segment->resendts = current + segment->rto;
            lost = 1;
        }
        else if (segment->fastack >= resent) {
// 快速重傳
            // ...
        }
        if (needsend) {
// 傳送資料
            // ...
        }
    // ...
}
```
</details>

一旦當前時間 `current` 大於 `segment->resendts` 超時重傳時間，說明在這段時間內，都沒有收到接收方的 ACK 包，觸發超時重傳機制，`needsend = 1`，重新發送數據。

擁有確認接收和超時重傳機制後，KCP 就能夠確保基本的可靠數據傳輸。然而，為了保持更穩定的數據流速，KCP 進行了更多的優化處理。現在我們一起來看看 KCP 採取了哪些進一步的優化措施。

##KCP 提升流速的策略

###快速重傳

發送端發送了序號為 `sn` 和 `sn + 1` 兩個資料包，如果只收到了 `sn + 1` 的 ACK 包，那可能是因為 `sn` 的 ACK 包在網路中還沒到達，又或者 ACK 包丟了，又或者 `sn` 資料包丟了，如果此時還沒到超時重傳的時間，網路也還不太擁擠，只是因為某種原因而突發丟包，那麼發送端主動提前發送 `sn` 資料包，可以幫助接收方更快地接收資料，提高流速。

KCP 內部也已實現快速重傳機制，同時在 `ikcp_flush` 中：

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

要啟用快速重傳，需滿足兩個條件：
* `segment->fastack >= resent`，resent 是可配置的参数 `kcp->fastresend`，配置為 0 會關閉快速重傳。`segment->fastack` 是在函數 `ikcp_parse_fastack` 裡面設置的，這個函數是在 `ikcp_input` 裡面調用，會根據 `ikcp_input` 算出的 `maxack` 來給所有 `sn` 小於 `maxack` 的 `segment->fastack` 加一，所以 `segment->fastack` 就是表示收到比 `sn` 大的包的次數。
當 `segment->xmit <= kcp->fastlimit || kcp->fastlimit <= 0` 時，`setgment->xmit` 代表傳送次數，`kcp->fastlimit` 則是可設定的最大快速重傳次數，傳送次數必須少於最大快速重傳次數。

當滿足快速重傳的上述條件時，KCP 將執行快速重傳，請注意快速重傳並不會重置超時重傳時間，原來的超時時間依然會生效。

###縮短逾時重傳時間

重送機制是一項非常良好的機制，但實在花費太多時間。按照 TCP 的策略，每次超時重傳的等待時間會倍增，那等待時間就會急速增加。在這等待時間內，由於接收端的接收窗口可能已經耗盡，無法接收新資料，同時需要等待重傳的封包序號卻在最前面。接收端必須等到收到重送的封包後，才能將所有數據返回給上層。這種情況下，整個網路的流速幾乎為零。KCP 增加了配置，可以減緩等待時間的增長，而且不會倍增。透過配置 `kcp->nodelay` 控制，每次等待時間僅會增長1倍的 RTO 或0.5倍的 RTO，有效地減緩等待時間的增長，協助網路盡快恢復流速。

###更新傳送視窗

傳送窗口是指同時傳輸的數據包數量，窗口越大，同時傳輸的數據越多，流速越快，但窗口太大可能導致網絡擁塞，丟包率增加，數據重傳次數增多，流速下降。因此，發送窗口需要根據網絡情況持續更新，逐漸接近最佳值。在KCP中有關發送窗口的程式碼：

<details>
<summary>發送視窗（點擊展開代碼）</summary>
```cpp
ikcpcb* ikcp_create(IUINT32 conv, void *user)
{
    // ...
`snd_wnd` 和 `rcv_wnd` 分別代表發送和接收緩衝區的大小。
    kcp->snd_wnd = IKCP_WND_SND;    // 32
    kcp->rcv_wnd = IKCP_WND_RCV;    // 128
對端接收視窗大小         128
    kcp->rmt_wnd = IKCP_WND_RCV
// 設置發送窗口 cwnd 初始值為 0
    kcp->cwnd = 0;
傳送視窗的位元組大小，用來計算擴 Congestion Window（cwnd）。
    kcp->incr = 0
慢啟動閾值，slow start threshold
    kcp->ssthresh = IKCP_THRESH_INIT;
// nocwnd is a configurable parameter, 1 disregards cwnd.
    kcp->nocwnd = 0;
    // ...
}

void ikcp_flush(ikcpcb *kcp)
{
    // ...
在發送數據時，首先計算發送窗口大小，即發送緩衝區大小和對方接收窗口大小的較小值。
    cwnd = _imin_(kcp->snd_wnd, kcp->rmt_wnd);
默認情況下，還需要考慮 kcp->cwnd，即不斷更新的發送窗口。
    if (kcp->nocwnd == 0) cwnd = _imin_(kcp->cwnd, cwnd);

根據 cwnd 的大小，將 snd_queue 移動到 snd_buf。
    while (_itimediff(kcp->snd_nxt, kcp->snd_una + cwnd) < 0) {
    }
傳送資料
    resent = (kcp->fastresend > 0)? (IUINT32)kcp->fastresend : 0xffffffff;
觸發超時重傳 lost = 1
觸發快速重傳 變更++

更新慢启动閾值和送出窗口
    if (change) {
如果觸發快速重傳，ssthresh 設置為網路上正在傳輸的資料包數量的一半。
        IUINT32 inflight = kcp->snd_nxt - kcp->snd_una;
        kcp->ssthresh = inflight / 2;
        if (kcp->ssthresh < IKCP_THRESH_MIN)
            kcp->ssthresh = IKCP_THRESH_MIN;

// 傳送窗口設為閾值再加上快速重傳相關的 resent
        kcp->cwnd = kcp->ssthresh + resent;
        kcp->incr = kcp->cwnd * kcp->mss;
    }

    if (lost) {
如果有超時重傳，將啟動慢啟動，ssthresh 閾值將設為傳送窗口的一半。
        kcp->ssthresh = cwnd / 2;
        if (kcp->ssthresh < IKCP_THRESH_MIN)
            kcp->ssthresh = IKCP_THRESH_MIN;
將傳送視窗重設為1，重新執行慢啟動增長。
        kcp->cwnd = 1;
        kcp->incr = kcp->mss;
    }

    if (kcp->cwnd < 1) {
因為初始化為 0，來到這裡會再設定成 1
        kcp->cwnd = 1;
        kcp->incr = kcp->mss;
    }
}

int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    IUINT32 prev_una = kcp->snd_una;
處理接收的資料

    while (1) {
        // ...
        data = ikcp_decode16u(data, &wnd)
// rmt_wnd 是對方的接收窗口大小
        kcp->rmt_wnd = wnd
        // ...
處理數據
    }

更新咗發送視窗
當 kcp->snd_una - prev_una > 0 時，表示這次輸入已收到 ACK 且發送緩衝區 snd_buf 有變化。
    if (_itimediff(kcp->snd_una, prev_una) > 0) {
再評估對方的接收窗口
        if (kcp->cwnd < kcp->rmt_wnd) {
            IUINT32 mss = kcp->mss;

            if (kcp->cwnd < kcp->ssthresh) {
小於慢啟動閾值時，成倍增加。
                kcp->cwnd++;
                kcp->incr += mss;

            }    else {
在超過慢啟動閾值之後，通過公式更新 incr，進而計算 cwnd。
                if (kcp->incr < mss) kcp->incr = mss;
                kcp->incr += (mss * mss) / kcp->incr + (mss / 16);
                if ((kcp->cwnd + 1) * mss <= kcp->incr) {
                    kcp->cwnd++;
                }
            }
// The value updated needs to be compared with rmt_wnd again.
            if (kcp->cwnd > kcp->rmt_wnd) {
                kcp->cwnd = kcp->rmt_wnd;
                kcp->incr = kcp->rmt_wnd * mss;
            }
        }
    }
}
```
</details>

計算發送窗口 `kcp->cwnd` 的大小相關的程式碼片段會稍微複雜一些，因為在發送和接收數據時都需要更新。`kcp->cwnd` 初始化為 0，
在初次呼叫 `ikcp_flush` 时，若结果小於1，便將其改為1。之後發送端依據發送窗口大小，發送相對應數量的資料包，並等候確認訊號。
回覆ACK封包。ACK封包在 `kcp->input` 中被處理，若 `kcp->input` 中判別出有ACK封包，並清除發送緩衝區中的發送資料封包，表示某資料封包已成功抵達，`kcp->cwnd++`。事實上很可能一次`kcp->input`只處理一個ACK封包，可理解為每收到一個ACK封包就會執行`kcp->cwnd++`，這個遞增的實現效果是倍增的，例如目前`kcp->cwnd = 2`，發送兩個資料封包，收到兩個ACK封包，觸發兩次遞增，最終就是`kcp->cwnd = 4`倍增。

`cwnd` 可以持續指數增長，直到超過慢啟動閾值，或者發生擁塞超時重傳、快速重傳的情況。發生了超時重傳之後，會觸發慢啟動，慢啟動閾值 `ssthresh = kcp->cwnd / 2`，發送窗口 `kcp->cwnd = 1`，回到最初重新指數增長。如果發生了快速重傳，KCP 先提前減少 `ssthresh`，也就是減少了 `cwnd` 指數增長的空間，降低增長速度，提前減緩擁塞的情況。

KCP 還增加了一個配置 `nocwnd`，當 `nocwnd = 1`，發送數據時不再考慮發送窗口大小，直接讓最大能發送的數量發送數據包，滿足高速模式下的要求。

##總結

本文簡單地分析了 KCP 的源碼，並討論了 KCP 上 ARQ 的實現，以及一些 KCP 提升流速的策略。還有很多細節沒有提到，感興趣的可以自己翻 KCP 的源碼對照著看，相信也能有不少的收穫。

--8<-- "footer_tc.md"


> 此訊息是使用 ChatGPT 翻譯的，請在[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
