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

閱讀本文之前，如果不熟悉 KCP 或完全不了解 KCP，請先花點時間閱讀 KCP 項目的說明文件：[傳送門](https://github.com/skywind3000/kcp)本文的目的是深入了解 KCP 的實現細節。

##什麼是 KCP

KCP 是一個快速可靠的協議，能夠以比 TCP 更低的延遲來傳送數據，數據重傳更快，等待時間更短。

> TCP 是為了流量而設計的（每秒內可以傳輸多少 KB 的資料），講究的是充分利用頻寬。而 KCP 是為了流速而設計的（單個數據包從一端發送到另一端需要多少時間），以 10%-20% 頻寬浪費的代價換取了比 TCP 快 30%-40% 的傳輸速度。TCP 信道是一條流速很慢，但每秒流量很大的大運河，而 KCP 是水流湍急的小激流。

以上是 KCP 文件上面寫的，關鍵詞是**帶寬**和**流速**，KCP 會損耗帶寬，帶來的好處是更大更均衡的傳輸速率。更多的說明參考 KCP 自身的文件。

##KCP 資料結構

KCP 源碼在 `ikcp.h` 和 `ikcp.c` 裡面，`ikcp.h` 核心是數據結構的聲明，首先是 `SEGMENT` 數據包，是 KCP 協議處理數據的最小單位：

<details>
<summary> SEGMENT 結構（點擊展開程式碼） </summary>
```cpp
//=====================================================================
// SEGMENT 一個 SETMENT 就是一個數據包
//=====================================================================
struct IKCPSEG
{
// 鏈表節點，發送和接收佇列都是這裡的鏈表結構
    struct IQUEUEHEAD node;

// 會話編號，同一個會話編號相同
    IUINT32 conv;

// 資料包類型，例如 DATA 或者 ACK
    IUINT32 cmd;

因為 MTU 的限制，大型數據包會被拆分為多個小型數據包，這是小型數據包的編號。
    IUINT32 frg

每個封包都會隨附寄送端的接收窗口大小。
    IUINT32 wnd;

發送時間，如果是 ACK 包，會設置為源數據包的 ts
    IUINT32 ts;

唯一標識資料包的編號
    IUINT32 sn;

// 代表小於 una 的數據包都接收成功，跟 TCP 含義一致：最舊的未確認序列號 SND
    IUINT32 una;

// 數據長度
    IUINT32 len;

// 超時重傳時間
    IUINT32 resendts;

下次超时等待时间
    IUINT32 rto;

快速重传是指一旦接收方收到某个数据包后，发现在该数据包之后漏掉的数据包数量达到一定阈值，就会立即请求重新发送丢失的数据包。
    IUINT32 fastack;

發送次數
    IUINT32 xmit;

// 資料
    char data[1];
};
```
</details>

看完`SEGMENT`的註釋，大致能看出 KCP 的核心也是一個 ARQ 協議，通過自動超時重傳來保證數據的送達。接著再來看看 KCP 結構`KCPCB`的定義：

<details>
<summary> KCP 結構（點擊展開程式碼） </summary>
```cpp
//---------------------------------------------------------------------
// IKCPCB
//---------------------------------------------------------------------
struct IKCPCB
{
// conv: 會話編號
// mtu, mss: 最大傳輸單元，最大資料段大小
// state: 會話狀態，0 有效，-1 斷開
    IUINT32 conv, mtu, mss, state;

// snd_una: 等待 ACK 的封包編號
// snd_nxt: 下一個等待發送的數據包編號
rcv_nxt: 下一個等待接收的資料包編號
    IUINT32 snd_una, snd_nxt, rcv_nxt;

// ts_recent, ts_lastack: Not used.
// ssthresh: 擁塞控制慢啟動閾值
    IUINT32 ts_recent, ts_lastack, ssthresh;

// rx_rto: rto (retransmission timeout)，重傳逾時時間
// rx_rttval, rx_srtt, rx_minrto: 計算 rto 的中間變數
    IINT32 rx_rttval, rx_srtt, rx_rto, rx_minrto;

// snd_wnd, rcv_wnd: 最大发送與接收窗口大小
// rmt_wnd: 遠端窗口，對端剩餘接收窗口大小
// cwnd: 可發送窗口大小
// probe: 是否要發送控制報文的標誌
    IUINT32 snd_wnd, rcv_wnd, rmt_wnd, cwnd, probe;

// current: 當前時間
// interval: 更新間隔
// ts_flush: 下次需要更新的時間
// 传送：傳送失敗次數
    IUINT32 current, interval, ts_flush, xmit;

// 對應鏈表的長度
    IUINT32 nrcv_buf, nsnd_buf;
    IUINT32 nrcv_que, nsnd_que;

// nodelay: 控制超時重傳的 rto 增長速度
// updated: Have you called ikcp_update before?
    IUINT32 nodelay, updated;

// ts_probe, probe_wait: When the receiving window of the remote end remains 0 for a long time, active regular inquiries are initiated.
    IUINT32 ts_probe, probe_wait;

// deal_link: The other end is not responding for a long time
// incr: 參與計算發送窗口大小
    IUINT32 dead_link, incr;

// queue: 與用戶層接觸的數據包
// buf: Protocol cache packet
    struct IQUEUEHEAD snd_queue;
    struct IQUEUEHEAD rcv_queue;
    struct IQUEUEHEAD snd_buf;
    struct IQUEUEHEAD rcv_buf;

需要發送 ack 的資料包資訊
    IUINT32 *acklist;

需要確認收到的封包數量
    IUINT32 ackcount;

// 傳回清單中的記憶體大小
    IUINT32 ackblock;

// 從用戶界面傳入的數據
    void *user;

// 存放一個 kcp 包的空間
    char *buffer;

// 觸發快速重傳的 fastack 次數
    int fastresend;

快速重传最大次数
    int fastlimit;

// nocwnd: 不考慮慢啟動的發送窗口大小
// stream: 流模式
    int nocwnd, stream;

    // debug log
    int logmask;

// 發送數據接口
    int (*output)(const char *buf, int len, struct IKCPCB *kcp, void *user);

    void (*writelog)(const char *log, struct IKCPCB *kcp, void *user);
};
```
</details>

將 KCP 結構中的每個字段逐一標上註釋，你會發現整個 KCP 協議並不是太複雜。通過仔細分析代碼，你和我都能讀懂並理解 KCP 協議。😊

##KCP 的 ARQ 實現

KCP 本質上是一個 ARQ（Auto Repeat-reQuest，自動重傳）協議，最基本的是要保證可靠的傳輸。那麼我們可以先來關注 KCP 的基本 ARQ 部分，KCP 是怎麼實現可靠傳輸的。

ARQ 顾名思义，当我们认为对端接收数据包失败时，自动重新发送对应的数据包，它是通过确认接收和超时重传两个机制，来实现可靠传输。具体的代码实现上，KCP 给每个数据包（就是上一节提到的 `SEGMENT`）分配唯一的 `sn` 标识符，一旦对端接收到数据包，会回复一个 ACK 包（同样是 `SEGMENT`），ACK 包的 `sn` 跟接收到的数据包 `sn` 相同，通知接收到此数据包已经接收成功。`SEGMENT` 上还有一个 `una` 字段，表示下一个期待接收的数据包的编号，换句话说，即是所有在该编号之前的数据包都已经接收完，相当于一个全量的 ACK 包，发送端可以更快的更新发送缓冲和发送窗口。

我們可以通過跟蹤 KCP 包的發送和接收代碼，來理解最基本的 ARQ 實現：

###發送

資料傳送的流程是 `ikcp_send` -> `ikcp_update` -> `ikcp_output`。上層呼叫 `ikcp_send` 將資料傳送給 KCP，KCP 在 `ikcp_update` 中處理資料的傳送。

<details>
<總結>ikcp_send（點擊展開代碼）</總結>
```cpp
//---------------------------------------------------------------------
// 發送數據接口，用戶調用 ikcp_send 來讓 kcp 發送數據
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
// 處理流模式
        // ......
    }

計算分包，如果數據長度 len 大於 mss，需要分成多個包發送，對端接收到之後再拼起來
    if (len <= (int)kcp->mss) count = 1;
    else count = (len + kcp->mss - 1) / kcp->mss;

    if (count >= (int)IKCP_WND_RCV) return -2;

    if (count == 0) count = 1;

// Subcontracting
    for (i = 0; i < count; i++) {
計算封包的資料長度，並分配對應的 seg 結構。
        int size = len > (int)kcp->mss ? (int)kcp->mss : len;
        seg = ikcp_segment_new(kcp, size);
        assert(seg);
        if (seg == NULL) {
            return -2;
        }

// 設定 seg 的數據資訊，frg 表示分包編號
        if (buffer && len > 0) {
            memcpy(seg->data, buffer, size);
        }
        seg->len = size;
        seg->frg = (kcp->stream == 0)? (count - i - 1) : 0;

// 加到 snd_queue 的末尾，nsnd_qua 加一
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

`ikcp_send` 是由 KCP 的上層來調用的發送資料介面，所有讓 KCP 發送的資料，都應該通過這個介面。`ikcp_send` 做的事情很簡單，主要就是把資料，根據 `kcp->mss` （一個包最大資料長度）來分成多個包，並設置分包編號，最後放到發送鏈表 `snd_queue` 的末尾。流模式就是把多次調用 `ikcp_send` 的資料都看成一個流，會先自動填充未滿的 `SEGMENT` 再分配新的，詳細實現本文不討論，感興趣的，相信看完本文，再對應看看代碼就能理解。

`ikcp_send` 調用完成之後，數據放在 KCP 的 `snd_queue` 中，那麼後面 KCP 需要找個時機，把待發送的數據發送出去，這塊代碼都放在 `ikcp_update` 和 `ikcp_flush` 裡面：

<details>
<summary> ikcp_update（點擊展開程式碼） </summary>
```cpp
//---------------------------------------------------------------------
// ikcp_update 是給上層定期調用的介面，用來更新 kcp 的狀態，發送數據
// update state (call it repeatedly, every 10ms-100ms), or you can ask 
// ikcp_check when to call it again (without ikcp_input/_send calling).
// 'current' - current timestamp in millisec. 
//---------------------------------------------------------------------
void ikcp_update(ikcpcb *kcp, IUINT32 current)
{
    IINT32 slap;

    kcp->current = current;

ikcp_flush 會檢查這個，上層必須呼叫過 ikcp_update 才能呼叫 ikcp_flush，建議只使用 ikcp_update。
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
// 下次 flush 的時間
        kcp->ts_flush += kcp->interval;
        if (_itimediff(kcp->current, kcp->ts_flush) >= 0) {
            kcp->ts_flush = kcp->current + kcp->interval;
        }
        ikcp_flush(kcp);
    }
}
```
</details>

`ikcp_update` 做的事情很簡單，判斷一下 `ts_flush` 的時間，符合條件則調用 `ikcp_flush`，主要的處理邏輯都在 `ikcp_flush` 裡面了，因為 `ikcp_flush` 內容較為複雜，我們目前只關注跟 ARQ 發送相關的部分：

<details>
<summary>發送資料（點擊展開程式碼）</summary>
```cpp
//---------------------------------------------------------------------
// ikcp_flush
//---------------------------------------------------------------------
void ikcp_flush(ikcpcb *kcp)
{
    IUINT32 current = kcp->current;

// buffer 是要傳給 ikcp_output 的資料，初始化為 3 倍資料包大小
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

// seg.wnd 是表示當前可接收窗口大小
    seg.wnd = ikcp_wnd_unused(kcp);
    seg.una = kcp->rcv_nxt;
    seg.len = 0;
    seg.sn = 0;
    seg.ts = 0;

// 傳送確認訊息
// 計算傳送窗口
    //...

// 把數據包從 snd_queue 移動到 snd_buf
移動時必須滿足發送窗口大小，當發送窗口已滿時，即停止移動。
// 放在 snd_buf 裡面的數據，就是可以直接調用 ikcp_output 給對端發送的數據
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

在這裡設置 una，通知對端下一個等待接收的包序號。
        newseg->una = kcp->rcv_nxt;
        newseg->resendts = current;
        newseg->rto = kcp->rx_rto;
        newseg->fastack = 0;
        newseg->xmit = 0;
    }

