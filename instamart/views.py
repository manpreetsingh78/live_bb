import json
import os
import time
#from bs4 import BeautifulSoup
from django.shortcuts import render,redirect
from app.models import Location, CityNames
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def instamart_search(search_query,lat,long):
    import requests
    headers = {
        'authority': 'www.swiggy.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
    }

    f = requests.get('https://www.swiggy.com/',headers=headers)
    # print(f.status_code)
    cok = f.cookies.items()
    cookie = ''
    for item in cok:
        data = list(item)
        print(data)
        cookie += data[0] + "=" + data[1] + ";"
    # print(cookie)



    headers = {
        'authority': 'www.swiggy.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
    'cookie': f'{cookie}'
    }

    f = requests.get('https://www.swiggy.com/mapi/homepage/getCards?lat=18.5642452&lng=73.7768511',headers=headers)
    print(f.status_code)
    # print(f.json())
    cok = f.cookies.items()
    for item in cok:
        data = list(item)
        print(data)
        cookie += data[0] + "=" + data[1] + ";"
    # print(cookie)
    import urllib.parse
    addres = 'Pune, Maharashtra, India'
    headers = {
        'authority': 'www.swiggy.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
    'cookie': f'{cookie} deliveryAddressId=; lat=s%3A{lat}; lng=s%3A{long}; address=s%3A{urllib.parse.quote_plus(addres)}; userLocation=%7B%22address%22%3A%22{urllib.parse.quote_plus(addres)}%22%2C%22lat%22%3A{lat}%2C%22lng%22%3A{long}%2C%22id%22%3A%22%22%7D;'
    }

    f = requests.get(f'https://www.swiggy.com/api/instamart/search?pageNumber=0&limit=100&query={search_query}&ageConsent=false&pageType=INSTAMART_SEARCH_PAGE&isPreSearchTag=false',headers=headers)
    print(f.status_code)
    json_data = f.json()
    return json_data

@login_required(login_url='/admin')
def instamart_page(request):
    city_names = CityNames.objects.all()
    if request.method == 'GET':
        return render(request,"instamart_index.html",{'city_names':city_names})
    elif request.method == 'POST':
        search_query = str(request.POST.get("search_query"))
        lat = request.POST.get("lat")
        long = request.POST.get("long")
        print(lat)
        print(long)
        search_query =search_query.strip().replace(" ","%20")
        print(search_query)
        json_data = instamart_search(search_query,lat,long)
        print(json_data)
        # loc='C:\\Users\\manpr\\Desktop\\ec2hosting_floder\\scrapped_data\\'
        # with open(loc+'instamart_'+search_query+'.json','w',encoding="utf-8") as f:
        #     f.writelines(json.dumps(json_data,indent=4))
        try:
            no_of_products = int(json_data['data']['totalResults'])
        except:
            return render(request,"instamart_index.html",{'city_names':city_names})
        print(no_of_products)
        item_name_data =[]
        brand_data =[]
        category_data =[]
        weight_data =[]
        price_data =[]
        image_data =[]
        for i in range(no_of_products):
            item_name = json_data['data']['widgets'][0]['data'][i]['product_name_without_brand']
            brand = json_data['data']['widgets'][0]['data'][i]['brand']
            category = json_data['data']['widgets'][0]['data'][i]['variations'][0]['sub_category_type']
            weight = json_data['data']['widgets'][0]['data'][i]['variations'][0]['quantity']
            price = json_data['data']['widgets'][0]['data'][i]['variations'][0]['price']['offer_price']
            image = 'https://res.cloudinary.com/swiggy/image/upload/' + json_data['data']['widgets'][0]['data'][i]['variations'][0]['images'][0]
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


    return render(request,"instamart_results.html",
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


