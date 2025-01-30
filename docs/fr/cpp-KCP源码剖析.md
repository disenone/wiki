---
layout: post
title: Analyse du code source KCP
categories:
- c++
catalog: true
tags:
- dev
description: Ce texte analyse simplement le code source de KCP, discute de la mise
  en œuvre de l'ARQ sur KCP, ainsi que de quelques stratégies pour augmenter la vitesse
  de transmission de KCP.
figures: []
---

<meta property="og:title" content="KCP 源码剖析" />

Avant de lire cet article, si vous n'avez jamais entendu parler de KCP ou si vous ne connaissez pas du tout KCP, merci de prendre un peu de temps pour consulter le document explicatif du projet KCP : [Portail](https://github.com/skywind3000/kcp)L'objectif de cet article est d'explorer en profondeur les détails de mise en œuvre de KCP afin de comprendre KCP.

##Qu'est-ce que le KCP ?

KCP est un protocole rapide et fiable, capable de transmettre des données avec une latence inférieure à celle du TCP, permettant une retransmission des données plus rapide et des temps d'attente plus courts.

> TCP est conçu pour le trafic (combien de KB de données peuvent être transférées par seconde), mettant l'accent sur une utilisation optimale de la bande passante. KCP, en revanche, est conçu pour la vitesse de transmission (le temps qu'un paquet de données met pour aller d'une extrémité à l'autre), échangeant un gaspillage de bande passante de 10 à 20 % pour obtenir une vitesse de transmission 30 à 40 % plus rapide que celle de TCP. Le canal TCP est comme un grand canal à débit lent mais avec un volume de trafic très élevé, tandis que KCP se compare à un petit torrent à fort courant.

Ce qui est écrit ci-dessus dans le document de KCP mentionne les mots-clés **bande passante** et **débit**. KCP consomme de la bande passante, ce qui entraîne des avantages comme des débits de transmission plus importants et plus équilibrés. Pour plus d'informations, veuillez vous référer à la documentation officielle de KCP.

##KCP structure de données

Le code source de KCP se trouve dans les fichiers `ikcp.h` et `ikcp.c`, où `ikcp.h` contient la déclaration des structures de données. La première est le paquet de données `SEGMENT`, qui représente l'unité minimale de traitement des données pour le protocole KCP :

<details>
<summary>Structure SEGMENT (cliquez pour afficher le code)</summary>
```cpp
//=====================================================================
SEGMENT est un paquet de données.
//=====================================================================
struct IKCPSEG
{
Noeud de la liste chaînée, à la fois la file d'attente de l'émission et la file d'attente de réception sont des structures de liste ici.
    struct IQUEUEHEAD node;

Identifiant de session, le même identifiant de session est identique.
    IUINT32 conv;

Type de paquet, par exemple DATA ou ACK.
    IUINT32 cmd;

// En raison des limites de MTU, les gros paquets sont fragmentés en plusieurs petits paquets, voici le numéro de petit paquet.
    IUINT32 frg

Chaque paquet de données est accompagné de la taille de la fenêtre de réception de l'émetteur.
    IUINT32 wnd;

// Le temps d'envoi, s'il s'agit d'un paquet ACK, sera défini sur le ts du paquet de données source
    IUINT32 ts;

// Numéro identifiant unique du paquet de données
    IUINT32 sn;

// Cela signifie que tous les paquets de données inférieurs à una ont été reçus avec succès, en accord avec le sens TCP : le plus ancien numéro de séquence non reconnu SND
    IUINT32 una;

Longueur des données
    IUINT32 len;

Temps de retransmission timeout
    IUINT32 resendts;

Prochain délai d'attente dépassé
    IUINT32 rto;

Réémission rapide, le nombre de paquets de données reçus après ce paquet dépasse un certain seuil, déclenchant ainsi la réémission rapide.
    IUINT32 fastack;

Le nombre d'envois.
    IUINT32 xmit;

// Données
    char data[1];
};
```
</details>

Après avoir regardé les commentaires sur `SEGMENT`, on peut voir que le cœur de KCP est également un protocole ARQ, garantissant la livraison des données par retransmission automatique en cas de dépassement de délai. Passons maintenant à la définition de la structure KCP `KCPCB` :

