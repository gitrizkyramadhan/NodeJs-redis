from user_profiling import UserProfileService
from post_reciever_message import PostReceiverMessage
from microsite_nlp_rivescript import Nlp
from dbutils import MysqlDbUtil
import requests
import json

profiler = UserProfileService()
post_receiver = PostReceiverMessage()
nlp = Nlp()
mysql = MysqlDbUtil()

class Register():

    def do(self, msisdn, ask, answer, first_name, socketid, data):

        url = "http://128.199.169.4:8004/createAccount"
        print "Register"
        # if int(sqlout[0][0]) == 0:
        if answer[:4] == 'rg00':
            post_receiver.sendMessageToCather(msisdn, socketid, answer[4:], first_name)
        elif answer[:4] == 'rg01':
            profiler.update_profile(msisdn, user_id=msisdn)
            profiler.update_profile(msisdn, handphone=ask)
            post_receiver.sendMessageToCather(msisdn, socketid, answer[4:], first_name)
        elif answer[:4] == 'rg02':
            if ask != '1234':
                query = "delete from user_profile where user_id = '" + msisdn + "'"
                mysql.insert(query)
                post_receiver.sendMessageToCather(msisdn, socketid, "maaf kode otp kamu salah", first_name)
                nlp.resetToRandom(msisdn, first_name)
            else:
                # url = "http://128.199.169.4:8004/checkAccount"
                # sql = "select cast(count(1) as char(1)) , handphone, secret_question from user_profile where " \
                #       "handphone = (select handphone from user_profile " \
                #       "where msisdn ='" + msisdn + "' and " \
                #       "coalesce(secret_question,'') != ''  limit 1) " \
                #       "group by handphone , secret_question limit 1"
                # print sql
                # sqlout = mysql.request(sql)
                # template = {"va": "8001" + sqlout[0][1]}
                # response = requests.post(url, template)
                # response = response.content
                # print response
                # data = json.loads(response)
                # post_receiver.sendMessageToCather(msisdn, socketid,
                #                                   "Sisa saldo UnikQu kamu saat ini sebesar Rp " + data['data'][
                #                                       'balance'], first_name)
                # sql = "update from user_activity set try_pin = 0 where user_id = '" + msisdn + "'"
                # print sql
                # mysql.insert(sql)
                # print sqlout[0]
                # if int(data['code']) == 1:
                #     post_receiver.sendMessageToCather(msisdn, socketid, "form registrasi1", first_name, type="form")
                # elif int(sqlout[0][0]) > 1:
                #     data = {
                #         "secret_question" : sqlout[0][2]
                #     }
                #     post_receiver.sendMessageToCather(msisdn, socketid, "form registrasi2", first_name, type="form", data=data)
                # else:
                post_receiver.sendMessageToCather(msisdn, socketid, "form registrasi", first_name, type="form")

        elif data:
            if type == 'registrasi':
                query = "select handphone as phone from user_profile where user_id = '" + msisdn + "' limit 1"
                sqlout = mysql.request(query)
                phone = sqlout[0][0]
                sql = "update user_profile set " \
                      "email = '" + data['email'] + \
                      "', nama_depan = '" + data['namadepan'] + \
                      "', nama_belakang = '" + data['namabelakang'] + \
                      "', secret_question = '" + data['secretquestion'] + \
                      "', answer_question = '" + data['answerquestion'] + \
                      "', pin = '" + data['pin'] + "' where user_id = '" + msisdn + "'"
                print sql
                mysql.insert(sql)
                template = {
                            "terminal_id":"CHATBOT",
                            "nomor_terminal":"00001",
                            "jenis_identitas":"3",
                            "no_hp": phone,
                            "nama_depan": data['namadepan'],
                            "cbsva":"1111111",
                            "tgllahir":"",
                            "namaibu":"",
                            "tempat_lahir": "",
                            "email":data['email'],
                            "nama_belakang": data['namabelakang']
                          }
                response = requests.post(url, template)
                response = response.content
                print response
                content = json.loads(response)
                post_receiver.sendMessageToCather(msisdn, socketid, content['message'], first_name)

        # elif answer[:4] == "rg03":
        #     profiler.update_profile(msisdn, email=ask)
        #     post_receiver.sendMessageToCather(msisdn, socketid, answer[4:], first_name)
        # elif answer[:4] == "rg04":
        #     profiler.update_profile(msisdn, nama_depan=ask)
        #     post_receiver.sendMessageToCather(msisdn, socketid, answer[4:], first_name)
        # elif answer[:4] == "rg05":
        #     profiler.update_profile(msisdn, nama_belakang=ask)
        #     post_receiver.sendMessageToCather(msisdn, socketid, answer[4:], first_name)
        # elif answer[:4] == "rg06":
        #     profiler.update_profile(msisdn, secret_question=ask)
        #     post_receiver.sendMessageToCather(msisdn, socketid, answer[4:], first_name)
        # elif answer[:4] == "rg07":
        #     profiler.update_profile(msisdn, secret_answer=ask)
        #     post_receiver.sendMessageToCather(msisdn, socketid, answer[4:], first_name)
        # elif answer[:4] == "rg08":
        #     profiler.update_profile(msisdn, pin=ask)
        #     post_receiver.sendMessageToCather(msisdn, socketid, answer[4:], first_name)
        # else:
        #     post_receiver.sendMessageToCather(msisdn, socketid, "Akun UnikQu kamu sudah terdaftar :)", first_name)
            # for data in parameter:
            #     if sqlout:
            #         if data['phone'] != "":
            #             print 'hit backend otp'
            #             profiler.update_profile(msisdn, handphone=data['value'])
            #         elif data['nama_depan'] == "":
            #             profiler.update_profile(msisdn, nama_depan=data['value'])
            #         elif data['nama_belakang'] == "":
            #             profiler.update_profile(msisdn, nama_belakang=data['value'])
            #         elif data['email'] == "":
            #             profiler.update_profile(msisdn, email=data['value'])
            #         elif data['secret_question'] == "":
            #             profiler.update_profile(msisdn, secret_question=data['value'])
            #         elif data['secret_pass'] == "":
            #             profiler.update_profile(msisdn, secret_pass=data['value'])
            #         elif data['pin'] == "":
            #             profiler.update_profile(msisdn, pin=data['value'])

