from django.urls import path
from . import views

urlpatterns =[
    path('',views.home,name='home_path'),
    path('accounts/login/',views.user_login,name='login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('accounts/register/',views.register,name='register'),
    path('logout/',views.custom_logout,name="logout")

]