from django.contrib import admin
from django.urls import path
from . import views
from django.views.generic import RedirectView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('product/<int:id>',views.product),
    path('add_to_cart/<int:id>',views.add_to_cart),
    path('register',views.register),
    path('login',views.login),
    path('logout',views.logout),
    path('cart',views.cart),
    path('delete/<int:id>',views.delete_order_item),
# //////////////////////////////////////////////////////////////////
    path('search/', views.search_results, name='search_results'),
# ///////////////////////////////////////////////////////////////////////////////
    path('your_addresses',views.your_addresses),
    path('add_new_address',views.add_new_address),
    path('select_address',views.select_address),
    path('select_payment_method/<int:id>',views.select_payment_method),
    path('review_order',views.review_order),
    path('create_order',views.create_order),
    path('complete_payment',views.complete_payment),
    # ///////////////////////////////////////////////////////////////////////////////#motaz
    path('cancel_order_and_items',views.cancel_order_items),
    path('cancel_order',views.cancel_order),
    path('user_orders',views.user_orders),
    #////////////////////////////////////////////////////////////////////
    path('change-password', views.change_password, name='change_password'),
    path('your_account', views.your_account, name='your_account'),
    path('complete', views.complete),
    path('search_order', views.search_order),
    path('invoice', views.invoice),
    path('delete_address/<int:id>', views.delete_address),
]



