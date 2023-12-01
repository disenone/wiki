---
layout: post
title: KCP Source Code Analysis
categories:
- c++
catalog: true
tags:
- dev
description: This article provides a brief analysis of the source code of KCP and
  discusses the implementation of ARQ on KCP, as well as some strategies to improve
  the flow rate of KCP.
figures: []
---


Before reading this article, if you haven't heard of KCP or have no knowledge of KCP at all, please take a moment to read the documentation of the KCP project: [link](https://github.com/skywind3000/kcp). The purpose of this article is to delve into the implementation details of KCP in order to understand KCP better.

## What is KCP

KCP is a fast and reliable protocol that can deliver data with lower latency than TCP, faster data retransmission, and shorter waiting time.

TCP is designed for traffic (how much data in KB can be transmitted per second), focusing on fully utilizing bandwidth. KCP, on the other hand, is designed for flow rate (how much time it takes for a single data packet to be sent from one end to the other), sacrificing 10%-20% of bandwidth to achieve 30%-40% faster transmission speed than TCP. The TCP channel is like a slow-flowing but high-volume canal, while KCP is like a turbulent and fast-flowing stream.

The above is written in the KCP documentation, with the key words **bandwidth** and **throughput**. KCP will consume bandwidth, but the benefit is a larger and more balanced transmission rate. For more details, please refer to the KCP's own documentation.

## KCP Data Structures

The source code of KCP is in `ikcp.h` and `ikcp.c`. The core of `ikcp.h` is the declaration of data structures, starting with the `SEGMENT` data packet, which is the smallest unit for data processing in the KCP protocol:

<details>
<summary> SEGMENT structure (Click to expand code) </summary>
```cpp
//=====================================================================
// A SEGMENT is just a data packet.
//=====================================================================
struct IKCPSEG
{
`// Linked list node, both the send queue and the receive queue are linked lists here`
    struct IQUEUEHEAD node;

// Session number, the same session number is the same.
    IUINT32 conv;

// Packet type, such as DATA or ACK
    IUINT32 cmd;

     // Due to the limitation of MTU, large data packets will be split into multiple smaller packets, and this is the number of the small packet.
    IUINT32 frg

// Each packet will be accompanied by the sender's receive window size.
    IUINT32 wnd;

// The sending time, if it is an ACK packet, will be set as the timestamp of the source data packet.
    IUINT32 ts;

// Unique identifier for the data packet
    IUINT32 sn;

// Represents that all packets less than `una` have been successfully received, consistent with the TCP meaning: oldest unacknowledged sequence number SND
    IUINT32 una;

// Data length
    IUINT32 len;

// Timeout retransmission time
    IUINT32 resendts;

    // Next timeout wait time
    IUINT32 rto;

// Fast retransmission, if the number of data packets received after this packet exceeds a certain threshold, fast retransmission is triggered.
    IUINT32 fastack;

// Number of Sendings
    IUINT32 xmit;

