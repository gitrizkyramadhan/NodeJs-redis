import json
import re
from decimal import Decimal
from parse_log import StructuredLog
from gmaps_geolocation import GMapsGeocoding

gmap = GMapsGeocoding()
slog = StructuredLog()
places = [(2,"Bali"),(4,"Bandar Lampung"),(5,"Bandung"),(9,"Jabodetabek"), (9,"Jakarta")]

class BankingModule():

    def __init__(self):
        print "Banking Module Loaded"

    def mreplace(self, text):

        c = '!@#$%^&*()_+"'
        cs = list(c)
        for a in cs:
            if a in text:
                text = text.replace(a, ' ').strip()
        return text

    # def _getKey(self, value):
    #     # print (value)
    #     if value['detail'] == None:
    #         return 0
    #     else :
    #         # print value['distance']
    #         return Decimal(value['distance'])

    def _getKey(self, value):
        try:
            return Decimal(value[len(value) - 1])
        except:
            return 0

    def getNearestATMLocation(self, latitude, longitude, **params):
        print "Bank :: getNearestATMLocation(%s,%s)" % (latitude,longitude)

        maxLoopCount = params.get("loopCount", 3)

        pLocObj = []
        userLocation = (Decimal(latitude), Decimal(longitude))

        data = slog.parse_simple_data('data/', 'atm_location.csv', separator='|')
        for row in data:
            try:
                longlat = row[7].split(',')
                atmLatLng = (Decimal(longlat[0]), Decimal(longlat[1]))
                row.append(str(gmap.calculateDistance(userLocation, atmLatLng)))
                pLocObj.append(row)
            except:
                continue



        # with open('json-atm.json') as jsonATM:
        #     content = jsonATM.read().splitlines()
        # atmJson = json.loads(content[0])
        # for atmDetail in atmJson :
        #     if atmDetail['detail'] == None:
        #         continue
        #     else :
        #         atmLatLng = (Decimal(atmDetail['detail']['latitude']), Decimal(atmDetail['detail']['longitude']))
        #         atmDetail['distance'] = str(gmap.calculateDistance(userLocation, atmLatLng))
        #         pLocObj.append(atmDetail)

        pLocObj.sort(key=self._getKey)


        count = 0
        resultList = []
        for atm in pLocObj:
            count += 1
            if count > maxLoopCount:
                break
            resultList.append(atm)
        print resultList
        return resultList

    def getNearestBranchLocation(self, latitude, longitude, **params):
        print "Bank :: getNearestBranchLocation(%s,%s)" % (latitude, longitude)

        maxLoopCount = params.get("loopCount", 3)

        pLocObj = []
        userLocation = (Decimal(latitude), Decimal(longitude))

        # with open('json-branch.json') as f:
        #     content = f.read()
        # f.close()
        # decodedJson = json.loads(content)
        # for branch in decodedJson :
        #     if branch['detail'] == None :
        #         continue
        #     print branch
        #     branchLatLng = (Decimal(branch['detail']['latitude']), Decimal(branch['detail']['longitude']))
        #     branch['distance'] = str(gmap.calculateDistance(userLocation, branchLatLng))
        #     pLocObj.append(branch)

        data = slog.parse_simple_data('data/', 'branch_location.csv', separator='|')
        for row in data:
            try:
                longlat = row[2].split(',')
                atmLatLng = (Decimal(longlat[0]), Decimal(longlat[1]))
                row.append(str(gmap.calculateDistance(userLocation, atmLatLng)))
                pLocObj.append(row)
            except:
                continue

        pLocObj.sort(key=self._getKey)

        count = 0
        resultList = []
        for branch in pLocObj :
            count += 1
            if count > maxLoopCount :
                break
            resultList.append(branch)
        print resultList
        return resultList

    def getNearestAgen(self, latitude, longitude, **params):

        print "Bank :: getNearestBranchLocation(%s,%s)" % (latitude, longitude)

        maxLoopCount = params.get("loopCount", 3)

        pLocObj = []
        userLocation = (Decimal(latitude), Decimal(longitude))

        data = slog.parse_simple_data('data/', 'DATA_AGENT_APPROVED__HARIAN_20170701.txt', separator='|')
        for row in data:
            try:
                latitude = self.mreplace(row[20])
                longitude = self.mreplace(row[21])
                atmLatLng = (Decimal(latitude), Decimal(longitude))
                row.append(str(gmap.calculateDistance(userLocation, atmLatLng)))
                pLocObj.append(row)
            except:
                continue

        pLocObj.sort(key=self._getKey)

        count = 0
        resultList = []
        for branch in pLocObj:
            count += 1
            if count > maxLoopCount:
                break
            resultList.append(branch)
        print resultList
        return resultList

    def getNearestPromo(self, **params):
        with open('cimb_promocc.json') as f:
            content = f.read()
        f.close()
        decodedJson = json.loads(content)
        promos = []
        for page in decodedJson['pages'] :
            for result in page['results'] :
                promocc = {}
                found = False
                if (params.has_key("location")):
                    print "LOCATION ==> "+params.get("location").lower()
                    p = re.compile('city=([^&]*)')
                    # print p.findall(page['pageUrl'])[0]
                    for key,value in places :
                        if value.lower() == params.get("location").lower():
                            if (params.has_key("merchant")):
                                print "MERCHANT ==> "+params.get("merchant").lower()
                                promoName = result['FANCYBOX.IFRAME_LINK/_title']
                                if promoName.lower().find(params.get("merchant").lower()) > -1 :
                                    found = True
                            else :
                                found = True
                    if not found :
                        continue;
                elif (params.has_key("merchant")) :
                    print "MERCHANT ==> "+params.get("merchant").lower()
                    promoName = result['FANCYBOX.IFRAME_LINK/_title']
                    if promoName.lower().find(params.get("merchant")) > -1:
                        found = True
                    if not found :
                        continue;
                promocc['name'] = result['FANCYBOX.IFRAME_LINK/_title']
                promocc['description'] = result['PEXTRAINFO_DESCRIPTION']
                promocc['image'] = result['PIMG_IMAGE']
                promocc['detailLink'] = result['FANCYBOX.IFRAME_LINK']
                promocc['sourceLink'] = page['pageUrl']
                promos.append(promocc)
        print json.dumps(promos)
        return promos

    def getProductInfo(self, **params):
        print ""

    def getBranchlessProduct(self, **params):
        print ""

# bank = BankingModule()
# bank.getNearestAgen(-7.99969,112.618605)
# bank.getNearestATMLocation( -7.99969,112.618605)
# bank.getNearestBranchLocation( -7.99969,112.618605)
# bank.getNearestBranchLocation(-8.000188, 112.618191)
# bank.getNearestATMLocation(-6.2501281, 106.5996596)
# cimb.getNearestPromo(location="jakarta")
# cimb.getNearestPromo(merchant="SKAI")
