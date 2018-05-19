from urllib.request import urlopen
import json
from geopy.geocoders import Nominatim
import time
import wikipedia
import csv
import re
from geopy.distance import vincenty

def get_city(city=True):
    getCitiesURL = {}
    getCitiesURL["vk_getCities"] = "https://api.vk.com/method/database.getCities.json?"
    getCitiesURL["country_id"] = "country_id=1" #1 - Russian VK_Api
    getCitiesURL["region_id"] = "region_id=1157049" #1157049 - Republic of Tuva VK_Api
    getCitiesURL["count"] = "count1000"
    getCitiesURL["token"] = "access_token=YOU_TOKEN_VK"
    getCitiesURL["version_vkapi"] = "v=5.52"
    try:
        urlcity = ("&".join(getCitiesURL.values()))
        response = urlopen(urlcity,timeout=1)
        data = response.read()
        city = json.loads(data)
    except Exception as e:
        return {'ERROR': str(e)}
    else:
        return city

def lat_lot():
    geolocator = Nominatim()
    wikipedia.set_lang("ru")
    gorod = get_city()["response"]["items"]
    goroda = []
    for cit in gorod:
        if 'area' in cit.keys():
            cit = cit
        else:
            cit["area"] = "Город"
        namegorod = cit["title"]+", Тыва"
        location = geolocator.geocode(namegorod, timeout=3 )
        if location:
            lat = location.latitude
            lot = location.longitude
            cit["latitude"] = lat
            cit["longitude"] = lot
            newport_ri = (51.705380, 94.444599) #Kyzyl
            cleveland_oh = (lat, lot)
            cit["Kyzyl"] = round(vincenty(newport_ri, cleveland_oh ).kilometers)
        else:
            lat = ""
            lot = ""
            cit["latitude"] = lat
            cit["longitude"] = lot
            cit["Kyzyl"] = ""
        try:
            namegorod = cit["title"] + ", Тыва"
            page = wikipedia.summary(namegorod)
            page = re.sub("\n"," ",page)
            if page:
                cit["info"] = page
            else:
                cit["info"] = ""
        except wikipedia.exceptions.DisambiguationError as e:
            cit["info"] = ""
        except wikipedia.exceptions.PageError as e:
            cit["info"] = ""
        goroda.append(cit)
        print(cit)
    return goroda

def record():
    with open( "d:/AnacodaProgect/gorod_cit.csv", "w", encoding='utf-8' ) as file:
        fieldnames = ['id', 'title', 'area', 'region', 'latitude', 'longitude', 'kyzyl_km', 'info']
        writer = csv.DictWriter( file,  delimiter='¦', fieldnames=fieldnames )
        writer.writeheader()
        for reccit in lat_lot():
            print (reccit)
            print ("ok")
            writer.writerow({'id': reccit["id"], 'title': reccit["title"], 'area': reccit["area"], 'region': reccit["region"], 'latitude': reccit["latitude"], 'longitude': reccit["longitude"], 'kyzyl_km': reccit["Kyzyl"],'info': reccit["info"]})

record()
