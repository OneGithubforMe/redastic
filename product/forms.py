from django import forms
from django.forms import BaseFormSet
from django.contrib.auth import get_user_model
from .models import (
    product_details, 
    product_available_location,
    product_img,
    product_profile_img,
    product_question,
    answer,
)



class product_details_form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(product_details_form, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'maxlength': '140',
            }
        )
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'maxlength': '5000',
                'id'    : 'product_description',
                'placeholder': 'Tell us about the product'
            }
        )
    )

    condition = forms.CharField(
        label = "Terms and Conditons",
        widget=forms.Textarea(
            attrs={
                "required": True,
                'maxlength': '5000',
            }
        )
    )

    class Meta:
        model = product_details
        fields = ['category', 'title', 'description', 'rent_rate', 'rent_type', 'deposit', 'condition']
    
    

    def customSave(self, user):
        my_form = self.save(commit=False)
        my_form.user = user
        my_form.save()
        return my_form
    
    

class RequiredFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False



class product_profile_img_form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(product_profile_img_form, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


    class Meta:
        model = product_profile_img
        fields = ['product_profile_img']

    def customSave(self, prodouct_id):
        my_form = self.save(commit=False)
        my_form.product_id = prodouct_id
        my_form.save()
        return my_form

class product_img_form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(product_img_form, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'



    class Meta:
        model = product_img
        fields = ['product_img']

    def customSave(self, prodouct_id):
        my_form = self.save(commit=False)
        my_form.product_id = prodouct_id
        my_form.save()
        return my_form


class product_available_location_form(forms.ModelForm):
    class Meta:
        model = product_available_location
        fields = ['latitude', 'longitude']

    def customSave(self, prodouct_id):
        my_form = self.save(commit=False)
        my_form.product_id = prodouct_id
        my_form.save()
        return my_form




class product_question_form(forms.ModelForm):
    class Meta:
        model = product_question
        fields = ['question']


class answer_form(forms.ModelForm):
    class Meta:
        model = answer
        fields = ['answer']