
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.dunzo_page, name="dunzo_page"),
    path('search/', views.search_results, name="dunzo search")

]
