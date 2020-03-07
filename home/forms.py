from django import forms
from django.forms import BaseFormSet
from django.contrib.auth import get_user_model

class feedback(forms.Form):
    name = forms.CharField(
        label = "Terms and Conditons",
        widget=forms.TextInput(
            attrs={
                'maxlength': '100',
                'placeholder': "Your Name",
            }
        ))

    email = forms.EmailField(
        label = "Your Email",
        widget=forms.EmailField(
            attrs={
                'placeholder': "E-mail",
            }
        )
    )

    feedback = forms.CharField(
        label = "Terms and Conditons",
        widget=forms.Textarea(
            attrs={
                "required": True,
                'maxlength': '5000',
            }
        )
    )