from geopy.distance import distance as geopy_distance
from django.db.models import Q
#from django.contrib.gis.geoip2 import GeoIP2
#from geopy.distance import geodesic 


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


# distance of user form the product
def get_all_the_products_list_distance(self, products_list, user_location):
    all_distance = []
    user_location = tuple(user_location)
    for product in products_list:
        available_location = product_available_location.objects.get(product = product.id)
        product_location = []
        product_location.append(float(available_location.latitude))
        product_location.append(float(available_location.longitude))
        product_location = tuple(product_location)

        distance = geopy_distance(user_location, product_location)
        distance = round(distance.km)
        all_distance.append(distance)

    return all_distance




def filtered_get_all_the_products_list_distance(self, products_list, user_location, max_distance):
    all_distance = []
    user_location = tuple(user_location)
    for product in products_list:
        available_location = product_available_location.objects.get(product = product.id)
        product_location = []
        product_location.append(float(available_location.latitude))
        product_location.append(float(available_location.longitude))
        product_location = tuple(product_location)

        distance = geopy_distance(user_location, product_location)
        distance = round(distance.km)
        if distance <= max_distance :
            products_list.remove(product)
            continue
        all_distance.append(distance)

    return all_distance



'''

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

'''