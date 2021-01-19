from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from geopy.distance import distance as geopy_distance

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from itertools import chain
from django.conf import settings
from django.forms import formset_factory, modelformset_factory
from django.core.files.storage import FileSystemStorage

from .forms import (
    product_details_form,
    product_img_form,
    product_available_location_form,
    RequiredFormSet,
    product_profile_img_form,
    product_question_form,
    answer_form,
)
from .models import (
    product_details,
    product_available_location,
    product_img,
    product_profile_img,
    product_question,
    answer,
)

#from extra_function.for_all_apps import check_for_location_session





@login_required(login_url='/account/login/')
def add_product(request):

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
        
        # required min - zero pictures
        # i = 0
        # for img_form in img_forms:
        #     i = i+1
        #     if (not img_form.is_valid()) and i<=1:
        #         messages.info(request, 'Minimum 2 product-images are required')
        #         return redirect("/product/add")


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
        return redirect("/product/view/"+str(product_id))

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








 
@login_required(login_url='/account/login/')
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




@login_required(login_url='/account/login/')
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
    

 


@login_required(login_url='/account/login/')
def product_edit(request, product_id):
    
    product = get_object_or_404(product_details, id = product_id)
    
    # To make sure that only the owner will delete or change the prodcut
    if not (product.user == request.user):
        raise Http404("You can't change the product")

    # img_formset              = modelformset_factory(product_img, fields=('product_img',), extra=5, max_num=5)
    # img_formset             = formset_factory(product_img_form, extra=5, max_num=5)
    
    available_location  = product_available_location.objects.get(product=product)
    #profile_img         = product_profile_img.objects.get(product = product)
    #imgs                = product_img.objects.filter(product = product)

    details_form             = product_details_form(request.POST or None, instance= product)
    available_location_form  = product_available_location_form(request.POST or None, instance=available_location)
    #img_forms                = img_formset(request.POST or None, request.FILES or None, queryset=product_img.objects.filter(product=product))         
    #img_forms                = img_formset(request.POST or None, request.FILES or None, instance= img)
    #profile_img_form         = product_profile_img_form(request.POST or None, request.FILES or None, instance=profile_img)
    
        
    if all([details_form.is_valid(), available_location_form.is_valid()]):
        details_form.save()
        available_location_form.save()

        messages.info(request, "edit")
        return redirect("/product/view/"+str(product_id))


    context = {
        #'imgs'                  : imgs,
        #'profile_img'           : profile_img,
        'details_form'          : details_form,
        'available_location_form': available_location_form,
        #'media_url'             : settings.MEDIA_URL, 
    }
    template_name = "product/product_edit.html"
    return render(request, template_name, context)






@login_required(login_url='/account/login/')
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
    return redirect('/account/profile')






def product_detail_view(request, product_id):
    # get the product
    try :
        product             = product_details.objects.get(id=product_id)
        imgs                = product_img.objects.filter(product = product.id)
        profile_img         = product_profile_img.objects.get(product= product.id)
        available_location  = product_available_location.objects.get(product= product.id)
    except:
        raise Http404("No Product Exist")

 
    # get all the question and answer for the product
    #question_form = product_question_form()
    all_question_and_answer = []
    one_question_answer = []
    questions_obj   = product_question.objects.filter(product = product.id)
    for question_obj in questions_obj:
        try:
            answer_obj = answer.objects.get(question = question_obj)
        except:
            answer_obj = None

        one_question_answer = [question_obj, answer_obj]
        all_question_and_answer.append(one_question_answer)
        

    context = {
            "product"       : product,
            "imgs"          : imgs,
            "profile_img"   : profile_img,
            "all_question_and_answer" : all_question_and_answer,
    }

    if "location" in request.session:
        # distance of user form the product
        user_location = request.session['location']
        user_location = tuple(user_location)

        product_location = []
        product_location.append(float(available_location.latitude))
        product_location.append(float(available_location.longitude))
        product_location = tuple(product_location)

        distance = geopy_distance(user_location, product_location)
        distance = round(distance.km)
        context["distance"] = distance



    if not request.user == product.user:    
        template_name = "product/product_detail_view.html"

    # when product owner is accessing the product details
    else :  
        number_of_imgs = len(imgs) + 1
        context["number_of_imgs"] = number_of_imgs 
        # if the number_of_imgs is more or equal to 6 then 'add more images' button will not show up.
        template_name = "product/product_owner_detail_view.html"
    return render(request, template_name, context)




