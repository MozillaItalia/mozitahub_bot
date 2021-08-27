#!/usr/bin/python3
import os
import json
import time
import datetime
import calendar
import telepot
import threading
import telegram_events
import tweepy as ty
from pathlib import Path
from datetime import datetime, timedelta
from configparser import ConfigParser
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

# must be defined at the beginning: while refactoring variable initialization must be
# in another function
def log(stampa, err):
    '''
    log: log function
    '''
    global response, data_salvataggio
    if err:
        stampa = str(response) + "\n\n" + str(stampa)
    stampa = stampa + "\n--------------------\n"
    try:
        # verifica l'esistenza del filela cartella "history_mozitabot", altrimenti la crea
        if os.path.exists("./history_mozitabot") == False:
            os.mkdir("./history_mozitabot")
    except Exception as exception_value:
        print("Excep:22 -> " + str(exception_value))
        log("Except:22 ->" + str(exception_value), True)

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
        log("Except:02 ->" + str(exception_value), True)

def load_list_from_path(generic_path):
    return json.loads(open(generic_path).read()) if Path(generic_path).exists() else []

def load_dict_from_path(generic_path):
    return json.loads(open(generic_path).read()) if Path(generic_path).exists() else {}

def fix_username(username):
    # add @ character if not provided
    if username[0] != "@":
        username = "@" + username
    return username

def safe_conf_get(config_parser, section, key_name):
    '''
    returns parsed value if key_name exists in config.ini, null otherwise
    '''
    try:
        return config_parser.get(section, key_name)
    except Exception:
        print(key_name + " non presente nella sezione " + section + "!")
        exit()

######################
#  LOADING SECRETS   #
######################
# managing config.ini
if not os.path.isfile("config.ini"):
    print(
        "Il file di configurazione non è presente.\n" +
        "Rinomina il file 'config-sample.ini' in 'config.ini' e inserisci i dati mancanti.")
    exit()

# useful object to manage secret values
script_path = os.path.dirname(os.path.realpath(__file__))
config_parser = ConfigParser()
config_parser.read(os.path.join(script_path, "config.ini"))
localtime = datetime.now()
data_salvataggio = localtime.strftime("%Y_%m_%d")
    
###########################
#  MANAGING BOT CONSTANTS #
###########################
TOKEN = safe_conf_get(config_parser, "bot", "TOKEN")
NEWS_CHANNEL = safe_conf_get(config_parser, "bot", "NEWS_CHANNEL")
GRUPPI_URL = {
    "home": "https://t.me/joinchat/BCql3UMy26nl4qxuRecDsQ",
    "news": "https://t.me/mozItaNews",
    "developers": "https://t.me/joinchat/gR1vRg16B9swNTU0",
    "l10n": "https://t.me/mozItaL10n",
    "design_marketing": "https://t.me/joinchat/2fJyoMoOKa1kNjM0"
}

# managing version and last update
versione = "1.6.3.1"
ultimo_aggiornamento = "27-08-2021"

print("(MozItaBot) Versione: " + versione +
      " - Aggiornamento: " + ultimo_aggiornamento)

# loading sentences from file
if Path("frasi.json").exists():
    frasi = json.loads(open("frasi.json", encoding="utf8").read())
else:
    print("File frasi non presente.")
    exit()

# setting lists --- almost everything is merged into one single file, to avoid confusion
lists_path = "liste.json"
liste = load_dict_from_path(lists_path)

all_users_path = "all_users.json"
avvisi_on_list_path = "avvisi_on_list.json"
adminlist = []

avvisi_on_list = load_list_from_path(avvisi_on_list_path)
all_users = load_list_from_path(all_users_path)

#######################
# TWITTER INTEGRATION #
#######################
# start time from OS
starttime=time.time()

def updateJSON(data, path):
    jsonstr = json.dumps(data, sort_keys=True, indent=4)
    jsonfile = open(path, "w")
    jsonfile.write(jsonstr)
    jsonfile.close()

def get_last_id_posted():
    last_twitter_id_path = "last_twitter_id.json"

    # managing last post id
    last_post_id = load_list_from_path(last_twitter_id_path)
    
    if len(last_post_id) != 1:
        print("Errore. Non c'e' un id dell'ultimo post salvato da Twitter nel file last_twitter_id.json")
        print("Rinomina il file last_twitter_id-sample.json, inserisci l'id dell'ultimo post e riprova")
        exit()

    return last_post_id[0]


