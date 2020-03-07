from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import cart
from product.models import (
    product_details,
    product_profile_img,
)


@login_required
def view_cart(request):
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


def add_in_cart(request, product_id):
    # when user is not loogged in
    if not request.user.is_authenticated:
        messages.info(request, "You have to Login or Resister")
        return redirect("/account/login")

    # only when user is login
    try :               
        criterion1 = Q(user=request.user)
        criterion2 = Q(product = product_id)
        cart.objects.get(criterion1 & criterion2)
        
        messages.info(request, 'Aleardy in cart....')
        return redirect("/")
    except:
        # you can't add your own prodcut in cart as well as for buy_now
        product = product_details.objects.get(id = product_id)
        
    if product.user == request.user:
        messages.info(request, "you can't add your own product in your cart")
        return redirect("/")           

    cart.objects.create(user = request.user, product = product)
    messages.info(request, 'Added in cart')
    return redirect("/")





@login_required
def remove_from_cart(request, product_id):

    try :
        criterion1 = Q(user=request.user)
        criterion2 = Q(product = product_id)
        cart_obj = cart.objects.get(criterion1 & criterion2)
        cart_obj.delete()
        return redirect("/cart/view")
    except :
        return redirect("/cart/view")