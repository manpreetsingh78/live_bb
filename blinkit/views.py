import json
import os
import time
#from bs4 import BeautifulSoup
from django.shortcuts import render,redirect
from app.models import Location
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def blinkit_search(search_query,lat,long):
    # view-source:https://blinkit.com/v5/search/merchants/30681/products/?lat=12.9715987&lon=77.5945627&q=good%20day&suggestion_type=0&start=0&size=50
    url = f'https://blinkit.com/v5/search/merchants/30681/products/?lat={lat}&lon={long}&q={search_query}&suggestion_type=0&start=0&size=50'
    # from selenium import webdriver
    # import time
    # from selenium.webdriver.firefox.options import Options
    # from selenium.webdriver.common.by import By
    # from selenium.webdriver.firefox.service import Service
    # print("Mark")

    # options =Options()
    # options.add_argument("--headless")

    # options.set_preference('network.proxy.type', 1)
    # options.set_preference('network.proxy.socks', '144.168.217.88')
    # options.set_preference('network.proxy.socks_port', 8780)
    # options.set_preference('network.proxy.socks_remote_dns', False)


    # driver = webdriver.Firefox(service=Service('/home/ec2-user/geckodriver'),options=options)
    # print("Mark")

    # driver.get('https://blinkit.com/')
    # print("Mark")
    # time.sleep(5)
    # driver.get('https://blinkit.com/v5/search/merchants/30681/products/?lat=12.9715987&lon=77.5945627&q=bread&suggestion_type=0&start=0&size=50')
    # print("Mark")
    # elem = driver.find_element(By.XPATH,"/html/body").text
    import cloudscraper

    proxies = {'http': '144.168.217.88:8780', 'https': '144.168.217.88:8780'}

    scraper = cloudscraper.create_scraper(browser={
            'browser': 'firefox',
            'platform': 'android',
            'desktop': True
        },debug=False,delay=15)
    res = scraper.get("https://blinkit.com/",)
    res = scraper.get(url,proxies=proxies)
    elem = res.text
    print("Mark")
    print(elem)
    print("Mark")
    json_data = json.loads(str(elem))
    # json_data = res
    # print(json_data)
    return json_data

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
def blinkit_page(request):
    if request.method == 'GET':
        return render(request,"blinkit_index.html")
    elif request.method == 'POST':
        search_query = str(request.POST.get("search_query"))
    lat = request.POST.get("lat")
    long = request.POST.get("long")
    print(lat)
    print(long)
    search_query =search_query.strip().replace(" ","%20")
    print(search_query)
    js_data = blinkit_search(search_query,lat,long)
    print(js_data)
    no_of_products = len(js_data['products'])
    print(no_of_products)
    item_name_data =[]
    brand_data =[]
    category_data =[]
    weight_data =[]
    price_data =[]
    image_data =[]
    for i in range(no_of_products):
        try:
            item_name = js_data['products'][i]['name']
            image = js_data['products'][i]['image_url']
            weight = js_data['products'][i]['unit']
            price = js_data['products'][i]['attributes']['price']
            brand = js_data['products'][i]['brand_type']
            category = js_data['products'][i]['level0_category'][0]['name']
            item_name_data.append(item_name)
            brand_data.append(brand)
            category_data.append(category)
            price_data.append("Rs. " + str(price))
            weight_data.append(weight)
            image_data.append(image)
        except Exception as e:
            print(e)
    # for data in result_final:
    #     data = json.dumps(data)
    #     result = json.loads(data)
    #     # result = result['tabs'][0]['product_info']['products']
    #     try:

    #         for i in range(24):
    #             item_name = result['tabs'][0]['product_info']['products'][i]['desc']
    #             brand = result['tabs'][0]['product_info']['products'][i]['brand']['name']
    #             category = result['tabs'][0]['product_info']['products'][i]['category']['tlc_name']
    #             weight = result['tabs'][0]['product_info']['products'][i]['w']
    #             price = "Rs." + result['tabs'][0]['product_info']['products'][i]['pricing']['discount']['mrp'] 
    #             image = result['tabs'][0]['product_info']['products'][i]['images'][0]['s']
    #             if len(result['tabs'][0]['product_info']['products'][i]['children']) > 0:
    #                 for k in range(len(result['tabs'][0]['product_info']['products'][i]['children'])):
    #                     weight = weight + " & " + result['tabs'][0]['product_info']['products'][i]['children'][k]['w']
    #                     price = price + " & " + "Rs." +  result['tabs'][0]['product_info']['products'][i]['children'][k]['pricing']['discount']['mrp']


    #             item_name_data.append(item_name)
    #             brand_data.append(brand)
    #             category_data.append(category)
    #             price_data.append(price)
    #             weight_data.append(weight)
    #             image_data.append(image)
    #             exee = {'item_name':item_name,'brand':brand,'category':category,'weight':weight,'price':price,'image':image}
    #             full_json[i] = {'Blinkit':exee,'Zepto':exee,'Swiggy ':exee,'Instamart':exee,}
    #     except Exception as e:
    #         print(e)
    mylist = zip(item_name_data, brand_data,category_data,weight_data,price_data,image_data)
    # print(full_json)
    context = {
        'mylist': mylist
    }


    return render(request,"blinkit_results.html",
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


