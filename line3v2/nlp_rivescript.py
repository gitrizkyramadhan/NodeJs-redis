from datetime import datetime, timedelta
import re
import json
from nltk.util import ngrams
import redis
import requests


class Nlp:
    def __init__(self):

        self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        self.redisconn = redis.StrictRedis()
        self.email_notification = 'a2c6dfee7e69677cc7c9@cloudmailin.net'

    def reply(self, msisdn, mesg):
        params = {'msisdn': msisdn, 'ask': mesg}
        resp = requests.post('http://localhost:3002/reply', data=json.dumps(params), headers=self.headers)
        return resp.text

    def updateNlp(self, rule):
        print "added rule: ", rule
        params = {'trigger': rule}
        resp = requests.post('http://localhost:3002/trigger', data=json.dumps(params), headers=self.headers)
        print "RICESCRIPT RULE ADDED BY AGENT"

    def set_uservar(self, msisdn, param, value):
        params = {'msisdn': msisdn, 'param': param, 'value': value}
        resp = requests.post('http://localhost:3002/setvar', data=json.dumps(params), headers=self.headers)

    def get_uservar(self, msisdn, param):
        params = {'msisdn': msisdn, 'param': param}
        resp = requests.post('http://localhost:3002/getvar', data=json.dumps(params), headers=self.headers)
        return resp.text


    def doNlp(self, mesg, msisdn, first_name):
        answer = self.reply(msisdn, mesg)
        if answer.find("<first_name>") > -1:
            answer = answer.replace("<first_name>",first_name)
        # print answer

        # incomingMsisdn = json.loads(self.redisconn.get("inc/%s" % (msisdn)))
        # try:
        #     bookingMsisdn = json.loads(self.redisconn.get("book/%s" % (msisdn)))
        # except:
        #     bookingMsisdn = {}
        #
        # print "NLP:", incomingMsisdn
        # #print "------->>", bookingMsisdn
        # self.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))
        # self.redisconn.set("book/%s" % (msisdn), json.dumps(bookingMsisdn))
        #s = json.loads(self.redisconn.get("book/%s" % (msisdn)))
        #print "------------->>", bookingMsisdn, s
        print self.get_uservar(msisdn, 'topic')
        return answer.strip()

    def create_incoming_msisdn(self):

        logDtm = (datetime.now() + timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')
        incomingMsisdn = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, logDtm, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1,
                          -1, -1, 0, "2017", "", [], 'no topic']
        return incomingMsisdn

    def resetToRandom(self , msisdn , first_name):

        incomingMsisdn = self.create_incoming_msisdn()
        answer = self.doNlp("userexittorandom", msisdn, first_name)
        self.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))

    def nlpSessionToRandom(self, msisdn, first_name):

        logDtm = (datetime.now() + timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')
        if self.redisconn.exists("inc/%s" % (msisdn)):
            incomingMsisdn = json.loads(self.redisconn.get("inc/%s" % (msisdn)))
            last_request = datetime.strptime(incomingMsisdn[12], '%Y-%m-%d %H:%M:%S')
            new_request = datetime.strptime(logDtm, '%Y-%m-%d %H:%M:%S')
            if (new_request - last_request).total_seconds() > 300:  # reset request after half an hour
                incomingMsisdn = self.create_incoming_msisdn()
                answer = self.doNlp("userexittorandom", msisdn, first_name)
        else:
            incomingMsisdn = self.create_incoming_msisdn()
