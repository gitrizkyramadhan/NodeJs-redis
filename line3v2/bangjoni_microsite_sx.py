import gevent.monkey
from flask import Flask, request
from flask_cors import CORS, cross_origin

from gevent import pywsgi

from microsite_tasksx import doworker as doworker_microsite

gevent.monkey.patch_all()

if __name__==  "__main__":
    print "Line bang joni bot personal assistant is online"
    app = Flask(__name__)
    CORS(app)
    @app.route('/celery', methods=['GET'])
    def home():
        print "Hello from Client..."
        return "Hello World!"

    @app.route('/microsite', methods=['POST'])
    def bangjoni_line():
        content = request.get_json()
        print content
        doworker_microsite.delay(content)
        return "OK"

    print "starting gevent wsgi..."
    pywsgi.WSGIServer(('', 8003), app).serve_forever()
