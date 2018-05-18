from urllib.request import urlopen
import json
from geopy.geocoders import Nominatim
import time
import wikipedia
import csv

access_token = "VK_TOKEN"
count1000 = "count1000"
versionvk = "v=5.52"

def get_city(city=True):
    getCitiesURL = {}
    getCitiesURL["vk_getCities"] = "https://api.vk.com/method/database.getCities.json?"
    getCitiesURL["country_id"] = "country_id=1" #ID Country
    getCitiesURL["region_id"] = "region_id=1157049" #ID Region 1157049 - Tuva Republic
    getCitiesURL["count"] = count1000
    getCitiesURL["token"] = access_token
    getCitiesURL["version_vkapi"] = versionvk
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
        location = geolocator.geocode( cit["title"], timeout=3 )
        if location:
            lat = location.latitude
            lot = location.longitude
            cit["latitude"] = lat
            cit["longitude"] = lot
        else:
            lat = ""
            lot = ""
            cit["latitude"] = lat
            cit["longitude"] = lot
        try:
            page = wikipedia.summary(cit["title"])
            if page:
                cit["info"] = page
            else:
                cit["info"] = ""
        except wikipedia.exceptions.DisambiguationError as e:
            cit["info"] = ""
        except wikipedia.exceptions.PageError as e:
            cit["info"] = ""
        except wikipedia.exceptions.UserWarning as e:
            cit["info"] = ""
        goroda.append(cit)
        print(cit)
    return goroda

def record():
    with open( "d:/AnacodaProgect/gorod_cit.csv", "w", encoding='utf-8' ) as file:
        fieldnames = ['id', 'title', 'area', 'region', 'latitude', 'longitude', 'info']
        writer = csv.DictWriter( file,  delimiter='¦', fieldnames=fieldnames )
        writer.writeheader()
        for reccit in lat_lot():
            print (reccit)
            print ("ok")
            writer.writerow({'id': reccit["id"], 'title': reccit["title"], 'area': reccit["area"], 'region': reccit["region"], 'latitude': reccit["latitude"], 'longitude': reccit["longitude"],'info': reccit["info"]})

record()

