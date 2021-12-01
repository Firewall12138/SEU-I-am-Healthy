import hashlib
import json
import urllib

import requests


def get_location(LAT, LON, ak, sk):
    gps_url = '/reverse_geocoding/v3/?ak=' + str(
        ak) + '&output=json&coordtype=wgs84ll&location=' + str(LAT) + ',' + str(LON)
    encodedStr = urllib.parse.quote(gps_url, safe="/:=&?#+!$,;'@()*[]")
    rawStr = encodedStr + str(sk)
    sn = hashlib.md5(urllib.parse.quote_plus(rawStr).encode('utf-8')).hexdigest()
    json_data = json.loads(requests.get('https://api.map.baidu.com' + gps_url + '&sn=' + sn).text)
    if json_data['status'] == 0:
        return True, json_data
    else:
        return False, json_data