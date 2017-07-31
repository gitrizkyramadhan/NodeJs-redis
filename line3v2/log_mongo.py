from datetime import datetime
from dbutils import MongoDbUtil

mongo = MongoDbUtil()

class MongoLog(object):

    def conversations(self,  platform, msisdn , question , answer, intent, confidence):

        result = mongo.insert('bni_conversation', {
            "datetime" : datetime.now(),
            "platform" : platform,
            "msisdn" : msisdn,
            "question" : question,
            "answer" : answer,
            "intent" : intent,
            "confidence" : confidence
        })