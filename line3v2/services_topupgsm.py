from dbutils import MysqlDbUtil
from post_reciever_message import PostReceiverMessage
import requests
import json

mysql = MysqlDbUtil()
post_receiver = PostReceiverMessage()

class TopUpGsm():

    def do(self,msisdn, answer, first_name, socketid, parameter):


        flag = 1
        handphone = ""
        provider = ""
        amount = ""
        va = ""
        pin = ""
        for data in parameter:
            if data['handphone'] == "" or data['provider'] == "" or data['amount'] == "":
                post_receiver.sendMessageToCather(msisdn, socketid, answer, first_name)
            else:
                query = "select no_va, pin from user_profile where user_id ='" + msisdn + "' limit 1"
                sqlout = mysql.request(query)
                if not sqlout:
                    handphone = data['handphone']
                    provider = data['provider']
                    amount = data['amount']
                    va, pin = sqlout
                    data_request = {"terminal_id":"CHATBOT","nomor_terminal":"00001"}
                    data_request['va'] = va
                    data_request['msisdn'] = handphone
                    data_request['provideId'] = provider
                    data_request['amount'] = amount
                    data_request['pin'] = pin
                    if data_request['pin'] == pin:
                        response = requests.post(url , json.dumps(data_request))
                        response = json.loads(response)
                        post_receiver.sendMessageToCather(msisdn, socketid, response, "")
                    else:

                        post_receiver.sendMessageToCather(msisdn, socketid, "pin anda salah silahkan ulangi lagi", "")







