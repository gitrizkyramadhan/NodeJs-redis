# coding: utf-8
from celery import Celery

from decimal import Decimal
import traceback

from nlp_rivescript import Nlp
from module_banking import BankingModule
from datetime import datetime, timedelta
import MySQLdb
import json
import PythonMagick
import pdfkit
import os
import sys
import PyPDF2
import urllib2
import random, string
from data.line_template import Template

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *
from gmaps_geolocation import GMapsGeocoding

import urlparse
import requests
import httplib2




from bot import Bot



import logging

def init_qtgui(display=None, style=None, qtargs=None):
    """Initiates the QApplication environment using the given args."""
    if QApplication.instance():
        print "0"
        logger.debug("QApplication has already been instantiated. \
                        Ignoring given arguments and returning existing QApplication.")
        return QApplication.instance()

    qtargs2 = [sys.argv[0]]
    if display:
        qtargs2.append('-display')
        qtargs2.append(display)
        # Also export DISPLAY var as this may be used
        # by flash plugin
        os.environ["DISPLAY"] = display

    if style:
        qtargs2.append('-style')
        qtargs2.append(style)

    qtargs2.extend(qtargs or [])
    return QApplication(qtargs2)

#First Initialization
TOKEN_TELEGRAM=""
KEYFILE=""
CERTFILE=""
URL_TELEGRAM=""
MYSQL_HOST=""
MYSQL_USER=""
MYSQL_PWD=""
MYSQL_DB=""
WEB_HOOK=""
EMAIL_NOTIF=""
LINE_TOKEN=""

LINE_IMAGES_ROUTE = "https://bangjoni.com/line_images"

DEBUG_MODE = "D" #I=Info, D=Debug, V=Verbose, E=Error

##########OPEN CONFIGURATION#######################
with open('BJCONFIG.txt') as f:
    content = f.read().splitlines()
f.close()
TOKEN_TELEGRAM=content[0].split('=')[1]
KEYFILE=content[1].split('=')[1]
CERTFILE=content[2].split('=')[1]
URL_TELEGRAM=content[3].split('=')[1]
MYSQL_HOST=content[4].split('=')[1]
MYSQL_USER=content[5].split('=')[1]
MYSQL_PWD=content[6].split('=')[1]
MYSQL_DB=content[7].split('=')[1]
WEB_HOOK=content[8].split('=')[1]
EMAIL_NOTIF=content[9].split('=')[1]
LINE_TOKEN=content[11].split('=')[1]

linebot = Bot(LINE_TOKEN)
lineNlp = Nlp()
app_gui = init_qtgui()
bank = BankingModule()
gmaps = GMapsGeocoding()
template = Template()

app = Celery('tasksx', backend = 'amqp', broker = 'redis://localhost:6379/1')

F_SRVC = None
F_BOOK = None
F_PAID = None
F_NOREPLY = None
F_ADDFRIENDS = None

when = ['hari ini|hr ini|siang ini|malam ini|pagi ini|sore ini','besok|bsok|bsk','lusa','januari|jan','februari|feb|pebruari','maret|mar','april|apr','mei','juni|jun','juli|jul','agustus|aug|agus','september|sept|sep','oktober|okt|october|oct','november|nov|nop','desember|des|december|dec']

def search_string(mesg, dict):
    idx = 0
    found = 0
    for item in dict:
        for subitem in item.split('|'):
            if subitem in mesg.lower():
                found = 1
        if found == 1:
            return idx
        idx += 1
    if found == 1:
        return idx
    else:
        return -1


def _log_print(message, log_level = None) :
    if DEBUG_MODE == "V" : #highest
        level = 0
    elif DEBUG_MODE == "D" :
        level = 1
    elif DEBUG_MODE == "E" :
        level = 2
    elif DEBUG_MODE == "I" :
        level = 3

    if log_level :
        if log_level == "V":
            msg_level = 0
        elif log_level == "D":
            msg_level = 1
        elif log_level == "E":
            msg_level = 2
        elif log_level == "I":
            msg_level = 3
    else :
        msg_level = 3

    if level <= msg_level :
        print message

def _print_info(msg) :
    _log_print(msg, "I")

def _print_error(msg) :
    _log_print(msg, "E")

