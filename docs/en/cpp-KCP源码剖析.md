---
layout: post
title: KCP Source Code Analysis
categories:
- c++
catalog: true
tags:
- dev
description: This article provides a simple analysis of the source code of KCP and
  discusses the implementation of ARQ on KCP, as well as some strategies to improve
  the flow rate of KCP.
figures: []
---

<meta property="og:title" content="KCP 源码剖析" />

Before reading this article, if you have never heard of KCP, or have no understanding of KCP at all, please take some time to read the documentation of the KCP project: [Link](https://github.com/skywind3000/kcp). The purpose of this article is to delve into the implementation details of KCP in order to understand it better.

## What is KCP

KCP is a fast and reliable protocol that can deliver data with lower latency than TCP, faster data retransmission, and shorter waiting time.

TCP is designed for traffic (how much KB of data can be transmitted per second), focusing on fully utilizing bandwidth. KCP, on the other hand, is designed for flow rate (how long it takes for a single data packet to be sent from one end to the other), trading off 10%-20% of bandwidth for a faster transmission speed of 30%-40% compared to TCP. TCP channel is like a large canal with slow flow rate but high traffic per second, while KCP is like a turbulent small stream with swift water flow.

The above is written in the KCP document, the key words are **bandwidth** and **throughput**. KCP will consume bandwidth, but the benefit is a larger and more balanced transmission rate. For more information, refer to KCP's own documentation.

## KCP Data Structure

The source code of KCP is located in `ikcp.h` and `ikcp.c`. The core of `ikcp.h` is the declaration of data structures. First of all, there is the `SEGMENT` data packet, which is the smallest unit for processing data in the KCP protocol:

<details>
<summary> SEGMENT Structure (Click to expand code) </summary>
```cpp
//=====================================================================
// A **segment** is a data packet.
//=====================================================================
struct IKCPSEG
{
// Linked list node, both send and receive queues use this linked list structure
    struct IQUEUEHEAD node;

// Session ID, the same session ID is identical.
    IUINT32 conv;

// Packet type, such as DATA or ACK
    IUINT32 cmd;

// Due to the limitation of the MTU, large data packets will be split into multiple smaller packets, and this is the numbering of the small packets
    IUINT32 frg

// Each data packet is accompanied by the sender's receive window size
    IUINT32 wnd;

// Send time, if it is an ACK packet, it will be set as the timestamp of the source data packet.
    IUINT32 ts;

// Number that uniquely identifies the data packet.
    IUINT32 sn;

// Represents that all packets with a sequence number less than "una" have been successfully received, consistent with the meaning of TCP: the oldest unacknowledged sequence number SND.
    IUINT32 una;

// Data length
    IUINT32 len;

// Timeout Retransmission Time
    IUINT32 resendts;

    // Next timeout waiting time
    IUINT32 rto;

// Fast retransmission, if the number of subsequent packets received after this packet exceeds a certain threshold, fast retransmission is triggered.
    IUINT32 fastack;

// Number of times sent
    IUINT32 xmit;

    // Data
    char data[1];
};
```
</details>

After reading the comments of `SEGMENT`, it can be roughly understood that the core of KCP is also an ARQ protocol, which ensures the delivery of data through automatic timeout retransmission. Next, let's take a look at the definition of the KCP structure `KCPCB`.

<details>
<summary>KCP Structure (Click to Expand Code)</summary>
```cpp
//---------------------------------------------------------------------
// IKCPCB
//---------------------------------------------------------------------
struct IKCPCB
{
Translate these text into English language:

    // conv: Conversation number
    // mtu, mss: Maximum transmission unit, Maximum segment size
    // state: Conversation state, 0 valid, -1 disconnected
    IUINT32 conv, mtu, mss, state;

// snd_una: Packet number waiting for ACK
// snd_nxt: Next packet number waiting to be sent
// rcv_nxt: Next packet number waiting to be received
    IUINT32 snd_una, snd_nxt, rcv_nxt;

Translate these text into English language:

// ts_recent, ts_lastack: Unused
// ssthresh: Congestion control slow start threshold


    IUINT32 ts_recent, ts_lastack, ssthresh;

    // rx_rto: rto (retransmission timeout), timeout for retransmission
    // rx_rttval, rx_srtt, rx_minrto: intermediate variables for calculating rto
    IINT32 rx_rttval, rx_srtt, rx_rto, rx_minrto;

// snd_wnd, rcv_wnd: Maximum send and receive window sizes
// rmt_wnd: Remote window size, the remaining receive window size of the peer
// cwnd: Size of the available send window
// probe: Flag indicating whether to send control messages
    IUINT32 snd_wnd, rcv_wnd, rmt_wnd, cwnd, probe;

Translate these text into English language:

// current: Current time
// interval: Update interval
// ts_flush: Next update time
// xmit: Number of failed transmissions
    IUINT32 current, interval, ts_flush, xmit;

// Length of the corresponding linked list
    IUINT32 nrcv_buf, nsnd_buf;
    IUINT32 nrcv_que, nsnd_que;

Translate these texts into English language:

    // nodelay: Control the rate at which the RTO (Retransmission Time Out) increases for timeout retransmissions.
    // updated: Whether or not the ikcp_update function has been called.
    IUINT32 nodelay, updated;

// ts_probe, probe_wait: Initiate periodic inquiries when the receiving window of the other party remains 0 for a long time.
    IUINT32 ts_probe, probe_wait;

// deal_link: No response from the opposite end for a long time
// incr: Participate in calculating the size of the send window
    IUINT32 dead_link, incr;

Translate these text into English language:

// queue: The data packet that interacts with the user layer.
// buf: The data packet that is cached by the protocol.
    struct IQUEUEHEAD snd_queue;
    struct IQUEUEHEAD rcv_queue;
    struct IQUEUEHEAD snd_buf;
    struct IQUEUEHEAD rcv_buf;

// Packet information that requires sending an ack
    IUINT32 *acklist;

// Number of packages that need to be ack
    IUINT32 ackcount;

// Memory size of the `acklist`
    IUINT32 ackblock;

// Data passed in by the user layer
    void *user;

// Storage space for a kcp package
    char *buffer;

// Number of fastack triggers to initiate fast retransmission
    int fastresend;

// Maximum number of fast retransmissions
    int fastlimit;

    // nocwnd: window size for sending without considering slow start
    // stream: stream mode
    int nocwnd, stream;

    // debug log
    int logmask;

// Send data interface
    int (*output)(const char *buf, int len, struct IKCPCB *kcp, void *user);

    void (*writelog)(const char *log, struct IKCPCB *kcp, void *user);
};
```
</details>

Annotate each field in the KCP structure one by one. You can have a preliminary feeling that the entire KCP protocol is not too complicated. By carefully analyzing the code, both you and I can read and understand the KCP protocol. :smile:

## KCP's ARQ Implementation

KCP is essentially an ARQ (Auto Repeat-reQuest) protocol that primarily focuses on ensuring reliable transmission. So, let's first pay attention to the basic ARQ component of KCP and how KCP achieves reliable transmission.

ARQ, as the name implies, automatically retransmits the corresponding data packet when we believe that the recipient has failed to receive it. This is achieved through two mechanisms: acknowledgement (ACK) and retransmission upon timeout. In terms of specific code implementation, KCP assigns a unique identifier, `sn`, to each data packet (referred to as `SEGMENT` in the previous section). Once the recipient receives a data packet, it responds with an ACK packet (also a `SEGMENT`) that has the same `sn` as the received data packet, indicating successful reception. The `SEGMENT` also includes a field called `una`, which represents the sequence number of the next expected data packet. In other words, it signifies that all data packets with a sequence number lower than `una` have been successfully received. It is equivalent to a full ACK packet, allowing the sender to update the send buffer and send window more efficiently.

We can understand the most basic ARQ implementation by tracking the sending and receiving code of KCP packets:

### Send

The process of sending is `ikcp_send` -> `ikcp_update` -> `ikcp_output`. The upper layer calls `ikcp_send` to pass the data to KCP, which handles the data transmission in `ikcp_update`.

<details>
<summary>ikcp_send (Click to expand code)</summary>
```cpp
//---------------------------------------------------------------------
// Send data interface, the user calls `ikcp_send` to let KCP send data.
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
// Processing Stream Mode
        // ......
    }

// Calculate sub-packages, if the data length len is greater than mss, divide it into multiple packages to send, and the receiving end will assemble them afterwards
    if (len <= (int)kcp->mss) count = 1;
    else count = (len + kcp->mss - 1) / kcp->mss;

    if (count >= (int)IKCP_WND_RCV) return -2;

    if (count == 0) count = 1;

// Subpackage
    for (i = 0; i < count; i++) {
// Calculate the length of the packet data and allocate the corresponding seg structure.
        int size = len > (int)kcp->mss ? (int)kcp->mss : len;
        seg = ikcp_segment_new(kcp, size);
        assert(seg);
        if (seg == NULL) {
            return -2;
        }

// Set the data information of [to_be_replaced[seg]], [to_be_replaced[frg]] represents the fragmentation number.
        if (buffer && len > 0) {
            memcpy(seg->data, buffer, size);
        }
        seg->len = size;
        seg->frg = (kcp->stream == 0)? (count - i - 1) : 0;

# Add to the end of snd_queue, increase nsnd_qua by one
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

The `ikcp_send` is a data sending interface called by the upper layer of KCP. All the data to be sent by KCP should go through this interface. The `ikcp_send` function does something very simple. It mainly divides the data into multiple packets based on the `kcp->mss` (the maximum data length per packet), sets the packet numbers for each segment, and finally puts them at the end of the sending queue `snd_queue`. In stream mode, multiple calls to `ikcp_send` are treated as a continuous stream of data. It will automatically fill the incomplete segments before allocating new ones. The detailed implementation is not discussed in this article. For those who are interested, I believe that after reading this article, you can understand it better by looking at the corresponding code.

After the completion of the `ikcp_send` invocation, the data will be placed in the `snd_queue` of KCP. Later, KCP needs to find a suitable opportunity to send the pending data. This part of the code is contained in the `ikcp_update` and `ikcp_flush` functions.

<details>
<summary>ikcp_update (Click to expand code)</summary>
```cpp
//---------------------------------------------------------------------
// ikcp_update is an interface that needs to be called regularly by the upper layer to update the state of KCP and send data.
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
// Time of next flush
        kcp->ts_flush += kcp->interval;
        if (_itimediff(kcp->current, kcp->ts_flush) >= 0) {
            kcp->ts_flush = kcp->current + kcp->interval;
        }
        ikcp_flush(kcp);
    }
}
```
</details>

The `ikcp_update` function does a simple task: it checks the time of `ts_flush` and if it meets the criteria, it calls `ikcp_flush`. The main processing logic is inside `ikcp_flush` because it is a bit more complex. Currently, we are only concerned with the parts related to ARQ sending.

<details>
<summary> Send Data (Click to Expand Code) </summary>
```cpp
//---------------------------------------------------------------------
// ikcp_flush
//---------------------------------------------------------------------
void ikcp_flush(ikcpcb *kcp)
{
    IUINT32 current = kcp->current;

// buffer is the data to be passed to ikcp_output, initialized to 3 times the size of the data packet
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

// `seg.wnd` represents the current receive window size.
    seg.wnd = ikcp_wnd_unused(kcp);
    seg.una = kcp->rcv_nxt;
    seg.len = 0;
    seg.sn = 0;
    seg.ts = 0;

    // Send ack
    // Calculate sending window
    //...

    // Move packets from snd_queue to snd_buf
    // The movement is subject to the condition that the sending window size is met. If the sending window is full, the movement will stop. 
    // The data placed in snd_buf can be directly passed to the kcp_output function to be sent to the peer.
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

// seg is a unique sequence number, which is actually an increasing value of kcp->snd_nxt.
        newseg->sn = kcp->snd_nxt++;

// Set `una` here, notifying the other side of the next packet sequence number to be received.
        newseg->una = kcp->rcv_nxt;
        newseg->resendts = current;
        newseg->rto = kcp->rx_rto;
        newseg->fastack = 0;
        newseg->xmit = 0;
    }

