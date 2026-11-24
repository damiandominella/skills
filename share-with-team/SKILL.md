---
name: share-with-team
description: Turn an agentic coding session into a ready-to-paste Discord message for Golee's @role_product channel, in Damian's established technical-sharing voice. Use this skill EVERY TIME the user wants to communicate to the team what was just built, refactored, or discovered in code. Triggers include "/share-with-team", "condividi col team", "scrivi il messaggio per il team", "messaggio discord", "comunica questa cosa al team", "spiega al team cosa ho fatto", "share this with the team", "write it up for the channel", or whenever the user finishes a piece of technical work and asks whether/how to communicate it. Input is the current coding session (git diff, files touched, decisions made in the conversation); output is a single Italian Discord message, focused on ONE topic, with real before/after code from the repo.
---

# Share with team (Discord @role_product)

Trasforma una sessione di coding in un messaggio Discord per il canale prodotto di Golee. Il pubblico è misto (prodotto + eng): capiscono il dominio e il codebase, ma non hanno seguito la sessione.

L'obiettivo non è "riportare cosa ho fatto". È **far sì che chi legge sappia usare la cosa, o sappia che esiste un vincolo nuovo**. Se dopo aver letto il messaggio il team non può fare niente di diverso da prima, il messaggio non serviva.

## Step 1 — Scegli UN argomento (non saltare questo step)

Una sessione agentica tocca 10 file e risolve 4 cose. Il messaggio ne racconta **una**.

Criterio di selezione, in ordine:

