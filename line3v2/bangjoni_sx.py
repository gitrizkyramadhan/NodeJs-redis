from gevent import pywsgi
from flask import Flask, render_template, request, redirect
from fbm_tasksx import doworker
#import logging
import gevent.monkey
gevent.monkey.patch_all()

if __name__==  "__main__":
    print "Line bang joni bot personal assistant is online"

    app = Flask(__name__)

    #import logging
    #log = logging.getLogger('werkzeug')
    #log.setLevel(logging.ERROR)

    #app.logger.setLevel(log.ERROR)	
    #app.debug = True

    @app.route('/celery', methods=['GET'])
    def home():
        print "Hello from Client..."
        return "Hello World!"

    @app.route('/callback_bangjoni', methods=['POST'])
    def bangjoni_fbm():
        content = request.get_json()
        print content
        doworker.delay(content)
        return "OK"

    print "starting gevent wsgi..."
    pywsgi.WSGIServer(('', 8002), app).serve_forever()
