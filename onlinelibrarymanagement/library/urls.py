from django.urls import path
from . import views

urlpatterns =[
    path('',views.home,name='home_path'),
    path('', views.view_all_books_home, name='view_book_home'),
    path('accounts/login/',views.user_login,name='login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_dashboard/edit_book/<int:pk>',views.edit_books,name = "edit_book"),
    path('accounts/register/',views.register,name='register'),
    path('admin_dashboard/add_book/',views.add_books,name="add_book"),
    path('admin_dashboard/view_book/',views.admin_book_list,name = "admin_book_list"),
    path('admin_dashboard/view_book_details/<int:pk>/',views.view_book_details,name="view_book_details"),
    path('admin_dashboard/delete_book/<int:pk>/', views.delete_book, name='delete_book'),
    path('admin_dashboard/add_author_book/',views.add_authors_from_book,name = "add_author_book"),
    path('admin_dashboard/add_author_admin/',views.add_authors_admin,name="add_author_admin"),
    path('admin_dashboard/edit_author/<int:pk>',views.edit_author,name = "edit_author"),
    path('admin_dashboard/view_authors/',views.view_author,name="view_author"),
    path('admin_dashboard/delete_author/<int:pk>/', views.delete_authors, name='delete_author'),
    path('admin_dashboard/add_category_book/',views.add_categories_from_book,name = "add_category_book"),
    path('admin_dashboard/edit_category/<int:pk>',views.edit_category,name = "edit_category"),
    path('admin_dashboard/view_category/',views.view_category,name="view_category"),
    path('admin_dashboard/delete_category/<int:pk>/', views.delete_category, name='delete_category'),
    path('admin_dashboard/add_category_admin/',views.add_categories_from_admin,name = "add_category_admin"),
    path('admin_dashboard/view_subscriptions/',views.view_subscriptions,name = "view_subscriptions"),
    path('view_book/', views.admin_book_list, name='book_list'),
    path('view_author/', views.author_list, name='admin_list'),
    path('view_categories/', views.category_list, name='category_list'),
    path('rent_book/<int:book_id>/', views.rent_book, name='rent_book'),
    path('rental_success/', views.rental_success, name='rental_success'),
    path('view_subscriptions_plan_user/',views.view_subscriptions_plan_user,name = "view_subscriptions_plans_user"),
    path('logout/',views.custom_logout,name="logout"),
    path('admin_dashboard/edit_subscriptions/<int:pk>/',views.edit_subscriptions,name='edit_subscriptions')

]