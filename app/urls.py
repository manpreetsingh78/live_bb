
from django.urls import path, include
from . import views
from . import scrapping_views
urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('search/', views.search_results, name="search"),

    path('open_area_scrap_page_func/', scrapping_views.open_area_scrap_page_func, name="open_area_scrap_page_func"),
    path('open_area_scrap_page', scrapping_views.open_area_scrap_page, name="open_area_scrap_page"),

    path('open_product_scrap_page_func/', scrapping_views.open_product_scrap_page_func, name="open_product_scrap_page_func"),
    path('open_product_scrap_page', scrapping_views.open_product_scrap_page, name="open_product_scrap_page"),


]
