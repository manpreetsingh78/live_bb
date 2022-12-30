
from django.urls import path, include
from bbnow import views
urlpatterns = [
    path('', views.bbnow, name="bbnow_homepage"),
    path('search/', views.search_results, name="bbnow search"),
]
