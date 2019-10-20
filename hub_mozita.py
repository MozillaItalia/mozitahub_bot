#!/usr/bin/python3
import os
from configparser import ConfigParser
import json
from pathlib import Path
from datetime import datetime
import calendar
import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

import telegram_events

if not os.path.isfile("config.ini"):
    print(
        "Il file di configurazione non è presente.\n" +
        "Rinomina il file 'config-sample.ini' in 'config.ini' e inserisci il token.".encode("utf-8"))
    exit()

script_path = os.path.dirname(os.path.realpath(__file__))
config_parser = ConfigParser()
config_parser.read(os.path.join(script_path, "config.ini"))

TOKEN = config_parser.get("access", "token")

if TOKEN == "":
    print("Token non presente.")
    exit()

# CARICAMENTO FRASI DA FILE

if Path("frasi.json").exists():
    frasi = json.loads(open("frasi.json", encoding="utf8").read())
else:
    print("File frasi non presente.")
    exit()

versione = "1.3.3"
ultimo_aggiornamento = "20-10-2019"

print("(MozItaBot) Versione: " + versione +
      " - Aggiornamento: " + ultimo_aggiornamento)

response = ""

# CARICAMENTO DELLE VARIE LISTE

adminlist_path = "adminlist_hub.json"
call_mensili_list_path = "call_mensili_list.json"
avvisi_on_list_path = "avvisi_on_list.json"
progetti_list_path = "progetti_list.json"
progetti_mozita_list_path = "progetti_mozita_list.json"
collaboratori_hub_path = "collaboratori_hub.json"
all_users_path = "all_users.json"
adminlist = []
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

# array mesi
listaMesi = [
    "Gennaio",
    "Febbraio",
    "Marzo",
    "Aprile",
    "Maggio",
    "Giugno",
    "Luglio",
    "Agosto",
    "Settembre",
    "Ottobre",
    "Novembre",
    "Dicembre"]


# questa funzione serve per calcolare il primo venerdì del mese

def first_friday_of_the_month(year, month):
    for day, weekday in calendar.Calendar().itermonthdays2(year, month):
        if weekday == 4:
            if(day != 0):
                return day
            else:
                return day + 7

# il "main"

