import googlemaps
import json
from django.conf import settings
from datetime import datetime

class Gmap:
    api_key = settings.GOOGLE_API_KEY
    max_items = 5

    def __init__(self):
        self.gmaps = googlemaps.Client(key=self.api_key)

    def place_nearby(self, loc, key):
        places = []
        count = 0
        ret = self.gmaps.places_nearby(location=loc, rank_by="distance", keyword=key, language='zh-TW')
        for obj in ret['results']:
            name = obj['name']
            try:
                if count == self.max_items:
                    break

                p = {}
                p['name'] = obj['name']
                p['lat'] = obj['geometry']['location']['lat']
                p['lng'] = obj['geometry']['location']['lng']
                l = (obj['geometry']['location']['lat'],obj['geometry']['location']['lng'])
                addrs = self.gmaps.reverse_geocode(l, language='zh-TW')
                p['addr'] = addrs[0]['formatted_address']
                if obj['opening_hours']['open_now'] == True:
                    p['name'] += "(營業中)"
                places.append(p)
                count = count + 1
            except Exception as e:
                print(e)

        return(places)
