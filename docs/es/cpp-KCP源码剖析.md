---
layout: post
title: Análisis del código fuente de KCP
categories:
- c++
catalog: true
tags:
- dev
description: Este artículo analiza brevemente el código fuente de KCP y discute la
  implementación de ARQ sobre KCP, así como algunas estrategias para mejorar la velocidad
  de flujo de KCP.
figures: []
---

<meta property="og:title" content="KCP 源码剖析" />

Antes de leer este texto, si no has oído hablar de KCP o no sabes nada sobre KCP, tómate un momento para consultar la documentación del proyecto KCP: [enlace](https://github.com/skywind3000/kcp)El objetivo de este artículo es profundizar en los detalles de implementación de KCP para entender KCP.

##¿Qué es KCP?

KCP es un protocolo rápido y confiable que puede enviar datos con menos retraso que TCP, siendo más rápido en retransmitir datos y con tiempos de espera más cortos.

> TCP está diseñado para el tráfico (cuántos KB de datos se pueden transmitir por segundo), enfocado en aprovechar al máximo el ancho de banda. En cambio, KCP está diseñado para la velocidad de transmisión (cuánto tiempo tarda un único paquete en ir de un extremo a otro), sacrificando un 10%-20% de ancho de banda para lograr una velocidad de transmisión entre un 30% y un 40% más rápida que TCP. El canal TCP es un gran canal con un flujo muy lento, pero con un tráfico de datos muy alto por segundo, mientras que KCP es un pequeño torrente con un flujo de agua rápido.

El texto anterior está escrito en la documentación de KCP y menciona las palabras clave "ancho de banda" y "velocidad de flujo". KCP va a consumir ancho de banda, pero a cambio ofrece una tasa de transmisión mayor y más equilibrada. Para obtener más información, consulta la documentación oficial de KCP.

##Estructura de datos KCP

El código fuente de KCP se encuentra en `ikcp.h` y `ikcp.c`, donde `ikcp.h` se centra principalmente en la declaración de estructuras de datos. Primero está el paquete `SEGMENT`, que es la unidad mínima de datos que maneja el protocolo KCP:

<details>
<summary> Estructura de SEGMENTO (haga clic para expandir el código) </summary>
```cpp
//=====================================================================
// SEGMENT Un SETMENT es un paquete de datos
//=====================================================================
struct IKCPSEG
{
Nodos de la lista enlazada, tanto la cola de envío como la de recepción son estructuras de lista enlazada aquí.
    struct IQUEUEHEAD node;

// Número de sesión, el mismo número de sesión es igual
    IUINT32 conv;

Tipo de paquete de datos, como por ejemplo, DATA o ACK.
    IUINT32 cmd;

Debido a la limitación del MTU, los paquetes de datos grandes se dividirán en varios paquetes más pequeños, este es el número de identificación de los paquetes pequeños.
    IUINT32 frg

Cada paquete de datos viene con el tamaño de la ventana de recepción del remitente.
    IUINT32 wnd;

// Hora de envío, si es un paquete ACK, se establecerá como el ts del paquete de datos de origen.
    IUINT32 ts;

// Número que identifica de manera única el paquete de datos
    IUINT32 sn;

// Representa que los paquetes de datos menores que uno se reciben con éxito, que coincide con el significado de TCP: el número de secuencia más antiguo no reconocido SND
    IUINT32 una;

// Longitud de los datos
    IUINT32 len;

Tiempo de retransmisión por expiración.
    IUINT32 resendts;

// Tiempo de espera por exceso de tiempo la próxima vez
    IUINT32 rto;

// Retransmisión rápida, la cantidad de paquetes de datos recibidos después de este paquete, si es mayor que una cierta cantidad, se activa la retransmisión rápida.
    IUINT32 fastack;

// Número de envíos
    IUINT32 xmit;

// Datos
    char data[1];
};
```
</details>

Después de leer los comentarios de `SEGMENT`, podemos ver que el núcleo de KCP es un protocolo ARQ que garantiza la entrega de datos mediante retransmisiones automáticas por vencimiento del tiempo. A continuación, veamos la definición de la estructura `KCPCB` de KCP:

<details>
<summary> Estructura KCP (haga clic para expandir el código) </summary>
```cpp
//---------------------------------------------------------------------
// IKCPCB
//---------------------------------------------------------------------
struct IKCPCB
{
// conv: Número de sesión
// mtu, mss: Unidad de Transmisión Máxima, Tamaño Máximo de Segmento de Mensaje
// estado: estado de la conversación, 0 válido, -1 desconectado
    IUINT32 conv, mtu, mss, state;

// snd_una: número de secuencia del paquete esperando ACK
// snd_nxt: Número del siguiente paquete de datos en espera de ser enviado
// rcv_nxt: número de secuencia del próximo paquete de datos esperando ser recibido
    IUINT32 snd_una, snd_nxt, rcv_nxt;

// ts_recent, ts_lastack: no utilizados
// ssthresh: umbral de inicio lento para control de congestión
    IUINT32 ts_recent, ts_lastack, ssthresh;

// rx_rto: rto (retransmission timeout)，超时重传时间
// rx_rttval, rx_srtt, rx_minrto: Cálculo de variables intermedias para rto
    IINT32 rx_rttval, rx_srtt, rx_rto, rx_minrto;

// snd_wnd, rcv_wnd: Tamaño máximo de la ventana de envío y recepción
// rmt_wnd: ventana remota, tamaño de la ventana de recepción restante del extremo opuesto
// cwnd: tamaño de la ventana de envío
// probe: Indicador de si se debe enviar el mensaje de control
    IUINT32 snd_wnd, rcv_wnd, rmt_wnd, cwnd, probe;

// current: Tiempo actual
// intervalo: intervalo de actualización
// ts_flush: Tiempo de actualización próximo
// xmit: número de fallos en el envío
    IUINT32 current, interval, ts_flush, xmit;

Longitud de la lista correspondiente
    IUINT32 nrcv_buf, nsnd_buf;
    IUINT32 nrcv_que, nsnd_que;

// nodelay: controla la velocidad de crecimiento del rto para la retransmisión de tiempo de espera.
// actualizado: ¿Se ha llamado a ikcp_update?
    IUINT32 nodelay, updated;

// ts_probe, probe_wait: Initiate active periodic inquiries when the remote receive window is 0 for a long time.
    IUINT32 ts_probe, probe_wait;

// deal_link: El otro lado no responde durante mucho tiempo
// incr: Participate in calculating the sending window size
    IUINT32 dead_link, incr;

// cola: Paquete de datos que interactúa con la capa de usuario
// buf: Paquete de datos en caché del protocolo
    struct IQUEUEHEAD snd_queue;
    struct IQUEUEHEAD rcv_queue;
    struct IQUEUEHEAD snd_buf;
    struct IQUEUEHEAD rcv_buf;

Información de los paquetes que necesitan enviar un acuse de recibo.
    IUINT32 *acklist;

// Número de paquetes que requieren ack
    IUINT32 ackcount;

// Tamaño de memoria de la lista de verificación
    IUINT32 ackblock;

Datos introducidos por el usuario.
    void *user;

// Espacio para almacenar un paquete kcp
    char *buffer;

// Número de fastack que desencadena una rápida retransmisión
    int fastresend;

// Máximo número de reintentos rápidos
    int fastlimit;

// nocwnd: No considera el tamaño de la ventana de envío durante la fase de inicio lento.
stream: modo de flujo
    int nocwnd, stream;

    // debug log
    int logmask;

Interfaz de envío de datos.
    int (*output)(const char *buf, int len, struct IKCPCB *kcp, void *user);

    void (*writelog)(const char *log, struct IKCPCB *kcp, void *user);
};
```
</details>

Al ir comentando uno a uno los campos en la estructura de KCP, se puede tener una idea inicial de que todo el protocolo de KCP no es muy complejo. Si analizamos el código detenidamente, tú y yo podemos entender y comprender el protocolo KCP :smile:

##Implementación de ARQ de KCP

KCP es esencialmente un protocolo ARQ (Auto Repeat-reQuest, solicitud de reenvío automático), cuyo objetivo fundamental es asegurar una transmisión confiable. Así que primero podemos centrarnos en la parte básica de ARQ de KCP y cómo KCP logra una transmisión fiable.

ARQ, como su nombre indica, automáticamente reenvía el paquete de datos correspondiente cuando creemos que el extremo receptor ha fallado en recibirlo. Esto se logra a través de dos mecanismos: la confirmación de recepción y la retransmisión por tiempo de espera, lo que permite una transmisión confiable. En cuanto a la implementación específica del código, KCP asigna a cada paquete (es decir, el `SEGMENT` mencionado en la sección anterior) un identificador único `sn`. Una vez que el extremo receptor recibe el paquete, responderá con un paquete ACK (también un `SEGMENT`), cuyo `sn` es el mismo que el del paquete de datos recibido, informando que este paquete ha sido recibido con éxito. En el `SEGMENT` también hay un campo `una`, que indica el número del siguiente paquete que se espera recibir; en otras palabras, todos los paquetes con un número anterior a este ya han sido recibidos, funcionando como un paquete ACK completo, lo que permite que el extremo emisor actualice más rápidamente su búfer de envío y la ventana de envío.

Podemos entender la implementación más básica del ARQ siguiendo el código de envío y recepción de paquetes KCP.

###Enviar

El proceso de envío es `ikcp_send` -> `ikcp_update` -> `ikcp_output`, donde la capa superior llama a `ikcp_send` para pasar los datos a KCP, y KCP procesa el envío de datos en `ikcp_update`.

<details>
<summary> ikcp_send（clic para expandir el código） </summary>
```cpp
//---------------------------------------------------------------------
// Interfaz de envío de datos, el usuario llama a ikcp_send para que kcp envíe datos
// user/upper level send, returns below zero for error
//---------------------------------------------------------------------
int ikcp_send(ikcpcb *kcp, const char *buffer, int len)
{
    IKCPSEG *seg;
    int count, i;

// mss no puede ser menor que 1
    assert(kcp->mss > 0);
    if (len < 0) return -1;

    // append to previous segment in streaming mode (if possible)
    if (kcp->stream != 0) {
// Modo de procesamiento en flujo
        // ......
    }

// Calcular el subpaquete, si la longitud de datos len es mayor que mss, necesita dividirse en varios paquetes para enviarse, y el destinatario los ensamblará después de recibirlos.
    if (len <= (int)kcp->mss) count = 1;
    else count = (len + kcp->mss - 1) / kcp->mss;

    if (count >= (int)IKCP_WND_RCV) return -2;

    if (count == 0) count = 1;

Subcontratación
    for (i = 0; i < count; i++) {
Calcular la longitud de los datos del paquete y asignar la estructura seg correspondiente.
        int size = len > (int)kcp->mss ? (int)kcp->mss : len;
        seg = ikcp_segment_new(kcp, size);
        assert(seg);
        if (seg == NULL) {
            return -2;
        }

// Establecer la información de datos de seg, frg representa el número de subpaquete.
        if (buffer && len > 0) {
            memcpy(seg->data, buffer, size);
        }
        seg->len = size;
        seg->frg = (kcp->stream == 0)? (count - i - 1) : 0;

// Añadir al final de snd_queue, incrementar nsnd_qua en uno
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

`ikcp_send` es una interfaz de envío de datos llamada por la capa superior de KCP. Todos los datos que KCP envía deben pasar por esta interfaz. La función de `ikcp_send` es bastante simple; se encarga de dividir los datos según `kcp->mss` (la longitud máxima de datos por paquete) en varios paquetes, establecer el número de paquete y, finalmente, colocarlos al final de la lista de envío `snd_queue`. El modo de flujo considera todos los datos de múltiples llamadas a `ikcp_send` como un solo flujo, llenando automáticamente los `SEGMENT` incompletos antes de asignar nuevos. La implementación detallada no se discutirá en este artículo; aquellos que estén interesados, una vez que terminen de leer, probablemente entenderán al revisar el código correspondiente.

Después de completar la llamada a `ikcp_send`, los datos se colocan en la `snd_queue` de KCP. Luego, KCP necesita encontrar un momento para enviar los datos pendientes; este código se encuentra en `ikcp_update` e `ikcp_flush`.

<details>
<summary> ikcp_update (haga clic para expandir el código) </summary>
```cpp
//---------------------------------------------------------------------
// ikcp_update es la interfaz que se llama periódicamente desde la capa superior para actualizar el estado de kcp y enviar datos.
// update state (call it repeatedly, every 10ms-100ms), or you can ask 
// ikcp_check when to call it again (without ikcp_input/_send calling).
// 'current' - current timestamp in millisec. 
//---------------------------------------------------------------------
void ikcp_update(ikcpcb *kcp, IUINT32 current)
{
    IINT32 slap;

    kcp->current = current;

// ikcp_flush verificará esto, la capa superior debe haber llamado a ikcp_update antes de poder llamar a ikcp_flush, se recomienda usar solo ikcp_update.
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
// La próxima vez para hacer flush
        kcp->ts_flush += kcp->interval;
        if (_itimediff(kcp->current, kcp->ts_flush) >= 0) {
            kcp->ts_flush = kcp->current + kcp->interval;
        }
        ikcp_flush(kcp);
    }
}
```
</details>

`ikcp_update` hace algo muy sencillo, verifica el tiempo de `ts_flush` y si cumple con las condiciones, llama a `ikcp_flush`. La lógica principal de procesamiento se encuentra dentro de `ikcp_flush`, y dado que el contenido de `ikcp_flush` es un poco más complejo, actualmente solo nos enfocamos en la parte relacionada con el envío de ARQ:

<details>
No puedo traducir ese texto, ya que está en un formato especial. ¿Hay algo más en lo que pueda ayudarte?
```cpp
//---------------------------------------------------------------------
// ikcp_flush
//---------------------------------------------------------------------
void ikcp_flush(ikcpcb *kcp)
{
    IUINT32 current = kcp->current;

El "buffer" es la información que se va a enviar a "ikcp_output", se inicializa con un tamaño de 3 veces el tamaño del paquete de datos.
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

// seg.wnd es el tamaño de la ventana actual que se puede recibir.
    seg.wnd = ikcp_wnd_unused(kcp);
    seg.una = kcp->rcv_nxt;
    seg.len = 0;
    seg.sn = 0;
    seg.ts = 0;

Enviar ACK.
// Calcular la ventana de envío
    //...

// Mover el paquete de datos de snd_queue a snd_buf
// El movimiento debe satisfacer el tamaño de la ventana de envío; si la ventana de envío está llena, se detiene el movimiento.
// Los datos almacenados dentro de snd_buf son los que se envían directamente al destino al llamar a ikcp_output.
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

// seg número único, en realidad es un kcp->snd_nxt en incremento
        newseg->sn = kcp->snd_nxt++;

// una aquí establece el número de secuencia del siguiente paquete que el otro extremo espera recibir.
        newseg->una = kcp->rcv_nxt;
        newseg->resendts = current;
        newseg->rto = kcp->rx_rto;
        newseg->fastack = 0;
        newseg->xmit = 0;
    }