# init almost everything needed by Twitter
def twitter_init(config_parser, starttime):
    # managing twitter tokens
    CONSUMER_KEY = safe_conf_get(config_parser, "twitter", "CONSUMER_KEY")
    CONSUMER_SECRET = safe_conf_get(config_parser, "twitter", "CONSUMER_SECRET")
    ACCESS_TOKEN = safe_conf_get(config_parser, "twitter", "ACCESS_TOKEN")
    ACCESS_SECRET = safe_conf_get(config_parser, "twitter", "ACCESS_SECRET")
    TWITTER_REFRESH_TIME = float(safe_conf_get(config_parser, "twitter", "TWITTER_REFRESH_TIME"))
    TWITTER_SOURCE_ACCOUNT = safe_conf_get(config_parser, "twitter", "TWITTER_SOURCE_ACCOUNT")

    # authorizes the code
    auth = ty.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    twitter_api = ty.API(auth)

    # check if user exists
    try:
        twitter_api.get_user(TWITTER_SOURCE_ACCOUNT)
    except Exception:
        print("Nome utente Twitter non valido! Assicurati di aver inserito il nome utente giusto e riprova!")
        log("Nome utente Twitter non valido! Assicurati di aver inserito il nome utente giusto e riprova!", True)
        exit()

    # tuple: it contains Twitter username and lastpostid
    user_params = [TWITTER_SOURCE_ACCOUNT,get_last_id_posted()]

    threading.Thread(target=fetch_twitter, args=(twitter_api, starttime, TWITTER_REFRESH_TIME, NEWS_CHANNEL, user_params)).start() 

# social function: updates twitter -- used by thread
def fetch_twitter(twitter_api, starttime, seconds=300.0, channel_username="@mozitanews", user_params=["MozillaItalia",'1']):
    channel_username = fix_username(channel_username)
    """ 
    function to fetch MozillaItalia's Tweets and post them on a channel
    """
    if channel_username not in channels_list:
        print("Errore! Il canale destinazione dove inoltrare i nuovi post di Twitter è errato, non esiste, non esiste nella channel_list.json o il bot non ha il permesso di scrivere! Assicurati di aver specificato l'username giusto in config.ini")
        exit()

    while True:
        user_params[1] = get_last_id_posted()

        get_user_tweet(twitter_api, channel_username, user_params)
        time.sleep(seconds - ((time.time() - starttime) % seconds))

# get tweets of a user and post it on a channel
def get_user_tweet(twitter_api, channel_name, user_params=["MozillaItalia",'1']):
    '''
    get tweets of a user and post it on a channel
    '''
    global tweet
    
    # get current date and time for time stamp and properly format it
    now = datetime.now()
    date_time = now.strftime("%d-%m-%Y %H:%M:%S")
    
    user = user_params[0]
    old_id = user_params[1]
    
    # fetch user timeline
    r = twitter_api.user_timeline(user, count=1, tweet_mode='extended')
    last_tweet_id = r[0].id
    status = twitter_api.get_status(last_tweet_id, tweet_mode="extended")
    
    # update last post id
    
    if last_tweet_id != old_id:
        # defining tweet text depending on the content
        try:
            tweet = "RT: " + status.retweeted_status.full_text
        except AttributeError:  # Not a Retweet
            tweet = status.full_text
        
        tweet_url = "https://twitter.com/" + user + "/status/" + str(status.id)

        # send message to mozitanews
        try:
            bot.sendMessage(channel_name,
                            tweet,
                            parse_mode="HTML",
                            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                [InlineKeyboardButton(
                                    text=frasi["view tweet"],
                                    url = tweet_url)]]))
            
            # updates last tweet file
            try:
                fd = open("last_twitter_id.json", "w")
                string =  "[" + str(r[0].id) + "]"
                fd.write(string)
            except Exception:
                print("Errore aggiornamento file!")
                exit()
            
            print("[" + date_time + "] " + "Tweet -> " + tweet)

        except Exception as exception_value:
            print("Excep:29 -> " + str(exception_value))
            log("Except:29 ->" + str(exception_value), True)
    else:
        print("[" + date_time + "] " + "Nessun nuovo Tweet. ")

# [TWITTER]: init everything and start
# twitter_init(config_parser, starttime)

##################################################################

response = ""

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


# calcola il primo venerdì del mese
def first_friday_of_the_month(year, month):
    for day, weekday in calendar.Calendar().itermonthdays2(year, month):
        if weekday == 4:
            if (day != 0):
                return day
            else:
                return day + 7


def remove_user_from_avvisi_allusers_lists(chat_id, userid_to_remove):
    '''
    bot.sendMessage(
        chat_id,
        "‼️❌ <a href='tg://user?id=" +
        str(userid_to_remove) + "'>" + str(userid_to_remove) + "</a> rimosso dalla lista.",
        parse_mode="HTML")
    '''
    try:
        if (userid_to_remove in avvisi_on_list):
            avvisi_on_list.remove(userid_to_remove)
            with open(avvisi_on_list_path, "wb") as file_with:
                file_with.write(json.dumps(
                    avvisi_on_list).encode("utf-8"))
        if (userid_to_remove in all_users):
            all_users.remove(userid_to_remove)
            with open(all_users_path, "wb") as file_with:
                file_with.write(json.dumps(
                    all_users).encode("utf-8"))
        testo_to_print = str(
            userid_to_remove) + " rimosso dalla lista all_users (ed eventualmente dalla avvisi_list)"
        print(testo_to_print)
        log(testo_to_print, False)
    except Exception as exception_value:
        print("Excep:24 -> " + str(exception_value))
        log("Except:24 ->" + str(exception_value), True)

