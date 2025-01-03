---
layout: post
title: KCP マスタリングソースコード
categories:
- c++
catalog: true
tags:
- dev
description: 本文は、KCPのソースコードを簡単に分析し、KCPでのARQの実装とKCPのスループット向上策について議論しています。
figures: []
---

<meta property="og:title" content="KCP 源码剖析" />

この文章を読む前に、KCPという言葉を聞いたことがないか、KCPについて全く知らない方は、少し時間を取ってKCPプロジェクトの説明文書を読んでみてください：[リンク](https://github.com/skywind3000/kcp)本文の目的は、KCP の実装の詳細に踏み込んで KCP を理解することです。

##KCP とは何ですか。

KCP は、TCP よりも低遅延でデータを送信し、データの再送も速く、待機時間が短い信頼性の高いプロトコルです。

> TCPは、トラフィックに適した設計です（一秒間にどれだけのデータを転送できるか）、帯域幅の効果的な利用に重点を置いています。一方、KCPは、速度に適した設計です（一つのデータパケットを一端から他端まで送るのにかかる時間）、TCPよりも30％〜40%速い転送速度を得るために、10％〜20%の帯域幅の無駄を払っています。TCPチャンネルは、流速は遅いが毎秒のトラフィック量が多い大きな運河になりますが、KCPは急流のような速い小川になります。

上記はKCPのドキュメントに記載されている内容で、キーワードは**帯域幅**と**フローサイズ**です。KCPは帯域幅を消費しますが、利点としてはより大きくより均等な転送速度をもたらします。詳細はKCPの公式ドキュメントをご参照ください。

##KCPデータ構造

KCPのソースコードは、`ikcp.h`と`ikcp.c`にあります。`ikcp.h`では、まず`SEGMENT`データパケットが宣言されており、これはKCPプロトコルがデータを処理する際の最小単位です。

<details>
<summary> SEGMENT structure (click to expand code) </summary>
```cpp
//=====================================================================
// 一个 SEGMENT 就是一个数据包
//=====================================================================
struct IKCPSEG
{
// リンクリストのノード、送信および受信キューはここでのリンクリストの構造です
    struct IQUEUEHEAD node;

同じ会話IDは同じです
    IUINT32 conv;

データパケットのタイプ、たとえばデータまたはACK
    IUINT32 cmd;

MTU制限のため、大きなデータパケットは複数の小さなデータパケットに分割され、これが小さなデータパケットの番号です。
    IUINT32 frg

すべてのデータパケットには、送信側の受信ウィンドウサイズが付属します。
    IUINT32 wnd;

送信時刻、ACK パケットの場合は元のデータパケットの ts に設定されます。
    IUINT32 ts;

データパケットを一意に識別するための番号
    IUINT32 sn;

unaの値未満のデータパケットはすべて正常に受信されました。これはTCPでいう「oldest unacknowledged sequence number (最も古い未確認シーケンス番号) SND」と同等です。
    IUINT32 una;

データ長
    IUINT32 len;

超時重送時間
    IUINT32 resendts;

// Next timeout waiting time
    IUINT32 rto;

このテキストを日本語に翻訳します:

    // ファストリトランスミッション。このデータパケットの後に受信したデータパケットの数が一定数を超えると、ファストリトランスミッションが発生します。
    IUINT32 fastack;

送信回数
    IUINT32 xmit;

// データ
    char data[1];
};
```
</details>

`SEGMENT` の注釈を確認すると、KCPのコアがARQプロトコルであることが大体分かります。データの到達を確実にするために自動的に再送信が行われます。次に、KCP構造`KCPCB`の定義を見てみましょう：

<details>
<summary> KCP 構造（コードを展開するにはクリック） </summary>
```cpp
//---------------------------------------------------------------------
// IKCPCB
//---------------------------------------------------------------------
struct IKCPCB
{
// conv: 会話番号
mtuとmssは、最大転送ユニットと最大メッセージセグメントサイズを意味します。
// state: 会话の状態、0 は有効、-1 は切断
    IUINT32 conv, mtu, mss, state;

// snd_una: The sequence number of the packet waiting for ACK.
// snd_nxt: The next sequence number of data packet waiting to be sent.
// rcv_nxt: The next sequence number of the data packet ready to be received.
    IUINT32 snd_una, snd_nxt, rcv_nxt;

// ts_recent, ts_lastack: Not used
ssthresh: 拥塞制御のスロースタート閾値
    IUINT32 ts_recent, ts_lastack, ssthresh;

// rx_rto: rto (retransmission timeout)，超时重传时间
// rx_rto：rto（再送信タイムアウト），再送信のタイムアウト時間
// rx_rttval, rx_srtt, rx_minrto: Variables used to calculate the intermediate value of the retransmission timeout (rto).
    IINT32 rx_rttval, rx_srtt, rx_rto, rx_minrto;

// snd_wnd, rcv_wnd: Maximum size of the send and receive windows.
// rmt_wnd: リモートウィンドウ、対向端の残り受信ウィンドウサイズ
// cwnd: 可发送窗口大小
// プローブ: 制御メッセージを送信するかどうかのフラグ
    IUINT32 snd_wnd, rcv_wnd, rmt_wnd, cwnd, probe;

// current: 現在時刻
// interval: 更新間隔
ts_flush: 次回更新が必要な時間
// xmit: 送信失敗回数
    IUINT32 current, interval, ts_flush, xmit;

// リストの長さ
    IUINT32 nrcv_buf, nsnd_buf;
    IUINT32 nrcv_que, nsnd_que;

// nodelay: Controlling the growth rate of RTO for timeout retransmission.
// updated: ikcp_update が呼び出されたかどうか
    IUINT32 nodelay, updated;

// ts_probe, probe_wait: Initiates regular inquiries when the receiving window of the remote end remains 0 for a long time.
    IUINT32 ts_probe, probe_wait;

// deal_link: 対向端末からの応答が長時間ない
// incr: 参与計算送信ウィンドウサイズ
    IUINT32 dead_link, incr;

// queue: ユーザーレベルでのパケット接触
// buf: プロトコルのキャッシュされたデータパケット
    struct IQUEUEHEAD snd_queue;
    struct IQUEUEHEAD rcv_queue;
    struct IQUEUEHEAD snd_buf;
    struct IQUEUEHEAD rcv_buf;

ack の送信が必要なデータパケット情報
    IUINT32 *acklist;

需要 ack 的包数量
    IUINT32 ackcount;

// ブラックリスト内のメモリサイズ
    IUINT32 ackblock;

以下のテキストを日本語に翻訳してください：

    // 用户层传进来的数据
    void *user;

kcp パケットを保持するスペース
    char *buffer;

// ファーストアップ回数、クイックリトランスミッションをトリガー
    int fastresend;

高速再送信の最大回数
    int fastlimit;

// nocwnd: 慢スタートしない送信ウィンドウのサイズを考慮しない
// stream: ストリーム
    int nocwnd, stream;

    // debug log
    int logmask;

// データ送信インターフェース
    int (*output)(const char *buf, int len, struct IKCPCB *kcp, void *user);

    void (*writelog)(const char *log, struct IKCPCB *kcp, void *user);
};
```
</details>

KCPの構造内のフィールドコメントを一つ一つ追加すると、KCPプロトコル全体がそれほど複雑でないことが最初に感じられますね。コードを注意深く分析すれば、あなたも私もKCPプロトコルを読んで理解できるでしょう :smile:

##KCPのARQ実装

KCPは本質的にARQ（Auto Repeat-reQuest、自動再送信）プロトコルであり、信頼性のある転送を確保することが最も基本的です。ですので、ますはKCPの基本的なARQ部分に焦点を当てて、KCPがどのように信頼性のある転送を実現しているのかを考えてみましょう。

ARQは、その名が示す通り、対端がデータパケットの受信に失敗した場合、自動的に該当するデータパケットを再送信する仕組みであり、受信確認とタイムアウト再送信の2つのメカニズムを使用して信頼性のある通信を実現しています。具体的なコード実装では、KCPは各データパケット（前述の「SEGMENT」）に一意の「sn」識別子を割り当て、対端がデータパケットを受信すると、受信に成功したことを通知するACKパケット（同じく「SEGMENT」）を返信します。ACKパケットの「sn」は受信したデータパケットの「sn」と同じであり、残りの受信待ちの次のデータパケットの番号を示す「una」フィールドが「SEGMENT」にもあります。つまり、この番号より前にあるすべてのデータパケットが受信済みであることを示し、ACKパケット全体と同等の効果があり、送信側は送信バッファと送信ウィンドウをより速く更新できます。

KCPパケットの送受信コードを追跡することで、最も基本的なARQ実装を理解することができます：

###送信

送信のプロセスは `ikcp_send` -> `ikcp_update` -> `ikcp_output` であり、上位層は `ikcp_send` を呼び出してデータをKCPに渡し、KCPは`ikcp_update`でデータの送信処理を行います。

<details>
ikcp_send（クリックしてコードを展開）
```cpp
//---------------------------------------------------------------------
データインターフェースを送信し、ユーザーはikcp_sendを呼び出して、kcpがデータを送信するようにします。
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

データ長 len が mss を超える場合、分割して送信する必要があり、受信側で再結合する必要があります。
    if (len <= (int)kcp->mss) count = 1;
    else count = (len + kcp->mss - 1) / kcp->mss;

    if (count >= (int)IKCP_WND_RCV) return -2;

    if (count == 0) count = 1;

サブコントラクト
    for (i = 0; i < count; i++) {
パックに含まれるデータの長さを計算し、対応するセグメント構造を割り当てます。
        int size = len > (int)kcp->mss ? (int)kcp->mss : len;
        seg = ikcp_segment_new(kcp, size);
        assert(seg);
        if (seg == NULL) {
            return -2;
        }

// segのデータ情報を設定します。frgは分割パケットの番号を示します。
        if (buffer && len > 0) {
            memcpy(seg->data, buffer, size);
        }
        seg->len = size;
        seg->frg = (kcp->stream == 0)? (count - i - 1) : 0;

// snd_queueの末尾に追加し、nsnd_quaを一つ増やす
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

`ikcp_send` は、KCPの上位層から呼び出されるデータ送信インターフェースで、KCPに送信させるすべてのデータはこのインターフェースを介して行われるべきです。`ikcp_send` は非常に単純な処理を行います。主に、データを`kcp->mss`（1つのパケットの最大データ長）に基づいて複数のパケットに分割し、各分割パケットに番号を割り当てて、最後に送信キュー`snd_queue`の末尾に配置します。ストリームモードでは、複数回の `ikcp_send`呼び出しのデータをすべて1つのストリームとして扱い、未満の `SEGMENT`を自動的に埋めてから新しいセグメントを割り当てます。具体的な実装についてはこの文書では詳細に論じませんが、興味のある方は、この文書を参照してコードを確認すると理解できると確信しています。

`ikcp_send` が呼び出されると、データはKCPの`snd_queue`に配置されます。その後、KCPは送信予定のデータを送信する機会を探す必要があります。これらのコードはすべて`ikcp_update`および`ikcp_flush`に配置されています。

<details>
<要約> ikcp_update（コードを展開するにはクリック） </要約>
```cpp
//---------------------------------------------------------------------
ikcp_update is an interface designed for higher-level periodic invocation, used to update the state of KCP and send data.
// update state (call it repeatedly, every 10ms-100ms), or you can ask 
// ikcp_check when to call it again (without ikcp_input/_send calling).
// 'current' - current timestamp in millisec. 
//---------------------------------------------------------------------
void ikcp_update(ikcpcb *kcp, IUINT32 current)
{
    IINT32 slap;

    kcp->current = current;

ikcp_flush Will check this, the upper layer must have called ikcp_update before calling ikcp_flush, it is recommended to only use ikcp_update.
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
// Next time to flush
        kcp->ts_flush += kcp->interval;
        if (_itimediff(kcp->current, kcp->ts_flush) >= 0) {
            kcp->ts_flush = kcp->current + kcp->interval;
        }
        ikcp_flush(kcp);
    }
}
```
</details>

`ikcp_update` が行うのは非常に単純で、`ts_flush` の時間を確認し、条件が満たされると `ikcp_flush` を呼び出します。主要な処理ロジックはすべて `ikcp_flush` にあります。`ikcp_flush` の内容は少し複雑ですので、現時点ではARQ送信に関連する部分に注目しています。

<details>
<summary> データを送信する（コードを展開するにはクリック） </summary>
```cpp
//---------------------------------------------------------------------
// ikcp_flush
//---------------------------------------------------------------------
void ikcp_flush(ikcpcb *kcp)
{
    IUINT32 current = kcp->current;

// bufferはikcp_outputに渡すデータで、データパケットサイズの3倍として初期化されます。
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

// seg.wnd indicates the current size of the receive window
    seg.wnd = ikcp_wnd_unused(kcp);
    seg.una = kcp->rcv_nxt;
    seg.len = 0;
    seg.sn = 0;
    seg.ts = 0;

// ACKを送信
// 送信ウィンドウの計算
    //...

snd_queue から snd_buf にパケットを移動します。
移動には送信ウィンドウのサイズを満たす必要があります。送信ウィンドウがいっぱいになると、移動が停止します。
`// snd_buf に置かれたデータは、ikcp_output を直接呼び出して対向に送信するデータです。`
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

//seg唯一な番号は、実際には単調増加するkcp->snd_nxtです。
        newseg->sn = kcp->snd_nxt++;

// una is set here to notify the other side of the next expected packet sequence number to receive.
        newseg->una = kcp->rcv_nxt;
        newseg->resendts = current;
        newseg->rto = kcp->rx_rto;
        newseg->fastack = 0;
        newseg->xmit = 0;
    }

