import requests
import json
import urllib

from geopy.distance import vincenty

APIKEY = "AIzaSyBRMZM-OHOO6O2yUE-lrWyG08naIU930S0"
BASEURL = "https://maps.googleapis.com/maps/api/geocode/json"
APIKEY_IMAGES = "AIzaSyBnxagHD6woF7jEVAoK0l4ns6o9edQ8XIk"
BASEURL_IMAGES = "https://maps.googleapis.com/maps/api/staticmap"

class GMapsGeocoding():

    def __init__(self):
        print "Load Google Maps Reverse Geocoding"

    def getLocationDetail(self, latitude, longitude):
        url = BASEURL + "?key=%s" % (APIKEY)
        url = url + "&latlng=%s,%s" % (latitude, longitude)
        print "Request :: %s" % (url)
        r = requests.get(url, headers={})
        decodedJson = json.dumps(r.json())
        decodedJson = json.loads(decodedJson)
        # print "Response :: %s" % (decodedJson)
        # print decodedJson['result'][0]
        if decodedJson['status'] == 'OK':
            return self.__translateGmapData(decodedJson)

    def getLatLng(self, address):
        url = BASEURL + "?key=%s" % (APIKEY)
        # address = address.replace(" ", "+")
        url = url + "&address=%s" % (address)
        print "Request :: %s" % (url)
        r = requests.get(url, headers={})
        decodedJson = json.dumps(r.json())
        decodedJson = json.loads(decodedJson)
        # print "Response :: %s" % (decodedJson)
        # print json.dumps(decodedJson['results'][0])
        if decodedJson['status'] == 'OK':
            return self.__translateGmapData(decodedJson)

    def calculateDistance(self, origin, destination):
        return vincenty(origin, destination).km

    def __translateGmapData(self, decodedJson):
        if decodedJson['status'] == 'OK':
            gmapData = decodedJson['results'][0]
            location = {}
            location['latitude'] = str(gmapData['geometry']['location']['lat'])
            location['longitude'] = str(gmapData['geometry']['location']['lng'])
            for addrObj in gmapData['address_components']:
                for admLevel in addrObj['types']:
                    if admLevel == 'administrative_area_level_4':
                        location['kelurahan'] = addrObj['long_name']
                    if admLevel == 'administrative_area_level_3':
                        location['kecamatan'] = addrObj['long_name']
                    if admLevel == 'administrative_area_level_2':
                        location['kota'] = addrObj['long_name']
                    if admLevel == 'administrative_area_level_1':
                        location['provinsi'] = addrObj['long_name']
            location['formattedAddr'] = gmapData['formatted_address']
            # print location
            return location

    def getImageLocationMap(self, latitude, longitude):
#https://maps.googleapis.com/maps/api/staticmap?center=47.5952,-122.3316&zoom=16&size=640x400&key=AIzaSyBnxagHD6woF7jEVAoK0l4ns6o9edQ8XIk
#https://maps.googleapis.com/maps/api/staticmap?size=640x400&center=-6.183611399999999%2C106.6313069&key=AIzaSyBnxagHD6woF7jEVAoK0l4ns6o9edQ8XIk&zoom=15
        data_param = {}
        data_param['center'] = str(latitude) + ',' + str(longitude)
        data_param['zoom'] = 15
        data_param['size'] = '640x400'
        data_param['key'] = APIKEY_IMAGES
        param_encode = urllib.urlencode(data_param)
        url = BASEURL_IMAGES + '?' + param_encode
        return url







# gmaps = GMapsGeocoding()
# gmaps.getLatLng('graha anabatic')
# data = gmaps.getLatLng('Jakarta')
# print data['latitude']
# data = gmaps.getImageLocationMap('-6.183611399999999','106.6313069')
# print data[:5]
# print gmaps.getLocationDetail(-6.2501281, 106.5996596)