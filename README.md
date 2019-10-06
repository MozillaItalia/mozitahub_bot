# Mozilla Italia Bot - @MozItaBot
Questo è il repository del bot di Mozilla Italia "@MozItaBot" su Telegram.


# Informazioni utili
Per segnalare errori aprire un nuovo ticket (si prega di aprire un ticket per ogni errore/idee/bug/ecc, poiché raggrupparli tutti in un unico issue è dispersivo).
Il bot è attualmente funzionante, basta cercare su Telegram _@MozItaBot_ e il gioco è fatto.

Grazie a tutti.

### Installazione ed esecuzione bot
Per poter eseguire il codice, quindi far girare il bot, è necessario seguire i seguenti passaggi (in ordine):
 - Clonare questa repository, quindi premere su *Fork* in alto a destra
 - Installare Python 3 (o verificare di averlo già installato) **sviluppato e testato con Python 3.7**, ma dovrebbe funzionare anche con altre versioni
 - Il bot attualmente gira su server con Python 3.5
 - Installare la libreria **telepot**, tramite *pip* (o verificare di averla già installata)

   > pip3 install telepot

### Frasi visualizzate e contenuto bottoni

Le frasi e il testo contenuto nei bottoni che vengono visualizzati dall'utente quando viene utilizzato il bot sono contenuti nel file **frasi.json**. È possibile perfino utilizzare l'HTML (vedi sotto "_Tag HTML supportati_")

Può essere sempre modificato, ma è necessario seguire le seguenti regole:

- Le variabili non vanno modificate.
  Le variabili sono identificabili facilmente perché sono del tipo: `{{**nome_variabile**}}`

##### Tag HTML Supportati

I tag HTML supportati da Telegram sono:

- `<b></b>`: testo in grassetto
- `<i></i>`: testo in corsivo
- `<a href="https://..."></a>`: inserire link
- `<a href="tg://user?id="></a>`: menzionare un utente sapendo il suo *user_id*
- `<code></code>`: codice/monospazio
- `<pre></pre>`: codice "preformattato"

**Altri tag potrebbero mandare il bot in crash**


# Funzionamento del bot
Il funzionamento del bot è molto basilare. Si prefigge l'obiettivo di rendere più dinamico l'approccio di chi vuole avere informazioni su Mozilla e, magari, di chi vuole unirsi nella nostra grande famiglia.

Sono disponibili svariate funzionalità:
 - /start: messaggio iniziale
 - /home: per essere reindirizzati al gruppo più attivo di tutti! Dove vengono trattate varie tematiche, anche di ordine generale, come aggiornamenti, novità, richiesta di informazione o supporto, e altro ancora. È il gruppo che accomuna tutti i volontari Mozilla Italia, a prescindere dal gruppo di appartenenza.
 - /gruppi: ottenere la lista di tutti i gruppi e canali ufficiali di Mozilla Italia.
 - /supporto: richiedere e ricevere assistenza, da parte dei nostri volontari, su prodotti e progetti di Mozilla
 - /collabora: per unirti ai volontari Mozilla Italia.
 - /vademecum: ottieni il vademecum, il volantino che in poche e semplici parole ti illustra che cosa è Mozilla e i vari progetti attivi.
 - /vademecumGenerale: ottieni subito il file Vademecum versione generale (VG)
 - /vademecumTecnico: ottieni subito il file Vademecum versione tecnica (VT)
 - /news: rimani sempre aggiornato sulle novità di Mozilla Italia; su questo canale potrai ricevere tutte le novità necessarie.
 - /iot: il gruppo dedicato strettamente alla tecnologia IoT di Mozilla.
 - /developer: il gruppo dei volontari sviluppatori di Mozilla Italia.
 - /design: il gruppo dei volontari designer di Mozilla Italia.
 - /feedback: sentiti libero di lasciare un feedback sul bot e sui servizi di Mozilla Italia. Ricorda di essere sincero e imparziale per permetterci di migliore ciò che offriamo :)
 - /progetti: visualizzare tutti i progetti di Mozilla attivi e anche quelli direttamente della nostra comunità.
 - /info: avere informazioni riguardo questo bot.
 - /meeting: avere informazioni sui meeting video mensili comunitari.
 - /prossimoMeeting: per sapere rapidamente qual è la prossima data del meeting (video) comunitario.
 - /regolamento: per leggere il regolamento comunitario.
 - /avvisi: vedere lo stato attuale degli avvisi, per attivarli o per disattivarli.
 - /avvisiOn: scorciatoia rapida per attivare gli avvisi.
 - /avvisiOff: scorciatoia rapida per disattivare gli avvisi.
 - /admin: (solo per admin) gestire alcune impostazioni del bot.

