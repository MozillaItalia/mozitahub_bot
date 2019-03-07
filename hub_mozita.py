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
    print("Il file di configurazione non è presente. Rinomina il file 'config-sample.ini' in 'config.ini' e inserisci il token.".encode("utf-8"))
    exit()

script_path = os.path.dirname(os.path.realpath(__file__))
config_parser = ConfigParser()
config_parser.read(os.path.join(script_path, "config.ini"))

TOKEN = config_parser.get("access", "token")

if TOKEN == "":
    print("Token non presente.")
    exit()

if Path("frasi.json").exists():
    frasi = json.loads(open("frasi.json",encoding="utf8").read())
else:
    print("File frasi non presente.")
    exit()

versione = "1.1.9"
ultimoAggiornamento = "08-03-2019"

print("Versione: "+versione+" - Aggiornamento: "+ultimoAggiornamento)

MIN_ANNO=2017 #costante - anno minimo delle call
MAX_ANNO=2019 #variabile - anno massimo delle call

adminlist_path = "adminlist_hub.json"
call_mensili_list_path = "call_mensili_list.json"
avvisi_on_list_path = "avvisi_on_list.json"
progetti_list_path = "progetti_list.json"
progetti_mozita_list_path = "progetti_mozita_list.json"
collaboratori_hub_path = "collaboratori_hub.json"
all_users_path = "all_users.json"
AdminList = []
if Path(call_mensili_list_path).exists():
    call_mensili_list = json.loads(open(call_mensili_list_path).read())
else:
    call_mensili_list = {}
if Path(avvisi_on_list_path).exists():
    avvisi_on_list = json.loads(open(avvisi_on_list_path).read())
else:
    avvisi_on_list = []
if Path(progetti_list_path).exists():
    progetti_list = json.loads(open(progetti_list_path).read())
else:
    progetti_list = {}
if Path(progetti_mozita_list_path).exists():
    progetti_mozita_list = json.loads(open(progetti_mozita_list_path).read())
else:
    progetti_mozita_list = {}
if Path(collaboratori_hub_path).exists():
    collaboratori_hub = json.loads(open(collaboratori_hub_path).read())
else:
    collaboratori_hub = []
if Path(all_users_path).exists():
    all_users = json.loads(open(all_users_path).read())
else:
    all_users = []

listaMesi = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

def generaListaPerAnno(year,type):
    call_mensili_list_ANNO_path = "call_mensili_list_"+str(year)+".json"
    if Path(call_mensili_list_ANNO_path).exists():
        call_mensili_list_ANNO = json.loads(open(call_mensili_list_ANNO_path).read())
    else:
        call_mensili_list_ANNO = {}
    if(str(type)=="button"):
        load_listaCallANNO=[]
        for x in call_mensili_list_ANNO:
            load_listaCallANNO.append([InlineKeyboardButton(text=str(x), url=str(call_mensili_list_ANNO[x]))])
        return InlineKeyboardMarkup(inline_keyboard=load_listaCallANNO)
    elif str(type)=="":
        load_listaCallANNO={}
        for x in call_mensili_list_ANNO:
            load_listaCallANNO[str(x)]=str(call_mensili_list_ANNO[x])
        return load_listaCallANNO

def first_friday_of_the_month(year, month):
    # questa funzione serve per calcolare il primo venerdì del mese
    for day, weekday in calendar.Calendar().itermonthdays2(year, month):
        if weekday == 4:
            if(day != 0):
                return day
            else:
                return day+7


