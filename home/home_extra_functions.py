from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.contrib import messages
from django.db.models import Q
from django.contrib.gis.geoip2 import GeoIP2
from geopy.distance import geodesic 


from product.models import (
    product_details,
    product_img, 
    product_category,
    product_profile_img,
    product_available_location,
    )



def get_all_the_products_list(self, user):
    if not user.is_authenticated:
        products_list = product_details.objects.all().exclude(Q(publish = False))
    else:
        criterion1 = Q(user=user)
        criterion2 = Q(publish = False)
        products_list = product_details.objects.all().exclude(criterion1 | criterion2)
        # Not show the product which are not publish or belongs to The user.

    return products_list




def get_all_the_products_list_images(self, products_list):
    imgs = []
    for product in products_list:
        img         = product_img.objects.filter(product = product.id)
        imgs.append(img)

    return imgs



def get_all_the_products_list_profile_img(self, products_list):
    imgs = []
    for product in products_list:
        img         = product_profile_img.objects.get(product = product.id)
        imgs.append(img)
    return imgs



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    g = GeoIP2(ip)
    return g.city()

     
    
def get_the_distance_between_customer_and_owner(self, products_list, customer_location):
    # customer_location = (float(customer_latitude), float(customer_longitude))
   
    distances = []
    for product in products_list:
        for product in products_list:
            product_location = product_available_location.objects.get(product = product)
            owner_location = (product_location.latitude, product_location.longitude)
            distance = geodesic(owner_location, customer_location)

        distances.append(distance)
    return distances
