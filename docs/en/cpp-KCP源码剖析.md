---
layout: post
title: Analysis of KCP Source Code
categories:
- c++
catalog: true
tags:
- dev
description: This article briefly analyzes the source code of KCP, discusses the implementation
  of ARQ on KCP, and some strategies to improve the flow rate of KCP.
figures: []
---

<meta property="og:title" content="KCP 源码剖析" />

Before reading this article, if you haven't heard of KCP or have no understanding of it at all, please take a moment to check out the project's documentation: [Portal](https://github.com/skywind3000/kcp)The purpose of this article is to delve into the implementation details of KCP in order to understand KCP better.

##What is KCP

KCP is a fast and reliable protocol that transmits data with lower latency than TCP, achieves quicker data retransmission, and has shorter waiting times.

> TCP is designed for traffic (how much data in KB can be transmitted per second), focusing on maximizing bandwidth utilization. In contrast, KCP is designed for speed (how much time it takes for a single data packet to be sent from one end to another), sacrificing 10%-20% of bandwidth for a 30%-40% faster transfer rate compared to TCP. A TCP channel is like a slow-moving but high-capacity canal, while KCP is akin to a swift and turbulent stream.

The above is written in the KCP documentation. The keywords are **bandwidth** and **throughput**. KCP will consume bandwidth, but the benefit is a larger and more balanced transmission rate. For further details, please refer to the KCP documentation itself.

##KCP data structure

The source code of KCP is found in `ikcp.h` and `ikcp.c`. The core of `ikcp.h` is the declaration of data structures, primarily the `SEGMENT` packet, which is the smallest unit of data processed by the KCP protocol.

<details>
<summary> SEGMENT structure (click to expand code) </summary>
```cpp
//=====================================================================
// SEGMENT A SETMENT is a data packet.
//=====================================================================
struct IKCPSEG
{
// Linked list node, both the sending and receiving queues are structured as linked lists here.
    struct IQUEUEHEAD node;

Session ID, the same session ID is identical
    IUINT32 conv;

Packet type, such as DATA or ACK.
    IUINT32 cmd;

Due to the MTU limitation, large data packets will be fragmented into multiple smaller packets, and this is the sequence number of the small packet.
    IUINT32 frg

Every data packet will come with the sender's receive window size.
    IUINT32 wnd;

Transmission time, if it is an ACK packet, will be set as the timestamp of the original data packet.
    IUINT32 ts;

// The unique identifier number for the data packet
    IUINT32 sn;

// It indicates that all packets smaller than una have been successfully received, consistent with the meaning in TCP: the oldest unacknowledged sequence number SND.
    IUINT32 una;

Data length
    IUINT32 len;

Retransmission Timeout.
    IUINT32 resendts;

// Next timeout waiting time
    IUINT32 rto;

// Fast retransmission. The number of packets received after this data packet, if it exceeds a certain amount, will trigger fast retransmission.
    IUINT32 fastack;

Number of times sent
    IUINT32 xmit;

// Data
    char data[1];
};
```
</details>

After reading the comments on `SEGMENT`, one can roughly see that the core of KCP is also an ARQ protocol, which ensures data delivery through automatic timeout retransmission. Next, let's take a look at the definition of the KCP structure `KCPCB`:

<details>
<summary> KCP Structure (Click to Expand Code) </summary>
```cpp
//---------------------------------------------------------------------
// IKCPCB
//---------------------------------------------------------------------
struct IKCPCB
{
// Session ID
// mtu, mss: Maximum Transmission Unit, Maximum Segment Size
// state: Session state, 0 valid, -1 disconnected
    IUINT32 conv, mtu, mss, state;

// snd_una: The packet number waiting for ACK
// snd_nxt: The packet number of the next data to be sent
// rcv_nxt: Next sequence number of the data packet waiting to be received
    IUINT32 snd_una, snd_nxt, rcv_nxt;

// ts_recent, ts_lastack: Not in use
// ssthresh: Congestion Control Slow Start Threshold
    IUINT32 ts_recent, ts_lastack, ssthresh;

// rx_rto: rto (retransmission timeout), the time for retransmitting after timeout
// rx_rttval, rx_srtt, rx_minrto: Intermediate variables for calculating the RTO
    IINT32 rx_rttval, rx_srtt, rx_rto, rx_minrto;

// snd_wnd, rcv_wnd: Maximum sizes of the sending and receiving windows.
remote window: Remaining Receive Window size on the remote end
// cwnd: Size of the send window
// probe: Indicates whether to send the control message
    IUINT32 snd_wnd, rcv_wnd, rmt_wnd, cwnd, probe;

current: current time
interval: refresh rate
// ts_flush: The next time the update is needed
// xmit: Number of transmission failures
    IUINT32 current, interval, ts_flush, xmit;

The length of the corresponding linked list.
    IUINT32 nrcv_buf, nsnd_buf;
    IUINT32 nrcv_que, nsnd_que;

// nodelay: Controls the growth rate of the RTO for timeout retransmissions
// updated: Whether ikcp_update has been called
    IUINT32 nodelay, updated;

// ts_probe, probe_wait: Actively initiate inquiries periodically when the receiving window on the other end remains 0 for an extended period.
    IUINT32 ts_probe, probe_wait;

deal_link: The other end is not responding for an extended period.
// incr: Participates in calculating the send window size
    IUINT32 dead_link, incr;

// queue: Data packets that interact with the user layer
// buf: Protocol buffer data packet
    struct IQUEUEHEAD snd_queue;
    struct IQUEUEHEAD rcv_queue;
    struct IQUEUEHEAD snd_buf;
    struct IQUEUEHEAD rcv_buf;

// Information about the packets that need to send an ack
    IUINT32 *acklist;

// Number of packets that require ack
    IUINT32 ackcount;

// Blacklist memory size
    IUINT32 ackblock;

// Data passed in from the user layer
    void *user;

// Space to store a kcp packet
    char *buffer;

// The number of fastack triggers for fast retransmission
    int fastresend;

Maximum number of fast retransmissions
    int fastlimit;

// nocwnd: Ignore the slow start size of the sending window
// stream: streaming mode
    int nocwnd, stream;

    // debug log
    int logmask;

Send data interface
    int (*output)(const char *buf, int len, struct IKCPCB *kcp, void *user);

    void (*writelog)(const char *log, struct IKCPCB *kcp, void *user);
};
```
</details>

Annotate the fields inside the KCP data structure one by one. You will start to get a sense that the KCP protocol suite is not too complex. By carefully analyzing the code, both you and I can read and understand the KCP protocol. 😊

##KCP's ARQ Implementation

KCP is essentially an ARQ (Automatic Repeat reQuest) protocol, whose fundamental goal is to ensure reliable transmission. So let's first focus on the basic ARQ component of KCP and how it achieves reliable transmission.

ARQ, as the name implies, automatically retransmits corresponding data packets when we consider that the receiving end has failed to receive them, achieving reliable transmission through two mechanisms: acknowledgment reception and timeout retransmission. In terms of specific code implementation, KCP assigns a unique 'sn' identifier to each data packet (which was mentioned in the previous section as a 'SEGMENT'). Once the receiving end receives a data packet, it replies with an ACK packet (also a 'SEGMENT') where the 'sn' of the ACK packet is the same as the 'sn' of the received data packet, indicating successful reception of that data packet. The 'SEGMENT' also includes a 'una' field, indicating the number of the next expected data packet to be received. In other words, all data packets with numbers before this are already received, essentially serving as a full acknowledgment packet. This allows the sending end to quickly update its sending buffer and sending window.

We can understand the most basic ARQ implementation by tracking the sending and receiving code of KCP packets.

###Send

The process involves `ikcp_send` -> `ikcp_update` -> `ikcp_output`, where the upper layer invokes `ikcp_send` to pass data to KCP, and KCP handles data transmission in `ikcp_update`.

<details>
<summary> ikcp_send (click to expand code) </summary>
```cpp
//---------------------------------------------------------------------
// Data transmission interface, users use ikcp_send to instruct kcp to send data
// user/upper level send, returns below zero for error
//---------------------------------------------------------------------
int ikcp_send(ikcpcb *kcp, const char *buffer, int len)
{
    IKCPSEG *seg;
    int count, i;

// mss cannot be less than 1
    assert(kcp->mss > 0);
    if (len < 0) return -1;

    // append to previous segment in streaming mode (if possible)
    if (kcp->stream != 0) {
Stream processing mode
        // ......
    }

// Calculate subpackets. If the data length len is greater than mss, it needs to be divided into multiple packets for sending, which will be reassembled by the recipient upon receipt.
    if (len <= (int)kcp->mss) count = 1;
    else count = (len + kcp->mss - 1) / kcp->mss;

    if (count >= (int)IKCP_WND_RCV) return -2;

    if (count == 0) count = 1;

// Subcontracting
    for (i = 0; i < count; i++) {
Calculate the length of the packet data and allocate the corresponding seg structure.
        int size = len > (int)kcp->mss ? (int)kcp->mss : len;
        seg = ikcp_segment_new(kcp, size);
        assert(seg);
        if (seg == NULL) {
            return -2;
        }

// Set the data information for seg, where frg represents the subpackage number.
        if (buffer && len > 0) {
            memcpy(seg->data, buffer, size);
        }
        seg->len = size;
        seg->frg = (kcp->stream == 0)? (count - i - 1) : 0;

// Add to the end of the snd_queue, increase nsnd_qua by one
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

`ikcp_send` is the interface for sending data called by the upper layer of KCP. All data intended for KCP transmission should go through this interface. The function of `ikcp_send` is quite simple; it primarily divides the data into multiple packets based on `kcp->mss` (the maximum data length of a packet), assigns segment numbers, and finally appends them to the end of the send queue `snd_queue`. The stream mode treats the data from multiple calls to `ikcp_send` as a single stream, automatically filling any incomplete `SEGMENT` before allocating new ones. This article will not delve into the detailed implementation, but for those interested, understanding the code after reading this will be insightful.

After the `ikcp_send` function is called, the data is placed in the `snd_queue` of KCP. Later on, KCP needs to find an opportunity to send out the pending data. This part of the code is all located within the `ikcp_update` and `ikcp_flush` functions.

<details>
<summary> ikcp_update (click to expand code) </summary>
```cpp
//---------------------------------------------------------------------
// ikcp_update is an interface that should be regularly called by the upper layer to update the kcp status and send data.
// update state (call it repeatedly, every 10ms-100ms), or you can ask 
// ikcp_check when to call it again (without ikcp_input/_send calling).
// 'current' - current timestamp in millisec. 
//---------------------------------------------------------------------
void ikcp_update(ikcpcb *kcp, IUINT32 current)
{
    IINT32 slap;

    kcp->current = current;

// ikcp_flush will check this, the upper layer must have called ikcp_update before calling ikcp_flush, it is recommended to only use ikcp_update.
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
// The time for the next flush
        kcp->ts_flush += kcp->interval;
        if (_itimediff(kcp->current, kcp->ts_flush) >= 0) {
            kcp->ts_flush = kcp->current + kcp->interval;
        }
        ikcp_flush(kcp);
    }
}
```
</details>

The function `ikcp_update` does something very simple - it checks the timestamp of `ts_flush`, if it meets the conditions, it calls `ikcp_flush`. The main processing logic is contained within `ikcp_flush` because it is a bit more complex. Currently, we are only focusing on the parts related to ARQ transmission.

<details>
<summary> Send Data (Click to Expand Code) </summary>
```cpp
//---------------------------------------------------------------------
// ikcp_flush
//---------------------------------------------------------------------
void ikcp_flush(ikcpcb *kcp)
{
    IUINT32 current = kcp->current;

The buffer is the data to be passed to ikcp_output, initialized to 3 times the packet size.
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

// seg.wnd represents the current receive window size
    seg.wnd = ikcp_wnd_unused(kcp);
    seg.una = kcp->rcv_nxt;
    seg.len = 0;
    seg.sn = 0;
    seg.ts = 0;

// Send ack
// Calculate the send window
    //...

Move the data packet from snd_queue to snd_buf.
// Movement needs to meet the size of the sending window; when the sending window is full, movement stops.
The data placed inside snd_buf is the data that can be directly sent to the peer by calling ikcp_output.
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

// seg The unique serial number, actually an increment of kcp->snd_nxt
        newseg->sn = kcp->snd_nxt++;

// una is set here to inform the other end of the next expected sequence number to receive
        newseg->una = kcp->rcv_nxt;
        newseg->resendts = current;
        newseg->rto = kcp->rx_rto;
        newseg->fastack = 0;
        newseg->xmit = 0;
    }

