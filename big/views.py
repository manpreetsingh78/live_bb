import json
import time
#from bs4 import BeautifulSoup
from django.shortcuts import render,redirect
from app.models import Location
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required


def homepage(request):
    return HttpResponse('''
    <h2><a href="bigbasket/">Bigbasket</a></h2>
    <h2><a href="blinkit/">Blinkit</a></h2>
    <h2><a href="instamart/">Instamart</a></h2>
    <h2><a href="zepto/">Zepto</a></h2>
    <h2><a href="dunzo/">Dunzo</a></h2>
    <h2><a href="bbnow/">BBnow</a></h2>
    ''')