Le funzionalità elencate sono tutte intuitive e molto facili da utilizzare. La funzionalità "/admin" è disponibile solo per i moderatori, e permette di gestire alcune impostazioni del bot in maniera rapida. Vedi sezione **Privilegi amministratori*.

 

Inoltre ogni singolo messaggio viene salvato in un file *.txt* per soli scopi di debug in caso di malfunzionamenti del bot:
 - history_hub.txt

### Privilegi amministratori
Ecco ciò che si può fare se si è admin.
 - Inviare un messaggio agli utenti:

     - **ANTEPRIMA DELL’INVIO**: prima di usare ‘avviso’ o ‘all users’ è bene accertarsi che il messaggio scritto sia corretto, anche di sintassi, perciò utilizzare prima questo comando: `/admin preview *MESSAGGIO DA INVIARE*`

        > /admin preview Testo messaggio di esempio

      - Agli utenti che hanno attivato il servizio "Avvisi news": `/admin avviso *MESSAGGIO DA INVIARE*`

        > /admin avviso *Testo messaggio di esempio*

      - A tutti gli utenti (NO SPAM, solo messaggi importanti -> usare con parsimonia): `/admin all users *MESSAGGIO DA INVIARE*`

        > /admin all users *Testo messaggio di esempio*

 - Gestire utenti (iscritti a "Avvisi news"):

     - Mostrare la lista degli utenti: `/admin avvisi list mostra`

        > /admin avvisi list mostra

    - Aggiungere forzatamente un utente alla lista: `/admin avvisi list aggiungi *CHAT_ID*`

      > /admin avvisi list aggiungi *123456789*

    - Rimuovere forzatamente un utente dalla lista: `/admin avvisi list elimina *CHAT_ID*`

      > /admin avvisi list elimina *123456789*

 - Gestire progetti (mozilla):
    - Inserire un nuovo progetto: `/admin progetto aggiungi *NOME PROGETTO* *LINK*`

      > /admin progetto aggiungi *Esempio nome di progetto* *https://linkprogetto.it/*
    - Modificare un nuovo progetto: `/admin progetto modifica *NOME PROGETTO* *LINK MODIFICATO*`

      > /admin progetto modifica *Esempio nome di progetto* *https://linkprogetto.it*
    - Eliminare un nuovo progetto: `/admin progetto elimina *NOME PROGETTO*`

      > /admin progetto elimina *Esempio nome di progetto*

 - Gestire progetti comunitari (mozilla italia):
    - Inserire un nuovo progetto: `/admin progetto mozita aggiungi *NOME PROGETTO* *LINK*`

      > /admin progetto mozita aggiungi *Esempio nome di progetto* *https://linkprogetto.it/*
    - Modificare un nuovo progetto: `/admin progetto mozita modifica *NOME PROGETTO* *LINK MODIFICATO*`

      > /admin progetto mozita modifica *Esempio nome di progetto* *https://linkprogetto.it*
    - Eliminare un nuovo progetto: `/admin progetto mozita elimina *NOME PROGETTO*`

      > /admin progetto mozita elimina *Esempio nome di progetto*

 - Gestire collaboratori:

  - Aggiungere un collaboratore: `/admin collaboratore aggiungi *NOME COGNOME (@USERNAME)*`

    > /admin collaboratore aggiungi *Mario Rossi (@marioRossiTelegram)* 

  - Rimuovere un collaboratore: `/admin collaboratore elimina *NOME COGNOME (@USERNAME)*`

    > /admin collaboratore elimina *Mario Rossi (@marioRossiTelegram)*

# Librerie utilizzate
Elenco delle librerie utilizzate nel codice (Python):
 - Telepot
 - Time
 - Datetime
 - Calendar
 - Json
 - Pathlib

## Installare le dipendenze

`pip3 install -r requirements.txt`

# Eccezioni
La lista di tutte le eccezioni catturate (e gestite), è riportata nel file "ECCEZIONI.md".
