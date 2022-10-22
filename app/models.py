from enum import unique
from django.db.models import Model as Base
from django.db import models

#4

class CityNames(Base):
    id = models.BigAutoField(primary_key=True)
    city_name = models.CharField(null=True,max_length=255,unique=True)
    city_id = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return f"id={self.id}, City name={self.city_name}"


class Products(Base):
    id = models.AutoField(primary_key=True)
    item_name = models.TextField(max_length=255,blank=False,null=False,unique=True)
    brand_name = models.TextField(null=True,blank=True)
    image = models.TextField(null=True,blank=True)
    base_category = models.TextField(null=True,blank=True)
    sub_category = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self) -> str:
        return f"id={self.id}, name={self.item_name}, brand_name={self.brand_name}"

class Location(Base):
    id = models.AutoField(primary_key=True)
    city_id = models.ForeignKey(CityNames,on_delete=models.CASCADE)
    area_name = models.TextField(unique=True, max_length=255)
    lat = models.TextField(null=True,blank=True)
    long = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self) -> str:
        return f"id={self.id}, city_id={self.city_id}, area_name={self.area_name}"



# class products_to_location_map(Base):
#     id = models.AutoField(primary_key=True)
#     product_id = models.ForeignKey(Products,on_delete = models.CASCADE)
#     location_id = models.ForeignKey(Location,on_delete = models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self) -> str:
#         return f"id={self.id}, product_id={self.product_id}, location_id={self.location_id}"


class price_weight_location_relation(Base):
    id = models.AutoField(primary_key=True)
    price = models.TextField(null=True,blank=True)
    weight = models.TextField(null=True,blank=True)
    product_id = models.ForeignKey(Products,on_delete = models.CASCADE,default=None)
    location_map_id = models.ForeignKey(Location,on_delete = models.CASCADE,default=None)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    
    def __str__(self) -> str:
        return f"id={self.id}, price={self.price}, weight={self.weight}, p_to_l_map={self.location_map_id}"

