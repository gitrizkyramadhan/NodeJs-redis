# coding: utf-8
from celery import Celery

from decimal import Decimal
import traceback

from nlp_rivescript import Nlp
from html2png import Html2Png
from module_banking import BankingModule
from datetime import datetime, timedelta
import MySQLdb
import json
import PythonMagick
import pdfkit
import os
import sys
import PyPDF2

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *
from gmaps_geolocation import GMapsGeocoding

import urlparse
import requests
import httplib2



from fbm_bot import Bot
from data.template import Template


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
        qtargs2.append('-stfyle')
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
TOKEN=""

LINE_IMAGES_ROUTE = "https://bangjoni.com/line_images"

DEBUG_MODE = "D" #I=Info, D=Debug, V=Verbose, E=Error

##########OPEN CONFIGURATION#######################
with open('BJCONFIG.txt') as f:
    content = f.read().splitlines()
f.close()
KEYFILE=content[1].split('=')[1]
CERTFILE=content[2].split('=')[1]
URL_TELEGRAM=content[3].split('=')[1]
MYSQL_HOST=content[4].split('=')[1]
MYSQL_USER=content[5].split('=')[1]
MYSQL_PWD=content[6].split('=')[1]
MYSQL_DB=content[7].split('=')[1]
WEB_HOOK=content[8].split('=')[1]
EMAIL_NOTIF=content[9].split('=')[1]


fbmbot = Bot("EAAUSZCuERiN4BAIYS7EtOXnnh4k8BC7EJZATEeFQHdOHOujY7g8pbgFZAL5EAiw2plGA5maNACEzX5ZAa0OwuBMq7ZCFog5S9UqbFbzynba7ZBZCBzqOeSMgsrY2AP6X9mRsxiB9ZBVZCVD75d0lIvERh0XMak0t6gUuZCGawc6Yc5nQZDZD")
fbmNlp = Nlp()
app_gui = init_qtgui()
lineHtml2Png = Html2Png()
bank = BankingModule()
gmaps = GMapsGeocoding()
template = Template()
app = Celery('fbm_tasksx', backend = 'amqp', broker = 'redis://localhost:6379/0')

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

def record_answers(msisdn, answer) :
    if fbmNlp.redisconn.exists("answers/%s" % (msisdn)):
        answers = json.loads(fbmNlp.redisconn.get("answers/%s" % (msisdn)))
    else :
        answers = []
    answers.append(answer)
    fbmNlp.redisconn.set("answers/%s" % (msisdn), json.dumps(answers))

def save_last10chat(dtm, msisdn, mesg, actor):
    chat = str(dtm) + "|" + str(msisdn) + "|" + str(mesg) + "|" + str(actor)
    id = "savedchat/" + msisdn
    chat_len = len(fbmNlp.redisconn.lrange(id,0,-1))
    if chat_len > 10:
        fbmNlp.redisconn.lpop(id)
        fbmNlp.redisconn.rpush(id, chat)

    if actor == 'BJ':
        record_answers(msisdn, str(mesg))

def create_incoming_msisdn():
    logDtm = (datetime.now() + timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')
    incomingMsisdn = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, logDtm, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, "2017", "", [], 'no topic']
    return incomingMsisdn