def risposte(msg):
    localtime = datetime.now()
    data_salvataggio = localtime.strftime("%Y_%m_%d")
    localtime = localtime.strftime("%d/%m/%y %H:%M:%S")
    messaggio = msg
    type_msg = "NM"  # Normal Message
    status_user = "-"

    global frasi

    if Path(adminlist_path).exists():
        global AdminList
        AdminList = json.loads(open(adminlist_path).read())
    else:
        # nel caso in cui non dovesse esistere alcun file "adminlist.json" imposta staticamente l'userid di Sav22999 -> così da poter confermare anche altri utenti
        AdminList = [240188083]

    if "text" in msg:
        # EVENTO MESSAGGIO (SOTTO-EVENTI MESSAGGIO)
        text = str(msg['text'])
        if "entities" in msg:
            # EVENTO LINK
            type_msg = "LK"  # Link
        else:
            # EVENTO MESSAGGIO PURO
            type_msg = "NM"  # Normal Message
    elif "data" in msg:
        # EVENTO PRESS BY INLINE BUTTON
        text = str(msg['data'])
        # print("Callback_query")
        type_msg = "BIC"  # Button Inline Click
    else:
        # EVENTO NON CATTURA/GESTITO -> ELIMINARE AUTOMATICAMENTE IL MESSAGGIO
        text = "--Testo non identificato--"
        type_msg = "NI"  # Not Identified

    user_id = msg['from']['id']
    if user_id in AdminList:
        status_user = "A"
    nousername = False
    if "username" in msg['from']:
        user_name = msg['from']['username']
    else:
        user_name = "[*NessunUsername*]"
        nousername = True

    if not "chat" in msg:
        msg = msg["message"]
    chat_id = msg['chat']['id']

    if(datetime.now().month == 12):
        annoCall = str(datetime.now().year+1)
        meseCall = listaMesi[0]
        giornoCall = str(first_friday_of_the_month(int(annoCall), 1))
    else:
        annoCall = str(datetime.now().year)
        giornoCall = first_friday_of_the_month(int(annoCall), datetime.now().month)
        if(datetime.now().day >= giornoCall):
            meseCall = datetime.now().month+1
            giornoCall = str(first_friday_of_the_month(
                int(annoCall), datetime.now().month+1))
        else:
            meseCall = datetime.now().month
            giornoCall = str(giornoCall)
        meseCall = listaMesi[meseCall-1]
        # non è possibile utilizzare la funzione datetime.now().(month+1).strftime("%B") perché lo restituisce in inglese

    home = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Vai al gruppo Home 🦊', url='https://t.me/joinchat/BCql3UMy26nl4qxuRecDsQ')],
    ])

    feedback = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Vai in 'Home' e lascia il tuo feedback 💬", url='https://t.me/joinchat/BCql3UMy26nl4qxuRecDsQ')],
        [InlineKeyboardButton(text="Chiedi di voler contribuire al bot in 'Home' ➡️", url='https://t.me/joinchat/BCql3UMy26nl4qxuRecDsQ')]
    ])

    start = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Mostrami che cosa posso fare ➡️', callback_data='/help')],
        [InlineKeyboardButton(text='Ho bisogno di assistenza 🆘', callback_data='/supporto')],
    ])

    supporto = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Supporto via Telegram', url='https://t.me/joinchat/BCql3UMy26nl4qxuRecDsQ'),
         InlineKeyboardButton(text='Supporto via forum', callback_data='/forum')],
        [InlineKeyboardButton(text='Leggi le FAQ dal forum di Mozilla Italia', url='https://forum.mozillaitalia.org/index.php?board=9.0')]
    ])

    help = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Gruppi 👥', callback_data='/gruppi'),
        InlineKeyboardButton(text='Vademecum', callback_data='/vademecum')],
        [InlineKeyboardButton(text='Avvisi 📢', callback_data='/avvisi'),
        InlineKeyboardButton(text='Supporto 🆘', callback_data='/supporto')],
        [InlineKeyboardButton(text='Call', callback_data='/call'),
        InlineKeyboardButton(text='Prossima call 📆', callback_data='/prossimacall'),
        InlineKeyboardButton(text='Lista call', callback_data='/listacall')],
        [InlineKeyboardButton(text='Info ℹ️', callback_data='/info'),
        InlineKeyboardButton(text='Progetti attivi', callback_data='/progetti'),
        InlineKeyboardButton(text='Regolamento 📙', callback_data='/regolamento')],
        [InlineKeyboardButton(text='Home 🦊', callback_data='/home'),
        InlineKeyboardButton(text='Collabora ✌🏻', callback_data='/collabora')],
        [InlineKeyboardButton(text='News 🆕', callback_data='/news'),
        InlineKeyboardButton(text='IoT', callback_data='/iot')],
        [InlineKeyboardButton(text='Developer 💻', callback_data='/developer'),
        InlineKeyboardButton(text='Design 📐', callback_data='/design')],
        [InlineKeyboardButton(text='Feedback 💬', callback_data='/feedback')],
    ])

    gruppi = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Home 🦊', url='https://t.me/joinchat/BCql3UMy26nl4qxuRecDsQ'),
         InlineKeyboardButton(text='News 🆕', url='https://t.me/mozItaNews')],
        [InlineKeyboardButton(text='Voglio diventare volontario ✌🏻', url='https://t.me/joinchat/B1cgtEQAHkGVBTbI0XPd-A')],
        [InlineKeyboardButton(text='Developer 💻', url='https://t.me/joinchat/B1cgtENXHcxd3jzFar7Kuw'),
         InlineKeyboardButton(text='L10N (chiedi in Home) 🗺', url='https://t.me/joinchat/BCql3UMy26nl4qxuRecDsQ')],
        [InlineKeyboardButton(text='Design 📐', url='https://t.me/joinchat/B1cgtA7DF3qDzuRvsEtT6g'),
         InlineKeyboardButton(text='IoT', url='https://t.me/joinchat/B1cgtEzLzr0gvSJcEicq1g')],
    ])

    developer = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Vai al gruppo Developer', url='https://t.me/joinchat/B1cgtENXHcxd3jzFar7Kuw')],
    ])

    design = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Vai al gruppo Design Team 📐', url='https://t.me/joinchat/B1cgtA7DF3qDzuRvsEtT6g')],
    ])

    iot = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Vai al gruppo IoT', url='https://t.me/joinchat/B1cgtEzLzr0gvSJcEicq1g')],
    ])

    vademecum = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Vademecum Generale', callback_data='/vademecumgenerale'),
         InlineKeyboardButton(text='Vademecum Tecnico', callback_data='/vademecumtecnico')],
    ])

    collabora = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Sì, vai al gruppo 'Home' 🆗", url='https://t.me/joinchat/BCql3UMy26nl4qxuRecDsQ'),
         InlineKeyboardButton(text="No, ma vorrei collaborare ✌🏻", url='https://t.me/joinchat/B1cgtEQAHkGVBTbI0XPd-A')],
    ])

    news = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Vai al canale ufficiale 'News' 🆕", url='https://t.me/mozItaNews')],
    ])

    forum = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Vai al forum di Mozilla Italia 🦊', url='https://forum.mozillaitalia.org/')],
    ])

    call = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Vedi tutte le call',  callback_data='/listacall')],
        [InlineKeyboardButton(text='Scopri quando sarà la prossima call 📆', callback_data='/prossimacall')],
    ])

    load_listaCall = []
    for x in call_mensili_list:
        load_listaCall.append([InlineKeyboardButton(text=str(x), callback_data=str(call_mensili_list[x]))])

    listaCall = InlineKeyboardMarkup(inline_keyboard=load_listaCall)

    listaCall2017 = generaListaPerAnno(2017,"button")
    listaCall2018 = generaListaPerAnno(2018,"button")
    listaCall2019 = generaListaPerAnno(2019,"button")

    load_progetti = []
    for x in progetti_list:
        load_progetti.append([InlineKeyboardButton(text=str(x), url=str(progetti_list[x]))])

    progetti = InlineKeyboardMarkup(inline_keyboard=load_progetti)

    load_progettiMozIta = []
    for x in progetti_mozita_list:
        load_progettiMozIta.append([InlineKeyboardButton(text=str(x), url=str(progetti_mozita_list[x]))])

    progettimozita = InlineKeyboardMarkup(inline_keyboard=load_progettiMozIta)

    regolamento = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Leggi Regolamento 📙', url='https://github.com/Sav22999/Guide/blob/master/Mozilla%20Italia/Telegram/regolamento.md')],
    ])

    avvisi = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Attiva avvisi 🔔', callback_data="/avvisiOn")],
        [InlineKeyboardButton(text='Disattiva avvisi 🔕', callback_data="/avvisiOff")],
    ])

    '''
    nome_nome = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Testo bottone (riga 1, col 1)', callback_data='/comando'),
                    InlineKeyboardButton(text='Testo bottone 2 (riga 1, col 2)', callback_data='/comando2')],
                    [InlineKeyboardButton(text='Testo bottone 3 (riga 2, col 1-2)', url='https://t.me/')],
                ])
    '''

    admin = False
    collaboratori_stampa = ""
    for x in sorted(collaboratori_hub):
        collaboratori_stampa += "\n - "+x

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
        stato_avvisi = frasi["avvisiStatoOn"]
    else:
        stato_avvisi = frasi["avvisiStatoOff"]

    if text == "/home":
        bot.sendMessage(chat_id, frasi["home"], reply_markup=home, parse_mode="Markdown")
    # elif text=="/stop":
        #bot.sendMessage(chat_id, "Stai per disattivare MozIta Hub. Per attivarlo nuovamente sara' sufficiente premere il pulsante sottostante 'Avvia' o digitare /start. Se lo desideri puoi anche lasciarci un feedback sulla tua esperienza d'utilizzo del bot e la motivazione dell'abbandono. Grazie.", reply_markup=stop)
    elif text == "/start":
        bot.sendMessage(chat_id, frasi["start"], parse_mode="Markdown")
        bot.sendMessage(chat_id, frasi["start2"], reply_markup=start, parse_mode="Markdown")
        if nousername:
            bot.sendMessage(chat_id, frasi["start_nousername"], parse_mode="Markdown")
    elif text == "/supporto":
        bot.sendMessage(chat_id, frasi["supporto"], parse_mode="Markdown")
        bot.sendMessage(chat_id, frasi["supporto2"], reply_markup=supporto, parse_mode="Markdown")
    elif text == "/gruppi":
        bot.sendMessage(chat_id, frasi["gruppi"], reply_markup=gruppi, parse_mode="Markdown")
    elif text == "/collabora":
        bot.sendMessage(chat_id, frasi["collabora"], parse_mode="Markdown")
        bot.sendMessage(chat_id, frasi["collabora2"], reply_markup=collabora, parse_mode="Markdown")
    elif text == "/vademecum":
        bot.sendMessage(chat_id, frasi["vademecum"], reply_markup=vademecum, parse_mode="Markdown")
    elif text == "/vademecumgenerale":
        bot.sendDocument(chat_id, open("VG.pdf","rb"))
    elif text == "/vademecumtecnico":
        bot.sendDocument(chat_id, open("VT.pdf","rb"))
    elif text == "/feedback":
        bot.sendMessage(chat_id, frasi["feedbak"], reply_markup=feedback, parse_mode="Markdown")
    elif text == "/help":
        bot.sendMessage(chat_id, frasi["help"], parse_mode="Markdown")
        bot.sendMessage(chat_id, frasi["help2"], reply_markup=help, parse_mode="Markdown")
    elif text == "/news":
        bot.sendMessage(chat_id, frasi["news"], reply_markup=news, parse_mode="Markdown")
    elif text == "/info":
        bot.sendMessage(chat_id, str(((frasi["info"]).replace("{{**versione**}}",str(versione))).replace("{{**ultimoAggiornamento**}}",str(ultimoAggiornamento))).replace("{{**collaboratori_stampa**}}",str(collaboratori_stampa)))
    elif text == "/forum":
        bot.sendMessage(chat_id, frasi["forum"], reply_markup=forum, parse_mode="Markdown")
    elif text == "/developer":
        bot.sendMessage(chat_id, frasi["developer"], reply_markup=developer, parse_mode="Markdown")
    elif text == "/design":
        bot.sendMessage(chat_id, frasi["design"], reply_markup=design, parse_mode="Markdown")
    elif text == "/iot":
        bot.sendMessage(chat_id, frasi["iot"], reply_markup=iot, parse_mode="Markdown")
    elif text == "/call":
        bot.sendMessage(chat_id, frasi["call"], reply_markup=call)
    elif text == "/listacall":
        bot.sendMessage(chat_id, frasi["listacall"], reply_markup=listaCall, parse_mode="Markdown")
    elif text == "/prossimacall":
        bot.sendMessage(chat_id, str(((frasi["prossima_call"]).replace("{{**giornoCall**}}",str(giornoCall))).replace("{{**meseCall**}}",str(meseCall))).replace("{{**annoCall**}}",str(annoCall)), parse_mode="Markdown")
    elif text == "/progetti":
        bot.sendMessage(chat_id, frasi["progetti"], reply_markup=progetti, parse_mode="Markdown")
        bot.sendMessage(chat_id, frasi["progetti2"], reply_markup=progettimozita, parse_mode="Markdown")
    elif text == "/regolamento":
        bot.sendMessage(chat_id, frasi["regolamento"], reply_markup=regolamento, parse_mode="Markdown")
    elif text == "/avvisi":
        bot.sendMessage(chat_id, str(frasi["avvisi"]).replace("{{**stato_avvisi**}}",str(stato_avvisi)), reply_markup=avvisi, parse_mode="Markdown")
    elif text == "/avvisiOn":
        if not (user_id in avvisi_on_list):
            avvisi_on_list.append(user_id)
            try:
                with open(avvisi_on_list_path, "wb") as f:
                    f.write(json.dumps(avvisi_on_list).encode("utf-8"))
                bot.sendMessage(chat_id, frasi["avvisiOn"], parse_mode="Markdown")
            except Exception as e:
                print("Excep:05 -> "+str(e))
                bot.sendMessage(chat_id, frasi["avvisiOn2"], parse_mode="Markdown")
        else:
            bot.sendMessage(chat_id, frasi["avvisiOn3"], parse_mode="Markdown")
    elif text == "/avvisiOff":
        if user_id in avvisi_on_list:
            avvisi_on_list.remove(user_id)
            try:
                with open(avvisi_on_list_path, "wb") as f:
                    f.write(json.dumps(avvisi_on_list).encode("utf-8"))
                bot.sendMessage(chat_id, frasi["avvisiOff"], parse_mode="Markdown")
            except Exception as e:
                print("Excep:06 -> "+str(e))
                bot.sendMessage(chat_id, frasi["avvisiOff2"])
        else:
            bot.sendMessage(chat_id, frasi["avvisiOff3"])
    elif "/anno2017" in text:
        bot.sendMessage(chat_id, str(frasi["anno"]).replace("{{**anno**}}","2017"), reply_markup=listaCall2017, parse_mode="Markdown")
    elif "/anno2018" in text:
        bot.sendMessage(chat_id, str(frasi["anno"]).replace("{{**anno**}}","2018"), reply_markup=listaCall2018, parse_mode="Markdown")
    elif "/anno2019" in text:
        bot.sendMessage(chat_id, str(frasi["anno"]).replace("{{**anno**}}","2019"), reply_markup=listaCall2019, parse_mode="Markdown")
    elif "/admin" in text:
        if status_user == "A":
            if type_msg == "LK":
                admin = True
        else:
            bot.sendMessage(chat_id, frasi["non_sei_admin"])
    else:
        bot.sendMessage(chat_id, frasi["comando_non_riconosciuto"], reply_markup=start)

    if admin:
        # CONTROLLO AZIONI ADMIN
        azione = list(text.split(" "))
        admin_err1 = False
        if(azione[0] == "/admin" and len(azione) >= 2):
            if(azione[1] == "help" and len(azione) == 2):
                # Elenco azioni
                bot.sendMessage(chat_id, "Ecco l'elenco delle azione che puoi eseguire:\n/admin\n>> avviso *Messaggio da inviare*\n>> all users *Messaggio da inviare* (solo messaggi 'fondamentali')\n>> call\n>> >> aggiungi *Mese (eventuale parte)* *Anno* *LinkCall*\n>> >> modifica *Mese (eventuale parte)* *Anno* *LinkCallModificato*\n>> >> elimina *Mese (eventuale parte)* *Anno*\n>> avvisi list\n>> >> aggiungi *Chat_id*\n>> >> elimina *Chat_id*\n>> progetto\n>> >> aggiungi *Nome progetto da aggiungere* *LinkProgetto*\n>> >> modifica *Nome progetto da modificare* *LinkProgettoModificato*\n>> >> elimina *Nome progetto da eliminare*\n>> progetto mozita\n>> >> aggiungi *Nome progetto comunitario da aggiungere* *LinkProgetto*\n>> >> modifica *Nome progetto comunitario da modificare* *LinkProgettoModificato*\n>> >> elimina *Nome progetto comunitario da eliminare*\n>> collaboratore\n>> >> aggiungi *Nome Cognome (@usernameTelegram)*\n>> >> elimina *Nome Cognome (@usernameTelegram)*\n\nEsempi:\n/admin avviso Messaggio di prova\n/admin call aggiungi Nome call di esempio 2019 https://mozillaitalia.it")
            elif(azione[1] == "avviso" and len(azione) >= 3):
                # Azioni sugli avvisi
                del azione[0]
                del azione[0]
                messaggio = ' '.join(azione)
                error08=False
                for x in avvisi_on_list:
                    try:
                        bot.sendMessage(x, messaggio + "\n\n--------------------\nRicevi questo messaggio perché hai attivato le notifiche per le novità in Mozilla Italia. Puoi controllare il tuo stato attuale, attivandole o disattivandole, rapidamente digitando /avvisi.", parse_mode="Markdown")
                        bot.sendMessage(chat_id, "✔️ Messaggio inviato alla chat: "+str(x))
                    except Exception as e:
                        print("Excep:08 -> "+str(e))
                        bot.sendMessage(chat_id, "❌ Non è stato possibile inviare il messaggio alla chat: "+str(x))
                        error08=True
                if(not error08):
                    bot.sendMessage(chat_id, "Messaggio inviato correttamente a tutti gli utenti iscritti alle news.\n\nIl messaggio inviato è:\n"+messaggio, parse_mode="Markdown")
                else:
                    bot.sendMessage(chat_id, "Messaggio inviato correttamente ad alcune chat.\n\nIl messaggio inviato è:\n"+messaggio, parse_mode="Markdown")

            elif(azione[1] == "all" and azione[2] == "users" and len(azione) >= 4):
                # Azioni sugli avvisi importanti (tutti gli utenti)
                del azione[0]
                del azione[0]
                del azione[0]
                messaggio = ' '.join(azione)
                for x in all_users:
                    try:
                        bot.sendMessage(x, messaggio)
                        bot.sendMessage(chat_id, "Messaggio inviato alla chat: "+str(x))
                    except Exception as e:
                        print("Excep:07 -> "+str(e))
                        bot.sendMessage(chat_id, "Non è stato possibile inviare il messaggio alla chat: "+str(x))
                bot.sendMessage(chat_id, "Messaggio inviato correttamente a tutti gli utenti.")
            elif(azione[1] == "call" and len(azione) >= 6):
                # Azioni sulle call mensili
                if(azione[2] == "aggiungi"):
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    link = azione[-1]
                    del azione[-1]
                    anno = azione[-1]
                    del azione[-1]
                    nome = ' '.join(azione)
                    if(anno.isdigit() and int(anno)<=MAX_ANNO and int(anno)>=MIN_ANNO):
                        call_mensili_list_anno=generaListaPerAnno(int(anno),"")
                        call_mensili_list_anno_path="call_mensili_list_"+str(anno)+".json"
                        if not (nome in call_mensili_list_anno.keys()):
                            call_mensili_list_anno[str(nome)] = str(link)
                            try:
                                with open(call_mensili_list_anno_path, "wb") as f:
                                    f.write(json.dumps(call_mensili_list_anno).encode("utf-8"))
                                bot.sendMessage(chat_id, "Call mensile '"+str(nome)+"' ("+str(link)+") inserita correttamente nel '"+str(anno)+"'.")
                            except Exception as e:
                                print("Excep:09 -> "+str(e))
                                bot.sendMessage(chat_id, "Si è verificato un errore inaspettato e non è possibile salvare 'call_mensili_list"+str(anno)+".json'.")
                        else:
                            bot.sendMessage(chat_id, "La call mensile '"+str(nome)+"' è già presente nel '"+str(anno)+"'.")
                    else:
                        bot.sendMessage(chat_id, "L'anno selezionato '"+str(anno)+"' non è valido.")
                elif(azione[2] == "modifica"):
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    link = azione[-1]
                    del azione[-1]
                    anno = azione[-1]
                    del azione[-1]
                    nome = ' '.join(azione)
                    if(anno.isdigit() and int(anno)<=MAX_ANNO and int(anno)>=MIN_ANNO):
                        call_mensili_list_anno=generaListaPerAnno(int(anno),"")
                        call_mensili_list_anno_path="call_mensili_list_"+str(anno)+".json"
                        if nome in call_mensili_list_anno.keys():
                            call_mensili_list_anno[str(nome)] = str(link)
                            try:
                                with open(call_mensili_list_anno_path, "wb") as f:
                                    f.write(json.dumps(call_mensili_list_anno).encode("utf-8"))
                                bot.sendMessage(chat_id, "Call mensile '"+str(nome)+"' ("+str(link)+") del '"+str(anno)+"' modificata correttamente.")
                            except Exception as e:
                                print("Excep:10 -> "+str(e))
                                bot.sendMessage(chat_id, "Si è verificato un errore inaspettato e non è possibile salvare 'call_mensili_list_"+str(anno)+".json'.")
                        else:
                            bot.sendMessage(chat_id, "La call mensile '"+str(nome)+"' non è stata trovata nel '"+str(anno)+"'.")
                    else:
                        bot.sendMessage(chat_id, "L'anno selezionato '"+str(anno)+"' non è valido.")
                elif(azione[2] == "elimina"):
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    anno = azione[-1]
                    del azione[-1]
                    nome = ' '.join(azione)
                    if(anno.isdigit() and int(anno)<=MAX_ANNO and int(anno)>=MIN_ANNO):
                        call_mensili_list_anno=generaListaPerAnno(int(anno),"")
                        call_mensili_list_anno_path="call_mensili_list_"+str(anno)+".json"
                        if nome in call_mensili_list_anno:
                            del call_mensili_list_anno[str(nome)]
                            try:
                                with open(call_mensili_list_anno_path, "wb") as f:
                                    f.write(json.dumps(call_mensili_list_anno).encode("utf-8"))
                                bot.sendMessage(chat_id, "Call mensile '"+str(nome)+"' del '"+str(anno)+"' eliminata correttamente.")
                            except Exception as e:
                                print("Excep:11 -> "+str(e))
                                bot.sendMessage(chat_id, "Si è verificato un errore inaspettato e non è possibile salvare 'call_mensili_list"+str(anno)+".json'.")
                        else:
                            bot.sendMessage(chat_id, "La call mensile '"+str(nome)+"' non è stata trovata nel '"+str(anno)+"'.")
                    else:
                        bot.sendMessage(chat_id, "L'anno selezionato '"+str(anno)+"' non è valido.")
                else:
                    admin_err1 = True
            elif(azione[1] == "avvisi" and azione[2] == "list" and len(azione) == 5):
                # Azioni sugli utenti (chat_id) presenti in avvisi_on_list.json
                if(azione[3] == "aggiungi"):
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    temp_chat_id = int(azione[0])
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
                        bot.sendMessage(chat_id, "La chat_id '" +
                                        str(temp_chat_id)+"' è già presente.")
                elif(azione[3] == "elimina"):
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    temp_chat_id = int(azione[0])
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
                        bot.sendMessage(chat_id, "La chat_id '" + str(temp_chat_id)+"' non è stata trovata.")
                else:
                    admin_err1 = True
            elif(azione[1] == "progetto" and azione[2] == "mozita" and len(azione) >= 5):
                # Azioni sui progetti comunitari (mozilla italia)
                if(azione[3] == "aggiungi"):
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    link = azione[-1]
                    del azione[-1]
                    nome = ' '.join(azione)
                    if not (nome in progetti_mozita_list):
                        progetti_mozita_list[str(nome)] = str(link)
                        try:
                            with open(progetti_mozita_list, "wb") as f:
                                f.write(json.dumps(progetti_mozita_list).encode("utf-8"))
                            bot.sendMessage(chat_id, "Progetto comunitario '"+str(nome)+"' ("+str(link)+") inserito correttamente.")
                        except Exception as e:
                            print("Excep:14 -> "+str(e))
                            bot.sendMessage(chat_id, "Si è verificato un errore inaspettato e non è possibile salvare 'progetti_mozita_list.json'.")
                    else:
                        bot.sendMessage(chat_id, "Il progetto comunitario '"+str(nome)+"' è già presente.")
                elif(azione[3] == "modifica"):
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    link = azione[-1]
                    del azione[-1]
                    nome = ' '.join(azione)
                    if nome in progetti_mozita_list:
                        progetti_mozita_list[str(nome)] = str(link)
                        try:
                            with open(progetti_mozita_list_path, "wb") as f:
                                f.write(json.dumps(progetti_mozita_list).encode("utf-8"))
                            bot.sendMessage(chat_id, "Progetto comunitario '"+str(nome)+"' ("+str(link)+") modificato correttamente.")
                        except Exception as e:
                            print("Excep:15 -> "+str(e))
                            bot.sendMessage(chat_id, "Si è verificato un errore inaspettato e non è possibile salvare 'progetti_mozita_list.json'.")
                    else:
                        bot.sendMessage(chat_id, "Il progetto comunitario '"+str(nome)+"' non è stato trovato.")
                elif(azione[3] == "elimina"):
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    nome = ' '.join(azione)
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
                    admin_err1 = True
            elif(azione[1] == "progetto" and len(azione) >= 4):
                # Azione sui progetti (mozilla)
                if(azione[2] == "aggiungi"):
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    link = azione[-1]
                    del azione[-1]
                    nome = ' '.join(azione)
                    if not (nome in progetti_list):
                        progetti_list[str(nome)] = str(link)
                        try:
                            with open(progetti_list_path, "wb") as f:
                                f.write(json.dumps(progetti_list).encode("utf-8"))
                            bot.sendMessage(chat_id, "Progetto '"+str(nome)+"' ("+str(link)+") inserito correttamente.")
                        except Exception as e:
                            print("Excep:17 -> "+str(e))
                            bot.sendMessage(chat_id, "Si è verificato un errore inaspettato e non è possibile salvare 'progetti_list.json'.")
                    else:
                        bot.sendMessage(chat_id, "Il progetto '" + str(nome)+"' è già presente.")
                elif(azione[2] == "modifica"):
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    link = azione[-1]
                    del azione[-1]
                    nome = ' '.join(azione)
                    if nome in progetti_list:
                        progetti_list[str(nome)] = str(link)
                        try:
                            with open(progetti_list_path, "wb") as f:
                                f.write(json.dumps(progetti_list).encode("utf-8"))
                            bot.sendMessage(chat_id, "Progetto '"+str(nome)+"' ("+str(link)+") modificato correttamente.")
                        except Exception as e:
                            print("Excep:18 -> "+str(e))
                            bot.sendMessage(chat_id, "Si è verificato un errore inaspettato e non è possibile salvare 'progetti_list.json'.")
                    else:
                        bot.sendMessage(chat_id, "Il progetto '" + str(nome)+"' non è stato trovato.")
                elif(azione[2] == "elimina"):
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    nome = ' '.join(azione)
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
                        bot.sendMessage(chat_id, "Il progetto '" + str(nome)+"' non è stato trovato.")
                else:
                    admin_err1 = True
            elif(azione[1] == "collaboratore" and len(azione) >= 4):
                # Azione sui collaboratori
                if(azione[2] == "aggiungi"):
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    nome = ' '.join(azione)
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
                elif(azione[2] == "elimina"):
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    nome = ' '.join(azione)
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
                    admin_err1 = True
            else:
                admin_err1 = True
        else:
            bot.sendMessage(chat_id, "Errore: Comando non riconosciuto.\nRicorda che se vuoi ottenere aiuto su ciò che puoi fare nella sezione ADMIN devi digitare anche la parola 'help'. In questo modo:\n'/admin help'.")

        if admin_err1:
            bot.sendMessage(chat_id, "Questo comando nella sezione ADMIN non è stato riconosciuto.\n\nPer scoprire tutti i comandi consentiti in questa sezione digita '/admin help'")

    try:
        stampa = str(localtime)+"  --  Utente: "+str(user_name)+" ("+str(user_id)+")["+str(status_user)+"]  --  Chat: "+str(
            chat_id)+"\n >> >> Tipo messaggio: "+str(type_msg)+"\n >> >> Contenuto messaggio: "+str(text)+"\n--------------------\n"
        print(stampa)
    except Exception as e:
        stampa = "Excep:01 -> "+str(e)+"\n--------------------\n"
        print(stampa)

    try:
        if(os.path.exists("./history_mozitabot")==False):
            os.mkdir("./history_mozitabot")
    except Exception as e:
        print("Excep:22 -> "+str(e))

    try:
        # apre il file in scrittura "append" per inserire orario e data -> log di utilizzo del bot (ANONIMO)
        file = open("./history_mozitabot/log_"+str(data_salvataggio)+".txt", "a", -1, "UTF-8")
        # ricordare che l'orario è in fuso orario UTC pari a 0 (Greenwich, Londra) - mentre l'Italia è a +1 (CET) o +2 (CEST - estate)
        file.write(stampa)
        file.close()
    except Exception as e:
        print("Excep:02 -> "+str(e))


try:
    bot = telepot.Bot(TOKEN)
    MessageLoop(bot, {'chat': risposte, 'callback_query': risposte}).run_as_thread()
except Exception as e:
    print("ERRORE GENERALE.\n\nError: "+str(e)+"\n--------------------\n")

while 1:
    time.sleep(10)
