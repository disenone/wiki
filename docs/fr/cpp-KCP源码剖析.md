---
layout: post
title: Analyse du code source de KCP
categories:
- c++
catalog: true
tags:
- dev
description: Ce texte analyse brièvement le code source de KCP, discute de la mise
  en œuvre du ARQ sur KCP et de certaines stratégies pour améliorer le débit de KCP.
figures: []
---

<meta property="og:title" content="KCP 源码剖析" />

Avant de lire ce texte, si vous n'avez jamais entendu parler de KCP ou si vous ne connaissez pas du tout KCP, veuillez prendre un moment pour consulter la documentation du projet KCP : [lien](https://github.com/skywind3000/kcp)Le but de ce texte est d'approfondir les détails de mise en oeuvre du KCP pour en comprendre le fonctionnement.

##Qu'est-ce que le KCP ?

KCP est un protocole rapide et fiable qui permet de transmettre des données avec moins de latence que TCP, une retransmission plus rapide des données et un temps d'attente plus court.

> TCP est conçu pour le trafic (combien de KB de données peuvent être transférées par seconde), et vise à tirer pleinement parti de la bande passante. En revanche, KCP est conçu pour la vitesse de débit (combien de temps il faut pour qu'un paquet de données soit envoyé d'une extrémité à l'autre), sacrifiant 10 à 20 % de la bande passante pour une vitesse de transmission 30 à 40 % plus rapide que TCP. Le canal TCP est comme un grand canal avec un débit lent mais un fort volume de données par seconde, tandis que KCP est semblable à un petit cours d'eau en rapide turbulence.

Ce qui précède est ce qui est écrit dans la documentation de KCP, les mots clés sont **bande passante** et **débit**. KCP consommera de la bande passante, ce qui entraînera un taux de transfert plus important et plus équilibré. Pour plus d'explications, veuillez consulter la documentation de KCP elle-même.

##Structure de données KCP

Le code source de KCP se trouve dans les fichiers `ikcp.h` et `ikcp.c`. Le fichier `ikcp.h` contient principalement les déclarations des structures de données, en commençant par le paquet de données `SEGMENT`, qui est l'unité minimale du protocole KCP pour le traitement des données :

<details>
<summary> Structure SEGMENT (cliquez pour afficher le code) </summary>
```cpp
//=====================================================================
Un "SEGMENT" est simplement un paquet de données.
//=====================================================================
struct IKCPSEG
{
Noeud de liste chaînée, les files d'envoi et de réception sont toutes les structures de liste ici.
    struct IQUEUEHEAD node;

Numéro de conversation, le même numéro de conversation est identique.
    IUINT32 conv;

Type de paquet de données, comme DATA ou ACK.
    IUINT32 cmd;

En raison des limitations de l'unité de transfert maximale (MTU), les gros paquets de données seront divisés en plusieurs petits paquets, ceci est le numéro du petit paquet.
    IUINT32 frg

Chaque paquet de données est accompagné de la taille de la fenêtre de réception de l'émetteur.
    IUINT32 wnd;

Horodatage de l'envoi, défini comme le temps de paquet source si c'est un paquet ACK.
    IUINT32 ts;

Identifiant unique du paquet de données
    IUINT32 sn;

Tous les paquets de données inférieurs à una sont reçus avec succès, ce qui correspond à la signification TCP : le plus ancien numéro de séquence non acquitté SND.
    IUINT32 una;

Longueur des données
    IUINT32 len;

Délai de retransmission après expiration du délai
    IUINT32 resendts;

Prochain délai d'attente dépassé
    IUINT32 rto;

Renvoi rapide: un certain nombre de paquets reçus après ce paquet déclenchera le renvoi rapide.
    IUINT32 fastack;

Nombre d'envois
    IUINT32 xmit;

Translate these text into French language:

    // Données
    char data[1];
};
```
</details>

Après avoir lu les commentaires de `SEGMENT`, on peut comprendre que le cœur de KCP est essentiellement un protocole ARQ qui garantit la livraison des données en utilisant la retransmission automatique après expiration du délai. Ensuite, examinons la définition de la structure `KCPCB` de KCP.

<details>
Résumé: Structure KCP (cliquez pour afficher le code)
```cpp
//---------------------------------------------------------------------
// IKCPCB
//---------------------------------------------------------------------
struct IKCPCB
{
// numéro de session
// mtu, mss: Maximum Transmission Unit, Maximum Segment Size
// state: état de la session, 0 valide, -1 déconnecté
    IUINT32 conv, mtu, mss, state;

// snd_una: Wait for the packet number ACK
// snd_nxt : numéro du prochain paquet de données en attente à envoyer
// rcv_nxt: Le prochain numéro de séquence du paquet de données en attente de réception
    IUINT32 snd_una, snd_nxt, rcv_nxt;

// ts_recent, ts_lastack: Unused
ssthresh: Seuil de démarrage lent de contrôle de congestion
    IUINT32 ts_recent, ts_lastack, ssthresh;

// rx_rto : temps d'attente de retransmission (retransmission timeout),
// rx_rttval, rx_srtt, rx_minrto: Calcul des variables intermédiaires pour calculer le RTO
    IINT32 rx_rttval, rx_srtt, rx_rto, rx_minrto;

// snd_wnd, rcv_wnd : taille maximale des fenêtres d'envoi et de réception
// rmt_wnd: fenêtre distante, taille restante de la fenêtre de réception de l'extrémité opposée
    // cwnd: Taille de la fenêtre pouvant être envoyée
- Sonde : Indicateur indiquant si un message de contrôle doit être envoyé
    IUINT32 snd_wnd, rcv_wnd, rmt_wnd, cwnd, probe;

current: temps actuel
intervalle : mise à jour de l'intervalle
// ts_flush: Prochaine fois à laquelle la mise à jour est nécessaire
// xmit: Nombre d'échecs de transmission
    IUINT32 current, interval, ts_flush, xmit;

La longueur de la liste chaînée
    IUINT32 nrcv_buf, nsnd_buf;
    IUINT32 nrcv_que, nsnd_que;

// nodelay: Adjusts the growth rate of the RTO for timeout retransmission.
// mise à jour : Est-ce que ikcp_update a été appelé ?
    IUINT32 nodelay, updated;

// ts_probe, probe_wait: Si la fenêtre de réception du destinataire reste longtemps à 0, une vérification périodique sera activement lancée
    IUINT32 ts_probe, probe_wait;

// deal_link : Aucune réponse de l'autre partie pendant une longue période
// incr: Join the calculation of the sending window size
    IUINT32 dead_link, incr;

queue: les paquets de données en contact avec la couche utilisateur
// buf: Les paquets de données mis en cache par le protocole
    struct IQUEUEHEAD snd_queue;
    struct IQUEUEHEAD rcv_queue;
    struct IQUEUEHEAD snd_buf;
    struct IQUEUEHEAD rcv_buf;

Les informations des paquets de données qui nécessitent l'envoi d'un accusé de réception
    IUINT32 *acklist;

Le nombre de paquets nécessitant un accusé de réception.
    IUINT32 ackcount;

Taille de la liste de marques d'acquittement
    IUINT32 ackblock;

Les données transmises par la couche utilisateur.
    void *user;

Stockage de l'espace pour un paquet kcp
    char *buffer;

Nombre de fastack déclenché pour la retransmission rapide
    int fastresend;

Nombre maximal de retransmissions rapides
    int fastlimit;

// nocwnd: Taille de la fenêtre d'envoi sans tenir compte du démarrage lent
stream: mode de flux
    int nocwnd, stream;

    // debug log
    int logmask;

Interface d'envoi de données
    int (*output)(const char *buf, int len, struct IKCPCB *kcp, void *user);

    void (*writelog)(const char *log, struct IKCPCB *kcp, void *user);
};
```
</details>

Ajoutez des commentaires aux champs de la structure KCP un par un, vous aurez l'impression initiale que le protocole KCP dans son ensemble n'est pas trop compliqué. En analysant attentivement le code, nous pouvons tous comprendre et interpréter le protocole KCP :smile:

##La mise en œuvre du ARQ de KCP.

Le KCP est essentiellement un protocole ARQ (Auto Repeat-reQuest, demande de répétition automatique), dont l'objectif principal est d'assurer une transmission fiable. Ensuite, nous pouvons nous concentrer sur la partie ARQ de base du KCP, et comment le KCP garantit une transmission fiable.

ARQ, comme son nom l'indique, permet de renvoyer automatiquement les paquets de données correspondants lorsque l'on pense que la réception par l'autre extrémité a échoué. Il utilise deux mécanismes, la confirmation de la réception et la retransmission en cas de dépassement du délai, pour assurer une transmission fiable. Dans l'implémentation concrète du code, KCP attribue un identifiant unique `sn` à chaque paquet de données (appelé `SEGMENT` dans le paragraphe précédent). Lorsque l'autre extrémité reçoit un paquet de données, elle renvoie un paquet ACK (également un `SEGMENT`), dont le `sn` correspond à celui du paquet de données reçu, confirmant la réception réussie. Le `SEGMENT` comporte également un champ `una`, indiquant le numéro du prochain paquet de données attendu. En d'autres termes, tous les paquets de données jusqu'à ce numéro ont déjà été reçus, agissant comme un ACK complet. Cela permet à l'émetteur de mettre à jour plus rapidement le tampon d'envoi et la fenêtre d'envoi.

Nous pouvons comprendre la mise en œuvre la plus élémentaire de ARQ en suivant le code d'envoi et de réception des paquets KCP.

###Envoyer

Le processus d'envoi se déroule de la manière suivante : `ikcp_send` -> `ikcp_update` -> `ikcp_output`. L'appel de la couche supérieure à `ikcp_send` transmet les données à KCP, qui les traite pour l'envoi des données dans `ikcp_update`.

<details>
<summary> ikcp_send (click to expand code) </summary>
```cpp
//---------------------------------------------------------------------
// Interface d'envoi de données, les utilisateurs appellent ikcp_send pour que kcp envoie des données
// user/upper level send, returns below zero for error
//---------------------------------------------------------------------
int ikcp_send(ikcpcb *kcp, const char *buffer, int len)
{
    IKCPSEG *seg;
    int count, i;

Le mss ne peut pas être inférieur à 1.
    assert(kcp->mss > 0);
    if (len < 0) return -1;

    // append to previous segment in streaming mode (if possible)
    if (kcp->stream != 0) {
Mode de traitement de flux
        // ......
    }

Calcul des sous-emballages : si la longueur des données len dépasse mss, il est nécessaire de les diviser en plusieurs paquets à envoyer, puis de les reconstituer côté récepteur.
    if (len <= (int)kcp->mss) count = 1;
    else count = (len + kcp->mss - 1) / kcp->mss;

    if (count >= (int)IKCP_WND_RCV) return -2;

    if (count == 0) count = 1;

Sous-traitement
    for (i = 0; i < count; i++) {
Calculer la longueur des données du paquet et allouer la structure seg correspondante.
        int size = len > (int)kcp->mss ? (int)kcp->mss : len;
        seg = ikcp_segment_new(kcp, size);
        assert(seg);
        if (seg == NULL) {
            return -2;
        }

Configurer les informations de données de la segmentation, frg indique le numéro de fragmentation.
        if (buffer && len > 0) {
            memcpy(seg->data, buffer, size);
        }
        seg->len = size;
        seg->frg = (kcp->stream == 0)? (count - i - 1) : 0;

Ajoutez à la fin de snd_queue, puis incrémentez nsnd_qua de un.
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

`ikcp_send` est l'interface d'envoi appelée par la couche supérieure de KCP pour envoyer des données. Toutes les données à envoyer par KCP doivent passer par cette interface. `ikcp_send` fait simplement en sorte de diviser les données en plusieurs paquets en fonction de `kcp->mss` (la longueur maximale des données d'un paquet), en leur attribuant un numéro de paquet, puis les place à la fin de la file d'envoi `snd_queue`. Le mode de flux considère toutes les données envoyées à `ikcp_send` comme un seul flux, remplissant automatiquement les `SEGMENT` incomplets avant d'en allouer de nouveaux. Les détails de mise en œuvre ne sont pas abordés dans cet article, mais je suis convaincu que toute personne intéressée comprendra mieux en le lisant et en examinant le code correspondant.

Une fois l'appel à `ikcp_send` est achevé, les données sont placées dans la `snd_queue` de KCP. Ensuite, KCP doit trouver un moment pour envoyer les données en attente. Cette partie du code est contenue dans `ikcp_update` et `ikcp_flush`.


<details>
<summary> ikcp_update (tap to expand code) </summary>
```cpp
//---------------------------------------------------------------------
ikcp_update est une interface appelée régulièrement par la couche supérieure pour mettre à jour l'état de kcp et envoyer des données.
// update state (call it repeatedly, every 10ms-100ms), or you can ask 
// ikcp_check when to call it again (without ikcp_input/_send calling).
// 'current' - current timestamp in millisec. 
//---------------------------------------------------------------------
void ikcp_update(ikcpcb *kcp, IUINT32 current)
{
    IINT32 slap;

    kcp->current = current;

La fonction ikcp_flush vérifiera cela ; il est recommandé que la fonction ikcp_update soit appelée avant d'appeler ikcp_flush.
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
Prochain moment pour vider le cache.
        kcp->ts_flush += kcp->interval;
        if (_itimediff(kcp->current, kcp->ts_flush) >= 0) {
            kcp->ts_flush = kcp->current + kcp->interval;
        }
        ikcp_flush(kcp);
    }
}
```
</details>

La fonction `ikcp_update` effectue une tâche assez simple : elle vérifie l'horodatage de `ts_flush` et, si nécessaire, appelle `ikcp_flush`. L'essentiel du traitement se trouve dans la fonction `ikcp_flush`, où la logique est un peu plus complexe. Pour l'instant, nous nous concentrons uniquement sur les aspects liés à l'envoi ARQ.

<details>
<summary>Envoyer des données (cliquez pour afficher le code)</summary>
```cpp
//---------------------------------------------------------------------
// ikcp_flush
//---------------------------------------------------------------------
void ikcp_flush(ikcpcb *kcp)
{
    IUINT32 current = kcp->current;

Le "buffer" est la donnée à transmettre à "ikcp_output", initialisé à 3 fois la taille du paquet de données.
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

// seg.wnd représente la taille actuelle de la fenêtre de réception
    seg.wnd = ikcp_wnd_unused(kcp);
    seg.una = kcp->rcv_nxt;
    seg.len = 0;
    seg.sn = 0;
    seg.ts = 0;

Envoyer l'accusé de réception
Calcul de la fenêtre d'envoi
    //...

Déplacez le paquet de données de la file d'envoi (snd_queue) vers le tampon d'envoi (snd_buf).
Déplacer nécessite de satisfaire la taille de la fenêtre d'envoi. Lorsque la fenêtre d'envoi est pleine, le déplacement s'arrête.
Les données placées dans snd_buf sont les données qui peuvent être directement envoyées à la partie distante en appelant ikcp_output.
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

// seg - The unique identifier is essentially an incrementing value of kcp->snd_nxt.
        newseg->sn = kcp->snd_nxt++;

// Ici, l'una est défini pour informer l'autre partie du prochain numéro de séquence de paquet à attendre.
        newseg->una = kcp->rcv_nxt;
        newseg->resendts = current;
        newseg->rto = kcp->rx_rto;
        newseg->fastack = 0;
        newseg->xmit = 0;
    }

