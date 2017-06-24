import googlemaps
import json
import gmap
from datetime import datetime

gmap = gmap.Gmap()
ret = gmap.place_nearby((24.977482, 121.275359),'7-11')

for obj in ret:
    print(obj['name'])