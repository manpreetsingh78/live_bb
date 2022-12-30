import json
from django.shortcuts import render,redirect
from .models import Location, LocationCookies, CityNames
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import grequests
import requests

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def create_cookie(lat,long):
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
    'authority': 'www.bigbasket.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'cookie': f'{cookie}',
    }

    f = requests.get(f'https://www.bigbasket.com/skip_explore/?c=1000046&l=0&s=0&n=/',headers=headers)
    cok = f.cookies.items()
    cookie = ''
    for item in cok:
        data = list(item)
        cookie += data[0] + "=" + data[1] + ";"
        if data[0] == '_bb_aid':
            cookie += '_bb_vid' + "=" + data[1] + ";"
    print(cookie)
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'{cookie}',
        'Host': 'www.bigbasket.com',
        'Referer': 'https://www.bigbasket.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }

    set_address_url = 'https://www.bigbasket.com/mapi/v4.1.0/set-current-address/'
    postdata = f'transient=1&src=2&referrer=other&lat={lat}&lng={long}&area=Baner'
    f = requests.post(set_address_url,headers=headers,data=postdata)
    print(f.text)
    cok = f.cookies.items()
    cookie = ''
    for item in cok:
        data = list(item)
        cookie += data[0] + "=" + data[1] + ";"
        if data[0] == '_bb_aid':
            cookie += '_bb_vid' + "=" + data[1] + ";"
    print(cookie)
    return cookie

def search_button_execution(search_query,lat,long,cookie_expired=False):
    location_id = Location.objects.filter(lat=lat,long=long).first()
    print(location_id)
    location_cookie = LocationCookies.objects.filter(location_id=location_id).exists()
    print("************")
    print(location_cookie)
    print("************")
    if location_cookie is False:
        cookie = create_cookie(lat,long)
        location_cookie = LocationCookies.objects.create(location_id=location_id,cookie=cookie)
    else:
        cookie = LocationCookies.objects.get(location_id=location_id).cookie
    if cookie_expired is True:
        cookie = create_cookie(lat,long)
        location_cookie.cookie = cookie
        location_cookie.save()


    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'{cookie}',
        'Host': 'www.bigbasket.com',
        'Referer': 'https://www.bigbasket.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }
    url = f"https://www.bigbasket.com/listing-svc/v2/products?type=ps&slug={search_query}"
    r = requests.get(f'https://www.bigbasket.com/listing-svc/v2/products?type=ps&slug={search_query}&page=1',headers=headers)
    if r.status_code != 200:
        search_button_execution(search_query,lat,long,cookie_expired=True)
    page_data_json = r.json()
    no_of_pages = int(page_data_json['tabs'][0]['product_info']['number_of_pages'])
    print("Total no. of Pages:- ",no_of_pages)
    # for k in range(1,no_of_pages+1):
    #     print("Scrapping Page:- ",k)
    #     f = requests.get(url=str(url)+"&page="+str(k),headers=headers)
    #     final_data.append(f.json())
    #     # print(data_json)
    urls = []
    for k in range(1,no_of_pages+1):
        print("Scrapping Page:- ",k)
        url=str(url)+"&page="+str(k)
        urls.append(url)

    # print(r.text)
    return urls,cookie

def get_data(urls,head):
    reqs = [grequests.get(link,headers=head) for link in urls]
    resp = grequests.map(reqs)
    return resp


def scrap(resp):
    final_data = []
    for r in resp:
        js_data = r.json()
        print(r.status_code)
        if r.status_code == 200:
            final_data.append(js_data)
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
def homepage(request):
    if request.method == 'GET':
        city_names = CityNames.objects.all()
        return render(request,"index.html",{'city_names':city_names})
    elif request.method == 'POST':
        search_query = str(request.POST.get("search_query"))
        lat = request.POST.get("lat")
        long = request.POST.get("long")
        print(lat)
        print(long)
        city_names = CityNames.objects.all()
        
        search_query =search_query.strip().replace(" ","%20")
        print(search_query)
        urls,cookie = search_button_execution(search_query,lat,long)
        head = {
            'Content-Type': 'application/json',
            'Cookie': f'{cookie}',
            'Host': 'www.bigbasket.com',
            'Referer': 'https://www.bigbasket.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
        }
        getdata = get_data(urls,head)
        result_final = scrap(getdata)
#        loc='C:\\Users\\manpr\\Desktop\\ec2hosting_floder\\scrapped_data\\'
#        with open(loc+'bigbasket_'+search_query+'.json','w',encoding="utf-8") as f:
#            f.writelines(json.dumps(result_final,indent=4))

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


        return render(request,"results.html",
            context
            )
# def homepage(request):
#     if request.method == 'GET':
#         return render(request,"index.html")
#     elif request.method == 'POST':
#         search_query = str(request.POST.get("search_query"))
#         print(search_query)
#         prod_obj = Products.objects.filter(item_name__icontains=search_query)

#         item_name_data =[]
#         brand_data =[]
#         base_category_data =[]
#         sub_category_data =[]
#         weight_data =[]
#         price_data =[]
#         image_data =[]
#         for obj in prod_obj:
#             price_weight = price_weight_location_relation.objects.filter(product_id=obj.id)
#             price_list = ''
#             weight_list = ''
#             for pw in price_weight:
#                 price_list += " Rs " +  str(pw.price)
#                 weight_list += " " +   str(pw.weight)
#             item_name_data.append(obj.item_name)
#             brand_data.append(obj.brand_name)
#             base_category_data.append(obj.base_category)
#             sub_category_data.append(obj.sub_category)
#             price_data.append(price_list)
#             weight_data.append(weight_list)
#             image_data.append(obj.image)

#         if not item_name_data:
#             return render(request,"index.html"
#             )
#         mylist = zip(item_name_data, brand_data,base_category_data,sub_category_data,weight_data,price_data,image_data)
#         context = {
#             'mylist': mylist
#         }


#         return render(request,"results.html",
#             context
#             )



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



def fetch_address_of_city(request,city_id):

    data_address = fetch_address_by_city(city_id)
    print(data_address)
    
    return HttpResponse(f'<p>SuccessFull {data_address}</p>')



