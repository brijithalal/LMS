
import re
from typing import Any
from django import forms
from django.shortcuts import redirect, render
from .models import  Authors, Book, Category, PlanCategory, Profile, SubscriptionPlans, User
from django.core.exceptions import ValidationError

class MyLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter Username'}
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Enter Password'}
        )
    )
# class userRegistrationForm(forms.ModelForm):
#     password = forms.CharField(label='password',widget=forms.PasswordInput)
#     password2 = forms.CharField(label='confirm password',widget=forms.PasswordInput)
#     # date_of_birth = forms.DateField(label='Date of Birth',widget=forms.DateInput)
#     date_of_birth = forms.DateField(
#         label='Date of Birth',
#         widget=forms.DateInput(attrs={'type': 'date'})
#     )
    
#     phone = forms.CharField(label='Phone Number',widget=forms.TextInput)
#     address = forms.CharField(label='Address',widget=forms.Textarea)

#     #since inheritance from ModelFormw
#     #i can use the model to declare the fields
#     class Meta:
#         model = User
#         #fields in the builtin Model User
#         fields = ('username', 'first_name','last_name','email','password')

#     #overriding a inbuilt method to  check the 
#     #password  = confirm password
#     #clean_<fieldname>
#     def clean_password2(self):
#         cd = self.cleaned_data
#         if cd['password']!=cd['password2']:
#             raise forms.ValidationError('password does not make correct')
#         return cd['password2']
    
    


class userRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        min_length=8,  # Ensuring password is at least 8 characters
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Date of Birth'}),
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}),
        min_length=10,  # Ensuring phone number has at least 10 digits
        max_length=15,  # Maximum phone number length
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Address', 'rows': 3}),
        max_length=255,  # Limit address to 255 characters
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        password = cd.get('password')
        password2 = cd.get('password2')

        if password != password2:
            raise ValidationError('Passwords do not match')
        # Additional password strength check: at least one digit, one lowercase, one uppercase letter
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[A-Z]).{8,}$', password):
            raise ValidationError('Password must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, and one number.')
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Check if the email is already in use
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email is already registered.')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Check if the phone number is valid (must be numeric and match a length)
        if not phone.isdigit():
            raise ValidationError('Phone number must only contain digits.')
        if len(phone) < 10 or len(phone) > 15:
            raise ValidationError('Phone number must be between 10 and 15 digits.')
        return phone

    def clean_address(self):
        address = self.cleaned_data.get('address')
        # Address length validation (optional)
        if len(address) > 255:
            raise ValidationError('Address cannot be longer than 255 characters.')
        return address

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        # Optional: Ensure the user is at least 18 years old
        from datetime import date
        age = (date.today() - date_of_birth).days // 365
        if age < 18:
            raise ValidationError('You must be at least 18 years old to register.')
        return date_of_birth

    def clean(self):
        cleaned_data = super().clean()
        # Additional overall validation (if needed)
        return cleaned_data
# class AddBookForm(forms.ModelForm):
#     class Meta:
#         model = Book
#         fields = ('ISBN', 'book_title','price','rent_price','description','hide_book','stock_quantity','book_image','content_file','publication_date','author','category')
    
#     def __init__(self, *args, **kwargs):
#         # Extract session data passed via kwargs
#         session_data = kwargs.pop('session_data', {})
#         super(AddBookForm, self).__init__(*args, **kwargs)

#         # Pre-fill form fields with session data if available
#         for field_name, value in session_data.items():
#             if field_name in self.fields:
#                 self.fields[field_name].initial = value