<details>
<summary>Structure KCP (cliquez pour afficher le code)</summary>
```cpp
//---------------------------------------------------------------------
// IKCPCB
//---------------------------------------------------------------------
struct IKCPCB
{
// conv : numéro de la conversation
mtu, mss: Unité de transfert maximale, taille maximale de segment de message
// état : état de la session, 0 valide, -1 déconnecté
    IUINT32 conv, mtu, mss, state;

// snd_una: Numéro de paquet en attente d'ACK
// snd_nxt: le numéro du paquet de données suivant à envoyer
// rcv_nxt : numéro du prochain paquet de données à recevoir
    IUINT32 snd_una, snd_nxt, rcv_nxt;

// ts_recent, ts_lastack : non utilisé
// ssthresh : seuil de contrôle de congestion pour le démarrage lent
    IUINT32 ts_recent, ts_lastack, ssthresh;

// rx_rto: rto (temps d'attente de retransmission) - temps de retransmission en cas de dépassement du délai
// rx_rttval, rx_srtt, rx_minrto: Calcul des variables intermédiaires pour le calcul de RTO
    IINT32 rx_rttval, rx_srtt, rx_rto, rx_minrto;

// snd_wnd, rcv_wnd : Taille maximale des fenêtres d'envoi et de réception
// rmt_wnd : fenêtre distante, taille restante de la fenêtre d'acceptation de l'autre partie
// cwnd : taille de la fenêtre d'envoi
// probe: Indicateur sur l'envoi de messages de contrôle
    IUINT32 snd_wnd, rcv_wnd, rmt_wnd, cwnd, probe;

// current: Heure actuelle
// interval: Intervalle de mise à jour
// ts_flush : Temps de mise à jour suivant nécessaire
// xmit : Nombre d'échecs d'envoi
    IUINT32 current, interval, ts_flush, xmit;

Longueur de la liste correspondante
    IUINT32 nrcv_buf, nsnd_buf;
    IUINT32 nrcv_que, nsnd_que;

// nodelay : Contrôle la vitesse d'augmentation du rto pour les retransmissions en cas de timeout
// mis à jour: Est-ce que ikcp_update a été appelé
    IUINT32 nodelay, updated;

// ts_probe, probe_wait : Lorsqu'il y a une fenêtre de réception à l'autre extrémité qui reste à 0 pendant une longue période, une interrogation est lancée activement et régulièrement.
    IUINT32 ts_probe, probe_wait;

// deal_link: Pas de réponse de l'autre partie depuis longtemps
// incr: Participation au calcul de la taille de la fenêtre d'envoi
    IUINT32 dead_link, incr;

// queue: paquet de données en contact avec la couche utilisateur
// buf: Paquet de données mis en cache par le protocole
    struct IQUEUEHEAD snd_queue;
    struct IQUEUEHEAD rcv_queue;
    struct IQUEUEHEAD snd_buf;
    struct IQUEUEHEAD rcv_buf;

// Informations sur les paquets de données nécessitant l'envoi d'un ack
    IUINT32 *acklist;

Le nombre de paquets nécessitant un accusé de réception.
    IUINT32 ackcount;

// Taille de la mémoire de la liste des exceptions
    IUINT32 ackblock;

Les données transmises par la couche utilisateur.
    void *user;

Stockage de l'espace pour un paquet KCP.
    char *buffer;

Le nombre de déclenchements du retransmission rapide (fastack)
    int fastresend;

// Nombre maximal de retransmissions rapides
    int fastlimit;

// nocwnd: Ne tient pas compte de la taille de la fenêtre d'envoi lors du démarrage lent
stream: mode flux
    int nocwnd, stream;

    // debug log
    int logmask;

Interface d'envoi de données.
    int (*output)(const char *buf, int len, struct IKCPCB *kcp, void *user);

    void (*writelog)(const char *log, struct IKCPCB *kcp, void *user);
};
```
</details>

En annotant un par un les champs dans la structure KCP, on peut avoir l'impression que l'ensemble du protocole KCP n'est pas très complexe. En analysant le code en détail, nous pouvons tous deux lire et comprendre le protocole KCP. :smile:

##La mise en œuvre de l'ARQ de KCP

KCP intrinsèquement un protocole ARQ (Auto Repeat-reQuest, retransmission automatique) visant principalement à assurer une transmission fiable. Ainsi, nous allons d'abord nous concentrer sur la partie ARQ fondamentale de KCP et comment KCP réalise la transmission fiable.

ARQ, comme son nom l'indique, renvoie automatiquement les paquets de données correspondants lorsque nous pensons que la réception par l'autre extrémité a échoué. Cela garantit une transmission fiable grâce à la confirmation de réception et à la retransmission en cas de dépassement de délai. Dans l'implémentation du code spécifique, KCP attribue un identifiant unique "sn" à chaque paquet de données (également mentionné dans la section précédente comme étant un 'SEGMENT'). Une fois que l'autre extrémité reçoit le paquet de données, elle renvoie un paquet ACK (également un 'SEGMENT') avec le même "sn" que celui du paquet reçu, indiquant la réception réussie de ce paquet de données. Le 'SEGMENT' comporte également un champ "una" indiquant le numéro du prochain paquet de données attendu. En d'autres termes, tous les paquets de données avant ce numéro ont déjà été reçus, devenant ainsi un paquet ACK complet. Cela permet à l'émetteur de mettre à jour plus rapidement le tampon d'envoi et la fenêtre d'envoi.

Nous pouvons comprendre les bases de la mise en œuvre de l'ARQ en suivant le code d'envoi et de réception des paquets KCP.

###Envoyer

Le processus d'envoi se déroule comme suit : `ikcp_send` -> `ikcp_update` -> `ikcp_output`. L'appel supérieur à `ikcp_send` transmet les données à KCP, qui les traite pour l'envoi dans `ikcp_update`.

