import re
from datetime import datetime, timedelta
import json
from rivescript import RiveScript
import sqlite3 as lite
import urllib

import Levenshtein
from nltk.util import ngrams

import csv

from redis_storage import RedisSessionStorage
import redis

class Nlp:
   def __init__(self):
   
      #self.rs = RiveScript(session_manager=RedisSessionStorage(),)
      #self.rs.load_directory("/home/bambangs/line3/rivescript/")
      #self.rs.sort_replies()	  
   
      self.city = []
      self.airportcode = []
      with open('bandara.json') as data_file:    
         data = json.load(data_file)
      for item in data["all_airport"]["airport"]:
         self.city.append(item["location_name"].lower())
         self.airportcode.append(item["airport_code"])   
      self.airlinecode = ['CITILINK','LION','GARUDA','SRIWIJAYA','AIRASIA','BATIK']
      self.airlinecode_rive = ['citilink','lion|lion air|lionair','garuda','sriwijaya','airasia|air asia','batik|batik air|batikair']
      self.timepart = ['pagi','siang','sore','malam']
      self.when = ['hari ini|hr ini|siang ini|malam ini|pagi ini|sore ini','besok|bsok|bsk','lusa','januari|jan','februari|feb','maret|mar','april|apr','mei','juni|jun','juli|jul','agustus|aug|agus','september|sept|sep','oktober|okt','november|nov|nop','desember|des']
      self.pool_xtrans = ['bale xtrans','bandara soeta(cgk)','batang','bekasi','bintaro','blok m','bsd','bsm','btp','cibubur','de batara','green batara','jatingaleh','jatiwaringin','jogja','jombor','karawaci','kelapa gading','kendal','laweyan','mtc','oncom raos','pabelan','pancoran','pasteur','pekalongan','pondok indah','pt inti','semanggi/kc','semarang','solo','tembalang','tomang','blora','pekalogan']
      

      #[cmd,service,2015-10-10,CGK,DPS,date,yes,no,GARUDA,adult,child,infant,logDtm,token,block reply,phase,with_paspor,with_baggage,flight_number,airlines_name,departure_time,CGK_str,DPS_str,pagi,langsung,reset/termurah,tahun]
	  
      self.redisconn = redis.StrictRedis()
      
      #self.incomingMsisdn = {}
      
      #self.bookingMsisdn = {}
      self.email_notification = 'a2c6dfee7e69677cc7c9@cloudmailin.net'

      #add train module
      self.city_train = []
      self.traincode = []
      with open('train_station.json') as data_file:    
         data = json.load(data_file)
      for item in data["stations"]["station"]:
         self.city_train.append(item["station_name"].strip().lower())
         self.traincode.append(item["station_code"])       

      self.cuisines_name = ['aceh','asian','bakmi','bakso','betawi','bubble','burger','chinese','coffee','dimsum','indonesian','japanese','jawa','makassar','manado','medan','padang','pizza','ramen','satay','soto','steakhouse','sunda','sushi','american','arabian','australian','bakery','balinese','bangka','batak','belanda','beverages','british','cafe','caribbean','continental','deli','desserts','drinks','european','fast','finger','french','german','greek','grill','healthy','ice','indian','irish','italian','juices','kalimantan','kebab','korean','lebanese','lombok','malaysian','mediterranean','mexican','middle','mongolian','north','pakistani','palembang','peranakan','portuguese','seafood','singaporean','south','spanish','street','sulawesi','sumatera','taiwanese','tex-mex','thai','turkish','vietnamese','western','yogyakarta'] 
      self.cuisines_id = ['237','3','261','249','239','247','168','25','161','781','114','60','240','242','243','244','235','82','320','312','260','141','234','177','1','4','131','5','236','238','255','250','270','133','30','158','35','192','100','268','38','40','271','45','134','156','181','143','233','148','135','55','164','241','178','67','66','251','69','70','73','137','74','50','139','245','118','87','83','119','85','89','90','259','246','190','150','95','142','99','248','253']

      self.kota_sholat = []
      self.kota_sholat_id = []
      self.kota_sholat_gmt = []
      with open('kota_sholat.csv', 'rb') as f:
         reader = csv.reader(f)
         for row in reader:
             self.kota_sholat.append(row[1].lower())
             self.kota_sholat_id.append(row[0].lower())
             self.kota_sholat_gmt.append(row[3])

	  
      self.prefix_operator = ['0811|0812|0813|0821|0822|0823|0852|0853|0851','0855|0856|0857|0858|0814|0815|0816','0817|0818|0819|0859|0877|0878|0838|0831|0832|0833','0896|0897|0898|0899','0881|0882|0883|0884|0885|0886|0887|0888|0889']
      self.markup_operator = ['500|550|500|550|500|500','525|525|99|500|500|500','550|550|99|500|500|500','587|575|500|537|575|0','500|575|500|500|500|500']

   def reply(self, msisdn, mesg):
      params = {'msisdn': msisdn, 'ask': mesg}
      resp = requests.post('http://localhost:3001/reply', data=params)	
      return resp.text	  
	  
	  
   def updateNlp(self, rule):
      print "added rule: ", rule
      params = {'trigger': rule}
      resp = requests.post('http://localhost:3001/trigger', data=params)	
      print "RICESCRIPT RULE ADDED BY AGENT"
	  
   def set_uservar(self, msisdn, param, value):
      params = {'msisdn': msisdn, 'param': param, 'value': value}
      resp = requests.post('http://localhost:3001/setvar', data=params)	

   def get_uservar(self, msisdn, param):
      params = {'msisdn': msisdn, 'param': param}
      resp = requests.post('http://localhost:3001/getvar', data=params)	
      return resp.text	 	  


   def search_string(self, mesg, dict):  
      idx = 0
      found = 0
      for item in dict:
         for subitem in item.split('|'):
            if subitem in mesg.lower():
               found = 1
         if found == 1:
           return idx
         idx += 1
      if found == 1:
         return idx
      else:
         return -1      

 
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

         
   def doNlp(self, mesg, msisdn, first_name):
      answer = self.rs.reply(msisdn, mesg)
      if answer.find("<first_name>") > -1:
           answer = answer.replace("<first_name>",first_name)
      #print answer

      incomingMsisdn = json.loads(self.redisconn.get("inc/%s" % (msisdn)))
      try:
          bookingMsisdn = json.loads(self.redisconn.get("book/%s" % (msisdn)))
      except:
          bookingMsisdn = {}
      #add token
      if answer[:4] == "pl01" :
         incomingMsisdn[1] = self.rs.get_uservar(msisdn,"id_pln")	  
		 
      if answer[:4] == "pl02" :
         x = self.rs.get_uservar(msisdn,"nominal_token")	
         if x == "dua puluh":
             incomingMsisdn[2] = "20000"
         elif x == "lima puluh":
             incomingMsisdn[2] = "50000"		 
         elif x == "seratus":
             incomingMsisdn[2] = "100000"		 
         elif x == "dua ratus":
             incomingMsisdn[2] = "200000"		 
         elif x == "lima ratus":
             incomingMsisdn[2] = "500000"		 
         elif x == "sejuta":
             incomingMsisdn[2] = "1000000"		 
         elif x == "lima juta":
             incomingMsisdn[2] = "5000000"		 			 
         elif x == "sepuluh juta":
             incomingMsisdn[2] = "10000000"		
         else:			 
             incomingMsisdn[2] = "50000000"				 

      if answer[:4] == "pl03" or answer[:4] == "pu03":
         x = self.rs.get_uservar(msisdn,"carabayar_token")			
         if x == "atm":
             incomingMsisdn[3] = "1|5"
         elif x == "mandiri ecash":
             incomingMsisdn[3] = "2"		 
         elif x == "kartu kredit":
             incomingMsisdn[3] = "1|7"		 
         elif x == "doku wallet":
             incomingMsisdn[3] = "1|4"		 
         else:
             incomingMsisdn[3] = "1|6"			 
		 
      #add pulsa
      if answer[:4] == "pu01" :
         incomingMsisdn[1] = self.rs.get_uservar(msisdn,"no_hp")	 
         idx = self.search_string_match(incomingMsisdn[1][:4], self.prefix_operator) 
         if idx == 0:
             incomingMsisdn[2] = 'Telkomsel'
             incomingMsisdn[4] = 'TSEL'			 
         elif idx == 1:			 
             incomingMsisdn[2] = 'Indosat'	  
             incomingMsisdn[4] = 'ISAT'			 
         elif idx == 2:			 
             incomingMsisdn[2] = 'XL'
             incomingMsisdn[4] = 'XL/Axis'			 
         elif idx == 3:			 
             incomingMsisdn[2] = 'Three'
             incomingMsisdn[4] = 'Three'				 
         elif idx == 4:			 
             incomingMsisdn[2] = 'Smartfren'
             incomingMsisdn[4] = 'Smartfren'			 
         else:			 
             incomingMsisdn[2] = 'Unknown'			 
         incomingMsisdn[3] = self.markup_operator[idx]

      if answer[:4] == "pu02" :
         x = self.rs.get_uservar(msisdn,"nominal_token")
         if x == "lima ribu":
             incomingMsisdn[5] = "1|" + incomingMsisdn[4] + " 5.000|5000"
         elif x == "sepuluh ribu":
             incomingMsisdn[5] = "1|" + incomingMsisdn[4] + " 10.000|10000"
         elif x == "dua puluh ribu":
             incomingMsisdn[5] = "1|" + incomingMsisdn[4] + " 20.000|20000"
         elif x == "dua puluh lima ribu":
             incomingMsisdn[5] = "1|" + incomingMsisdn[4] + " 25.000|25000"
         elif x == "lima puluh ribu":
             incomingMsisdn[5] = "1|" + incomingMsisdn[4] + " 50.000|50000"
         elif x == "seratus ribu":
             incomingMsisdn[5] = "1|" + incomingMsisdn[4] + " 100.000|100000"

		 
      #add translator
      if answer[:4] == "tr01" :
         incomingMsisdn[2] = self.rs.get_uservar(msisdn,"translate_lang")	  
	  
      #add info tol jasa marga module (jagorawi|cikampek|tangerang|joor|palikanci|purbaleunyi|cipali|dalkot|dalam kota)
      if answer[:4] == "to01" or answer[:4] == "xx01":
         tol_cabang = self.rs.get_uservar(msisdn,"tol_name")
         incomingMsisdn[2] = tol_cabang
      '''   
      if tol_cabang == "jagorawi":
             incomingMsisdn[3] = "1"
         elif tol_cabang == "cikampek":
             incomingMsisdn[3] = "2"
         elif tol_cabang == "tangerang":
             incomingMsisdn[3] = "3"
         elif tol_cabang == "dalkot":
             incomingMsisdn[3] = "4"
         elif tol_cabang == "dalam kota":
             incomingMsisdn[3] = "4"
         elif tol_cabang == "purbaleunyi":
             incomingMsisdn[3] = "5"
         elif tol_cabang == "cipularang":
             incomingMsisdn[3] = "5"
         elif tol_cabang == "purbalenyi":
             incomingMsisdn[3] = "5"
         elif tol_cabang == "joor":
             incomingMsisdn[3] = "11"
         elif tol_cabang == "palikanci":
             incomingMsisdn[3] = "12"
         else:
             incomingMsisdn[3] = "0"
      '''
	  
      #add reminder module
      if answer[:4] == "sc01" :
         incomingMsisdn[2] = self.rs.get_uservar(msisdn,"sholat_kota")
         idx = self.search_string(self.rs.get_uservar(msisdn,"sholat_kota"), self.kota_sholat)
         if idx > -1:
             incomingMsisdn[3] = self.kota_sholat_gmt[idx]
             incomingMsisdn[4] = self.kota_sholat_id[idx]
			 
      #add reminder sholat module
      if answer[:4] == "rs01":
         idx = self.search_string(self.rs.get_uservar(msisdn,"sholat_kota"), self.kota_sholat)
         if idx > -1:
             incomingMsisdn[4] = self.kota_sholat_id[idx]
             incomingMsisdn[3] = self.rs.get_uservar(msisdn,"sholat_kota") 
             incomingMsisdn[5] = self.kota_sholat_gmt[idx]
			 
	  
      #add reminder module
      if answer[:4] == "re01" or answer[:4] == "re02":
         incomingMsisdn[7] = self.rs.get_uservar(msisdn,"sholat_kota")
         idx = self.search_string(self.rs.get_uservar(msisdn,"sholat_kota"), self.kota_sholat)
         if idx > -1:
             incomingMsisdn[8] = self.kota_sholat_gmt[idx]
         incomingMsisdn[2] = "None"		 
         incomingMsisdn[3] = "None"		 
         incomingMsisdn[4] = "None"		 
         incomingMsisdn[5] = "None"	 
         mesg = mesg + " "
         incomingMsisdn[6] = mesg
		 
         p = re.compile("(hr ini|hari ini|besok|bsok|lusa)|([0-9]{1,2}(\s|-)*(jan|feb|mar|apr|mei|juni|juli|aug|sept|okt|nov|dec|januari|februari|maret|april|mei|juni|juli|agustus|september|oktober|november|desember)((\s|-)*[0-9]{2,4})?)|((tgl|tanggal)(\s)*[0-9]{1,2}(\s)+)")
         for m in p.finditer(mesg):
             incomingMsisdn[6] = incomingMsisdn[6].replace(m.group(),"")
             idx = self.search_string(m.group(), self.when)
             print "------------->", idx
             if idx == 0:
                 incomingMsisdn[2] = (datetime.now() + timedelta(hours=7)).strftime('%Y-%m-%d')
             elif idx == 1:
                 incomingMsisdn[2] = (datetime.now() + timedelta(hours=(7+24))).strftime('%Y-%m-%d')
             elif idx == 2:
                 incomingMsisdn[2] = (datetime.now() + timedelta(hours=(7+48))).strftime('%Y-%m-%d')
             elif idx in range(3,15):
                 str_date = re.findall(r'\d+',m.group())
                 if len(str_date) == 1:
                     incomingMsisdn[2] = "%04s-" % (incomingMsisdn[26]) + "%02d" % (idx - 2) + "-" + str_date[0].zfill(2)
                 else:
                     incomingMsisdn[2] = "%04s-" % (str_date[1]) + "%02d" % (idx - 2) + "-" + str_date[0].zfill(2)	
             else:
                 str_date = re.findall(r'\d+',m.group())         
                 incomingMsisdn[2] = "2016-01-%02d" % (int(str_date[0]))				 

         p = re.compile("(jam(\s)*[0-9]{1,2}(\s)+([0-9]{1,2})?)|(jam(\s)*[0-9]{1,2}.[0-9]{1,2}(\s)+)")
         for m in p.finditer(mesg):
             incomingMsisdn[6] = incomingMsisdn[6].replace(m.group(),"")
             str_date = re.findall(r'\d+',m.group())
             if len(str_date) == 1:
                 incomingMsisdn[3] = "%02d:00:00" % (int(str_date[0]))
             else:
                 incomingMsisdn[3] = "%02d:%02d:00" % (int(str_date[0]), int(str_date[1]))
			 
         p = re.compile("(senin|selasa|rabu|kamis|jumat|sabtu|minggu)")
         for m in p.finditer(mesg):
             incomingMsisdn[6] = incomingMsisdn[6].replace(m.group(),"")
             if m.group() == "senin":
                 incomingMsisdn[4] = "Monday"
             elif m.group() == "selasa":
                 incomingMsisdn[4] = "Tuesday"
             elif m.group() == "rabu":
                 incomingMsisdn[4] = "Wednesday"
             elif m.group() == "kamis":
                 incomingMsisdn[4] = "Thursday"
             elif m.group() == "jumat":
                 incomingMsisdn[4] = "Friday"
             elif m.group() == "sabtu":
                 incomingMsisdn[4] = "Saturday"
             elif m.group() == "minggu":
                 incomingMsisdn[4] = "Sunday"				 
				 
				 
         p = re.compile("tiap")
         for m in p.finditer(mesg):
             incomingMsisdn[6] = incomingMsisdn[6].replace(m.group(),"")
             incomingMsisdn[5] = m.group()    

         incomingMsisdn[6] = re.sub(r'\W+',' ',incomingMsisdn[6])		 
         incomingMsisdn[6] = incomingMsisdn[6].replace("ingetin ","")
         incomingMsisdn[6] = incomingMsisdn[6].replace("reminder ","")
         incomingMsisdn[6] = incomingMsisdn[6].replace("bangunin ","")
         print "RECOG: ", incomingMsisdn[2], incomingMsisdn[3], incomingMsisdn[4], incomingMsisdn[5], incomingMsisdn[6]
	  
	  
      #add euro2016 module
      if answer[:4] == "eu02":
         incomingMsisdn[3] = self.rs.get_uservar(msisdn,"europlayer")
      if answer[:4] == "eu03":
         incomingMsisdn[3] = self.rs.get_uservar(msisdn,"euroday")

      #add waktu sholat module
      if answer[:4] == "sh01":
         idx = self.search_string(self.rs.get_uservar(msisdn,"sholat_kota"), self.kota_sholat)
         if idx > -1:
             incomingMsisdn[4] = self.kota_sholat_id[idx]	  
             incomingMsisdn[3] = self.rs.get_uservar(msisdn,"sholat_kota")	
         print ">>>>>>>", incomingMsisdn[3], idx, self.rs.get_uservar(msisdn,"sholat_kota")
	  
      #add zomato module
      if answer[:4] == "zo01":
         incomingMsisdn[3] = self.rs.get_uservar(msisdn,"zomato_cuisine")
         incomingMsisdn[4] = self.rs.get_uservar(msisdn,"zomato_location")
      if answer[:4] == "zo02":
         idx = self.search_string(self.rs.get_uservar(msisdn,"zomato_cuisine"), self.cuisines_name)
         if idx > -1:
             incomingMsisdn[4] = self.cuisines_id[idx]

      #add xtrans module
      if answer[:4] == "xt02":
         xtrans_pool = self.rs.get_uservar(msisdn,"xtrans_pool")
         if xtrans_pool == "pt inti":
             xtrans_pool = "pt.inti"
         if xtrans_pool == "bandara soetacgk":
             xtrans_pool = "bandara soeta(cgk)"
         incomingMsisdn[3] = xtrans_pool

      if answer[:4] == "xt03":
         #mapping jumlah penumpang
         incomingMsisdn[1] = int(re.findall(r'\d+',self.rs.get_uservar(msisdn,"xtrans_dewasa"))[0])

         #mapping departure date    
         idx = self.search_string(self.rs.get_uservar(msisdn,"xtrans_derpature_date"), self.when)
         if idx == 0:
             incomingMsisdn[2] = (datetime.now() + timedelta(hours=7)).strftime('%Y-%m-%d')
         elif idx == 1:
             incomingMsisdn[2] = (datetime.now() + timedelta(hours=(7+24))).strftime('%Y-%m-%d')
         elif idx == 2:
             incomingMsisdn[2] = (datetime.now() + timedelta(hours=(7+48))).strftime('%Y-%m-%d')
         elif idx in range(3,15):
             str_date = re.findall(r'\d+',self.rs.get_uservar(msisdn,"xtrans_derpature_date"))
             if len(str_date) == 1:
                 incomingMsisdn[2] = "%04s-" % (incomingMsisdn[26]) + "%02d" % (idx - 2) + "-" + str_date[0].zfill(2)
             else:
                 incomingMsisdn[2] = "%04s-" % (str_date[1]) + "%02d" % (idx - 2) + "-" + str_date[0].zfill(2)

      if answer[:4] == "xt04":
         xtrans_pilih_no = self.rs.get_uservar(msisdn,"xtrans_pilih_no")         
         isnumeric = re.findall(r'\d+',xtrans_pilih_no)
         incomingMsisdn[10] = isnumeric[0]
 
      if answer[:4] == "xt05":
          data_penumpang = mesg.lower().replace("\n",",")
          if incomingMsisdn[1] == 1:             
              incomingMsisdn[9] = data_penumpang
              self.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))
              return "xt06 Oke, semua data lengkap. Berikut denah kursinya, sebut 1 nomor kursi untuk Bang Joni booking.\n"
          else:
              if (len(data_penumpang.split(","))) == incomingMsisdn[1]:
                  incomingMsisdn[9] = data_penumpang
                  print "---->", incomingMsisdn[9]
                  self.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))				  
                  return "xt06 Oke, semua data lengkap. Berikut denah kursinya, sebut %s nomor kursi untuk Bang Joni booking.\nGunakan koma untuk memisah nomor kursi (Contoh: 2,3)" % (incomingMsisdn[1])
              else:
                  self.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))              			  
                  return "Ada format data yang tidak sesuai, tolong perbaiki..."

      if answer[:4] == "xt07":
         #xtrans_seat = self.rs.get_uservar(msisdn,"xtrans_seat")         
         isnumeric = re.findall(r'\d+', mesg.lower().replace("\n",";"))
         if len(isnumeric) == incomingMsisdn[1]:
             incomingMsisdn[3] = mesg.lower().replace("\n",";")
             print "---->", incomingMsisdn[3]
             self.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))			 
             return "xt07 OK, sebelum Bang Joni booking, berapa no HP kamu buat xtrans hubungi?"			 
         else:
             self.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))		 
             return "Jumlah kursi harus sesuai dengan jumlan penumpang, tolong diperbaiki..."


      if answer[:4] == "xt08":
         xtrans_hp = self.rs.get_uservar(msisdn,"xtrans_hp") 
         print "HP:",xtrans_hp
         if xtrans_hp[:1] == "8":
             xtrans_hp = "0" + xtrans_hp
         print "HP:",xtrans_hp
         incomingMsisdn[7] = xtrans_hp
         self.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))		 
         return "xt08 Okay. Semua data sudah benar dan lengkap, pilih metode pembayaran berikut:"
			 
      if answer[:4] == "xt09":
         xtrans_payment = self.rs.get_uservar(msisdn,"xtrans_payment") 
         if xtrans_payment == "atm":
             incomingMsisdn[5] = "fin195"
             incomingMsisdn[8] = "ATM"			 
         elif xtrans_payment == "mandiri ecash": 			 
             incomingMsisdn[5] = "MeM"
             incomingMsisdn[8] = "Mandiri eCash"				 
         elif xtrans_payment == "bca klikpay": 			 
             incomingMsisdn[5] = "405"
             incomingMsisdn[8] = "BCA Klikpay"				 
         elif xtrans_payment == "kartu kredit": 			 
             incomingMsisdn[5] = "veritrans"
             incomingMsisdn[8] = "Kartu Kredit"				 
         elif xtrans_payment == "tcash": 			 
             incomingMsisdn[5] = "301"
             incomingMsisdn[8] = "TCash"				 
         elif xtrans_payment == "cimb clicks": 			 
             incomingMsisdn[5] = "niaga"	
             incomingMsisdn[8] = "Cimb Clicks"				 
         elif xtrans_payment == "mandiri clickPay": 			 
             incomingMsisdn[5] = "406"
             incomingMsisdn[8] = "Mandiri ClickPay"				 
         elif xtrans_payment == "indomaret": 			 
             incomingMsisdn[5] = "indomaret"
             incomingMsisdn[8] = "Indomaret"				 
         elif xtrans_payment == "xl tunai": 			 
             incomingMsisdn[5] = "303"	
             incomingMsisdn[8] = "XL Tunai"				 
         self.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))			 
         return "xt09 OK, Bang Joni booking ke xtrans sekarang, tungggu maksimal 5 menit..."		 
      #End xtrans module


      #add train module
      if answer[:4] == "ke01":
         psw_derpature_city = self.rs.get_uservar(msisdn,"psw_derpature_city")
         psw_arrival_city = self.rs.get_uservar(msisdn,"psw_arrival_city")
         psw_derpature_date = self.rs.get_uservar(msisdn,"psw_derpature_date")
         psw_dewasa = self.rs.get_uservar(msisdn,"psw_dewasa")
         psw_bayi = self.rs.get_uservar(msisdn,"psw_bayi")
         psw_class = self.rs.get_uservar(msisdn,"psw_class")

         print ">>>>>>dep:", self.rs.get_uservar(msisdn,"psw_derpature_city")
         print ">>>>>>arr:", self.rs.get_uservar(msisdn,"psw_arrival_city")
         print ">>>>>>date:", self.rs.get_uservar(msisdn,"psw_derpature_date")
         print ">>>>>>dewasa:", self.rs.get_uservar(msisdn,"psw_dewasa")
         print ">>>>>>bayi:", self.rs.get_uservar(msisdn,"psw_bayi") 
         print ">>>>>>class:", self.rs.get_uservar(msisdn,"psw_class")  

         #mapping city name to city code
         idx = self.search_string(psw_derpature_city, self.city_train)
         if idx > -1:
             incomingMsisdn[3] = self.traincode[idx]
         idx = self.search_string(psw_arrival_city, self.city_train)
         if idx > -1:
             incomingMsisdn[4] = self.traincode[idx]   
         #get numbers of passengers
         incomingMsisdn[9] = 0
         incomingMsisdn[10] = 0
         incomingMsisdn[11] = 0         
         if psw_dewasa != "undefined": incomingMsisdn[9] = int(re.findall(r'\d+',psw_dewasa)[0])         
         if psw_bayi != "undefined": incomingMsisdn[10] = int(re.findall(r'\d+',psw_bayi)[0])
         #mapping departure date    
         idx = self.search_string(psw_derpature_date, self.when)
         if idx == 0:
             incomingMsisdn[2] = (datetime.now() + timedelta(hours=7)).strftime('%Y-%m-%d')
         elif idx == 1:
             incomingMsisdn[2] = (datetime.now() + timedelta(hours=(7+24))).strftime('%Y-%m-%d')
         elif idx == 2:
             incomingMsisdn[2] = (datetime.now() + timedelta(hours=(7+48))).strftime('%Y-%m-%d')
         elif idx in range(3,15):
             str_date = re.findall(r'\d+',psw_derpature_date)
             if len(str_date) == 1:
                 incomingMsisdn[2] = "%04s-" % (incomingMsisdn[26]) + "%02d" % (idx - 2) + "-" + str_date[0].zfill(2)
             else:
                 incomingMsisdn[2] = "%04s-" % (str_date[1]) + "%02d" % (idx - 2) + "-" + str_date[0].zfill(2)

         print ">>:", incomingMsisdn[3], incomingMsisdn[4], incomingMsisdn[9], incomingMsisdn[10], incomingMsisdn[2]

      if answer[:4] == "ke02":         
         kereta_user_choose = self.rs.get_uservar(msisdn,"kereta_user_choose")         
         isnumeric = re.findall(r'\d+',kereta_user_choose)
         print "      psw_derpature_time:", kereta_user_choose, isnumeric[0] 
         bookingMsisdn = {}
         bookingMsisdn['train_id'] = isnumeric[0]



      if answer[:4] == "ke03":
         res = "ok"
         data_penumpang = mesg.lower().replace("\n",";").split(';')
         print ">>", data_penumpang
         s = ""         
         for item in data_penumpang:
             if item != "":
                s = s + item.strip() + ";"
         print s
         data_penumpang = s.split(';')
         if incomingMsisdn[9] > 0 and incomingMsisdn[10] == 0: #only adult
             idx = 0
             for adult in range(incomingMsisdn[9]): 
                bookingMsisdn['salutationAdult'+`adult+1`] = self.convertTitle(data_penumpang[idx])
                bookingMsisdn['nameAdult'+`adult+1`] = urllib.quote_plus(data_penumpang[idx + 1])
                bookingMsisdn['IdCardAdult'+`adult+1`] = data_penumpang[idx + 2]
                idx = idx + 3
         
         print "---**************1>", bookingMsisdn
         bookingMsisdn['conSalutation'] = bookingMsisdn['salutationAdult1']
         bookingMsisdn['conFirstName'] = bookingMsisdn['nameAdult1']
         bookingMsisdn['conPhone'] = urllib.quote_plus("+628119772759")
         bookingMsisdn['conEmailAddress'] = urllib.quote_plus(self.email_notification)
         bookingMsisdn['adult'] = str(incomingMsisdn[9])
         bookingMsisdn['infant'] = str(incomingMsisdn[10])
 
         print "---**************1>", bookingMsisdn
         self.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))		 
         return "ke04 Sip. Semua data sudah benar dan lengkap. Bang Joni booking sekarang, tunggu ya maksimal 5 menit..."    
      #End train module
  
  
      if answer[:4] == "fl01":
         psw_derpature_city = self.rs.get_uservar(msisdn,"psw_derpature_city")
         psw_arrival_city = self.rs.get_uservar(msisdn,"psw_arrival_city")
         psw_derpature_date = self.rs.get_uservar(msisdn,"psw_derpature_date")
         psw_dewasa = self.rs.get_uservar(msisdn,"psw_dewasa")
         psw_anak = self.rs.get_uservar(msisdn,"psw_anak")
         psw_bayi = self.rs.get_uservar(msisdn,"psw_bayi")
         psw_maskapai = self.rs.get_uservar(msisdn,"psw_maskapai")
         psw_derpature_time = self.rs.get_uservar(msisdn,"psw_derpature_time")   

         #print ">>>>>>dewasa:", self.rs.get_uservar(msisdn,"psw_dewasa")
         #print ">>>>>>anak:", self.rs.get_uservar(msisdn,"psw_anak")
         #print ">>>>>>bayi:", self.rs.get_uservar(msisdn,"psw_bayi")

         #mapping city name to city code
         idx = self.search_string(psw_derpature_city, self.city)
         if idx > -1:
             incomingMsisdn[3] = self.airportcode[idx]
         idx = self.search_string(psw_arrival_city, self.city)
         if idx > -1:
             incomingMsisdn[4] = self.airportcode[idx]   
         #get numbers of passengers
         incomingMsisdn[9] = 0
         incomingMsisdn[10] = 0
         incomingMsisdn[11] = 0         
         if psw_dewasa != "undefined": incomingMsisdn[9] = int(re.findall(r'\d+',psw_dewasa)[0])         
         if psw_anak != "undefined": incomingMsisdn[10] = int(re.findall(r'\d+',psw_anak)[0])
         if psw_bayi != "undefined": incomingMsisdn[11] = int(re.findall(r'\d+',psw_bayi)[0])
         #mapping maskapai
         incomingMsisdn[8] = 'ALL'
         idx = self.search_string(psw_maskapai, self.airlinecode_rive)
         if idx > -1:
             incomingMsisdn[8] = self.airlinecode[idx]         
         #mapping departure time part
         incomingMsisdn[23] = '-1'
         idx = self.search_string(psw_derpature_time, self.timepart)
         if idx > -1:
             incomingMsisdn[23] = idx
         #mapping departure date    
         idx = self.search_string(psw_derpature_date, self.when)
         if idx == 0:
             incomingMsisdn[2] = (datetime.now() + timedelta(hours=7)).strftime('%Y-%m-%d')
         elif idx == 1:
             incomingMsisdn[2] = (datetime.now() + timedelta(hours=(7+24))).strftime('%Y-%m-%d')
         elif idx == 2:
             incomingMsisdn[2] = (datetime.now() + timedelta(hours=(7+48))).strftime('%Y-%m-%d')
         elif idx in range(3,15):
             str_date = re.findall(r'\d+',psw_derpature_date)
             if len(str_date) == 1:
                 incomingMsisdn[2] = "%04s-" % (incomingMsisdn[26]) + "%02d" % (idx - 2) + "-" + str_date[0].zfill(2)
             else:
                 incomingMsisdn[2] = "%04s-" % (str_date[1]) + "%02d" % (idx - 2) + "-" + str_date[0].zfill(2)
                 
         #print "      psw_derpature_city:", self.rs.get_uservar(msisdn,"psw_derpature_city"), incomingMsisdn[3]
         #print "      psw_arrival_city:", self.rs.get_uservar(msisdn,"psw_arrival_city"), incomingMsisdn[4]
         #print "      psw_derpature_date:", self.rs.get_uservar(msisdn,"psw_derpature_date"), incomingMsisdn[2]
         #print "      psw_dewasa:", self.rs.get_uservar(msisdn,"psw_dewasa"), incomingMsisdn[9]
         #print "      psw_anak:", self.rs.get_uservar(msisdn,"psw_anak"), incomingMsisdn[10]
         #print "      psw_bayi:", self.rs.get_uservar(msisdn,"psw_bayi"), incomingMsisdn[11]
         #print "      psw_maskapai:", self.rs.get_uservar(msisdn,"psw_maskapai"), incomingMsisdn[8]
         #print "      psw_derpature_time:", self.rs.get_uservar(msisdn,"psw_derpature_time"), incomingMsisdn[23]

      if answer[:4] == "fl02":         
         psw_user_choose = self.rs.get_uservar(msisdn,"psw_user_choose")         
         isnumeric = re.findall(r'\d+',psw_user_choose)
         print "      psw_derpature_time:", psw_user_choose, isnumeric[0] 
         bookingMsisdn = {}
         bookingMsisdn['flight_id'] = isnumeric[0]

      if answer[:4] == "fl03":
         res = "ok"
         data_penumpang = mesg.lower().replace("\n",";").split(';')
         print ">>", data_penumpang
         s = ""         
         for item in data_penumpang:
             if item != "":
                s = s + item.strip() + ";"
         print s
         data_penumpang = s.split(';')         
         if incomingMsisdn[10] == 0 and incomingMsisdn[11] == 0: #only adult
             idx = 0
             child = 0
             infant = 0
             try:
                for adult in range(incomingMsisdn[9]): 
                   bookingMsisdn['titlea'+`adult+1`] = self.convertTitle(data_penumpang[idx])
                   bookingMsisdn['firstnamea'+`adult+1`] = urllib.quote_plus(data_penumpang[idx + 1])
                   bookingMsisdn['birthdatea'+`adult+1`] = self.convertDate(data_penumpang[idx + 2])
                   bookingMsisdn['passportnationalitya'+`adult+1`] = "id"
                   if incomingMsisdn[16] == -1 and incomingMsisdn[17] == -1:
                        idx = idx + 3
                   if incomingMsisdn[16] == 1 and incomingMsisdn[17] == -1:
                         bookingMsisdn['passportnoa'+`adult+1`] = data_penumpang[idx + 3]
                         bookingMsisdn['passportissuinga'+`adult+1`] = data_penumpang[idx + 4]
                         bookingMsisdn['passportissueddatea'+`adult+1`] = self.convertDate(data_penumpang[idx + 5])
                         bookingMsisdn['passportExpiryDatea'+`adult+1`] = self.convertDate(data_penumpang[idx + 6])
                         idx = idx + 7
                   if incomingMsisdn[16] == -1 and incomingMsisdn[17] == 1:    
                         bookingMsisdn['dcheckinbaggagea1'+`adult+1`] = data_penumpang[idx + 3]
                         idx = idx + 4
                   if incomingMsisdn[16] == 1 and incomingMsisdn[17] == 1:
                         bookingMsisdn['passportnoa'+`adult+1`] = data_penumpang[idx + 3]
                         bookingMsisdn['passportissuinga'+`adult+1`] = data_penumpang[idx + 4]
                         bookingMsisdn['passportissueddatea'+`adult+1`] = self.convertDate(data_penumpang[idx + 5])
                         bookingMsisdn['passportExpiryDatea'+`adult+1`] = self.convertDate(data_penumpang[idx + 6])
                         bookingMsisdn['dcheckinbaggagea1'+`adult+1`] = data_penumpang[idx + 7]
                         idx = idx + 8
                   print bookingMsisdn
                adult += 1         
             except:
                res = "Ada format data yg salah, tolong diisi ulang.."
                self.rs.set_uservar(msisdn,"flight_passenger","0")
                self.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))				
                return res

         if incomingMsisdn[10] > 0 or incomingMsisdn[11] > 0:  #with child or infant            
             idx = 0
             if incomingMsisdn[16] == -1 and incomingMsisdn[17] == -1:
                   incr = 4
             if incomingMsisdn[16] == 1 and incomingMsisdn[17] == -1:
                   incr = 8
             if incomingMsisdn[16] == -1 and incomingMsisdn[17] == 1:
                   incr = 5
             if incomingMsisdn[16] == 1 and incomingMsisdn[17] == 1:
                   incr = 9
             adult = 0
             child = 0
             infant = 0
             #print "?", data_penumpang, len(data_penumpang)
             while idx < len(data_penumpang):
                try: 
                   if data_penumpang[idx] == "d": 
                         tag = "a"
                         adult = adult + 1
                         tag2 = adult
                   if data_penumpang[idx] == "a": 
                         tag = "c"
                         child = child + 1
                         tag2 = child
                   if data_penumpang[idx] == "b": 
                         tag = "i"
                         infant = infant + 1
                         tag2 = infant
                   bookingMsisdn['title'+tag+`tag2`] = self.convertTitle(data_penumpang[idx+1])
                   bookingMsisdn['firstname'+tag+`tag2`] = urllib.quote_plus(data_penumpang[idx + 2])
                   bookingMsisdn['birthdate'+tag+`tag2`] = self.convertDate(data_penumpang[idx + 3])
                   bookingMsisdn['passportnationality'+tag+`tag2`] = "id"                
                   if incomingMsisdn[16] == 1 and incomingMsisdn[17] == -1:
                         bookingMsisdn['passportno'+tag+`tag2`] = data_penumpang[idx + 4]
                         bookingMsisdn['passportissuing'+tag+`tag2`] = data_penumpang[idx + 5]
                         bookingMsisdn['passportissueddate'+tag+`tag2`] = self.convertDate(data_penumpang[idx + 6])
                         bookingMsisdn['passportExpiryDate'+tag+`tag2`] = self.convertDate(data_penumpang[idx + 7])
                   if incomingMsisdn[16] == -1 and incomingMsisdn[17] == 1:    
                         bookingMsisdn['dcheckinbaggage'+tag+'1'+`tag2`] = data_penumpang[idx + 4]
                   if incomingMsisdn[16] == 1 and incomingMsisdn[17] == 1:
                         bookingMsisdn['passportno'+tag+`tag2`] = data_penumpang[idx + 4]
                         bookingMsisdn['passportissuing'+tag+`tag2`] = data_penumpang[idx + 5]
                         bookingMsisdn['passportissueddate'+tag+`tag2`] = self.convertDate(data_penumpang[idx + 6])
                         bookingMsisdn['passportExpiryDate'+tag+`tag2`] = self.convertDate(data_penumpang[idx + 7])
                         bookingMsisdn['dcheckinbaggage'+tag+'1'+`tag2`] = data_penumpang[idx + 8]
                   #print "--->", bookingMsisdn, idx
                   idx = idx + incr
                   #print "?", idx
                except:
                   break
                    
         try:    
            bookingMsisdn['conSalutation'] = bookingMsisdn['titlea1']
            bookingMsisdn['conFirstName'] = bookingMsisdn['firstnamea1']
            #bookingMsisdn['conPhone'] = urllib.quote_plus("+" + msisdn)
            bookingMsisdn['conPhone'] = urllib.quote_plus("+628119772759")
            bookingMsisdn['conEmailAddress'] = urllib.quote_plus(self.email_notification)
            bookingMsisdn['adult'] = str(incomingMsisdn[9])
            bookingMsisdn['child'] = str(incomingMsisdn[10])
            bookingMsisdn['infant'] = str(incomingMsisdn[11])
            if incomingMsisdn[11] > 0:
                if incomingMsisdn[9] < incomingMsisdn[11]:
                    res = "Jumlah bayi melebihi jumlah penumpang dewasa, tolong diisi ulang.."
                    self.rs.set_uservar(msisdn,"flight_passenger","0")
                    self.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))					
                    return res
                else:
                    for i in range(incomingMsisdn[11]):
                        bookingMsisdn['parenti'+`i+1`] = str(i+1)


            print "---**************1>", bookingMsisdn
         except:
            print "something anomaly.." 
            res = "Ada format data yg salah, tolong diisi ulang.."
            self.rs.set_uservar(msisdn,"flight_passenger","0")
            self.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))			
            return res
         
         #checking form anomaly
         for key in bookingMsisdn:
            if key.find("conSalutation") != -1 or key.find("title") != -1:
                if bookingMsisdn[key] == "error": 
                    res = "Title tdk sesuai format, tolong diulang.."
                    break
            if key.find("birthdate") != -1 or key.find("passportissueddate") != -1 or key.find("passportExpiryDate") != -1:
                if self.checkDate(bookingMsisdn[key]) == 1:
                    res = "Tanggal tidak sesuai format, tolong diulang.."
                    break
            if key.find("conFirstName") != -1 or key.find("firstname") != -1:
                if self.checkAlpha(bookingMsisdn[key]) == 1:
                    res = "Nama harus alfabet, tolong diulang.."
                    break
            if key.find("dcheckinbaggage") != -1:
                if bookingMsisdn[key].isdigit() == False:
                    res = "Bagasi harus angka, tolong diulang.."
                    break
            if key.find("passportno") != -1:
                if bookingMsisdn[key].isalnum() == False:
                    res = "Paspor harus alfanumeric, tolong diulang.."
                    break
            if key.find("passportissuing") != -1:
                if bookingMsisdn[key].isalpha() == False:
                    res = "Negara penerbit paspor harus alfabet, tolong diulang.."
                    break
                elif bookingMsisdn[key].lower() != "indonesia":
                    res = "Untuk sementara hanya kewarganegaraan Indonesia."
                    break
                else:
                    bookingMsisdn[key] = "id"
            
         if res != "ok":
            self.rs.set_uservar(msisdn,"flight_passenger","0")
            self.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))			
            return res
         elif adult != incomingMsisdn[9] or child != incomingMsisdn[10] or infant != incomingMsisdn[11]:
            self.rs.set_uservar(msisdn,"flight_passenger","0")
            self.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))			
            return "Jumlah penumpang tidak sesuai dg pesanan, tolong diisi ulang"
         elif res != "ok":
            self.rs.set_uservar(msisdn,"flight_passenger","0")
            self.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))			
            return res
         else:
            print "---**************2>", bookingMsisdn
            self.rs.set_uservar(msisdn,"flight_passenger","1")
            self.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))	
            self.redisconn.set("book/%s" % (msisdn), json.dumps(bookingMsisdn))				
            return "fl04 Sip. Semua data sudah benar dan lengkap, sekarang Bang Joni minta no Hp kamu buat maskapai kasih info penerbanganmu?" 

      if answer[:4] == "fl05":
         flight_hp = self.rs.get_uservar(msisdn,"flight_hp") 
         print "HP:",flight_hp
         if flight_hp[:1] == "8":
             flight_hp = "+62" + flight_hp
         elif flight_hp[:1] == "0":
             flight_hp = "+62" + flight_hp[1:]
         elif flight_hp[:2] == "62":
             flight_hp = "+" + flight_hp[1:]
         print "HP:",flight_hp
         bookingMsisdn['conPhone'] = urllib.quote_plus(flight_hp)
         self.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))		 
         self.redisconn.set("book/%s" % (msisdn), json.dumps(bookingMsisdn))	
         return "fl05 Okay, sebelum Bang Joni booking, pilih pembayaran berikut:"

      if answer[:4] == "fl06":
         flight_payment = self.rs.get_uservar(msisdn,"flight_payment") 
         if flight_payment == "atm":
             incomingMsisdn[16] = "ATM Transfer"	 
         elif flight_payment == "kartu kredit": 			 
             incomingMsisdn[16] = "Credit Card"		 
         elif flight_payment == "bca klikpay": 			 
             incomingMsisdn[16] = "BCA KlikPay"
         elif flight_payment == "mandiri clickpay": 			 
             incomingMsisdn[16] = "Mandiri Clickpay"		 
         elif flight_payment == "cimb clicks": 			 
             incomingMsisdn[16] = "CIMB Clicks"
         
         self.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))
         return "fl06 OK, Bang Joni booking sekarang, tungggu maksimal 5 menit..."	

      #print "NLP:", incomingMsisdn
      #print "------->>", bookingMsisdn
      self.redisconn.set("inc/%s" % (msisdn), json.dumps(incomingMsisdn))         
      self.redisconn.set("book/%s" % (msisdn), json.dumps(bookingMsisdn))	
      #s = json.loads(self.redisconn.get("book/%s" % (msisdn)))			  
      #print "------------->>", bookingMsisdn, s

      print self.get_uservar()
      return answer
      
               
 
      
   def convertTitle(self, msg):
         if msg == "tn":
              return "Mr"
         elif msg == "ny":
              return "Mrs"
         elif msg == "nona":
              return "Ms"
         else:
              return "error"

   def validate(self, mesg, dict):  
      idx = 0
      found = 0
      for item in dict:
         for subitem in item.split('|'):
            if subitem in mesg.lower():
               found = 1
         if found == 1:
           return idx
         idx += 1
      if found == 1:
         return idx
      else:
         return -1
         
   def validate_num(self, mesg, dict, item_idx):
     idx = 0
     loc_key = -1
     for item in dict:
        if idx == item_idx or item_idx == -1:
           for subitem in item.split('|'):
             loc_key = mesg.find(subitem)
             if loc_key > -1:
                break
           if loc_key > -1:
             break  
        idx += 1    
     if loc_key > -1:
        x = re.split(r'[-;,\s]\s*',mesg[:loc_key].rstrip(' -'))[-1]
        if x.isdigit():
           return x
     return -1
              
   def validate_num_last(self, mesg, dict, item_idx):
     idx = 0
     loc_key = -1
     for item in dict:
        if idx == item_idx or item_idx == -1:
           for subitem in item.split('|'):
             loc_key = mesg.find(subitem)
             if loc_key > -1:
                break
           if loc_key > -1:
             break  
        idx += 1    
     if loc_key > -1:
        #x = re.split(r'[-;,\s]\s*',mesg[:loc_key].rstrip(' -'))[-1]
        x = mesg[loc_key+len(subitem):]
        if x:
           return x
     return -1              
              
   def convertDate(self, msg):
      mmsg = msg.replace(" ","").replace("-","")       
      mth = self.validate(mmsg,self.when)
      if mth != -1:
         dt = self.validate_num(mmsg,self.when,-1)
         yr = self.validate_num_last(mmsg,self.when,-1) 
         return yr + "-%02d-" % (mth - 2) + dt.zfill(2)                     
      else:
         return "x"                   
         
   def checkDate(self, msg):
      res = 0
      if len(msg) != 10:
         res = 1
      else:
         j = 0
         for item in msg.split('-'):
            j += 1
            if item.isdigit() == False: res = 1
         if j != 3: res = 1
      return res
      
   def checkAlpha(self, msg):
      res = 0
      for item in msg.split('+'):
         if item.isalpha() == False: res = 1
      return res                 

   def spell_correctness(self, ask):
    fuzzy_str = {}
    fuzzy_ratio = {}
    new_ask = {}
    fuzzy_str2 = {}
    fuzzy_ratio2 = {}
    new_ask2 = {}   

    i = 0
    for word in ask.split(' '):
        ratio = 0
        for pool in self.pool_xtrans:
            
            if pool.find(word) != -1 and len(word) > 3:
                x = 0.71
            else:
                x = Levenshtein.ratio(word, pool)
                
            if ratio < x:
                ratio = x
                fuzzy_str[i] = pool
                fuzzy_ratio[i] = x
        new_ask[i] = word
        if fuzzy_ratio[i] > 0.7:
            new_ask[i] = fuzzy_str[i]

        i = i + 1                
    #print "     answer", fuzzy_str
    #print "     ratio", fuzzy_ratio
    #print "     new ask", new_ask
    
    #print "-------------------------------"
    
    #try using bigrams
    bigram = ngrams(ask.split(), 2)
    fuzzy_str2 = {}
    fuzzy_ratio2 = {}
    new_ask2 = {}
    i = 0
    for grams in bigram:
        token = ' '.join(grams)
        
        ratio = 0
        for pool in self.pool_xtrans:
            x = Levenshtein.ratio(token, pool)
            if ratio < x:
                ratio = x
                fuzzy_str2[i] = pool
                fuzzy_ratio2[i] = x 
        new_ask2[i] = token
        if fuzzy_ratio2[i] > 0.7:
            new_ask2[i] = fuzzy_str2[i]
           
        i = i + 1
    #print "     answer", fuzzy_str2
    #print "     ratio", fuzzy_ratio2
    #print "     new ask", new_ask2    
  
    j = 0
    i = 0
    ask_correction = {}
    ask_array = ask.split(' ')
    words_count = len(ask.split(' '))
    while (i < words_count):
        if i < (words_count -1):
            if fuzzy_ratio[i] <= 0.7 and fuzzy_ratio2[i] <= 0.7:
                ask_correction[j] = ask_array[i]
            elif fuzzy_ratio[i] <= 0.7 and fuzzy_ratio2[i] > 0.7:
                ask_correction[j] = fuzzy_str2[i]
                i = i + 1                
            elif fuzzy_ratio[i] > 0.7 and fuzzy_ratio2[i] <= 0.7:
                ask_correction[j] = fuzzy_str[i]
            elif fuzzy_ratio[i] > 0.7 and fuzzy_ratio2[i] > 0.7:
                ask_correction[j] = fuzzy_str[i]
                if fuzzy_ratio2[i] > fuzzy_ratio[i]:
                    ask_correction[j] = fuzzy_str2[i]
        else:
           if fuzzy_ratio[i] <= 0.7:
                ask_correction[j] = ask_array[i]
           else:
                ask_correction[j] = fuzzy_str[i]
        i = i + 1
        j = j + 1
    
    #print ask_correction              
    s = ''
    for key, value in ask_correction.iteritems():
        s = s + value + ' '
    #print s
    return s


   def spell_correctness2(self, ask, dictionary):
    final_candidate_str = []
    final_candidate_ratio = []

    for word in ask.split(' '):
        candidate_str = []
        candidate_ratio = []
        for dict in dictionary:
           if word in dict:
               candidate_str.append(str(dict))
               candidate_ratio.append(Levenshtein.ratio(word, str(dict)))
        #print "1 ",candidate_str
        #print "1 ",candidate_ratio
        
        temp_candidate_str = candidate_str
        temp_candidate_ratio = candidate_ratio
        candidate_str = []
        candidate_ratio = []
        i = 0
        for item in temp_candidate_str:
            if (word + " ") in item or (" " + word) in item:
                candidate_str.append(item)
                candidate_ratio.append(temp_candidate_ratio[i])
            i = i + 1
    
        #print "2 ",candidate_str
        #print "2 ",candidate_ratio
        
        if len(candidate_str) == 1:
            final_candidate_str.append(candidate_str[0])
            final_candidate_ratio.append(candidate_ratio[0])
        elif len(candidate_str) > 1:
            x = 0
            j = 0
            i = 0
            for item in candidate_str:
                if x < candidate_ratio[i]:
                    x = candidate_ratio[i]
                    j = i
                i = i + 1
            final_candidate_str.append(candidate_str[j])
            final_candidate_ratio.append(candidate_ratio[j])            
        elif len(candidate_str) == 0:
            if len(word) > 3 and len(temp_candidate_str) > 0:
                x = 0
                j = 0
                i = 0
                for item in temp_candidate_str:
                    if x < temp_candidate_ratio[i]:
                        x = temp_candidate_ratio[i]
                        j = i
                    i = i + 1
                final_candidate_str.append(temp_candidate_str[j])
                final_candidate_ratio.append(temp_candidate_ratio[j])
            else:
                final_candidate_str.append(word)
                final_candidate_ratio.append(0)
                         
    #print ">>",final_candidate_str
    #print ">>",final_candidate_ratio

    
    s = ''
    x = ''
    for item in final_candidate_str:
        if x != item:
            s = s + item + ' '
        x = item
    return s
   
   
   
