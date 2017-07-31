from microsite_nlp_rivescript import Nlp
from dbutils import MysqlDbUtil
from post_reciever_message import PostReceiverMessage
from dbutils import MysqlDbUtil
import json
import requests
post_receiver = PostReceiverMessage()
mysql = MysqlDbUtil()
nlp = Nlp()

class Pulsa():

    def search_string_match(self, mesg, dict):
        idx = 0
        found = 0
        for item in dict:
            for subitem in item.split('|'):
                if subitem == mesg.lower():
                    found = 1
            if found == 1:
                return idx
            idx += 1
        if found == 1:
            return idx
        else:
            return -1

    def getProvider(self, no_hp):
        prefix_operator = ['0811|0812|0813|0821|0822|0823|0852|0853|0851', '0855|0856|0857|0858|0814|0815|0816',
                           '0817|0818|0819|0859|0877|0878|0838|0831|0832|0833', '0896|0897|0898|0899',
                           '0881|0882|0883|0884|0885|0886|0887|0888|0889']
        idx = self.search_string_match(no_hp[1:4], prefix_operator)
        if idx == 0:
            provider = 'TSEL'
        elif idx == 1:
            provider = 'ISAT'
        elif idx == 2:
            provider = 'XL'
        elif idx == 3:
            provider = 'Three'
        elif idx == 4:
            provider = 'Smartfren'
        else:
            provider = 'Unknown'
        return provider


    def do(self, msisdn, ask, answer, first_name, socketid, data):

        if data:
            sql = "select A.no_va, coalesce(B.try_pin,0), A.pin from user_profile A " \
                  "join user_activity B on A.user_id = B.user_id  " \
                  "where A.user_id ='" + msisdn + "' limit 1"
            print sql
            sqlout = mysql.request(sql)
            url = "http://128.199.169.4:8004/topUPGSM"
            provider = self.getProvider(data['nomortelepon'])
            template = {"va": sqlout[0][0]}
            response = requests.post(url, template)
            response = response.content
            data = {
                       "terminal_id": "CHATBOT",
                       "nomor_terminal": "00001",
                       "va": sqlout[0][0],
                       "msisdn": data['nomortelepon'],
                       "providerId": provider,
                       "amount": data['nominalpulsa'],
                       "pin": '1234'
            }
            print response
            data = json.loads(response)
            post_receiver.sendMessageToCather(msisdn, socketid, data['message'], first_name)
            sql = "insert into transactions " \
                  "(user_id, trx_type , C, D, description, status) " \
                  "values ('"+ msisdn +"','pulsa',0,'" + data['nomortelepon'] + "','transaksi pulsa', 'success')"
            print sql
            mysql.insert(sql)
        else:
            post_receiver.sendMessageToCather(msisdn, socketid, "form pulsa", first_name, type="form")


        # no_hp = ""
        # nominal = ""
        # provider = ""
        # if nlp.redisconn.exists("pulsa/%s" % (msisdn)):
        #     incomingMsisdn = json.loads(nlp.redisconn.get("pulsa/%s" % (msisdn)))
        #     no_hp = incomingMsisdn[0]
        # else:
        #     incomingMsisdn = nlp.create_incoming_msisdn()
        # sql = "select A.no_va, coalesce(B.try_pin,0), A.pin from user_profile A " \
        #       "join user_activity B on A.user_id = B.user_id  " \
        #       "where A.user_id ='" + msisdn + "' limit 1"
        # print sql
        # sqlout = mysql.request(sql)
        # print sqlout
        # no_va = sqlout[0][0]
        # try_pin = sqlout[0][1]
        # pin = sqlout[0][1]
        # if answer[:4] == 'pu00' :
        #     post_receiver.sendMessageToCather(msisdn, socketid, "form pulsa", first_name, type="form")
        # if answer[:4] == 'pu01' : # pin auth
        #     print "pin auth"
        #     # if try_pin <= 3:
        #         if ask == 1234:
        #             post_receiver.sendMessageToCather(msisdn, socketid, "form pulsa", first_name, type="form")
        #         else:
        #             post_receiver.sendMessageToCather(msisdn, socketid, "pin anda salah silahkan ulangi lagi ya :)", "")


        # if answer[:4] == "pu02": # set no_hp
        #     print "set no_hp"
        #     incomingMsisdn[0] = ask
        #     post_receiver.sendMessageToCather(msisdn, socketid, answer[4:], first_name)
        #     json.loads(nlp.redisconn.set("pulsa/%s" % (msisdn), incomingMsisdn))
        # if answer[:4] == "pu03": # set nominal
        #     print "set nominal"
        #     nominal = ask
        #     provider = self.getProvider(no_hp)
        #     post_receiver.sendMessageToCather(msisdn, socketid, answer[4:], first_name)
        #     url = "http://128.199.169.4:8004/topUPGSM"
        #     template = {"va": sqlout[0][0]}
        #     response = requests.post(url, template)
        #     response = response.content
        #     data = {
        #                "terminal_id": "CHATBOT",
        #                "nomor_terminal": "00001",
        #                "va": no_va,
        #                "msisdn": no_hp,
        #                "providerId": provider,
        #                "amount": nominal,
        #                "pin": pin
        #     }
        #     print response
        #     data = json.loads(response)
        #     post_receiver.sendMessageToCather(msisdn, socketid, data['message'], first_name)
        #     sql = "update from user_activity set try_pin = 0 where user_id = '" + msisdn + "'"
        #     print sql
        #     mysql.insert(sql)
        #     nlp.doNlp('userexittorandom', msisdn, first_name)
        #     post_receiver.sendMessageToCather(msisdn, socketid, answer[4:], first_name)


