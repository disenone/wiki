---
layout: post
title: KCP Analysis of Source Code
categories:
- c++
catalog: true
tags:
- dev
description: Este texto analiza brevemente el código fuente de KCP y discute la implementación
  de ARQ en KCP, así como algunas estrategias para mejorar la velocidad de flujo en
  KCP.
figures: []
---

<meta property="og:title" content="KCP 源码剖析" />

Antes de leer este texto, si no has oído hablar de KCP o no sabes nada sobre KCP, te ruego que dediques un poco de tiempo a consultar la documentación del proyecto KCP: [Enlace](https://github.com/skywind3000/kcp)El propósito de este texto es profundizar en los detalles de implementación de KCP para comprender KCP.

##¿Qué es KCP?

KCP es un protocolo rápido y confiable que puede transmitir datos con una latencia más baja que TCP, con retransmisión de datos más rápida y tiempos de espera más cortos.

> TCP está diseñado para el flujo de tráfico (cuántos KB de datos se pueden transmitir por segundo), enfocándose en aprovechar al máximo el ancho de banda. Por otro lado, KCP está diseñado para la velocidad del flujo (cuánto tiempo se necesita para enviar un paquete de datos de un extremo a otro), a costa de desperdiciar entre un 10% y un 20% del ancho de banda para obtener una velocidad de transmisión un 30% a 40% más rápida que TCP. Un canal TCP es como un gran canal de navegación lento pero con un gran caudal de tráfico por segundo, mientras que KCP es como un pequeño arroyo con un flujo rápido y agitado.

La información anterior está escrita en la documentación de KCP, y las palabras clave son **ancho de banda** y **velocidad de flujo**. KCP consume ancho de banda, pero ofrece la ventaja de una velocidad de transmisión mayor y más equilibrada. Para obtener más información, consulte la documentación de KCP.

##KCP Estructura de datos

El código fuente de KCP se encuentra en `ikcp.h` e `ikcp.c`, el núcleo de `ikcp.h` es la declaración de las estructuras de datos. En primer lugar, está el paquete de datos `SEGMENT`, que es la unidad mínima de procesamiento de datos en el protocolo KCP:

<details>
<summary> ESTRUCTURA SEGMENTO (haga clic para mostrar el código) </summary>
```cpp
//=====================================================================
// SEGMENT 一个 SETMENT 就是一个数据包

// SEGMENT es simplemente un paquete de datos.
//=====================================================================
struct IKCPSEG
{
// 链表节点，发送和接受队列都是这里的链表的结构

    // Los nodos de la lista enlazada, tanto las colas de envío como las de recepción son estructuras de esta lista.
    struct IQUEUEHEAD node;

    // Número de sesión, el mismo número de sesión es igual
    IUINT32 conv;

    // Tipo de paquete, por ejemplo, DATA o ACK
    IUINT32 cmd;

    // Debido a la limitación del MTU, los paquetes de datos grandes se dividen en varios paquetes más pequeños, este es el número de paquete más pequeño
    IUINT32 frg

    // Cada paquete de datos lleva consigo el tamaño de la ventana de recepción del remitente
    IUINT32 wnd;

    // Tiempo de envío, si el paquete es un ACK, se establecerá como la marca de tiempo del paquete de origen.
    IUINT32 ts;

    // Número de identificación único del paquete de datos
    IUINT32 sn;

    // El símbolo significa que todos los paquetes inferiores a una han sido recibidos correctamente, al igual que el significado en TCP: el número de secuencia no reconocido más antiguo SND.
    IUINT32 una;

// Longitud de los datos
    IUINT32 len;

// Tiempo de retransmisión por tiempo de espera
    IUINT32 resendts;

// Tiempo de espera para la próxima expiración
    IUINT32 rto;

// Fast retransmission, if the number of data packets received after this packet exceeds a certain threshold, fast retransmission is triggered.
    IUINT32 fastack;

    // Número de envíos
    IUINT32 xmit;

// Datos
    char data[1];
};
```
</details>

Después de leer los comentarios de `SEGMENT`, se puede entender que el núcleo de KCP también es un protocolo ARQ que garantiza la entrega de datos mediante retransmisión automática por tiempo de espera. A continuación, veamos la definición de la estructura `KCPCB` en KCP:

<details>
<summary> Estructura KCP (Hacer clic para desplegar el código) </summary>
```cpp
//---------------------------------------------------------------------
// IKCPCB
//---------------------------------------------------------------------
struct IKCPCB
{
    // conv: Número de sesión
// mtu, mss: Máxima Unidad de Transferencia, Tamaño Máximo del Segmento de Datos
    // state: Estado de la sesión, 0 válido, -1 desconectado
    IUINT32 conv, mtu, mss, state;

    // snd_una: package number waiting for ACK
// snd_nxt: número de secuencia del próximo paquete de datos en espera de ser enviado
    // rcv_nxt: Número de secuencia del siguiente paquete de datos a recibir
    IUINT32 snd_una, snd_nxt, rcv_nxt;

    // ts_recent, ts_lastack: No utilizados
// ssthresh: Umbral de inicio lento para el control de congestión
    IUINT32 ts_recent, ts_lastack, ssthresh;

    // rx_rto: rto (retransmission timeout)，超时重传时间
    // rx_rttval, rx_srtt, rx_minrto: Variables intermedias para calcular el RTO
    IINT32 rx_rttval, rx_srtt, rx_rto, rx_minrto;

// snd_wnd, rcv_wnd: Tamaño máximo de la ventana de envío y recepción
    // rmt_wnd: tamaño de la ventana de recepción restante en el extremo remoto
// cwnd: tamaño de la ventana de envío disponible
    // prueba: ¿Indica si se debe enviar una señal de control?
    IUINT32 snd_wnd, rcv_wnd, rmt_wnd, cwnd, probe;

    // current: Tiempo actual
    // interval: Actualización del intervalo
// ts_flush: Próxima vez que se necesite actualizar el tiempo
// xmit: Número de intentos fallidos de envío.
    IUINT32 current, interval, ts_flush, xmit;

    // Longitud de la lista correspondiente
    IUINT32 nrcv_buf, nsnd_buf;
    IUINT32 nrcv_que, nsnd_que;

    // nodelay: Controla la velocidad de incremento del tiempo de espera de retransmisión (RTO).
    // actualizado: ¿se ha llamado a ikcp_update?
    IUINT32 nodelay, updated;

    // ts_probe, probe_wait: Active inquiry periodically initiated when the receiving window on the other end remains 0 for a long time.
    IUINT32 ts_probe, probe_wait;

    // deal_link: Falta de respuesta por parte del otro extremo durante mucho tiempo
    // incr: Participa en el cálculo del tamaño de la ventana de envío
    IUINT32 dead_link, incr;

    // cola: paquete de datos que interactúa con la capa de usuario
    // buf: paquete de datos en el búfer del protocolo
    struct IQUEUEHEAD snd_queue;
    struct IQUEUEHEAD rcv_queue;
    struct IQUEUEHEAD snd_buf;
    struct IQUEUEHEAD rcv_buf;

// Información del paquete de datos que requiere enviar un ACK
    IUINT32 *acklist;

// Número de paquetes que requieren ACK
    IUINT32 ackcount;

// Tamaño de la memoria de la lista de comprobación
    IUINT32 ackblock;

// Datos proporcionados por la capa de usuario
    void *user;

    // Almacena un espacio para un paquete kcp
    char *buffer;

    // Número de veces que se activa la retransmisión rápida de fastack
    int fastresend;

    // Número máximo de retransmisiones rápidas
    int fastlimit;

    // nocwnd: Tamaño de la ventana de envío sin tener en cuenta el inicio lento
    // stream: modo de flujo
    int nocwnd, stream;

    // debug log
    int logmask;

// Interfaz de envío de datos
    int (*output)(const char *buf, int len, struct IKCPCB *kcp, void *user);

    void (*writelog)(const char *log, struct IKCPCB *kcp, void *user);
};
```
</details>

### Traducción

Vamos a comentar cada campo en la estructura KCP uno por uno. Al hacerlo, podemos tener una primera impresión de que el protocolo KCP en su totalidad no es demasiado complicado. Si analizamos detenidamente el código, tanto tú como yo podemos leer y comprender el protocolo KCP. :smile:

##Implementación de ARQ en KCP

KCP básicamente es un protocolo ARQ (Auto Repeat-reQuest, repetición automática de solicitudes) cuyo objetivo es garantizar una transmisión confiable. Entonces, primero podemos centrarnos en la parte fundamental de ARQ de KCP y cómo logra dicha transmisión confiable.

ARQ, como su nombre indica, reenvía automáticamente los paquetes de datos cuando creemos que han fallado en ser recibidos por el destinatario. Esto se logra mediante dos mecanismos: la confirmación de recepción y la retransmisión por tiempo de espera, con el objetivo de lograr una transmisión confiable. En cuanto a la implementación de código específica, KCP asigna a cada paquete de datos (llamado `SEGMENT` en la sección anterior) un identificador único llamado `sn`. Una vez que el destinatario ha recibido el paquete de datos, envía un paquete ACK (también un `SEGMENT`), cuyo `sn` coincide con el `sn` del paquete de datos recibido, notificando que el paquete ha sido recibido exitosamente. Además, el `SEGMENT` tiene un campo llamado `una`, que indica el número del siguiente paquete de datos esperado. En otras palabras, todos los paquetes de datos con un número inferior a este ya han sido recibidos, equivaliendo a un paquete ACK completo. Esto permite que el remitente pueda actualizar rápidamente su búfer de envío y ventana de envío.

Podemos entender la implementación más básica de ARQ mediante el seguimiento de códigos de envío y recepción de paquetes KCP:

###`Enviar`

El proceso de envío es `ikcp_send` -> `ikcp_update` -> `ikcp_output`, la capa superior llama a `ikcp_send` para pasar los datos a KCP, KCP procesa el envío de datos en `ikcp_update`.

<details>
<summary> ikcp_send（click to expand code） </summary>
```cpp
//---------------------------------------------------------------------
// Interfaz de envío de datos, los usuarios llaman a ikcp_send para enviar datos a través de KCP
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
        // Modo de flujo de procesamiento
        // ......
    }

// Calcular subpaquetes, si la longitud de los datos len es mayor que mss, se deben enviar en varios paquetes y el receptor los reensamblará después de recibirlos.
    if (len <= (int)kcp->mss) count = 1;
    else count = (len + kcp->mss - 1) / kcp->mss;

    if (count >= (int)IKCP_WND_RCV) return -2;

    if (count == 0) count = 1;

// Subpackage
    for (i = 0; i < count; i++) {
        // Calculating the length of the data packet and allocating the corresponding seg structure
        int size = len > (int)kcp->mss ? (int)kcp->mss : len;
        seg = ikcp_segment_new(kcp, size);
        assert(seg);
        if (seg == NULL) {
            return -2;
        }

        // Establecer la información de datos para seg, frg representa el número de paquete dividido
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

`ikcp_send` es la interfaz de envío de datos que se llama desde la capa superior de KCP. Todos los datos que se desean enviar a través de KCP deben pasar por esta interfaz. La función de `ikcp_send` es bastante sencilla: divide los datos en varios paquetes de acuerdo con la longitud máxima de datos por paquete (`kcp->mss`), les asigna un número de secuencia y finalmente los coloca al final de la lista de envío `snd_queue`. En el modo de flujo, todas las llamadas sucesivas a `ikcp_send` se consideran como una secuencia continua de datos, se rellenan automáticamente los `SEGMENT` no completos y se asignan nuevos si es necesario. No vamos a discutir aquí la implementación detallada, pero si estás interesado, después de leer este texto, te recomiendo revisar el código correspondiente para una mejor comprensión.

Después de completar la llamada a `ikcp_send`, los datos se colocan en la `snd_queue` de KCP, así que más adelante KCP necesita encontrar un momento para enviar los datos pendientes. Este bloque de código se encuentra en `ikcp_update` y `ikcp_flush`.

<details>
<summary>ikcp_update (click to expand code)</summary>
```cpp
//---------------------------------------------------------------------
// `ikcp_update` is an interface that the upper layer calls regularly to update the state of KCP and send data.
// update state (call it repeatedly, every 10ms-100ms), or you can ask 
// ikcp_check when to call it again (without ikcp_input/_send calling).
// 'current' - current timestamp in millisec. 
//---------------------------------------------------------------------
void ikcp_update(ikcpcb *kcp, IUINT32 current)
{
    IINT32 slap;

    kcp->current = current;

// `ikcp_flush` verificará esto, la capa superior debe haber llamado a `ikcp_update` antes de llamar a `ikcp_flush`, se recomienda usar solo `ikcp_update`.
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
        // Próxima vez que se realizará un "flush"
        kcp->ts_flush += kcp->interval;
        if (_itimediff(kcp->current, kcp->ts_flush) >= 0) {
            kcp->ts_flush = kcp->current + kcp->interval;
        }
        ikcp_flush(kcp);
    }
}
```
</details>

El trabajo realizado por `ikcp_update` es bastante simple. Se evalúa el tiempo de `ts_flush` y, si se cumple cierta condición, se llama a `ikcp_flush`. La mayor parte de la lógica de procesamiento se encuentra dentro de `ikcp_flush`, ya que es ahí donde se manejan las partes relacionadas con el envío ARQ, que es lo que nos interesa en este momento.

<details>
<summary>Envío de datos (Haga clic para desplegar el código)</summary>
```cpp
//---------------------------------------------------------------------
// ikcp_flush
//---------------------------------------------------------------------
void ikcp_flush(ikcpcb *kcp)
{
    IUINT32 current = kcp->current;

    // buffer es el dato que se pasará a ikcp_output, se inicializa como el triple del tamaño del paquete de datos
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

    // seg.wnd representa el tamaño actual de la ventana de recepción.
    seg.wnd = ikcp_wnd_unused(kcp);
    seg.una = kcp->rcv_nxt;
    seg.len = 0;
    seg.sn = 0;
    seg.ts = 0;

// Enviar ack
// Calcular la ventana de envío
    //...

// Mover los paquetes de datos desde la cola de envío (snd_queue) al búfer de envío (snd_buf)
// Moverse requerirá cumplir con el tamaño de la ventana de envío. Si la ventana de envío está llena, se detendrá el movimiento.
// Los datos colocados dentro de snd_buf son los que se pueden enviar directamente al destino utilizando la función ikcp_output.
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

        // seg es un número de secuencia único, que en realidad es un KCP en aumento de kcp->snd_nxt
        newseg->sn = kcp->snd_nxt++;

        // una 在这里设置，通知对端下一个等待接收的包序号

        // una se establece aquí para informar al extremo opuesto el número de secuencia del próximo paquete esperado.
        newseg->una = kcp->rcv_nxt;
        newseg->resendts = current;
        newseg->rto = kcp->rx_rto;
        newseg->fastack = 0;
        newseg->xmit = 0;
    }

