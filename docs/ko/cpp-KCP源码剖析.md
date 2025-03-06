---
layout: post
title: KCP 소스 코드 분석
categories:
- c++
catalog: true
tags:
- dev
description: 본문에서는 KCP의 소스 코드를 간단히 분석하고, KCP에서의 ARQ 구현과 KCP의 전송 속도 향상을 위한 여러 전략에 대해
  논의하고 있습니다.
figures: []
---

<meta property="og:title" content="KCP 源码剖析" />

이 문서를 읽기 전에 KCP에 대해 들어본 적이 없거나 KCP를 전혀 모르는 사람들은 시간을 내어 KCP 프로젝트 설명서를 먼저 살펴보시기 바랍니다: [링크](https://github.com/skywind3000/kcp)이 문서의 목적은 KCP의 구현 세부사항을 심도 있게 이해하는 것입니다.

##KCP란 무엇인가요?

KCP는 빠르고 신뢰할 수 있는 프로토콜로, TCP보다 낮은 지연 시간으로 데이터를 전송하며, 데이터 재전송 속도가 빠르고 대기 시간이 짧습니다.

> TCP는 데이터 처리량을 중시하는 것으로, 대역폭을 최대한 활용하는 것에 중점을 둔다. 반면 KCP는 데이터 전송 속도를 중시하는 것으로, TCP보다 30%-40% 빠른 전송 속도를 위해 10%-20%의 대역폭 낭비를 감수하는 것이 특징이다. TCP 채널은 느리지만 대량 데이터를 전송하는 큰 운하와 달리, KCP는 빠르게 흐르는 작은 시내를 상징한다.

위에 적힌 내용은 KCP 문서에 나와 있습니다. 핵심 키워드는 **대역폭**과 **흐름 속도**입니다. KCP는 대역폭을 소모하지만, 더 크고 균형있는 전송 속도를 가져다줍니다. 더 자세한 내용은 KCP 자체 문서를 참고해 주세요.

##KCP 데이터 구조

KCP 소스코드는 `ikcp.h`와 `ikcp.c`에 있습니다. `ikcp.h`에는 데이터 구조의 선언이 중심이며, 먼저 `SEGMENT` 데이터 패킷이 있습니다. 이는 KCP 프로토콜에서 데이터를 처리하는 최소 단위입니다.

<details>
<summary> SEGMENT Structure (코드 펼치기) </summary>
```cpp
//=====================================================================
세그먼트 하나는 데이터 패킷 하나입니다.
//=====================================================================
struct IKCPSEG
{
// 링크드 리스트 노드, 송신 및 수신 대기열 모두 여기 링크드 리스트의 구조입니다.
    struct IQUEUEHEAD node;

// 대화 식별자, 동일한 대화 식별자가 같음
    IUINT32 conv;

// 패킷 유형, 예를 들어 데이터 또는 ACK
    IUINT32 cmd;

MTU 제한으로 대규모 데이터 패킷이 여러 작은 데이터 패킷으로 분할됩니다. 이것은 작은 데이터 패킷의 번호입니다.
    IUINT32 frg

모든 데이터 패킷은 송신 측의 수신 창 크기와 함께 전송됩니다.
    IUINT32 wnd;

발송 시간은 ACK 패킷인 경우 원본 데이터 패킷의 ts로 설정됩니다.
    IUINT32 ts;

데이터 패킷을 유일하게 식별하는 번호입니다.
    IUINT32 sn;

una보다 작은 값의 데이터 패킷은 모두 성공적으로 수신되었으며, TCP에서 의미하는 것과 동일합니다: 최고로 인정되지 않은 시퀀스 번호 SND.
    IUINT32 una;

데이터 길이
    IUINT32 len;

시간 초과 재전송 설정
    IUINT32 resendts;

// 다음 회보 에 대기 시간
    IUINT32 rto;

이 텍스트를 한국어로 번역하십시오:

    // 빠른 재전송, 이 데이터 패킷을 수신한 후의 패킷 수는 일정 수 이상이면 빠른 재전송이 트리거됩니다.
    IUINT32 fastack;

전송 횟수
    IUINT32 xmit;

// 자료
    char data[1];
};
```
</details>

`SEGMENT`의 주석을 읽어 보면 KCP의 핵심이 ARQ 프로토콜인 것을 대략 알 수 있습니다. 데이터 전달을 보장하기 위해 자동 타임아웃 재전송을 통해 작동합니다. 그 다음은 KCP 구조 KCPCB의 정의를 살펴봅시다:

<details>
KCP 구조 (코드 펼치기 클릭)
```cpp
//---------------------------------------------------------------------
// IKCPCB
//---------------------------------------------------------------------
struct IKCPCB
{
// conv: 대화 번호
// mtu, mss: 최대 전송 단위, 최대 세그먼트 크기
// state: 세션 상태, 0 유효, -1 연결 끊김
    IUINT32 conv, mtu, mss, state;

// snd_una: ACK를 기다리는 패킷 번호
// snd_nxt: 다음으로 전송 대기 중인 데이터 패킷 번호
// rcv_nxt: The next packet number waiting to be received.
    IUINT32 snd_una, snd_nxt, rcv_nxt;

// ts_recent, ts_lastack: 사용되지 않음
// ssthresh: 혼잡 제어 슬로 스타트 임계값
    IUINT32 ts_recent, ts_lastack, ssthresh;

// rx_rto: rto (retransmission timeout), 超时重传时间
// rx_rttval, rx_srtt, rx_minrto: 중간 변수로 rto를 계산합니다.
    IINT32 rx_rttval, rx_srtt, rx_rto, rx_minrto;

// snd_wnd, rcv_wnd: Maximum size of the sending and receiving windows
// rmt_wnd: 원격 창, 대상의 남은 수신 창 크기
// cwnd: 전송 가능한 창 크기
// 탐지: 제어 메시지를 보낼지 여부를 나타내는 플래그
    IUINT32 snd_wnd, rcv_wnd, rmt_wnd, cwnd, probe;

// 현재: 현재 시간
// interval: 갱신 간격
// ts_flush: 다음으로 업데이트해야 하는 시간
// xmit: 전송 실패 횟수
    IUINT32 current, interval, ts_flush, xmit;

연결 리스트의 길이
    IUINT32 nrcv_buf, nsnd_buf;
    IUINT32 nrcv_que, nsnd_que;

// nodelay: RTO의 증가 속도를 제어합니다.
ikcp_update를 호출했는지 여부:
    IUINT32 nodelay, updated;

ts_probe, probe_wait: 상대방 수신 창이 장기간 0인 경우 주기적으로 질문을 시작함
    IUINT32 ts_probe, probe_wait;

// deal_link: 상대편이 장시간 응답하지 않음
// incr: 참여하여 전송 창 크기를 계산합니다.
    IUINT32 dead_link, incr;

// queue: 사용자 레이어와 상호 작용하는 데이터 패킷
// buf: 프로토콜 캐시 데이터 패킷
    struct IQUEUEHEAD snd_queue;
    struct IQUEUEHEAD rcv_queue;
    struct IQUEUEHEAD snd_buf;
    struct IQUEUEHEAD rcv_buf;

ACK를 보내야 하는 데이터 패킷 정보
    IUINT32 *acklist;

// ack가 필요한 패킷 수량
    IUINT32 ackcount;

acklist 내부의 메모리 크기
    IUINT32 ackblock;

// 사용자로부터 전달받은 데이터
    void *user;

// kcp 패키지를 보관하는 공간
    char *buffer;

빠른 전송을 유발하는 fastack 횟수
    int fastresend;

최대 빠른 전송 재시도 횟수
    int fastlimit;

// nocwnd: 슬로 스타트를 고려하지 않는 전송 윈도우 크기
// stream: 흐름 모드
    int nocwnd, stream;

    // debug log
    int logmask;

데이터 전송 인터페이스
    int (*output)(const char *buf, int len, struct IKCPCB *kcp, void *user);

    void (*writelog)(const char *log, struct IKCPCB *kcp, void *user);
};
```
</details>

KCP 구조의 각 필드에 설명을 추가하면서 조금씩 느끼기 시작합니다. KCP 프로토콜 세트가 그리 복잡하지 않다는 것을 코드를 꼼꼼히 분석하면 이해할 수 있다. :smile:

##KCP의 ARQ 구현

KCP는 본질적으로 ARQ (Auto Repeat-reQuest, 자동 재전송) 프로토콜로, 가장 중요한 것은 신뢰할 수 있는 전송을 보장하는 것입니다. 그래서 우리는 먼저 KCP의 기본 ARQ 부분에 초점을 맞춰볼 수 있으며, KCP가 어떻게 신뢰할 수 있는 전송을 구현하는지 알아볼 수 있습니다.

ARQ라는 용어는 받는 쪽이 데이터 패킷을 받지 못했다고 생각할 때, 해당 데이터 패킷을 자동으로 다시 보내는 것을 의미합니다. 이는 수신 확인과 시간 초과 재전송 두 가지 메커니즘을 사용하여 신뢰할 수 있는 전송을 구현합니다. 구체적인 코드 구현에서 KCP는 각 데이터 패킷(이전 섹션에서 언급한 `SEGMENT`)에 고유한 `sn` 식별자를 할당합니다. 받는 쪽이 데이터 패킷을 수신하면 동일한 `sn`을 가진 ACK 패킷(또한 `SEGMENT`)을 응답하여 이 데이터 패킷이 성공적으로 수신되었음을 알립니다. `SEGMENT`에는 `una` 필드가 있어 다음에 기대하는 데이터 패킷의 번호를 나타냅니다. 다시 말해, 해당 번호 이전의 모든 데이터 패킷이 이미 수신되었음을 의미하며, 마치 완전한 ACK 패킷처럼 작용하여 발신 측이 전송 버퍼 및 전송 창을 빠르게 업데이트할 수 있습니다.

KCP 패킷의 송수신 코드를 추적하여 기본적인 ARQ 구현을 이해할 수 있습니다:

###전송

전송 과정은 `ikcp_send` -> `ikcp_update` -> `ikcp_output`이 되며, 상위 레벨에서는 `ikcp_send`를 호출하여 데이터를 KCP에 전달하고, KCP는 `ikcp_update`에서 데이터 전송을 처리합니다.

<details>
<요약> ikcp_send (코드 펼치기를 클릭하십시오) </요약>
```cpp
//---------------------------------------------------------------------
데이터를 전송하는 인터페이스로, 사용자는 ikcp_send를 호출하여 kcp가 데이터를 전송하도록 합니다.
// user/upper level send, returns below zero for error
//---------------------------------------------------------------------
int ikcp_send(ikcpcb *kcp, const char *buffer, int len)
{
    IKCPSEG *seg;
    int count, i;

// mss는 1보다 작을 수 없습니다.
    assert(kcp->mss > 0);
    if (len < 0) return -1;

    // append to previous segment in streaming mode (if possible)
    if (kcp->stream != 0) {
// Stream processing mode
        // ......
    }

데이터 길이인 len이 MSS보다 크다면 여러 개의 패킷으로 나누어 전송해야 하며 상대방이 수신한 후에 다시 조립해야 합니다.
    if (len <= (int)kcp->mss) count = 1;
    else count = (len + kcp->mss - 1) / kcp->mss;

    if (count >= (int)IKCP_WND_RCV) return -2;

    if (count == 0) count = 1;

// Subcontracting
    for (i = 0; i < count; i++) {
패킷 데이터 길이를 계산하고 해당 seg 구조체를 할당합니다.
        int size = len > (int)kcp->mss ? (int)kcp->mss : len;
        seg = ikcp_segment_new(kcp, size);
        assert(seg);
        if (seg == NULL) {
            return -2;
        }

seg의 데이터 정보를 설정합니다. frg는 분할 번호를 나타냅니다.
        if (buffer && len > 0) {
            memcpy(seg->data, buffer, size);
        }
        seg->len = size;
        seg->frg = (kcp->stream == 0)? (count - i - 1) : 0;

// snd_queue의 끝에 추가하고, nsnd_qua를 증가시킵니다.
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

`ikcp_send` is a data transmission interface called by the upper layer of KCP. All data sent by KCP should go through this interface. The function of `ikcp_send` is simple, mainly dividing the data into multiple segments based on `kcp->mss` (maximum segment size) and assigning segment numbers, then placing them at the end of the transmission queue `snd_queue`. In stream mode, data sent through multiple calls of `ikcp_send` are considered as a single stream and will automatically fill incomplete segments before allocating new ones. Detailed implementation is not discussed in this article. Readers who are interested can understand by reading this article and reviewing the corresponding code.

`ikcp_send` 함수 호출이 완료되면, 데이터는 KCP의 `snd_queue`에 저장됩니다. 그 후, KCP는 전송 대기 중인 데이터를 전송하기 위한 적절한 시기를 찾아야 합니다. 이 부분의 코드는 모두 `ikcp_update`와 `ikcp_flush` 내에 포함되어 있습니다.

<details>
<summary> ikcp_update(클릭하여 코드 펼치기) </summary>
```cpp
//---------------------------------------------------------------------
ikcp_update는 상위 레이어에서 주기적으로 호출되는 인터페이스로, kcp의 상태를 업데이트하고 데이터를 전송하는 데 사용됩니다.
// update state (call it repeatedly, every 10ms-100ms), or you can ask 
// ikcp_check when to call it again (without ikcp_input/_send calling).
// 'current' - current timestamp in millisec. 
//---------------------------------------------------------------------
void ikcp_update(ikcpcb *kcp, IUINT32 current)
{
    IINT32 slap;

    kcp->current = current;

ikcp_flush checks this, the upper layer must have called ikcp_update before calling ikcp_flush, it is recommended to only use ikcp_update.
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
// 다음 flush 시간
        kcp->ts_flush += kcp->interval;
        if (_itimediff(kcp->current, kcp->ts_flush) >= 0) {
            kcp->ts_flush = kcp->current + kcp->interval;
        }
        ikcp_flush(kcp);
    }
}
```
</details>

`ikcp_update` 하는 일은 굉장히 간단해. `ts_flush` 시간을 체크하고, 조건에 맞으면 `ikcp_flush`를 호출해. 주요 처리 로직은 모두 `ikcp_flush`에 있어. `ikcp_flush`는 조금 복잡하기 때문에 현재는 ARQ 전송과 관련된 부분에만 집중하고 있어:

<details>
<요약> 데이터 전송(코드 펼치기 클릭) </요약>
```cpp
//---------------------------------------------------------------------
// ikcp_flush
//---------------------------------------------------------------------
void ikcp_flush(ikcpcb *kcp)
{
    IUINT32 current = kcp->current;

// buffer to be passed to ikcp_output, initialized to 3 times the packet size.
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

seg.wnd 는 현재 수신 창 크기를 나타냅니다.
    seg.wnd = ikcp_wnd_unused(kcp);
    seg.una = kcp->rcv_nxt;
    seg.len = 0;
    seg.sn = 0;
    seg.ts = 0;

// ACK 전송
// 송신 윈도우 크기 계산
    //...

// snd_queue에서 데이터 패킷을 snd_buf로 이동합니다.
이동 중에는 전송 윈도우 크기를 충족해야하며, 전송 창이 가득 차면 이동을 중지해야합니다.
snd_buf에 넣은 데이터는 상대에게 직접 ikcp_output을 호출하여 보낼 수 있는 데이터입니다.
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

// seg 唯一序号，其实就是一个递增的 kcp->snd_nxt
        newseg->sn = kcp->snd_nxt++;

여기서 una를 설정하여 상대편에 다음으로 수신할 패킷 번호를 통지합니다.
        newseg->una = kcp->rcv_nxt;
        newseg->resendts = current;
        newseg->rto = kcp->rx_rto;
        newseg->fastack = 0;
        newseg->xmit = 0;
    }