// Data
    char data[1];
};
```
</details>

After reading the comments of `SEGMENT`, you can roughly see that the core of KCP is also an ARQ protocol which ensures data delivery through automatic timeout retransmission. Then let's take a look at the definition of the KCP structure `KCPCB`.

<details>
<summary> KCP Structure (Click to expand code) </summary>
```cpp
//---------------------------------------------------------------------
// IKCPCB
//---------------------------------------------------------------------
struct IKCPCB
{
```markdown
// conv: Conversation number
// mtu, mss: Maximum transmission unit, Maximum Segment size
// state: Conversation status, 0 valid, -1 disconnected
```
    IUINT32 conv, mtu, mss, state;

```
// snd_una: Packet number waiting for ACK
// snd_nxt: Next data packet to be sent
// rcv_nxt: Next data packet to be received
```
    IUINT32 snd_una, snd_nxt, rcv_nxt;

```plaintext
// ts_recent, ts_lastack: not used
// ssthresh: congestion control slow start threshold
```
    IUINT32 ts_recent, ts_lastack, ssthresh;

// rx_rto: retransmission timeout, the time for retransmitting when a timeout occurs
// rx_rttval, rx_srtt, rx_minrto: intermediate variables for calculating rto
    IINT32 rx_rttval, rx_srtt, rx_rto, rx_minrto;

// snd_wnd, rcv_wnd: Maximum send and receive window size
    // rmt_wnd: remote window, the remaining receive window size on the other side
    // cwnd: Congestion window size
    // probe: Flag indicating whether to send control packets
    IUINT32 snd_wnd, rcv_wnd, rmt_wnd, cwnd, probe;

```
// current: Current time
// interval: Update interval
// ts_flush: Next update time
// xmit: Number of failed transmissions
```
    IUINT32 current, interval, ts_flush, xmit;

// Length of the corresponding linked list
    IUINT32 nrcv_buf, nsnd_buf;
    IUINT32 nrcv_que, nsnd_que;

```markdown
// nodelay: Controls the rate at which the retransmission timeout (RTO) increases in the event of timeouts.
// updated: Indicates whether the ikcp_update function has been called.
```
    IUINT32 nodelay, updated;

// ts_probe, probe_wait: Initiates regular inquiries when the peer's receive window remains 0 for a prolonged period.
    IUINT32 ts_probe, probe_wait;

```
// deal_link: No response from the other side for a long time
// incr: Participate in calculating the size of the send window
```
    IUINT32 dead_link, incr;

     // queue: Data packets that interact with the user layer
     // buf: Data packets cached by the protocol
    struct IQUEUEHEAD snd_queue;
    struct IQUEUEHEAD rcv_queue;
    struct IQUEUEHEAD snd_buf;
    struct IQUEUEHEAD rcv_buf;

// Packet information that needs to be sent the ACK
    IUINT32 *acklist;

// Number of packages requiring acknowledgement
    IUINT32 ackcount;

// Size of the `acklist` memory
    IUINT32 ackblock;

// Data passed in from the user layer
    void *user;

// Storage space for one kcp packet
    char *buffer;

// The number of fastack triggers for fast retransmission.
    int fastresend;

// Maximum number of fast retransmissions
    int fastlimit;

```markdown
// nocwnd: Don't consider the size of the congestion window without slow start
// stream: Stream mode
```
    int nocwnd, stream;

    // debug log
    int logmask;

// Send data interface
    int (*output)(const char *buf, int len, struct IKCPCB *kcp, void *user);

    void (*writelog)(const char *log, struct IKCPCB *kcp, void *user);
};
```
</details>

Annotate each field in the KCP structure one by one. It can be initially felt that the entire KCP protocol is not too complicated. By carefully analyzing the code, both you and I can read and understand the KCP protocol :smile:

## KCP's ARQ Implementation

KCP is essentially an ARQ (Auto Repeat-reQuest) protocol, the most basic requirement is to ensure reliable transmission. So let's first focus on the basic ARQ part of KCP and how it achieves reliable transmission.

ARQ, as the name suggests, automatically retransmits corresponding packets when we believe that the receiving endpoint has failed to receive them. It achieves reliable transmission through two mechanisms: acknowledgment of reception and timeout retransmission. In terms of specific code implementation, KCP assigns a unique identifier (`sn`) to each packet (referred to as a `SEGMENT` in the previous section). Once the receiving end receives a packet, it responds with an ACK packet (also a `SEGMENT`), in which the `sn` is the same as that of the received packet, indicating that the packet has been successfully received. The `SEGMENT` also has a `una` field, which represents the number of the next expected packet to be received. In other words, it means that all packets with numbers before this have been received, equivalent to a full ACK packet. The sender can update the send buffer and send window more quickly based on this information.

We can understand the basic implementation of ARQ by tracking the sending and receiving codes of KCP packets:

### Send

The process of sending is `ikcp_send` -> `ikcp_update` -> `ikcp_output`. The upper layer calls `ikcp_send` to pass data to KCP, and KCP handles the data transmission in `ikcp_update`.

<details>
<summary>ikcp_send (Click to expand code)</summary>
```cpp
//---------------------------------------------------------------------
// Send data interface, users call `ikcp_send` to enable KCP to send data.
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
// Handle Stream Mode
        // ......
    }

