import operator
from django.shortcuts import render, redirect
#from django.contrib.sessions.models import Session
from product.models import (
    product_details,
    product_img,
    )
from django.db.models import Q
from .home_extra_functions import *





def index(request):    
    navbar = product_category.objects.all()

    context = {
            "navbar"    : navbar,
         }
    template_name = 'home/index.html'
    return render(request, template_name, context)






def load_index_page_content(request):
    user=request.user
    products_list = get_all_the_products_list(request, user)
    
    if len(products_list) == 0 :
        products = None    
    
    else :
        profile_imgs = get_all_the_products_list_profile_img(request, products_list)
        products = zip(products_list, profile_imgs)

    template_name = 'home/index_page_content.html'
    context = {
            "products"  : products,
         }
    return render(request, template_name, context)


