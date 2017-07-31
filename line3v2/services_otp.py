from nlp_rivescript import Nlp
from bs4 import BeautifulSoup as Soup
import requests
nlp = Nlp()
url = 'http://128.199.169.4/getOtp'
class Otp:

    def send_otp(self, handphone):
        otp = ""
        template = '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" ' \
                   'xmlns:otp="http://service.bni.co.id/otp"><soapenv:Header/><soapenv:Body><otp:request><otpRequest>' \
                   '<applicationId>GetOTP</applicationId><channelId>MINE</channelId><keyValue>' + handphone +'</keyValue>' \
                   '</otpRequest></otp:request></soapenv:Body></soapenv:Envelope>'
        response = requests.post(url, template)
        response = response.content
        soup = Soup(response, 'lxml')
        for message in soup.find_all('otpresult'):
            otp = message.get_text()
        return otp