class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('ISBN', 'book_title', 'price', 'rent_price', 'description', 
                  'hide_book', 'stock_quantity', 'book_image', 'content_file', 
                  'publication_date', 'author', 'category')
        widgets = {
            'ISBN': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter ISBN'
            }),
            'book_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price'
            }),
            'rent_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter rent price'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book description',
                'rows': 3
            }),
            'hide_book': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'stock_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter stock quantity'
            }),
            'book_image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'content_file': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'publication_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'author': forms.Select(attrs={
                'class': 'form-select'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def __init__(self, *args, **kwargs):
        # Extract session data passed via kwargs
        session_data = kwargs.pop('session_data', {})
        super(AddBookForm, self).__init__(*args, **kwargs)

        # Pre-fill form fields with session data if available
        for field_name, value in session_data.items():
            if field_name in self.fields:
                self.fields[field_name].initial = value  

        self.fields['author'].empty_label = "Select Author"
        self.fields['category'].empty_label = "Select Category"  
    
    
    
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


# class EditBookForm(forms.ModelForm):
#     class Meta:
#         model = Book
#         fields = ('book_title','price','rent_price','hide_book','stock_quantity')


class EditBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('book_title', 'price', 'rent_price', 'hide_book', 'stock_quantity')
        widgets = {
            'book_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price'
            }),
            'rent_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter rent price'
            }),
            'hide_book': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'stock_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter stock quantity'
            }),
        }

# class EditAuthorForm(forms.ModelForm):
#     class Meta:
#         model = Authors
#         fields = ('author_name',)

class EditAuthorForm(forms.ModelForm):
    class Meta:
        model = Authors
        fields = ('author_name',)
        widgets = {
            'author_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author name'
            }),
        }

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
    

class EditSubscriptionForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Accessible Categories"
    )

    class Meta:
        model = SubscriptionPlans
        fields = ['plan_name', 'price', 'duration']

    def save(self, commit=True):
        # Save the subscription plan instance
        subscription_plan = super().save(commit=False)
        if commit:
            subscription_plan.save()

        # Update the categories in the PlanCategory table
        if 'categories' in self.cleaned_data:
            selected_categories = self.cleaned_data['categories']

            # Clear existing categories for the plan
            subscription_plan.plans.all().delete()
            for category in selected_categories:
                PlanCategory.objects.create(plan=subscription_plan, category=category)

        return subscription_plan



class EditSubscriptionForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label="Accessible Categories"
    )

    class Meta:
        model = SubscriptionPlans
        fields = ['plan_name', 'price', 'duration']
        widgets = {
            'plan_name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        subscription_plan = super().save(commit=False)
        if commit:
            subscription_plan.save()

        if 'categories' in self.cleaned_data:
            selected_categories = self.cleaned_data['categories']
            subscription_plan.plans.all().delete()
            for category in selected_categories:
                PlanCategory.objects.create(plan=subscription_plan, category=category)

        return subscription_plan
    
# class ProfileForm(forms.ModelForm):
#     date_of_birth = forms.DateField(
#         widget=forms.TextInput(attrs={'type': 'date'}),  # HTML5 date picker
#         required=False
#     )

#     class Meta:
#         model = Profile
#         fields = ['phone', 'address', 'date_of_birth']

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email']


class ProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.TextInput(attrs={
            'type': 'date', 
            'class': 'form-control',  # Bootstrap styling
            'placeholder': 'Enter your date of birth'
        }),
        required=False
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone number'
        }),
        required=False
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Enter your address'
        }),
        required=False
    )

    class Meta:
        model = Profile
        fields = ['phone', 'address', 'date_of_birth']


class UserForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        }),
        required=False
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        }),
        required=False
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        }),
        required=False
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']



from . models import comments,Reviews

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = comments
        fields = ('comment_text',)
        widgets = {
            'comment_text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your comment here...'})
        }

class AddReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ('rating', 'title', 'description')
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Review Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your review here...'})
        }

# class UserEditForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email']
#         widgets = {
#             'first_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'last_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#         }

# class ProfileEditForm(forms.ModelForm):
#     class Meta:
#         model = Profile  # Assuming you have a Profile model for additional fields
#         fields = ['phone']
#         widgets = {
#             'phone': forms.TextInput(attrs={'class': 'form-control'}),
#         }
