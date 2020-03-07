from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from itertools import chain
from django.conf import settings
from django.forms import formset_factory, modelformset_factory

from .forms import (
    product_details_form,
    product_img_form,
    product_available_location_form,
    RequiredFormSet,
    product_profile_img_form,
)
from .models import (
    product_details,
    product_available_location,
    product_img,
    product_profile_img,
)







#@login_required
def add_product(request):
    if not request.user.is_authenticated:
        messages.info(request, "You have to login or Sign-up to add a product")
        return redirect("/account/login")


    img_formset = formset_factory(product_img_form, formset=RequiredFormSet, extra=5, max_num = 5)
    
    if request.method == "POST":
        details_form                = product_details_form(request.POST)
        img_forms                   = img_formset(request.POST, request.FILES)
        available_location_form     = product_available_location_form(request.POST)
        profile_img_form            = product_profile_img_form(request.POST, request.FILES)

        if not all([details_form.is_valid(), available_location_form.is_valid(), profile_img_form.is_valid()]):
            if not details_form.is_valid() :
                messages.info(request, "problem in datials")
            if not profile_img_form.is_valid() :
                messages.info(request, "problem in profile img")
            if not available_location_form.is_valid() :
                messages.info(request, "problem in location")
            return redirect("/product/add")    
        
        # required min - one pictures
        i = 0
        for img_form in img_forms:
            i = i+1
            if (not img_form.is_valid()) and i<=1:
                messages.info(request, 'Minimum 2 product-images are required')
                return redirect("/product/add")


        details_form.instance.publish = True
        saved_form = details_form.customSave(request.user)
        product_id = saved_form.pk

        available_location_form.customSave(product_id)  
        profile_img_form.customSave(product_id)

        # add only img_forms which has image in it.
        for img_form in img_forms:
            if not img_form.is_valid():
                continue
            img_form.customSave(product_id)
        
        messages.info(request, 'Product Added SuccessFully')
        return redirect("/")

    details_form             = product_details_form()
    img_forms                = img_formset()
    available_location_form  = product_available_location_form()
    profile_img_form         = product_profile_img_form()
    
    context = {
        'details_form'      : details_form,
        'img_forms'         : img_forms, 
        'available_location_form': available_location_form,
        'profile_img_form'  : profile_img_form,
    }
    return render(request, 'product/product_add.html', context)








 
@login_required         # add a prodcut in draft
def add_product_draft(request):
    img_formset = formset_factory(product_img_form, formset=RequiredFormSet, extra=6, max_num = 6)

    if request.method == "POST":
        details_form             = product_details_form(request.POST)
        img_forms                = img_formset(request.POST, request.FILES)
        available_location_form  = product_available_location_form(request.POST)
        profile_img_form         = product_profile_img_form(request.POST, request.FILES)

        


        if not all([details_form.is_valid(), profile_img_form.is_valid(), available_location_form.is_valid()]):
            messages.info(request, "Try again")
            return redirect("/product/add")    
        
        #check_for_min_two_images_required(request, img_forms)
        # required min - 2 pictures
        i = 0
        for img_form in img_forms:
            if img_form.is_valid():
                i = i+1
        if not i>=1:
            messages.info(request, 'Minimum 2 product-images are required')
            return redirect("/product/add")    
            

        saved_form = details_form.customSave(request.user)
        product_id = saved_form.pk
        
        available_location_form.customSave(product_id)  
        profile_img_form.customSave(product_id)
        
        # add only img_forms which has image in it.
        for img_form in img_forms:
            if img_form.is_valid():
                img_form.customSave(product_id)
        
        messages.info(request, 'Product Added SuccessFully in Draft')
        return redirect("/")
    raise Http404




def change_publish_draft(request, product_id):
    product = get_object_or_404(product_details, pk = product_id)

    # To make sure that only the owner will delete or change the prodcut
    if not (product.user == request.user):
        raise Http404("You can't Delete this product")
    
    if product.publish == True:
        product.publish = False
    else :
        product.publish = True

    product.save()
    return redirect("/account/profile")
    

 


 
@login_required
def product_edit(request, product_id):
    
    product = get_object_or_404(product_details, id = product_id)
    
    # To make sure that only the owner will delete or change the prodcut
    if not (product.user == request.user):
        raise Http404("You can't change the product")

    # img_formset              = modelformset_factory(product_img, fields=('product_img',), extra=5, max_num=5)
    # img_formset             = formset_factory(product_img_form, extra=5, max_num=5)
    
    available_location  = product_available_location.objects.get(product=product)
    profile_img         = product_profile_img.objects.get(product = product)
    imgs                = product_img.objects.filter(product = product)

    details_form             = product_details_form(request.POST or None, instance= product)
    available_location_form  = product_available_location_form(request.POST or None, instance=available_location)
    #img_forms                = img_formset(request.POST or None, request.FILES or None, queryset=product_img.objects.filter(product=product))         
    #img_forms                = img_formset(request.POST or None, request.FILES or None, instance= img)
    #profile_img_form         = product_profile_img_form(request.POST or None, request.FILES or None, instance=profile_img)
    
        
    if all([details_form.is_valid(), available_location_form.is_valid()]):
        details_form.save()
        available_location_form.save()

        messages.info(request, "edit")
        return redirect("/product/edit/"+str(product_id))


    context = {
        'imgs'                  : imgs,
        'profile_img'           : profile_img,
        'details_form'          : details_form,
        'available_location_form': available_location_form,
        'media_url'             : settings.MEDIA_URL, 
    }
    template_name = "product/product_edit.html"
    return render(request, template_name, context)








@login_required
def product_delete(request, product_id):

    # function is in extra functions file
    product = get_object_or_404(product_details, id = product_id)
    
    # To make sure that only the owner will delete or change the prodcut
    if not (product.user == request.user):
        raise Http404("You can't Delete this product")
    
    if request.method == "POST":
        # to confrom that I want to delete this.
        pass

    product.delete()
    messages.info(request, "Sucessfully Deleted")
    return redirect('/')






def product_detail_view(request, product_id):
    try :
        product     = product_details.objects.get(id=product_id)
        imgs        = product_img.objects.filter(product = product.id)
        profile_img = product_profile_img.objects.get(product= product.id)
    except:
        raise Http404("No Product Exist")
    
    context = {
            "product"       : product,
            "imgs"          : imgs,
            "profile_img"   : profile_img,
    }
    if not request.user == product.user:
        template_name = "product/product_detail_view.html"
    else :
        template_name = "product/owner_detail_view.html" 
    return render(request, template_name, context)