# send a message in a channel
def send_message_channel(channel_name, messaggio, chat_id, optional_text = ""):
    
    try:
        bot.sendMessage(channel_name.lower(),
                        messaggio,
                        parse_mode="HTML")

        bot.sendMessage(
            chat_id,
            "Messaggio inviato correttamente sul canale <code>" + channel_name.lower() + "</code>" +
            ".\n\nIl messaggio inviato è:\n" +
            messaggio,
            parse_mode="HTML")
    except Exception as exception_value:
        print("Excep:25 -> " + str(exception_value))
        log("Except:25 ->" + str(exception_value), True)
        
        if optional_text != "":
            bot.sendMessage(
                chat_id,
                optional_text + "canale <code>" + channel_name.lower() + "</code>.\n",
                parse_mode="HTML"
            )
        else:
            bot.sendMessage(
                chat_id,
                "Si è verificato un errore per il canale <code>" + channel_name.lower() + "</code>.\n" +
                "Controlla che: \n" +
                "- il bot abbia i privilegi giusti\n" +
                "- BotFather sia settato correttamente\n" +
                "- hai aggiunto l'ID nella lista canali (con la @)\n\n" +
                "Se ancora hai problemi potrebbe trattarsi di un errore momentaneo.\n" +
                "Riprova più tardi!",
                parse_mode="HTML"
            )

        
def send_log(nome_file, chat_id):
    if os.path.exists("./history_mozitabot/" + nome_file):
        bot.sendMessage(chat_id, "<i>Invio del file " +
                        nome_file + " in corso</i>", parse_mode="HTML")
        bot.sendDocument(chat_id, open(
            "./history_mozitabot/" + nome_file, "rb"))
    else:
        bot.sendMessage(
            chat_id, "Il file <i>" + nome_file + "</i> non esiste.", parse_mode="HTML")