クイックリトランスミットフラグとタイムアウト待ち時間を計算します。
    // ...

// 送信 snd_buf
    for (p = kcp->snd_buf.next; p != &kcp->snd_buf; p = p->next) {
        IKCPSEG *segment = iqueue_entry(p, IKCPSEG, node);
        int needsend = 0;
        if (segment->xmit == 0) {
// 初回送信
// set->xmit は送信回数を表します
// 超時時の再送時間
            needsend = 1;
            segment->xmit++;
            segment->rto = kcp->rx_rto;
            segment->resendts = current + segment->rto + rtomin;
        }
        else if (_itimediff(current, segment->resendts) >= 0) {
// リトライ時間制限
            // ...
        }
        else if (segment->fastack >= resent) {
// ファーストリトランスミッション
            // ...
        }

        if (needsend) {
            int need;
            segment->ts = current;
            segment->wnd = seg.wnd;
            segment->una = kcp->rcv_nxt;

            size = (int)(ptr - buffer);
            need = IKCP_OVERHEAD + segment->len;

バッファ内のデータが MTU を超えるたびに、それを優先して送信して、できるだけローカルレベルでの再分割を避けるようにしてください。
            if (size + need > (int)kcp->mtu) {
                ikcp_output(kcp, buffer, size);
                ptr = buffer;
            }

// 将seg控制数据复制到缓冲区上，由KCP自行处理大小端问题。
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

// Calculate ssthresh, update slow start window
    // ...
}
```
</details>

現在私たちは `ikcp_flush` に関するデータ送信に焦点を当てています。

最初、KCP は相手の受信ウィンドウのサイズに応じて、`snd_queue` からデータを `snd_buf` に移動し、移動するデータの量は `num = snd_nxt - (snd_una + cwnd)` の式で計算されます。つまり、送信済みの最大パケット番号 `snd_una` にスライディングウィンドウのサイズ `cwnd` を加えた値が次に送信するべきパケット番号 `snd_nxt` よりも大きい場合、新しいデータパケットを送信できます。`SEG` の移動中に、制御フィールドも設定されます。

`snd_buf`を走査し、データパケットを送信する必要があればデータを`buffer`にコピーし、コピーしながら`ikcp_encode_seg`を使用して制御フィールドデータのエンディアン問題を処理します。

「最終的に `ikcp_output` を呼び出して、`buffer` 上のデータを送信します。」

ここまで、KCP はデータの送信を完了しました。

###受け取る

データを受信するプロセスは送信と逆です：`ikcp_input` → `ikcp_update` → `ikcp_recv`。ユーザーがネットワークからデータを受信すると、`ikcp_input`を呼び出してKCPにデータを渡し、`ikcp_update`を呼び出すと送信元にACKパケットが返信されます。上位レベルは`ikcp_recv`を呼び出してKCPによって解析されたデータを受信します。

<details>
データを受信（クリックしてコードを展開）
```cpp
//---------------------------------------------------------------------
// input data
//---------------------------------------------------------------------
int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    IUINT32 prev_una = kcp->snd_una;
    IUINT32 maxack = 0, latest_ts = 0;
    int flag = 0;

合法性検査
    if (data == NULL || (int)size < (int)IKCP_OVERHEAD) return -1;

// データは複数のKCPパケットであり、ループ処理されます。
    while (1) {
        IUINT32 ts, sn, len, una, conv;
        IUINT16 wnd;
        IUINT8 cmd, frg;
        IKCPSEG *seg;

// Not enough for a KCP packet, exiting.
        if (size < (int)IKCP_OVERHEAD) break;

// 制御フィールドをまず解析します
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

// データパケットタイプのチェック
        if (cmd != IKCP_CMD_PUSH && cmd != IKCP_CMD_ACK &&
            cmd != IKCP_CMD_WASK && cmd != IKCP_CMD_WINS) 
            return -3;

        kcp->rmt_wnd = wnd;

ここでの「una」は送信元の「kcp->rcv_nxt」です。このデータに基づいて、確認済みの受信データを削除できます。
        ikcp_parse_una(kcp, una);
受信確認済みのパケットを除外して、snd_una を更新し、次に送信するシーケンス番号を更新します。
        ikcp_shrink_buf(kcp);

        if (cmd == IKCP_CMD_ACK) {
// ack 包
            // ...
        }
        else if (cmd == IKCP_CMD_PUSH) {
// データパケット
受信したデータパケットのシーケンス番号snが受信ウィンドウ内にある場合、通常処理を行います。それ以外の場合は却下し、再送信を待ちます。
            if (_itimediff(sn, kcp->rcv_nxt + kcp->rcv_wnd) < 0) {

受け取ったすべてのデータパケットには、ackパケットを返信し、記録してください。
                ikcp_ack_push(kcp, sn, ts);

// 受信データは、ikcp_parse_data を使用して処理されます。
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
検索ウィンドウパック
            // ...
        }
        else if (cmd == IKCP_CMD_WINS) {
//応答パケットを検索します
            // ...
        }
        else {
            return -3;
        }

        data += len;
        size -= len;
    }

// ファストリトランスミッションロジックを処理します
    // ...

更新送信ウィンドウ
    // ...

    return 0;
}
```
</details>

`ikcp_input` は各`SEG`パッケージを処理して、まずパッケージの妥当性とタイプを確認します。各データパッケージには`una`が付属しており、これには送信側が受信を待っているパッケージ番号が格納されています。`una`よりも小さい必要のあるパッケージは、すでに対向側が正常に受信したものです。そのため、`snd_buff`から`una`よりも小さなパッケージを全て削除し、`snd_nxt`を更新する必要があります。この処理は`ikcp_parse_una`と`ikcp_shrink_buf`によって行われます。受信した各データパッケージはACKパッケージで応答する必要があり、これは`ikcp_ack_push`で記録され、最後に`ikcp_parse_data`がデータを処理します。

<details>
データを分析します（コードを展開するにはクリックしてください）
```cpp
void ikcp_parse_data(ikcpcb *kcp, IKCPSEG *newseg)
{
    struct IQUEUEHEAD *p, *prev;
    IUINT32 sn = newseg->sn;
    int repeat = 0;

//通し番号チェック
    if (_itimediff(sn, kcp->rcv_nxt + kcp->rcv_wnd) >= 0 ||
        _itimediff(sn, kcp->rcv_nxt) < 0) {
        ikcp_segment_delete(kcp, newseg);
        return;
    }

newsegが置かれるべき場所を見つけてください。受信したsegはソートされていない可能性があるためです。
    for (p = kcp->rcv_buf.prev; p != &kcp->rcv_buf; p = prev) {
        IKCPSEG *seg = iqueue_entry(p, IKCPSEG, node);
        prev = p->prev;
        if (seg->sn == sn) {
// 繰り返し受信
            repeat = 1;
            break;
        }
        if (_itimediff(sn, seg->sn) > 0) {
            break;
        }
    }

// Put newseg in the right position of rcv_buf.
    if (repeat == 0) {
        iqueue_init(&newseg->node);
        iqueue_add(&newseg->node, p);
        kcp->nrcv_buf++;
    }    else {
        ikcp_segment_delete(kcp, newseg);
    }

// rcv_buf から rcv_queue にデータを移動します
    while (! iqueue_is_empty(&kcp->rcv_buf)) {
        IKCPSEG *seg = iqueue_entry(kcp->rcv_buf.next, IKCPSEG, node);
// もしsegの番号が受信待ちの番号だったら、rcv_queueに移動します
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

`ikcp_parse_data` の主な仕事は、`newseg` を `kcp->rcv_buf` の適切な位置に配置し、`rcv_buf` から `rcv_queue` にデータを移動することです。`rcv_buf` の適切な位置とは、`rcv_buf` が`sn`の増加順に並んでいることを意味し、`newseg`は自分の`sn`の大きさに基づいて適切な位置を見つける必要があります。 `rcv_buf`にあるデータを`rcv_queue`に移動する条件は、`rcv_buf`にあるデータパケットのシーケンス番号が、KCPが待機しているパケットシーケンス番号 `kcp->rcv_nxt` と等しいことです。 データパケットを1つ移動した後、`kcp->rvc_nxt`を更新し、次のデータパケットを処理する必要があります。

`ikcp_input` の後、上位の `ikcp_update` を呼び出すと ACK パケットが送信され、`ikcp_recv` を呼び出すと有効なデータが上位に返されます。`ikcp_update` と `ikcp_recv` はお互いに独立しており、呼び出しの順序は要求されません。上位の呼び出しのタイミングによって決まります。最初に、`ikcp_update` の中で ACK 送信に関する部分を見てみましょう：

<details>
<summary> 回答 ACK（コードを表示するをクリックしてください）</summary>
```cpp
前方で述べたように、ikcp_updateは最終的にikcp_flushを呼び出します。
void ikcp_flush(ikcpcb *kcp, IUINT32 current)
{
    // ...

// 応答 ACK パケット
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

ACKパケットは以前に`ikcp_ack_push`によって保存されましたので、ここでは単に`ikcp_ack_get`を使用して各ACKパケットの情報を取得し、相手に送信するだけです。上位レイヤーでは`ikcp_recv`を使用してKCPからデータを取得できます：

<details>
<summary> ikcp_recv（クリックしてコードを展開） </summary>
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

// 一部の有効性チェック
    if (iqueue_is_empty(&kcp->rcv_queue))
        return -1;
    if (len < 0) len = -len;

// それが戻せるデータの長さを計算します。
    peeksize = ikcp_peeksize(kcp);

    if (peeksize < 0)
        return -2;
    if (peeksize > len)
        return -3;

// 受信ウィンドウを確認します
    if (kcp->nrcv_que >= kcp->rcv_wnd)
        recover = 1;

// rcv_queueを繰り返し、データをbufferにコピーします
    for (len = 0, p = kcp->rcv_queue.next; p != &kcp->rcv_queue; ) {
        int fragment;
        seg = iqueue_entry(p, IKCPSEG, node);
        p = p->next;

        if (buffer) {
            memcpy(buffer, seg->data, seg->len);
            buffer += seg->len;
        }

        len += seg->len;

パッケージ分割
        fragment = seg->frg;

データパケットを削除します
        if (ispeek == 0) {
            iqueue_del(&seg->node);
            ikcp_segment_delete(kcp, seg);
            kcp->nrcv_que--;
        }

すべてのサブパッケージがコピーされたら、ループを終了します。
        if (fragment == 0)
            break;
    }

    assert(len == peeksize);

// rcv_queue has emptied some more, trying to continue moving from rcv_buf to rcv_queue
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

`ikcp_recv`関数は、一度の呼び出しで完全なデータパケットを返します。上位レイヤーは、データが返されなくなるまで繰り返し呼び出すことができます。関数のロジックは非常に単純で、`rcv_queue`からデータを上位に提供された`buffer`にコピーすることです。これにより、受信側は受信したデータパケットを処理しました。

受信側がデータパケットを処理する際、送信側に ACK パケットを送信しました。次に、送信側が ACK パケットを受け取る処理を見てみましょう。

<details>
<summary>ACKパケットの処理（コードを展開するにはクリックしてください）</summary>
```cpp
int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    // ...
    IUINT32 maxack = 0, latest_ts = 0;
    // ...
    while (1) {
        // ...
// ts は相手の kcp-> current です
        data = ikcp_decode32u(data, &ts);
        data = ikcp_decode32u(data, &sn);

        if (cmd == IKCP_CMD_ACK) {
// ローテーションの更新
            if (_itimediff(kcp->current, ts) >= 0) {
                ikcp_update_ack(kcp, _itimediff(kcp->current, ts));
            }
// 更新 snd_buf
            ikcp_parse_ack(kcp, sn);
            ikcp_shrink_buf(kcp);

// maxack = 今回の入力のすべてのACKパケットの中で最大のシーケンス番号
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

ACK パケットを受信した場合、クイック再送信用に記録します。
    if (flag != 0) {
        ikcp_parse_fastack(kcp, maxack, latest_ts);
    }
}
```
</details>

ACK パケットを受信すると、`ikcp_parse_ack` と `ikcp_shrink_buf` を使用して `snd_buf` を更新する必要があります。さらに、`ikcp_update_ack` を呼び出して rto（再送タイムアウト）を計算する必要があります。 `ikcp_input` は受信したACKパケットの最大シーケンス番号を計算し、高速再送用に記録します。 このようにして、送信側はACKパケットを受信すると、送信データを`snd_buf`から削除し、そのデータパケットが受信側に信頼性の高い方法で到達したことを確認します。完全なARQ受信のプロセスが終了します。

###再送信

前述はKCPによるARQでの確認受信機構造を紹介しており、ARQには信頼性を確保するためのタイムアウト再送機能も必要です。次に、KCPがどのようにタイムアウト再送を行っているかを見ていきましょう。

`ikcp_flush` 関数に戻りましょう：

<details>
「超時再送信（コードを展開するにはクリック）」
```cpp
void ikcp_flush(ikcpcb *kcp)
{
    // ...
// 送信snd_buf
    for (p = kcp->snd_buf.next; p != &kcp->snd_buf; p = p->next) {
        IKCPSEG *segment = iqueue_entry(p, IKCPSEG, node);
        int needsend = 0;
        if (segment->xmit == 0) {
// First time sending
            needsend = 1;
            segment->xmit++;
// segment->rtoを設定します.
segment->rto を使用して、segment->resendts のタイムアウト再送信時間を計算します。
            segment->rto = kcp->rx_rto;
            segment->resendts = current + segment->rto + rtomin;
        }
        else if (_itimediff(current, segment->resendts) >= 0) {
再送超え
            needsend = 1;
            segment->xmit++;
            kcp->xmit++;
nodelayは、次回のタイムアウト再送信時間の計算を制御します。
            if (kcp->nodelay == 0) {
                segment->rto += kcp->rx_rto;
            }    else {
                segment->rto += kcp->rx_rto / 2;
            }
            segment->resendts = current + segment->rto;
            lost = 1;
        }
        else if (segment->fastack >= resent) {
クイックリトランスミッション
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

一旦現在の時間 `current` が `segment->resendts` を超えると、タイムアウト再送信時間が経過したことを意味します。この期間中に受信者から ACK パケットが受信されなかったため、タイムアウト再送信メカニズムがトリガーされ、`needsend = 1` としてデータを再送信します。

受信確認とタイムアウト再送信機構を備えたKCPにより、基本的な信頼性のあるデータ転送が保証されます。しかし、より安定したデータフローを維持するために、KCPはさらなる最適化を行っています。次に、KCPがどんな最適化を行ったかを見ていきましょう。

##KCPのフロー速度向上戦略

###高速再送

送信元は `sn` と `sn + 1` の2つのデータパケットを送信しました。`sn + 1` の ACK パケットしか受信しない場合、`sn` の ACK パケットがまだネットワーク内に到達していない、または ACK パケットが失われている可能性があります。さらには、`sn` データパケットが失われた可能性もあります。この時、まだタイムアウト再送信の時間に達しておらず、ネットワークも混雑していない場合、突然のパケット損失が起きている可能性があります。その場合、送信元が積極的に `sn` データパケットを事前に送信することで、受信側がより迅速にデータを受信し、スループットを向上させることができます。

KCPの内部でも高速再送機構が実装されており、`ikcp_flush`内でも行われています。

<details>
<i>サマリー：高速リトランスミッション（コードを展開するにはクリック）</i>
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
クイックリカバリ
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

快速再送要求には、2つの条件があります：
segment->fastack >= resent では、resent は設定可能なパラメータで、kcp->fastresend という設定を指します。設定が 0 の場合、クイック再送を無効にします。segment->fastack は関数 ikcp_parse_fastack で設定され、この関数はikcp_inputで呼び出され、ikcp_input によって算出された maxack に基づいて、maxack より小さいすべての sn の segment->fastack に 1 を加算します。したがって、segment->fastack は、sn よりも大きなパケットを受信した回数を表します。
`segment->xmit <= kcp->fastlimit || kcp->fastlimit <= 0`、`setgment->xmit` は送信回数を表し、`kcp->fastlimit` は設定可能な最大高速再送回数を示します。送信回数は最大高速再送回数未満である必要があります。

上記の条件でKCPはすぐに高速リトランスミッションを行います。高速リトランスミッションはタイムアウト再送時間をリセットしないことに注意してください。以前のタイムアウト時間は引き続き有効です。

###超時再送信時間を短縮

再送信時間（Fast Retransmit）は素晴らしいメカニズムだが、ただ時間がかかりすぎるんだ。TCPの戦略によると、毎回の再送信時間は2倍になるんだ。待ち時間がどんどん膨らんで、待ってる間に受信側のウィンドウが一杯になって新しいデータを受信できない場合がよくある。さらに、再送信するパケットの番号が前にあると、受信側は再送信されたパケットを受信しないと全部のデータを上位に返すことができない。この状況では、ネットワーク全体のスループットはほぼ0になる。KCPは待ち時間の増加を緩和するための設定を追加し、しかも2倍ではなく、`kcp->nodelay`を通じて毎回の待ち時間が1倍のRTOまたは0.5倍のRTOだけ増加するように制御できる。これにより、待ち時間の増加を効果的に緩和し、ネットワークができるだけ早くスループットを回復できるのを支援する。

###更新送信ウィンドウ

送信ウィンドウに表示されるのは、同時に送信されるデータパケットの数です。ウィンドウが大きいほど、同時に送信されるデータが多く、スループットも大きくなりますが、ウィンドウが大きすぎるとネットワークの過負荷、パケットロスの増加、データの再送信が増え、スループットが低下する可能性があります。そのため、送信ウィンドウはネットワーク状況に応じて常に更新され、徐々に最適な値に近づけられるべきです。KCPにおける送信ウィンドウに関するコード：

<details>
<summary>送信ウィンドウ（コードを展開するにはクリック）</summary>
```cpp
ikcpcb* ikcp_create(IUINT32 conv, void *user)
{
    // ...
// snd_wnd、rcv_wndは送信および受信のバッファサイズです。
    kcp->snd_wnd = IKCP_WND_SND;    // 32
    kcp->rcv_wnd = IKCP_WND_RCV;    // 128
// 受信ウィンドウサイズ               // 128
    kcp->rmt_wnd = IKCP_WND_RCV
// 送信ウィンドウ cwnd の初期化 0
    kcp->cwnd = 0;
ウィンドウサイズのバイト数を送信して、cwnd の計算に参加します。
    kcp->incr = 0
慢启动阈值、slow start threshold
    kcp->ssthresh = IKCP_THRESH_INIT;
nocwndは設定可能なパラメータで、1はcwndを考慮しないことを示しています。
    kcp->nocwnd = 0;
    // ...
}

void ikcp_flush(ikcpcb *kcp)
{
    // ...
データを送信する際には、送信ウィンドウサイズを計算してください。これは送信バッファサイズと相手の受信ウィンドウサイズの小さい方です。
    cwnd = _imin_(kcp->snd_wnd, kcp->rmt_wnd);
// デフォルトでは、kcp->cwnd を考慮する必要があります。つまり、常に更新される送信ウィンドウです。
    if (kcp->nocwnd == 0) cwnd = _imin_(kcp->cwnd, cwnd);

"cwndのサイズに応じて、snd_queueはsnd_bufに移動します。"
    while (_itimediff(kcp->snd_nxt, kcp->snd_una + cwnd) < 0) {
    }
// データの送信
    resent = (kcp->fastresend > 0)? (IUINT32)kcp->fastresend : 0xffffffff;
// タイムアウトによる再送信トリガー lost = 1
// ファストリトランスミットのトリガーが変更++

更新慢スタートしきい値と送信ウィンドウ
    if (change) {
もし速やかな再送信が発生した場合、ssthresh は現在ネットワーク上を送信中のデータパケット数の半分に設定されます。
        IUINT32 inflight = kcp->snd_nxt - kcp->snd_una;
        kcp->ssthresh = inflight / 2;
        if (kcp->ssthresh < IKCP_THRESH_MIN)
            kcp->ssthresh = IKCP_THRESH_MIN;

// ウィンドウサイズはしきい値に再送関連の高速再送を加えたものです
        kcp->cwnd = kcp->ssthresh + resent;
        kcp->incr = kcp->cwnd * kcp->mss;
    }

    if (lost) {
超时重传が発生した場合、スロープスタートがトリガーされ、ssthreshの閾値は送信ウィンドウの半分に設定されます。
        kcp->ssthresh = cwnd / 2;
        if (kcp->ssthresh < IKCP_THRESH_MIN)
            kcp->ssthresh = IKCP_THRESH_MIN;
//送窗口を1に戻し、再びスロースタートで成長させる
        kcp->cwnd = 1;
        kcp->incr = kcp->mss;
    }

    if (kcp->cwnd < 1) {
// 0 に初期化されているため、ここに来ると 1 に設定されます
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
// rmt_wnd is the size of the receiving window on the other side
        kcp->rmt_wnd = wnd
        // ...
データ処理
    }

// 最終的な更新を送信する窓口
// kcp->snd_una - prev_una > 0, indicates that ACK has been received in this input and the send buffer snd_buf has changed.
    if (_itimediff(kcp->snd_una, prev_una) > 0) {
// 相手の受信ウィンドウを再評価します。
        if (kcp->cwnd < kcp->rmt_wnd) {
            IUINT32 mss = kcp->mss;

            if (kcp->cwnd < kcp->ssthresh) {
慢スタートの閾値未満の場合、倍増します。
                kcp->cwnd++;
                kcp->incr += mss;

            }    else {
慢スタートしきい値を超えた後、式を使用して incr を更新し、それに基づいて cwnd を計算します。
                if (kcp->incr < mss) kcp->incr = mss;
                kcp->incr += (mss * mss) / kcp->incr + (mss / 16);
                if ((kcp->cwnd + 1) * mss <= kcp->incr) {
                    kcp->cwnd++;
                }
            }
// 更新された値を再度rmt_wndと比較する必要があります
            if (kcp->cwnd > kcp->rmt_wnd) {
                kcp->cwnd = kcp->rmt_wnd;
                kcp->incr = kcp->rmt_wnd * mss;
            }
        }
    }
}
```
</details>

`kcp->cwnd` のサイズを計算するコード断片は少し長くなります。データの送受信時に更新が必要だからです。`kcp->cwnd` は 0 で初期化されています。
`ikcp_flush` が最初に呼び出されたときに、値が1未満の場合、値を1に修正します。その後、送信側は送信ウィンドウサイズに基づいて対応する数のデータパケットを送信し、ACKを待ちます。
返事パケット。ACKパケットは、`kcp->input`内で処理されます。`kcp->input`中でACKパケットが判断され、送信バッファの送信データパケットがクリアされている場合、データパケットがすでに到着したことを示します。`kcp->cwnd++`。実際には、1回の`kcp->input`ではACKパケットのみが処理される可能性が高いです。ACKパケットを受信するたびに、`kcp->cwnd++`が実行されると考えられます。この増加の実装は、倍増の効果をもたらします。たとえば、現在`kcp->cwnd = 2`で、2つのデータパケットを送信し、2つのACKパケットを受信した場合、2回の増加が発生し、最終的に`kcp->cwnd = 4`の倍増となります。



KCP は `nocwnd` という設定を追加しました。`nocwnd = 1` の場合、データ送信は送信ウィンドウのサイズを考慮せず、最大限に送信できる数のデータパケットを直接送信し、高速モードの要件を満たします。

##結論

本文はKCPのソースコードを簡単に分析し、KCPにおけるARQの実装と、流速を向上させるいくつかのKCP戦略について議論しています。触れられていない詳細もたくさんありますが、興味のある方はKCPのソースコードを自分で調べてみてください。きっと多くの知識を得られるはずです。

--8<-- "footer_ja.md"


> この投稿はChatGPTを使用して翻訳されたものです。[**フィードバック**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。 -> どこか見落とされている点があれば指摘してください。 
