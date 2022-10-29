import json
from django.shortcuts import render,redirect
from .models import CityNames,Location, Products, price_weight_location_relation
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def search_button_execution(search_query,lat,long):
    import requests
    from .token_generate import tokengenerate
    token = tokengenerate()
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
    # get_places = f'https://www.bigbasket.com/places/v1/places/autocomplete/?inputText={search_query}&token={token}'

    # r = requests.get(get_places,headers=headers)
    # print(r.text)
    # json_data = r.json()

    # place_id = str(json_data['predictions'][0]['placeId'])
    # desc = str(json_data['predictions'][0]['description'])
    # print(place_id)
    # print(desc)

    # get_lat_long_url = f'https://www.bigbasket.com/places/v1/places/address?placeId={place_id}&token={token}'

    # r = requests.get(get_lat_long_url,headers=headers)

    # json_data = r.json()
    # lat = json_data['lat']
    # long = json_data['lng']
    # print(lat)
    # print(long)

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
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'{cookie}',
        'Host': 'www.bigbasket.com',
        'Referer': 'https://www.bigbasket.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }
    url = f"https://www.bigbasket.com/listing-svc/v2/products?type=ps&slug={search_query}"
    r = requests.get(f'https://www.bigbasket.com/listing-svc/v2/products?type=ps&slug={search_query}&page=1',headers=headers)
    page_data_json = r.json()
    final_data = []
    no_of_pages = int(page_data_json['tabs'][0]['product_info']['number_of_pages'])
    items = int(page_data_json['tabs'][0]['product_info']['total_count'])
    print("Total no. of Pages:- ",no_of_pages)
    for k in range(1,no_of_pages+1):
        print("Scrapping Page:- ",k)
        f = requests.get(url=str(url)+"&page="+str(k),headers=headers)
        final_data.append(f.json())
        # print(data_json)

    # print(r.text)
    return final_data , no_of_pages,items

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
        return render(request,"index.html")
    elif request.method == 'POST':
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
    full_json = {}
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
                exee = {'item_name':item_name,'brand':brand,'category':category,'weight':weight,'price':price,'image':image}
                full_json[i] = {'Blinkit':exee,'Zepto':exee,'Swiggy ':exee,'Instamart':exee,}
        except Exception as e:
            print(e)
    mylist = zip(item_name_data, brand_data,category_data,weight_data,price_data,image_data)
    print(full_json)
    context = {
        'mylist': mylist,
        'items_found':ite,
        'no_of_pages':no
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
        if len(game) < 3:
            return JsonResponse({})
        print(game)
        qs = Location.objects.filter(area_name__icontains=game)
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



