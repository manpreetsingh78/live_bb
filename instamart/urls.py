
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.instamart_page, name="instamart_page"),
    path('search/', views.search_results, name="instamart search")

]
