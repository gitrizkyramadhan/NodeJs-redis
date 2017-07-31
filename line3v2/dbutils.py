import MySQLdb
from pymongo import MongoClient
from datetime import datetime, timedelta



class MysqlDbUtil:

    def __init__(self):
        self.MYSQL_HOST = 'localhost'
        self.MYSQL_USER = 'root'
        self.MYSQL_PWD = 'cikapali99'
        self.MYSQL_DB = 'bj_enterprise'

    def request(self, sql):
        try:
            db_connect = MySQLdb.connect(host=self.MYSQL_HOST, port=3306, user=self.MYSQL_USER, passwd=self.MYSQL_PWD, db=self.MYSQL_DB)
            # Create cursor
            cursor = db_connect.cursor()
            cursor.execute(sql)
            sqlout = cursor.fetchall()
            return sqlout
        except MySQLdb.Error, e:
            logDtm = (datetime.now() + timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')
            print e.args
            print "ERROR: %d: %s" % (e.args[0], e.args[1])

    def insert(self, sql):
        try:
            db_connect = MySQLdb.connect(host=self.MYSQL_HOST, port=3306, user=self.MYSQL_USER, passwd=self.MYSQL_PWD, db=self.MYSQL_DB)
            # Create cursor
            cursor = db_connect.cursor()
            cursor.execute(sql)
            db_connect.commit()
        except MySQLdb.Error, e:
            logDtm = (datetime.now() + timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')
            print e.args
            print "ERROR: %d: %s" % (e.args[0], e.args[1])


class MongoDbUtil:

    def __init__(self):
        print "Mongo has been loaded"
        self.client = MongoClient("mongodb://bj_operation:B1sm1ll4h@139.59.96.133/bangjoni")
        self.db = self.client['bangjoni']

    def request(self, collection, type, query):

        if type == "aggregate":
            return list(self.db[collection].aggregate[query])
        elif type == "find":
            return list(self.db[collection].find[query])

    def insert(self, collection, data):

        return self.db[collection].insert_one(data)

