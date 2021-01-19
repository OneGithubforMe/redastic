from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import cart
from product.models import (
    product_details,
    product_profile_img,
)


def view_cart(request):
    if not request.user.is_authenticated: 
        return redirect("/ajax/cart/view_session_cart")


    cart_obj = cart.objects.filter(user = request.user)

    if not cart_obj:
    # in case when cart is empty
        template_name = "cart/cart_view.html"
        context = {
            "products": cart_obj,
            }
        return render(request, template_name, context)    

    # in case cart is not empty
    products = []
    imgs = []
        
    for obj in cart_obj:
        product     = product_details.objects.get(id = obj.product.id)    
        profile_img = product_profile_img.objects.get(product = product.id)
        products.append(product)
        imgs.append(profile_img)

    products = zip(products, imgs)
    template_name = "cart/cart_view.html"
    context = {
        "products": products,
        }
    return render(request, template_name, context)




@login_required(login_url='/account/login/')
def add_in_cart(request, product_id):
    response = {}
    # only when user is login
    try :               
        criterion1 = Q(user=request.user)
        criterion2 = Q(product = product_id)
        cart.objects.get(criterion1 & criterion2)
        
        response["data"] = 'Aleardy in Cart' 
        return JsonResponse(response)
    except:
        # you can't add your own prodcut in cart as well as for buy_now
        product = product_details.objects.get(id = product_id)
        
    if product.user == request.user:
        response["data"] = "you can't add your own product in your cart"
        return JsonResponse(response)

    cart.objects.create(user = request.user, product = product)
    response["data"] = "Added in cart"
    return JsonResponse(response)





def remove_from_cart(request, product_id):

    # in case user want to remove from session_cart
    if not request.user.is_authenticated:
        session_cart = request.session["cart"]
        if product_id in session_cart:
            session_cart.remove(product_id)
            request.session["cart"] = session_cart
            if not session_cart :
                del request.session["cart"]

            return redirect(request.META.get('HTTP_REFERER'))


    # Remove from the user cart
    try :
        criterion1 = Q(user=request.user)
        criterion2 = Q(product = product_id)
        cart_obj = cart.objects.get(criterion1 & criterion2)
        cart_obj.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    except :
        return redirect(request.META.get('HTTP_REFERER'))