from django.shortcuts import render
from home.home_extra_functions import *
from product.models import product_available_location,product_category
from geopy.distance import geodesic 


def search(request):
    user = request.user
    products_list = get_all_the_products_list(request, user)

    if request.method == 'GET':
        search      = request.GET.get('search', None)
        category    = request.GET.get('category', None)
        distance    = request.GET.get('distance', None)
        #customer_longitude  = request.GET.get('longitude', 0)
        #customer_latitude   = request.GET.get('latitude', 0)
        search              = search.strip()
        query               = search.split()


    # if search field is empty and user click on 'search' then redirect user to home page
    if search == "" :
        return redirect("/")

    # filter based on the category
    if category is not None:
        products_list = products_list.filter(
            Q(category__category__exact = category)
            )
    

    
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
    

    '''

    # distance filter
    distance_filter_product = []
    all_distance = []
    if distance is not None:
        # use lat-long data for location
        customer_location = (float(customer_latitude), float(customer_longitude))
        for product in products_list:
            product_location = product_available_location.objects.get(product = product)
            owner_location = (product_location.latitude, product_location.longitude)
            customer_distance = geodesic(owner_location, customer_location)
            if customer_distance <= float(distance) :
                distance_filter_product.append(product)
                all_distance.append(customer_distance)

        products_list = distance_filter_product

'''
    # sort or order the products
    number_of_products = len(products_list)    
    profile_img = get_all_the_products_list_profile_img(request, products_list)


# calculate distance for every product
    '''    
    all_distance = []
    customer_location = (float(customer_latitude), float(customer_longitude))

    for product in products_list:
        # use lat-long data for location
        product_location = product_available_location.objects.get(product = product)
        owner_location = (product_location.latitude, product_location.longitude)
        customer_distance = geodesic(owner_location, customer_location)
        all_distance.append(customer_distance)
        
    products = zip(products_list, imgs, all_distance)
    
    '''
    
    products = zip(products_list, profile_img)

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

 