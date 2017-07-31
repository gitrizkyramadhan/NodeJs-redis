from gevent import pywsgi
from flask import Flask, request
from fbm_tasksx import doworker
#import logging
import gevent.monkey
import json
gevent.monkey.patch_all()


if __name__==  "__main__":
    print "Uniqu services is online"

    app = Flask(__name__)

    @app.route('/createAccount', methods=['POST'])
    def createAccunt():
        content = request.get_json()
        print content
        if content['terminal_id'] != "":
            result = {
              "code": 1,
              "message": "Terimakasih account VA anda telah aktif, Maks : Rp. 1.000.000, no. acc:8001081290351111. PIN anda adalah 006365. Silakan cash in di agen terdekat.",
              "data": {
                "emoney_va": "8001081290351111",
                "no_identitas": "",
                "nama_depan": "ica",
                "nama_belakang": "husnul",
                "no_hp": "081290351111",
                "email": "ica@gmail.com",
                "tanggal_lahir": "01061992",
                "balance": "0",
                "rekening_pooling": "115208477"
            }
        }
        else:
            result = {
                "code": -1,
                "message": "Account terdaftar silahkan menggunakan identitas lain atau lakukan reset password",
                "data": "-"
            }
        return json.dumps(result)

    @app.route('/checkAccount', methods=['POST'])
    def checkAccunt():
        # content = request.get_json()
        # print content
        # if content['emoney_va'] != "":
        result =  {
          "code": "1",
          "message": "Data ditemukan",
          "data": {
            "emoney_va": "8001081290354777",
            "no_identitas": "2541365214789456",
            "nama_depan": "ahy'a",
            "nama_belakang": "mukhlis",
            "nama_lengkap": "ahy'a mukhlis",
            "no_hp": "081290354777",
            "msisdn": "081290354777",
            "email": "ahya0348@gmail.com",
            "tanggal_lahir": "03111995",
            "balance": "218059",
            "nama_ibu": "di'na",
            "tempat_lahir": "jakarta",
            "jenis_identitas": "4",
            "keterangan_identitas": "HP",
            "tipe_nasabah": "REGISTER",
            "status_aktif": "1",
            "rekening_pooling": "115208477"
            }
        }
        # else :
        #     result = {
        #         "code": "-1",
        #         "message": "Nomor Virtual Account tidak ditemukan.",
        #         "data": ""}
        return json.dumps(result)

    @app.route('/getOtp', methods=['POST'])
    def getOtp():

        return '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soapenc="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><soapenv:Header/><soapenv:Body><otp:requestResponse xmlns:otp="http://service.bni.co.id/otp"><otpResponse><otpResult>12345</otpResult></otpResponse></otp:requestResponse></soapenv:Body></soapenv:Envelope>'

    @app.route('/topUPGSM', methods=['POST'])
    def topUpGsm():

        content = request.get_json()
        print content
        if content['va']:
            result = {"code": "1","coreJournal": "713789","reffNum": "0000250000000101","message": "Anda berhasil melakukan top up AS - 081290354777 Rp. 25000 pada 24 October 2016, 16:38:45","sql": {
    "code": "1","message": "Proses cashOut berhasil","data": {"emoney_va": "8001081290354777","no_identitas": "2541365214789456","nama_depan": "Ahya","nama_belakang": "Mukhlis","nama_lengkap": "Ahya Mukhlis","no_hp": "081290354777","msisdn": "081290354777",
    "email": "ahyaica@gmail.com","tanggal_lahir": "03111995","balance": "3860309","nama_ibu": "di'na","tempat_lahir": "jakarta","jenis_identitas": "4",
    "keterangan_identitas": "HP","tipe_nasabah": "REGISTER","status_aktif": "1","rekening_pooling": "115208477"}}}
        else :
            result = {"code": "-1","ori_message": "Pastikan nomor yang Anda input benar","message": "GAGALAS14 : Transaksi gagal dilakukan",
    "sql": {"code": "1","message": "Proses cashOut berhasil","data": {"emoney_va": "8001081290354777",
    "no_identitas": "2541365214789456","nama_depan": "Ahya","nama_belakang": "Mukhlis","nama_lengkap": "Ahya Mukhlis",
    "no_hp": "081290354777","msisdn": "081290354777","email": "ahyaIca@gmail.com","tanggal_lahir": "03111995","balance": "2846809",
    "nama_ibu": "di'na","tempat_lahir": "jakarta","jenis_identitas": "4","keterangan_identitas": "HP","tipe_nasabah": "REGISTER",
    "status_aktif": "1","rekening_pooling": "115208477"
    },
    "sql": ""}}
        return json.dumps(result)

    print "starting gevent wsgi..."
    pywsgi.WSGIServer(('', 8004), app).serve_forever()

