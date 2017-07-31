from rivescript import RiveScript
from gevent import pywsgi
from flask import Flask, render_template, request, redirect
from redis_storage import RedisSessionStorage
import redis

#import logging
import gevent.monkey
gevent.monkey.patch_all()


rs = RiveScript(session_manager=RedisSessionStorage(),)
rs.load_directory("/home/luky/line3v2/rivescript_microsite/")
rs.sort_replies()

redisconn = redis.StrictRedis()

if __name__==  "__main__":
    print "Rivescript is online"

    app = Flask(__name__)

    @app.route('/reply', methods=['POST'])
    def reply():
        content = request.get_json()
        print "reply:", content
        return rs.reply(content['msisdn'], content['ask'])

    print "starting gevent wsgi..."
    pywsgi.WSGIServer(('', 3003), app).serve_forever()