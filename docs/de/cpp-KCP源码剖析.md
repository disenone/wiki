---
layout: post
title: KCP Quellcode-Analyse
categories:
- c++
catalog: true
tags:
- dev
description: Dieser Artikel analysiert einfach den Quellcode von KCP und diskutiert
  die Implementierung von ARQ auf KCP sowie einige Strategien zur Steigerung der Übertragungsgeschwindigkeit
  von KCP.
figures: []
---

<meta property="og:title" content="KCP 源码剖析" />

Bevor Sie diesen Text lesen, nehmen Sie sich bitte einen Moment Zeit, um die KCP-Projektdokumentation anzusehen, wenn Sie noch nie von KCP gehört haben oder überhaupt nichts darüber wissen: [Link](https://github.com/skywind3000/kcp)Der Zweck dieses Textes ist es, sich eingehend mit den Implementierungsdetails von KCP zu beschäftigen, um KCP zu verstehen.

##Was ist KCP

KCP ist ein schnelles und zuverlässiges Protokoll, das Daten mit geringerer Verzögerung als TCP übertragen kann, was zu schnelleren Datenübertragungen und kürzeren Wartezeiten bei der Datenübertragung führt.

> TCP ist für den Datenverkehr entworfen (wie viele KB Daten pro Sekunde übertragen werden können) und legt Wert auf eine effiziente Nutzung der Bandbreite. KCP hingegen ist auf die Übertragungsgeschwindigkeit ausgelegt (wie lange ein einzelnes Datenpaket benötigt, um von einem Ende zum anderen zu gelangen) und erzielt bei einer 10%-20%igen Bandbreitenausnutzung eine Übertragungsgeschwindigkeit, die 30%-40% schneller ist als die von TCP. Der TCP-Kanal ist ein sehr langsamer, aber sehr breiter Verkehrsfluss, während KCP ein rasch fließender kleiner Bach ist.

Oben steht, was im KCP-Dokument geschrieben ist, die Schlüsselwörter sind **Bandbreite** und **Übertragungsgeschwindigkeit**. KCP reduziert die Bandbreite, bringt jedoch den Vorteil einer größeren, gleichmäßigeren Übertragungsrate. Weitere Erläuterungen finden Sie in der KCP-Dokumentation selbst.

##KCP Datenstruktur

Der KCP-Quellcode befindet sich in `ikcp.h` und `ikcp.c`. In `ikcp.h` liegt der Schwerpunkt auf der Deklaration von Datenstrukturen, wobei zunächst das `SEGMENT`-Paket genannt wird, das die kleinste Einheit zur Verarbeitung von Daten im KCP-Protokoll darstellt:

<details>
<summary> SEGMENT-Struktur (Klicken Sie hier, um den Code zu erweitern) </summary>
```cpp
//=====================================================================
// EIN SEGMENT IST EIN DATENPAKET
//=====================================================================
struct IKCPSEG
{
// Listenknotem, sowohl das Senden als auch das Empfangen von Warteschlangen basieren auf der Struktur dieser Liste.
    struct IQUEUEHEAD node;

Session ID, die gleiche Session ID ist gleich.
    IUINT32 conv;

// Pakettyp, wie z.B. DATA oder ACK
    IUINT32 cmd;

Aufgrund der MTU-Beschränkung werden große Datenpakete in mehrere kleine Datenpakete aufgeteilt, dies ist die Nummer des kleinen Datenpakets.
    IUINT32 frg

// Jedes Datenpaket wird mit der Empfangsfenstergröße des Senders versehen.
    IUINT32 wnd;

// Sendezeit, wenn es sich um ein ACK-Paket handelt, wird sie auf den ts des Quellpakets gesetzt.
    IUINT32 ts;

// Die Nummer, die das Datenpaket eindeutig identifiziert
    IUINT32 sn;

// Paketdaten, die kleiner als una sind, wurden erfolgreich empfangen, was mit der Bedeutung von TCP übereinstimmt: älteste nicht bestätigte Sequenznummer SND
    IUINT32 una;

// Datenlänge
    IUINT32 len;

Übertragungszeitüberschreitung
    IUINT32 resendts;

Das nächste Mal die Ablaufzeit.
    IUINT32 rto;

Sobald eine bestimmte Anzahl von Datenpaketen nach dem Empfang dieses Pakets erreicht ist, wird eine schnelle Neuübertragung ausgelöst.
    IUINT32 fastack;

// Anzahl der Sendungen
    IUINT32 xmit;

// Daten
    char data[1];
};
```
</details>

Nachdem du die Kommentare von `SEGMENT` gelesen hast, kannst du grob erkennen, dass der Kern von KCP auch ein ARQ-Protokoll ist, das die Datenübermittlung durch automatisches Timeout-Resending gewährleistet. Schauen wir uns jetzt die Definition der KCP-Struktur `KCPCB` an:

<details>
<Zusammenfassung> KCP-Struktur (Klicken Sie, um den Code anzuzeigen) </Zusammenfassung>
```cpp
//---------------------------------------------------------------------
// IKCPCB
//---------------------------------------------------------------------
struct IKCPCB
{
// Gesprächs-ID
// mtu, mss: Maximum Transmission Unit, maximum segment size
// Zustand: Sitzungstatus, 0 gültig, -1 getrennt
    IUINT32 conv, mtu, mss, state;

// snd_una: Paketnummer des erwarteten ACK
// snd_nxt: Next sequence number of the packet waiting to be sent.
// rcv_nxt: Die Nummer des nächsten zu empfangenden Datenpakets
    IUINT32 snd_una, snd_nxt, rcv_nxt;

// ts_recent, ts_lastack: Nicht verwendet
// ssthresh: Staukontrolle Schwellenwert für den langsamen Start
    IUINT32 ts_recent, ts_lastack, ssthresh;

// rx_rto: rto (Retransmission-Timeout), Zeit für erneute Übertragungen bei Zeitüberschreitung
// rx_rttval, rx_srtt, rx_minrto: Calculate intermediate variables for calculating RTO.
    IINT32 rx_rttval, rx_srtt, rx_rto, rx_minrto;

// snd_wnd, rcv_wnd: Maximum send and receive window size
// rmt_wnd: Remote-Fenster, verbleibende Empfangsfenstergröße auf der Gegenstelle
// cwnd: Größe des sendbaren Fensters
// Stichprobe: Flag, ob Steuerungsdaten gesendet werden sollen
    IUINT32 snd_wnd, rcv_wnd, rmt_wnd, cwnd, probe;

// aktuell: aktuelle Zeit
- Intervall: Update-Intervall
// ts_flush: Zeitpunkt für das nächste erforderliche Update
// xmit: Anzahl der gescheiterten Sendungen
    IUINT32 current, interval, ts_flush, xmit;

// Die Länge der verknüpften Liste
    IUINT32 nrcv_buf, nsnd_buf;
    IUINT32 nrcv_que, nsnd_que;

// nodelay: Steuerung der Wachstumsrate des rto für das Timeout-Resend
// aktualisiert: Wurde ikcp_update aufgerufen?
    IUINT32 nodelay, updated;

// ts_probe, probe_wait: Bei dauerhaftem Empfangsfenster des Gegenüber von 0 wird aktiv regelmäßig eine Anfrage gestartet.
    IUINT32 ts_probe, probe_wait;

// deal_link: Gegenüber reagiert lange Zeit nicht
// erhöht: Beteiligt sich an der Berechnung der Sendefenstergröße
    IUINT32 dead_link, incr;

// queue: Die Datenpakete, die mit der Benutzerebene in Kontakt stehen
// buf: Protokollcache-Datenpaket
    struct IQUEUEHEAD snd_queue;
    struct IQUEUEHEAD rcv_queue;
    struct IQUEUEHEAD snd_buf;
    struct IQUEUEHEAD rcv_buf;

// Informationen zu den Datenpaketen, die ein ack senden müssen
    IUINT32 *acklist;

// Anzahl der Pakete, die ein ack benötigen
    IUINT32 ackcount;

// acklist Speichergröße
    IUINT32 ackblock;

// Vom Benutzer geschickte Daten
    void *user;

Speicherplatz für ein KCP-Paket bereitstellen.
    char *buffer;

// Anzahl der fastack-Auslöser für schnelle erneute Übertragung
    int fastresend;

// Maximale Anzahl der schnellen Wiederübertragungen
    int fastlimit;

// nocwnd: Berücksichtigt nicht die Größe des Sendefensters beim langsamen Start
// stream: Strommodus
    int nocwnd, stream;

    // debug log
    int logmask;

// Daten senden-Schnittstelle
    int (*output)(const char *buf, int len, struct IKCPCB *kcp, void *user);

    void (*writelog)(const char *log, struct IKCPCB *kcp, void *user);
};
```
</details>

Indem wir die Felder der KCP-Struktur einzeln kommentieren, können wir zunächst feststellen, dass das gesamte KCP-Protokoll nicht sehr komplex ist. Wenn wir den Code im Detail analysieren, können wir beide das KCP-Protokoll lesen und verstehen :smile:

##Die ARQ-Implementierung von KCP

KCP ist im Wesentlichen ein ARQ (Auto Repeat-reQuest, automatische Wiederholungsanforderung) Protokoll, dessen grundlegende Aufgabe die Sicherstellung zuverlässiger Übertragungen ist. Lassen Sie uns also zunächst auf den grundlegenden ARQ-Teil von KCP eingehen, wie KCP die zuverlässige Übertragung realisiert.

ARQ, wie der Name schon sagt, sendet automatisch das entsprechende Datenpaket erneut, wenn wir vermuten, dass das Gegenüber das Datenpaket nicht erfolgreich empfangen hat. Dies wird durch zwei Mechanismen – Bestätigungsempfang und Zeitüberschreitung – erreicht, um eine zuverlässige Übertragung zu gewährleisten. In der konkreten Implementierung weist KCP jedem Datenpaket (das im vorherigen Abschnitt erwähnte `SEGMENT`) eine eindeutige `sn`-Kennung zu. Sobald das Gegenüber das Datenpaket empfängt, sendet es ein ACK-Paket (ebenfalls ein `SEGMENT`) als Antwort. Die `sn` des ACK-Pakets entspricht der `sn` des empfangenen Datenpakets und signalisiert, dass das Datenpaket erfolgreich empfangen wurde. Außerdem gibt es im `SEGMENT` ein `una`-Feld, das die Nummer des nächsten erwarteten Datenpakets angibt. Mit anderen Worten: Alle vorhergehenden Datenpakete wurden bereits empfangen, was einem vollständigen ACK-Paket entspricht. Der Sender kann so schneller den Sendepuffer und das Sendefenster aktualisieren.

Wir können durch Verfolgung des Sendens und Empfangens von KCP-Paketen den grundlegendsten ARQ-Implementierungen nachvollziehen:

###Senden

Der Sendvorgang ist `ikcp_send` -> `ikcp_update` -> `ikcp_output`. Die obere Schicht ruft `ikcp_send` auf, um Daten an KCP zu übermitteln, KCP verarbeitet die Datenübertragung in `ikcp_update`.

<details>
<summary> ikcp_send（Klicken Sie hier, um den Code auszuweiten） </summary>
```cpp
//---------------------------------------------------------------------
// Datenübermittlungs-Schnittstelle, Benutzer ruft ikcp_send auf, um kcp zum Senden von Daten zu bringen
// user/upper level send, returns below zero for error
//---------------------------------------------------------------------
int ikcp_send(ikcpcb *kcp, const char *buffer, int len)
{
    IKCPSEG *seg;
    int count, i;

Das "mss" darf nicht kleiner als 1 sein.
    assert(kcp->mss > 0);
    if (len < 0) return -1;

    // append to previous segment in streaming mode (if possible)
    if (kcp->stream != 0) {
// Verarbeitungsstrommodus
        // ......
    }

Berechnen Sie die Fragmentierung. Wenn die Datenlänge len größer als mss ist, müssen sie in mehrere Pakete aufgeteilt und gesendet werden, die dann vom Empfänger wieder zusammengesetzt werden.
    if (len <= (int)kcp->mss) count = 1;
    else count = (len + kcp->mss - 1) / kcp->mss;

    if (count >= (int)IKCP_WND_RCV) return -2;

    if (count == 0) count = 1;

// Unterauftragnehmer
    for (i = 0; i < count; i++) {
Berechne die Länge der Paketdaten und weise der entsprechenden Seg-Struktur zu.
        int size = len > (int)kcp->mss ? (int)kcp->mss : len;
        seg = ikcp_segment_new(kcp, size);
        assert(seg);
        if (seg == NULL) {
            return -2;
        }

// Setze die Dateninformationen von seg, frg steht für die Teilpaketnummer
        if (buffer && len > 0) {
            memcpy(seg->data, buffer, size);
        }
        seg->len = size;
        seg->frg = (kcp->stream == 0)? (count - i - 1) : 0;

// Füge am Ende der snd_queue hinzu, nsnd_qua um eins erhöhen
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

`ikcp_send` is the data sending interface called by the higher layers of KCP. All data to be sent by KCP should go through this interface. `ikcp_send` simply divides the data into multiple packets according to `kcp->mss` (maximum data length per packet), sets packet numbers, and then appends them to the end of the send queue `snd_queue`. In streaming mode, data sent through multiple calls to `ikcp_send` is treated as a continuous stream. It will first fill in incomplete `SEGMENT`s automatically before allocating new ones. The detailed implementation is not discussed in this text. Those interested can understand it by reading this text and then looking at the corresponding code.

Nachdem der Aufruf von `ikcp_send` abgeschlossen ist, werden die Daten in der `snd_queue` von KCP abgelegt. Danach muss KCP einen geeigneten Zeitpunkt finden, um die zu sendenden Daten zu übertragen. Dieser Code befindet sich sowohl in `ikcp_update` als auch in `ikcp_flush`.

<details>
<summary> ikcp_update（Klicken Sie hier, um den Code anzuzeigen） </summary>
```cpp
//---------------------------------------------------------------------
// ikcp_update ist eine Schnittstelle, die regelmäßig von der oberen Ebene aufgerufen wird, um den Status von kcp zu aktualisieren und Daten zu senden.
// update state (call it repeatedly, every 10ms-100ms), or you can ask 
// ikcp_check when to call it again (without ikcp_input/_send calling).
// 'current' - current timestamp in millisec. 
//---------------------------------------------------------------------
void ikcp_update(ikcpcb *kcp, IUINT32 current)
{
    IINT32 slap;

    kcp->current = current;

// ikcp_flush wird dies überprüfen, die obere Schicht muss ikcp_update aufgerufen haben, bevor ikcp_flush aufgerufen werden kann. Es wird empfohlen, nur ikcp_update zu verwenden.
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
// Nächste Flush-Zeit
        kcp->ts_flush += kcp->interval;
        if (_itimediff(kcp->current, kcp->ts_flush) >= 0) {
            kcp->ts_flush = kcp->current + kcp->interval;
        }
        ikcp_flush(kcp);
    }
}
```
</details>

Die `ikcp_update` Funktion ist recht einfach: Es überprüft die Zeit von `ts_flush`, und wenn die Bedingung erfüllt ist, wird `ikcp_flush` aufgerufen. Der Hauptteil der Verarbeitungslogik liegt in `ikcp_flush`, da der Inhalt von `ikcp_flush` etwas komplexer ist. Wir konzentrieren uns momentan nur auf die Teile, die mit dem Senden im Zusammenhang mit dem ARQ zu tun haben.

<details>
Zusammenfassung: Senden von Daten (Klicken, um den Code anzuzeigen)
```cpp
//---------------------------------------------------------------------
// ikcp_flush
//---------------------------------------------------------------------
void ikcp_flush(ikcpcb *kcp)
{
    IUINT32 current = kcp->current;

// Der Puffer ist die Daten, die an ikcp_output übergeben werden sollen, und wird mit der dreifachen Größe des Datenpakets initialisiert.
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

// seg.wnd ist die aktuelle Größe des empfangbaren Fensters
    seg.wnd = ikcp_wnd_unused(kcp);
    seg.una = kcp->rcv_nxt;
    seg.len = 0;
    seg.sn = 0;
    seg.ts = 0;

// ACK senden
// Berechne das Sendefenster
    //...

// Bewege das Datenpaket von snd_queue nach snd_buf
Die Bewegung hängt von der Größe des Sendefensters ab. Wenn das Sendefenster voll ist, wird die Bewegung gestoppt.
// Die Daten, die sich im snd_buf befinden, sind die Daten, die direkt mit ikcp_output an die Gegenstelle gesendet werden können.
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

// seg eindeutige Seriennummer, eigentlich ist es eine inkrementelle kcp->snd_nxt
        newseg->sn = kcp->snd_nxt++;

// una is set here to notify the other end of the next package number to be received.
        newseg->una = kcp->rcv_nxt;
        newseg->resendts = current;
        newseg->rto = kcp->rx_rto;
        newseg->fastack = 0;
        newseg->xmit = 0;
    }

