import json
import os
import time
#from bs4 import BeautifulSoup
from django.shortcuts import render,redirect
from app.models import Location, CityNames
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import requests

headers = {
    'Host': 'user-search.zepto.co.in',
    'source': 'APP_STORE',
    'x-requested-with': 'XMLHttpRequest',
    'User-Agent': 'zeptoConsumerApp/3 CFNetwork/1399 Darwin/22.1.0',
    'storeid': '1703e30b-0199-4850-b59a-e0b2eb5396a9',
    'systemversion': '16.1',
    'appversion': '22.11.1',
    'compatible_components': 'CONVENIENCE_FEE,RAIN_FEE,EXTERNAL_COUPONS,STANDSTILL,BUNDLE,MULTI_SELLER_ENABLED,PIP_V1,ROLLUPS,SCHEDULED_DELIVERY,SAMPLING_ENABLED',
    'platform': 'ios',
    'Connection': 'keep-alive',
    'Authorization': 'eyJhbGciOiJIUzUxMiJ9.eyJ2ZXJzaW9uIjoxLCJzdWIiOiJjMDQxMjZjZS1jNTljLTRmOTAtYTkxNS0yMTc3YTljZDgyNDAiLCJpYXQiOjE2Njg1Mzc5NzIsImV4cCI6MTY2ODYyNDM3Mn0.bU6C-NAlnPmO3FnT5gWudpTTU9fZp7xX51gab1efY_3yf9TnEX7gGRrAewdgZw_BpYNotL8CRpdkyPfwMwxIPQ',
    'sessionid': '296cc505-359d-4b28-91b1-2163aee68ce0',
    'isinternaluser': 'false',
    'deviceuid': 'C7FC21E2-2D30-410C-8C5D-E4F18B0F1CFB',
    'device_model': 'iPhone 11',
    'Accept-Language': 'en-IN,en-GB;q=0.9,en;q=0.8',
    'access-control-allow-credentials': 'true',
    'Accept': 'application/json',
    'Content-Type': 'application/json; charset=utf-8',
    'Accept-Encoding': 'gzip, deflate, br',
    'device_brand': 'Apple',
    'requestid': '2c7115e3-c0cb-4d9a-a032-6372618efeb8'
    }

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def get_place_id(query):
    autocomplete_url=f'https://api.zepto.co.in/api/v1/maps/place/autocomplete/?place_name={query}&is_location_enabled=false'
    r = requests.get(autocomplete_url,headers=headers)
    jsdata=json.loads(r.text)
    print(r.text)
    return jsdata['predictions'][0]['place_id']
def get_lat_long(placeid):
    autocomplete_url=f'https://api.zepto.co.in/api/v1/maps/place/details/?place_id={placeid}&is_location_enabled=false'
    r = requests.get(autocomplete_url)
    print(r.text)
    jsdata=json.loads(r.text)

    return jsdata['result']['geometry']['viewport']['northeast']['lat'],jsdata['result']['geometry']['viewport']['northeast']['lng']


def zepto_search(search_query,lat,long):
    # store ID
    url_2 = f'https://api.zepto.co.in/api/v1/config/layout/?latitude={lat}&longitude={long}&page_type=HOME&version=v2'
    r= requests.get(url_2,headers=headers)
    print(a:=r.text)
    data = json.loads(a)
    store_id =''
    if data['storeServiceableResponse']['serviceable']:
        store_id= data['storeServiceableResponse']['storeId']
    else:
        return None
    url = 'https://user-search.zepto.co.in/api/v1/search'
    post_data = {
        "algoliaRequest":
        {"query":f"{search_query}",
        "filters":f"storeId: \"{store_id}\" AND (NOT   enabled:false)",
        "enablePersonalization":False,
        "clickAnalytics":True,
        "userToken":"c04126ce-c59c-4f90-a915-2177a9cd8240",
        "ruleContexts":["chennai"],
        "analyticsTags":["chennai"]}
        }
    # print(type(post_data))
    r = requests.post(url=url,headers=headers,json=post_data)
    a=r.text
    # js_data = json.dumps(r.text,indent=4)
    js_data = json.loads(a)
    return js_data
    

@login_required(login_url='/admin')
def zepto_page(request):
    city_names = CityNames.objects.all()
    if request.method == 'GET':
        return render(request,"zepto_index.html",{'city_names':city_names})
    elif request.method == 'POST':
        search_query = str(request.POST.get("search_query"))
        loc_name = request.POST.get("location_name")
        print("Location name",loc_name)
        place_id=get_place_id(str(loc_name))
        lat,long =get_lat_long(place_id)
        print(lat,long)
        search_query =search_query.strip().replace(" ","%20")
        print(search_query)
        js_data = zepto_search(search_query,lat,long)
        print(js_data)
        # loc='C:\\Users\\manpr\\Desktop\\ec2hosting_floder\\scrapped_data\\'
        # with open(loc+'zepto_'+search_query+'.json','w',encoding="utf-8") as f:
        #     f.writelines(json.dumps(js_data,indent=4))
        try:
            n = len(js_data['hits'])
        except:
            return render(request,"zepto_index.html",{'city_names':city_names})
        print(n)
        item_name_data =[]
        brand_data =[]
        weight_data =[]
        price_data =[]
        image_data =[]
        for i in range(n):
            item_name= js_data['hits'][i]['productResponse']['product']['name']
            brand= js_data['hits'][i]['productResponse']['product']['brand']
            weight= js_data['hits'][i]['productResponse']['productVariant']['weightInGms']
            price= js_data['hits'][i]['productResponse']['discountedSellingPrice']
            image= 'https://ik.imagekit.io/jupdt2k6txi/'+js_data['hits'][i]['productResponse']['productVariant']['images'][0]['path']
            item_name_data.append(item_name)
            brand_data.append(brand)
            price_data.append("Rs. " + str(price/100))
            weight_data.append(weight)
            image_data.append(image)
        mylist = zip(item_name_data, brand_data,weight_data,price_data,image_data)
        city_names = CityNames.objects.all()
        context = {
            'mylist': mylist,
            'city_names':city_names
        }


        return render(request,"zepto_results.html",
            context
            )

def search_results(request):
    if is_ajax(request=request):
        game = request.POST.get('game')
        if len(game) < 3:
            return JsonResponse({})
        print(game)
        # qs = Location.objects.filter(area_name__icontains=game)
        # print(qs)
        # if len(qs) > 0 and len(game) > 0:
        #     data = []
        #     for pos in qs:
        #         item = {
        #             'pk':pos.pk,
        #             'address':pos.area_name,
        #             'lat':pos.lat,
        #             'long':pos.long
        #         }
        #         data.append(item)
        #     res = data
        # else:
        #     res = "Not found"
        # return JsonResponse({'data':res})
        import requests

        google_api_key = "AIzaSyBCt_J0srN8BsPDF1Nq_JUEfrmC1v_-lso"
        
        url = f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input={game}&types=geocode&key={google_api_key}"
        js_data = requests.get(url=url).json()
        data = []
        for i in range(len(js_data['predictions'])):
            place_id = js_data['predictions'][i]['place_id']
            place_details_url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=geometry&key={google_api_key}'
            lat_long_data = requests.get(place_details_url).json()
            lat = lat_long_data['result']['geometry']['viewport']['northeast']['lat']
            long = lat_long_data['result']['geometry']['viewport']['northeast']['lng']
            
            item = {
                    'pk':i,
                    'address':js_data['predictions'][i]['description'],
                    'lat':lat,
                    'long':long
                }
            data.append(item)
        return JsonResponse({'data':data})
    return JsonResponse({})