// Calculate fast retransmit flag, timeout waiting time
    // ...

// Send snd_buf
    for (p = kcp->snd_buf.next; p != &kcp->snd_buf; p = p->next) {
        IKCPSEG *segment = iqueue_entry(p, IKCPSEG, node);
        int needsend = 0;
        if (segment->xmit == 0) {
// First send
set->xmit indicates the number of transmissions.
// resendts The waiting time for timeout retransmission
            needsend = 1;
            segment->xmit++;
            segment->rto = kcp->rx_rto;
            segment->resendts = current + segment->rto + rtomin;
        }
        else if (_itimediff(current, segment->resendts) >= 0) {
// Timeout retransmission
            // ...
        }
        else if (segment->fastack >= resent) {
// Fast retransmission
            // ...
        }

        if (needsend) {
            int need;
            segment->ts = current;
            segment->wnd = seg.wnd;
            segment->una = kcp->rcv_nxt;

            size = (int)(ptr - buffer);
            need = IKCP_OVERHEAD + segment->len;

// Whenever the data in the buffer exceeds the mtu, it will be sent out first to avoid further segmentation at the lower level.
            if (size + need > (int)kcp->mtu) {
                ikcp_output(kcp, buffer, size);
                ptr = buffer;
            }

Copy the control data from "seg" to the buffer, letting KCP handle endianness on its own.
            ptr = ikcp_encode_seg(ptr, segment);

// Copy the data again
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

Calculate ssthresh, update slow start window
    // ...
}
```
</details>

We are currently only focusing on the logic related to sending data inside `ikcp_flush`.

First, KCP will move the data from `snd_queue` to `snd_buf` based on the receiving window size of the peer. The formula to calculate the number of data to move is `num = snd_nxt - (snd_una + cwnd)`, which means: if the sum of the maximum packet number successfully sent `snd_una` and the sliding window size `cwnd` is greater than the next packet number to be sent `snd_nxt`, then new data packets can be sent. While moving the `SEG`, control fields are also set.

Traverse `snd_buf`, if a data packet needs to be sent, copy the data to `buffer`, and at the same time use `ikcp_encode_seg` to handle the endianness of control field data.

Finally, call `ikcp_output` to send the data on `buffer` out.

At this point, KCP has completed the data transmission.

###Receive

The process of receiving is the opposite of sending: `ikcp_input` -> `ikcp_update` -> `ikcp_recv`. After the user receives data from the network, they need to call `ikcp_input` to pass the data to KCP for parsing. When `ikcp_update` is called, an ACK packet will be sent back to the sender, and the upper layer can receive the data parsed by KCP by calling `ikcp_recv`.

<details>
<summary>Receive Data (Click to Expand Code)</summary>
```cpp
//---------------------------------------------------------------------
// input data
//---------------------------------------------------------------------
int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    IUINT32 prev_una = kcp->snd_una;
    IUINT32 maxack = 0, latest_ts = 0;
    int flag = 0;

Legitimacy Check
    if (data == NULL || (int)size < (int)IKCP_OVERHEAD) return -1;

// data may consist of multiple KCP packets, processed in a loop
    while (1) {
        IUINT32 ts, sn, len, una, conv;
        IUINT16 wnd;
        IUINT8 cmd, frg;
        IKCPSEG *seg;

// Not enough for a KCP packet, exiting.
        if (size < (int)IKCP_OVERHEAD) break;

// First, parse out the control fields.
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

Packet type check
        if (cmd != IKCP_CMD_PUSH && cmd != IKCP_CMD_ACK &&
            cmd != IKCP_CMD_WASK && cmd != IKCP_CMD_WINS) 
            return -3;

        kcp->rmt_wnd = wnd;

Here, `una` is the `kcp->rcv_nxt` of the sender. Based on this data, the received data packets that have already been confirmed can be removed.
        ikcp_parse_una(kcp, una);
After removing the packets that have been acknowledged, update the next sequence number to be sent, snd_una.
        ikcp_shrink_buf(kcp);

        if (cmd == IKCP_CMD_ACK) {
            // ack package
            // ...
        }
        else if (cmd == IKCP_CMD_PUSH) {
// Data packet
// If the received packet sequence number sn is within the receiving window, process it normally; otherwise, discard it and wait for retransmission.
            if (_itimediff(sn, kcp->rcv_nxt + kcp->rcv_wnd) < 0) {

For each received data packet, it should send back an acknowledgment packet and keep a record of it.
                ikcp_ack_push(kcp, sn, ts);

// The received data is processed by calling ikcp_parse_data.
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
Query window package
            // ...
        }
        else if (cmd == IKCP_CMD_WINS) {
// Query window's reply packet
            // ...
        }
        else {
            return -3;
        }

        data += len;
        size -= len;
    }

Handle fast retransmission logic.
    // ...

// Update the sending window
    // ...

    return 0;
}
```
</details>

Process `ikcp_input` loops through each `SEG` packet, first checking the validity and type of the data packet. Since each data packet carries `una`, which holds the sequence number of the packets the sender is waiting to receive, any packet with a sequence number less than `una` has already been successfully received by the other party. Therefore, the packets in `snd_buff` that need to be less than `una` can be deleted, and `snd_nxt` can be updated. This part is handled by `ikcp_parse_una` and `ikcp_shrink_buf`. Each received data packet needs to reply with an ACK packet, which is recorded by `ikcp_ack_push`, and finally `ikcp_parse_data` is called to process the data.

<details>
<summary>Parse data (click to expand code)</summary>
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

// Find the position where newseg should be placed, because the received seg may be out of order.
    for (p = kcp->rcv_buf.prev; p != &kcp->rcv_buf; p = prev) {
        IKCPSEG *seg = iqueue_entry(p, IKCPSEG, node);
        prev = p->prev;
        if (seg->sn == sn) {
// Received repeatedly
            repeat = 1;
            break;
        }
        if (_itimediff(sn, seg->sn) > 0) {
            break;
        }
    }

// Place newseg in the correct position in rcv_buf
    if (repeat == 0) {
        iqueue_init(&newseg->node);
        iqueue_add(&newseg->node, p);
        kcp->nrcv_buf++;
    }    else {
        ikcp_segment_delete(kcp, newseg);
    }

// Move data from rcv_buf to rcv_queue
    while (! iqueue_is_empty(&kcp->rcv_buf)) {
        IKCPSEG *seg = iqueue_entry(kcp->rcv_buf.next, IKCPSEG, node);
Move to the rcv_queue if the segment number is the expected one for reception.
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

The main task of `ikcp_parse_data` is to place `newseg` into the appropriate position in `kcp->rcv_buf` and to move the data from `rcv_buf` to `rcv_queue`. The appropriate position in `rcv_buf` means that `rcv_buf` is arranged in increasing order of `sn`, and `newseg` needs to find the correct position based on its own `sn` size. Data in `rcv_buf` is moved to `rcv_queue` when the packet sequence number in `rcv_buf` matches the next expected packet sequence number that KCP is waiting to receive, `kcp->rcv_nxt`. After moving one packet, it is necessary to update `kcp->rcv_nxt` and then process the next packet.

After `ikcp_input`, when the upper layer calls `ikcp_update`, it will send an ACK packet, and calling `ikcp_recv` will return valid data to the upper layer. `ikcp_update` and `ikcp_recv` are independent of each other and have no order of invocation requirements, depending on the timing of the upper layer calls. Let's first look at the part in `ikcp_update` related to sending ACKs:

<details>
<summary> Reply ACK (Click to expand code) </summary>
```cpp
As mentioned earlier, ikcp_update ultimately calls ikcp_flush.
void ikcp_flush(ikcpcb *kcp, IUINT32 current)
{
    // ...

// Reply ACK packet
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

The previous ACK packets have been saved by `ikcp_ack_push`, so here you just need to use `ikcp_ack_get` to retrieve the information of each ACK packet and send it to the other party. The upper layer can use `ikcp_recv` to receive data from KCP:

<details>
ikcp_recv (Click to expand code)
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

// Some validity checks
    if (iqueue_is_empty(&kcp->rcv_queue))
        return -1;
    if (len < 0) len = -len;

// Calculate the length of data that can be returned
    peeksize = ikcp_peeksize(kcp);

    if (peeksize < 0)
        return -2;
    if (peeksize > len)
        return -3;

// Determine the reception window
    if (kcp->nrcv_que >= kcp->rcv_wnd)
        recover = 1;

Traverse the rcv_queue and copy the data to the buffer.
    for (len = 0, p = kcp->rcv_queue.next; p != &kcp->rcv_queue; ) {
        int fragment;
        seg = iqueue_entry(p, IKCPSEG, node);
        p = p->next;

        if (buffer) {
            memcpy(buffer, seg->data, seg->len);
            buffer += seg->len;
        }

        len += seg->len;

Determine subpackage.
        fragment = seg->frg;

// Remove packet
        if (ispeek == 0) {
            iqueue_del(&seg->node);
            ikcp_segment_delete(kcp, seg);
            kcp->nrcv_que--;
        }

// All subcontracting is completed, exit the loop
        if (fragment == 0)
            break;
    }

    assert(len == peeksize);

The rcv_queue has emptied some more, trying to continue moving from rcv_buf to rcv_queue.
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

The `ikcp_recv` function will only return a complete data packet for each call. The upper layer can repeatedly call it until no data is returned. The logic of the function is simple: it copies data from the `rcv_queue` to the `buffer` passed in by the upper layer. At this point, the receiver has finished processing the received data packet.

When the recipient processes the data packet, it sends an ACK packet to the sender. Let's now examine how the sender handles the received ACK packet:

<details>
<summary> Handle ACK packets (click to expand code) </summary>
```cpp
int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    // ...
    IUINT32 maxack = 0, latest_ts = 0;
    // ...
    while (1) {
        // ...
// ts is the kcp->current on the opposite end
        data = ikcp_decode32u(data, &ts);
        data = ikcp_decode32u(data, &sn);

        if (cmd == IKCP_CMD_ACK) {
Update rot.
            if (_itimediff(kcp->current, ts) >= 0) {
                ikcp_update_ack(kcp, _itimediff(kcp->current, ts));
            }
// Update snd_buf
            ikcp_parse_ack(kcp, sn);
            ikcp_shrink_buf(kcp);

// maxack = the largest sn among all the ACK packets in this input
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

If an ACK packet is received, record it for fast retransmission.
    if (flag != 0) {
        ikcp_parse_fastack(kcp, maxack, latest_ts);
    }
}
```
</details>

After receiving the ACK packet, it is necessary to use `ikcp_parse_ack` and `ikcp_shrink_buf` to update the `snd_buf`, and additionally call `ikcp_update_ack` to calculate the updated RTO (retransmission timeout). The `ikcp_input` function calculates the maximum sequence number from the received ACK packets to record it for fast retransmission purposes. In this way, once the sender receives the ACK packet, it removes the sent data from the `snd_buf`, confirming that the data packet has been reliably delivered to the receiver, thus completing a full ARQ acknowledgment process.

###Timeout retransmission

The previous section discussed the acknowledgment mechanism in ARQ implemented by KCP. In addition to acknowledgments, ARQ also requires a timeout retransmission mechanism to ensure reliability. Let's now explore how KCP handles timeout retransmissions.

Let's go back to the `ikcp_flush` function:

<details>
<summary> Timeout Retransmission (click to expand code) </summary>
```cpp
void ikcp_flush(ikcpcb *kcp)
{
    // ...
// Send snd_buf
    for (p = kcp->snd_buf.next; p != &kcp->snd_buf; p = p->next) {
        IKCPSEG *segment = iqueue_entry(p, IKCPSEG, node);
        int needsend = 0;
        if (segment->xmit == 0) {
Initial transmission
            needsend = 1;
            segment->xmit++;
Set segment->rto.
Calculate the timeout retransmission time based on segment->rto and segment->resendts.
            segment->rto = kcp->rx_rto;
            segment->resendts = current + segment->rto + rtomin;
        }
        else if (_itimediff(current, segment->resendts) >= 0) {
Timeout retransmission
            needsend = 1;
            segment->xmit++;
            kcp->xmit++;
// nodelay controls the calculation of the timeout retransmission time for the next occurrence.
            if (kcp->nodelay == 0) {
                segment->rto += kcp->rx_rto;
            }    else {
                segment->rto += kcp->rx_rto / 2;
            }
            segment->resendts = current + segment->rto;
            lost = 1;
        }
        else if (segment->fastack >= resent) {
// Fast Retransmission
            // ...
        }
        if (needsend) {
// Send data
            // ...
        }
    // ...
}
```
</details>

Once the current time `current` exceeds the `segment->resendts` timeout retransmission time, it indicates that during this period, no ACK packets from the receiver have been received, triggering the timeout retransmission mechanism, `needsend = 1`, to resend the data.

With the addition of acknowledgment of receipt and retransmission on timeout mechanisms, KCP can ensure basic reliable data transmission. However, in order to maintain a more stable data flow rate, KCP has done more. Let's take a look at the optimizations that KCP has implemented.

##KCP strategy to increase flow rate

###Fast retransmission

The sender has transmitted two data packets with sequence numbers `sn` and `sn + 1`. If only the ACK packet for `sn + 1` is received, it could be due to the ACK packet for `sn` not yet reaching the network, or being lost, or the data packet for `sn` being lost. If it is not yet time for a timeout retransmission, the network is not too congested, and the loss is sudden due to some reason, the sender can proactively send the `sn` data packet to help the receiver to faster receive the data and improve the throughput.

KCP also implements a fast retransmission mechanism, which is reflected in `ikcp_flush`:

<details>
<summary> Fast retransmission (click to expand code) </summary>
```cpp
void ikcp_flush(ikcpcb *kcp)
{
    // ...
    resent = (kcp->fastresend > 0)? (IUINT32)kcp->fastresend : 0xffffffff;

// Send snd_buf
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
Fast Retransmission
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
// Send data
            // ...
        }
    // ...
}
```
</details>

To initiate fast retransmission, two conditions must be met:
* `segment->fastack >= resent`, where resent is a configurable parameter `kcp->fastresend`, and setting it to 0 will disable fast retransmission. `segment->fastack` is set in the function `ikcp_parse_fastack`, which is called within `ikcp_input`. This function increments `segment->fastack` for all `sn` less than `maxack`, calculated by `ikcp_input`. Therefore, `segment->fastack` represents the number of times packets larger than `sn` have been received.
`segment->xmit <= kcp->fastlimit || kcp->fastlimit <= 0`, where `segment->xmit` represents the number of transmissions, and `kcp->fastlimit` is the configurable maximum number of fast retransmissions. The transmission count must be less than the maximum fast retransmission count.

Once the above conditions for fast retransmission are met, KCP will execute the fast retransmission. It is important to note that fast retransmission does not reset the timeout retransmission timer; the original timeout period will still apply.

###Shorten the timeout retransmission time.

Timeout retransmission is a great mechanism, but it can be quite time-consuming. According to TCP's strategy, each timeout doubles the retransmission time, leading to rapidly escalating wait times. During this waiting period, it's likely that the receiver's window has been exhausted and cannot accept new data. Moreover, the packet number waiting for retransmission is at the front, and the receiver needs to receive the retransmitted packet before it can return all data to the upper layer. In such a scenario, the overall network flow rate is nearly zero. KCP introduces a configuration that can lessen the growth of waiting times, and it won't simply double. By configuring `kcp->nodelay`, each wait time can increase by only 1 times the RTO or 0.5 times the RTO, effectively slowing the growth of waiting times and helping the network recover its flow rate more quickly.

###Update send window.

The sending window refers to the number of data packets transmitted simultaneously. The larger the window, the more data can be transmitted at the same time, resulting in higher flow rate. However, if the window is too large, it can lead to network congestion, increased packet loss, more data retransmissions, and decreased flow rate. Therefore, the sending window needs to be continuously updated based on the network conditions, gradually approaching the optimal value. Regarding the sending window in KCP, it is expressed in the code as:

<details>
<summary>Send Window (click to expand code)</summary>
```cpp
ikcpcb* ikcp_create(IUINT32 conv, void *user)
{
    // ...
// snd_wnd, rcv_wnd the size of the send and receive buffer
    kcp->snd_wnd = IKCP_WND_SND;    // 32
    kcp->rcv_wnd = IKCP_WND_RCV;    // 128
// Receiver window size of the peer              // 128
    kcp->rmt_wnd = IKCP_WND_RCV
Initialize the sending window cwnd to 0.
    kcp->cwnd = 0;
// The size of the send window in bytes, participates in the calculation of cwnd
    kcp->incr = 0
// Slow start threshold
    kcp->ssthresh = IKCP_THRESH_INIT;
// nocwnd is a configurable parameter, where 1 means not to consider cwnd.
    kcp->nocwnd = 0;
    // ...
}

void ikcp_flush(ikcpcb *kcp)
{
    // ...
Before sending data, calculate the size of the sending window, which is the minimum value between the sending buffer size and the receiving window size of the other party.
    cwnd = _imin_(kcp->snd_wnd, kcp->rmt_wnd);
// By default, we also need to consider kcp->cwnd, which is the continuously updated sending window.
    if (kcp->nocwnd == 0) cwnd = _imin_(kcp->cwnd, cwnd);

Move snd_queue to snd_buf based on the size of cwnd.
    while (_itimediff(kcp->snd_nxt, kcp->snd_una + cwnd) < 0) {
    }
// Send data
    resent = (kcp->fastresend > 0)? (IUINT32)kcp->fastresend : 0xffffffff;
// Trigger timeout retransmission lost = 1
// Trigger fast retransmit change++

Update slow start threshold and congestion window.
    if (change) {
// If fast retransmit is triggered, set ssthresh to half of the number of packets currently being transmitted on the network.
        IUINT32 inflight = kcp->snd_nxt - kcp->snd_una;
        kcp->ssthresh = inflight / 2;
        if (kcp->ssthresh < IKCP_THRESH_MIN)
            kcp->ssthresh = IKCP_THRESH_MIN;

// The sending window is the threshold plus the resent related to fast retransmission.
        kcp->cwnd = kcp->ssthresh + resent;
        kcp->incr = kcp->cwnd * kcp->mss;
    }

    if (lost) {
// If there is a timeout retransmission, slow start is triggered, with the ssthresh threshold set to half of the sending window.
        kcp->ssthresh = cwnd / 2;
        if (kcp->ssthresh < IKCP_THRESH_MIN)
            kcp->ssthresh = IKCP_THRESH_MIN;
// Send the window back to 1 and restart slow start growth.
        kcp->cwnd = 1;
        kcp->incr = kcp->mss;
    }

    if (kcp->cwnd < 1) {
// Because it is initialized to 0, it will be set to 1 here.
        kcp->cwnd = 1;
        kcp->incr = kcp->mss;
    }
}

int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    IUINT32 prev_una = kcp->snd_una;
Processing received data

    while (1) {
        // ...
        data = ikcp_decode16u(data, &wnd)
// rmt_wnd is the receiver window size of the other party.
        kcp->rmt_wnd = wnd
        // ...
Process data
    }

Update the last transmission window.
If kcp->snd_una - prev_una > 0, it means that this input has received an ACK and the send buffer snd_buf has changed.
    if (_itimediff(kcp->snd_una, prev_una) > 0) {
// Re-evaluate the other party's receiving window
        if (kcp->cwnd < kcp->rmt_wnd) {
            IUINT32 mss = kcp->mss;

            if (kcp->cwnd < kcp->ssthresh) {
If less than the slow-start threshold, double the growth.
                kcp->cwnd++;
                kcp->incr += mss;

            }    else {
After exceeding the slow-start threshold, the formula is used to update incr and then calculate cwnd.
                if (kcp->incr < mss) kcp->incr = mss;
                kcp->incr += (mss * mss) / kcp->incr + (mss / 16);
                if ((kcp->cwnd + 1) * mss <= kcp->incr) {
                    kcp->cwnd++;
                }
            }
The updated value also needs to be compared to rmt_wnd again.
            if (kcp->cwnd > kcp->rmt_wnd) {
                kcp->cwnd = kcp->rmt_wnd;
                kcp->incr = kcp->rmt_wnd * mss;
            }
        }
    }
}
```
</details>

Calculating the size of the sending window `kcp->cwnd` involves a slightly longer code snippet, because it needs to be updated when sending and receiving data. `kcp->cwnd` is initialized as 0,
After that, when `ikcp_flush` is called for the first time, it will check if it is less than 1 and change it to 1. Then, the sender will send out the corresponding number of packets based on the size of the sending window and wait for the ACK.
Responding to packets. The ACK packets are processed in `kcp->input`. If ACK packets are detected in `kcp->input` and there is a clearing of the data packets in the sending buffer, it indicates that the data packets have been successfully delivered, `kcp->cwnd++`. In reality, it is highly likely that only one ACK packet is processed in one `kcp->input`. It can be understood that each received ACK packet will trigger `kcp->cwnd++`, this increment achieves a doubling effect. For instance, if the current `kcp->cwnd = 2`, and two data packets are sent, receiving two ACK packets will trigger two increments, resulting in `kcp->cwnd = 4`, a doubling effect.

The `cwnd` can keep growing exponentially until it exceeds the slow start threshold or experiences congestion timeout retransmission, or fast retransmission. After a timeout retransmission occurs, it triggers slow start, where the slow start threshold `ssthresh = kcp->cwnd / 2`, and the sending window `kcp->cwnd = 1`, restarts exponential growth from the beginning. If fast retransmission occurs, KCP first reduces `ssthresh` in advance, that is, reducing the space for exponential growth of `cwnd`, slowing down the growth rate in advance to alleviate congestion.

KCP has also added a configuration `nocwnd`. When `nocwnd = 1`, data is sent without considering the size of the sending window, allowing the maximum possible amount of data packets to be sent, thereby meeting the requirements of high-speed mode.

##Summary

This article briefly analyzes the source code of KCP and discusses the implementation of ARQ on KCP, as well as some strategies for improving flow rates in KCP. There are many details that have not been mentioned; those interested can review the KCP source code for comparison, and I'm sure there will be significant insights to gain.

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please provide [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Point out any omissions. 