// Berechnen des Fast-Retransmit-Flags, der Timeout-Wartezeit.
    // ...

// sende snd_buf
    for (p = kcp->snd_buf.next; p != &kcp->snd_buf; p = p->next) {
        IKCPSEG *segment = iqueue_entry(p, IKCPSEG, node);
        int needsend = 0;
        if (segment->xmit == 0) {
// Erstmalige Sendung
// set->xmit zeigt die Anzahl der Sendungen an
// resendts Wartezeit für zeitlich begrenzte Neuübertragung
            needsend = 1;
            segment->xmit++;
            segment->rto = kcp->rx_rto;
            segment->resendts = current + segment->rto + rtomin;
        }
        else if (_itimediff(current, segment->resendts) >= 0) {
            // Timeout-Wiederübertragung
            // ...
        }
        else if (segment->fastack >= resent) {
// Schnelles Retransmission
            // ...
        }

        if (needsend) {
            int need;
            segment->ts = current;
            segment->wnd = seg.wnd;
            segment->una = kcp->rcv_nxt;

            size = (int)(ptr - buffer);
            need = IKCP_OVERHEAD + segment->len;

Sobald die Daten im Puffer die MTU überschreiten, sollten sie zuerst gesendet werden, um zu vermeiden, dass sie erneut auf unterer Ebene aufgeteilt werden.
            if (size + need > (int)kcp->mtu) {
                ikcp_output(kcp, buffer, size);
                ptr = buffer;
            }

// Kopiere die seg Steuerdaten in den Puffer, kcp kümmert sich selbst um die Endianness-Problematik.
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

// Berechnung von ssthresh, Aktualisierung des Slow-Start-Fensters
    // ...
}
```
</details>

Wir konzentrieren uns derzeit nur auf die Logik des Datenversands innerhalb der Funktion "ikcp_flush".

Zuerst wird KCP basierend auf der Empfangsfenstergröße der Gegenstelle die Daten aus der `snd_queue` in den `snd_buf` verschieben. Die Formel zur Berechnung der Verschiebungsanzahl lautet `num = snd_nxt - (snd_una + cwnd)`, das heißt: die maximal erfolgreich gesendete Paketsequenznummer `snd_una` plus die Größe des Gleitfensters `cwnd` ist größer als die nächste zu sendende Paketsequenznummer `snd_nxt`, dann können neue Datenpakete weiter gesendet werden. Beim Verschieben von `SEG` werden gleichzeitig Steuerfelder gesetzt.

* Durchlaufe `snd_buf`, und falls ein Datenpaket gesendet werden muss, kopiere die Daten in den `buffer`. Während des Kopiervorgangs wird das Endianness-Problem der Steuerfeld-Daten mit `ikcp_encode_seg` behandelt.

Am Ende wird `ikcp_output` aufgerufen, um die Daten auf `buffer` zu senden.

Damit hat KCP die Datenübertragung abgeschlossen.

###Empfang

Der Empfangsprozess verläuft entgegengesetzt zu dem des Sendens: `ikcp_input` -> `ikcp_update` -> `ikcp_recv`. Nachdem der Benutzer die Daten aus dem Netzwerk empfangen hat, muss er `ikcp_input` aufrufen, um sie an KCP zur Analyse weiterzuleiten. Bei der Ausführung von `ikcp_update` wird ein ACK-Paket an die sendende Seite zurückgesendet, und die Anwendungsschicht verwendet `ikcp_recv`, um die von KCP analysierten Daten zu empfangen.

<details>
Zusammenfassung: Daten empfangen (Zum Anzeigen des Codes klicken)
```cpp
//---------------------------------------------------------------------
// input data
//---------------------------------------------------------------------
int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    IUINT32 prev_una = kcp->snd_una;
    IUINT32 maxack = 0, latest_ts = 0;
    int flag = 0;

// Rechtsprüfung
    if (data == NULL || (int)size < (int)IKCP_OVERHEAD) return -1;

// Daten können mehrere KCP-Pakete sein, Verarbeitung in einer Schleife
    while (1) {
        IUINT32 ts, sn, len, una, conv;
        IUINT16 wnd;
        IUINT8 cmd, frg;
        IKCPSEG *seg;

// Nicht genug für ein KCP-Paket, beenden
        if (size < (int)IKCP_OVERHEAD) break;

Zuerst sollten die Steuerzeichen analysiert werden.
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

// Hier ist una der kcp->rcv_nxt des Senders. Anhand dieser Daten können die bereits bestätigten empfangenen Pakete entfernt werden.
        ikcp_parse_una(kcp, una);
// Nachdem die bestätigten Pakete entfernt wurden, aktualisiere die nächste zu sendende Sequenznummer snd_una
        ikcp_shrink_buf(kcp);

        if (cmd == IKCP_CMD_ACK) {
// Bestätigungspaket
            // ...
        }
        else if (cmd == IKCP_CMD_PUSH) {
Datapaket
// Wenn die empfangene Datenpaketnummer sn im Empfangsfenster liegt, wird sie normal verarbeitet, andernfalls wird sie sofort verworfen und auf eine erneute Übertragung gewartet.
            if (_itimediff(sn, kcp->rcv_nxt + kcp->rcv_wnd) < 0) {

// Jedes empfangene Datenpaket muss mit einem Ack-Paket zurückgesendet werden, das protokolliert wird.
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
// Erkundigen Sie sich bei Fensterpaket
            // ...
        }
        else if (cmd == IKCP_CMD_WINS) {
// Antwortpaket für die Abfrageanzeige
            // ...
        }
        else {
            return -3;
        }

        data += len;
        size -= len;
    }

// Verarbeitung der Logik für schnelle Übertragungswiederholungen
    // ...

// Aktualisiere das Senden-Fenster
    // ...

    return 0;
}
```
</details>

`ikcp_input` verarbeitet jede `SEG`-Pack, indem zunächst die Gültigkeit und der Typ des Datenpakets überprüft werden. Da jedes Datenpaket eine `una`-Nummer enthält, die die vom Sender erwartete Empfangssequenz markiert, sind alle Pakete mit einer Sequenznummer, die kleiner als `una` ist, bereits erfolgreich vom Empfänger akzeptiert worden. Daher kann man alle Pakete im `snd_buff`, die kleiner als `una` sind, löschen und `snd_nxt` aktualisieren. Dieser Teil wird von `ikcp_parse_una` und `ikcp_shrink_buf` bearbeitet. Jedes empfangene Datenpaket muss mit einem ACK-Paket beantwortet werden, das von `ikcp_ack_push` erfasst wird. Schließlich wird `ikcp_parse_data` aufgerufen, um die Daten zu verarbeiten.

<details>
<Zusammenfassung> Analysiere Daten (Klicken Sie, um den Code anzuzeigen) </Zusammenfassung>
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

Ermitteln Sie den Ort, an dem newseg platziert werden soll, da der empfangene seg möglicherweise nicht in der richtigen Reihenfolge ist.
    for (p = kcp->rcv_buf.prev; p != &kcp->rcv_buf; p = prev) {
        IKCPSEG *seg = iqueue_entry(p, IKCPSEG, node);
        prev = p->prev;
        if (seg->sn == sn) {
// Wiederholte Empfang
            repeat = 1;
            break;
        }
        if (_itimediff(sn, seg->sn) > 0) {
            break;
        }
    }

// Setze newseg an die richtige Stelle in rcv_buf
    if (repeat == 0) {
        iqueue_init(&newseg->node);
        iqueue_add(&newseg->node, p);
        kcp->nrcv_buf++;
    }    else {
        ikcp_segment_delete(kcp, newseg);
    }

// Bewege die Daten von rcv_buf zu rcv_queue
    while (! iqueue_is_empty(&kcp->rcv_buf)) {
        IKCPSEG *seg = iqueue_entry(kcp->rcv_buf.next, IKCPSEG, node);
Wenn die SEG-Nummer auf die Empfangsnummer wartet, wird sie in die Empfangswarteschlange verschoben.
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

Die Hauptaufgabe von `ikcp_parse_data` besteht darin, `newseg` an die richtige Stelle im `kcp->rcv_buf` zu platzieren und die Daten vom `rcv_buf` in die `rcv_queue` zu verschieben. Die richtige Position im `rcv_buf` bedeutet, dass der `rcv_buf` nach `sn` aufsteigend sortiert ist und `newseg` die passende Position entsprechend seiner `sn` finden muss. Die Daten auf dem `rcv_buf` werden in die `rcv_queue` verschoben, wenn die Paketnummer auf dem `rcv_buf` der Paketnummer entspricht, auf die KCP wartet, `kcp->rcv_nxt`. Nach dem Verschieben eines Datenpakets muss `kcp->rcv_nxt` aktualisiert und das nächste Datenpaket verarbeitet werden.

Nach `ikcp_input` sendet der obere Layer beim Aufruf von `ikcp_update` ein ACK-Paket, und der Aufruf von `ikcp_recv` gibt dem oberen Layer gültige Daten zurück. `ikcp_update` und `ikcp_recv` sind unabhängig voneinander und haben keine Anforderungen an die Aufrufreihenfolge, abhängig von dem Zeitpunkt der Aufrufe des oberen Layers. Schauen wir uns zunächst den Teil von `ikcp_update` an, der mit dem Senden von ACKs zu tun hat:

<details>
<summary> Antwort ACK (Code anzeigen) </summary>
```cpp
Wie zuvor erwähnt, ruft ikcp_update letzten Endes ikcp_flush auf.
void ikcp_flush(ikcpcb *kcp, IUINT32 current)
{
    // ...

// Antwort ACK-Paket
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

Die ACK-Pakete wurden zuvor mit `ikcp_ack_push` gespeichert, deshalb muss hier nur `ikcp_ack_get` verwendet werden, um Informationen zu jedem ACK-Paket zu erhalten und sie dem Empfänger zu senden. Die Anwendungsschicht kann `ikcp_recv` verwenden, um Daten von KCP zu erhalten:

<details>
<Zusammenfassung> ikcp_recv (Klicken Sie, um den Code anzuzeigen) </Zusammenfassung>
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

// Einige Gültigkeitsprüfungen
    if (iqueue_is_empty(&kcp->rcv_queue))
        return -1;
    if (len < 0) len = -len;

// Berechnung der zurückgegebenen Datenlänge
    peeksize = ikcp_peeksize(kcp);

    if (peeksize < 0)
        return -2;
    if (peeksize > len)
        return -3;

Überprüfen Sie das Empfangsfenster.
    if (kcp->nrcv_que >= kcp->rcv_wnd)
        recover = 1;

// Durchsuche die rcv_queue und kopiere die Daten auf den Puffer
    for (len = 0, p = kcp->rcv_queue.next; p != &kcp->rcv_queue; ) {
        int fragment;
        seg = iqueue_entry(p, IKCPSEG, node);
        p = p->next;

        if (buffer) {
            memcpy(buffer, seg->data, seg->len);
            buffer += seg->len;
        }

        len += seg->len;

// Subunternehmer bestimmen
        fragment = seg->frg;

Entferne Datenpaket.
        if (ispeek == 0) {
            iqueue_del(&seg->node);
            ikcp_segment_delete(kcp, seg);
            kcp->nrcv_que--;
        }

// Alle Subaufträge sind kopiert, Schleife verlassen
        if (fragment == 0)
            break;
    }

    assert(len == peeksize);

Die `rcv_queue` wurde erneut teilweise geleert. Versuche weiterhin Daten vom `rcv_buf` in die `rcv_queue` zu verschieben.
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

`ikcp_recv` wird bei jedem Aufruf ein vollständiges Datenpaket zurückgeben. Die obere Schicht kann den Aufruf in einer Schleife wiederholen, bis kein Daten mehr zurückgegeben wird. Die Funktion ist recht einfach: Sie kopiert Daten aus der `rcv_queue` in den vom Aufrufer übergebenen `Buffer`. Damit hat der Empfänger die empfangenen Datenpakete vollständig verarbeitet.

Wenn der Empfänger das Datenpaket verarbeitet, sendet er ein ACK-Paket an den Sender. Schauen wir uns nun an, wie der Sender das ACK-Paket empfängt und verarbeitet:

<details>
Behandlung von ACK-Paketen (Zum Anzeigen des Codes klicken)
```cpp
int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    // ...
    IUINT32 maxack = 0, latest_ts = 0;
    // ...
    while (1) {
        // ...
// ts is the counterpart of kcp->current
        data = ikcp_decode32u(data, &ts);
        data = ikcp_decode32u(data, &sn);

        if (cmd == IKCP_CMD_ACK) {
// Update rot
            if (_itimediff(kcp->current, ts) >= 0) {
                ikcp_update_ack(kcp, _itimediff(kcp->current, ts));
            }
// Aktualisiere snd_buf
            ikcp_parse_ack(kcp, sn);
            ikcp_shrink_buf(kcp);

// maxack = die größte sn aus allen ACK-Paketen dieses Inputs
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

// Wenn ein ACK-Paket empfangen wird, wird es zur schnellen Retransmission aufgezeichnet.
    if (flag != 0) {
        ikcp_parse_fastack(kcp, maxack, latest_ts);
    }
}
```
</details>

Nach Erhalt des ACK-Pakets wird deutlich, dass `ikcp_parse_ack` und `ikcp_shrink_buf` zur Aktualisierung von `snd_buf` erforderlich sind. Außerdem muss `ikcp_update_ack` aufgerufen werden, um die rto (Retransmission Timeout, Zeit für erneute Übertragung) zu aktualisieren. `ikcp_input` berechnet die höchste Sequenznummer im empfangenen ACK-Paket, um sie für schnelle Neuübertragungen zu verwenden. So entfernt der Sender nach Erhalt des ACK-Pakets die zu sendenden Daten aus `snd_buf`, und das Datenpaket wird zuverlässig an den Empfänger übermittelt, wodurch der vollständige ARQ-Bestätigungsprozess abgeschlossen wird.

###Timeout Wiederübertragung

Im Folgenden wird der Bestätigungsmechanismus in der ARQ-Implementierung von KCP vorgestellt. ARQ benötigt auch einen Timeout-Wiederholungsmechanismus, um die Zuverlässigkeit zu gewährleisten. Lassen Sie uns nun ansehen, wie KCP die Timeout-Wiederholungen umsetzt.

Lassen Sie uns zur Funktion `ikcp_flush` zurückkehren:

<details>
<summary> Zeitüberschreitung beim erneuten Senden (Klicken, um den Code zu erweitern) </summary>
```cpp
void ikcp_flush(ikcpcb *kcp)
{
    // ...
// snd_buf senden
    for (p = kcp->snd_buf.next; p != &kcp->snd_buf; p = p->next) {
        IKCPSEG *segment = iqueue_entry(p, IKCPSEG, node);
        int needsend = 0;
        if (segment->xmit == 0) {
// Erster Versand
            needsend = 1;
            segment->xmit++;
// Setze segment->rto
// Berechnung der Timeout-Wiederübertragungszeit von segment->resendts durch segment->rto
            segment->rto = kcp->rx_rto;
            segment->resendts = current + segment->rto + rtomin;
        }
        else if (_itimediff(current, segment->resendts) >= 0) {
Timeout retransmission.
            needsend = 1;
            segment->xmit++;
            kcp->xmit++;
// nodelay steuert die Berechnung der Zeit für die nächste Timeout-Wiederübertragung.
            if (kcp->nodelay == 0) {
                segment->rto += kcp->rx_rto;
            }    else {
                segment->rto += kcp->rx_rto / 2;
            }
            segment->resendts = current + segment->rto;
            lost = 1;
        }
        else if (segment->fastack >= resent) {
Schnelle Übertragung

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

Sobald die aktuelle Zeit `current` größer als die Timeout-Wiederübertragungszeit `segment->resendts` ist, bedeutet das, dass in diesem Zeitraum keine ACK-Pakete vom Empfänger empfangen wurden. Dies löst den Timeout-Wiederübertragungsmechanismus aus, `needsend = 1`, und die Daten werden erneut gesendet.

Mit Bestätigung des Empfangs und dem Mechanismus für erneutes Senden bei Zeitüberschreitung kann KCP die grundlegende zuverlässige Datenübertragung gewährleisten. Doch um einen stabileren Datenfluss zu gewährleisten, hat KCP noch weitere Optimierungen vorgenommen. Mal sehen, welche Verbesserungen noch von KCP implementiert wurden.

##KCP Strategien zur Steigerung der Fließgeschwindigkeit

###Schnelle Neusendung

Der Sender hat zwei Datenpakete mit den Sequenznummern `sn` und `sn + 1` gesendet. Wenn nur das ACK-Paket für `sn + 1` empfangen wurde, kann das darauf hindeuten, dass das ACK-Paket für `sn` noch nicht im Netzwerk angekommen ist, dass das ACK-Paket verloren gegangen ist oder dass das Datenpaket für `sn` verloren gegangen ist. Wenn zu diesem Zeitpunkt die Zeit für eine Zeitüberschreitung noch nicht erreicht ist und das Netzwerk noch nicht zu überlastet ist, sondern nur aus einem bestimmten Grund temporär Pakete verloren gehen, kann der Sender aktiv das Datenpaket für `sn` vorzeitig senden, um dem Empfänger zu helfen, die Daten schneller zu empfangen und die Übertragungsrate zu erhöhen.

KCP implementiert auch einen Mechanismus für schnelle Übertragungen, der in `ikcp_flush` zu finden ist.

<details>
Zusammenfassung: Schnelle Übertragung (Klicken Sie hier, um den Code anzuzeigen)
```cpp
void ikcp_flush(ikcpcb *kcp)
{
    // ...
    resent = (kcp->fastresend > 0)? (IUINT32)kcp->fastresend : 0xffffffff;

// snd_buf senden
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
Schnelle Rückübertragung
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

Um eine schnelle Wiederübertragung zu initiieren, gibt es zwei Bedingungen:
* `segment->fastack >= resent`，resent ist ein konfigurierbarer Parameter `kcp->fastresend`, der bei 0 die schnelle Wiederübertragung deaktiviert. `segment->fastack` wird in der Funktion `ikcp_parse_fastack` gesetzt, die innerhalb von `ikcp_input` aufgerufen wird. Diese Funktion erhöht für alle `sn`, die kleiner sind als `maxack`, den Wert von `segment->fastack` um eins, basierend auf dem von `ikcp_input` berechneten `maxack`. Daher stellt `segment->fastack` die Anzahl der empfangenen Pakete dar, die eine größere SN haben.
`segment->xmit <= kcp->fastlimit || kcp->fastlimit <= 0`，“setgment->xmit” steht für die Anzahl der Sendungen, während “kcp->fastlimit” die konfigurierbare maximale Anzahl an schnellen Wiederholungen darstellt. Die Anzahl der Sendungen muss kleiner sein als die maximale Anzahl an schnellen Wiederholungen.

Sobald die oben genannten Bedingungen für die schnelle Wiederübertragung erfüllt sind, wird KCP die schnelle Wiederübertragung ausführen. Es ist zu beachten, dass die schnelle Wiederübertragung die Zeit für die zeitgesteuerte Wiederübertragung nicht zurücksetzt; die ursprüngliche Zeitüberschreitung bleibt weiterhin gültig.

###Verringern Sie die Zeit für das Timeout und die erneute Übertragung.

Die Timeout-Wiederübertragung ist ein sehr gutes Mechanismus, aber sie dauert einfach zu lange. Nach der TCP-Politik verdoppelt sich die Wiederübertragungszeit bei jedem Timeout, was dazu führt, dass die Wartezeit schnell anwächst. Während dieser Wartezeit kann es sehr gut sein, dass das Empfangsfenster auf der Empfängerseite erschöpft ist und keine neuen Daten empfangen kann. Da die zu erwartende Wiederübertragungsnummer ganz vorne steht, muss die Empfangsseite das wiederübertragene Paket erhalten, um alle Daten an die obere Ebene zurückgeben zu können. In solch einem Fall liegt die gesamte Netzwerkgeschwindigkeit nahezu bei 0. KCP bietet zusätzliche Konfigurationsmöglichkeiten, um das Wachstum der Wartezeit zu verlangsamen, und es geschieht nicht durch Verdopplung. Durch die Konfiguration von `kcp->nodelay` kann die Wartezeit bei jedem Mal nur um das 1-fache RTO oder um das 0,5-fache RTO wachsen, was effektiv das Wachstum der Wartezeit verlangsamt und dem Netzwerk hilft, die Geschwindigkeit schnell wiederherzustellen.

###Aktualisierungsfenster senden

Das Sende-Fenster gibt die Anzahl der gleichzeitig übertragenen Datenpakete an. Je größer das Fenster, desto mehr Daten können gleichzeitig übertragen werden, und desto höher ist die Übertragungsgeschwindigkeit. Ein zu großes Fenster kann jedoch zu Netzwerküberlastung führen, die Paketverlustrate erhöhen und die Anzahl der Datenwiederholungen steigern, was die Übertragungsgeschwindigkeit verringert. Daher muss das Sende-Fenster kontinuierlich an die Netzwerkbedingungen angepasst werden, um sich allmählich dem Optimum anzunähern. Der Code zum Sende-Fenster in KCP:

<details>
<summary> Sendefenster (klicken Sie hier, um den Code zu erweitern) </summary>
```cpp
ikcpcb* ikcp_create(IUINT32 conv, void *user)
{
    // ...
// snd_wnd, rcv_wnd - Größe der Sendepuffer und Empfangspuffer
    kcp->snd_wnd = IKCP_WND_SND;    // 32
    kcp->rcv_wnd = IKCP_WND_RCV;    // 128
// Empfangsfenstergröße des Gegenendpunkts              // 128
    kcp->rmt_wnd = IKCP_WND_RCV
// Initialize Send-Fenster cwnd auf 0
    kcp->cwnd = 0;
Übermitteln Sie die Größe des Fensterbytes, die zur Berechnung von cwnd verwendet wird.
    kcp->incr = 0
// Langsame Startschwelle, slow start threshold
    kcp->ssthresh = IKCP_THRESH_INIT;
// nocwnd ist ein konfigurierbarer Parameter, 1 berücksichtigt cwnd nicht
    kcp->nocwnd = 0;
    // ...
}

void ikcp_flush(ikcpcb *kcp)
{
    // ...
// Beim Senden von Daten wird zunächst die Größe des Sendefensters berechnet, die der kleinere Wert zwischen der Größe des Sendepuffers und der Größe des Empfangsfensters des anderen ist.
    cwnd = _imin_(kcp->snd_wnd, kcp->rmt_wnd);
Bei der Betrachtung muss auch kcp->cwnd berücksichtigt werden, das die ständig aktualisierten Sendefenster beinhaltet.
    if (kcp->nocwnd == 0) cwnd = _imin_(kcp->cwnd, cwnd);

Basierend auf der Größe von cwnd wird die snd_queue in das snd_buf verschoben.
    while (_itimediff(kcp->snd_nxt, kcp->snd_una + cwnd) < 0) {
    }
// Daten senden
    resent = (kcp->fastresend > 0)? (IUINT32)kcp->fastresend : 0xffffffff;
// Auslösen einer Timeout-Wiederübertragung lost = 1
// Schnelles Retransmit auslösen change++

// Aktualisierung der langsamen Startgrenze und des Sendefensters
    if (change) {
// Wenn eine schnelle Wiederübertragung ausgelöst wird, wird ssthresh auf die Hälfte der Anzahl der momentan im Netzwerk übertragenen Pakete gesetzt.
        IUINT32 inflight = kcp->snd_nxt - kcp->snd_una;
        kcp->ssthresh = inflight / 2;
        if (kcp->ssthresh < IKCP_THRESH_MIN)
            kcp->ssthresh = IKCP_THRESH_MIN;

// Das Senden des Fensters ist gleich dem Schwellenwert plus der mit schnellem Wiederaufbau zusammenhängenden erneuten Sendung.
        kcp->cwnd = kcp->ssthresh + resent;
        kcp->incr = kcp->cwnd * kcp->mss;
    }

    if (lost) {
Wenn es zu Timeout-Wiederholungen kommt, wird die Slow-Start ausgelöst, wobei der ssthresh-Schwellenwert auf die Hälfte des Sendefensters gesetzt wird.
        kcp->ssthresh = cwnd / 2;
        if (kcp->ssthresh < IKCP_THRESH_MIN)
            kcp->ssthresh = IKCP_THRESH_MIN;
// Das Sende-Fenster zurück auf 1, langsam wieder hochfahren
        kcp->cwnd = 1;
        kcp->incr = kcp->mss;
    }

    if (kcp->cwnd < 1) {
// Da es auf 0 initialisiert ist, wird es hier auf 1 gesetzt.
        kcp->cwnd = 1;
        kcp->incr = kcp->mss;
    }
}

int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    IUINT32 prev_una = kcp->snd_una;
Verarbeite die empfangenen Daten.

    while (1) {
        // ...
        data = ikcp_decode16u(data, &wnd)
// rmt_wnd is the size of the receiving window on the other side
        kcp->rmt_wnd = wnd
        // ...
// Daten verarbeiten
    }

Letzte Aktualisierung des Sendefensters
kcp->snd_una - prev_una > 0 bedeutet, dass bei diesem Input ACK empfangen wurde und der Sendepuffer snd_buf geändert wurde.
    if (_itimediff(kcp->snd_una, prev_una) > 0) {
// Erneute Überprüfung des Empfangsfensters der anderen Partei
        if (kcp->cwnd < kcp->rmt_wnd) {
            IUINT32 mss = kcp->mss;

            if (kcp->cwnd < kcp->ssthresh) {
// Unter dem langsamen Startschwellenwert, doppelte Steigerung
                kcp->cwnd++;
                kcp->incr += mss;

            }    else {
Nach Überschreiten des Schwellenwerts für die langsamen Start wird 'incr' gemäß der Formel aktualisiert, um dann 'cwnd' zu berechnen.
                if (kcp->incr < mss) kcp->incr = mss;
                kcp->incr += (mss * mss) / kcp->incr + (mss / 16);
                if ((kcp->cwnd + 1) * mss <= kcp->incr) {
                    kcp->cwnd++;
                }
            }
// Die aktualisierten Werte müssen noch mit rmt_wnd verglichen werden.
            if (kcp->cwnd > kcp->rmt_wnd) {
                kcp->cwnd = kcp->rmt_wnd;
                kcp->incr = kcp->rmt_wnd * mss;
            }
        }
    }
}
```
</details>

Die Berechnung der Größe des Sendefensters `kcp->cwnd` erfordert etwas mehr Code, da beim Senden und Empfangen von Daten Aktualisierungen erforderlich sind. `kcp->cwnd` wird mit 0 initialisiert.
Bei der ersten Aufruf von `ikcp_flush` wird überprüft, ob es kleiner als 1 ist, und dann auf 1 geändert. Anschließend sendet der Absender entsprechend der Größe des Sendefensters eine entsprechende Anzahl von Datenpaketen und wartet auf die Bestätigung (ACK).
Respond package. ACK packets are processed in `kcp->input`. If an ACK packet is detected in `kcp->input` and there is a clearing of the sent data packets in the sending buffer, it means that a data packet has been successfully delivered, and `kcp->cwnd++` is executed. In reality, it is highly likely that each execution of `kcp->input` processes only one ACK packet. It can be understood that every time an ACK packet is received, `kcp->cwnd++` is executed, and this increment operation achieves a doubling effect. For example, if `kcp->cwnd = 2` currently, and two data packets are sent and two ACK packets are received, triggering two increment operations, the final result will be `kcp->cwnd = 4`, a doubling.

Die `cwnd` kann exponentiell wachsen, bis sie den Schwellenwert für den langsamen Start überschreitet oder es zu einer Congestion Time-out-Retransmission oder einer Fast Retransmission kommt. Nach einer Timeout-Retransmission wird der Slow-Start ausgelöste, wobei der Schwellenwert für den langsamen Start `ssthresh = kcp->cwnd / 2` beträgt, das Sendefenster `kcp->cwnd = 1` ist und das exponentielle Wachstum von Neuem beginnt. Bei einer Fast Retransmission reduziert KCP zunächst vorzeitig `ssthresh`, was bedeutet, dass der Raum für das exponentielle Wachstum von `cwnd` verringert wird, die Wachstumsgeschwindigkeit verringert wird und eine vorzeitige Verlangsamung der Congestion eintritt.

KCP hat auch eine Konfiguration namens `nocwnd` hinzugefügt. Wenn `nocwnd = 1` ist, wird bei der Datenübertragung die Größe des Sendefensters nicht mehr berücksichtigt, wodurch die maximal mögliche Anzahl an Datenpaketen direkt gesendet wird, um die Anforderungen des Hochgeschwindigkeitsmodus zu erfüllen.

##Zusammenfassung.

Der Text analysiert kurz den Quellcode von KCP und diskutiert die Implementierung von ARQ auf KCP sowie einige Strategien zur Steigerung der Datenübertragungsrate von KCP. Es gibt viele Details, die hier nicht erwähnt wurden. Wer Interesse hat, kann den Quellcode von KCP selbst überprüfen und vergleichen, ich bin sicher, es wird viele Erkenntnisse bringen.

--8<-- "footer_de.md"


> Dieser Beitrag wurde mit ChatGPT übersetzt, bitte in [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Bitte weisen Sie auf alle fehlenden Punkte hin. 