<details>
<summary> ikcp_send（cliquez pour développer le code） </summary>
```cpp
//---------------------------------------------------------------------
// Interface d'envoi de données, l'utilisateur appelle ikcp_send pour permettre à kcp d'envoyer des données
// user/upper level send, returns below zero for error
//---------------------------------------------------------------------
int ikcp_send(ikcpcb *kcp, const char *buffer, int len)
{
    IKCPSEG *seg;
    int count, i;

// mss ne peut pas être inférieur à 1
    assert(kcp->mss > 0);
    if (len < 0) return -1;

    // append to previous segment in streaming mode (if possible)
    if (kcp->stream != 0) {
// Traitement du mode flux
        // ......
    }

// Calcul des sous-paquets, si la longueur des données len est supérieure à mss, elle doit être divisée en plusieurs paquets pour être envoyée, l'autre partie les assemblera une fois reçus.
    if (len <= (int)kcp->mss) count = 1;
    else count = (len + kcp->mss - 1) / kcp->mss;

    if (count >= (int)IKCP_WND_RCV) return -2;

    if (count == 0) count = 1;

// Sous-traitance
    for (i = 0; i < count; i++) {
Calculer la longueur des données du paquet et allouer la structure seg correspondante
        int size = len > (int)kcp->mss ? (int)kcp->mss : len;
        seg = ikcp_segment_new(kcp, size);
        assert(seg);
        if (seg == NULL) {
            return -2;
        }

Définir les informations de données de seg, frg représente le numéro de fragmentation.
        if (buffer && len > 0) {
            memcpy(seg->data, buffer, size);
        }
        seg->len = size;
        seg->frg = (kcp->stream == 0)? (count - i - 1) : 0;

        // Ajoutez à la fin de snd_queue, nsnd_qua augmente de un
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

`ikcp_send` est l'interface d'envoi de données appelée par le niveau supérieur de KCP. Toutes les données à envoyer via KCP doivent passer par cette interface. Ce que fait `ikcp_send` est assez simple : il divise les données en plusieurs paquets selon `kcp->mss` (longueur maximale des données par paquet), attribue un numéro de sous-paquet, puis place le tout à la fin de la liste d'envoi `snd_queue`. En mode flux, les données provenant de plusieurs appels à `ikcp_send` sont considérées comme un flux unique, remplissant d'abord automatiquement les `SEGMENT` inachevés avant de répartir les nouveaux. Les détails de cette mise en œuvre ne seront pas discutés ici, mais ceux qui sont intéressés peuvent, après avoir lu cet article, se référer au code correspondant pour mieux comprendre.

Après l'appel à `ikcp_send`, les données sont placées dans la `snd_queue` de KCP. Ensuite, KCP doit trouver un moment pour envoyer les données en attente d'envoi ; tout ce code se trouve dans `ikcp_update` et `ikcp_flush`.

<details>
<summary> ikcp_mise_à_jour（Cliquez pour développer le code） </summary>
```cpp
//---------------------------------------------------------------------
// ikcp_update est une interface appelée périodiquement par le niveau supérieur, utilisée pour mettre à jour l'état de kcp et envoyer des données.
// update state (call it repeatedly, every 10ms-100ms), or you can ask 
// ikcp_check when to call it again (without ikcp_input/_send calling).
// 'current' - current timestamp in millisec. 
//---------------------------------------------------------------------
void ikcp_update(ikcpcb *kcp, IUINT32 current)
{
    IINT32 slap;

    kcp->current = current;

// ikcp_flush vérifiera cela, la couche supérieure doit avoir appelé ikcp_update avant de pouvoir appeler ikcp_flush, il est conseillé d'utiliser uniquement ikcp_update.
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
// Le temps de la prochaine exécution flush
        kcp->ts_flush += kcp->interval;
        if (_itimediff(kcp->current, kcp->ts_flush) >= 0) {
            kcp->ts_flush = kcp->current + kcp->interval;
        }
        ikcp_flush(kcp);
    }
}
```
</details>

`ikcp_update` fait des choses très simples, il vérifie le temps de `ts_flush`, si les conditions sont remplies alors il appelle `ikcp_flush`. La principale logique de traitement se trouve dans `ikcp_flush`, car le contenu de `ikcp_flush` est un peu plus complexe, nous nous concentrons actuellement uniquement sur la partie liée à l'envoi ARQ :

<details>
<summary> Envoyer des données (cliquez pour afficher le code) </summary>
```cpp
//---------------------------------------------------------------------
// ikcp_flush
//---------------------------------------------------------------------
void ikcp_flush(ikcpcb *kcp)
{
    IUINT32 current = kcp->current;

// Le tampon est une donnée à transmettre à ikcp_output, initialisé à 3 fois la taille du paquet de données.
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

// seg.wnd représente la taille actuelle de la fenêtre réceptrice.
    seg.wnd = ikcp_wnd_unused(kcp);
    seg.una = kcp->rcv_nxt;
    seg.len = 0;
    seg.sn = 0;
    seg.ts = 0;

// Envoyer un accusé de réception
Calcul de la fenêtre d'envoi
    //...

// Déplacer le paquet de données de snd_queue vers snd_buf
Le déplacement nécessite de respecter la taille de la fenêtre d'envoi. Lorsque la fenêtre d'envoi est pleine, le déplacement s'arrête.
// Les données placées à l'intérieur de snd_buf sont celles que vous pouvez directement envoyer à l'autre partie en appelant ikcp_output.
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

// seg is a unique identifier, essentially an increasing kcp->snd_nxt.
        newseg->sn = kcp->snd_nxt++;

// La variable una est définie ici pour informer l'autre extrémité du prochain numéro de séquence du paquet à recevoir.
        newseg->una = kcp->rcv_nxt;
        newseg->resendts = current;
        newseg->rto = kcp->rx_rto;
        newseg->fastack = 0;
        newseg->xmit = 0;
    }

// Calcul de l'indicateur de retransmission rapide, temps d'attente d'expiration
    // ...

