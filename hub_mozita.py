#!/usr/bin/python3
import telepot
import time
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
import calendar
import json
from pathlib import Path
import os
from configparser import ConfigParser

if not os.path.isfile("config.ini"):
    print("Il file di configurazione non è presente. Rinomina il file 'config-sample.ini' in 'config.ini' e inserisci il token.")
    exit()

script_path = os.path.dirname(os.path.realpath(__file__))
config_parser = ConfigParser()
config_parser.read(os.path.join(script_path,"config.ini"))

TOKEN=config_parser.get("access","token")

if TOKEN == "":
    print("Token non presente.")
    exit()

versione="0.2.2 alpha"
ultimoAggiornamento="18-01-2019"

adminlist_path="adminlist_hub.json"
call_mensili_list_path="call_mensili_list.json"
avvisi_on_list_path="avvisi_on_list.json"
progetti_list_path="progetti_list.json"
progetti_mozita_list_path="progetti_mozita_list.json"
collaboratori_hub_path="collaboratori_hub.json"
all_users_path="all_users.json"
AdminList=[]
if Path(call_mensili_list_path).exists():
    call_mensili_list=json.loads(open(call_mensili_list_path).read())
else:
    call_mensili_list=[]
if Path(avvisi_on_list_path).exists():
    avvisi_on_list=json.loads(open(avvisi_on_list_path).read())
else:
    avvisi_on_list=[]
if Path(progetti_list_path).exists():
    progetti_list=json.loads(open(progetti_list_path).read())
else:
    progetti_list=[]
if Path(progetti_mozita_list_path).exists():
    progetti_mozita_list=json.loads(open(progetti_mozita_list_path).read())
else:
    progetti_mozita_list=[]
if Path(collaboratori_hub_path).exists():
    collaboratori_hub=json.loads(open(collaboratori_hub_path).read())
else:
    collaboratori_hub=[]
if Path(all_users_path).exists():
    all_users=json.loads(open(all_users_path).read())
else:
    all_users=[]

listaMesi=["Gennaio","Febbraio","Marzo","Aprile","Maggio","Giugno","Luglio","Agosto","Settembre","Ottobre","Novembre","Dicembre"]

def first_friday_of_the_month(year, month):
    #questa funzione serve per calcolare il primo venerdì del mese
    for day, weekday in calendar.Calendar().itermonthdays2(year, month):
        if weekday == 4:
            if(day!=0):
                return day
            else:
                return day+7

