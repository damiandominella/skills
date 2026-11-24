# Integrazione CSI

> [!NOTE] Questa funzionalità è in **BETA**.

L'integrazione con il CSI permette di:

- collegare Golee al portale dei tesseramenti CSI con le stesse credenziali della società;
- importare e aggiornare in Golee i tesseramenti presenti sul portale;
- emettere una tessera CSI dal profilo di una persona, nuova o in rinnovo;
- scaricare il modulo 2T di una tessera certificata.

> [!INFO] La sincronizzazione legge il portale e scrive solo in Golee. L'emissione fa il contrario: crea una tessera reale sul portale e ne scala il credito.

## In questo articolo

- [Integrazione CSI](#integrazione-csi)
    - [In questo articolo](#in-questo-articolo)
    - [Prima di iniziare](#prima-di-iniziare)
    - [Come collegare Golee al portale CSI](#come-collegare-golee-al-portale-csi)
        - [Scollegare l'account](#scollegare-laccount)
    - [Come emettere una tessera CSI](#come-emettere-una-tessera-csi)
    - [Problemi comuni](#problemi-comuni)

## Prima di iniziare

Assicurati che:

- il CSI sia presente tra le federazioni della società;
- tu abbia le credenziali usate per accedere al portale dei tesseramenti CSI;
- le anagrafiche dei tesserati abbiano un codice fiscale valido.

> [!DASHED] senza il CSI tra le federazioni della società, o senza i permessi per gestire federazioni e tesseramenti, non vedi le azioni di collegamento, sincronizzazione ed emissione.

## Come collegare Golee al portale CSI

Vai in: **La tua società > Club > Federazioni ed Enti**.

Dalla scheda del CSI, seleziona **Collegati al portale ufficiale** e compila:

- **Codice di accesso società**: il codice numerico di 8 cifre usato sul portale CSI.
- **Comitato**: il codice di 3 cifre del Comitato CSI.
- **Password**: la stessa password usata sul portale dei tesseramenti.

Password dimenticata? Puoi richiederla dal [portale ufficiale CSI](https://tesseramento.csi-net.it/S_Accesso.asp).

### Scollegare l'account

Dal menu della scheda CSI collegata, seleziona **Scollega dal portale**. Le credenziali salvate vengono eliminate.

## Come emettere una tessera CSI

> [!WARNING] L'emissione crea una tessera reale sul portale CSI e scala il relativo credito. Si fa dal profilo della persona, uno alla volta.

Apri il profilo e vai alla sezione **Tesseramento**. Dal pulsante + scegli **Tessera ufficialmente** e seleziona il CSI.

L'anagrafica deve contenere:

1. codice fiscale;
2. data e luogo di nascita;
3. sesso.

> [!DASHED] un'emissione confermata non può essere annullata da Golee. Per correggere o annullare una tessera sul portale devi contattare il tuo Comitato CSI.

## Problemi comuni

### Le credenziali non vengono accettate

Controlla codice di accesso, Comitato e password. Finché la verifica fallisce, Golee non salva le credenziali.

### Il portale non è raggiungibile

Golee non riesce a parlare con il CSI in quel momento. Riprova. Se l'errore arriva dopo **Calcola costo**, i dati restano in maschera.