@login_required(login_url='/account/login/')
def ask_question(request, product_id):
    if request.method == 'POST':
        question = request.POST.get("question")
        question = question.strip()
        if(question == ""):
            return redirect(request.META.get('HTTP_REFERER'))

        product = product_details.objects.get(id = product_id)
        product_question.objects.create(who_is_asking=request.user, product=product, question =  question)
        return redirect(request.META.get('HTTP_REFERER'))

        #form = product_question_form(request.POST)
        #if form.is_valid():
        #    question = form.cleaned_data["question"]
        #    product = product_details.objects.get(id = product_id)
        #    product_question.objects.create(product=product, question =  question)
        #    return redirect(request.META.get('HTTP_REFERER'))



@login_required(login_url='/account/login/')
def delete_question(request, question_id):
    question = product_question.objects.get(id=question_id)
    if not request.user == question.who_is_asking :
        messages.info(request, "You don't have permission to delete this Question")
        return redirect(request.META.get('HTTP_REFERER'))
    question.delete()
    return redirect(request.META.get('HTTP_REFERER'))



def answer_of_question(request, question_id):
    if request.method == 'POST':
        ans = request.POST.get("answer")
        ans = ans.strip()
        question = product_question.objects.get(id = question_id)
        if(ans == ""):
            return redirect(request.META.get('HTTP_REFERER'))

        try :   
            answer_obj = answer.objects.get(question=question)
            # when user try to change his previous answer
            answer_obj.answer = ans
            answer_obj.save()
        except: # question ans is not not the database so create new data
            answer.objects.create(question=question, answer=ans)

        return redirect(request.META.get('HTTP_REFERER'))

        #form = answer_form(request.POST)
        #if form.is_valid():
        #    answer = form.cleaned_data["answer"]
        #    question = product_question.objects.get(id = question_id)
        #    answer.objects.create(question = question, answer = answer)
        #    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/account/login/')
def delete_answer(request, answer_id):
    answer_obj = answer.objects.get(id=answer_id)
    if not request.user == answer_obj.question.product.user :
        messages.info(request, "You don't have permission to delete this answer")
        return redirect(request.META.get('HTTP_REFERER'))
    answer_obj.delete()
    return redirect(request.META.get('HTTP_REFERER'))





def change_product_img(request, img_id):
    if request.method == 'POST' and request.FILES['product_img']:
        myfile = request.FILES['product_img']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)

        change_img  = product_img.objects.get(id = img_id)
        change_img.product_img = filename
        change_img.save()
        return redirect(request.META.get('HTTP_REFERER'))





def remove_product_img(request, img_id):
    if request.method == 'POST':
        remove_img  = product_img.objects.get(id = img_id)
        remove_img.delete()
        return redirect(request.META.get('HTTP_REFERER'))


def change_product_profile_img(request, img_id):
    if request.method == 'POST' and request.FILES['product_profile_img']:
        myfile = request.FILES['product_profile_img']
        fs = FileSystemStorage()
        filename = fs.save (myfile.name, myfile)

        change_img  = product_profile_img.objects.get(id = img_id)
        change_img.product_profile_img = filename
        change_img.save()
        return redirect(request.META.get('HTTP_REFERER'))


def add_product_img(request, product_id):
    if request.method == 'POST' and request.FILES['add_more_img']:
        myfile = request.FILES['add_more_img']
        fs = FileSystemStorage()
        filename = fs.save (myfile.name, myfile)

        product_img.objects.create(product=product_details.objects.get(id=product_id), product_img = filename)
        return redirect(request.META.get('HTTP_REFERER'))