計算快速重傳標誌，超時等待時間
    // ...

// Send snd_buf
    for (p = kcp->snd_buf.next; p != &kcp->snd_buf; p = p->next) {
        IKCPSEG *segment = iqueue_entry(p, IKCPSEG, node);
        int needsend = 0;
        if (segment->xmit == 0) {
// 初次發送
// set->xmit 表示發送次數
// resendts 超時重傳的等待時間
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
            // 快速重傳
            // ...
        }

        if (needsend) {
            int need;
            segment->ts = current;
            segment->wnd = seg.wnd;
            segment->una = kcp->rcv_nxt;

            size = (int)(ptr - buffer);
            need = IKCP_OVERHEAD + segment->len;

當緩衝區中的數據超過 MTU 時，儘快發送出去，盡量避免底層再次分包。
            if (size + need > (int)kcp->mtu) {
                ikcp_output(kcp, buffer, size);
                ptr = buffer;
            }

// 把 seg 控制數據複製到 buffer 上，kcp 自己來處理大小端問題
            ptr = ikcp_encode_seg(ptr, segment);

// 再複製資料
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

我們目前只關注 `ikcp_flush` 裡面有關發送數據的邏輯：

首先，根據對端的接收窗口大小，KCP會將`snd_queue`中的數據移至`snd_buf`，移動數量的計算公式為`num = snd_nxt - (snd_una + cwnd)`，換言之：已成功發送的最大數據包序號`snd_una`加上滑動窗口大小`cwnd`大於下一個待發送的數據包序號`snd_nxt`，即可繼續發送新數據包。在移動`SEG`的同時，設置控制字段。

遍歷 `snd_buf`，如果需要發送資料包，則將資料複製到 `buffer` 上，同時在複製時使用 `ikcp_encode_seg` 處理控制字段資料的大小端問題。

最後呼叫`ikcp_output`將`buffer`上的資料傳送出去

至此，KCP 完成數據的發送。

###接收

接收的過程是跟發送相反的：`ikcp_input` -> `ikcp_update` -> `ikcp_recv`，使用者接收到網絡上的數據之後，需要調用 `ikcp_input` 傳給 KCP 解析，調用 `ikcp_update` 的時候會給發送端回覆 ACK 包，上層通過調用 `ikcp_recv` 來接收 KCP 解析之後的數據。

<details>
<summary> 接收數據（點擊展開代碼） </summary>
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

// data 可能是多個 KCP 包，循環處理
    while (1) {
        IUINT32 ts, sn, len, una, conv;
        IUINT16 wnd;
        IUINT8 cmd, frg;
        IKCPSEG *seg;

// 不夠一個 KCP 包，退出
        if (size < (int)IKCP_OVERHEAD) break;

// 先把控制字段解析出來
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

資料包類型檢查
        if (cmd != IKCP_CMD_PUSH && cmd != IKCP_CMD_ACK &&
            cmd != IKCP_CMD_WASK && cmd != IKCP_CMD_WINS) 
            return -3;

        kcp->rmt_wnd = wnd;

// 這裡的 una 是發送方的 kcp->rcv_nxt，根據這個數據，可以去掉已確認接收的數據包
        ikcp_parse_una(kcp, una);
// 去掉已確認接收的包後，更新 snd_una 下一個要發送的序號
        ikcp_shrink_buf(kcp);

        if (cmd == IKCP_CMD_ACK) {
// ack 包
            // ...
        }
        else if (cmd == IKCP_CMD_PUSH) {
數據包
// 如果接收到的數據包序號 sn，在接收窗口內，則正常處理，否則直接丟棄，等重傳
            if (_itimediff(sn, kcp->rcv_nxt + kcp->rcv_wnd) < 0) {

收到的每個資料封包都應該發回一個確認封包，並加以記錄。
                ikcp_ack_push(kcp, sn, ts);

// 接收的數據調用 ikcp_parse_data 處理
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
// 查詢視窗包
            // ...
        }
        else if (cmd == IKCP_CMD_WINS) {
// 查詢窗口的回覆包
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

// 更新發送窗口
    // ...

    return 0;
}
```
</details>

`ikcp_input` 循環處理每一個 `SEG` 包，先檢查數據包的合法性和類型，因為每個數據包都會帶上 `una`，存放的是發送端等待接收的包序號，需要小於 `una` 的包對端都已經接受成功，所以可以把 `snd_buff` 中需要小於 `una` 的都刪掉，並更新 `snd_nxt`，這一部分由 `ikcp_parse_una` 和 `ikcp_shrink_buf` 來處理。接收到的每個數據包，都需要回覆 ACK 包，由 `ikcp_ack_push` 記錄下來，最後調用 `ikcp_parse_data` 處理數據。

<details>
<summary> 解析數據（點擊展開代碼） </summary>
```cpp
void ikcp_parse_data(ikcpcb *kcp, IKCPSEG *newseg)
{
    struct IQUEUEHEAD *p, *prev;
    IUINT32 sn = newseg->sn;
    int repeat = 0;

序號檢查
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
// 重複收到
            repeat = 1;
            break;
        }
        if (_itimediff(sn, seg->sn) > 0) {
            break;
        }
    }

將 newseg 放置在 rcv_buf 的正確位置上。
    if (repeat == 0) {
        iqueue_init(&newseg->node);
        iqueue_add(&newseg->node, p);
        kcp->nrcv_buf++;
    }    else {
        ikcp_segment_delete(kcp, newseg);
    }

將資料從 rcv_buf 移動到 rcv_queue。
    while (! iqueue_is_empty(&kcp->rcv_buf)) {
        IKCPSEG *seg = iqueue_entry(kcp->rcv_buf.next, IKCPSEG, node);
// 如果 seg 序號是等待接收的序號，移動到 rcv_queue
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

`ikcp_parse_data` 主要的工作就是把 `newseg` 放置到 `kcp->rcv_buf` 合適的位置上，並把數據從 `rcv_buf` 移動到 `rcv_queue`。`rcv_buf` 合適的位置的意思是，`rcv_buf` 是按照 `sn` 的遞增順序排列的，`newseg` 需要根據自己的 `sn` 大小查找合適的位置。`rcv_buf` 上的數據要移動到 `rcv_queue`，條件是 `rcv_buf` 上的數據包序號等於 KCP 在等待接收的包序號 `kcp->rcv_nxt`，移動一個數據包之後，需要更新 `kcp->rcv_nxt`，再處理下一個數據包。

在`ikcp_input`後，上層呼叫`ikcp_update`時會發送 ACK 封包，呼叫`ikcp_recv`會提供有效資料給上層。`ikcp_update`和`ikcp_recv`彼此獨立，沒有呼叫順序要求，取決於上層的呼叫時機。現在讓我們先看看`ikcp_update`裡面有關 ACK 發送的部分：

<details>
<summary>回應 ACK（點擊展開程式碼）</summary>
```cpp
// 前面提到，ikcp_update 最終是調用 ikcp_flush
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

ACK 包的之前已由 `ikcp_ack_push` 保存起來了，所以這裡只需要 `ikcp_ack_get` 獲取每個 ACK 包的信息，發送給對方。上層可以使用 `ikcp_recv` 從 KCP 獲取數據：

<details>
<summary> ikcp_recv（點擊展開代碼） </summary>
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

// 計算能返回的數據長度
    peeksize = ikcp_peeksize(kcp);

    if (peeksize < 0)
        return -2;
    if (peeksize > len)
        return -3;

// 判斷下接收窗口
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

刪除封包
        if (ispeek == 0) {
            iqueue_del(&seg->node);
            ikcp_segment_delete(kcp, seg);
            kcp->nrcv_que--;
        }

// 所有分包都複製完，退出循環
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

當接收端處理數據包時，會向發送端發送確認包。現在讓我們來看看發送端如何處理接收到的確認包：

<details>
<summary> 處理 ACK 包（點擊展開代碼） </summary>
```cpp
int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    // ...
    IUINT32 maxack = 0, latest_ts = 0;
    // ...
    while (1) {
        // ...
ts 是對端的 kcp-> current
        data = ikcp_decode32u(data, &ts);
        data = ikcp_decode32u(data, &sn);

        if (cmd == IKCP_CMD_ACK) {
// 更新 rot
            if (_itimediff(kcp->current, ts) >= 0) {
                ikcp_update_ack(kcp, _itimediff(kcp->current, ts));
            }
// 更新 snd_buf
            ikcp_parse_ack(kcp, sn);
            ikcp_shrink_buf(kcp);

// maxack = 這次 input 的所有 ACK 包中最大的 sn
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

如果收到 ACK 封包，請記錄下來以供快速重傳。
    if (flag != 0) {
        ikcp_parse_fastack(kcp, maxack, latest_ts);
    }
}
```
</details>

收到 ACK 包後，會需要使用 `ikcp_parse_ack` 和 `ikcp_shrink_buf` 來更新 `snd_buf`，同時也要呼叫 `ikcp_update_ack` 來計算更新 rto（重傳超時時間）。`ikcp_input` 會計算收到的 ACK 包中的最大序號，以便快速重傳。這樣一來，當發送端收到 ACK 包後，將從 `snd_buf` 中移除發送的數據，表示該數據包已可靠地傳送到接收端，一次完整的 ARQ 確認接收過程就此結束。

###超时重传

前面介紹的是 KCP 實現的 ARQ 中的 確認接收機制，ARQ 還需要一個超時重傳來保證可靠性，下面我們來看看 KCP 是怎麼做超時重傳的。

讓我們回到 `ikcp_flush` 函數：

<details>
超時重傳（點擊展開代碼）
```cpp
void ikcp_flush(ikcpcb *kcp)
{
    // ...
// 發送 snd_buf
    for (p = kcp->snd_buf.next; p != &kcp->snd_buf; p = p->next) {
        IKCPSEG *segment = iqueue_entry(p, IKCPSEG, node);
        int needsend = 0;
        if (segment->xmit == 0) {
            // 首次發送
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

有了確認接收和超時重傳機制，KCP 就可以保證基礎的可靠數據傳輸。但是為了能夠保持更穩定的數據流速，KCP 還做了更多的事情，下面我們一起看看 KCP 還做了哪些優化。

##KCP 提升流速的策略

###快速重傳

發送方發送了序號為 `sn` 和 `sn + 1` 兩個資料包，如果只收到了 `sn + 1` 的 ACK 包，那可能是因為 `sn` 的 ACK 包在網路中還沒到達，又或者 ACK 包丟了，又或者 `sn` 資料包丟了，如果此時還沒到超時重傳的時間，網路也還不太擁擠，只是因為某種原因而突發丟包，那麼發送方主動提前發送 `sn` 資料包，可以幫助接收方更快地接收資料，提高流速。

KCP 內也同時實現了快速重傳機制，在 `ikcp_flush` 函數中：

<details>
<summary> 快速重傳（點擊展開代碼） </summary>
```cpp
void ikcp_flush(ikcpcb *kcp)
{
    // ...
    resent = (kcp->fastresend > 0)? (IUINT32)kcp->fastresend : 0xffffffff;

// 發送 snd_buf
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
// 快速重傳
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
// 發送數據
            // ...
        }
    // ...
}
```
</details>

要啟用快速重傳，必須滿足兩個條件：
* `segment->fastack >= resent`，resent 是可配置的參數 `kcp->fastresend`，配置為 0 會關閉快速重傳。`segment->fastack` 是在函數 `ikcp_parse_fastack` 裡面設置的，這個函數是在 `ikcp_input` 裡面調用，會根據 `ikcp_input` 算出的 `maxack` 來給所有 `sn` 小於 `maxack` 的 `segment->fastack` 加一，所以 `segment->fastack` 就是表示收到比 `sn` 大的包的次數。
* `segment->xmit <= kcp->fastlimit || kcp->fastlimit <= 0`，`segment->xmit` 是發送次數，`kcp->fastlimit` 是可配置的最大快速重傳次數，發送次數需要小於最大快速重傳次數。

一旦滿足快速重傳的以上條件，KCP 就會執行快速重傳，要注意快速重傳並不會重置超時重傳時間，原來的超時時間依然會生效。

###縮短超時重傳時間

超時重傳是一個很好的機制，但就是太花時間了，按照 TCP 的策略，每次超時重傳時間翻倍，等待時間膨脹得很快，在等待時間內，很可能由於接收端的接收窗口已耗盡，無法接收新數據，而等待重傳的包序號是在最前面，接收方要接收到重傳的包才能把所有數據返回給上層，這種情況，整個網路的流速幾乎為0。KCP 增加了配置可以減緩等待的時間增長，而且也不會是翻倍，通過配置 `kcp->nodelay` 控制每次等待時間只會增長1倍的 RTO 或者0.5倍的 RTO，有效減緩等待時間的增長，幫助網路尽快恢復流速。

###更新發送窗口

發送窗口表示的是同時傳輸的數據包數量，窗口越大，同時傳輸的數據越多，流速越大，但窗口過大，會導致網路擁塞，丟包率上升，數據重傳增多，流速下降。所以發送窗口需要根據網路情況不斷更新，慢慢趨近最優。KCP 中關於發送窗口的程式碼：

<details>
<summary> 發送窗口（點擊展開代碼） </summary>
```cpp
ikcpcb* ikcp_create(IUINT32 conv, void *user)
{
    // ...
snd_wnd和rcv_wnd是用來指定發送和接收緩衝區大小的參數。
    kcp->snd_wnd = IKCP_WND_SND;    // 32
    kcp->rcv_wnd = IKCP_WND_RCV;    // 128
// The size of the receive window on the other end           // 128
    kcp->rmt_wnd = IKCP_WND_RCV
// 發送窗口 cwnd 初始化 0
    kcp->cwnd = 0;
// 發送窗口字節數大小，參與計算 cwnd
    kcp->incr = 0
// 慢啟動閾值，slow start threshold
    kcp->ssthresh = IKCP_THRESH_INIT;
// nocwnd 是可配置參數，1 不考慮 cwnd
    kcp->nocwnd = 0;
    // ...
}

void ikcp_flush(ikcpcb *kcp)
{
    // ...
在發送數據之前，首先要計算發送窗口大小，這是指發送緩衝區大小和對方接收窗口大小的較小值。
    cwnd = _imin_(kcp->snd_wnd, kcp->rmt_wnd);
// 預設還需要考慮 kcp->cwnd，即是不斷更新的傳送視窗
    if (kcp->nocwnd == 0) cwnd = _imin_(kcp->cwnd, cwnd);

根據 cwnd 大小，snd_queue 移動到 snd_buf
    while (_itimediff(kcp->snd_nxt, kcp->snd_una + cwnd) < 0) {
    }
// 傳送資料
    resent = (kcp->fastresend > 0)? (IUINT32)kcp->fastresend : 0xffffffff;
觸發超時重傳 lost = 1
// 觸發快速重傳 change++

更新慢啟動閾值和傳送視窗.
    if (change) {
// 如果有觸發快速重傳，ssthresh 設置為網絡上正在傳輸的數據包數量的一半
        IUINT32 inflight = kcp->snd_nxt - kcp->snd_una;
        kcp->ssthresh = inflight / 2;
        if (kcp->ssthresh < IKCP_THRESH_MIN)
            kcp->ssthresh = IKCP_THRESH_MIN;

將這段文字翻譯成繁體中文：

// 發送窗口為閾值再加上快速重傳相關的 resent
        kcp->cwnd = kcp->ssthresh + resent;
        kcp->incr = kcp->cwnd * kcp->mss;
    }

    if (lost) {
// 如果有超時重傳，觸發慢啟動，ssthresh 閾值為發送窗口的一半
        kcp->ssthresh = cwnd / 2;
        if (kcp->ssthresh < IKCP_THRESH_MIN)
            kcp->ssthresh = IKCP_THRESH_MIN;
將發送窗口重新設置為1，重新啟動慢啟動增長。
        kcp->cwnd = 1;
        kcp->incr = kcp->mss;
    }

    if (kcp->cwnd < 1) {
// 因為初始化為 0，來到這裡會再設置成 1
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
rmt_wnd represents the receive window size of the other party.
        kcp->rmt_wnd = wnd
        // ...
// 處理數據
    }

// 最後更新發送窗口
// kcp->snd_una - prev_una > 0，表示本次 input 有收到 ACK 而且發送緩衝 snd_buf 有變化
    if (_itimediff(kcp->snd_una, prev_una) > 0) {
// 再判斷對方的接收窗口
        if (kcp->cwnd < kcp->rmt_wnd) {
            IUINT32 mss = kcp->mss;

            if (kcp->cwnd < kcp->ssthresh) {
// 小於慢啟動閾值，雙倍增長
                kcp->cwnd++;
                kcp->incr += mss;

            }    else {
// 大於慢啟動閾值之後，通過公式更新 incr，進而計算 cwnd
                if (kcp->incr < mss) kcp->incr = mss;
                kcp->incr += (mss * mss) / kcp->incr + (mss / 16);
                if ((kcp->cwnd + 1) * mss <= kcp->incr) {
                    kcp->cwnd++;
                }
            }
更新出來的值還要再比較下 rmt_wnd
            if (kcp->cwnd > kcp->rmt_wnd) {
                kcp->cwnd = kcp->rmt_wnd;
                kcp->incr = kcp->rmt_wnd * mss;
            }
        }
    }
}
```
</details>

計算發送窗口 `kcp->cwnd` 的大小涉及的代碼片段會稍微多一些，因為在發送和接收數據的時候，都会需要更新。`kcp->cwnd` 初始化為 0，
之後會在第一次調用 `ikcp_flush` 的時候，判斷是否小於 1 ，若是則修改為 1。之後發送方根據發送窗口大小，發送相應數量的數據包，等待 ACK。
回复包。ACK 包在 `kcp->input` 中進行處理，`kcp->input` 中如果判斷有 ACK 包，並有清除發送緩衝中的發送數據包，說明有數據包已經完成送達，`kcp->cwnd++`。實際上很可能一次 `kcp->input` 只處理到一個 ACK 包，可以理解為，每收到一個 ACK 包都會有 `kcp->cwnd++`，這句自增實現的是翻倍的效果，例如當前 `kcp->cwnd = 2`，發送兩個數據包，收到兩個 ACK 包，觸發了兩次自增，最後就是 `kcp->cwnd = 4` 翻倍。

`cwnd` 可以持續指數增長，直到超過慢啟動閾值，或發生擁塞超時重傳、快速重傳的情況。發生超時重傳後，會觸發慢啟動，慢啟動閾值 `ssthresh = kcp->cwnd / 2`，發送窗口 `kcp->cwnd = 1`，回到最初重新指數增長。如果發生快速重傳，KCP 會先提前減少 `ssthresh`，也就是減少了 `cwnd` 指數增長的空間，降低增長速度，提前減緩擁塞的情況。

KCP 還增加了一個配置 `nocwnd`，當 `nocwnd = 1`，發送數據時不再考慮發送窗口大小，直接讓最大能發送的數量發送數據包，滿足高速模式下的要求。

##小結

本文簡單地分析了 KCP 的原始碼，並討論了 KCP 上 ARQ 的實現，以及一些 KCP 提升流速的策略。還有很多細節沒有提到，感興趣的可以自己翻 KCP 的原始碼對照著看，相信也能有不少的收穫。

--8<-- "footer_tc.md"


> 此篇文章是使用 ChatGPT 翻譯的，如有[**反饋**](https://github.com/disenone/wiki_blog/issues/new)指出任何遺漏之處。 
