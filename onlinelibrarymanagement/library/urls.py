from django.urls import path
from . import views

urlpatterns =[
    path('',views.home,name='home_path'),
    path('accounts/login/',views.user_login,name='login'),
    path('accounts/register/',views.register,name='register')
]