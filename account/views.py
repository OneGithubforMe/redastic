from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, auth

from django.http import HttpResponse
from .forms import (
    profile_information_form, 
    full_name_change_form,
)
from .models import profile_information
from django.conf import settings
#from order.models import cart
from django.db.models import Q
from product.models import (
    product_details,
    product_profile_img,
)




def login(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        username = request.POST['email'].lower()
        password = request.POST['password']
        user = auth.authenticate(username = username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request, 'invalid credentials')
            return redirect('/account/login')
    else:    
        return render(request, 'account/login.html')






def register(request):
    if request.user.is_authenticated:
        return redirect("/")
    
    if request.method == 'POST':
        full_name   = request.POST["full_name"].title()
        email       = request.POST['email'].lower()
        password    = request.POST['password']
        agree_terms = request.POST["agree_terms"]
        
        if not agree_terms:
            messages.info(request, 'You Got to Agree terms and conditions to continue')
            return redirect('/account/register')

        full_name = full_name.strip()
        if full_name == "":         # in case someone put fullname = " " or "  Rahul  "
            messages.info(request, 'user must have a name')
            return redirect('/account/register')         #.... How we can keep the data and input it again so that user don't need to put again
        
        User = get_user_model()
        if User.objects.filter(email = email).exists():
            messages.info(request, 'email already exist')
            return redirect('/account/register')
        
        user = User.objects.create_user(email=email, password=password, full_name = full_name)
        user.save()
        messages.info(request, 'User Created successfully')
        return redirect('/account/register')    
            
    else:    
        return render(request, 'account/register.html')





def logout(request):
    auth.logout(request)
    return redirect("/")





@login_required
def profile(request):       # Show the profile Date
    try:
        user_info = profile_information.objects.get(user=request.user)  
    except profile_information.DoesNotExist:
        # if the user information doesn't exist then except will go    
        if request.method == "POST":
            my_form = profile_information_form(request.POST, request.FILES)
            if my_form.is_valid():
                my_form.instance.user = request.user
                my_form.save()
                messages.info(request, 'profile updated')
                return redirect("/")
                    
        my_form = profile_information_form()
        return render(request, 'account/update_profile.html', {"form": my_form})    


    # list of all owned products by user 
    products_list = product_details.objects.filter(user=request.user)
    

    # in case when user don't have any product
    if not products_list:
        products = products_list
        context = {
            "products"  : products,
            'user_info' : user_info, 
        }
        template_name = 'account/profile.html'

        return render(request, template_name, context)


    imgs = []
    for product in products_list:
        img         = product_profile_img.objects.get(product = product.id)
        imgs.append(img)
        
    products = zip(products_list, imgs)

    context = {
            "products"  : products,
            'user_info' : user_info, 
            'media_url' : settings.MEDIA_URL,
        }
    template_name = 'account/profile.html'

    return render(request, template_name, context)




def profile_for_other(request, user_id):
    
    if request.user.id == user_id : 
        return redirect("/account/profile")

    # Profile information for the user to display name and Profile Pic
    User = get_user_model()
    user = User.objects.get(pk = user_id)
    try:
        user_info = profile_information.objects.get(user = user)
    except:
        user_info = None    
    
    # get the public products from the user
    criterion1 = Q(user = user)
    criterion2 = Q(publish = True)
    products_list = product_details.objects.filter(criterion1 | criterion2)

    # profile img for all the owned products by the user
    imgs = []
    for product in products_list:
        img         = product_profile_img.objects.get(product = product.id)
        imgs.append(img)
        
    products = zip(products_list, imgs)
    
    # in case when user don't have any product
    if not products_list:
        products = None

    context = {
            "products"  : products,
            'user'      : user,
            'user_info' : user_info, 
            'media_url' : settings.MEDIA_URL,
        }
    template_name = 'account/profile_for_other.html'
    return render(request, template_name, context)



def edit_profile(request):
    try:
        user_info = profile_information.objects.get(user = request.user)
    except:
        return redirect("account/profile")

    info_form = profile_information_form(request.POST or None,  request.FILES or None, instance = user_info) 
    name_change_form = full_name_change_form(request.POST or None, initial = {"full_name": request.user.full_name})

    if request.method == "POST":
        if(info_form.is_valid() and name_change_form.is_valid()):
            info_form.save()
            
            full_name = name_change_form.cleaned_data["full_name"]

            User = get_user_model()
            user = User.objects.get(pk = request.user.id)
            user.full_name = full_name
            user.save()
            
            return redirect("/account/profile")    


    template_name = 'account/edit_profile.html'
    context = {
        "info_form": info_form,
        "name_change_form" : name_change_form,
    }
    return render(request, template_name, context)