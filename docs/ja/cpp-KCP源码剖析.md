---
layout: post
title: KCP コード解析
categories:
- c++
catalog: true
tags:
- dev
description: 本文は KCP のソースコードを簡単に分析し、KCP 上の ARQ の実装や KCP の流速を向上させるためのいくつかの戦略について議論しています。
figures: []
---

<meta property="og:title" content="KCP 源码剖析" />

この記事を読む前に、KCPについて聞いたことがない、またはKCPを全く理解していない場合は、少し時間を割いてKCPプロジェクトの説明文書を見てください：[伝送門](https://github.com/skywind3000/kcp)本文の目的は、KCP の実装の詳細を深く理解することです。

##KCPとは何ですか

KCP は、TCP よりも低遅延でデータを送信し、データ再送も速く、待ち時間も短くする信頼性の高いプロトコルです。

> TCPは帯域幅を有効活用するためにデザインされたもので、毎秒どれくらいのデータ（KB）を転送できるかが重要です。一方、KCPは送信元から送信先までの個々のデータパケットがどれくらいの時間を要するかに注力し、TCPよりも30%〜40%高速な転送速度を10%〜20%の帯域幅の無駄を払って得ています。TCPは流速は遅いけれども大容量の大運河であり、KCPは激しい小川のような速度を持っています。

以上は KCP 文書に書かれている内容で、キーワードは**帯域幅**と**流速**です。KCP は帯域幅を損失しますが、その利点はより大きく均等な伝送速度です。詳細については KCP 自身の文書を参照してください。

##KCP データ構造

KCPのソースコードは `ikcp.h` と `ikcp.c` にあります。`ikcp.h` では、データ構造の宣言が中心となっており、まずは KCP プロトコルがデータを処理する最小単位である `SEGMENT` パケットについて説明します。

<details>
<summary> SEGMENT 構造（クリックしてコードを展開） </summary>
```cpp
//=====================================================================
// セグメントとは、1つのデータパケットのことです。
//=====================================================================
struct IKCPSEG
{
// リストノード、送信および受信キューはここでのリストの構造です
    struct IQUEUEHEAD node;

// 会話番号、同じ会話番号は同じです
    IUINT32 conv;

// データパケットのタイプ、例えば DATA または ACK
    IUINT32 cmd;

MTU の制限により、大きなデータパケットは複数の小さなデータパケットに分割されます。これは小さなデータパケットの番号です。
    IUINT32 frg

すべてのデータパケットには、送信元の受信ウィンドウサイズが付属しています。
    IUINT32 wnd;

送信時刻、ACKパケットの場合は、元のデータパケットのtsに設定されます。
    IUINT32 ts;

// データパケットを一意に識別する番号
    IUINT32 sn;

// 代表小于 una 的データパケットはすべて受信成功で、TCPの意味と一致します：最も古い未確認シーケンス番号 SND
    IUINT32 una;

// データの長さ
    IUINT32 len;

超时重传时间
    IUINT32 resendts;

// 次回のタイムアウト待機時間
    IUINT32 rto;

// 高速再送信、受信したデータパケット以降のデータパケットの数が一定の数を超えると、高速再送信がトリガーされる。
    IUINT32 fastack;

送信回数
    IUINT32 xmit;

// データ
    char data[1];
};
```
</details>

`SEGMENT` のコメントを読み終わると、KCPの中核がARQプロトコルであり、データの到着を確実にするために自動的にタイムアウトして再送信することがわかります。続いて、KCP構造体`KCPCB`の定義を見てみましょう：

<details>
<summary> KCP 構造（クリックしてコード展開） </summary>
```cpp
//---------------------------------------------------------------------
// IKCPCB
//---------------------------------------------------------------------
struct IKCPCB
{
// conv: 会話番号
mtu、mss: Maximum Transmission Unit（最大伝送ユニット）、Maximum Segment Size（最大セグメントサイズ）
// state: 会議状態、0 有効、-1 切断
    IUINT32 conv, mtu, mss, state;

// snd_una: 等待 ACK 的包编号
// snd_nxt: 次に送信を待機しているデータパケットの番号
// rcv_nxt: The next sequence number of the data packet waiting to be received.
    IUINT32 snd_una, snd_nxt, rcv_nxt;

// ts_recent, ts_lastack: Unused
// ssthresh：Congestion Control Slow Start Threshold
    IUINT32 ts_recent, ts_lastack, ssthresh;

// rx_rto: rto（再送信タイムアウト）、タイムアウト再送信時間
// rx_rttval, rx_srtt, rx_minrto: RTOを計算するための中間変数
    IINT32 rx_rttval, rx_srtt, rx_rto, rx_minrto;

// snd_wnd, rcv_wnd: 最大小送りウィンドウと受信ウィンドウのサイズ
// rmt_wnd: リモートウィンドウ、相手の残り受信ウィンドウサイズ
// cwnd: 送信可能ウィンドウサイズ
// probe: Whether to send a control message flag.
    IUINT32 snd_wnd, rcv_wnd, rmt_wnd, cwnd, probe;

// 現在: 現在の時間
// インターバル: 更新間隔
// ts_flush: 次に更新が必要な時間
// xmit: 送信失敗回数
    IUINT32 current, interval, ts_flush, xmit;

リストの長さ
    IUINT32 nrcv_buf, nsnd_buf;
    IUINT32 nrcv_que, nsnd_que;

// nodelay: タイムアウト再送信の rto 増加速度を制御する
// updated: ikcp_update 関数をすでに呼び出しましたか
    IUINT32 nodelay, updated;

// ts_probe, probe_wait: 相手側の受信ウィンドウが長期間0のままの場合、定期的に問い合わせを積極的に行う
    IUINT32 ts_probe, probe_wait;

// deal_link: 相手が長時間応答しません
// incr: 送信ウィンドウサイズの計算に参加する
    IUINT32 dead_link, incr;

// queue: ユーザー層と接触するデータパケット
// buf: プロトコルのキャッシュされたデータパケット
    struct IQUEUEHEAD snd_queue;
    struct IQUEUEHEAD rcv_queue;
    struct IQUEUEHEAD snd_buf;
    struct IQUEUEHEAD rcv_buf;

// ack を送信する必要があるデータパケット情報
    IUINT32 *acklist;

必要な ack のパケット数
    IUINT32 ackcount;

// acklist 内存大小  ->  // バックリストのメモリサイズ
    IUINT32 ackblock;

// ユーザーから入力されたデータ
    void *user;

// kcp パケットの収納スペース
    char *buffer;

ファスタックによる急速再送信のトリガー回数
    int fastresend;

// 最大転送再送次数
    int fastlimit;

// nocwnd: Slow start ウィンドウサイズを考慮しない
stream: ストリーム
    int nocwnd, stream;

    // debug log
    int logmask;

データ送信インターフェース
    int (*output)(const char *buf, int len, struct IKCPCB *kcp, void *user);

    void (*writelog)(const char *log, struct IKCPCB *kcp, void *user);
};
```
</details>

KCPの構造内のフィールドコメントを一つずつ追加すると、KCPプロトコル全体がそれほど複雑でないことが初めて感じられます。コードを細かく分析すれば、あなたも私もKCPプロトコルを読んで理解することができます :smile:

##KCPのARQ実装

KCPは基本的にARQ（Auto Repeat-reQuest、自動再送信）プロトコルであり、信頼性のあるデータ転送を確保することが最も重要です。では、まずはKCPの基本的なARQ部分に焦点を当てて、KCPが信頼性のあるデータ転送をどのように実現しているかを考えてみましょう。

ARQとは、名前の通り、端末がデータパケットの受信に失敗したとき、該当するデータパケットを自動的に再送信することで、確実なデータ転送を実現する確認受信とタイムアウト再送信の2つのメカニズムを使用しています。具体的なコード実装では、KCPは各データパケット（前のセクションで言及された `SEGMENT`）に一意の `sn` 識別子を割り当てます。端末がデータパケットを受信すると、ACKパケット（同様に `SEGMENT`）が送信され、ACKパケットの `sn` は受信したデータパケットの `sn` と同じであり、このデータパケットの受信が成功したことが通知されます。`SEGMENT`にはさらに `una` フィールドがあり、次に期待されるデータパケットの番号を示しています。他の言葉で言えば、この番号よりも前にあるすべてのデータパケットがすでに受信されていることを意味し、あたかも完全なACKパケットのように、送信側は送信バッファと送信ウィンドウをより速く更新できます。

私たちは、KCPパケットの送信と受信コードを追跡することで、最も基本的なARQ実装を理解できます。

###送信

送信のプロセスは `ikcp_send` -> `ikcp_update` -> `ikcp_output` です。上位呼び出しは `ikcp_send` を使ってデータを KCP に送りますが、KCP は `ikcp_update` でデータの送信を処理します。

<details>
<summary>ikcp_send (click to expand code)</summary>
```cpp
//---------------------------------------------------------------------
// データ送信インターフェース、ユーザーは ikcp_send を呼び出して kcp にデータを送信させます
// user/upper level send, returns below zero for error
//---------------------------------------------------------------------
int ikcp_send(ikcpcb *kcp, const char *buffer, int len)
{
    IKCPSEG *seg;
    int count, i;

// mss must not be less than 1
    assert(kcp->mss > 0);
    if (len < 0) return -1;

    // append to previous segment in streaming mode (if possible)
    if (kcp->stream != 0) {
処理フローモード
        // ......
    }

データ長さが mss を超える場合は、パケットを分割して送信する必要があります。相手が受け取った後に再度組み立てます。
    if (len <= (int)kcp->mss) count = 1;
    else count = (len + kcp->mss - 1) / kcp->mss;

    if (count >= (int)IKCP_WND_RCV) return -2;

    if (count == 0) count = 1;

// 分包
    for (i = 0; i < count; i++) {
包のデータ長を計算し、対応するセグメント構造を割り当てます。
        int size = len > (int)kcp->mss ? (int)kcp->mss : len;
        seg = ikcp_segment_new(kcp, size);
        assert(seg);
        if (seg == NULL) {
            return -2;
        }

// segのデータ情報を設定します。frgはサブパッケージ番号を示します。
        if (buffer && len > 0) {
            memcpy(seg->data, buffer, size);
        }
        seg->len = size;
        seg->frg = (kcp->stream == 0)? (count - i - 1) : 0;

// snd_queue の末尾に追加し、nsnd_qua を1増やす
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

`ikcp_send` はKCPの上位レイヤーから呼び出されるデータ送信インタフェースであり、KCPに送信させるすべてのデータはこのインタフェースを介して行われます。 `ikcp_send` は非常に単純で、主な目的はデータを`kcp->mss`（1つのパケットの最大データ長）に基づいて複数のパケットに分割し、パケット番号を設定し、最後に送信キュー`snd_queue`の末尾に配置することです。 ストリームモードは、`ikcp_send`を複数回呼び出したデータをすべて1つのストリームとして扱い、まず未完了の`SEGMENT`を自動的に埋め、それから新しいものを割り当てます。 詳細な実装についてはこの文書では議論しませんが、興味がある方は、この文書を読み終えた後、コードを参照して理解できると信じています。

`ikcp_send`の呼び出しが完了すると、データはKCPの`snd_queue`に入れられます。その後、KCPは送信されるデータを送信するタイミングを見つける必要があります。この部分のコードはすべて`ikcp_update`と`ikcp_flush`に配置されています：

<details>
<summary> ikcp_update（クリックしてコードを展開） </summary>
```cpp
//---------------------------------------------------------------------
ikcp_updateは、定期的に呼び出される上位レイヤー向けのインタフェースであり、kcpの状態を更新しデータを送信するために使用されます。
// update state (call it repeatedly, every 10ms-100ms), or you can ask 
// ikcp_check when to call it again (without ikcp_input/_send calling).
// 'current' - current timestamp in millisec. 
//---------------------------------------------------------------------
void ikcp_update(ikcpcb *kcp, IUINT32 current)
{
    IINT32 slap;

    kcp->current = current;

// ikcp_flush はこれを確認します。上位層は ikcp_update を呼び出す必要があり、ikcp_flush を呼び出すことができます。ikcp_update のみを使用することをお勧めします。
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
次回のフラッシュ時刻
        kcp->ts_flush += kcp->interval;
        if (_itimediff(kcp->current, kcp->ts_flush) >= 0) {
            kcp->ts_flush = kcp->current + kcp->interval;
        }
        ikcp_flush(kcp);
    }
}
```
</details>

`ikcp_update` が行うことは非常に簡単で、`ts_flush` の時間を確認し、条件が満たされる場合は`ikcp_flush`を呼び出します。メインの処理ロジックは主に`ikcp_flush`にあるため、`ikcp_flush`の内容が少し複雑なので、現時点ではARQ送信に関連する部分に焦点を当てています：

<details>
<summary> データを送信する（コードを展開するにはクリック） </summary>
```cpp
//---------------------------------------------------------------------
// ikcp_flush
//---------------------------------------------------------------------
void ikcp_flush(ikcpcb *kcp)
{
    IUINT32 current = kcp->current;

// buffer is the data to be passed to ikcp_output, initialized to 3 times the packet size.
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

// seg.wndは現在受信可能なウィンドウサイズを示します。
    seg.wnd = ikcp_wnd_unused(kcp);
    seg.una = kcp->rcv_nxt;
    seg.len = 0;
    seg.sn = 0;
    seg.ts = 0;

// ackを送信
送信ウィンドウを計算します。
    //...

snd_queue から snd_buf にデータパケットを移動します。
移動するには送信ウィンドウのサイズを満たす必要があります。送信ウィンドウがいっぱいになると移動が停止します。
夢中の snd_buf に入れたデータは、直接 ikcp_output を呼び出して対向に送信できるデータです。
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

// seg 唯一序号は実際には kcp->snd_nxt の増加したものです。
        newseg->sn = kcp->snd_nxt++;

// ここで una を設定し、対側に次の受信待ちのパケット番号を通知します。
        newseg->una = kcp->rcv_nxt;
        newseg->resendts = current;
        newseg->rto = kcp->rx_rto;
        newseg->fastack = 0;
        newseg->xmit = 0;
    }

