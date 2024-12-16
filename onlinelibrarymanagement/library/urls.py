from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeView,PasswordChangeDoneView
from django.contrib.auth import views as auth_views

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
    path('admin_dashboard/edit_subscriptions/<int:pk>/',views.edit_subscriptions,name='edit_subscriptions'),
    path('subscribe/<int:pk>',views.subscribe,name="subscribe"),
    path('payment/',views.process_payment,name="process_payment"),
    path('upgrade_plan/<int:pk>/',views.upgrade_plan,name="upgrade_plan"),
    # path('process_payment/<int:subscription_id>/', views.process_payment, name='process_payment'),
    path('confirm_subscription/<int:pk>/', views.confirm_subscription, name='confirm_subscription'),
    # path('subscribe/', views.subscribe_plan, name='subscribe_plan'),
    # path('subscribe/<int:pk>/',views.subscribe,name="subscribe")
    path('subscription/',views.subscription_home,name="subscription_home"),
    path('purchase_book/<int:pk>/',views.purchase_book,name="purchase_book"),
    path("notifications/",views.notifications,name="notifications"),
    # path('read_book/<int:book_id>/', views.reading_interface, name='reading_interface'),
    # path('book/<int:book_id>/pdf/', views.serve_pdf, name='serve_pdf'),

    # path('book/<int:book_id>/read/', views.reading_interface, name='reading_interface'),
    path('my_rented_books/', views.rented_books, name='rented_books'),
    # path('book/<int:book_id>/read/', views.save_pdf_as_images, name='serve_pdf'),
    path('book/<int:book_id>/read/', views.reading_interface, name='reading_interface'),
    # path('book/<int:book_id>/read/', views.reading_interface, name='reading_interface'),
    path('edit_profile/',views.edit_profile,name="profile"),
    path("view_user_profile/",views.user_details,name="user_view"),
    path('view_purchase/',views.view_purchased_books,name="purchase"),

    path('wishlist/add/<int:book_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:book_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/', views.view_wishlist, name='wishlist'),
    path('book_view/<int:pk>',views.book_view,name="book_details"),

    path('subscribe_upgrade/<int:pk>/',views.subscribe_upgrade,name='subscribe_upgrade'),
    # path('fetch-upgradeable-plans/', views.fetch_upgradeable_plans, name='fetch_upgradeable_plans'),
    path('purchase_invoice/',views.purchase_invoice,name="purchase_invoice"),

    path('cart/add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/checkout/', views.checkout, name='checkout'),
     path('process-payment/<int:total_amount>/', views.process_payments, name='process_payments'),
    path('accounts/password-change/', auth_views.PasswordChangeView.as_view(),name='password_change'),
    path('accounts/password-change/done',auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path('admin_dashboard/manage_users/',views.user_list, name="admin_manage_user"),
     path('checkout/', views.checkout, name='checkout'),
    
    
    
    # path('notify/',views.notification_view,name="notifications")


]