# coding: utf-8
import json
import os
import random
import string
import sys
from datetime import datetime, timedelta
from microsite_nlp_rivescript import Nlp
from post_reciever_message import PostReceiverMessage

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *
from PyQt4.QtWebKit import *
from celery import Celery

from intent_maper import IntentMaper

maper = IntentMaper()
nlp = Nlp()
post_receiver = PostReceiverMessage()

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

app_gui = init_qtgui()
app = Celery('microsite_tasksx', backend = 'amqp', broker = 'redis://localhost:6379/2')

def genToken(digits):
    return ''.join(random.choice(string.lowercase) for i in range(digits))

@app.task(ignore_result=True)
def doworker(req):
    content = json.dumps(req)
    content = json.loads(content)
    print ""
    print "================================NEW MICROSITE REQUEST============================================="
    print content

    if content.has_key('microsite_catcher'):
        for event in content['microsite_catcher']:
            socketid = event['socket_id']
            msisdn = event['msisdn']
            msg = event['msg']
            token = event['token']
            logDtm = (datetime.now() + timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')
            maper.maper(msisdn, msg, "", socketid)
            # if nlp.redisconn.get("token/%s" % (token)):
            #     print "found key"
            #     incomingMsisdn = json.loads(nlp.redisconn.get("token/%s" % (token)))
            #     last_request = datetime.strptime(incomingMsisdn[12], '%Y-%m-%d %H:%M:%S')
            #     new_request = datetime.strptime(logDtm, '%Y-%m-%d %H:%M:%S')
            #     if (new_request - last_request).total_seconds() > 10:
            #         print "timeoust session"
            #         post_receiver.sendMessageToCather(msisdn,socketid,"tm00","")
            #     else:
            #         print "update session"
            #         incomingMsisdn[12] = logDtm
            #         nlp.redisconn.set("token/%s" % (token), json.dumps(incomingMsisdn))
            #         post_receiver.onMessageTransactional(msisdn, socketid, msg, "")
            # else:
            #     print "create new session"

print "Microsite Worker is online"