// Calculate fast retransmission flag and timeout waiting time
    // ...

// Send snd_buf
    for (p = kcp->snd_buf.next; p != &kcp->snd_buf; p = p->next) {
        IKCPSEG *segment = iqueue_entry(p, IKCPSEG, node);
        int needsend = 0;
        if (segment->xmit == 0) {
// First transmission
// set->xmit indicates the number of transmissions
// resendts represents the waiting time for timeout retransmission
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

// Whenever the data in the buffer exceeds the MTU (Maximum Transmission Unit), it should be sent out first to avoid further fragmentation at the lower level.
            if (size + need > (int)kcp->mtu) {
                ikcp_output(kcp, buffer, size);
                ptr = buffer;
            }

// Copy the control data of `seg` to the buffer, let KCP handle the endianness issue itself
            ptr = ikcp_encode_seg(ptr, segment);

// Copy data again
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

// Calculate ssthresh and update the slow start window
    // ...
}
```
</details>

We are currently only focused on the logic related to sending data in `ikcp_flush` function:

First, KCP will move the data on `snd_queue` to `snd_buf` based on the receiver's window size. The formula for calculating the number of moved data is `num = snd_nxt - (snd_una + cwnd)`, i.e., if the sum of the successfully sent maximum packet sequence number `snd_una` and the sliding window size `cwnd` is greater than the next packet sequence number to be sent `snd_nxt`, then new data packets can be sent again. While moving the `SEG`, the control fields are set.

* Iterate through `snd_buf`, if there is a need to send a data packet, copy the data to `buffer` and simultaneously use `ikcp_encode_seg` to handle the endianness issue of the control field data.

Finally, call `ikcp_output` to send the data on `buffer`

Thus far, KCP has completed the transmission of the data.

### Receive

The receiving process is opposite to the sending process: `ikcp_input` -> `ikcp_update` -> `ikcp_recv`. After the user receives data from the network, they need to call `ikcp_input` to pass it to KCP for parsing. When calling `ikcp_update`, ACK packets will be sent back to the sender. The upper layer can then receive the data parsed by KCP by calling `ikcp_recv`.

<details>
<summary> Receive data (Click to expand code) </summary>
```cpp
//---------------------------------------------------------------------
// input data
//---------------------------------------------------------------------
int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    IUINT32 prev_una = kcp->snd_una;
    IUINT32 maxack = 0, latest_ts = 0;
    int flag = 0;

// Legitimacy check
    if (data == NULL || (int)size < (int)IKCP_OVERHEAD) return -1;

// data may be multiple KCP packets, process in a loop
    while (1) {
        IUINT32 ts, sn, len, una, conv;
        IUINT16 wnd;
        IUINT8 cmd, frg;
        IKCPSEG *seg;

// Not enough data for a KCP packet, exiting.
        if (size < (int)IKCP_OVERHEAD) break;

// First, parse the control fields.
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

// Check data packet type
        if (cmd != IKCP_CMD_PUSH && cmd != IKCP_CMD_ACK &&
            cmd != IKCP_CMD_WASK && cmd != IKCP_CMD_WINS) 
            return -3;

        kcp->rmt_wnd = wnd;

        // Here, `una` represents the `kcp->rcv_nxt` of the sender, based on this data, the already confirmed received packets can be discarded.
        ikcp_parse_una(kcp, una);
// After removing the acknowledged packets, update snd_una to the next sequence number to be sent
        ikcp_shrink_buf(kcp);

        if (cmd == IKCP_CMD_ACK) {
// Ack Package
            // ...
        }
        else if (cmd == IKCP_CMD_PUSH) {
// Data packet
// If the received packet sequence number sn is within the receive window, process it normally; otherwise, discard it directly and wait for retransmission.
            if (_itimediff(sn, kcp->rcv_nxt + kcp->rcv_wnd) < 0) {

// For each received packet, we need to send an acknowledgment packet and keep a record of it.
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
// Query Window Package
            // ...
        }
        else if (cmd == IKCP_CMD_WINS) {
// Reply package for querying window
            // ...
        }
        else {
            return -3;
        }

        data += len;
        size -= len;
    }

// Handling fast retransmission logic
    // ...

// Update the send window
    // ...

    return 0;
}
```
</details>

Loop through each `SEG` packet in `ikcp_input`, first check the legality and type of the packet, because each packet carries `una`, which stores the sequence number of the packet that the sender is waiting to receive. Packets with sequence numbers smaller than `una` have already been successfully received by the other end, so we can delete all packets in `snd_buff` that need to be smaller than `una`, and update `snd_nxt`. This part is handled by `ikcp_parse_una` and `ikcp_shrink_buf`. For each received packet, an ACK packet needs to be replied, which is recorded by `ikcp_ack_push`, and finally `ikcp_parse_data` is called to process the data.

<details>
<summary>Parse Data (Click to Expand Code)</summary>
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

// Find the position where `newseg` should be placed, as the received `seg` may be unordered.
    for (p = kcp->rcv_buf.prev; p != &kcp->rcv_buf; p = prev) {
        IKCPSEG *seg = iqueue_entry(p, IKCPSEG, node);
        prev = p->prev;
        if (seg->sn == sn) {
// Received duplicate
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
// If the seg number is the waiting to be received number, move it to the rcv_queue.
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

The main purpose of `ikcp_parse_data` is to place `newseg` on the appropriate position in `kcp->rcv_buf` and move the data from `rcv_buf` to `rcv_queue`. The appropriate position in `rcv_buf` means that `rcv_buf` is arranged in ascending order according to `sn`. `newseg` needs to find the appropriate position based on its own `sn`. The data on `rcv_buf` needs to be moved to `rcv_queue` under the condition that the packet sequence number on `rcv_buf` is equal to the expected packet sequence number `kcp->rcv_nxt` that KCP is waiting to receive. After moving a data packet, `kcp->rcv_nxt` needs to be updated for the next data packet to be processed.

After `ikcp_input`, when `ikcp_update` is called, ACK packets will be sent, and when `ikcp_recv` is called, valid data will be returned to the upper layer. `ikcp_update` and `ikcp_recv` are independent of each other, with no specific order of calling, depending on the calling timing of the upper layer. Let's first take a look at the part related to ACK sending in `ikcp_update`:

<details>
<summary> Reply ACK (Click to expand code) </summary>
```cpp
// As mentioned earlier, `ikcp_update` ultimately calls `ikcp_flush`.
void ikcp_flush(ikcpcb *kcp, IUINT32 current)
{
    // ...

// Reply with ACK packet
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

The information of ACK packets has been already stored by `ikcp_ack_push`, so here we only need to use `ikcp_ack_get` to obtain the information of each ACK packet and send it to the other party. The upper layer can utilize `ikcp_recv` to retrieve data from KCP.

<details>
<summary>ikcp_recv (click to expand code)</summary>
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

// Check the receive window.
    if (kcp->nrcv_que >= kcp->rcv_wnd)
        recover = 1;

// Traverse the `rcv_queue` and copy the data to the `buffer`
    for (len = 0, p = kcp->rcv_queue.next; p != &kcp->rcv_queue; ) {
        int fragment;
        seg = iqueue_entry(p, IKCPSEG, node);
        p = p->next;

        if (buffer) {
            memcpy(buffer, seg->data, seg->len);
            buffer += seg->len;
        }

        len += seg->len;

        // Determine sub-packages
        fragment = seg->frg;

// Remove data packet
        if (ispeek == 0) {
            iqueue_del(&seg->node);
            ikcp_segment_delete(kcp, seg);
            kcp->nrcv_que--;
        }

// All sub-packages have been copied, exit the loop.
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

The `ikcp_recv` function will only return one complete data packet with each call. The upper layer can loop the function until no data is returned. The logic of the function is simple: it copies data from the `rcv_queue` to the `buffer` passed in from the upper layer. At this point, the receiving side has finished processing the received data packet.

When the recipient processes the data packet, it sends an ACK packet to the sender. Let's now take a look at how the sender handles the received ACK packet:

<details>
<summary> Processing ACK packets (click to expand the code) </summary>
```cpp
int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    // ...
    IUINT32 maxack = 0, latest_ts = 0;
    // ...
    while (1) {
        // ...
// ts is the current of the peer's kcp
        data = ikcp_decode32u(data, &ts);
        data = ikcp_decode32u(data, &sn);

        if (cmd == IKCP_CMD_ACK) {
// Update rot
            if (_itimediff(kcp->current, ts) >= 0) {
                ikcp_update_ack(kcp, _itimediff(kcp->current, ts));
            }
// Update snd_buf
            ikcp_parse_ack(kcp, sn);
            ikcp_shrink_buf(kcp);

// maxack = the largest sn among all ACK packets in this input
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

// If an ACK packet is received, record it for fast retransmission
    if (flag != 0) {
        ikcp_parse_fastack(kcp, maxack, latest_ts);
    }
}
```
</details>

You can see that after receiving the ACK packet, you will also need to use `ikcp_parse_ack` and `ikcp_shrink_buf` to update `snd_buf`. In addition, you need to call `ikcp_update_ack` to calculate and update the retransmission timeout (rto). `ikcp_input` calculates the maximum sequence number in the received ACK packet to record for fast retransmission. That's how it goes - when the sender receives the ACK packet, it removes the transmitted data from `snd_buf`, ensuring that the packet is reliably delivered to the receiver, and completes a full ARQ acknowledgment process.

### Timeout retransmission

The previous section introduced the acknowledgment-receiving mechanism implemented in KCP's ARQ. However, ARQ also requires a timeout retransmission to ensure reliability. Now let's take a look at how KCP handles timeout retransmission.

Let's go back to the `ikcp_flush` function:

<details>
<summary> Retransmission Timeout (Click to expand code) </summary>
```cpp
void ikcp_flush(ikcpcb *kcp)
{
    // ...
// Send snd_buf
    for (p = kcp->snd_buf.next; p != &kcp->snd_buf; p = p->next) {
        IKCPSEG *segment = iqueue_entry(p, IKCPSEG, node);
        int needsend = 0;
        if (segment->xmit == 0) {
            // First send
            needsend = 1;
            segment->xmit++;
// Set segment->rto
// Calculate segment->resendts timeout retransmission time based on segment->rto
            segment->rto = kcp->rx_rto;
            segment->resendts = current + segment->rto + rtomin;
        }
        else if (_itimediff(current, segment->resendts) >= 0) {
// Retransmission on timeout
            needsend = 1;
            segment->xmit++;
            kcp->xmit++;
// nodelay controls the calculation of the next timeout for retransmission.
            if (kcp->nodelay == 0) {
                segment->rto += kcp->rx_rto;
            }    else {
                segment->rto += kcp->rx_rto / 2;
            }
            segment->resendts = current + segment->rto;
            lost = 1;
        }
        else if (segment->fastack >= resent) {
            // Fast retransmission
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

Once the current time `current` is greater than the timeout resend time `segment->resendts`, it means that no ACK packet has been received from the receiver during this period. This triggers the timeout resend mechanism, setting `needsend = 1` to resend the data.

With the confirmation reception and timeout retransmission mechanism, KCP can guarantee basic reliable data transmission. However, in order to maintain a more stable data flow rate, KCP has also done more. Now let's take a look at the optimizations that KCP has made.

## Strategies to Increase Flow Rate of KCP

### Fast Retransmission

The sender has sent two packets with serial numbers `sn` and `sn + 1`. If only the ACK packet for `sn + 1` is received, it is possible that the ACK packet for `sn` hasn't arrived yet in the network, or the ACK packet has been lost, or the `sn` packet has been lost. If it is not yet time for timeout retransmission and the network is not heavily congested, but rather due to some unexpected packet loss, the sender can proactively send the `sn` packet in advance to help the receiver receive the data faster and improve the flow rate.

KCP also implements a fast retransmission mechanism, which is located inside `ikcp_flush`.

<details>
<summary> Fast Retransmission (click to expand code) </summary>
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
// Fast retransmission
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
// Sending data
            // ...
        }
    // ...
}
```
</details>

To initiate fast retransmission, there are two conditions:

* `segment->fastack >= resent`: The variable `resent` is a configurable parameter `kcp->fastresend`. Setting it to 0 will disable fast retransmission. `segment->fastack` is set in the function `ikcp_parse_fastack`, which is called within `ikcp_input`. It increments `segment->fastack` by one for all segments with `sn` smaller than `maxack` calculated by `ikcp_input`. Therefore, `segment->fastack` represents the number of received packets with a sequence number greater than `sn`.
* `segment->xmit <= kcp->fastlimit || kcp->fastlimit <= 0`: `segment->xmit` represents the number of times the segment has been sent, while `kcp->fastlimit` is the maximum configurable number of fast retransmissions. The number of transmissions (`segment->xmit`) must be smaller than the maximum fast retransmission limit (`kcp->fastlimit`) or the limit must be set to 0.

Once the above conditions for fast retransmission are met, KCP will perform fast retransmission. It is important to note that fast retransmission does not reset the timeout for retransmission, the original timeout will still take effect.

### Shorten Timeout Retransmission Time

Timeout retransmission is a great mechanism, but it takes too much time. According to TCP's strategy, the timeout interval doubles each time, and the waiting time expands quickly. During the waiting time, it is highly likely that the receiving end's receive window is exhausted, making it unable to receive new data. The sequence number of the packet waiting for retransmission is at the very front, and the receiver needs to receive the retransmitted packet in order to return all the data to the upper layer. In this situation, the overall network throughput is almost zero. KCP adds a configuration option that can slow down the growth of waiting time, and it is not a doubling mechanism. By configuring `kcp->nodelay`, the waiting time only increases by a factor of 1 or 0.5 times the RTO (Retransmission Timeout), effectively mitigating the growth of waiting time and helping the network to recover its throughput as quickly as possible.

### Update Sending Window

The sending window indicates the number of data packets transmitted simultaneously. The larger the window, the more data can be transmitted simultaneously and the higher the flow rate. However, if the window is too large, it may cause network congestion, increase packet loss rate, and lead to more data retransmission, resulting in a decrease in flow rate. Therefore, the sending window needs to be continuously updated based on the network conditions, gradually approaching the optimal value. The code related to the sending window in KCP is as follows:


<details>
<summary>Send Window (click to expand code)</summary>
```cpp
ikcpcb* ikcp_create(IUINT32 conv, void *user)
{
    // ...
// snd_wnd, rcv_wnd The size of the send and receive buffer
    kcp->snd_wnd = IKCP_WND_SND;    // 32
    kcp->rcv_wnd = IKCP_WND_RCV;    // 128
// Receiver window size on the other side // 128
    kcp->rmt_wnd = IKCP_WND_RCV
// Initialize sending window cwnd to 0
    kcp->cwnd = 0;
    // The size of the sent window in bytes, participating in the calculation of cwnd.
    kcp->incr = 0
    // 慢启动阈值，slow start threshold
    kcp->ssthresh = IKCP_THRESH_INIT;
// nocwnd is a configurable parameter, 1 means cwnd is not considered.
    kcp->nocwnd = 0;
    // ...
}

void ikcp_flush(ikcpcb *kcp)
{
    // ...
    // Before sending data, first calculate the size of the sending window, which is the minimum value between the size of the sending buffer and the size of the receiving window of the other party.
    cwnd = _imin_(kcp->snd_wnd, kcp->rmt_wnd);
// We also need to consider `kcp->cwnd`, which is the continuously updated sending window.
    if (kcp->nocwnd == 0) cwnd = _imin_(kcp->cwnd, cwnd);

// Move snd_queue to snd_buf based on the size of cwnd
    while (_itimediff(kcp->snd_nxt, kcp->snd_una + cwnd) < 0) {
    }
// Send data
    resent = (kcp->fastresend > 0)? (IUINT32)kcp->fastresend : 0xffffffff;
// Trigger timeout retransmission lost = 1
// Trigger fast retransmission change++

    // Update the slow start threshold and the congestion window
    if (change) {
        // If fast retransmission is triggered, ssthresh is set to half the number of packets currently being transmitted on the network.
        IUINT32 inflight = kcp->snd_nxt - kcp->snd_una;
        kcp->ssthresh = inflight / 2;
        if (kcp->ssthresh < IKCP_THRESH_MIN)
            kcp->ssthresh = IKCP_THRESH_MIN;

// The sending window is the threshold plus the resent related to fast retransmission.
        kcp->cwnd = kcp->ssthresh + resent;
        kcp->incr = kcp->cwnd * kcp->mss;
    }

    if (lost) {
// If there is a timeout retransmission, trigger slow start. The ssthresh threshold is half of the send window.
        kcp->ssthresh = cwnd / 2;
        if (kcp->ssthresh < IKCP_THRESH_MIN)
            kcp->ssthresh = IKCP_THRESH_MIN;
// Send the window back to 1 and restart slow start growth
        kcp->cwnd = 1;
        kcp->incr = kcp->mss;
    }

    if (kcp->cwnd < 1) {
// Because it is initialized to 0, it will be set to 1 again here.
        kcp->cwnd = 1;
        kcp->incr = kcp->mss;
    }
}

int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    IUINT32 prev_una = kcp->snd_una;
// Processing received data

    while (1) {
        // ...
        data = ikcp_decode16u(data, &wnd)
`// rmt_wnd` is the receiving window size of the other party.
        kcp->rmt_wnd = wnd
        // ...
// Process data
    }

// Finally update the send window
// kcp->snd_una - prev_una > 0 means that ACK has been received for this input and the send buffer snd_buf has changed.
    if (_itimediff(kcp->snd_una, prev_una) > 0) {
// Then determine the receiving window of the other party.
        if (kcp->cwnd < kcp->rmt_wnd) {
            IUINT32 mss = kcp->mss;

            if (kcp->cwnd < kcp->ssthresh) {
// Less than slow-start threshold, double the growth
                kcp->cwnd++;
                kcp->incr += mss;

            }    else {
// After exceeding the slow start threshold, update the increment using the formula and then calculate the congestion window (cwnd).
                if (kcp->incr < mss) kcp->incr = mss;
                kcp->incr += (mss * mss) / kcp->incr + (mss / 16);
                if ((kcp->cwnd + 1) * mss <= kcp->incr) {
                    kcp->cwnd++;
                }
            }
// The updated value also needs to be compared with rmt_wnd.
            if (kcp->cwnd > kcp->rmt_wnd) {
                kcp->cwnd = kcp->rmt_wnd;
                kcp->incr = kcp->rmt_wnd * mss;
            }
        }
    }
}
```
</details>

The code snippet involving the calculation of the sending window size `kcp->cwnd` will be a bit longer, as it needs to be updated both when sending and receiving data. `kcp->cwnd` is initialized as 0 and will be modified to 1 when the `ikcp_flush` function is called for the first time and it is found to be less than 1. Afterwards, the sender will send a corresponding number of data packets based on the sending window size and wait for ACK reply packets. The ACK packets are processed in the `kcp->input` function. If ACK packets are detected and there is a clearing of sent data packets in the sending buffer, it means that some packets have been successfully delivered, and `kcp->cwnd` will be incremented. In fact, it is likely that only one ACK packet is processed in each `kcp->input` call, so it can be understood that each received ACK packet triggers an increment of `kcp->cwnd`, which has a doubling effect. For example, if the current `kcp->cwnd` is 2 and two data packets are sent and two ACK packets are received, then two increments will be triggered, resulting in `kcp->cwnd` becoming 4 through doubling.

`cwnd` can continue to grow exponentially until it exceeds the slow start threshold or there is congestion timeout retransmission or fast retransmission. After a congestion timeout retransmission occurs, slow start is triggered, and the slow start threshold `ssthresh = kcp->cwnd / 2`, and the send window `kcp->cwnd = 1` return to initial exponential growth. If fast retransmission occurs, KCP first reduces `ssthresh`, which reduces the space for `cwnd` exponential growth and slows down the growth rate, thereby preemptively mitigating congestion.

KCP has added a new configuration parameter called `nocwnd`. When `nocwnd = 1`, the sender no longer considers the size of the sending window when sending data. It simply sends the maximum number of data packets that can be sent, meeting the requirements of high-speed mode.

## Conclusion

This article provides a simple analysis of the source code for KCP and discusses the implementation of ARQ on KCP, as well as some strategies for improving the flow rate of KCP. There are many details that have not been mentioned, so those who are interested can refer to the source code of KCP and compare it themselves. It is believed that there will be many valuable insights to be gained.

--8<-- "footer_en.md"


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