// Envoyer snd_buf
    for (p = kcp->snd_buf.next; p != &kcp->snd_buf; p = p->next) {
        IKCPSEG *segment = iqueue_entry(p, IKCPSEG, node);
        int needsend = 0;
        if (segment->xmit == 0) {
// Première envoi
// set->xmit représente le nombre d'envois
// Le temps d'attente pour la retransmission en cas de dépassement du délai
            needsend = 1;
            segment->xmit++;
            segment->rto = kcp->rx_rto;
            segment->resendts = current + segment->rto + rtomin;
        }
        else if (_itimediff(current, segment->resendts) >= 0) {
Re-transmission en cas de dépassement du délai
            // ...
        }
        else if (segment->fastack >= resent) {
Requête de retransmission rapide
            // ...
        }

        if (needsend) {
            int need;
            segment->ts = current;
            segment->wnd = seg.wnd;
            segment->una = kcp->rcv_nxt;

            size = (int)(ptr - buffer);
            need = IKCP_OVERHEAD + segment->len;

// Chaque fois que les données dans le buffer dépassent le mtu, il faut les envoyer tout de suite, en essayant d'éviter le découpage au niveau inférieur.
            if (size + need > (int)kcp->mtu) {
                ikcp_output(kcp, buffer, size);
                ptr = buffer;
            }

// Copiez les données de contrôle seg dans le tampon, kcp gère lui-même les problèmes de endianess.
            ptr = ikcp_encode_seg(ptr, segment);

// Copie des données à nouveau
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

Calculer le seuil ssthresh, mettre à jour la taille de la fenêtre de congestion lente.
    // ...
}
```
</details>

Nous nous concentrons actuellement uniquement sur la logique d'envoi de données dans `ikcp_flush` :

Tout d'abord, KCP déplacera les données de `snd_queue` vers `snd_buf` en fonction de la taille de la fenêtre de réception de l'autre côté. La formule pour calculer le nombre de déplacements est `num = snd_nxt - (snd_una + cwnd)`, c'est-à-dire : si le numéro de séquence du maximum de paquets envoyés avec succès `snd_una` ajouté à la taille de la fenêtre glissante `cwnd` est supérieur au prochain numéro de paquet à envoyer `snd_nxt`, alors il est possible de continuer à envoyer de nouveaux paquets de données. En déplaçant le `SEG`, les champs de contrôle sont également définis.

* Parcourez `snd_buf`, si un paquet de données doit être envoyé, copiez les données dans `buffer`, tout en utilisant `ikcp_encode_seg` pour traiter les problèmes d'endianness des données de champ de contrôle.

* Enfin, appelez `ikcp_output` pour envoyer les données du `buffer`.

Jusqu'ici, KCP a terminé l'envoi des données.

###Réception

Le processus de réception est l'opposé de celui de l'envoi : `ikcp_input` -> `ikcp_update` -> `ikcp_recv`. Après que l'utilisateur ait reçu des données sur le réseau, il doit appeler `ikcp_input` pour les transmettre à KCP pour analyse. Lors de l'appel de `ikcp_update`, un paquet ACK est renvoyé à l'expéditeur. Le niveau supérieur reçoit les données après analyse par KCP en appelant `ikcp_recv`.

<details>
<summary> Recevoir des données (cliquez pour développer le code) </summary>
```cpp
//---------------------------------------------------------------------
// input data
//---------------------------------------------------------------------
int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    IUINT32 prev_una = kcp->snd_una;
    IUINT32 maxack = 0, latest_ts = 0;
    int flag = 0;

// Vérification de légalité
    if (data == NULL || (int)size < (int)IKCP_OVERHEAD) return -1;

// data peut être plusieurs paquets KCP, traitement en boucle
    while (1) {
        IUINT32 ts, sn, len, una, conv;
        IUINT16 wnd;
        IUINT8 cmd, frg;
        IKCPSEG *seg;

// Pas assez d'un paquet KCP, sortie
        if (size < (int)IKCP_OVERHEAD) break;

D'abord, analysez les champs de contrôle.
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

Vérification du type de paquet de données
        if (cmd != IKCP_CMD_PUSH && cmd != IKCP_CMD_ACK &&
            cmd != IKCP_CMD_WASK && cmd != IKCP_CMD_WINS) 
            return -3;

        kcp->rmt_wnd = wnd;

// Ici, "una" est le kcp->rcv_nxt de l'expéditeur. À partir de cette donnée, il est possible de supprimer les paquets de données qui ont été reçus et confirmés.
        ikcp_parse_una(kcp, una);
// Après avoir supprimé les paquets déjà confirmés comme reçus, mettre à jour le numéro de séquence snd_una du prochain paquet à envoyer.
        ikcp_shrink_buf(kcp);

        if (cmd == IKCP_CMD_ACK) {
// paquet ack
            // ...
        }
        else if (cmd == IKCP_CMD_PUSH) {
// Paquet de données
Si le numéro de séquence sn des paquets reçus se trouve dans la fenêtre de réception, il est traité normalement. Sinon, il est simplement rejeté en attendant d'être renvoyé.
            if (_itimediff(sn, kcp->rcv_nxt + kcp->rcv_wnd) < 0) {

Chaque paquet de données reçu doit être suivi d'un paquet d'accusé de réception pour enregistrer l'information.
                ikcp_ack_push(kcp, sn, ts);

// Les données reçues sont traitées par ikcp_parse_data
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
Veuillez traduire ce texte en français :

            // Package de fenêtre de requête
            // ...
        }
        else if (cmd == IKCP_CMD_WINS) {
// Paquet de réponse de la fenêtre de requête
            // ...
        }
        else {
            return -3;
        }

        data += len;
        size -= len;
    }

// Gérer la logique de retransmission rapide
    // ...

Mettre à jour la fenêtre d'envoi.
    // ...

    return 0;
}
```
</details>

`ikcp_input` traite chaque paquet `SEG` en vérifiant d'abord la légalité et le type du paquet, car chaque paquet contient `una`, qui stocke le numéro de séquence du paquet en attente de réception par l'expéditeur. Les paquets dont le numéro est inférieur à `una` ont déjà été acceptés par l'autre partie, il est donc possible de supprimer de `snd_buff` tous ceux qui doivent être inférieurs à `una` et de mettre à jour `snd_nxt`. Cette partie est gérée par `ikcp_parse_una` et `ikcp_shrink_buf`. Chaque paquet de données reçu nécessite de renvoyer un paquet ACK, qui est enregistré par `ikcp_ack_push`, et ensuite `ikcp_parse_data` est appelé pour traiter les données.

<details>
<summary> Analyser les données (cliquez pour développer le code) </summary>
```cpp
void ikcp_parse_data(ikcpcb *kcp, IKCPSEG *newseg)
{
    struct IQUEUEHEAD *p, *prev;
    IUINT32 sn = newseg->sn;
    int repeat = 0;

Vérification du numéro de séquence
    if (_itimediff(sn, kcp->rcv_nxt + kcp->rcv_wnd) >= 0 ||
        _itimediff(sn, kcp->rcv_nxt) < 0) {
        ikcp_segment_delete(kcp, newseg);
        return;
    }

// Trouver l'emplacement où newseg devrait être placé, car le seg reçu peut être désordonné.
    for (p = kcp->rcv_buf.prev; p != &kcp->rcv_buf; p = prev) {
        IKCPSEG *seg = iqueue_entry(p, IKCPSEG, node);
        prev = p->prev;
        if (seg->sn == sn) {
// Reçu en double
            repeat = 1;
            break;
        }
        if (_itimediff(sn, seg->sn) > 0) {
            break;
        }
    }

Placer le newseg à la bonne position dans rcv_buf.
    if (repeat == 0) {
        iqueue_init(&newseg->node);
        iqueue_add(&newseg->node, p);
        kcp->nrcv_buf++;
    }    else {
        ikcp_segment_delete(kcp, newseg);
    }

Déplacez les données de rcv_buf vers rcv_queue.
    while (! iqueue_is_empty(&kcp->rcv_buf)) {
        IKCPSEG *seg = iqueue_entry(kcp->rcv_buf.next, IKCPSEG, node);
// Si le numéro de séquence seg est le numéro d'attente de réception, déplacez-le vers rcv_queue
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

La fonction `ikcp_parse_data` a pour principal objectif de placer le segment `newseg` au bon endroit dans `kcp->rcv_buf` et de déplacer les données de `rcv_buf` vers `rcv_queue`. Le bon emplacement dans `rcv_buf` signifie que `rcv_buf` est trié par ordre croissant de `sn` et que `newseg` doit trouver sa place en fonction de sa propre valeur `sn`. Les données sur `rcv_buf` doivent être déplacées vers `rcv_queue` lorsque le numéro de séquence du paquet de données sur `rcv_buf` est égal au prochain numéro de séquence attendu par KCP, `kcp->rcv_nxt`. Après le déplacement d'un paquet de données, il est nécessaire de mettre à jour `kcp->rcv_nxt` avant de traiter le paquet de données suivant.

Après `ikcp_input`, lorsque la couche supérieure appelle `ikcp_update`, un paquet ACK sera envoyé, et l'appel à `ikcp_recv` renverra des données valides à la couche supérieure. `ikcp_update` et `ikcp_recv` sont indépendants l'un de l'autre et n'ont pas d'exigence de séquence d'appel, cela dépend du moment des appels de la couche supérieure. Examinons d'abord la partie concernant l'envoi d'ACK dans `ikcp_update` :

<details>
<résumé> Répondre ACK (cliquez pour afficher le code) </résumé>
```cpp
// Comme mentionné précédemment, ikcp_update appelle finalement ikcp_flush
void ikcp_flush(ikcpcb *kcp, IUINT32 current)
{
    // ...

Répondre au paquet ACK
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

Le paquet ACK a déjà été sauvegardé par `ikcp_ack_push`, donc ici il suffit d'utiliser `ikcp_ack_get` pour obtenir les informations de chaque paquet ACK et les envoyer à l'autre partie. La couche supérieure peut utiliser `ikcp_recv` pour recevoir des données de KCP :

<details>
ikcp_recv（cliquer pour afficher le code）
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

// Certaines vérifications de validité
    if (iqueue_is_empty(&kcp->rcv_queue))
        return -1;
    if (len < 0) len = -len;

Calculer la longueur des données pouvant être renvoyées
    peeksize = ikcp_peeksize(kcp);

    if (peeksize < 0)
        return -2;
    if (peeksize > len)
        return -3;

Vérifiez la taille de la fenêtre de réception.
    if (kcp->nrcv_que >= kcp->rcv_wnd)
        recover = 1;

// Parcourir rcv_queue et copier les données dans le buffer.
    for (len = 0, p = kcp->rcv_queue.next; p != &kcp->rcv_queue; ) {
        int fragment;
        seg = iqueue_entry(p, IKCPSEG, node);
        p = p->next;

        if (buffer) {
            memcpy(buffer, seg->data, seg->len);
            buffer += seg->len;
        }

        len += seg->len;

// Déterminer le sous-ensemble
        fragment = seg->frg;

Supprimer le paquet de données
        if (ispeek == 0) {
            iqueue_del(&seg->node);
            ikcp_segment_delete(kcp, seg);
            kcp->nrcv_que--;
        }

// Tous les sous-embouts sont copiés, quitter la boucle.
        if (fragment == 0)
            break;
    }

    assert(len == peeksize);

// rcv_queue s'est encore un peu vidé, essayons de continuer à déplacer de rcv_buf vers rcv_queue.
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

`ikcp_recv` est une fonction qui ne renvoie qu'un seul paquet de données complet à chaque appel. La couche supérieure peut l'appeler en boucle jusqu'à ce qu'il n'y ait plus de données à renvoyer. La logique de la fonction est assez simple, elle consiste à copier les données de `rcv_queue` dans le `buffer` fourni par la couche supérieure. À ce stade, le récepteur a déjà traité le paquet de données reçu.

Lorsque le destinataire traite le paquet de données, il envoie un paquet ACK à l'expéditeur. Voyons maintenant comment l'expéditeur gère la réception du paquet ACK :

<details>
<summary> Traitement des paquets ACK (cliquez pour développer le code) </summary>
```cpp
int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    // ...
    IUINT32 maxack = 0, latest_ts = 0;
    // ...
    while (1) {
        // ...
// ts est le kcp-> current de l'autre côté
        data = ikcp_decode32u(data, &ts);
        data = ikcp_decode32u(data, &sn);

        if (cmd == IKCP_CMD_ACK) {
Mettre à jour rot
            if (_itimediff(kcp->current, ts) >= 0) {
                ikcp_update_ack(kcp, _itimediff(kcp->current, ts));
            }
Mettre à jour snd_buf
            ikcp_parse_ack(kcp, sn);
            ikcp_shrink_buf(kcp);

maxack = le plus grand numéro de séquence parmi tous les paquets ACK de cette entrée
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

Si un paquet ACK est reçu, enregistrez-le pour effectuer une retransmission rapide.
    if (flag != 0) {
        ikcp_parse_fastack(kcp, maxack, latest_ts);
    }
}
```
</details>

On peut voir qu'après avoir reçu le paquet ACK, il est nécessaire d'utiliser `ikcp_parse_ack` et `ikcp_shrink_buf` pour mettre à jour `snd_buf`, en plus d'appeler `ikcp_update_ack` pour calculer le nouveau RTT (retransmission timeout, délai de retransmission). `ikcp_input` détermine le numéro de séquence le plus élevé dans le paquet ACK reçu, ce qui est enregistré pour un éventuel renvoi rapide. Ainsi, une fois que l'émetteur reçoit le paquet ACK, les données envoyées sont retirées de `snd_buf`, assurant ainsi que le paquet est bien reçu par le destinataire et que le cycle de confirmation de réception ARQ est achevé.

###Re-transmission en cas de dépassement du délai

Ce qui précède est le mécanisme de confirmation de réception dans l'ARQ mis en œuvre par KCP. L'ARQ nécessite également une retransmission en cas de dépassement de délai pour garantir la fiabilité. Voyons ci-dessous comment KCP gère la retransmission en cas de dépassement de délai.

Revenons à la fonction `ikcp_flush` :

<details>
<summary> Réexpédition en cas de délai d'attente (cliquez pour développer le code) </summary>
```cpp
void ikcp_flush(ikcpcb *kcp)
{
    // ...
// Envoyer snd_buf
    for (p = kcp->snd_buf.next; p != &kcp->snd_buf; p = p->next) {
        IKCPSEG *segment = iqueue_entry(p, IKCPSEG, node);
        int needsend = 0;
        if (segment->xmit == 0) {
// Première envoi
            needsend = 1;
            segment->xmit++;
            // Définir segment->rto
Calculez le temps de retransmission du segment->resendts en fonction de segment->rto.
            segment->rto = kcp->rx_rto;
            segment->resendts = current + segment->rto + rtomin;
        }
        else if (_itimediff(current, segment->resendts) >= 0) {
// Rétransmission après délai d'attente
            needsend = 1;
            segment->xmit++;
            kcp->xmit++;
Contrôle du calcul du temps de retransmission en cas de délai nul.
            if (kcp->nodelay == 0) {
                segment->rto += kcp->rx_rto;
            }    else {
                segment->rto += kcp->rx_rto / 2;
            }
            segment->resendts = current + segment->rto;
            lost = 1;
        }
        else if (segment->fastack >= resent) {
// Répétition rapide
            // ...
        }
        if (needsend) {
            // Envoyer des données
            // ...
        }
    // ...
}
```
</details>

Une fois que le temps actuel `current` dépasse le temps de retransmission de `segment->resendts`, cela signifie qu'aucun paquet ACK de la part du destinataire n'a été reçu pendant cette période, déclenchant le mécanisme de retransmission par timeout, `needsend = 1`, et les données doivent être renvoyées.

Avec les mécanismes de réception confirmée et de retransmission en cas de dépassement du délai, KCP peut garantir une transmission de données fiable de base. Cependant, pour maintenir un débit de données plus stable, KCP a effectué davantage d'optimisations. Jetons un œil aux autres améliorations apportées par KCP.

##Stratégie pour augmenter le débit KCP

###Rétransmission rapide

L'expéditeur a envoyé deux paquets de données, numérotés `sn` et `sn + 1`. Si seul l'ACK pour `sn + 1` a été reçu, cela pourrait être dû au fait que l'ACK pour `sn` n'est pas encore arrivé dans le réseau, ou que l'ACK a été perdu, ou que le paquet de données `sn` a été perdu. Si le délai de retransmission n'est pas encore atteint et que le réseau n'est pas encore trop encombré, mais que des pertes de paquets se produisent pour une raison quelconque, l'expéditeur peut choisir d'envoyer à nouveau le paquet de données `sn` de manière proactive, afin d'aider le récepteur à recevoir les données plus rapidement et d'augmenter le débit.

KCP met également en œuvre un mécanisme de retransmission rapide à l'intérieur de la fonction `ikcp_flush`.

<details>
<summary> Fast retransmission (click to expand code) </summary>
```cpp
void ikcp_flush(ikcpcb *kcp)
{
    // ...
    resent = (kcp->fastresend > 0)? (IUINT32)kcp->fastresend : 0xffffffff;

// Envoyer snd_buf
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
// Transmission rapide
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
            // Envoyer des données
            // ...
        }
    // ...
}
```
</details>

Pour une retransmission rapide au départ, deux conditions doivent être remplies :
* `segment->fastack >= resent`, resent est un paramètre configurable `kcp->fastresend`, configuré sur 0 désactive la retransmission rapide. `segment->fastack` est défini dans la fonction `ikcp_parse_fastack`, qui est appelée dans `ikcp_input`, et augmente `segment->fastack` de un pour tous les `sn` inférieurs à `maxack` calculé dans `ikcp_input`. Ainsi, `segment->fastack` représente le nombre de paquets reçus dont le numéro de séquence (sn) est supérieur.
Le texte à traduire en français est le suivant :

* `segment->xmit <= kcp->fastlimit || kcp->fastlimit <= 0`，`setgment->xmit` est le nombre d'envois, `kcp->fastlimit` est le nombre maximum configurable de retransmissions rapides, le nombre d'envois doit être inférieur au nombre maximum de retransmissions rapides.

Une fois que les conditions requises pour un accusé de réception rapide sont remplies, KCP procédera à l'accusé de réception rapide. Attention, l'accusé de réception rapide ne réinitialisera pas le délai de retransmission, le délai de retransmission d'origine restera en vigueur.

###Réduire le temps de retransmission des délais d'attente.

Le mécanisme de retransmission après expiration du délai est très utile, mais prend beaucoup de temps. Selon la stratégie TCP, le temps de retransmission après expiration du délai double à chaque fois, ce qui entraîne une augmentation rapide du temps d'attente. Pendant ce temps d'attente, il est probable que le récepteur ait épuisé sa fenêtre de réception, l'empêchant de recevoir de nouvelles données. De plus, le paquet à retransmettre se trouve en tête de file, ce qui signifie que le destinataire doit recevoir ce paquet avant de renvoyer toutes les données à la couche supérieure. Dans une telle situation, la vitesse du réseau est quasiment nulle. KCP propose une option de configuration pour ralentir la croissance du temps d'attente sans la doubler à chaque fois. En configurant `kcp->nodelay`, vous pouvez contrôler la croissance du temps d'attente pour qu'elle n'augmente que de 1 fois le RTO ou de 0,5 fois le RTO, ce qui permet de ralentir efficacement l'augmentation du temps d'attente et d'aider le réseau à retrouver rapidement sa vitesse.

###Fenêtre d'envoi de mise à jour

La fenêtre d'envoi représente le nombre de paquets de données transférés simultanément. Plus la fenêtre est grande, plus il y a de données transférées simultanément, une vitesse de transmission plus rapide. Cependant, une fenêtre trop grande peut entraîner une congestion du réseau, une augmentation du taux de perte de paquets, une augmentation des retransmissions de données et une diminution de la vitesse de transmission. Par conséquent, la fenêtre d'envoi doit être constamment mise à jour en fonction de la situation du réseau, progressivement approcher de l'optimum. Le code sur la fenêtre d'envoi dans KCP :

<details>
<summary>Envoyer la fenêtre (cliquez pour afficher le code)</summary>
```cpp
ikcpcb* ikcp_create(IUINT32 conv, void *user)
{
    // ...
// snd_wnd, rcv_wnd taille des buffer d'envoi et de réception
    kcp->snd_wnd = IKCP_WND_SND;    // 32
    kcp->rcv_wnd = IKCP_WND_RCV;    // 128
// Taille de la fenêtre de réception de l'autre extrémité              // 128
    kcp->rmt_wnd = IKCP_WND_RCV
Initialiser la fenêtre d'envoi cwnd à 0.
    kcp->cwnd = 0;
Transmettre la taille en octets de la fenêtre d'envoi, participant au calcul de la cwnd
    kcp->incr = 0
Seuil de démarrage lent
    kcp->ssthresh = IKCP_THRESH_INIT;
Le "nocwnd" est un paramètre configurable, avec 1 qui ne prend pas en compte le cwnd.
    kcp->nocwnd = 0;
    // ...
}

void ikcp_flush(ikcpcb *kcp)
{
    // ...
Lors de l'envoi de données, commencez par calculer la taille de la fenêtre d'envoi, qui est le minimum entre la taille du tampon d'envoi et la taille de la fenêtre de réception de l'autre partie.
    cwnd = _imin_(kcp->snd_wnd, kcp->rmt_wnd);
Il est également nécessaire de prendre en compte kcp->cwnd, qui est la fenêtre d'envoi en constante évolution.
    if (kcp->nocwnd == 0) cwnd = _imin_(kcp->cwnd, cwnd);

// Déplacer snd_queue vers snd_buf en fonction de la taille de cwnd
    while (_itimediff(kcp->snd_nxt, kcp->snd_una + cwnd) < 0) {
    }
Envoyez les données
    resent = (kcp->fastresend > 0)? (IUINT32)kcp->fastresend : 0xffffffff;
// Déclencher la retransmission de temporisation lost = 1
Déclencher la répétition rapide après un changement++

// Mettre à jour le seuil de démarrage lent et la fenêtre d'envoi
    if (change) {
Si un déclenchement de retransmission rapide se produit, la valeur de ssthresh est établie à la moitié du nombre de paquets en transit sur le réseau.
        IUINT32 inflight = kcp->snd_nxt - kcp->snd_una;
        kcp->ssthresh = inflight / 2;
        if (kcp->ssthresh < IKCP_THRESH_MIN)
            kcp->ssthresh = IKCP_THRESH_MIN;

// La fenêtre d'envoi est égale à la valeur du seuil plus les renvois liés à la retransmission rapide.
        kcp->cwnd = kcp->ssthresh + resent;
        kcp->incr = kcp->cwnd * kcp->mss;
    }

    if (lost) {
Si des retransmissions sont déclenchées en cas de dépassement de délai, cela déclenche un démarrage lent, avec le seuil ssthresh défini comme la moitié de la fenêtre d'envoi.
        kcp->ssthresh = cwnd / 2;
        if (kcp->ssthresh < IKCP_THRESH_MIN)
            kcp->ssthresh = IKCP_THRESH_MIN;
// Envoyer la fenêtre de retour à 1, redémarrer la croissance à un rythme lent
        kcp->cwnd = 1;
        kcp->incr = kcp->mss;
    }

    if (kcp->cwnd < 1) {
// Parce qu'il est initialisé à 0, il sera de nouveau réglé à 1 ici.
        kcp->cwnd = 1;
        kcp->incr = kcp->mss;
    }
}

int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    IUINT32 prev_una = kcp->snd_una;
// Traiter les données reçues

    while (1) {
        // ...
        data = ikcp_decode16u(data, &wnd)
// rmt_wnd est la taille de la fenêtre de réception de l'autre partie.
        kcp->rmt_wnd = wnd
        // ...
// Traitement des données
    }

// Dernière mise à jour de la fenêtre d'envoi
// kcp->snd_una - prev_una > 0, cela indique que cette fois l'input a reçu un ACK et que le tampon d'envoi snd_buf a changé.
    if (_itimediff(kcp->snd_una, prev_una) > 0) {
Vérifie à nouveau la fenêtre de réception de la partie opposée.
        if (kcp->cwnd < kcp->rmt_wnd) {
            IUINT32 mss = kcp->mss;

            if (kcp->cwnd < kcp->ssthresh) {
Lorsque la quantité de données est inférieure au seuil de démarrage lent, la croissance est doublée.
                kcp->cwnd++;
                kcp->incr += mss;

            }    else {
Lorsque le seuil de démarrage lent est dépassé, incr est mis à jour en utilisant la formule, puis cwnd est calculé.
                if (kcp->incr < mss) kcp->incr = mss;
                kcp->incr += (mss * mss) / kcp->incr + (mss / 16);
                if ((kcp->cwnd + 1) * mss <= kcp->incr) {
                    kcp->cwnd++;
                }
            }
// Les valeurs mises à jour doivent encore être comparées à rmt_wnd
            if (kcp->cwnd > kcp->rmt_wnd) {
                kcp->cwnd = kcp->rmt_wnd;
                kcp->incr = kcp->rmt_wnd * mss;
            }
        }
    }
}
```
</details>

La traduction en français du texte est la suivante :

La taille du fenêtre d'envoi `kcp->cwnd` nécessite un peu plus de code, car elle doit être mise à jour à la fois lors de l'envoi et de la réception de données. `kcp->cwnd` est initialisé à 0.
Ensuite, lors de la première invocation de `ikcp_flush`, si la valeur est inférieure à 1, elle sera modifiée à 1. Par la suite, l'expéditeur enverra un nombre correspondant de paquets de données en fonction de la taille de la fenêtre d'envoi, en attendant les ACK.
Traitez les paquets de réponse. Les paquets ACK sont traités dans `kcp->input`, si un paquet ACK est détecté dans `kcp->input` et qu'il y a une suppression des paquets de données envoyés dans le tampon d'envoi, cela signifie que les paquets de données ont été livrés avec succès, alors `kcp->cwnd++`. En réalité, il est très probable qu'un seul paquet ACK soit traité à chaque fois dans `kcp->input`. On peut dire que pour chaque ACK reçu, il y a `kcp->cwnd++`. Cette incrémentation implique un effet de doublement, par exemple si `kcp->cwnd = 2`, en envoyant deux paquets de données et en recevant deux ACK, cela déclenche deux incréments, aboutissant finalement à `kcp->cwnd = 4`, un doublement.

`cwnd` peut continuer à croître de manière exponentielle jusqu'à dépasser le seuil de démarrage lent, ou en cas de retransmission par timeout ou de retransmission rapide. Après une retransmission par timeout, le démarrage lent est déclenché, le seuil de démarrage lent `ssthresh = kcp->cwnd / 2`, la fenêtre d'envoi `kcp->cwnd = 1`, et on revient au début pour une nouvelle croissance exponentielle. En cas de retransmission rapide, KCP réduit d'abord `ssthresh`, c'est-à-dire qu'il réduit l'espace de croissance exponentielle de `cwnd`, ralentissant ainsi la vitesse de croissance et atténuant les problèmes de congestion.

KCP a également ajouté une configuration "nocwnd". Lorsque "nocwnd = 1", l'envoi de données ne tient plus compte de la taille de la fenêtre d'envoi. Il envoie directement le maximum de paquets de données qui peuvent être envoyés, répondant ainsi aux exigences du mode haute vitesse.

##Résumé

Cet article analyse simplement le code source de KCP et discute de l'implémentation de l'ARQ sur KCP, ainsi que de certaines stratégies pour améliorer le débit de KCP. Il reste de nombreux détails non abordés, ceux qui sont intéressés peuvent consulter le code source de KCP par eux-mêmes et s'attendre à en tirer également de nombreux apprentissages.

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT, veuillez laisser vos commentaires dans [**Feedback**](https://github.com/disenone/wiki_blog/issues/new)Veuillez signaler toute omission. 
