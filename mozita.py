import telepot
import time
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

TOKEN="---NASCOSTO---"

#COPIARE E INCOLLARE DA QUI - IL TOKEN E' GIA' INSERITO

versione="0.1.0 alpha"
ultimoAggiornamento="26-10-2018"

def risposte(msg):
    localtime=datetime.now()
    localtime=localtime.strftime("%d/%m/%y %H:%M:%S")
    try:
        chat_id=msg['chat']['id']
        text=msg['text']
    except:
        print("Exception:001 - "+localtime)
        ##entra in questa eccezione se NON è avviato come comando diretto (digitato come comando e inviato)
    try:
        query_id, chat_id, text = telepot.glance(msg, flavor='callback_query')
    except:
        print("Exception:002 - "+localtime)
        ##entra in questa eccezione se NON è stato premendo su un pulsante delle inlineKeyboard
    ##I try-except precedenti servono per assegnare, in qualunque circostanza, chat_id e text corettamente (in base al caso)

    if(datetime.now().month==12):
        annoCall=str(datetime.now().year+1)
        meseCall="Gennaio"
    else:
        annoCall=str(datetime.now().year)
        meseCall=datetime.now().month
        if(int(localtime.strftime("%d"))<=7) meseCall=datetime.now().month+1
        if(meseCall==1):
            meseCall="Gennaio"
        elif(meseCall==2):
            meseCall="Febbraio"
        elif(meseCall==3):
            meseCall="Marzo"
        elif(meseCall==4):
            meseCall="Aprile"
        elif(meseCall==5):
            meseCall="Maggio"
        elif(meseCall==6):
            meseCall="Giugno"
        elif(meseCall==7):
            meseCall="Luglio"
        elif(meseCall==8):
            meseCall="Agosto"
        elif(meseCall==9):
            meseCall="Settembre"
        elif(meseCall==10):
            meseCall="Ottobre"
        elif(meseCall==11):
            meseCall="Novembre"
        elif(meseCall==12):
            meseCall="Dicembre"
        #non è possibile utilizzare la funzione datetime.now().(month+1).strftime("%B") perché lo restituisce in inglese

    home = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Vai al gruppo Home', url='https://t.me/joinchat/BCql3UMy26nl4qxuRecDsQ')],
                ])

    feedback = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Vai in 'Home' e lascia il tuo feedback", url='https://t.me/joinchat/BCql3UMy26nl4qxuRecDsQ')],
                    [InlineKeyboardButton(text="Chiedi di voler contribuire al bot in 'Home'", url='https://t.me/joinchat/BCql3UMy26nl4qxuRecDsQ')]
                ])

    start = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Mostrami che cosa posso fare', callback_data='/help')],
                    [InlineKeyboardButton(text='Ho bisogno di assistenza', callback_data='/supporto')],
                ])

    supporto = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Supporto via Telegram', url='https://t.me/joinchat/BCql3UMy26nl4qxuRecDsQ'),
                    InlineKeyboardButton(text='Supporto via forum', callback_data='/forum')],
                    [InlineKeyboardButton(text='Leggi FAQ dal forum di Mozilla Italia', url='https://forum.mozillaitalia.org/index.php?board=9.0')]
                ])

    help = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Home', callback_data='/home'),
                    InlineKeyboardButton(text='Gruppi', callback_data='/gruppi'),
                    InlineKeyboardButton(text='Supporto', callback_data='/supporto')],
                    [InlineKeyboardButton(text='Collabora', callback_data='/collabora'),
                    InlineKeyboardButton(text='Vademecum', callback_data='/vademecum')],
                    [InlineKeyboardButton(text='News', callback_data='/news'),
                    InlineKeyboardButton(text='IoT', callback_data='/iot'),
                    InlineKeyboardButton(text='Developer', callback_data='/developer')],
                    [InlineKeyboardButton(text='Design', callback_data='/design'),
                    InlineKeyboardButton(text='Feedback', callback_data='/feedback'),
                    InlineKeyboardButton(text='Info', callback_data='/info')],
                    [InlineKeyboardButton(text='Call', callback_data='/call'), 
                    InlineKeyboardButton(text='Lista call', callback_data='/listacall'), 
                    InlineKeyboardButton(text='Prossima call', callback_data='/prossimacall')],
                    [InlineKeyboardButton(text='Progetti attivi', callback_data='/progetti')],
                ])

    gruppi = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Home', url='https://t.me/joinchat/BCql3UMy26nl4qxuRecDsQ'),
                    InlineKeyboardButton(text='News', url='https://t.me/mozItaNews')],
                    [InlineKeyboardButton(text='Voglio diventare volontario', url='https://t.me/joinchat/B1cgtEQAHkGVBTbI0XPd-A')],
                    [InlineKeyboardButton(text='Developer', url='https://t.me/joinchat/B1cgtENXHcxd3jzFar7Kuw'),
                    InlineKeyboardButton(text='L10N (chiedi in Home)', url='https://t.me/joinchat/BCql3UMy26nl4qxuRecDsQ')],
                    [InlineKeyboardButton(text='Design', url='https://t.me/joinchat/B1cgtA7DF3qDzuRvsEtT6g'),
                    InlineKeyboardButton(text='IoT', url='https://t.me/joinchat/B1cgtEzLzr0gvSJcEicq1g')],
                ])

    developer = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Vai al gruppo Developer', url='https://t.me/joinchat/B1cgtENXHcxd3jzFar7Kuw')],
                ])

    design = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Vai al gruppo Design Team', url='https://t.me/joinchat/B1cgtA7DF3qDzuRvsEtT6g')],
                ])

    iot = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Vai al gruppo IoT', url='https://t.me/joinchat/B1cgtEzLzr0gvSJcEicq1g')],
                ])

    vademecum = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Vademecum Generale', url='https://github.com/MozillaItalia/firefox-vademecum/blob/master/volantino/Vademecum_2.0_VG.pdf'),
                    InlineKeyboardButton(text='Vademecum Tecnico', url='https://github.com/MozillaItalia/firefox-vademecum/blob/master/volantino/Vademecum_2.0_VT.pdf')],
                ])

    collabora = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Si, vai al gruppo 'Home'", url='https://t.me/joinchat/BCql3UMy26nl4qxuRecDsQ'),
                    InlineKeyboardButton(text="No, ma vorrei collaborare", url='https://t.me/joinchat/B1cgtEQAHkGVBTbI0XPd-A')],
                ])

    news = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Vai al canale ufficiale 'News'", url='https://t.me/mozItaNews')],
                ])

    forum = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Vai al forum di Mozilla Italia', url='https://forum.mozillaitalia.org/')],
                ])
    
    call = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Vedi tutte le call', callback_data='/listacall')],
                    [InlineKeyboardButton(text='Scopri quando e\' la prossima call', callback_data='/prossimacall')],
                ])

    listaCall = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Guarda la call di Dicembre 2017', url='http://edovio.in/call/Call_MozillaItalia_271217.mp4')],
                    [InlineKeyboardButton(text='Guarda la call di Gennaio 2018', url='https://drive.google.com/file/d/1FPBtUT1NVyem2e1q1d_F_dZ6Lzmb64EK/view')],
                    [InlineKeyboardButton(text='Guarda la call di Marzo 2018', url='https://drive.google.com/file/d/1XY4tUt9tzYUZjy08tRB1vkhpwfQ7xA9Q/view')],
                    [InlineKeyboardButton(text='Guarda la call di Aprile 2018 (1)', url='https://drive.google.com/file/d/1PJXI4h88NjXNp2hMINYMnu_0ADhdG0ZK/view')],
                    [InlineKeyboardButton(text='Guarda la call di Aprile 2018 (2)', url='https://drive.google.com/file/d/1B8H2Lf5Egz2GKy8iDWDihn8fBlXx5BLO/view')],
                    [InlineKeyboardButton(text='Guarda la call di Maggio 2018', url='https://drive.google.com/file/d/1B8H2Lf5Egz2GKy8iDWDihn8fBlXx5BLO/view')],
                    [InlineKeyboardButton(text='Guarda la call di Agosto 2018', url='https://drive.google.com/file/d/1swzPNUJYh6Jd7wVaQvVr2TCVoc96f67n/view')],
                    [InlineKeyboardButton(text='Guarda la call di Settembre 2018', url='https://drive.google.com/file/d/1lQFgj-32bWGaaHGReW8fY0kdIuRt4eTZ/view')],
                ])
    
    progetti = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Common Voice', url='https://voice.mozilla.org/it/new')],
                    [InlineKeyboardButton(text='Internet Health Report', url='https://internethealthreport.org/')],
                    [InlineKeyboardButton(text='Thimble', url='https://thimble.mozilla.org/it/')],
                    [InlineKeyboardButton(text='Firefox', url='https://www.mozilla.org/it/firefox/new/')],
                    [InlineKeyboardButton(text='Thunderbird', url='https://www.thunderbird.net/it/')],
                    [InlineKeyboardButton(text='SeaMonkey', url='http://www.seamonkey-project.org/')],
                    [InlineKeyboardButton(text='Firefox Mobile', url='https://www.mozilla.org/it/firefox/mobile/')],
                    [InlineKeyboardButton(text='Firefox Focus', url='https://support.mozilla.org/it/kb/firefox-focus-android')],
                    [InlineKeyboardButton(text='Rust', url='https://www.rust-lang.org/en-US/')],
                    [InlineKeyboardButton(text='Firefox Reality', url='https://blog.mozilla.org/blog/2018/09/18/firefox-reality-now-available/')],
                    [InlineKeyboardButton(text='MDN (Mozilla Developer Network)', url='https://developer.mozilla.org/it/')],
                    [InlineKeyboardButton(text='Firefox Lockbox', url='https://testpilot.firefox.com/experiments/firefox-lockbox/')],
                ])
    
    progettimozita = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Vademecum', url='https://github.com/MozillaItalia/firefox-vademecum')],
                    [InlineKeyboardButton(text='MozIta Hub Bot', url='https://github.com/Sav22999/mozitahub_bot')],
                    [InlineKeyboardButton(text='Slide Common Voice', url='https://docs.google.com/presentation/d/1oFkstTY140Tp6cazOgSC6LBeTRF0labJNCl-0DogfQI/edit?ts=5babc6c8#slide=id.g4165a8ce60_0_51')],
                ])
    
    '''
    nome_nome = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Testo bottone (riga 1, col 1)', callback_data='/comando'),
                    InlineKeyboardButton(text='Testo bottone 2 (riga 1, col 2)', callback_data='/comando2')],
                    [InlineKeyboardButton(text='Testo bottone 3 (riga 2, col 1-2)', url='https://t.me/')],
                ])
    '''

    if text=="/home":
        bot.sendMessage(chat_id, "Mozilla Italia - Home e' gruppo che accomuna tutti i volontari Mozilla Italia, a prescindere dal gruppo di provenienza. Unisciti anche tu e diventa parte di questa grande famiglia!", reply_markup=home)
    #elif text=="/stop":
        #bot.sendMessage(chat_id, "Stai per disattivare MozIta Hub. Per attivarlo nuovamente sara' sufficiente premere il pulsante sottostante 'Avvia' o digitare /start. Se lo desideri puoi anche lasciarci un feedback sulla tua esperienza d'utilizzo del bot e la motivazione dell'abbandono. Grazie.", reply_markup=stop)
    elif text=="/start":
        bot.sendMessage(chat_id, "Benvenuto/a in Mozilla Italia Hub.\nQui potrai usufruire di funzioni uniche, come ottenere informazioni, richiedere supporto, e molto altro.\nScopri tutto cio' che puoi fare digitando /help.")
        bot.sendMessage(chat_id, "Dopo questa breve presentazione, che cosa desideri fare?", reply_markup=start)
    elif text=="/supporto":
        bot.sendMessage(chat_id, "Puoi aprire un topic sul nostro forum ufficiale dove, il team di volontari del Supporto Mozilla (SuMo), ti assistera' nel migliore modo possibile.\nIn alternativa puoi provare a chiedere nel gruppo 'Home' della comunita' direttamente da Telegram.\n\nTi consigliamo, comunque, di leggere prima le FAQ (le risposte a domande frequenti) poiche' potresti trovare la soluzione al tuo probema direttamente li'.")
        bot.sendMessage(chat_id, "Scegli tu cosa vuoi fare :)", reply_markup=supporto)
    elif text=="/gruppi":
        bot.sendMessage(chat_id, "Ecco qui la lista di tutti i canali e gruppi ufficiali di Mozilla Italia su Telegram:\n\n'Mozilla Italia - HOME' (/home):\nil gruppo dove vengono trattate varie tematiche come aggiornamenti, novita', richiesta di informazione o supporto, e altro ancora. In poche parole il gruppo che accomuna tutti i volontari Mozilla Italia, a prescindere dal gruppo di appartenenza.\n\n'Mozilla Italia - News' (/news):\nil canale che ti permette di rimanere sempre aggiornato sulle ultime novità da Mozilla Italia.\n\n'Mozilla Italia - Voglio diventare volontario' (/collabora):\nil gruppo adatto per chi vuole entrare a far parte della comunità. Qui potrai avere maggiori informazioni su ciascun gruppo o, se non sai ancora come puoi contribuire alla causa, troverai persone che sono in grado di indirizzarti nel gruppo piu' adatto alle tue caratteristiche, alle tue abilita' e alle tue attitudini.\n\n'Mozilla Italia - Developers' (/developer):\nil gruppo dedicato agli sviluppatori Mozilla Italia, quindi a coloro che si dedicano maggiormente alla programmazione.\n\n'Mozilla Italia - L10N' (privato):\nil gruppo dedicato ai localizzatori (traduttori). Questo gruppo è privato, quindi chiedere nel gruppo Home di essere inserite se si e' interessati.\n\n'Mozilla Italia - Design Team' (/design):\nil gruppo dedicato ai 'designer' e a coloro che si dedicano maggiormente alla grafica.\n\n'Mozilla Italia - IoT' (/iot):\nil gruppo dedicato alle tecnologie Internet of Thing di Mozilla.\n\nPuoi appartenere e unirti anche a piu' gruppi contemporaneamente. Ti consigliamo, comunque, di unirti al gruppo 'Home' che è quello piu' generico :)", reply_markup=gruppi)
    elif text=="/collabora":
        bot.sendMessage(chat_id, "In Mozilla abbiamo bisogno di tutte le abilita'!\nLa comunita' di Mozilla Italia, infatti, si occupa di tradurre progetti e documentazione Mozilla, sviluppare progetti interni a Mozilla Italia, ma anche direttamente per Mozilla, prestare supporto tecnico a utenti bisognosi e tanto altro.")
        bot.sendMessage(chat_id, "Sai gia' come potresti essere utile e contribuire a Mozilla Italia?", reply_markup=collabora)
    elif text=="/vademecum":
        bot.sendMessage(chat_id, "Il vademecum e' un volantino che, in foglio A4 fronte-retro, riesce a spiegarti (molto brevemente) che cosa e' Mozilla, che cosa e' Mozilla Italia, i progetti attivi e altro.\nEsistono 2 tipi di Vademecum: il Generale, adatto a tutti, e il Tecnico, adatto piu' specificatamente per gli sviluppatori e programmatori (o chi e' in questo campo).\nQuindi, di quale versione vuoi prendere visione?", reply_markup=vademecum)
    elif text=="/feedback":
        bot.sendMessage(chat_id, "Puoi lasciare quando vuoi un feedback sui servizi offerti da Mozilla Italia, semplicemente recandoti sul gruppo 'Home', quindi riportando il feedback.\nNon preoccuparti, nessuno ti giudichera' o aggredira', ma anzi, troverai persone pronte a capire i tuoi problemi e i tuoi suggerimenti ed, eventualmente, a segnalarli direttamente a Mozilla :)", reply_markup=feedback)
    elif text=="/help":
        bot.sendMessage(chat_id, "Ecco cosa puoi fare su MozIta HUB:\n/home: per essere reindirizzato al gruppo piu' attivo di tutti! Dove vengono trattate varie tematiche, anche di ordine generale, come aggiornamenti, novita', richiesta di informazione o supporto, e altro ancora. E' il gruppo che accomuna tutti i volontari Mozilla Italia, a prescindere dal gruppo di appartenenza.\n/gruppi: ottenere la lista di tutti i gruppi e canali ufficiali di Mozilla Italia.\n/supporto: richiedere e ricevere assistenza, da parte dei nostri volontari, su prodotti e progetti di Mozilla\n/collabora: per unirti ai volontari Mozilla Italia.\n/vademecum: ottieni il vademecum, il volantino che in poche e semplici parole ti illustra che cosa è Mozilla e i vari progetti attivi.\n/news: rimani sempre aggiornato sulle novità di Mozilla Italia; su questo canale potrai ricevere tutte le novità necessarie.\n/iot: il gruppo dedicato strettamente alla tecnologia IoT di Mozilla.\n/developer: il gruppo dei volontari sviluppatori di Mozilla Italia.\n/design: il gruppo dei volontari designer di Mozilla Italia.\n/feedback: sentiti libero di lasciare un feedback sul bot e sui servizi di Mozilla Italia. Ricorda di essere sincero e imparziale per permetterci di migliore ciò che offriamo :)\n/progetti: visualizzare tutti i progetti di Mozilla attivi e anche quelli direttamente della nostra comunità.\n/info: avere informazioni riguardo questo bot./call: avere informazioni sulle call mensili comunitarie.\n/listacall: per vedere la lista completa delle call comutarie di Mozilla Italia con il link diretto al video, per poterlo vedere facilmente.\n/prossimacall: per sapere rapidamente qual e' la prossima call comunitaria.")
        bot.sendMessage(chat_id, "Allora, che cosa vorresti fare?", reply_markup=help)
    elif text=="/news":
        bot.sendMessage(chat_id, "Rimani sempre aggiornato sul mondo Mozilla! Grazie a questo canale ufficiale sarai a conoscenze sempre delle ultime novita' da Mozilla Italia.", reply_markup=news)
    elif text=="/info":
        bot.sendMessage(chat_id, "MozIta Hub e' un bot realizzato per Mozilla Italia\nVersione: "+versione+"\nUltimo aggiornamento: "+ultimoAggiornamento+"\n\nCreatore: Saverio Morelli (@Sav22999)\nCollaboratori (ordine alfabetico):\n- Daniele Scasciafratte (@Mte90)\n- Martin Ligabue (@MartinLigabue)\n- Sara Todaro (@kitsunenosaraT)")
    elif text=="/forum":
        bot.sendMessage(chat_id, "La comunita' di Mozilla Italia presta supporto tramite il forum ufficiale (www.forum.mozillaitalia.org) gratuitamente e quasi in tempo reale. Prima di aprire un topic e' necessario leggere il regolamento e accertarsi, ovviamente, che un topic uguale non sia stato gia' aperto e, magari, anche risolto.", reply_markup=forum)
    elif text=="/developer":
        bot.sendMessage(chat_id, "Entra a far parte del gruppo dedicato agli sviluppatori Mozilla Italia.", reply_markup=developer)
    elif text=="/design":
        bot.sendMessage(chat_id, "Unisciti al gruppo dei designer di Mozilla Italia.", reply_markup=design)
    elif text=="/iot":
        bot.sendMessage(chat_id, "Unisciti al gruppo ufficiale di Mozilla Italia dedicato allo sviluppo delle IoT.", reply_markup=iot)
    elif text=="/call":
        bot.sendMessage(chat_id, "La comunita' di Mozilla Italia organizza, salvo imprevisti, il primo venerdi' di ogni mese una call comunitaria, per poter parlare di tutto ciò che e' accaduto in quel mese nella comunita', di nuovi progetti, eventi o proposte. Tutti possono partecipare, sia membri di Mozilla Italia sia non membri, ma comunque interessati.\nQueste call vengono registrate e successivamente pubblicate per poterle (ri)vedere liberamente.", reply_markup=call)
    elif text=="/listacall":
        bot.sendMessage(chat_id, "Questo e' tutte l'elenco delle call gia' tenute, con il relativo link per poterle guardare.", reply_markup=listaCall)
    elif text=="/prossimacall":
        bot.sendMessage(chat_id, "La prossima call comunitaria sara' quella di "+meseCall+" "+annoCall+", il primo venerdi' del mese alle ore 18:30.\nQuesta e' una stima, potrebbero esserci slittamenti o annullamenti. Per maggiore sicurezza chiedi nel gruppo Home di Mozilla Italia.")
    elif text=="/progetti":
        bot.sendMessage(chat_id, "Questi sono i progetti di mozilla attualmente attivi:", reply_markup=progetti)
        bot.sendMessage(chat_id, "Questi, invece, sono i progetti della comunità di mozilla italia:", reply_markup=progettimozita)
    else:
        bot.sendMessage(chat_id, "Errore: comando non riconosciuto", reply_markup=start)



bot=telepot.Bot(TOKEN)
MessageLoop(bot, {'chat': risposte, 'callback_query': risposte}).run_as_thread()

while 1:
    time.sleep(10)