def risposte(msg):
    global data_salvataggio
    global localtime
    if isinstance(localtime, str):
        localtime = datetime.now()
    localtime = localtime.strftime("%d/%m/%y %H:%M:%S")
    type_msg = "NM"  # Normal Message
    status_user = "-"  # inizializzazione dello 'status' dell'utente {"A"|"-"}
    # Admin, Other

    global frasi  # frasi è il dictionary globali che contiene tutte le frasi da visualizzare
    global response
    global adminlist

    response = bot.getUpdates()

    if not liste["adminlist"] or not liste["adminlist"] == {}:
        adminlist = [ int(admin) for admin in list(liste["adminlist"].keys()) ]  # definita in liste.json
    else:
        # nel caso in cui non dovesse esistere alcuna lista admin imposta staticamente l'userid di Sav22999
        # -> così da poter confermare anche altri utenti anche se ci sono 'malfunzionamenti' (NON DOVREBBERO ESSERCENE!)
        adminlist = [240188083]

    # caricamento degli eventi gestiti
    eventi_list = {}
    eventi_list = telegram_events.events(msg, ["LK", "NM"], response)
    text = eventi_list["text"]
    type_msg = eventi_list["type_msg"]

    query_id = "-"
    if type_msg == "BIC" and "id" in msg:
        query_id = msg["id"]

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
         InlineKeyboardButton(
             text=frasi["button_testo_social"], callback_data='/social'),
         InlineKeyboardButton(text=frasi["button_testo_supporto"], callback_data='/supporto')],

        [InlineKeyboardButton(text=frasi["button_testo_avvisi"], callback_data='/avvisi'),
         InlineKeyboardButton(
             text=frasi["button_testo_call"], callback_data='/meeting'),
         InlineKeyboardButton(text=frasi["button_testo_progetti_attivi"], callback_data='/progetti')],

        [InlineKeyboardButton(text=frasi["button_testo_vademecum"], callback_data='/vademecum'),
         InlineKeyboardButton(
             text=frasi["button_testo_regolamento"], callback_data='/regolamento'),
         InlineKeyboardButton(text=frasi["button_testo_info"], callback_data='/info')],
        [InlineKeyboardButton(text=frasi["button_feedback"],
                              callback_data='/feedback')],
    ])


    gruppi = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=frasi["button_testo_home"], url=GRUPPI_URL['home']),
         InlineKeyboardButton(text=frasi["button_testo_news"], url=GRUPPI_URL['news'])],
        [InlineKeyboardButton(text=frasi["button_testo_developers"], url=GRUPPI_URL['developers']),
         InlineKeyboardButton(text=frasi["button_testo_L10n"], url=GRUPPI_URL["l10n"])],
        [InlineKeyboardButton(text=frasi["button_testo_design_marketing"], url=GRUPPI_URL["design_marketing"])],
        [InlineKeyboardButton(
            text=frasi["button_mostra_help"], callback_data='/help')],
    ])

    developers = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=frasi["button_developers"],
                              url=GRUPPI_URL['developers'])],
        [InlineKeyboardButton(
            text=frasi["button_mostra_help"], callback_data='/help')],
    ])

    design_marketing = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=frasi["button_design_marketing"],
                              url=GRUPPI_URL['design_marketing'])],
        [InlineKeyboardButton(
            text=frasi["button_mostra_help"], callback_data='/help')],
    ])

    L10n = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=frasi["button_L10n"],
                              url=GRUPPI_URL['l10n'])],
        [InlineKeyboardButton(
            text=frasi["button_mostra_help"], callback_data='/help')],
    ])

    vademecum = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=frasi["button_vg"], callback_data='/vademecumGenerale'),
         InlineKeyboardButton(text=frasi["button_vt"], callback_data='/vademecumTecnico')],
         [InlineKeyboardButton(text=frasi["button_cv"], callback_data='/vademecumCV')],
        [InlineKeyboardButton(
            text=frasi["button_mostra_help"], callback_data='/help')],
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
        [InlineKeyboardButton(text=frasi["button_vai_a_canale_youtube"],
                              url='https://www.youtube.com/channel/UCsTquqVS0AJxCf4D3n9hQ1w')],
        [InlineKeyboardButton(text=frasi["button_call2"],
                              callback_data='/prossimoMeeting')],
        [InlineKeyboardButton(
            text=frasi["button_mostra_help"], callback_data='/help')],
    ])

    load_progetti = [ [InlineKeyboardButton(
            text=str(proj), url=liste["progetti"][proj])] for proj in list(liste["progetti"].keys()) ]
    load_progetti.append([InlineKeyboardButton(
        text=frasi["button_mostra_help"], callback_data='/help')])

    progetti = InlineKeyboardMarkup(inline_keyboard=load_progetti)
    
    load_progettimozita = []
    load_progettimozita = [ [InlineKeyboardButton(
            text=str(proj), url=liste["progetti_mozita"][proj])] for proj in list(liste["progetti_mozita"].keys()) ]
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

    # aggiungere instagram in futuro
    load_social = []
    load_social = [ [InlineKeyboardButton(
            text=social, url=liste["social"][social])] for social in list(liste["social"].keys()) ]
    load_social.append([InlineKeyboardButton(
        text=frasi["button_mostra_help"], callback_data='/help')])

    social = InlineKeyboardMarkup(inline_keyboard=load_social)

    admin = False
    collaboratori_stampa = ""
    for k, v in liste["collaboratori"].items():
        collaboratori_stampa += k + " - " + v + "\n"

    if chat_id not in all_users:
        all_users.append(chat_id)
        avvisi_on_list.append(user_id)
        try:
            with open(all_users_path, "wb") as file_with:
                file_with.write(json.dumps(all_users).encode("utf-8"))
        except Exception as exception_value:
            print("Excep:03 -> " + str(exception_value))
            log("Except:03 ->" + str(exception_value), True)
        try:
            with open(avvisi_on_list_path, "wb") as file_with:
                file_with.write(json.dumps(avvisi_on_list).encode("utf-8"))
        except Exception as exception_value:
            print("Excep:04 -> " + str(exception_value))
            log("Except:04 ->" + str(exception_value), True)

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
    elif text.lower() == "/vademecum":
        bot.sendMessage(chat_id, frasi["vademecum"],
                        reply_markup=vademecum, parse_mode="HTML")
    elif text.lower() == "/vademecumGenerale".lower():
        bot.sendMessage(chat_id, frasi["invio_vg_in_corso"], parse_mode="HTML")
        bot.sendDocument(chat_id, open("VG.pdf", "rb"))
    elif text.lower() == "/vademecumTecnico".lower():
        bot.sendMessage(chat_id, frasi["invio_vt_in_corso"], parse_mode="HTML")
        bot.sendDocument(chat_id, open("VT.pdf", "rb"))
    elif text.lower() == "/vademecumCV".lower():
        bot.sendMessage(chat_id, frasi["invio_cv_in_corso"], parse_mode="HTML")
        bot.sendDocument(chat_id, open("CV.pdf", "rb"))
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
    elif text.lower() == "/developers":
        bot.sendMessage(chat_id, frasi["developers"],
                        reply_markup=developers, parse_mode="HTML")
    elif text.lower() == "/dem":
        bot.sendMessage(chat_id, frasi["design_marketing"],
                        reply_markup=design_marketing, parse_mode="HTML")
    elif text.lower() == "/l10n":
        bot.sendMessage(chat_id, frasi["L10n"],
                        reply_markup=L10n, parse_mode="HTML")
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
                log("Except:05 ->" + str(exception_value), True)
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
                log("Except:06 ->" + str(exception_value), True)
                bot.sendMessage(
                    chat_id, frasi["avvisiOff2"], parse_mode="HTML")
        else:
            bot.sendMessage(chat_id, frasi["avvisiOff3"])
    elif text.lower() == "/social".lower():
        bot.sendMessage(chat_id, frasi["social"],
                        reply_markup=social, parse_mode="HTML")
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

    if type_msg == "BIC" and query_id != "-":
        bot.answerCallbackQuery(query_id,
                                cache_time=0)  # se voglio mostrare un messaggio a scomparsa: bot.answerCallbackQuery(chat_id, text="Testo (0-200 caratteri)" cache_time=0)

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
                                "- <code>/admin avviso preview |Messaggio da inviare|</code>\n  <i>Anteprima del messaggio da inviare, per verificare che tutto venga visualizzato correttamente</i>\n" +
                                "- <code>/admin all users |Messaggio importante da inviare|</code>\n  <i>Solo per messaggi importanti, altrimenti usare 'avviso'</i>\n" +
                                "\n" +
                                "<b>Gestione lista degli iscritti agli avvisi</b>\n" +
                                "- <code>/admin avvisi list mostra</code>\n" +
                                "- <code>/admin avvisi list aggiungi |Id chat|</code>\n" +
                                "- <code>/admin avvisi list elimina |Id chat|</code>\n" +
                                "\n" +
                                "<b>Gestione canali</b>:\n" +
                                "- <code>/admin canale mostra</code>\n" +
                                "- <code>/admin canale aggiungi |Username canale|</code>\n" +
                                "- <code>/admin canale elimina |Username canale|</code>\n" +
                                
                                "- <code>/admin canale preview |Username canale| |Messaggio da inviare in un canale|</code>\n  <i>Anteprima del messaggio da inviare, per verificare che tutto venga visualizzato correttamente</i>\n" + 
                                "- <code>/admin canale |Username canale| |Messaggio da inviare in un canale|</code>\n" + 
                                "- <code>/admin canale broadcast |Messaggio da inviare in tutti i canali|</code>\n" + 

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
                                "- <code>/admin scarica today</code>\n" +
                                "- <code>/admin scarica yesterday</code>\n" +
                                "\n" +
                                "<b>Esempi:</b>\n" +
                                "- <code>/admin avviso Messaggio di prova</code>\n" +
                                "- <code>/admin call aggiungi Nome call di esempio 2019 https://mozillaitalia.it</code>\n" +
                                "- <code>/admin scarica 2019 10 09</code>",
                                parse_mode="HTML")
            # ======
            # AVVISO
            # ======
            elif azione[1].lower() == "avviso" and len(azione) >= 3:
                # Azioni sugli avvisi
                del azione[0]
                del azione[0]

                # Syntax : /admin avviso preview |Messaggio da inviare|
                if azione[0].lower() == "preview" and len(azione) >= 4:
                    del azione[0]
                    messaggio = ' '.join(azione)
                    try:
                        bot.sendMessage(
                            chat_id,
                            "<b>‼️‼️ ||PREVIEW DEL MESSAGGIO|| ‼️‼</b>️\n\n" +
                            messaggio +
                            "\n\n--------------------\n" +
                            frasi["footer_messaggio_avviso"],
                            parse_mode="HTML")
                    except Exception as exception_value:
                        print("Excep:23 -> " + str(exception_value))
                        log("Except:23 ->" + str(exception_value), True)
                        bot.sendMessage(
                            chat_id,
                            "‼️ <b>ERRORE</b>: il messaggio contiene degli errori di sintassi.\n" +
                            "Verificare di avere <b>chiuso</b> tutti i tag usati.",
                            parse_mode="HTML")
                else:
                    # Syntax : /admin avviso |Messaggio da inviare|
                    messaggio = ' '.join(azione)
                    error08 = False
                    bot.sendMessage(
                        chat_id,
                        "<i>Invio del messaggio in corso...\nRiceverai un messaggio quando finisce l'invio.</i>",
                        parse_mode="HTML")
                    remove_these_users = []
                    for value_for in avvisi_on_list:
                        time.sleep(.3)
                        try:
                            bot.sendMessage(
                                value_for,
                                messaggio +
                                "\n\n--------------------\n" +
                                frasi["footer_messaggio_avviso"],
                                parse_mode="HTML")
                            print(" >> Messaggio inviato alla chat: " + str(value_for))
                            '''
                            bot.sendMessage(
                                chat_id,
                                "✔️ Messaggio inviato alla chat: <a href='tg://user?id=" + str(value_for) + "'>" +
                                str(value_for) + "</a>",
                                parse_mode="HTML")
                            '''
                        except Exception as exception_value:
                            print("Excep:08 -> " + str(exception_value))
                            log("Except:08 ->" +
                                str(exception_value), True)
                            remove_these_users.append(value_for)
                            error08 = True
                    for value_to_remove in remove_these_users:
                        remove_user_from_avvisi_allusers_lists(
                            chat_id, value_to_remove)
                    if (not error08):
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

            # canale => gestisce i canali
            # syntax: /admin canale mostra
            # OPPURE
            # syntax: /admin canale lista
            elif azione[1].lower() == "canale" and len(azione) >= 3:
                del azione[0]
                del azione[0]

                # shows channels saved on file
                # everytime it reloads the file to avoid uncommon situations
                if azione[0] == "mostra" or azione[0] == "lista" and len(azione) == 1:
                    channels_list = list(liste["channels"].keys())
                    bot.sendMessage(
                        chat_id, "Lista canali disponibili:\n{}".format(channels_list))

                # preview messaggio canale => non invia il messaggio
                # syntax: /admin canale preview |canale||messaggio|
                elif len(azione) >= 4 and azione[0].lower() == "preview":
                    # delete all the part not-related to the message (preview)
                    del azione[0]

                    # saves channel name
                    ch = azione[0]
                    del azione[0]

                    messaggio = ' '.join(azione)

                    if messaggio != "":
                        try:
                            bot.sendMessage(
                                chat_id,
                                "<b>== PREVIEW DEL MESSAGGIO ==</b>️\n" +
                                "<i>Questo messaggio sarà inoltrato in: <code>" + ch + "</code></i>️\n\n"+
                                messaggio + "\n",
                                parse_mode="HTML")
                        except Exception as exception_value:
                            print("Excep:26 -> " + str(exception_value))
                            log("Except:26 ->" +
                                str(exception_value), True)
                            bot.sendMessage(
                                chat_id,
                                "‼️ <b>ERRORE</b>: il messaggio contiene degli errori di sintassi.\n" +
                                "Verificare di avere <b>chiuso</b> tutti i tag usati.",
                                parse_mode="HTML")
                    else:
                        bot.sendMessage(
                            chat_id,
                            "‼️ <b>ERRORE</b>: La preview è vuota! Assicurati di inserire un messaggio " +
                            "e riprova",
                            parse_mode="HTML")
                        print("La preview non può essere vuota.")

                # adds a channel in a file
                # syntax /admin canale aggiungi |username canale | descrizione |
                elif azione[0].lower() == "aggiungi" and len(azione) == 2:
                    # lets fix the username by adding @ at the beginning if not present
                    fixed_username = fix_username(azione[1]).lower()
                    
                    # manage the case the user doesn't put anything
                    # TODO: let the user choice the name
                    
                    # lets check if username is not present in the channel_list
                    if fixed_username not in liste["channels"]:
                        try:
                            liste["channels"][fixed_username] = "undefined"
                            updateJSON(liste, lists_path)

                            bot.sendMessage(
                                chat_id, "Canale <code>{}</code> aggiunto correttamente".format(fixed_username), parse_mode="HTML")
                        except Exception as exception_value:
                            print("Excep:28 -> {}".format(exception_value))
                            log("Except:28 -> {}".format(exception_value), True)
                            bot.sendMessage(
                                chat_id, "Il canale <code>{}</code> non è stato aggiunto in lista".format(fixed_username), parse_mode="HTML")
                    else:
                        print("Il canale " + fixed_username + " è già presente!")
                        bot.sendMessage(
                            chat_id, "Il canale <code>{}</code> è già presente nella lista!".format(fixed_username), parse_mode="HTML")


                # removes a channel in a file
                # syntax /admin canale elimina |username canale| IN ALTERNATIVA
                # syntax /admin canale rimuovi |username canale|
                elif azione[0].lower() == "elimina" or azione[0].lower() == "rimuovi" and len(azione) == 2:
                    try:
                        liste["channels"].pop(fix_username(azione[1]))
                        updateJSON(liste, lists_path)

                        bot.sendMessage(
                            chat_id, "Canale <code>{}</code> rimosso correttamente".format(azione[1].lower()), parse_mode="HTML")
                    except Exception as exception_value:
                        print("Excep:28 -> {}".format(exception_value))
                        log("Except:28 -> {}".format(exception_value), True)
                        bot.sendMessage(
                            chat_id, "Il canale <code>{}</code> non è stato rimosso dalla lista".format(azione[1].lower()), parse_mode="HTML")

                # canale |canale| |messaggio| => invia il messaggio a quel canale
                # syntax: /admin canale | canale | |Messaggio da inviare in un canale|"
                # syntax: /admin canale broadcast |Messaggio da inviare in tutti i canali|"
                elif len(azione) >= 2 or len(azione) >= 1:
                    messaggio = ""

                    # check: empty channels
                    if len(liste["channels"]) == 0:
                        bot.sendMessage(
                            chat_id,
                            "Lista canali vuota! Impossibile inviare un messaggio!",
                            parse_mode="HTML")

                        print("Lista canali vuota! Impossibile inviare un messaggio!")
                    else:
                        if azione[0].lower() == "broadcast":
                            del azione[0]

                            messaggio = ' '.join(azione)

                            if messaggio != "":
                                for channel_name in liste["channels"].keys():
                                    send_message_channel(
                                        channel_name, messaggio, chat_id, "Messaggio non inviato in ")
                            else:
                                bot.sendMessage(
                                    chat_id,
                                    "Messaggio vuoto. Impossibile procedere.",
                                    parse_mode="HTML")

                                print("Messaggio vuoto. Impossibile procedere.")
                        else:
                            # it is not a broadcast message
                            channel_name = fix_username(azione[0])
                            del azione[0]

                            messaggio = ' '.join(azione)

                            if messaggio != "":
                                send_message_channel(
                                    channel_name, messaggio, chat_id)
                            else:
                                bot.sendMessage(
                                    chat_id,
                                    "Messaggio vuoto. Impossibile procedere.",
                                    parse_mode="HTML")


                else:
                    print("Comando non riconosciuto.")
                    admin_err1 = True

            # /admin all users
            elif azione[1].lower() == "all" and azione[2].lower() == "users" and len(azione) >= 4:
                # Azioni sugli avvisi importanti (tutti gli utenti)
                del azione[0]
                del azione[0]
                del azione[0]
                messaggio = ' '.join(azione)
                bot.sendMessage(
                    chat_id,
                    "<i>Invio del messaggio in corso...\nRiceverai un messaggio quando finisce l'invio.</i>",
                    parse_mode="HTML")
                remove_these_users = []
                for value_for in all_users:
                    time.sleep(.3)
                    try:
                        bot.sendMessage(
                            value_for,
                            "<b>Messaggio importante</b>\n" + messaggio,
                            parse_mode="HTML")
                        print(" >> Messaggio inviato alla chat: " + str(value_for))
                        '''bot.sendMessage(
                            chat_id, "✔️ Messaggio inviato alla chat: <a href='tg://user?id=" + str(value_for) + "'>" +
                                     str(value_for) + "</a>",
                            parse_mode="HTML")'''
                    except Exception as exception_value:
                        print("Excep:07 -> " + str(exception_value))
                        log("Except:07 ->" +
                            str(exception_value), True)
                        remove_these_users.append(value_for)
                for value_to_remove in remove_these_users:
                    remove_user_from_avvisi_allusers_lists(
                        chat_id, value_to_remove)
                bot.sendMessage(
                    chat_id,
                    "Messaggio inviato correttamente a tutti gli utenti.\n\nIl messaggio inviato è:\n" +
                    messaggio,
                    parse_mode="HTML")
            elif azione[1].lower() == "avvisi" and azione[2].lower() == "list" and len(azione) >= 4:
                # Azioni sugli utenti (chat_id) presenti in avvisi_on_list.json
                if azione[3].lower() == "mostra":
                    bot.sendMessage(
                        chat_id, "Ecco la 'avvisi_on_list':\n\n" + str(avvisi_on_list))
                elif azione[3].lower() == "aggiungi":
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
                            log("Except:12 ->" +
                                str(exception_value), True)
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
                            log("Except:13 ->" +
                                str(exception_value), True)
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
                    if not nome in liste["progetti_mozita"]:
                        liste["progetti_mozita"][nome] = str(link)
                        try:
                            updateJSON(liste, lists_path)
                            bot.sendMessage(
                                chat_id,
                                "Progetto comunitario '" +
                                str(nome) +
                                "' (" +
                                str(link) +
                                ") inserito correttamente.")
                        except Exception as exception_value:
                            print("Excep:17 -> " + str(exception_value))
                            log("Except:17 ->" +
                                str(exception_value), True)
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
                    if nome in liste["progetti_mozita"]:
                        liste["progetti_mozita"][nome] = str(link)
                        try:
                            updateJSON(liste, lists_path)
                            bot.sendMessage(
                                chat_id,
                                "Progetto '" +
                                str(nome) +
                                "' (" +
                                str(link) +
                                ") modificato correttamente.")
                        except Exception as exception_value:
                            print("Excep:18 -> " + str(exception_value))
                            log("Except:18 ->" +
                                str(exception_value), True)
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
                    if nome in liste["progetti_mozita"]:
                        liste["progetti_mozita"].pop(nome)
                        try:
                            updateJSON(liste, lists_path)
                            bot.sendMessage(
                                chat_id, "Progetto comunitario '" + str(nome) + "' eliminato correttamente.")
                        except Exception as exception_value:
                            print("Excep:19 -> " + str(exception_value))
                            log("Except:19 ->" +
                                str(exception_value), True)
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
                    if not nome in liste["progetti"]:
                        liste["progetti"][nome] = str(link)
                        try:
                            updateJSON(liste, lists_path)
                            bot.sendMessage(
                                chat_id,
                                "Progetto '" +
                                str(nome) +
                                "' (" +
                                str(link) +
                                ") inserito correttamente.")
                        except Exception as exception_value:
                            print("Excep:17 -> " + str(exception_value))
                            log("Except:17 ->" +
                                str(exception_value), True)
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

                    if nome in liste["progetti"]:
                        liste["progetti"][nome] = str(link)
                        try:
                            updateJSON(liste, lists_path)

                            bot.sendMessage(
                                chat_id,
                                "Progetto '" +
                                str(nome) +
                                "' (" +
                                str(link) +
                                ") modificato correttamente.")
                        except Exception as exception_value:
                            print("Excep:18 -> " + str(exception_value))
                            log("Except:18 ->" +
                                str(exception_value), True)
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
                    if nome in liste["progetti"]:
                        liste["progetti"][nome] = str(link)
                        try:
                            updateJSON(liste, lists_path)
                            bot.sendMessage(
                                chat_id, "Progetto '" + str(nome) + "' eliminato correttamente.")
                        except Exception as exception_value:
                            print("Excep:19 -> " + str(exception_value))
                            log("Except:19 ->" +
                                str(exception_value), True)
                            bot.sendMessage(
                                chat_id,
                                "Si è verificato un errore inaspettato e non è possibile salvare 'progetti_list.json'.")
                    else:
                        bot.sendMessage(chat_id, "Il progetto '" +
                                        str(nome) + "' non è stato trovato.")
                else:
                    admin_err1 = True
            elif azione[1].lower() == "collaboratore":
                # Azione sui collaboratori
                if azione[2].lower() == "aggiungi" and len(azione) >= 5:
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    username = azione[-1]
                    del azione[-1]
                    nome = ' '.join(azione)
                    if not username in liste["collaboratori"]:
                        liste["collaboratori"][fix_username(username)] = str(nome)
                        try:
                            updateJSON(liste, lists_path)

                            bot.sendMessage(
                                chat_id, "'" + str(nome) + "' aggiunto correttamente ai collaboratori.")
                        except Exception as exception_value:
                            print("Excep:20 -> " + str(exception_value))
                            log("Except:20 ->" +
                                str(exception_value), True)
                            bot.sendMessage(
                                chat_id,
                                "Si è verificato un errore inaspettato e non è possibile salvare 'collaboratori_hub.json'.")
                    else:
                        bot.sendMessage(chat_id, "'" + str(nome) + "' è già presente nella lista dei collaboratori.")
                elif azione[2].lower() == "elimina" or azione[2].lower() == "rimuovi":
                    del azione[0]
                    del azione[0]
                    del azione[0]
                    username = ' '.join(azione)
                    if fix_username(username) in liste["collaboratori"]:
                        liste["collaboratori"].pop(fix_username(username))
                        try:
                            updateJSON(liste, lists_path)

                            bot.sendMessage(
                                chat_id, "'" + str(username) + "' rimosso correttamente dai collaboratori.")
                        except Exception as exception_value:
                            print("Excep:21 -> " + str(exception_value))
                            log("Except:21 ->" +
                                str(exception_value), True)
                            bot.sendMessage(
                                chat_id,
                                "Si è verificato un errore inaspettato e non è possibile salvare 'collaboratori_hub.json'.")
                    else:
                        bot.sendMessage(
                            chat_id, "'" + str(username) + "' non è presente nella lista dei collaboratori.")
                else:
                    admin_err1 = True
            elif azione[1].lower() == "scarica" and len(azione) == 5:
                # Azione per scaricare file di log -> esempio: /admin scarica 2019 10 20
                nome_file = "log_" + azione[2] + "_" + \
                    azione[3] + "_" + azione[4] + ".txt"
                send_log(nome_file, chat_id)
            elif azione[1].lower() == "scarica" and azione[2].lower() == "today":
                # Azione per scaricare file di log di oggi
                nome_file = "log_" + data_salvataggio + ".txt"
                send_log(nome_file, chat_id)
            elif azione[1].lower() == "scarica" and azione[2].lower() == "yesterday":
                # Azione per scaricare file di log di ieri
                yesterday_time = datetime.now() - timedelta(days = 1)
                data_ieri = yesterday_time.strftime("%Y_%m_%d")
                nome_file = "log_" + data_ieri + ".txt"
                send_log(nome_file, chat_id)
            else:
                admin_err1 = True
        else:
            bot.sendMessage(
                chat_id,
                "Errore: Comando non riconosciuto.\nPer scoprire tutti i comandi consentiti in questa sezione digita /admin",
                parse_mode="HTML")

        if admin_err1:
            bot.sendMessage(
                chat_id,
                "Questo comando nella sezione ADMIN non è stato riconosciuto.\n\nPer scoprire tutti i comandi consentiti in questa sezione digita /admin",
                parse_mode="HTML")

    try:
        # stringa stampata a terminale, per ogni operazione effettuata
        stampa = str(localtime) + "  --  Utente: " + str(user_name) + " (" + str(user_id) + ")[" + str(
            status_user) + "]  --  Chat: " + str(
            chat_id) + "\n >> >> Tipo messaggio: " + str(type_msg) + "\n >> >> Contenuto messaggio: " + str(
            text)
        print(stampa + "\n--------------------\n")
        log(stampa, False)
    except Exception as exception_value:
        stampa = "Excep:01 -> " + \
            str(exception_value) + "\n--------------------\n"
        print(stampa)
        log("Except:01 ->" + str(exception_value), True)


try:
    bot = telepot.Bot(TOKEN)
    MessageLoop(
        bot, {'chat': risposte, 'callback_query': risposte}).run_as_thread()
except Exception as exception_value:
    print("ERRORE GENERALE.\n\nError: " +
        str(exception_value) + "\n--------------------\n")
    log("ERRORE GENERALE.\n\nError: " + str(exception_value), True)

# keeps the bot alive
while True:
    pass
