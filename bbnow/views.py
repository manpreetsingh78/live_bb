import json
from django.shortcuts import render,redirect
from app.models import Location, LocationCookies, CityNames
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import grequests
import requests

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def search_button_execution(search_query,lat,long):
    import requests
    headers ={
    'authority': 'www.bigbasket.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }
    f = requests.get('https://www.bigbasket.com/',headers=headers)


    cok = f.cookies.items()
    cookie = ''
    for item in cok:
        data = list(item)
        cookie += data[0] + "=" + data[1] + ";"
        if data[0] == '_bb_aid':
            cookie += '_bb_vid' + "=" + data[1] + ";"
    print(cookie)
    headers ={
    'Host': 'www.bigbasket.com',
'X-channel': 'BB-IOS',
'X-Tcp-Platform': 'native',
'X-Entry-Context-Id': '10',
'newrelic': 'ewoiZCI6IHsKImFjIjogIjgzNzMwNCIsCiJhcCI6ICI2NjE2MjAwIiwKImlkIjogIjQzNWY0ZDA5MjJmNzQxMjAiLAoidGkiOiAxNjcwODI5MTY1NjE1LAoidHIiOiAiMWEyMDAwZWY1NzI3NjYzMjMxYjFlMzQ3MzkwYmUzNGQiLAoidHkiOiAiTW9iaWxlIgp9LAoidiI6IFsKMCwKMgpdCn0=',
'traceparent': '00-1a2000ef5727663231b1e347390be34d-435f4d0922f74120-00',
'tracestate': '@nr=0-2-837304-6616200-435f4d0922f74120--0--1670829165615',
'X-Tracker': '7C33D3BA-EFBC-4E15-BF70-899097CD80A4',
'Accept': '*/*',
'x-csurftoken': 'b7j60A.Njc4ODE0Mjc5OA==.1670829101010.w2HYjM/+vOwi39r517G8WEAT38Ohac3t7GF9ds+/0LM=',
'Accept-Language': 'en-IN,en-GB;q=0.9,en;q=0.8',
'Accept-Encoding': 'gzip, deflate, br',
'X-Entry-Context': 'bbnow',
'Content-Type': 'application/json',
'User-Agent': 'BB iOS/v6.4.14/os 16.1',
'Connection': 'keep-alive',
'X-NewRelic-ID': 'XAUAUlZXGwUGVVdQBwE=',
'X-Tcp-Device-Version': 'iOS_6.4.14_3',
    'cookie': f'_bb_source=app;{cookie}',
    }

    f = requests.get(f'https://www.bigbasket.com/skip_explore/?c=1000046&l=0&s=0&n=/',headers=headers)
    cok = f.cookies.items()
    for item in cok:
        data = list(item)
        cookie += data[0] + "=" + data[1] + ";"
        if data[0] == '_bb_aid':
            cookie += '_bb_vid' + "=" + data[1] + ";"
    print(cookie)
    headers = {
        'Host': 'www.bigbasket.com',
'X-channel': 'BB-IOS',
'X-Tcp-Platform': 'native',
'X-Entry-Context-Id': '10',
'newrelic': 'ewoiZCI6IHsKImFjIjogIjgzNzMwNCIsCiJhcCI6ICI2NjE2MjAwIiwKImlkIjogIjQzNWY0ZDA5MjJmNzQxMjAiLAoidGkiOiAxNjcwODI5MTY1NjE1LAoidHIiOiAiMWEyMDAwZWY1NzI3NjYzMjMxYjFlMzQ3MzkwYmUzNGQiLAoidHkiOiAiTW9iaWxlIgp9LAoidiI6IFsKMCwKMgpdCn0=',
'traceparent': '00-1a2000ef5727663231b1e347390be34d-435f4d0922f74120-00',
'tracestate': '@nr=0-2-837304-6616200-435f4d0922f74120--0--1670829165615',
'X-Tracker': '7C33D3BA-EFBC-4E15-BF70-899097CD80A4',
'Accept': '*/*',
'x-csurftoken': 'b7j60A.Njc4ODE0Mjc5OA==.1670829101010.w2HYjM/+vOwi39r517G8WEAT38Ohac3t7GF9ds+/0LM=',
'Accept-Language': 'en-IN,en-GB;q=0.9,en;q=0.8',
'Accept-Encoding': 'gzip, deflate, br',
'X-Entry-Context': 'bbnow',
'Content-Type': 'application/json',
'User-Agent': 'BB iOS/v6.4.14/os 16.1',
'Connection': 'keep-alive',
'X-NewRelic-ID': 'XAUAUlZXGwUGVVdQBwE=',
'X-Tcp-Device-Version': 'iOS_6.4.14_3',
        'Cookie': f'{cookie}'
    }

    set_address_url = 'https://www.bigbasket.com/mapi/v4.1.0/set-current-address/'
    postdata = f'transient=1&src=2&referrer=other&lat={lat}&lng={long}&area=Baner'
    f = requests.post(set_address_url,headers=headers,data=postdata)
    print(f.text)
    cok = f.cookies.items()
    for item in cok:
        data = list(item)
        cookie += data[0] + "=" + data[1] + ";"
        if data[0] == '_bb_aid':
            cookie += '_bb_vid' + "=" + data[1] + ";"
    print(cookie)
    headers = {
        'Host': 'www.bigbasket.com',
'X-channel': 'BB-IOS',
'X-Tcp-Platform': 'native',
'X-Entry-Context-Id': '10',
'newrelic': 'ewoiZCI6IHsKImFjIjogIjgzNzMwNCIsCiJhcCI6ICI2NjE2MjAwIiwKImlkIjogIjQzNWY0ZDA5MjJmNzQxMjAiLAoidGkiOiAxNjcwODI5MTY1NjE1LAoidHIiOiAiMWEyMDAwZWY1NzI3NjYzMjMxYjFlMzQ3MzkwYmUzNGQiLAoidHkiOiAiTW9iaWxlIgp9LAoidiI6IFsKMCwKMgpdCn0=',
'traceparent': '00-1a2000ef5727663231b1e347390be34d-435f4d0922f74120-00',
'tracestate': '@nr=0-2-837304-6616200-435f4d0922f74120--0--1670829165615',
'X-Tracker': '7C33D3BA-EFBC-4E15-BF70-899097CD80A4',
'Accept': '*/*',
'x-csurftoken': 'b7j60A.Njc4ODE0Mjc5OA==.1670829101010.w2HYjM/+vOwi39r517G8WEAT38Ohac3t7GF9ds+/0LM=',
'Accept-Language': 'en-IN,en-GB;q=0.9,en;q=0.8',
'Accept-Encoding': 'gzip, deflate, br',
'X-Entry-Context': 'bbnow',
'Content-Type': 'application/json',
'User-Agent': 'BB iOS/v6.4.14/os 16.1',
'Connection': 'keep-alive',
'X-NewRelic-ID': 'XAUAUlZXGwUGVVdQBwE=',
'X-Tcp-Device-Version': 'iOS_6.4.14_3',
        'Cookie': f'{cookie}'
    }
    url = f"https://www.bigbasket.com/listing-svc/v2/products?type=ps&slug={search_query}"
    r = requests.get(f'https://www.bigbasket.com/listing-svc/v2/products?type=ps&slug={search_query}&page=1',headers=headers)
    page_data_json = r.json()
    final_data = []
    no_of_pages = int(page_data_json['tabs'][0]['product_info']['number_of_pages'])
    items = int(page_data_json['tabs'][0]['product_info']['total_count'])
    print("Total no. of Pages:- ",no_of_pages)
    print(page_data_json['tabs'][0]['product_info']['total_count'])
    for k in range(1,no_of_pages+1):
        print("Scrapping Page:- ",k)
        f = requests.get(url=str(url)+"&page="+str(k),headers=headers)
        final_data.append(f.json())
        # print(data_json)

    # print(r.text)
    return final_data

def home_bkp():
    search_query = str(request.POST.get("search_query"))
    lat = request.POST.get("lat")
    long = request.POST.get("long")
    print(lat)
    print(long)
    search_query =search_query.strip().replace(" ","%20")
    print(search_query)
    result_final , no ,ite = search_button_execution(search_query,lat,long)
    item_name_data =[]
    brand_data =[]
    category_data =[]
    weight_data =[]
    price_data =[]
    image_data =[]
    for data in result_final:
        data = json.dumps(data)
        result = json.loads(data)
        # result = result['tabs'][0]['product_info']['products']
        try:

            for i in range(24):
                item_name = result['tabs'][0]['product_info']['products'][i]['desc']
                brand = result['tabs'][0]['product_info']['products'][i]['brand']['name']
                category = result['tabs'][0]['product_info']['products'][i]['category']['tlc_name']
                weight = result['tabs'][0]['product_info']['products'][i]['w']
                price = "Rs." + result['tabs'][0]['product_info']['products'][i]['pricing']['discount']['mrp'] 
                image = result['tabs'][0]['product_info']['products'][i]['images'][0]['s']
                if len(result['tabs'][0]['product_info']['products'][i]['children']) > 0:
                    for k in range(len(result['tabs'][0]['product_info']['products'][i]['children'])):
                        weight = weight + " & " + result['tabs'][0]['product_info']['products'][i]['children'][k]['w']
                        price = price + " & " + "Rs." +  result['tabs'][0]['product_info']['products'][i]['children'][k]['pricing']['discount']['mrp']


                item_name_data.append(item_name)
                brand_data.append(brand)
                category_data.append(category)
                price_data.append(price)
                weight_data.append(weight)
                image_data.append(image)
        except Exception as e:
            print(e)
    mylist = zip(item_name_data, brand_data,category_data,weight_data,price_data,image_data)
    context = {
        'mylist': mylist,
        'items_found':ite,
        'no_of_pages':no
    }


    return render(request,"results.html",
        context
        )

@login_required(login_url='/admin')
def bbnow(request):
    if request.method == 'GET':
        city_names = CityNames.objects.all()
        return render(request,"bbnow_index.html",{'city_names':city_names})
    elif request.method == 'POST':
        search_query = str(request.POST.get("search_query"))
        lat = request.POST.get("lat")
        long = request.POST.get("long")
        print(lat)
        print(long)
        city_names = CityNames.objects.all()
        
        search_query =search_query.strip().replace(" ","%20")
        print(search_query)
        result_final = search_button_execution(search_query,lat,long)
        # loc='C:\\Users\\manpr\\Desktop\\ec2hosting_floder\\scrapped_data\\'
        # with open(loc+'bigbasket_'+search_query+'.json','w',encoding="utf-8") as f:
        #     f.writelines(json.dumps(result_final,indent=4))

        item_name_data =[]
        brand_data =[]
        category_data =[]
        weight_data =[]
        price_data =[]
        image_data =[]
        for data in result_final:
            data = json.dumps(data)
            result = json.loads(data)
            try:
                for i in range(24):
                    item_name = result['tabs'][0]['product_info']['products'][i]['desc']
                    brand = result['tabs'][0]['product_info']['products'][i]['brand']['name']
                    category = result['tabs'][0]['product_info']['products'][i]['category']['tlc_name']
                    weight = result['tabs'][0]['product_info']['products'][i]['w']
                    price = "Rs." + result['tabs'][0]['product_info']['products'][i]['pricing']['discount']['mrp'] 
                    image = result['tabs'][0]['product_info']['products'][i]['images'][0]['s']
                    if len(result['tabs'][0]['product_info']['products'][i]['children']) > 0:
                        for k in range(len(result['tabs'][0]['product_info']['products'][i]['children'])):
                            weight = weight + " & " + result['tabs'][0]['product_info']['products'][i]['children'][k]['w']
                            price = price + " & " + "Rs." +  result['tabs'][0]['product_info']['products'][i]['children'][k]['pricing']['discount']['mrp']


                    item_name_data.append(item_name)
                    brand_data.append(brand)
                    category_data.append(category)
                    price_data.append(price)
                    weight_data.append(weight)
                    image_data.append(image)
            except Exception as e:
                print(e)
        mylist = zip(item_name_data, brand_data,category_data,weight_data,price_data,image_data)
        context = {
            'mylist': mylist,
            'city_names':city_names
        }


        return render(request,"bbnow_results.html",
            context
            )


def search_results(request):
    if is_ajax(request=request):
        game = request.POST.get('game')
        city_id_post = request.POST.get('city_id')
        city_obj = CityNames.objects.get(city_id=city_id_post)
        print("city_id->>>>>>",city_id_post)
        if len(game) < 3:
            return JsonResponse({})
        print(game)
        qs = Location.objects.filter(area_name__icontains=game,city_id=city_obj)
        print(qs)
        if len(qs) > 0 and len(game) > 0:
            data = []
            for pos in qs:
                item = {
                    'pk':pos.pk,
                    'address':pos.area_name,
                    'lat':pos.lat,
                    'long':pos.long
                }
                data.append(item)
            res = data
        else:
            res = "Not found"
        return JsonResponse({'data':res})
    return JsonResponse({})




