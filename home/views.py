from django.shortcuts import render
from product.models import (
    product_details,
    product_img,
    )
from django.db.models import Q
from .home_extra_functions import *
from .models import (
    user_feedback,
    feedback_without_email,
    feedback_with_email,
)


# Things in which you can search -
# Title, description, category, conditions, 
# 

# Filters - Distance form you, type,  
# - 


def index(request):
    user=request.user
    products_list = get_all_the_products_list(request, user)
    
    profile_imgs = get_all_the_products_list_profile_img(request, products_list)
        
    products = zip(products_list, profile_imgs)
    
    navbar = product_category.objects.all()

    context = {
            "products"  : products,
            "navbar"    : navbar,
         }
    template_name = 'index.html'
    return render(request, template_name, context)



'''
def category(request, category):
    
    # get all the products and filter to the category that user want
    user = request.user
    products_list = get_all_the_products_list(request, user)
    products_list = products_list.filter(category__category.id = category)
    # get image of all the products
    imgs = get_all_the_products_list_images(request, products_list)
    products = zip(products_list, imgs)
    
    # get the navBar to show on the page
    navbar = product_category.objects.all()

    context = {
            "products"  : products,
            "navbar"    : navbar,
        }
    template_name = 'index.html'
    return render(request, template_name, context)


'''



def feedback(request):
    
    if not request.method == "POST":
        return redirect(request.META.get('HTTP_REFERER'))

    feedback = request.POST.get("feedback")
    print(feedback)
    if not request.user.is_authenticated :
        email  = request.POST.get("feedback_email")
        if not email:
            feedback = feedback_without_email.objects.create(feedback = feedback)
            feedback.save()
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            feedback = feedback_with_email.objects.create(email = email, feedback = feedback)
            feedback.save()
            return redirect(request.META.get('HTTP_REFERER'))

    else:
        feedback = user_feedback.objects.create(user=request.user, feedback = feedback)
        feedback.save()
        return redirect(request.META.get('HTTP_REFERER'))
