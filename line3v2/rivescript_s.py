from rivescript import RiveScript
from gevent import pywsgi
from flask import Flask, render_template, request, redirect
from redis_storage import RedisSessionStorage
import redis
import sys
from StringIO import StringIO

from time import sleep
from apscheduler.schedulers.blocking import BlockingScheduler
import thread

from shutil import copyfile
from shutil import move
import os
from datetime import datetime, timedelta
import json

#import logging
import gevent.monkey
gevent.monkey.patch_all()


rs = RiveScript(session_manager=RedisSessionStorage(),)
# rs.load_directory("/home/bambangs/line3/rivescript/")
rs.load_directory("/home/bambangs/line3v2/rivescript/")
rs.sort_replies()

redisconn = redis.StrictRedis()

def reloadRive():
    print "trigger reload"
    dtm = (datetime.now() + timedelta(hours=0)).strftime('%Y%m%d_%H%M%S')
    changeScript = 0

    if (os.path.exists('/home/bambangs/line3/rivescript/edit/reservation.rive.OK')):
        #write new trigger from edit script web
        print "RIVESCRIPT UPDATED"
        move("/home/bambangs/line3/rivescript/reservation.rive", "/home/bambangs/line3/rivescript/reservation.rive.%s" % (dtm))
        copyfile("/home/bambangs/line3/rivescript/edit/reservation.rive.OK", "/home/bambangs/line3/rivescript/reservation.rive")
        #os.remove("/home/bambangs/line3/rivescript/edit/reservation.rive.OK")		
        changeScript = 1

    #write new trigger from chat-agent
    trigger = redisconn.get("trigger")
    if trigger is not None:
        lasttrigger = json.loads(redisconn.get("trigger"))
        if (len(lasttrigger) > 0):
            print "RIVESCRIPT UPDATED FROM CHAT"
            f = open('/home/bambangs/line3/rivescript/reservation.rive')
            text = f.read()
            f.close()
            f = open('/home/bambangs/line3/rivescript/reservation.rive', 'w')
            f.write("/////////////////Add Trigger From Chat at %s ////////////////\n" % (dtm))
            for i in range(len(lasttrigger)):
                f.write(lasttrigger[str(i)])
                f.write("\n\n")
            f.write("////////////////////////////////////////////////////////////////////////////////////////////////////////////////\n\n")
            f.write(text)
            f.close()
            lasttrigger = {}
            redisconn.set("trigger", json.dumps(lasttrigger))
            changeScript = 1
            copyfile("/home/bambangs/line3/rivescript/reservation.rive", "/home/bambangs/line3/rivescript/edit/reservation.rive.OK")

    if  changeScript == 1:
        global rs
        try:
            rs = None
            rs = RiveScript(session_manager=RedisSessionStorage(),)
            rs.load_directory("/home/bambangs/line3/rivescript/")
            rs.sort_replies()
            redisconn.set("rivescript/update", "SUCCED")
        except:
            redisconn.set("rivescript/update", "ERROR")
    else:
        print "RIVESCRIPT UNTOUCHED"
        redisconn.set("rivescript/update", "UNTOUCHED")


def start_scheduler():
    scheduler = BlockingScheduler()
    scheduler.add_job(reloadRive, 'cron', hour=1, minute=1)
    #scheduler.add_job(reloadRive, 'interval', minutes=1)
    scheduler.start()



if __name__==  "__main__":
    print "Rivescript is online"



    app = Flask(__name__)

    @app.route('/reply', methods=['POST'])
    def reply():
        content = request.get_json()
        print "reply:", content
        return rs.reply(content['msisdn'], content['ask'])

    @app.route('/trigger', methods=['POST'])
    def trigger():
        content = request.get_json()
        print "trigger:", content
        rs.stream(content['trigger'])
        rs.sort_replies()

        trigger = redisconn.get("trigger")
        if trigger is not None:
            lasttrigger = json.loads(trigger)
            lasttrigger[len(lasttrigger)] = content['trigger']
            redisconn.set("trigger", json.dumps(lasttrigger))
        else:
            lasttrigger = {}
            lasttrigger[0] = content['trigger']
            redisconn.set("trigger", json.dumps(lasttrigger))
        return "OK"

    @app.route('/getvar', methods=['POST'])
    def getvar():
        content = request.get_json()
        print "getvar:", content
        return rs.get_uservar(content['msisdn'], content['param'])

    @app.route('/setvar', methods=['POST'])
    def setvar():
        content = request.get_json()
        print "setvar:", content
        rs.set_uservar(content['msisdn'], content['param'], content['value'])
        return "OK"

    @app.route('/checkscript', methods=['POST'])
    def checkscript():
        content = request.get_json()
        print "checkscript:", content
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        rss = RiveScript()
        rss.load_file(content['filename'])
        print "OK"
        sys.stdout = old_stdout
        print "----->", mystdout.getvalue()
        rss = None
        return mystdout.getvalue()

    @app.route('/updatescript', methods=['POST'])
    def updatescript():
        content = request.get_json()
        print "updatescript", content
        reloadRive()
        return "OK"

    #thread.start_new_thread(start_scheduler, ())


    print "starting gevent wsgi..."
    pywsgi.WSGIServer(('', 3001), app).serve_forever()