// Calcular la bandera de retransmisión rápida, el tiempo de espera de espera de tiempo
    // ...

// Enviar snd_buf
    for (p = kcp->snd_buf.next; p != &kcp->snd_buf; p = p->next) {
        IKCPSEG *segment = iqueue_entry(p, IKCPSEG, node);
        int needsend = 0;
        if (segment->xmit == 0) {
            // Primera vez que se envía
            // set->xmit indica el número de veces que se ha enviado
// resendts tiempo de espera para la retransmisión por tiempo de espera excedido
            needsend = 1;
            segment->xmit++;
            segment->rto = kcp->rx_rto;
            segment->resendts = current + segment->rto + rtomin;
        }
        else if (_itimediff(current, segment->resendts) >= 0) {
// Superposición de tiempo
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

            // Cada vez que los datos en el búfer superen el MTU, se envían primero para evitar al máximo la fragmentación adicional en el nivel inferior.
            if (size + need > (int)kcp->mtu) {
                ikcp_output(kcp, buffer, size);
                ptr = buffer;
            }

            // Copia los datos de control de seg a buffer, para que KCP se encargue de los problemas de orden de bytes.
            ptr = ikcp_encode_seg(ptr, segment);

            // Copiar los datos de nuevo
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

// Calculating ssthresh, updating slow start window
    // ...
}
```
</details>

Actualmente solo nos estamos centrando en la lógica relacionada con el envío de datos en `ikcp_flush`:

* Primero, KCP moverá los datos de la cola de envío `snd_queue` a la ventana de envío `snd_buf` según el tamaño de la ventana de recepción del extremo opuesto. La fórmula para calcular la cantidad de datos a mover es `num = snd_nxt - (snd_una + cwnd)`, es decir: si la suma del número de secuencia del último paquete enviado con éxito `snd_una` y el tamaño de la ventana deslizante `cwnd` es mayor que el número de secuencia del siguiente paquete a enviar `snd_nxt`, entonces se puede continuar enviando nuevos paquetes de datos. Al mover los `SEG`, también se configuran los campos de control.

Recorre `snd_buf`, si es necesario enviar un paquete de datos, copia los datos en `buffer`, al mismo tiempo que utiliza `ikcp_encode_seg` para manejar el problema de secuencia de orden de los datos del campo de control.

Por último, se llama a `ikcp_output` para enviar los datos del `buffer`.

Hasta aquí, KCP ha completado el envío de los datos.

###**接收**

El proceso de recepción es contrario al de envío: `ikcp_input` -> `ikcp_update` -> `ikcp_recv`. Después de que el usuario reciba datos en la red, debe llamar a `ikcp_input` para enviarlos a KCP para su análisis. Al llamar a `ikcp_update`, se enviará un paquete ACK al remitente, y la capa superior recibirá los datos analizados por KCP al llamar a `ikcp_recv`.

<details>
<summary>Recibir datos (haz clic para desplegar el código)</summary>
```cpp
//---------------------------------------------------------------------
// input data
//---------------------------------------------------------------------
int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    IUINT32 prev_una = kcp->snd_una;
    IUINT32 maxack = 0, latest_ts = 0;
    int flag = 0;

// Comprobación de legalidad
    if (data == NULL || (int)size < (int)IKCP_OVERHEAD) return -1;

// data puede contener varios paquetes KCP, procesar en bucle
    while (1) {
        IUINT32 ts, sn, len, una, conv;
        IUINT16 wnd;
        IUINT8 cmd, frg;
        IKCPSEG *seg;

        // No hay suficientes paquetes KCP, salir
        if (size < (int)IKCP_OVERHEAD) break;

        // Primero, se analizan los campos de control
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

// Comprobación del tipo de paquete de datos
        if (cmd != IKCP_CMD_PUSH && cmd != IKCP_CMD_ACK &&
            cmd != IKCP_CMD_WASK && cmd != IKCP_CMD_WINS) 
            return -3;

        kcp->rmt_wnd = wnd;

        // Aquí, `una` es el valor `kcp->rcv_nxt` del remitente. Con esta información, se pueden descartar los paquetes de datos que ya han sido confirmados como recibidos.
        ikcp_parse_una(kcp, una);
// Después de eliminar los paquetes ya confirmados recibidos, se actualiza snd_una con el siguiente número de secuencia a enviar.
        ikcp_shrink_buf(kcp);

        if (cmd == IKCP_CMD_ACK) {
            // paquete de ack
            // ...
        }
        else if (cmd == IKCP_CMD_PUSH) {
            // Paquete de datos
// Si el número de secuencia del paquete recibido, sn, está dentro de la ventana de recepción, se procesa normalmente; de lo contrario, se descarta y se espera la retransmisión.
            if (_itimediff(sn, kcp->rcv_nxt + kcp->rcv_wnd) < 0) {

                // Por cada paquete de datos recibido, se debe enviar un paquete de ack para registrarlo
                ikcp_ack_push(kcp, sn, ts);

                // El dato recibido se procesa mediante la llamada a ikcp_parse_data
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
            // Paquete de la ventana de consulta
            // ...
        }
        else if (cmd == IKCP_CMD_WINS) {
            // Paquete de respuesta de la ventana de consulta
            // ...
        }
        else {
            return -3;
        }

        data += len;
        size -= len;
    }

// Procesando la lógica de retransmisión rápida
    // ...

// Actualizar ventana de envío
    // ...

    return 0;
}
```
</details>

El `ikcp_input` procesa en bucle cada paquete `SEG`, primero verifica la validez y el tipo del paquete de datos porque cada paquete lleva `una`, que es el número de secuencia del paquete que espera el remitente. Los paquetes del otro extremo que tienen un número de secuencia menor que `una` se consideran recibidos con éxito, por lo que se pueden eliminar del `snd_buff` los que necesitan ser menores que `una` y se actualiza `snd_nxt`. Esta parte la manejan `ikcp_parse_una` y `ikcp_shrink_buf`. Cada paquete de datos recibido requiere una respuesta de ACK, que se registra con `ikcp_ack_push` y finalmente se llama a `ikcp_parse_data` para procesar los datos.

<details>
<summary> Analizando datos (haga clic para desplegar el código) </summary>
```cpp
void ikcp_parse_data(ikcpcb *kcp, IKCPSEG *newseg)
{
    struct IQUEUEHEAD *p, *prev;
    IUINT32 sn = newseg->sn;
    int repeat = 0;

// Comprobación de número de secuencia
    if (_itimediff(sn, kcp->rcv_nxt + kcp->rcv_wnd) >= 0 ||
        _itimediff(sn, kcp->rcv_nxt) < 0) {
        ikcp_segment_delete(kcp, newseg);
        return;
    }

// Busca la ubicación donde debe colocarse `newseg`, ya que `seg` recibido puede estar desordenado.
    for (p = kcp->rcv_buf.prev; p != &kcp->rcv_buf; p = prev) {
        IKCPSEG *seg = iqueue_entry(p, IKCPSEG, node);
        prev = p->prev;
        if (seg->sn == sn) {
            // Repetido recibido
            repeat = 1;
            break;
        }
        if (_itimediff(sn, seg->sn) > 0) {
            break;
        }
    }

// Coloca newseg en la posición correcta en rcv_buf
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
        // Si el número de secuencia "seg" es el número de secuencia esperado, mueve a la cola de recepción "rcv_queue"
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

La función principal de `ikcp_parse_data` es colocar `newseg` en la posición adecuada dentro de `kcp->rcv_buf` y mover los datos de `rcv_buf` a `rcv_queue`. La posición adecuada en `rcv_buf` significa que `rcv_buf` está ordenado en orden creciente según el número de secuencia (`sn`), por lo que `newseg` debe buscar la posición adecuada según su propio número de secuencia (`sn`). Los datos en `rcv_buf` se mueven a `rcv_queue` cuando el número de secuencia del paquete en `rcv_buf` es igual al número de secuencia del paquete que KCP está esperando recibir (`kcp->rcv_nxt`). Después de mover un paquete de datos, es necesario actualizar `kcp->rcv_nxt` y continuar con el siguiente paquete de datos.

Después de `ikcp_input`, al llamar a `ikcp_update`, se enviará un paquete ACK, y al llamar a `ikcp_recv`, se devolverán datos válidos a la capa superior. `ikcp_update` y `ikcp_recv` son independientes entre sí, no tienen requisitos de secuencia de llamadas, dependen del momento de la llamada de la capa superior. Primero veamos la parte de envío de ACK en `ikcp_update`:

<details>
<summary> Respuesta ACK (haga clic para mostrar el código) </summary>
```cpp
// Como se mencionó anteriormente, la función ikcp_update finalmente llama a ikcp_flush.
void ikcp_flush(ikcpcb *kcp, IUINT32 current)
{
    // ...

// Responder al paquete ACK
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

El ACK del paquete se guarda anteriormente por `ikcp_ack_push`, por lo que aquí solo necesitamos obtener la información de cada ACK del paquete mediante `ikcp_ack_get` y enviarla al destinatario. La aplicación superior puede utilizar `ikcp_recv` para obtener datos de KCP.

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

// Algunas comprobaciones de validez
    if (iqueue_is_empty(&kcp->rcv_queue))
        return -1;
    if (len < 0) len = -len;

// Calcular la longitud de los datos que se pueden devolver
    peeksize = ikcp_peeksize(kcp);

    if (peeksize < 0)
        return -2;
    if (peeksize > len)
        return -3;

// Verificar la ventana de recepción
    if (kcp->nrcv_que >= kcp->rcv_wnd)
        recover = 1;

// Recorre la cola rcv_queue y copia los datos en el buffer
    for (len = 0, p = kcp->rcv_queue.next; p != &kcp->rcv_queue; ) {
        int fragment;
        seg = iqueue_entry(p, IKCPSEG, node);
        p = p->next;

        if (buffer) {
            memcpy(buffer, seg->data, seg->len);
            buffer += seg->len;
        }

        len += seg->len;

// Comprueba la división de paquetes
        fragment = seg->frg;

// Eliminar paquete de datos
        if (ispeek == 0) {
            iqueue_del(&seg->node);
            ikcp_segment_delete(kcp, seg);
            kcp->nrcv_que--;
        }

        // Todos los paquetes han sido copiados, salir del bucle
        if (fragment == 0)
            break;
    }

    assert(len == peeksize);

// rcv_queue ha vuelto a vaciarse un poco, intentamos continuar moviendo desde rcv_buf a rcv_queue
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

`ikcp_recv` es una función que devuelve únicamente un paquete de datos completo por llamada. Es posible llamarla en un bucle hasta que no haya más datos para recibir. La lógica de la función es bastante sencilla: copia los datos de la `rcv_queue` al `buffer` proporcionado por la capa superior. De esta manera, el receptor ha completado el procesamiento del paquete recibido.

Cuando el destinatario procesa el paquete de datos, envía un paquete de ACK al remitente. A continuación, analizaremos el tratamiento que recibe el remitente al recibir el paquete de ACK.

<details>
<summary> Procesando paquetes ACK (haga clic para ver el código) </summary>
```cpp
int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    // ...
    IUINT32 maxack = 0, latest_ts = 0;
    // ...
    while (1) {
        // ...
        // ts es el kcp->current del extremo opuesto
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

    // Si se recibe un paquete ACK, se registra para su uso en la retransmisión rápida
    if (flag != 0) {
        ikcp_parse_fastack(kcp, maxack, latest_ts);
    }
}
```
</details>

Se puede observar que después de recibir un paquete ACK, también se requerirá utilizar `ikcp_parse_ack` y `ikcp_shrink_buf` para actualizar `snd_buf`. Además, es necesario llamar a `ikcp_update_ack` para calcular la actualización de rto (retransmission timeout, tiempo de retransmisión por tiempo de espera). `ikcp_input` calcula el número de secuencia máximo recibido en el paquete ACK para registrarlo y utilizarlo en la recuperación rápida. De esta manera, cuando el remitente recibe el paquete ACK, elimina los datos enviados de `snd_buf` y se confirma que el paquete de datos ha sido entregado de manera confiable al receptor, finalizando así el proceso completo de confirmación y recepción de ARQ.

###超时重传

El mecanismo de recepción de confirmación implementado por KCP fue presentado anteriormente en el ARQ. Sin embargo, el ARQ también requiere un mecanismo de retransmisión por tiempo de espera para garantizar la confiabilidad. A continuación, veremos cómo KCP maneja esta retransmisión por tiempo de espera.

Volvamos a la función `ikcp_flush`:

<details>
<summary>Reenvío por tiempo de espera (haz clic para ver el código)</summary>
```cpp
void ikcp_flush(ikcpcb *kcp)
{
    // ...
// Enviar snd_buf
    for (p = kcp->snd_buf.next; p != &kcp->snd_buf; p = p->next) {
        IKCPSEG *segment = iqueue_entry(p, IKCPSEG, node);
        int needsend = 0;
        if (segment->xmit == 0) {
// Primera vez que se envía
            needsend = 1;
            segment->xmit++;
// Establecer segmento->rto
            // Calcular el tiempo de retransmisión por tiempo fuera segment->rto usando segment->resendts 
            segment->rto = kcp->rx_rto;
            segment->resendts = current + segment->rto + rtomin;
        }
        else if (_itimediff(current, segment->resendts) >= 0) {
// Tiempo de espera de retransmisión
            needsend = 1;
            segment->xmit++;
            kcp->xmit++;
// `nodelay` controla el cálculo del tiempo para el próximo reenvío luego de expirar el tiempo de espera.
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
// Enviar datos
            // ...
        }
    // ...
}
```
</details>

Una vez que el tiempo actual `current` sea mayor que el tiempo de reenvío `segment->resendts`, esto significa que durante ese intervalo de tiempo no se recibió ningún paquete de ACK del receptor, lo que activa el mecanismo de retransmisión por tiempo de espera. En este caso, `needsend = 1` y se reenvían los datos.

Con la implementación de un mecanismo de confirmación de recepción y retransmisión por tiempo de espera, KCP puede garantizar una transmisión de datos fiable en su base. Sin embargo, para lograr una velocidad de flujo de datos más estable, KCP también realiza otras optimizaciones. A continuación, veamos qué otras mejoras ha implementado KCP.

##KCP Estrategia para aumentar la velocidad de flujo

###**快速重传** se traduce al español como **Reenvío rápido**.

El remitente envía los paquetes de datos con los números de secuencia `sn` y `sn + 1`. Si solo se recibe el paquete de ACK `sn + 1`, esto puede ser debido a que el paquete de ACK `sn` aún no ha llegado a la red, o se ha perdido el paquete de ACK `sn`, o se ha perdido el paquete de datos `sn`. Si en este momento aún no ha transcurrido el tiempo de retransmisión de tiempo de espera y la red no está demasiado congestionada, y solo se ha producido una pérdida ocasional del paquete debido a alguna razón, entonces el remitente puede enviar activamente el paquete de datos `sn` de manera anticipada para ayudar al receptor a recibir los datos más rápidamente y mejorar la velocidad de transferencia.

KCP también implementa un mecanismo de retransmisión rápida en el interior, que se encuentra en `ikcp_flush`.

<details>
<summary>Reenvío rápido (haga clic para mostrar el código)</summary>
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
            // Quick retransmission
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
* `segment->fastack >= resent`，`resent` es un parámetro configurable llamado `kcp->fastresend`, si se configura en 0 se desactiva la retransmisión rápida. `segment->fastack` se establece en la función `ikcp_parse_fastack`, la cual es invocada en `ikcp_input`, aumentando en uno `segment->fastack` para todos los segmentos con `sn` menor a `maxack`, calculado por `ikcp_input`. Por lo tanto, `segment->fastack` indica la cantidad de veces que se ha recibido un paquete con un número de secuencia mayor a `sn`.
* `segment->xmit <= kcp->fastlimit || kcp->fastlimit <= 0`，`setgment->xmit` is the number of transmissions, `kcp->fastlimit` is the configurable maximum number of fast retransmissions, the number of transmissions must be less than the maximum number of fast retransmissions.

Una vez que se cumplen las condiciones anteriores para la rápida retransmisión, KCP llevará a cabo dicha retransmisión. Es importante tener en cuenta que la rápida retransmisión no reinicia el tiempo de retransmisión por tiempo agotado, el tiempo de retransmisión original seguirá siendo efectivo.

###**缩短超时重传时间** se traduce al español como **Reducir el tiempo de reenvío por tiempo de espera**.

超时重传 es un mecanismo muy bueno, pero simplemente lleva mucho tiempo. Según la estrategia de TCP, cada vez que se produce un tiempo de espera, el tiempo de espera se duplica. El tiempo de espera se expande rápidamente. Durante el tiempo de espera, es muy probable que el receptor haya agotado la ventana de recepción y no pueda recibir nuevos datos. El número de secuencia del paquete que espera ser retransmitido se encuentra al principio, el receptor debe recibir el paquete retransmitido para devolver todos los datos a la capa superior. En esta situación, la velocidad de flujo de toda la red es casi cero. KCP agrega una configuración para retardar el aumento del tiempo de espera, y tampoco es una duplicación. A través de la configuración `kcp->nodelay`, se controlará que el tiempo de espera solo aumente 1 vez del RTO o 0.5 veces del RTO, reduciendo efectivamente el aumento del tiempo de espera y ayudando a que la red recupere la velocidad de flujo lo más rápido posible.

###**Actualizar ventana de envío**

La `ventana de envío` indica la cantidad de paquetes de datos que se transmiten simultáneamente. Cuanto más grande sea la ventana, más datos se transmitirán al mismo tiempo, lo que aumentará la velocidad del flujo. Sin embargo, si la ventana es demasiado grande, puede provocar congestión en la red, aumentar la tasa de pérdida de paquetes, aumentar la retransmisión de datos y disminuir la velocidad del flujo. Por lo tanto, es necesario actualizar constantemente la ventana de envío según la situación de la red, acercándose gradualmente al óptimo. El código relacionado con la ventana de envío en KCP es el siguiente:

<details>
<summary>Enviar ventana (haz clic para desplegar el código)</summary>
```cpp
ikcpcb* ikcp_create(IUINT32 conv, void *user)
{
    // ...
// snd_wnd, rcv_wnd Tamaño de los buffers de envío y recepción
    kcp->snd_wnd = IKCP_WND_SND;    // 32
    kcp->rcv_wnd = IKCP_WND_RCV;    // 128
    // Tamaño de la ventana de recepción del extremo opuesto              // 128
    kcp->rmt_wnd = IKCP_WND_RCV
    // Inicialización de la ventana de envío cwnd en 0
    kcp->cwnd = 0;
    // Enviar el tamaño en bytes de la ventana de envío, para participar en el cálculo de cwnd
    kcp->incr = 0
    // Umbral de arranque lento, umbral de inicio lento
    kcp->ssthresh = IKCP_THRESH_INIT;
// `nocwnd` is a configurable parameter, with a value of 1 it means no consideration of `cwnd`.
    kcp->nocwnd = 0;
    // ...
}

void ikcp_flush(ikcpcb *kcp)
{
    // ...
// Al enviar datos, primero se calcula el tamaño de la ventana de envío, que es el valor mínimo entre el tamaño del búfer de envío y el tamaño de la ventana de recepción del destinatario.
    cwnd = _imin_(kcp->snd_wnd, kcp->rmt_wnd);
    // Además, hay que tener en cuenta kcp->cwnd, es decir, la ventana de envío continuamente actualizada.
    if (kcp->nocwnd == 0) cwnd = _imin_(kcp->cwnd, cwnd);

// Según el tamaño de cwnd, snd_queue se mueve a snd_buf
    while (_itimediff(kcp->snd_nxt, kcp->snd_una + cwnd) < 0) {
    }
// Enviar datos
    resent = (kcp->fastresend > 0)? (IUINT32)kcp->fastresend : 0xffffffff;
// Trigger retransmission timeout lost = 1

// Activar retransmisión de tiempo de espera pérdida = 1
// Cambio++ para activar la retransmisión rápida

    // Actualizar el umbral de arranque lento y la ventana de envío
    if (change) {
// Si se produce una retransmisión rápida, ssthresh se establece en la mitad de la cantidad de paquetes de datos que se están transmitiendo en la red.
        IUINT32 inflight = kcp->snd_nxt - kcp->snd_una;
        kcp->ssthresh = inflight / 2;
        if (kcp->ssthresh < IKCP_THRESH_MIN)
            kcp->ssthresh = IKCP_THRESH_MIN;

        // Enviar ventana establecida más la retransmisión rápida relacionada con resent
        kcp->cwnd = kcp->ssthresh + resent;
        kcp->incr = kcp->cwnd * kcp->mss;
    }

    if (lost) {
        // Si hay retransmisiones por tiempo de espera, se activa el inicio lento, el umbral ssthresh es la mitad de la ventana de envío.
        kcp->ssthresh = cwnd / 2;
        if (kcp->ssthresh < IKCP_THRESH_MIN)
            kcp->ssthresh = IKCP_THRESH_MIN;
// Enviar ventana de regreso a 1, reiniciar el crecimiento lento
        kcp->cwnd = 1;
        kcp->incr = kcp->mss;
    }

    if (kcp->cwnd < 1) {
        // Debido a que está inicializado a 0, al llegar aquí se reestablecerá a 1
        kcp->cwnd = 1;
        kcp->incr = kcp->mss;
    }
}

int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    IUINT32 prev_una = kcp->snd_una;
// Procesar los datos recibidos

    while (1) {
        // ...
        data = ikcp_decode16u(data, &wnd)
        // rmt_wnd es el tamaño de la ventana de recepción del otro lado
        kcp->rmt_wnd = wnd
        // ...
// Procesando datos
    }

    // Última actualización de la ventana de envío
    // kcp->snd_una - prev_una > 0, indicates that this input has received ACK and the send buffer snd_buf has changed.
    if (_itimediff(kcp->snd_una, prev_una) > 0) {
        // Luego se verifica la ventana de recepción del otro lado
        if (kcp->cwnd < kcp->rmt_wnd) {
            IUINT32 mss = kcp->mss;

            if (kcp->cwnd < kcp->ssthresh) {
                // Si es menor que el umbral de inicio lento, se duplica el crecimiento
                kcp->cwnd++;
                kcp->incr += mss;

            }    else {
                // Después de superar el umbral de arranque lento, actualice incr utilizando la fórmula y calcule cwnd.
                if (kcp->incr < mss) kcp->incr = mss;
                kcp->incr += (mss * mss) / kcp->incr + (mss / 16);
                if ((kcp->cwnd + 1) * mss <= kcp->incr) {
                    kcp->cwnd++;
                }
            }
// No dude en volver a comparar el valor actualizado de rmt_wnd
            if (kcp->cwnd > kcp->rmt_wnd) {
                kcp->cwnd = kcp->rmt_wnd;
                kcp->incr = kcp->rmt_wnd * mss;
            }
        }
    }
}
```
</details>

if (kcp->cwnd < kcp->ssthresh)
    kcp->cwnd++;
else{
    if (kcp->cwnd < kcp->rto_backoff)
        kcp->cwnd++; // slow start
    else{
        if (kcp->cwnd < kcp->cwnd_max) {
            kcp->cwnd += kcp->cwnd_max/kcp->cwnd;
        } else {
            kcp->cwnd ++;
        }
    }
}

El código que involucra el cálculo del tamaño de la ventana de envío `kcp->cwnd` es un poco más extenso, ya que debe actualizarse tanto al enviar como al recibir datos. `kcp->cwnd` se inicializa en 0.

si (kcp->cwnd < kcp->ssthresh)
    kcp->cwnd++;
sino{
    si (kcp->cwnd < kcp->rto_backoff)
        kcp->cwnd++; // inicio lento
    sino{
        si (kcp->cwnd < kcp->cwnd_max) {
            kcp->cwnd += kcp->cwnd_max/kcp->cwnd;
        } else {
            kcp->cwnd ++;
        }
    }
}
Después, en la primera llamada a `ikcp_flush`, se comprobará si es menor que 1 y, de ser así, se modificará a 1. A continuación, el remitente enviará la cantidad correspondiente de paquetes de datos según el tamaño de la ventana de envío, y esperará por el ACK.
Responder al paquete. El paquete ACK se procesa en `kcp->input`. Si se detecta un paquete ACK en`kcp->input` y se borran los paquetes de datos enviados del búfer de envío, esto indica que se han entregado los paquetes de datos. `kcp->cwnd++`. En realidad, es muy probable que `kcp->input` solo procese un paquete ACK a la vez. Se puede entender que cada vez que se recibe un paquete ACK, `kcp->cwnd++` aumenta, lo que resulta en un efecto de duplicación. Por ejemplo, supongamos que en el momento actual `kcp->cwnd = 2`, se envían dos paquetes de datos y se reciben dos paquetes ACK, lo que activa dos incrementos, y al final `kcp->cwnd = 4`, es decir, se duplica.

`cwnd` puede crecer exponencialmente hasta superar el umbral de arranque lento, o hasta que ocurra una retransmisión por tiempo de espera de congestión o una retransmisión rápida. Después de una retransmisión por tiempo de espera, se desencadena un arranque lento, con un umbral de arranque lento `ssthresh = kcp->cwnd / 2`, y la ventana de envío `kcp->cwnd = 1` vuelve a crecer exponencialmente desde el principio. Si ocurre una retransmisión rápida, KCP reduce previamente `ssthresh`, lo que reduce el espacio de crecimiento exponencial de `cwnd`, disminuyendo la velocidad de crecimiento y atenuando anticipadamente la congestión.

KCP ha agregado una nueva configuración `nocwnd`, cuando `nocwnd = 1`, el envío de datos ya no tiene en cuenta el tamaño de la ventana de envío y, en cambio, envía directamente la cantidad máxima de paquetes de datos que se pueden enviar, cumpliendo así con los requisitos del modo de alta velocidad.

##**Resumen**

Este texto analiza brevemente el código fuente de KCP y discute la implementación de ARQ en KCP, así como algunas estrategias para mejorar la velocidad de flujo de KCP. Hay muchos detalles que no se mencionan aquí, si estás interesado, puedes investigar el código fuente de KCP por ti mismo y compararlo, estoy seguro de que obtendrás muchos beneficios.

--8<-- "footer_en.md"


> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki_blog/issues/new) si hay alguna omisión.
