
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.zepto_page, name="zepto_page"),
    path('search/', views.search_results, name="zepto search")

]
