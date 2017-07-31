from post_reciever_message import PostReceiverMessage
from dbutils import MysqlDbUtil
import requests
from nlp_rivescript import Nlp
import json
post_receiver = PostReceiverMessage()
mysql = MysqlDbUtil()
nlp = Nlp()

class CekSaldo():

    def do(self, msisdn, ask, answer, first_name, socketid):

        sql = "select A.no_va, coalesce(B.try_pin,0) from user_profile A "  \
              "join user_activity B on A.user_id = B.user_id  "  \
              "where A.user_id ='" + msisdn + "' limit 1"
        print sql
        sqlout = mysql.request(sql)
        print sqlout
        no_va = sqlout[0][0]
        try_pin = sqlout[0][1]
        print sqlout
        if answer[:4] == 'ck00' :
            post_receiver.sendMessageToCather(msisdn, socketid, answer[4:], first_name)
        if answer[:4] == 'ck01' :
            if try_pin <= 3:
                if int(ask) == 1234:
                    url = "http://128.199.169.4:8004/checkAccount"
                    template = {"va": sqlout[0][0]}
                    response = requests.post(url, template)
                    response = response.content
                    print response
                    data = json.loads(response)
                    post_receiver.sendMessageToCather(msisdn, socketid,
                                                      "Sisa saldo UnikQu kamu saat ini sebesar Rp " + data['data'][
                                                          'balance'], first_name)
                    sql = "update from user_activity set try_pin = 0 where user_id = '" + msisdn + "'"
                    print sql
                    mysql.insert(sql)
                    nlp.doNlp('userexittorandom', msisdn, first_name)
                else :
                    post_receiver.sendMessageToCather(msisdn, socketid, "pin kamu salah silahkan masukan lagi",
                                                      first_name)
                    sql = "update from user_activity set try_pin = try_pin + 1 where user_id = '" + msisdn + "'"
                    mysql.insert(sql)
                    nlp.doNlp('usertrypin', msisdn, first_name)


            else :
                post_receiver.sendMessageToCather(msisdn, socketid,
                                                  "pin kamu sudah salah 3x mohon untuk reset di kantor cabanf terdekat",
                                                  first_name)
                nlp.doNlp('userexittorandom', msisdn, first_name)