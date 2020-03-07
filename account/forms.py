from django import forms
from django.forms import BaseFormSet
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import profile_information

User = get_user_model()

class UserAdminCreationForm(forms.ModelForm):
    # form for creating new users. Include all required fields
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    full_name = forms.CharField(label='Your Name', widget=forms.TextInput)

    class Meta:
        model = User
        fields = ('full_name', 'email')
    
    def clean_password(self):
        password = self.cleaned_data.get("password")
        return password

    def save(self, commit=True):
        # save the provided password in hashed Format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    # A form for updating sers. 

    password  = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password', 'active', 'admin')

    def clean_password(self):
        # regardless of what the user provides, return the initial value
        # this is done here, rather then on the field, because the 
        # field does not have access to the initial value
        return self.initial['password']    
    



#class Login_form(forms.Form):
 #   email = forms.EmailField(label="Email", required=True)
  #  password = forms.PasswordInput(label="Password", required=True)


class full_name_change_form(forms.Form):
    def __init__(self, *args, **kwargs):
        self.obj = kwargs.pop('obj', None)
        super(full_name_change_form, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

   
   
    full_name = forms.CharField(widget=forms.TextInput(
                            attrs= {
                                "placeholder": "+91-",
                                "max_length" : "20",
                                "class"      : "form-control",
                                }),
                        label="Your Name", 
                        required=True,
                        )


class profile_information_form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.obj = kwargs.pop('obj', None)
        super(profile_information_form, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


    phone_number    = forms.CharField(
                        widget=forms.NumberInput(
                            attrs= {
                                "placeholder": "+91-"
                            }
                        ),
                        label="Phone Number", 
                        required=True,
                        # max_length=10,
                        )
    profile_picture = forms.ImageField(label="Profile Picture")
    
    class Meta:
        model = profile_information
        fields = [
            'profile_picture', 
            'phone_number',
            ]

    def clean_phone_number(self, *args, **kwargs):
        phone_number = self.cleaned_data.get("phone_number")
        if not phone_number.isnumeric() or not len(phone_number)==10 :
            print("it's a validation error")
            raise forms.ValidationError("Not a valid phone number")
        return phone_number

    def clean_profile_picture(self, *args, **kwargs):
        data = self.cleaned_data.get('profile_picture')
        if not data:
            data = self.obj.profile_picture
        return data



