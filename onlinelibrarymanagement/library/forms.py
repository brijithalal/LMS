
from typing import Any
from django import forms
from django.shortcuts import redirect, render
from .models import  Authors, Book, Category, PlanCategory, SubscriptionPlans, User
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
    
class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('ISBN', 'book_title','price','rent_price','description','hide_book','stock_quantity','book_image','content_file','publication_date','author','category')
    
    def __init__(self, *args, **kwargs):
        # Extract session data passed via kwargs
        session_data = kwargs.pop('session_data', {})
        super(AddBookForm, self).__init__(*args, **kwargs)

        # Pre-fill form fields with session data if available
        for field_name, value in session_data.items():
            if field_name in self.fields:
                self.fields[field_name].initial = value
    
    
    
    
    # def clean_book_image(self):
    #     book_image = self.cleaned_data.get('book_image')
    #     if book_image:
    #         if not book_image.name.lower().endswith(('.png','.jpg','.jpeg')):
    #             raise forms.ValidationError('Image must be in PNG, JPG, or JPEG format!') 
    #     return book_image 
    # def clean_book_pdf(self):
    #     book_content = self.cleaned_data.get('content_file')
    #     if book_content:
    #         if not book_content.name.lower().endswith(('.pdf',)):
    #             raise forms.ValidationError('Content must be in  Pdf!') 
    #     return book_content 
class AddAuthorForm(forms.ModelForm):
    class Meta:
        model = Authors   
        fields = ('author_name',)     

# class AddCategoryForm(forms.ModelForm):
#     class Meta:
#         model = Category
#         fields = ('category_name',)


class EditBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('book_title','price','rent_price','hide_book','stock_quantity')

class EditAuthorForm(forms.ModelForm):
    class Meta:
        model = Authors
        fields = ('author_name',)

# class EditCategoryForm(forms.ModelForm):
#     class Meta:
#         model = Category
#         fields = ('category_name',)


class AddCategoryForm(forms.ModelForm):
    plans = forms.ModelMultipleChoiceField(
        queryset=SubscriptionPlans.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Subscription Plans"
    )

    class Meta:
        model = Category
        fields = ['category_name',]

    def save(self, commit=True):
        # Save the category instance
        category = super().save(commit=False)
        if commit:
            category.save()
        # Add selected plans to the PlanCategory table
        if 'plans' in self.cleaned_data:
            selected_plans = self.cleaned_data['plans']
            for plan in selected_plans:
                PlanCategory.objects.create(plan=plan, category=category)
        return category
    

    
class EditCategoryForm(forms.ModelForm):
    plans = forms.ModelMultipleChoiceField(
        queryset=SubscriptionPlans.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Subscription Plans"
    )

    class Meta:
        model = Category
        fields = ['category_name',]

    def save(self, commit=True):
        # Save the category instance
        category = super().save(commit=False)
        if commit:
            category.save()
        # Add selected plans to the PlanCategory table
        if 'plans' in self.cleaned_data:
            selected_plans = self.cleaned_data['plans']

             # Clear existing plans for the category
            category.plans.all().delete()
            for plan in selected_plans:
                PlanCategory.objects.create(plan=plan, category=category)
        return category