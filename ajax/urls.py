from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('set_location_in_session', views.set_location_in_session, name="set_location_in_session"),
    path('get_owner_contact_detail', views.get_owner_contact_detail, name="get_owner_contact_detail"),
    path('feedback', views.feedback, name="user_feedback"),
    path('cart/add_in_session/<int:product_id>', views.add_to_cart_in_session),
    path('cart/view_session_cart', views.view_session_cart),
    path('cart/get_number_of_items_in_cart', views.get_number_of_items_in_cart, name="get_number_of_items_in_cart")
]