def _print_verbose(msg) :
    _log_print(msg, "V")

def _print_debug(msg) :
    _log_print(msg, "D")

def setup_logger(loggername, logfile):
    l = logging.getLogger(loggername)
    fileHandler = logging.FileHandler(logfile, mode='a')
    streamHandler = logging.StreamHandler()
    l.setLevel(level=logging.INFO)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler)

def save_last10chat(dtm, msisdn, mesg, actor):
    chat = str(dtm) + "|" + str(msisdn) + "|" + str(mesg) + "|" + str(actor)
    id = "savedchat/" + msisdn
    chat_len = len(lineNlp.redisconn.lrange(id,0,-1))
    if chat_len > 10:
        lineNlp.redisconn.lpop(id)
    lineNlp.redisconn.rpush(id, chat)
    if actor == 'BJ':
        record_answers(msisdn, str(mesg))

def request(sql):
    try:
        db_connect = MySQLdb.connect(host = MYSQL_HOST, port = 3306, user = MYSQL_USER, passwd = MYSQL_PWD, db = MYSQL_DB)
        # Create cursor
        cursor = db_connect.cursor()
        cursor.execute(sql)
        sqlout = cursor.fetchall()
        return sqlout
    except MySQLdb.Error, e:
        logDtm = (datetime.now() + timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')
        print e.args
        print "ERROR: %d: %s" % (e.args[0], e.args[1])

def insert(sql):
    try:
        db_connect = MySQLdb.connect(host = MYSQL_HOST, port = 3306, user = MYSQL_USER, passwd = MYSQL_PWD, db = MYSQL_DB)
        # Create cursor
        cursor = db_connect.cursor()
        cursor.execute(sql)
        db_connect.commit()
    except MySQLdb.Error, e:
        logDtm = (datetime.now() + timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')
        print e.args
        print "ERROR: %d: %s" % (e.args[0], e.args[1])

def insert5(sql):
    try:
        db_connect = MySQLdb.connect(host = "139.59.96.133", port = 3306, user = "root", passwd = "cikapali99", db = "bangjoni")
        # Create cursor
        cursor = db_connect.cursor()
        cursor.execute(sql)
        db_connect.commit()
    except MySQLdb.Error, e:
        logDtm = (datetime.now() + timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')
        print e.args
        print "ERROR: %d: %s" % (e.args[0], e.args[1])

def request5(sql):
    try:
        db_connect = MySQLdb.connect(host = "139.59.96.133", port = 3306, user = "root", passwd = "cikapali99", db = "bangjoni")
        # Create cursor
        cursor = db_connect.cursor()
        cursor.execute(sql)
        sqlout = cursor.fetchall()
        return sqlout
    except MySQLdb.Error, e:
        logDtm = (datetime.now() + timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')
        print e.args
        print "ERROR: %d: %s" % (e.args[0], e.args[1])

def fetchJSON(url):
    (resp_headers, content) = connAPI.request(url, "GET")

    try:
        decoded = json.loads(content)
        #print json.dumps(decoded, sort_keys=True, indent=4)
        return decoded
    except (ValueError, KeyError, TypeError):
        print "JSON format error"

#def fetchHTML(url):
#        try:
#           r = requests.get(url)
#           print "resp html: ", r.content
#           return r.content
#        except Exception as e:
#           print ">>Error is:",e


def fetchHTML(url):
    connAPI = httplib2.Http()
    try:
        (resp_headers, content) = connAPI.request(url, "GET")
        #print ">>resp_header", resp_headers
        return content
    except Exception as e:
        print ">>Error is:",e


def sendMessageTX(msisdn, message, keyboard):
    # linebot.send_message(msisdn, message.strip())
    linebot.send_text_message(msisdn, message)
    logDtm = (datetime.now() + timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')
    save_last10chat(logDtm, msisdn, message.strip(), 'BJ')

def sendPhotoTX(msisdn, file_path, caption, keyboard):
    # print "---------->", file_path.split('/')[6]
    # file_path = file_path.split('/')[6]
    # img_url = "http://128.199.88.72/line_images/%s" % (file_path)
    # linebot.send_images(msisdn,"http://128.199.88.72/line_images/%s" % (file_path), "http://128.199.88.72/line_images/%s" % (file_path.split('/')[6]))
    if file_path.find('') < 0:
        file_path = LINE_IMAGES_ROUTE+file_path
    linebot.send_image_message(msisdn, file_path)

def sendMessageT2(msisdn, message, keyboard = 0):
    sendMessageTX(msisdn, message, keyboard)

def sendPhotoT2(msisdn, file_path, caption = "", keyboard = 0):
    sendPhotoTX(msisdn, file_path, caption, keyboard)

def sendPhotoCaptionT2(msisdn, link_url, previewImageUrl, message):
    # linebot.send_images_text(msisdn, link_url, previewImageUrl, message.strip())
    linebot.send_image_message(msisdn, link_url)
    linebot.send_text_message(msisdn, message)
    logDtm = (datetime.now() + timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')
    save_last10chat(logDtm, msisdn, message.strip(), 'BJ')

def sendRichCaptionT2(msisdn, link_url, message, keyboard):
    if keyboard == "tiketux":
        # linebot.send_rich_message_payment_tiketux_text(msisdn, link_url,"Rich Message", message.strip())
        linebot.send_imagemap(msisdn, 'payment_tiketux')
        linebot.send_text_message(msisdn, message.strip())
    if keyboard == "tiketdotcom":
        # linebot.send_rich_message_payment_tiketdotcom_text(msisdn, link_url,"Rich Message", message.strip())
        linebot.send_imagemap(msisdn, 'payment_tiketdotcom')
        linebot.send_text_message(msisdn, message.strip())
    if keyboard == "tokenpln":
        # linebot.send_rich_message_token_pln_text(msisdn, link_url,"Rich Message", message.strip())
        linebot.send_imagemap(msisdn, 'payment_token')
        linebot.send_text_message(msisdn, message.strip())
    if keyboard == "pulsahp":
        # linebot.send_rich_message_pulsa_hp_text(msisdn, link_url,"Rich Message", message.strip())
        linebot.send_imagemap(msisdn, 'pulsa')
        linebot.send_text_message(msisdn, message.strip())
    if keyboard == "pulsaxl":
        linebot.send_imagemap(msisdn, 'pulsa_xl')
        linebot.send_text_message(msisdn, message.strip())
    if keyboard == "jatis":
        linebot.send_rich_message_payment_jatis_text(msisdn, link_url,"Rich Message", message.strip())
    if keyboard == "bjpayregister":
        # linebot.send_rich_message_bjpay_register_text(msisdn, link_url,"Rich Message", message.strip())
        linebot.send_imagemap(msisdn, 'bjpay_register')
        # linebot.send_text_message(msisdn, message.strip())
    if keyboard == "bjpaydeposit":
        # linebot.send_rich_message_bjpay_deposit_text(msisdn, link_url,"Rich Message", message.strip())
        linebot.send_imagemap(msisdn, 'bjpay_deposit')
        linebot.send_text_message(msisdn, message.strip())
    logDtm = (datetime.now() + timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')
    save_last10chat(logDtm, msisdn, message.strip(), 'BJ')

def sendLinkMessageT2(msisdn, message1, message2, message3, link_url, previewImageUrl):
    # print "-x-x-x-x-x-x-", message1, message2, message3, link_url
    # linebot.send_link_message(msisdn, message1.strip(), message2, message3, link_url, previewImageUrl)
    linebot.send_link_message(msisdn, 'Link Message', previewImageUrl, message1, message2, message3, link_url)
    logDtm = (datetime.now() + timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')
    save_last10chat(logDtm, msisdn, message1.strip(), 'BJ')

def log_service(logDtm, msisdn, first_name, service, desc = 'None'):
    #sql = "insert into request_service values('" + logDtm + "','" + msisdn + "','" + first_name + "','" + service + "')"
    sql = logDtm + "," + msisdn + "," + first_name + "," + service + "," + desc
    F_SRVC.info(sql)

def log_book(logDtm, msisdn, first_name, service, desc = 'None'):
    sql = logDtm + "," + msisdn + "," + first_name + "," + service + "," + desc
    F_BOOK.info(sql)

def log_paid(logDtm, msisdn, first_name, service, desc = 'None'):
    sql = logDtm + "," + msisdn + "," + first_name + "," + service + "," + desc
    F_PAID.info(sql)

def log_addfriends(logDtm, msisdn, first_name, service, desc = 'None'):
    sql = logDtm + "," + msisdn + "," + first_name + "," + service + "," + desc
    F_ADDFRIENDS.info(sql)

def record_answers(msisdn, answer) :
    if lineNlp.redisconn.exists("answers/%s" % (msisdn)):
        answers = json.loads(lineNlp.redisconn.get("answers/%s" % (msisdn)))
    else :
        answers = []
    answers.append(answer)
    lineNlp.redisconn.set("answers/%s" % (msisdn), json.dumps(answers))


def create_incoming_msisdn():
    logDtm = (datetime.now() + timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')
    incomingMsisdn = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, logDtm, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, "2017", "", [], 'no topic']
    return incomingMsisdn

    column = {}
    actions = []
    actions.append({'type': 'uri', 'label': 'Pilih destinasi lain', 'uri': microsite_url + 'msisdn=' + msisdn + '&d=CGK&a=SUB'})
    # actions.append({'type': 'message', 'label': 'Pilih destinasi lain', 'text': "ubah tanggal"})
    column['thumbnail_image_url'] = 'https://bangjoni.com/v2/carousel/flight/tujuan_lain.png'
    column['title'] = 'Gak ada?'
    column['text'] = "Tap 'Pilih' buat cari destinasi atau jadwal lain"
    if (len(column['text']) > 60):
        column['text'] = column['text'][:57] + '...'
    column['actions'] = actions
    columns.append(column)

    return columns

def genToken(digits):
    return ''.join(random.choice(string.lowercase) for i in range(digits))


def onMessage(msisdn, ask, first_name):

    # if ask == 'userexittorandom' :
    #     return

    if ask[:5] != "[LOC]":
        #ask = ask.translate(None, ",!.?$%").lower()
        #ask = ask.translate(None, "!?$%").lower()
        ask = ask.replace("-"," ")
        ask = ask.replace("!","")
        ask = ask.replace("?","")
        ask = ask.replace("$","")
        ask = ask.replace("\\","")
        ask = ask.replace("%","").lower()
    logDtm = (datetime.now() + timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')
    answer = ""
    print "--------------------------------------------------->",logDtm, msisdn, ask

    if lineNlp.redisconn.exists("inc/%s" % (msisdn)):
        incomingMsisdn = json.loads(lineNlp.redisconn.get("inc/%s" % (msisdn)))
        last_request = datetime.strptime(incomingMsisdn[12],'%Y-%m-%d %H:%M:%S')
        new_request = datetime.strptime(logDtm,'%Y-%m-%d %H:%M:%S')
        if (new_request - last_request).total_seconds() > 1800: #reset request after half an hour
            incomingMsisdn = create_incoming_msisdn()
            answer = lineNlp.doNlp("userexittorandom", msisdn, first_name)
    else:
        incomingMsisdn = create_incoming_msisdn()
    lineNlp.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))

    ask_temp = ask
    save_last10chat(logDtm, msisdn, ask, first_name)
    if ask[:5] != "[LOC]":

        answer = lineNlp.doNlp(ask, msisdn, first_name)
        answer = answer.strip()
        incomingMsisdn = json.loads(lineNlp.redisconn.get("inc/%s" % (msisdn)))

        print "_____________________>", answer, incomingMsisdn
        if (answer[:2] == "ee" and (incomingMsisdn[11] == "xt01" or incomingMsisdn[11] == "xt02")):
            ask = lineNlp.spell_correctness3(ask)
            print "correctness to: ", ask
            answer = lineNlp.doNlp(ask, msisdn, first_name)
            incomingMsisdn = json.loads(lineNlp.redisconn.get("inc/%s" % (msisdn)))
            incomingMsisdn[11] == ""
            print "-->", answer

    print "ask : " + ask + " dan answer :" + answer

    if ask[:5] == "[LOC]" and incomingMsisdn[11] == 'share_loc_atm':
        columns = []
        longlat = ask[5:].split(';')
        data_nearest_atm = bank.getNearestATMLocation(Decimal(longlat[0]), Decimal(longlat[1]))
        for i, data in enumerate(data_nearest_atm[:5]):
            i += 1
            column = {}
            actions = []
            column['thumbnail_image_url'] = gmaps.getImageLocationMap(Decimal(longlat[0]), Decimal(longlat[1]))
            column['title'] = data[3]
            column['text'] = data[8] + ' ' + data[9] + ' ' + data[10]
            if (len(column['text']) > 60):
                column['text'] = column['text'][:57] + '...'
            url_view = 'https://www.google.com/maps/search/?api=1&query='+str(longlat[0])+','+str(longlat[1])
            actions.append({'type' : 'postback', 'label' : 'Detail Lokasi', 'data' : '&evt=lokasi_atm&alamat_lengkap=' + data[8] + ' ' + data[9] + ' ' + data[10]})
            actions.append({'type': 'uri', 'label': 'Lihat Peta','uri': url_view})
            column['actions'] = actions
            columns.append(column)
        linebot.send_composed_carousel(msisdn, 'Lokasi ATM Terdekat', columns)
        # linebot.send_text_message(msisdn, 'location saved')

    if ask[:5] == "[LOC]" and incomingMsisdn[11] == 'share_loc_branch':
        columns = []
        longlat = ask[5:].split(';')
        data_nearest_atm = bank.getNearestBranchLocation(Decimal(longlat[0]), Decimal(longlat[1]))
        for i, data in enumerate(data_nearest_atm[:5]):
            i += 1
            column = {}
            actions = []
            column['thumbnail_image_url'] = gmaps.getImageLocationMap(Decimal(longlat[0]), Decimal(longlat[1]))
            column['title'] = 'Lokasi ' + str(i)
            column['text'] = data[3]
            if (len(column['text']) > 60):
                column['text'] = column['text'][:57] + '...'
            url_view = 'https://www.google.com/maps/search/?api=1&query='+str(longlat[0])+','+str(longlat[1])
            actions.append({'type' : 'postback', 'label' : 'Detail Lokasi', 'data' : '&evt=lokasi_atm&alamat_lengkap=' + data[8] + ' ' + data[9] + ' ' + data[10]})
            actions.append({'type': 'uri', 'label': 'Lihat Peta','uri': url_view})
            column['actions'] = actions
            columns.append(column)
        linebot.send_composed_carousel(msisdn, 'Lokasi ATM Terdekat', columns)


    if ask[:5] == "[LOC]" and incomingMsisdn[11] == 'share_loc_agen':
        columns = []
        longlat = ask[5:].split(';')
        data_nearest_atm = bank.getNearestAgen(Decimal(longlat[0]), Decimal(longlat[1]))
        for i, data in enumerate(data_nearest_atm[:5]):
            i += 1
            column = {}
            actions = []
            column['thumbnail_image_url'] = gmaps.getImageLocationMap(Decimal(longlat[0]), Decimal(longlat[1]))
            column['title'] = data[6]
            column['text'] = data[9]
            if (len(column['text']) > 60):
                column['text'] = column['text'][:57] + '...'
            url_view = 'https://www.google.com/maps/search/?api=1&query='+str(longlat[0])+','+str(longlat[1])
            actions.append({'type' : 'postback', 'label' : 'Detail Lokasi', 'data' : 'evt=detail_lokasi_agen&alamat=' + data[9] + ' , ' + data[11] + ' , ' + data[12] + ' , ' + data[13] + '&telp=' + data[17] + '&nama=' + data[6] + '&jenis=' + data[25]})
            actions.append({'type': 'uri', 'label': 'Lihat Peta','uri': url_view})
            column['actions'] = actions
            columns.append(column)
        linebot.send_composed_carousel(msisdn, 'Lokasi ATM Terdekat', columns)

    ####################GREETINGS####################
    if answer[:4] == "gr01":
        linebot.send_text_message(msisdn,'Selamat datang ' + first_name + ', saya Maya, asisten pribadi Anda untuk chat banking dari BNI. Ada yang bisa saya bantu?')
        linebot.send_carousel(msisdn, 'greetings')
        linebot.send_text_message(msisdn, answer[4:])


    ###################ATM LOCATION##################
    if answer.strip().lower() == "info atm":
        linebot.send_text_message(msisdn, 'Silakan gunakan fitur share location untuk melakukan pencarian ATM BNI terdekat dari lokasi Anda')
        if (new_request - last_request).total_seconds() > 1800:  # reset request after half an hour
            incomingMsisdn = create_incoming_msisdn()
        incomingMsisdn[11] = 'share_loc_atm'
        lineNlp.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))

    if answer.strip().lower() == "info branch":
        linebot.send_text_message(msisdn, 'Silakan gunakan fitur share location untuk melakukan pencarian kantor cabang BNI terdekat dari lokasi Anda')
        if (new_request - last_request).total_seconds() > 1800:  # reset request after half an hour
            incomingMsisdn = create_incoming_msisdn()
        incomingMsisdn[11] = 'share_loc_branch'
        lineNlp.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))

    if answer.strip().lower() == "info agen":
        linebot.send_text_message(msisdn, 'Silakan gunakan fitur share location untuk melakukan pencarian agen46 BNI terdekat dari lokasi Anda')
        if (new_request - last_request).total_seconds() > 1800:  # reset request after half an hour
            incomingMsisdn = create_incoming_msisdn()
        incomingMsisdn[11] = 'share_loc_agen'
        lineNlp.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))

    if ask.__contains__("register") :
        columns = []
        token = genToken(16)
        column = {}
        actions = []
        column['thumbnail_image_url'] = 'https://bangjoni.com/images/bni/BNI-Carousel-Menu_Produk.jpg'
        column['title'] = "Register"
        column['text'] = "Mulai Register !"
        if (len(column['text']) > 60):
            column['text'] = column['text'][:57] + '...'
        url_view = 'http://128.199.88.72:3000/chat?msisdn=' + msisdn + '&service=createAccount' + '&key=' + token
        actions.append({'type': 'uri', 'label': 'Register', 'uri': url_view})
        column['actions'] = actions
        columns.append(column)
        incomingMsisdn = create_incoming_msisdn()
        key_session = 'token/' + token
        lineNlp.redisconn.set(key_session, json.dumps(incomingMsisdn))
    linebot.send_composed_carousel(msisdn, 'Mulai Register', columns)

    ###################INFO PROMO##################
    if answer.strip().lower() == "info promo":
        linebot.send_image_button(msisdn, "promo")

    ###################INFO PROMO##################
    if answer.strip().lower() == "info produk":
        linebot.send_image_button(msisdn, "produk")

def sendMessageToCather(msisdn, socetid, ask, firs_tname):

    data = {
        "msisdn" : msisdn,
        "socketid" : socetid,
        "msg" : ask,
        "first_name" : firs_tname
    }
    req = urllib2.Request("http://128.199.88.72:3000/callback")
    req.add_header('Content-Type', 'application/json')

    response = urllib2.urlopen(req, json.dumps(data))
    print response
    return "OK"


def onMessageTransactional(msisdn, socketid,  ask, first_name):

    logDtm = (datetime.now() + timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')
    answer = ""
    print "--------------------------------------------------->", logDtm, msisdn, ask

    if lineNlp.redisconn.exists("inc/%s" % (msisdn)):
        incomingMsisdn = json.loads(lineNlp.redisconn.get("inc/%s" % (msisdn)))
        last_request = datetime.strptime(incomingMsisdn[12],'%Y-%m-%d %H:%M:%S')
        new_request = datetime.strptime(logDtm,'%Y-%m-%d %H:%M:%S')
        if (new_request - last_request).total_seconds() > 1800: #reset request after half an hour
            incomingMsisdn = create_incoming_msisdn()
            answer = lineNlp.doNlp("userexittorandom", msisdn, first_name)
    else:
        incomingMsisdn = create_incoming_msisdn()
    lineNlp.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))

    ask_temp = ask
    save_last10chat(logDtm, msisdn, ask, first_name)




