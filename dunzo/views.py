import json,requests
import os
import time
#from bs4 import BeautifulSoup
from django.shortcuts import render,redirect
from app.models import Location, CityNames
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def dunzo_search(search_query,lat,long):
    headers={
    'PHONE_MAKE': 'Asus | 25 | 3.57.0.0 | 2071 | gps- 21.48.57 (040800-424705839) : 214857023 | phone_info- ASUS_Z01QD, ASUS_Z01QD, Asus-user 7.1.2 20171130.276299 release-keys, 7.1.2 | ORIGINAL_APP',
    'sessionId': 'c76ca505e3a3881bedbee6e0745ebf40263dafee',
    'appSessionId': 'c76ca505e3a3881bedbee6e0745ebf40263dafee',
    'launchSessionId': '8203cdde879701f30eeb3c2454e8485bdb1329a3',
    'userId': 'c5a07f25-c137-489b-a950-7cabc437eb2f',
    'CLIENT_NAME': 'ANDROID',
    'clientname': 'ANDROID',
    'CLIENT_VERSION': '3.57.0.0',
    'clientversion': '3.57.0.0',
    'deviceId': '0d5c663fdd2b00a2',
    'ipAddress': '172.27.157.72',
    'client_flavour': 'ORIGINAL_APP',
    'Authorization': 'JWT eyJhbGciOiJFUzI1NiIsImtpZCI6ImtleV9pZF8xIiwidHlwIjoiSldUIiwidmVyc2lvbiI6IjEifQ.eyJ0eXBlIjoiIiwicmVzb3VyY2VzIjpudWxsLCJ1c2VyX2lkIjowLCJ1c2VyX3V1aWQiOiJjNWEwN2YyNS1jMTM3LTQ4OWItYTk1MC03Y2FiYzQzN2ViMmYiLCJ1c2VyX3R5cGUiOiJDIiwiZnVsbF9uYW1lIjoiZ3Vlc3QgdXNlciIsInNlc3Npb25faWQiOiIiLCJtZXRhIjp7ImFwcHNfZmx5ZXJfaWQiOiIxNjcwMDcxOTYwMDc4LTE2NTE4MTMwMjk0MjAzMDQyNjEiLCJkZXZpY2VfaWQiOiIwZDVjNjYzZmRkMmIwMGEyIiwiZ3Vlc3RfdXNlciI6dHJ1ZSwiaXNfY2FtcGFpZ25fZWxpZ2libGUiOmZhbHNlLCJwaG9uZV9tYWtlIjoiQXN1cyB8IDI1IHwgMy41Ny4wLjAgfCAyMDcxIHwgZ3BzLSAyMS40OC41NyAoMDQwODAwLTQyNDcwNTgzOSkgOiAyMTQ4NTcwMjMgfCBwaG9uZV9pbmZvLSBBU1VTX1owMVFELCBBU1VTX1owMVFELCBBc3VzLXVzZXIgNy4xLjIgMjAxNzExMzAuMjc2Mjk5IHJlbGVhc2Uta2V5cywgNy4xLjIgfCBPUklHSU5BTF9BUFAiLCJwaG9uZV90eXBlIjoiQSJ9LCJpc3MiOiJkdW56by1hdXRoLXN2YyIsInN1YiI6IjAiLCJleHAiOjE4Mjc4NzI2NDMsImlhdCI6MTY3MDA3MjY0MywianRpIjoiYTYxZGY1M2QtNWRhZS00MDM5LWI5N2UtYzQ1MzYyMTE1ZGM0In0.Azo81DDwar_XbNC9TGA8bCxKi6Ahf7KZw4FVEycHbChVi-YxZ28sapjx2jcBNwuQ9o088DDLoSPKl4JRv6qKrQ',
    'Content-Type': 'application/json; charset=UTF-8',
    'Host': 'apis.dunzo.in',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'okhttp/4.10.0',
    }

    
    search_url= 'https://apis.dunzo.in/api/gateway/proxy/messenger/v8/search/dunzodaily'

    post_data='''{"query":"search_query","subTag":"dunzodaily_load","event":"AUTO","supportedWidgetTypes":["LABEL","STORE_HEADER_GRID_ROW_X","GOOGLE_STORE","ADVERTISEMENT_BANNER","GRID_ROW_X","SEPARATOR"],"queryContext":{"tabType":"ITEM","category":"search"},"location":{"lat":"latitute","lng":"longitute"},"userId":"c5a07f25-c137-489b-a950-7cabc437eb2f","page":1,"size":10,"searchContext":{"placeholder":"Search for an item in Dunzo Daily","context":{"dzid":"782590c3-9949-4efb-a156-0c319e29dc67","landingFrom":"DUNZO_DAILY_PAGE"},"landingPageEnabled":true},"context":{"discountOptions":[{"id":"549a19c011ec42d8973c6edcb260e5d9","type":"SKU_OFFER","text":"Upto 50% off on select products! ","imageUrl":"https://ik.imagekit.io/dunzo/tr:w-$w$,h-$h$/offer_2.png","subtext":"","is_coupon_associated":false},{"id":"3c655bb61d8d49a486120b24c5f63f1e","type":"SKU_OFFER","text":"Upto 50% off on select products! ","imageUrl":"https://ik.imagekit.io/dunzo/tr:w-$w$,h-$h$/offer_2.png","subtext":"","is_coupon_associated":false},{"id":"4e2f7c6277f349818048fa197a201d77","type":"SKU_OFFER","text":"Upto 50% off on select products! ","imageUrl":"https://ik.imagekit.io/dunzo/tr:w-$w$,h-$h$/offer_2.png","subtext":"","is_coupon_associated":false},{"id":"1092494f174d40458646c9ff34620107","type":"SKU_OFFER","text":"Upto 50% off on select products! ","imageUrl":"https://ik.imagekit.io/dunzo/tr:w-$w$,h-$h$/offer_2.png","subtext":"","is_coupon_associated":false},{"id":"4b347ed848ba42c6a7662c7bc3c0f993","type":"SKU_OFFER","text":"Upto 50% off on select products! ","imageUrl":"https://ik.imagekit.io/dunzo/tr:w-$w$,h-$h$/offer_2.png","subtext":"","is_coupon_associated":false},{"id":"01ffcb97946e467ab465dcd1942355ea","type":"SKU_OFFER","text":"Upto 50% off on select products! ","imageUrl":"https://ik.imagekit.io/dunzo/tr:w-$w$,h-$h$/offer_2.png","subtext":"","is_coupon_associated":false},{"id":"66915295b21648179cc6ed5392ca1bb2","type":"SKU_OFFER","text":"Upto 50% off on select products! ","imageUrl":"https://ik.imagekit.io/dunzo/tr:w-$w$,h-$h$/offer_2.png","subtext":"","is_coupon_associated":false},{"id":"b135fb9ddf2342ba84bd198b7a27cda2","type":"SKU_OFFER","text":"Upto 50% off on select products! ","imageUrl":"https://ik.imagekit.io/dunzo/tr:w-$w$,h-$h$/offer_2.png","subtext":"","is_coupon_associated":false},{"id":"28cab36eb9df495d8dafc302ad0f93e4","type":"SKU_OFFER","text":"Upto 50% off on select products! ","imageUrl":"https://ik.imagekit.io/dunzo/tr:w-$w$,h-$h$/offer_2.png","subtext":"","is_coupon_associated":false}],"landingFrom":"DUNZO_DAILY_PAGE","subTag":"GROCERY","iconReferenceId":"","dzid":"782590c3-9949-4efb-a156-0c319e29dc67","exclusiveOfferIds":["549a19c011ec42d8973c6edcb260e5d9","3c655bb61d8d49a486120b24c5f63f1e","4e2f7c6277f349818048fa197a201d77","1092494f174d40458646c9ff34620107","4b347ed848ba42c6a7662c7bc3c0f993","01ffcb97946e467ab465dcd1942355ea","66915295b21648179cc6ed5392ca1bb2","b135fb9ddf2342ba84bd198b7a27cda2","28cab36eb9df495d8dafc302ad0f93e4"]}}'''.replace("search_query",search_query).replace("latitute",str(lat)).replace("longitute",str(long))

    r = requests.post(url=search_url,headers=headers,data=post_data)

    print(r.status_code)
    json_data = r.json()
    return json_data

