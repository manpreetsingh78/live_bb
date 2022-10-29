
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.blinkit_page, name="blinkit_page"),
    path('search/', views.search_results, name="blinkit search")


]