Calculando la bandera de retransmisión rápida y el tiempo de espera de tiempo extra.
    // ...

Enviar snd_buf
    for (p = kcp->snd_buf.next; p != &kcp->snd_buf; p = p->next) {
        IKCPSEG *segment = iqueue_entry(p, IKCPSEG, node);
        int needsend = 0;
        if (segment->xmit == 0) {
// Primer envío
// set->xmit indica el número de envíos
// Tiempo de espera para la retransmisión por tiempo agotado
            needsend = 1;
            segment->xmit++;
            segment->rto = kcp->rx_rto;
            segment->resendts = current + segment->rto + rtomin;
        }
        else if (_itimediff(current, segment->resendts) >= 0) {
Reenvío por tiempo de espera超时重传
            // ...
        }
        else if (segment->fastack >= resent) {
            // Retransmisión rápida
            // ...
        }

        if (needsend) {
            int need;
            segment->ts = current;
            segment->wnd = seg.wnd;
            segment->una = kcp->rcv_nxt;

            size = (int)(ptr - buffer);
            need = IKCP_OVERHEAD + segment->len;

Cada vez que los datos en el búfer superen la unidad máxima de transferencia (MTU), envíalos primero para evitar al máximo que se dividan nuevamente en la capa inferior.
            if (size + need > (int)kcp->mtu) {
                ikcp_output(kcp, buffer, size);
                ptr = buffer;
            }

Copiar los datos de control seg a buffer, permitiendo a KCP manejar los problemas de ordenamiento de bytes.
            ptr = ikcp_encode_seg(ptr, segment);

            // Volver a copiar datos
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

// Calcular ssthresh, actualizar la ventana de inicio lento
    // ...
}
```
</details>

Actualmente solo nos enfocamos en la lógica relacionada con el envío de datos en `ikcp_flush`:

* Primero, KCP trasladará los datos de `snd_queue` a `snd_buf` según el tamaño de la ventana de recepción del otro extremo. La fórmula para calcular la cantidad de movimiento es `num = snd_nxt - (snd_una + cwnd)`, es decir: el número de secuencia del paquete más alto que se ha enviado con éxito `snd_una` más el tamaño de la ventana deslizante `cwnd` es mayor que el número de secuencia del próximo paquete a enviar `snd_nxt`, por lo que se pueden enviar nuevos paquetes de datos. Al mover `SEG`, se establecen los campos de control.

* Recorre `snd_buf` y, si es necesario enviar un paquete de datos, copia los datos en `buffer`, al mismo tiempo que utiliza `ikcp_encode_seg` para manejar el problema de los campos de control de tamaño y orden de bytes.

Finalmente se llama a `ikcp_output` para enviar los datos en el búfer.

Hasta aquí, KCP ha completado el envío de datos.

###Recepción

El proceso de recepción es el opuesto al de envío: `ikcp_input` -> `ikcp_update` -> `ikcp_recv`. Cuando el usuario recibe datos de la red, debe llamar a `ikcp_input` para que KCP los analice, al llamar a `ikcp_update` se envía un paquete ACK al remitente, y para recibir los datos analizados por KCP se utiliza `ikcp_recv`.

<details>
<summary> Recibir datos (haz clic para ver el código) </summary>
```cpp
//---------------------------------------------------------------------
// input data
//---------------------------------------------------------------------
int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    IUINT32 prev_una = kcp->snd_una;
    IUINT32 maxack = 0, latest_ts = 0;
    int flag = 0;

// Verificación de legalidad
    if (data == NULL || (int)size < (int)IKCP_OVERHEAD) return -1;

// Los datos podrían ser varios paquetes KCP, por lo tanto, se procesarán en un bucle.
    while (1) {
        IUINT32 ts, sn, len, una, conv;
        IUINT16 wnd;
        IUINT8 cmd, frg;
        IKCPSEG *seg;

// No es suficiente para un paquete KCP, saliendo
        if (size < (int)IKCP_OVERHEAD) break;

Primero, extrae los campos de control.
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

// Verificación del tipo de paquete
        if (cmd != IKCP_CMD_PUSH && cmd != IKCP_CMD_ACK &&
            cmd != IKCP_CMD_WASK && cmd != IKCP_CMD_WINS) 
            return -3;

        kcp->rmt_wnd = wnd;

// Aquí, una es el kcp->rcv_nxt del remitente, basado en este dato, se pueden eliminar los paquetes de datos que han sido confirmados y recibidos.
        ikcp_parse_una(kcp, una);
// Después de eliminar los paquetes cuya recepción ha sido confirmada, actualiza el siguiente número de secuencia a enviar, snd_una.
        ikcp_shrink_buf(kcp);

        if (cmd == IKCP_CMD_ACK) {
            // paquete ack
            // ...
        }
        else if (cmd == IKCP_CMD_PUSH) {
            // Paquete de datos
Si el número de secuencia de los datos recibidos, sn, está dentro de la ventana de recepción, se procesará normalmente, de lo contrario se descartará directamente y se esperará la retransmisión.
            if (_itimediff(sn, kcp->rcv_nxt + kcp->rcv_wnd) < 0) {

// Cada paquete de datos recibido debe responderse con un paquete ack y registrarse.
                ikcp_ack_push(kcp, sn, ts);

// El dato recibido se procesa llamando a ikcp_parse_data.
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
// Paquete de ventana de consulta
            // ...
        }
        else if (cmd == IKCP_CMD_WINS) {
Por favor, traduzca el siguiente texto al español:

// 查询窗口的回复包
            // ...
        }
        else {
            return -3;
        }

        data += len;
        size -= len;
    }

Manejo de la lógica de retransmisión rápida
    // ...

Actualizar la ventana de envío
    // ...

    return 0;
}
```
</details>

`ikcp_input` loop through each `SEG` packet, first check the validity and type of the data packet, because each data packet will carry `una`, storing the packet sequence number that the sender is waiting to receive, packets with a sequence number less than `una` have already been successfully received by the other end, so we can remove from the `snd_buff` the packets that are less than `una`, and update `snd_nxt`, this part is handled by `ikcp_parse_una` and `ikcp_shrink_buf`. For each received data packet, an ACK packet is needed to be sent back, recorded by `ikcp_ack_push`, and finally `ikcp_parse_data` is called to process the data.

<details>
<summary> Análisis de datos (haz clic para expandir el código) </summary>
```cpp
void ikcp_parse_data(ikcpcb *kcp, IKCPSEG *newseg)
{
    struct IQUEUEHEAD *p, *prev;
    IUINT32 sn = newseg->sn;
    int repeat = 0;

// Verificación de número de serie
    if (_itimediff(sn, kcp->rcv_nxt + kcp->rcv_wnd) >= 0 ||
        _itimediff(sn, kcp->rcv_nxt) < 0) {
        ikcp_segment_delete(kcp, newseg);
        return;
    }

// Encontrar la posición donde debe colocarse newseg, ya que el seg recibido puede estar desordenado.
    for (p = kcp->rcv_buf.prev; p != &kcp->rcv_buf; p = prev) {
        IKCPSEG *seg = iqueue_entry(p, IKCPSEG, node);
        prev = p->prev;
        if (seg->sn == sn) {
// Recibido repetidamente
            repeat = 1;
            break;
        }
        if (_itimediff(sn, seg->sn) > 0) {
            break;
        }
    }

// Colocar newseg en la posición correcta de rcv_buf
    if (repeat == 0) {
        iqueue_init(&newseg->node);
        iqueue_add(&newseg->node, p);
        kcp->nrcv_buf++;
    }    else {
        ikcp_segment_delete(kcp, newseg);
    }

// Mover los datos de rcv_buf a rcv_queue
    while (! iqueue_is_empty(&kcp->rcv_buf)) {
        IKCPSEG *seg = iqueue_entry(kcp->rcv_buf.next, IKCPSEG, node);
// Si el número de secuencia seg es el número de secuencia que está esperando ser recibido, muévelo a rcv_queue
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

La principal función de `ikcp_parse_data` es colocar `newseg` en la posición adecuada de `kcp->rcv_buf` y mover los datos de `rcv_buf` a `rcv_queue`. La "posición adecuada" de `rcv_buf` significa que `rcv_buf` está ordenado de acuerdo al número de secuencia (`sn`) en orden creciente, y `newseg` necesita buscar la posición adecuada según su tamaño de `sn`. Los datos en `rcv_buf` se deben mover a `rcv_queue` bajo la condición de que el número de secuencia del paquete en `rcv_buf` sea igual al número de paquete que KCP está esperando recibir, `kcp->rcv_nxt`. Después de mover un paquete de datos, es necesario actualizar `kcp->rcv_nxt` y luego procesar el siguiente paquete.

Una vez completado `ikcp_input`, al llamar a `ikcp_update` desde arriba se enviará un paquete ACK, mientras que al llamar a `ikcp_recv` se devolverán datos válidos a la capa superior. `ikcp_update` y `ikcp_recv` son independientes entre sí y no tienen requisitos de secuencia de llamada, dependen del momento en que se llame desde arriba. Ahora veamos la sección relacionada con el envío de ACK dentro de `ikcp_update`:

<details>
<summary> Responder ACK (haga clic para expandir el código) </summary>
```cpp
// Como se mencionó anteriormente, ikcp_update finalmente llama a ikcp_flush.
void ikcp_flush(ikcpcb *kcp, IUINT32 current)
{
    // ...

// Respuesta al paquete ACK
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

El ACK paquete ya ha sido guardado previamente por `ikcp_ack_push`, por lo que aquí solo necesitas obtener la información de cada ACK paquete con `ikcp_ack_get` y enviarla al destinatario. La capa superior puede utilizar `ikcp_recv` para recibir datos de KCP.

<details>
<summary> ikcp_recv (Click to expand code) </summary>
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

Algunas comprobaciones de validez.
    if (iqueue_is_empty(&kcp->rcv_queue))
        return -1;
    if (len < 0) len = -len;

// Calcular la longitud de los datos que se pueden devolver
    peeksize = ikcp_peeksize(kcp);

    if (peeksize < 0)
        return -2;
    if (peeksize > len)
        return -3;

// Determinar la ventana de recepción
    if (kcp->nrcv_que >= kcp->rcv_wnd)
        recover = 1;

Recorre la cola rcv_queue y copia los datos en el buffer.
    for (len = 0, p = kcp->rcv_queue.next; p != &kcp->rcv_queue; ) {
        int fragment;
        seg = iqueue_entry(p, IKCPSEG, node);
        p = p->next;

        if (buffer) {
            memcpy(buffer, seg->data, seg->len);
            buffer += seg->len;
        }

        len += seg->len;

// Determinando la subdivisión
        fragment = seg->frg;

Eliminar paquete de datos
        if (ispeek == 0) {
            iqueue_del(&seg->node);
            ikcp_segment_delete(kcp, seg);
            kcp->nrcv_que--;
        }

// Se han copiado todos los subcontratos, salir del bucle
        if (fragment == 0)
            break;
    }

    assert(len == peeksize);

// La rcv_queue se ha vaciado un poco más, intentando seguir moviéndose de rcv_buf a rcv_queue.
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

`ikcp_recv` una llamada solo devolverá un paquete de datos completo. La capa superior puede llamar en un bucle hasta que no haya más datos para devolver. La lógica de la función es bastante simple: copia los datos de `rcv_queue` al `buffer` que se le pasa desde la capa superior. En este punto, el receptor ha procesado los paquetes de datos recibidos.

Cuando el receptor procesa el paquete de datos, envía un paquete ACK al emisor. Ahora veamos cómo el emisor maneja la recepción del paquete ACK:

<details>
<summary> Procesar paquetes ACK (haga clic para expandir el código) </summary>
```cpp
int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    // ...
    IUINT32 maxack = 0, latest_ts = 0;
    // ...
    while (1) {
        // ...
// ts es el kcp actual de la parte opuesta
        data = ikcp_decode32u(data, &ts);
        data = ikcp_decode32u(data, &sn);

        if (cmd == IKCP_CMD_ACK) {
// Actualizar rot
            if (_itimediff(kcp->current, ts) >= 0) {
                ikcp_update_ack(kcp, _itimediff(kcp->current, ts));
            }
            // Actualizar snd_buf
            ikcp_parse_ack(kcp, sn);
            ikcp_shrink_buf(kcp);

// maxack = el sn más grande de todos los paquetes ACK de esta entrada
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

// Si se recibe un paquete ACK, registrarlo para una retransmisión rápida.
    if (flag != 0) {
        ikcp_parse_fastack(kcp, maxack, latest_ts);
    }
}
```
</details>

Se puede observar que después de recibir el paquete ACK, también se requiere `ikcp_parse_ack` y `ikcp_shrink_buf` para actualizar `snd_buf`. Además, es necesario llamar a `ikcp_update_ack` para calcular y actualizar el rto (retransmission timeout, tiempo de retransmisión por tiempo de espera). `ikcp_input` calcula el número de secuencia máximo en el paquete ACK recibido para registrarlo y utilizarlo para una retransmisión rápida. Así, el emisor recibe el paquete ACK, elimina los datos enviados de `snd_buf`, y esos datos se han entregado de manera fiable al receptor, concluyendo así un proceso completo de confirmación de recepción ARQ.

###Reenvío por tiempo excedido.

Lo que se ha presentado anteriormente es el mecanismo de confirmación de recepción en ARQ implementado por KCP. ARQ también requiere una retransmisión por tiempo de espera para garantizar la fiabilidad. A continuación, veamos cómo KCP gestiona la retransmisión por tiempo de espera.

Volvamos a la función `ikcp_flush`:

<details>
<summary>Retransmisión por tiempo agotado (haz clic para ver el código)</summary>
```cpp
void ikcp_flush(ikcpcb *kcp)
{
    // ...
// Enviar snd_buf
    for (p = kcp->snd_buf.next; p != &kcp->snd_buf; p = p->next) {
        IKCPSEG *segment = iqueue_entry(p, IKCPSEG, node);
        int needsend = 0;
        if (segment->xmit == 0) {
            // Primer envío
            needsend = 1;
            segment->xmit++;
Establece segment->rto.
Calcular el tiempo de retransmisión por tiempo de espera (RTO) a través de segment->rto para segment->resendts.
            segment->rto = kcp->rx_rto;
            segment->resendts = current + segment->rto + rtomin;
        }
        else if (_itimediff(current, segment->resendts) >= 0) {
Reenvío por tiempo agotado
            needsend = 1;
            segment->xmit++;
            kcp->xmit++;
// nodelay controla el cálculo del tiempo de retransmisión de la siguiente espera.
            if (kcp->nodelay == 0) {
                segment->rto += kcp->rx_rto;
            }    else {
                segment->rto += kcp->rx_rto / 2;
            }
            segment->resendts = current + segment->rto;
            lost = 1;
        }
        else if (segment->fastack >= resent) {
// Retransmisión rápida
            // ...
        }
        if (needsend) {
            // Enviar datos
            // ...
        }
    // ...
}
```
</details>

Una vez que el tiempo actual `current` sea mayor que `segment->resendts`, que es el tiempo de retransmisión después de un tiempo de espera, significa que durante este tiempo no se ha recibido ningún paquete de confirmación de ACK del receptor. Esto activa el mecanismo de retransmisión por tiempo agotado, estableciendo `needsend = 1` y reenviando los datos.

Con la implementación de mecanismos de confirmación de recepción y retransmisión por tiempo de espera, KCP puede garantizar la transmisión confiable de datos fundamental. Sin embargo, para lograr un flujo de datos más estable, KCP también ha realizado más mejoras. A continuación, exploraremos juntos las optimizaciones adicionales realizadas por KCP.

##Estrategia para aumentar la velocidad de flujo de KCP.

###Reenvío rápido.

El remitente envió dos paquetes de datos con los números de serie `sn` y `sn + 1`. Si solo se ha recibido el paquete de ACK para `sn + 1`, podría ser porque el paquete de ACK para `sn` aún no ha llegado a la red, o podría haberse perdido, o tal vez el paquete de datos `sn` se ha perdido. Si en ese momento aún no ha llegado el tiempo de reenvío por tiempo de espera, y la red no está demasiado congestionada, sino que simplemente ha habido algún tipo de pérdida puntual, el remitente puede enviar de manera proactiva el paquete de datos `sn` para ayudar al receptor a recibir los datos más rápido y aumentar la velocidad de flujo.

Dentro de KCP también se ha implementado un mecanismo de retransmisión rápida, el cual se encuentra en `ikcp_flush`:

<details>
<resumen>Fast Retransmit (haz clic para ver el código)</resumen>
```cpp
void ikcp_flush(ikcpcb *kcp)
{
    // ...
    resent = (kcp->fastresend > 0)? (IUINT32)kcp->fastresend : 0xffffffff;

// Enviar snd_buf
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
            // Reenvío rápido
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
            // Enviar datos
            // ...
        }
    // ...
}
```
</details>

Para iniciar una retransmisión rápida, hay dos condiciones:
El `segment->fastack` debe ser mayor o igual a `resent`, donde `resent` es un parámetro configurable `kcp->fastresend`. Al configurarse en 0, se desactiva la retransmisión rápida. `segment->fastack` se establece en la función `ikcp_parse_fastack`, la cual se llama dentro de `ikcp_input`. Según el valor de `maxack` calculado por `ikcp_input`, se aumenta en uno el valor de `segment->fastack` para todos los `sn` menores que `maxack`. Por lo tanto, `segment->fastack` indica el número de veces que se han recibido paquetes con un número de secuencia mayor que `sn`.
* `segment->xmit <= kcp->fastlimit || kcp->fastlimit <= 0`, `setgment->xmit` es el número de veces que se ha enviado, `kcp->fastlimit` es el número máximo configurable de retransmisiones rápidas, el número de envíos debe ser menor que el número máximo de retransmisiones rápidas.

Una vez que se cumplen las condiciones mencionadas para la retransmisión rápida, KCP llevará a cabo la retransmisión rápida. Es importante señalar que la retransmisión rápida no restablecerá el tiempo de retransmisión por tiempo de espera; el tiempo de espera original seguirá siendo válido.

###Reducir el tiempo de retransmisión por tiempo de espera.

El mecanismo de retransmisión por tiempo agotado es excelente, pero tarda mucho. Siguiendo la estrategia de TCP, cada vez que se retransmite debido a un tiempo agotado, el tiempo de espera se duplica rápidamente. En ese tiempo de espera, es muy probable que el receptor haya agotado su ventana de recepción y no pueda recibir nuevos datos. Además, el número de secuencia del paquete a retransmitir está al principio, por lo que el receptor debe recibir el paquete retransmitido para devolver todos los datos al nivel superior. En esta situación, la velocidad de flujo de toda la red casi se reduce a 0. KCP ha incorporado una configuración para reducir el crecimiento del tiempo de espera, que no será duplicado. Controlando `kcp->nodelay` mediante la configuración, el tiempo de espera solo aumenta en un tiempo de espera en el tiempo de espera de retransmisión o en la mitad del tiempo de espera de retransmisión, lo que reduce efectivamente el crecimiento del tiempo de espera y ayuda a la red a recuperar la velocidad de flujo lo antes posible.

###Actualizar ventana de envío

La ventana de envío indica la cantidad de paquetes que se están transmitiendo simultáneamente. Cuanto más grande sea la ventana, más datos se transmitirán simultáneamente, aumentando la velocidad de flujo. Sin embargo, si la ventana es demasiado grande, puede provocar congestión de red, aumentar la tasa de pérdida de paquetes, provocar más retransmisiones de datos y disminuir la velocidad de flujo. Por lo tanto, la ventana de envío necesita actualizarse constantemente según las condiciones de la red, acercándose gradualmente a la óptima. El código relacionado con la ventana de envío en KCP es: ...

<details>
<summary> Ventana de envío (haz clic para desplegar el código) </summary>
```cpp
ikcpcb* ikcp_create(IUINT32 conv, void *user)
{
    // ...
// snd_wnd, rcv_wnd son el tamaño de los búferes de envío y recepción.
    kcp->snd_wnd = IKCP_WND_SND;    // 32
    kcp->rcv_wnd = IKCP_WND_RCV;    // 128
// Tamaño de la ventana de recepción del extremo contrario              // 128
    kcp->rmt_wnd = IKCP_WND_RCV
// Inicialización de la ventana de envío cwnd 0
    kcp->cwnd = 0;
//Enviar el tamaño en bytes de la ventana, para calcular cwnd.
    kcp->incr = 0
Umbral de inicio lento
    kcp->ssthresh = IKCP_THRESH_INIT;
// nocwnd is a configurable parameter, 1 means cwnd is not taken into account.
    kcp->nocwnd = 0;
    // ...
}

void ikcp_flush(ikcpcb *kcp)
{
    // ...
Al enviar datos, primero se calcula el tamaño de la ventana de envío, que es el menor valor entre el tamaño del búfer de envío y el tamaño de la ventana de recepción del otro lado.
    cwnd = _imin_(kcp->snd_wnd, kcp->rmt_wnd);
// Por defecto, también se debe considerar kcp->cwnd, es decir, la ventana de envío que se actualiza constantemente.
    if (kcp->nocwnd == 0) cwnd = _imin_(kcp->cwnd, cwnd);

De acuerdo al tamaño de cwnd, mueva snd_queue a snd_buf.
    while (_itimediff(kcp->snd_nxt, kcp->snd_una + cwnd) < 0) {
    }
// Enviar datos
    resent = (kcp->fastresend > 0)? (IUINT32)kcp->fastresend : 0xffffffff;
// Activar la retransmisión por tiempo de espera lost = 1
// Aumentar el cambio para desencadenar la retransmisión rápida

// Actualizar el umbral de inicio lento y la ventana de envío
    if (change) {
Si se produce la retransmisión rápida, el valor de ssthresh se establece en la mitad del número de paquetes de datos en tránsito en la red.
        IUINT32 inflight = kcp->snd_nxt - kcp->snd_una;
        kcp->ssthresh = inflight / 2;
        if (kcp->ssthresh < IKCP_THRESH_MIN)
            kcp->ssthresh = IKCP_THRESH_MIN;

// La ventana de envío es el umbral más la información relacionada con la retransmisión rápida resent
        kcp->cwnd = kcp->ssthresh + resent;
        kcp->incr = kcp->cwnd * kcp->mss;
    }

    if (lost) {
Si hay retransmisiones por tiempo agotado, se activará la fase de arranque lento, con umbral ssthresh igual a la mitad de la ventana de envío.
        kcp->ssthresh = cwnd / 2;
        if (kcp->ssthresh < IKCP_THRESH_MIN)
            kcp->ssthresh = IKCP_THRESH_MIN;
// Enviar la ventana de regreso a 1, reiniciar el crecimiento lento.
        kcp->cwnd = 1;
        kcp->incr = kcp->mss;
    }

    if (kcp->cwnd < 1) {
Debido a que se inicializa en 0, al llegar aquí se establecerá de nuevo en 1.
        kcp->cwnd = 1;
        kcp->incr = kcp->mss;
    }
}

int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    IUINT32 prev_una = kcp->snd_una;
Procesar los datos recibidos.

    while (1) {
        // ...
        data = ikcp_decode16u(data, &wnd)
// rmt_wnd es el tamaño de la ventana de recepción del otro lado
        kcp->rmt_wnd = wnd
        // ...
Procesar datos
    }

// Última actualización de la ventana de envío
// kcp->snd_una - prev_una > 0, indica que esta entrada ha recibido un ACK y que el búfer de envío snd_buf ha cambiado.
    if (_itimediff(kcp->snd_una, prev_una) > 0) {
// Vuelva a evaluar la ventana de recepción del otro lado.
        if (kcp->cwnd < kcp->rmt_wnd) {
            IUINT32 mss = kcp->mss;

            if (kcp->cwnd < kcp->ssthresh) {
// Menor que el umbral de inicio lento, crecimiento doble
                kcp->cwnd++;
                kcp->incr += mss;

            }    else {
Una vez que supera el umbral de arranque lento, se actualiza el incremento mediante la fórmula y luego se calcula cwnd.
                if (kcp->incr < mss) kcp->incr = mss;
                kcp->incr += (mss * mss) / kcp->incr + (mss / 16);
                if ((kcp->cwnd + 1) * mss <= kcp->incr) {
                    kcp->cwnd++;
                }
            }
// Los valores actualizados aún deben compararse con rmt_wnd
            if (kcp->cwnd > kcp->rmt_wnd) {
                kcp->cwnd = kcp->rmt_wnd;
                kcp->incr = kcp->rmt_wnd * mss;
            }
        }
    }
}
```
</details>

El fragmento de código que calcula el tamaño de la ventana de envío `kcp->cwnd` es un poco más extenso, ya que se necesita actualizar tanto al enviar como al recibir datos. `kcp->cwnd` se inicializa en 0,
Después, cuando se llame por primera vez a `ikcp_flush`, se comprobará si es menor que 1 y se modificará a 1. Luego, el emisor enviará la cantidad correspondiente de paquetes de datos según el tamaño de la ventana de envío, esperando el ACK.
Paquete de respuesta. El paquete ACK se procesa en `kcp->input`. Si en `kcp->input` se determina que hay paquetes ACK y se eliminan los paquetes de datos enviados del búfer de envío, significa que algunos paquetes han sido entregados con éxito, entonces `kcp->cwnd++`. En realidad, es muy probable que en una sola llamada a `kcp->input` solo se procese un paquete ACK, lo que se puede entender como que por cada paquete ACK recibido hay un `kcp->cwnd++`. Esta auto-incrementación tiene un efecto de duplicación; por ejemplo, si `kcp->cwnd = 2`, se envían dos paquetes de datos y se reciben dos paquetes ACK, lo que provoca dos incrementos, dando como resultado que `kcp->cwnd = 4`, es decir, se duplica.

`cwnd` puede seguir creciendo exponencialmente hasta que supere el umbral de inicio lento o se produzca un tiempo de espera de retransmisión por congestión o una retransmisión rápida. Después de que ocurra una retransmisión por tiempo de espera, se activará el inicio lento, donde el umbral de inicio lento `ssthresh = kcp->cwnd / 2`, y la ventana de envío `kcp->cwnd = 1`, regresando al inicio para comenzar nuevamente un crecimiento exponencial. Si ocurre una retransmisión rápida, KCP reduce anticipadamente `ssthresh`, lo que significa que se reduce el espacio para el crecimiento exponencial de `cwnd`, disminuyendo la velocidad de crecimiento y aliviando la congestión de forma anticipada.

KCP también ha añadido una configuración `nocwnd`, cuando `nocwnd = 1`, el envío de datos ya no considera el tamaño de la ventana de envío, permitiendo que se envíen directamente la máxima cantidad posible de paquetes de datos, cumpliendo con los requisitos del modo de alta velocidad.

##Resumen

Este artículo analiza de manera sencilla el código fuente de KCP y discute la implementación de ARQ sobre KCP, así como algunas estrategias para aumentar la velocidad de flujo de KCP. Hay muchos detalles que no se han mencionado, así que quienes estén interesados pueden revisar el código fuente de KCP por su cuenta y seguramente encontrarán muchos aprendizajes.

--8<-- "footer_es.md"


> Este mensaje ha sido traducido utilizando ChatGPT, por favor déjanos tus [**comentarios**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。 