def risposte(msg):
    localtime = datetime.now()
    data_salvataggio = localtime.strftime("%Y_%m_%d")
    localtime = localtime.strftime("%d/%m/%y %H:%M:%S")
    type_msg = "NM"  # Normal Message
    status_user = "-"  # inizializzazione dello 'status' dell'utente {"A"|"-"}
    # Admin, Other

    global frasi  # frasi è il dictionary globali che contiene tutte le frasi da visualizzare

    global response
    response = bot.getUpdates()
    # print(response)

    global adminlist

    if Path(adminlist_path).exists():
        adminlist = json.loads(open(adminlist_path).read())
    else:
        # nel caso in cui non dovesse esistere alcun file "adminlist.json" imposta staticamente l'userid di Sav22999
        # -> così da poter confermare anche altri utenti anche se ci sono 'malfunzionamenti' (NON DOVREBBERO ESSERCENE!)
        adminlist = [240188083]

    # caricamento degli eventi gestiti
    eventi_list = {}
    eventi_list = telegram_events.events(msg, ["LK", "NM"], response)
    text = eventi_list["text"]
    type_msg = eventi_list["type_msg"]
    # modificato=eventi_list["modificato"]
    # risposta=eventi_list["risposta"]

    link_regolamento = "https://github.com/MozillaItalia/mozitaantispam_bot/wiki/Regolamento"

    user_id = msg['from']['id']
    if user_id in adminlist:
        status_user = "A"
    nousername = False
    if "username" in msg['from']:
        user_name = msg['from']['username']
    else:
        user_name = "[*NessunUsername*]"
        nousername = True

    if "chat" not in msg:
        msg = msg["message"]
    chat_id = msg['chat']['id']

    if datetime.now().month == 12:
        anno_call = str(datetime.now().year + 1)
        mese_call = listaMesi[0]
        giorno_call = str(first_friday_of_the_month(int(anno_call), 1))
    else:
        anno_call = str(datetime.now().year)
        giorno_call = first_friday_of_the_month(
            int(anno_call), datetime.now().month)
        if datetime.now().day >= giorno_call:
            mese_call = datetime.now().month + 1
            giorno_call = str(first_friday_of_the_month(
                int(anno_call), datetime.now().month + 1))
        else:
            mese_call = datetime.now().month
            giorno_call = str(giorno_call)
        mese_call = listaMesi[mese_call - 1]
        # non è possibile utilizzare la funzione
        # datetime.now().(month+1).strftime("%B") perché lo restituisce in
        # inglese

    home = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=frasi["button_vai_a_home"],
                              url='https://t.me/joinchat/BCql3UMy26nl4qxuRecDsQ')],
        [InlineKeyboardButton(
            text=frasi["button_mostra_help"], callback_data='/help')],
    ])

    feedback = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=frasi["button_feedback"],
                              url='https://t.me/joinchat/BCql3UMy26nl4qxuRecDsQ')],
        [InlineKeyboardButton(text=frasi["button_feedback2"],
                              url='https://t.me/joinchat/BCql3UMy26nl4qxuRecDsQ')],
        [InlineKeyboardButton(
            text=frasi["button_mostra_help"], callback_data='/help')],
    ])

    start = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=frasi["button_start"],
                              callback_data='/help')],
        [InlineKeyboardButton(text=frasi["button_start2"],
                              callback_data='/supporto')],
    ])

    supporto = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=frasi["button_support"], url='https://t.me/joinchat/BCql3UMy26nl4qxuRecDsQ'),
         InlineKeyboardButton(text=frasi["button_support2"], callback_data='/forum')],
        [InlineKeyboardButton(text=frasi["button_support3"],
                              url='https://forum.mozillaitalia.org/index.php?board=9.0')],
        [InlineKeyboardButton(
            text=frasi["button_mostra_help"], callback_data='/help')],
    ])

    help = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=frasi["button_testo_gruppi"], callback_data='/gruppi'),
         InlineKeyboardButton(text=frasi["button_testo_supporto"], callback_data='/supporto'),
         InlineKeyboardButton(text=frasi["button_testo_avvisi"], callback_data='/avvisi')],
        [InlineKeyboardButton(text=frasi["button_testo_call"], callback_data='/meeting'),
         InlineKeyboardButton(text=frasi["button_testo_progetti_attivi"], callback_data='/progetti'),
         InlineKeyboardButton(text=frasi["button_testo_vademecum"], callback_data='/vademecum')],
        [InlineKeyboardButton(text=frasi["button_testo_regolamento"], callback_data='/regolamento'),
         InlineKeyboardButton(text=frasi["button_testo_info"], callback_data='/info')],
        [InlineKeyboardButton(text=frasi["button_feedback"],callback_data='/feedback')],
    ])

    gruppi = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=frasi["button_testo_home"], url='https://t.me/joinchat/BCql3UMy26nl4qxuRecDsQ'),
         InlineKeyboardButton(text=frasi["button_testo_news"], url='https://t.me/mozItaNews')],
        [InlineKeyboardButton(text=frasi["button_testo_vog_div_volontario"],
                              url='https://t.me/joinchat/B1cgtEQAHkGVBTbI0XPd-A')],
        [InlineKeyboardButton(text=frasi["button_testo_developer"], url='https://t.me/joinchat/B1cgtENXHcxd3jzFar7Kuw'),
         InlineKeyboardButton(text=frasi["button_testo_l10n"], url='https://t.me/joinchat/BCql3UMy26nl4qxuRecDsQ')],
        [InlineKeyboardButton(text=frasi["button_testo_design"], url='https://t.me/joinchat/B1cgtA7DF3qDzuRvsEtT6g'),
         InlineKeyboardButton(text=frasi["button_testo_iot"], url='https://t.me/joinchat/B1cgtEzLzr0gvSJcEicq1g')],
        [InlineKeyboardButton(
            text=frasi["button_mostra_help"], callback_data='/help')],
    ])

    developer = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=frasi["button_developer"],
                              url='https://t.me/joinchat/B1cgtENXHcxd3jzFar7Kuw')],
        [InlineKeyboardButton(
            text=frasi["button_mostra_help"], callback_data='/help')],
    ])

    design = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=frasi["button_design"],
                              url='https://t.me/joinchat/B1cgtA7DF3qDzuRvsEtT6g')],
        [InlineKeyboardButton(
            text=frasi["button_mostra_help"], callback_data='/help')],
    ])

    iot = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=frasi["button_iot"], url='https://t.me/joinchat/B1cgtEzLzr0gvSJcEicq1g')],
        [InlineKeyboardButton(
            text=frasi["button_mostra_help"], callback_data='/help')],
    ])

    vademecum = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=frasi["button_vg"], callback_data='/vademecumGenerale'),
         InlineKeyboardButton(text=frasi["button_vt"], callback_data='/vademecumTecnico')],
        [InlineKeyboardButton(
            text=frasi["button_mostra_help"], callback_data='/help')],
    ])

    collabora = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=frasi["button_collabora"],
                    url='https://t.me/joinchat/BCql3UMy26nl4qxuRecDsQ'),
                InlineKeyboardButton(
                    text=frasi["button_collabora2"],
                    url='https://t.me/joinchat/B1cgtEQAHkGVBTbI0XPd-A')],
            [
                InlineKeyboardButton(
                    text=frasi["button_mostra_help"],
                    callback_data='/help')],
        ])

    news = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=frasi["button_news"],
                              url='https://t.me/mozItaNews')],
        [InlineKeyboardButton(
            text=frasi["button_mostra_help"], callback_data='/help')],
    ])

    forum = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=frasi["button_forum"],
                              url='https://forum.mozillaitalia.org/')],
        [InlineKeyboardButton(
            text=frasi["button_mostra_help"], callback_data='/help')],
    ])

    call = InlineKeyboardMarkup(inline_keyboard=[
        # [InlineKeyboardButton(text=frasi["button_call"],
                              # callback_data='/listacall')],
        [InlineKeyboardButton(text=frasi["button_vai_a_canale_youtube"],
                              url='https://www.youtube.com/channel/UCsTquqVS0AJxCf4D3n9hQ1w')],
        [InlineKeyboardButton(text=frasi["button_call2"],
                              callback_data='/prossimoMeeting')],
        [InlineKeyboardButton(
            text=frasi["button_mostra_help"], callback_data='/help')],
    ])

    load_progetti = []
    for value_for in progetti_list:
        load_progetti.append([InlineKeyboardButton(
            text=str(value_for), url=str(progetti_list[value_for]))])
    load_progetti.append([InlineKeyboardButton(
        text=frasi["button_mostra_help"], callback_data='/help')])

    progetti = InlineKeyboardMarkup(inline_keyboard=load_progetti)

    load_progettimozita = []
    for value_for in progetti_mozita_list:
        load_progettimozita.append([InlineKeyboardButton(
            text=str(value_for), url=str(progetti_mozita_list[value_for]))])
    load_progettimozita.append([InlineKeyboardButton(
        text=frasi["button_mostra_help"], callback_data='/help')])

    progettimozita = InlineKeyboardMarkup(inline_keyboard=load_progettimozita)

    regolamento = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=frasi["button_regolamento"],
                              url=link_regolamento)],
        [InlineKeyboardButton(
            text=frasi["button_mostra_help"], callback_data='/help')],
    ])

    avvisi = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=frasi["button_avvisi"], callback_data="/avvisiOn"),
         InlineKeyboardButton(text=frasi["button_avvisi2"], callback_data="/avvisiOff")],
        [InlineKeyboardButton(
            text=frasi["button_mostra_help"], callback_data='/help')],
    ])

    '''
    mostra_menu_principale = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=frasi["button_mostra_help"], callback_data='/help')],
    ])
    '''

    '''
    nome_nome = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Testo bottone (riga 1, col 1)', callback_data='/comando'),
                    InlineKeyboardButton(text='Testo bottone 2 (riga 1, col 2)', callback_data='/comando2')],
                    [InlineKeyboardButton(text='Testo bottone 3 (riga 2, col 1-2)', url='https://t.me/')],
                ])
    '''

    admin = False
    collaboratori_stampa = ""
    for value_for in sorted(collaboratori_hub):
        collaboratori_stampa += "\n - " + value_for

    if chat_id not in all_users:
        all_users.append(chat_id)
        avvisi_on_list.append(user_id)
        try:
            with open(all_users_path, "wb") as file_with:
                file_with.write(json.dumps(all_users).encode("utf-8"))
        except Exception as exception_value:
            print("Excep:03 -> " + str(exception_value))
        try:
            with open(avvisi_on_list_path, "wb") as file_with:
                file_with.write(json.dumps(avvisi_on_list).encode("utf-8"))
        except Exception as exception_value:
            print("Excep:04 -> " + str(exception_value))

    if user_id in avvisi_on_list:
        stato_avvisi = frasi["avvisiStatoOn"]
    else:
        stato_avvisi = frasi["avvisiStatoOff"]

    if text.lower() == "/home":
        bot.sendMessage(chat_id, frasi["home"],
                        reply_markup=home, parse_mode="HTML")
    elif text.lower() == "/start":
        bot.sendMessage(chat_id, frasi["start"], parse_mode="HTML")
        bot.sendMessage(chat_id, frasi["start2"],
                        reply_markup=start, parse_mode="HTML")
        if nousername:
            bot.sendMessage(
                chat_id, frasi["start_nousername"], parse_mode="HTML")
    elif text.lower() == "/supporto":
        bot.sendMessage(chat_id, frasi["supporto"],
                        reply_markup=supporto, parse_mode="HTML")
    elif text.lower() == "/gruppi":
        bot.sendMessage(chat_id, frasi["gruppi"],
                        reply_markup=gruppi, parse_mode="HTML")
    elif text.lower() == "/collabora":
        bot.sendMessage(chat_id, frasi["collabora"], parse_mode="HTML")
        bot.sendMessage(chat_id, frasi["collabora2"],
                        reply_markup=collabora, parse_mode="HTML")
    elif text.lower() == "/vademecum":
        bot.sendMessage(chat_id, frasi["vademecum"],
                        reply_markup=vademecum, parse_mode="HTML")
    elif text.lower() == "/vademecumGenerale".lower():
        bot.sendMessage(chat_id, frasi["invio_vg_in_corso"], parse_mode="HTML")
        bot.sendDocument(chat_id, open("VG.pdf", "rb"))
    elif text.lower() == "/vademecumTecnico".lower():
        bot.sendMessage(chat_id, frasi["invio_vt_in_corso"], parse_mode="HTML")
        bot.sendDocument(chat_id, open("VT.pdf", "rb"))
    elif text.lower() == "/feedback":
        bot.sendMessage(chat_id, frasi["feedback"],
                        reply_markup=feedback, parse_mode="HTML")
    elif text.lower() == "/help" or text == "/aiuto":
        bot.sendMessage(chat_id, frasi["help"], parse_mode="HTML")
        bot.sendMessage(chat_id, frasi["help2"],
                        reply_markup=help, parse_mode="HTML")
    elif text.lower() == "/news":
        bot.sendMessage(chat_id, frasi["news"],
                        reply_markup=news, parse_mode="HTML")
    elif text.lower() == "/info":
        bot.sendMessage(
            chat_id,
            str(
                ((frasi["info"]).replace(
                    "{{**versione**}}",
                    str(versione))).replace(
                    "{{**ultimo_aggiornamento**}}",
                    str(ultimo_aggiornamento))).replace(
                "{{**collaboratori_stampa**}}",
                str(collaboratori_stampa)),
            parse_mode="HTML")
    elif text.lower() == "/forum":
        bot.sendMessage(chat_id, frasi["forum"],
                        reply_markup=forum, parse_mode="HTML")
    elif text.lower() == "/developer":
        bot.sendMessage(chat_id, frasi["developer"],
                        reply_markup=developer, parse_mode="HTML")
    elif text.lower() == "/design":
        bot.sendMessage(chat_id, frasi["design"],
                        reply_markup=design, parse_mode="HTML")
    elif text.lower() == "/iot":
        bot.sendMessage(chat_id, frasi["iot"],
                        reply_markup=iot, parse_mode="HTML")
    elif text.lower() == "/call" or text.lower() == "/meeting":
        bot.sendMessage(chat_id, frasi["call"],
                        reply_markup=call, parse_mode="HTML")
    elif text.lower() == "/prossimacall" or text.lower() == "/prossimoMeeting".lower():
        bot.sendMessage(
            chat_id,
            str(
                ((frasi["prossima_call"]).replace(
                    "{{**giorno_call**}}",
                    str(giorno_call))).replace(
                    "{{**mese_call**}}",
                    str(mese_call))).replace(
                "{{**anno_call**}}",
                str(anno_call)),
            parse_mode="HTML")
    elif text.lower() == "/progetti":
        bot.sendMessage(chat_id, frasi["progetti"],
                        reply_markup=progetti, parse_mode="HTML")
        bot.sendMessage(
            chat_id,
            frasi["progetti2"],
            reply_markup=progettimozita,
            parse_mode="HTML")
    elif text.lower() == "/regolamento":
        bot.sendMessage(chat_id, frasi["regolamento"],
                        reply_markup=regolamento, parse_mode="HTML")
    elif text.lower() == "/avvisi":
        bot.sendMessage(chat_id, str(frasi["avvisi"]).replace(
            "{{**stato_avvisi**}}", str(stato_avvisi)), reply_markup=avvisi, parse_mode="HTML")
    elif text.lower() == "/avvisiOn".lower():
        if not (user_id in avvisi_on_list):
            avvisi_on_list.append(user_id)
            try:
                with open(avvisi_on_list_path, "wb") as file_with:
                    file_with.write(json.dumps(avvisi_on_list).encode("utf-8"))
                bot.sendMessage(chat_id, frasi["avvisiOn"], parse_mode="HTML")
            except Exception as exception_value:
                print("Excep:05 -> " + str(exception_value))
                bot.sendMessage(chat_id, frasi["avvisiOn2"], parse_mode="HTML")
        else:
            bot.sendMessage(chat_id, frasi["avvisiOn3"], parse_mode="HTML")
    elif text.lower() == "/avvisiOff".lower():
        if user_id in avvisi_on_list:
            avvisi_on_list.remove(user_id)
            try:
                with open(avvisi_on_list_path, "wb") as file_with:
                    file_with.write(json.dumps(avvisi_on_list).encode("utf-8"))
                bot.sendMessage(chat_id, frasi["avvisiOff"], parse_mode="HTML")
            except Exception as exception_value:
                print("Excep:06 -> " + str(exception_value))
                bot.sendMessage(
                    chat_id, frasi["avvisiOff2"], parse_mode="HTML")
        else:
            bot.sendMessage(chat_id, frasi["avvisiOff3"])
    elif "/admin" in text.lower():
        if status_user == "A":
            if type_msg == "LK":
                admin = True
        else:
            bot.sendMessage(chat_id, frasi["non_sei_admin"], parse_mode="HTML")
    else:
        bot.sendMessage(
            chat_id,
            frasi["comando_non_riconosciuto"],
            reply_markup=start,
            parse_mode="HTML")

    if admin:
        # CONTROLLO AZIONI ADMIN
        azione = list(text.split(" "))
        admin_err1 = False
        if azione[0].lower() == "/admin" and len(azione) >= 1:
            if len(azione) == 1 or (azione[1].lower() == "help" and len(azione) == 2):
                # Elenco azioni
                bot.sendMessage(chat_id,
                    "Questo è l'elenco dei comandi che puoi eseguire:\n" +
                    "\n\n" +
                    "<b>Generali</b>:\n"
                    "- <code>/admin avviso |Messaggio da inviare|</code>\n" +
                    "- <code>/admin preview |Messaggio da inviare|</code> <i>Anteprima del messaggio da inviare, per verificare che tutto venga visualizzato correttamente</i>\n" +
                    "- <code>/admin all users |Messaggio importante da inviare|</code> <i>Solo per messaggio importanti, altrimenti usare 'avviso'</i>\n" +
                    "\n" +
                    "<b>Gestione lista degli iscritti agli avvisi</b>\n" +
                    "- <code>/admin avvisi list mostra</code>\n" +
                    "- <code>/admin avvisi list aggiungi |Chat_id|</code>\n" +
                    "- <code>/admin avvisi list elimina |Chat_id|</code>\n" +
                    "\n" +
                    "<b>Gestione progetti (Mozilla)</b>:\n" +
                    "- <code>/admin progetto aggiungi |Nome progetto da aggiungere| |LinkProgetto|</code>\n" +
                    "- <code>/admin progetto modifica |Nome progetto da modificare| |LinkProgettoModificato|</code>\n" +
                    "- <code>/admin progetto elimina |Nome progetto da eliminare|</code>\n" +
                    "\n" +
                    "<b>Gestione progetti Mozilla Italia</b>:\n" +
                    "- <code>/admin progetto mozita aggiungi |Nome progetto comunitario da aggiungere| |LinkProgetto|</code>\n" +
                    "- <code>/admin progetto mozita modifica |Nome progetto comunitario da modificare| |LinkProgettoModificato|</code>\n" +
                    "- <code>/admin progetto mozita elimina |Nome progetto comunitario da eliminare|</code>\n" +
                    "\n" +
                    "<b>Gestione collaboratori di MozItaBot</b>:\n" +
                    "- <code>/admin collaboratore aggiungi |Nome Cognome (@usernameTelegram)|</code>\n" +
                    "- <code>/admin collaboratore elimina |Nome Cognome (@usernameTelegram)|</code>\n" +
                    "\n" +
                    "<b>Scaricare file log di MozItaBot</b>:\n" +
                    "- <code>/admin scarica |ANNO| |MESE| |GIORNO|</code>\n" +
                    "\n" +
                    "<b>Esempi:</b>\n" +
                    "- <code>/admin avviso Messaggio di prova</code>\n" +
                    "- <code>/admin call aggiungi Nome call di esempio 2019 https://mozillaitalia.it</code>\n" +
                    "- <code>/admin scarica 2019 10 09</code>",
                    parse_mode="HTML")
            elif azione[1].lower() == "avviso" and len(azione) >= 3:
                # Azioni sugli avvisi
                del azione[0]
                del azione[0]
                messaggio = ' '.join(azione)
                error08 = False
                for value_for in avvisi_on_list:
                    try:
                        bot.sendMessage(
                            value_for,
                            messaggio +
                            "\n\n--------------------\n" +
                                frasi["footer_messaggio_avviso"],
                                parse_mode="HTML")
                        bot.sendMessage(
                            chat_id,
                                "✔️ Messaggio inviato alla chat: <a href='tg://user?id=" + str(value_for) + "'>" +
                                str(value_for) + "</a>",
                                parse_mode="HTML")
                    except Exception as exception_value:
                        print("Excep:08 -> " + str(exception_value))
                        if (str(exception_value) == "('Bad Request: chat not found', 400, {'ok': False, 'error_code': 400, 'description': 'Bad Request: chat not found'})"):
                            bot.sendMessage(
                                chat_id,
                                    "‼️❌ Chat non trovata: <a href='tg://user?id=" +
                                    str(value_for) + "'>" + str(value_for) + "</a>",
                                    parse_mode="HTML")
                        else:
                            bot.sendMessage(
                                chat_id,
                                    "❌ Non è stato possibile inviare il messaggio alla chat: <a href='tg://user?id=" +
                                    str(value_for) + "'>" + str(value_for) + "</a>",
                                    parse_mode="HTML")
                        error08 = True
                if(not error08):
                    bot.sendMessage(
                        chat_id,
                            "Messaggio inviato correttamente a tutti gli utenti iscritti alle news.\n\nIl messaggio inviato è:\n" +
                            messaggio,
                            parse_mode="HTML")
                else:
                    bot.sendMessage(
                        chat_id,
                            "Messaggio inviato correttamente ad alcune chat.\n\nIl messaggio inviato è:\n" +
                            messaggio,
                            parse_mode="HTML")

            elif azione[1].lower() == "preview" and len(azione) >= 3:
                del azione[0]
                del azione[0]
                messaggio = ' '.join(azione)
                try:
                    bot.sendMessage(
                            chat_id,
                                "<b>‼️‼️ ||PREVIEW DEL MESSAGGIO||</b>‼️‼️\n\n"+
                                messaggio +
                                "\n\n--------------------\n" + frasi["footer_messaggio_avviso"],
                                parse_mode="HTML")
                except Exception as exception_value:
                        print("Excep:23 -> " + str(exception_value))
                        bot.sendMessage(
                            chat_id,
                                "‼️ <b>ERRORE</b>: il messaggio contiene degli errori di sintassi.\n"+
                                "Verificare di avere <b>chiuso</b> tutti i tag usati.",
                            parse_mode="HTML")

            elif azione[1].lower() == "all" and azione[2].lower() == "users" and len(azione) >= 4:
                # Azioni sugli avvisi importanti (tutti gli utenti)
                del azione[0]
                del azione[0]
                del azione[0]
                messaggio = ' '.join(azione)
                for value_for in all_users:
                    try:
                        bot.sendMessage(
                            value_for,
                            "<b>Messaggio importante</b>\n" + messaggio,
                            parse_mode="HTML")
                        bot.sendMessage(
                            chat_id, "✔️ Messaggio inviato alla chat: <a href='tg://user?id=" + str(value_for) + "'>" +
                                str(value_for) + "</a>",
                                parse_mode="HTML")
                    except Exception as exception_value:
                        print("Excep:07 -> " + str(exception_value))
                        if (str(exception_value) == "('Bad Request: chat not found', 400, {'ok': False, 'error_code': 400, 'description': 'Bad Request: chat not found'})"):
                            bot.sendMessage(
                                chat_id,
                                    "‼️❌ Chat non trovata: <a href='tg://user?id=" +
                                    str(value_for) + "'>" + str(value_for) + "</a>",
                                    parse_mode="HTML")
                        else:
                            bot.sendMessage(
                                chat_id,
                                    "❌ Non è stato possibile inviare il messaggio alla chat: <a href='tg://user?id=" +
                                    str(value_for) + "'>" + str(value_for) + "</a>",
                                    parse_mode="HTML")
                bot.sendMessage(
                    chat_id,
                        "Messaggio inviato correttamente a tutti gli utenti.\n\nIl messaggio inviato è:\n" +
                        messaggio,
                        parse_mode="HTML")
            elif azione[1].lower() == "avvisi" and azione[2].lower() == "list" and len(azione) >= 4:
                # Azioni sugli utenti (chat_id) presenti in avvisi_on_list.json
                if azione[3] == "mostra":
                    bot.sendMessage(chat_id,"Ecco la 'avvisi_on_list':\n\n"+str(avvisi_on_list))
                elif azione[3] == "aggiungi":
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    temp_chat_id = int(azione[0])
                    if temp_chat_id not in avvisi_on_list:
                        avvisi_on_list.append(temp_chat_id)
                        try:
                            with open(avvisi_on_list_path, "wb") as file_with:
                                file_with.write(json.dumps(
                                    avvisi_on_list).encode("utf-8"))
                            bot.sendMessage(
                                chat_id,
                                "La chat_id '" +
                                str(temp_chat_id) +
                                "' è stata inserita correttamente.")
                        except Exception as exception_value:
                            print("Excep:12 -> " + str(exception_value))
                            bot.sendMessage(
                                chat_id,
                                "Si è verificato un errore inaspettato e non è possibile salvare 'avvisi_on_list.json'.")
                    else:
                        bot.sendMessage(
                            chat_id,
                            "La chat_id '" +
                            str(temp_chat_id) +
                            "' è già presente.")
                elif azione[3].lower() == "elimina":
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    temp_chat_id = int(azione[0])
                    if temp_chat_id in avvisi_on_list:
                        avvisi_on_list.remove(temp_chat_id)
                        try:
                            with open(avvisi_on_list_path, "wb") as file_with:
                                file_with.write(json.dumps(
                                    avvisi_on_list).encode("utf-8"))
                            bot.sendMessage(
                                chat_id,
                                "La chat_id '" +
                                str(temp_chat_id) +
                                "' è stata eliminata correttamente.")
                        except Exception as exception_value:
                            print("Excep:13 -> " + str(exception_value))
                            bot.sendMessage(
                                chat_id,
                                "Si è verificato un errore inaspettato e non è possibile salvare 'avvisi_on_list.json'.")
                    else:
                        bot.sendMessage(
                            chat_id,
                            "La chat_id '" +
                            str(temp_chat_id) +
                            "' non è stata trovata.")
                else:
                    admin_err1 = True
            elif azione[1].lower() == "progetto" and azione[2].lower() == "mozita" and len(azione) >= 5:
                # Azioni sui progetti comunitari (mozilla italia)
                if azione[3].lower() == "aggiungi":
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
                            with open(progetti_mozita_list_path, "wb") as file_with:
                                file_with.write(json.dumps(
                                    progetti_mozita_list).encode("utf-8"))
                            bot.sendMessage(
                                chat_id,
                                "Progetto comunitario '" +
                                str(nome) +
                                "' (" +
                                str(link) +
                                ") inserito correttamente.")
                        except Exception as exception_value:
                            print("Excep:17 -> " + str(exception_value))
                            bot.sendMessage(
                                chat_id,
                                "Si è verificato un errore inaspettato e non è possibile salvare 'progetti_mozita_list.json'.")
                    else:
                        bot.sendMessage(chat_id, "Il progetto comunitario '" +
                                        str(nome) + "' è già presente.")
                elif azione[3].lower() == "modifica":
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
                            with open(progetti_mozita_list_path, "wb") as file_with:
                                file_with.write(json.dumps(
                                    progetti_mozita_list).encode("utf-8"))
                            bot.sendMessage(
                                chat_id,
                                "Progetto '" +
                                str(nome) +
                                "' (" +
                                str(link) +
                                ") modificato correttamente.")
                        except Exception as exception_value:
                            print("Excep:18 -> " + str(exception_value))
                            bot.sendMessage(
                                chat_id,
                                "Si è verificato un errore inaspettato e non è possibile salvare 'progetti_mozita_list.json'.")
                    else:
                        bot.sendMessage(chat_id, "Il progetto comunitario '" +
                                        str(nome) + "' non è stato trovato.")
                elif azione[3].lower() == "elimina":
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    nome = ' '.join(azione)
                    if nome in progetti_mozita_list:
                        del progetti_mozita_list[str(nome)]
                        try:
                            with open(progetti_mozita_list_path, "wb") as file_with:
                                file_with.write(json.dumps(
                                    progetti_mozita_list).encode("utf-8"))
                            bot.sendMessage(
                                chat_id, "Progetto comunitario '" + str(nome) + "' eliminato correttamente.")
                        except Exception as exception_value:
                            print("Excep:19 -> " + str(exception_value))
                            bot.sendMessage(
                                chat_id,
                                "Si è verificato un errore inaspettato e non è possibile salvare 'progetti_mozita_list.json'.")
                    else:
                        bot.sendMessage(chat_id, "Il progetto '" +
                                        str(nome) + "' non è stato trovato.")
                else:
                    admin_err1 = True
            elif azione[1].lower() == "progetto" and len(azione) >= 4:
                # Azione sui progetti (mozilla)
                if azione[2] == "aggiungi":
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    link = azione[-1]
                    del azione[-1]
                    nome = ' '.join(azione)
                    if not (nome in progetti_list):
                        progetti_list[str(nome)] = str(link)
                        try:
                            with open(progetti_list_path, "wb") as file_with:
                                file_with.write(json.dumps(
                                    progetti_list).encode("utf-8"))
                            bot.sendMessage(
                                chat_id,
                                "Progetto '" +
                                str(nome) +
                                "' (" +
                                str(link) +
                                ") inserito correttamente.")
                        except Exception as exception_value:
                            print("Excep:17 -> " + str(exception_value))
                            bot.sendMessage(
                                chat_id,
                                "Si è verificato un errore inaspettato e non è possibile salvare 'progetti_list.json'.")
                    else:
                        bot.sendMessage(chat_id, "Il progetto '" +
                                        str(nome) + "' è già presente.")
                elif azione[2].lower() == "modifica":
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    link = azione[-1]
                    del azione[-1]
                    nome = ' '.join(azione)
                    if nome in progetti_list:
                        progetti_list[str(nome)] = str(link)
                        try:
                            with open(progetti_list_path, "wb") as file_with:
                                file_with.write(json.dumps(
                                    progetti_list).encode("utf-8"))
                            bot.sendMessage(
                                chat_id,
                                "Progetto '" +
                                str(nome) +
                                "' (" +
                                str(link) +
                                ") modificato correttamente.")
                        except Exception as exception_value:
                            print("Excep:18 -> " + str(exception_value))
                            bot.sendMessage(
                                chat_id,
                                "Si è verificato un errore inaspettato e non è possibile salvare 'progetti_list.json'.")
                    else:
                        bot.sendMessage(chat_id, "Il progetto '" +
                                        str(nome) + "' non è stato trovato.")
                elif azione[2].lower() == "elimina":
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    nome = ' '.join(azione)
                    if nome in progetti_list:
                        del progetti_list[str(nome)]
                        try:
                            with open(progetti_list_path, "wb") as file_with:
                                file_with.write(json.dumps(
                                    progetti_list).encode("utf-8"))
                            bot.sendMessage(
                                chat_id, "Progetto '" + str(nome) + "' eliminato correttamente.")
                        except Exception as exception_value:
                            print("Excep:19 -> " + str(exception_value))
                            bot.sendMessage(
                                chat_id,
                                "Si è verificato un errore inaspettato e non è possibile salvare 'progetti_list.json'.")
                    else:
                        bot.sendMessage(chat_id, "Il progetto '" +
                                        str(nome) + "' non è stato trovato.")
                else:
                    admin_err1 = True
            elif azione[1].lower() == "collaboratore" and len(azione) >= 4:
                # Azione sui collaboratori
                if azione[2] == "aggiungi":
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    nome = ' '.join(azione)
                    if nome not in collaboratori_hub:
                        collaboratori_hub.append(str(nome))
                        try:
                            with open(collaboratori_hub_path, "wb") as file_with:
                                file_with.write(json.dumps(
                                    sorted(collaboratori_hub)).encode("utf-8"))
                            bot.sendMessage(
                                chat_id, "'" + str(nome) + "' aggiunto correttamente ai collaboratori.")
                        except Exception as exception_value:
                            print("Excep:20 -> " + str(exception_value))
                            bot.sendMessage(
                                chat_id,
                                "Si è verificato un errore inaspettato e non è possibile salvare 'collaboratori_hub.json'.")
                    else:
                        bot.sendMessage(
                            chat_id,
                            "'" +
                            str(nome) +
                            "' è già presente nella lista dei collaboratori.")
                elif azione[2].lower() == "elimina":
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    nome = ' '.join(azione)
                    if nome in collaboratori_hub:
                        collaboratori_hub.remove(str(nome))
                        try:
                            with open(collaboratori_hub_path, "wb") as file_with:
                                file_with.write(json.dumps(
                                    collaboratori_hub).encode("utf-8"))
                            bot.sendMessage(
                                chat_id, "'" + str(nome) + "' rimosso correttamente dai collaboratori.")
                        except Exception as exception_value:
                            print("Excep:21 -> " + str(exception_value))
                            bot.sendMessage(
                                chat_id,
                                "Si è verificato un errore inaspettato e non è possibile salvare 'collaboratori_hub.json'.")
                    else:
                        bot.sendMessage(
                            chat_id,
                            "'" +
                            str(nome) +
                            "' non è presente nella lista dei collaboratori.")
                else:
                    admin_err1 = True
            elif azione[1].lower() == "scarica" and len(azione) == 5:
                # Azione per scaricare file di log -> esempio: /admin scarica 2019 10 20
                nome_file = "log_"+azione[2]+"_"+azione[3]+"_"+azione[4]+".txt"
                if os.path.exists("./history_mozitabot/"+nome_file):
                    bot.sendMessage(chat_id, "<i>Invio del file "+nome_file+" in corso</i>", parse_mode="HTML")
                    bot.sendDocument(chat_id, open("./history_mozitabot/"+nome_file, "rb"))
                else:
                    bot.sendMessage(chat_id, "Il file <i>" + nome_file + "</i> non esiste.", parse_mode="HTML")
            else:
                admin_err1 = True
        else:
            bot.sendMessage(
                chat_id,
                "Errore: Comando non riconosciuto.\nPer scoprire tutti i comandi consentiti in questa sezione digita /admin", parse_mode="HTML")

        if admin_err1:
            bot.sendMessage(
                chat_id,
                "Questo comando nella sezione ADMIN non è stato riconosciuto.\n\nPer scoprire tutti i comandi consentiti in questa sezione digita /admin", parse_mode="HTML")

    try:
        # stringa stampata a terminale, per ogni operazione effettuata
        stampa = str(localtime) + "  --  Utente: " + str(user_name) + " (" + str(user_id) + ")[" + str(status_user) + "]  --  Chat: " + str(
            chat_id) + "\n >> >> Tipo messaggio: " + str(type_msg) + "\n >> >> Contenuto messaggio: " + str(text) + "\n--------------------\n"
        print(stampa)
    except Exception as exception_value:
        stampa = "Excep:01 -> " + str(exception_value) + "\n--------------------\n"
        print(stampa)

    try:
        # verifica l'esistenza del filela cartella "history_mozitabot", altrimenti la crea
        if os.path.exists("./history_mozitabot") == False:
            os.mkdir("./history_mozitabot")
    except Exception as exception_value:
        print("Excep:22 -> " + str(exception_value))

    try:
        # apre il file in scrittura "append" per inserire orario e data -> log
        # di utilizzo del bot (ANONIMO)
        file = open("./history_mozitabot/log_" +
                    str(data_salvataggio) + ".txt", "a", -1, "UTF-8")
        # ricordare che l'orario è in fuso orario UTC pari a 0 (Greenwich,
        # Londra) - mentre l'Italia è a +1 (CET) o +2 (CEST - estate)
        file.write(stampa)
        file.close()
    except Exception as exception_value:
        print("Excep:02 -> " + str(exception_value))


try:
    bot = telepot.Bot(TOKEN)
    MessageLoop(
        bot, {'chat': risposte, 'callback_query': risposte}).run_as_thread()
except Exception as exception_value:
    print("ERRORE GENERALE.\n\nError: " + str(exception_value) + "\n--------------------\n")

while True:
    time.sleep(10)
