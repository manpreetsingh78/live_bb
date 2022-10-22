from django.contrib import admin

from app.models import CityNames,Location,price_weight_location_relation,Products
# Register your models here.

admin.site.register(CityNames)
admin.site.register(Location)
admin.site.register(price_weight_location_relation)
admin.site.register(Products)