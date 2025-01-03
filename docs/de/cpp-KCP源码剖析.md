---
layout: post
title: KCP Source Code Analysis
categories:
- c++
catalog: true
tags:
- dev
description: Dieser Text analysiert kurz den Quellcode von KCP und diskutiert die
  Implementierung von ARQ auf KCP sowie einige Strategien zur Steigerung des Datenflusses
  auf KCP.
figures: []
---

<meta property="og:title" content="KCP 源码剖析" />

Bevor Sie diesen Text lesen, nehmen Sie sich bitte einen Moment Zeit, um das Benutzerhandbuch des KCP-Projekts zu lesen, falls Sie noch nicht von KCP gehört haben oder keine Ahnung davon haben. [Link zum Handbuch](https://github.com/skywind3000/kcp)Der Zweck dieses Textes besteht darin, die Implementierungsdetails von KCP eingehend zu verstehen.

##Was ist KCP?

KCP is ein Protokoll, das schnell und zuverlässig ist, um Daten mit geringerer Latenz als TCP zu übertragen, Daten schneller wieder zu senden und die Wartezeit zu verkürzen.

> TCP ist für Datenströme konzipiert (wie viele KB Daten pro Sekunde übertragen werden), es geht darum, die Bandbreite optimal zu nutzen. hingegen ist KCP für Geschwindigkeit konzipiert (wie lange es dauert, bis ein einzelnes Datenpaket von einer Seite zur anderen gelangt), auf Kosten von 10%-20% Bandbreitenverschwendung erreicht es eine Übertragungsgeschwindigkeit von 30% -40% schneller als TCP. Eine TCP-Verbindung ist wie ein langsamer, aber starker Fluss, während KCP wie ein wilder kleiner Strom ist.

Das steht im KCP-Dokument: Die Schlüsselwörter sind **Bandbreite** und **Flussrate**. KCP würde Bandbreite verbrauchen, was zu einer größeren und gleichmäßigeren Übertragungsgeschwindigkeit führt. Für weitere Informationen siehe das KCP-eigene Dokument.

##KCP data structure

Das KCP Quellcode befindet sich in `ikcp.h` und `ikcp.c`. In `ikcp.h` werden hauptsächlich die Datenstrukturen deklariert. Die erste ist das `SEGMENT` Datenpaket, die kleinste Einheit, die vom KCP-Protokoll zur Datenverarbeitung verwendet wird.

<details>
SEGMENT structure (Klicken Sie hier, um den Code anzuzeigen)
```cpp
//=====================================================================
// Ein Segment ist einfach ein Datenpaket.
//=====================================================================
struct IKCPSEG
{
// Listenknoten, sowohl die Sendeschlange als auch die Empfangsschlange verwenden die Struktur dieser Listenkette.
    struct IQUEUEHEAD node;

// Conversation ID, die gleiche Konversations-ID ist identisch
    IUINT32 conv;

// Packet-Typen wie DATA oder ACK
    IUINT32 cmd;

Aufgrund der MTU-Beschränkung werden große Datenpakete in mehrere kleine Datenpakete aufgeteilt. Dies ist die Nummerierung der kleinen Datenpakete.
    IUINT32 frg

Jedes Datenpaket wird mit der Größe des Empfangsfensters des Senders übermittelt.
    IUINT32 wnd;

// Sendezeit, wird auf die Zeit des Quellpakets gesetzt, wenn es sich um ein ACK-Paket handelt
    IUINT32 ts;

// Die eindeutige Kennung für das Datenpaket.
    IUINT32 sn;

Alle Pakete mit einer Sequenznummer kleiner als una wurden erfolgreich empfangen, was dem TCP-Konzept entspricht: älteste unbestätigte Sequenznummer SND.
    IUINT32 una;

// Datenlänge
    IUINT32 len;

Übertragungszeitüberschreitung
    IUINT32 resendts;

// Nächste Zeitüberschreitungswartezeit
    IUINT32 rto;

Nach Erhalt dieser Datenpakets werden bei einer bestimmten Anzahl von nachfolgenden Datenpaketen die Schnellübertragung ausgelöst.
    IUINT32 fastack;

// Anzahl der Sendungen
    IUINT32 xmit;

// Daten
    char data[1];
};
```
</details>

Nachdem Sie die Kommentare von `SEGMENT` gelesen haben, können Sie grob erkennen, dass der Kern von KCP auch ein ARQ-Protokoll ist, das durch automatische Timeout-Wiederholung die Zustellung von Daten gewährleistet. Schauen Sie sich dann die Definition der KCP-Struktur `KCPCB` an:

<details>
<Zusammenfassung> KCP-Struktur (Klicken Sie, um den Code anzuzeigen) </Zusammenfassung>
```cpp
//---------------------------------------------------------------------
// IKCPCB
//---------------------------------------------------------------------
struct IKCPCB
{
// conv: Konversations-ID
// mtu, mss: Maximum Transmission Unit, Maximale Segmentgröße
// Status: Sitzungsstatus, 0 gültig, -1 getrennt
    IUINT32 conv, mtu, mss, state;

// snd_una: Waiting for the packet number of ACK
// snd_nxt: Next sequence number of the awaiting packet to be sent.
// rcv_nxt: Die nächste zu empfangende Datenpaketnummer.
    IUINT32 snd_una, snd_nxt, rcv_nxt;

// ts_recent, ts_lastack: Not used
// ssthresh: Congestion Control Slow Start Threshold
    IUINT32 ts_recent, ts_lastack, ssthresh;

// rx_rto: rto (retransmission timeout)，Zeitüberschreitung für erneute Übertragung
// rx_rttval, rx_srtt, rx_minrto: Calculate intermediate variables for calculating the RTO.
    IINT32 rx_rttval, rx_srtt, rx_rto, rx_minrto;

// snd_wnd, rcv_wnd: Maximum send and receive window size
// rmt_wnd: Remote-Fenster, Größe des verbleibenden Empfangsfensters auf der Gegenseite.
// cwnd: the size of the window that specifies the amount of data that can be sent
// Prüfen: Flagge zum Senden von Steuerungsnachrichten.
    IUINT32 snd_wnd, rcv_wnd, rmt_wnd, cwnd, probe;

// current: Aktuelle Zeit
// Intervall: Aktualisierungsintervall
// ts_flush: Zeitpunkt des nächsten Updates
// xmit: Anzahl der fehlgeschlagenen Sendevorgänge
    IUINT32 current, interval, ts_flush, xmit;

// Länge der entsprechenden Verkettung
    IUINT32 nrcv_buf, nsnd_buf;
    IUINT32 nrcv_que, nsnd_que;

// nodelay: Controlling the RTO growth rate for timeout retransmissions.
// aktualisiert: Wurde ikcp_update aufgerufen?
    IUINT32 nodelay, updated;

// ts_probe, probe_wait: Initiieren Sie regelmäßig Anfragen, wenn das Empfangsfenster des Remote-Endes für längere Zeit 0 ist.
    IUINT32 ts_probe, probe_wait;

// deal_link: Gegenüber reagiert lange Zeit nicht
// incr: Participate in calculating the sending window size
    IUINT32 dead_link, incr;

// Warteschlange: Datenpakete, die mit der Benutzeroberfläche in Kontakt stehen
// buf: Datenpaket des Protokollcaches
    struct IQUEUEHEAD snd_queue;
    struct IQUEUEHEAD rcv_queue;
    struct IQUEUEHEAD snd_buf;
    struct IQUEUEHEAD rcv_buf;

Bitte senden Sie die Informationen zum Datenpaket, das eine Bestätigung erfordert.
    IUINT32 *acklist;

Bitte übersetzen Sie diesen Text ins Deutsche:

// Anzahl der Pakete, die ack benötigen.
    IUINT32 ackcount;

// Erinnerungsgröße in der Acklist
    IUINT32 ackblock;

Die vom Benutzer übermittelten Daten
    void *user;

Speicherplatz für ein KCP-Paket bereitstellen.
    char *buffer;

// Anzahl der fastack-Auslösungen, die zur schnellen Übertragung führen.
    int fastresend;

Maximale Anzahl der Schnellübertragungen
    int fastlimit;

// nocwnd: Ignoriert die Größe des Sendefensters beim Slow-Start.
// stream: Strommodus
    int nocwnd, stream;

    // debug log
    int logmask;

// Daten senden Schnittstelle
    int (*output)(const char *buf, int len, struct IKCPCB *kcp, void *user);

    void (*writelog)(const char *log, struct IKCPCB *kcp, void *user);
};
```
</details>

Kommentiere nacheinander die Felder in der KCP-Struktur. Man kann bereits feststellen, dass das gesamte KCP-Protokoll nicht allzu kompliziert ist. Wenn man den Code sorgfältig analysiert, können wir beide das KCP-Protokoll lesen und verstehen. 😊

##Die Implementierung von ARQ in KCP.

KCP ist im Wesentlichen ein ARQ (Auto Repeat-reQuest, automatische Wiederholungsanforderung) Protokoll, dessen grundlegendes Ziel es ist, eine zuverlässige Übertragung sicherzustellen. Lassen Sie uns zunächst einmal auf den grundlegenden ARQ-Teil von KCP eingehen und wie es die zuverlässige Übertragung erreicht.

ARQ, wie der Name schon sagt, bedeutet automatische Wiederübertragung des entsprechenden Datenpakets, wenn wir der Meinung sind, dass das Gegenende das Datenpaket nicht erhalten hat. Dies wird durch zwei Mechanismen, nämlich Bestätigungsempfang und Timeout-Wiederholung, erreicht, um eine zuverlässige Übertragung zu gewährleisten. In der spezifischen Codeimplementierung weist KCP jedem Datenpaket (wie im vorherigen Abschnitt erwähntes `SEGMENT`) eine eindeutige `sn`-Kennung zu. Sobald das Gegenende ein Datenpaket empfängt, wird ein ACK-Paket (ebenfalls ein `SEGMENT`) gesendet. Die `sn` des ACK-Pakets entspricht der `sn` des empfangenen Datenpakets und signalisiert den erfolgreichen Empfang dieses Datenpakets. Auf dem `SEGMENT` befindet sich auch ein Feld `una`, das die Nummer des nächsten erwarteten Datenpakets angibt. Mit anderen Worten, alle Datenpakete bis zu dieser Nummer wurden vollständig empfangen - im Grunde genommen ein vollständiges ACK-Paket, was es dem Sender ermöglicht, den Sendepuffer und das Sendefenster schneller zu aktualisieren.

Wir können durch das Verfolgen des Sendens und Empfangens von KCP-Paketen verstehen, wie das grundlegendste ARQ implementiert wird:

###Versenden

Der Ablauf erfolgt über `ikcp_send` -> `ikcp_update` -> `ikcp_output`. Die oberste Ebene ruft `ikcp_send` auf, um die Daten an KCP zu übergeben. In `ikcp_update` verarbeitet KCP den Datenversand.

<details>
ikcp_send(Klicken Sie hier, um den Code anzuzeigen)
```cpp
//---------------------------------------------------------------------
Übersetze den Text ins Deutsche:

// Daten senden Schnittstelle, Benutzer ruft ikcp_send auf, um kcp zum Senden von Daten zu bringen
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
Verarbeitung des Strömungsmodus
        // ......
    }

Berechnen der Paketteilung: Wenn die Datenlänge len größer als mss ist, müssen sie in mehrere Pakete aufgeteilt und gesendet werden, die vom Empfänger wieder zusammengesetzt werden.
    if (len <= (int)kcp->mss) count = 1;
    else count = (len + kcp->mss - 1) / kcp->mss;

    if (count >= (int)IKCP_WND_RCV) return -2;

    if (count == 0) count = 1;

// Subauftrag
    for (i = 0; i < count; i++) {
// Berechnen der Länge der Daten im Paket und Zuweisen der entsprechenden Seg-Struktur.
        int size = len > (int)kcp->mss ? (int)kcp->mss : len;
        seg = ikcp_segment_new(kcp, size);
        assert(seg);
        if (seg == NULL) {
            return -2;
        }

Legen Sie die Dateninformationen für "seg" fest, wobei "frg" die Paketnummer angibt.
        if (buffer && len > 0) {
            memcpy(seg->data, buffer, size);
        }
        seg->len = size;
        seg->frg = (kcp->stream == 0)? (count - i - 1) : 0;

Füge am Ende von snd_queue hinzu und erhöhe nsnd_qua um eins.
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

`ikcp_send` wird von der oberen Schicht von KCP aufgerufen, um Daten zu senden. Alle Daten, die KCP senden soll, sollten über diese Schnittstelle gesendet werden. `ikcp_send` macht etwas sehr einfaches: Es teilt die Daten basierend auf `kcp->mss` (der maximalen Datenlänge eines Pakets) in mehrere Pakete auf, setzt Paketnummern und fügt sie schließlich am Ende der Sendewarteschlange `snd_queue` hinzu. Im Streammodus werden Daten, die mehrmals mit `ikcp_send` gesendet werden, als ein Datenstrom betrachtet. Zunächst werden nicht vollständige `SEGMENTs` automatisch aufgefüllt und dann neue zugewiesen. Die detaillierte Implementierung wird in diesem Text nicht behandelt. Wenn Sie daran interessiert sind, bin ich sicher, dass Sie nach dem Lesen dieses Textes und dem Vergleich mit dem entsprechenden Code ein Verständnis dafür haben werden.

Nachdem der Aufruf von `ikcp_send` abgeschlossen ist, wird die Daten in die `snd_queue` von KCP gelegt. Später muss KCP einen Zeitpunkt finden, um die zu sendenden Daten zu versenden. Dieser Code befindet sich in `ikcp_update` und `ikcp_flush`.

<details>
<Zusammenfassung> ikcp_update（Klicken Sie hier, um den Code anzuzeigen） </Zusammenfassung>
```cpp
//---------------------------------------------------------------------
ikcp_update is an interface that is regularly called by the upper layer to update the state of KCP and send data.
// update state (call it repeatedly, every 10ms-100ms), or you can ask 
// ikcp_check when to call it again (without ikcp_input/_send calling).
// 'current' - current timestamp in millisec. 
//---------------------------------------------------------------------
void ikcp_update(ikcpcb *kcp, IUINT32 current)
{
    IINT32 slap;

    kcp->current = current;

Ikcp_flush will check this, the upper layer must have called ikcp_update before calling ikcp_flush, it is recommended to only use ikcp_update.
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
// Das nächste Zeitfenster für das Leeren (flush)
        kcp->ts_flush += kcp->interval;
        if (_itimediff(kcp->current, kcp->ts_flush) >= 0) {
            kcp->ts_flush = kcp->current + kcp->interval;
        }
        ikcp_flush(kcp);
    }
}
```
</details>

`ikcp_update` does something very simple, it checks the time of `ts_flush`, if conditions are met, it calls `ikcp_flush`. The main processing logic is inside `ikcp_flush`, because the content in `ikcp_flush` is a bit complex. Currently, we are only focusing on the parts related to ARQ transmission.

<details>
<summary> Send data (Click to expand code) </summary>
```cpp
//---------------------------------------------------------------------
// ikcp_flush
//---------------------------------------------------------------------
void ikcp_flush(ikcpcb *kcp)
{
    IUINT32 current = kcp->current;

// Der Puffer enthält die Daten, die an ikcp_output übergeben werden sollen, und wird mit der dreifachen Größe des Datenpakets initialisiert.
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

// seg.wnd is the indication of the current available receiving window size.
    seg.wnd = ikcp_wnd_unused(kcp);
    seg.una = kcp->rcv_nxt;
    seg.len = 0;
    seg.sn = 0;
    seg.ts = 0;

// sende Ack
// Berechnung des Sendefensters
    //...

Verschieben Sie das Datenpaket von der snd_queue in den snd_buf.
Die Bewegung muss der Größe des Sendefensters entsprechen. Wenn das Sendefenster voll ist, wird die Bewegung gestoppt.
Die in snd_buf enthaltenen Daten sind die Daten, die direkt durch Aufruf von ikcp_output an den entfernten Endpunkt gesendet werden können.
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

// seg is a unique identifier, actually an increasing kcp->snd_nxt.
        newseg->sn = kcp->snd_nxt++;

// una wird hier gesetzt, um dem anderen Ende die nächste zu empfangende Paketnummer mitzuteilen.
        newseg->una = kcp->rcv_nxt;
        newseg->resendts = current;
        newseg->rto = kcp->rx_rto;
        newseg->fastack = 0;
        newseg->xmit = 0;
    }

