
from typing import Any
from django import forms
from django.shortcuts import redirect, render
from .models import  User
from django.core.exceptions import ValidationError

class MyLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
        attrs={'class' : 'form-control',
               'placeholder':'Enter Username'}))

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class':'form-control',
                  'placeholder':'Enter Password' }
        )
    )
class userRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password',widget=forms.PasswordInput)
    #since inheritance from ModelForm
    #i can use the model to declare the fields
    class Meta:
        model = User
        #fields in the builtin Model User
        fields = ('username', 'first_name','email','password')

    #overriding a inbuilt method to  check the 
    #password  = confirm password
    #clean_<fieldname>
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password']!=cd['password2']:
            raise forms.ValidationError('password does not make correct')
        return cd['password2']
    