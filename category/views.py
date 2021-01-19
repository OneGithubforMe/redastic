from django.shortcuts import render,redirect
import operator
#from django.contrib.sessions.models import Session
from product.models import (
    product_details,
    product_img,
    )
from django.db.models import Q
from home.home_extra_functions import *




def go_to_category(request, category_id):

    # get the navigation bar.
    navbar = product_category.objects.all()

    # to show checked to the current category in category filter section 
    category = product_category.objects.get(id=category_id)
    current_category = category.category

    template_name = "category/category.html"
    context = {
        "navbar"            : navbar,
        "current_category"  : current_category,
    }
    return render(request, template_name, context)
    
    
    '''
    
    # check for location session
    if not "location" in request.session:
        success_url = "/"+str(category_id)
        context = {
            'success_url': success_url 
        }
        return render(request, "location_session_using_ajax.html", context)
    
    user = request.user
    all_products_list = get_all_the_products_list(request, user)

    category_products = all_products_list.filter(Q(category__id__exact = category_id))
        
    number_of_products = len(category_products)    

    # get the product distance form user
    user_location = request.session['location']
    all_distance = get_all_the_products_list_distance(request, category_products, user_location)
    
    # get the prodcuts profile image
    profile_img = get_all_the_products_list_profile_img(request, category_products)

    
    products = zip(category_products, profile_img, all_distance)

    # sort the product with distance 
    zipped = list(products)
    products = sorted(zipped, key = operator.itemgetter(2)) 


    # get the navigation bar.
    navbar = product_category.objects.all()

    # to show checked to the current category in category filter section 
    category = product_category.objects.get(id=category_id)
    current_category = category.category

    template_name = "category/category.html"
    context = {
        "products"          : products,
        "number_of_products": number_of_products,
        "navbar"            : navbar,
        "current_category"  : current_category,
    }
    return render(request, template_name, context)
'''



def all_filter_in_category(request):
    apply_these_category_filter     = request.POST.get('apply_these_category_filter')
    apply_these_rent_type_filter    = request.POST.get('apply_these_rent_type_filter')
    min_deposit                     = request.POST.get('min_deposit')
    max_deposit                     = request.POST.get('max_deposit')
    sort_by                         = request.POST.get('sort_by')

    list_apply_these_category_filter    = apply_these_category_filter.split(",")
    list_apply_these_rent_type_filter   = apply_these_rent_type_filter.split(",")
    

    user = request.user
    products = get_all_the_products_list(request, user)

    if not list_apply_these_rent_type_filter == ['']:
        products = products.filter(
            Q(rent_type__rent_type__in = list_apply_these_rent_type_filter)
        )
    if not list_apply_these_category_filter == ['']:
        products = products.filter(
            Q(category__category__in = list_apply_these_category_filter)
        )
    if not min_deposit == "":
        products = products.filter(
            Q(deposit__gte = int(min_deposit))
        )
    if not max_deposit == "":
        products = products.filter(
            Q(deposit__lte = int(max_deposit))
        )
            
    products_list = list(dict.fromkeys(products)) # get only the unique values

    if sort_by == "Date Published" : # sort by Date Published
        products_list.reverse()
    

    # get the product distance form user
    user_location = request.session['location']
    all_distance = get_all_the_products_list_distance(request, products_list, user_location)
    
    # get the prodcuts profile image
    profile_img = get_all_the_products_list_profile_img(request, products_list)
    
    # zip the product details
    products = zip(products_list, profile_img, all_distance)


    if sort_by == "Near-By First":              # sort the product with distance
        zipped = list(products)
        products = sorted(zipped, key = operator.itemgetter(2)) 


    number_of_products = len(products_list)

    context = {
        "products"          : products,
        "number_of_products": number_of_products,
    }
    template_name = "category/category_filter_result.html"
    return render(request, template_name, context)