def risposte(msg):
    localtime=datetime.now()
    localtime=localtime.strftime("%d/%m/%y %H:%M:%S")
    messaggio=msg
    type_msg="NM" #Normal Message
    status_user="-"

    if Path(adminlist_path).exists():
        global AdminList
        AdminList = json.loads(open(adminlist_path).read())
    else:
        AdminList=[240188083] #nel caso in cui non dovesse esistere alcun file "adminlist.json" imposta staticamente l'userid di Sav22999 -> così da poter confermare anche altri utenti

    if "text" in msg:
        #EVENTO MESSAGGIO (SOTTO-EVENTI MESSAGGIO)
        text=str(msg['text'])
        if "entities" in msg:
            #EVENTO LINK
            type_msg="LK" #Link
        else:
            #EVENTO MESSAGGIO PURO
            type_msg="NM" #Normal Message
    elif "data" in msg:
        #EVENTO PRESS BY INLINE BUTTON
        text=str(msg['data'])
        #print("Callback_query")
        type_msg="BIC" #Button Inline Click
    else:
        #EVENTO NON CATTURA/GESTITO -> ELIMINARE AUTOMATICAMENTE IL MESSAGGIO
        text="--Testo non identificato--"
        type_msg="NI" #Not Identified

    user_id=msg['from']['id']
    if user_id in AdminList:
        status_user="A"
    nousername=False
    if "username" in msg['from']:
        user_name=msg['from']['username']
    else:
        user_name="NessunUsername"
        nousername=True
        
    if not "chat" in msg:
        msg=msg["message"]
    chat_id=msg['chat']['id']

    if(datetime.now().month==12):
        annoCall=str(datetime.now().year+1)
        meseCall=listaMesi[0]
        giornoCall=str(first_friday_of_the_month(int(annoCall),1))
    else:
        annoCall=str(datetime.now().year)
        giornoCall=first_friday_of_the_month(int(annoCall),datetime.now().month)
        if(datetime.now().day>=giornoCall):
            meseCall=datetime.now().month+1
            giornoCall=str(first_friday_of_the_month(int(annoCall),datetime.now().month+1))
        else:
            meseCall=datetime.now().month
            giornoCall=str(giornoCall)
        meseCall=listaMesi[meseCall-1]
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
                    [InlineKeyboardButton(text='Leggi le FAQ dal forum di Mozilla Italia', url='https://forum.mozillaitalia.org/index.php?board=9.0')]
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
                    [InlineKeyboardButton(text='Progetti attivi', callback_data='/progetti'),
                    InlineKeyboardButton(text='Regolamento', callback_data='/regolamento')],
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
                    [InlineKeyboardButton(text="Sì, vai al gruppo 'Home'", url='https://t.me/joinchat/BCql3UMy26nl4qxuRecDsQ'),
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
                    [InlineKeyboardButton(text='Scopri quando sarà la prossima call', callback_data='/prossimacall')],
                ])

    load_listaCall=[]
    for x in call_mensili_list:
        load_listaCall.append([InlineKeyboardButton(text=str(x), url=str(call_mensili_list[x]))])

    listaCall = InlineKeyboardMarkup(inline_keyboard=load_listaCall)

    load_progetti=[]
    for x in progetti_list:
        load_progetti.append([InlineKeyboardButton(text=str(x), url=str(progetti_list[x]))])

    progetti = InlineKeyboardMarkup(inline_keyboard=load_progetti)

    load_progettiMozIta=[]
    for x in progetti_mozita_list:
        load_progettiMozIta.append([InlineKeyboardButton(text=str(x), url=str(progetti_mozita_list[x]))])

    progettimozita = InlineKeyboardMarkup(inline_keyboard=load_progettiMozIta)

    regolamento = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Leggi Regolamento', url='https://github.com/Sav22999/Guide/blob/master/Mozilla%20Italia/Telegram/regolamento.md')],
                ])

    avvisi=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Attiva avvisi', callback_data="/avvisiOn")],
                    [InlineKeyboardButton(text='Disattiva avvisi', callback_data="/avvisiOff")],
                ])

    '''
    nome_nome = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Testo bottone (riga 1, col 1)', callback_data='/comando'),
                    InlineKeyboardButton(text='Testo bottone 2 (riga 1, col 2)', callback_data='/comando2')],
                    [InlineKeyboardButton(text='Testo bottone 3 (riga 2, col 1-2)', url='https://t.me/')],
                ])
    '''

    admin=False
    collaboratori_stampa=""
    for x in sorted(collaboratori_hub):
        collaboratori_stampa+="\n - "+x

    if not (chat_id in all_users):
        all_users.append(chat_id)
        avvisi_on_list.append(user_id)
        try:
            with open(all_users_path, "wb") as f:
                f.write(json.dumps(all_users).encode("utf-8"))
        except Exception as e:
            print("Excep:03 -> "+str(e))
        try:
            with open(avvisi_on_list_path, "wb") as f:
                f.write(json.dumps(avvisi_on_list).encode("utf-8"))
        except Exception as e:
            print("Excep:04 -> "+str(e))

    if user_id in avvisi_on_list:
        stato_avvisi="ATTIVATO"
    else:
        stato_avvisi="DISATTIVATO"

    if text=="/home":
        bot.sendMessage(chat_id, "Mozilla Italia - Home è gruppo che accomuna tutti i volontari Mozilla Italia, a prescindere dal gruppo di provenienza. Unisciti anche tu e diventa parte di questa grande famiglia!", reply_markup=home)
    #elif text=="/stop":
        #bot.sendMessage(chat_id, "Stai per disattivare MozIta Hub. Per attivarlo nuovamente sara' sufficiente premere il pulsante sottostante 'Avvia' o digitare /start. Se lo desideri puoi anche lasciarci un feedback sulla tua esperienza d'utilizzo del bot e la motivazione dell'abbandono. Grazie.", reply_markup=stop)
    elif text=="/start":
        bot.sendMessage(chat_id, "Benvenuto/a in Mozilla Italia Hub.\nQui potrai usufruire di funzioni uniche, come ottenere informazioni, richiedere supporto, e molto altro.\nScopri tutto ciò che puoi fare digitando /help.\n\nIn automatico sono state attivate le notifiche per le news. Controlla il tuo stato digitando /avvisi, lì potrai attivarli e disattivarli rapidamente.")
        bot.sendMessage(chat_id, "Dopo questa breve presentazione, che cosa desideri fare?", reply_markup=start)
        if nousername:
            bot.sendMessage(chat_id, "Attenzione: non hai impostato alcun username. Per poterti unire ai gruppi Mozilla Italia è necessario averne impostato uno (altrimenti si viene automaticamente cacciati e bloccati).")
    elif text=="/supporto":
        bot.sendMessage(chat_id, "Puoi aprire un topic sul nostro forum ufficiale dove, il team di volontari del Supporto Mozilla (SuMo), ti assisterà nel migliore modo possibile.\nIn alternativa puoi provare a chiedere nel gruppo 'Home' della comunità direttamente da Telegram.\n\nTi consigliamo, comunque, di leggere prima le FAQ (le risposte a domande frequenti) poichè potresti trovare la soluzione al tuo probema direttamente lì.")
        bot.sendMessage(chat_id, "Scegli tu cosa vuoi fare :)", reply_markup=supporto)
    elif text=="/gruppi":
        bot.sendMessage(chat_id, "Ecco qui la lista di tutti i canali e gruppi ufficiali di Mozilla Italia su Telegram:\n\n'Mozilla Italia - HOME' (/home):\nil gruppo dove vengono trattate varie tematiche come aggiornamenti, novità, richiesta di informazione o supporto, e altro ancora. In poche parole il gruppo che accomuna tutti i volontari Mozilla Italia, a prescindere dal gruppo di appartenenza.\n\n'Mozilla Italia - News' (/news):\nil canale che ti permette di rimanere sempre aggiornato sulle ultime novità da Mozilla Italia.\n\n'Mozilla Italia - Voglio diventare volontario' (/collabora):\nil gruppo adatto per chi vuole entrare a far parte della comunità. Qui potrai avere maggiori informazioni su ciascun gruppo o, se non sai ancora come puoi contribuire alla causa, troverai persone che sono in grado di indirizzarti nel gruppo più adatto alle tue caratteristiche, alle tue abilità e alle tue attitudini.\n\n'Mozilla Italia - Developers' (/developer):\nil gruppo dedicato agli sviluppatori Mozilla Italia, quindi a coloro che si dedicano maggiormente alla programmazione.\n\n'Mozilla Italia - L10N' (privato):\nil gruppo dedicato ai localizzatori (traduttori). Questo gruppo è privato, quindi chiedere nel gruppo Home di essere inserite se si è interessati.\n\n'Mozilla Italia - Design Team' (/design):\nil gruppo dedicato ai 'designer' e a coloro che si dedicano maggiormente alla grafica.\n\n'Mozilla Italia - IoT' (/iot):\nil gruppo dedicato alle tecnologie Internet of Thing di Mozilla.\n\nPuoi appartenere e unirti anche a più gruppi contemporaneamente. Ti consigliamo, comunque, di unirti al gruppo 'Home' che è quello piu' generico :)", reply_markup=gruppi)
    elif text=="/collabora":
        bot.sendMessage(chat_id, "In Mozilla abbiamo bisogno di tutte le abilità!\nLa comunità di Mozilla Italia, infatti, si occupa di tradurre progetti e documentazione Mozilla, sviluppare progetti interni a Mozilla Italia, ma anche direttamente per Mozilla, prestare supporto tecnico a utenti bisognosi e tanto altro.")
        bot.sendMessage(chat_id, "Sai già come potresti essere utile e contribuire a Mozilla Italia?", reply_markup=collabora)
    elif text=="/vademecum":
        bot.sendMessage(chat_id, "Il vademecum è un volantino che, in foglio A4 fronte-retro, riesce a spiegarti (molto brevemente) che cosa è Mozilla, che cosa è Mozilla Italia, i progetti attivi e altro.\nEsistono 2 tipi di Vademecum: il Generale, adatto a tutti, e il Tecnico, adatto più specificatamente per gli sviluppatori e programmatori (o chi è in questo campo).\nQuindi, di quale versione vuoi prendere visione?", reply_markup=vademecum)
    elif text=="/feedback":
        bot.sendMessage(chat_id, "Puoi lasciare quando vuoi un feedback sui servizi offerti da Mozilla Italia, semplicemente recandoti sul gruppo 'Home', quindi riportando il feedback.\nNon preoccuparti, nessuno ti giudicherà o aggredirà, ma anzi, troverai persone pronte a capire i tuoi problemi e i tuoi suggerimenti ed, eventualmente, a segnalarli direttamente a Mozilla :)", reply_markup=feedback)
    elif text=="/help":
        bot.sendMessage(chat_id, "Ecco cosa puoi fare su MozIta HUB:\n/home: per essere reindirizzato al gruppo più attivo di tutti! Dove vengono trattate varie tematiche, anche di ordine generale, come aggiornamenti, novità, richiesta di informazione o supporto, e altro ancora. È il gruppo che accomuna tutti i volontari Mozilla Italia, a prescindere dal gruppo di appartenenza.\n/gruppi: ottenere la lista di tutti i gruppi e canali ufficiali di Mozilla Italia.\n/supporto: richiedere e ricevere assistenza, da parte dei nostri volontari, su prodotti e progetti di Mozilla\n/collabora: per unirti ai volontari Mozilla Italia.\n/vademecum: ottieni il vademecum, il volantino che in poche e semplici parole ti illustra che cosa è Mozilla e i vari progetti attivi.\n/news: rimani sempre aggiornato sulle novità di Mozilla Italia; su questo canale potrai ricevere tutte le novità necessarie.\n/iot: il gruppo dedicato strettamente alla tecnologia IoT di Mozilla.\n/developer: il gruppo dei volontari sviluppatori di Mozilla Italia.\n/design: il gruppo dei volontari designer di Mozilla Italia.\n/feedback: sentiti libero di lasciare un feedback sul bot e sui servizi di Mozilla Italia. Ricorda di essere sincero e imparziale per permetterci di migliore ciò che offriamo :)\n/progetti: visualizzare tutti i progetti di Mozilla attivi e anche quelli direttamente della nostra comunità.\n/info: avere informazioni riguardo questo bot.\n/call: avere informazioni sulle call mensili comunitarie.\n/listacall: per vedere la lista completa delle call comutarie di Mozilla Italia con il link diretto al video, per poterlo vedere facilmente.\n/prossimacall: per sapere rapidamente qual è la prossima call comunitaria.\n/regolamento: per leggere il regolamento comunitario.\n/avvisi: vedere lo stato attuale degli avvisi, per attivarli o per disattivarli.\n/avvisiOn: scorciatoia rapida per attivare gli avvisi.\n/avvisiOff: scorciatoia rapida per disattivare gli avvisi.\n/admin help: (solo per admin) gestire alcune impostazioni del bot.")
        bot.sendMessage(chat_id, "Allora, che cosa vorresti fare?", reply_markup=help)
    elif text=="/news":
        bot.sendMessage(chat_id, "Rimani sempre aggiornato sul mondo Mozilla! Grazie a questo canale ufficiale sarai a conoscenze sempre delle ultime novità da Mozilla Italia.", reply_markup=news)
    elif text=="/info":
        bot.sendMessage(chat_id, "MozIta Hub è un bot realizzato per Mozilla Italia\nVersione: "+versione+"\nUltimo aggiornamento: "+ultimoAggiornamento+"\n\nCreatore: Saverio Morelli (@Sav22999)\nCollaboratori (ordine alfabetico):"+str(collaboratori_stampa))
    elif text=="/forum":
        bot.sendMessage(chat_id, "La comunità di Mozilla Italia presta supporto tramite il forum ufficiale (www.forum.mozillaitalia.org) gratuitamente e quasi in tempo reale. Prima di aprire un topic è necessario leggere il regolamento e accertarsi, ovviamente, che un topic uguale non sia stato già aperto e, magari, anche risolto.", reply_markup=forum)
    elif text=="/developer":
        bot.sendMessage(chat_id, "Entra a far parte del gruppo dedicato agli sviluppatori Mozilla Italia.", reply_markup=developer)
    elif text=="/design":
        bot.sendMessage(chat_id, "Unisciti al gruppo dei designer di Mozilla Italia.", reply_markup=design)
    elif text=="/iot":
        bot.sendMessage(chat_id, "Unisciti al gruppo ufficiale di Mozilla Italia dedicato allo sviluppo delle IoT.", reply_markup=iot)
    elif text=="/call":
        bot.sendMessage(chat_id, "La comunità di Mozilla Italia organizza, salvo imprevisti, il primo venerdì di ogni mese una call comunitaria, per poter parlare di tutto ciò che è accaduto in quel mese nella comunità, di nuovi progetti, eventi o proposte. Tutti possono partecipare, sia membri di Mozilla Italia sia non membri, ma comunque interessati.\nQueste call vengono registrate e successivamente pubblicate per poterle (ri)vedere liberamente.", reply_markup=call)
    elif text=="/listacall":
        bot.sendMessage(chat_id, "Questo è tutte l'elenco delle call già tenute, con il relativo link per poterle guardare.", reply_markup=listaCall)
    elif text=="/prossimacall":
        bot.sendMessage(chat_id, "La prossima call comunitaria sarà quella del "+giornoCall+" "+meseCall+" "+annoCall+", (il primo venerdì del mese) alle ore 18:30.\nQuesta è una stima, potrebbero esserci slittamenti o annullamenti. Per maggiore sicurezza chiedi nel gruppo Home di Mozilla Italia.")
    elif text=="/progetti":
        bot.sendMessage(chat_id, "Questi sono i progetti di mozilla attualmente attivi:", reply_markup=progetti)
        bot.sendMessage(chat_id, "Questi, invece, sono i progetti della comunità di mozilla italia:", reply_markup=progettimozita)
    elif text=="/regolamento":
        bot.sendMessage(chat_id, "Leggi il regolamento vigente nei gruppi comunitari di Mozilla Italia:", reply_markup=regolamento)
    elif text=="/avvisi":
        bot.sendMessage(chat_id, "Il tuo stato attutale è: "+stato_avvisi+"\n\nPuoi attivare o disattivare gli avvisi in qualunque momento, digitando '/avvisiOn' o '/avvisiOff', o premendo i seguenti pulsanti:", reply_markup=avvisi)
    elif text=="/avvisiOn":
        if not (user_id in avvisi_on_list):
            avvisi_on_list.append(user_id)
            try:
                with open(avvisi_on_list_path, "wb") as f:
                    f.write(json.dumps(avvisi_on_list).encode("utf-8"))
                bot.sendMessage(chat_id, "Hai attivato correttamente gli avvisi news di mozilla italia.\nOra riceverai notizie sulle novità riguardo il mondo mozilla e mozilla italia periodicamente.\nNel caso volessi disattivarli è sufficiente digitare '/avvisiOff'.")
            except Exception as e:
                print("Excep:05 -> "+str(e))
                bot.sendMessage(chat_id, "Si è verificato un errore imprevisto durante l'attivazione degli avvisi.")
        else:
            bot.sendMessage(chat_id, "Gli avvisi sono già stati attivati.")
    elif text=="/avvisiOff":
        if user_id in avvisi_on_list:
            avvisi_on_list.remove(user_id)
            try:
                with open(avvisi_on_list_path, "wb") as f:
                    f.write(json.dumps(avvisi_on_list).encode("utf-8"))
                bot.sendMessage(chat_id, "Hai disattivato correttamente gli avvisi news di mozilla italia.\nDa ora non ricevere più novità.\nPuoi riattivarli velocemente digitando '/avvisiOn'.\n\nN.B. Potresti, tuttavia, ricevere gli avvisi ritenuti 'fondamentali' per la comunità.")
            except Exception as e:
                print("Excep:06 -> "+str(e))
                bot.sendMessage(chat_id, "Si è verificato un errore imprevisto durante la disattivazione degli avvisi.")
        else:
            bot.sendMessage(chat_id, "Gli avvisi sono già stati disattivati.")
    elif "/admin" in text:
        if status_user=="A":
            if type_msg=="LK":
                admin=True
        else:
            bot.sendMessage(chat_id, "Non sei un admin, pertanto non hai i permessi per utilizzare questa azione.")
    else:
        bot.sendMessage(chat_id, "Questo comando non è stato riconosciuto.", reply_markup=start)

    if admin:
        ## CONTROLLO AZIONI ADMIN
        azione=list(text.split(" "))
        admin_err1=False
        if(azione[0]=="/admin" and len(azione)>=2):
            if(azione[1]=="help" and len(azione)==2):
                # Elenco azioni
                bot.sendMessage(chat_id, "Ecco l'elenco delle azione che puoi eseguire:\n/admin\n>> avviso Messaggio da inviare\n>> all users Messaggio da inviare (solo messaggi 'fondamentali')\n>> call\n>> >> aggiungi Nome call da aggiungere LinkCall\n>> >> modifica Nome call da modificare LinkCallModificato\n>> >> elimina Nome call da eliminare\n>> avvisi list\n>> >> aggiungi Chat_id\n>> >> elimina Chat_id\n>> progetto\n>> >> aggiungi Nome progetto da aggiungere LinkProgetto\n>> >> modifica Nome progetto da modificare LinkProgettoModificato\n>> >> elimina Nome progetto da eliminare\n>> progetto mozita\n>> >> aggiungi Nome progetto comunitario da aggiungere LinkProgetto\n>> >> modifica Nome progetto comunitario da modificare LinkProgettoModificato\n>> >> elimina Nome progetto comunitario da eliminare\n>> collaboratore\n>> >> aggiungi Nome Cognome (@usernameTelegram)\n>> >> elimina Nome Cognome (@usernameTelegram)\n\nEsempi:\n/admin avviso Messaggio di prova\n/admin call aggiungi Nome call di esempio https://mozillaitalia.it")
            elif(azione[1]=="avviso" and len(azione)>=3):
                # Azioni sugli avvisi
                del azione[0]
                del azione[0]
                messaggio=' '.join(azione)
                for x in avvisi_on_list:
                    try:
                        bot.sendMessage(x, messaggio + "\n\n--------------------\nRicevi questo messaggio perché hai attivato le notifiche per le novità in Mozilla Italia. Puoi controllare il tuo stato attuale, attivandole o disattivandole, rapidamente digitando /avvisi.")
                        bot.sendMessage(chat_id, "Messaggio inviato alla chat: "+str(x))
                    except Exception as e:
                        print("Excep:08 -> "+str(e))
                        bot.sendMessage(chat_id, "Non è stato possibile inviare il messaggio alla chat: "+str(x))
                bot.sendMessage(chat_id, "Messaggio inviato correttamente a tutti gli utenti iscritti alle news.")
            elif(azione[1]=="all" and azione[2]=="users" and len(azione)>=4):
                # Azioni sugli avvisi importanti (tutti gli utenti)
                del azione[0]
                del azione[0]
                del azione[0]
                messaggio=' '.join(azione)
                for x in all_users:
                    try:
                        bot.sendMessage(x, messaggio)
                        bot.sendMessage(chat_id, "Messaggio inviato alla chat: "+str(x))
                    except Exception as e:
                        print("Excep:07 -> "+str(e))
                        bot.sendMessage(chat_id, "Non è stato possibile inviare il messaggio alla chat: "+str(x))
                bot.sendMessage(chat_id, "Messaggio inviato correttamente a tutti gli utenti.")
            elif(azione[1]=="call" and len(azione)>=5):
                # Azioni sulle call mensili
                if(azione[2]=="aggiungi"):
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    link=azione[-1]
                    del azione[-1]
                    nome=' '.join(azione)
                    if not (nome in call_mensili_list):
                        call_mensili_list[str(nome)]=str(link)
                        try:
                            with open(call_mensili_list_path, "wb") as f:
                                f.write(json.dumps(call_mensili_list).encode("utf-8"))
                            bot.sendMessage(chat_id, "Call mensile '"+str(nome)+"' ("+str(link)+") inserita correttamente.")
                        except Exception as e:
                            print("Excep:09 -> "+str(e))
                            bot.sendMessage(chat_id, "Si è verificato un errore inaspettato e non è possibile salvare 'call_mensili_list.json'.")
                    else:
                        bot.sendMessage(chat_id, "La call mensile '"+str(nome)+"' è già presente.")
                elif(azione[2]=="modifica"):
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    link=azione[-1]
                    del azione[-1]
                    nome=' '.join(azione)
                    if nome in call_mensili_list:
                        call_mensili_list[str(nome)]=str(link)
                        try:
                            with open(call_mensili_list_path, "wb") as f:
                                f.write(json.dumps(call_mensili_list).encode("utf-8"))
                            bot.sendMessage(chat_id, "Call mensile '"+str(nome)+"' ("+str(link)+") modificata correttamente.")
                        except Exception as e:
                            print("Excep:10 -> "+str(e))
                            bot.sendMessage(chat_id, "Si è verificato un errore inaspettato e non è possibile salvare 'call_mensili_list.json'.")
                    else:
                        bot.sendMessage(chat_id, "La call mensile '"+str(nome)+"' non è stata trovata.")
                elif(azione[2]=="elimina"):
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    nome=' '.join(azione)
                    if nome in call_mensili_list:
                        del call_mensili_list[str(nome)]
                        try:
                            with open(call_mensili_list_path, "wb") as f:
                                f.write(json.dumps(call_mensili_list).encode("utf-8"))
                            bot.sendMessage(chat_id, "Call mensile '"+str(nome)+"' eliminata correttamente.")
                        except Exception as e:
                            print("Excep:11 -> "+str(e))
                            bot.sendMessage(chat_id, "Si è verificato un errore inaspettato e non è possibile salvare 'call_mensili_list.json'.")
                    else:
                        bot.sendMessage(chat_id, "La call mensile '"+str(nome)+"' non è stata trovata.")
                else:
                    admin_err1=True
            elif(azione[1]=="avvisi" and azione[2]=="list" and len(azione)==5):
                # Azioni sugli utenti (chat_id) presenti in avvisi_on_list.json
                if(azione[3]=="aggiungi"):
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    temp_chat_id=int(azione[0])
                    if not (temp_chat_id in avvisi_on_list):
                        avvisi_on_list.append(temp_chat_id)
                        try:
                            with open(avvisi_on_list_path, "wb") as f:
                                f.write(json.dumps(avvisi_on_list).encode("utf-8"))
                            bot.sendMessage(chat_id, "La chat_id '"+str(temp_chat_id)+"' è stata inserita correttamente.")
                        except Exception as e:
                            print("Excep:12 -> "+str(e))
                            bot.sendMessage(chat_id, "Si è verificato un errore inaspettato e non è possibile salvare 'avvisi_on_list.json'.")
                    else:
                        bot.sendMessage(chat_id, "La chat_id '"+str(temp_chat_id)+"' è già presente.")
                elif(azione[3]=="elimina"):
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    temp_chat_id=int(azione[0])
                    if temp_chat_id in avvisi_on_list:
                        avvisi_on_list.remove(temp_chat_id)
                        try:
                            with open(avvisi_on_list_path, "wb") as f:
                                f.write(json.dumps(avvisi_on_list).encode("utf-8"))
                            bot.sendMessage(chat_id, "La chat_id '"+str(temp_chat_id)+"' è stata eliminata correttamente.")
                        except Exception as e:
                            print("Excep:13 -> "+str(e))
                            bot.sendMessage(chat_id, "Si è verificato un errore inaspettato e non è possibile salvare 'avvisi_on_list.json'.")
                    else:
                        bot.sendMessage(chat_id, "La chat_id '"+str(temp_chat_id)+"' non è stata trovata.")
                else:
                    admin_err1=True
            elif(azione[1]=="progetto" and azione[2]=="mozita" and len(azione)>=5):
                # Azioni sui progetti comunitari (mozilla italia)
                if(azione[3]=="aggiungi"):
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    link=azione[-1]
                    del azione[-1]
                    nome=' '.join(azione)
                    if not (nome in progetti_mozita_list):
                        progetti_mozita_list[str(nome)]=str(link)
                        try:
                            with open(progetti_mozita_list, "wb") as f:
                                f.write(json.dumps(progetti_mozita_list).encode("utf-8"))
                            bot.sendMessage(chat_id, "Progetto comunitario '"+str(nome)+"' ("+str(link)+") inserito correttamente.")
                        except Exception as e:
                            print("Excep:14 -> "+str(e))
                            bot.sendMessage(chat_id, "Si è verificato un errore inaspettato e non è possibile salvare 'progetti_mozita_list.json'.")
                    else:
                        bot.sendMessage(chat_id, "Il progetto comunitario '"+str(nome)+"' è già presente.")
                elif(azione[3]=="modifica"):
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    link=azione[-1]
                    del azione[-1]
                    nome=' '.join(azione)
                    if nome in progetti_mozita_list:
                        progetti_mozita_list[str(nome)]=str(link)
                        try:
                            with open(progetti_mozita_list_path, "wb") as f:
                                f.write(json.dumps(progetti_mozita_list).encode("utf-8"))
                            bot.sendMessage(chat_id, "Progetto comunitario '"+str(nome)+"' ("+str(link)+") modificato correttamente.")
                        except Exception as e:
                            print("Excep:15 -> "+str(e))
                            bot.sendMessage(chat_id, "Si è verificato un errore inaspettato e non è possibile salvare 'progetti_mozita_list.json'.")
                    else:
                        bot.sendMessage(chat_id, "Il progetto comunitario '"+str(nome)+"' non è stato trovato.")
                elif(azione[3]=="elimina"):
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    nome=' '.join(azione)
                    if nome in progetti_mozita_list:
                        del progetti_mozita_list[str(nome)]
                        try:
                            with open(progetti_mozita_list_path, "wb") as f:
                                f.write(json.dumps(progetti_mozita_list).encode("utf-8"))
                            bot.sendMessage(chat_id, "Progetto comunitario '"+str(nome)+"' eliminato correttamente.")
                        except Exception as e:
                            print("Excep:16 -> "+str(e))
                            bot.sendMessage(chat_id, "Si è verificato un errore inaspettato e non è possibile salvare 'progetti_mozita_list.json'.")
                    else:
                        bot.sendMessage(chat_id, "Il progetto comunitario '"+str(nome)+"' non è stato trovato.")
                else:
                    admin_err1=True
            elif(azione[1]=="progetto" and len(azione)>=4):
                # Azione sui progetti (mozilla)
                if(azione[2]=="aggiungi"):
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    link=azione[-1]
                    del azione[-1]
                    nome=' '.join(azione)
                    if not (nome in progetti_list):
                        progetti_list[str(nome)]=str(link)
                        try:
                            with open(progetti_list_path, "wb") as f:
                                f.write(json.dumps(progetti_list).encode("utf-8"))
                            bot.sendMessage(chat_id, "Progetto '"+str(nome)+"' ("+str(link)+") inserito correttamente.")
                        except Exception as e:
                            print("Excep:17 -> "+str(e))
                            bot.sendMessage(chat_id, "Si è verificato un errore inaspettato e non è possibile salvare 'progetti_list.json'.")
                    else:
                        bot.sendMessage(chat_id, "Il progetto '"+str(nome)+"' è già presente.")
                elif(azione[2]=="modifica"):
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    link=azione[-1]
                    del azione[-1]
                    nome=' '.join(azione)
                    if nome in progetti_list:
                        progetti_list[str(nome)]=str(link)
                        try:
                            with open(progetti_list_path, "wb") as f:
                                f.write(json.dumps(progetti_list).encode("utf-8"))
                            bot.sendMessage(chat_id, "Progetto '"+str(nome)+"' ("+str(link)+") modificato correttamente.")
                        except Exception as e:
                            print("Excep:18 -> "+str(e))
                            bot.sendMessage(chat_id, "Si è verificato un errore inaspettato e non è possibile salvare 'progetti_list.json'.")
                    else:
                        bot.sendMessage(chat_id, "Il progetto '"+str(nome)+"' non è stato trovato.")
                elif(azione[2]=="elimina"):
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    nome=' '.join(azione)
                    if nome in progetti_list:
                        del progetti_list[str(nome)]
                        try:
                            with open(progetti_list_path, "wb") as f:
                                f.write(json.dumps(progetti_list).encode("utf-8"))
                            bot.sendMessage(chat_id, "Progetto '"+str(nome)+"' eliminato correttamente.")
                        except Exception as e:
                            print("Excep:19 -> "+str(e))
                            bot.sendMessage(chat_id, "Si è verificato un errore inaspettato e non è possibile salvare 'progetti_list.json'.")
                    else:
                        bot.sendMessage(chat_id, "Il progetto '"+str(nome)+"' non è stato trovato.")
                else:
                    admin_err1=True
            elif(azione[1]=="collaboratore" and len(azione)>=4):
                # Azione sui collaboratori
                if(azione[2]=="aggiungi"):
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    nome=' '.join(azione)
                    if not (nome in collaboratori_hub):
                        collaboratori_hub.append(str(nome))
                        try:
                            with open(collaboratori_hub_path, "wb") as f:
                                f.write(json.dumps(sorted(collaboratori_hub)).encode("utf-8"))
                            bot.sendMessage(chat_id, "'"+str(nome)+"' aggiunto correttamente ai collaboratori.")
                        except Exception as e:
                            print("Excep:20 -> "+str(e))
                            bot.sendMessage(chat_id, "Si è verificato un errore inaspettato e non è possibile salvare 'collaboratori_hub.json'.")
                    else:
                        bot.sendMessage(chat_id, "'"+str(nome)+"' è già presente nella lista dei collaboratori.")
                elif(azione[2]=="elimina"):
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    nome=' '.join(azione)
                    if nome in collaboratori_hub:
                        collaboratori_hub.remove(str(nome))
                        try:
                            with open(collaboratori_hub_path, "wb") as f:
                                f.write(json.dumps(collaboratori_hub).encode("utf-8"))
                            bot.sendMessage(chat_id, "'"+str(nome)+"' rimosso correttamente dai collaboratori.")
                        except Exception as e:
                            print("Excep:21 -> "+str(e))
                            bot.sendMessage(chat_id, "Si è verificato un errore inaspettato e non è possibile salvare 'collaboratori_hub.json'.")
                    else:
                        bot.sendMessage(chat_id, "'"+str(nome)+"' non è presente nella lista dei collaboratori.")
                else:
                    admin_err1=True
            else:
                admin_err1=True
        else:
            bot.sendMessage(chat_id, "Errore: Comando non riconosciuto.\nRicorda che se vuoi ottenere aiuto su ciò che puoi fare nella sezione ADMIN devi digitare anche la parola 'help'. In questo modo:\n'/admin help'.")

        if admin_err1:
            bot.sendMessage(chat_id, "Questo comando nella sezione ADMIN non è stato riconosciuto.\n\nPer scoprire tutti i comandi consentiti in questa sezione digita '/admin help'")

    try:
        stampa=str(localtime)+"  --  Utente: "+str(user_name)+" ("+str(user_id)+")["+str(status_user)+"]  --  Chat: "+str(chat_id)+"\n >> >> Tipo messaggio: "+str(type_msg)+"\n >> >> Contenuto messaggio: "+str(text)+"\n--------------------\n"
        print(stampa)
    except Exception as e:
        stampa="Excep:01 -> "+str(e)+"\n--------------------\n"
        print(stampa)

    try:
        file=open("history_hub.txt","a",-1,"UTF-8") #apre il file in scrittura "append" per inserire orario e data -> log di utilizzo del bot (ANONIMO)
        file.write(stampa) #ricordare che l'orario è in fuso orario UTC pari a 0 (Greenwich, Londra) - mentre l'Italia è a +1 (CET) o +2 (CEST - estate)
        file.close()
    except Exception as e:
        print("Excep:02 -> "+str(e))


try:
    bot=telepot.Bot(TOKEN)
    MessageLoop(bot, {'chat': risposte, 'callback_query': risposte}).run_as_thread()
except Exception as e:
    print("ERRORE GENERALE.\n\nError: "+str(e)+"\n--------------------\n")

while 1:
    time.sleep(10)
