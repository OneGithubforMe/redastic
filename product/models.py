from django.contrib.auth import get_user_model
from django.db import models


class product_category(models.Model):
    category = models.CharField(max_length=100, verbose_name="Category")   # product category


    def __str__(self):
        return self.category

class product_rent_type(models.Model):
    rent_type = models.CharField(max_length=100)

    def __str__(self):
        return self.rent_type

class product_details(models.Model):
    user            = models.ForeignKey(get_user_model(), on_delete=models.CASCADE) # change user -> owner
    category        = models.ForeignKey(product_category, on_delete=models.PROTECT)
    title           = models.CharField(max_length=255)
    description     = models.TextField(verbose_name="Description")
    rent_type       = models.ForeignKey(product_rent_type, on_delete=models.PROTECT)
    rent_rate       = models.IntegerField(verbose_name="Rent")        # we can create other category
    deposit         = models.IntegerField(verbose_name="Deposit", default=0)
    upload_time     = models.DateTimeField(verbose_name='Uploaded at', auto_now_add=True)
    last_edit_time  = models.DateTimeField(verbose_name='Last edit', auto_now=True)
    publish         = models.BooleanField(default=False)   # publish - True or Draft - False
    condition       = models.TextField(verbose_name="Terms and Conditions")
    


    def __str__(self):
        return self.title


class product_profile_img(models.Model):
    product     = models.OneToOneField(product_details, on_delete=models.CASCADE)
    product_profile_img = models.ImageField(upload_to='pics/add_product/product_img', null = False, blank = False, verbose_name='Product Profile Image',)
    
    



class product_img(models.Model):
    product     = models.ForeignKey(product_details, on_delete=models.CASCADE)
    product_img = models.ImageField(upload_to='pics/add_product/product_img', null = False, blank = False, verbose_name='Product Image',)
    
    def __str__(self):
        return self.product.title


class product_available_location(models.Model):
    product     = models.OneToOneField(product_details, on_delete=models.CASCADE)
    latitude    = models.DecimalField(decimal_places =15 ,max_digits=20) 
    longitude   = models.DecimalField(decimal_places =15,max_digits=20) 

    def __str__(self):
        return self.product.title



class product_question(models.Model):
    who_is_asking       = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product             = models.ForeignKey(product_details, on_delete=models.CASCADE)
    question            = models.CharField(max_length=100)
    question_time       = models.DateTimeField(auto_now_add=True)
    last_edit_time      = models.DateTimeField(auto_now=True)
    


class answer(models.Model):
    question        = models.ForeignKey(product_question, on_delete=models.CASCADE)
    answer          = models.CharField(max_length=255)
    answer_time     = models.DateTimeField(auto_now_add=True)
    last_edit_time  = models.DateTimeField(auto_now=True)
    