빠른 전송 신호와 시간 초과 대기 시간을 계산합니다.
    // ...

// 발신 snd_buf
    for (p = kcp->snd_buf.next; p != &kcp->snd_buf; p = p->next) {
        IKCPSEG *segment = iqueue_entry(p, IKCPSEG, node);
        int needsend = 0;
        if (segment->xmit == 0) {
첫 전송
// set->xmit은 전송 횟수를 나타냅니다.
// resendts 超时重传的等待时间
            needsend = 1;
            segment->xmit++;
            segment->rto = kcp->rx_rto;
            segment->resendts = current + segment->rto + rtomin;
        }
        else if (_itimediff(current, segment->resendts) >= 0) {
시간 초과로 재전송
            // ...
        }
        else if (segment->fastack >= resent) {
빠른 재전송
            // ...
        }

        if (needsend) {
            int need;
            segment->ts = current;
            segment->wnd = seg.wnd;
            segment->una = kcp->rcv_nxt;

            size = (int)(ptr - buffer);
            need = IKCP_OVERHEAD + segment->len;

buffer 안의 데이터가 mtu를 초과할 때마다 데이터를 먼저 보내서 가능한 한 하위 레벨에서의 다시 패킷 분할을 피하십시오.
            if (size + need > (int)kcp->mtu) {
                ikcp_output(kcp, buffer, size);
                ptr = buffer;
            }

// seg 제어 데이터를 버퍼에 복사하고, kcp가 자체적으로 엔디안 문제를 다루게 합니다.
            ptr = ikcp_encode_seg(ptr, segment);

// 데이터 다시 복사
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

ssthresh를 계산하고 현재 슬로 스타트 창을 업데이트합니다.
    // ...
}
```
</details>

현재 우리는 `ikcp_flush`에 관한 데이터 전송 로직에만 주목하고 있습니다:

먼저 KCP는 상대방의 수신 창 크기에 따라 'snd_queue'의 데이터를 'snd_buf'로 이동시키며, 이동량은 'num = snd_nxt - (snd_una + cwnd)'로 계산됩니다. 즉, 성공적으로 전송된 최대 패킷 번호 'snd_una'에 슬라이딩 창 크기 'cwnd'를 더한 값이 다음 전송 대기 중인 패킷 번호 'snd_nxt'보다 크다면 새 데이터 패킷을 계속 전송할 수 있습니다. 'SEG'를 이동하는 동안 제어 필드를 설정합니다.

`snd_buf` 를 순회하면서 데이터 패킷을 전송해야 하는 경우 데이터를 `buffer`로 복사하고 동시에 `ikcp_encode_seg`를 사용하여 제어 필드 데이터의 엔디안 문제를 처리합니다.

`ikcp_output` 함수를 호출하여 `buffer`의 데이터를 전송합니다.

여기까지, KCP가 데이터 전송을 완료했습니다.

###수신

수신 프로세스는 송신과 반대입니다: `ikcp_input` -> `ikcp_update` -> `ikcp_recv`. 사용자가 네트워크에서 데이터를 받은 후에는 `ikcp_input`을 호출하여 KCP로 전달해야 하고, `ikcp_update`를 호출하면 송신자에게 ACK 패킷을 응답합니다. 응용 프로그램은 `ikcp_recv`를 호출하여 KCP에서 분석된 데이터를 수신합니다.

<details>
<summary> 데이터 수신 (코드 펼치기 클릭) </summary>
```cpp
//---------------------------------------------------------------------
// input data
//---------------------------------------------------------------------
int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    IUINT32 prev_una = kcp->snd_una;
    IUINT32 maxack = 0, latest_ts = 0;
    int flag = 0;

합법성 검사
    if (data == NULL || (int)size < (int)IKCP_OVERHEAD) return -1;

// 데이터는 여러 개의 KCP 패킷일 수 있으며, 루프로 처리합니다.
    while (1) {
        IUINT32 ts, sn, len, una, conv;
        IUINT16 wnd;
        IUINT8 cmd, frg;
        IKCPSEG *seg;

// 한 개의 KCP 패킷이 부족하여 종료합니다.
        if (size < (int)IKCP_OVERHEAD) break;

// 먼저 제어 필드를 해석합니다.
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

// 데이터 패킷 유형 확인
        if (cmd != IKCP_CMD_PUSH && cmd != IKCP_CMD_ACK &&
            cmd != IKCP_CMD_WASK && cmd != IKCP_CMD_WINS) 
            return -3;

        kcp->rmt_wnd = wnd;

여기서의 'una'는 송신측의 'kcp->rcv_nxt'입니다. 이 데이터를 기반으로 이미 확인된 수신 데이터 패킷을 제거할 수 있습니다.
        ikcp_parse_una(kcp, una);
확인된 패킷을 제거한 후에, snd_una를 업데이트하여 다음으로 보낼 일련번호를 설정합니다.

        ikcp_shrink_buf(kcp);

        if (cmd == IKCP_CMD_ACK) {
// 감사 패킷
            // ...
        }
        else if (cmd == IKCP_CMD_PUSH) {
데이터 패키지
수신된 데이터 패킷의 일련 번호 `sn`이 수신 창 안에 있다면 정상적으로 처리하고, 그렇지 않으면 직접 버리고 재전송을 기다립니다.
            if (_itimediff(sn, kcp->rcv_nxt + kcp->rcv_wnd) < 0) {

받은 각 데이터 패킷마다 ack 패킷을 보내고 기록해야 합니다.
                ikcp_ack_push(kcp, sn, ts);

// 받은 데이터를 ikcp_parse_data를 호출해 처리합니다.
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
// 창문 패키지 조회
            // ...
        }
        else if (cmd == IKCP_CMD_WINS) {
// 응답 패킷을 찾습니다.
            // ...
        }
        else {
            return -3;
        }

        data += len;
        size -= len;
    }

빠른 재전송 로직을 처리합니다.
    // ...

업데이트 전송 창
    // ...

    return 0;
}
```
</details>

`ikcp_input`는 각 `SEG` 패킷을 순환하며 처리합니다. 먼저 패킷의 유효성과 종류를 확인합니다. 각 데이터 패킷에는 발신 측이 수신을 기다리는 패킷 번호가 포함되어 있는데, 이 번호보다 작아야 하는 패킷은 상대방이 이미 성공적으로 수신했다는 뜻입니다. 따라서 `una`보다 작은 패킷은 `snd_buff`에서 삭제하고 `snd_nxt`를 업데이트해야 합니다. 이 작업은 `ikcp_parse_una`와 `ikcp_shrink_buf`에서 처리됩니다. 각 받은 데이터 패킷은 ACK 패킷을 응답해야 하며, 이 정보는 `ikcp_ack_push`에 기록됩니다. 마지막으로 `ikcp_parse_data`를 호출하여 데이터를 처리합니다.

<details>
<요약> 데이터 분석하기 (코드 펼치기 클릭) </요약>
```cpp
void ikcp_parse_data(ikcpcb *kcp, IKCPSEG *newseg)
{
    struct IQUEUEHEAD *p, *prev;
    IUINT32 sn = newseg->sn;
    int repeat = 0;

// 일련번호 확인
    if (_itimediff(sn, kcp->rcv_nxt + kcp->rcv_wnd) >= 0 ||
        _itimediff(sn, kcp->rcv_nxt) < 0) {
        ikcp_segment_delete(kcp, newseg);
        return;
    }

newseg가 위치해야 하는 곳을 찾으십시오. 왜냐하면 받은 seg가 뒤죽박죽일 수 있기 때문입니다.
    for (p = kcp->rcv_buf.prev; p != &kcp->rcv_buf; p = prev) {
        IKCPSEG *seg = iqueue_entry(p, IKCPSEG, node);
        prev = p->prev;
        if (seg->sn == sn) {
// 반복 수신
            repeat = 1;
            break;
        }
        if (_itimediff(sn, seg->sn) > 0) {
            break;
        }
    }

newseg을 rcv_buf의 올바른 위치에 두세요.
    if (repeat == 0) {
        iqueue_init(&newseg->node);
        iqueue_add(&newseg->node, p);
        kcp->nrcv_buf++;
    }    else {
        ikcp_segment_delete(kcp, newseg);
    }

rcv_buf에서 rcv_queue로 데이터를 이동합니다.
    while (! iqueue_is_empty(&kcp->rcv_buf)) {
        IKCPSEG *seg = iqueue_entry(kcp->rcv_buf.next, IKCPSEG, node);
// 만약 seg의 번호가 받을 준비가 된 번호라면, rcv_queue로 이동합니다.
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

'ikcp_parse_data' 함수의 주요 작업은 'newseg'를 'kcp->rcv_buf'에 적절한 위치에 넣고, 데이터를 'rcv_buf'에서 'rcv_queue'로 이동하는 것입니다. 'rcv_buf'의 적절한 위치는 'sn'에 따라 오름차순으로 정렬되어 있으며, 'newseg'는 자신의 'sn' 크기에 맞는 위치를 찾아야 합니다. 'rcv_buf'에 있는 데이터를 'rcv_queue'로 이동해야 하는 조건은 'rcv_buf'에 있는 데이터 패킷 번호가 KCP가 기다리는 패킷 번호 'kcp->rcv_nxt'와 동일한 경우입니다. 데이터 패킷을 하나 이동한 후에는 'kcp->rcv_nxt'를 업데이트하고, 그 다음 데이터 패킷을 처리해야 합니다.

`ikcp_input` 이후, 상위 호출에서 `ikcp_update`를 호출하면 ACK 패킷이 전송됩니다. `ikcp_recv`를 호출하면 상위로 유효한 데이터가 반환됩니다. `ikcp_update`와 `ikcp_recv`는 상호 독립적이며 호출 순서 요구사항이 없으며, 상위 호출 시기에 따라 달라집니다. 먼저 ACK 전송 관련 부분이 있는 `ikcp_update`를 살펴보겠습니다:

<details>
<summary> 답장 ACK(코드 펼치기) </summary>
```cpp
앞에서 말했듯이, ikcp_update는 결국 ikcp_flush를 호출합니다.
void ikcp_flush(ikcpcb *kcp, IUINT32 current)
{
    // ...

ACK 패킷에 회신합니다.
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

ACK 패킷은 이미 `ikcp_ack_push`에 의해 이전에 저장되었으므로 여기서는 각 ACK 패킷의 정보를 얻고 상대방에게 전송하기만 하면 됩니다. 상위 레벨에서는 `ikcp_recv`를 사용하여 KCP에서 데이터를 가져올 수 있습니다:

<details>
<summary>ikcp_recv(코드 펼치기)</summary>
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

일부 유효성 검사
    if (iqueue_is_empty(&kcp->rcv_queue))
        return -1;
    if (len < 0) len = -len;

// 반환할 수 있는 데이터 길이 계산
    peeksize = ikcp_peeksize(kcp);

    if (peeksize < 0)
        return -2;
    if (peeksize > len)
        return -3;

// 수신 창 크기 확인
    if (kcp->nrcv_que >= kcp->rcv_wnd)
        recover = 1;

rcv_queue를 반복하여 데이터를 buffer로 복사합니다.
    for (len = 0, p = kcp->rcv_queue.next; p != &kcp->rcv_queue; ) {
        int fragment;
        seg = iqueue_entry(p, IKCPSEG, node);
        p = p->next;

        if (buffer) {
            memcpy(buffer, seg->data, seg->len);
            buffer += seg->len;
        }

        len += seg->len;

// 분할 포장 판단
        fragment = seg->frg;

데이터 패키지를 제거하세요.
        if (ispeek == 0) {
            iqueue_del(&seg->node);
            ikcp_segment_delete(kcp, seg);
            kcp->nrcv_que--;
        }

// 모든 하위 패키지가 복사되었습니다. 루프를 종료합니다.
        if (fragment == 0)
            break;
    }

    assert(len == peeksize);

rcv_queue가 또 조금 비었는데 rcv_buf에서 rcv_queue로 계속 이동을 시도해 봅니다.
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

`ikcp_recv` 함수는 한 번 호출할 때 완전한 데이터 패킷 하나만 반환하며, 상위 레벨에서 데이터가 더 이상 반환되지 않을 때까지 반복해서 호출할 수 있습니다. 함수의 로직은 꽤 간단합니다. `rcv_queue`에서 데이터를 상위로 전달된 `buffer`로 복사하는 것뿐입니다. 이로써 수신 측은 받은 데이터 패킷을 처리했습니다.

수신 측이 데이터 패킷을 처리할 때 ACK 패킷을 송신 측에 전송했습니다. 이제 송신 측이 ACK 패킷을 받아들이는 처리를 살펴봅시다:

<details>
<summary> ACK 패킷 처리 (코드 펼치기) </summary>
```cpp
int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    // ...
    IUINT32 maxack = 0, latest_ts = 0;
    // ...
    while (1) {
        // ...
// ts refers to the kcp->current on the opposite end
        data = ikcp_decode32u(data, &ts);
        data = ikcp_decode32u(data, &sn);

        if (cmd == IKCP_CMD_ACK) {
// rot 업데이트
            if (_itimediff(kcp->current, ts) >= 0) {
                ikcp_update_ack(kcp, _itimediff(kcp->current, ts));
            }
// snd_buf 업데이트
            ikcp_parse_ack(kcp, sn);
            ikcp_shrink_buf(kcp);

// maxack = 이번 입력의 모든 ACK 패킷 중에서 가장 큰 sn
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

ACK 패킷을 수신한 경우, 빠른 재전송을 위해 기록합니다.
    if (flag != 0) {
        ikcp_parse_fastack(kcp, maxack, latest_ts);
    }
}
```
</details>

ACK 패킷 수신 후 `ikcp_parse_ack` 및 `ikcp_shrink_buf` 함수를 사용하여 `snd_buf`를 업데이트해야 함을 볼 수 있습니다. 또한 `ikcp_update_ack`를 호출하여 rto(재전송 시간 초과)를 업데이트해야 합니다. `ikcp_input`은 수신한 ACK 패킷에서 최대 일련 번호를 계산하여 빠른 재전송을 위해 기록합니다. 송신 측은 ACK 패킷을 받으면 `snd_buf`에서 데이터를 제거하고 해당 데이터 패킷이 수신 측으로 안전하게 전달되었음을 의미하며, 전체적인 ARQ 확인 수신 과정이 완료됩니다.

###업로드 시간 초과 후 재전송

앞서 설명한 것은 KCP에서 구현된 ARQ의 확인 수신기 메커니즘이었습니다. ARQ는 신뢰성을 보장하기 위해 타임아웃 재전송이 필요합니다. 이제 KCP가 타임아웃 재전송을 어떻게 수행하는지 살펴보겠습니다.

`ikcp_flush` 함수로 돌아가 봅시다:

<details>
<요약> 타임 아웃 재전송(코드 펼치기를 클릭하세요) </요약>
```cpp
void ikcp_flush(ikcpcb *kcp)
{
    // ...
// snd_buf를 전송합니다.
    for (p = kcp->snd_buf.next; p != &kcp->snd_buf; p = p->next) {
        IKCPSEG *segment = iqueue_entry(p, IKCPSEG, node);
        int needsend = 0;
        if (segment->xmit == 0) {
첫 전송
            needsend = 1;
            segment->xmit++;
// 세그먼트->rto 설정
segment->rto를 사용하여 segment->resendts의 타임아웃 재전송 시간을 계산합니다.
            segment->rto = kcp->rx_rto;
            segment->resendts = current + segment->rto + rtomin;
        }
        else if (_itimediff(current, segment->resendts) >= 0) {
// 시간 초과 재전송
            needsend = 1;
            segment->xmit++;
            kcp->xmit++;
// nodelay controls the calculation of the next timeout retransmission time.
            if (kcp->nodelay == 0) {
                segment->rto += kcp->rx_rto;
            }    else {
                segment->rto += kcp->rx_rto / 2;
            }
            segment->resendts = current + segment->rto;
            lost = 1;
        }
        else if (segment->fastack >= resent) {
빠른 재전송
            // ...
        }
        if (needsend) {
// 데이터 전송
            // ...
        }
    // ...
}
```
</details>

현재 시간인 `current`이 `segment->resendts` 재전송 시간을 초과하면 해당 시간 동안 수신 측 ACK 패킷을 받지 못한 것으로 판단되어 타임아웃 재전송 메커니즘이 트리거되고, `needsend = 1`로 데이터를 다시 전송하게 됩니다.

확인 수신과 타임아웃 재전송 메커니즘을 사용하면 KCP는 기본 신뢰성 있는 데이터 전송을 보장할 수 있습니다. 그러나 더 안정적인 데이터 흐름을 유지하기 위해 KCP는 추가적인 작업을 수행했습니다. 아래에서 KCP가 어떤 최적화를 수행했는지 살펴보겠습니다.

##KCP의 유속 향상 전략

###빨리 재전송

발신자가 'sn'과 'sn + 1' 두 데이터 패킷을 보냈어. 'sn + 1'의 ACK 패킷만 받았다면, 'sn'의 ACK 패킷이 네트워크에 도착하기 전이거나 ACK 패킷이 누락되었거나, 'sn' 데이터 패킷이 누락된 걸지도 몰라. 이때 아직 재전송 시간이 아니거나 네트워크가 혼잡하지 않다면, 갑자기 패킷이 누락된 이유 때문이었을 걸; 발신자가 'sn' 데이터 패킷을 미리 보내면 수신측이 더 빨리 데이터를 받을 수 있게 해주고 흐름을 향상시켜 줄 수 있어.

KCP 내부에는 빠른 재전송 메커니즘이 구현되었고, `ikcp_flush` 함수에서도 그 역할을 합니다.

<details>
<요약> 빠른 재전송 (코드 펼치기를 클릭하십시오) </요약>
```cpp
void ikcp_flush(ikcpcb *kcp)
{
    // ...
    resent = (kcp->fastresend > 0)? (IUINT32)kcp->fastresend : 0xffffffff;

// 송신 snd_buf
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
빠른 재전송 
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
// 데이터 전송
            // ...
        }
    // ...
}
```
</details>

출발하려면 빠른 재전송이 필요합니다. 두 가지 조건이 있습니다:
`segment->fastack >= resent`은 `resent`가 설정 가능한 매개변수인 `kcp->fastresend`에 해당합니다. 만약 0으로 설정하면 빠른 재전송이 비활성화됩니다. `segment->fastack`는 `ikcp_parse_fastack` 함수에서 설정됩니다. 이 함수는 `ikcp_input` 함수 내부에서 호출되며 `ikcp_input`에서 계산된 `maxack`에 기초하여 `maxack`보다 작은 모든 `sn`에 대해 `segment->fastack`를 증가시킵니다. 따라서 `segment->fastack`는 `sn`보다 큰 패킷을 받은 횟수를 나타냅니다.
`segment->xmit <= kcp->fastlimit || kcp->fastlimit <= 0`，`setgment->xmit` is the number of transmissions, `kcp->fastlimit` is the configurable maximum number of fast retransmissions, and the number of transmissions must be less than the maximum number of fast retransmissions.

위 조건들이 충족되면, KCP는 빠른 재전송을 실행하며, 빠른 재전송은 타임아웃 재전송 시간을 초기화하지 않음에 주의해야 합니다. 이전의 타임아웃 시간은 여전히 유효합니다.

###시간 초과 재전송 시간을 단축하십시오.

컴팩트한 전송(Compact Transmission)은 좋은 메커니즘이지만, 시간을 너무 많이 소모하죠. TCP 전략을 따르면, 매번 컴팩트한 전송이 시간이 두 배로 증가하고, 대기 시간이 급증합니다. 대기 시간 동안, 수신 창문이 이미 다 차서 새로운 데이터를 받을 수 없는 상황이 발생할 수 있습니다. 또한 다시 전송을 기다리는 패킷 번호가 가장 앞에 위치하므로, 수신측은 모든 데이터를 상위 계층으로 반환하려면 재전송된 패킷을 수신해야 합니다. 이러한 상황에서 전체 네트워크의 스르밍 속도는 거의 0에 가깝습니다. KCP는 대기 시간 증가를 완화할 수 있는 구성을 추가했는데, 그리고 두 배로 증가하지 않도록 조정되었어요. `kcp->nodelay`를 통해 설정하여, 각 대기 시간은 RTO의 1배 또는 0.5배만 증가하게 제어할 수 있어서, 대기 시간의 증가를 효과적으로 완화하여 네트워크가 빠르게 스트리밍 속도를 회복할 수 있도록 도와줍니다.

###발신 창 업데이트

송신 창은 동시에 전송되는 데이터 패킷의 수를 나타내며, 창이 클수록 동시에 전송되는 데이터가 많아지고 흐름이 빨라집니다. 그러나 창이 너무 커지면 네트워크 혼잡을 초래하여 패킷 손실률이 증가하고, 데이터 재전송이 늘어나며 흐름이 감소합니다. 따라서 송신 창은 네트워크 상황에 따라 지속적으로 업데이트되어 최적에 가까워져야 합니다. KCP에서 송신 창과 관련된 코드:

<details>
<summary>창 보내기(코드 펼치기 클릭)</summary>
```cpp
ikcpcb* ikcp_create(IUINT32 conv, void *user)
{
    // ...
// snd_wnd, rcv_wnd은 전송 및 수신 버퍼의 크기입니다.
    kcp->snd_wnd = IKCP_WND_SND;    // 32
    kcp->rcv_wnd = IKCP_WND_RCV;    // 128
// 수신 창 크기             // 128
    kcp->rmt_wnd = IKCP_WND_RCV
// 전송 창 cwnd 초기화 0
    kcp->cwnd = 0;
// 창 크기 바이트 수를 보내어 cwnd를 계산합니다.
    kcp->incr = 0
느린 시작 임계값
    kcp->ssthresh = IKCP_THRESH_INIT;
nocwnd은 구성 가능한 매개변수로, 1은 cwnd를 고려하지 않습니다.
    kcp->nocwnd = 0;
    // ...
}

void ikcp_flush(ikcpcb *kcp)
{
    // ...
데이터를 전송할 때 먼저 전송 창 크기를 계산하십시오. 이는 송신 버퍼 크기 및 상대방의 수신 창 크기 중 작은 값입니다.
    cwnd = _imin_(kcp->snd_wnd, kcp->rmt_wnd);
기본적으로는 kcp->cwnd인 계속 업데이트되는 전송 창 크기를 고려해야 합니다.
    if (kcp->nocwnd == 0) cwnd = _imin_(kcp->cwnd, cwnd);

cwnd 크기에 따라 snd_queue가 snd_buf로 이동합니다.
    while (_itimediff(kcp->snd_nxt, kcp->snd_una + cwnd) < 0) {
    }
// 데이터 전송
    resent = (kcp->fastresend > 0)? (IUINT32)kcp->fastresend : 0xffffffff;
// 타임아웃으로 재전송 트리거되었습니다. lost = 1
// 빠른 재전송 트리거 변경++

// 느린 시작 임계값과 송신 윈도우를 업데이트합니다.
    if (change) {
만약 빠른 재전송이 발생한다면, ssthresh는 네트워크를 통해 전송 중인 데이터 패킷 수의 절반으로 설정됩니다.
        IUINT32 inflight = kcp->snd_nxt - kcp->snd_una;
        kcp->ssthresh = inflight / 2;
        if (kcp->ssthresh < IKCP_THRESH_MIN)
            kcp->ssthresh = IKCP_THRESH_MIN;

// 발신 창 크기는 임계 값에 빠른 재전송 관련 resent를 더한 것입니다.
        kcp->cwnd = kcp->ssthresh + resent;
        kcp->incr = kcp->cwnd * kcp->mss;
    }

    if (lost) {
만약 타임아웃 되었다면, 슬로 스타트를 시작해서 ssthresh 값을 전송 창의 절반으로 설정합니다.
        kcp->ssthresh = cwnd / 2;
        if (kcp->ssthresh < IKCP_THRESH_MIN)
            kcp->ssthresh = IKCP_THRESH_MIN;
// 창 크기를 1로 다시 설정하여 천천히 증가 시작합니다.
        kcp->cwnd = 1;
        kcp->incr = kcp->mss;
    }

    if (kcp->cwnd < 1) {
// 초기값이 0으로 설정되어 있어서 여기에 도달하면 1로 다시 설정됩니다.
        kcp->cwnd = 1;
        kcp->incr = kcp->mss;
    }
}

int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    IUINT32 prev_una = kcp->snd_una;
수신된 데이터 처리

    while (1) {
        // ...
        data = ikcp_decode16u(data, &wnd)
// rmt_wnd 는 상대방의 수신 창 크기입니다
        kcp->rmt_wnd = wnd
        // ...
// 데이터 처리
    }

최종 업데이트 송수신 창口
kcp->snd_una - prev_una > 0, indicates that this input has received an ACK and the sending buffer snd_buf has changed.
    if (_itimediff(kcp->snd_una, prev_una) > 0) {
상대의 수신 창을 다시 확인하십시오.
        if (kcp->cwnd < kcp->rmt_wnd) {
            IUINT32 mss = kcp->mss;

            if (kcp->cwnd < kcp->ssthresh) {
// 작은 값일 때, 두 배로 증가합니다.
                kcp->cwnd++;
                kcp->incr += mss;

            }    else {
스로 시작 임계값을 초과하면 증가를 업데이트하는 공식을 통해 cwnd를 계산합니다.
                if (kcp->incr < mss) kcp->incr = mss;
                kcp->incr += (mss * mss) / kcp->incr + (mss / 16);
                if ((kcp->cwnd + 1) * mss <= kcp->incr) {
                    kcp->cwnd++;
                }
            }
// 업데이트된 값은 rmt_wnd와 다시 비교해야 합니다.
            if (kcp->cwnd > kcp->rmt_wnd) {
                kcp->cwnd = kcp->rmt_wnd;
                kcp->incr = kcp->rmt_wnd * mss;
            }
        }
    }
}
```
</details>

`kcp->cwnd` 크기를 계산하는 코드 조각은 약간 더 많다. 데이터를 보내고 받을 때마다 업데이트해야 하기 때문이다. `kcp->cwnd`는 0으로 초기화된다.
`ikcp_flush`가 처음 호출될 때 1보다 작은 경우 1로 수정됩니다. 그런 다음 송신 측은 송신 윈도우 크기에 따라 해당하는 데이터 패킷을 전송하고 ACK를 기다립니다.
ACK 패킷에 대한 응답입니다. `kcp->input`에서 ACK 패킷을 처리하며, `kcp->input`에서 ACK 패킷이 감지되고 송신 버퍼에서 송신 데이터 패킷이 삭제되면 데이터 패킷이 이미 전달된 것을 의미하며, `kcp->cwnd++`가 실행됩니다. 사실 한 번에 `kcp->input`가 하나의 ACK 패킷만 처리하기도 합니다. 이해할 수 있듯이, ACK 패킷을 받을 때마다 `kcp->cwnd++`가 실행되며, 이 증가 구현은 두 배 효과를 제공합니다. 예를 들어 현재 `kcp->cwnd = 2`이고, 두 개의 데이터 패킷을 전송하고, 두 개의 ACK 패킷을 받으면 두 번의 자가증이가 발생하여 최종적으로 `kcp->cwnd = 4`인 두 배로 증가합니다.

cwnd는 지수적으로 증가할 수 있으며 Congestion Timeout이나 Fast Retransmit이 발생하여 Slow Start threshold를 초과할 때까지입니다. Congestion Timeout이 발생하면 Slow Start가 트리거되고 Slow Start threshold ssthresh = kcp->cwnd / 2, 송신창 kcp->cwnd = 1로 초기화되어 처음부터 다시 지수적으로 증가합니다. Fast Retransmit이 발생하면 KCP는 미리 ssthresh를 줄이고, 따라서 증가 속도를 낮춘 cwnd의 지수적 증가 공간을 줄여 Congestion을 조기에 완화합니다.

KCP는 'nocwnd'라는 설정을 추가했습니다. 'nocwnd = 1'로 설정하면 데이터를 전송할 때 더 이상 전송 창 크기를 고려하지 않고, 최대 전송 가능한 양의 데이터 패킷을 바로 전송하여 고속 모드 요구 사항을 충족합니다.

##결론

이 문서는 간단히 KCP의 소스 코드를 분석하고, KCP에서 ARQ를 구현하는 방법 및 KCP의 속도를 향상시키는 몇 가지 전략을 논의합니다. 많은 세부 사항이 언급되지 않았지만 관심 있는 사람은 KCP의 소스 코드를 직접 살펴보면서 비교해 볼 수 있으며, 분명히 많은 것을 얻을 수 있을 것이라고 믿습니다.

--8<-- "footer_ko.md"


> 본 게시물은 ChatGPT로 번역되었습니다. 문제가 있으면 [**피드백**](https://github.com/disenone/wiki_blog/issues/new)어떤 빠진 부분이나 오류를 지적해 주세요. 
