import requests
import json

class RasaConsumer() :

    def __init__(self, confident_level = 0.5, host = '127.0.0.1', port = '5000', ssl = False):
        self.CONFIDENT_LEVEL = confident_level
        self.HOST = host
        self.PORT = port
        self.SSL = ssl

    def query(self, query_text):
        params = {"q":query_text}
        url = self.build_url(self.SSL, self.HOST, self.PORT)
        resp = requests.post(url, json=params)
        print url
        print resp
        content = json.loads(resp.text)
        confident_level = content['intent']['confidence']
        content['confidence'] = float(confident_level) > float(self.CONFIDENT_LEVEL)
        return content

    def build_url(self, ssl, host, port):
        url = ''

        if ssl:
            url = 'https://'
        else:
            url = 'http://'

        url = url + str(host) + ':' + str(port) + '/parse'
        return url


rasa_c = RasaConsumer(confident_level=0.3, host='128.199.169.4', port='5000', ssl=False)
data_rasa = rasa_c.query('tabungan')
print data_rasa