// Berechnung des Fast-Retransmit-Flags und der Zeit für das Timeout.
    // ...

// Send snd_buf
    for (p = kcp->snd_buf.next; p != &kcp->snd_buf; p = p->next) {
        IKCPSEG *segment = iqueue_entry(p, IKCPSEG, node);
        int needsend = 0;
        if (segment->xmit == 0) {
Erste Sendung
// set->xmit indicates the number of transmissions.
// Wartezeit für die erneute Übertragung bei Zeitüberschreitung
            needsend = 1;
            segment->xmit++;
            segment->rto = kcp->rx_rto;
            segment->resendts = current + segment->rto + rtomin;
        }
        else if (_itimediff(current, segment->resendts) >= 0) {
Timeout retransmission.
            // ...
        }
        else if (segment->fastack >= resent) {
// Schnelle Übertragung
            // ...
        }

        if (needsend) {
            int need;
            segment->ts = current;
            segment->wnd = seg.wnd;
            segment->una = kcp->rcv_nxt;

            size = (int)(ptr - buffer);
            need = IKCP_OVERHEAD + segment->len;

Sobald die Daten im Puffer größer als die MTU sind, sollten sie zuerst gesendet werden, um das erneute Paketieren auf der unteren Ebene möglichst zu vermeiden.
            if (size + need > (int)kcp->mtu) {
                ikcp_output(kcp, buffer, size);
                ptr = buffer;
            }

Kopiere die Steuerdaten von "seg" in den Puffer, damit "kcp" sich um die Endianness-Kompatibilität kümmert.
            ptr = ikcp_encode_seg(ptr, segment);

// Daten erneut kopieren
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

Berechnen Sie ssthresh und aktualisieren Sie das Slow-Start-Fenster.
    // ...
}
```
</details>

Wir konzentrieren uns derzeit nur auf die Logik in `ikcp_flush`, die sich mit dem Senden von Daten befasst:

Zunächst wird KCP basierend auf der Empfangsfenstergröße des Empfängers Daten von `snd_queue` in `snd_buf` verschieben. Die Formel zur Berechnung der Anzahl der zu verschiebenden Daten lautet `num = snd_nxt - (snd_una + cwnd)`. Dies bedeutet: Wenn die größte bereits erfolgreich gesendete Paketnummer `snd_una` plus die Größe des Gleitfensters `cwnd` größer ist als die nächste zu sendende Paketnummer `snd_nxt`, können neue Datenpakete weiterhin gesendet werden. Während des Verschiebens der `SEG` werden Steuerfelder gesetzt.

Durchlaufe 'snd_buf', kopiere die Daten in den 'Buffer', wenn ein Datenpaket gesendet werden muss, verarbeite dabei mithilfe von 'ikcp_encode_seg' das Endian-Problem der Steuerdaten.

Finaler Aufruf von `ikcp_output`, um die Daten auf dem `Buffer` zu senden.

An dieser Stelle hat KCP den Datentransfer abgeschlossen.

###Empfangen

Der Empfangsprozess ist das genaue Gegenteil des Sendeprozesses: `ikcp_input` -> `ikcp_update` -> `ikcp_recv`. Wenn der Benutzer Daten aus dem Netzwerk empfängt, muss er `ikcp_input` aufrufen, um sie an KCP zu übergeben. Beim Aufrufen von `ikcp_update` wird ein ACK-Paket an den Sender zurückgesendet. Die oberste Schicht ruft `ikcp_recv` auf, um die von KCP analysierten Daten zu empfangen.

<details>
Empfang von Daten (Klicken, um den Code anzuzeigen)
```cpp
//---------------------------------------------------------------------
// input data
//---------------------------------------------------------------------
int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    IUINT32 prev_una = kcp->snd_una;
    IUINT32 maxack = 0, latest_ts = 0;
    int flag = 0;

Legitimitätsprüfung
    if (data == NULL || (int)size < (int)IKCP_OVERHEAD) return -1;

// data can be multiple KCP packets, process them in a loop.
    while (1) {
        IUINT32 ts, sn, len, una, conv;
        IUINT16 wnd;
        IUINT8 cmd, frg;
        IKCPSEG *seg;

// Nicht genug für ein KCP-Paket, beenden
        if (size < (int)IKCP_OVERHEAD) break;

`Zuerst werden die Steuerfelder analysiert.`
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

// Überprüfung des Pakettyps
        if (cmd != IKCP_CMD_PUSH && cmd != IKCP_CMD_ACK &&
            cmd != IKCP_CMD_WASK && cmd != IKCP_CMD_WINS) 
            return -3;

        kcp->rmt_wnd = wnd;

// Hier ist 'una' das 'kcp->rcv_nxt' des Senders. Basierend auf diesen Daten können die bereits bestätigten Datenpakete entfernt werden.
        ikcp_parse_una(kcp, una);
Nachdem die bestätigten Pakete entfernt wurden, wird die nächste zu sendende Sequenznummer snd_una aktualisiert.
        ikcp_shrink_buf(kcp);

        if (cmd == IKCP_CMD_ACK) {
// Bestätigungspaket
            // ...
        }
        else if (cmd == IKCP_CMD_PUSH) {
// Datenpaket
Wenn die Paketnummer sn innerhalb des Empfangsfensters liegt, wird es normal verarbeitet, ansonsten wird es direkt verworfen und auf eine erneute Übertragung gewartet.
            if (_itimediff(sn, kcp->rcv_nxt + kcp->rcv_wnd) < 0) {

Jedes empfangene Datenpaket muss mit einem Bestätigungspaket beantwortet und protokolliert werden.
                ikcp_ack_push(kcp, sn, ts);

// Die empfangenen Daten werden mit ikcp_parse_data verarbeitet.
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
// Suchmodul
            // ...
        }
        else if (cmd == IKCP_CMD_WINS) {
Bitte übersetzen Sie diesen Text ins Deutsche:

// Antwortpaket des Abfragefensters
            // ...
        }
        else {
            return -3;
        }

        data += len;
        size -= len;
    }

Behandlung der Schnellübertragungslogik
    // ...

Aktualisieren des Sendefensters
    // ...

    return 0;
}
```
</details>

`ikcp_input` function iterates through each `SEG` package, it first checks the validity and type of the data package. Each data package carries `una`, storing the sequence number of the packet that the sender is waiting to receive. Packets with sequence numbers smaller than `una` have already been successfully received by the opposite end, so we can delete all packets in `snd_buff` that are smaller than `una` and update `snd_nxt`. This part is handled by `ikcp_parse_una` and `ikcp_shrink_buf`. Every received data package needs to reply with an ACK package, which is recorded by `ikcp_ack_push`, and finally, `ikcp_parse_data` is called to process the data.

<details>
<Zusammenfassung> Analyse von Daten (Klicken Sie hier, um den Code anzuzeigen) </Zusammenfassung>
```cpp
void ikcp_parse_data(ikcpcb *kcp, IKCPSEG *newseg)
{
    struct IQUEUEHEAD *p, *prev;
    IUINT32 sn = newseg->sn;
    int repeat = 0;

// Überprüfung der Seriennummer
    if (_itimediff(sn, kcp->rcv_nxt + kcp->rcv_wnd) >= 0 ||
        _itimediff(sn, kcp->rcv_nxt) < 0) {
        ikcp_segment_delete(kcp, newseg);
        return;
    }

Ermitteln Sie den richtigen Speicherort für das newseg, da der empfangene seg möglicherweise durcheinander ist.
    for (p = kcp->rcv_buf.prev; p != &kcp->rcv_buf; p = prev) {
        IKCPSEG *seg = iqueue_entry(p, IKCPSEG, node);
        prev = p->prev;
        if (seg->sn == sn) {
// Repeat received
            repeat = 1;
            break;
        }
        if (_itimediff(sn, seg->sn) > 0) {
            break;
        }
    }

Legen Sie newseg an die richtige Stelle in rcv_buf.
    if (repeat == 0) {
        iqueue_init(&newseg->node);
        iqueue_add(&newseg->node, p);
        kcp->nrcv_buf++;
    }    else {
        ikcp_segment_delete(kcp, newseg);
    }

Verschiebe Daten vom rcv_buf in die rcv_queue.
    while (! iqueue_is_empty(&kcp->rcv_buf)) {
        IKCPSEG *seg = iqueue_entry(kcp->rcv_buf.next, IKCPSEG, node);
Wenn die Segmente die gleiche Nummer haben wie die Segmente, die auf den Empfang warten, sollen sie in die Empfangswarteschlange verschoben werden.
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

Die Hauptaufgabe von `ikcp_parse_data` besteht darin, `newseg` an die richtige Stelle in `kcp->rcv_buf` zu platzieren und die Daten von `rcv_buf` in `rcv_queue` zu verschieben. Die "richtige Stelle" in `rcv_buf` bedeutet, dass `rcv_buf` nach aufsteigender Reihenfolge von `sn` sortiert ist und `newseg` den passenden Platz entsprechend seiner eigenen `sn` finden muss. Die Daten auf `rcv_buf` müssen in `rcv_queue` verschoben werden, wenn die Paketnummer auf `rcv_buf` der Paketnummer entspricht, die KCP auf das Empfangen wartet, `kcp->rcv_nxt`. Nach dem Verschieben eines Datenpakets muss `kcp->rcv_nxt` aktualisiert und das nächste Datenpaket verarbeitet werden.

Nach `ikcp_input` wird beim Aufruf von `ikcp_update` ein ACK-Paket gesendet, und beim Aufruf von `ikcp_recv` werden dem oberen Layer gültige Daten zurückgegeben. `ikcp_update` und `ikcp_recv` sind unabhängig voneinander, ohne spezielle Reihenfolge bei den Aufrufen, abhängig vom Timing des oberen Layers. Schauen wir uns zunächst den Teil in `ikcp_update` an, der den ACK-Versand betrifft:

<details>
<summary> Antwort ACK (Klicken Sie, um den Code anzuzeigen) </summary>
```cpp
Vorhin schon erwähnt, ruft ikcp_update letztendlich ikcp_flush auf.
void ikcp_flush(ikcpcb *kcp, IUINT32 current)
{
    // ...

Antworten Sie auf das ACK-Paket.
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

Die ACK-Pakete wurden bereits zuvor von `ikcp_ack_push` gespeichert, daher müssen hier nur die Informationen zu jedem ACK-Paket mit `ikcp_ack_get` abgerufen und an die andere Partei gesendet werden. Die oberste Ebene kann `ikcp_recv` verwenden, um Daten von KCP zu erhalten:

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

Einige Überprüfungen der Gültigkeit.
    if (iqueue_is_empty(&kcp->rcv_queue))
        return -1;
    if (len < 0) len = -len;

// Berechnen Sie die Länge der zurückgegebenen Daten.
    peeksize = ikcp_peeksize(kcp);

    if (peeksize < 0)
        return -2;
    if (peeksize > len)
        return -3;

Überprüfen Sie das Empfangsfenster.
    if (kcp->nrcv_que >= kcp->rcv_wnd)
        recover = 1;

Durchsuchen Sie die rcv_queue und kopieren Sie die Daten in den Puffer.
    for (len = 0, p = kcp->rcv_queue.next; p != &kcp->rcv_queue; ) {
        int fragment;
        seg = iqueue_entry(p, IKCPSEG, node);
        p = p->next;

        if (buffer) {
            memcpy(buffer, seg->data, seg->len);
            buffer += seg->len;
        }

        len += seg->len;

// Überprüfen des Teil-Pakets
        fragment = seg->frg;

Entfernen von Datenpaket.
        if (ispeek == 0) {
            iqueue_del(&seg->node);
            ikcp_segment_delete(kcp, seg);
            kcp->nrcv_que--;
        }

Alle Unterdateien wurden kopiert, verlassen Sie die Schleife.
        if (fragment == 0)
            break;
    }

    assert(len == peeksize);

Der `rcv_queue` ist wieder etwas leer, versuchen Sie weiterhin, Daten vom `rcv_buf` in den `rcv_queue` zu verschieben.
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

`ikcp_recv` returns only one complete data packet in each call. The upper layer can loop the call until no data is returned. The function's logic is quite simple: it copies data from `rcv_queue` to the `buffer` passed in from the upper layer. At this point, the receiver has finished processing the received data packet.

Wenn der Empfänger das Datenpaket verarbeitet, sendet er dem Sender ein ACK-Paket. Schauen wir uns nun an, wie der Sender das ACK-Paket empfängt.

<details>
Bearbeiten von ACK-Paketen (zum Anzeigen des Codes klicken)
```cpp
int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    // ...
    IUINT32 maxack = 0, latest_ts = 0;
    // ...
    while (1) {
        // ...
// ts corresponds to the remote kcp->current
        data = ikcp_decode32u(data, &ts);
        data = ikcp_decode32u(data, &sn);

        if (cmd == IKCP_CMD_ACK) {
Aktualisiere in Rot.
            if (_itimediff(kcp->current, ts) >= 0) {
                ikcp_update_ack(kcp, _itimediff(kcp->current, ts));
            }
Aktualisieren snd_buf
            ikcp_parse_ack(kcp, sn);
            ikcp_shrink_buf(kcp);

maxack = Die größte Sequenznummer in allen ACK-Paketen dieses Eingangs.
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

Wenn ein ACK-Paket empfangen wird, wird es zur schnellen Wiederaussendung aufgezeichnet.
    if (flag != 0) {
        ikcp_parse_fastack(kcp, maxack, latest_ts);
    }
}
```
</details>

Es ist zu erkennen, dass nach dem Empfang des ACK-Pakets auch `ikcp_parse_ack` und `ikcp_shrink_buf` benötigt werden, um `snd_buf` zu aktualisieren. Außerdem muss `ikcp_update_ack` aufgerufen werden, um die rto (Retransmission Timeout, Wiederholungszeitüberschreitung) zu berechnen. `ikcp_input` berechnet die höchste Sequenznummer im empfangenen ACK-Paket, um sie für schnelle erneute Übertragungszwecke zu speichern. Auf diese Weise, wenn der Sender ein ACK-Paket empfängt, wird die gesendete Daten aus `snd_buf` entfernt, und das Datenpaket wird zuverlässig an den Empfänger übertragen, wodurch der vollständige ARQ-Bestätigungsprozess endet.

###Retransmission due to timeout.

Der vorherige Abschnitt beschrieb das Bestätigungsmechanismus im ARQ-Protokoll von KCP. Um Zuverlässigkeit zu gewährleisten, benötigt ARQ auch eine Timeout-Neuübertragung. Jetzt schauen wir, wie KCP diese Timeout-Neuübertragung umsetzt.

Lassen Sie uns zur Funktion "ikcp_flush" zurückkehren:

<details>
Übersetzen Sie diesen Text ins Deutsche:

<summary> Timeout und erneutes Übertragen (Klicken Sie hier, um den Code anzuzeigen) </summary>
```cpp
void ikcp_flush(ikcpcb *kcp)
{
    // ...
// Send snd_buf
    for (p = kcp->snd_buf.next; p != &kcp->snd_buf; p = p->next) {
        IKCPSEG *segment = iqueue_entry(p, IKCPSEG, node);
        int needsend = 0;
        if (segment->xmit == 0) {
Erstmaliges Senden.
            needsend = 1;
            segment->xmit++;
// Setzen von segment->rto
// Berechnen der Zeit für die Retransmission basierend auf segment->rto und segment->resendts.
            segment->rto = kcp->rx_rto;
            segment->resendts = current + segment->rto + rtomin;
        }
        else if (_itimediff(current, segment->resendts) >= 0) {
Timeout retransmission
            needsend = 1;
            segment->xmit++;
            kcp->xmit++;
// Kontrolle, um die Berechnung der Wartezeit für die nächste erneute Übertragung nach einem Timeout zu steuern.
            if (kcp->nodelay == 0) {
                segment->rto += kcp->rx_rto;
            }    else {
                segment->rto += kcp->rx_rto / 2;
            }
            segment->resendts = current + segment->rto;
            lost = 1;
        }
        else if (segment->fastack >= resent) {
// Schnelle Wiederübertragung
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

Sobald die aktuelle Zeit `current` größer als `segment->resendts` Timeout-Retransmissionszeit ist, bedeutet dies, dass während dieser Zeit kein ACK-Paket vom Empfänger empfangen wurde. Dies löst den Timeout-Retransmissionsmechanismus aus, `needsend = 1`, um die Daten erneut zu senden.

Mit der Implementierung von Bestätigungen und der Mechanik zur erneuten Übertragung bei Zeitüberschreitung kann KCP die Grundlage für eine zuverlässige Datenübertragung bieten. Doch um eine stabilere Datenflussrate aufrechtzuerhalten, hat KCP noch weitere Optimierungen vorgenommen. Lassen Sie uns gemeinsam einen Blick darauf werfen, welche weiteren Optimierungen KCP durchgeführt hat.

##KCP-Strategie zur Steigerung des Durchflusses

###Schnelle Wiederübertragung

Der Absender hat Pakete mit den Nummern 'sn' und 'sn + 1' gesendet. Wenn nur das ACK-Paket von 'sn + 1' erhalten wurde, könnte dies daran liegen, dass das ACK-Paket von 'sn' noch nicht im Netzwerk angekommen ist, oder es verloren gegangen ist, oder aber das Datenpaket 'sn' verloren gegangen ist. Wenn zu diesem Zeitpunkt die Zeit für die erneute Übertragung noch nicht abgelaufen ist, das Netzwerk auch noch nicht zu überlastet ist, sondern nur aus irgendeinem Grund unerwartet Pakete verloren gegangen sind, dann kann das vorzeitige Senden des 'sn' Datenpakets durch den Absender dem Empfänger helfen, die Daten schneller zu erhalten und die Übertragungsgeschwindigkeit zu verbessern.

KCP implementiert auch einen schnellen Wiederholungsmechanismus, der in `ikcp_flush` enthalten ist:

<details>
Zusammenfassung: Schnelle Wiederübertragung (zum Anzeigen des Codes klicken)
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
Schnelle Übertragung
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

Um eine schnelle erneute Übertragung zu ermöglichen, müssen zwei Bedingungen erfüllt sein:
`segment->fastack >= resent`，resent ist ein konfigurierbarer Parameter `kcp->fastresend`, die Konfiguration auf 0 schaltet das Schnellwiederholen aus. `segment->fastack` wird in der Funktion `ikcp_parse_fastack` gesetzt, diese Funktion wird in `ikcp_input` aufgerufen und erhöht `segment->fastack` für alle `sn` kleiner als `maxack`, der durch `ikcp_input` berechnet wird. Dadurch zeigt `segment->fastack` die Anzahl der erhaltenen Pakete mit einer Sequenznummer größer als `sn` an.
`segment->xmit <= kcp->fastlimit || kcp->fastlimit <= 0`，`setgment->xmit` represents the number of transmissions, while `kcp->fastlimit` stands for the configurable maximum fast retransmission times. The number of transmissions must be less than the maximum fast retransmission times.

Sobald die oben genannten Bedingungen für schnelle Wiederübertragung erfüllt sind, wird KCP diese durchführen. Beachten Sie, dass die schnelle Wiederübertragung die Übertragungszeit nicht zurücksetzt, die ursprüngliche Zeit bleibt gültig.

###Kürzen Sie die Timeouts für die Retransmission.

The retransmission timeout is a great mechanism, but it just takes too much time. Following TCP's strategy, the retransmission timeout doubles each time, causing the wait time to rapidly expand. During this waiting period, it's very likely that the receiving end's window is already full and unable to receive new data. The packet awaiting retransmission is at the front, so the receiver must get the retransmitted packet before returning all the data to the higher layer. In this scenario, the network's speed is nearly zero. KCP introduces configurations to slow down the growing wait time, and it won't double. By setting `kcp->nodelay`, the wait time will only increase by 1 or 0.5 times the RTO, effectively slowing down the growth of waiting time and helping the network to quickly restore its speed.

###Aktualisieren Sie das sendende Fenster.

Das Sendefenster gibt an, wie viele Datenpakete gleichzeitig übertragen werden, je größer das Fenster, desto mehr Daten werden gleichzeitig übertragen, die Datenrate steigt. Ein zu großes Fenster kann jedoch zu Netzwerküberlastung führen, was zu erhöhter Paketverlust, vermehrten Datenwiederholungen und letztendlich zu einer Verringerung der Datenrate führt. Daher muss das Sendefenster je nach Netzwerkbedingungen kontinuierlich aktualisiert werden, um sich allmählich der optimalen Größe anzunähern. Im KCP ist die Implementierung des Sendefensters im Code wie folgt:

<details>
<Zusammenfassung> Sendefenster (zum Anzeigen des Codes klicken) </Zusammenfassung>
```cpp
ikcpcb* ikcp_create(IUINT32 conv, void *user)
{
    // ...
// snd_wnd, rcv_wnd Die Größe der Sendungs- und Empfangspuffer.
    kcp->snd_wnd = IKCP_WND_SND;    // 32
    kcp->rcv_wnd = IKCP_WND_RCV;    // 128
// Empfangsfenstergröße auf der Zielseite              // 128
    kcp->rmt_wnd = IKCP_WND_RCV
// Initialisierung des Sendefensters cwnd auf 0
    kcp->cwnd = 0;
Übermitteln Sie die Größe des Fensterbytes, die zur Berechnung von cwnd verwendet wird.
    kcp->incr = 0
// Slow-start-Schwelle
    kcp->ssthresh = IKCP_THRESH_INIT;
nocwnd ist eine konfigurierbare Parameter, 1 vernachlässigt cwnd.
    kcp->nocwnd = 0;
    // ...
}

void ikcp_flush(ikcpcb *kcp)
{
    // ...
Beim Senden von Daten wird zuerst die Größe des Sendefensters berechnet, die das Minimum aus der Sendepuffergröße und der Größe des Empfangsfensters des Gegenübers ist.
    cwnd = _imin_(kcp->snd_wnd, kcp->rmt_wnd);
Standardmäßig muss auch kcp->cwnd berücksichtigt werden, das ist das ständig aktualisierte Sendefenster.
    if (kcp->nocwnd == 0) cwnd = _imin_(kcp->cwnd, cwnd);

// Basierend auf der Größe von cwnd wird snd_queue in snd_buf verschoben.
    while (_itimediff(kcp->snd_nxt, kcp->snd_una + cwnd) < 0) {
    }
// Sende Daten
    resent = (kcp->fastresend > 0)? (IUINT32)kcp->fastresend : 0xffffffff;
Auslösen von erneuter Übertragung bei Zeitüberschreitung lost = 1
// Auslösen von schnellem Re-Send-Change++

Aktualisieren Sie den Slow-Start-Schwellenwert und das Sendefenster.
    if (change) {
Wenn Schnellübertragung ausgelöst wird, wird der Schwellenwert (ssthresh) auf die Hälfte der Anzahl der Datenpakete festgelegt, die gerade im Netzwerk übertragen werden.
        IUINT32 inflight = kcp->snd_nxt - kcp->snd_una;
        kcp->ssthresh = inflight / 2;
        if (kcp->ssthresh < IKCP_THRESH_MIN)
            kcp->ssthresh = IKCP_THRESH_MIN;

// Das Sendefenster ist die Schwelle plus Resent relevante Informationen für schnelles erneutes Senden.
        kcp->cwnd = kcp->ssthresh + resent;
        kcp->incr = kcp->cwnd * kcp->mss;
    }

    if (lost) {
Wenn ein Timeout auftritt und eine erneute Übertragung erforderlich ist, wird eine langsame Starte ausgelöst, wobei der ssthresh-Schwellenwert auf die Hälfte des Sendefensters gesetzt wird.
        kcp->ssthresh = cwnd / 2;
        if (kcp->ssthresh < IKCP_THRESH_MIN)
            kcp->ssthresh = IKCP_THRESH_MIN;
Stellen Sie das Sendefenster wieder auf 1 und starten Sie das langsame Wachstum erneut.
        kcp->cwnd = 1;
        kcp->incr = kcp->mss;
    }

    if (kcp->cwnd < 1) {
Da es als 0 initialisiert wird, wird es hier auf 1 gesetzt.
        kcp->cwnd = 1;
        kcp->incr = kcp->mss;
    }
}

int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    IUINT32 prev_una = kcp->snd_una;
Verarbeite empfangene Daten.

    while (1) {
        // ...
        data = ikcp_decode16u(data, &wnd)
// rmt_wnd is the size of the receiving window on the other side
        kcp->rmt_wnd = wnd
        // ...
Verarbeite Daten.
    }

Bitte übersetzen Sie diesen Text ins Deutsche:

// Letztes Update der Sendewindow
kcp->snd_una - prev_una > 0, indicates that this input has received an ACK and the send buffer snd_buf has changed.
    if (_itimediff(kcp->snd_una, prev_una) > 0) {
// Überprüfen Sie erneut das Empfangsfenster des Gegners
        if (kcp->cwnd < kcp->rmt_wnd) {
            IUINT32 mss = kcp->mss;

            if (kcp->cwnd < kcp->ssthresh) {
Kleiner als die Slow-Start-Schwelle, verdoppelt sich die Größe.
                kcp->cwnd++;
                kcp->incr += mss;

            }    else {
Nach Überschreitung des Schwellenwerts für das langsame Starten wird die Variable "incr" gemäß der Formel aktualisiert, um dann die Variable "cwnd" zu berechnen.
                if (kcp->incr < mss) kcp->incr = mss;
                kcp->incr += (mss * mss) / kcp->incr + (mss / 16);
                if ((kcp->cwnd + 1) * mss <= kcp->incr) {
                    kcp->cwnd++;
                }
            }
Die aktualisierten Werte müssen noch mit rmt_wnd verglichen werden.
            if (kcp->cwnd > kcp->rmt_wnd) {
                kcp->cwnd = kcp->rmt_wnd;
                kcp->incr = kcp->rmt_wnd * mss;
            }
        }
    }
}
```
</details>

Die Berechnung der Größe des Sendefensters "kcp->cwnd" in Codeausschnitten ist etwas umfangreicher, da sie beim Senden und Empfangen von Daten aktualisiert werden muss. "kcp->cwnd" wird mit 0 initialisiert,
Bei der ersten Verwendung von `ikcp_flush` wird geprüft, ob es kleiner als 1 ist, und in diesem Fall auf 1 geändert. Dann sendet der Absender entsprechend der Größe des Sendefensters die entsprechende Anzahl von Datenpaketen und wartet auf die Bestätigung (ACK).
Reply package. ACK packets are processed in `kcp->input`. If the `kcp->input` detects an ACK packet and there is a clearing of sent data packets in the send buffer, it means that some data packets have been successfully delivered, and `kcp->cwnd++`. In reality, it is likely that only one ACK packet is handled in each `kcp->input`, so for each ACK packet received, `kcp->cwnd++`, leading to a doubling effect. For instance, if the current `kcp->cwnd = 2`, two data packets are sent, and receiving two ACK packets triggers two increments, resulting in `kcp->cwnd = 4`, doubling the value.

`cwnd` kann exponentiell wachsen, bis es den Schwellenwert für den langsamen Start überschreitet oder es zu Staus kommt, die eine Timeout-Retransmission oder eine schnelle Retransmission auslösen. Nach einer Timeout-Retransmission wird der langsame Start ausgelöst, der Schwellenwert für den langsamen Start beträgt `ssthresh = kcp->cwnd / 2`, das Sendefenster `kcp->cwnd = 1` wird auf den Anfangswert zurückgesetzt und beginnt erneut exponentiell zu wachsen. Bei einer schnellen Retransmission reduziert KCP zunächst vorzeitig die `ssthresh`, was bedeutet, dass der Raum für das exponentielle Wachstum von `cwnd` reduziert wird, die Wachstumsgeschwindigkeit verringert wird und die Stausituation frühzeitig entschärft wird.

KCP hat eine Konfiguration namens 'nocwnd' hinzugefügt. Wenn 'nocwnd = 1' ist, wird beim Senden von Daten die Sendefenstergröße nicht mehr berücksichtigt. Stattdessen werden die maximal mögliche Anzahl an Datenpaketen direkt gesendet, um die Anforderungen des Hochgeschwindigkeitsmodus zu erfüllen.

##Zusammenfassung

Der Text analysiert kurz den Quellcode von KCP sowie die Implementierung von ARQ auf KCP und einige Strategien zur Steigerung der Übertragungsgeschwindigkeit von KCP. Es werden viele Details nicht erwähnt, also kann man sich bei Interesse den Quellcode von KCP selbst anschauen und Vergleiche anstellen, um sicherlich Erkenntnisse zu gewinnen.

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt, bitte lassen Sie es uns in [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Weise auf etwaige Auslassungen hin. 