@app.task(ignore_result=True)
def doworker(req):
    content = json.dumps(req)
    content = json.loads(content)
    print ""
    print "================================NEW LINE REQUEST============================================="
    print content

    if content.has_key('microsite_catcher'):
        for event in content['microsite_catcher']:
            socketid = event['socket_id']
            msisdn = event['msisdn']
            msg = event['msg']
            token = event['token']
            logDtm = (datetime.now() + timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')
            if lineNlp.redisconn.get("token/%s" % (token)):
                print "found key"
                incomingMsisdn = json.loads(lineNlp.redisconn.get("token/%s" % (token)))
                last_request = datetime.strptime(incomingMsisdn[12], '%Y-%m-%d %H:%M:%S')
                new_request = datetime.strptime(logDtm, '%Y-%m-%d %H:%M:%S')
                if (new_request - last_request).total_seconds() > 10:
                    print "timeoust session"
                    sendMessageToCather(msisdn,socketid,"tm00","")
                else:
                    print "update session"
                    incomingMsisdn[12] = logDtm
                    lineNlp.redisconn.set("token/%s" % (token), json.dumps(incomingMsisdn))
                    onMessageTransactional(msisdn, socketid, msg, "")
            else:
                print "create new session"
                # incomingMsisdn = create_incoming_msisdn()
                # lineNlp.redisconn.set("token/%s" % (token), incomingMsisdn)
                # onMessageTransactional(msisdn, socketid, msg, "")

    if not content.has_key('events'):
        return
    for event in content["events"] :
        msisdn = ""
        ask = ""
        longitude = ""
        latitude = ""
        username = ""
        first_name = ""
        last_name = ""
        phone_number = ""
        first_name_c = ""
        last_name_c = ""
        address = ""
        sticker	= ""
        stickerid = ""
        contentType = 0
        opType = ""

        try:
            if event["type"] == "message":
                contentType = event["message"]["type"]
                msisdn = str(event["source"]["userId"])
                if contentType == "text":
                    ask = str(event["message"]["text"])
                elif contentType == "location":
                    longitude = event["message"]["longitude"]
                    latitude = event["message"]["latitude"]
                    # address = event["message"]["address"]
                elif contentType == "sticker":
                    sticker = event["message"]["packageId"]
                    stickerid = event["message"]["stickerId"]
                    print "--->STICKER", sticker, stickerid
                    sendMessageT2(msisdn, "Makasih sticker-nya..", 0)
                elif contentType == "image":
                    print "--->IMAGE"
                    sendMessageT2(msisdn, "Makasih sharing fotonya ya..", 0)
                else:
                    print "--->"+contentType.capitalize()
                    sendMessageT2(msisdn, "Makasih sharing fotonya ya..", 0)
            else:
                opType = event["type"]
                if event["source"].has_key('userId'):
                    msisdn = str(event["source"]["userId"])
                elif event["source"].has_key('groupId'):
                    msisdn = str(event["source"]["groupId"])
                print "-->", opType, msisdn
        except:
            opType = content["result"][0]["content"]["opType"]
            msisdn = str(content["result"][0]["content"]["params"][0])
            print "-->", opType, msisdn


        logDtm = (datetime.now() + timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')

        if event["type"] == "message":
            if contentType == "text" or contentType == "location": # request text location
                print "Incoming>>>", logDtm, first_name, msisdn, ask, longitude, latitude, username

                incomingClient = lineNlp.redisconn.get("status/%s" % (msisdn))
                if incomingClient is None:
                    lineNlp.redisconn.set("status/%s" % (msisdn), 0)
                    incomingClient = "0"

                    #if incomingClient == "0":
                    #lineNlp.redisconn.set("status/%s" % (msisdn), 1)
                if longitude != "":
                    ask = "[LOC]" + str(latitude) + ";" + str(longitude)
                    print ">>>>>>>", longitude, ask
                displayname = ""
                try:
                    onMessage(str(msisdn), ask, displayname)
                    lineNlp.redisconn.set("status/%s" % (msisdn), 0)
                except Exception as e:
                    # print e
                    traceback.print_exc()
                    print "ERROR HAPPEN!!!"
                    lineNlp.redisconn.set("status/%s" % (msisdn), 0)
                    lineNlp.redisconn.delete("rs-users/%s" % (msisdn))

                    failureAns = lineNlp.doNlp("bjsysfail", msisdn, first_name)
                    sendMessageT2(msisdn, failureAns, 0)
        # elif event["type"] == "follow" or event["type"] == "unfollow": # request add friend and unblock
        #     displayname = ""
        #     reply = "Halo " + displayname + ", terima kasih telah add Bang Joni sebagai teman.\n\nBang Joni adalah teman virtual kamu yang bisa diandalkan kapan aja dan di mana aja.\nSekarang Bang Joni bisa bantu kamu pesen tiket pesawat, travel xtrans, uber, isi pulsa, isi token pln, infoin jalan tol dan cuaca, terjemahkan bahasa.\n\n"
        #     reply = reply + "Untuk memulai ketik aja \"Halo bang\"\n\nOh iya, pake penulisan yang benar ya, jangan terlalu banyak singkatan, biar Bang Joni nggak bingung."
        #     sendMessageT2(msisdn, reply, 0)
        #     log_addfriends(logDtm, msisdn, displayname, "ADD FRIENDS")

        elif event["type"] == "postback":
            msisdn = str(event["source"]["userId"])
            parsed = urlparse.urlparse('?' + event["postback"]["data"])
            postback_event = urlparse.parse_qs(parsed.query)['evt'][0]

            if postback_event == "lokasi_atm":
                alamat_lengkap = urlparse.parse_qs(parsed.query)['alamat_lengkap'][0]
                try:
                    linebot.send_text_message(msisdn,alamat_lengkap)
                except:
                    pass

            elif postback_event == "promo":
                number = urlparse.parse_qs(parsed.query)['num'][0]
                subevt = urlparse.parse_qs(parsed.query)['subevt'][0]
                if sub_event == "simpanan":
                    linebot.send_image_message(msisdn, "https://bangjoni.com/images/bni/Mengapa-BNI-Taplus.jpg")
                elif sub_event == "kredit":
                    linebot.send_image_message(msisdn, "https://bangjoni.com/images/bni/Kartu-Kredit-BNI.jpg")
                elif sub_event == "pinjaman":
                    linebot.send_image_message(msisdn, "https://bangjoni.com/images/bni/Suku-Bunga-BNI-Taplus.jpg")
            elif postback_event == "produk":
                sub_event = urlparse.parse_qs(parsed.query)['subevt'][0]
                if sub_event == "makanan":
                    linebot.send_carousel(msisdn, "promo_makanan")
                elif sub_event == "gadget":
                    linebot.send_carousel(msisdn, "promo_gadget")
            elif postback_event == "info_promo":
                sub_event = urlparse.parse_qs(parsed.query)['subevt'][0]
                detail_info = urlparse.parse_qs(parsed.query)['detail_info'][0]
                linebot.send_text_message(msisdn, detail_info)
            elif postback_event == 'detail_lokasi_agen':
                alamat = urlparse.parse_qs(parsed.query)['alamat'][0]
                telp = urlparse.parse_qs(parsed.query)['telp'][0]
                nama = urlparse.parse_qs(parsed.query)['nama'][0]
                jenis = urlparse.parse_qs(parsed.query)['jenis'][0]
                compose_detail = 'Nama : ' + nama + '\n' + 'Telp : ' + telp + '\n' + 'Alamat : ' + alamat + '\n' + 'Jenis : ' + jenis
                linebot.send_text_message(msisdn, compose_detail)
                linebot.send_confirmation(msisdn, "back_to_greetings")



#Second Initialization
print "Line bang joni bot personal assistant is online"

setup_logger('F_SRVC', '/home/bambangs/LOGBJ/F_SRVC.log')
setup_logger('F_BOOK', '/home/bambangs/LOGBJ/F_BOOK.log')
setup_logger('F_PAID', '/home/bambangs/LOGBJ/F_PAID.log')
setup_logger('F_NOREPLY', '/home/bambangs/LOGBJ/F_NOREPLY.log')
setup_logger('F_ADDFRIENDS', '/home/bambangs/LOGBJ/F_ADDFRIENDS.log')
F_SRVC = logging.getLogger('F_SRVC')
F_BOOK = logging.getLogger('F_BOOK')
F_PAID = logging.getLogger('F_PAID')
F_NOREPLY = logging.getLogger('F_NOREPLY')
F_ADDFRIENDS = logging.getLogger('F_ADDFRIENDS')  

