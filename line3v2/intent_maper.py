from services_register import Register
from services_topupgsm import TopUpGsm
from services_nointent import NoIntent
from services_ceksaldo import CekSaldo
from services_pulsa import Pulsa
from rasa_consumer import RasaConsumer
from post_reciever_message import PostReceiverMessage
from microsite_nlp_rivescript  import Nlp
from datetime import datetime, timedelta

nlp = Nlp()
rasa = RasaConsumer()
post_receiver = PostReceiverMessage()
class IntentMaper(object):

    def maper(self, msisdn, ask, first_name, socketid):
        answer = ""
        intent_name = ""
        data = ""
        type = ""
        if not isinstance(ask, list):
            ask = ask.strip()
            nlp.nlpSessionToRandom(msisdn, first_name)
            answer = nlp.doNlp(ask, msisdn, "")
            logDtm = (datetime.now() + timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')
            print "--------------------------------------------------->", logDtm, msisdn, ask
            print "--------------------------------------------------->", logDtm, msisdn, answer
            intent = rasa.query(ask)
            intent = intent['intent']
            confidence = intent['confidence']
            intent_name = intent['name']
            if confidence < 0.3:
                intent_name = ""
        else:
            data = ask[0]
            type = data['type']
        if answer[:4] == "gr01":
            post_receiver.sendMessageToCather(msisdn, socketid, "halo :D", "")
        elif intent_name == "Registrasi UnikQu" or answer[:2] == "rg" or type == "registrasi":
            register = Register()
            register.do(msisdn, ask, answer, first_name, socketid, data)
        elif intent_name == "Cek Saldo UnikQu" or answer[:2] == "ck":
            ceksaldo = CekSaldo()
            ceksaldo.do(msisdn,ask,answer,first_name,socketid)
        elif intent_name == "Pulsa Pre-Paid" or answer[:2] == "pu":
            pulsa = Pulsa()
            pulsa.do(msisdn, ask, answer, first_name, socketid, data)
        else:
            nointent = NoIntent()
            nointent.do(msisdn, ask, answer, first_name, socketid)