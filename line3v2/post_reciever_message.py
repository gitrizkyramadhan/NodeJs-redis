import urllib2
import json

class PostReceiverMessage():

    def sendMessageToCather(self, msisdn, socketid, answer, first_name, type="message", data=None):

        data = {
            "msisdn" : msisdn,
            "socketid" : socketid,
            "msg" : answer,
            "first_name" : first_name,
            "type" : type,
            "data" : data
        }
        print "sendMessageToCather"
        req = urllib2.Request("http://128.199.88.72:3000/callback")
        req.add_header('Content-Type', 'application/json')

        response = urllib2.urlopen(req, json.dumps(data))
        print response
        return "OK"