1. **Cambia il modo in cui gli altri scrivono codice?** (nuovo pattern, nuova prop, nuovo componente da usare, breaking change nell'output di qualcosa) → questo vince sempre.
2. **Cambia il modo in cui gli altri lavorano?** (nuovo script da lanciare, nuova convenzione, nuovo posto dove guardare)
3. **È una scoperta / un rischio che gli altri devono conoscere?** (comportamento inaspettato, debito che abbiamo appena visto, limite di un sistema)
4. **È un miglioramento visibile che qualcuno aveva chiesto?**

Bugfix di routine, refactor invisibili, dipendenze aggiornate, test aggiunti: **non sono messaggi**. Al massimo diventano una riga dentro un messaggio più grande ("e ho aggiunto un accenno di test").

Se la sessione contiene genuinamente 2+ cose da tier 1-3, non fonderle. Elenca all'utente cosa hai trovato e chiedi quale raccontare, oppure proponi due messaggi separati.

Se non c'è niente sopra il tier 4, dillo: "questa sessione non ha molto da condividere, è tutta roba interna. Vuoi che lo scriva lo stesso?". Meglio non mandare un messaggio che mandarne uno inutile.

## Step 2 — Raccogli il materiale dal repo, non dall'utente

Non chiedere all'utente di rispiegare cosa ha fatto. È dentro la sessione. Ricostruisci da:

```bash
git diff HEAD           # o git diff main...HEAD se sei su branch
git diff --stat
git log --oneline -15
```

Ti servono, per l'argomento scelto:
- Il **codice prima** (dal diff, le righe rimosse) e il **codice dopo** (righe aggiunte), con i nomi file reali.
- Il **motivo** della modifica: cercalo nella conversazione della sessione, nel ticket, nel commit message.
- **Come si usa** la cosa nuova: la firma reale, la prop reale, il comando reale.
- **Cosa NON copre**: casi esclusi di proposito, parti legacy non toccate, feature flag, rollout graduale.

I frammenti di codice nel messaggio devono essere **codice vero del repo**, accorciato ma non inventato. Mai pseudocodice, mai `// ... resto della logica`. Se un file è troppo lungo, taglia alle righe che dimostrano il punto e tieni il nome file in un commento sopra.

## Step 3 — Scegli la forma

Tre forme ricorrenti. Riconosci quale calza, non forzarle tutte e tre.

### Forma A — Refactor / riscrittura di un pattern
Quando hai unificato o semplificato qualcosa che prima era gestito in N modi diversi.

```
@role_product [apertura colloquiale + cosa hai toccato]

[L'obiettivo, 1 frase]

Il problema di prima
[Elenco puntato di come era gestita la cosa, in modi incoerenti]

[1-2 frasi su cosa questo causava: duplicazione, prop drilling, comportamenti diversi a parità di schermata]

Cosa ho fatto
[Il nuovo pattern, in 2-4 blocchi. Ogni blocco: nome della decisione in grassetto o a inizio riga, poi spiegazione con esempi tra parentesi]

Perché è meglio
[Il confronto strutturale: prima ogni X doveva sapere Y, ora no. Chiudi sul numero: "un solo fallbackTo invece di N configurazioni per N percorsi"]
```

L'esempio concreto prima/dopo, se è lungo, va in un **secondo messaggio** separato (vedi sotto).

### Forma B — Nuova capability / API interna
Quando hai aggiunto qualcosa che gli altri useranno.

```
@role_product [apertura + cosa hai fatto]

[Contesto breve: da dove nasce, richiesta di chi, cosa c'era già parzialmente]

Cosa è cambiato a livello tecnico:
[Punto 1: la generalizzazione fatta]
[Punto 2: il pezzo nuovo, con snippet di utilizzo reale]

[Snippet: come si usa, copiabile]

[Dettagli su cosa succede dietro le quinte, 1-2 frasi]

Cosa viene [ricordato/coperto]: [elenco inline]
Cosa NON viene [ricordato/coperto] di proposito: [elenco inline + motivo]

nota: [il caso non coperto, il legacy, il debito che resta]
```

### Forma C — Heads-up / pratica da adottare
Quando non hai costruito una feature ma hai scoperto qualcosa, o vuoi che il team faccia una cosa nuova.

```
@role_product

Butto qui sta cosa. [Contesto: con chi ne parlavi, da dove nasce]

[La storia: cosa è successo in passato, cosa ci ha morso]

[Come lo monitoriamo oggi, con link se c'è]

[Onestà sui limiti: "Non è perfetto, non ti dice davvero..."]

[Stato attuale: quanto è grave adesso, cosa lo mitiga]

[L'ask: cosa chiedi al team di fare, con comando/procedura]

[Perché conviene farlo: il beneficio secondario]
```

## Tono di voce

Queste regole valgono per tutte le forme. Sono la parte che distingue un messaggio scritto da Damian da un changelog generato.

**Apertura sottotono, mai celebrativa.** "vi condivido quanto fatto stamattina", "ho fatto un po' di refactor e pulizia", "Ho iterato un po' sul componente", "Butto qui sta cosa". Mai "Sono felice di annunciare", "Grande novità", "Ho implementato con successo".

**Understatement sistematico.** "un po' di refactor", "un accenno di test", "ho messo delle ADR di esempio". Il lavoro si dimensiona da solo leggendo il contenuto, non serve gonfiarlo. Anche l'opposto: se hai fatto una cosa grossa, virgolettala per ridimensionarla ("ho 'stravolto' ma semplificato").

**Mini-header in testo piatto, non markdown.** "Il problema di prima", "Cosa ho fatto", "Perché è meglio", "Cosa è cambiato a livello tecnico:". Niente `##`, niente `**Titolo:**` ovunque. Il grassetto si usa dentro i paragrafi per il nome di una decisione, non per titolare sezioni.

**Il prima/dopo è sempre codice vero, commentato.** I commenti dentro lo snippet narrano:
```
// payments.page.tsx — la lista passava la tab di provenienza nell'URL
// notification-navigation.ts — le notifiche facevano lo stesso, con un valore diverso
// Prima usciva questo
// Ora esce questo
```

**Spazio negativo esplicito.** Ogni messaggio dice cosa NON fa, e perché. "Cosa NON viene ricordato di proposito: la pagina corrente e il testo di ricerca". "le tabelle legacy NON passano da questo sistema". "not_any_of [temporaneamente disabilitato]". Questa è la parte che il team usa di più e che un riassunto generico salta sempre.

**Caveat segnalati con parole, non con emoji-warning.** "nota:", "Occhio,", "Attenzione". Mai ⚠️🚨.

**Onestà sui limiti, senza scusarsi.** "Non è perfetto, non ti dice davvero quanti utenti hanno quale versione". "Come si converte un'ADR in una rule? Non lo so. Penso non lo sappia nessuno veramente in realtà 🤣". "in passato ci siamo fatti un po' malino". Il messaggio non vende, descrive.

**Lavoro futuro parcheggiato tra parentesi, senza impegno.** "In futuro, possiamo estenderlo a", "(che gradualmente faremo quando accetteremo che...)", "più avanti avremo una cosa più consolidata".

**Italiano colloquiale.** "manco gli interessa", "sta cosa", "li si che ci sono beghe", "per non farla troppo lunga". Registro parlato, non documentazione.

**Emoji: al massimo una, e solo se autoironica** (🤣). Zero emoji decorative, zero ✅ negli elenchi, zero 🚀. Questo canale non è Telegram né Frill.

**Niente em dash.** Usa virgole, parentesi, o spezza la frase.

**Le parentesi fanno il lavoro degli incisi.** "(es. notifica → dettaglio → indietro torna alle notifiche)", "(probabilmente questioni di browser locale più che di CDN netlify...)". Usale generosamente, sono la firma del registro.

**Chiudi sul punto strutturale, non con un saluto.** Nessun "fatemi sapere!", nessun "spero sia utile". L'ultima frase è la conseguenza pratica o l'ask.

## Quando spezzare in due messaggi

I messaggi lunghi vanno divisi come li dividerebbe una persona che scrive su Discord: il primo messaggio è il ragionamento completo, il secondo è **l'esempio concreto** su un caso specifico.

Spezza quando:
- il messaggio supera ~2000 caratteri di prosa, oppure
- l'esempio prima/dopo richiede 3+ blocchi di codice.

Il secondo messaggio si apre nominando il caso: "Esempio concreto: pagamenti", e ha una struttura fissa: `Prima:` + snippet, separatore `---`, `Dopo:` + snippet, poi 1-2 frasi che spiegano il comportamento risultante.

## Anti-pattern (da non fare mai)

- Bullet list di tutto quello che la sessione ha toccato. Il messaggio ha un argomento, non un inventario.
- Header markdown `##` o titoli in grassetto per ogni sezione.
- Spiegare concetti generali (cos'è un hook, cos'è la cache del browser) al pubblico. Sanno il mestiere.
- Pseudocodice o snippet inventati per illustrare l'idea.
- Tono da release note ("Miglioramenti alle performance", "Fix vari").
- Chiudere con un invito generico al feedback.
- Numeri o metriche che non hai misurato davvero.
- Tradurre in inglese: il canale è italiano.

## Workflow

1. Leggi la sessione, il diff e i commit. Non chiedere all'utente di riassumere.
2. Applica il criterio di **selezione** dello Step 1. Se ci sono più candidati, chiedi. Se non ce n'è nessuno, dillo.
3. Estrai i frammenti di codice reali per il prima/dopo.
4. Scegli la **forma** (A / B / C).
5. Scrivi in italiano, applicando le regole di tono.
6. Decidi se spezzare in due messaggi.
7. Segnala all'utente, fuori dal messaggio, ogni buco: link mancanti (ticket, dashboard, doc), decisioni che non riesci a ricostruire dal diff, punti dove hai dovuto ipotizzare. Usa placeholder evidenti tipo `[LINK ADR]` invece di inventare.

## Formato di output

- Messaggio in italiano, **non wrappato in un code block esterno**: contiene già dei code fence al suo interno e si romperebbero annidati. Delimitalo con una riga di separazione prima e dopo.
- Se sono due messaggi, separali con `--- messaggio 2 ---` così è chiaro dove tagliare.
- Sotto al messaggio, fuori, massimo 3 righe: cosa ti manca e cosa hai assunto.
- Se l'utente vuole varianti, offri due tagli (più corto / più dettagliato sull'esempio), non due toni diversi.