Calculer le drapeau de retransmission rapide et le temps d'attente d'expiration.
    // ...

// Envoyer snd_buf
    for (p = kcp->snd_buf.next; p != &kcp->snd_buf; p = p->next) {
        IKCPSEG *segment = iqueue_entry(p, IKCPSEG, node);
        int needsend = 0;
        if (segment->xmit == 0) {
Premier envoi.
// set->xmit 表示发送次数

// set->xmit représente le nombre d'envois
// Le temps d'attente pour le retransmission en cas de dépassement du délai
            needsend = 1;
            segment->xmit++;
            segment->rto = kcp->rx_rto;
            segment->resendts = current + segment->rto + rtomin;
        }
        else if (_itimediff(current, segment->resendts) >= 0) {
Re-transmission en cas de dépassement du délai.
            // ...
        }
        else if (segment->fastack >= resent) {
Renvoi rapide
            // ...
        }

        if (needsend) {
            int need;
            segment->ts = current;
            segment->wnd = seg.wnd;
            segment->una = kcp->rcv_nxt;

            size = (int)(ptr - buffer);
            need = IKCP_OVERHEAD + segment->len;

Chaque fois que les données du tampon dépassent l'unité de transfert maximale (MTU), elles sont envoyées en premier pour éviter autant que possible la fragmentation supplémentaire au niveau inférieur.
            if (size + need > (int)kcp->mtu) {
                ikcp_output(kcp, buffer, size);
                ptr = buffer;
            }

Copiez les données de contrôle de seg dans le tampon, laissez KCP traiter lui-même les problèmes de boutisme.
            ptr = ikcp_encode_seg(ptr, segment);

Copiez à nouveau les données
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

Calculer ssthresh, mettre à jour la fenêtre de démarrage lent.
    // ...
}
```
</details>

Nous nous concentrons actuellement uniquement sur la logique d'envoi des données dans `ikcp_flush`.

Tout d'abord, KCP déplacera les données de la file `snd_queue` vers le tampon `snd_buf` en fonction de la taille de la fenêtre de réception de l'autre extrémité. La formule pour calculer le nombre de données déplacées est `num = snd_nxt - (snd_una + cwnd)`. En d'autres termes, si le numéro de séquence maximal des paquets déjà envoyés, `snd_una`, augmenté de la taille de la fenêtre de congestion, `cwnd`, est supérieur au numéro de séquence du prochain paquet à envoyer, `snd_nxt`, alors il est possible de continuer à envoyer de nouvelles données. Pendant le déplacement des segments, les champs de contrôle sont définis.

Parcourir `snd_buf`, si un paquet de données doit être envoyé, copier les données dans le tampon (`buffer`) tout en gérant les problèmes de boutisme de données du champ de contrôle grâce à `ikcp_encode_seg`.

Finalement, appeler `ikcp_output` pour envoyer les données se trouvant sur le `buffer`.

Jusqu'ici, KCP a finalisé l'envoi des données.

###Recevoir

Le processus de réception est l'inverse de l'envoi : `ikcp_input` -> `ikcp_update` -> `ikcp_recv`. Une fois que l'utilisateur a reçu des données du réseau, il doit appeler `ikcp_input` pour les transmettre à KCP pour analyse. Lors de l'appel à `ikcp_update`, une réponse ACK est renvoyée à l'émetteur, et la couche supérieure récupère les données analysées par KCP en appelant `ikcp_recv`.

<details>
Résumé : Recevoir des données (Cliquez pour afficher le code)
```cpp
//---------------------------------------------------------------------
// input data
//---------------------------------------------------------------------
int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    IUINT32 prev_una = kcp->snd_una;
    IUINT32 maxack = 0, latest_ts = 0;
    int flag = 0;

Vérification de la légalité
    if (data == NULL || (int)size < (int)IKCP_OVERHEAD) return -1;

// Les données peuvent être plusieurs paquets KCP, traités en boucle
    while (1) {
        IUINT32 ts, sn, len, una, conv;
        IUINT16 wnd;
        IUINT8 cmd, frg;
        IKCPSEG *seg;

Insuffisant pour former un paquet KCP, sortie.
        if (size < (int)IKCP_OVERHEAD) break;

Translating the text into French:

// Tout d'abord, analysez les champs de contrôle.
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

Vérification du type de paquet de données.
        if (cmd != IKCP_CMD_PUSH && cmd != IKCP_CMD_ACK &&
            cmd != IKCP_CMD_WASK && cmd != IKCP_CMD_WINS) 
            return -3;

        kcp->rmt_wnd = wnd;

Ici, "una" fait référence à "kcp->rcv_nxt" de l'expéditeur, en fonction de ces données, il est possible d'éliminer les paquets déjà reçus et confirmés.
        ikcp_parse_una(kcp, una);
Après avoir supprimé les paquets déjà confirmés comme reçus, mettez à jour snd_una avec le prochain numéro de séquence à envoyer.
        ikcp_shrink_buf(kcp);

        if (cmd == IKCP_CMD_ACK) {
// paquet d'acquittement
            // ...
        }
        else if (cmd == IKCP_CMD_PUSH) {
// Paquet de données
Si le numéro de séquence du paquet de données reçu, noté sn, se trouve dans la fenêtre de réception, il est traité normalement. Sinon, il est tout simplement ignoré, en attente d'une retransmission.
            if (_itimediff(sn, kcp->rcv_nxt + kcp->rcv_wnd) < 0) {

Chaque paquet de données reçu doit être suivi d'un paquet ack pour enregistrer l'information.
                ikcp_ack_push(kcp, sn, ts);

// Les données reçues sont traitées en appelant ikcp_parse_data.
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
Recherche de la fenêtre de paquet
            // ...
        }
        else if (cmd == IKCP_CMD_WINS) {
Trouvez les réponses de la fenêtre de requête.
            // ...
        }
        else {
            return -3;
        }

        data += len;
        size -= len;
    }

Traiter la logique de retransmission rapide.
    // ...

Actualiser la fenêtre d'envoi
    // ...

    return 0;
}
```
</details>

Le `ikcp_input` boucle sur chaque segment `SEG`, vérifie d'abord la validité et le type du paquet de données, car chaque paquet de données contient un `una` qui contient le numéro de séquence des paquets que l'expéditeur attend de recevoir. Les paquets avec un numéro de séquence inférieur à `una` ont déjà été reçus avec succès par le destinataire. Ainsi, tous les éléments de `snd_buff` dont le numéro de séquence est inférieur à `una` peuvent être supprimés, et `snd_nxt` est mis à jour. Cette partie est gérée par `ikcp_parse_una` et `ikcp_shrink_buf`. Chaque paquet de données reçu nécessite une réponse ACK, enregistrée par `ikcp_ack_push`, et est ensuite traitée par l'appel à `ikcp_parse_data`.

<details>
Résumé: Analyser les données (cliquez pour afficher le code)
```cpp
void ikcp_parse_data(ikcpcb *kcp, IKCPSEG *newseg)
{
    struct IQUEUEHEAD *p, *prev;
    IUINT32 sn = newseg->sn;
    int repeat = 0;

Vérification du numéro de série.
    if (_itimediff(sn, kcp->rcv_nxt + kcp->rcv_wnd) >= 0 ||
        _itimediff(sn, kcp->rcv_nxt) < 0) {
        ikcp_segment_delete(kcp, newseg);
        return;
    }

Trouvez l'emplacement où le segment newseg doit être placé, car le segment reçu peut être désordonné.
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

Placer le newseg à l'emplacement correct du rcv_buf.
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
Si le numéro de séquence seg est celui en attente de réception, déplacez-le dans la file d'attente de réception.
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

La fonction principale de `ikcp_parse_data` est de placer `newseg` dans la position appropriée de `kcp->rcv_buf` et de déplacer les données de `rcv_buf` vers `rcv_queue`. La position appropriée dans `rcv_buf` signifie que `rcv_buf` est trié par ordre croissant de `sn`, et `newseg` doit trouver la position appropriée en fonction de sa propre valeur `sn`. Les données sur `rcv_buf` doivent être déplacées vers `rcv_queue` lorsque le numéro de séquence du paquet de données sur `rcv_buf` est égal au prochain numéro de séquence de paquet attendu par KCP, `kcp->rcv_nxt`. Après avoir déplacé un paquet de données, il est nécessaire de mettre à jour `kcp->rcv_nxt` avant de traiter le paquet de données suivant.

Après `ikcp_input`, lorsque vous appelez la fonction `ikcp_update`, un paquet ACK est envoyé, et en appelant `ikcp_recv`, des données valides sont renvoyées à la couche supérieure. Les fonctions `ikcp_update` et `ikcp_recv` sont indépendantes l'une de l'autre, il n'y a pas d'exigence d'ordre d'appel, cela dépend du moment où la couche supérieure les appelle. Examinons d'abord la partie de l'envoi des ACK dans la fonction `ikcp_update`:

<details>
<summary> Répondre ACK (cliquez pour afficher le code) </summary>
```cpp
Comme mentionné précédemment, ikcp_update appelle finalement ikcp_flush.
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

Les données ACK ont déjà été sauvegardées par `ikcp_ack_push` précédemment, donc ici il suffit d'utiliser `ikcp_ack_get` pour obtenir les informations de chaque paquet ACK et les envoyer à l'autre partie. Ensuite, l'application peut utiliser `ikcp_recv` pour récupérer des données depuis KCP :

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

Quelques vérifications de validité
    if (iqueue_is_empty(&kcp->rcv_queue))
        return -1;
    if (len < 0) len = -len;

Calculer la longueur des données pouvant être renvoyées.
    peeksize = ikcp_peeksize(kcp);

    if (peeksize < 0)
        return -2;
    if (peeksize > len)
        return -3;

Veuillez traduire ce texte en français :

    // 判断下接收窗口
    if (kcp->nrcv_que >= kcp->rcv_wnd)
        recover = 1;

Parcourir la file rcv_queue et copier les données dans le tampon.
    for (len = 0, p = kcp->rcv_queue.next; p != &kcp->rcv_queue; ) {
        int fragment;
        seg = iqueue_entry(p, IKCPSEG, node);
        p = p->next;

        if (buffer) {
            memcpy(buffer, seg->data, seg->len);
            buffer += seg->len;
        }

        len += seg->len;

Vérification du sous-ensemble
        fragment = seg->frg;

Supprimer le paquet de données.
        if (ispeek == 0) {
            iqueue_del(&seg->node);
            ikcp_segment_delete(kcp, seg);
            kcp->nrcv_que--;
        }

Toutes les sous-parties sont copiées, sortie de la boucle.
        if (fragment == 0)
            break;
    }

    assert(len == peeksize);

La file de rcv est à nouveau un peu vide, essayez de continuer à déplacer depuis rcv_buf vers rcv_queue.
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

`ikcp_recv` Une seule invocation renverra un paquet de données complet. La couche supérieure peut appeler en boucle jusqu'à ce qu'aucune donnée ne soit renvoyée. La logique de la fonction est plutôt simple : elle copie les données de la `rcv_queue` dans le `buffer` fourni par la couche supérieure. À ce stade, le destinataire a terminé le traitement du paquet reçu.

Lorsque le destinataire traite le paquet de données, il envoie un accusé de réception à l'expéditeur. Voyons maintenant comment l'expéditeur gère la réception de cet accusé de réception (ACK).

<details>
<summary>TRAITEMENT DU PAQUET ACK (CLIQUEZ POUR AFFICHER LE CODE)</summary>
```cpp
int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    // ...
    IUINT32 maxack = 0, latest_ts = 0;
    // ...
    while (1) {
        // ...
// ts corresponds to the peer's kcp-> current
        data = ikcp_decode32u(data, &ts);
        data = ikcp_decode32u(data, &sn);

        if (cmd == IKCP_CMD_ACK) {
Mettre à jour rot
            if (_itimediff(kcp->current, ts) >= 0) {
                ikcp_update_ack(kcp, _itimediff(kcp->current, ts));
            }
Actualiser le snd_buf.
            ikcp_parse_ack(kcp, sn);
            ikcp_shrink_buf(kcp);

// maxack = Le plus grand numéro de séquence parmi tous les paquets ACK de cette entrée
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

On peut voir que, une fois le paquet ACK reçu, il est nécessaire d'utiliser `ikcp_parse_ack` et `ikcp_shrink_buf` pour mettre à jour `snd_buf`, puis d'appeler `ikcp_update_ack` pour calculer et mettre à jour le RTT (retransmission timeout, délai de retransmission). `ikcp_input` calcule le numéro de séquence le plus élevé reçu dans le paquet ACK pour être utilisé dans le mécanisme de retransmission rapide. Ainsi, lorsque l'émetteur reçoit un paquet ACK, il supprime les données à envoyer de `snd_buf`, garantissant ainsi que le paquet de données est bien reçu par le destinataire, marquant ainsi la fin d'une procédure complète de confirmation ARQ.

###Retransmission après délai écoulé

Le texte mentionne le mécanisme de confirmation de réception dans le ARQ mis en œuvre par KCP. Le ARQ nécessite également une retransmission après expiration d'un délai pour garantir la fiabilité. Voyons maintenant comment KCP gère les retransmissions en cas de dépassement de délai.

Revenons à la fonction "ikcp_flush" :

<details>
Résumé: Retransmission après délai dépassé (cliquez pour afficher le code)
```cpp
void ikcp_flush(ikcpcb *kcp)
{
    // ...
// Envoyer snd_buf
    for (p = kcp->snd_buf.next; p != &kcp->snd_buf; p = p->next) {
        IKCPSEG *segment = iqueue_entry(p, IKCPSEG, node);
        int needsend = 0;
        if (segment->xmit == 0) {
Premier envoi
            needsend = 1;
            segment->xmit++;
Définir segment->rto
Calculer le temps de retransmission par délai d'attente du segment->rto pour le segment->resendts.
            segment->rto = kcp->rx_rto;
            segment->resendts = current + segment->rto + rtomin;
        }
        else if (_itimediff(current, segment->resendts) >= 0) {
Re-transmission en cas de dépassement du délai
            needsend = 1;
            segment->xmit++;
            kcp->xmit++;
Le texte traduit en français est le suivant :

// Calcul du temps de retransmission suivant sous contrôle de non-délai
            if (kcp->nodelay == 0) {
                segment->rto += kcp->rx_rto;
            }    else {
                segment->rto += kcp->rx_rto / 2;
            }
            segment->resendts = current + segment->rto;
            lost = 1;
        }
        else if (segment->fastack >= resent) {
Retransmission rapide.
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

Une fois que l'heure actuelle `current` est supérieure à l'heure de retransmission `segment->resendts`, ce qui signifie qu'aucun paquet ACK n'a été reçu de la part du destinataire pendant cette période, déclenche le mécanisme de retransmission en cas de dépassement du délai, `needsend = 1`, et retransmet les données.

Avec des mécanismes de confirmation de réception et de retransmission en cas de dépassement du délai, KCP peut garantir une transmission de données fiable de base. Toutefois, pour maintenir un débit plus stable, KCP a également réalisé plus d'optimisations. Regardons ensemble quelles autres améliorations KCP a apportées.

##Stratégie d'augmentation de la vitesse de flux de KCP

###Reprise rapide

Le sender a envoyé les paquets de données numérotés `sn` et `sn + 1`. S'il ne reçoit que le ACK du `sn + 1`, cela peut être dû au fait que le ACK du `sn` n'est pas encore arrivé dans le réseau, ou qu'il a été perdu, ou que le paquet `sn` a été perdu. S'il n'est pas encore l'heure de retransmettre suite à un dépassement du délai, que le réseau n'est pas encore trop encombré, mais qu'il y a eu une perte soudaine pour une raison quelconque, le sender peut alors envoyer activement le paquet `sn` en avance pour aider le receiver à recevoir les données plus rapidement et à augmenter le débit.

KCP a également mis en œuvre un mécanisme de retransmission rapide à l'intérieur et se trouve également dans `ikcp_flush`:

<details>
<summary>Fast retransmission (click to expand code)</summary>
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
// Requête de retransmission rapide
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
Envoyer des données
            // ...
        }
    // ...
}
```
</details>

Pour démarrer une retransmission rapide, il y a deux conditions :
`segment->fastack >= resent`, resent is a configurable parameter `kcp->fastresend`, setting it to 0 will disable fast retransmission. `segment->fastack` is set within the function `ikcp_parse_fastack`, which is called within `ikcp_input`. It increments the `segment->fastack` for all `sn` less than `maxack` calculated by `ikcp_input`, indicating the number of packets received larger than `sn`.
Translate these text into French language:

* `segment->xmit <= kcp->fastlimit || kcp->fastlimit <= 0`，`setgment->xmit` is the number of transmissions, `kcp->fastlimit` is the configurable maximum number of fast retransmissions, the number of transmissions must be less than the maximum number of fast retransmissions.

Une fois que les conditions pour la retransmission rapide sont remplies, le KCP effectuera la retransmission rapide. Il est à noter que la retransmission rapide ne réinitialisera pas le temps de retransmission d'expiration, le temps d'expiration initial restera toujours en vigueur.

###Réduire le temps de retransmission en cas de dépassement du délai.

Le mécanisme de retransmission après expiration du délai est vraiment efficace, mais ça prend juste beaucoup de temps. Selon la stratégie de TCP, le temps de retransmission après expiration du délai double à chaque fois, ce qui fait que l'attente s'étend rapidement. Pendant cette attente, il est très probable que, à cause de l'épuisement de la fenêtre de réception côté destinataire, il ne puisse pas recevoir de nouvelles données. De plus, le numéro de séquence du paquet en attente de retransmission est en première position. Le destinataire doit recevoir ce paquet retransmis pour renvoyer toutes les données à la couche supérieure. Dans ce cas, le débit de l'ensemble du réseau est presque nul. KCP introduit une option de configuration pour ralentir la croissance du temps d'attente et cela ne doublera pas non plus. En configurant `kcp->nodelay`, on peut contrôler que le temps d'attente ne croîtra que d'un facteur de 1 fois le RTO ou 0.5 fois le RTO, ce qui réduit efficacement la croissance du temps d'attente et aide le réseau à retrouver rapidement son débit.

###Mettre à jour la fenêtre d'envoi.

La fenêtre d'envoi fait référence au nombre de paquets de données transmis simultanément. Plus la fenêtre est grande, plus il y a de données transmises simultanément, une vitesse de transmission plus élevée. Cependant, si la fenêtre est trop grande, cela peut entraîner des congestions réseau, une augmentation du taux de perte de paquets, une augmentation des retransmissions de données et une baisse de la vitesse de transmission. Par conséquent, la fenêtre d'envoi doit être continuellement mise à jour en fonction de la situation du réseau, se rapprochant progressivement de l'optimum. Le code relatif à la fenêtre d'envoi dans KCP :

<details>
<summary> Send window (click to expand code) </summary>
```cpp
ikcpcb* ikcp_create(IUINT32 conv, void *user)
{
    // ...
snd_wnd，rcv_wnd sont les tailles des buffers d'envoi et de réception.
    kcp->snd_wnd = IKCP_WND_SND;    // 32
    kcp->rcv_wnd = IKCP_WND_RCV;    // 128
// Taille de la fenêtre de réception du côté distant              // 128
    kcp->rmt_wnd = IKCP_WND_RCV
Initialiser la fenêtre d'envoi cwnd à 0.
    kcp->cwnd = 0;
Transmettre la taille en octets de la fenêtre d'envoi pour le calcul de cwnd.
    kcp->incr = 0
Seuil de démarrage lent.
    kcp->ssthresh = IKCP_THRESH_INIT;
Le « nocwnd » est un paramètre configurable, avec 1 signifiant qu'on ne considère pas le Cwnd.
    kcp->nocwnd = 0;
    // ...
}

void ikcp_flush(ikcpcb *kcp)
{
    // ...
Lors de l'envoi de données, commencez par calculer la taille de la fenêtre d'envoi, qui est le minimum entre la taille du tampon d'envoi et la taille de la fenêtre de réception du destinataire.
    cwnd = _imin_(kcp->snd_wnd, kcp->rmt_wnd);
Il est également nécessaire de prendre en compte kcp->cwnd, qui est la fenêtre d'envoi constamment mise à jour.
    if (kcp->nocwnd == 0) cwnd = _imin_(kcp->cwnd, cwnd);

Selon la taille de cwnd, move snd_queue vers snd_buf.
    while (_itimediff(kcp->snd_nxt, kcp->snd_una + cwnd) < 0) {
    }
Envoyer des données
    resent = (kcp->fastresend > 0)? (IUINT32)kcp->fastresend : 0xffffffff;
Déclencher la retransmission dû à un délai dépassé, lost = 1
Déclencher la retransmission rapide changement++

Modifier le seuil de démarrage lent et la fenêtre d'envoi.
    if (change) {
Si une retransmission rapide est déclenchée, la valeur de seuil de congestion (ssthresh) est définie à la moitié du nombre de paquets en cours de transmission sur le réseau.
        IUINT32 inflight = kcp->snd_nxt - kcp->snd_una;
        kcp->ssthresh = inflight / 2;
        if (kcp->ssthresh < IKCP_THRESH_MIN)
            kcp->ssthresh = IKCP_THRESH_MIN;

// Envoyer la fenêtre est égale à la valeur seuil plus les réémissions liées à la retransmission rapide.
        kcp->cwnd = kcp->ssthresh + resent;
        kcp->incr = kcp->cwnd * kcp->mss;
    }

    if (lost) {
Si des retransmissions dues à des délais surviennent, cela déclenche le démarrage lent, et le seuil ssthresh est défini comme la moitié de la fenêtre d'envoi.
        kcp->ssthresh = cwnd / 2;
        if (kcp->ssthresh < IKCP_THRESH_MIN)
            kcp->ssthresh = IKCP_THRESH_MIN;
Réglez la fenêtre d'envoi à 1 pour reprendre la croissance lente de la phase de démarrage.
        kcp->cwnd = 1;
        kcp->incr = kcp->mss;
    }

    if (kcp->cwnd < 1) {
Étant donné que l'initialisation est de 0, elle sera réinitialisée à 1 lorsqu'elle arrivera ici.
        kcp->cwnd = 1;
        kcp->incr = kcp->mss;
    }
}

int ikcp_input(ikcpcb *kcp, const char *data, long size)
{
    IUINT32 prev_una = kcp->snd_una;
Traiter les données reçues

    while (1) {
        // ...
        data = ikcp_decode16u(data, &wnd)
// rmt_wnd est la taille de la fenêtre de réception de l'autre partie.
        kcp->rmt_wnd = wnd
        // ...
Traiter les données
    }

// Mettre à jour la fenêtre d'envoi
kcp->snd_una - prev_una > 0, indicates that this input has received an ACK and the sending buffer snd_buf has changed.
    if (_itimediff(kcp->snd_una, prev_una) > 0) {
// Reconsidérez ensuite la fenêtre de réception de la partie opposée
        if (kcp->cwnd < kcp->rmt_wnd) {
            IUINT32 mss = kcp->mss;

            if (kcp->cwnd < kcp->ssthresh) {
Lorsque le seuil de démarrage lent est dépassé, la croissance est doublée.
                kcp->cwnd++;
                kcp->incr += mss;

            }    else {
Une fois que la valeur dépasse le seuil de démarrage lent, incr est mis à jour selon une formule pour calculer ensuite cwnd.
                if (kcp->incr < mss) kcp->incr = mss;
                kcp->incr += (mss * mss) / kcp->incr + (mss / 16);
                if ((kcp->cwnd + 1) * mss <= kcp->incr) {
                    kcp->cwnd++;
                }
            }
Les valeurs mises à jour doivent encore être comparées à rmt_wnd.
            if (kcp->cwnd > kcp->rmt_wnd) {
                kcp->cwnd = kcp->rmt_wnd;
                kcp->incr = kcp->rmt_wnd * mss;
            }
        }
    }
}
```
</details>

Calculer la taille de la fenêtre d'envoi `kcp->cwnd` implique quelques morceaux de code supplémentaires, car des mises à jour seront nécessaires lors de l'envoi et de la réception de données. `kcp->cwnd` est initialement fixé à 0.
Lors du premier appel à `ikcp_flush`, si la valeur est inférieure à 1, elle sera modifiée à 1. Ensuite, l'émetteur enverra un nombre correspondant de paquets de données en fonction de la taille de la fenêtre d'envoi, puis attendra l'ACK.
Répondre au paquet. Les paquets ACK sont traités dans `kcp->input`. Si un paquet ACK est identifié dans `kcp->input` et que des données de transmission ont été effacées du tampon d'envoi, cela signifie qu'un paquet de données a été correctement livré. En conséquence, `kcp->cwnd++`. En réalité, il est très probable qu'un seul paquet ACK soit traité à la fois dans `kcp->input`. On peut considérer que chaque réception d'un paquet ACK entraîne `kcp->cwnd++`. Cette incrémentation implémente en fait un effet de doublement ; par exemple, si `kcp->cwnd = 2` actuellement, envoi de deux paquets de données, réception de deux paquets ACK déclenchant deux incréments, le résultat final sera que `kcp->cwnd = 4`, soit un doublement.

Le `cwnd` peut continuer à augmenter de manière exponentielle jusqu'à dépasser le seuil de démarrage lent, ou en cas de dépassement du délai de congestion ou de retransmission rapide. Après un dépassement du délai de congestion, le démarrage lent est déclenché, avec un seuil de démarrage lent `ssthresh = kcp->cwnd / 2`, une fenêtre d'envoi `kcp->cwnd = 1`, revenant à une croissance exponentielle initiale. En cas de retransmission rapide, KCP diminue d'abord `ssthresh`, réduisant ainsi l'espace de croissance exponentielle de `cwnd` et ralentissant la vitesse de croissance pour atténuer précocément les congestions.

KCP a également ajouté une configuration `nocwnd`, lorsque `nocwnd = 1`, l'envoi des données ne tient plus compte de la taille de la fenêtre d'envoi, mais envoie directement le nombre maximum de paquets pouvant être envoyés, répondant ainsi aux exigences du mode de haute vitesse.

##Résumé

Ce texte analyse simplement le code source de KCP et aborde la mise en œuvre de l'ARQ sur KCP, ainsi que certaines stratégies pour améliorer le débit de KCP. Il y a encore beaucoup de détails non mentionnés, ceux qui sont intéressés peuvent consulter le code source de KCP et le comparer pour eux-mêmes, je suis sûr qu'ils en retireront de nombreux bénéfices.

--8<-- "footer_fr.md"


> Ce message a été traduit en utilisant ChatGPT. Veuillez laisser vos commentaires dans la section de [**feedback**](https://github.com/disenone/wiki_blog/issues/new)Veuillez signaler tout oubli. 
