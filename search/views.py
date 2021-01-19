from django.shortcuts import render,redirect
import operator 
from home.home_extra_functions import *
from product.models import product_available_location,product_category
 
def search(request):
    search      = request.GET.get('search', None)
    if search == "" or search is None:
        return redirect("/")
    
    search  = search.strip()
    
    navbar = product_category.objects.all()

    template_name = "search/search.html"
    context = {
        "search"            : search,
        "navbar"            : navbar,
    }
    return render(request, template_name, context)
    
    
    
    '''
    
    # check for location session
    if not "location" in request.session:
        success_url = "/search"
        context = {
            'success_url': success_url 
        }
        return render(request, "location_session_using_ajax.html", context)


    user = request.user
    products_list = get_all_the_products_list(request, user)


    search      = request.GET.get('search', None)
    if search == "" or search is None:
        return redirect("/")

    category    = request.GET.get('category', None)
    distance    = request.GET.get('distance', None)
    
    search  = search.strip()
    query   = search.split()

    # Perform the Real search
    querySet = []  
    if query:
        for q in query:
            products = products_list.filter(
                    Q(title__icontains= q) |
                    Q(description__icontains = q)
                ).distinct()
        
            for product in products:
                querySet.append(product)
        
    products_list = list(dict.fromkeys(querySet)) # get only the unique values
    
    number_of_products = len(products_list)    

    # get the product distance form user
    user_location = request.session['location']
    all_distance = get_all_the_products_list_distance(request, products_list, user_location)
    
    # get the prodcuts profile image
    profile_img = get_all_the_products_list_profile_img(request, products_list)

    
    products = zip(products_list, profile_img, all_distance)

    # sort the product with distance 
    zipped = list(products)
    products = sorted(zipped, key = operator.itemgetter(2)) 


    # get the navigation bar.
    navbar = product_category.objects.all()

    template_name = "search/search.html"
    context = {
        "products"          : products,
        "search"            : search,
        "number_of_products": number_of_products,
        "navbar"            : navbar,
        "category"          : category,
        "distance"          : distance,
    }
    return render(request, template_name, context)

 '''



 
def all_filter_in_serach(request):
    search                          = request.POST.get('search')
    apply_these_category_filter     = request.POST.get('apply_these_category_filter')
    apply_these_rent_type_filter    = request.POST.get('apply_these_rent_type_filter')
    min_deposit                     = request.POST.get('min_deposit')
    max_deposit                     = request.POST.get('max_deposit')
    sort_by                         = request.POST.get('sort_by')

    list_apply_these_category_filter    = apply_these_category_filter.split(",")
    list_apply_these_rent_type_filter   = apply_these_rent_type_filter.split(",")
    

    user = request.user
    products_list = get_all_the_products_list(request, user)

    search  = search.strip()
    query   = search.split()
    querySet = []  
    # Perform the Real search and deposit filters
    if query:
        for q in query:

            products = products_list.filter(
                    ( Q(title__icontains= q) | Q(description__icontains = q) )
                    ).distinct()

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
            

            for product in products:
                querySet.append(product)               


    products_list = list(dict.fromkeys(querySet)) # get only the unique values

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
    template_name = "search/search_filter_result.html"
    return render(request, template_name, context)