// クイックリカバリーフラグ、タイムアウト待ち時間を計算します。
    // ...

// 送信snd_buf
    for (p = kcp->snd_buf.next; p != &kcp->snd_buf; p = p->next) {
        IKCPSEG *segment = iqueue_entry(p, IKCPSEG, node);
        int needsend = 0;
        if (segment->xmit == 0) {
初めて送信
// set->xmit 表示发送次数
// 超時再送信の待ち時間
            needsend = 1;
            segment->xmit++;
            segment->rto = kcp->rx_rto;
            segment->resendts = current + segment->rto + rtomin;
        }
        else if (_itimediff(current, segment->resendts) >= 0) {
// タイムアウト再送
            // ...
        }
        else if (segment->fastack >= resent) {
クイックリトランスミッション
            // ...
        }

        if (needsend) {
            int need;
            segment->ts = current;
            segment->wnd = seg.wnd;
            segment->una = kcp->rcv_nxt;

            size = (int)(ptr - buffer);
            need = IKCP_OVERHEAD + segment->len;

// バッファ内のデータが mtu を超えるたびに、まず送信し、できるだけ下層での分割を避ける。
            if (size + need > (int)kcp->mtu) {
                ikcp_output(kcp, buffer, size);
                ptr = buffer;
            }

// segの制御データをbufferにコピーし、KCPが自動的にエンディアンの問題を処理する
            ptr = ikcp_encode_seg(ptr, segment);

// データを再コピー
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

ssthreshを計算し、慢性窓口を更新します。
    // ...
}
```
</details>

私たちは現在、`ikcp_flush` 内の送信データに関するロジックにのみ注目しています：

まず、KCPは相手の受信ウィンドウのサイズに基づいて、`snd_queue`上のデータを`snd_buf`に移動させます。移動数の計算式は`num = snd_nxt - (snd_una + cwnd)`です。つまり、成功裏に送信された最大パケットシーケンス番号`snd_una`にスライディングウィンドウのサイズ`cwnd`を足したものが次に送信待ちのパケットシーケンス番号`snd_nxt`を上回った場合、新しいデータパケットを送信し続けることができます。`SEG`を移動させる際に、制御フィールドを設定します。

`snd_buf`を遍歴し、データパケットを送信する必要がある場合は、データを`buffer`にコピーし、コピーの際に`ikcp_encode_seg`を使って制御フィールドのデータのエンドiannessの問題を処理します。

* 最後に `ikcp_output` を呼び出して `buffer` のデータを送信します。

これにより、KCPはデータの送信を完了しました。

###取りまとめ

受信のプロセスは送信と逆です：`ikcp_input` -> `ikcp_update` -> `ikcp_recv`。ユーザーがネットワークからデータを受信した後、`ikcp_input` を呼び出してKCPに渡し、`ikcp_update` を呼び出すと送信元にACKパケットを返します。上位レイヤーは`ikcp_recv` を呼び出して、KCPに解析されたデータを受信します。

<details>
<summary> データを受信する（クリックしてコードを展開） </summary>
```cpp
//---------------------------------------------------------------------
// input data
//---------------------------------------------------------------------
int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    IUINT32 prev_una = kcp->snd_una;
    IUINT32 maxack = 0, latest_ts = 0;
    int flag = 0;

// 合法性チェック
    if (data == NULL || (int)size < (int)IKCP_OVERHEAD) return -1;

// data can be multiple KCP packets, handle them in a loop
    while (1) {
        IUINT32 ts, sn, len, una, conv;
        IUINT16 wnd;
        IUINT8 cmd, frg;
        IKCPSEG *seg;

// KCPパッケージに満たないため、退出します
        if (size < (int)IKCP_OVERHEAD) break;

// まず、制御フィールドを解析します
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

// データパッケージタイプチェック
        if (cmd != IKCP_CMD_PUSH && cmd != IKCP_CMD_ACK &&
            cmd != IKCP_CMD_WASK && cmd != IKCP_CMD_WINS) 
            return -3;

        kcp->rmt_wnd = wnd;

ここでの "una" は送信元の kcp->rcv_nxt です。このデータに基づいて、確認済みのデータパケットを削除することができます。
        ikcp_parse_una(kcp, una);
受信確認済みのパケットを除いた後、snd_unaを更新して、次に送信するシーケンス番号を設定します。
        ikcp_shrink_buf(kcp);

        if (cmd == IKCP_CMD_ACK) {
// ack パッケージ
            // ...
        }
        else if (cmd == IKCP_CMD_PUSH) {
// データパケット
// 受信したデータパケットのシーケンス番号 sn が受信ウィンドウ内であれば、正常に処理します。それ以外の場合は直接破棄し、再送信を待ちます。
            if (_itimediff(sn, kcp->rcv_nxt + kcp->rcv_wnd) < 0) {

受信したすべてのデータパケットには、ACKパケットを返信し、記録してください。
                ikcp_ack_push(kcp, sn, ts);

// Received data is processed by calling ikcp_parse_data.
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
// クエリウィンドウパッケージ
            // ...
        }
        else if (cmd == IKCP_CMD_WINS) {
// 返信パケットの検索窓口
            // ...
        }
        else {
            return -3;
        }

        data += len;
        size -= len;
    }

// 高速再送信ロジックを処理する
    // ...

// ウィンドウを更新する
    // ...

    return 0;
}
```
</details>

`ikcp_input` は各`SEG`パッケージを処理します。まずパッケージの正当性と種類をチェックします。各データパッケージには`una`が含まれており、送信元が受信を待機しているパッケージ番号が格納されています。`una`よりも小さな番号のパッケージは相手側にすでに正常に受信されている必要があります。したがって、`snd_buff`から`una`より小さいパッケージを削除し、`snd_nxt`を更新する必要があります。この処理は`ikcp_parse_una`と`ikcp_shrink_buf`が担当します。受信した各データパッケージにはACKパッケージを返信する必要があり、これは`ikcp_ack_push`によって記録され、最後に`ikcp_parse_data`でデータが処理されます。

<details>
<summary>データを分析する（コードを展開する）</summary>
```cpp
void ikcp_parse_data(ikcpcb *kcp, IKCPSEG *newseg)
{
    struct IQUEUEHEAD *p, *prev;
    IUINT32 sn = newseg->sn;
    int repeat = 0;

// シリアルナンバーチェック
    if (_itimediff(sn, kcp->rcv_nxt + kcp->rcv_wnd) >= 0 ||
        _itimediff(sn, kcp->rcv_nxt) < 0) {
        ikcp_segment_delete(kcp, newseg);
        return;
    }

// newseg を配置すべき位置を見つける。受信した seg は順不同の可能性があるため。
    for (p = kcp->rcv_buf.prev; p != &kcp->rcv_buf; p = prev) {
        IKCPSEG *seg = iqueue_entry(p, IKCPSEG, node);
        prev = p->prev;
        if (seg->sn == sn) {
// 受信済
            repeat = 1;
            break;
        }
        if (_itimediff(sn, seg->sn) > 0) {
            break;
        }
    }

// newseg を rcv_buf の正しい位置に置く
    if (repeat == 0) {
        iqueue_init(&newseg->node);
        iqueue_add(&newseg->node, p);
        kcp->nrcv_buf++;
    }    else {
        ikcp_segment_delete(kcp, newseg);
    }

// rcv_buf から rcv_queue へデータを移動する
    while (! iqueue_is_empty(&kcp->rcv_buf)) {
        IKCPSEG *seg = iqueue_entry(kcp->rcv_buf.next, IKCPSEG, node);
// もし、segの番号が受信待ちの番号ならば、rcv_queueに移動します。
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

`ikcp_parse_data` の主要な仕事は`newseg`を`kcp->rcv_buf`内の適切な位置に配置し、データを`rcv_buf`から`rcv_queue`に移動することです。`rcv_buf`内の適切な位置とは、`rcv_buf`が`sn`の昇順に並んでいることを意味し、`newseg`は自身の`sn`のサイズに合わせて適切な位置を検索する必要があります。`rcv_buf`のデータを`rcv_queue`に移動させる条件は、`rcv_buf`上のデータパケット番号がKCPが受信を待っているパケット番号`kcp->rcv_nxt`に等しい場合です。データパケットを1つ移動した後は、`kcp->rcv_nxt`を更新してから次のデータパケットを処理する必要があります。

`ikcp_input` の後、上位の呼び出しが `ikcp_update` を行うと、ACK パケットが送信され、`ikcp_recv` を呼び出すと、有効なデータが上位に返されます。`ikcp_update` と `ikcp_recv` は互いに独立しており、呼び出しの順序は要求されません。それは上位の呼び出しのタイミングによります。まずは、ACK 送信に関連する部分を持つ `ikcp_update` を見てみましょう。

<details>
<summary>返信 ACK（コードを開くにはクリック）</summary>
```cpp
前述の通り、ikcp_update は最終的に ikcp_flush を呼び出します。
void ikcp_flush(ikcpcb *kcp, IUINT32 current)
{
    // ...

// ACK パッケージを返信する
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

ACKパケットはすでに`ikcp_ack_push`によって保存されているため、ここでは`ikcp_ack_get`を使用して各ACKパケットの情報を取得し、相手に送信するだけです。上位層は`ikcp_recv`を使用してKCPからデータを取得できます：

<details>
<summary>ikcp_recv（クリックしてコードを展開）</summary>
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

一部分の有効性チェック
    if (iqueue_is_empty(&kcp->rcv_queue))
        return -1;
    if (len < 0) len = -len;

返却可能なデータ長を計算します。
    peeksize = ikcp_peeksize(kcp);

    if (peeksize < 0)
        return -2;
    if (peeksize > len)
        return -3;

// 受信ウィンドウの判定
    if (kcp->nrcv_que >= kcp->rcv_wnd)
        recover = 1;

// rcv_queueをループして、データをbufferにコピーします
    for (len = 0, p = kcp->rcv_queue.next; p != &kcp->rcv_queue; ) {
        int fragment;
        seg = iqueue_entry(p, IKCPSEG, node);
        p = p->next;

        if (buffer) {
            memcpy(buffer, seg->data, seg->len);
            buffer += seg->len;
        }

        len += seg->len;

// 分包判断
        fragment = seg->frg;

データパケットを削除します。
        if (ispeek == 0) {
            iqueue_del(&seg->node);
            ikcp_segment_delete(kcp, seg);
            kcp->nrcv_que--;
        }

// 所有のパッケージがコピーされるまでループを終了する。
        if (fragment == 0)
            break;
    }

    assert(len == peeksize);

// rcv_queue がさらに空いたので、rcv_buf から rcv_queue にデータを移動しようとしています。
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

`ikcp_recv` の一次呼び出しは、1 つの完全なデータパケットのみを返します。上位層は、データが戻らなくなるまでループ呼び出しをすることができます。この関数のロジックは比較的単純で、`rcv_queue` からデータを上位層から渡された `buffer` にコピーするだけです。これにより、受信者は受信したデータパケットの処理が完了しました。

受信者がデータパケットを処理する際、送信者にACKパケットを送信しました。次に、送信者がACKパケットを受け取る処理を見てみましょう：

<details>
<summary> ACKパケットの処理（コードを展開するにはクリック） </summary>
```cpp
int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    // ...
    IUINT32 maxack = 0, latest_ts = 0;
    // ...
    while (1) {
        // ...
// ts は対端の kcp-> current です
        data = ikcp_decode32u(data, &ts);
        data = ikcp_decode32u(data, &sn);

        if (cmd == IKCP_CMD_ACK) {
// 更新 rot
            if (_itimediff(kcp->current, ts) >= 0) {
                ikcp_update_ack(kcp, _itimediff(kcp->current, ts));
            }
// Update snd_buf
            ikcp_parse_ack(kcp, sn);
            ikcp_shrink_buf(kcp);

// maxack = 今回の入力のすべてのACKパケットの中で最大のsn
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

// ACKパケットを受信した場合、すばやい再送のために記録する
    if (flag != 0) {
        ikcp_parse_fastack(kcp, maxack, latest_ts);
    }
}
```
</details>

ACKパケットを受信すると同様に、`ikcp_parse_ack`と`ikcp_shrink_buf`を使って`snd_buf`を更新する必要があります。また、`ikcp_update_ack`を呼び出してRTO（再送信タイムアウト）を計算して更新する必要があります。`ikcp_input`では受け取ったACKパケットの最大シーケンス番号を計算し、快速再送信のために記録します。こうして、送信者はACKパケットを受け取り、送信データを`snd_buf`から削除し、そのデータパケットは受信者に確実に届き、一連のARQ確認受信プロセスが終了します。

###再送信

前面紹介したのは、KCPが実装したARQの確認受信メカニズムです。ARQは信頼性を保証するためにタイムアウト再送も必要です。次に、KCPがどのようにタイムアウト再送を行っているのか見ていきましょう。

私たちは `ikcp_flush` 関数に戻りましょう：

<details>
This text is written in HTML markup language which cannot be translated.
```cpp
void ikcp_flush(ikcpcb *kcp)
{
    // ...
// 送信 snd_buf
    for (p = kcp->snd_buf.next; p != &kcp->snd_buf; p = p->next) {
        IKCPSEG *segment = iqueue_entry(p, IKCPSEG, node);
        int needsend = 0;
        if (segment->xmit == 0) {
初回送信
            needsend = 1;
            segment->xmit++;
// セグメント->rtoを設定する
// segment->rto を使用して segment->resendts のタイムアウト再送信時間を計算する
            segment->rto = kcp->rx_rto;
            segment->resendts = current + segment->rto + rtomin;
        }
        else if (_itimediff(current, segment->resendts) >= 0) {
// タイムアウト再送
            needsend = 1;
            segment->xmit++;
            kcp->xmit++;
// nodelay は次回のタイムアウト再送時間の計算を制御します
            if (kcp->nodelay == 0) {
                segment->rto += kcp->rx_rto;
            }    else {
                segment->rto += kcp->rx_rto / 2;
            }
            segment->resendts = current + segment->rto;
            lost = 1;
        }
        else if (segment->fastack >= resent) {
// 高速再送
            // ...
        }
        if (needsend) {
// データを送信
            // ...
        }
    // ...
}
```
</details>

一旦現在の時間 `current` が `segment->resendts` を超えると、タイムアウト再送信時間を意味し、この期間中に受信側からの ACK パケットを一切受信していないことを示します。この状況でタイムアウト再送信メカニズムが発動し、`needsend = 1` となります。データを再送信します。

確認受信とタイムアウト再送機能が整ったことで、KCPは基本的な信頼性のあるデータ転送を保証できます。しかし、より安定したデータ流速を維持するために、KCPはさらに多くの工夫を行っています。以下で、KCPが行ったその他の最適化について見ていきましょう。

##KCPの流速向上戦略

###高速再送信

送信者は、`sn` と `sn + 1` のシーケンス番号を持つ2つのデータパケットを送信しました。`sn + 1` の ACK パケットのみを受信した場合、`sn` の ACK パケットがまだネットワーク上に到達していないか、ACK パケットが紛失した可能性があります。また、`sn` のデータパケットが紛失したかもしれません。この時点でまだ再送のタイムアウトが発生しておらず、ネットワークが混み合っていない場合、一定の理由による急なパケット紛失のため、送信者が自ら `sn` のデータパケットを事前に送信することで、受信者がデータをより速く受信し、スループットを向上させることができます。

KCP内では、高速再送機構も実装されており、`ikcp_flush`内でも処理されています。

<details>
<summary>Fast Retransmission (Click to Expand Code)</summary>
```cpp
void ikcp_flush(ikcpcb *kcp)
{
    // ...
    resent = (kcp->fastresend > 0)? (IUINT32)kcp->fastresend : 0xffffffff;

// 送信 snd_buf
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
// 高速再送
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
// データを送信
            // ...
        }
    // ...
}
```
</details>

早急に再送信する必要があります。2つの条件があります：
* `segment->fastack >= resent`、resentは設定可能なパラメータ`kcp->fastresend`で、0に設定すると迅速な再送信が無効になります。`segment->fastack`は関数`ikcp_parse_fastack`内で設定され、この関数は`ikcp_input`内で呼び出され、`ikcp_input`で算出された`maxack`に基づいて、すべての`sn`が`maxack`より小さい`segment->fastack`を1増やします。したがって、`segment->fastack`は、`sn`より大きいパケットを受け取った回数を示しています。
`segment->xmit <= kcp->fastlimit || kcp->fastlimit <= 0`は、`setgment->xmit`が送信回数、`kcp->fastlimit`が設定可能な最大高速再送回数であり、送信回数は最大高速再送回数より小さい必要があります。

一旦上述条件满足，KCP 就会执行快速重传。需要注意的是，快速重传并不会重置超时重传时间，原来的超时时间仍然有效。

###タイムアウト再送信時間を短縮する

超時再送は素晴らしいメカニズムですが、ただ時間がかかりすぎますね。TCPの戦略に従うと、毎回の超時再送時間が倍増し、待ち時間が非常に速く膨張します。待機時間中に、受信側の受信ウィンドウが枯渇して新しいデータを受信できないことが非常にあります。再送信を待っているパケット番号は最初にあり、受信側は再送信パケットを受信して初めてすべてのデータを上位層に返すことが可能です。このような状況では、ネットワーク全体のフローはほぼゼロになりますね。KCPは待機時間の増加を緩和するための構成を追加しています。そして、倍々にならないので、`kcp->nodelay`を通じて、待機時間は毎回、RTOの倍またはRTOの0.5倍のみ増加するよう制御できます。待ち時間の増加を効果的に緩和し、ネットワークの速度ができるだけ早く回復するのを支援します。

###更新送信ウィンドウ

送信ウィンドウは同時に送信されるデータパケット数を示しています。ウィンドウが大きいほど、同時に送信されるデータが多くなり、データの流れも速くなりますが、ウィンドウが大きすぎるとネットワークが混雑し、パケットロスが増加し、データの再送信が多くなり、データの流れも遅くなります。したがって、送信ウィンドウはネットワークの状況に応じて常に更新され、最適な状態に徐々に近づけられる必要があります。KCPにおける送信ウィンドウに関するコード：

<details>
<summary>送信ウィンドウ（コードを展開するにはクリック）</summary>
```cpp
ikcpcb* ikcp_create(IUINT32 conv, void *user)
{
    // ...
// snd_wnd、rcv_wndは送信と受信用のバッファサイズです。
    kcp->snd_wnd = IKCP_WND_SND;    // 32
    kcp->rcv_wnd = IKCP_WND_RCV;    // 128
// 対端受信ウィンドウサイズ              // 128
    kcp->rmt_wnd = IKCP_WND_RCV
// 送信ウィンドウ cwnd 初期化 0
    kcp->cwnd = 0;
// 送信ウィンドウのバイト数のサイズ、cwnd の計算に参加します
    kcp->incr = 0
// スロースタート閾値、slow start threshold
    kcp->ssthresh = IKCP_THRESH_INIT;
// nocwnd は設定可能なパラメータで、1 は cwnd を考慮しないことを意味します。
    kcp->nocwnd = 0;
    // ...
}

void ikcp_flush(ikcpcb *kcp)
{
    // ...
// データを送信する際は、送信ウィンドウサイズを計算します。これは、送信バッファサイズと相手の受信ウィンドウサイズの小さい方の値です。
    cwnd = _imin_(kcp->snd_wnd, kcp->rmt_wnd);
// デフォルトでは kcp->cwnd、つまり常に更新される送信ウィンドウも考慮する必要があります
    if (kcp->nocwnd == 0) cwnd = _imin_(kcp->cwnd, cwnd);

// cwnd のサイズに基づいて、snd_queue を snd_buf に移動する
    while (_itimediff(kcp->snd_nxt, kcp->snd_una + cwnd) < 0) {
    }
データ送信
    resent = (kcp->fastresend > 0)? (IUINT32)kcp->fastresend : 0xffffffff;
// タイムアウト再送信をトリガー lost = 1
// クイック再送信をトリガー change++

// スロースタート閾値と送信ウィンドウを更新
    if (change) {
もし急速リトランスミッションが発生した場合、ssthresh は現在ネットワーク上を伝送中のデータパケット数の半分に設定されます。
        IUINT32 inflight = kcp->snd_nxt - kcp->snd_una;
        kcp->ssthresh = inflight / 2;
        if (kcp->ssthresh < IKCP_THRESH_MIN)
            kcp->ssthresh = IKCP_THRESH_MIN;

//送信ウィンドウのしきい値に再送関連の高速再送を加えたもの
        kcp->cwnd = kcp->ssthresh + resent;
        kcp->incr = kcp->cwnd * kcp->mss;
    }

    if (lost) {
// タイムアウト再送が発生した場合、スロースタートをトリガーし、ssthreshの閾値は送信ウィンドウの半分です
        kcp->ssthresh = cwnd / 2;
        if (kcp->ssthresh < IKCP_THRESH_MIN)
            kcp->ssthresh = IKCP_THRESH_MIN;
// ウィンドウを 1 に戻し、再びスロースタートを開始する
        kcp->cwnd = 1;
        kcp->incr = kcp->mss;
    }

    if (kcp->cwnd < 1) {
// 初期値が 0 なので、ここに来たときに 1 に再設定されます。
        kcp->cwnd = 1;
        kcp->incr = kcp->mss;
    }
}

int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    IUINT32 prev_una = kcp->snd_una;
受信データの処理

    while (1) {
        // ...
        data = ikcp_decode16u(data, &wnd)
// rmt_wnd is the size of the recipient's receiving window
        kcp->rmt_wnd = wnd
        // ...
データ処理
    }

// 最後に更新した送信ウィンドウ
// kcp->snd_una - prev_una > 0 の場合、これは今回の入力が ACK を受信し、送信バッファ snd_buf に変化があったことを示します。
    if (_itimediff(kcp->snd_una, prev_una) > 0) {
相手の受信ウィンドウを再評価してください。
        if (kcp->cwnd < kcp->rmt_wnd) {
            IUINT32 mss = kcp->mss;

            if (kcp->cwnd < kcp->ssthresh) {
// スロースタートの閾値未満で、倍増
                kcp->cwnd++;
                kcp->incr += mss;

            }    else {
慢スタートしきい値を超えた後、式を使用してincrを更新し、その後cwndを計算します。
                if (kcp->incr < mss) kcp->incr = mss;
                kcp->incr += (mss * mss) / kcp->incr + (mss / 16);
                if ((kcp->cwnd + 1) * mss <= kcp->incr) {
                    kcp->cwnd++;
                }
            }
// 更新できる値は、再度 rmt_wnd を比較する必要があります。
            if (kcp->cwnd > kcp->rmt_wnd) {
                kcp->cwnd = kcp->rmt_wnd;
                kcp->incr = kcp->rmt_wnd * mss;
            }
        }
    }
}
```
</details>

送信ウィンドウ `kcp->cwnd` のサイズを計算するコード断片は少し長くなります。データ送信と受信の両方で更新が必要だからです。`kcp->cwnd` は0で初期化されます。
`ikcp_flush` が最初に呼び出された際、値が1未満の場合、1に変更されます。その後、送信者は送信ウィンドウサイズに基づいて、対応するデータパケットを送信し、ACKを待ちます。
返信パケット。ACKパケットは`kcp->input`で処理され、`kcp->input`内にACKパケットが存在し、送信バッファ内の送信データパケットをクリアする条件が整った場合、データパケットが既に到達したことを示しており、`kcp->cwnd++`が実行されます。実際には、1回の`kcp->input`で処理されるACKパケットは1つだけの可能性が高く、つまり、ACKパケットを受け取るごとに`kcp->cwnd++`が行われることが理解できます。このインクリメントの実装は倍増効果を持ち、例えば現在の`kcp->cwnd = 2`の状態で、2つのデータパケットを送信し、2つのACKパケットを受信した場合、2回のインクリメントが発生し、最終的に`kcp->cwnd = 4`となり、倍増します。

`cwnd` can continue to grow exponentially until it exceeds the slow start threshold or congestion timeout retransmission, in the case of fast retransmission. After a timeout retransmission occurs, it triggers slow start. The slow start threshold `ssthresh = kcp->cwnd / 2`, the send window `kcp->cwnd = 1`, returning to the initial exponential growth. If fast retransmission occurs, KCP first reduces `ssthresh` in advance, which reduces the space for exponential growth of `cwnd`, slows down the growth rate, and preemptively alleviates congestion.

KCPには、`nocwnd`という構成が追加されました。`nocwnd = 1`の場合、データ送信時に送信ウィンドウサイズを考慮しないで、最大送信可能数のデータパケットを直接送信し、高速モードの要件を満たします。

##小结の翻訳は「小結」になります。

本文では、KCPのソースコードを簡単に分析し、KCPでのARQの実装とKCPの帯域幅向上策を議論しています。触れられていない詳細部分も多くありますが、興味のある方はKCPのソースコードを参照しながら自分で確認してみてください。きっと多くの知見が得られるでしょう。

--8<-- "footer_ja.md"


> この投稿はChatGPTを使って翻訳されました。フィードバックは[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)どんな抜け漏れも指摘してください。 