// Calculate sub-packages, if the data length len is greater than mss, it needs to be divided into multiple packages for transmission, and then reassembled by the receiving end
    if (len <= (int)kcp->mss) count = 1;
    else count = (len + kcp->mss - 1) / kcp->mss;

    if (count >= (int)IKCP_WND_RCV) return -2;

    if (count == 0) count = 1;

// Subpackage
    for (i = 0; i < count; i++) {
```cpp
// Calculate the length of the package data and allocate the corresponding seg structure
```
        int size = len > (int)kcp->mss ? (int)kcp->mss : len;
        seg = ikcp_segment_new(kcp, size);
        assert(seg);
        if (seg == NULL) {
            return -2;
        }

// Set the data information of seg, frg represents the packet number.
        if (buffer && len > 0) {
            memcpy(seg->data, buffer, size);
        }
        seg->len = size;
        seg->frg = (kcp->stream == 0)? (count - i - 1) : 0;

        // Add to the end of snd_queue and increment nsnd_qua by one
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

`ikcp_send` is the data sending interface called by the upper layer of KCP. All data to be sent by KCP should be passed through this interface. `ikcp_send` does a simple task, which is to divide the data into multiple packets according to `kcp->mss` (the maximum data length of a packet), and set packet numbers, and finally put them at the end of the send queue `snd_queue`. In streaming mode, multiple calls to `ikcp_send` are treated as a stream, and the unfilled `SEGMENT` will be automatically filled before allocating new ones. The detailed implementation is not discussed in this article. If you are interested, I believe that after reading this article, you will be able to understand it by matching it with the code.

After the completion of the `ikcp_send` function, the data is placed in the `snd_queue` of KCP. Later, KCP needs to find an opportunity to send the pending data. This part of the code is located in the `ikcp_update` and `ikcp_flush` functions.

<details>
<summary>ikcp_update (click to expand the code)</summary>
```cpp
//---------------------------------------------------------------------
// `ikcp_update` is an interface that needs to be called regularly by the upper layer to update the state of KCP and send data.
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
        // Time for the next flush
        kcp->ts_flush += kcp->interval;
        if (_itimediff(kcp->current, kcp->ts_flush) >= 0) {
            kcp->ts_flush = kcp->current + kcp->interval;
        }
        ikcp_flush(kcp);
    }
}
```
</details>

### Translation:

What `ikcp_update` does is quite simple. It checks the time of `ts_flush` and if it meets the conditions, it calls `ikcp_flush`. The main processing logic is all inside `ikcp_flush`. Since the content of `ikcp_flush` is a bit complex, we currently only focus on the parts related to ARQ sending.

<details>
<summary> Send Data (Click to expand code) </summary>
```cpp
//---------------------------------------------------------------------
// ikcp_flush
//---------------------------------------------------------------------
void ikcp_flush(ikcpcb *kcp)
{
    IUINT32 current = kcp->current;

```plaintext
// buffer is the data to be passed to ikcp_output, initialized as 3 times the size of the data packet
```
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

```markdown
// seg.wnd represents the current size of the receive window
```
    seg.wnd = ikcp_wnd_unused(kcp);
    seg.una = kcp->rcv_nxt;
    seg.len = 0;
    seg.sn = 0;
    seg.ts = 0;

    // Send ack
    // Calculate send window
    //...

```markdown
// Move the data packet from snd_queue to snd_buf
// Moving is subject to the size of the sending window. If the sending window is full, the movement stops
// The data placed in snd_buf is the data that can be directly called by ikcp_output to send to the other end
```
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

// seg Unique ID, which is actually an incrementing value of kcp->snd_nxt
        newseg->sn = kcp->snd_nxt++;

// Set `una` here, notify the other end the next packet sequence number to be received.
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
```markdown
// First send
// set->xmit indicates the number of times sent
// resendts represents the waiting time for timeout retransmission
```
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

// Whenever the data in the buffer exceeds the MTU, it is sent out first to avoid further fragmentation at the lower level.
            if (size + need > (int)kcp->mtu) {
                ikcp_output(kcp, buffer, size);
                ptr = buffer;
            }

// Copy the control data of seg to buffer, let KCP handle the endian issue itself.
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

// Calculate ssthresh, update slow start window
    // ...
}
```
</details>

We are currently only focusing on the logic related to sending data in `ikcp_flush` function:

First of all, KCP will move the data on the `snd_queue` to the `snd_buf` based on the receiving window size of the peer. The formula for calculating the number of data to move is `num = snd_nxt - (snd_una + cwnd)`. In other words, if the maximum packet sequence number that has been successfully sent `snd_una` plus the sliding window size `cwnd` is greater than the next packet sequence number to be sent `snd_nxt`, then new data packets can be sent again. While moving the `SEG`, the control fields are set.

Traverse `snd_buf`, if data packets need to be sent, copy the data to `buffer` and simultaneously handle the endianness of the control field data with `ikcp_encode_seg`.

Finally, call `ikcp_output` to send the data on the `buffer`.

So far, KCP has completed the data transmission.

### Receive

The receiving process is opposite to the sending process: `ikcp_input` -> `ikcp_update` -> `ikcp_recv`. After the user receives data from the network, they need to call `ikcp_input` to pass it to KCP for parsing. When calling `ikcp_update`, ACK packets are sent back to the sender. The upper layer receives the parsed data from KCP by calling `ikcp_recv`.

<details>
<summary> Receive Data (Click to Expand Code) </summary>
```cpp
//---------------------------------------------------------------------
// input data
//---------------------------------------------------------------------
int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    IUINT32 prev_una = kcp->snd_una;
    IUINT32 maxack = 0, latest_ts = 0;
    int flag = 0;

// Validity check
    if (data == NULL || (int)size < (int)IKCP_OVERHEAD) return -1;

// [to_be_replace[Data]] may be multiple KCP packets, process in a loop.
    while (1) {
        IUINT32 ts, sn, len, una, conv;
        IUINT16 wnd;
        IUINT8 cmd, frg;
        IKCPSEG *seg;

// Not enough for a KCP package, exit.
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

// Packet type check
        if (cmd != IKCP_CMD_PUSH && cmd != IKCP_CMD_ACK &&
            cmd != IKCP_CMD_WASK && cmd != IKCP_CMD_WINS) 
            return -3;

        kcp->rmt_wnd = wnd;

```python
// Here, `una` is the value of `kcp->rcv_nxt`, which can be used to remove the already acknowledged received packets.
```
        ikcp_parse_una(kcp, una);
// After removing the received packets that have been confirmed, update snd_una to the next sequence number to be sent.
        ikcp_shrink_buf(kcp);

        if (cmd == IKCP_CMD_ACK) {
// ack package
            // ...
        }
        else if (cmd == IKCP_CMD_PUSH) {
```python
        // Packet
        // If the received packet sequence number `sn` is within the receive window, 
        // process it normally. Otherwise, discard it and wait for retransmission.
```
            if (_itimediff(sn, kcp->rcv_nxt + kcp->rcv_wnd) < 0) {

```
// For each received packet, a corresponding acknowledgment packet is sent back and logged.
```
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
// Query response package for the window
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

// Update send window
    // ...

    return 0;
}
```
</details>

`ikcp_input` cycles through each `SEG` packet, first checking the validity and type of the packet. Since each packet carries the `una`, which is the sequence number of the packets the sender is waiting to receive, all packets with a sequence number smaller than `una` have already been successfully received by the other end. Therefore, the packets in `snd_buff` with a sequence number smaller than `una` can be deleted, and `snd_nxt` should be updated accordingly. This part is handled by `ikcp_parse_una` and `ikcp_shrink_buf`. For every received packet, an ACK packet needs to be sent in response, which is recorded by `ikcp_ack_push`, and finally, `ikcp_parse_data` is called to process the data.

<details>
<summary> Parse Data (Click to Expand Code) </summary>
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

// Find the position where the newseg should be placed, as the received seg might be in disorder.
    for (p = kcp->rcv_buf.prev; p != &kcp->rcv_buf; p = prev) {
        IKCPSEG *seg = iqueue_entry(p, IKCPSEG, node);
        prev = p->prev;
        if (seg->sn == sn) {
// Repeatedly received
            repeat = 1;
            break;
        }
        if (_itimediff(sn, seg->sn) > 0) {
            break;
        }
    }

// Put `newseg` at the correct position in `rcv_buf`.
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
```python
// If the seg number is the expected number to be received, move it to the rcv_queue
```
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

`ikcp_parse_data`'s main task is to place `newseg` in the appropriate position in `kcp->rcv_buf` and move the data from `rcv_buf` to `rcv_queue`. The meaning of the appropriate position in `rcv_buf` is that `rcv_buf` is arranged in ascending order according to `sn`, and `newseg` needs to find the appropriate position based on its own `sn` size. The data on `rcv_buf` needs to be moved to `rcv_queue` under the condition that the data packet sequence number on `rcv_buf` is equal to the KCP's expected sequence number `kcp->rcv_nxt`. After moving a data packet, `kcp->rcv_nxt` needs to be updated before processing the next data packet.

After `ikcp_input`, when the upper layer calls `ikcp_update`, it will send ACK packets, and calling `ikcp_recv` will return valid data to the upper layer. `ikcp_update` and `ikcp_recv` are independent of each other and do not have a specific calling sequence requirement, depending on when the upper layer calls them. Let's first take a look at the part related to ACK sending in `ikcp_update`:

<details>
<summary> Reply ACK (click to expand code) </summary>
```cpp
// As mentioned before, `ikcp_update` ultimately calls `ikcp_flush`.
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

The information of ACK packets has been previously saved by `ikcp_ack_push`, so here we just need to use `ikcp_ack_get` to retrieve the information of each ACK packet and send it to the other party. The upper layer can use `ikcp_recv` to retrieve data from KCP.

<details>
<summary>ikcp_recv (Click to expand code)</summary>
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

```python
# Calculate the length of the data that can be returned
```
    peeksize = ikcp_peeksize(kcp);

    if (peeksize < 0)
        return -2;
    if (peeksize > len)
        return -3;

// Check the receiving window
    if (kcp->nrcv_que >= kcp->rcv_wnd)
        recover = 1;

```python
# Traverse rcv_queue and copy the data to buffer
```
    for (len = 0, p = kcp->rcv_queue.next; p != &kcp->rcv_queue; ) {
        int fragment;
        seg = iqueue_entry(p, IKCPSEG, node);
        p = p->next;

        if (buffer) {
            memcpy(buffer, seg->data, seg->len);
            buffer += seg->len;
        }

        len += seg->len;

// Check sub-packages
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

// The rcv_queue has emptied again, trying to continue moving from rcv_buf to rcv_queue
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

`ikcp_recv` will only return a complete packet in one call. The upper layer can call it repeatedly until no more data is returned. The logic of the function is simple: it copies the data from the `rcv_queue` to the `buffer` provided by the upper layer. At this point, the receiver has finished processing the received packet.

When the receiving party processes the data packet, it sends an ACK packet to the sending party. Let's now take a look at how the sending party handles the received ACK packet:


<details>
<summary> Handle ACK packets (click to expand the code) </summary>
```cpp
int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    // ...
    IUINT32 maxack = 0, latest_ts = 0;
    // ...
    while (1) {
        // ...
// `ts` is the counterpart's kcp->current.
        data = ikcp_decode32u(data, &ts);
        data = ikcp_decode32u(data, &sn);

        if (cmd == IKCP_CMD_ACK) {
// Update `rot`
            if (_itimediff(kcp->current, ts) >= 0) {
                ikcp_update_ack(kcp, _itimediff(kcp->current, ts));
            }
// Update snd_buf
            ikcp_parse_ack(kcp, sn);
            ikcp_shrink_buf(kcp);

// maxack = The maximum sn among all the ACK packets of this input.
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

// If the ACK packet is received, record it for fast retransmission.
    if (flag != 0) {
        ikcp_parse_fastack(kcp, maxack, latest_ts);
    }
}
```
</details>

You can see that after receiving an ACK packet, you also need to use `ikcp_parse_ack` and `ikcp_shrink_buf` to update `snd_buf`. In addition, you need to call `ikcp_update_ack` to calculate and update the RTO (retransmission timeout). `ikcp_input` calculates the maximum sequence number in the received ACK packet to record for fast retransmission. In this way, when the sender receives an ACK packet, it removes the sent data from `snd_buf`, and the data packet is reliably delivered to the receiver, completing a complete ARQ acknowledgment process.

### Timeout retransmission

The previous section introduced the acknowledgment-receiver mechanism implemented in KCP for ARQ. ARQ also requires a timeout retransmission to ensure reliability. Now let's take a look at how KCP handles timeout retransmission.

Let's go back to the `ikcp_flush` function:

<details>
<summary> Timeout retransmission (click to expand code) </summary>
```cpp
void ikcp_flush(ikcpcb *kcp)
{
    // ...
// Send `snd_buf`
    for (p = kcp->snd_buf.next; p != &kcp->snd_buf; p = p->next) {
        IKCPSEG *segment = iqueue_entry(p, IKCPSEG, node);
        int needsend = 0;
        if (segment->xmit == 0) {
// First send
            needsend = 1;
            segment->xmit++;
```python
// Set segment->rto
// Calculate segment->resendts (timeout retransmission time) based on segment->rto
```
            segment->rto = kcp->rx_rto;
            segment->resendts = current + segment->rto + rtomin;
        }
        else if (_itimediff(current, segment->resendts) >= 0) {
// Timeout retransmission
            needsend = 1;
            segment->xmit++;
            kcp->xmit++;
// `nodelay` controls the calculation of the next timeout for retransmission.
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

Once the current time `current` is greater than the timeout resend time `segment->resendts`, it means that no ACK packet has been received from the receiver during this period. This triggers the timeout resend mechanism, setting `needsend = 1`, and retransmitting the data.

With the confirmation of reception and timeout retransmission mechanism, KCP can ensure the basic reliable data transmission. However, in order to maintain a more stable data flow rate, KCP has done more optimizations. Let's take a look at what optimizations KCP has done.

## Strategies to Improve Flow Rate of KCP

### Fast Retransmission

The sender has sent two packets with sequence numbers `sn` and `sn + 1`. If only the ACK packet for `sn + 1` is received, it could be because the ACK packet for `sn` has not yet arrived in the network, or it has been lost, or the packet `sn` itself has been lost. If it is still not time for timeout retransmission and the network is not heavily congested, but the loss occurred due to some unexpected reasons, then the sender can proactively send the packet `sn` in advance. This can help the receiver to receive the data faster and improve the flow rate.

KCP also implements fast retransmission mechanism, which is also included in `ikcp_flush`.

<details>
<summary> Fast Retransmission (Click to Expand Code) </summary>
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
            // Send data
            // ...
        }
    // ...
}
```
</details>

To initiate fast retransmission, there are two conditions:

* `segment->fastack >= resent`: `resent` is a configurable parameter `kcp->fastresend`. When configured as 0, fast retransmission is disabled. `segment->fastack` is set in the function `ikcp_parse_fastack`, which is called in `ikcp_input`. It increments `segment->fastack` by one for all segments with sequence number (`sn`) less than `maxack`, calculated by `ikcp_input`. Therefore, `segment->fastack` represents the number of received packets with a sequence number greater than `sn`.

* `segment->xmit <= kcp->fastlimit || kcp->fastlimit <= 0`: `segment->xmit` is the number of times the segment has been sent. `kcp->fastlimit` is the configurable maximum number of fast retransmissions. The number of sends must be smaller than the maximum fast retransmission count.

Once the above conditions for fast retransmission are met, KCP will execute fast retransmission. Please note that fast retransmission does not reset the timeout retransmission time, and the original timeout time will still take effect.

### Reduce timeout retransmission time

Timeout retransmission is a good mechanism, but it takes too much time. According to TCP's strategy, the timeout retransmission time doubles each time, and the waiting time quickly becomes inflated. During the waiting time, it is likely that the receiving end's receive window has been exhausted and cannot receive new data. Meanwhile, the sequence number of the packet waiting for retransmission is at the front, and the receiving end needs to receive the retransmitted packet in order to return all the data to the upper layer. In this situation, the overall network throughput is almost 0.

KCP adds a configuration to reduce the growth of waiting time, and it won't double the time. By configuring `kcp->nodelay`, the waiting time will only increase by 1 times the RTO or 0.5 times the RTO, effectively reducing the growth of waiting time and helping the network recover its throughput as soon as possible.

### Update Send Window

The sending window represents the number of data packets that can be transmitted simultaneously. The larger the window, the more data can be transmitted at the same time, resulting in a higher flow rate. However, if the window is too large, it can lead to network congestion, increased packet loss, increased data retransmission, and decreased flow rate. Therefore, the sending window needs to be constantly updated according to the network conditions, gradually approaching the optimal value. The code related to the sending window in KCP is as follows:

<details>
<summary> Send Window (Click to expand code) </summary>
```cpp
ikcpcb* ikcp_create(IUINT32 conv, void *user)
{
    // ...
// snd_wnd, rcv_wnd size of the send and receive buffers
    kcp->snd_wnd = IKCP_WND_SND;    // 32
    kcp->rcv_wnd = IKCP_WND_RCV;    // 128
// Receiver window size on the other side        // 128
    kcp->rmt_wnd = IKCP_WND_RCV
// Initialize sending window cwnd to 0
    kcp->cwnd = 0;
// Number of bytes of the sending window size, involved in the calculation of cwnd
    kcp->incr = 0
// Slow start threshold
    kcp->ssthresh = IKCP_THRESH_INIT;
```c
// nocwnd is a configurable parameter, 1 means cwnd is not considered
```
    kcp->nocwnd = 0;
    // ...
}

void ikcp_flush(ikcpcb *kcp)
{
    // ...
// Calculate the size of the sending window before sending data, which is the minimum value between the size of the sending buffer and the size of the receiving window on the other end.
    cwnd = _imin_(kcp->snd_wnd, kcp->rmt_wnd);
    // Need to consider kcp->cwnd, which is the continuously updated se
    if (kcp->nocwnd == 0) cwnd = _imin_(kcp->cwnd, cwnd);

// Move snd_queue to snd_buf based on the size of cwnd.
    while (_itimediff(kcp->snd_nxt, kcp->snd_una + cwnd) < 0) {
    }
// Send data
    resent = (kcp->fastresend > 0)? (IUINT32)kcp->fastresend : 0xffffffff;
```markdown
// Trigger timeout retransmission lost = 1
// Trigger fast retransmission change++
```

// Update slow start threshold and congestion window
    if (change) {
// If fast retransmission is triggered, ssthresh is set to half of the number of packets being transmitted on the network.
        IUINT32 inflight = kcp->snd_nxt - kcp->snd_una;
        kcp->ssthresh = inflight / 2;
        if (kcp->ssthresh < IKCP_THRESH_MIN)
            kcp->ssthresh = IKCP_THRESH_MIN;

// The sending window is the threshold plus the retransmissions related to fast recovery.
        kcp->cwnd = kcp->ssthresh + resent;
        kcp->incr = kcp->cwnd * kcp->mss;
    }

    if (lost) {
// If there is a timeout retransmission, trigger slow start, and the ssthresh threshold is half of the sending window.
        kcp->ssthresh = cwnd / 2;
        if (kcp->ssthresh < IKCP_THRESH_MIN)
            kcp->ssthresh = IKCP_THRESH_MIN;
// Sending window returns to 1, restarts slow start growth
        kcp->cwnd = 1;
        kcp->incr = kcp->mss;
    }

    if (kcp->cwnd < 1) {
// Because it is initialized as 0, coming here will set it again to 1.
        kcp->cwnd = 1;
        kcp->incr = kcp->mss;
    }
}

int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    IUINT32 prev_una = kcp->snd_una;
// Process the received data

    while (1) {
        // ...
        data = ikcp_decode16u(data, &wnd)
        // rmt_wnd is the receiving window size of the other party
        kcp->rmt_wnd = wnd
        // ...
// Process data
    }

// Last updated send window
// kcp->snd_una - prev_una > 0 indicates that ACK has been received in this input and the send buffer snd_buf has changed
    if (_itimediff(kcp->snd_una, prev_una) > 0) {
// Then check the receiving window of the other party.
        if (kcp->cwnd < kcp->rmt_wnd) {
            IUINT32 mss = kcp->mss;

            if (kcp->cwnd < kcp->ssthresh) {
```javascript
// If smaller than slow start threshold, double the growth
```
                kcp->cwnd++;
                kcp->incr += mss;

            }    else {
// After exceeding the slow start threshold, update "incr" through the formula and then calculate cwnd.
                if (kcp->incr < mss) kcp->incr = mss;
                kcp->incr += (mss * mss) / kcp->incr + (mss / 16);
                if ((kcp->cwnd + 1) * mss <= kcp->incr) {
                    kcp->cwnd++;
                }
            }
// The updated value needs to be compared again with `rmt_wnd`
            if (kcp->cwnd > kcp->rmt_wnd) {
                kcp->cwnd = kcp->rmt_wnd;
                kcp->incr = kcp->rmt_wnd * mss;
            }
        }
    }
}
```
</details>

The code snippet for calculating the size of the sending window `kcp->cwnd` will be slightly longer because it needs to be updated when sending and receiving data. `kcp->cwnd` is initialized to 0, and then modified to 1 in the first call to `ikcp_flush` if it is less than 1. Afterwards, the sender sends a corresponding number of data packets based on the size of the sending window and waits for ACK reply packets. ACK packets are processed in `kcp->input`, and if ACK packets are detected and there is a need to clear the send buffer, it means that some data packets have been successfully delivered, so `kcp->cwnd++`. In fact, it is likely that each call to `kcp->input` only processes one ACK packet, so it can be understood that `kcp->cwnd++` is increased every time an ACK packet is received, achieving a doubling effect. For example, if the current `kcp->cwnd = 2`, two data packets are sent and two ACK packets are received, triggering the increment twice, resulting in `kcp->cwnd = 4`, which is a doubling effect.

`cwnd` can exponentially increase until it exceeds the slow start threshold or a congestion timeout or fast retransmit occurs. After a congestion timeout, slow start is triggered. The slow start threshold `ssthresh = kcp->cwnd / 2` and the sending window `kcp->cwnd = 1` are set, returning to the initial exponential growth. If a fast retransmit occurs, KCP first reduces `ssthresh`, thereby reducing the space for exponential growth of `cwnd` and slowing down the growth rate to proactively mitigate congestion.

KCP also adds a configuration called `nocwnd`. When `nocwnd = 1`, sending data no longer takes into account the size of the sending window. Instead, it directly sends the maximum number of data packets that can be sent, satisfying the requirements of high-speed mode.

## Summary

This article provides a simple analysis of the KCP source code, discusses the implementation of ARQ on KCP, and some strategies to improve the flow rate of KCP. There are many details that have not been mentioned, so if you are interested, you can compare them by yourself with the KCP source code. I believe you will gain a lot from it.

> Original: <https://disenone.github.io/wiki>  
> This post is protected by [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by/4.0/deed.en) agreement, should be reproduced with attribution.


> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.