def onMessage(msisdn, ask, first_name):



    logDtm = (datetime.now() + timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')

    if fbmNlp.redisconn.exists("inc/%s" % (msisdn)):
        incomingMsisdn = json.loads(fbmNlp.redisconn.get("inc/%s" % (msisdn)))
        last_request = datetime.strptime(incomingMsisdn[12],'%Y-%m-%d %H:%M:%S')
        new_request = datetime.strptime(logDtm,'%Y-%m-%d %H:%M:%S')
        if (new_request - last_request).total_seconds() > 1800: #reset request after half an hour
            incomingMsisdn = create_incoming_msisdn()
            answer = fbmNlp.doNlp("userexittorandom", msisdn, first_name)
    else:
        incomingMsisdn = create_incoming_msisdn()

    print ask
    print incomingMsisdn
    fbmNlp.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))

    if ask[:4] == "gr01":
        fbmbot.send_text_message(msisdn, 'Selamat datang '+ first_name +', saya Maya, asisten pribadi Anda untuk chat banking dari BNI. Ada yang bisa saya bantu?')
        fbmbot.send_generic_message(msisdn, template.data_template_greeting)
    elif ask == "info promo":
        fbmbot.send_generic_message(msisdn, template.data_template_promo)
    elif ask == "info produk":
        fbmbot.send_generic_message(msisdn, template.data_template_produk)
    elif ask == "info atm":
        # fbmbot.send_text_message(msisdn, 'Silakan gunakan fitur share location untuk melakukan pencarian ATM BNI terdekat dari lokasi Anda')
        fbmbot.send_quick_replies_messages(msisdn, 'Silakan gunakan fitur share location untuk melakukan pencarian ATM BNI terdekat dari lokasi Anda', [{"content_type":"location"}])
        if (new_request - last_request).total_seconds() > 1800:  # reset request after half an hour
            incomingMsisdn = create_incoming_msisdn()
        incomingMsisdn[11] = 'share_loc_atm'
        fbmNlp.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))
    elif ask == "info makanan":
        fbmbot.send_generic_message(msisdn, template.data_template_promo_makanan)
        fbmbot.send_button_message(msisdn, "Baik " + first_name + ", apa ada lagi yang dapat Maya bantu?",
                                   template.data_button_greeting)
    elif ask == "info gadget":
        fbmbot.send_generic_message(msisdn, template.data_template_promo_gadget)
        fbmbot.send_button_message(msisdn, "Baik " + first_name + ", apa ada lagi yang dapat Maya bantu?",
                                   template.data_button_greeting)
    elif ask == "simpanan":
        fbmbot.send_image_url(msisdn, 'https://bangjoni.com/images/bni/Mengapa-BNI-Taplus.jpg')
        fbmbot.send_button_message(msisdn, "Baik " + first_name + ", apa ada lagi yang dapat Maya bantu?",
                                   template.data_button_greeting)
    elif ask == "kartu kredit":
        fbmbot.send_image_url(msisdn, 'https://bangjoni.com/images/bni/Kartu-Kredit-BNI.jpg')
        fbmbot.send_button_message(msisdn, "Baik " + first_name + ", apa ada lagi yang dapat Maya bantu?",
                                   template.data_button_greeting)
    elif ask == "pinjaman" :
        fbmbot.send_image_url(msisdn, 'https://bangjoni.com/images/bni/Suku-Bunga-BNI-Taplus.jpg')
        fbmbot.send_button_message(msisdn, "Baik " + first_name + ", apa ada lagi yang dapat Maya bantu?",
                                   template.data_button_greeting)
    elif ask == "info cabang":
        # fbmbot.send_text_message(msisdn, 'Silakan gunakan fitur share location untuk melakukan pencarian kantor cabang BNI terdekat dari lokasi Anda')
        fbmbot.send_quick_replies_messages(msisdn, 'Silakan gunakan fitur share location untuk melakukan pencarian kantor cabang BNI terdekat dari lokasi Anda',[{"content_type": "location"}])
        if (new_request - last_request).total_seconds() > 1800:  # reset request after half an hour
            incomingMsisdn = create_incoming_msisdn()
        incomingMsisdn[11] = 'share_loc_branch'
        fbmNlp.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))
    elif ask == "info agen":
        # fbmbot.send_text_message(msisdn, 'Silakan gunakan fitur share location untuk melakukan pencarian agen46 BNI terdekat dari lokasi Anda')
        fbmbot.send_quick_replies_messages(msisdn, 'Silakan gunakan fitur share location untuk melakukan pencarian agen46 BNI terdekat dari lokasi Anda',[{"content_type": "location"}])
        if (new_request - last_request).total_seconds() > 1800:  # reset request after half an hour
            incomingMsisdn = create_incoming_msisdn()
        incomingMsisdn[11] = 'share_loc_agen'
        fbmNlp.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))
    elif ask[:4] == "nh01":
        fbmbot.send_text_message(msisdn,"Terima	kasih, data Anda sudah saya	catat dan petugas BNI akan segera menghubungi Anda untuk proses selanjutnya. Apa ada lagi yang dapat Maya bantu?")
        fbmbot.send_generic_message(msisdn, template.data_template_greeting)


    elif ask[:19] == "[USER_GET_SERVICES]":
        fbmbot.send_text_message(msisdn,"Silakan ketik Nama	Lengkap	beserta	Nomor HP Anda (contoh: Kenzie Abinaya 08123456789)")
        if (new_request - last_request).total_seconds() > 1800:  # reset request after half an hour
            incomingMsisdn = create_incoming_msisdn()
        incomingMsisdn[29] = 'nama_handphone'
        fbmNlp.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))
    # if ask[:19] == "" and incomingMsisdn[11] == "user_submit_data_services" :
    #     fbmbot.send_text_message(msisdn,"Terima	kasih, data Anda sudah saya	catat dan petugas BNI akan segera menghubungi Anda untuk proses selanjutnya. Apa ada lagi yang dapat Maya bantu?")
    #     fbmbot.send_generic_message(msisdn, template.data_template_greeting)


    elif ask[:5] == "[LOC]" and incomingMsisdn[11] == 'share_loc_atm':
        columns = []
        longlat = ask[5:].split(',')
        data_nearest_atm = bank.getNearestATMLocation(Decimal(longlat[0]), Decimal(longlat[1]))
        for data in data_nearest_atm:
            row = {}
            row['title'] = data[3]
            row['subtitle'] = data[8]
            row['image_url'] = gmaps.getImageLocationMap(Decimal(longlat[0]), Decimal(longlat[1]))
            button = []
            fill_button = {}
            fill_button['type'] = "postback"
            fill_button['title'] = "Detail Lokasi"
            fill_button['payload'] = "evt=detail_lokasi_atm&alamat=" + data[8] + ' ' + data[9] + ' ' + data[10] + "&jenis=" + data[4]
            button.append(fill_button)
            fill_button1 = {}
            url_view = 'https://www.google.com/maps/search/?api=1&query='+str(longlat[0])+','+str(longlat[1])
            fill_button1['type'] = "web_url"
            fill_button1['title'] = "View Map"
            fill_button1['url'] = url_view
            button.append(fill_button1)
            row['buttons'] = button
            columns.append(row)
            print columns
        fbmbot.send_generic_message(msisdn, columns)



    elif ask[:5] == "[LOC]" and incomingMsisdn[11] == 'share_loc_branch':
        columns = []
        longlat = ask[5:].split(',')
        data_nearest = bank.getNearestBranchLocation(Decimal(longlat[0]), Decimal(longlat[1]))
        print data_nearest
        counter = 0
        for data in data_nearest:
            counter += 1
            row = {}
            row['title'] = 'Lokasi ' + str(counter)
            row['subtitle'] = data[3]
            if (len(row['subtitle']) > 60):
                row['subtitle'] = row['subtitle'][:60] + '...'
            row['image_url'] = gmaps.getImageLocationMap(Decimal(longlat[0]), Decimal(longlat[1]))
            button = []
            fill_button = {}
            fill_button['type'] = "postback"
            fill_button['title'] = "Detail Lokasi"
            fill_button['payload'] = "evt=detail_lokasi&alamat=" + data[3]
            button.append(fill_button)
            fill_button1 = {}
            url_view = 'https://www.google.com/maps/search/?api=1&query=' + str(longlat[0]) + ',' + str(longlat[1])
            fill_button1['type'] = "web_url"
            fill_button1['title'] = "View Map"
            fill_button1['url'] = url_view
            button.append(fill_button1)
            row['buttons'] = button
            columns.append(row)
            print columns
        fbmbot.send_generic_message(msisdn, columns)

    elif ask[:5] == "[LOC]" and incomingMsisdn[11] == 'share_loc_agen':
        columns = []
        longlat = ask[5:].split(',')
        data_nearest = bank.getNearestAgen(Decimal(longlat[0]), Decimal(longlat[1]))
        print data_nearest
        counter = 0
        for data in data_nearest:
            counter += 1
            row = {}
            row['title'] = data[6]
            row['subtitle'] = data[9]
            if (len(row['subtitle']) > 60):
                row['subtitle'] = row['subtitle'][:60] + '...'
            row['image_url'] = gmaps.getImageLocationMap(Decimal(longlat[0]), Decimal(longlat[1]))
            button = []
            fill_button = {}
            fill_button['type'] = "postback"
            fill_button['title'] = "Detail Agen"
            fill_button['payload'] = "evt=detail_lokasi_agen&alamat=" + data[9] + ' , ' + data[11] + ' , ' + data[12] + ' , ' + data[13] + '&telp=' + data[17] + '&nama=' + data[6] + '&jenis=' + data[25]
            button.append(fill_button)
            fill_button1 = {}
            url_view = 'https://www.google.com/maps/search/?api=1&query=' + str(longlat[0]) + ',' + str(longlat[1])
            fill_button1['type'] = "web_url"
            fill_button1['title'] = "View Map"
            fill_button1['url'] = url_view
            button.append(fill_button1)
            row['buttons'] = button
            columns.append(row)
            print columns
        fbmbot.send_generic_message(msisdn, columns)
    else:
        fbmbot.send_text_message(msisdn, ask)



