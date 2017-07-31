from dbutils import MysqlDbUtil

mysql = MysqlDbUtil()

class UserProfileService():

    def __init__(self):
        print "UserProfileService is loaded"

    def update_profile(self, msisdn, **params):
        sql_select = "SELECT * FROM user_profile WHERE user_id = '"+msisdn+"'"
        row = mysql.request(sql_select)
        if row :
            data = ''
            for key, value in params.iteritems():
                data += str(key) + " = '" + str(value) + "',"

            data = data[:len(data) - 1]
            sql = "UPDATE user_profile SET " + data + " WHERE user_id='"+msisdn+"'"
            print sql
            mysql.insert(sql)
        else :
            for key, value in params.iteritems():
                sql = "INSERT INTO user_profile (user_id,handphone) VALUES ('" + msisdn + "','"+ str(value) +"')"
            print sql
            mysql.insert(sql)


# up = UserProfileService()
# up.update_profile('2ghbdsbfhbdhfbhdbf', handphohne='2093892832938')
