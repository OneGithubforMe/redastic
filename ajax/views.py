from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

#from product.models import product_available_location,product_category
from product.models import *
from account.models import profile_information
from home.models import (
    user_feedback,
    feedback_without_email,
    feedback_with_email,
)




def set_location_in_session(request):
    latitude = request.GET.get('latitude', None)
    longitude = request.GET.get('longitude', None)
    #success_url = request.GET.get('success_url')
    if latitude and longitude:
        location_data = [float(latitude), float(longitude)]
        request.session['location'] = location_data
        expiry_time = 60*60*3              # 3 hours = 60*60*3 sec
        request.session.set_expiry(expiry_time)
    
    #return redirect(success_url)
    #return redirect(request.META.get('HTTP_REFERER'))
    return HttpResponse('')



@login_required(login_url='/account/login/')
def get_owner_contact_detail(request):
    data = {}

    owner_id = request.POST.get('owner')
    User = get_user_model()
    try :
        owner_obj = User.objects.get(pk = owner_id)
        data["email"] = owner_obj.email
        profile_info = profile_information.objects.get(user=owner_obj)
        data["phone_number"] = profile_info.phone_number
    except:
        pass
    return JsonResponse(data)





def feedback(request):
    feedback = request.POST.get("feedback")
    if not request.user.is_authenticated :
        email  = request.POST.get("feedback_email")
        if not email:
            feedback = feedback_without_email.objects.create(feedback = feedback)
            feedback.save()
            return HttpResponse('')
        else:
            feedback = feedback_with_email.objects.create(email = email, feedback = feedback)
            feedback.save()
            return HttpResponse('')

    else:
        feedback = user_feedback.objects.create(user=request.user, feedback = feedback)
        feedback.save()
        return HttpResponse('')
        #return redirect(request.META.get('HTTP_REFERER'))



def add_to_cart_in_session(request, product_id):
    response = {}

    if 'cart' in request.session :
        cart = request.session['cart']
        if not product_id in cart:
            cart.append(product_id)
            request.session['cart'] = cart
            response["data"] = 'Added in Cart'
        else:
            response["data"] = 'Already in Cart'
    else:
        request.session['cart'] = []
        request.session['cart'].append(product_id) 
        response["data"] = 'Added in Cart'

    return JsonResponse(response)




def view_session_cart(request):
    if request.user.is_authenticated:
        redirect("/cart/view_cart")

    # in case when session cart is empty
    if not "cart" in request.session :
        template_name = "cart/cart_view.html"
        context = {
            "products": None,
            }
        return render(request, template_name, context)    

    # in case cart is not empty
    cart = request.session["cart"]
    products = []
    imgs = []
        
    for product_id in cart:
        product     = product_details.objects.get(id = product_id)    
        profile_img = product_profile_img.objects.get(product = product.id)
        products.append(product)
        imgs.append(profile_img)

    products = zip(products, imgs)
    template_name = "cart/cart_view.html"
    context = {
        "products": products,
        }
    return render(request, template_name, context)



def get_number_of_items_in_cart(request):
    response = {}
    if not request.user.is_authenticated:
        session_cart = request.session["cart"]
        response["number_of_items_in_cart"] = len(session_cart)
    else:
        cart_obj = cart.objects.filter(user = request.user)
        response["number_of_items_in_cart"] = len(cart_obj)

    return JsonResponse(response)
    