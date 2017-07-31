# coding: utf-8
from celery import Celery
from decimal import Decimal
from nlp_rivescript import Nlp
from module_banking import BankingModule
from datetime import datetime, timedelta
import MySQLdb
import json
import os
import sys
import urlparse

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *
from gmaps_geolocation import GMapsGeocoding
from rasa_consumer import RasaConsumer
from log_mongo import MongoLog


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
        qtargs2.append('-style')
        qtargs2.append(style)

    qtargs2.extend(qtargs or [])
    return QApplication(qtargs2)

fbmbot = Bot("EAAUSZCuERiN4BAIYS7EtOXnnh4k8BC7EJZATEeFQHdOHOujY7g8pbgFZAL5EAiw2plGA5maNACEzX5ZAa0OwuBMq7ZCFog5S9UqbFbzynba7ZBZCBzqOeSMgsrY2AP6X9mRsxiB9ZBVZCVD75d0lIvERh0XMak0t6gUuZCGawc6Yc5nQZDZD")
fbmNlp = Nlp()
app_gui = init_qtgui()
bank = BankingModule()
gmaps = GMapsGeocoding()
template = Template()
rasa = RasaConsumer(confident_level=0.3, host='128.199.169.4', port='5000', ssl=False)
app = Celery('fbm_tasksx', backend = 'amqp', broker = 'redis://localhost:6379/0')
rasa = RasaConsumer()
mongo = MongoLog()

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
    fbmNlp.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))
    answer = fbmNlp.doNlp(ask, msisdn, first_name)
    if ask[:5] == '[LOC]':
        intent_name = ""
        confidence = 1.0
    else :
        intent = rasa.query(ask)
        confidence = intent['intent']['confidence']
        intent_name = intent['intent']['name']
        intent_log = intent_name
        if confidence < 0.3 :
            intent_name = ""

    print ask
    print incomingMsisdn

    if answer[:4] == "gr01" or intent_name == "Default Welcome Intent":
        fbmbot.send_text_message(msisdn, 'Selamat datang '+ first_name +', saya Maya, asisten pribadi Anda untuk chat banking dari BNI. Ada yang bisa saya bantu?')
        fbmbot.send_generic_message(msisdn, template.data_template_greeting)
    elif answer == "info promo" or intent_name == "promo lainnya" or intent_name == "promo hotel":
        fbmbot.send_generic_message(msisdn, template.data_template_promo)
    elif answer == "info produk":
        fbmbot.send_generic_message(msisdn, template.data_template_produk)
    elif answer == "info atm" or intent_name == " lokasi atm":
        # fbmbot.send_text_message(msisdn, 'Silakan gunakan fitur share location untuk melakukan pencarian ATM BNI terdekat dari lokasi Anda')
        fbmbot.send_quick_replies_messages(msisdn, 'Silakan gunakan fitur share location untuk melakukan pencarian ATM BNI terdekat dari lokasi Anda', [{"content_type":"location"}])
        if (new_request - last_request).total_seconds() > 1800:  # reset request after half an hour
            incomingMsisdn = create_incoming_msisdn()
        incomingMsisdn[11] = 'share_loc_atm'
        fbmNlp.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))
    elif answer == "info makanan" or intent_name == "promo makanan":
        fbmbot.send_generic_message(msisdn, template.data_template_promo_makanan)
        fbmbot.send_button_message(msisdn, "Baik " + first_name + ", apa ada lagi yang dapat Maya bantu?",
                                   template.data_button_greeting)
    elif answer == "info gadget" or intent_name == "promo gadget":
        fbmbot.send_generic_message(msisdn, template.data_template_promo_gadget)
        fbmbot.send_button_message(msisdn, "Baik " + first_name + ", apa ada lagi yang dapat Maya bantu?",
                                   template.data_button_greeting)
    elif answer == "simpanan" or intent_name == "simpanan":
        fbmbot.send_image_url(msisdn, 'https://bangjoni.com/images/bni/Mengapa-BNI-Taplus.jpg')
        fbmbot.send_image_url(msisdn, 'https://bangjoni.com/images/bni/Suku-Bunga-BNI-Taplus.jpg')
        fbmbot.send_button_message(msisdn, "Baik " + first_name + ", apa ada lagi yang dapat Maya bantu?",
                                   template.data_button_greeting)
    elif answer == "kartu kredit" or intent_name == "kartu kredit":
        fbmbot.send_image_url(msisdn, 'https://bangjoni.com/images/bni/Kartu-Kredit-BNI.jpg')
        fbmbot.send_button_message(msisdn, "Baik " + first_name + ", apa ada lagi yang dapat Maya bantu?",
                                   template.data_button_greeting)
    elif answer == "pinjaman" or intent_name == "pinjaman":
        fbmbot.send_image_url(msisdn, 'https://bangjoni.com/images/bni/Pinjaman-BNI.jpg')
        fbmbot.send_button_message(msisdn, "Baik " + first_name + ", apa ada lagi yang dapat Maya bantu?",
                                   template.data_button_greeting)
    elif answer == "info cabang" or intent_name == "lokasi cabang":
        # fbmbot.send_text_message(msisdn, 'Silakan gunakan fitur share location untuk melakukan pencarian kantor cabang BNI terdekat dari lokasi Anda')
        fbmbot.send_quick_replies_messages(msisdn, 'Silakan gunakan fitur share location untuk melakukan pencarian kantor cabang BNI terdekat dari lokasi Anda',[{"content_type": "location"}])
        if (new_request - last_request).total_seconds() > 1800:  # reset request after half an hour
            incomingMsisdn = create_incoming_msisdn()
        incomingMsisdn[11] = 'share_loc_branch'
        fbmNlp.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))
    elif answer == "info agen" or intent_name == "lokasi agen46":
        # fbmbot.send_text_message(msisdn, 'Silakan gunakan fitur share location untuk melakukan pencarian agen46 BNI terdekat dari lokasi Anda')
        fbmbot.send_quick_replies_messages(msisdn, 'Silakan gunakan fitur share location untuk melakukan pencarian agen46 BNI terdekat dari lokasi Anda',[{"content_type": "location"}])
        if (new_request - last_request).total_seconds() > 1800:  # reset request after half an hour
            incomingMsisdn = create_incoming_msisdn()
        incomingMsisdn[11] = 'share_loc_agen'
        fbmNlp.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))
    elif answer[:4] == "nh01":
        fbmbot.send_text_message(msisdn,"Terima	kasih, data Anda sudah saya	catat dan petugas BNI akan segera menghubungi Anda untuk proses selanjutnya. Apa ada lagi yang dapat Maya bantu?")
        fbmbot.send_generic_message(msisdn, template.data_template_greeting)
    elif answer[:19] == "[USER_GET_SERVICES]":
        fbmbot.send_text_message(msisdn,"Silakan ketik Nama	Lengkap	beserta	Nomor HP Anda (contoh: Kenzie Abinaya 08123456789)")
        if (new_request - last_request).total_seconds() > 1800:  # reset request after half an hour
            incomingMsisdn = create_incoming_msisdn()
        incomingMsisdn[29] = 'nama_handphone'
        fbmNlp.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))
    elif answer[:4] == "rg00" or intent_name == "Registrasi UnikQu":
        print "register uniqku"
        fbmbot.send_generic_message(msisdn, [
        {
            "title": "REGISTER",
            "image_url": "https://bangjoni.com/images/bni/BNI-Carousel-Menu_Promo.jpg",
            "buttons": [
                {
                    "type": "web_url",
                    "title": "REGISTER",
                    "url": "https://bangjoni.com/chat?msisdn=" + msisdn + "&service=createAccount&key=xcnhkcdmkicgkrzb",
                    "webview_height_ratio": "compact"
                }
            ]
        }
    ])
    elif answer[:4] == 'ck00' or intent_name == "Cek Saldo UnikQu":
        print "cek saldo"
        fbmbot.send_generic_message(msisdn, [
        {
            "title": "CEK SALDO",
            "image_url": "https://bangjoni.com/images/bni/BNI-Carousel-Menu_Promo.jpg",
            "buttons": [
                {
                    "type": "web_url",
                    "title": "CEK SALDO",
                    "url": "https://bangjoni.com/chat?msisdn=" + msisdn + "&service=checkAccount&key=xcnhkcdmkicgkrzb",
                    "webview_height_ratio": "compact"
                }
            ]
        }
    ])
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
        fbmbot.send_text_message(msisdn, answer)
    mongo.conversations('facebook', msisdn, ask, answer, intent_log, confidence)




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
                    onMessage(msisdn, ask.lower(), first_name)
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
                elif event == 'detail_lokasi':
                    alamat = urlparse.parse_qs(parsed.query)['alamat'][0]
                    fbmbot.send_text_message(msisdn, alamat)
                    fbmbot.send_button_message(msisdn, "Baik " + first_name + ", apa ada lagi yang dapat Maya bantu?",
                                               template.data_button_greeting)
                elif event == 'detail_lokasi_atm':
                    alamat = urlparse.parse_qs(parsed.query)['alamat'][0]
                    jenis = urlparse.parse_qs(parsed.query)['jenis'][0]
                    jenis = "Rp." + jenis + ".000"
                    compose_detail = "alamat : " + alamat + "\n" + "jenis pecahan: " + jenis
                    fbmbot.send_text_message(msisdn, compose_detail)
                    fbmbot.send_button_message(msisdn, "Baik " + first_name + ", apa ada lagi yang dapat Maya bantu?",
                                               template.data_button_greeting)
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
                    print detail_info
                    fbmbot.send_text_message(msisdn, detail_info)
                    fbmbot.send_button_message(msisdn, "Baik " + first_name + ", apa ada lagi yang dapat Maya bantu?",
                                               template.data_button_greeting)
                elif event == 'iya_services':
                    onMessage(msisdn,"[USER_GET_SERVICES]",first_name)
                elif event == 'tidak_services':
                    fbmbot.send_text_message(msisdn,"Baik " + first_name +", apa ada lagi yang dapat Maya bantu?")
                    fbmbot.send_generic_message(msisdn, template.data_template_greeting)
                elif event == 'iya_greting':
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
print "fbm bot personal assistant is online"