@app.task
def doloadtest():
    print "testloads"
    #onMessage(str("load/%s" % (random.randrange(1, 10000))), "testloads", "testload")
    onMessage(str("load/%s" % (random.randrange(1, 10000))), "galon", "testload")



@app.task(ignore_result=True)
def doworker(req):
    content = json.dumps(req)
    content = json.loads(content)
    print ""
    print "================================NEW FBM REQUEST============================================="
    print content

    if not content.has_key('entry'):
        return
    for key in content["entry"]:
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
        timerespon = ""


        for sub_key in key['messaging']:
            timerespon = sub_key['timestamp']
            recipient = sub_key['recipient']
            page_msisdn = recipient['id']
            sender = sub_key['sender']
            msisdn = sender['id']
            user_profile = fbmbot.get_user_info(msisdn,fields=['first_name'])
            first_name = user_profile['first_name']
            if 'message' in sub_key:
                if 'attachments' in sub_key['message']:
                    for data in sub_key['message']['attachments']:
                        latitude = data['payload']['coordinates']['lat']
                        print latitude
                        longitude = data['payload']['coordinates']['long']
                        print longitude
                        onMessage(msisdn, '[LOC] ' + str(latitude) + ',' + str(longitude), '')
                else:
                    ask = sub_key['message']['text']
                    print ask
                    answer = fbmNlp.doNlp(ask, msisdn, first_name)
                    print answer
                    onMessage(msisdn, answer, first_name)
            elif 'postback' in sub_key:
                parsed = urlparse.urlparse('?' + sub_key['postback']['payload'])
                event = urlparse.parse_qs(parsed.query)['evt'][0]
                print event
                if event == 'lihat_produk':
                    onMessage(msisdn,"info produk",first_name)
                elif event == 'lihat_promo':
                    onMessage(msisdn, 'info promo', first_name)
                elif event == 'lihat_atm':
                    onMessage(msisdn, 'info atm', first_name)
                elif event == 'lihat_cabang':
                    onMessage(msisdn, 'info cabang', first_name)
                elif event == 'lihat_agen':
                    onMessage(msisdn, 'info agen', first_name)
                elif event == 'detail_lokasi_agen':
                    alamat = urlparse.parse_qs(parsed.query)['alamat'][0]
                    telp = urlparse.parse_qs(parsed.query)['telp'][0]
                    nama = urlparse.parse_qs(parsed.query)['nama'][0]
                    jenis = urlparse.parse_qs(parsed.query)['jenis'][0]
                    compose_detail = 'Nama : ' + nama + '\n' + 'Telp : ' + telp + '\n' + 'Alamat : ' + alamat + '\n' + 'Jenis : ' + jenis
                    fbmbot.send_text_message(msisdn, compose_detail)
                    fbmbot.send_button_message(msisdn, "Baik " + first_name + ", apa ada lagi yang dapat Maya bantu?",
                                               template.data_button_greeting)
                elif event == 'info_makanan':
                    onMessage(msisdn, "info makanan", first_name)
                elif event == 'info_gadget':
                    onMessage(msisdn, "info gadget", first_name)
                elif event == 'info_promo':
                    detail_info = urlparse.parse_qs(parsed.query)['detail_info'][0]
                    fbmbot.send_text_message(msisdn, detail_info)
                    fbmbot.send_button_message(msisdn, "Baik " + first_name + ", apa ada lagi yang dapat Maya bantu?",
                                               template.data_button_greeting)
                elif event == 'iya_services':
                    onMessage(msisdn,"[USER_GET_SERVICES]",first_name)
                elif event == 'tidak_services':
                    fbmbot.send_text_message(msisdn,"Baik " + first_name +", apa ada lagi yang dapat Maya bantu?")
                    fbmbot.send_generic_message(msisdn, template.data_template_greeting)
                elif event == 'iya_greeting':
                    fbmbot.send_generic_message(msisdn, template.data_template_greeting)
                elif event == 'tidak_greeting':
                    fbmbot.send_text_message(msisdn, "Baik " + first_name + ", terima kasih")
                elif event == "lihat_simpanan":
                    onMessage(msisdn, "simpanan", first_name)
                elif event == "lihat_kartu_kredit":
                    onMessage(msisdn, "kartu kredit", first_name)
                elif event == "lihat_pinjaman":
                    onMessage(msisdn, "pinjaman", first_name)
            print msisdn








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