@login_required(login_url='/admin')
def dunzo_page(request):
    city_names = CityNames.objects.all()
    if request.method == 'GET':
        return render(request,"dunzo_index.html",{'city_names':city_names})
    elif request.method == 'POST':
        search_query = str(request.POST.get("search_query"))
        lat = request.POST.get("lat")
        long = request.POST.get("long")
        print(lat)
        print(long)
        # search_query =search_query.strip().replace(" ","%20")
        print(search_query)
        json_data = dunzo_search(search_query,lat,long)
        print(json_data)
        # loc='C:\\Users\\manpr\\Desktop\\ec2hosting_floder\\scrapped_data\\'
        # with open(loc+'dunzo_'+search_query+'.json','w',encoding="utf-8") as f:
        #     f.writelines(json.dumps(json_data,indent=4))
        try:
            no_of_products = int(json_data['eventMeta']['result_count'])
        except:
            return render(request,"dunzo_index.html",{'city_names':city_names})
        print(no_of_products)
        item_name_data =[]
        brand_data =[]
        category_data =[]
        weight_data =[]
        price_data =[]
        image_data =[]
        for i in range(no_of_products):
            item_name = json_data['widgets'][i]['item']['title']
            brand = json_data['widgets'][i]['item']['brandName']
            category = json_data['widgets'][i]['item']['category']
            image = json_data['widgets'][i]['item']['imageUrl']
            vartiants= len(json_data['widgets'][i]['item']['customizationData']['variantTypes'][0]['variants'])
            print(vartiants)
            for y in range(vartiants):
                price = json_data['widgets'][i]['item']['customizationData']['variantTypes'][0]['variants'][y]['price']
                weight = json_data['widgets'][i]['item']['customizationData']['variantTypes'][0]['variants'][y]['itemQuantityOrWeight']
            
            item_name_data.append(item_name)
            brand_data.append(brand)
            category_data.append(category)
            price_data.append("Rs. " + str(price))
            weight_data.append(weight)
            image_data.append(image)
        mylist = zip(item_name_data, brand_data,category_data,weight_data,price_data,image_data)
        city_names = CityNames.objects.all()
        context = {
            'mylist': mylist,
            'city_names':city_names
        }


        return render(request,"dunzo_results.html",
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
